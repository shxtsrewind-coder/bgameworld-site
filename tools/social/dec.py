"""Puzzle posts for 27 November - 10 December 2026 (p117-p172), same slots as nov.py:
4 a day on Facebook (06, 09, 16, 19 UTC, around the 12:00 challenge post) and as Pinterest Pins (06/10/14/18 UTC).

    python3 dec.py            # check every puzzle, render images, write answer pages + src/posts.json + src/pins.json
"""
import json, datetime as dt
import gamedata as g
import nov
from nov import wordezy, lingo, sortezy, scramble, warmezy, ladder, letterezy, search

LINKS = json.load(open(nov.HERE / "data" / "links-dec.json"))
def linkezy(i, cap): return nov.linkezy(i, cap, LINKS)

def build_puzzles():
    P = [
     # ---------------- Fri 27 Nov
     wordezy("chill", ["clash", "allow", "river"], "chil?", ["child", "chili", "chill"],
             "ALLOW shows two gold Ls, so the word has two of them. Child and chili only have one, which leaves CHILL.",
             sub="Child, chili or chill?"),
     lingo("es", "rope", ["ropa", "cuchara", "cuerda", "camisa"], "“Rope” in Spanish?", "One of these is what you'd wear.",
           "How do you say \"rope\" in Spanish? Pick the obvious one and you'll end up holding a pile of clothes."),
     sortezy("BBCA DDAA DBCC ACBD".split(), 10),
     scramble("cocoa", 31, "a hot drink for a cold day.", headline="5 letters. One word."),
     # ---------------- Sat 28
     warmezy("blizzard", ["snow", "storm", "fog", "hurricane", "ice", "number"], ["snowstorm", "whiteout", "avalanche", "wintry"],
             "A wintry secret word", ""),
     ladder("cold", "heat", "Time to warm up. How fast can you do it?"),
     letterezy("blanket", "lp", 27, "snuggle under it on a cold night."),
     linkezy(0, "Join each pair of matching dots without crossing lines, and fill every square. There's only one way to do it. Can you find it?"),
     # ---------------- Sun 29
     search("TOBOGGAN", [(1 + i, 2) for i in range(8)], ["SKATES", "SNOWMAN", "IGLOO", "COCOA", "GLOVES", "CHILLY", "FLEECE", "FROST"],
            [("TOBOG", (0, 1)), ("TOBO", (1, 1)), ("GGAN", (0, -1))], 53, "The TOBOG and TOBO near-misses are decoys."),
     wordezy("skate", ["known", "later", "after"], "s?ate", ["skate", "slate", "state"],
             "K turned gold in KNOWN, so the word has a K. Slate and state don't, which leaves SKATE.", sub="Skate, slate or state?"),
     sortezy("CACB CBDB ADDC DAAB".split(), 11),
     scramble("snowman", 33, "he has a carrot for a nose."),
     # ---------------- Mon 30
     lingo("fr", "cave", ["café", "grotte", "cave", "glace"], "Say “cave” in French", "Careful: one of these is a wine cellar.",
           "How do you say \"cave\" in French? The obvious answer will send you down to the wine cellar."),
     warmezy("fireplace", ["chimney", "stove", "kitchen", "roof", "wood", "number"], ["hearth", "mantel", "patio", "staircase"],
             "A cosy secret word", ""),
     ladder("work", "rest", "Happy Monday. How fast can you get to REST?"),
     linkezy(1, "Five pairs, one solution. Join each pair of matching dots without crossing lines, and fill every square."),
     # ---------------- Tue 1 Dec
     wordezy("north", ["actor", "entry", "other"], "?orth", ["forth", "north", "worth"],
             "N turned gold in ENTRY, so the word has an N. Forth and worth don't, which leaves NORTH.",
             headline="Hello, December!", sub="One letter left. Forth, north or worth?"),
     letterezy("pudding", "eu", 28, "a sweet dessert, often served with custard."),
     search("CHRISTMAS", [(9 - i, 1 + i) for i in range(9)], ["TREE", "STAR", "GIFTS", "BELLS", "ELVES", "CAROLS", "WREATH", "TINSEL"],
            [("CHRIS", (1, 0)), ("CHRI", (0, 1)), ("STMAS", (0, -1))], 55, "The CHRIS and CHRI near-misses are decoys."),
     sortezy("DCBB BCAC BADA CDAD".split(), 12),
     # ---------------- Wed 2
     scramble("sleigh", 35, "Santa's ride across the sky."),
     lingo("de", "corn", ["Korn", "Maus", "Kopf", "Mais"], "“Corn” in German?", "One of these is any old grain.",
           "How do you say \"corn\" in German? One of these looks perfect, but it just means grain."),
     warmezy("gingerbread", ["cookies", "cake", "pumpkin", "cinnamon", "bread", "issues"], ["shortbread", "fruitcake", "eggnog", "brownies"],
             "Find the secret word", "Think holiday baking. "),
     linkezy(2, "Six pairs this time. Join each pair of matching dots without crossing lines, and fill every square. There's only one way."),
     # ---------------- Thu 3
     wordezy("roast", ["storm", "water", "cents"], "?oast", ["boast", "coast", "roast", "toast"],
             "R turned gold in STORM and WATER, so the word has an R. Boast, coast and toast don't, which leaves ROAST."),
     ladder("wish", "gift", "From wish list to present. What's your route?"),
     letterezy("lantern", "ao", 29, "a light you can carry."),
     search("CHOCOLATE", [(5, 10 - i) for i in range(9)], ["CANDY", "FUDGE", "TOFFEE", "COOKIE", "CARAMEL", "BROWNIE", "MINT", "CREAM"],
            [("CHOCO", (1, 0)), ("CHOC", (0, 1)), ("LATE", (1, 1))], 57, "The CHOCO and CHOC near-misses are decoys."),
     # ---------------- Fri 4
     sortezy("BDAC DCAD CBCA BADB".split(), 13),
     scramble("cookies", 37, "leave some out for Santa."),
     lingo("it", "confetti", ["confetti", "coltello", "coriandoli", "colore"], "“Confetti” in Italian?", "One of these is a sweet treat.",
           "How do you say \"confetti\" in Italian? Throw the obvious one at a party and you'll be throwing sugared almonds."),
     linkezy(3, "Join each pair of matching dots without crossing lines, and fill every square. Six pairs, one solution. How fast can you find it?"),
     # ---------------- Sat 5
     wordezy("polar", ["about", "group", "train"], "?olar", ["molar", "polar", "solar"],
             "P turned gold in GROUP, so the word has a P. Molar and solar don't, which leaves POLAR.", sub="Molar, polar or solar?"),
     warmezy("ornament", ["decorations", "antique", "christmas", "tree", "glass", "number"], ["tinsel", "keepsake", "decorative", "ornate"],
             "A festive secret word", "Deck the halls. "),
     ladder("lead", "gold", "Real alchemy. Can you do it?"),
     letterezy("biscuit", "ae", 30, "dunk it in your tea."),
     # ---------------- Sun 6
     search("SNOWBOARD", [(9 - i, 9) for i in range(9)], ["SKIS", "SLOPE", "LIFT", "POLES", "HELMET", "GOGGLES", "LODGE", "PISTE"],
            [("SNOWB", (0, 1)), ("SNOW", (1, 1)), ("BOARD", (1, 0))], 59, "The SNOWB and SNOW near-misses are decoys."),
     sortezy("ADCA BCBC CDAD ABBD".split(), 12),
     scramble("jingle", 39, "___ Bells."),
     linkezy(4, "Join each pair of matching dots without crossing lines, and fill every square. There's only one way. Can you find it?"),
     # ---------------- Mon 7
     wordezy("sweet", ["write", "white", "today"], "s?eet", ["sheet", "sleet", "sweet"],
             "W turned gold in WRITE and WHITE, so the word has a W. Sheet and sleet don't, which leaves SWEET.", sub="Sheet, sleet or sweet?"),
     lingo("pt", "balcony", ["varanda", "barco", "balcão", "vazio"], "“Balcony” in Portuguese?", "One of these is a shop counter.",
           "How do you say \"balcony\" in Portuguese? Pick the obvious one and you'll be standing at a shop counter."),
     warmezy("marshmallow", ["chocolate", "jelly", "vanilla", "candy", "sugar", "plans"], ["fluff", "caramel", "toffee", "gooey"],
             "A sweet secret word", "Perfect in hot cocoa. "),
     ladder("word", "game", "Our favourite kind of game. What's your route?"),
     # ---------------- Tue 8
     letterezy("cracker", "ei", 31, "eat one with cheese, or pull one at Christmas dinner."),
     search("MISTLETOE", [(1, 1 + i) for i in range(9)], ["HOLLY", "IVY", "PINE", "FIR", "BERRY", "CONES", "CEDAR", "SPRUCE"],
            [("MISTLE", (1, 0)), ("MIST", (1, 1)), ("LETOE", (0, -1))], 61, "The MISTLE and MIST near-misses are decoys."),
     sortezy("BCBC ACDA DBDA CBAD".split(), 14, sub="One of our hardest.", extra="One of our toughest water sorts. "),
     linkezy(5, "Seven pairs, the biggest size. Join each pair of matching dots without crossing lines, and fill every square."),
     # ---------------- Wed 9
     wordezy("holly", ["blood", "whose", "local"], "?olly", ["dolly", "folly", "holly", "jolly"],
             "H turned gold in WHOSE, so the word has an H. Dolly, folly and jolly don't, which leaves HOLLY."),
     scramble("frosty", 41, "how it feels outside on a winter morning."),
     lingo("es", "carpet", ["carta", "carpeta", "camisa", "alfombra"], "“Carpet” in Spanish?", "One of these belongs in your office.",
           "How do you say \"carpet\" in Spanish? The obvious answer is something you'd keep your papers in."),
     warmezy("cinnamon", ["ginger", "cloves", "spices", "sugar", "bread", "support"], ["nutmeg", "cardamom", "vanilla", "allspice"],
             "A spicy secret word", ""),
     # ---------------- Thu 10
     wordezy("merry", ["prime", "range", "after"], "?erry", ["berry", "ferry", "merry"],
             "M turned gold in PRIME, so the word has an M. Berry and ferry don't, which leaves MERRY.", sub="Berry, ferry or merry?"),
     ladder("bell", "ring", "Ring in the season. What's your route?"),
     letterezy("iceberg", "ap", 32, "most of it hides under the water."),
     search("PAJAMAS", [(2 + i, 8 - i) for i in range(7)], ["SLIPPERS", "PILLOW", "ROBE", "TEDDY", "LAMP", "BOOK", "NAPS", "SOCKS"],
            [("PAJAM", (0, 1)), ("PAJA", (1, 0)), ("JAMAS", (0, -1))], 63, "The PAJAM and PAJA near-misses are decoys."),
    ]
    start = dt.datetime(2026, 11, 27, tzinfo=dt.timezone.utc)
    for i, p in enumerate(P):
        day, slot = divmod(i, 4)
        p["id"] = f"p{117 + i:03d}"
        p["at"] = (start + dt.timedelta(days=day, hours=(6, 9, 16, 19)[slot])).strftime("%Y-%m-%dT%H:%M:%SZ")
        p["pin_at"] = (start + dt.timedelta(days=day, hours=(6, 10, 14, 18)[slot])).strftime("%Y-%m-%dT%H:%M:%SZ")
    return P

def check(P):
    """Nothing repeats an earlier answer, every Wordezy option is a real word, 4 posts a day, no game twice in a day."""
    import collections, pathlib, re, html
    old = {html.unescape(re.sub(r"<.*?>", "", m)).upper() for f in pathlib.Path(nov.SITE / "a").glob("p*/index.html")
           if int(f.parent.name[1:]) < 117 for m in re.findall(r"<h2[^>]*>(.*?)</h2>", f.read_text())}
    words = [p for p in P if p["game"] not in ("sortezy", "linkezy")]      # those two have generic answer titles
    for p in words:
        assert p["ans_title"].upper() not in old, (p["id"], p["ans_title"])
        if p["game"] == "wordezy":
            listed = [w.lower().strip(" ?") for w in re.split(r",| or ", p["sub"].split(".")[-1])]
            assert all(w in g.WZ_DICT for w in listed) and p["ans_title"].split()[-1].lower() in listed, (p["id"], listed)
    days = collections.defaultdict(list)
    for p in P: days[p["at"][:10]].append(p["game"])
    assert all(len(v) == 4 and len(set(v)) == 4 for v in days.values()), days
    assert len(P) == 56 and len({p["ans_title"] for p in words}) == len(words)
    assert len({p["vis"] for p in P}) == 56

if __name__ == "__main__":
    P = build_puzzles(); check(P); nov.publish(P)
