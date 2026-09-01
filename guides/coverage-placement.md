---
id: coverage-placement
title: Coverage & Placement
section: infrastructure
order: 1
last_reviewed: 2026-04-21
---

# Coverage & Placement

Where you put a node matters more than what kind of node it is. This guide is about reasoning through coverage — whether a given spot is worth the install, how far a node at that spot will actually reach, and how hops work in practice.

If you're planning a repeater install specifically, read this first, then **[Hardware, Antennas & Enclosures](?section=hardware-setup)** for the physical build.

---

## The basic rule

LoRa is line-of-sight. 915 MHz punches through a few trees and some light construction, but it does not meaningfully bend around hills, buildings, or terrain. If you can't see the destination, your signal has to reflect or hop its way there, and reflections are unreliable at these frequencies.

**Practical consequence:** the single best thing you can do for a repeater's range is put it higher.

- A repeater on a hill at 300 m elevation with a 6 dBi antenna will beat the same hardware at 10 m on flat ground every time.
- Even a second-story attic with a window view is much better than ground level.
- A basement node, no matter how fancy, is effectively deaf.

---

## Will a repeater at my house help?

This comes up constantly. Three considerations:

### 1. Are you filling a coverage gap?
Open [nhmesh.live](/) and look at which nodes are active near you. If there are already two or three healthy repeaters within a few miles and they have good coverage of your area, a fourth at ground level doesn't add much. If you're in a pocket that has no repeaters within 10 miles, even a modest setup helps.

### 2. Do you have elevation or line-of-sight?
A repeater at your house helps if:
- You're on a hill relative to the surrounding area, or
- You have clear sight lines to specific other repeaters or high-traffic areas, or
- You can get the antenna up high enough to see over local obstructions.

A repeater at your house does not help much if you're in a valley with no line-of-sight to anywhere the mesh lives.

### 3. Is the install permanent?
Infrastructure is most valuable when it stays up. A repeater that runs for 6 months is more useful than one that runs for 6 weeks and then comes down because you got bored. Be honest with yourself about whether you'll maintain it.

**Rule of thumb:** if you have an attic or a rooftop spot with sight lines to anywhere the mesh currently is, yes, put up a repeater. Even a basic Heltec V4 in a plastic box in the attic with a stock antenna adds measurable value. You can always upgrade.

---

## Using the Planner

The **[Mesh Planner](/planner)** at nhmesh.live lets you drop a proposed node on a map and run line-of-sight calculations against existing infrastructure and terrain elevation data. Use it before you commit to an install.

Workflow:
1. Go to `/planner`.
2. Click the proposed location.
3. The tool computes Fresnel zone clearance against each existing node and tells you whether you have a viable path.
4. Iterate on the exact spot and antenna height until you see green links to at least 2–3 existing nodes.

If the Planner says you have no viable paths at any reasonable height, the install will not work. This is the cheapest way to learn that — cheaper than putting up a tower and then discovering it's blocked.

---

## How far is "far enough"?

In NH terrain, realistic direct-link ranges:

| Setup | Typical range (clear LOS) |
|---|---|
| Handheld Companion, stock antenna, ground level | 0.5 – 2 miles |
| Handheld with upgraded antenna, outdoors | 1 – 5 miles |
| Attic repeater, 5.8 dBi antenna | 5 – 15 miles |
| Rooftop repeater, well-tuned, elevated | 15 – 40+ miles |
| Hill-top repeater with directional | 50+ miles, up to 100+ with matching antennas both ends |

These are direct-link numbers. In practice, most traffic traverses multiple hops, which means a well-placed repeater anywhere in the chain makes a big difference even if it can't hit the farthest endpoints directly.

---

## Hops and why they matter

A "hop" is one relay between a sender and receiver. A Companion node 20 miles from another Companion probably can't reach it directly — but if there's a Repeater halfway between them, the message goes Companion → Repeater → Companion in two hops.

MeshCore supports up to 64 hops. Meshtastic typically caps at 3–7 in practice. More hops means more total range but each hop adds latency and airtime cost.

**What operators worry about:**
- Every hop burns airtime for every node in range. Ten hops is ten broadcasts competing with each other's messages.
- Long-hop paths are fragile — if any intermediate node goes offline, the path breaks and the mesh has to rediscover.
- "Hop farms" (chains of many repeaters with no real coverage between them) look impressive on paper but deliver less than you'd expect.

A well-designed mesh has a few high-reach backbone nodes on hills, connected by 2–3 hop paths to most users, not long chains of adjacent repeaters.

---

## Why does it take hours for a new node to start routing traffic?

MeshCore builds routing state over time. When you first power up a new Repeater, it announces itself (via adverts), and nearby nodes learn about it. But the routing decisions other nodes make — "should I route through this new repeater for packets heading in that direction?" — depend on observed link quality, which takes a while to converge.

Expect something like:

- **Minute 0:** Node powers up, sends first flood advert. Some nearby nodes record its existence.
- **Minute 5–30:** More adverts from the new node propagate through the mesh. Other nodes' routing tables start including paths through it.
- **Hour 1–12:** Link quality observations accumulate. The mesh starts preferring the new node for traffic where it offers a better path than existing alternatives.
- **Day 1+:** Behavior is stable. The new node is integrated.

If your new Repeater seems to be online but "not really helping" after an hour, that's normal. Give it half a day. If after a day it still doesn't show up in traceroutes or observed paths, there is probably something wrong with the physical install (no LOS to other infrastructure) rather than something wrong with the firmware or routing.

---

## Do I still need a home repeater if there's one 1 mile from me?

Usually yes, provided yours is outdoor or attic-mounted. Reasons:

- Your indoor Companion probably can't reach the 1-mile repeater directly (walls, elevation). A repeater outside your house gives you a zero-hop link.
- Redundancy — if the other repeater goes down, yours fills the gap.
- The 1-mile repeater is probably at someone's house too; neither of you has perfect coverage alone.

Exception: if you're line-of-sight from your desk to a high-elevation repeater and your messages reliably get through, you don't need to add more noise to the mesh.

---

## Regional considerations for NH specifically

- **Seacoast (Portsmouth, Dover, Exeter):** flat-ish, coverage grows reliably with elevation.
- **Central NH (Concord, Manchester):** rolling hills, a few high points dominate (Stratham Hill, Pack Monadnock, Uncanoonucs).
- **White Mountains:** line-of-sight is excellent from summits but the terrain is harsh. Installs up there need to survive winter wind and ice.
- **Lakes Region:** mixed terrain, water can act as an RF mirror — some unusual long paths exist across lakes.

We coordinate regional coverage in Discord. If you're planning an install, share the proposed spot — someone may have already tried that location or know about a better nearby one.

---

## Related guides

- **[Hardware, Antennas & Enclosures](?section=hardware-setup)** — the physical build
- **[Power & Solar](?section=power-solar)** — if the spot has no mains power
- **[Mesh Network Basics](?section=mesh-basics)** — the underlying physics and architecture
