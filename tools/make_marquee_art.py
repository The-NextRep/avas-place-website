"""Draws the illustrated hero-marquee scenes into images/marquee/*.svg.

Real photos dropped into images/marquee/ (youth-*.jpg etc.) take priority
when tools/build_marquee.py runs; delete the matching .svg files to use only photos.
"""
import pathlib, math

OUT = pathlib.Path(__file__).resolve().parent.parent / "images" / "marquee"
OUT.mkdir(parents=True, exist_ok=True)

SKIN = ["#8D5524", "#C68642", "#E0AC69", "#5C3A21", "#F1C27D", "#A0662F"]
HAIR = ["#1E140C", "#2B1A10", "#3B2416", "#121212", "#5A3A1E"]

BG = {
    "youth": ("#2C6FA6", "#9CC4E4", "#5E8F5A"),
    "families": ("#C98A2E", "#F3D59A", "#7D9A5B"),
    "disability": ("#2E8577", "#A9DCCF", "#6E9C6A"),
    "athletes": ("#7A2E3E", "#E8A9A0", "#4E7D4A"),
}


def scene(key, body, sun=(238, 46)):
    top, bottom, ground = BG[key]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="600" height="400">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs>
<rect width="300" height="200" fill="url(#sky)"/>
<circle cx="{sun[0]}" cy="{sun[1]}" r="34" fill="#FFE7A3" opacity="0.35"/><circle cx="{sun[0]}" cy="{sun[1]}" r="20" fill="#FFE7A3" opacity="0.75"/>
<path d="M0 168 Q150 150 300 168 V200 H0 Z" fill="{ground}"/>
{body}
</svg>'''


def arm(sx, sy, ex, ey, s, color):
    return f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{color}" stroke-width="{6.5*s:.1f}" stroke-linecap="round"/>'


ARMS = {  # endpoint offsets from shoulder, in units of s
    "down": (5, 30), "up": (8, -34), "out": (24, -2), "hold": (14, 18), "wave": (16, -30), "forward": (22, 10),
}


def person(x, g, s=1.0, skin=0, hair=0, shirt="#F2B33D", pants="#0B3A5C", left="down", right="down",
           run=False, backpack=None, hair_long=False, facing=1):
    sk, hr = SKIN[skin % len(SKIN)], HAIR[hair % len(HAIR)]
    hy = g - 92 * s
    parts = []
    # legs
    if run:
        parts.append(f'<path d="M{x-4*s:.1f} {g-42*s:.1f} L{x-18*s*facing:.1f} {g-14*s:.1f} L{x-26*s*facing:.1f} {g-2*s:.1f}" fill="none" stroke="{pants}" stroke-width="{8*s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
        parts.append(f'<path d="M{x+4*s:.1f} {g-42*s:.1f} L{x+14*s*facing:.1f} {g-22*s:.1f} L{x+24*s*facing:.1f} {g-4*s:.1f}" fill="none" stroke="{pants}" stroke-width="{8*s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        for dx in (-6, 6):
            parts.append(f'<line x1="{x+dx*s:.1f}" y1="{g-42*s:.1f}" x2="{x+dx*1.15*s:.1f}" y2="{g-2*s:.1f}" stroke="{pants}" stroke-width="{8*s:.1f}" stroke-linecap="round"/>')
    if backpack:
        parts.append(f'<rect x="{x-17*s*facing - (0 if facing>0 else 10*s):.1f}" y="{g-80*s:.1f}" width="{10*s:.1f}" height="{30*s:.1f}" rx="{4*s:.1f}" fill="{backpack}"/>')
    # torso
    parts.append(f'<rect x="{x-13*s:.1f}" y="{g-81*s:.1f}" width="{26*s:.1f}" height="{42*s:.1f}" rx="{10*s:.1f}" fill="{shirt}"/>')
    # arms
    for side, pose in ((-1, left), (1, right)):
        ox, oy = ARMS[pose]
        sx, sy = x + side * 11 * s, g - 74 * s
        parts.append(arm(sx, sy, sx + side * ox * s, sy + oy * s, s, sk))
    # head
    if hair_long:
        parts.append(f'<path d="M{x-13*s:.1f} {hy:.1f} Q{x-15*s:.1f} {hy+22*s:.1f} {x-8*s:.1f} {hy+20*s:.1f} L{x+8*s:.1f} {hy+20*s:.1f} Q{x+15*s:.1f} {hy+22*s:.1f} {x+13*s:.1f} {hy:.1f} Z" fill="{hr}"/>')
    parts.append(f'<circle cx="{x:.1f}" cy="{hy:.1f}" r="{11*s:.1f}" fill="{sk}"/>')
    parts.append(f'<path d="M{x-11.5*s:.1f} {hy-1*s:.1f} A{11.5*s:.1f} {11.5*s:.1f} 0 0 1 {x+11.5*s:.1f} {hy-1*s:.1f} Q{x:.1f} {hy-6*s:.1f} {x-11.5*s:.1f} {hy-1*s:.1f} Z" fill="{hr}"/>')
    return "\n".join(parts)


def wheelchair(x, g, s=1.0, skin=0, hair=0, shirt="#F2B33D", pants="#0B3A5C", right="down", left="hold", hair_long=False):
    sk, hr = SKIN[skin % len(SKIN)], HAIR[hair % len(HAIR)]
    seat_y = g - 34 * s
    p = []
    p.append(f'<circle cx="{x-2*s:.1f}" cy="{g-26*s:.1f}" r="{25*s:.1f}" fill="none" stroke="#1B2433" stroke-width="{4*s:.1f}"/>')
    p.append(f'<circle cx="{x-2*s:.1f}" cy="{g-26*s:.1f}" r="{19*s:.1f}" fill="none" stroke="#CFD6DE" stroke-width="{2*s:.1f}"/>')
    p.append(f'<circle cx="{x+30*s:.1f}" cy="{g-6*s:.1f}" r="{6*s:.1f}" fill="none" stroke="#1B2433" stroke-width="{3*s:.1f}"/>')
    p.append(f'<path d="M{x-14*s:.1f} {g-74*s:.1f} L{x-12*s:.1f} {seat_y:.1f} L{x+26*s:.1f} {seat_y:.1f} L{x+30*s:.1f} {g-8*s:.1f}" fill="none" stroke="#1B2433" stroke-width="{3.5*s:.1f}" stroke-linejoin="round"/>')
    # legs (bent)
    p.append(f'<path d="M{x-2*s:.1f} {seat_y-6*s:.1f} L{x+22*s:.1f} {seat_y-6*s:.1f} L{x+24*s:.1f} {g-10*s:.1f}" fill="none" stroke="{pants}" stroke-width="{8*s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    # torso
    p.append(f'<rect x="{x-12*s:.1f}" y="{seat_y-46*s:.1f}" width="{24*s:.1f}" height="{42*s:.1f}" rx="{10*s:.1f}" fill="{shirt}"/>')
    for side, pose in ((-1, left), (1, right)):
        ox, oy = ARMS[pose]
        sx, sy = x + side * 10 * s, seat_y - 40 * s
        p.append(arm(sx, sy, sx + side * ox * s, sy + oy * s, s, sk))
    hy = seat_y - 58 * s
    if hair_long:
        p.append(f'<path d="M{x-13*s:.1f} {hy:.1f} Q{x-15*s:.1f} {hy+22*s:.1f} {x-8*s:.1f} {hy+20*s:.1f} L{x+8*s:.1f} {hy+20*s:.1f} Q{x+15*s:.1f} {hy+22*s:.1f} {x+13*s:.1f} {hy:.1f} Z" fill="{hr}"/>')
    p.append(f'<circle cx="{x:.1f}" cy="{hy:.1f}" r="{11*s:.1f}" fill="{sk}"/>')
    p.append(f'<path d="M{x-11.5*s:.1f} {hy-1*s:.1f} A{11.5*s:.1f} {11.5*s:.1f} 0 0 1 {x+11.5*s:.1f} {hy-1*s:.1f} Q{x:.1f} {hy-6*s:.1f} {x-11.5*s:.1f} {hy-1*s:.1f} Z" fill="{hr}"/>')
    return "\n".join(p)


def book(x, y, color="#D8382E"):
    return f'<rect x="{x}" y="{y}" width="16" height="12" rx="2" fill="{color}"/><line x1="{x+8}" y1="{y}" x2="{x+8}" y2="{y+12}" stroke="#FFFFFF" stroke-width="1.5"/>'


def football(x, y, r=0):
    return f'<g transform="translate({x} {y}) rotate({r})"><ellipse rx="10" ry="6" fill="#7A3E1B"/><line x1="-4" y1="0" x2="4" y2="0" stroke="#FFFFFF" stroke-width="1.4"/><line x1="-2" y1="-2" x2="-2" y2="2" stroke="#FFFFFF" stroke-width="1"/><line x1="0" y1="-2" x2="0" y2="2" stroke="#FFFFFF" stroke-width="1"/><line x1="2" y1="-2" x2="2" y2="2" stroke="#FFFFFF" stroke-width="1"/></g>'


SCENES = {
    # Youth: kids learning
    "youth-1": scene("youth", person(110, 182, 0.85, skin=0, hair=0, shirt="#F2B33D", left="down", right="up", backpack="#D8382E")
                     + person(178, 182, 0.8, skin=4, hair=4, shirt="#FFFFFF", pants="#2E4057", left="hold", right="down", hair_long=True, backpack="#1D7A6B")
                     + book(186, 120)),
    "youth-2": scene("youth", '<rect x="40" y="132" width="220" height="8" rx="3" fill="#7A4E26"/><rect x="52" y="140" width="6" height="30" fill="#7A4E26"/><rect x="242" y="140" width="6" height="30" fill="#7A4E26"/>'
                     + person(95, 176, 0.75, skin=2, hair=1, shirt="#E8765A", left="down", right="up")
                     + person(150, 176, 0.75, skin=3, hair=3, shirt="#F2B33D", left="hold", right="hold", hair_long=True)
                     + person(205, 176, 0.75, skin=1, hair=2, shirt="#5DA9E9", left="up", right="down")
                     + book(142, 122, "#0B3A5C") + book(78, 122, "#2E8577"), sun=(260, 36)),
    # Families
    "families-1": scene("families", person(105, 182, 1.0, skin=1, hair=0, shirt="#0B3A5C", pants="#2B2B2B", left="down", right="out")
                        + person(150, 182, 0.62, skin=1, hair=1, shirt="#E8765A", left="out", right="out", hair_long=True)
                        + person(195, 182, 0.95, skin=1, hair=2, shirt="#7CC4A0", pants="#3A3A3A", left="out", right="down", hair_long=True)),
    "families-2": scene("families", person(120, 182, 1.0, skin=3, hair=3, shirt="#B9A4E8", pants="#2E4057", left="hold", right="out", hair_long=True)
                        + person(172, 182, 0.6, skin=3, hair=0, shirt="#F2B33D", left="out", right="wave")
                        + person(222, 182, 0.5, skin=3, hair=1, shirt="#5DA9E9", left="wave", right="down"), sun=(60, 44)),
    # Disability community
    "disability-1": scene("disability", wheelchair(120, 182, 1.0, skin=2, hair=1, shirt="#F2B33D", right="wave")
                          + person(205, 182, 0.95, skin=0, hair=0, shirt="#0B3A5C", pants="#2B2B2B", left="wave", right="down")),
    "disability-2": scene("disability", wheelchair(110, 182, 0.95, skin=4, hair=4, shirt="#E8765A", right="up", hair_long=True)
                          + wheelchair(200, 182, 0.95, skin=3, hair=3, shirt="#5DA9E9", right="up")
                          + '<circle cx="155" cy="70" r="7" fill="#F2B33D"/>', sun=(50, 40)),
    # Athletes
    "athletes-1": scene("athletes", person(150, 182, 1.05, skin=3, hair=3, shirt="#F2B33D", pants="#FFFFFF", left="up", right="up")
                        + football(150, 66, -20)
                        + '<g stroke="#FFFFFF" stroke-width="2" opacity="0.6"><line x1="20" y1="172" x2="280" y2="172"/><line x1="60" y1="164" x2="60" y2="180"/><line x1="240" y1="164" x2="240" y2="180"/></g>'),
    "athletes-2": scene("athletes", person(130, 182, 1.0, skin=0, hair=0, shirt="#0B3A5C", pants="#2B2B2B", left="forward", right="wave", run=True)
                        + person(215, 182, 0.9, skin=2, hair=4, shirt="#FFFFFF", pants="#7A2E3E", left="wave", right="forward", run=True, hair_long=True)
                        + '<g stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.55"><line x1="70" y1="110" x2="92" y2="110"/><line x1="64" y1="124" x2="90" y2="124"/><line x1="160" y1="118" x2="180" y2="118"/></g>', sun=(50, 44)),
}

for name, svg in SCENES.items():
    (OUT / f"{name}.svg").write_text(svg)
print(f"Wrote {len(SCENES)} scenes to {OUT}")
