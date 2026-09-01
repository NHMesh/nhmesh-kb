# NHMesh Knowledge Base

The guides behind the **Knowledge Base** tab on [nhmesh.live](https://nhmesh.live).
This repository is the source of truth for that content. Edits merged here appear
on the site within a few minutes.

NHMesh is an independent, community-run LoRa mesh network covering New Hampshire
and the surrounding region. These guides are how someone goes from "I bought a
radio" to "my node is on the map."

## Contributing

**Yes, please.** Fix a typo, correct a setting that changed with a firmware
release, or write a guide for the thing you had to figure out the hard way.

- Small fix → edit the file on GitHub and open a pull request.
- Not sure it's right, or don't want to write it → [open an issue](../../issues/new/choose).
  Reporting that a guide is wrong is a real contribution.

[`CONTRIBUTING.md`](CONTRIBUTING.md) has the details, but the short version is:
edit a file in `guides/`, bump `last_reviewed`, open a PR.

## Layout

| Path | What it is |
|---|---|
| `guides/*.md` | The guides. One file per page, YAML frontmatter on top. |
| `sections.json` | Section names and their order in the sidebar. |
| `tools/kb.py` | Validates the content and renders what the site serves. |
| `tools/test_kb.py` | Adversarial tests proving the validator rejects what it claims to. |
| `deploy/` | How merged content reaches the web host. |

**`index.json` is generated, not edited.** It used to be hand-maintained, which
meant every concurrent change collided in the same file. It is now built from each
guide's frontmatter, so adding a page means adding a page.

## Working locally

No dependencies beyond Python 3.9+.

```sh
python3 tools/kb.py validate    # check everything, same as CI
python3 tools/kb.py build dist  # render guides/ + index.json into dist/
python3 tools/test_kb.py        # exercise the validator against hostile input
```

## How this reaches the site

The web host polls this repository, validates it with **its own** pinned copy of
`tools/kb.py`, renders the guides, and moves them into place one atomic rename at
a time. Content from this repository is never executed, and a build that fails
validation leaves the published site untouched.

That design is deliberate: it means a merged pull request can change what
nhmesh.live *says*, and nothing else. See [`SECURITY.md`](SECURITY.md).

## License

Guide content is [CC BY-SA 4.0](LICENSE) — use it, adapt it, translate it for your
own mesh community, with attribution and under the same license. The scripts in
`tools/` and `deploy/` are MIT; see [`tools/LICENSE`](tools/LICENSE).
