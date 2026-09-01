#!/usr/bin/env python3
"""Validate and build the NHMesh knowledge base.

    python3 tools/kb.py validate          # check sources, exit 1 on any error
    python3 tools/kb.py build [OUTDIR]    # validate, then emit the publishable payload

The build output is what nginx serves at /guides/ on nhmesh.live: frontmatter
stripped from each guide, plus a generated index.json. Nothing else is emitted.

This runs in CI on every pull request AND again on the web host before anything
is swapped into place, so a merge that skipped CI still cannot publish. Standard
library only, by design: the host must be able to run it with no install step.
"""
import json
import os
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

# KB_ROOT lets a trusted, host-pinned copy of this script validate content it did
# not ship with. The web host runs its own copy against a downloaded tarball and
# never executes tools/ from that tarball — otherwise merging a documentation
# pull request would be remote code execution on the production host.
ROOT = Path(os.environ.get("KB_ROOT") or Path(__file__).resolve().parent.parent).resolve()
GUIDES = ROOT / "guides"
ASSETS = ROOT / "assets"
SECTIONS = ROOT / "sections.json"

REQUIRED_KEYS = ["id", "title", "section", "order", "last_reviewed"]
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
FM_LINE_RE = re.compile(r"^([a-z_]+): (.+)$")

MAX_GUIDE_BYTES = 128 * 1024
MAX_TOTAL_BYTES = 4 * 1024 * 1024
MAX_ASSET_BYTES = 512 * 1024
ASSET_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

# Schemes a link may use. http:// is excluded on purpose: the site is HTTPS-only
# and a plaintext link is a downgrade we do not need to offer anyone.
ALLOWED_SCHEMES = {"https", "mailto"}

# Link shorteners hide their destination, which defeats the entire point of
# reviewing a pull request's links. Contributors must paste the real URL.
SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "ow.ly", "buff.ly",
    "rebrand.ly", "cutt.ly", "shorturl.at", "rb.gy", "tiny.cc", "shorte.st",
    "adf.ly", "lnkd.in", "s.id", "trib.al", "dub.sh",
}

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
# Autolinks are legal markdown and legal HTML-looking text; everything else that
# opens an angle bracket on a letter or slash is treated as raw HTML.
# Matches every CommonMark autolink, not just the ones we allow — an autolink
# with a scheme we reject must be *recognised* here so check_scheme can refuse
# it. Matching only good schemes would let <javascript:alert(1)> fall through
# both this and the raw-HTML scan.
AUTOLINK_RE = re.compile(r"<(?:[a-zA-Z][a-zA-Z0-9+.-]{1,31}:[^\s<>]*|[^\s<>@]+@[^\s<>@]+)>")
HTML_TAG_RE = re.compile(r"<\s*/?\s*[a-zA-Z][a-zA-Z0-9-]*(?:\s|/?>)")
LINK_RE = re.compile(r"(!?)\[(?:[^\]\\]|\\.)*\]\(\s*<?([^)\s>]*)>?(?:\s+\"[^\"]*\")?\s*\)")
SCHEME_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.-]*):")


class Problem(Exception):
    pass


def strip_code(text):
    """Blank out fenced blocks and inline code so scans see prose only.

    Guides legitimately write things like `<REGION>` and `<pubkey>` as
    placeholders inside code. Those must not read as raw HTML.
    """
    out, fence = [], None
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if fence is None and m:
            fence = m.group(1)[0] * 3
            out.append("")
            continue
        if fence is not None:
            if m and m.group(1)[0] * 3 == fence:
                fence = None
            out.append("")
            continue
        out.append(INLINE_CODE_RE.sub("", line))
    return "\n".join(out)


def parse_frontmatter(path, raw):
    """Parse the restricted frontmatter subset: flat `key: value` lines only.

    Deliberately not YAML. A real YAML parser accepts anchors, tags, and nested
    structures we have no use for and would then have to reason about.
    """
    if not raw.startswith("---\n"):
        raise Problem(f"{path.name}: missing frontmatter (file must start with '---')")
    end = raw.find("\n---\n", 3)
    if end == -1:
        raise Problem(f"{path.name}: frontmatter is not closed with '---'")

    meta = {}
    for n, line in enumerate(raw[4:end].split("\n"), start=2):
        if not line.strip():
            continue
        m = FM_LINE_RE.match(line)
        if not m:
            raise Problem(f"{path.name}:{n}: frontmatter must be 'key: value' — got {line!r}")
        key, value = m.group(1), m.group(2).strip()
        if key in meta:
            raise Problem(f"{path.name}:{n}: duplicate frontmatter key {key!r}")
        meta[key] = value

    unknown = sorted(set(meta) - set(REQUIRED_KEYS))
    if unknown:
        raise Problem(f"{path.name}: unknown frontmatter key(s): {', '.join(unknown)}")
    missing = [k for k in REQUIRED_KEYS if k not in meta]
    if missing:
        raise Problem(f"{path.name}: missing frontmatter key(s): {', '.join(missing)}")

    body = raw[end + 5:].lstrip("\n")
    return meta, body


def check_meta(path, meta, section_ids):
    stem = path.stem
    if meta["id"] != stem:
        raise Problem(f"{path.name}: id {meta['id']!r} must match the filename ({stem!r})")
    if not ID_RE.match(meta["id"]):
        raise Problem(f"{path.name}: id must be lowercase letters, digits and hyphens")
    if meta["section"] not in section_ids:
        raise Problem(
            f"{path.name}: section {meta['section']!r} is not in sections.json "
            f"(known: {', '.join(sorted(section_ids))})"
        )
    if not meta["order"].isdigit() or int(meta["order"]) < 1:
        raise Problem(f"{path.name}: order must be a positive integer")
    if not meta["title"].strip():
        raise Problem(f"{path.name}: title must not be empty")
    if len(meta["title"]) > 80:
        raise Problem(f"{path.name}: title must be 80 characters or fewer")
    try:
        reviewed = datetime.strptime(meta["last_reviewed"], "%Y-%m-%d").date()
    except ValueError:
        raise Problem(f"{path.name}: last_reviewed must be YYYY-MM-DD")
    if reviewed > date.today():
        raise Problem(f"{path.name}: last_reviewed is in the future")


def check_html(path, prose):
    for autolink in AUTOLINK_RE.finditer(prose):
        prose = prose.replace(autolink.group(0), "")
    m = HTML_TAG_RE.search(prose)
    if m:
        line = prose[:m.start()].count("\n") + 1
        raise Problem(
            f"{path.name}:~{line}: raw HTML is not allowed ({m.group(0).strip()!r}). "
            "Use markdown, or wrap literal angle brackets in backticks."
        )


def check_scheme(where, url):
    """Reject any URI scheme we do not publish. Only ever called on link targets.

    Scanning prose for 'data:' or 'javascript:' as bare substrings produces
    false positives on ordinary English ("two ways of moving data:"), so the
    scheme rules apply strictly to parsed link targets and autolinks.
    """
    m = SCHEME_RE.match(url)
    if not m:
        return False
    scheme = m.group(1).lower()
    if scheme not in ALLOWED_SCHEMES:
        hint = " — use https" if scheme == "http" else ""
        raise Problem(f"{where}: {scheme}: links are not allowed{hint} ({url!r})")
    if scheme == "https":
        host = url[len("https://"):].split("/")[0].split("@")[-1].split(":")[0].lower()
        if host in SHORTENERS or host.removeprefix("www.") in SHORTENERS:
            raise Problem(f"{where}: link shortener {host!r} — link the real destination")
    return True


def check_links(path, prose, guide_ids):
    for m in AUTOLINK_RE.finditer(prose):
        line = prose[:m.start()].count("\n") + 1
        check_scheme(f"{path.name}:~{line}", m.group(0)[1:-1])

    for m in LINK_RE.finditer(prose):
        is_image, url = m.group(1) == "!", m.group(2).strip()
        line = prose[:m.start()].count("\n") + 1
        where = f"{path.name}:~{line}"
        if not url:
            raise Problem(f"{where}: empty link target")

        if is_image:
            if "://" in url or url.startswith("//") or url.startswith("data:"):
                raise Problem(
                    f"{where}: images must be committed to assets/ and referenced "
                    f"relatively — external image URLs leak reader IP addresses ({url!r})"
                )
            if not url.startswith("assets/"):
                raise Problem(f"{where}: image path must start with 'assets/' — got {url!r}")
            if not (ASSETS / url[len("assets/"):]).is_file():
                raise Problem(f"{where}: image {url!r} is not committed to the repo")
            continue

        if check_scheme(where, url):
            continue
        if url.startswith("#"):
            continue
        if url.startswith("?section="):
            target = url[len("?section="):].split("&")[0]
            if target not in guide_ids:
                raise Problem(f"{where}: ?section={target} does not match any guide id")
            continue
        if url.startswith("./") and url.endswith(".md"):
            target = url[2:-3]
            if target not in guide_ids:
                raise Problem(f"{where}: link to {url!r} but there is no such guide")
            continue
        if url.startswith("/"):
            if url.startswith("//"):
                raise Problem(f"{where}: protocol-relative URLs are not allowed ({url!r})")
            continue

        raise Problem(
            f"{where}: relative link {url!r} is not a form we publish. Use "
            "'?section=<guide-id>' for KB links or a full https:// URL."
        )


def load():
    """Read and fully validate every source file. Returns (sections, guides)."""
    problems, guides = [], {}

    if not SECTIONS.is_file():
        raise SystemExit("error: sections.json is missing")
    try:
        sections_doc = json.loads(SECTIONS.read_text())
        sections = sections_doc["sections"]
        section_ids = [s["id"] for s in sections]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        raise SystemExit(f"error: sections.json is malformed: {e}")
    if len(section_ids) != len(set(section_ids)):
        raise SystemExit("error: sections.json has duplicate section ids")

    paths = sorted(GUIDES.glob("*.md"))
    if not paths:
        raise SystemExit("error: no guides found")

    stray = sorted(p.name for p in GUIDES.iterdir() if p.suffix != ".md")
    if stray:
        problems.append(f"guides/ must contain only .md files — found: {', '.join(stray)}")

    total = 0
    for path in paths:
        size = path.stat().st_size
        total += size
        if size > MAX_GUIDE_BYTES:
            problems.append(f"{path.name}: {size} bytes exceeds the {MAX_GUIDE_BYTES} byte cap")
            continue
        raw = path.read_text(encoding="utf-8")
        try:
            meta, body = parse_frontmatter(path, raw)
            check_meta(path, meta, set(section_ids))
        except Problem as e:
            problems.append(str(e))
            continue
        guides[meta["id"]] = {"meta": meta, "body": body, "path": path}

    if total > MAX_TOTAL_BYTES:
        problems.append(f"guides total {total} bytes, over the {MAX_TOTAL_BYTES} byte cap")

    guide_ids = set(guides)
    for gid, g in sorted(guides.items()):
        prose = strip_code(g["body"])
        for check in (
            lambda: check_html(g["path"], prose),
            lambda: check_links(g["path"], prose, guide_ids),
        ):
            try:
                check()
            except Problem as e:
                problems.append(str(e))

    seen = {}
    for gid, g in sorted(guides.items()):
        key = (g["meta"]["section"], int(g["meta"]["order"]))
        if key in seen:
            problems.append(
                f"{gid}: section/order {key[0]}/{key[1]} already used by {seen[key]}"
            )
        seen[key] = gid

    if ASSETS.is_dir():
        for asset in sorted(ASSETS.rglob("*")):
            if asset.is_dir():
                continue
            if asset.suffix.lower() not in ASSET_SUFFIXES:
                problems.append(f"assets/{asset.relative_to(ASSETS)}: unsupported file type")
            elif asset.stat().st_size > MAX_ASSET_BYTES:
                problems.append(f"assets/{asset.relative_to(ASSETS)}: over 512 KiB")

    if problems:
        print(f"{len(problems)} problem(s):\n", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        raise SystemExit(1)

    return sections, guides


def build_index(sections, guides):
    out = []
    for section in sections:
        members = sorted(
            (g for g in guides.values() if g["meta"]["section"] == section["id"]),
            key=lambda g: int(g["meta"]["order"]),
        )
        if not members:
            continue
        out.append({
            "id": section["id"],
            "title": section["title"],
            "guides": [
                {
                    "id": g["meta"]["id"],
                    "title": g["meta"]["title"],
                    "file": f"/guides/{g['meta']['id']}.md",
                }
                for g in members
            ],
        })
    return {"version": 1, "sections": out}


def cmd_build(outdir):
    sections, guides = load()
    dest = Path(outdir).resolve() / "guides"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    for gid, g in sorted(guides.items()):
        (dest / f"{gid}.md").write_text(g["body"], encoding="utf-8")
    (dest / "index.json").write_text(
        json.dumps(build_index(sections, guides), indent=2) + "\n", encoding="utf-8"
    )
    if ASSETS.is_dir():
        shutil.copytree(ASSETS, dest / "assets")

    print(f"built {len(guides)} guides into {dest}")


def cmd_validate():
    sections, guides = load()
    stale = sorted(
        (g["meta"]["last_reviewed"], gid)
        for gid, g in guides.items()
        if (date.today() - datetime.strptime(g["meta"]["last_reviewed"], "%Y-%m-%d").date()).days > 180
    )
    print(f"ok: {len(guides)} guides across {len(sections)} sections")
    if stale:
        print(f"\nnote: {len(stale)} guide(s) not reviewed in over 180 days:")
        for reviewed, gid in stale:
            print(f"  - {gid} (last reviewed {reviewed})")


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ("validate", "build"):
        raise SystemExit(__doc__)
    if args[0] == "validate":
        cmd_validate()
    else:
        cmd_build(args[1] if len(args) > 1 else "dist")


if __name__ == "__main__":
    main()
