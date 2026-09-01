#!/usr/bin/env bash
#
# Publish merged knowledge-base content to nhmesh.live.
#
# Runs on the web host on a timer. Fetches the public repo at PUBLISHED_REF,
# validates it with the host's own pinned copy of kb.py, and moves the rendered
# guides into the directory nginx serves. On any failure the currently published
# content is left exactly as it is.
#
# Two properties this script exists to guarantee:
#
#   1. Code from the repo is never executed. kb.py comes from $KB_BIN on this
#      host, which the tarball cannot write to. A merged pull request supplies
#      content and nothing else.
#   2. Publishing is reversible without touching git. Pin PUBLISHED_REF to a
#      known-good commit, or stop the timer, and the site stops tracking main.
#
set -euo pipefail

REPO="${KB_REPO:-NHMesh/nhmesh-kb}"
CONF_DIR="${KB_CONF_DIR:-/etc/nhmesh-kb}"
DEST="${KB_DEST:-/srv/nhmesh-kb/guides}"
KB_BIN="${KB_BIN:-/opt/nhmesh-kb/kb.py}"
STATE="${KB_STATE:-/var/lib/nhmesh-kb}"
REF="$(cat "$CONF_DIR/PUBLISHED_REF" 2>/dev/null || echo main)"
# Overridable so the script can be exercised against a fork or a local tarball
# before it is pointed at production.
TARBALL_URL="${KB_TARBALL_URL:-https://codeload.github.com/$REPO/tar.gz/$REF}"

log() { printf '%s kb-sync: %s\n' "$(date -Is)" "$*"; }
die() { log "ERROR: $*"; exit 1; }

[ -f "$KB_BIN" ] || die "validator missing at $KB_BIN"
[ -d "$DEST" ]   || die "publish target $DEST does not exist"
mkdir -p "$STATE"

# One run at a time. A timer that overlaps itself mid-swap would interleave writes.
exec 9>"$STATE/lock"
flock -n 9 || { log "another run holds the lock; skipping"; exit 0; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

log "fetching $TARBALL_URL"
curl -fsSL --max-time 120 --retry 3 --retry-delay 5 \
  -o "$WORK/src.tar.gz" "$TARBALL_URL" \
  || die "fetch failed; keeping current content"

# --no-same-owner and the strip keep a hostile archive from writing outside $WORK;
# tar refuses absolute and ../ members by default.
mkdir -p "$WORK/src"
tar -xzf "$WORK/src.tar.gz" -C "$WORK/src" --strip-components=1 --no-same-owner \
  || die "extract failed; keeping current content"

[ -d "$WORK/src/guides" ] || die "tarball has no guides/ directory"
[ -f "$WORK/src/sections.json" ] || die "tarball has no sections.json"

# Validate and render with THIS host's validator, never the tarball's.
log "validating with $KB_BIN"
KB_ROOT="$WORK/src" python3 "$KB_BIN" validate || die "validation failed; keeping current content"
KB_ROOT="$WORK/src" python3 "$KB_BIN" build "$WORK/out" || die "build failed; keeping current content"

NEW="$WORK/out/guides"
[ -f "$NEW/index.json" ] || die "build produced no index.json"

# Publish. Each file lands with an atomic rename, so a reader gets either the old
# or the new file, never half of one. index.json goes last: it is the manifest,
# and it must never name a guide that is not on disk yet.
published=0
for f in "$NEW"/*.md; do
  name="$(basename "$f")"
  if [ -f "$DEST/$name" ] && cmp -s "$f" "$DEST/$name"; then
    continue
  fi
  cp "$f" "$DEST/.$name.tmp" && mv -f "$DEST/.$name.tmp" "$DEST/$name"
  published=$((published + 1))
  log "updated $name"
done

if [ -d "$NEW/assets" ]; then
  mkdir -p "$DEST/assets"
  for f in "$NEW"/assets/*; do
    [ -f "$f" ] || continue
    name="$(basename "$f")"
    if [ -f "$DEST/assets/$name" ] && cmp -s "$f" "$DEST/assets/$name"; then
      continue
    fi
    cp "$f" "$DEST/assets/.$name.tmp" && mv -f "$DEST/assets/.$name.tmp" "$DEST/assets/$name"
    published=$((published + 1))
  done
fi

# Remove guides deleted upstream, so a retracted page actually disappears.
for f in "$DEST"/*.md; do
  [ -f "$f" ] || continue
  name="$(basename "$f")"
  if [ ! -f "$NEW/$name" ]; then
    rm -f "$f"
    published=$((published + 1))
    log "removed $name (no longer in the repo)"
  fi
done

if ! cmp -s "$NEW/index.json" "$DEST/index.json"; then
  cp "$NEW/index.json" "$DEST/.index.json.tmp" && mv -f "$DEST/.index.json.tmp" "$DEST/index.json"
  published=$((published + 1))
  log "updated index.json"
fi

if [ "$published" -eq 0 ]; then
  log "no change (ref $REF)"
else
  log "published $published file(s) from ref $REF"
fi

# Record what is live so the state can be read back without guessing.
{
  echo "ref=$REF"
  echo "synced_at=$(date -Is)"
  echo "files_changed=$published"
} > "$STATE/published"
