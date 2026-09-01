# Publishing

How merged content reaches nhmesh.live.

The web host runs `kb-sync.sh` on a timer. It fetches this repository at
`PUBLISHED_REF`, validates and renders it **with the host's own copy of
`kb.py`**, and moves the result into the directory nginx serves. Nothing from the
repository is executed. Any failure leaves the published site untouched.

## Install

Run on the host that serves nhmesh.live.

```sh
# 1. The validator and the sync script, owned by root so the sync (running as
#    an unprivileged user) cannot rewrite the code that validates its input.
sudo mkdir -p /opt/nhmesh-kb /etc/nhmesh-kb /var/lib/nhmesh-kb
sudo install -m 0644 -o root -g root tools/kb.py       /opt/nhmesh-kb/kb.py
sudo install -m 0755 -o root -g root deploy/kb-sync.sh /opt/nhmesh-kb/kb-sync.sh
sudo chown nhmesh:nhmesh /var/lib/nhmesh-kb

# 2. Which ref to publish. `main` tracks the repository; a commit SHA pins it.
echo main | sudo tee /etc/nhmesh-kb/PUBLISHED_REF

# 3. Seed the served directory from the image's current guides, so the site keeps
#    working if the very first sync fails.
mkdir -p /srv/nhmesh-kb/guides
docker cp "$(docker compose ps -q live-frontend)":/usr/share/nginx/html/guides/. \
  /srv/nhmesh-kb/guides/

# 4. First run, in the foreground, before anything is automated.
sudo KB_DEST=/srv/nhmesh-kb/guides /opt/nhmesh-kb/kb-sync.sh
```

Then mount it over the image's copy in `docker-compose.yml`. Use the same path
as `KB_DEST` above:

```yaml
  live-frontend:
    volumes:
      - /srv/nhmesh-kb/guides:/usr/share/nginx/html/guides:ro
```

`docker compose up -d live-frontend`, then confirm the site is serving the mounted
copy:

```sh
curl -s https://nhmesh.live/guides/index.json | head -5
```

Finally, enable the timer:

```sh
sudo install -m 0644 deploy/kb-sync.service /etc/systemd/system/
sudo install -m 0644 deploy/kb-sync.timer   /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now kb-sync.timer
```

The guides baked into the frontend image stay there as a fallback. If the mount is
removed, the site falls back to image content rather than serving nothing.

## Operating

```sh
systemctl list-timers kb-sync.timer     # when it next runs
journalctl -u kb-sync.service -n 50     # what it did
cat /var/lib/nhmesh-kb/published        # ref and time of the last sync
```

## Stopping or rolling back

Publishing follows a ref the host controls, so neither of these needs a git
revert or a rebuild:

```sh
# Pin to known-good content. The next sync moves there and stays.
echo <commit-sha> | sudo tee /etc/nhmesh-kb/PUBLISHED_REF

# Or stop publishing entirely. The site keeps serving what is already there.
sudo systemctl stop kb-sync.timer
```

## Environment

| Variable | Default | Purpose |
|---|---|---|
| `KB_REPO` | `NHMesh/nhmesh-kb` | Repository to publish from |
| `KB_CONF_DIR` | `/etc/nhmesh-kb` | Holds `PUBLISHED_REF` |
| `KB_DEST` | `/srv/nhmesh-kb/guides` | Directory nginx serves |
| `KB_BIN` | `/opt/nhmesh-kb/kb.py` | The host's validator — never the tarball's |
| `KB_STATE` | `/var/lib/nhmesh-kb` | Lock file and last-sync record |
| `KB_TARBALL_URL` | derived from repo + ref | Override to test against a fork or a local tarball |
