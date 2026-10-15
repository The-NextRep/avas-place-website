"""Builds one page per course (course-*.html) and the printable rep-card.html.

Course content lives in tools/courses.json (from the Ava's Place Mini-Course Catalog doc).
Run:  python3 tools/build_courses.py   (it runs this script too)
"""
import json, pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
e = html.escape
DATA = json.loads((ROOT / "tools" / "courses.json").read_text())

TRACKS = [
    ("track-yourself", "Knowing yourself", "#E0A93B", [10, 15, 11, 21]),
    ("track-others", "Working with others", "#2E8B6E", [16, 18, 2, 1, 3]),
    ("track-manage", "Managing yourself", "#0B3A5C", [4, 5, 6, 7]),
    ("track-college", "College & career readiness", "#A8452F", [19, 20, 8, 9]),
    ("track-ready", "Real-world readiness", "#6B4FA0", [14, 12, 17, 13]),
]
ORDER = [n for _, _, _, ns in TRACKS for n in ns]
TRACK_OF = {n: (tid, name, color) for tid, name, color, ns in TRACKS for n in ns}
TITLES = {8: "SAT Prep", 9: "Entrepreneurship", 13: "NIL & Recruiting", 16: "Bullying: Stand Strong, Stand Up"}
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

    if c.get("parents"):
        out.append(f'<div class="card info-card" style="margin-top:24px"><p class="level">For parents &amp; guardians</p><p>{e(tidy(c["parents"]))}</p></div>')
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

CONTACT = "info@the-nextrep.com"   # where school / Title I / sponsor requests are emailed — change in one place

PATHS = [
    ("Sprouts", "Grades K–5", "20-minute sessions with stories, games and picture cards. Best done with a parent or teacher.", [10, 15, 16, 18, 6, 12, 17, 14]),
    ("Builders", "Grades 6–8", "30-minute sessions with scenarios, partner practice and simple trackers.", [10, 15, 11, 16, 18, 6, 4, 12, 17, 14]),
    ("Launchers", "Grades 9–12", "40-minute sessions with case studies, role-play and personal plans.", [10, 15, 6, 11, 4, 14, 12, 19, 20, 8, 13]),
    ("Leaders", "College & first-year adults", "Self-paced or 50-minute sessions with real-life projects and reflection.", [10, 15, 6, 5, 14, 19, 17, 9]),
]


def start_page():
    cards = []
    for tier, stage, desc, path in PATHS:
        items = "".join(f'<li><a href="{slug(n)}">{e(title(n))}</a></li>' for n in path)
        cards.append(f'<article class="card path-card" id="{tier.lower()}"><p class="level">{e(stage)}</p><h3>{e(tier)}</h3><p class="soft">{e(desc)}</p><ol class="path-list">{items}</ol><a class="btn btn-primary self-start push" href="{slug(path[0])}">Start this path</a></article>')
    body = f'''
    <section class="page-hero bg-sky">
      <div class="container">
        <p class="eyebrow">Families &amp; learners · Free</p>
        <h1>Start learning free.</h1>
        <p class="lead" style="margin-top:14px;max-width:760px">No account, no cost. Every Ava's Place course is open to every family. Pick your stage, follow the suggested path, and keep track on a printable Rep Card.</p>
        <ol class="steps-row">
          <li><span>1</span>Pick your stage below</li>
          <li><span>2</span>Open a course and work through its sessions</li>
          <li><span>3</span>Print a <a href="rep-card.html">Rep Card</a>, then a <a href="certificate.html">certificate</a> when you finish</li>
        </ol>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-head"><p class="eyebrow">Suggested paths</p><h2>Choose your stage.</h2><p class="soft" style="margin-top:10px">Each course stands alone, so feel free to jump to whatever you need most. These orders build on each other.</p></div>
        <div class="grid path-grid">{"".join(cards)}</div>
        <div class="card info-card" style="margin-top:28px"><p class="level">Social-emotional essentials</p><p>New to Ava's Place? These five build the inner skills everything else rests on: <a href="{slug(10)}">Confidence</a>, <a href="{slug(15)}">Emotional Intelligence</a>, <a href="{slug(11)}">Peer Pressure</a>, <a href="{slug(16)}">Bullying</a> and <a href="{slug(6)}">Resilience</a>.</p></div>
        <div class="card info-card" style="margin-top:16px"><p class="level">Students with disabilities</p><p>Add <a href="{slug(21)}">My Voice, My Plan</a> to any path to practice self-advocacy, lead your own IEP or 504 meeting, and plan for college and work.</p></div>
        <div class="card info-card" style="margin-top:16px"><p class="level">Athletes</p><p>Add <a href="{slug(13)}">NIL &amp; Recruiting</a> (grades 9–12 and college) to any path, with a track for parents and guardians.</p></div>
        <p class="note">Prefer to browse? See the <a href="courses.html">full course catalog</a>.</p>
      </div>
    </section>
'''
    return head("Start Learning Free", "Free Ava's Place courses for every family: pick your stage and follow a suggested learning path.") + body + FOOT


def certificate_page():
    opts = "".join(f'<option>{e(title(n))}</option>' for n in ORDER)
    body = f'''
    <section class="page-hero bg-sky no-print">
      <div class="container">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="start.html">Start learning</a> <span aria-hidden="true">›</span> Certificate</nav>
        <h1>Print your certificate</h1>
        <p class="lead" style="margin-top:12px;max-width:720px">Finished a course and your Real-World Rep? Fill in your name, pick the course, and print.</p>
      </div>
    </section>
    <section class="section">
      <div class="container cert-layout">
        <form class="card cert-form no-print" id="cert-form">
          <label for="cert-name">Learner's name</label><input id="cert-name" type="text" autocomplete="name" placeholder="First and last name">
          <label for="cert-course">Course completed</label><select id="cert-course">{opts}</select>
          <label for="cert-date">Date</label><input id="cert-date" type="date">
          <button type="button" class="btn btn-primary" onclick="window.print()">Print certificate</button>
        </form>
        <div class="certificate" id="certificate" aria-live="polite">
          <img src="images/logo-mark-clear.webp" width="520" height="338" alt="" class="cert-logo">
          <p class="cert-kicker">Ava's Place Foundation</p>
          <p class="cert-title">Certificate of Completion</p>
          <p class="cert-small">This certifies that</p>
          <p class="cert-name" id="out-name">Your Name</p>
          <p class="cert-small">completed the course and its Real-World Rep</p>
          <p class="cert-course" id="out-course">{e(title(ORDER[0]))}</p>
          <p class="cert-date" id="out-date"></p>
          <p class="cert-pillars">Support · Connection · Opportunity</p>
        </div>
      </div>
    </section>
'''
    return head("Certificate", "Print an Ava's Place course completion certificate.") + body + FOOT


def schools_page():
    body = f'''
    <section class="page-hero bg-sky">
      <div class="container">
        <p class="eyebrow">Schools, districts &amp; colleges</p>
        <h1>Bring Ava's Place to your students.</h1>
        <p class="lead" style="margin-top:14px;max-width:780px">All 21 courses are free for families. Schools and colleges pay one flat yearly fee for the training, support and reporting around them, and Title I schools get the full package free through sponsors.</p>
        <div class="btn-row" style="margin-top:20px"><a href="#request" class="btn btn-primary">Request a license</a><a href="#title-i" class="btn btn-outline">Title I schools</a></div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="section-head"><p class="eyebrow">Licenses</p><h2>Simple yearly pricing.</h2></div>
        <div class="sheet-wrap"><table class="sheet price-table"><thead><tr><th scope="col">License</th><th scope="col">Who</th><th scope="col">Per year</th><th scope="col">What's included</th></tr></thead><tbody>
          <tr><td>Elementary school</td><td>Individual K–5 schools</td><td><strong>$750</strong></td><td>All courses, facilitator kit, recorded teacher training, whole-class setup, before-and-after results report</td></tr>
          <tr><td>Middle or high school</td><td>Individual 6–12 schools</td><td><strong>$1,000–$1,500</strong></td><td>Everything in Elementary, plus SAT Prep for high schools</td></tr>
          <tr><td>District</td><td>5 or more schools</td><td><strong>20% off each school</strong></td><td>Same as the school licenses, with one district-wide report</td></tr>
          <tr><td>College or university</td><td>Colleges, first-year programs</td><td><strong>$3,000–$5,000 per campus</strong></td><td>Everything in Schools, plus Entrepreneurship cohorts, a Pitch Day judging panel and live guest speakers</td></tr>
          <tr><td>Title I schools</td><td>Schools serving a high share of low-income students</td><td><strong>Free</strong></td><td>The full school package, paid for by a sponsor</td></tr>
          <tr><td>Add-on: live training</td><td>Any school or college</td><td><strong>$500–$1,000 per session</strong></td><td>Live virtual facilitator training for teachers or staff</td></tr>
        </tbody></table></div>
        <p class="note">One flat fee per school is easier to approve than per-student pricing.</p>
      </div>
    </section>
    <section class="section bg-mist" id="title-i">
      <div class="container split">
        <div><p class="eyebrow">Title I schools</p><h2>Free for the schools that need it most.</h2></div>
        <div class="soft">
          <p>Each sponsor covers the full license for one or more Title I schools for a year, about $1,000 per school. Sponsors are named on those schools' course pages and in our annual impact report.</p>
          <p>Title I schools can apply with the form below. Businesses and donors who want to sponsor a school can use it too.</p>
        </div>
      </div>
    </section>
    <section class="section" id="request">
      <div class="container"><span id="title-i-apply" class="anchor"></span><span id="sponsor" class="anchor"></span>
        <div class="section-head"><p class="eyebrow">Get started</p><h2>Request a license or apply.</h2><p class="soft" style="margin-top:10px">Send us a few details and we'll follow up with next steps. Submitting opens your email with everything filled in.</p></div>
        <form class="card req-form" id="req-form" data-to="{CONTACT}">
          <div class="fgrid">
            <div class="f full"><label for="r-type">I'm interested in</label>
              <select id="r-type" name="Request type" required>
                <option>School license</option><option>District license (5+ schools)</option><option>College or university license</option><option value="Title I school application">Title I school application (free)</option><option>Sponsoring a Title I school</option><option>Live training add-on</option>
              </select></div>
            <div class="f"><label for="r-name">Your name</label><input id="r-name" name="Name" autocomplete="name" required></div>
            <div class="f"><label for="r-role">Your role</label><input id="r-role" name="Role" placeholder="Principal, counselor, teacher…"></div>
            <div class="f"><label for="r-org">School, district, college or company</label><input id="r-org" name="Organization" autocomplete="organization" required></div>
            <div class="f"><label for="r-state">City and state</label><input id="r-state" name="Location"></div>
            <div class="f"><label for="r-grades">Grades or programs</label><input id="r-grades" name="Grades" placeholder="e.g. K–5, 9–12, first-year seminar"></div>
            <div class="f"><label for="r-size">Approximate number of students</label><input id="r-size" name="Students" inputmode="numeric"></div>
            <div class="f"><label for="r-email">Email</label><input id="r-email" name="Email" type="email" autocomplete="email" required></div>
            <div class="f"><label for="r-phone">Phone (optional)</label><input id="r-phone" name="Phone" type="tel" autocomplete="tel"></div>
            <div class="f full"><label for="r-msg">Anything else we should know?</label><textarea id="r-msg" name="Message" rows="4" placeholder="Courses you're most interested in, timing, questions…"></textarea></div>
          </div>
          <button type="submit" class="btn btn-accent self-start">Send request</button>
          <p class="small soft">Or email us directly at <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
        </form>
      </div>
    </section>
'''
    return head("Schools & Colleges", "Ava's Place school, district and college licenses, and free access for Title I schools.") + body + FOOT


(ROOT / "start.html").write_text(start_page())
(ROOT / "certificate.html").write_text(certificate_page())
(ROOT / "schools.html").write_text(schools_page())
print("Built start.html, certificate.html, schools.html")
