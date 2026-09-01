---
id: meshtastic-mqtt-setup
title: Meshtastic MQTT Client
section: setup
order: 5
last_reviewed: 2026-04-21
---

# Meshtastic MQTT Client Setup

This guide configures your Meshtastic node's built-in MQTT client so its packets reach **nhmesh.live**. Your node connects to our broker directly over WiFi or Ethernet; no Raspberry Pi or separate observer script required.

If you're running MeshCore, see **[Observer / Gateway Setup](?section=letsmesh-observer)** instead.

---

## Prerequisites

- A Meshtastic node with WiFi (ESP32-based boards: Heltec V3/V4, T-Beam, RAK 4631 with Wireless module, etc.). Nodes without WiFi can't use this path directly.
- Firmware 2.3.0 or later. Earlier versions had MQTT bugs that were since fixed.
- NHMesh MQTT credentials. Get them from the **[MQTT Setup page](?section=mqtt-auth)**.

---

## Configuration

Open the Meshtastic app (phone or web client) and navigate to **Module Configuration → MQTT**.

### Connection

| Field | Value |
|---|---|
| Enable MQTT Client | **On** |
| Broker Address | `mqtt.nhmesh.live` |
| Port | `1883` |
| Username | *(your NHMesh username)* |
| Password | *(your NHMesh password)* |
| TLS Enabled | **Off** |

### Topic

| Field | Value |
|---|---|
| Root Topic | `msh/US/NH` |

The `US/NH` path is what our collector watches for — publishes to `msh/US/<OTHER_STATE>` or to the default `msh/US` will still reach the broker but won't be picked up by our NH-focused ingestion.

### WiFi

If you haven't already:

- **Module Configuration → Network → WiFi** → set SSID and password.
- Save and reboot.

Once WiFi is connected and MQTT is enabled, the node will try to connect to the broker on every boot. The OLED (if present) shows "MQTT Connected" when it succeeds.

---

## Data flow modes

Meshtastic's MQTT module has an uplink/downlink model. Pick one.

### Uplink only (recommended for most)
Your node **publishes** its traffic to MQTT (so it appears on the map), but **does not** rebroadcast remote MQTT traffic to its local RF mesh.

- Enable Uplink: **On**
- Enable Downlink: **Off**

This is what we recommend unless you are specifically trying to bridge remote traffic into your local area. Downlink-enabled nodes add a lot of RF chatter, which gets expensive on airtime when there are many of them.

### Full bridge (advanced)
Both uplink and downlink on. Your node publishes local packets to MQTT **and** takes packets from MQTT and rebroadcasts them over your local RF mesh.

- Enable Uplink: **On**
- Enable Downlink: **On**

Only use this if you know why you want it. We have seen full-bridge nodes accidentally create message loops, flood the local mesh, and burn through a lot of airtime. If in doubt, stay uplink-only.

---

## Per-channel settings

For each channel you want included in MQTT:

- **Uplink enabled** must be on.
- **Downlink enabled** must be on if you chose the full-bridge mode above.

Default is **off** for both on most channels, so an "MQTT Connected" status does not mean traffic is actually flowing. Double-check each channel you care about.

---

## Verification

After saving and rebooting:

1. OLED (if present) should show "MQTT Connected" within 15 seconds.
2. Send a test message on a channel with uplink enabled.
3. Watch [nhmesh.live](/) — the message should appear within a minute.

If you don't see traffic:

- Check `mosquitto_sub -h mqtt.nhmesh.live -u USER -P PASS -t 'msh/#' -v` to see if your packets are at least reaching the broker. If they are, the issue is downstream (channel encryption or topic).
- See **[MQTT Troubleshooting → Step 3](?section=troubleshooting-mqtt)**.

---

## Common gotchas

### Region set to UNSET
Meshtastic's region affects the MQTT topic prefix. If your device shows region `UNSET`, set it to `US`. Otherwise your traffic goes to a topic we don't watch.

### Channel encryption
Our collector has the default `#nhmesh` channel PSK (pre-shared key) and a few other public NHMesh channels. If you're on a custom channel with a unique key, we can't decrypt your traffic even though we see it arrive. This is by design — the key is yours to keep.

### Firmware below 2.3.0
Older firmware had a bug where MQTT credentials weren't passed correctly in some configurations, causing auth failures that looked like broker issues. If you're below 2.3.0, update before debugging further.

---

## Related guides

- **[MQTT Setup](?section=mqtt-auth)** — broker credentials and general overview
- **[Meshtastic Channel Setup](?section=meshtastic-channel-setup)** — channel config and PSKs
- **[MQTT Troubleshooting](?section=troubleshooting-mqtt)** — when the connection isn't working
