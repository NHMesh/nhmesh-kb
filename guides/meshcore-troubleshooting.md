---
id: meshcore-troubleshooting
title: MeshCore Troubleshooting
section: troubleshooting
order: 5
last_reviewed: 2026-11-12
---

# MeshCore Troubleshooting

Use this when your MeshCore node can't see anyone, your adverts aren't showing up, you're not on the map, or your contacts list is empty. It's for MeshCore only; for Meshtastic nodes see **[My Node Isn't on the Map](?section=troubleshooting-visibility)** and **[Firmware Bugs & Recovery](?section=troubleshooting-firmware)**.

Work top to bottom. Each step is cheap and the first three fix most cases.

---

## Step 1: Check the radio settings

A MeshCore node on the wrong radio settings hears nothing and nobody hears it. Everything else is moot until this matches.

1. Open the app → your node → Radio settings.
2. Pick the **US Recommended** preset. It must read `910.525,62.5,7,5` (frequency MHz, bandwidth kHz, spreading factor, coding rate).
3. Reboot the node.

MeshCore's firmware default is `869.618,62.5,8,5`, which is a European setting, so a node that was flashed but never given a US preset will hear nothing here ([MeshCore CLI reference](https://github.com/meshcore-dev/MeshCore/blob/main/docs/cli_commands.md)).

## Step 2: Check you flashed the right firmware

- A phone only connects to **Companion** firmware over Bluetooth. A node flashed as Repeater or Room Server won't pair with the app ([MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)).
- Use the **Bluetooth** companion build, not a USB-only one.
- The default Bluetooth PIN is `123456`.
- Flash the US 915 MHz variant. See **[MeshCore Node Setup](?section=meshcore-setup)**.

## Step 3: Check the clock

A wrong clock is the most common documented reason contacts don't appear or show stale "last seen" times ([MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)). Reconnect the node to your phone so the app syncs the time, then send a new advert. A T-Deck with no GPS lock can have no valid time at all.

---

## Reading the symptom

| Symptom | Likely cause | Fix |
|---|---|---|
| Contacts list is empty | You haven't heard any adverts yet, or the clock is wrong | Wait for others' adverts (repeaters send theirs on a timer), fix the clock, then send your own advert |
| I can see others but they can't see me | Your advert was zero-hop and nobody was in direct range | Send a **Flood Routed Advert**, not a zero-hop one |
| Advert sent, still not on the map | No observer heard it, or lat/lon is `0` | Set a real lat/lon, enable **Advert Location Source**, send a flood advert, wait 3 minutes |
| Seen by one place but not another | You're only within range of one repeater | Move the node higher or outdoors; see **[Coverage & Placement](?section=coverage-placement)** |
| Messages to a contact fail | The stored path is broken | Reset the path for that contact, or let the app retry; the last retry floods by default |
| Phone won't pair | Wrong firmware role, or the node is paired to another phone | Reflash as Companion; remove the old Bluetooth pairing |
| Heltec V3 drops Bluetooth | Tiny on-board coil antenna | Replace it with a 31 mm wire ([MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)) |

---

## "I can't see anyone"

1. Radio settings match (Step 1), and the antenna is attached.
2. You're somewhere that can hear a repeater. Indoors in a basement often can't. Go outside or to a window and wait 5 minutes.
3. Check **[nhmesh.live/observers](/observers)**. If the observers near you show offline, the problem isn't your node.
4. Check the **[Health Check](?section=health-check)**: it tells you which observers heard a ping from you.

## "My adverts aren't showing"

An advert carries your name, location and public key. There are two kinds:

- **Zero-hop** is heard only by radios that can hear you directly.
- **Flood** is repeated by repeaters, so it travels across the mesh.

A client only adverts when you tell it to ([MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)). Send a **Flood Routed Advert** from the signal icon and wait 2 to 3 minutes. Don't spam adverts; each flood advert uses airtime for the whole region. See **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)**.

## "I'm not on the map"

The map is fed by observers that hear your advert and forward it. Companion nodes don't need extra setup, but an observer has to be in range of you or of a repeater that carries your advert. Work through:

1. Lat/lon is non-zero and **Advert Location Source** is on.
2. You sent a flood advert after setting them.
3. The Health Check shows at least one observer hearing you.

If you pass all three and still don't appear after 10 minutes, ask in `#nhmesh` or the Discord. See **[NH Cheat Sheet](?section=nh-cheat-sheet)** for where to get help.

## "My contacts are missing"

- Contacts are built from adverts you hear. A freshly flashed node has none.
- Fix the clock (Step 3) first.
- Whether your app auto-adds heard adverts as contacts is an app setting. **Unverified:** the exact setting name differs between app versions; check your app's contact or advert settings.
- You can import a contact from its QR code or by sharing it.

---

## Related guides

- **[MeshCore Node Setup](?section=meshcore-setup)**
- **[MeshCore Repeaters & Regions in NH](?section=meshcore-repeaters-regions)**
- **[FAQ & Glossary](?section=faq-glossary)**
