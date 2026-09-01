---
id: matrix-and-community
title: Matrix Server & Community
section: reference
order: 3
last_reviewed: 2026-04-21
---

# Matrix Server & Community

Where to find other NHMesh operators when you're not on the mesh itself. This guide covers the community channels we maintain and how to participate.

---

## Discord

**The main place we talk.** The NHMesh Discord is where most setup questions get answered, announcements happen, and people coordinate infrastructure builds.

- **Invite:** [nhmesh.live](/) has the current link in the footer; also posted in our monthly community updates.
- **Key channels:**
  - `#general` — community chat
  - `#support` / `#help` — setup questions, troubleshooting
  - `#infrastructure` — coordinating repeater placement and backbone operations
  - `#announcements` — read-only, major updates

We monitor `#support` casually throughout the day. Response time is usually under an hour during waking hours. No question is too basic — the people answering struggled with the same setup steps you're asking about, recently.

---

## Matrix

For people who prefer not to use Discord, we run a Matrix server bridged to some of the Discord channels.

- **Server:** `matrix.nhmesh.com`
- **Registration:** open to anyone — create an account via Element or any Matrix client.
- **Current rooms:** a general chat + MeshCore bridging. Still small — a few regular users.

### Joining from Matrix

If you already have a Matrix account on another server (matrix.org, element.io, your own server):

1. Join the space by searching for `#nhmesh-space:matrix.nhmesh.com` in your client, or visiting the direct link from Element.
2. From there you can join the general chat room.

**Known issue:** some matrix.org-hosted accounts have hit room-join failures with a 403 error. If that happens to you, tell us in Discord — we can usually work around it on our server.

### Using a Matrix account on our server

You can also register directly on `matrix.nhmesh.com`:

1. In Element, choose **Edit** when asked for homeserver during sign-up.
2. Enter `matrix.nhmesh.com`.
3. Register.

Our server is maintained by volunteers and runs on community infrastructure. It's not a Signal / Slack replacement — we lean on Discord for day-to-day coordination — but it's there if you want a federated / open-protocol option.

---

## The mesh itself

Obviously: if you're on the mesh, that is also a way to talk to us.

- `#nhmesh` — general community chat, slower-paced than Discord but works without internet
- DMs — person-to-person coordination

See **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** for our guidelines on when to use which channel.

---

## Meetups

We hold in-person meetups periodically — usually once a quarter in different parts of NH or MA, sometimes aligned with events like Hamvention or local maker fairs. Details get announced in Discord and the monthly community update.

If you want to host one near you or at a site you run, post in `#infrastructure` — coordinating a gathering in an area we haven't visited before is always welcome.

---

## Tools & external resources

Useful community-maintained tools and docs:

### Related maps and analyzers
- **[analyzer.letsmesh.net](https://analyzer.letsmesh.net)** — the LetsMesh packet analyzer for MeshCore. Broader than NHMesh specifically, but overlaps heavily with our coverage area.
- **[boston.mesh](https://live.bostonme.sh)** — our neighbors in Eastern MA. Friendly, well-run, shares infrastructure and operators with us.

### Firmware and flashing
- **[flasher.meshcore.co.uk](https://flasher.meshcore.co.uk)** — official MeshCore web flasher
- **[config.meshcore.dev](https://config.meshcore.dev)** — MeshCore web config tool for Repeaters and Room Servers
- **[Meshtastic Flasher](https://flasher.meshtastic.org)** — Meshtastic firmware flasher

### Third-party apps and tools
- **[MeshSense](https://affirmatech.com/meshsense)** — open-source "network dashboard" for Meshtastic
- **Meshtastic Reddit community** — [r/meshtastic](https://www.reddit.com/r/meshtastic/) has a lot of troubleshooting crowd-sourced knowledge

### Vendor resources
- **[Meshtastic official docs](https://meshtastic.org)** — the authoritative source for Meshtastic firmware behavior
- **[MeshCore GitHub](https://github.com/meshcore-dev/MeshCore)** — source code, issue tracker, release notes

---

## Contributing

NHMesh is entirely community-run. If you want to help:

- **Operate a repeater.** The single most valuable contribution is more high-quality infrastructure. See **[Coverage & Placement](?section=coverage-placement)**.
- **Answer questions.** The more people who answer setup questions, the faster newcomers get unstuck.
- **Improve this knowledge base.** Every guide here is Markdown in a public repo. Spotted a mistake or missing info? PR it or mention it in Discord.
- **Write a guide.** If you figured out something the rest of us haven't documented, contribute it.

---

## Related guides

- **[Welcome](?section=getting-started)** — if you got here without going through the front door
- **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** — on-mesh community etiquette
