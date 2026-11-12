---
id: meshtastic-setup
title: Meshtastic Node Setup
section: setup
order: 2
last_reviewed: 2026-11-12
---

# Meshtastic Setup Guide

Most of NHMesh now runs MeshCore. If you are new, start with **[MeshCore Node Setup](?section=meshcore-setup)** instead.

This guide is for people who already run Meshtastic or want to. It sets up your device on the stock **LongFast** preset, which is the Meshtastic default.

## Step 1: Get a Device
To join the network, you'll need a compatible LoRa device. Common choices include:
- **Heltec V3** (Affordable, great for mobile/handheld use)
- **RAK Wireless WisBlock** (Excellent battery life, ideal for solar-powered repeaters)
- **LilyGO T-Beam** (Includes built-in GPS and battery management)
- **Station G1/G2** (Ruggedized, ready-to-use desktop or outdoor units)

## Step 2: Install the App
Download the Meshtastic app for your device:
- [iOS App Store](https://apps.apple.com/us/app/meshtastic/id1586432531)
- [Android Play Store](https://play.google.com/store/apps/details?id=com.geeksville.mesh)
- [Web Client](https://client.meshtastic.org/) (for browser-based setup via USB)

## Step 3: Initial Configuration
1. **Power on your device** and open the Meshtastic app.
2. **Connect via Bluetooth** (usually labeled as "Meshtastic [XXXX]").
3. **Set your Region:** Go to Settings > Radio Configuration > LoRa and set Region to **US**.
4. **Set Your Name:** Pick a unique display name and a 4-letter short name (e.g., "GraniteNode" / "GRNT").

## Step 4: Use the Default Channel
1. Go to **Channels** and leave the primary channel (Channel 0) as the stock default.
2. Confirm **Modem Preset** is `LongFast`. This is the default, so you normally change nothing.
3. Leave the **PSK** at its default value.

Optional: add the **NHMesh** channel as a secondary channel. It is not required. See the **[Meshtastic Channel Setup Guide](?section=meshtastic-channel-setup)**.

## Step 5: Advanced Optimization
For permanent installs, reconsider your device **Role**:
- **CLIENT:** Standard role for most users.
- **ROUTER:** For high-altitude, permanent sites to help packets travel further.
- **REPEATER:** Similar to router but invisible in the node list to save bandwidth.

---

_For the optional NHMesh channel, see **[Meshtastic Channel Setup](?section=meshtastic-channel-setup)**._
