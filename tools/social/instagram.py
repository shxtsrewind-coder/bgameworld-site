"""Instagram, 7 posts a day: puzzle carousels (slide 1 the puzzle, slide 2 the answer), the Daily Seven and
puzzle Reels -> src/instagram.json.

Instagram captions can't hold working links, so each post answers itself: swipe for the answer, and
"link in bio" for the games. Images are JPEG (the only kind Instagram's API takes), 1080x1350 (4:5).

    python3 instagram.py      # renders social/ig/<id>.jpg + <id>-a.jpg for dec.py's puzzles, writes src/instagram.json

Schedule (UTC), each puzzle after its Facebook post (06:00, 09:00, 12:00 Daily Seven, 16:00, 19:00):
    07:30 puzzle 1 · 10:30 puzzle 2 · 12:30 Daily Seven · 15:00 Reel · 17:00 puzzle 3 · 20:00 puzzle 4 · 22:30 Reel
Reels are the puzzle Shorts (social/shorts/, nov.py's puzzles), 2 a day while they last.
Slots before FIRST are left out, so switching on part-way through a day doesn't post a burst of catch-ups.
"""
import json, re, pathlib, tempfile, datetime as dt
from playwright.sync_api import sync_playwright
import design as d, render, nov, dec, shorts_schedule as ss

SITE = d.SITE
OUT = SITE / "social" / "ig"
START, DAYS = dt.date(2026, 11, 27), 14                          # puzzles and Daily Seven 27 Nov - 10 Dec
FIRST = "2026-11-27T14:30:00Z"                                    # Instagram went from 3 to 7 a day at 14:00 UTC on 27 Nov
PUZZLE_AT, CH_AT, REEL_AT = ["07:30", "10:30", "17:00", "20:00"], "12:30", ["15:00", "22:30"]

# answer slide: a smaller headline, room for the explanation, and the visual scaled to fill what's left
ANS_CSS = """.ans h1{font-size:36px}.ans .sub{font-size:17px}.ans .close{width:430px}.ans .anstag{display:inline-block;margin:0 0 10px;padding:6px 12px;
border-radius:999px;background:#3A8B55;color:#fff;font:700 14px/1 "Libre Franklin",sans-serif;letter-spacing:.06em;text-transform:uppercase}"""
FIT = """() => { const v = document.querySelector('.vis'), c = v.firstElementChild; c.style.zoom = 1;
  const r = c.getBoundingClientRect(), vr = v.getBoundingClientRect();
  c.style.zoom = Math.min(1.35, (vr.width - 24) / r.width, (vr.height - 28) / r.height); }"""

def slides(P):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = pathlib.Path(tempfile.mkdtemp()); bad = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 540, "height": 675}, device_scale_factor=2)
        for p in P:
            a = dict(p, headline=f'<span class="anstag">Answer</span><br>{d.e(p["ans_title"])}', sub=p["ans_text"], vis=p["ans_vis"], zoom=1)
            for name, html, fit in [(p["id"], d.post_html(p, "fb", cta="Swipe for the answer →"), False),
                                    (f"{p['id']}-a", d.post_html(a, "fb", cta="More free puzzles: link in bio", cls="ans", css=ANS_CSS), True)]:
                f = tmp / f"{name}.html"; f.write_text(html)
                pg.goto(f"file://{f}"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(120)
                if fit: pg.evaluate(FIT); pg.wait_for_timeout(60)
                r = pg.evaluate(render.CHECK)
                if r["bad"] or not r["fonts"]: bad[name] = r
                pg.locator(".post").screenshot(path=str(OUT / f"{name}.jpg"), type="jpeg", quality=90)
        b.close()
    return bad

def first_para(p):
    return re.sub(r"\s+", " ", p["caption"].split("\n\n")[0]).strip()

def hashtags(game):
    tags = ["puzzle", "brainteaser", "puzzlegame", "dailypuzzle"] + [t.replace(" ", "") for t in ss.GAME_TAGS[game]] + ["bgameworld"]
    return " ".join("#" + t for t in dict.fromkeys(tags))

def carousel(p, at):
    g = d.game(p["game"])
    cap = (f"{first_para(p)}\n\nSwipe ➡️ for the answer. Did you get it? Tell us in the comments 👇\n\n"
           f"Play {g['name']} and more free daily puzzles at bgameworld.com (link in bio 🔗)\n\n{hashtags(p['game'])}")
    return {"id": f"ig-{p['id']}", "at": at, "kind": "carousel", "game": p["game"],
            "images": [f"social/ig/{p['id']}.jpg", f"social/ig/{p['id']}-a.jpg"], "caption": cap}

def reel(p, at):
    g = d.game(p["game"])
    cap = (f"{first_para(p)} Watch to the end for the answer ⏱️\n\n"
           f"Play {g['name']} and more free daily puzzles at bgameworld.com (link in bio 🔗)\n\n#reels {hashtags(p['game'])}")
    return {"id": f"igr-{p['id']}", "at": at, "kind": "reel", "game": p["game"], "video": f"social/shorts/{p['id']}.mp4", "caption": cap}

def daily_seven(c, at):
    """The Facebook Daily Seven post as a single Instagram image; the link paragraph becomes 'link in bio'."""
    from PIL import Image
    jpg = OUT / f"{c['id']}.jpg"
    Image.open(SITE / "social/fb" / f"{c['id']}.png").convert("RGB").save(jpg, quality=90)
    paras = [x if "https://" not in x else "Make a free account and play at bgameworld.com (link in bio 🔗)" for x in c["caption"].split("\n\n")]
    return {"id": f"ig-{c['id']}", "at": at, "kind": "image", "game": "challenge", "image": f"social/ig/{c['id']}.jpg", "caption": "\n\n".join(paras)}

def schedule(P):
    out = []
    posts = {x["id"]: x for x in json.load(open(SITE / "src/posts.json"))}
    for i in range(DAYS):
        date = START + dt.timedelta(days=i); day = date.isoformat()
        out += [carousel(p, f"{day}T{t}:00Z") for p, t in zip(P[4 * i: 4 * i + 4], PUZZLE_AT)]
        out.append(daily_seven(posts[f"ch{date:%m%d}"], f"{day}T{CH_AT}:00Z"))
    R = nov.build_puzzles()
    for i, p in enumerate(R):
        day = (START + dt.timedelta(days=i // 2)).isoformat()
        out.append(reel(p, f"{day}T{REEL_AT[i % 2]}:00Z"))
    out = sorted((x for x in out if x["at"] >= FIRST), key=lambda x: x["at"])
    for x in out:
        for f in x.get("images", []) + [x[k] for k in ("video", "image") if k in x]: assert (SITE / f).exists(), f
        assert len(x["caption"]) <= 2200 and x["caption"].count("#") <= 30, x["id"]      # Instagram's caption limits
        pid = x["id"].split("-", 1)[1]
        assert posts[pid]["at"] < x["at"], x["id"]                                         # never answers before its Facebook post
    (SITE / "src/instagram.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    return out

if __name__ == "__main__":
    P = dec.build_puzzles()
    bad = slides(P)
    for k, v in bad.items(): print("LAYOUT", k, v)
    out = schedule(P)
    print(len(out), "Instagram posts,", out[0]["at"], "->", out[-1]["at"])
