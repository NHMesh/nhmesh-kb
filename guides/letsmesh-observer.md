---
id: letsmesh-observer
title: Observer / Gateway Setup
section: setup
order: 6
last_reviewed: 2026-04-21
---

# Observer / Gateway Setup

An **observer** (sometimes called a gateway) is a piece of software running on a small computer — a Raspberry Pi, a Mac Mini, an Intel NUC, whatever — that listens to its attached LoRa node and publishes everything it hears to an MQTT broker. Observers are how RF traffic becomes map data.

This guide covers setting up a MeshCore observer for NHMesh specifically. It assumes you've already picked hardware and flashed firmware — if you haven't, see **[Hardware Picker](?section=hardware-picker)** and **[Your First Node](?section=first-node)** first.

If you're running Meshtastic, you don't need an observer — the Meshtastic firmware has built-in MQTT. See **[Meshtastic MQTT Client Setup](?section=meshtastic-mqtt-setup)**.

---

## What an observer actually does

1. Connects to a LoRa node over USB/serial or Bluetooth.
2. Receives every RF packet the node hears (adverts, messages, status pings).
3. Publishes those packets to an MQTT broker in a structured format.

The node itself doesn't need to be anything special — a normal MeshCore Companion or Repeater works fine. Some operators dedicate a node to the observer role; others piggyback on a regular node that is also used for messaging. Either works.

---

## Pick your observer software

Several open-source observer implementations exist. The popular ones in our community:

| Software | Best for | Notes |
|---|---|---|
| **meshcore-packet-capture** | Raspberry Pi / Linux, set-and-forget | Small Python service, easy config, handles reconnection well |
| **meshcoretomqtt** | General purpose | Slightly older, widely deployed |
| **RemoteTerm** | Desktop use with a GUI | Good if you want to watch traffic live; has a Private MQTT integration for NHMesh |
| **Custom** | If you know what you're doing | Roll your own — our collector doesn't care as long as the topics are right |

We recommend **meshcore-packet-capture** for dedicated observer installs. It's the backbone of most of our current gateway fleet.

---

## Step 1: Install meshcore-packet-capture

Follow the official **[LetsMesh Observer Onboarding](https://analyzer.letsmesh.net/observer/onboard)** guide for the base install. It gets you a working observer publishing to LetsMesh.

Once that's running, come back here to add NHMesh as a second MQTT target.

---

## Step 2: Add NHMesh as a second MQTT server

meshcore-packet-capture supports multiple MQTT endpoints. Add ours as a secondary alongside LetsMesh.

### Get credentials
Visit the **[MQTT Setup page](?section=mqtt-auth)** and grab your NHMesh username and password.

### Configure the connection

In the observer's environment / config file, add:

```
PACKETCAPTURE_MQTT3_ENABLED=true
PACKETCAPTURE_MQTT3_HOST=mqtt.nhmesh.live
PACKETCAPTURE_MQTT3_PORT=1883
PACKETCAPTURE_MQTT3_USERNAME=<your-nhmesh-username>
PACKETCAPTURE_MQTT3_PASSWORD=<your-nhmesh-password>
```

### Configure the topics

This is where most people go wrong. **The topic structure matters.** NHMesh expects:

```
meshcore/<REGION>/<pubkey>/packets
meshcore/<REGION>/<pubkey>/status
meshcore/<REGION>/<pubkey>/raw
```

Where:
- `<REGION>` is a 3-letter IATA-style code for your general area. Current regions we track:
  - `CON` — Concord / central NH
  - `BOS` — Greater Boston and Eastern MA
  - `PVD` — Providence / Rhode Island
  - If your area doesn't fit any of these, pick the closest one or ask us in Discord to add a code.
- `<pubkey>` is your node's full 64-character public key in **uppercase** hex.

In the config:

```
PACKETCAPTURE_MQTT3_TOPIC_STATUS=meshcore/CON/<YOUR_PUBKEY>/status
PACKETCAPTURE_MQTT3_TOPIC_PACKETS=meshcore/CON/<YOUR_PUBKEY>/packets
PACKETCAPTURE_MQTT3_TOPIC_RAW=meshcore/CON/<YOUR_PUBKEY>/raw
```

Replace `CON` with your region and `<YOUR_PUBKEY>` with your actual hex. If your pubkey is `0B9467187B919F9A44143EC54BC75151DD5D12A86A0783A8031A48C478568C98`, it goes in verbatim.

---

## Step 3: Restart and verify

Restart the observer service (`systemctl restart`, `docker restart`, whatever fits your setup).

### Confirm it connected
Watch the observer logs for MQTT connection messages. You should see something like:

```
Connected to MQTT broker at mqtt.nhmesh.live:1883
```

### Confirm publishes are landing
Open **[nhmesh.live/observers](/observers)**. Your observer should appear within a couple of minutes under your chosen region, with status **ONLINE** and a recent heartbeat.

If it appears but is marked **DARK** or **OFFLINE**, check:

- **Topic format** — most common issue. Verify the `<REGION>` and `<pubkey>` are correct.
- **Bot heartbeat interval** — some observers only publish status every several minutes; wait a little longer.
- **See [MQTT Troubleshooting](?section=troubleshooting-mqtt)** for the full diagnostic flow.

---

## Common mistakes

### Using `meshcore/packets/` (or root)
Some observer defaults publish to a non-regional topic. Our collector will see these, but you lose per-region grouping and your observer won't appear on the **Observers** page correctly. Always use the full `meshcore/<REGION>/<pubkey>/` prefix.

### Lowercase pubkey
Our queries uppercase the pubkey for matching, but some older integrations assume lowercase. If your observer appears with two different entries (one lowercase, one uppercase hex), normalize your config to uppercase.

### Wrong region
An observer in Concord publishing under `BOS` still works — our collector ingests it — but it shows up under Boston on the regional rollup. Pick the right one.

### Observer publishes its own node's advert
Some observer implementations forward packets from their attached node back out over MQTT. That's expected. But if you expected to see a specific *other* node in your publishes and you only see your own, check what the observer is configured to forward.

---

## Running a dedicated vs. shared observer

### Dedicated (recommended for fixed infrastructure)
A Raspberry Pi Zero W with a node attached over USB, sitting next to your repeater, running meshcore-packet-capture as a systemd service. Draws about 1W. Boots unattended, reconnects on network loss, survives firmware updates. This is how most of our backbone runs.

### Shared (works for casual use)
Run the observer software on your desktop or laptop when you happen to be home. Simpler setup, no dedicated hardware, but coverage is spotty. Useful if you're just testing or don't have infrastructure ambitions.

---

## Related guides

- **[MQTT Setup](?section=mqtt-auth)** — credentials and broker basics
- **[Topic Hierarchy Reference](?section=topic-hierarchy)** — canonical topic structure
- **[MQTT Troubleshooting](?section=troubleshooting-mqtt)** — when the observer isn't publishing correctly
- **[Hardware, Antennas & Enclosures](?section=hardware-setup)** — physical build for a dedicated observer
