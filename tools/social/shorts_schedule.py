"""Writes src/shorts.json: 5 YouTube Shorts a day for 13-26 Nov 2026.

Each day: that day's 4 puzzles (each a few hours after its Facebook post, so the Short's answer
never comes before the question) plus one Linkezy gameplay video.
    09:00 UTC puzzle 1 · 13:00 puzzle 2 · 16:00 Linkezy gameplay · 19:00 puzzle 3 · 22:00 puzzle 4
"""
import json, re, datetime as dt
import nov, design as d

SITE = d.SITE
LEVELS = [12, 16, 21, 25, 28, 32, 35, 38, 42, 45, 48, 52, 55, 58]
GAME_TAGS = {
    "wordezy": ["wordle", "word game", "5 letter words", "word puzzle"],
    "lingoezy": ["language learning", "false friends", "learn spanish", "vocabulary quiz"],
    "sortezy": ["water sort", "water sort puzzle", "sorting game", "satisfying"],
    "scramble": ["word scramble", "anagram", "unscramble", "word game"],
    "warmezy": ["guess the word", "word game", "semantle", "word puzzle"],
    "letterezy": ["anagram", "word game", "spelling", "word puzzle"],
    "ladder": ["word ladder", "word game", "word puzzle", "doublets"],
    "search": ["word search", "find the word", "word puzzle", "word find"],
    "linkezy": ["connect the dots", "logic puzzle", "flow puzzle", "satisfying"],
}
BASE_TAGS = ["puzzle", "brain teaser", "puzzle game", "free games", "bgameworld"]

def puzzle_short(p, at):
    g = d.game(p["game"])
    first = re.sub(r"\s+", " ", p["caption"].split("\n\n")[0]).strip()
    title = f"{p['pin_title']} #shorts"
    assert len(title) <= 100, title
    hashtags = " ".join(t for t in nov.TAGS[p["game"]].split() if t != "#puzzle")
    desc = (f"{first} Watch to the end for the answer!\n\n"
            f"Play today's {g['name']} free, no download: {g['url']}\n"
            f"Every BGameWorld game: https://bgameworld.com\n\n#shorts #puzzle {hashtags}")
    return {"id": f"yt-{p['id']}", "at": at, "file": f"social/shorts/{p['id']}.mp4", "title": title,
            "description": desc, "tags": BASE_TAGS + [g["name"].lower()] + GAME_TAGS[p["game"]]}

LK_TITLES = ["Linkezy Level {L}: connect every pair without crossing 🧩 #shorts",
             "Can you solve Linkezy Level {L} faster? 🧩 #shorts",
             "Satisfying connect-the-dots puzzle: Level {L} ✅ #shorts",
             "Only one way to solve this: Linkezy Level {L} 🧩 #shorts"]
def linkezy_short(i, at):
    L = LEVELS[i]; g = d.game("linkezy")
    return {"id": f"yt-lk{L}", "at": at, "file": f"social/reels/linkezy-level{L}.mp4",
            "title": LK_TITLES[i % len(LK_TITLES)].format(L=L),
            "description": (f"Join each pair of matching dots without crossing lines, and fill every square. "
                            f"Here's Linkezy Level {L} being solved. How long would it take you?\n\n"
                            f"Play Linkezy free, no download: {g['url']}\nEvery BGameWorld game: https://bgameworld.com\n\n"
                            f"#shorts #puzzle #connectthedots #logicpuzzle #satisfying"),
            "tags": BASE_TAGS + ["linkezy"] + GAME_TAGS["linkezy"]}

def main():
    P = nov.build_puzzles(); start = dt.date(2026, 11, 13); out = []
    for i in range(14):
        day = (start + dt.timedelta(days=i)).isoformat()
        ps = P[4 * i: 4 * i + 4]
        out += [puzzle_short(ps[0], f"{day}T09:00:00Z"), puzzle_short(ps[1], f"{day}T13:00:00Z"),
                linkezy_short(i, f"{day}T16:00:00Z"),
                puzzle_short(ps[2], f"{day}T19:00:00Z"), puzzle_short(ps[3], f"{day}T22:00:00Z")]
    for s in out:
        assert (SITE / s["file"]).exists(), s["file"]
        assert len(",".join(s["tags"])) < 450 and len(s["description"]) < 4500
    by_id = {x["id"]: x for x in json.load(open(SITE / "src/posts.json"))}
    for s in out:                                           # a Short never reveals an answer before its Facebook post
        pid = s["id"][3:]
        if pid in by_id: assert by_id[pid]["at"] < s["at"], s["id"]
    (SITE / "src/shorts.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(out), "Shorts,", out[0]["at"], "->", out[-1]["at"])

if __name__ == "__main__":
    main()
