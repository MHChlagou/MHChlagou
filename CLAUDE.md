# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`MHChlagou/MHChlagou` is a GitHub profile repository: GitHub renders its `README.md` on the profile page at github.com/MHChlagou. The content is `README.md` plus the animated SVGs in `assets/`. There is no build, lint or test step; changes take effect when they are pushed to `main` on `origin`.

To check rendering before pushing, preview the Markdown in a GitHub-flavored renderer (GitHub's web editor preview is the reference, since profile READMEs use GitHub-specific rendering).

## README structure

The README is laid out top to bottom as:

1. A centered `<div align="center">` header: `assets/hero.svg` (name, role, tagline), contact badges (LinkedIn, email) using shields.io with `style=for-the-badge`, and `assets/terminal.svg`.
2. `#### 🎯 Focus` showing `assets/focus.svg` (focus areas and motto).
3. `#### 🔁 How I ship` showing `assets/pipeline.svg`.
4. `#### 🚀 Live on GitHub Pages`: one card SVG per repo with GitHub Pages enabled, each wrapped in a link to the live site. `assets/apps/lintel.svg` is the full-width featured card; the others are `width="49%"`, two per paragraph. Below them, a centered row of shields.io `website` badges (one per app, labeled with the repo name) reports real live status and links to the source repo.
5. Skill sections (`#### ⚙️ DevOps & Cloud`, `#### 🛡️ Security`), each a run of shields.io badges with `style=flat-square`, one badge per line.
6. A centered closing `<sub>` quote.
7. A trailing HTML comment from GitHub's profile README template; leave it in place.

Sections are separated by their `####` headings only; there are no `---` rules.

## Animated SVGs

GitHub strips scripts and inline styles from READMEs, so all animation lives in self-hosted SVGs loaded with `<img>`. They use SMIL (`<animate>`, `<set>`, `<animateMotion>`) and system font stacks only, because an SVG loaded as an image cannot fetch web fonts or external resources. Each has its own dark background so they read the same in GitHub's light and dark themes.

- `assets/terminal.svg` loops every 16s from a master clock (`<animate id="cycle" begin="0s;cycle.end">`). Each line appears with a `<set>` timed from `cycle.begin`. Typed commands use `textLength` to force an 8.4px glyph advance, so the discrete `width` steps on their `clipPath` and the moving cursor line up with characters. Changing a command means recomputing its step values, clip width and the start times of every later line.
- `assets/focus.svg` loops every 10s: a scan beam passes over each of the four cards in turn (queued, scanning, verified), then the header and "Verify always." turn green. Card text is plain and editable; subtitles fit about 38 characters.
- `assets/pipeline.svg` loops every 9s: the packet moves for 8s, then the board holds green. Each stage lights up at the `keyTimes` offset where the packet reaches it. Stage and gate labels are plain text and can be edited directly; keep gate labels at 14 characters or fewer or they overlap their neighbors.

- `assets/hero.svg` runs independent loops: a name shimmer (moving `gradientTransform`), a scan band, rotating rings and a check mark that draws itself.
- `assets/apps/*.svg` share one card frame: accent line on top, icon box, title, kicker, two description lines and stack chips, with a light sweep that is staggered per card. SVG text does not wrap, so description lines are split by hand (about 50 characters each on small cards). Each card has a small looping icon animation; the Lintel card shows a commit passing through its hook gate.

With linear interpolation (the default), SMIL ignores any animation whose `keyTimes` does not end at 1. Only `calcMode="discrete"` may end earlier.

When adding a Pages app, add a card SVG in the same style, link it to the live site, and add its status badge with the URL percent-encoded. Never put a hard-coded "live" indicator inside a card; status comes only from the badge.

## Conventions for edits

- Skill badges follow one pattern: `![Label](https://img.shields.io/badge/Label-HEXCOLOR?style=flat-square&logo=simpleicons-slug&logoColor=white)`. Use the tool's official brand color and its Simple Icons slug for `logo`. Use `logoColor=black` on light backgrounds (as on Linux and Vault). Spaces in the label are written as `_`.
- Keep contact badges on `style=for-the-badge` and skill and status badges on `style=flat-square`; the styles are intentional.
- The name, role and tagline appear in `assets/hero.svg`, `assets/terminal.svg` and the image alt text, and the focus areas appear in `assets/focus.svg` and its alt text. Update every copy when one changes.
