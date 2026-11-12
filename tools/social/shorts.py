"""Puzzle Shorts: 1080x1920 vertical videos made from the same puzzles as the posts.

  0.0-0.6s   the puzzle appears          "Can you solve it in 10 seconds?"
  0.6-10.6s  countdown 10..1, the bar drains, a tick each second
  10.6-15.6s the answer (same visual as the answer page) with a chime
  15.6-18.1s end card: play free at bgameworld.com

    python3 shorts.py            # all of nov.py's puzzles -> social/shorts/<id>.mp4
"""
import sys, wave, json, shutil, pathlib, subprocess, tempfile
import numpy as np
from playwright.sync_api import sync_playwright
import design as d

SITE = d.SITE
OUT = SITE / "social" / "shorts"
FPS, INTRO, COUNT, REVEAL, END = 30, 0.6, 10, 5.0, 2.5
BAR = (220, 1386, 804, 28)         # x, y, w, h in video pixels: covers the countdown track (.cd at top 668px)

CSS = f"""
*{{box-sizing:border-box}}html,body{{margin:0;background:#fff}}
.s{{position:relative;width:540px;height:960px;background:#fff;color:{d.INK};font-family:"Libre Franklin",sans-serif;overflow:hidden}}
.band{{display:flex;align-items:center;gap:14px;padding:18px 28px;background:var(--tile)}}
.band .ic{{width:58px;height:58px;flex:none;display:grid;place-items:center;background:#fff;border:2.5px solid {d.INK};border-radius:12px}}
.band .ic svg{{width:40px;height:40px}}
.band b{{display:block;font:700 28px/1 "Zilla Slab",serif}}.band small{{display:block;margin-top:4px;font:600 16px/1.2 "Libre Franklin",sans-serif}}
.qq{{margin:26px 28px 0;font:700 42px/1.02 "Zilla Slab",serif;letter-spacing:-.02em;min-height:86px}}
.sub{{margin:8px 28px 0;font:500 19px/1.35 "Libre Franklin",sans-serif;color:{d.INK2};min-height:52px}}
.vis{{position:absolute;left:0;right:0;top:290px;height:360px;display:flex;align-items:center;justify-content:center}}
.cd{{position:absolute;left:30px;right:30px;top:668px;display:flex;align-items:center;gap:16px}}
.num{{width:64px;height:64px;flex:none;border-radius:50%;background:{d.INK};color:#fff;display:grid;place-items:center;font:700 34px/1 "Zilla Slab",serif}}
.track{{flex:1;height:12px;border-radius:6px;background:{d.INK}}}
.ans .num{{background:#3A8B55}}
.ans .track{{background:#3A8B55}}
.tag{{position:absolute;left:28px;top:752px;font:600 18px/1.3 "Libre Franklin",sans-serif;color:{d.INK3}}}
.end{{display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:150px}}
.end img{{width:250px;height:auto}}
.end h2{{margin:34px 28px 0;font:700 54px/1 "Zilla Slab",serif;letter-spacing:-.02em}}
.end p{{margin:16px 40px 0;font:500 21px/1.4 "Libre Franklin",sans-serif;color:{d.INK2}}}
.end .pill{{margin-top:30px;background:{d.INK};color:#fff;font:600 21px/1 "Libre Franklin",sans-serif;padding:18px 28px;border-radius:999px}}
"""

def lead(h):
    h = h.strip()
    return h if h[-1:] in ".?!" else h + "."

def page(p, state, k=10):
    g = d.game(p["game"])
    band = f'<div class="band"><span class="ic">{g["icon"]}</span><span><b>{d.e(g["name"])}</b><small>{d.e(d.LABEL[p["game"]])}</small></span></div>'
    if state == "end":
        body = (f'<div class="s end"><img src="file://{SITE}/logo.webp" alt=""><h2>New puzzles<br>every day</h2>'
                f'<p>{d.e(g["name"])} and 10 more free games. No download, no sign-up.</p><span class="pill">Play free at bgameworld.com</span></div>')
    elif state == "count":
        body = (f'<div class="s" style="--tile:{g["color"]}">{band}<h1 class="qq">Can you solve it in 10 seconds?</h1>'
                f'<p class="sub">{lead(p["headline"])} {d.e(p["sub"])}</p><div class="vis"><div style="zoom:{p.get("szoom", 1)}">{p["vis"]}</div></div>'
                f'<div class="cd"><span class="num">{k}</span><span class="track"></span></div><p class="tag">Answer in {k} second{"s" * (k != 1)}</p></div>')
    else:
        body = (f'<div class="s ans" style="--tile:{g["color"]}">{band}<h1 class="qq"{' style="font-size:28px;min-height:58px"' if len(p["ans_title"]) > 26 else ''}>{d.e(p["ans_title"])}</h1>'
                f'<p class="sub">{d.e(p["ans_text"])}</p><div class="vis"><div style="zoom:{p.get("azoom", 1)}">{p["ans_vis"]}</div></div>'
                f'<p class="tag" style="top:690px">Play today\'s {d.e(g["name"])} free at bgameworld.com</p></div>')
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{d.FONT}{d.VIS_CSS}{CSS}</style></head><body>{body}</body></html>'

FIT = """() => { const v = document.querySelector('.vis'); if (!v) return 1; const c = v.firstElementChild;
  const r = c.getBoundingClientRect(), vr = v.getBoundingClientRect();
  return Math.min(1.45, (vr.width - 40) / r.width, (vr.height - 10) / r.height); }"""
OVER = """() => { const s = document.querySelector('.s').getBoundingClientRect(), bad = [];
  for (const el of document.querySelectorAll(".qq, .sub, .tag, .vis > div")) { const x = el.getBoundingClientRect();
    if (x.right > s.right - 10 || x.left < s.left + 10) bad.push(el.className || 'vis'); }
  const sub = document.querySelector('.sub'), vis = document.querySelector('.vis > div');
  if (sub && vis && sub.getBoundingClientRect().bottom > vis.getBoundingClientRect().top + 2) bad.push('text runs into the puzzle');
  return bad; }"""

def tone(f, dur, decay, v, sr=48000):
    t = np.arange(int(dur * sr)) / sr
    return v * np.sin(2 * np.pi * f * t) * np.exp(-t * decay)

def soundtrack(path, total, sr=48000):
    a = np.zeros(int((total + 1) * sr))
    def add(sig, s):
        i = int(s * sr); a[i:i + len(sig)] += sig[:max(0, len(a) - i)]
    add(tone(523, .18, 18, .16), .05); add(tone(784, .25, 14, .14), .14)
    for k in range(COUNT):
        t = INTRO + k
        add(tone(1800 if k < 7 else 2300, .05, 90, .12 if k < 7 else .18), t)
    add(tone(196, .45, 6, .22), INTRO + COUNT - .02); add(tone(147, .5, 6, .18), INTRO + COUNT + .05)
    for j, f in enumerate((784, 988, 1175, 1568)): add(tone(f, .9, 4, .18), INTRO + COUNT + .15 + .1 * j)
    add(tone(660, .14, 25, .16), INTRO + COUNT + REVEAL + .05); add(tone(990, .2, 20, .12), INTRO + COUNT + REVEAL + .12)
    pcm = (np.clip(a[:int(total * sr)], -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())

def ff(*a): subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y", *a], check=True)

def make(posts, out=OUT):
    out.mkdir(parents=True, exist_ok=True)
    report = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        for p in posts:
            tmp = pathlib.Path(tempfile.mkdtemp()); html = tmp / "s.html"
            def shot(name, state, k=10):
                html.write_text(page(p, state, k)); pg.goto(f"file://{html}"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(60)
                pg.screenshot(path=str(tmp / f"{name}.png")); return pg.evaluate(OVER)
            # size the puzzle and the answer to fill their space
            html.write_text(page(dict(p, szoom=1), "count")); pg.goto(f"file://{html}"); pg.evaluate("document.fonts.ready"); p["szoom"] = round(pg.evaluate(FIT), 3)
            html.write_text(page(dict(p, azoom=1), "ans")); pg.goto(f"file://{html}"); pg.evaluate("document.fonts.ready"); p["azoom"] = round(pg.evaluate(FIT), 3)
            bad = []
            for k in range(10, 0, -1): bad += shot(f"c{k}", "count", k)
            bad += shot("ans", "ans"); shot("end", "end")
            report[p["id"]] = sorted(set(bad))
            # stills -> video, with the bar draining smoothly over the countdown
            lst = tmp / "list.txt"
            seq = [("c10", INTRO + 1)] + [(f"c{k}", 1) for k in range(9, 0, -1)] + [("ans", REVEAL), ("end", END)]
            lst.write_text("".join(f"file '{tmp / n}.png'\nduration {dur}\n" for n, dur in seq) + f"file '{tmp}/end.png'\n")
            total = INTRO + COUNT + REVEAL + END
            soundtrack(tmp / "a.wav", total)
            x, y, w, h = BAR
            ff("-f", "concat", "-safe", "0", "-i", str(lst), "-f", "lavfi", "-i", f"color=c=white:s={w}x{h}:r={FPS}", "-i", str(tmp / "a.wav"),
               "-filter_complex",
               f"[0:v]fps={FPS},format=yuv420p[base];"
               f"[base][1:v]overlay=x='if(between(t,{INTRO},{INTRO + COUNT}),{x}+{w}*(1-(t-{INTRO})/{COUNT}),2000)':y={y}:shortest=1:eval=frame,format=yuv420p[v]",
               "-map", "[v]", "-map", "2:a", "-t", f"{total}", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-r", str(FPS),
               "-g", str(FPS * 2), "-keyint_min", str(FPS * 2), "-sc_threshold", "0", "-profile:v", "high", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(out / f"{p['id']}.mp4"))
            shutil.rmtree(tmp)
        b.close()
    return report

if __name__ == "__main__":
    import nov
    P = nov.build_puzzles()
    if len(sys.argv) > 1: P = [p for p in P if p["id"] in sys.argv[1:]]
    for k, v in make(P).items():
        if v: print("LAYOUT", k, v)
    print("done", len(P))
