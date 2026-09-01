---
id: meshtastic-setup
title: Meshtastic Node Setup
section: setup
order: 1
last_reviewed: 2026-01-19
---

# Meshtastic Setup Guide

This guide will help you set up your Meshtastic device and join the NHMesh community network.

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

## Step 4: Join NHMesh
To communicate with the local NH community, you must configure the **NHMesh** channel:
1. Go to **Channels**.
2. Tap on the primary channel (Channel 0).
3. Set the **Name** to `NHMesh` (case-sensitive).
4. Set the **Modem Preset** to `Medium Fast`.
5. Set the **PSK** to `NA==`.

> **TIP:** **Scan the QR Code:** The easiest way to join is to scan the NHMesh QR code found on our website or provided by a local community member. This will configure the channel and modem settings automatically!

## Step 5: Advanced Optimization
For permanent installs, reconsider your device **Role**:
- **CLIENT:** Standard role for most users.
- **ROUTER:** For high-altitude, permanent sites to help packets travel further.
- **REPEATER:** Similar to router but invisible in the node list to save bandwidth.

---

_For detailed channel configuration instructions, see the **Meshtastic Channel Setup Guide**._
