---
id: mesh-basics
title: Mesh Network Basics
section: start-here
order: 5
last_reviewed: 2026-01-19
---

# Mesh Network Basics

Understanding how a mesh network functions is key to getting the most out of NHMesh. Unlike traditional Wi-Fi or cellular networks, a mesh is decentralized and grows stronger as more people join.

## 1. What is a Mesh?
In a traditional network, your device connects to a central tower or router. In NHMesh, **every device (node) is a part of the infrastructure**. 

- **Decentralized:** No central server or internet required.
- **Self-Healing:** If one node goes offline, the network automatically finds a new path for your messages.
- **Peer-to-Peer:** Communication happens directly between user devices and repeaters.

## 2. LoRa Technology
NHMesh uses **LoRa** (Long Range) radio technology. It is designed to send very small amounts of data (like text messages and GPS coordinates) over vast distances using very little power. 

- **Range:** Can reach 10+ miles with a clear line-of-sight.
- **Penetration:** Better at passing through trees and buildings than high-frequency signals like Wi-Fi.

## 3. Nodes and Hops
When a node isn't close enough to see the sender directly, it relies on other nodes to relay the signal. This relay process is called a **hop**.

- **Direct Link (0 hops):** You are communicating directly with another node.
- **Multi-hop (1+ hops):** Your message is "bounced" through intermediate nodes to reach its destination.
- **Hop Limit:** To prevent a message from circulating forever and clogging the airwaves, every packet has a "Hop Limit." Once it reaches zero, the packet is discarded.

> **IMPORTANT:** **More hops aren't always better.** High hop counts (above 5-7 on Meshtastic) can create network "bloat," where outdated packets occupy valuable airtime and collide with new messages.

## 4. Signal Quality: SNR and RSSI
The NHMesh map displays two key metrics for every signal:

### RSSI (Received Signal Strength Indicator)
Measured in **dBm**, this tells you how "loud" the signal is.
- **-30 to -60:** Very strong (often too close!)
- **-70 to -90:** Good, stable signal.
- **-100 to -120:** Weak, approaching the limit of reception.

### SNR (Signal-to-Noise Ratio)
Measured in **dB**, this is the most important metric for LoRa. It tells you how clear the signal is relative to the background electrical noise.
- **+5 to +10:** Excellent clarity.
- **0 to +5:** Clean, reliable signal.
- **Negative values (-5 to -20):** LoRa can actually "hear" signals below the noise floor! These are weak but often still usable for text messages.

## 5. Routing Architectures
NHMesh supports two different ways of moving data:

### Flooding Mesh (Meshtastic)
A "simplified" approach where every node that hears a message rebroadcasts it until the hop limit is reached.
- **Pros:** Extremely resilient; no complex setup required.
- **Cons:** Can become inefficient in very dense areas due to many nodes talking at once.

### Directed Routing (MeshCore)
A "smart" approach where nodes keep track of their neighbors and only send messages along the most efficient path.
- **Pros:** Faster delivery; lower airtime usage; supports very high hop counts (up to 64).
- **Cons:** Requires "state-aware" nodes that actively map the network.

---

_For help setting up your specific hardware, see the **Meshtastic Setup** or **MeshCore Setup** guides._
