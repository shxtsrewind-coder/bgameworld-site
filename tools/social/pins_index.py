"""Writes social/pins.json: the title, game and picture of every scheduled
post and Pin, for the admin page's "Top pins" tab. Public (it only repeats what
the posts themselves show). Run after adding a batch:  python3 pins_index.py"""
import json, pathlib

SITE = pathlib.Path(__file__).resolve().parents[2]

def build():
    pins = json.load(open(SITE / "src/pins.json"))
    posts = json.load(open(SITE / "src/posts.json"))
    out = {}
    for p in posts:  # Facebook posts: the first line of the caption is the hook
        out[p["id"]] = {"title": p["caption"].split("\n")[0][:120], "game": p.get("game"), "posted": p["at"][:10],
                        "image": f"/social/fb/{p['id']}.png" if (SITE / "social/fb" / f"{p['id']}.png").exists() else None}
    for p in pins:   # Pins win: their title is written to be read on its own
        out[p["id"]] = {**out.get(p["id"], {}), "title": p["title"], "game": p.get("game"), "board": p.get("board"),
                        "pinned": p["at"][:10], "image": f"/social/pin/{p['id']}.jpg" if (SITE / "social/pin" / f"{p['id']}.jpg").exists() else out.get(p["id"], {}).get("image")}
    (SITE / "social/pins.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    return len(out)

if __name__ == "__main__":
    print(build(), "posts and pins in social/pins.json")
