---
id: meshcore-repeaters-regions
title: MeshCore Repeaters & Regions in NH
section: setup
order: 3
last_reviewed: 2026-11-12
---

# MeshCore Repeaters & Regions in NH

This guide is for people running a MeshCore repeater in New Hampshire: which settings matter, how often to advert, and how regions (also called scopes) are used here. If you only carry a Companion, you can skip it. To flash a repeater first, see **[MeshCore Node Setup](?section=meshcore-setup)**.

Commands below are from the [MeshCore CLI reference](https://github.com/meshcore-dev/MeshCore/blob/main/docs/cli_commands.md) and [FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md). Region commands need firmware 1.10 or later; `region list` needs 1.12 or later.

---

## Radio settings

All NH MeshCore nodes use the US preset:

```
set radio 910.525,62.5,7,5
```

That's frequency in MHz, bandwidth in kHz, spreading factor 7, coding rate 5. Reboot afterward; the change doesn't apply until you do. The firmware default is a European setting, so don't skip it.

## Core repeater settings

| Setting | Command | Notes |
|---|---|---|
| Name | `set name YOUR_NAME` | Include the place, like `Chester_Ledge` |
| Location | `set lat 43.0000` and `set lon -71.0000` | Use the real, exact location; repeaters never move |
| TX power | `set tx 22` | 1 to 22 dBm. Some boards add an amplifier, so check yours; don't exceed legal limits |
| Repeating | `set repeat on` | Default is on. Leave on for repeaters |
| Admin password | change from `password` | Do this before you mount it |
| Max flood hops | `set flood.max 64` | Default 64. Lower it only if a neighbor's traffic is a problem |

Run each as `get <setting>` to read it back. Room Servers should not use `set repeat on`; run the repeater and the room server on separate devices ([MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)).

## Adverts

- **Zero-hop advert** (`set advert.interval MINUTES`): heard only by nodes that hear you directly. Valid range is 60 to 240 minutes; once configured the default is 0 (off).
- **Flood advert** (`set flood.advert.interval HOURS`): repeated across the mesh. Valid range is 3 to 168 hours. The CLI reference lists the repeater default as 47 hours; the FAQ says 12 hours. **Unverified which is current for your firmware;** run `get flood.advert.interval` to see yours.

Don't set these shorter than you need. Every advert is airtime for everyone. NH hasn't published a community-wide interval; **unverified** if one is agreed, so ask in the Discord before changing the default.

## Regions (scopes) as NH uses them

A region is a named label that a sender can attach to a flood packet. A repeater can allow or block floods by region, so traffic meant for one area doesn't ripple across the whole state. NH repeaters use these regions:

| Region | Meaning |
|---|---|
| `nh` | The home and default region for NH repeaters |
| `northeast` | A wider region that reaches neighboring states |

and they allow packets with no region too (`region allowf *`).

To set this up on a repeater (serial or remote admin):

```
region put nh
region put northeast
region allowf nh
region allowf northeast
region allowf *
region home nh
region default nh
region save
```

Run `region` to check the result, and always run `region save` or the change is lost at reboot. `region allowf *` allows packets that have no region at all; `region denyf *` would drop them ([CLI reference](https://github.com/meshcore-dev/MeshCore/blob/main/docs/cli_commands.md)).

**Unverified:** the exact parent/child layout of `nh` and `northeast` on live NH repeaters. The commands above create them as siblings under the wildcard; confirm with a repeater operator before copying a hierarchy.

If a noisy neighbor floods your area, a gentler option than `region denyf *` is to limit unscoped floods, for example `set flood.max.unscoped 3` ([CLI reference](https://github.com/meshcore-dev/MeshCore/blob/main/docs/cli_commands.md)).

## Path hashes: identify your repeaters

A route lists repeaters by a short hash of each one's public key. By default that's 1 byte, so two repeaters can collide. Newer firmware supports 2-byte and 3-byte hashes, which tell repeaters apart more reliably at the cost of fewer hops (about 64, 32 and 21 hops for 1, 2 and 3 bytes).

- **2-byte path hashes** make it easier to tell which repeater a packet went through, which helps when you're tracing a route to an NH repeater.
- On a repeater, `set path.hash.mode 1` makes its own adverts use 2 bytes (0 is 1 byte, 1 is 2, 2 is 3). It does not change what the repeater forwards.
- Repeaters on firmware 1.14 or newer forward 1, 2 and 3-byte packets. Older repeaters silently drop larger hashes, so update repeaters before relying on this ([MeshCore FAQ](https://github.com/meshcore-dev/MeshCore/blob/main/docs/faq.md)).
- When you set up a new repeater, pick a public key whose first byte nobody nearby uses.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Repeater never shows on the map | Lat/lon is `0`, or no flood advert has gone out | Set lat/lon, then send a flood advert |
| Messages cross your area but not the state | Region mismatch | Check `region`; make sure `nh` and `northeast` allow flood |
| Region changes vanish after reboot | You didn't save | Run `region save` |
| Packets with 2-byte hashes vanish | A repeater on firmware older than 1.14 | Update it |
| Repeater can't hear nearby nodes | SX1262 deafness | `set agc.reset.interval 4` (FAQ) |

## Related guides

- **[Stewardship & Hashtag Channels](?section=meshcore-hashtag-channels)**
- **[Coverage & Placement](?section=coverage-placement)**
- **[Observer / Gateway Setup](?section=letsmesh-observer)**
