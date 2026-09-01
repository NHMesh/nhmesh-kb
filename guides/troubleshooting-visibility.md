---
id: troubleshooting-visibility
title: My Node Isn't on the Map
section: troubleshooting
order: 1
last_reviewed: 2026-04-21
---

# Troubleshooting: My Node Isn't on the Map

The single most common support request we get is some variation of: "I set everything up but my node isn't showing on nhmesh.live — what's wrong?" This guide is a symptom-first walk-through for that problem.

We organize it as a decision tree. Start at **Step 0**, answer the question, follow the branch. Most issues resolve within the first three steps.

If you have not yet gone through the initial setup, stop here and do **[Your First Node](?section=first-node)** first.

---

## Step 0: What does "not on the map" actually mean?

Clarify the symptom before chasing fixes. There are four distinct failure modes and they have different causes:

| Symptom | Most likely cause | Jump to |
|---|---|---|
| My node doesn't appear on the map at all, ever | No gateway is hearing my node's packets | Step 1 |
| My node appears but has no position (showing at 0,0 or off-screen) | Lat/lon not being published in adverts | Step 4 |
| My node appears but my messages don't show up in channels | MQTT bridging issue, or channel mismatch | Step 5 |
| My node was on the map yesterday but isn't now | It has gone stale (no recent adverts) | Step 6 |

Pick your row and follow that step.

---

## Step 1: Is your node broadcasting adverts?

An **advert** is how a MeshCore or Meshtastic node announces itself to the mesh. Without an advert, no gateway can forward your existence to the infrastructure.

**How to check:**

- **MeshCore app:** open your node, tap the signal / broadcast icon, send a **Flood Routed Advert**. Do this three times with about 30 seconds between each.
- **Meshtastic:** just power it on and leave it running. Meshtastic broadcasts adverts automatically every ~15 minutes.
- **CLI:** connect over USB serial and run `advert` (MeshCore) or check log lines for `SendPosition` (Meshtastic).

After sending three adverts, wait about 2 minutes, then refresh **nhmesh.live**.

If still nothing: move to Step 2.

---

## Step 2: Is any NHMesh gateway in RF range of your node?

Adverts are radio transmissions. They can only reach an MQTT gateway if a gateway is within LoRa range of your node. Our gateways are listed on the **[Observers page](/observers)**.

**How to check:**

- Open the **Observers** tab on nhmesh.live. You will see all ~30 active gateways and their approximate locations.
- Is the nearest one within 5–10 miles of you, with reasonable line-of-sight (no large hills between you)?

**If no gateway is nearby:** this is the most likely cause. LoRa is line-of-sight limited, and 915 MHz punches through trees but not hills. Options:

- **Move.** Try sending adverts from a higher elevation (top of a hill, a car park with a view, an upper-floor window).
- **Be patient.** If someone has their Companion node in the area and it's a zero-hop relay to a gateway, your advert might get through once they are online.
- **Ask in Discord.** The community can tell you who is active near you and whether they are currently relaying.
- **Put up a repeater.** If the nearest gateway is too far, consider running a MeshCore Repeater of your own. See **[Coverage & Placement](?section=coverage-placement)**.

**If a gateway is nearby but still nothing:** move to Step 3.

---

## Step 3: Is your radio actually transmitting?

Some failures look like "I'm not being heard" but the real issue is "I'm not transmitting cleanly." Common causes:

### TX power set too low
- **MeshCore:** default is around 22 dBm. If you see something like 10 dBm in your config, that is much too low for any useful range. Bump it to 20–22 dBm.
- **Meshtastic:** same. Default is fine; if someone changed it, reset.

### Antenna issue
- **Is an antenna actually connected?** Transmitting without an antenna can damage the radio permanently. If you suspect you transmitted for a while without one connected, the radio may be silent even though it looks like it's working.
- **Is the U.FL connector fully seated?** On a Heltec V4 this is a common fault — a tiny click that didn't happen. Unplug, reconnect, listen for a definite seat.
- **Is the antenna tuned to 915 MHz?** A 433 MHz or 868 MHz antenna will radiate almost nothing at 915 MHz.

### Board-specific bugs
- **Heltec V4 low receive sensitivity:** there is a known bug in some firmware builds where the LNA is disabled on boot. From the CLI, run `radio.rxgain on`. See **[Troubleshooting Firmware](?section=troubleshooting-firmware)**.
- **Clock drift:** if your node's clock is significantly wrong (hours or days off), some mesh operations misbehave. From CLI: `time.sync`.

If none of the above: try Step 4.

---

## Step 4: Is your node publishing its location?

A node without a location appears in our database but not on the map. Check:

### MeshCore
- Open the app → your node → Radio settings.
- **Lat/Lon:** must be non-zero. If you don't want to share your exact home address, fuzz it by a few tenths of a mile — the map just needs a point.
- **Advert Location Source:** should be **enabled**. Without this, your lat/lon is not included in adverts.

### Meshtastic
- In the app: Settings → Position → set your device location and make sure **Fixed Position** or **GPS** is configured.

After changing these, send an advert and wait a few minutes.

---

## Step 5: My node is on the map but my messages aren't showing up

This is a different problem from visibility. Your node is reaching a gateway. Your messages are either not being published to the public channels, or they're on a channel we don't bridge.

**Check:**

- **Which channel are you messaging on?** We monitor `#nhmesh`, `#nhhc`, and the MeshCore public channel. DMs are private and won't appear.
- **Are you on the right primary channel?** As of 2026, Meshtastic users should have `NHMesh` as Channel 0 (primary). See **[Switching to Medium Fast](?section=switching-to-medium-fast)**.
- **MQTT configuration:** if you are relying on MQTT to relay rather than radio, see **[MQTT Troubleshooting](?section=troubleshooting-mqtt)**.

---

## Step 6: My node was working and now it isn't

Stale node. Common causes:

- **Battery died.** Check the device, charge it.
- **Clock drifted.** Especially after extended power-off. Reconnect, sync time, send advert.
- **Firmware update.** If you recently flashed a new firmware, your config may have reset. Re-enter region, name, channel.
- **Gateway outage.** Check the **[Observers page](/observers)** — if the gateway nearest you is OFFLINE or DEGRADED, that is why no one is hearing you.

---

## Still stuck?

In Discord, post:

- Your node's hardware (e.g., "Heltec V4")
- Firmware and version (e.g., "MeshCore Companion v1.14.1")
- Your general location (town is fine)
- A screenshot of your radio config
- What you've tried

Someone will respond within an hour during waking hours. The community has solved every variation of this problem.

---

## Related guides

- **[MQTT Troubleshooting](?section=troubleshooting-mqtt)** — if you suspect MQTT is the issue
- **[Firmware Bugs & Recovery](?section=troubleshooting-firmware)** — known bugs per firmware version
- **[Coverage & Placement](?section=coverage-placement)** — will a repeater at my house help?
