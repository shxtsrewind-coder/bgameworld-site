"""Game data and puzzle checks for BGameWorld's social posts.

Every puzzle posted to Facebook or Pinterest is built and checked here with the
game's own word lists and rules, cloned from GitHub into REPOS:

    mkdir -p /home/claude/repos && cd /home/claude/repos
    for r in wordezy wordezy-ladder Wordezy-Scramble letterezy Warmezy Lingoezy; do
      git clone --depth 1 https://github.com/shxtsrewind-coder/$r.git; done

Not served by the website (tools/ is in .assetsignore).
"""
import os, re, json, math, random, subprocess, itertools, unicodedata
from collections import deque, Counter

REPOS = os.environ.get("BGW_REPOS", "/home/claude/repos")

# ------------------------------------------------------------------ word frequency (Warmezy's vocab is frequency-ordered)
VOCAB = open(f"{REPOS}/Warmezy/data/vocab.txt").read().split()
FREQ = {w: i for i, w in enumerate(VOCAB)}
def freq(w): return FREQ.get(w.lower(), 10**6)

# ------------------------------------------------------------------ Wordezy
WZ_DICT = set(re.findall(r'"([a-z]{5})"', open(f"{REPOS}/wordezy/src/data/dictionary.ts").read()))

def wordle_colors(guess, answer):
    res = ["x"] * 5; rem = Counter()
    for i in range(5):
        if guess[i] == answer[i]: res[i] = "g"
        else: rem[answer[i]] += 1
    for i in range(5):
        if res[i] != "g" and rem[guess[i]] > 0:
            res[i] = "y"; rem[guess[i]] -= 1
    return "".join(res)

def wordezy_board(answer, guesses, typed):
    """Three guesses plus a part-typed row ('?' = missing) that only the answer fits."""
    for g in guesses + [answer]:
        assert g in WZ_DICT, g
    cands = [w for w in WZ_DICT
             if all(wordle_colors(g, w) == wordle_colors(g, answer) for g in guesses)
             and all(typed[i] in ("?", w[i]) for i in range(5))]
    assert cands == [answer], (answer, cands)
    others = sorted(w for w in WZ_DICT if w != answer and all(typed[i] in ("?", w[i]) for i in range(5)))
    return {"rows": [{"letters": g.upper(), "colors": wordle_colors(g, answer)} for g in guesses],
            "typed": typed.upper(), "answer": answer.upper(), "others": others}

def wz_find(ans, n_hidden, tries=4000, seed=1, maxfreq=6000):
    D = sorted(WZ_DICT); common = [w for w in D if freq(w) < maxfreq]; rnd = random.Random(seed); out = []
    for hid in itertools.combinations(range(5), n_hidden):
        typed = "".join("?" if i in hid else ans[i] for i in range(5))
        pm = [w for w in D if all(typed[i] in ("?", w[i]) for i in range(5))]
        if len(pm) < 3: continue
        for _ in range(tries):
            gs = rnd.sample(common, 3)
            if ans in gs: continue
            cs = [wordle_colors(g, ans) for g in gs]
            if any(c == "ggggg" for c in cs) or any(c[i] == "g" for c in cs for i in hid): continue
            if [w for w in pm if all(wordle_colors(g, w) == c for g, c in zip(gs, cs))] != [ans]: continue
            score = len(pm) * 3 + sum(c.count("y") for c in cs) - sum(freq(g) for g in gs) / 3000
            out.append((round(score, 2), typed, gs, cs, pm))
    out.sort(reverse=True); seen = set(); res = []
    for o in out:
        if o[1] not in seen: seen.add(o[1]); res.append(o)
    return res[:3]

# ------------------------------------------------------------------ Sortezy (fewest moves; one move pours every matching layer that fits)
def sort_solve(tubes, cap=4):
    start = tuple(tuple(t) for t in tubes)
    solved = lambda s: all(len(t) == 0 or (len(t) == cap and len(set(t)) == 1) for t in s)
    def moves(s):
        for i, a in enumerate(s):
            if not a: continue
            top = a[-1]; k = 1
            while k < len(a) and a[-1 - k] == top: k += 1
            for j, b in enumerate(s):
                if i == j or len(b) == cap or (b and b[-1] != top): continue
                n = min(k, cap - len(b)); t = list(s); t[i] = a[:-n]; t[j] = b + (top,) * n
                yield (i, j), tuple(t)
    key = lambda s: tuple(sorted(s)); par = {key(start): None}; q = deque([start])
    while q:
        s = q.popleft()
        if solved(s):
            path = []; k = key(s)
            while par[k]:
                prev, mv = par[k]; path.append(mv); k = key(prev)
            return path[::-1]
        for mv, t in moves(s):
            k = key(t)
            if k not in par: par[k] = (s, mv); q.append(t)

def sort_find(n_moves, how_many, start_seed, exclude=()):
    out = []
    for seed in range(start_seed, start_seed + 20000):
        rnd = random.Random(seed); balls = list("AAAABBBBCCCCDDDD"); rnd.shuffle(balls)
        tubes = [balls[i * 4:(i + 1) * 4] for i in range(4)] + [[], []]
        if any(len(set(t)) == 1 for t in tubes if t) or any(t[-1] == t[-2] == t[-3] for t in tubes if t): continue
        key = tuple("".join(t) for t in tubes[:4])
        if key in exclude: continue
        sol = sort_solve(tubes)
        if sol and len(sol) == n_moves:
            out.append(list(key))
            if len(out) == how_many: return out
    return out

SORT_COLORS = {"A": "#E5484D", "B": "#F2CF3A", "C": "#3CC6D9", "D": "#8B5CF6"}

# ------------------------------------------------------------------ Wordezy Ladder
_lsrc = open(f"{REPOS}/wordezy-ladder/src/data/words.ts").read()
CORE4 = set(re.search(r'export const CORE_4\s*=\s*"([^"]*)"', _lsrc).group(1).split())

def _nb(w):
    for i in range(4):
        for ch in "abcdefghijklmnopqrstuvwxyz":
            x = w[:i] + ch + w[i + 1:]
            if x != w and x in CORE4: yield x

def _dist(a):
    dist = {a: 0}; q = deque([a])
    while q:
        w = q.popleft()
        for x in _nb(w):
            if x not in dist: dist[x] = dist[w] + 1; q.append(x)
    return dist

def ladder_path(a, b):
    """Shortest route whose least common word is as common as possible."""
    da, db = _dist(a), _dist(b)
    if b not in da: return None
    L = da[b]; path = [a]; w = a
    while w != b:
        opts = [x for x in _nb(w) if da.get(x) == da[w] + 1 and db.get(x) == L - da[w] - 1]
        w = min(opts, key=freq); path.append(w)
    return [x.upper() for x in path]

def ladder_ok(path):
    p = [w.lower() for w in path]
    assert all(w in CORE4 for w in p), path
    assert all(sum(x != y for x, y in zip(a, b)) == 1 for a, b in zip(p, p[1:])), path
    assert _dist(p[0])[p[-1]] == len(p) - 1, "not the shortest"

# ------------------------------------------------------------------ Wordezy Scramble + Letterezy word lists
_ssrc = open(f"{REPOS}/Wordezy-Scramble/src/data/words.ts").read()
def _obj(name):
    m = re.search(r"export const " + name + r"[^=]*=\s*(\{.*?\});", _ssrc, re.S)
    t = re.sub(r"(\d+):", r'"\1":', m.group(1)); t = re.sub(r",\s*([}\]])", r"\1", t)
    return json.loads(t)
SCR_ANS = {int(k): v for k, v in _obj("ANSWERS_BY_LENGTH").items()}
SCR_ALSO = _obj("ALSO_ACCEPTED")
_letsrc = open(f"{REPOS}/letterezy/src/data/words.ts").read()
LET_VALID = set(re.search(r'export const VALID_WORDS = "([^"]*)"', _letsrc).group(1).split())
_vals = re.search(r"export const VALUES[^{]*\{(.*?)\}", open(f"{REPOS}/letterezy/src/lib/letters.ts").read(), re.S).group(1)
LET_VALUES = {k: int(v) for k, v in re.findall(r"([a-z]):\s*(\d+)", _vals)}

def letter_score(word):
    """Letterezy's wordScore: 4th letter doubles, reaching the 5th square doubles the word, 7 letters add 20."""
    w = word.lower(); s = sum(LET_VALUES[c] * (2 if i == 3 else 1) for i, c in enumerate(w))
    if len(w) > 4: s *= 2
    if len(w) == 7: s += 20
    return s

_upcoming = None
def scramble_upcoming(days_back=21, days_ahead=90):
    """Every answer in Scramble's daily puzzles around now, computed by the game's own code."""
    global _upcoming
    if _upcoming is None:
        js = ("import { getDailyPuzzle } from '%s/Wordezy-Scramble/src/lib/scramble.ts';"
              "const out=new Set();const d0=Date.now()-%d*864e5;"
              "for(let i=0;i<%d;i++){const d=new Date(d0+i*864e5).toISOString().slice(0,10);"
              "for(const r of getDailyPuzzle(d).rounds)out.add(r.answer);}console.log(JSON.stringify([...out]));"
              % (REPOS, days_back, days_back + days_ahead))
        r = subprocess.run(["node", "--experimental-strip-types", "--no-warnings", "--input-type=module", "-e", js],
                           capture_output=True, text=True, check=True)
        _upcoming = set(json.loads(r.stdout))
    return _upcoming

def scramble_ok(word, scrambled):
    big = LET_VALID | {w for L in SCR_ANS.values() for w in L}
    anagrams = [w for w in big if sorted(w) == sorted(word)]
    assert anagrams == [word], (word, anagrams)
    assert not SCR_ALSO.get(word), (word, SCR_ALSO.get(word))
    assert word not in scramble_upcoming(), (word, "is in an upcoming daily Scramble")
    s = scrambled.lower()
    assert sorted(s) == sorted(word) and all(a != b for a, b in zip(s, word))

def derange(word, seed):
    """A scramble with no letter in its own place and no 3-letter run of the word."""
    rnd = random.Random(seed); w = word.upper()
    for _ in range(20000):
        s = "".join(rnd.sample(w, len(w)))
        if all(a != b for a, b in zip(s, w)) and not any(w[i:i + 3] in s for i in range(len(w) - 2)):
            return s
    raise ValueError(word)

def _formable(w, rack):
    c = Counter(rack.lower()); return all(c[k] >= v for k, v in Counter(w).items())

def letter_extras(word, letters="abdegilmnoprstu"):
    """Pairs of extra letters that leave `word` as the only 7+ letter word in the 9."""
    L7 = [w for w in LET_VALID if len(w) >= 7]
    return ["".join(ex) for ex in itertools.combinations_with_replacement(letters, 2)
            if [w for w in L7 if _formable(w, word + "".join(ex))] == [word]]

def letter_rack(word, extra, seed):
    rnd = random.Random(seed); letters = (word + extra).upper()
    for _ in range(20000):
        s = "".join(rnd.sample(letters, len(letters)))
        if not any(word.upper()[i:i + 3] in s for i in range(len(word) - 2)): return s
    raise ValueError(word)

def letter_ok(word, rack):
    hits = [w for w in LET_VALID if len(w) >= 7 and _formable(w, rack)]
    assert hits == [word], (word, hits)

# ------------------------------------------------------------------ Lingoezy false friends
_H = open(f"{REPOS}/Lingoezy/public/index.html").read()
_raw = re.search(r"const VOCAB_RAW = `(.*?)`;", _H, re.S).group(1).strip().split("\n")
LINGO_VOC = [r.split("|") for r in _raw]
LINGO_COL = {"es": 1, "fr": 2, "pt": 3, "de": 4, "it": 5}
_ffsrc = re.search(r"const FALSE_FRIENDS = (\{.*?\n\});", _H, re.S).group(1)
FF = {lang: [json.loads("[" + m.replace("'", '"') + "]") for m in re.findall(r"\[(.*?)\]", body)]
      for lang, body in re.findall(r"(\w\w): \[(.*?)\n  \]", _ffsrc, re.S)}

def lingo_bank(lang):
    words = {}
    for r in LINGO_VOC: words.setdefault(r[LINGO_COL[lang]], r[0])
    for en, w, trap, trap_en in FF[lang]:
        words.setdefault(w, en); words.setdefault(trap, trap_en)
    return words

def _fold(s): return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c)).lower()

def lingo_lookalikes(target, lang, ex_words, ex_meanings, n=8):
    words = lingo_bank(lang); ft = _fold(target); out = []
    for w, m in words.items():
        if w in ex_words or m in ex_meanings or _fold(w) == ft: continue
        f = _fold(w); p = 0
        while p < len(f) and p < len(ft) and f[p] == ft[p]: p += 1
        s = min(p, 4) * 3 + (3 if f[0] == ft[0] else 0) - abs(len(f) - len(ft)) * 0.7 + (1 if f[-1] == ft[-1] else 0)
        out.append((round(s, 1), w, m))
    return sorted(out, reverse=True)[:n]

def lingo_answer(lang, en, options):
    """Checks a 4-option question and explains every option with the game's own meanings."""
    words = lingo_bank(lang)
    _, answer, trap, trap_en = next(r for r in FF[lang] if r[0] == en)
    assert answer in options and trap in options and len(set(options)) == 4
    expl = []
    for o in options:
        m = en if o == answer else trap_en if o == trap else words[o]
        expl.append({"word": o, "means": m, "kind": "good" if o == answer else "bad" if o == trap else ""})
    expl.sort(key=lambda x: {"good": 0, "bad": 1}.get(x["kind"], 2))
    return {"letter": "ABCD"[options.index(answer)], "answer": answer, "trap": trap, "trap_en": trap_en, "explain": expl}

# ------------------------------------------------------------------ Warmezy
_W = f"{REPOS}/Warmezy/data"
_V = None
WARM_ANS = json.load(open(f"{_W}/answers.json")); WARM_ANSSET = set(WARM_ANS["daily"]) | set(WARM_ANS["practice"])
WARM_BLOCK = set(open(f"{_W}/blocked.txt").read().split())
IDX = {w: i for i, w in enumerate(VOCAB)}

def warm_ranking(word):
    import numpy as np
    global _V
    if _V is None:
        _V = np.fromfile(f"{_W}/vectors.i8", dtype=np.int8).reshape(len(VOCAB), 300).astype(np.int32)
    a = IDX[word]; sims = _V @ _V[a]; sims[a] = 2**31 - 1
    order = np.lexsort((np.arange(len(VOCAB)), -sims.astype(np.int64)))
    rank = np.empty(len(VOCAB), dtype=np.int64); rank[order] = np.arange(1, len(VOCAB) + 1)
    return order, rank

def warm_band(r):
    return "Boiling" if r <= 50 else "Hot" if r <= 300 else "Warm" if r <= 1500 else "Cool" if r <= 5000 else "Cold"

def warm_rows(secret, guesses):
    assert secret not in WARM_ANSSET, (secret, "is a Warmezy answer")
    order, rank = warm_ranking(secret)
    rows = []
    for g in guesses:
        r = int(rank[IDX[g]]); pct = round(max(0.03, 1 - math.log(r) / math.log(len(VOCAB))) * 100, 1)
        rows.append({"word": g, "rank": r, "band": warm_band(r), "pct": pct})
    assert [x["rank"] for x in rows] == sorted(x["rank"] for x in rows)
    closest = [(VOCAB[i], int(rank[i])) for i in order[1:60] if VOCAB[i] not in WARM_BLOCK]
    return rows, closest

def warm_options(secret):
    """Common guesses per heat band, to hand-pick a row set from."""
    order, rank = warm_ranking(secret)
    pick = lambda lo, hi, n, mx: [(VOCAB[i], int(rank[i])) for i in order[lo:hi] if i < mx and VOCAB[i] not in WARM_BLOCK and VOCAB[i].isalpha()][:n]
    return {"top": pick(1, 51, 18, 20000), "hot": pick(51, 301, 16, 6000), "warm": pick(301, 1501, 12, 3000),
            "cold": [(VOCAB[i], int(rank[i])) for i in range(200, 1400, 53) if rank[i] > 5000][:8]}

# ------------------------------------------------------------------ Linkezy (6x6, one solution)
N6 = 6
def _nbrs(p):
    r, c = p
    for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        a, b = r + dr, c + dc
        if 0 <= a < N6 and 0 <= b < N6: yield (a, b)

def _ham(rnd):
    path = []
    for r in range(N6):
        row = [(r, c) for c in range(N6)]; path += row if r % 2 == 0 else row[::-1]
    for _ in range(3000):
        if rnd.random() < 0.5: path.reverse()
        x = rnd.choice([x for x in _nbrs(path[-1]) if x != path[-2]]); i = path.index(x)
        path = path[:i + 1] + path[i + 1:][::-1]
    return path

def link_solutions(ends, limit=2):
    grid = {}
    for k, (a, b) in enumerate(ends): grid[a] = k; grid[b] = k
    count = [0]
    def rec(k, head, filled):
        if count[0] >= limit: return
        for x in _nbrs(head):
            if x == ends[k][1]:
                if k + 1 == len(ends):
                    if filled == N6 * N6: count[0] += 1
                else: rec(k + 1, ends[k + 1][0], filled)
                continue
            if x not in grid:
                grid[x] = k; rec(k, x, filled + 1); del grid[x]
    rec(0, ends[0][0], 2 * len(ends))
    return count[0]

def link_find(K, start_seed):
    for seed in range(start_seed, start_seed + 60000):
        rnd = random.Random(seed); path = _ham(rnd)
        cuts = sorted(rnd.sample(range(3, N6 * N6 - 2), K - 1)); segs = []; prev = 0
        for c in cuts + [N6 * N6]: segs.append(path[prev:c]); prev = c
        if any(len(s) < 3 for s in segs): continue
        if link_solutions([(s[0], s[-1]) for s in segs]) == 1:
            return [[list(p) for p in s] for s in segs]

def link_ok(segs):
    assert sum(len(s) for s in segs) == 36
    assert link_solutions([(tuple(s[0]), tuple(s[-1])) for s in segs]) == 1

LINK_COLORS = ["#E4002B", "#0072CE", "#00A651", "#FFC20E", "#F47B20", "#8E44AD", "#00B5E2"]   # Linkezy's own pair colours (A, B, C...)

# ------------------------------------------------------------------ Word search (11x11, target once, decoys)
NWS = 11
DIR8 = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]
WS_BAD = ["ASS", "SEX", "FUCK", "FUK", "FUC", "SHIT", "CUM", "TIT", "DICK", "COCK", "PISS", "NAZI", "FAG", "CUNT", "DAMN", "BITCH", "SLUT",
          "WHORE", "NIG", "RAPE", "PORN", "BOOB", "ANAL", "ANUS", "PENIS", "PENI", "HELL", "KKK", "JIZZ", "TWAT", "DIK", "FAP", "WTF", "POO",
          "PEE", "HOE", "GOD", "KILL", "DIE", "GUN"]

def ws_count(g, w):
    n = 0
    for r in range(NWS):
        for c in range(NWS):
            for dr, dc in DIR8:
                if all(0 <= r + dr * i < NWS and 0 <= c + dc * i < NWS and g[r + dr * i][c + dc * i] == ch for i, ch in enumerate(w)): n += 1
    return n

def ws_make(target, cells, others, decoys, seed):
    rnd = random.Random(seed)
    for _ in range(5000):
        g = [[None] * NWS for _ in range(NWS)]
        for i, (a, b) in enumerate(cells): g[a][b] = target[i]
        ok = True
        for w in others:
            for _ in range(400):
                dr, dc = rnd.choice([(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0)])
                r = rnd.randrange(NWS); c = rnd.randrange(NWS)
                cs = [(r + dr * i, c + dc * i) for i in range(len(w))]
                if all(0 <= a < NWS and 0 <= b < NWS and g[a][b] in (None, w[i]) for i, (a, b) in enumerate(cs)):
                    for i, (a, b) in enumerate(cs): g[a][b] = w[i]
                    break
            else: ok = False; break
        if not ok: continue
        for w, (dr, dc) in decoys:
            for _ in range(400):
                r = rnd.randrange(NWS); c = rnd.randrange(NWS)
                cs = [(r + dr * i, c + dc * i) for i in range(len(w))]
                if all(0 <= a < NWS and 0 <= b < NWS and g[a][b] is None for (a, b) in cs):
                    for i, (a, b) in enumerate(cs): g[a][b] = w[i]
                    break
        for r in range(NWS):
            for c in range(NWS):
                if g[r][c] is None: g[r][c] = rnd.choice("ABCDEFGHIKLMNOPRSTUVWY")
        if ws_count(g, target) == 1 and all(ws_count(g, w) == 1 for w in others) and not any(ws_count(g, b) for b in WS_BAD):
            return ["".join(r) for r in g]

def ws_ok(grid, cells, target, others):
    assert ws_count(grid, target) == 1 and all(ws_count(grid, w) == 1 for w in others)
    assert not any(ws_count(grid, b) for b in WS_BAD)
    assert "".join(grid[r][c] for r, c in cells) == target
