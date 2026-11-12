---
id: health-check
title: Using the Health Check
section: troubleshooting
order: 4
last_reviewed: 2026-11-12
---

# Using the Health Check

The Health Check is a lightweight tool we built to help you answer one question: **does the mesh actually reach me right now?**

You send a short test code through the `#nh-hc` channel from your MeshCore radio, and the page shows which observers heard it, how many hops it took and at what signal strength. Think of it as a one-shot speed test for LoRa coverage. It is MeshCore only.

This guide explains how to use it, when it's useful, and how to interpret the results.

---

## What it is

Health Check is a page at [nhmesh.live/health-check](/health-check) with two tools:

1. **Test code**: the page generates a code (`NHC-XXXXXX`). You send it on `#nh-hc` from your MeshCore radio (the page does not transmit anything). It then listens for that message in our collector and lists every observer that heard it.
2. **Node lookup** ("Is my node alive?"): type a node name or the start of its public key and see which observers heard it in the last hour and 24 hours. No code needed. This is the quick check for a repeater.

The test results show a verdict plus, per observer, hop count, SNR, RSSI and when it arrived relative to the first observer. Results usually start appearing within a few seconds of your message and the page keeps watching for 20 minutes.

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

1. Go to [nhmesh.live/health-check](/health-check) and press **Generate Code**.
2. In your MeshCore app, send the code as a message on the `#nh-hc` hashtag channel (add the channel if you do not have it).
3. The page shows observers as they report in.

The results show:

- **Verdict** (Excellent, Good, Marginal or Not heard) with a one-line reason, for example "Heard within 1 hop by 3 of the 5 nearest observers, best SNR +8 dB".
- **Per observer**: hops (direct, 1 hop, 2 hops...), SNR and RSSI where the observer reports them, and arrival time relative to the first observer. Some observers do not report signal data, those show a dash.
- **A map** of active observers: green dots heard you, grey did not, and a dashed ring marks the five nearest to your node.

### How the verdict works

It is based on where you are, not on how many observers exist statewide. We take the five observers nearest your node's last known position (or, if the node has no position, the observers that heard it directly) and look at how many of them heard the test within one hop, plus the best SNR.

- **Excellent**: most of the nearest observers hear you within one hop and SNR is healthy.
- **Good**: at least a couple of the nearest observers hear you, directly or by relay.
- **Marginal**: heard, but by few observers or with weak signal.
- **Not heard**: no observer received it.

### Looking up a node

Use **Is my node alive?** and enter a name or the first characters of the public key. If several nodes match you get a list to pick from. You see how many observers heard the node in the last hour and 24 hours, adverts and relayed packets heard, the last advert age, and per-observer SNR. MeshCore only identifies repeaters in a packet path by a short key prefix, so the page tells you when other nodes share your prefix and the relay evidence is less certain.

---

## How to interpret the results

### No observer heard anything
Either you're out of RF range of all our observers, or your node isn't transmitting. Work through **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** Steps 1–3.

### One observer heard you with low SNR (-10 or worse)
You're on the edge of reach. A better antenna or a slightly higher install point would help a lot. See **[Hardware, Antennas & Enclosures](?section=hardware-setup)**.

### Multiple observers heard you, all with healthy SNR (+5 or better)
You're well-connected. Nothing to do.

### Observers heard you but only after several hops
Your node isn't in direct range of any observer, you're being relayed through intermediate nodes. This is fine for messaging, but:

- Every hop adds latency and airtime.
- If the intermediate nodes go offline, so does your connectivity.
- Consider whether a higher-elevation install or a small local repeater would give you a direct-to-gateway path.

---

## Stewardship: please don't spam

Health Check uses its own `#nh-hc` hashtag channel so test messages stay separate from normal conversation. A test still uses airtime because repeaters flood it. Guidelines:

- **One health check per relocation** is reasonable.
- **Rapid-fire repeated checks** (more than once a minute) add up. Your ping is a few hundred bytes; multiply by every repeater relaying and it's real airtime.
- **War-driving?** Use `#nh-hc` with single pings per stop, not continuous broadcasts.

See **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** for the full airtime etiquette.

---

## How it works under the hood

- Your test message is a normal MeshCore channel message on `#nh-hc`.
- Our observers (listed on **[Observers](/observers)**) forward everything they hear to our MQTT broker.
- The collector records every reception: which observer heard which packet, its path, hop count, SNR and RSSI.
- The Health Check page finds your code in the message log, matches it to those receptions, and renders the result. Results for a code stay available for 24 hours (tests older than the reception log may show observers without hop or signal data).

There is no magic. It's the same path every normal message takes, we're just giving you a focused view of what happened to one specific message.

---

## Related guides

- **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** — when Health Check shows no gateways
- **[Coverage & Placement](?section=coverage-placement)** — when Health Check shows weak signal
- **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** — why we use `#nh-hc`
