---
id: troubleshooting-firmware
title: Firmware Bugs & Recovery
section: troubleshooting
order: 3
last_reviewed: 2026-04-21
---

# Troubleshooting: Firmware Bugs & Recovery

This guide is a running log of known firmware issues and their workarounds, plus general recovery procedures for when a node gets into a bad state. Entries here come from real support conversations in our Discord — if you hit something that isn't listed, tell us and we'll add it.

---

## Recovery: "my node was working and just stopped"

Before assuming a firmware bug, walk through the quick checks:

1. **Power cycle.** Unplug USB / pull the battery. Wait 30 seconds. Reconnect.
2. **Clock sync.** From the CLI (MeshCore) or app (Meshtastic), sync time. Clock drift is a common silent cause of flaky behavior.
3. **Check the config.** Firmware updates sometimes reset config. Re-verify region, name, channel, lat/lon.
4. **Send a fresh advert.** If you're on MeshCore, send three floods. If you're on Meshtastic, reboot to force an immediate position broadcast.
5. **Verify you're on the right firmware version.** Some bugs are specific to a build. Check the version in the app or on the OLED.

If none of the above fixes it, see the specific issue lists below.

---

## Known MeshCore bugs

### Heltec V4 — deaf receiver (LNA disabled)
- **Affects:** some Heltec V4 Companion/Repeater builds around firmware 1.14.x.
- **Symptom:** node TX works fine (other people see your adverts), but your node hears nothing. CLI shows 0 packets received over long periods.
- **Workaround:** from the CLI, run:
  ```
  radio.rxgain on
  ```
  This stays set until the next reboot. If you need it persistent, add it to your startup script or update to firmware 1.15+ where it was fixed upstream.
- **Upstream tracking:** [meshcore-dev/MeshCore#2145](https://github.com/meshcore-dev/MeshCore/issues/2145)

### Advert with lat/lon = 0,0
- **Affects:** nodes that haven't configured a location.
- **Symptom:** node appears in our database but never on the map, or the collector logs errors about `check_latitude_longitude_not_zero`.
- **Workaround:** set a real location (see **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** Step 4) and send a new advert. On our side, we've also patched the collector to skip 0,0 positions cleanly rather than rolling back the transaction — so this matters less than it used to.

### Tapback / reply interactions stop working
- **Affects:** some MeshCore iOS/Android app versions.
- **Symptom:** tapping to react to a message silently fails.
- **Workaround:** force-quit the app, relaunch. If that doesn't work, unpair and re-pair the Bluetooth connection. A full app reinstall has resolved it when nothing else would.

### Max Retransmission error
- **Affects:** nodes trying to DM another node that's out of reach.
- **Symptom:** the app shows "Max Retransmission" after several retries.
- **Meaning:** you sent a DM and the destination didn't acknowledge after the configured retry count. Either the destination is offline, or the path is too lossy. Try sending on the `#nhmesh` hashtag channel instead, where ACKs aren't required.

---

## Known Meshtastic issues

### Default channel (Channel 0) mismatch after MF switchover
- **Affects:** anyone who was on LongFast before the 2026 Medium Fast transition.
- **Symptom:** you switch to Medium Fast, but the `NHMesh` channel is still at Channel 1 instead of Channel 0.
- **Workaround:** delete the default LongFast channel at position 0, then re-add NHMesh as Channel 0. See **[Switching to Medium Fast](?section=switching-to-medium-fast)**.

### Flood-happy mobile nodes
- **Affects:** Companion nodes that move frequently and can't find their way back to peers.
- **Symptom:** your node floods the mesh every time you move, consuming airtime unnecessarily.
- **Workaround:** configure your node as Client_Mute when moving (doesn't repeat others, still sends its own). See **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** for our recommendations on minimizing flood traffic.

---

## "My device bricked during a firmware flash"

Not usually as bad as it sounds. The recovery path depends on the board:

### Heltec V3 / V4
1. Hold the `BOOT` button while connecting USB — this forces ROM bootloader mode.
2. Re-open the flasher. The device should show up as a generic serial device.
3. Flash a fresh build. If that doesn't work, try a completely erased image from [espressif.com](https://espressif.com) first.

### RAK 4631
1. Double-click the RESET button quickly. The device should show up as a USB mass-storage drive named `RAK4631` or similar.
2. Drag the firmware `.uf2` file onto the drive. It will flash automatically and reboot.

### LilyGo T-Beam / T-Deck
Similar to Heltec — hold `BOOT`, reconnect USB, flash fresh.

If the device is truly unresponsive (no USB enumeration, no LED activity, no serial output): the ESP32 may need an external programmer. Ask in Discord — someone usually has the right tools.

---

## How to capture good diagnostic info

When you ask for help, including these details makes everyone's life easier:

- **Hardware:** exact board name and revision ("Heltec V4 1.1", not just "Heltec")
- **Firmware:** name and version ("MeshCore Companion v1.14.1-467959c" — the hash matters)
- **What you did last:** "I just flashed a new build" / "I ran a CLI command and it broke" / "it just stopped"
- **Logs:** connect over serial and paste the last 50 lines from a fresh power-on
- **App screenshot:** if the issue is visible in the app, a screenshot is worth 100 words

---

## Related guides

- **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** — for "not on the map" issues
- **[Troubleshooting: MQTT](?section=troubleshooting-mqtt)** — for publish / bridging issues
- **[Hardware Picker](?section=hardware-picker)** — when it's time to replace the device
