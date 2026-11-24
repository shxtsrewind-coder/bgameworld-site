"""Adds the puzzle videos (the same files as the YouTube Shorts) to src/reels.json as Facebook Reels.

    python3 reels_schedule.py 2026-11-24T20:30 p061 p116     # 2 a day at 10:30 and 20:30 UTC from the first slot

Each Reel only goes out after its puzzle's Facebook picture post, so the answer never comes first.
"""
import sys, json, datetime as dt, pathlib
SITE = pathlib.Path(__file__).resolve().parents[2]
HOOKS = ["Can you solve it before the timer runs out? ⏱️", "10 seconds. Can you get it? ⏱️", "Beat the timer 👇",
         "How fast can you solve this? 🧩", "Pause it if you need to 😉", "Only 10 seconds. Go! ⏱️"]

def main(first, a, b):
    shorts = {s["id"][3:]: s for s in json.load(open(SITE / "src/shorts.json")) if s["id"].startswith("yt-p")}
    posts = {p["id"]: p for p in json.load(open(SITE / "src/posts.json"))}
    ids = [f"p{i:03d}" for i in range(int(a[1:]), int(b[1:]) + 1)]
    t = dt.datetime.fromisoformat(first).replace(tzinfo=dt.timezone.utc); out = []
    for i, pid in enumerate(ids):
        s = shorts[pid]
        body = s["description"].replace("Watch to the end for the answer!", "Watch to the end for the answer 👀").replace("#shorts", "#reels")
        cap = f"{HOOKS[i % len(HOOKS)]}\n\n{body}"
        at = t.strftime("%Y-%m-%dT%H:%M:%SZ")
        assert posts[pid]["at"] < at, pid
        assert (SITE / s["file"]).exists()
        out.append({"id": f"rv-{pid}", "at": at, "file": s["file"], "title": s["title"].replace(" #shorts", ""), "caption": cap})
        t += dt.timedelta(hours=10) if t.hour == 10 else dt.timedelta(hours=14)     # 10:30 -> 20:30 -> next day 10:30
    reels = [r for r in json.load(open(SITE / "src/reels.json")) if r["id"] not in {x["id"] for x in out}] + out
    reels.sort(key=lambda r: r["at"])
    (SITE / "src/reels.json").write_text(json.dumps(reels, indent=1, ensure_ascii=False))
    print(len(out), "Reels,", out[0]["at"], "->", out[-1]["at"])

if __name__ == "__main__":
    main(*sys.argv[1:4])
