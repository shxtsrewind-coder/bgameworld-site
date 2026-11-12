"""Renders post images with headless Chromium and checks nothing spills off the card."""
import pathlib, tempfile
from playwright.sync_api import sync_playwright
import design

CHECK = """() => {
  const c = document.querySelector('.post'), r = c.getBoundingClientRect(), bad = [];
  for (const el of c.querySelectorAll('h1, .sub, .vis > div > *, .foot')) {
    const x = el.getBoundingClientRect();
    if (x.right > r.right - 12 || x.left < r.left + 12 || x.bottom > r.bottom + 0.5) bad.push(el.className || el.tagName);
  }
  const v = document.querySelector('.vis'), inner = v.firstElementChild.getBoundingClientRect(), vr = v.getBoundingClientRect();
  if (inner.height > vr.height + 1) bad.push('visual too tall by ' + Math.round(inner.height - vr.height));
  if (inner.width > vr.width + 1) bad.push('visual too wide by ' + Math.round(inner.width - vr.width));
  const h = document.querySelector('h1').getBoundingClientRect();
  return {bad, fonts: document.fonts.check('700 40px "Zilla Slab"') && document.fonts.check('600 16px "Libre Franklin"'),
          headLines: Math.round(h.height / 47)};
}"""

def render(posts, kind, out_dir, ext=None):
    out_dir = pathlib.Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    w, h = (540, 675) if kind == "fb" else (500, 750)
    ext = ext or ("png" if kind == "fb" else "jpg")
    tmp = pathlib.Path(tempfile.mkdtemp())
    report = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
        for p in posts:
            f = tmp / f"{p['id']}-{kind}.html"; f.write_text(design.post_html(p, kind))
            pg.goto(f"file://{f}"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(120)
            report[p["id"]] = pg.evaluate(CHECK)
            path = out_dir / f"{p['id']}.{ext}"
            if ext == "jpg": pg.locator(".post").screenshot(path=str(path), type="jpeg", quality=88)
            else: pg.locator(".post").screenshot(path=str(path))
        b.close()
    return report
