---
version: 1
slug: "index-html"
primary_target: "index.html"
related_targets: []
---

# Homepage (bgameworld.com/)

Scope: the portal homepage `index.html` (plus the challenge dialog it contains). Visitor mode: **Persuade** — success is a visitor starting a game within seconds; for regulars, finishing today's set.

Audience and job: daily puzzle regulars (phones, morning ritual) and first-time arrivals from social posts, weighted equally. Action: open a game; secondary, start today's 7-game challenge. Proof: the real daily mechanism (shared puzzles, reset at 00:00 UTC, today's seven), shown live, not claimed. Constraints: AdSense-friendly (no unprompted pop-ups), static HTML, no build step, owner-pinned NYT-Games feel under BGameWorld's own brand (no NYT marks or licensed faces).

## Direction contract

THESIS: The homepage is today's edition of a puzzle page: one calm, light, editorial sheet where every game is a flat colour tile with its own drawn icon and "today" is the headline. It refuses the dark neon game-portal template (glows, gradient headlines, poster carousels, letter-spaced labels above headings).

OWN-WORLD: White paper ground, near-black ink #121212, hairline grey rules. Each game owns one flat, saturated tile colour; icons are authored SVG in ink on that colour, one stroke weight. Type: Zilla Slab bold for headlines and game names, Libre Franklin for everything else, both self-hosted. Buttons are black pills with white text; secondary buttons are outlined in ink. No gradients, no glow, no glass.

STORY: A visitor reads the date and "Today's puzzles", sees which seven games make today's challenge and when puzzles reset, taps a tile and plays. A regular checks the countdown, starts the challenge, and comes back tomorrow.

FIRST VIEWPORT: Header (icon + set wordmark left; Games, Today's challenge, FAQ right). A masthead row: H1 "Today's puzzles" in large slab type with the full date beside it on the same baseline and "New puzzles in 5h 12m" under the date. Directly beneath, the challenge strip: seven small colour squares for today's games, one line of explanation, a black "Start today's challenge" pill. Then the game tiles begin: four across on desktop (two rows visible at 1440x900), one column of tile rows on phones (colour square left, name and one-line description, Play button right).

FORM: Pinned by the owner (NYT Games feel), translated to BGameWorld's own materials; no concept roll. seed: none (unavailable)

SIGNATURE: On hover or keyboard focus, each tile's icon performs one tiny version of its game's move (a letter tile flips, a tube tips, a ladder rung lights), once, then rests; reduced motion keeps it still.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
