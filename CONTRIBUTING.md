# Contributing

This knowledge base is maintained by the people who use the network. If you have
put up a node, you know something worth writing down.

You do not need to be an expert, and you do not need to write well. A reviewer
can fix wording. Nobody can fix a guide that says the wrong thing about firmware
they have never run.

## The quickest useful contribution

Find a guide that's wrong. Click the pencil icon on GitHub. Fix it. Open a pull
request. That's the whole process.

## Making a change

Guides live in `guides/`, one markdown file per page. Each starts with frontmatter:

```yaml
---
id: meshtastic-setup          # must match the filename
title: Meshtastic Node Setup  # sidebar label, 80 characters or fewer
section: setup                # a section id from sections.json
order: 1                      # position within that section
last_reviewed: 2026-09-01     # bump this whenever you touch the guide
---
```

Then write markdown below it.

**Always bump `last_reviewed`.** It drives the monthly sweep that finds rotting
pages. Reading a guide, confirming it's still accurate, and bumping the date
without changing anything else is a genuinely valuable pull request — it is how
we tell "still correct" apart from "nobody has looked in a year."

### Adding a new guide

1. Create `guides/<your-id>.md` with the frontmatter above.
2. Pick a `section` from `sections.json` and an `order` no other guide in that
   section uses.
3. Run `python3 tools/kb.py validate`.

Do not edit `index.json` — it doesn't exist in this repo. It's generated at build
time from your frontmatter, so new guides can't collide in it.

### Checking your work

```sh
python3 tools/kb.py validate
```

Python 3.9+, nothing to install. CI runs the same command, and so does the web
host before it publishes anything.

## Rules the validator enforces

These are checked automatically, so you'll hear about it before a human does.

- **No raw HTML.** The site renders markdown with HTML escaped. Angle brackets in
  a placeholder like `<REGION>` are fine inside backticks or a code fence — that's
  where they belong anyway.
- **Links are `https://`, or `?section=<guide-id>` for another KB page.** Plain
  `http://` is a downgrade we don't need to offer readers.
- **No link shorteners.** They hide the destination, which makes a link
  unreviewable. Paste the real URL.
- **Images live in `assets/` in this repo** and are referenced relatively.
  Hotlinking an external image hands that server the IP address of every reader.
- **Internal links must resolve.** A `?section=` or `./guide.md` link pointing at
  a guide that doesn't exist fails the build.

## Style

Short version: write like you're helping one person, not addressing an audience.
Second person, present tense, concrete steps with real values. Say what to do
before why it works. [`STYLE.md`](STYLE.md) has the rest.

Some things worth knowing:

- **Say which firmware or app version you're describing.** Most of our staleness
  comes from menus that moved between releases. A version number turns a wrong
  guide into a dated one, which is much easier to fix.
- **Both protocols.** We run Meshtastic *and* MeshCore. If something applies to
  only one, say so in the sentence, not just the section heading.
- **Don't paste credentials.** Not yours, not an example account's, not a
  screenshot with a key in the corner. Use obvious placeholders.

## Review

Content is reviewed by the maintainers; changes to `tools/`, `deploy/`, and
`.github/` need an owner's review because they decide what content is allowed to
exist and how it gets published.

If a review goes quiet for a week, comment on the PR and say so — that's not
rudeness, it's a bump, and it's welcome. Maintainers do this in their spare time.

## Licensing your contribution

Guide content is [CC BY-SA 4.0](LICENSE). Opening a pull request means you're
offering your contribution under that license and confirming it's yours to give
— not copied out of someone's manual, wiki, or forum post without permission.

Quoting a short passage with attribution is fine. Pasting a vendor's
documentation wholesale is not.
