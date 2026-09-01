<!-- Thanks for improving the NHMesh knowledge base. Nothing here is
     bureaucracy — every line is something a reviewer would otherwise have to
     ask you about, which is what makes reviews slow. -->

## What changed

<!-- One or two sentences. Which guide, and what is different now? -->

## How do you know it's right

<!-- The most useful thing you can tell a reviewer. Pick whichever applies:
     - I run this setup and these are the settings that work for me
     - I followed the guide as written and hit the step that is wrong
     - Source: <link to firmware docs, release notes, upstream issue>
     Reviewers cannot verify every claim on real hardware, so where a fact
     comes from matters more than how confident it sounds. -->

## Checklist

- [ ] I updated `last_reviewed` in the frontmatter of every guide I touched
- [ ] Links are full `https://` URLs (no shorteners) or `?section=<guide-id>` for KB pages
- [ ] I did not paste anyone's credentials, keys, or personal information
- [ ] `python3 tools/kb.py validate` passes locally (CI runs it too)

<!-- Adding a brand new guide? Also add it to the right section in the
     frontmatter and pick an `order`. You do not edit index.json — it is
     generated. -->
