"""Builds the hero marquee in index.html.

Drop photos into images/marquee/ named by audience, e.g.
  youth-1.jpg, families-2.jpg, disability-1.jpg, athletes-3.jpg
then run:  python3 tools/build_marquee.py
Audiences without photos fall back to branded tiles.
"""
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
PHOTOS = ROOT / "images" / "marquee"

AUDIENCES = {
    "youth": ("Youth", '<path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.9z"/>'),
    "families": ("Families", '<circle cx="8" cy="7" r="3"/><circle cx="17" cy="9" r="2.4"/><path d="M2.5 20c0-3.3 2.5-6 5.5-6s5.5 2.7 5.5 6"/><path d="M14 20c0-2.6 1.4-4.6 3-4.6s3.5 2 3.5 4.6"/>'),
    "disability": ("Disability community", '<circle cx="12" cy="4.5" r="1.8"/><path d="M5 8.5h14"/><path d="M12 8.5v5l-3.5 7"/><path d="M12 13.5l3.5 7"/>'),
    "athletes": ("Athletes", '<path d="M7 4h10v4a5 5 0 0 1-10 0z"/><path d="M7 6H4.5a2.5 2.5 0 0 0 2.6 3"/><path d="M17 6h2.5a2.5 2.5 0 0 1-2.6 3"/><path d="M12 13v4"/><path d="M8.5 20h7"/>'),
}
ORDER = ["youth", "families", "disability", "athletes"]
ROWS = [("", 0), (" reverse", 1), (" slow", 2), (" reverse", 3)]
TILES_PER_ROW = 8


def photos_for(key):
    if not PHOTOS.exists():
        return []
    return sorted(p for p in PHOTOS.iterdir() if p.name.startswith(key) and p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})


def tile(key, n):
    label, icon = AUDIENCES[key]
    pics = photos_for(key)
    if pics:
        src = pics[n % len(pics)].relative_to(ROOT).as_posix()
        inner = f'<img src="{src}" alt="" loading="lazy">'
    else:
        inner = f'<svg class="tile-icon" viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{icon}</svg>'
    return f'<div class="tile tile-{key}">{inner}<span class="tile-label">{html.escape(label)}</span></div>'


def build():
    rows = []
    count = {k: 0 for k in ORDER}
    for cls, offset in ROWS:
        tiles = []
        for i in range(TILES_PER_ROW):
            key = ORDER[(i + offset) % len(ORDER)]
            tiles.append(tile(key, count[key]))
            count[key] += 1
        seq = "".join(tiles)
        rows.append(f'        <div class="marquee-row{cls}">{seq}{seq}</div>')  # doubled for a seamless loop
    return '      <div class="marquee" aria-hidden="true">\n' + "\n".join(rows) + "\n      </div>\n"


text = INDEX.read_text()
start = text.index("<!-- MARQUEE:START")
start = text.index("-->", start) + 3
end = text.index("      <!-- MARQUEE:END -->")
INDEX.write_text(text[:start] + "\n" + build() + text[end:])
print("Marquee rebuilt.")
