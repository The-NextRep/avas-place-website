"""Draws the original sports illustrations in images/sports/.

Run: python3 tools/make_sports_art.py
Each file is a flat, bold spot illustration: a colored disc, a sports ball or
piece of gear, and motion lines. No outside artwork is used.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "images", "sports")
os.makedirs(OUT, exist_ok=True)

INK = "#0E1B2B"


def svg(body, w=400, h=400):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">{body}</svg>\n')


def speed(color, x=40, y=150, n=3, gap=34, length=110):
    out = ""
    for i in range(n):
        ln = length - i * 26
        out += (f'<line x1="{x}" y1="{y + i * gap}" x2="{x + ln}" y2="{y + i * gap}" '
                f'stroke="{color}" stroke-width="14" stroke-linecap="round"/>')
    return out


def frame(bg, disc, inner):
    return svg(
        f'<rect width="400" height="400" rx="56" fill="{bg}"/>'
        f'<circle cx="230" cy="200" r="150" fill="{disc}"/>'
        f'<circle cx="335" cy="70" r="16" fill="#FFFFFF" opacity="0.6"/>'
        f'<circle cx="360" cy="110" r="8" fill="#FFFFFF" opacity="0.5"/>'
        + inner)


def basketball():
    ball = ('<g transform="translate(240 200)">'
            '<circle r="96" fill="#F07A2A" stroke="' + INK + '" stroke-width="8"/>'
            '<path d="M-96 0 H96 M0 -96 V96" stroke="' + INK + '" stroke-width="7" fill="none"/>'
            '<path d="M-68 -68 Q-30 0 -68 68 M68 -68 Q30 0 68 68" stroke="' + INK + '" stroke-width="7" fill="none"/>'
            '</g>')
    return frame("#FFE3CC", "#FFC79E", speed("#F07A2A", 26, 140) + ball)


def soccer():
    pent = "0,-30 28.5,-9.3 17.6,24.3 -17.6,24.3 -28.5,-9.3"
    ball = ('<g transform="translate(240 200)">'
            '<circle r="96" fill="#FFFFFF" stroke="' + INK + '" stroke-width="8"/>'
            f'<polygon points="{pent}" fill="{INK}"/>')
    for ang in (0, 72, 144, 216, 288):
        ball += (f'<g transform="rotate({ang}) translate(0 -74)">'
                 f'<polygon points="{pent}" transform="scale(0.62)" fill="{INK}"/></g>'
                 f'<line x1="0" y1="-30" x2="0" y2="-56" transform="rotate({ang})" stroke="{INK}" stroke-width="5"/>')
    ball += '</g>'
    return frame("#D9F5E5", "#9EE3BC", speed("#1F9D5C", 26, 140) + ball)


def football():
    ball = ('<g transform="translate(236 200) rotate(-30)">'
            '<ellipse rx="112" ry="70" fill="#8A4A22" stroke="' + INK + '" stroke-width="8"/>'
            '<path d="M-78 -46 Q-60 0 -78 46 M78 -46 Q60 0 78 46" stroke="#FFFFFF" stroke-width="8" fill="none"/>'
            '<line x1="-40" y1="0" x2="40" y2="0" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>')
    for x in (-24, -8, 8, 24):
        ball += f'<line x1="{x}" y1="-11" x2="{x}" y2="11" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>'
    ball += '</g>'
    return frame("#E3ECFF", "#B7CBFF", speed("#2F5DD8", 20, 150) + ball)


def track():
    # running shoe
    shoe = ('<g transform="translate(240 222)">'
            '<path d="M-118 20 Q-120 -30 -84 -40 L-40 -48 Q-20 -86 18 -84 L30 -58 Q70 -40 108 -16 Q130 0 120 24 Z" '
            'fill="#FF4F6D" stroke="' + INK + '" stroke-width="8" stroke-linejoin="round"/>'
            '<path d="M-124 20 H122 Q124 46 96 48 H-100 Q-126 46 -124 20 Z" fill="#FFFFFF" stroke="' + INK + '" stroke-width="8" stroke-linejoin="round"/>'
            '<path d="M-6 -66 L36 -48 M-18 -52 L24 -34 M-30 -38 L12 -20" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'
            '<path d="M-80 -10 Q-40 6 0 -4 Q40 -14 80 0" stroke="' + INK + '" stroke-width="6" fill="none" stroke-linecap="round"/>'
            '</g>')
    return frame("#FFE0E6", "#FFB3C1", speed("#FF4F6D", 20, 150) + shoe)


def volleyball():
    ball = ('<g transform="translate(240 200)">'
            '<circle r="96" fill="#FFF4C2" stroke="' + INK + '" stroke-width="8"/>'
            '<path d="M0 0 Q-10 -60 -50 -82 M0 0 Q60 -20 92 12 M0 0 Q-40 50 -20 94" stroke="' + INK + '" stroke-width="7" fill="none"/>'
            '<path d="M-30 -24 Q-60 -40 -90 -20 M40 4 Q60 50 40 86 M-16 32 Q-60 30 -84 52" stroke="#3E7CF2" stroke-width="7" fill="none"/>'
            '</g>')
    return frame("#FFF4C2", "#FFE27A", speed("#E0A93B", 20, 140) + ball)


def baseball():
    ball = ('<g transform="translate(240 200)">'
            '<circle r="96" fill="#FFFFFF" stroke="' + INK + '" stroke-width="8"/>'
            '<path d="M-56 -78 Q-20 0 -56 78 M56 -78 Q20 0 56 78" stroke="#E2384D" stroke-width="7" fill="none"/>')
    for i in range(-3, 4):
        y = i * 20
        ball += (f'<line x1="{-44 + abs(i) * 3}" y1="{y}" x2="{-30 + abs(i) * 3}" y2="{y - 8}" stroke="#E2384D" stroke-width="5" stroke-linecap="round"/>'
                 f'<line x1="{44 - abs(i) * 3}" y1="{y}" x2="{30 - abs(i) * 3}" y2="{y - 8}" stroke="#E2384D" stroke-width="5" stroke-linecap="round"/>')
    ball += '</g>'
    return frame("#EDE4FF", "#CDB8FF", speed("#7A4DE0", 20, 150) + ball)


def hero():
    """Wide program-page banner: stadium lights, field lines and flying balls."""
    w, h = 1200, 640
    b = ('<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#0B3A5C"/><stop offset="1" stop-color="#16588A"/></linearGradient>'
         '<radialGradient id="l" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#FFF6D6" stop-opacity="0.9"/>'
         '<stop offset="1" stop-color="#FFF6D6" stop-opacity="0"/></radialGradient></defs>'
         f'<rect width="{w}" height="{h}" fill="url(#g)"/>')
    for cx in (140, 1060):
        b += (f'<circle cx="{cx}" cy="90" r="150" fill="url(#l)"/>'
              f'<rect x="{cx - 60}" y="60" width="120" height="44" rx="10" fill="#FFF6D6"/>'
              f'<rect x="{cx - 6}" y="104" width="12" height="160" fill="#0A2F4C"/>')
    b += (f'<path d="M0 470 Q600 400 1200 470 V640 H0 Z" fill="#2E9E5B"/>'
          f'<path d="M0 520 Q600 450 1200 520" stroke="#FFFFFF" stroke-width="6" fill="none" opacity="0.7"/>'
          f'<path d="M0 580 Q600 510 1200 580" stroke="#FFFFFF" stroke-width="6" fill="none" opacity="0.7"/>')
    for x, y, c in ((300, 250, "#F07A2A"), (620, 190, "#FFFFFF"), (900, 290, "#FF4F6D")):
        for i in range(3):
            b += (f'<line x1="{x - 190 + i * 30}" y1="{y - 20 + i * 22}" x2="{x - 90}" y2="{y - 20 + i * 22}" '
                  f'stroke="{c}" stroke-width="10" stroke-linecap="round" opacity="0.55"/>')
    b += ('<g transform="translate(300 250)"><circle r="62" fill="#F07A2A" stroke="#0E1B2B" stroke-width="6"/>'
          '<path d="M-62 0 H62 M0 -62 V62 M-44 -44 Q-18 0 -44 44 M44 -44 Q18 0 44 44" stroke="#0E1B2B" stroke-width="5" fill="none"/></g>'
          '<g transform="translate(620 190) rotate(-25)"><ellipse rx="78" ry="48" fill="#8A4A22" stroke="#0E1B2B" stroke-width="6"/>'
          '<path d="M-54 -32 Q-42 0 -54 32 M54 -32 Q42 0 54 32" stroke="#FFFFFF" stroke-width="6" fill="none"/>'
          '<line x1="-26" y1="0" x2="26" y2="0" stroke="#FFFFFF" stroke-width="5"/></g>'
          '<g transform="translate(900 290)"><circle r="56" fill="#FFFFFF" stroke="#0E1B2B" stroke-width="6"/>'
          '<polygon points="0,-18 17,-6 11,15 -11,15 -17,-6" fill="#0E1B2B"/>'
          '<path d="M0 -18 V-40 M17 -6 L38 -14 M11 15 L24 34 M-11 15 L-24 34 M-17 -6 L-38 -14" stroke="#0E1B2B" stroke-width="4"/></g>')
    for sx, sy in ((520, 70), (760, 110), (980, 60), (420, 130), (200, 330)):
        b += f'<circle cx="{sx}" cy="{sy}" r="4" fill="#FFF6D6" opacity="0.8"/>'
    return svg(b, w, h)


ART = {
    "basketball": basketball, "soccer": soccer, "football": football,
    "track": track, "volleyball": volleyball, "baseball": baseball, "hero": hero,
}

for name, fn in ART.items():
    with open(os.path.join(OUT, f"{name}.svg"), "w") as fh:
        fh.write(fn())
print("wrote", len(ART), "files to images/sports/")
