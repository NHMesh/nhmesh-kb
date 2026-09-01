---
id: advanced-config
title: Advanced Configuration
section: reference
order: 4
last_reviewed: 2026-01-19
---

# Advanced Configuration Options

This guide covers advanced configuration options for Meshtastic devices, allowing you to customize your setup for specific use cases.

## Prerequisites

Before diving into advanced configurations, ensure you have:

- A working Meshtastic device already set up
- The latest Meshtastic software installed
- Basic familiarity with Meshtastic operations

## Advanced Channel Settings

### Multiple Channels

Meshtastic devices support multiple channels (up to 8), which can be useful for different communication purposes:

```bash
# Add a secondary channel
meshtastic --ch-add name="EmergencyChannel" --ch-index 1

# Configure channel settings
meshtastic --ch-set name="EmergencyChannel" --ch-index 1 --ch-longslow
```

### Channel Modem Configuration

Modem settings affect range, bandwidth, and battery life. Use these parameters to optimize for your specific needs:

```bash
# Long-range, slow data rate
meshtastic --ch-set modem-config="Bw125Cr48Sf4096" --ch-index 0

# Short-range, fast data rate
meshtastic --ch-set modem-config="Bw500Cr45Sf128" --ch-index 0
```

## Power Management

### Power Saving Modes

Configure power saving to extend battery life:

```bash
# Configure sleep settings
meshtastic --set ls_secs=300  # Sleep after 5 minutes of inactivity

# Configure screen timeout
meshtastic --set screen_on_secs=60  # Screen turns off after 60 seconds
```

### GPS Power Management

The GPS module consumes significant power. Configure its behavior with:

```bash
# Set GPS update interval
meshtastic --set gps_update_interval=60  # GPS position update every 60 seconds

# Configure GPS mode
meshtastic --set gps_mode=0  # 0=disabled, 1=enabled, 2=enabled_no_power_save, 3=enabled_pin_wakeup
```

## Device Role Configuration

### Router Mode

Configure a device to act as a dedicated router:

```bash
# Set device as a router
meshtastic --set is_router=1

# Disable router mode
meshtastic --set is_router=0
```

### Relay Mode

Relay nodes rebroadcast messages to extend the network:

```bash
# Enable relay mode
meshtastic --set is_repeater=1
```

## Advanced MQTT Integration

### Custom MQTT Server

Configure a device to connect to a custom MQTT server:

```bash
# Set MQTT server
meshtastic --set mqtt_server="mqtt.example.com" --set mqtt_username="user" --set mqtt_password="pass"
```

### MQTT Topics Configuration

```bash
# Set custom MQTT topic prefix
meshtastic --set mqtt_topic_prefix="meshtastic/mynetwork"
```

## Encryption and Security

### Custom Encryption Keys

Set custom encryption keys for enhanced security:

```bash
# Set a custom PSK
meshtastic --set-channel-psk "MySecretKey1234567890123456"
```

### Disabling Serial Console

For security-sensitive applications, disable the serial console:

```bash
# Disable serial console
meshtastic --set serial_disabled=1
```

## Troubleshooting Advanced Configurations

### Factory Reset

If your configuration causes issues, reset the device:

```bash
# Factory reset
meshtastic --factory-reset
```

### Debug Logging

Enable debug logging for troubleshooting:

```bash
# Enable debug logs
meshtastic --set debug_log_enabled=1
```

## Next Steps

After mastering these advanced configurations, you may want to explore:

- Building custom hardware
- Developing Meshtastic plugins
- Integration with external systems

These advanced configurations allow you to tailor Meshtastic to your specific needs, whether for emergency communications, IoT applications, or specialized networking requirements.
