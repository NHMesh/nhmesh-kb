---
id: hardware-setup
title: Hardware, Antennas & Enclosures
section: infrastructure
order: 2
last_reviewed: 2026-04-21
---

# Hardware, Antennas & Enclosures

This is the physical-build deep-dive. Once you've picked a node (see **[Hardware Picker](?section=hardware-picker)**) and decided where to put it (see **[Coverage & Placement](?section=coverage-placement)**), this guide covers the actual assembly: which antenna, which cable, which enclosure, how to mount it, how not to burn out the radio.

If this is your first node and you just want to get on the mesh, skip this and go to **[Your First Node](?section=first-node)** — you don't need any of this for a handheld setup. This guide matters when you're building a fixed install.

---

## Antennas: the only thing that matters more than location

A properly-tuned 915 MHz antenna on a short run of good coax is worth more than a 10 dBi antenna on a 50 ft run of RG-58. Signal loss at 915 MHz adds up fast.

### Antenna types

**Omnidirectional fiberglass collinear (the default).** Tall vertical stick. Radiates 360° horizontally. This is what most repeaters run.

- **3 dBi:** narrow pattern, works at high elevations and flat terrain
- **5.8 dBi:** our community default — good balance of gain and pattern
- **8+ dBi:** tight vertical pattern (the "pancake" problem), can overshoot nearby nodes if you're on a hill. Use carefully.

**Dipole / rubber duck.** Short antenna. Used for handhelds and indoor installs. Lower gain but omnidirectional.

- The **muzi 915 MHz** from Amazon is a cheap, well-regarded pocket upgrade to the factory whips.

**Directional (Yagi, panel).** Narrow beam. Used for long-distance point-to-point backbones.

- Only useful if you know the exact direction to the target. Not for first-time installs.

### Tuning

The single most important antenna spec: **frequency range**. A 433 MHz or 868 MHz antenna radiates almost nothing at 915 MHz. Confirm:

- The antenna is labeled for 902–928 MHz or the US ISM band
- Avoid "broadband" antennas without specific 915 MHz tuning claims
- If you can, check SWR at 915 MHz. Under 2:1 is good; under 1.5:1 is excellent

### The "pancake" problem

Higher-gain omnis achieve gain by focusing radiation into a narrower vertical pattern. An 8 dBi omni has a much flatter vertical beam than a 3 dBi. Consequences:

- Great for flat terrain, long horizontal reach
- Bad on a mountaintop — nearby valley nodes are below your radiation pattern
- Bad at low elevations — tilting the ground plane tilts the whole pattern into the sky or ground

For NH hilly terrain, **5.8 dBi is the sweet spot.** Going higher rarely helps and often hurts.

---

## Coax and feedline

Signal loss per foot at 915 MHz, approximate:

| Cable | Loss per 100 ft |
|---|---|
| RG-58 | ~17 dB |
| LMR-240 | ~7 dB |
| LMR-400 | ~3.5 dB |
| Heliax LDF4 | ~2.5 dB |

That's per 100 ft. For a 25 ft run, RG-58 costs you over 4 dB — meaning you're radiating about a third of your power. Don't use RG-58 for 915 MHz installs if the run is over a few feet.

### Recommendations

- **Under 10 ft:** LMR-240 is fine, cheap, flexible
- **10–30 ft:** LMR-400 is worth the extra cost
- **Over 30 ft:** LMR-400 or Heliax, and move the node closer to the antenna if possible

### Connectors

Most boards use U.FL (tiny snap-on connector). Most antennas use N-type or SMA. You need pigtails.

- **U.FL to SMA pigtail** (15 cm is standard): connects the board to the outside world
- **SMA to N-type adapter**: if your antenna uses N-type connectors
- **Weatherproof** all outdoor connections with self-amalgamating tape. Regular electrical tape is not enough

---

## Enclosures

For outdoor infrastructure, the enclosure is the second-most-common point of failure (after antennas).

### IP rating

- **IP65:** dust-tight, water jets. Minimum for outdoor NH use.
- **IP67:** dust-tight, temporary submersion. Preferred for fixed installs.
- **IP68:** continuous submersion. Overkill for our use case.

### Size

You need room for:

- The node board (small — Heltec V4 is ~52 × 25 mm)
- The battery (if off-grid)
- The charge controller
- Cable routing
- Some air volume so the electronics don't cook in summer

A 150 × 100 × 70 mm enclosure fits most builds comfortably.

### Cable entry

Never drill unprotected holes. Use:

- **Cable glands** (PG-7 for small cables, PG-13 for LMR-240): screw into a drilled hole, squeeze the cable, IP-rated
- **Bulkhead connectors**: SMA, N-type, or USB bulkheads for clean pass-through with antenna changes

### Breathing

All sealed outdoor enclosures trap humidity. See **[Power & Solar](?section=power-solar)** for the silica-gel vs. breather-vent discussion. Either works. Not addressing it means water damage over the first winter.

---

## Mounting

### Attic install

- Antenna up against the roof peak (ideally just above roofline via a short mast)
- Enclosure anywhere in the attic with a clean feedline run
- Power from a nearby outlet or a UPS

### Rooftop install

- Antenna on a mast or chimney mount, stainless steel hose clamps
- Feedline down along the chimney or through a flashed roof boot
- Ground the mast if you're worried about lightning (NH gets storms; not a huge risk at our scale, but it's good practice for anything on a roof)

### Tree mount

- Enclosure strapped to the trunk with tree straps (never nails — hurts the tree and creates attack points for rot)
- Antenna on a short mast above canopy, or in the crown if you can get it there
- Feedline in a UV-rated conduit or at least cable-tied carefully

### Tower

- If you have a tower, you probably know more about this than this guide. Follow RF ground practice, lightning arrestors, and don't run coax along power lines.

---

## Assembly checklist

Before you power on the first time:

- [ ] Antenna connected to the board
- [ ] All connectors seated (U.FL clicks; SMA hand-tight plus quarter turn)
- [ ] Antenna tuned for 915 MHz
- [ ] No kinks in coax
- [ ] Cable strain relief so nothing pulls on the board
- [ ] Enclosure gasket seated
- [ ] Cable glands tightened
- [ ] Desiccant or breather vent installed
- [ ] Power source connected with correct polarity
- [ ] Firmware already flashed (don't flash at the top of a tree)

**Critical:** never power on a node without an antenna attached. Unterminated transmit can damage the LoRa radio into silence. If you powered on briefly without an antenna, the radio may still work at reduced sensitivity — if your installed node seems deaf, this is a possible cause.

---

## Common mistakes

| Mistake | Consequence |
|---|---|
| RG-58 for a 30 ft run | Radiate about 1/3 of actual power |
| 868 MHz antenna (often marked "ISM") | Radiate almost nothing |
| Sealed enclosure, no vent or desiccant | Water damage after first season |
| Cable gland over-tightened | Crushed cable, shorted inner conductor |
| Antenna mounted horizontally | Polarization mismatch with everyone else's vertical antennas → ~20 dB loss |
| 12 dBi high-gain omni on a hill | Overshoots nearby users in valleys |
| U.FL connector only half-seated | Intermittent connectivity, looks like firmware bug |
| Power-on with no antenna attached | Radio damage, reduced sensitivity permanently |

---

## Related guides

- **[Hardware Picker](?section=hardware-picker)** — choosing the node
- **[Power & Solar](?section=power-solar)** — off-grid power system
- **[Coverage & Placement](?section=coverage-placement)** — where to put the install
- **[Troubleshooting: Visibility](?section=troubleshooting-visibility)** — when the install is done but nothing works
