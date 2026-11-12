---
id: meshtastic-channel-setup
title: Meshtastic Channel Setup
section: operating
order: 2
last_reviewed: 2026-11-12
---

# Meshtastic Channel Setup Guide

This guide is for Meshtastic users who want to add the optional **NHMesh** channel. Most of NHMesh runs MeshCore, so if you are new, start at **[MeshCore Node Setup](?section=meshcore-setup)**.

## Default Settings
Keep your primary channel (Channel 0) on the Meshtastic stock defaults:

| Setting | Value |
| :--- | :--- |
| **Primary Channel** | Stock default (unnamed) |
| **Modem Preset** | `LongFast` |
| **PSK (Encryption)** | Default |

You do not need the NHMesh channel to use the mesh.

## Add the NHMesh Channel (Optional)
The NHMesh channel is an extra channel for local chat. It goes in a secondary slot, never Channel 0.

1. Open the Meshtastic app and go to **Channels**.
2. Tap an empty slot (Channel 1 or higher).
3. Set the **Name** to `NHMesh` (case-sensitive).
4. Set the **PSK** to `NA==`.
5. Save and apply. Your device will reboot.

To do the same from the CLI with the Meshtastic Python tools:

```bash
meshtastic --ch-add NHMesh
meshtastic --ch-index 1 --ch-set psk "NA=="
```

We recommend leaving your modem preset on `LongFast`. `MediumFast` is still supported and shows up on the map, but we don't recommend it. Channels share the one radio preset set under Radio Configuration → LoRa.

## Other Channels
You can add private, encrypted channels in the remaining slots for your family or local group.
