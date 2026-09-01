---
id: power-solar
title: Power & Solar Builds
section: infrastructure
order: 3
last_reviewed: 2026-04-21
---

# Power & Solar Builds

Every fixed node needs a way to stay powered. Attic nodes with mains power are easy. Off-grid nodes — on a tree, a tower, a remote hilltop — need solar. This guide is about making that work, including the dozen small mistakes that have caused failed installs in our community.

---

## Can your node run off solar?

Yes, but sizing matters. A MeshCore Repeater draws about 50–200 mA on average, depending on traffic and hardware. In NH, with short winter days and a week of cloud cover in February, you need more panel and battery than the spec-sheet math suggests.

Minimums we've had work year-round:

| Hardware | Panel (min) | Battery (min) |
|---|---|---|
| Heltec V4 Repeater | 10 W | 10,000 mAh / 3.7 V Li-ion |
| RAK 4631 Repeater (low-power mode) | 5 W | 5,000 mAh / 3.7 V Li-ion |
| Room Server (always-on, more traffic) | 15 W | 15,000 mAh |

**Rule of thumb:** oversize by 2× what the math says. Winter solar in NH is brutal.

---

## Parts list for a basic solar repeater

What most of our solar builds look like:

| Part | Spec | Approximate cost |
|---|---|---|
| Solar panel | 10 W, 6 V monocrystalline, weatherproof | $25 |
| Charge controller | TP4056 module (Li-ion) or MPPT for larger builds | $3 – $30 |
| Battery | 2 × 18650 Li-ion (3.7 V, 3500 mAh each) in parallel | $15 |
| Battery holder | 2-cell 18650 with protection circuit | $5 |
| Enclosure | IP65 ABS box with cable glands | $15 |
| Node | Heltec V4 or RAK 4631 | $30 – $130 |
| Antenna | 5.8 dBi fiberglass, 915 MHz tuned | $25 |
| Pigtail | U.FL to SMA, 15 cm | $5 |
| Feedline | LMR-240 or LMR-400, as short as practical | $10 – $30 |
| Mounting hardware | Hose clamps, U-bolts, tree strap | $10 |

Total for a reasonable build: **$140 – $280**.

---

## Off-the-shelf solar nodes

If you don't want to source parts, two community-designed builds exist:

### Zabranch
Compact solar Companion/Repeater in a camo enclosure. Designed for tree mounts. Available on Etsy — ask in Discord for the current listing since the seller rotates links. Runs ~$85 pre-built.

### PicoHive
Modular community build with a published BOM. Ask in Discord for the parts list; several NH operators have built these.

---

## Battery chemistry: Li-ion vs. LiFePO4

The single most important thing to get right.

### Li-ion 18650 (the default)
- Cheap, widely available, good energy density.
- **Cannot charge below 0 °C (32 °F).** In NH winter, a Li-ion cell outside will refuse to accept solar charge for weeks at a time. Some protection circuits prevent charging in cold; others let it happen and damage the cell.
- **Can discharge** down to about -20 °C, so a Li-ion node will run through the winter on its existing charge — it just can't replenish.

**Use Li-ion if:** your node is indoors, in a well-insulated enclosure, or you accept that winter performance will be worse.

### LiFePO4 (recommended for outdoor NH)
- Slightly more expensive.
- Lower energy density (need more cells for the same capacity).
- **Charges down to -20 °C** and discharges reliably across a wide temp range.
- Much longer cycle life — 2,000+ cycles vs. 500 for Li-ion.

**Use LiFePO4 if:** the node is outdoors year-round. The cost difference pays for itself the first winter.

---

## Charge controllers

### TP4056 — small Li-ion builds
Tiny, cheap, works. For single-cell Li-ion with panels under 5 W. Not suitable for LiFePO4.

### CN3791 / CN3767 — MPPT for small solar
Maximum Power Point Tracking for small panels. Better efficiency on cloudy days than a straight TP4056.

### Victron SmartSolar MPPT 75/10 — full-sized builds
Overkill for a single node but bulletproof. Bluetooth monitoring. Worth it if you're running a Room Server or multiple nodes off one system.

### What to avoid
Generic "solar charge controller" boards from marketplaces with no documented chemistry support. Most are tuned for lead-acid and will over- or under-charge Li-ion/LiFePO4.

---

## Enclosures and the condensation problem

Sealed enclosures trap moisture. Daily temperature swings condense humidity out of the air inside the box, which then drips onto your electronics. Over a season this destroys boards.

### Two solutions that work

**Silica gel packet.** Throw in 50 g of silica desiccant. Replace once a year. Simple, effective, cheap.

**Breather vent.** A Gore-Tex or Amazon-generic "waterproof pressure equalizing breather vent" (sometimes called a PTFE breather). Screws into a hole in the side of the enclosure. Lets air pass but not water. Around $10, one-time install, maintenance-free.

We've seen both work. For nodes that will be serviced rarely (hilltop installs), breather vents are better — no need to swap silica. For nodes you can open up annually, silica is fine.

### Drilling vent holes directly
Do not drill unprotected holes. You just converted an IP65 enclosure into a rain trap. If you drill, install a breather vent in the hole.

---

## The antenna problem on tree-mounts

Putting a node in a tree is attractive — free elevation, free LOS. But:

- Tree trunks and canopy absorb 915 MHz significantly. A node inside the canopy does worse than one on a pole at the same height.
- Cable runs from a pole-top antenna down to a ground-level box add loss. At 915 MHz, 25 ft of LMR-400 is about 1.5 dB loss; 25 ft of cheap RG-58 is closer to 4 dB. That matters.
- The ideal is: antenna above the canopy, feedline as short as possible, node + battery near the antenna (in the tree).

**Practical setup:** enclosure in the tree with a short pigtail (15 cm) from the node's U.FL to an SMA bulkhead on the enclosure, then a short jumper (1–2 m of LMR-240) to the antenna on the pole above.

---

## Power consumption tips

A few knobs that extend battery life:

- **Reduce TX power.** If your link margin is good, dropping from 22 dBm to 17 dBm saves a notable amount of power. Verify with **[Health Check](?section=health-check)** first.
- **Enable sleep modes.** MeshCore and Meshtastic both have low-power modes that duty-cycle the radio. Reduces sensitivity but cuts consumption dramatically.
- **Run a Repeater, not a Room Server.** Room Servers have more always-on overhead.

---

## Common failure modes

| Symptom | Likely cause | Prevention |
|---|---|---|
| Node works in summer, dies in February | Panel undersized, or Li-ion in cold | Oversize panel; switch to LiFePO4 |
| Condensation damage after first spring | Sealed enclosure, no vent or silica | Add breather vent |
| Battery dies after a few months | Cheap battery or bad charge controller | Use protected cells; Victron or TP4056 |
| Works on the bench, silent on deployment | Antenna not tuned for 915 MHz, or cable too lossy | Verify antenna spec; use LMR-240 or better |
| Node reboots randomly during the day | Solar panel under-spec, browns out at dusk | Larger battery, or panel with more winter margin |

---

## Related guides

- **[Hardware Picker](?section=hardware-picker)** — choosing the node itself
- **[Hardware, Antennas & Enclosures](?section=hardware-setup)** — antenna deep dive and physical install
- **[Coverage & Placement](?section=coverage-placement)** — deciding where to put the solar node
