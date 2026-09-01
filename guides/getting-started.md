---
id: getting-started
title: Welcome
section: start-here
order: 1
last_reviewed: 2026-04-21
---

# Welcome to NHMesh

NHMesh is an independent, community-run mesh radio network covering New Hampshire and the surrounding region. The network runs on LoRa radios — small, low-power devices that can pass short text messages across tens of miles without cellular service, internet, or a central provider. Every node anyone puts up makes the network better for everyone else.

We are a dual-protocol network. Both **Meshtastic** and **MeshCore** run over the same hardware on the same frequencies, and our infrastructure (repeaters, MQTT bridges, the live map) supports both. You pick whichever protocol fits your goals; many of us run both.

This page is a short orientation. Pick the path below that matches where you are.

---

## Pick your path

### I'm brand new and don't own any hardware yet
Start with these three guides in order:

1. **[Meshtastic vs. MeshCore](?section=meshtastic-vs-meshcore)** — a neutral comparison so you can pick a protocol.
2. **[Hardware Picker](?section=hardware-picker)** — what to buy for your use case and budget.
3. **[Your First Node](?section=first-node)** — a quick-start from unboxing to on the mesh.

### I have hardware and I want to get on the mesh
Jump directly to a setup guide:

- **[MeshCore Node Setup](?section=meshcore-setup)** — our recommended default for new NH-area nodes.
- **[Meshtastic Node Setup](?section=meshtastic-setup)** — if you want the more mature app ecosystem.

### Something is broken / my node isn't showing up
Head to **Troubleshooting** (in the sidebar) for symptom-based flowcharts. The most common issue — "I'm set up but nothing is happening" — is covered in the **[Map Visibility](?section=troubleshooting-visibility)** guide.

### I want to understand how the network actually works
Read the **[Mesh Network Basics](?section=mesh-basics)** primer. It covers LoRa, hops, signal quality, and the two routing architectures we use. Not strictly required to get on the mesh, but it helps you reason about coverage and why things sometimes take a few minutes to stabilize.

---

## What you can do on the mesh

- **Send text messages** to specific people or to community channels. No accounts, no servers; the radios do it directly.
- **Share your location** periodically so others (and the live map) can see where you are.
- **Run a repeater** to extend coverage for your neighborhood. We are always short on good high-elevation infrastructure.
- **Pass traffic in an outage.** LoRa doesn't need power or internet at the intermediate hops, which makes it useful when the usual networks are down.

The live map at [nhmesh.live](/) shows everyone currently online. The **Nodes** tab shows the full roster. The **Observers** tab shows the gateway fleet that keeps the map fed.

---

## Where to get help

- **Discord** — the main place we talk. Ask in the setup/support channel; response time is usually under an hour during waking hours.
- **Matrix** — `matrix.nhmesh.com` — bridged to the MeshCore room if you prefer Matrix over Discord.
- **In-network** — the `#nhmesh` hashtag channel is general chat; `#nhhc` is for health-check pings.

No question is too basic. Most of us struggled with the same setup steps you're about to, and we are happy to walk through them. If you find yourself stuck on something the knowledge base doesn't cover, tell us — that's how this documentation grows.
