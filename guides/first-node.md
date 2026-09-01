---
id: first-node
title: Your First Node
section: start-here
order: 4
last_reviewed: 2026-04-21
---

# Your First Node

This guide walks you from "I just received a Heltec V4 in the mail" to "I sent my first mesh message." It assumes MeshCore because that is what we recommend for new nodes. If you chose Meshtastic, see **[Meshtastic Node Setup](?section=meshtastic-setup)** instead.

Total time: about 30 minutes. Most of it is waiting for firmware to flash and for the device to find other nodes.

---

## What you need

- Heltec V4 (or any supported 915 MHz LoRa board — see **[Hardware Picker](?section=hardware-picker)**)
- USB-C cable (data, not just charge — some cheap cables are power-only and will not work)
- A computer with a Chromium-based browser (Chrome, Edge, Brave, Arc)
- An iPhone or Android phone
- About 30 minutes

You do **not** need an antenna to do the initial setup. You will need one to actually receive traffic, but the onboard trace antenna is fine for the first-boot walkthrough.

> **Warning:** do not transmit with the device powered on if there is no antenna attached. The radio can damage itself into dead silence if it is keyed up without a load. For the first-boot steps below we are only receiving, so this is safe. Plug in an antenna (even a small one) before you send anything.

---

## Step 1: Flash the firmware

1. Connect the Heltec V4 to your computer with a USB-C cable. You should see a small "hello world" splash on the OLED screen.
2. Open [flasher.meshcore.co.uk](https://flasher.meshcore.co.uk) in Chrome or Edge.
3. Click **Connect** and select your device from the list. It usually shows up as `CP210x` or `CH9102`.
4. Choose the **Companion** build for your board. Click **Erase Device** first — we want to start fresh.
5. Click **Flash**. It takes about 90 seconds. The OLED will blink during the process.
6. When it finishes, the device will reboot and the OLED should show the MeshCore startup screen with a short hex prefix (your public key).

If the flasher cannot find the device:

- Try a different USB cable. Cheap ones are the single most common cause of failure here.
- On Windows, you may need to install the CP210x driver from Silicon Labs' site.
- On macOS, you may need to approve the connection in System Settings → Privacy & Security.

---

## Step 2: Install the MeshCore app

- **iPhone:** search "MeshCore" on the App Store.
- **Android:** search "MeshCore" on the Play Store.

Install and open it.

---

## Step 3: Pair your device

1. In the app, tap **Add device** or the plus icon.
2. Choose **Bluetooth**.
3. Your Heltec V4 should appear in the list with a name like `MC-xxxx`. Tap it.
4. Enter the default pairing PIN (`123456` on most factory builds) if asked.

You should now see the main app screen with your node listed.

---

## Step 4: Set your region and identity

In the app, open your node's settings:

1. **Region:** set to `US Recommended` (or the equivalent for your country).
2. **Name:** give your node a short name. 16 characters max. This is what other people see.
3. **Location:** if you have a permanent install, enter the latitude and longitude. For a pocket device, enable **Advert Location Source** so the GPS (if present) fills this in automatically. If you're uncomfortable sharing an exact address, fuzz it — the map just needs a point, not a rooftop.

Save.

---

## Step 5: Send a flood advert

An **advert** is how your node announces itself to the mesh. Until you send one, nobody knows you exist.

In the app, look for the signal / broadcast icon and tap **Send Flood Routed Advert**. Give it a minute. Nearby nodes will pick up the advert and retransmit it for you.

You can also do this periodically from the CLI with `advert` if you connect over serial — but the app is easier.

---

## Step 6: Check that it worked

Open [nhmesh.live](/) in a browser.

- Your node should appear on the map within a few minutes, assuming another node heard your advert.
- Check the **Nodes** tab for your node name in the list.
- Check the **Observers** tab (coming soon from the sidebar) to see which gateway heard you.

If nothing shows up after 10 minutes, head to **[Troubleshooting: Map Visibility](?section=troubleshooting-visibility)**. This is the single most common "why isn't my node working" path, and we have a flowchart for it.

---

## Step 7: Send your first message

From the app:

1. Open the **Channels** tab.
2. Find `#nhmesh` — our general-chat hashtag channel.
3. Send a hello.

Within a minute, someone will usually say hi back. We monitor `#nhmesh` casually throughout the day. If you get no response, that is usually a sign that your node is not reaching any other node — see the troubleshooting guide.

You can also direct-message another node by tapping them in the contacts list.

---

## What to do next

- **Add an antenna.** The onboard antenna works for the walk-through but you will want to upgrade. See **[Hardware, Antennas & Enclosures](?section=hardware-setup)**.
- **Join the Discord.** The community is the most valuable piece of the mesh.
- **Read the stewardship guide.** We share airtime with everyone in range — **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)** explains how to be a good neighbor.
- **Consider a repeater.** If you have a high-elevation spot (attic, roof, hill), running a MeshCore Repeater helps everyone. We are always short on good infrastructure.

---

## If something went wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| Device not showing in the flasher | Bad USB cable | Try a different cable; cables marked "charge only" will not work |
| Flashed successfully but OLED is blank | Power issue or defective OLED | Unplug for 30 seconds, try again. If still blank, the OLED is rarely the actual fault — try pairing via Bluetooth anyway |
| App cannot find the device over Bluetooth | Device not in pairing mode | Long-press the user button on the Heltec until the OLED shows "Pairing" |
| Node appears in the app but never on the map | No gateway heard your advert | See **[Troubleshooting: Map Visibility](?section=troubleshooting-visibility)** |
| Advert sent, no responses | You are out of RF range of any other node | Move somewhere higher / outdoors; try sending from a few different locations |

Not covered here? Ask in Discord. Someone has run into it.
