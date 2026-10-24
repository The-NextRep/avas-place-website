import sys, math, subprocess, wave, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from module_video_scripts import COURSES

W, H, FPS = 1280, 720, 30
FD = "/home/claude/vid/fonts/"
def F(name, s): return ImageFont.truetype(FD + name, s)
LORA = lambda s: F("lora-700-normal.ttf", s)
LORA_I = lambda s: F("lora-600-italic.ttf", s)
SANS = lambda s, w="600": F(f"source-sans-3-{w}-normal.ttf", s)
CINZ = lambda s: F("cinzel-latin-700-normal.ttf", s)
NAVY = (11, 58, 92); NAVY_D = (7, 40, 66); GOLD = (224, 169, 59); GOLD_D = (143, 96, 10)
CREAM = (251, 246, 234); INK = (14, 27, 43); SOFT = (58, 70, 86); LINE = (234, 227, 210)
OUT = "/home/claude/modvid/out"; os.makedirs(OUT, exist_ok=True)
LOGO = Image.open("/home/claude/avas-place-website/images/logo-mark-clear.png").convert("RGBA")

def ease(x): x = min(max(x, 0.0), 1.0); return 1 - (1 - x) ** 3
def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def text_block(d, x, y, text, font, fill, maxw, lh=1.25, align="left", alpha=255):
    lines = wrap(text, font, maxw); sz = font.size
    for i, ln in enumerate(lines):
        lx = x if align == "left" else x + (maxw - font.getlength(ln)) / 2
        d.text((lx, y + i * sz * lh), ln, font=font, fill=fill + (alpha,))
    return y + len(lines) * sz * lh
def block_height(text, font, maxw, lh=1.25): return len(wrap(text, font, maxw)) * font.size * lh

def bg(color, grad=None):
    if grad is None: return Image.new("RGBA", (W, H), color + (255,))
    yy = np.linspace(0, 1, H)[:, None, None]
    a = np.array(color, np.float32) * (1 - yy) + np.array(grad, np.float32) * yy
    return Image.fromarray(np.repeat(a, W, 1).astype(np.uint8)).convert("RGBA")
BG_CREAM = bg(CREAM, (246, 238, 220)); BG_NAVY = bg(NAVY, NAVY_D); BG_GOLD = bg((232, 180, 74), (214, 156, 44))

def logo(size_h):
    w = int(LOGO.width * size_h / LOGO.height); return LOGO.resize((w, size_h), Image.LANCZOS)
LOGO_S = logo(46); LOGO_L = logo(150)
WM = logo(300); WM.putalpha(WM.getchannel("A").point(lambda v: int(v * 0.22)))

def footer_brand(img, dark_bg):
    d = ImageDraw.Draw(img)
    img.alpha_composite(LOGO_S, (56, H - 46 - 34))
    d.text((56 + LOGO_S.width + 12, H - 34 - 23), "AVA'S PLACE", font=CINZ(20), fill=(CREAM if dark_bg else NAVY) + (255,), anchor="lm")

def build_scenes(course, mi):
    title, idea, points, rep = course["modules"][mi]
    S = [("title", 4.2), ("idea", 6.0), ("points", 15.0), ("rep", 6.5), ("tool", 5.0), ("outro", 3.3)]
    return S, dict(title=title, idea=idea, points=points, rep=rep)

def frame(course, mi, t, S, c):
    acc = 0
    for name, dur in S:
        if t < acc + dur or name == "outro": break
        acc += dur
    u = t - acc; L = dur
    fade = min(1, u / 0.35, max(0, (L - u)) / 0.3) if name != "outro" else min(1, u / 0.35, max(0, L - u) / 0.6)
    A = lambda a: int(255 * max(0, min(1, a)) * fade)
    eyebrow = f"{course['name'].upper()}  ·  MODULE {mi + 1}"
    if name == "title":
        img = BG_CREAM.copy(); d = ImageDraw.Draw(img)
        wm = WM.copy(); wm.putalpha(wm.getchannel("A").point(lambda v: int(v * A(1) / 255)))
        img.alpha_composite(wm, (W - wm.width - 40, (H - wm.height) // 2 - 20)); d = ImageDraw.Draw(img)
        f = LORA(80); th = block_height(c["title"], f, 760, 1.12); y0 = (H - th) / 2 - 30
        d.text((96, y0 - 50), eyebrow, font=SANS(26, "700"), fill=GOLD_D + (A(ease(u / .5)),))
        y = y0 + (1 - ease(u / .6)) * 24
        y2 = text_block(d, 96, y, c["title"], f, NAVY, 760, 1.12, alpha=A(ease(u / .6)))
        ln = 220 * ease((u - .4) / .6); d.rectangle([96, y2 + 22, 96 + ln, y2 + 28], fill=GOLD + (A(1),))
        footer_brand(img, False)
    elif name == "idea":
        img = BG_NAVY.copy(); d = ImageDraw.Draw(img)
        f = LORA_I(60); h = block_height(c["idea"], f, 1060, 1.22); y0 = (H - h) / 2 - 20
        d.text((96, y0 - 52), "THE BIG IDEA", font=SANS(24, "700"), fill=GOLD + (A(ease(u / .4)),))
        text_block(d, 96, y0 + (1 - ease(u / .7)) * 20, c["idea"], f, CREAM, 1060, 1.22, alpha=A(ease((u - .15) / .6)))
        footer_brand(img, True)
    elif name == "points":
        img = BG_CREAM.copy(); d = ImageDraw.Draw(img)
        per = L / 3
        tot = sum(max(block_height(p, SANS(38, "600"), 960, 1.25), 56) + 40 for p in c["points"]); y = max(130, (H - tot) / 2 + 10)
        d.text((96, y - 60), "WHAT TO KNOW", font=SANS(24, "700"), fill=GOLD_D + (A(1),))
        for k, p in enumerate(c["points"]):
            st = k * per
            if u < st: break
            a = ease((u - st) / .5); active = st <= u < st + per
            f = SANS(38, "600"); h = block_height(p, f, 960, 1.25)
            cy = y + 26
            d.ellipse([96, cy - 26, 148, cy + 26], fill=(GOLD if active else LINE) + (A(a),))
            d.text((122, cy), str(k + 1), font=SANS(28, "700"), fill=(NAVY if active else SOFT) + (A(a),), anchor="mm")
            text_block(d, 180, y + 4 + (1 - a) * 14, p, f, NAVY if active else SOFT, 960, 1.25, alpha=A(a if active else a * .75))
            y += max(h, 56) + 40
        footer_brand(img, False)
    elif name == "rep":
        img = BG_GOLD.copy(); d = ImageDraw.Draw(img)
        h = block_height(c["rep"], LORA(56), 1080, 1.2); y0 = (H - h) / 2 - 20
        d.text((96, y0 - 52), "YOUR REP", font=SANS(26, "700"), fill=NAVY_D + (A(ease(u / .4)),))
        text_block(d, 96, y0 + (1 - ease(u / .6)) * 20, c["rep"], LORA(56), NAVY_D, 1080, 1.2, alpha=A(ease((u - .1) / .6)))
        footer_brand(img, False)
    elif name == "tool":
        img = BG_CREAM.copy(); d = ImageDraw.Draw(img)
        th = block_height(course["tool"], SANS(40, "600"), W - 272, 1.3); bh = th + 80; y0 = (H - bh) / 2 - 40
        d.text((96, y0 - 50), "USE YOUR " + course["tool_name"].upper(), font=SANS(26, "700"), fill=GOLD_D + (A(ease(u / .4)),))
        d.rounded_rectangle([96, y0, W - 96, y0 + bh], 22, fill=(255, 255, 255, A(ease(u / .5))), outline=LINE + (A(1),), width=3)
        text_block(d, 136, y0 + 40, course["tool"], SANS(40, "600"), NAVY, W - 272, 1.3, alpha=A(ease((u - .2) / .5)))
        d.text((96, y0 + bh + 34), "Fill it in after every module. It's how you see your progress.", font=SANS(28, "400"), fill=SOFT + (A(ease((u - .6) / .5)),))
        footer_brand(img, False)
    else:
        img = BG_NAVY.copy(); d = ImageDraw.Draw(img)
        a = A(ease(u / .5))
        L2 = LOGO_L.copy(); L2.putalpha(L2.getchannel("A").point(lambda v: int(v * a / 255)))
        img.alpha_composite(L2, ((W - L2.width) // 2, 170))
        d.text((W / 2, 370), "AVA'S PLACE", font=CINZ(44), fill=CREAM + (a,), anchor="mm")
        d.text((W / 2, 420), "A Place to Belong. A Path Forward.", font=LORA_I(28), fill=GOLD + (a,), anchor="mm")
        d.text((W / 2, 480), "avasplace.org", font=SANS(26, "600"), fill=CREAM + (int(a * .8),), anchor="mm")
    return img

def music(dur, path):
    SR = 44100; n = int(SR * dur); t = np.arange(n) / SR; out = np.zeros(n, np.float32)
    chords = [[220.0, 277.18, 329.63], [196.0, 246.94, 293.66], [174.61, 220.0, 261.63], [196.0, 246.94, 329.63]]  # A, G, F, G-ish warm
    bar = 2.857  # 84 bpm, 4 beats
    for i in range(int(dur / bar) + 1):
        ch = chords[i % 4]; s = int(i * bar * SR); m = min(n - s, int(bar * 1.2 * SR))
        if m <= 0: break
        x = np.arange(m) / SR; env = np.minimum(1, x / 0.6) * np.exp(-x * 0.5)
        pad = sum(np.sin(2 * np.pi * f * x) + 0.3 * np.sin(4 * np.pi * f * x) for f in ch) * env * 0.05
        out[s:s + m] += pad.astype(np.float32)
        for k in range(8):  # soft pluck arpeggio, 8th notes
            ps = s + int(k * bar / 8 * SR); pm = min(n - ps, int(0.6 * SR))
            if pm <= 0: continue
            px = np.arange(pm) / SR; f = ch[k % 3] * 2
            pl = (np.sin(2 * np.pi * f * px) * np.exp(-px * 7) * 0.06).astype(np.float32)
            out[ps:ps + pm] += pl
    out *= np.clip(t / 1.0, 0, 1) * np.clip((dur - t) / 1.5, 0, 1)
    out /= max(1e-6, np.abs(out).max()) / 0.5
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())

def render(slug, mi):
    course = COURSES[slug]; S, c = build_scenes(course, mi); dur = sum(d for _, d in S)
    wav = f"{OUT}/{slug}-{mi + 1}.wav"; music(dur, wav)
    outp = f"{OUT}/{slug}-module-{mi + 1}.mp4"
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                          "-i", "-", "-i", wav, "-c:v", "libx264", "-crf", "26", "-preset", "medium", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart", outp], stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        img = frame(course, mi, i / FPS, S, c)
        p.stdin.write(np.asarray(img.convert("RGB")).tobytes())
        if i in (60, 240, 600, 820, 960): img.convert("RGB").save(f"{OUT}/{slug}-{mi + 1}-p{i}.jpg", quality=80)
    p.stdin.close(); p.wait(); os.remove(wav)
    # poster frame (title card)
    frame(course, mi, 2.5, S, c).convert("RGB").save(f"{OUT}/{slug}-module-{mi + 1}.jpg", quality=82)
    print("done", outp, flush=True)

if __name__ == "__main__":
    jobs = [(s, i) for s in COURSES for i in range(len(COURSES[s]["modules"]))]
    if sys.argv[1] == "one": render(sys.argv[2], int(sys.argv[3]))
    else:
        part, nparts = int(sys.argv[1]), int(sys.argv[2])
        for k, (s, i) in enumerate(jobs):
            if k % nparts == part: render(s, i)
