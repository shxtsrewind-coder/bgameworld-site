# Social posts

Makes BGameWorld's scheduled Facebook and Pinterest posts. The Worker in `src/` posts them; this folder only builds them.
It is not served by the website (`tools` is in `.assetsignore`).

Setup (once per machine): clone the game repos the checks read from, into `/home/claude/repos` (or set `BGW_REPOS`):

    for r in wordezy wordezy-ladder Wordezy-Scramble letterezy Warmezy Lingoezy; do
      git clone --depth 1 https://github.com/shxtsrewind-coder/$r.git; done

Needs Python 3 with playwright, numpy and Pillow, plus Node 22+ (it runs Scramble's and the homepage's own code).

- `gamedata.py`: word lists, rules and checks for each game (every puzzle must have exactly one answer).
- `design.py`: the post, Pin and answer-page look, from DESIGN.md (white paper, ink, one colour per game).
- `render.py`: screenshots each post with Chromium and flags anything that spills off the card.
- `nov.py`: the puzzles for 13-26 Nov 2026 (p061-p116), the builders for each game, and `publish()`.
- `dec.py`: the puzzles for 27 Nov - 10 Dec 2026 (p117-p172). It reuses nov.py's builders and checks that no
  answer repeats an earlier post. Copy it for the next batch (new ids, start date and Linkezy file).
- `instagram.py`: Instagram carousels (the puzzle, then the answer, as JPEG slides in social/ig/) and puzzle Reels,
  written to src/instagram.json and posted by src/worker.js through src/instagram.js.
- `challenge.py`: the Daily Seven posts, e.g. `python3 challenge.py 2026-11-27 2026-12-10`.

Outputs: `social/fb/<id>.png` (1080x1350), `social/pin/<id>.jpg` (1000x1500), `a/<id>/index.html`,
and new rows in `src/posts.json` and `src/pins.json`.
