"""Builds one page per course (course-*.html) and the printable rep-card.html.

Course content lives in tools/courses.json (from the Ava's Place Mini-Course Catalog doc).
Run:  python3 tools/build_courses.py   (it runs this script too)
"""
import json, pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
e = html.escape
DATA = json.loads((ROOT / "tools" / "courses.json").read_text())

TRACKS = [
    ("track-yourself", "Knowing yourself", "#E0A93B", [10, 11]),
    ("track-others", "Working with others", "#2E8B6E", [1, 2, 3]),
    ("track-manage", "Managing yourself", "#0B3A5C", [4, 5, 6, 7]),
    ("track-college", "College readiness", "#A8452F", [8, 9]),
]
ORDER = [n for _, _, _, ns in TRACKS for n in ns]
TRACK_OF = {n: (tid, name, color) for tid, name, color, ns in TRACKS for n in ns}
TITLES = {8: "SAT Prep", 9: "Entrepreneurship"}
TIER_TIME = {"Sprouts": "20 min", "Builders": "30 min", "Launchers": "40 min", "Leaders": "50 min or self-paced"}


def title(n):
    return TITLES.get(n, DATA[str(n)]["heading"])


def slug(n):
    return "course-" + re.sub(r"[^a-z0-9]+", "-", title(n).lower()).strip("-") + ".html"


def tidy(s):
    return re.sub(r"\s*\(source(, source)*\)", "", s or "").strip()


TEMPLATE = (ROOT / "tools" / "courses.template.html").read_text()
HEAD, rest = TEMPLATE.split('<main id="main">', 1)
FOOT = "</main>" + rest.split("</main>", 1)[1]


def head(page_title, desc):
    h = re.sub(r"<title>.*?</title>", f"<title>{e(page_title)} — Ava's Place Foundation</title>", HEAD, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', h)
    return h + '<main id="main">'


def course_page(n):
    c = DATA[str(n)]
    tid, tname, color = TRACK_OF[n]
    is_module = len(c["sessions"]) == 6
    unit = "Module" if is_module else "Session"
    tool_name, _, tool_rest = (c["tool"] or "").partition(". ")
    tool_name = tool_name.strip()
    tool_name = tool_name[0].upper() + tool_name[1:] if tool_name else ""
    meta = c["who"] if c.get("who") else "4 sessions · adapts to all four learner tiers (K–college)"
    i = ORDER.index(n)
    prev_n, next_n = (ORDER[i - 1] if i > 0 else None), (ORDER[i + 1] if i < len(ORDER) - 1 else None)

    out = [head(title(n), tidy(c["idea"]))]
    out.append(f'''
    <section class="page-hero bg-sky course-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="courses.html">Courses</a> <span aria-hidden="true">›</span> <a href="courses.html#{tid}">{e(tname)}</a></nav>
        <p class="eyebrow"><span class="track-dot" style="background:{color};display:inline-block;vertical-align:middle;margin-right:8px"></span>{e(tname)}</p>
        <h1>{e(title(n))}</h1>
        <p class="lead" style="margin-top:14px;max-width:760px">{e(tidy(c["idea"]))}</p>
        <p class="course-meta" style="margin-top:12px">{e(meta)}</p>
        <div class="btn-row" style="margin-top:22px">
          <a href="#s1" class="btn btn-primary">Start {unit.lower()} 1</a>
          <a href="rep-card.html" class="btn btn-outline">Print a Rep Card</a>
        </div>
      </div>
    </section>

    <section class="section" style="padding-top:56px;padding-bottom:24px">
      <div class="container course-top">
        <div class="tool big-tool"><p class="level" style="color:var(--blue)">Core tool</p><h2 class="tool-name">{e(tool_name)}</h2><p>{e(tidy(tool_rest))}</p></div>
        <form class="selfcheck card" aria-labelledby="sc-{n}">
          <h2 id="sc-{n}" class="h3">Before you start: quick self-check</h2>
          <p class="soft small">Rate each line from 1 (not yet) to 5 (definitely) before {unit.lower()} 1, then again after your Real-World Rep.</p>''')
    for k, stmt in enumerate(c.get("selfcheck", [])):
        out.append(f'<fieldset><legend>{e(stmt)}</legend><div class="scale">' +
                   "".join(f'<label><input type="radio" name="q{k}" value="{v}"><span>{v}</span></label>' for v in range(1, 6)) +
                   '</div></fieldset>')
    out.append('''</form>
      </div>
    </section>''')

    if c.get("test"):
        out.append(f'''
    <section class="section" style="padding-top:24px;padding-bottom:0"><div class="container"><div class="card info-card"><p class="level">The test at a glance</p><p>{e(tidy(c["test"]))}</p>{f'<p class="soft" style="margin-top:8px"><strong>Free practice:</strong> {e(tidy(c["free"]))}</p>' if c.get("free") else ""}</div></div></section>''')

    out.append(f'''
    <section class="section" style="padding-top:48px">
      <div class="container">
        <div class="section-head"><p class="eyebrow">The {unit.lower()}s</p><h2>{len(c["sessions"])} {unit.lower()}s, {"one per week" if is_module else "three beats each"}.</h2>
        <p class="soft" style="margin-top:10px">{"Each module: a short video, a practice set or field task, and a log entry. Go at your own pace; one module a week works well." if is_module else "Every session runs Hook → Rep → Reflect, so learners know what to expect each time."}</p></div>
        <ol class="lesson-list">''')
    for s in c["sessions"]:
        skill = f'<p class="skill">Skill it applies: {e(s["skill"])}</p>' if s.get("skill") else ""
        out.append(f'''
          <li class="lesson" id="s{s["num"]}">
            <div class="lesson-head"><span class="lesson-num">{unit} {s["num"]}</span><h3>{e(s["title"])}</h3></div>
            <div class="beats">
              <div class="beat"><span class="beat-name">Hook</span><span class="beat-time">5–10 min</span><p>{e(s["hook"])}</p></div>
              <div class="beat rep"><span class="beat-name">Rep</span><span class="beat-time">10–30 min</span><p>{e(s["rep"])}</p></div>
              <div class="beat"><span class="beat-name">Reflect</span><span class="beat-time">5–10 min</span><p>{"Log what you missed and why in your Error Log." if n == 8 else "Update your Build–Test–Learn Board: what we believed, tested, heard and will change." if n == 9 else "Write one line on your Rep Card: what I tried, what happened, what I'll try next."}</p></div>
            </div>{skill}
          </li>''')
    out.append('</ol>')

    if c.get("options"):
        out.append(f'<div class="card info-card" style="margin-top:24px"><p class="level">Pick your venture</p><p>{e(tidy(c["options"]))}</p></div>')
    out.append(f'''
        <div class="rw-callout"><p class="level" style="color:var(--gold-deep)">Real-World Rep</p><p class="rw-text">{e(tidy(c["rep"]))}</p></div>
      </div>
    </section>''')

    if c["tiers"]:
        out.append('''
    <section class="section bg-mist">
      <div class="container">
        <div class="section-head"><p class="eyebrow">By age</p><h2>How it adapts for each learner tier.</h2></div>
        <div class="grid tier-grid">''')
        for t in c["tiers"]:
            out.append(f'<div class="card tier"><p class="level">{e(t["stage"])}</p><h3>{e(t["tier"])}</h3><p class="tier-time">{TIER_TIME[t["tier"]]} sessions</p><p class="soft">{e(tidy(t["text"]))}</p></div>')
        out.append('</div></div></section>')

    if n == 8:
        out.append(worksheet("Error Log", ["Date", "Topic", "Why I missed it", "The fix", "Retest date"],
                             "For every missed question, log why: didn't know, misread, rushed or ran out of time."))
    if n == 9:
        out.append(worksheet("Build–Test–Learn Board", ["Week", "What we believe", "What we tested", "What customers said or did", "What we'll change"],
                             "One row per week. Share it with your mentor."))

    fac = [x for x in (c.get("facilitator"), (("How progress is measured: " + tidy(c["measure"])) if c.get("measure") else None)) if x]
    if fac:
        out.append('<section class="section" style="padding-bottom:0"><div class="container"><div class="card fac-card"><p class="level">For teachers &amp; facilitators</p>' +
                   "".join(f"<p>{e(tidy(x))}</p>" for x in fac) + '</div></div></section>')

    nav = []
    if prev_n: nav.append(f'<a class="pn prev" href="{slug(prev_n)}"><span>← Previous course</span><strong>{e(title(prev_n))}</strong></a>')
    else: nav.append('<span></span>')
    if next_n: nav.append(f'<a class="pn next" href="{slug(next_n)}"><span>Next course →</span><strong>{e(title(next_n))}</strong></a>')
    out.append(f'<section class="section"><div class="container prev-next">{"".join(nav)}</div></section>')
    out.append(FOOT)
    return "\n".join(out)


def worksheet(name, cols, note, rows=8):
    th = "".join(f"<th scope='col'>{e(c)}</th>" for c in cols)
    tr = "".join("<tr>" + "".join("<td></td>" for _ in cols) + "</tr>" for _ in range(rows))
    return f'''
    <section class="section">
      <div class="container">
        <div class="section-head row"><div><p class="eyebrow">Printable</p><h2>{e(name)}</h2><p class="soft" style="margin-top:10px">{e(note)}</p></div>
        <button type="button" class="btn btn-outline print-btn" onclick="window.print()">Print this page</button></div>
        <div class="sheet-wrap"><table class="sheet"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>
      </div>
    </section>'''


def rep_card():
    cols = ["Date", "Course / session", "What I tried", "What happened", "Next time I'll…", "Confidence (1–5)"]
    body = f'''
    <section class="page-hero bg-sky">
      <div class="container">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="courses.html">Courses</a> <span aria-hidden="true">›</span> Rep Card</nav>
        <h1>Rep Card</h1>
        <p class="lead" style="margin-top:12px;max-width:720px">One line per session. Track what you tried, what happened and what you'll try next. No grades, no tests.</p>
        <div class="btn-row" style="margin-top:20px"><button type="button" class="btn btn-primary" onclick="window.print()">Print the Rep Card</button></div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <p class="print-only print-title">Ava's Place · Rep Card · Name: ______________________</p>
        <div class="sheet-wrap"><table class="sheet"><thead><tr>{"".join(f"<th scope='col'>{e(c)}</th>" for c in cols)}</tr></thead>
        <tbody>{"".join("<tr>" + "".join("<td></td>" for _ in cols) + "</tr>" for _ in range(12))}</tbody></table></div>
        <p class="note">Sprouts (K–5): use smiley faces instead of 1–5, and draw instead of write.</p>
      </div>
    </section>
'''
    return head("Rep Card", "A printable Rep Card for tracking practice across Ava's Place courses.") + body + FOOT


for n in ORDER:
    (ROOT / slug(n)).write_text(course_page(n))
(ROOT / "rep-card.html").write_text(rep_card())
print(f"Built {len(ORDER)} course pages + rep-card.html")
