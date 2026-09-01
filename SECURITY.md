# Security

## Reporting

Report anything security-relevant privately through
[GitHub security advisories](https://github.com/NHMesh/nhmesh-kb/security/advisories/new).
Please don't open a public issue for it.

That includes content problems, not just code: a merged guide that links somewhere
malicious, or that instructs readers to do something unsafe with their node or
their credentials, is a security issue here.

## What this repository is allowed to do

This is a public repository that accepts pull requests from anyone, and its
content is published to a production site. The design goal is that **a merged
pull request can change what nhmesh.live says, and nothing else.**

Concretely:

**No secrets exist here.** No registry credentials, no deploy tokens, no cloud
keys, nothing that reaches infrastructure. The knowledge base was deliberately
extracted from the application repository — which does hold those things — rather
than making that repository public. A fork PR has nothing here to steal.

**CI runs untrusted code with no privileges.** Validation uses `pull_request`, not
`pull_request_target`. `pull_request_target` runs with the base repository's write
token while checking out the contributor's branch, which is the usual way public
repositories are compromised through a fork. Workflows declare `contents: read`
and third-party actions are pinned to commit SHAs, not tags.

**The web host never executes code from this repository.** It downloads the
content, then validates and renders it with its own pinned copy of `tools/kb.py`,
which lives outside the download and cannot be written by it. If the host ran the
tarball's `tools/kb.py`, merging a documentation change would be remote code
execution on the production host. It doesn't.

**Publishing fails closed.** Validation runs again on the host before anything is
swapped in — CI passing is not treated as proof. Fetch failure, validation
failure, or a malformed archive all leave the currently published content exactly
as it was. Files are replaced by atomic rename, and `index.json` is written last
so the manifest never references a guide that isn't on disk.

**Rendering escapes HTML.** The site renders guides with `react-markdown` and no
`rehype-raw`, so raw HTML in markdown is escaped rather than executed, and link
targets are filtered before they reach the DOM. The validator rejects raw HTML
too, so this holds at both ends.

> **Standing constraint:** adding `rehype-raw` (or any equivalent raw-HTML pass)
> to the site's markdown renderer would turn every merged pull request into
> stored XSS on nhmesh.live. Don't. If rich formatting is ever genuinely needed,
> extend the markdown, not the HTML surface.

## Reverting bad content

Publishing tracks a ref the host controls, not whatever is newest:

- Write a commit SHA to `/etc/nhmesh-kb/PUBLISHED_REF` to pin the site to known-good
  content. The next sync moves it there and holds.
- `systemctl stop kb-sync.timer` freezes publishing entirely.

Neither requires a git revert, a rebuild, or a deploy, so recovering from a bad
merge doesn't depend on being able to push.

## Branch protection

`main` requires a pull request, a passing `Validate` check, and an approving
review. Force-push and deletion are blocked, and `CODEOWNERS` is enforced so
changes to the validator, workflows, and publish scripts need an owner's approval
regardless of who else signed off.
