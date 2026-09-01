---
id: meshcore-hashtag-channels
title: Stewardship & Hashtag Channels
section: operating
order: 1
last_reviewed: 2026-04-21
---

# Stewardship & Hashtag Channels

LoRa is a shared medium. Every packet anyone transmits uses airtime that nobody else can use at the same time. As the NH mesh grows, casual habits that were fine with 20 nodes become expensive with 200. This guide is about how we — operators and users — keep the network useful.

The short version: **use hashtag channels instead of the Public channel whenever possible, and don't flood-broadcast things that don't need everyone to hear them.**

---

## The flooding problem

MeshCore's Public channel is a flood-routed channel — every node that hears a packet retransmits it, up to 64 hops. That is powerful, and it is exactly what you want when a message needs to reach every node in the region (real emergencies, critical coordination). It is also expensive: one message turns into hundreds of radio transmissions across the fleet.

Imagine sending a "radio check" test message on the Public channel:

- Your node transmits once
- Every repeater in range retransmits it
- Every repeater in range of those retransmits it
- Ripples outward until the hop limit runs out

Your "is my radio working" check just used airtime from every node in the eastern half of the state.

This isn't an abstract concern. On a busy afternoon we see the network approach saturation when Public channel traffic spikes — which means real messages (health checks, DMs, important channel chat) get dropped or delayed.

---

## Hashtag channels: the solution we have today

A hashtag channel is a named channel whose encryption key is derived from the channel name itself. Anyone who types `#nhmesh` joins the same channel. Traffic on the channel still floods across the mesh, but only nodes that have joined that specific channel will decode and relay it — the others see ciphertext they can't identify and drop it.

This gives us a way to segment traffic by purpose without needing firmware-level regional routing (which is still in flux). Using the right hashtag for the right activity is the single biggest habit we ask of everyone.

---

## Our standard channels

| Hashtag | Primary use | Flood level |
|---|---|---|
| **#nhmesh** | General chat: introductions, community talk, mesh shop talk | Normal |
| **#nhhc** | Health checks and radio tests — use this instead of the Public channel for any "is my node working" pings | Normal |
| **#emergency** | Actual emergencies. Floods aggressively on purpose | Max |
| **#nh-seacoast / #nh-monadnock / #nh-lakes** | Regional chatter when it doesn't need to reach the whole state | Normal |
| **Public** | Only when you need absolute reach — onboarding new users, reaching someone in a region you don't have a channel for | Max |

---

## Practical examples

| Situation | Right channel |
|---|---|
| Testing a new node | `#nhhc` — one ping, wait for the map, done |
| War-driving in your car | `#nhhc` with occasional stops (not continuous broadcast) |
| Asking a setup question | `#nhmesh` |
| Chatting with a neighbor two hops away | DM, or `#nhmesh` if it's community-relevant |
| Coordinating a local event | `#nh-{your-region}` |
| Grid-down, actual emergency | Public + `#emergency`, flood away |
| "Hello, is anyone out there?" | `#nhmesh` |

---

## Why not just everyone on Public all the time?

A few people doing this is fine. A hundred is not. The math gets steep fast:

- One user sends a message on Public → flooded across the network, maybe 30 retransmissions total
- 100 users each sending a message an hour → 3,000 retransmissions per hour on Public alone
- At typical MeshCore airtime budgets, that approaches saturation

Hashtag channels cut most of that traffic because only interested nodes retransmit. A single regional hashtag channel can carry the same conversational load with a fraction of the mesh-wide cost.

---

## Security note

Hashtag channels are **not private**. The key is derived from a public string (the hashtag name) via a known function. Anyone can compute the same key by joining the same hashtag. Treat hashtag channels as semi-public chat — fine for community conversation, not fine for sensitive data.

For private communication, use direct messages. DMs are end-to-end encrypted with the recipient's public key and are not broadcast across the network.

---

## Joining a hashtag channel

### MeshCore app
1. Channels tab → Add Channel → Join Hashtag.
2. Enter the hashtag name (the `#` prefix is often implicit — enter `nhmesh`, not `#nhmesh`).
3. The app derives the key and subscribes you.

### Meshtastic
Meshtastic's channel model is different — channels are configured per-device with explicit PSKs. See **[Meshtastic Channel Setup](?section=meshtastic-channel-setup)** for the mapping between our hashtag channels and Meshtastic channel config.

---

## For infrastructure operators

If you run a Repeater or Room Server, a few additional habits help:

- **Monitor airtime utilization.** MeshCore exposes per-node airtime counters. If your node is consistently over 10% airtime utilization, something is generating more traffic than is healthy.
- **Report saturation.** If you see network-wide congestion (packets dropping, long delays), post in `#nhmesh` so others can investigate.
- **Limit NeighborInfo broadcasts.** On Meshtastic Repeaters, disable NeighborInfo — it's chatty and the functionality is limited in recent firmware.
- **Host regional rooms if appropriate.** A Room Server in a town can absorb local chatter that would otherwise flood the region.

---

## Related guides

- **[Meshtastic Channel Setup](?section=meshtastic-channel-setup)** — how to configure Meshtastic channels to match our standards
- **[Recommended Settings](?section=recommended-settings)** — radio and module config defaults
- **[Using the Health Check](?section=health-check)** — how to test coverage without flooding
