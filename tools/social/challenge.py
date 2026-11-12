"""Daily 7-Game Challenge posts: one Facebook image a day at 12:00 UTC showing that day's seven games,
picked by the landing page's own code (index.html: GAMES, rand, pickDailyGames).

    python3 challenge.py 2026-11-13 2026-11-26
"""
import sys, json, re, subprocess, pathlib, tempfile, datetime as dt
import design as d

SITE = d.SITE
TAGS = "#dailychallenge #puzzlegames #wordgames #brainteaser #braingames #freegames"
LINK = "https://bgameworld.com/#challenge"

def lineups(days):
    src = (SITE / "index.html").read_text()
    js = "\n".join([re.search(r"const GAMES = \[.*?\n\];", src, re.S).group(0),
                    re.search(r"function rand\(seed\).*?\n", src).group(0),
                    re.search(r"function pickDailyGames\(dateStr\) \{.*?\n\}", src, re.S).group(0),
                    f"console.log(JSON.stringify({json.dumps(days)}.map(x => pickDailyGames(x).map(g => g.guide))));"])
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    return dict(zip(days, json.loads(out)))

CSS = """
*{box-sizing:border-box}html,body{margin:0;background:#fff}
.post{width:540px;height:675px;background:#fff;color:#121212;font-family:"Libre Franklin",sans-serif;display:flex;flex-direction:column;padding:26px 26px 0}
.date{display:flex;justify-content:space-between;align-items:baseline;padding-bottom:10px;border-bottom:1px solid #DCDCD7;font:700 17px/1 "Libre Franklin",sans-serif}
.date span{font-weight:600;color:#6B6B6B;font-size:15px}
h1{margin:16px 0 0;font:700 54px/.98 "Zilla Slab",serif;letter-spacing:-.02em}
.sub{margin:10px 0 0;font:500 18px/1.35 "Libre Franklin",sans-serif;color:#4A4A4A}
.seven{flex:1;display:grid;grid-template-columns:repeat(8,1fr);gap:14px 12px;align-content:center;padding:6px 0}
.g{grid-column:span 2;display:flex;flex-direction:column;align-items:center;gap:7px}
.g:nth-child(5){grid-column:2/span 2}
.sq{position:relative;width:100%;aspect-ratio:1;border-radius:12px;background:var(--tile);display:grid;place-items:center}
.sq svg{width:58%;height:58%}
.sq i{position:absolute;top:6px;left:6px;width:22px;height:22px;border-radius:50%;background:#121212;color:#fff;font:700 13px/22px "Zilla Slab",serif;text-align:center;font-style:normal}
.g b{font:700 15px/1.15 "Zilla Slab",serif;text-align:center}
.foot{padding:12px 0 16px;border-top:3px solid #121212;display:flex;align-items:center;justify-content:space-between}
.foot img{height:40px;width:auto;display:block}
.pill{background:#121212;color:#fff;font:600 15px/1 "Libre Franklin",sans-serif;padding:12px 18px;border-radius:999px}
"""

def html(day, guides, launch=False):
    date = dt.date.fromisoformat(day)
    tiles = "".join(f'<div class="g"><span class="sq" style="--tile:{d.GAMES[x]["color"]}">{d.GAMES[x]["icon"]}<i>{i + 1}</i></span><b>{d.e(d.GAMES[x]["name"])}</b></div>'
                    for i, x in enumerate(guides))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{d.FONT}{CSS}</style></head><body>
<div class="post"><div class="date">{date.strftime('%A')}, {date.strftime('%B')} {date.day}<span>Daily 7-Game Challenge</span></div>
<h1>Today's seven</h1>
<p class="sub">Same seven free games for everyone today. Can you finish all seven?</p>
<div class="seven">{tiles}</div>
<div class="foot"><img src="file://{SITE}/logo.webp" alt=""><span class="pill">Play free at bgameworld.com</span></div></div></body></html>"""

WORD = {"wordezy", "wordezy-search", "wordezy-scramble", "wordezy-ladder", "warmezy", "letterezy"}
LOGIC = {"sortezy", "linkezy", "mergezy"}
TRIVIA = {"when-and-where": "a history photo guessing game", "lingoezy": "a language quiz"}
NUM = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
def mix(guides):
    w = sum(x in WORD for x in guides); l = sum(x in LOGIC for x in guides)
    parts = ([f"{NUM[w]} word game{'s' * (w > 1)}"] if w else []) + ([f"{NUM[l]} logic puzzle{'s' * (l > 1)}"] if l else []) + [TRIVIA[x] for x in guides if x in TRIVIA]
    assert w + l + sum(x in TRIVIA for x in guides) == 7
    s = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    return s[0].upper() + s[1:]

HOOKS = ["Today's 7-Game Challenge is live 🏆", "Can you finish all seven today? 🧩", "Seven games, one day. How many can you finish? ⏱️",
         "Your daily brain workout is here 🧠", "Weekend challenge time ☕🏆", "Today's seven are ready 🏆", "New day, new seven 🧩"]
ENDS = ["Which one will slow you down? 👇", "Comment how many you finished 👇", "Which one's your favourite? 👇",
        "Can you get through all seven? 👇", "Tag someone who'd beat you 👇"]

def captions(day, guides, i):
    date = dt.date.fromisoformat(day)
    names = [d.GAMES[x]["name"] for x in guides]
    hook = "Happy Thanksgiving! 🦃 Today's 7-Game Challenge is live." if day == "2026-11-26" else \
           ("Weekend challenge time ☕🏆" if date.weekday() >= 5 else HOOKS[i % len(HOOKS)])
    return (f"{hook}\n\n{date.strftime('%A')}'s seven: {', '.join(names[:-1])} and {names[-1]}.\n\n"
            f"{mix(guides)}. {ENDS[i % len(ENDS)]}\n\nPlay all seven free, no download: {LINK}\n\n{TAGS}")

def main(first, last):
    from playwright.sync_api import sync_playwright
    d0, d1 = dt.date.fromisoformat(first), dt.date.fromisoformat(last)
    days = [(d0 + dt.timedelta(days=i)).isoformat() for i in range((d1 - d0).days + 1)]
    L = lineups(days); tmp = pathlib.Path(tempfile.mkdtemp())
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 540, "height": 675}, device_scale_factor=2)
        for day in days:
            f = tmp / f"{day}.html"; f.write_text(html(day, L[day]))
            pg.goto(f"file://{f}"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(100)
            over = pg.evaluate("(()=>{const s=document.querySelector('.seven'),r=s.getBoundingClientRect(),last=[...s.children].pop().getBoundingClientRect();return Math.round(last.bottom-r.bottom)})()")
            assert over <= 0, (day, over)
            pg.locator(".post").screenshot(path=str(SITE / "social/fb" / f"ch{day[5:7]}{day[8:10]}.png"))
        b.close()
    ids = {f"ch{x[5:7]}{x[8:10]}" for x in days}
    posts = [x for x in json.load(open(SITE / "src/posts.json")) if x["id"] not in ids]
    for i, day in enumerate(days):
        posts.append({"id": f"ch{day[5:7]}{day[8:10]}", "at": f"{day}T12:00:00Z", "game": "challenge",
                      "lineup": [d.GAMES[x]["name"] for x in L[day]], "caption": captions(day, L[day], i)})
    posts.sort(key=lambda x: x["at"])
    (SITE / "src/posts.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
    print(f"{len(days)} challenge posts")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
