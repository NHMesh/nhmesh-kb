---
id: meshcore-setup
title: MeshCore Node Setup
section: setup
order: 2
last_reviewed: 2026-04-21
---

# MeshCore Node Setup

This guide walks through setting up a MeshCore node end-to-end: picking a role, flashing the firmware, configuring it, and getting on the mesh. It's the detailed version of **[Your First Node](?section=first-node)**, with the decision points fully explained.

If you haven't picked between Meshtastic and MeshCore yet, see **[Meshtastic vs. MeshCore](?section=meshtastic-vs-meshcore)**.

---

## Step 1: Pick your role

MeshCore has three first-class node roles. The firmware build you flash depends on which you want. The role is **permanent until you reflash** — you can't switch at runtime.

| Role | What it does | Typical hardware | Example |
|---|---|---|---|
| **Companion** | Personal device paired with a phone app over Bluetooth | Any handheld | Heltec V4 in your pocket |
| **Repeater** | Stationary relay that forwards traffic for nearby nodes | Outdoor / high-elevation | RAK 4631 on your roof |
| **Room Server** | Hosts persistent group chat channels | Fixed install with decent uptime | A node at home with 24/7 power |

### How to decide

- **You want to send and receive messages yourself, typically from your phone** → **Companion**. This is 90% of the network.
- **You have a good high-elevation spot (attic, roof, hill, tower) and want to help the mesh** → **Repeater**. We always need more.
- **You want to run a persistent group chat for a town or community** → **Room Server**. Can also act as a Repeater simultaneously.

If you're unsure, start as a Companion. You can always reflash to Repeater later.

---

## Step 2: Flash the firmware

### Prerequisites
- Your board (Heltec V4, RAK 4631, T-Beam, etc.) — see **[Hardware Picker](?section=hardware-picker)**.
- A USB-C cable with data lines (not just charge).
- A Chromium-based browser (Chrome, Edge, Brave, Arc).
- **Antenna attached.** Do not key up the radio without one.

### The process

1. Connect your board to your computer via USB.
2. Open [flasher.meshcore.co.uk](https://flasher.meshcore.co.uk).
3. Click **Connect** and select your device.
4. Click **Erase Device** — always start clean.
5. Pick the firmware for your role:
   - `Companion` for Companion nodes
   - `Repeater` for Repeaters
   - `RoomServer` for Room Servers
6. Make sure you pick the **US 915 MHz** variant. Other regions use different LoRa parameters and won't work here.
7. Click **Flash**. Wait for completion (about 90 seconds).

After flashing, the device reboots and shows the MeshCore splash with a short hex prefix of your public key.

If the flasher can't find your device:
- Try a different USB cable. The most common failure.
- On Windows, install the CP210x driver from Silicon Labs.
- On macOS, approve the connection in System Settings → Privacy & Security.

---

## Step 3: Configure by role

### Companion

1. Install the MeshCore app on your phone (iOS App Store or Google Play).
2. Pair with your node via Bluetooth. Default PIN is `123456`.
3. In the app, open your node's settings:
   - **Region**: `US Recommended`
   - **Name**: something short (16 chars max)
   - **Location**: enter lat/lon, or enable Advert Location Source if you have GPS
   - **Advert Location Source**: on
4. Send a **Flood Routed Advert** from the signal icon. Wait 2–3 minutes. Check [nhmesh.live](/) for your node.

See **[Your First Node](?section=first-node)** for more detail on this path.

### Repeater

Repeaters are configured via a web tool or CLI, not the phone app.

1. Connect your Repeater to a computer via USB.
2. Open [config.meshcore.dev](https://config.meshcore.dev) in Chrome.
3. Connect to the device.
4. Set:
   - **Name**: include the location (e.g., `Chester_Ledge`, `Mt_Major_Summit`)
   - **Location**: lat/lon entered manually with full precision. Repeaters never move, so nail it exactly.
   - **Admin Password**: change from the default `password` to something you'll remember
   - **Guest Password**: for users who want to query the repeater (optional)
   - **Public Key prefix**: verify it's unique on the local mesh (first few chars)
   - **Flood Advert**: on (so nearby nodes can discover it)
5. Save and reboot.

For physical install — weatherproofing, power, antenna — see **[Hardware, Antennas & Enclosures](?section=hardware-setup)** and **[Coverage & Placement](?section=coverage-placement)**.

### Room Server

Same as Repeater, plus:

- **Room names**: create the channels you want to host. The convention is `#townname` or `#topic` (short, lowercase, no spaces).
- **Room Admin Password**: controls who can configure rooms.
- **Public Access**: decide whether each room is discoverable (default yes) or by-invite.

Announce your Room Server in the Discord so people know it exists. Include the room names and which geographic area it serves.

---

## Step 4: Test

Regardless of role, the final step is confirming you're actually on the mesh.

1. Send a message on the `#nhmesh` hashtag channel.
2. Watch for responses.
3. Check [nhmesh.live](/) to see your node on the map.
4. Check [nhmesh.live/health-check](/health-check) to see which gateways can hear you.

If nothing is happening after 10 minutes, see **[Troubleshooting: Visibility](?section=troubleshooting-visibility)**.

---

## Step 5: Integrate with NHMesh (optional but encouraged)

If you want your node's packets to appear on our map and contribute to the gateway / collector ecosystem:

- **Companion nodes** don't need additional setup. Another observer will pick up your adverts and forward them automatically, as long as one is in range.
- **Repeater and Room Server operators** should consider running a dedicated observer — see **[Observer / Gateway Setup](?section=letsmesh-observer)**. An observer co-located with your infrastructure means every packet the node hears gets into our data pipeline.

---

## Key configuration values worth knowing

| Setting | Default | What it does |
|---|---|---|
| Region | Varies by flash | Sets LoRa parameters for regulatory compliance |
| TX Power | ~22 dBm | Output strength. Don't go above regional max |
| Coding Rate | 5 | LoRa error correction. Higher = more reliable but slower |
| Bandwidth | 62.5 kHz | Channel width. NHMesh standard |
| Spreading Factor | 7 | Modulation depth. Lower = faster but shorter range |
| Frequency | 910.525 MHz | Our primary channel. Do not change unless you know why |

The NHMesh community standard radio config is `910.525,62.5,7,5` (freq, bw, sf, cr). Most observer status messages include this string; if yours differs, you may be on a different channel than everyone else.

---

## Related guides

- **[Your First Node](?section=first-node)** — simpler quickstart version of this guide
- **[Hardware Picker](?section=hardware-picker)** — what to buy
- **[MeshCore Hashtag Channels](?section=meshcore-hashtag-channels)** — stewardship and the `#nhmesh` / `#nhhc` channels
- **[Observer / Gateway Setup](?section=letsmesh-observer)** — next step if you want to contribute to the map data
- **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** — if things don't work
