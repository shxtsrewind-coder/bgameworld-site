# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences matter equally (confirmed):

- **Daily puzzle regulars** who come back each day for the shared daily puzzles, streaks and the daily 7-game challenge, mostly on phones; casual and word-game leaning.
- **New visitors arriving from social posts** (Facebook, TikTok, Pinterest; the worker schedules these) who need to understand what the site is and start a game within seconds.

## Product Purpose

BGameWorld is a free portal of short daily browser games. The homepage's job is to get a visitor into a game fast and to give regulars a reason to return each day. Success is a visitor starting a game, and a regular finishing today's set.

## Positioning

Every game has one daily puzzle shared by every player, resetting at midnight UTC, plus a daily 7-game challenge (7 of the 11 games, picked the same for everyone each day) with an optional leaderboard. All free, no install, no sign-up wall.

## Operating Context

- Static site served by a Cloudflare Worker (`wrangler.jsonc`, `src/worker.js`); the worker also runs scheduled social posting and Pinterest feeds. No build step.
- Each game lives on its own subdomain (`<game>.bgameworld.com`) in a separate codebase; the homepage links out to them.
- Accounts, profiles and challenge scores are in Supabase (`portal_profiles`, `portal_challenge_scores`); each game reports its own challenge score using the access token passed in the URL fragment.
- Monetised with Google AdSense; the site must stay acceptable to AdSense review (no unprompted pop-ups gating content).

## Capabilities and Constraints

- 11 live games: When & Where, Wordezy, Wordezy Search, Wordezy Scramble, Wordezy Ladder, Sortezy, Lingoezy, Linkezy, Warmezy, Letterezy, Mergezy. Coming soon: Jetpack Surge, Crossword.
- Game list is edited in `index.html` (`GAMES`, `COMING`); the JSON-LD and footer are kept in step with it.
- Accounts are optional; playing never requires one.

## Brand Commitments

- Name **BGameWorld** and its logo/icon (`logo.webp`, `icon.webp`, favicons) stay.
- Game names keep the "-ezy" family naming.
- Visual reference pinned by the owner: the feel of the New York Times' own games hub (light, editorial, calm, each game a flat colour tile with a drawn icon), **under BGameWorld's own brand**: never the NYT name, logo, "T" mark, or its licensed typefaces (Cheltenham, Karnak, NYT Franklin), and no copying of NYT game art, code, word lists or puzzles.

## Evidence on Hand

- Real game descriptions (the `blurb`s in `index.html`) and FAQ answers.
- Painted per-game posters and banners in `art/` (still used for social; retired from the homepage tiles by owner decision).
- No player counts, ratings, press or testimonials exist; none may be invented.

## Product Principles

1. One tap from arrival to a game.
2. "Today" first: the shared daily puzzle is the reason to come back.
3. Free and honest: no sign-up walls, ads disclosed, data use explained.
4. The challenge is optional and never blocks play.
