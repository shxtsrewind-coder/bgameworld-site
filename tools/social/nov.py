"""Puzzle posts for 13-26 November 2026 (p061-p116): 4 a day on Facebook (06, 09, 16, 19 UTC, around the
12:00 challenge post) and the same puzzles as Pinterest Pins (4 a day, 06/10/14/18 UTC).

    python3 nov.py            # check every puzzle, render images, write answer pages + src/posts.json + src/pins.json
"""
import json, pathlib, re, datetime as dt
import gamedata as g
import design as d

SITE = d.SITE
HERE = pathlib.Path(__file__).parent
WZ_TAIL = "Comment your answer 👇 Then check it and play today's Wordezy free: {link}"

TAGS = {
    "wordezy": "#wordgame #wordpuzzle #5letterwords #brainteaser #puzzle",
    "lingoezy": "#languagelearning #falsefriends #learnlanguages #quiz #polyglot",
    "sortezy": "#watersort #puzzlegame #satisfying #brainteaser #puzzle",
    "scramble": "#wordscramble #anagram #wordgame #wordpuzzle #brainteaser",
    "warmezy": "#wordgame #guesstheword #wordpuzzle #brainteaser #puzzle",
    "letterezy": "#anagram #wordgame #wordpuzzle #spelling #brainteaser",
    "ladder": "#wordladder #wordgame #wordpuzzle #brainteaser #puzzle",
    "search": "#wordsearch #findtheword #wordpuzzle #brainteaser #puzzle",
    "linkezy": "#connectthedots #logicpuzzle #puzzlegame #brainteaser #puzzle",
}
BOARD = {"lingoezy": "language", "sortezy": "logic", "linkezy": "logic"}
KEYWORDS = {"word": "Word puzzle, brain teaser, free online word game for adults and kids.",
            "logic": "Logic puzzle, brain teaser, free online puzzle game.",
            "language": "Language learning quiz, false friends, free online vocabulary game."}
color = lambda key: d.game(key)["color"]

# ================================================================== the puzzles, each checked as it's built
def wordezy(ans, guesses, typed, listed, why, headline=None, sub=None):
    b = g.wordezy_board(ans, guesses, typed)
    shown = typed.upper().replace("?", "_")
    opts = (", ".join(listed[:-1]) + " or " + listed[-1]).capitalize()
    n = typed.count("?")
    return dict(game="wordezy", headline=headline or ("One letter left." if n == 1 else "Two letters missing."),
                sub=sub or f"{opts}?", vis=d.wz_board(b),
                caption=f"{'One letter' if n == 1 else 'Two letters'} left: {shown}. {opts}? Only one fits the colours.\n\n" + WZ_TAIL,
                ans_title=f"The answer was {ans.upper()}", ans_vis=d.wz_solved(b), ans_text=why,
                pin_title="Wordle-Style Puzzle: " + (", ".join(w.upper() for w in listed[-3:-1]) + " or " + listed[-1].upper()) + "?")

def lingo(lang, en, options, headline, sub, caption):
    names = {"es": "Spanish", "fr": "French", "de": "German", "pt": "Portuguese", "it": "Italian"}
    a = g.lingo_answer(lang, en, options)
    trap_note = f"{a['trap']} looks like the obvious answer, but it means {a['trap_en']}."
    return dict(game="lingoezy", headline=headline, sub=sub, vis=d.lingo_card(f"English → {names[lang]}", en, options),
                caption=caption + "\n\nSee if you got fooled and play today's Lingoezy free: {link}",
                ans_title=f"The answer is {a['letter']}: {a['answer']}", ans_vis=d.lingo_explain(a),
                ans_text=f"{trap_note[0].upper() + trap_note[1:]} {en[0].upper() + en[1:]} in {names[lang]} is {a['answer']}.",
                pin_title=f"{names[lang]} False Friends Quiz: How Do You Say \"{en.title()}\"?")

def sortezy(tubes, n, sub="Pour onto the same colour or an empty tube.", extra=""):
    t = [list(x) for x in tubes] + [[], []]
    moves = g.sort_solve(t); assert len(moves) == n, (tubes, len(moves))
    return dict(game="sortezy", headline=f"Sort it in {n} moves?", sub=sub, vis=d.sort_tubes(t, g.SORT_COLORS),
                caption=f"{extra}Can you sort it in {n} moves? Pour only onto the same colour or into an empty tube. {n} is the fewest possible.\n\nStep-by-step solution and today's free puzzle: {{link}}",
                ans_title=f"The {n}-move solution", ans_vis=d.moves_list(moves),
                ans_text="Tubes are numbered 1 to 6 from the left. Each move pours the top colour of one tube into another.",
                pin_title=f"Water Sort Puzzle: Can You Solve It in {n} Moves?")

def scramble(word, seed, hint, headline=None):
    s = g.derange(word, seed); g.scramble_ok(word, s); n = len(word)
    words = {4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}[n]
    return dict(game="scramble", headline=headline or f"{n} letters. One word.", sub="Can you unscramble it?",
                vis=d.scramble_tiles(s, hint), zoom={4: 1, 5: 1, 6: 1, 7: 0.86, 8: 0.78}[n],
                caption=f"Unscramble this: {' '.join(s)}. {words} letters, one answer. Hint: {hint}\n\nReveal the word and play today's Scramble free: {{link}}",
                ans_title=f"The word was {word.upper()}", ans_vis=d.tiles(word.upper(), [color("scramble")] * n, 48, 6),
                ans_text=f"{' '.join(s)} → {word.upper()}.", pin_title=f"Word Scramble: Unscramble {s}")

def warmezy(secret, guesses, picks, headline, flavour):
    rows, close = g.warm_rows(secret, guesses)
    rk = {r["word"]: r["rank"] for r in rows}; a, b, c = guesses[:3]
    return dict(game="warmezy", headline=headline, sub="The lower the number, the hotter you are.", vis=d.warm_rows(rows),
                caption=f"Guess the secret word. Every guess gets a rank by how close its meaning is: {a} is #{rk[a]}, {b} is #{rk[b]}, {c} is #{rk[c]}. {flavour}What's #1?\n\nReveal it and play today's Warmezy free: {{link}}",
                ans_title=f"The secret word was {secret.upper()}", ans_vis=d.warm_closest(close, picks),
                ans_text=f"Those are some of the closest words to {secret.upper()} in Warmezy's own rankings. {a.title()} (#{rk[a]}) and {b} (#{rk[b]}) were already boiling.",
                pin_title=f"Guess the Secret Word: {a} #{rk[a]}, {b} #{rk[b]}")

def ladder(a, b, q):
    path = g.ladder_path(a, b); g.ladder_ok(path); n = len(path) - 1
    size = 54 if len(path) <= 5 else 48 if len(path) == 6 else 44
    return dict(game="ladder", headline=f"Turn {a.upper()} into {b.upper()}", sub=f"One letter at a time, real words only. Par is {n}.",
                vis=d.ladder_vis(path, color("ladder"), size=size),
                caption=f"Turn {a.upper()} into {b.upper()}, one letter at a time. Every step has to be a real word, and it can be done in {n} moves. {q}\n\nThe {n}-step answer and today's free ladder: {{link}}",
                ans_title=" → ".join(path), ans_vis=d.ladder_vis(path, color("ladder"), solved=True, size=42),
                ans_text=f"That's one {n}-move route. Found a different one? If every step is a real word, it counts.",
                pin_title=f"Word Ladder Puzzle: Turn {a.upper()} Into {b.upper()} in {n} Moves")

def letterezy(word, extra, seed, hint, headline="9 letters. One 7-letter word."):
    rack = g.letter_rack(word, extra, seed); g.letter_ok(word, rack)
    return dict(game="letterezy", headline=headline, sub="Use 7 of these 9 letters for the +20 bonus.", vis=d.letter_rack(rack, g.LET_VALUES),
                caption=f"Find the 7-letter word hidden in these 9 letters: {' '.join(rack)}. Hint: {hint}\n\nReveal the word and play today's Letterezy free: {{link}}",
                ans_title=f"The word was {word.upper()}", ans_vis=d.tiles(word.upper(), [color("letterezy")] * 7, 44, 6),
                ans_text=f"In Letterezy it scores {g.letter_score(word)}: the 4th letter counts double, reaching the 5th square doubles the word, and a 7-letter word adds 20.",
                pin_title=f"Find the 7-Letter Word in {' '.join(rack)}")

LINKS = json.load(open(HERE / "data" / "links-nov.json"))
def linkezy(i, cap):
    segs = LINKS[i]; g.link_ok(segs); k = len(segs)
    return dict(game="linkezy", headline=f"{k} pairs. One way.", sub="Join each pair. Lines can't cross, and every square gets filled.",
                vis=d.link_grid(segs, g.LINK_COLORS), caption=cap + "\n\nSee the solution and play today's Linkezy free: {link}",
                ans_title="The only solution", ans_vis=d.link_grid(segs, g.LINK_COLORS, solved=True, cell=46),
                ans_text="Each colour fills its own path, and together they cover all 36 squares.",
                pin_title=f"Connect the Dots Puzzle: {k} Pairs, Only One Solution")

DIRS = {(0, 1): "left to right", (0, -1): "backwards, right to left", (1, 0): "straight down", (-1, 0): "straight up",
        (1, 1): "diagonally down to the right", (-1, -1): "diagonally up to the left", (1, -1): "diagonally down to the left", (-1, 1): "diagonally up to the right"}
def search(target, cells, others, decoys, seed, decoy_note):
    grid = next((x for x in (g.ws_make(target, cells, others, decoys, sd) for sd in range(seed, seed + 30)) if x), None); assert grid, target
    g.ws_ok(grid, cells, target, others)
    (r0, c0), (r1, c1) = cells[0], cells[1]
    where = f"It runs {DIRS[(r1 - r0, c1 - c0)]}, starting from the {target[0]} in row {r0 + 1}, column {c0 + 1}. {decoy_note}"
    return dict(game="search", headline=f"Find {target}", sub="It's hiding once, in any direction. Watch out for the fakes.",
                vis=d.ws_grid(grid, cells, color("search"), cell=34, fs=19),
                caption=f"Find the word {target}. It's hiding in this grid exactly once, in any direction. Watch out for the fakes.\n\nSee where it is and play today's word search free: {{link}}",
                ans_title=f"Here's {target}", ans_vis=d.ws_grid(grid, cells, color("search"), True, 30, 17), ans_text=where,
                pin_title=f"Word Search Puzzle: Find {target} in the Grid")

def build_puzzles():
    P = [
     # ---------------- Fri 13
     wordezy("storm", ["north", "court", "movie"], "stor?", ["store", "stork", "story", "storm"],
             "M turned gold in MOVIE, so the word has an M. Store, stork and story don't have one, which leaves STORM."),
     lingo("es", "soap", ["jabón", "sopa", "jardín", "silla"], "“Soap” in Spanish?", "One of these is what you'd eat for lunch.",
           "How do you say \"soap\" in Spanish? Careful: one of these is something you eat with a spoon."),
     sortezy("BDAB ACCD BAAB CCDD".split(), 10),
     scramble("sweater", 3, "cosy, knitted, and perfect for November."),
     # ---------------- Sat 14
     warmezy("lighthouse", ["tower", "beacon", "shore", "coast", "sea", "number"], ["harbour", "lookout", "pier", "reef"],
             "Find the secret word", "Think coast. "),
     ladder("east", "west", "Only 3 moves. How fast can you do it?"),
     letterezy("rainbow", "ap", 21, "you might see one after the rain."),
     linkezy(0, "Join each pair of matching dots without crossing lines, and fill every square. There's only one way to do it. Can you find it?"),
     # ---------------- Sun 15
     search("SQUIRREL", [(3, 9 - i) for i in range(8)], ["ACORN", "MAPLE", "BEAVER", "RACCOON", "BADGER", "CHIPMUNK", "WALNUT", "HEDGEHOG"],
            [("SQUIR", (0, 1)), ("SQUI", (1, 0)), ("RREL", (1, 1))], 41, "The other SQUIR and SQUI near-misses are decoys."),
     wordezy("tiger", ["large", "bring", "until"], "ti?er", ["tiler", "timer", "tiger"],
             "G turned gold in LARGE and BRING, so the word has a G. Tiler and timer don't, which leaves TIGER.", sub="Timer or tiger?"),
     sortezy("CBDA BCBA DCCA DDBA".split(), 11),
     scramble("napkin", 5, "you'll want one at the dinner table."),
     # ---------------- Mon 16
     lingo("fr", "coin", ["porte", "coin", "couteau", "pièce"], "Say “coin” in French", "Careful: one of these means corner.",
           "How do you say \"coin\" in French? The obvious answer will leave you standing in a corner."),
     warmezy("unicorn", ["dragon", "elephant", "eagle", "magic", "golden", "number"], ["lion", "beast", "demon", "rhino"],
             "A magical secret word", ""),
     ladder("pass", "fail", "Can you do it in 5?"),
     linkezy(1, "Five pairs, one solution. Join each pair of matching dots without crossing lines, and fill every square."),
     # ---------------- Tue 17
     wordezy("towel", ["plate", "elect", "wrote"], "?owel", ["bowel", "dowel", "vowel", "towel"],
             "T turned gold in PLATE, ELECT and WROTE, so the word has a T. Bowel, dowel and vowel don't, which leaves TOWEL."),
     letterezy("chicken", "bu", 22, "it crossed the road."),
     search("KANGAROO", [(1 + i, 8) for i in range(8)], ["KOALA", "WOMBAT", "DINGO", "WALLABY", "POSSUM", "LIZARD", "PLATYPUS", "EMUS"],
            [("KANGA", (0, 1)), ("KANG", (1, 1)), ("GAROO", (0, -1))], 43, "The KANGA and KANG near-misses are decoys."),
     sortezy("DACC DBAB CCAB BDAD".split(), 12),
     # ---------------- Wed 18
     scramble("football", 9, "a big part of Thanksgiving Day.", headline="8 letters. One word."),
     lingo("de", "chef", ["Koch", "Chef", "Kopf", "König"], "“Chef” in German?", "One of these means your boss.",
           "How do you say \"chef\" in German? One of these looks perfect, but it means your boss."),
     warmezy("waffle", ["batter", "syrup", "butter", "breakfast", "shop", "issues"], ["fries", "sausage", "pastry", "cookies"],
             "A tasty secret word", ""),
     linkezy(2, "Six pairs this time. Join each pair of matching dots without crossing lines, and fill every square. There's only one way."),
     # ---------------- Thu 19
     wordezy("flame", ["never", "later", "medal"], "fla?e", ["flake", "flare", "flame"],
             "M turned gold in MEDAL, so the word has an M. Flake and flare don't, which leaves FLAME.", sub="Flake, flare or flame?"),
     ladder("fish", "bird", "From sea to sky in 6 moves. What's your route?"),
     letterezy("popcorn", "ag", 23, "the movie-night snack."),
     search("BUTTERFLY", [(1 + i, 1 + i) for i in range(9)], ["BEETLE", "CRICKET", "LADYBUG", "SPIDER", "HORNET", "MOTH", "WASP", "GNAT"],
            [("BUTTER", (0, 1)), ("BUTTE", (1, 0)), ("RFLY", (0, -1))], 45, "The BUTTER and BUTTE near-misses are decoys."),
     # ---------------- Fri 20
     sortezy("BDCA ACDB CDAA BDCB".split(), 13),
     scramble("potato", 11, "mash it, bake it or fry it."),
     lingo("pt", "lunch", ["lanche", "amigo", "almoço", "leite"], "“Lunch” in Portuguese?", "One of these is only a snack.",
           "How do you say \"lunch\" in Portuguese? One of these looks right, but you'd still be hungry."),
     linkezy(3, "Join each pair of matching dots without crossing lines, and fill every square. Six pairs, one solution. How fast can you find it?"),
     # ---------------- Sat 21
     wordezy("scarf", ["asked", "cause", "draft"], "scar?", ["scare", "scary", "scarf"],
             "F turned gold in DRAFT, so the word has an F. Scare and scary don't, which leaves SCARF.", sub="Scare, scary or scarf?"),
     warmezy("scarecrow", ["lantern", "witch", "ghost", "cat", "festival", "number"], ["wizard", "dorothy", "cowardly", "donkey"],
             "A spooky secret word", ""),
     ladder("moon", "star", "Can you get there in 6?"),
     letterezy("library", "ag", 24, "where you borrow books."),
     # ---------------- Sun 22
     search("PINEAPPLE", [(8, 1 + i) for i in range(9)], ["MANGO", "BANANA", "CHERRY", "LEMON", "PEACH", "PLUM", "MELON", "KIWI"],
            [("PINEA", (1, 0)), ("PINEAP", (1, 1)), ("APPLE", (0, -1))], 47, "The PINEA and PINEAP near-misses are decoys."),
     sortezy("BCDB ABCA DCDB ACAD".split(), 14, sub="The hardest one yet.", extra="Our hardest water sort so far. "),
     scramble("pilgrim", 13, "think of the Mayflower."),
     linkezy(4, "Join each pair of matching dots without crossing lines, and fill every square. There's only one way. Can you find it?"),
     # ---------------- Mon 23
     wordezy("plate", ["swept", "after", "metal"], "?late", ["slate", "plate"],
             "P turned gold in SWEPT, so the word has a P. Slate doesn't, which leaves PLATE.", sub="Slate or plate?"),
     lingo("it", "magazine", ["magazzino", "ricco", "rivista", "mercato"], "“Magazine” in Italian?", "One of these is a warehouse.",
           "How do you say \"magazine\" in Italian? Pick the obvious one and you'll end up in a warehouse."),
     warmezy("reindeer", ["elk", "moose", "wolf", "christmas", "winter", "number"], ["sheep", "herds", "deer", "bison"],
             "Find the secret word", "It's getting festive. "),
     ladder("warm", "cozy", "Perfect for a cold night. Can you do it in 6?"),
     # ---------------- Tue 24
     letterezy("pyramid", "at", 25, "you'll find famous ones in Egypt."),
     search("SNOWFLAKE", [(9 - i, 1) for i in range(9)], ["MITTEN", "SCARF", "SLED", "ICICLE", "BOOTS", "FROST", "IGLOO", "WINTER"],
            [("SNOWF", (0, 1)), ("SNOW", (1, 1)), ("FLAKE", (1, 0))], 49, "The SNOWF and SNOW near-misses are decoys."),
     sortezy("BBCD CACC DBDA BAAD".split(), 12),
     linkezy(5, "Seven pairs, our biggest one yet. Join each pair of matching dots without crossing lines, and fill every square."),
     # ---------------- Wed 25
     wordezy("cider", ["price", "board", "raise"], "?ider", ["hider", "rider", "cider"],
             "C turned gold in PRICE, so the word has a C. Hider and rider don't, which leaves CIDER.", sub="Hider, rider or cider?"),
     scramble("grateful", 15, "how you might feel at Thanksgiving.", headline="8 letters. One word."),
     lingo("es", "dessert", ["desierto", "postre", "dinero", "puerta"], "“Dessert” in Spanish?", "Save room for this one.",
           "How do you say \"dessert\" in Spanish? Pick the obvious one and you'll end up in the desert."),
     warmezy("cranberry", ["pumpkin", "sauce", "fruit", "apple", "salt", "number"], ["juice", "pineapple", "tomato", "strawberry"],
             "A Thanksgiving secret word", ""),
     # ---------------- Thu 26 (Thanksgiving)
     wordezy("feast", ["known", "later", "after"], "?east", ["beast", "least", "yeast", "feast"],
             "F turned gold in AFTER, so the word has an F. Beast, least and yeast don't, which leaves FEAST.",
             headline="Happy Thanksgiving!", sub="One letter left. Beast, least, yeast or feast?"),
     ladder("cook", "meal", "Happy Thanksgiving! Can you do it in 6?"),
     letterezy("cupcake", "as", 26, "a little cake with frosting on top."),
     search("STUFFING", [(9 - i, 1 + i) for i in range(8)], ["GRAVY", "POTATO", "PUMPKIN", "BREAD", "BEANS", "CORN", "ROLLS", "SQUASH"],
            [("STUFF", (0, 1)), ("STUF", (1, 0)), ("FFING", (0, -1))], 51, "The STUFF and STUF near-misses are decoys."),
    ]
    start = dt.datetime(2026, 11, 13, tzinfo=dt.timezone.utc)
    for i, p in enumerate(P):
        day, slot = divmod(i, 4)
        p["id"] = f"p{61 + i:03d}"
        p["at"] = (start + dt.timedelta(days=day, hours=(6, 9, 16, 19)[slot])).strftime("%Y-%m-%dT%H:%M:%SZ")
        p["pin_at"] = (start + dt.timedelta(days=day, hours=(6, 10, 14, 18)[slot])).strftime("%Y-%m-%dT%H:%M:%SZ")
    return P

MORE = ["wordezy", "linkezy", "warmezy", "sortezy", "lingoezy", "scramble", "letterezy", "search", "ladder"]
def more_for(p, i):
    pool = [k for k in MORE if k != p["game"]]
    return [pool[(i + j * 3) % len(pool)] for j in range(3)]

def main():
    import render
    P = build_puzzles()
    rep_fb = render.render(P, "fb", SITE / "social" / "fb")
    rep_pin = render.render(P, "pin", SITE / "social" / "pin")
    bad = {k: v for k, v in list(rep_fb.items()) + list(rep_pin.items()) if v["bad"] or not v["fonts"]}
    for k, v in bad.items(): print("LAYOUT", k, v)
    if bad: raise SystemExit("fix the layout problems above; nothing written")
    for i, p in enumerate(P):
        page = SITE / "a" / p["id"]; page.mkdir(parents=True, exist_ok=True)
        (page / "index.html").write_text(d.answer_page(p, more_for(p, i)))
    ids = {p["id"] for p in P}
    posts = [x for x in json.load(open(SITE / "src/posts.json")) if x["id"] not in ids]
    for p in P:
        posts.append({"id": p["id"], "at": p["at"], "game": p["game"],
                      "caption": p["caption"].format(link=f"https://bgameworld.com/a/{p['id']}") + "\n\n" + TAGS[p["game"]]})
    posts.sort(key=lambda x: x["at"])
    (SITE / "src/posts.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
    pins = [x for x in json.load(open(SITE / "src/pins.json")) if x["id"] not in ids]
    for p in P:
        board = BOARD.get(p["game"], "word")
        first = p["caption"].split("\n\n")[0]
        desc = f"{first} Tap the Pin for the answer, then play today's free puzzle at bgameworld.com. {KEYWORDS[board]}"
        assert len(desc) <= 500 and len(p["pin_title"]) <= 100, p["id"]
        q = f"utm_source=pinterest&utm_medium=social&utm_campaign={p['game']}&utm_content={p['id']}"
        pins.append({"id": p["id"], "at": p["pin_at"], "board": board, "game": p["game"], "title": p["pin_title"],
                     "description": desc, "link": f"https://bgameworld.com/a/{p['id']}/?{q}",
                     "image": f"https://bgameworld.com/social/pin/{p['id']}.jpg", "bytes": (SITE / "social/pin" / f"{p['id']}.jpg").stat().st_size})
    pins.sort(key=lambda x: x["at"])
    (SITE / "src/pins.json").write_text(json.dumps(pins, indent=1, ensure_ascii=False))
    print(f"{len(P)} puzzles: images, answer pages, posts.json ({len(posts)}), pins.json ({len(pins)})")

if __name__ == "__main__":
    main()
