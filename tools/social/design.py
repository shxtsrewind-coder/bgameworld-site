"""BGameWorld social look ("Today's Edition", see DESIGN.md): white paper, ink, one flat colour per game,
Zilla Slab for names and headlines, Libre Franklin for everything else.

post_html(p, "fb")  -> 540x675 CSS px page, screenshot at 2x = 1080x1350 Facebook image
post_html(p, "pin") -> 500x750 CSS px page, screenshot at 2x = 1000x1500 Pinterest image
answer_page(p)      -> /a/<id>/ answer page in the site's guide-page style
"""
import re, html, pathlib

SITE = pathlib.Path(__file__).resolve().parents[2]
e = html.escape
INK, INK2, INK3, PAPER, PAPER2, RULE = "#121212", "#4A4A4A", "#6B6B6B", "#FFFFFF", "#F4F4F1", "#DCDCD7"

# ------------------------------------------------------------------ games, colours and icons, read from the site itself
_idx = (SITE / "index.html").read_text()
_games_src = re.search(r"const GAMES = \[(.*?)\n\];", _idx, re.S).group(1)
GAMES = {}
for m in re.finditer(r'\{ name: "([^"]+)", line: "([^"]+)", cat: "([^"]+)", art: "([^"]+)", guide: "([^"]+)", color: "([^"]+)", url: "([^"]+)"', _games_src):
    name, line, cat, art, guide, color, url = m.groups()
    GAMES[guide] = dict(name=name, line=line, cat=cat, art=art, guide=guide, color=color, url=url)

def _icon(guide):
    src = (SITE / "games" / guide / "index.html").read_text()
    svg = re.search(r'<span class="tile" style="--tile:[^"]+">(<svg.*?</svg>)</span>', src, re.S).group(1)
    return re.sub(r'role="img" aria-label="[^"]*"', 'aria-hidden="true"', svg)
for g in GAMES.values():
    g["icon"] = _icon(g["guide"])

KEY = {"wordezy": "wordezy", "lingoezy": "lingoezy", "sortezy": "sortezy", "scramble": "wordezy-scramble",
       "warmezy": "warmezy", "ladder": "wordezy-ladder", "letterezy": "letterezy", "linkezy": "linkezy",
       "search": "wordezy-search", "mergezy": "mergezy", "timeguess": "when-and-where"}
LABEL = {"wordezy": "Daily 5-letter word", "lingoezy": "False friends quiz", "sortezy": "Water sort puzzle",
         "scramble": "Word scramble", "warmezy": "Hot and cold word game", "ladder": "Word ladder",
         "letterezy": "Letter bag word game", "linkezy": "Connect the dots", "search": "Word search"}
def game(key): return GAMES[KEY[key]]

FONT = f"""@font-face{{font-family:"Zilla Slab";font-weight:700;src:url(file://{SITE}/fonts/zilla-slab-700.woff2) format("woff2")}}
@font-face{{font-family:"Zilla Slab";font-weight:600;src:url(file://{SITE}/fonts/zilla-slab-600.woff2) format("woff2")}}
@font-face{{font-family:"Libre Franklin";font-weight:100 900;src:url(file://{SITE}/fonts/libre-franklin.woff2) format("woff2")}}"""
FONT_SITE = """@font-face{font-family:"Zilla Slab";font-style:normal;font-weight:700;font-display:swap;src:url(/fonts/zilla-slab-700.woff2) format("woff2")}
@font-face{font-family:"Libre Franklin";font-style:normal;font-weight:100 900;font-display:swap;src:url(/fonts/libre-franklin.woff2) format("woff2")}"""

# ------------------------------------------------------------------ visual CSS (shared by images and answer pages)
VIS_CSS = f"""
.row{{display:flex}}.col{{display:flex;flex-direction:column}}
.t{{display:flex;align-items:center;justify-content:center;border-radius:6px;font:700 30px/1 "Zilla Slab",Georgia,serif;flex-shrink:0;color:#fff}}
.t.blank{{background:#fff;color:{INK};border:2.5px solid {INK}}}
.t.q{{background:#fff;color:{INK};border:2.5px dashed {INK}}}
.lc{{width:100%;background:{PAPER2};border:1px solid {RULE};border-radius:12px;padding:18px 22px 20px}}
.lc small{{display:block;font:600 14px/1.2 "Libre Franklin",sans-serif;color:{INK3}}}
.lc b{{display:block;margin-top:6px;font:700 46px/1.05 "Zilla Slab",Georgia,serif;color:{INK}}}
.opts{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;width:100%}}
.opt{{min-height:56px;border:1.5px solid {INK};border-radius:999px;padding:0 16px 0 8px;display:flex;align-items:center;gap:10px;font:600 20px/1.1 "Libre Franklin",sans-serif;color:{INK};background:#fff}}
.opt i{{font-style:normal;width:34px;height:34px;flex:none;border-radius:50%;background:{INK};color:#fff;display:grid;place-items:center;font:700 16px/1 "Zilla Slab",serif}}
.tube{{width:56px;border:2.5px solid {INK};border-top:none;border-radius:0 0 28px 28px;background:#fff;padding:0 5px 7px;display:flex;flex-direction:column;justify-content:flex-end;gap:3px}}
.tube span{{display:block;height:40px;border-radius:4px}}
.tube span:first-child{{border-radius:4px 4px 22px 22px}}
.sct{{width:60px;height:60px;border-radius:8px;background:#fff;border:2.5px solid {INK};display:grid;place-items:center;font:700 34px/1 "Zilla Slab",serif;color:{INK}}}
.scs{{width:60px;height:60px;border-radius:8px;border:2px dashed #8A8A8A}}
.hint{{margin:4px 0 0;font:500 19px/1.35 "Libre Franklin",sans-serif;color:{INK2};text-align:center}}
.hint b{{color:{INK};font-weight:700}}
.wr{{position:relative;height:44px;border-bottom:1px solid {RULE};display:flex;align-items:center;justify-content:space-between;padding:0 12px;font:600 20px/1 "Libre Franklin",sans-serif;color:{INK}}}
.wr.secret{{border:2px dashed {INK};border-radius:8px;margin-bottom:4px;font-weight:600;color:{INK2}}}
.wr .rk{{display:flex;align-items:baseline;gap:12px;font-variant-numeric:tabular-nums;font-weight:700}}
.wr .bd{{font-weight:600;font-size:14px}}
.wr .bar{{position:absolute;left:0;bottom:-1px;height:4px}}
.lad{{display:flex;flex-direction:column;align-items:center;gap:9px}}
.rung{{display:flex;gap:7px}}
.lt{{position:relative;width:64px;height:64px;border-radius:8px;background:#fff;border:2.5px solid {INK};display:grid;place-items:center;font:700 34px/1 "Zilla Slab",serif;color:{INK}}}
.lt sub{{position:absolute;right:6px;bottom:5px;font:700 13px/1 "Libre Franklin",sans-serif}}
.sl{{width:46px;height:46px;border-radius:7px;border:1.5px solid #8A8A8A;display:grid;place-items:center;font:700 12px/1 "Libre Franklin",sans-serif;color:{INK2}}}
.lk{{display:grid;gap:3px;background:{RULE};border:3px solid {INK};border-radius:10px;padding:3px}}
.lk div{{display:grid;place-items:center;background:#fff;border-radius:4px}}
.dot{{border-radius:50%;display:grid;place-items:center;font:700 18px/1 "Zilla Slab",serif;color:#fff}}
.ws{{display:grid;gap:0;border:2.5px solid {INK};border-radius:10px;padding:8px;background:#fff;font:700 19px/1 "Libre Franklin",sans-serif;color:{INK}}}
.ws div{{display:grid;place-items:center;border-radius:6px}}
.moves{{margin:0;padding:0 0 0 28px;columns:2;column-gap:44px;font:600 16px/1.3 "Libre Franklin",sans-serif;color:{INK}}}
.moves li{{margin:0 0 6px}}
.alist{{list-style:none;margin:0;padding:0;width:100%}}
.alist li{{padding:10px 0;border-top:1px solid {RULE};font:400 17px/1.45 "Libre Franklin",sans-serif;color:{INK2}}}
.alist li b{{color:{INK}}}
.alist li.good b:first-child{{background:#E3F0E7;padding:0 4px;border-radius:3px}}
.alist li.bad b:first-child{{text-decoration:line-through;text-decoration-thickness:2px}}
.close{{display:grid;grid-template-columns:1fr 1fr;gap:6px 14px;width:100%}}
.close div{{display:flex;justify-content:space-between;padding:8px 0;border-top:1px solid {RULE};font:600 17px/1.2 "Libre Franklin",sans-serif;color:{INK}}}
.close span{{color:{INK3};font-variant-numeric:tabular-nums}}
"""

WZ = {"g": "#3A8B55", "y": "#B5841E", "x": "#787C7E"}       # Wordezy's own tile colours
WARM = {"Boiling": "#D9442B", "Hot": "#E8743F", "Warm": "#D99A1E", "Cool": "#4AA3C9", "Cold": "#6E8BBF"}

# ------------------------------------------------------------------ visuals
def tiles(word, colors=None, size=62, gap=8, fs=None):
    fs = fs or int(size * 0.5); out = []
    for i, ch in enumerate(word):
        c = colors[i] if colors else None
        if ch == "?": cls, st = "t q", ""
        elif c in WZ: cls, st = "t", f"background:{WZ[c]};"
        elif c and c.startswith("#"): cls, st = "t", f"background:{c};color:{INK};"
        else: cls, st = "t blank", ""
        out.append(f'<div class="{cls}" style="width:{size}px;height:{size}px;font-size:{fs}px;{st}">{e(ch)}</div>')
    return f'<div class="row" style="gap:{gap}px">' + "".join(out) + "</div>"

def wz_board(b, size=62):
    rows = [tiles(r["letters"], r["colors"], size) for r in b["rows"]] + [tiles(b["typed"], None, size)]
    return f'<div class="col" style="gap:8px">' + "".join(rows) + "</div>"

def wz_solved(b, size=46):
    rows = [tiles(r["letters"], r["colors"], size, 6) for r in b["rows"]] + [tiles(b["answer"], "ggggg", size, 6)]
    return '<div class="col" style="gap:6px">' + "".join(rows) + "</div>"

def lingo_card(lang_label, prompt, options):
    opts = "".join(f'<div class="opt"><i>{"ABCD"[i]}</i><span>{e(o)}</span></div>' for i, o in enumerate(options))
    return (f'<div class="col" style="gap:16px;width:440px"><div class="lc"><small>{e(lang_label)}</small><b>{e(prompt)}</b></div>'
            f'<div class="opts">{opts}</div></div>')

def lingo_explain(a):
    li = []
    for x in a["explain"]:
        tail = " That's the trap." if x["kind"] == "bad" else ""
        li.append(f'<li class="{x["kind"]}"><b>{e(x["word"])}</b> means <b>{e(x["means"])}</b>.{tail}</li>')
    return '<ul class="alist">' + "".join(li) + "</ul>"

def sort_tubes(tubes, colors):
    out = []
    for t in tubes:
        layers = "".join(f'<span style="background:{colors[c]}"></span>' for c in reversed(t))
        out.append(f'<div class="tube" style="height:{4 * 43 + 12}px">{layers}</div>')
    return '<div class="row" style="gap:16px;align-items:flex-end">' + "".join(out) + "</div>"

def moves_list(moves):
    return '<ol class="moves">' + "".join(f"<li>Tube {a + 1} → Tube {b + 1}</li>" for a, b in moves) + "</ol>"

def scramble_tiles(letters, hint):
    rots = [-6, 5, -3, 6, -5, 4, -4, 3]
    t = "".join(f'<div class="sct" style="transform:rotate({rots[i % 8]}deg)">{ch}</div>' for i, ch in enumerate(letters))
    s = "".join('<div class="scs"></div>' for _ in letters)
    return (f'<div class="col" style="gap:18px;align-items:center"><div class="row" style="gap:8px">{t}</div>'
            f'<div class="row" style="gap:8px">{s}</div><p class="hint"><b>Hint:</b> {e(hint)}</p></div>')

def warm_rows(rows, width=440):
    out = [f'<div class="wr secret"><span>the secret word</span><span class="rk">#1</span></div>']
    for r in rows:
        col = WARM[r["band"]]
        out.append(f'<div class="wr"><span>{e(r["word"])}</span><span class="rk"><span class="bd" style="color:{col}">{r["band"]}</span>'
                   f'<span>#{r["rank"]:,}</span></span><span class="bar" style="width:{r["pct"]}%;background:{col}"></span></div>')
    return f'<div class="col" style="width:{width}px">' + "".join(out) + "</div>"

def warm_closest(closest, picks):
    d = dict(closest)
    return '<div class="close">' + "".join(f'<div>{e(w)}<span>#{d[w]}</span></div>' for w in picks) + "</div>"

def ladder_vis(words, color, solved=False, size=54):
    n = len(words[0]); out = []
    for i, w in enumerate(words):
        if solved or i in (0, len(words) - 1):
            fill = color if i in (0, len(words) - 1) else None
            out.append(tiles(w, [fill] * n if fill else None, size, 7))
        else:
            out.append(tiles("?" * n, None, size, 7).replace(">?<", "><"))
    return f'<div class="lad">' + "".join(out) + "</div>"

def letter_rack(rack, values):
    tile = lambda ch: f'<div class="lt">{ch}<sub>{values[ch.lower()]}</sub></div>'
    slots = "".join(f'<div class="sl">{"2×L" if i == 3 else "2×W" if i == 4 else ""}</div>' for i in range(7))
    return (f'<div class="col" style="gap:10px;align-items:center"><div class="row" style="gap:8px">{"".join(tile(c) for c in rack[:5])}</div>'
            f'<div class="row" style="gap:8px">{"".join(tile(c) for c in rack[5:])}</div><div class="row" style="gap:6px;margin-top:12px">{slots}</div></div>')

def link_grid(segs, colors, solved=False, cell=56):
    owner = {tuple(p): k for k, s in enumerate(segs) for p in s}
    ends = {tuple(s[0]): k for k, s in enumerate(segs)}; ends.update({tuple(s[-1]): k for k, s in enumerate(segs)})
    out = []
    for r in range(6):
        for c in range(6):
            k = owner[(r, c)]; col = colors[k]; dot = ""
            if (r, c) in ends:
                ring = f"box-shadow:0 0 0 3px #fff,0 0 0 5px {INK};" if solved else ""
                dot = f'<span class="dot" style="width:{int(cell * .68)}px;height:{int(cell * .68)}px;background:{col};{ring}">{"ABCDEFG"[k]}</span>'
            bg = f"background:{col}" if solved else ""
            out.append(f'<div style="{bg}">{dot}</div>')
    return f'<div class="lk" style="grid-template-columns:repeat(6,{cell}px);grid-auto-rows:{cell}px">' + "".join(out) + "</div>"

def ws_grid(grid, cells, color, highlight=False, cell=36, fs=20):
    hl = set(map(tuple, cells)) if highlight else set()
    out = [f'<div style="{"background:" + color if (r, c) in hl else ""}">{ch}</div>' for r, row in enumerate(grid) for c, ch in enumerate(row)]
    return f'<div class="ws" style="grid-template-columns:repeat(11,{cell}px);grid-auto-rows:{cell}px;font-size:{fs}px">' + "".join(out) + "</div>"

# ------------------------------------------------------------------ the post image
POST_CSS = f"""
*{{box-sizing:border-box}}html,body{{margin:0;background:#fff}}
.post{{position:relative;width:540px;height:675px;background:#fff;color:{INK};font-family:"Libre Franklin",sans-serif;display:flex;flex-direction:column;overflow:hidden}}
.post.pin{{width:500px;height:750px}}
.band{{display:flex;align-items:center;gap:14px;padding:16px 26px;background:var(--tile)}}
.band .ic{{width:54px;height:54px;flex:none;display:grid;place-items:center;background:#fff;border:2.5px solid {INK};border-radius:12px}}
.band .ic svg{{width:38px;height:38px}}
.band b{{display:block;font:700 27px/1 "Zilla Slab",serif}}
.band small{{display:block;margin-top:4px;font:600 15px/1.2 "Libre Franklin",sans-serif}}
.body{{flex:1;display:flex;flex-direction:column;padding:20px 26px 0;min-height:0}}
h1{{margin:0;font:700 46px/1.02 "Zilla Slab",serif;letter-spacing:-.02em}}
.sub{{margin:8px 0 0;font:500 18px/1.35 "Libre Franklin",sans-serif;color:{INK2}}}
.vis{{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;padding:14px 0}}
.foot{{margin:0 26px;padding:12px 0 16px;border-top:3px solid {INK};display:flex;align-items:center;justify-content:space-between}}
.foot img{{height:40px;width:auto;display:block}}
.pill{{background:{INK};color:#fff;font:600 15px/1 "Libre Franklin",sans-serif;padding:12px 18px;border-radius:999px}}
.pin .body{{padding-top:26px}}.pin h1{{font-size:48px}}.pin .foot{{padding-bottom:20px}}
"""

def post_html(p, kind="fb"):
    g = game(p["game"])
    cta = "Answer: link in the post" if kind == "fb" else "Tap for the answer"
    zoom = p.get("zoom", 1)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONT}{VIS_CSS}{POST_CSS}</style></head><body>
<div class="post {kind}" style="--tile:{g['color']}">
<div class="band"><span class="ic">{g['icon']}</span><span><b>{e(g['name'])}</b><small>{e(LABEL[p['game']])}</small></span></div>
<div class="body"><h1>{p['headline']}</h1><p class="sub">{e(p['sub'])}</p>
<div class="vis"><div style="zoom:{zoom}">{p['vis']}</div></div></div>
<div class="foot"><img src="file://{SITE}/logo.webp" alt=""><span class="pill">{cta}</span></div></div></body></html>"""

# ------------------------------------------------------------------ the answer page (/a/<id>/), in the guide pages' style
PAGE_CSS = f"""
:root{{--ink:{INK};--ink-2:{INK2};--ink-3:{INK3};--paper:#FFFFFF;--paper-2:{PAPER2};--rule:{RULE};--focus:#2860D8;
  --slab:"Zilla Slab",Rockwell,"Roboto Slab",Georgia,serif;--sans:"Libre Franklin","Franklin Gothic Medium","Helvetica Neue",Arial,sans-serif}}
*{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}
body{{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.6 var(--sans);-webkit-font-smoothing:antialiased}}
:focus-visible{{outline:3px solid var(--focus);outline-offset:3px}}
main{{max-width:640px;margin:0 auto;padding:28px 20px 64px}}
.top{{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px 16px;margin-bottom:28px;padding-bottom:16px;border-bottom:1px solid var(--rule)}}
.top img{{width:120px;height:auto;display:block}}
.top nav{{display:flex;flex-wrap:wrap;gap:4px 18px}}
.top nav a{{color:var(--ink);font-size:15px;font-weight:600;text-decoration:none}}
.top nav a:hover{{text-decoration:underline;text-underline-offset:4px}}
.crumb{{font-size:14px;color:var(--ink-3);margin:0 0 10px}}.crumb a{{color:var(--ink-3)}}
.hero{{display:grid;grid-template-columns:auto 1fr;gap:16px;align-items:center;margin:0 0 18px}}
.tile{{display:grid;place-items:center;width:72px;height:72px;border-radius:12px;background:var(--tile)}}
.tile svg{{width:44px;height:44px}}
h1{{font:700 clamp(30px,7vw,44px)/1.05 var(--slab);letter-spacing:-.02em;margin:0}}
.puz{{display:block;width:100%;height:auto;border:1px solid var(--rule);border-radius:12px;margin:0 0 18px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:0 24px;border-radius:999px;background:var(--ink);color:#fff;font:600 16px/1 var(--sans);text-decoration:none;border:0;cursor:pointer}}
.btn:hover{{background:#333}}
.btn.ghost{{background:transparent;color:var(--ink);border:1.5px solid var(--ink)}}.btn.ghost:hover{{background:var(--paper-2)}}
.actions{{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 8px}}
.ans{{margin:0 0 26px}}
.rule{{border:0;border-top:3px solid var(--ink);margin:0 0 18px}}
h2{{font:700 28px/1.15 var(--slab);margin:0 0 16px}}
.vwrap{{display:flex;justify-content:center;margin:0 0 18px;overflow-x:auto}}
.ans p{{color:var(--ink-2);margin:0 0 14px}}
h3{{font:700 22px/1.2 var(--slab);margin:30px 0 12px}}
.grid{{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}}
.grid a{{display:flex;gap:12px;align-items:center;padding:10px;border:1px solid var(--rule);border-radius:12px;text-decoration:none;color:var(--ink);height:100%}}
.grid a:hover{{border-color:var(--ink)}}
.grid .tile{{width:52px;height:52px;border-radius:10px;flex:none}}.grid .tile svg{{width:32px;height:32px}}
.grid b{{display:block;font:700 17px/1.2 var(--slab)}}.grid small{{display:block;font-size:13.5px;color:var(--ink-3);line-height:1.35}}
footer{{border-top:1px solid var(--rule);margin-top:40px;padding-top:18px;color:var(--ink-3);font-size:15px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px 20px}}
footer a{{color:var(--ink-3)}}
@media (max-width:440px){{.moves{{columns:1}}}}
"""

def answer_page(p, more):
    g = game(p["game"]); pid = p["id"]
    utm = lambda key, extra="": f"utm_source=social&utm_medium=answer&utm_campaign={key}&utm_content={pid}{extra}"
    cards = "".join(f'<li><a href="{game(k)["url"]}/?{utm(k, "-more")}"><span class="tile" style="--tile:{game(k)["color"]}">{game(k)["icon"]}</span>'
                    f'<span><b>{e(game(k)["name"])}</b><small>{e(game(k)["line"])}</small></span></a></li>' for k in more)
    title = re.sub("<[^>]+>", " ", p["headline"]).replace("  ", " ").strip()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(g['name'])} puzzle answer | BGameWorld</title>
<meta name="description" content="{e(title)} {e(p['sub'])} See the answer, then play today's {e(g['name'])} free.">
<meta name="robots" content="noindex">
<meta property="og:title" content="{e(title)}">
<meta property="og:image" content="https://bgameworld.com/social/fb/{pid}.png">
<link rel="icon" href="/favicon.ico">
<link rel="preload" href="/fonts/zilla-slab-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/libre-franklin.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#FFFFFF">
<style>
{FONT_SITE}
{PAGE_CSS}
{VIS_CSS}
</style>
</head>
<body>
<main>
  <div class="top">
    <a href="/?{utm('portal', '-logo')}" aria-label="BGameWorld home"><img src="/logo.webp" alt="BGameWorld" width="602" height="348"></a>
    <nav aria-label="Site"><a href="/">Games</a><a href="/games/">Guides</a><a href="/about/">About</a></nav>
  </div>
  <p class="crumb">Puzzle answer / <a href="/games/{g['guide']}/">{e(g['name'])}</a></p>
  <div class="hero"><span class="tile" style="--tile:{g['color']}">{g['icon']}</span><h1>{p['headline']}</h1></div>
  <img class="puz" src="/social/fb/{pid}.png" alt="{e(title)} {e(p['sub'])}" width="1080" height="1350">
  <div class="actions"><button class="btn ghost" id="show" type="button">Show the answer</button></div>
  <section class="ans" id="ans" hidden>
    <hr class="rule">
    <h2>{e(p['ans_title'])}</h2>
    <div class="vwrap">{p['ans_vis']}</div>
    <p>{e(p['ans_text'])}</p>
  </section>
  <div class="actions"><a class="btn" href="{g['url']}/?{utm(p['game'])}">Play today's {e(g['name'])}</a><a class="btn ghost" href="/?{utm('portal')}">All {len(GAMES)} games</a></div>
  <h3>More free puzzles today</h3>
  <ul class="grid">{cards}</ul>
  <footer><span>Free, no download · <a href="/">bgameworld.com</a></span><span><a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a></span></footer>
</main>
<noscript><style>#ans{{display:block!important}}#show{{display:none}}</style></noscript>
<script>
document.getElementById('show').addEventListener('click',function(){{var a=document.getElementById('ans');a.hidden=false;this.style.display='none';a.scrollIntoView({{behavior:'smooth',block:'start'}});}});
</script>
</body>
</html>
"""
