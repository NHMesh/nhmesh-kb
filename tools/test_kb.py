#!/usr/bin/env python3
"""Adversarial tests for the KB validator.

Each case copies the real repo to a temp dir, applies one poisoned edit, and
asserts `kb.py validate` rejects it. A validator nobody has watched fail is
decoration, so this runs in CI alongside the validation of real content.

    python3 tools/test_kb.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FM = "---\nid: poison\ntitle: Poison\nsection: reference\norder: 99\nlast_reviewed: 2026-01-01\n---\n\n"

# (name, filename, contents) — every one of these must be rejected.
MUST_REJECT = [
    ("script tag", "poison.md", FM + "# P\n\n<script>alert(1)</script>\n"),
    ("iframe", "poison.md", FM + "# P\n\n<iframe src=\"https://evil.test\"></iframe>\n"),
    ("img onerror", "poison.md", FM + "# P\n\n<img src=x onerror=alert(1)>\n"),
    ("closing tag", "poison.md", FM + "# P\n\n</div>\n"),
    ("javascript: link", "poison.md", FM + "# P\n\n[click](javascript:alert(1))\n"),
    ("data: uri link", "poison.md", FM + "# P\n\n[x](data:text/html;base64,PHNjcmlwdD4=)\n"),
    ("vbscript: link", "poison.md", FM + "# P\n\n[x](vbscript:msgbox(1))\n"),
    ("file: link", "poison.md", FM + "# P\n\n[x](file:///etc/passwd)\n"),
    ("http downgrade", "poison.md", FM + "# P\n\n[x](http://insecure.test)\n"),
    ("protocol-relative", "poison.md", FM + "# P\n\n[x](//evil.test/a)\n"),
    ("link shortener", "poison.md", FM + "# P\n\n[x](https://bit.ly/3abcdef)\n"),
    ("shortener with www", "poison.md", FM + "# P\n\n[x](https://www.tinyurl.com/x)\n"),
    ("external image", "poison.md", FM + "# P\n\n![x](https://evil.test/pixel.png)\n"),
    ("uncommitted image", "poison.md", FM + "# P\n\n![x](assets/nope.png)\n"),
    ("javascript autolink", "poison.md", FM + "# P\n\n<javascript:alert(1)>\n"),
    ("broken ?section link", "poison.md", FM + "# P\n\n[x](?section=does-not-exist)\n"),
    ("broken relative link", "poison.md", FM + "# P\n\n[x](./does-not-exist.md)\n"),
    ("no frontmatter", "poison.md", "# P\n\nbody\n"),
    ("unterminated frontmatter", "poison.md", "---\nid: poison\n\n# P\n"),
    ("id/filename mismatch", "poison.md", FM.replace("id: poison", "id: other") + "# P\n"),
    ("unknown section", "poison.md", FM.replace("section: reference", "section: nope") + "# P\n"),
    ("future review date", "poison.md", FM.replace("2026-01-01", "2099-01-01") + "# P\n"),
    ("bad date format", "poison.md", FM.replace("2026-01-01", "Jan 1 2026") + "# P\n"),
    ("unknown frontmatter key", "poison.md", FM.replace("---\n\n", "evil: yes\n---\n\n") + "# P\n"),
    ("nested frontmatter", "poison.md", "---\nid: poison\nx:\n  - a\n---\n\n# P\n"),
    ("non-md file in guides", "poison.sh", "#!/bin/sh\nrm -rf /\n"),
    ("oversized guide", "poison.md", FM + "# P\n\n" + ("A" * 200_000)),
]


def run(cwd):
    return subprocess.run(
        [sys.executable, "tools/kb.py", "validate"],
        cwd=cwd, capture_output=True, text=True,
    )


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp) / "repo"
        shutil.copytree(ROOT, base, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))

        clean = run(base)
        if clean.returncode != 0:
            print("FAIL: the unmodified repo does not validate — fix that first")
            print(clean.stdout + clean.stderr)
            return 1
        print("baseline: clean repo validates ok")

        for name, filename, contents in MUST_REJECT:
            target = base / "guides" / filename
            target.write_text(contents)
            result = run(base)
            target.unlink()
            if result.returncode == 0:
                failures.append(name)
                print(f"  NOT CAUGHT  {name}")
            else:
                print(f"  caught      {name}")

        # A duplicate section/order pair must also be rejected.
        dup = base / "guides" / "poison.md"
        existing = (base / "guides" / "resources.md").read_text().split("---")[1]
        order = [l for l in existing.strip().split("\n") if l.startswith(("section:", "order:"))]
        dup.write_text(
            "---\nid: poison\ntitle: Poison\n" + "\n".join(order)
            + "\nlast_reviewed: 2026-01-01\n---\n\n# P\n"
        )
        if run(base).returncode == 0:
            failures.append("duplicate section/order")
            print("  NOT CAUGHT  duplicate section/order")
        else:
            print("  caught      duplicate section/order")
        dup.unlink()

        # Guard against over-blocking: these must all still PASS.
        ok_cases = [
            ("angle brackets in code", FM + "# P\n\nUse `meshcore/<REGION>/<pubkey>/packets`.\n"),
            ("angle brackets in fence", FM + "# P\n\n```\nmeshcore/<REGION>/<pubkey>\n```\n"),
            ("prose colon", FM + "# P\n\nTwo ways of moving data: radio and MQTT.\n"),
            ("https autolink", FM + "# P\n\n<https://meshtastic.org>\n"),
            ("valid kb link", FM + "# P\n\n[x](?section=mqtt-auth)\n"),
            ("root-relative link", FM + "# P\n\n[map](/)\n"),
        ]
        for name, contents in ok_cases:
            target = base / "guides" / "poison.md"
            target.write_text(contents)
            result = run(base)
            target.unlink()
            if result.returncode != 0:
                failures.append(f"false positive: {name}")
                print(f"  FALSE POS   {name}\n{result.stderr}")
            else:
                print(f"  allowed     {name}")

    print()
    if failures:
        print(f"{len(failures)} FAILURE(S): {', '.join(failures)}")
        return 1
    print(f"all {len(MUST_REJECT) + len(ok_cases) + 1} cases behaved correctly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
