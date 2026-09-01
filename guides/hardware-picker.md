---
id: hardware-picker
title: Hardware Picker
section: start-here
order: 3
last_reviewed: 2026-04-21
---

# Hardware Picker

What to buy, by use case and budget. All prices approximate as of early 2026; links go to the specific products we have seen work in our mesh. Nothing here is sponsored.

If you want a one-line answer: **buy a Heltec V4** (~$30), flash MeshCore Companion, and you are on the mesh. Come back when you want to upgrade.

---

## First, what are you trying to do?

| Use case | Recommended starting point |
|---|---|
| Text messages from a phone, around town and into the woods | Companion node + smartphone |
| Fixed install in an attic or on a roof to relay traffic | Repeater node |
| Outdoor, off-grid, powered by sun | Solar repeater build |
| Standalone pocket device with its own keyboard and screen | T-Deck Pro |
| Learning / tinkering / custom firmware | Any of the dev boards below |

Pick the row that fits and jump to that section.

---

## Companion nodes (carry in your pocket)

A Companion is a small radio you pair with your phone over Bluetooth. The phone is the keyboard and screen; the radio handles the LoRa side.

### Heltec WiFi LoRa 32 V4 — ~$30
The default recommendation. Small, cheap, widely available, good enough for most users. OLED screen shows basic status. USB-C charging.

- **Pros:** Cheap, small, ubiquitous, every guide is written with this in mind.
- **Cons:** No built-in GPS. The built-in antenna is a compromise — you'll want to upgrade.
- **Buy:** search "Heltec V4 LoRa 915MHz" on AliExpress or Amazon. Make sure it's the 915 MHz US band version, not 868 MHz.
- **Firmware:** MeshCore or Meshtastic Companion.

**Note:** There are ongoing hardware revisions. If you get a V4 that seems less sensitive than expected, try the CLI command `radio.rxgain on` — there is a known bug where the LNA is disabled on boot. See **[Troubleshooting Firmware](?section=troubleshooting-firmware)**.

### Heltec V3 — ~$25
The predecessor. Still works well. Slightly larger, same general experience. If you already have one, keep using it. If you're buying new, get the V4.

### LilyGo T-Beam Supreme — ~$65
Bigger, better, built-in GPS, better battery life. Heavier in the pocket. If you want accurate location sharing without pairing a phone, this is the sweet spot.

- **Pros:** Built-in GPS, removable 18650 battery, room for a better antenna.
- **Cons:** More expensive, larger.

### RAK 4631 (WisBlock) — ~$80–$150 depending on modules
The "build your own" option. Modular stack: radio, GPS, battery, case. More work to assemble but the end result is the nicest hardware we use in the mesh.

- **Pros:** Best build quality, modular, easy to service, excellent for long-term installs.
- **Cons:** Costs more, requires assembly, case sold separately.

---

## Repeater nodes (fixed install)

A repeater sits in one place — ideally high up — and relays traffic for everyone in range. This is the infrastructure. We are chronically short on good repeater placement in NH, so if you have a good site, run one.

### RAK 4631 in a weatherproof case — ~$130 built
This is what most of our current backbone runs. The WisBlock platform is designed for outdoor IoT and the weatherproof case options are mature.

- **Firmware:** MeshCore Repeater.
- **Power:** 12V DC with a solar charge controller if off-grid; USB-C if you have mains.
- **Enclosure:** see the **[Hardware, Antennas & Enclosures](?section=hardware-setup)** guide.

### Heltec V4 as a temporary repeater — ~$30
If you want to test a location before committing, a V4 in a plastic box does the job for a few weeks. Not recommended as permanent infrastructure — the hardware is not rated for outdoor temperature and humidity swings.

---

## Solar / off-grid builds

These are community-designed solar nodes that handle everything (radio, panel, battery, controller, case) in one package.

### Zabranch — ~$85 built
A compact solar companion/repeater designed by an NH operator. Camo enclosure suitable for tree mounts, 915 MHz tuned, runs MeshCore or Meshtastic. Available on Etsy; ask in Discord for the current link since listings rotate.

### PicoHive
Another community solar build. Ask in Discord for the parts list and current pricing; the community shares the BOM.

### DIY
- **Panel:** 5–10W 6V monocrystalline, waterproof.
- **Battery:** 3.7V 18650 Li-ion with protection circuit, or a small LiFePO4 pack.
- **Charge controller:** TP4056 for small builds; Victron SmartSolar for larger.
- **Enclosure:** IP65 or better, with a vent (a Gore-Tex or equivalent breathable membrane stops condensation).

See the **[Power & Solar](?section=power-solar)** guide for the build walkthrough.

---

## Standalone devices (no phone required)

### LilyGo T-Deck Pro — ~$150
A full QWERTY keyboard, a screen, a battery, and a radio in one handheld. You can use it as a standalone messenger without pairing to anything. Pro model has better build quality than the original T-Deck.

- **Pros:** Self-contained, no app required, looks great.
- **Cons:** Expensive, tiny keyboard.

### Station G2 — ~$200+
Higher-end standalone gear. Usually overkill for casual use; good for serious field deployment.

---

## Antennas

The stock antenna on most boards is a compromise. Upgrading is the single highest-value change you can make for range.

### Handheld upgrade — muzi 915 MHz
A small rubber-duck antenna that is noticeably better than the factory whip. ~$8 on Amazon. Fits in a pocket. Recommended by several of our operators.

### Fixed install — 5.8 dBi fiberglass
For a repeater, a proper 5.8 dBi fiberglass omni (the standard "tall stick" you see on rooftops) gives you serious gain over any short whip. The specific brand matters less than making sure it is tuned to 915 MHz.

- **Key spec:** tuned for 902–928 MHz (the US 915 MHz band).
- **Connector:** most boards are U.FL; you'll want a U.FL-to-SMA pigtail, then SMA to N-type or whatever the antenna uses.
- **Cable:** LMR-400 for runs over 10 feet. LMR-240 for shorter. Cheap coax loses a lot of signal at 915 MHz.

### What to avoid
- Antennas tuned for 433 MHz, 868 MHz, or unspecified. Wrong frequency kills performance.
- Huge 12 dBi "extreme range" omnis. On paper they look great; in practice their narrow vertical radiation pattern means you hear nothing from nearby stations.

---

## Cheat sheet by budget

| Budget | What to buy |
|---|---|
| $30 | Heltec V4 |
| $40 | Heltec V4 + muzi antenna |
| $75 | Heltec V4 + muzi + T-Beam Supreme (gives you one mobile + one with GPS) |
| $130 | RAK 4631 in weatherproof case — your first real repeater |
| $200 | RAK 4631 repeater + 5.8 dBi fixed antenna + LMR-400 cable |
| $250+ | T-Deck Pro for standalone use, or a proper solar repeater build |

---

## Next steps

- **[Your First Node](?section=first-node)** — from unboxing to on the mesh, step by step.
- **[MeshCore Node Setup](?section=meshcore-setup)** — detailed firmware walk-through.
- **[Hardware, Antennas & Enclosures](?section=hardware-setup)** — the physics deep dive for when you want to understand what you just bought.
