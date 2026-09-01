---
id: producer-setup
title: NHMesh Producer (Backbone Operators)
section: infrastructure
order: 4
last_reviewed: 2026-01-19
---

# NHMesh Producer Setup Guide

The `nhmesh-producer` is a specialized Python application designed for infrastructure owners who want to feed high-quality data from their backbone nodes into the NHMesh collector and map. 

Unlike the built-in MQTT module in Meshtastic, the Producer is more resilient, supports automatic reconnection, and provides enhanced traceroute monitoring.

---

## 1. Prerequisites

- A Meshtastic node reachable via **TCP/Network** (e.g., WisBlock with Ethernet/WiFi) or **USB/Serial**.
- Docker (recommended) or Python 3.13+.
- MQTT credentials (ask a moderator in chat).

---

## 2. Running with Docker (Recommended)

Docker is the easiest way to deploy the producer and ensure it stays running.

```bash
docker run -d \
    --name nhmesh-producer \
    --restart unless-stopped \
    -e NODE_IP=192.168.1.100 \
    -e MQTT_ENDPOINT=mqtt.nhmesh.live \
    -e MQTT_USERNAME=your_username \
    -e MQTT_PASSWORD=your_password \
    -e MQTT_TOPIC=msh/US/NH/ \
    ghcr.io/nhmesh/producer:latest
```

---

## 3. Configuration Variables

If you are using a `docker-compose.yml` or a `.env` file, here are the key variables:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `NODE_IP` | IP address of your Meshtastic node. | (Required for TCP) |
| `CONNECTION_TYPE` | `tcp` or `serial`. | `tcp` |
| `MQTT_ENDPOINT` | The NHMesh MQTT broker. | `mqtt.nhmesh.live` |
| `MQTT_TOPIC` | The root topic for your region. | `msh/US/NH/` |
| `TRACEROUTE_INTERVAL` | How often to poll for path data. | `43200` (12 hours) |

---

## 4. Connection Types

### TCP Connection (Network)
Best for permanent infrastructure where the node is powered by PoE or a stable DC source and connected to your local network.
- Ensure the node has **"Module Config > Serial > Mode"** set to `PROTO` or `TEXTUAL` depending on your version, though recent firmware handles this automatically for TCP.

### Serial Connection (USB)
Best for "Base Station" nodes connected directly to a Raspberry Pi or server via USB.
- Use `CONNECTION_TYPE=serial` and `SERIAL_PORT=/dev/ttyUSB0`.

---

## 5. Why use the Producer instead of the App's MQTT?

1.  **Resilience:** The producer handles "Broken Pipe" errors and TCP timeouts much better than the standard firmware.
2.  **Health Monitoring:** It continuously checks the connection and reboots the link if data stops flowing.
3.  **Advanced Forensics:** It automatically triggers traceroutes to new nodes it hears, helping build the network map more accurately.

---

_For more technical details, visit the [nhmesh-producer GitHub repository](https://github.com/nhmesh/nhmesh-producer)._
