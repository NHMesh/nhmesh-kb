---
id: meshtastic-channel-setup
title: Meshtastic Channel Setup
section: operating
order: 2
last_reviewed: 2026-01-19
---

# Meshtastic Channel Setup Guide

This guide focuses on the technical details of configuring Meshtastic channels to follow the **NHMesh 2026 standards**.

## Official Network Standards
To maintain a high-quality mesh in New Hampshire, we have standardized the following settings:

| Setting | Value |
| :--- | :--- |
| **Primary Channel Name** | `NHMesh` |
| **Modem Preset** | `Medium Fast` |
| **PSK (Encryption)** | `NA==` |
| **Frequency Slot** | Auto-calculated from name |

## Why the Change?
As the NHMesh project grows, the generic "LongFast" channel (the default for all Meshtastic devices worldwide) becomes congested with traffic from unrelated nodes. 

By using the **NHMesh** channel on **Medium Fast**:
1. **Network Capacity:** We effectively triple our data rate (3.52 kbps vs 1.07 kbps).
2. **Local Isolation:** We move our traffic to a unique local sub-frequency, reducing interference from non-local devices.
3. **Airtime Efficiency:** Packets are shorter, meaning fewer collisions and higher reliability.

---

## Configuring the NHMesh Channel

### Method 1: The App (Recommended)
1. Open the Meshtastic App and go to **Channels**.
2. Select **Channel 0** (the Primary channel).
3. Change the **Name** to `NHMesh` (case-sensitive).
4. Select **Modem Preset** and choose `Medium Fast`.
5. Ensure **PSK** is set to `NA==`.
6. Save and Apply. Your device will reboot.

### Method 2: CLI (For Power Users)
If you have the Meshtastic Python tools installed, you can configure your node with one command:

```bash
meshtastic --ch-index 0 --ch-set name "NHMesh" --ch-set modem_config "MediumFast" --ch-set psk "NA=="
```

## Frequency Slot Verification
After changing to the `NHMesh` name, your device will calculate a new frequency slot. For the US region, this ensures we are still within the legal 902-928 MHz band but separated from the standard "LongFast" traffic.

---

## Multiple Channels
You can still maintain other channels alongside NHMesh. 
- **NHMesh (Primary):** Should be in Slot 0 for reliable community communication.
- **Private Channels:** You can add private, encrypted channels in Slots 1-7 for your family or local group.
- **Coexistence:** Your node will still repeat encrypted packets from other networks if they share the same radio settings (Medium Fast).

---

_Last updated: January 2026 for the NHMesh Dual-Protocol Initiative._
