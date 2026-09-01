# Style

The reader is usually stuck, often outdoors, and sometimes on a phone. Write for
that person.

## Voice

- **Second person, present tense.** "Open the Meshtastic app and tap Radio
  Configuration" — not "the user should open" or "we will now open."
- **Action before theory.** Say what to do, then explain why if it helps. Someone
  mid-setup will read the first line and skip the paragraph.
- **Concrete values.** `MediumFast`, `906.875 MHz`, `Region: US`. Not "the
  appropriate preset."
- **Plain words.** "Your node won't show up" beats "visibility will be
  impaired."

## Structure

- Open with one or two sentences saying what the page gets the reader, and who
  it's for. If a different guide fits them better, link it right there.
- `##` for major steps, `###` beneath. Don't nest further.
- Numbered lists for ordered steps. Bullets for options and symptom lists.
- Put troubleshooting at the end, as a symptom → cause → fix table where possible.
- Long guides earn a summary table at the bottom. Short ones don't need one.

## Technical detail

- **Name the version.** "As of firmware 2.5.x, this lives under Radio
  Configuration → LoRa." Menus move between releases, and a dated statement is
  repairable in a way that a wrong one isn't.
- **Say which protocol.** We run Meshtastic and MeshCore side by side. If a step
  applies to only one, say so in the sentence itself — readers arrive from search
  and skip headings.
- **Placeholders in code, in caps:** `<REGION>`, `<pubkey>`, `YOUR_USERNAME`.
  Keep them inside backticks or a fence, both so they read as placeholders and
  because bare angle brackets aren't allowed in prose.
- **Real commands, copy-pasteable.** Include the flags. Don't abbreviate a command
  into something that won't run.

## Linking

- Other KB pages: `[MQTT Setup](?section=mqtt-auth)`. Not a full URL.
- External: full `https://` URL, no shorteners.
- Link the specific page, not a site's front door.

## What not to write

- No credentials, keys, tokens, or personal information — including in
  screenshots.
- No promises about what the network will do in future. Guides describe what
  exists.
- Don't disparage other mesh projects or communities. We interoperate with our
  neighbors and share operators with them.
- Don't document a workaround for something already fixed upstream without saying
  which versions still need it.
