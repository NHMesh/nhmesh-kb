---
id: mqtt-auth
title: MQTT Setup
section: setup
order: 4
last_reviewed: 2026-04-21
---

# MQTT Setup

MQTT is how we bridge the radio mesh to the internet — specifically, how your node's packets reach **nhmesh.live**, the observer fleet, and the LetsMesh integration. This guide walks through getting connected to our broker end-to-end.

If you just need to debug an MQTT problem you've already set up, skip to **[MQTT Troubleshooting](?section=troubleshooting-mqtt)**.

---

## What you're configuring

```
your node ──(RF)──▶ gateway/observer ──(MQTT)──▶ mqtt.nhmesh.live ──▶ collector ──▶ live map
```

Or, if you're running your own observer that publishes directly:

```
your observer ──(MQTT)──▶ mqtt.nhmesh.live ──▶ collector ──▶ live map
```

Either way, you need **credentials** for the broker and a **topic** your publishes land under. The rest of this guide is about getting those two things right.

---

## Step 1: Get credentials

1. Sign in to [nhmesh.live](/) with Discord. This is also how we set your MQTT username.
2. The **MQTT Self-Service** tool on this page generates or resets your password. Your username is derived from your Discord identity.
3. Save the password somewhere safe. We do not store it in plain text on our end — if you lose it, you reset and get a new one.

Broker details are the same for everyone:

| Setting | Value |
|---|---|
| **Host** | `mqtt.nhmesh.live` |
| **Port** | `1883` |
| **Username** | *(from the self-service tool above)* |
| **Password** | *(from the self-service tool above)* |
| **Encryption** | Disabled (plain TCP — our edge terminates TLS internally) |

---

## Step 2: Pick your integration path

Different devices and observer scripts want slightly different config.

### Meshtastic nodes
See **[Meshtastic MQTT Client Setup](?section=meshtastic-mqtt-setup)** for the full walk-through. Short version: enable the MQTT module in the app, point it at the broker above, and set the root topic to `msh/US/NH`.

### MeshCore observers (meshcore-packet-capture, meshcoretomqtt, RemoteTerm)
See **[Observer / Gateway Setup](?section=letsmesh-observer)** for the full walk-through. Short version: configure your observer script to publish to `meshcore/<REGION>/<pubkey>/(packets|status|raw)` where `<REGION>` is a 3-letter code for your area (`CON`, `BOS`, `PVD`, etc.).

### Something else
As long as you can speak MQTT 3.1/5 and publish to our broker with valid credentials, you're fine. The canonical topic formats are documented in **[Topic Hierarchy Reference](?section=topic-hierarchy)**.

---

## Step 3: Verify

The fastest way to confirm you're connected is to subscribe to your own traffic with a separate tool and watch it land:

```
mosquitto_sub -h mqtt.nhmesh.live -p 1883 \
  -u YOUR_USERNAME -P YOUR_PASSWORD \
  -t 'meshcore/#' -v
```

You should see a stream of messages from the whole fleet, including your own once your node starts publishing. If nothing shows up:

- Try `-t '#'` (subscribe to all topics) — if you now see Meshtastic traffic under `msh/...`, the broker is fine and the issue is specific to your topic.
- Check the **[Observers page](/observers)** — if your node isn't there after a few minutes, your publishes aren't reaching the broker at all. See **[MQTT Troubleshooting](?section=troubleshooting-mqtt)**.

---

## A few things worth knowing

### Your credentials are per-person, not per-device
You can run a Meshtastic node, a MeshCore observer, and a test subscription with the same username and password. The broker does not care.

### Passwords are reset, not retrieved
If you forget your password, you reset. Our broker validates against a bcrypt hash; nobody (including us) can read the original.

### ACLs are granted automatically
When your user is created, a DB trigger adds a wildcard ACL so you can publish and subscribe to any `meshcore/#` or `msh/#` topic. If you ever hit a "not authorised" error on a topic that should work, tell us in Discord — we've had a few edge cases where the trigger didn't fire and we had to backfill manually.

### Plain TCP, not TLS
Our public broker is currently plaintext on port 1883. Traffic on the mesh is already broadcast unencrypted over RF, so the incremental privacy loss of a cleartext MQTT hop is minimal, and a lot of embedded devices don't handle TLS gracefully. If you care about transport encryption, tunnel through SSH or a VPN. We may add TLS on a separate port in the future.

---

## Related guides

- **[Meshtastic MQTT Client Setup](?section=meshtastic-mqtt-setup)** — Meshtastic-specific config
- **[Observer / Gateway Setup](?section=letsmesh-observer)** — MeshCore observer config
- **[Topic Hierarchy Reference](?section=topic-hierarchy)** — canonical topic structure
- **[MQTT Troubleshooting](?section=troubleshooting-mqtt)** — when something isn't working
