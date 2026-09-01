---
id: recommended-settings
title: Recommended Settings
section: operating
order: 3
last_reviewed: 2026-01-19
---

# NHMesh Recommended Configuration Settings

To ensure a robust and reliable mesh network using NHMesh devices, we recommend the following configuration settings. These guidelines are based on best practices and community experience.

## Radio Configuration
These settings primarily affect how your device interacts with the LoRa radio and the mesh network.

### Device Settings
- **Role:** `CLIENT` or `CLIENT_MUTE`
  - `CLIENT` is suitable for most user devices that need to send and receive messages.
  - `CLIENT_MUTE` is useful for devices that primarily need to act as repeaters without generating their own traffic.
  - Consider power consumption when choosing roles.
- **NodeInfo Broadcast Interval:** `10800` (3 hours)
  - This setting controls how frequently your device announces its presence to the network.
  - A longer interval reduces network congestion.

### Position Settings
- **Smart Position Enabled:** `True`
  - Allows the device to intelligently determine when to broadcast its position.
- **Position Broadcast Interval:** `3600` (1 hour)
  - Controls how often your device broadcasts its location.
  - Adjust based on your needs for location awareness vs. battery life.
- **GPS Update Interval:** `1800` (30 minutes)
  - Sets how often the device attempts to get a GPS fix.
  - A longer interval saves power.
- **Position Flags:** Disable unused flags
  - Disable any flags that are not relevant to your device's usage.
  - For example, fixed nodes should disable most or all position flags, as their location is static.

### LoRa Settings
- **Hop Limit:** `5`
  - The maximum number of hops a message can take to reach its destination.
  - _Important:_ Do not increase this value significantly. A higher hop limit can lead to excessive network traffic.
  - A setting above 6 is strongly discouraged.
- **Ignore MQTT:** `False`
  - If your node is primarily acting as a router and doesn't need to interact with an MQTT server, enable this.
- **OK to MQTT:** `True`
  - If you want your node to be visible on online mapping tools and connected to an MQTT server.
  - This setting was introduced in firmware version 2.5.0.

## Module Configuration

### Telemetry
- **Device Metrics Update Interval:** `3600` (1 hour)
  - How often the device sends telemetry data (battery, signal strength, etc.).
- **Environment Metrics Update Interval:** `3600` (1 hour)
  - How often the device sends environmental sensor data.
- **Power Metrics Module Enabled:** `False`
  - Disable this unless you are using an I²C power monitoring chip.

> **IMPORTANT:** If you are not using the `Environment metrics` or `Air Quality metrics` modules, consider disabling them to conserve resources.

### Neighbor Info
- **Neighbor Info Enabled:** `False`
  - Neighbor Info functionality has been limited in recent firmware versions.
  - Disabling it can improve performance.

---

By following these recommendations, you can help ensure a stable, efficient, and reliable NHMesh network.
