---
name: BGameWorld
description: Today's edition of a puzzle page. White paper, black ink, one flat colour per game.
colors:
  ink: "#121212"
  ink-2: "#4A4A4A"
  ink-3: "#6B6B6B"
  paper: "#FFFFFF"
  paper-2: "#F4F4F1"
  rule: "#DCDCD7"
  field-stroke: "#8A8A8A"
  focus: "#2860D8"
  error: "#B3261E"
  success: "#1E6B3A"
  tile-wordezy: "#7CC4A4"
  tile-wordezy-search: "#F5C54A"
  tile-wordezy-scramble: "#F4977A"
  tile-wordezy-ladder: "#9CC3F0"
  tile-warmezy: "#F7A35C"
  tile-letterezy: "#D9C792"
  tile-lingoezy: "#79D0CF"
  tile-sortezy: "#C9A8EC"
  tile-linkezy: "#F28FA2"
  tile-mergezy: "#8FA9F5"
  tile-when-and-where: "#E8B96A"
typography:
  display:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "clamp(2.6rem, 6vw, 4.4rem)"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "-0.02em"
  display-page:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "clamp(40px, 9vw, 60px)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
  headline-dialog:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "clamp(1.7rem, 5vw, 2.2rem)"
    fontWeight: 700
    lineHeight: 1.05
  headline-lg:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "34px"
    fontWeight: 700
    lineHeight: 1.1
  headline:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "30px"
    fontWeight: 700
    lineHeight: 1.1
  headline-sm:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "26px"
    fontWeight: 700
    lineHeight: 1.1
  wordmark:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "25px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.01em"
  title:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "23px"
    fontWeight: 700
    lineHeight: 1.1
  title-sm:
    fontFamily: "Zilla Slab, Rockwell, Roboto Slab, Georgia, serif"
    fontSize: "20px"
    fontWeight: 700
    lineHeight: 1.2
  body:
    fontFamily: "Libre Franklin, Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  body-reading:
    fontFamily: "Libre Franklin, Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.65
  body-sm:
    fontFamily: "Libre Franklin, Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.45
  date:
    fontFamily: "Libre Franklin, Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 700
    lineHeight: 1.2
  button:
    fontFamily: "Libre Franklin, Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1
  nav:
    fontFamily: "Libre Franklin, Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 600
    lineHeight: 1.5
  label:
    fontFamily: "Libre Franklin, Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 600
    lineHeight: 1.5
rounded:
  tile-sm: "6px"
  field: "8px"
  tile-md: "10px"
  card: "12px"
  dialog: "14px"
  pill: "999px"
spacing:
  gutter-phone: "20px"
  gutter-tablet: "40px"
  gutter-desktop: "64px"
  container: "1280px"
  grid-gap: "20px"
  card-pad: "14px 18px 16px"
  tap-min: "44px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "0 22px"
    height: "44px"
  button-primary-hover:
    backgroundColor: "#333333"
    textColor: "{colors.paper}"
  button-outline:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "0 22px"
    height: "44px"
  button-outline-hover:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
  button-compact:
    typography: "{typography.button}"
    rounded: "{rounded.pill}"
    padding: "0 16px"
    height: "40px"
  header:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    height: "64px"
  subnav-link:
    textColor: "{colors.ink}"
    typography: "{typography.nav}"
    padding: "0 12px"
    height: "44px"
  daily-seven-tile:
    rounded: "{rounded.tile-sm}"
    size: "40px"
  game-card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "{spacing.card-pad}"
  game-card-band:
    height: "96px"
  game-card-row-tile:
    rounded: "{rounded.tile-md}"
    size: "64px"
  challenge-dialog:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.dialog}"
    padding: "36px"
    width: "min(680px, calc(100vw - 24px))"
  challenge-thumb:
    rounded: "{rounded.tile-md}"
    size: "76px"
  challenge-path:
    backgroundColor: "{colors.paper}"
    rounded: "{rounded.card}"
    padding: "18px"
  challenge-note:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "10px 12px"
  input-field:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.field}"
    padding: "0 12px"
    height: "46px"
  footer:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink-2}"
    padding: "44px 0 32px"
  info-box:
    backgroundColor: "{colors.paper-2}"
    rounded: "{rounded.card}"
    padding: "18px 20px"
---

# Design System: BGameWorld

## Overview

**Creative North Star: "Today's Edition"**

BGameWorld reads like the day's puzzle page of a good newspaper: one calm, light sheet, dated at the top, where every game is a flat colour tile carrying its own drawn icon. "Today" is the headline. The date, the reset countdown and the Daily Seven sit above the games because the shared daily puzzle is the reason to come back. Everything else is paper, ink and hairline rules.

The density is a broadsheet's, not a dashboard's. Sections are separated by printed rules instead of boxes and backgrounds. Colour lives almost entirely in the game tiles, so the page's colour is the games themselves; the chrome around them stays black and white. Motion is held back to one signature: on hover or keyboard focus, a tile's icon performs a tiny version of its game's move, once, then rests.

The owner pinned the feel of the New York Times games hub, carried out entirely in BGameWorld's own materials: its own name, badge and logo, its own self-hosted faces (Zilla Slab and Libre Franklin, both SIL OFL), and its own authored icons. The dark neon game-portal template is rejected: no glows, gradient headlines, poster carousels or letter-spaced labels above headings.

**Key Characteristics:**
- White paper ground, near-black ink, warm hairline grey rules.
- One flat, light, saturated colour per game; ink icons sit on it.
- Slab headlines and game names; a sturdy grotesque for everything else.
- Black pill for the action, ink-outlined pill for the alternative.
- Flat at rest; a soft lift on card hover and a shadow under the dialog are the only depth.
- One tiny, game-specific icon move on hover or focus; nothing under reduced motion.

## Colors

The page is paper and ink, with colour reserved for the games: eleven flat tile colours that each belong to one game and nothing else.

### Primary
- **Newsprint Ink** (ink): Headlines, body copy, the primary pill, the 3px section rules, the outline of secondary pills, and every stroke and fill in the game icons. Near-black rather than pure black, so it reads printed rather than digital.

### Neutral
- **Paper White** (paper): The page ground, cards, dialog, input fields, and the white paper fills inside icons.
- **Second Paper** (paper-2): A slightly warm off-white, used on purpose as the page's second sheet: the footer ground, the hover fill of outline pills and the dialog close button, the dialog's offline note, and the boxed notes on the privacy and terms pages. It marks quieter zones without making a new colour.
- **Soft Ink** (ink-2): Secondary text: descriptions, FAQ answers, the reset countdown, footer links (8.9:1 on white).
- **Pencil Grey** (ink-3): Tertiary text: game counts, category labels, placeholders, the legal line (5.3:1 on white).
- **Hairline Grey** (rule): Every 1px rule: header and sub-nav bottoms, card borders, FAQ dividers, list rows.
- **Field Stroke** (field-stroke): The 1.5px border of text inputs at rest. It turns to ink on focus.

### Functional
- **Focus Blue** (focus): The 3px focus outline on every interactive element (offset 3px; 1px on inputs). The only blue in the chrome.
- **Error Red** (error): Inline form error messages.
- **Success Green** (success): Confirmation and "you're in" messages in the dialog.

### Game Tiles
Each game owns one tile colour. It appears on the game's card band, its phone row square, its Daily Seven square and its dialog thumbnail, always with the ink icon on top.
- **Wordezy**: Sage Green (tile-wordezy)
- **Wordezy Search**: Yolk Yellow (tile-wordezy-search). Also the text-selection highlight across all pages.
- **Wordezy Scramble**: Salmon (tile-wordezy-scramble)
- **Wordezy Ladder**: Sky Blue (tile-wordezy-ladder)
- **Warmezy**: Tangerine (tile-warmezy)
- **Letterezy**: Parchment Tan (tile-letterezy)
- **Lingoezy**: Aqua (tile-lingoezy)
- **Sortezy**: Lilac (tile-sortezy)
- **Linkezy**: Rose (tile-linkezy)
- **Mergezy**: Periwinkle (tile-mergezy)
- **When & Where**: Honey (tile-when-and-where)

The colours are set per game in the `GAMES` array and passed to each tile as the `--tile` custom property.

### Named Rules
**The One Colour Per Game Rule.** A tile colour belongs to exactly one game and appears only where that game appears. A new game gets a new flat colour, light enough that #121212 ink reads on it. Chrome, buttons and headings never borrow a tile colour.

**The Second Paper Rule.** #F4F4F1 is the only off-white. Use it for quieter sheets (footer, notes, boxed asides) and for hover fills on paper-coloured controls, never as the main page ground.

**The No Gloss Rule.** Every colour is flat: no gradients, glows or glass, on tiles or anywhere else.

## Typography

**Display Font:** Zilla Slab 700 (600 also shipped), falling back to Rockwell, Roboto Slab, Georgia, serif
**Body Font:** Libre Franklin, variable 100–900, falling back to Franklin Gothic Medium, Helvetica Neue, Arial, sans-serif

**Character:** A bold slab with a newspaper headline's weight, paired with a plain, sturdy grotesque. The slab carries everything you might call a name (the page title, section heads, game names, the wordmark); the grotesque carries everything you read or press. Both are self-hosted from `/fonts/` under the SIL Open Font License, and the slab 700 and Franklin files are preloaded.

### Hierarchy
- **Display** (700, clamp(2.6rem, 6vw, 4.4rem), 0.95, -0.02em): The homepage masthead, "Today's puzzles", sharing a baseline with the date on desktop.
- **Display Page** (700, clamp(40px, 9vw, 60px), 1): The H1 on the privacy and terms pages.
- **Headline Dialog** (700, clamp(1.7rem, 5vw, 2.2rem), 1.05): The challenge dialog title.
- **Headline LG / Headline / Headline SM** (700; 34px, 30px and 26px; 1.1): The FAQ heading, the "All games" heading and the Daily Seven heading, in that order. The Daily Seven drops to 23px below 600px. Legal-page H2s use 24px at 1.2.
- **Wordmark** (700, 25px, -0.01em; 21px below 720px): "BGameWorld", set beside the badge in the header.
- **Title** (700, 23px, 1.1; 20px in phone rows): Game names on cards.
- **Title SM** (700, 20px, 1.2–1.3): FAQ questions and dialog sub-panel heads (guest / sign-up / leaderboard). Footer column heads use 18px.
- **Body** (400, 16px, 1.5): Default copy. FAQ answers are capped at 34em and dialog intros at 56ch.
- **Body Reading** (400, 17px, 1.65): Long-form text on the privacy and terms pages, in a 720px column.
- **Body SM** (400, 15px, 1.45): Card descriptions (14.5px/1.35 in phone rows), the reset countdown, the game count, footer links.
- **Date** (700, 18px; 16px below 600px): The edition date in the masthead.
- **Button / Nav** (600, 15px; 14px in compact pills): Pill labels and header links.
- **Label** (600–700, 13px, sentence case): The category under a card and the "In today's seven" badge.

Numbers that tick or rank (the countdown, leaderboard ranks and scores) use tabular figures.

### Named Rules
**The Slab Names Things Rule.** Zilla Slab is for titles and names only: the page title, section heads, game names, the wordmark, leaderboard ranks, and letters drawn inside icons. Body, buttons, labels and navigation are always Libre Franklin.

**The Sentence Case Rule.** Labels stay in sentence case at normal tracking. No uppercase, letter-spaced labels anywhere, and nothing set above a heading.

## Layout

A single 1280px column centred on the page, with side gutters of 20px on phones, 40px from 768px and 64px from 1200px. The homepage reads top to bottom like a front page: sticky header, masthead (title left; date and countdown right, on the same baseline), the Daily Seven band, the games grid, the FAQ, then the footer.

- **Games grid:** `repeat(auto-fill, minmax(220px, 1fr))` with a 20px gap, so four across at desktop widths. Below 560px the grid becomes a single list of rows separated by hairlines (no gap).
- **Daily Seven band:** a three-column grid (text | seven squares | pill) that stacks into one column below 960px, with the pill aligned left.
- **FAQ:** one column; from 880px each item splits question | answer at 0.9fr / 1.4fr with a 32px gap.
- **Footer:** three columns (logo | games in two text columns | site links), which becomes two columns below 768px with the logo spanning the full row.
- **Header:** 64px tall and sticky. Below 720px the text links move to a 44px sub-nav row under the header and the challenge pill's label shortens to "Challenge".
- **Legal pages:** a single 720px reading column.
- **Rhythm:** vertical padding is set per band rather than from a strict scale: 20–56px around the games, 52–64px around the FAQ, 44px at the top of the footer. Every tap target is at least 44px tall on phones, and the footer bottom adds the safe-area inset.

## Elevation & Depth

The system is flat. Depth comes from printed rules and the second paper, not from layers. Only two shadows exist: a soft lift when the pointer is over a card, and the dialog sitting above a dimmed page.

### Shadow Vocabulary
- **Card lift** (`box-shadow: 0 10px 24px -14px rgba(18,18,18,.35)`, with the border darkening to #B9B9B3): Card hover only, on desktop. It is turned off in phone rows.
- **Dialog** (`box-shadow: 0 24px 60px -20px rgba(0,0,0,.45)`), over a backdrop of `rgba(18,18,18,.5)`: The challenge dialog.
- **Header veil** (`rgba(255,255,255,.96)`): The sticky header's near-opaque paper. It is not blurred and not glass.

### Named Rules
**The Two Rules Rule.** A 3px ink rule starts a new part of the edition: under the masthead, above the FAQ, above the dialog leaderboard, and under the "last updated" line on legal pages. A 1px hairline separates items within a part. Never use any other rule weight.

**The Flat By Default Rule.** Surfaces rest flat. A shadow appears only as a response (card hover) or for a true overlay (the dialog).

## Shapes

Gently rounded rectangles, getting rounder as the object gets bigger, plus full pills for actions. Small 6px corners on the 40px Daily Seven squares; 8px on inputs and notes; 10px on the 64px phone-row squares and the dialog thumbnails; 12px on cards, dialog panels and legal-page boxes; 14px on the dialog itself; 999px pills for every button. Circles are used only for the dialog's close button and the 8px "today" dot. Inside cards the colour band runs edge to edge and is clipped by the card's corner. Icons use small 1.5–4 unit corner radii on their drawn tiles, matching this language.

## Components

### Buttons
Tactile and plain, like a stamped ticket.
- **Shape:** Full pill (999px), at least 44px tall; 40px in the header and on desktop cards.
- **Primary:** Ink fill with white text, 600 weight at 15px, 22px side padding. Hover lightens it to #333. Use it for the one action in each band ("Start today's challenge", "Play", "Sign up").
- **Outline:** Paper fill with a 1.5px inset ink ring and ink text. Hover fills with Second Paper. Use it for the header's "Today's challenge" and "Continue as guest".
- **Disabled:** 45% opacity with a not-allowed cursor.
- **Focus:** The global 3px Focus Blue outline, offset 3px.
- **Text links in the dialog:** 600 weight, ink, underlined with a 3px offset.

### Header and Phone Sub-nav
- A sticky paper bar, 64px tall, with a hairline underneath. On the left, the cropped `icon.webp` badge and the slab wordmark. On the right, "All games" and "FAQ" (600, 15px; hover adds a 2px underline at a 5px offset), with the outline challenge pill last as the header's one action.
- Below 720px the links move into a 44px-tall sub-nav row (All games, FAQ, Privacy) with its own hairline, and the pill reads "Challenge".

### Masthead
- The Display "Today's puzzles" H1, with the edition sitting opposite on the same baseline: the full date in 700 and "New puzzles in Xh Ym" in Soft Ink with tabular figures. Below 600px everything stacks and aligns left. The masthead closes with the 3px ink rule.

### Daily Seven Band
- A slab headline, one line of explanation (52ch max), a row of seven 40px tile squares (6px corners, 6px gaps, 28px icons, each with the game's name as its accessible label), and the black "Start today's challenge" pill. A hairline closes the band.

### Game Card (desktop)
- **Corner Style:** 12px, with a 1px hairline border and overflow clipped.
- **Band:** A 96px flat band in the game's tile colour, with the 66px icon centred on it.
- **Body:** 14px 18px 16px padding. The slab name, then the one-line description in Soft Ink, then a footer row holding the badge or category on the left and a compact "Play" pill on the right.
- **Badge:** If the game is in today's seven, an 8px ink dot plus "In today's seven" (700, 13px). Otherwise the category in Pencil Grey (600, 13px).
- **Hover / Focus:** Card lift (see Elevation), plus the icon move. Focus uses the global outline at a 2px offset.
- The whole card is one link. The Play pill inside it is decorative (`aria-hidden`).

### Game Card (phone row)
- Below 560px each card becomes a row: a 64px colour square with 10px corners and a 42px icon | the name (20px), the line (14.5px) and the badge | a 44px Play pill. Rows are divided by hairlines, with no border, radius or hover shadow.

### Challenge Dialog
- A centred paper sheet, at most 680px wide, with 14px corners and the Dialog shadow over a 50% ink backdrop. Opening fades it in and eases it up from -47% to -50% over 0.3s on the house ease. A 44px circular close button sits top right. Focus is trapped inside, and Escape or a backdrop click closes it.
- **Contents:** the slab title, the date, a short intro, then seven 76px thumbnails (10px corners, a 12px 600 name underneath; a four-column grid below 600px).
- **Gate state:** two 12px-cornered hairline panels side by side from 600px: "Play as guest" (outline pill) and "Sign up to compete" (inputs plus primary pill, a sign-in toggle, and fine print in 13px Pencil Grey).
- **Offline state:** a Second Paper note at the top of the sign-up panel. The submit button and the toggle are disabled.
- **Playing state:** a 700 16px Success Green status line, the seven thumbnails as new-tab links, and an optional underlined "Sign up or sign in" link for guests.
- **Leaderboard:** opens with a 3px ink rule. Each row is separated by a hairline and shows a slab tabular rank, the name (truncated with an ellipsis) and a 700 tabular score.

### Inputs / Fields
- **Style:** 46px tall, with a 1.5px Field Stroke border, 8px corners, white fill, 16px Libre Franklin, and placeholders in Pencil Grey. Labels are visually hidden but present.
- **Focus:** a 3px Focus Blue outline at a 1px offset, and the border turns to ink.
- **Error:** a red border with `aria-invalid`, plus an Error Red message in the live status line.

### FAQ List
- A description list. Each item has a hairline on top and the last item also has one underneath. Questions are Title SM slab; answers are Soft Ink body. From 880px each item is a two-column question | answer row.

### Footer
- A Second Paper ground with a hairline on top. The logo is 160px wide, followed by an 18px slab column head and Soft Ink links that turn to ink and underline on hover. The legal line sits below a hairline in 14px Pencil Grey.

### Game Icons (signature)
- Every game has an authored inline SVG on a **64-unit viewBox**, drawn in **ink #121212 on the tile colour**, with white used only as a paper fill inside ink outlines or as type inside ink shapes. There is **one stroke weight, 2.5**, with round caps and joins where lines end. Letters drawn inside icons are Zilla Slab 700.
- Each icon marks the part that performs its game's move as `.mv`, and names the keyframes in the `--move` custom property (flip, sweep, spin, climb, tip, pop, draw, rise, lift, bob, gather). On card hover or focus, the move plays **once** for 0.9s on the house ease, then the icon rests. Under `prefers-reduced-motion: reduce` there is no move at all.
- Icons inside a card are decorative (`aria-hidden`). In the Daily Seven squares they carry the game's name as their label.

### Named Rules
**The One Move Rule.** An icon moves only in answer to hover or focus, performs its own game's move once, and stops. It never loops, never plays on load, and never moves under reduced motion.

**The Ink On Colour Rule.** Game art is always drawn in ink on its flat tile colour. Never use photos, painted posters, emoji or glyph characters as game tiles.

## Do's and Don'ts

### Do:
- **Do** give each game exactly one flat tile colour and draw its icon in #121212 on a 64-unit viewBox at a 2.5 stroke.
- **Do** set titles and game names in Zilla Slab 700, and everything else in Libre Franklin, both self-hosted.
- **Do** use a black pill (999px) for the single action in a band, and an ink-outlined pill for the alternative.
- **Do** separate parts of the page with the 3px ink rule and items within a part with the 1px #DCDCD7 hairline.
- **Do** use #F4F4F1 as the second paper for the footer, notes and hover fills.
- **Do** keep every tap target at least 44px on phones, and keep the 3px #2860D8 focus outline on everything interactive.
- **Do** keep the BGameWorld name, badge and logo, and the "-ezy" game names.

### Don't:
- **Don't** use the New York Times name, logo or "T" mark, or its licensed typefaces (Cheltenham, Karnak, NYT Franklin), and don't copy NYT game art, code, word lists or puzzles.
- **Don't** use gradients, glows, glass, neon or dark portal grounds.
- **Don't** put letter-spaced uppercase labels or any text above a heading.
- **Don't** reuse a game's tile colour on chrome, buttons or another game.
- **Don't** put the painted posters from `art/` back onto homepage tiles. They are for social only.
- **Don't** loop icon motion, play it on load, or run it under reduced motion.
- **Don't** add shadows to surfaces at rest.
