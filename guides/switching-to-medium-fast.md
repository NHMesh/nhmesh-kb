---
id: switching-to-medium-fast
title: Switching to Medium Fast
section: setup
order: 3
last_reviewed: 2026-01-19
---

# Switching to Medium Fast

As NHMesh grows, we are transitioning away from the global "LongFast" default settings to a more efficient local standard: **NHMesh** on the **Medium Fast** preset. This guide explains how to make the move safely and reliably.

> **IMPORTANT: The Golden Rule: Infrastructure First**
> If you own a rooftop repeater, solar node, or any permanent backbone infrastructure, you **MUST** update those nodes before updating your handheld or personal mobile units. If you update your handheld first, you will lose the ability to talk to your own repeaters until they are also updated.

---

## The Migration Strategy: Order of Operations

To avoid "islanding" yourself or sections of the network, follow this specific order:

1.  **Remote Backbone Nodes:** Update any nodes that are difficult to access physically (rooftop, mountain top, remote solar).
2.  **Home Base / Static Nodes:** Update your permanent home or office nodes.
3.  **Personal Handhelds:** Finally, update the devices you carry with you.

---

## Step-by-Step Transition

### 1. Update Infrastructure (CLI Recommended)
For backbone nodes, using the CLI is often the most reliable way to ensure all parameters are set correctly in one go.

Run the following command (replace `0` with the correct channel index if necessary):

```bash
meshtastic --ch-index 0 --ch-set name "NHMesh" --ch-set modem_config "MediumFast" --ch-set psk "NA=="
```

**Verification:**
After the command, wait for the node to reboot and verify its status:
```bash
meshtastic --info
```
Look for `modem_config: MediumFast` and the channel name `NHMesh`.

### 2. Update Personal Nodes (App)
1.  Open the Meshtastic App and connect to your device.
2.  Go to **Channels** > **Channel 0** (Primary).
3.  **Name:** Change to `NHMesh` (case-sensitive).
4.  **Modem Preset:** Select `Medium Fast`.
5.  **PSK:** Set to `NA==`.
6.  **Apply / Save:** Your device will reboot.

---

## Why are we doing this?

| Feature | Long Fast (Global Default) | Medium Fast (NH Standard) |
| :--- | :--- | :--- |
| **Bitrate** | ~1.07 kbps | **~3.52 kbps** (3x faster!) |
| **Airtime** | High (Slow packets) | **Low** (Fast, efficient packets) |
| **Congestion** | High (Global traffic) | **Low** (Isolated local traffic) |
| **Reliability** | Moderate | **High** (Fewer collisions) |

By moving to **Medium Fast**, we effectively triple the capacity of the New Hampshire network, allowing more users to share the same airwaves with fewer "collision" errors and much faster message delivery.

---

## Troubleshooting Connectivity
If you lose contact with a node after switching:
- **Check the PSK:** Ensure it is exactly `NA==`.
- **Check the Name:** Ensure it is exactly `NHMesh`.
- **SNR Check:** Since Medium Fast has slightly less range than Long Fast, a link that was "on the edge" (SNR -15 or lower) might require better antenna placement or a higher altitude to remain stable on the faster preset.

---

_For general mesh educational concepts, see the **Mesh Network Basics** guide._
