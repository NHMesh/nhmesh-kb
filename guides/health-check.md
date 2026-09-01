---
id: health-check
title: Using the Health Check
section: troubleshooting
order: 4
last_reviewed: 2026-04-21
---

# Using the Health Check

The Health Check is a lightweight tool we built to help you answer one question: **does the mesh actually reach me right now?**

It sends a single ping through the `#nhhc` channel and tracks which gateways heard it. Think of it as a one-shot speed test for LoRa coverage.

This guide explains how to use it, when it's useful, and how to interpret the results.

---

## What it is

Health Check is a page at [nhmesh.live/health-check](/health-check) that:

1. Triggers a small test message from your node (or asks you to send one manually).
2. Listens for that message landing in our collector from any of our ~30 gateways.
3. Shows you which gateways picked it up, with RSSI and SNR.

The whole round trip takes about 10 seconds. It's designed to be cheap enough to run frequently without stressing the airtime budget.

---

## When to use it

### Before you add a new node
- You've picked a location for a repeater. Health Check confirms the spot actually reaches our gateways before you commit to the install.

### When you just moved
- Drove to a new spot, want to know if you're on the mesh. One check tells you what you're hearing and who's hearing you.

### When something feels off
- Messages weren't delivered, map looks weird. Health Check is a fast "is my node even working" signal.

### After firmware changes
- Flashed a new build or changed TX power? Health Check tells you immediately if the change helped or hurt.

---

## How to run one

1. Go to [nhmesh.live/health-check](/health-check).
2. The page will prompt you to send a specific test payload from your node — typically via the `#nhhc` hashtag channel.
3. In your MeshCore or Meshtastic app, send that payload on `#nhhc`.
4. The page watches for the payload to appear in our packet stream and displays the results.

The results panel shows:

- **Gateways that heard you** with their location, RSSI (signal strength), and SNR (signal quality).
- **Propagation time** from send to receipt.
- **Hop count** if your packet traveled through intermediate nodes.

---

## How to interpret the results

### No gateway heard anything
Either you're out of RF range of all our infrastructure, or your node isn't transmitting. Work through **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** Steps 1–3.

### One gateway heard you with low SNR (-10 or worse)
You're on the edge of reach. A better antenna or a slightly higher install point would help a lot. See **[Hardware, Antennas & Enclosures](?section=hardware-setup)**.

### Multiple gateways heard you, all with healthy SNR (+5 or better)
You're well-connected. Nothing to do.

### Gateways heard you but the message took several hops
Your node isn't in direct range of any gateway — you're being relayed through intermediate nodes. This is fine for messaging, but:

- Every hop adds latency.
- If the intermediate nodes go offline, so does your connectivity.
- Consider whether a higher-elevation install or a small local repeater would give you a direct-to-gateway path.

---

## Stewardship: please don't spam

Health Check is on the `#nhhc` hashtag channel exactly so normal mesh traffic doesn't see the flood of test pings. But `#nhhc` still uses airtime. Guidelines:

- **One health check per relocation** is reasonable.
- **Rapid-fire repeated checks** (more than once a minute) add up. Your ping is a few hundred bytes; multiply by 30 gateways relaying and it's real airtime.
- **War-driving?** Use `#nhhc` with single pings per stop, not continuous broadcasts.

See **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** for the full airtime etiquette.

---

## How it works under the hood

- Your test message is sent like any other `#nhhc` packet.
- Our gateways (listed on **[Observers](/observers)**) forward everything they hear to our MQTT broker.
- The collector records each packet with its gateway of origin, RSSI, and SNR.
- The Health Check page queries our packet log for the specific payload you sent, and renders the results.

There is no magic. It's the same path every normal message takes — we're just giving you a focused view of what happened to one specific ping.

---

## Related guides

- **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** — when Health Check shows no gateways
- **[Coverage & Placement](?section=coverage-placement)** — when Health Check shows weak signal
- **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** — why we use `#nhhc`
