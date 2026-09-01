---
id: meshtastic-vs-meshcore
title: Meshtastic vs. MeshCore
section: start-here
order: 2
last_reviewed: 2026-04-21
---

# Meshtastic vs. MeshCore

We run both. They are both good. The question is which fits what you're trying to do.

This guide is neutral. It is written by people who operate infrastructure for both protocols and have no stake in which one you pick. If you come away from this thinking one is clearly better than the other for **your** use case, that is the intended outcome. If you come away thinking one is better overall — go read it again, we did not make that argument.

---

## The short answer

| If this describes you… | Start with |
|---|---|
| I want a polished phone app, casual text chat, and the largest ecosystem | Meshtastic |
| I want messages to be delivered fast, even when the mesh is busy | MeshCore |
| I want to learn how a mesh actually routes packets | MeshCore |
| I want the lowest-friction out-of-box experience | Meshtastic |
| I want to run a repeater or room server for my community | MeshCore |
| I don't care, just pick for me | MeshCore |

We recommend MeshCore as the default for new NH-area nodes as of 2026. It is what most of our current active repeater operators run, it uses less airtime, and it handles our current node density better. Meshtastic is still fully supported, and if you are already comfortable with it, there is no reason to switch.

---

## How they differ, in plain language

### Meshtastic uses flooding
When you send a message, every node that hears it rebroadcasts it, and every node that hears **that** rebroadcasts it again, until the hop limit runs out. Simple, resilient, and works without any coordination between nodes. It also means every message uses airtime from every node in range, which gets expensive fast as the mesh gets denser.

### MeshCore uses state-aware routing
Nodes keep a map of their neighbors and send messages along a specific path toward the destination, with flooding as a fallback. This uses less airtime on average, delivers faster when the route is known, and scales better with density. The trade-off is that the routing state has to warm up — a brand-new MeshCore node takes a few minutes to start appearing in other nodes' routing tables.

### Meshtastic has the app
The Meshtastic app (iOS and Android) is the most polished piece of software in the LoRa mesh world right now. If your use case is "I want to text my friend who is out of cell range," the app experience matters a lot.

### MeshCore has better role separation
Out of the box, MeshCore distinguishes a **Companion** (what you carry around), a **Repeater** (what you install high up), and a **Room Server** (a persistent group chat host). Meshtastic can do all of these but the configuration is less explicit.

---

## What stays the same

- **Same hardware.** Heltec V3/V4, T-Beam, RAK 4631, LilyGo devices all run either firmware. You can flash back and forth as you learn.
- **Same frequencies and region settings.** 915 MHz in the US, with the same regulatory rules.
- **Same physics.** Range, antenna choice, line-of-sight — all the same.
- **Same community.** You will see nodes of both protocols in our Discord and on our map.

---

## Interoperability

We are building bridges that let a Meshtastic user send a message that reaches a MeshCore user and vice versa, via our infrastructure. Bridging is **not** the same as native support — some message types pass through cleanly, others do not. If you plan to rely on cross-protocol messaging, do not. If it works, consider it a bonus.

---

## What we recommend in practice

**If you are brand new:** start with MeshCore. Flash a Heltec V4 with the Companion firmware, pair it with the MeshCore app, and you are on the mesh in under 30 minutes. If you decide later that you want to try Meshtastic, the same hardware will run it — erase and reflash.

**If you have been running Meshtastic and it works for you:** there is no requirement to switch. The NHMesh infrastructure will keep supporting Meshtastic for the foreseeable future. Take a look at MeshCore when you have a spare afternoon and want to see the difference firsthand.

**If you are building backbone infrastructure (a repeater on a hill, a room server for a town):** use MeshCore. The routing and role model are a better fit for fixed infrastructure.

---

## Common misconceptions

**"MeshCore is newer so it must be worse."** It is newer. Newer in protocol design generally means it learned from the things Meshtastic had to figure out the hard way. In some ways it is more mature; in other ways (app polish, documentation depth, number of devices shipped) Meshtastic has the lead.

**"Meshtastic is dying."** Not even close. It has a much larger global user base and active development.

**"You can only run one."** You can literally run both on different devices in your pocket. Some of us do.

---

## Next steps

- **[Hardware Picker](?section=hardware-picker)** — what to buy, by use case and budget.
- **[MeshCore Node Setup](?section=meshcore-setup)** — if you picked MeshCore.
- **[Meshtastic Node Setup](?section=meshtastic-setup)** — if you picked Meshtastic.
