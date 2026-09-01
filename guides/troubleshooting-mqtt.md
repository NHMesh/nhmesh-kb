---
id: troubleshooting-mqtt
title: MQTT Isn't Working
section: troubleshooting
order: 2
last_reviewed: 2026-04-21
---

# Troubleshooting: MQTT

MQTT is the internet-side bridge that lets our map, observer fleet, and LetsMesh integration see what is happening on the mesh. When people say "MQTT isn't working" they usually mean one of three distinct things:

| What you mean | What's actually wrong | Jump to |
|---|---|---|
| I can't log in to the NHMesh MQTT broker | Credentials or ACL | Step 1 |
| I logged in but my packets aren't showing up | Topic or intent config | Step 2 |
| My Meshtastic node says "MQTT connected" but messages don't appear on nhmesh.live | Channel encryption or region mismatch | Step 3 |

Pick your row. If you don't know yet, start at Step 1.

---

## Step 1: Can you authenticate to the broker?

**Broker:** `mqtt.nhmesh.live` on port `1883` (unencrypted TCP, internal cluster does TLS).

**Credentials** are per-user. You need to sign into [nhmesh.live](/) with Discord first, then visit the **[MQTT Setup guide](?section=mqtt-auth)** to generate / reset your password. The page will show you the exact username and password string to use.

**Test with mosquitto_sub:**

```
mosquitto_sub -h mqtt.nhmesh.live -p 1883 -u YOUR_USERNAME -P YOUR_PASSWORD -t 'meshcore/#' -v
```

You should see a stream of packet and status messages. If instead you see:

- **"Connection Refused: bad user name or password"** → your credentials are wrong. Reset on the MQTT Setup page.
- **"Connection Refused: not authorised"** → you authenticated but your ACL grant is missing. This was a known issue for several accounts in April 2026; we've since backfilled ACLs for all provisioned users, but if your account is new and you hit this, ask in Discord and we can check.
- **No output, but no errors** → you're connected and subscribed, but no traffic is flowing. Either the broker is quiet at that moment, or you subscribed to the wrong topic. Try `-t '#'` to see everything.

**Not installed locally?** Use a container:

```
docker run --rm -it eclipse-mosquitto mosquitto_sub \
  -h mqtt.nhmesh.live -p 1883 -u USER -P PASS -t 'meshcore/#' -v
```

---

## Step 2: You're connected, but your packets aren't landing

This is the most common phase of the problem. You've configured your node to publish to the broker, it connects successfully, but **nhmesh.live** doesn't see anything.

### The canonical topic hierarchy

NHMesh expects publishers to use a topic structure that lets us group by region. The canonical form for a MeshCore observer is:

```
meshcore/<REGION>/<pubkey>/packets
meshcore/<REGION>/<pubkey>/status
```

Where `<REGION>` is a 3-letter IATA-style code for your area (e.g., `CON` for Concord, `BOS` for Boston, `PVD` for Providence). `<pubkey>` is your node's full 64-char public key in uppercase hex.

**Common mis-configurations we see:**

| What people publish to | What's wrong |
|---|---|
| `meshcore/packets/` | No region code, non-canonical. Collector ignores it. |
| `meshcore/gateway/packets` | Older default, still accepted but loses per-node grouping |
| `meshcore/` (root) | Some clients default here — works but noisy |
| `meshcore/CON/<pubkey>/packets` | Canonical, what we want |

If your client lets you specify a topic prefix, use `meshcore/<YOUR_REGION>/<YOUR_PUBKEY>` and let the client append `/packets` and `/status`.

### meshcore-packet-capture (most common observer client)

In the config:

```
PACKETCAPTURE_MQTT3_TOPIC_STATUS=meshcore/<REGION>/<PUBKEY>/status
PACKETCAPTURE_MQTT3_TOPIC_PACKETS=meshcore/<REGION>/<PUBKEY>/packets
PACKETCAPTURE_MQTT3_TOPIC_RAW=meshcore/<REGION>/<PUBKEY>/raw
```

### RemoteTerm / Private MQTT

If you're setting up an observer through RemoteTerm, the **Private MQTT** integration tends to work more reliably than the Community MQTT integration, at least based on community experience. The difference is subtle and not fully documented upstream — use Private MQTT first, switch to Community if it doesn't work.

### Check the Observers page

Go to [nhmesh.live/observers](/observers). If your node is actively publishing, it will appear in the list within ~60 seconds of a heartbeat. The page shows:

- Whether your observer is ONLINE (fresh heartbeat), DEGRADED (errors or stale), OFFLINE (> 24h silent), or DARK (provisioned in our user table but never heartbeat'd).
- Which region your publishes are being tagged under.
- Last heartbeat timestamp.

If you are **DARK** despite configuring everything, your publishes are not reaching our broker at all. Most likely your topic is wrong or you're pointing at a different broker. Use `mosquitto_sub` from Step 1 to verify you can see your own traffic when subscribed to `meshcore/#`.

---

## Step 3: Meshtastic says "MQTT connected" but nothing appears

Meshtastic's MQTT integration is different from the MeshCore observer flow. A Meshtastic node publishes to a Meshtastic-formatted topic hierarchy, not the `meshcore/` one.

**The topic:** `msh/US/NH/<your-gateway-id>/<channel>`

For NHMesh, you want `msh/US/NH/...`.

### Common issues

**"Encrypted" channel traffic not showing up on the map:**
Our collector decrypts channels for which we have the pre-shared key. The default `#nhmesh` channel key is public and shared with every member. If you're on a custom channel with a key nobody else has, your traffic won't be decoded. This is by design.

**Region set to something other than US:**
Meshtastic's region setting affects the MQTT topic prefix. Confirm your device is set to `US` or `UNSET` → `US`.

**Uplink / Downlink disabled per channel:**
In the Meshtastic channel settings, both **Uplink enabled** and **Downlink enabled** must be on for the channel you want bridged. Uplink-only still publishes to MQTT but your node won't receive replies.

**See [Meshtastic MQTT Client Setup](?section=meshtastic-mqtt-setup)** for the full config walk-through.

---

## Quick diagnostic table

| Symptom | First thing to check |
|---|---|
| `mosquitto_sub` returns "bad user name or password" | Reset MQTT password on the setup page |
| `mosquitto_sub` returns "not authorised" | Ask in Discord — your ACL may be missing |
| `mosquitto_sub` works but shows no traffic | Try `-t '#'` (subscribe to everything) to confirm broker is live |
| Observer appears DARK on `/observers` | Your publishes aren't reaching the broker — topic or network issue |
| Observer appears DEGRADED with errors > 0 | Check your client logs; queue backup or hardware issue |
| Observer ONLINE but no packets in the DB | Topic format wrong; check Step 2 |
| Meshtastic node shows MQTT connected but nothing on map | Region not US, uplink disabled, or custom channel key |

---

## Related guides

- **[MQTT Setup](?section=mqtt-auth)** — credentials and broker config
- **[Observer / Gateway Setup](?section=letsmesh-observer)** — full observer walk-through
- **[Topic Hierarchy Reference](?section=topic-hierarchy)** — canonical topic structure
