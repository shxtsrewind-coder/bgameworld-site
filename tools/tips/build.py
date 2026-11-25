"""Build bgameworld.com/tips/ from tools/tips/articles.py.

Run from the repository root:  python3 tools/tips/build.py
Pages borrow the <style> block from the Wordezy guide so they match the site.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from articles import ARTICLES  # noqa: E402

PUBLISHED = "2026-11-22"
SITE = "https://bgameworld.com"
TEMPLATE = open("games/wordezy/index.html", encoding="utf-8").read()
STYLE = re.search(r"<style>.*?</style>", TEMPLATE, re.S).group(0)
EXTRA_CSS = """<style>
.article p, .article li { line-height: 1.65; }
.article ul { padding-left: 1.2em; }
.article li { margin: .35em 0; }
.read { color: #5a5a5a; font-size: 14px; }
.tips { list-style: none; padding: 0; display: grid; gap: 14px; }
.tips a { display: block; padding: 16px 18px; border: 1px solid #e2e2e2; border-radius: 12px; text-decoration: none; color: inherit; background: #fff; }
.tips a:hover { border-color: #121212; }
.tips b { display: block; font-size: 18px; margin-bottom: 4px; }
.tips small { color: #5a5a5a; font-size: 15px; line-height: 1.5; }
</style>"""
TOP = """<div class="top">
    <a href="/" aria-label="BGameWorld home"><img src="/logo.webp" alt="BGameWorld" width="602" height="348"></a>
    <nav aria-label="Site"><a href="/">Games</a><a href="/games/">Guides</a><a href="/tips/">Tips</a><a href="/about/">About</a><a href="/contact/">Contact</a></nav>
  </div>"""
FOOTER = """<footer>
    <span>&copy; 2026 BGameWorld</span>
    <nav aria-label="Footer"><a href="/games/">Game guides</a><a href="/tips/">Puzzle tips</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></nav>
  </footer>"""
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3551074498139485" crossorigin="anonymous"></script>'
e = html.escape


def head(title, desc, url, kind, ld):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="BGameWorld">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<link rel="icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/zilla-slab-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/libre-franklin.woff2" as="font" type="font/woff2" crossorigin>
<meta name="theme-color" content="#FFFFFF">
{ADS}
<script type="application/ld+json">{json.dumps(ld)}</script>
{STYLE}
{EXTRA_CSS}
<script src="/visit.js" defer></script>
</head>"""


def words(a):
    n = len(a["lede"].split())
    for _, parts in a["sections"]:
        for p in parts:
            n += sum(len(i.split()) for i in p[1]) if isinstance(p, tuple) else len(p.split())
    return n


def body_html(a):
    out = []
    for h, parts in a["sections"]:
        out.append(f"  <h2>{e(h)}</h2>")
        for p in parts:
            if isinstance(p, tuple):
                out.append("  <ul>\n" + "\n".join(f"    <li>{e(i)}</li>" for i in p[1]) + "\n  </ul>")
            else:
                out.append(f"  <p>{e(p)}</p>")
    return "\n".join(out)


def article_page(a):
    url = f"{SITE}/tips/{a['slug']}/"
    mins = max(2, round(words(a) / 200))
    name, play, guide = a["game"]
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
          "datePublished": PUBLISHED, "dateModified": PUBLISHED, "mainEntityOfPage": url,
          "author": {"@type": "Organization", "name": "BGameWorld"}, "publisher": {"@type": "Organization", "name": "BGameWorld", "logo": {"@type": "ImageObject", "url": f"{SITE}/logo.webp"}},
          "image": f"{SITE}/og-image.jpg"}
    others = [o for o in ARTICLES if o is not a][:4]
    more = "\n".join(f'    <li><a href="/tips/{o["slug"]}/"><b>{e(o["title"])}</b><small>{e(o["desc"])}</small></a></li>' for o in others)
    try_it = (f'<p><strong>Try it.</strong> Put these ideas to work in <a href="{play}">{e(name)}</a>, free in your browser, '
              f'or read the <a href="{guide}">full guide</a>.</p>') if guide.startswith("/games/") and guide != "/games/" else \
             f'<p><strong>Try it.</strong> Pick today\'s puzzles on the <a href="/">BGameWorld homepage</a>, or browse the <a href="/games/">game guides</a>.</p>'
    return f"""{head(a['title'] + ' | BGameWorld', a['desc'], url, 'article', ld)}
<body>
<main>
  {TOP}
  <p class="crumb"><a href="/tips/">Puzzle tips</a> / {e(a['title'])}</p>
  <h1>{e(a['title'])}</h1>
  <p class="read">BGameWorld &middot; {mins} min read &middot; <time datetime="{PUBLISHED}">22 November 2026</time></p>
  <p class="lede">{e(a['lede'])}</p>
  <hr class="rule">
  <div class="article">
{body_html(a)}
  </div>
  <div class="box">{try_it}</div>

  <h2>More puzzle tips</h2>
  <ul class="tips">
{more}
  </ul>

  {FOOTER}
</main>
</body>
</html>
"""


def index_page():
    url = f"{SITE}/tips/"
    desc = "Practical tips and short reads on word puzzles, logic puzzles and trivia: better first guesses, word ladders, word searches, anagrams, false friends and more."
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Puzzle tips", "description": desc, "url": url,
          "hasPart": [{"@type": "Article", "headline": a["title"], "url": f"{SITE}/tips/{a['slug']}/"} for a in ARTICLES]}
    items = "\n".join(f'    <li><a href="/tips/{a["slug"]}/"><b>{e(a["title"])}</b><small>{e(a["desc"])}</small></a></li>' for a in ARTICLES)
    return f"""{head('Puzzle tips: strategies for word and logic puzzles | BGameWorld', desc, url, 'website', ld)}
<body>
<main>
  {TOP}
  <h1>Puzzle tips</h1>
  <p class="lede">Short, practical reads on getting better at daily puzzles: how to open a word game, solve a ladder, spot hidden words, unscramble anagrams, sort colours, avoid false friends and read old photographs. Each one links to a game where you can try the idea straight away.</p>
  <hr class="rule">
  <ul class="tips">
{items}
  </ul>
  <div class="box"><p><strong>New to BGameWorld?</strong> Every game also has a step-by-step <a href="/games/">guide</a> with its rules and scoring.</p></div>

  {FOOTER}
</main>
</body>
</html>
"""


os.makedirs("tips", exist_ok=True)
open("tips/index.html", "w", encoding="utf-8").write(index_page())
for a in ARTICLES:
    os.makedirs(f"tips/{a['slug']}", exist_ok=True)
    open(f"tips/{a['slug']}/index.html", "w", encoding="utf-8").write(article_page(a))
    print(f"{words(a):5d} words  /tips/{a['slug']}/")
