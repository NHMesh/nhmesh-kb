---
id: faq-glossary
title: FAQ & Glossary
section: reference
order: 5
last_reviewed: 2026-11-12
---

# FAQ & Glossary

Short answers and plain-English definitions for terms you'll see in these guides. Written for MeshCore first; Meshtastic notes are marked. For MeshCore's own FAQ see [docs.meshcore.io/faq](https://docs.meshcore.io/faq/).

---

## Glossary

| Term | Meaning |
|---|---|
| **Companion** | A MeshCore node paired to your phone over Bluetooth. Clients don't repeat other people's traffic. |
| **Repeater** | A stationary MeshCore node that forwards traffic to extend range. It can't pair with the phone app over Bluetooth. |
| **Room server** | A MeshCore node that acts like a simple bulletin board: it stores posts so people can catch up later. |
| **Observer** | A node plus a small uplink that reports every packet it hears to the map. See **[Observer / Gateway Setup](?section=letsmesh-observer)**. |
| **Advert** | A MeshCore packet announcing your name, position and public key. Others add you to their contacts from it. |
| **Zero-hop advert** | An advert heard only by radios in direct range. |
| **Flood advert** | An advert that repeaters rebroadcast, so it spreads across the mesh. |
| **Flood routing** | Every repeater that hears a packet rebroadcasts it. Used for channels and for a first message to a contact. |
| **Direct routing** | After a first flooded message, later messages follow the stored list of repeaters, so only those forward them. |
| **Path hash** | The short ID of each repeater in a route. 1, 2 or 3 bytes; more bytes identify repeaters more reliably. |
| **Region / scope** | A label on a flood packet that repeaters can allow or block. See **[MeshCore Repeaters & Regions in NH](?section=meshcore-repeaters-regions)**. |
| **Hashtag channel** | A channel whose key comes from its name, like `#nhmesh`. Anyone can join; it isn't private. |
| **LongFast** | The Meshtastic preset NHMesh uses. |
| **MediumFast** | A Meshtastic preset. Supported on NHMesh but not recommended. |
| **Preset** | A packaged set of LoRa radio parameters. MeshCore's NH one is `910.525,62.5,7,5`. |

Sources for MeshCore definitions: [MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md) and [CLI reference](https://github.com/meshcore-dev/MeshCore/blob/main/docs/cli_commands.md).

---

## FAQ

### Should I run MeshCore or Meshtastic?

We recommend MeshCore for new nodes. See **[Meshtastic vs. MeshCore](?section=meshtastic-vs-meshcore)**. The two don't talk to each other over the air.

### Why can't my phone connect to my repeater?

Only Companion firmware pairs over Bluetooth. Repeaters are configured by USB, the web config tool, or remote admin. See **[MeshCore Node Setup](?section=meshcore-setup)**.

### What's the Bluetooth PIN?

`123456` by default.

### How often should I send an advert?

Only when you need to: after setup, after moving, or after fixing your clock. Repeaters advert on their own timer. Send a flood advert, not zero-hop, if you want the map to see you.

### What's the difference between flood and direct?

Flood is a shout that every repeater repeats. Direct is a whisper along a known path. Channels always flood. A first message to a contact floods, then the stored path is reused.

### Why does a contact message fail?

The stored path may be broken. After 3 failed retries the app resets the path and floods by default.

### Can I use MediumFast?

On Meshtastic, yes; it's supported but we don't recommend it. LongFast is the NHMesh standard.

### Which channel do I use to test?

`#nh-hc`, the health-check channel. Not the Public channel. See **[Using the Health Check](?section=health-check)**.

### Where do I get help?

See **[NH Cheat Sheet](?section=nh-cheat-sheet)**.

### Why am I not on the map?

See **[MeshCore Troubleshooting](?section=meshcore-troubleshooting)**.
