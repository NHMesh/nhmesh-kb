---
id: topic-hierarchy
title: MQTT Topic Hierarchy
section: reference
order: 1
last_reviewed: 2026-04-21
---

# MQTT Topic Hierarchy Reference

This is a reference for how our MQTT broker's topic space is organized. If you're writing a client that publishes to or subscribes from **mqtt.nhmesh.live**, this document is the source of truth for topic naming.

For the why and how of MQTT setup, see **[MQTT Setup](?section=mqtt-auth)**. This guide is just the canonical namespace.

---

## Namespace overview

```
meshcore/                          (MeshCore protocol)
  <REGION>/                        3-letter IATA-style region code
    <pubkey>/                      node's 64-char uppercase hex public key
      packets                      received LoRa packets (JSON)
      status                       periodic heartbeats (JSON)
      raw                          raw byte-level packet captures (JSON)

msh/                               (Meshtastic protocol)
  US/                              region (always US for NHMesh)
    NH/                            state
      <gateway_id>/                Meshtastic gateway ID
        <channel>                  channel name or ID
        ...
```

---

## MeshCore topics

### `meshcore/<REGION>/<pubkey>/packets`

Every LoRa packet the observer hears. Published as JSON.

**Example topic:**
```
meshcore/CON/0B9467187B919F9A44143EC54BC75151DD5D12A86A0783A8031A48C478568C98/packets
```

**Example payload:**
```json
{
  "origin": "TrickyNodee",
  "origin_id": "0B9467187B919F9A44143EC54BC75151DD5D12A86A0783A8031A48C478568C98",
  "timestamp": "2026-04-21T12:37:31.245000",
  "type": "PACKET",
  "direction": "rx",
  "payload_type": "0",
  "route": "F",
  "raw": "15007A70AB881EB15AFD147851BF2DEE9EC7E23F6F4C580BCF0233FD3CD4ADF25B38A70C32",
  "snr": 12.5,
  "rssi": -65
}
```

### `meshcore/<REGION>/<pubkey>/status`

Periodic observer heartbeat. Published every ~60 seconds, usually.

**Example payload:**
```json
{
  "status": "online",
  "timestamp": "2026-04-21T13:15:42.123456",
  "origin": "Cheesefish Producer",
  "origin_id": "09BD6FC7...",
  "model": "Heltec V3",
  "firmware_version": "v1.14.1-467959c (Build: 20-Mar-2026)",
  "radio": "910.525,62.5,7,5",
  "client_version": "meshcore-packet-capture/1.2.1-1bd909c",
  "stats": {
    "battery_mv": 4017,
    "uptime_secs": 299000,
    "errors": 0,
    "queue_len": 0,
    "noise_floor": -111,
    "last_rssi": -64,
    "last_snr": 12.5,
    "tx_air_secs": 12,
    "rx_air_secs": 7642
  }
}
```

### `meshcore/<REGION>/<pubkey>/raw`

Raw packet dumps. Used for forensics and less-common integrations; our live collector primarily uses `packets`.

---

## Meshtastic topics

### `msh/US/NH/<gateway_id>/...`

Standard Meshtastic MQTT topic. NHMesh watches anything under `msh/US/NH/`.

The `<gateway_id>` is the Meshtastic gateway node's short ID (8-char hex, preceded by `!`). Beneath that, Meshtastic structures topics by channel and subtopic automatically.

**Examples:**
```
msh/US/NH/!435ae460/2/e/LongFast/!abc12345
msh/US/NH/!1c11710c/2/e/NHMesh/!def67890
msh/US/NH/peter/!1c11710c
```

The exact structure is defined by the Meshtastic firmware and documented in the [Meshtastic MQTT spec](https://meshtastic.org/docs/configuration/module/mqtt/).

---

## Region codes

| Code | Area |
|---|---|
| `CON` | Concord / central NH |
| `BOS` | Greater Boston and Eastern MA |
| `PVD` | Providence / Rhode Island |

If your area doesn't fit any of these, pick the closest one. If none make sense, propose a new 3-letter code in Discord — we can add it.

---

## Common mistakes

### Publishing to `meshcore/packets/...`
This is a legacy / non-canonical pattern that some older observer defaults produced. Our collector still ingests it but you lose per-region grouping. Always use `meshcore/<REGION>/<pubkey>/...`.

### Publishing to root `meshcore/`
Similarly non-canonical. Works in a crude sense but we cannot attribute the traffic to a specific observer. Use the full hierarchy.

### Lowercase pubkey
Our queries normalize to uppercase, but some clients publish in lowercase. This generally works but can cause you to appear twice in the Observers page if the DB has entries under both cases. Always use uppercase.

### Missing region
Some observer scripts omit the region segment entirely: `meshcore/<pubkey>/packets`. Technically ingested but loses the region attribution we use for the Observers page rollup.

---

## For subscribers / integrators

If you want to consume the NHMesh MQTT stream programmatically:

- **Credentials:** same broker, same user account path as publishers. See **[MQTT Setup](?section=mqtt-auth)**.
- **Subscribe pattern:** `meshcore/#` gets everything MeshCore-side; `msh/US/NH/#` gets Meshtastic traffic.
- **Filter per-region:** `meshcore/CON/#` subscribes to just the Concord-area observer publishes.
- **Filter per-observer:** `meshcore/+/<pubkey>/#` subscribes to a specific observer regardless of region.

---

## Ownership and changes

The topic namespace is stable but not frozen. If we need to evolve it, we'll publish deprecation notices in the `#nhmesh` Discord channel and keep old patterns ingestable for at least a release cycle.

Questions or suggestions go to Discord or the `#nhmesh` hashtag channel on the mesh itself.

---

## Related guides

- **[MQTT Setup](?section=mqtt-auth)** — credentials and broker basics
- **[Observer / Gateway Setup](?section=letsmesh-observer)** — publisher configuration
- **[MQTT Troubleshooting](?section=troubleshooting-mqtt)** — when something isn't working
