"""Builds courses.html from the course data below.

Edit the COURSES list, then run:  python3 tools/build_courses.py
"""
import pathlib, html, re, runpy

ROOT = pathlib.Path(__file__).resolve().parent.parent
e = html.escape

TRACKS = [
    ("track-yourself", "Knowing yourself", "#E0A93B", [10, 15, 11, 21]),
    ("track-others", "Working with others", "#2E8B6E", [16, 18, 2, 1, 3]),
    ("track-manage", "Managing yourself", "#0B3A5C", [4, 5, 6, 7]),
    ("track-college", "College & career readiness", "#A8452F", [19, 20, 8, 9]),
    ("track-ready", "Real-world readiness", "#6B4FA0", [14, 12, 17, 13]),
]

STD = "4 sessions · all four learner tiers"

COURSES = {
    1: dict(
        title="Handling Uncertainty & Ambiguity", meta=STD,
        idea="When there is no script, you can still take a first step. Learners practice breaking open-ended problems into what I know, what I don't, and what I can try.",
        tool=("Know / Don't Know / Try card", "Three boxes learners fill in whenever a task feels unclear."),
        sessions=[("No Instructions Included", "Fill the Know / Don't Know / Try card for a task with missing directions, then attempt it."),
                  ("Good Questions Beat Guesses", "Turn \"I don't get it\" into one specific question."),
                  ("Small Bets", "Try three quick versions of a solution and keep the one that works best."),
                  ("Comfortable With Not Knowing", "A group challenge whose rules change halfway through, then a debrief on how they adapted.")],
        tiers=[("Sprouts", "\"Mystery Box\" clue game and a picture-based Try card."),
               ("Builders", "A deliberately vague group project brief; teams write their own success criteria."),
               ("Launchers", "\"Your manager quits mid-shift\": map the options and pick a first move."),
               ("Leaders", "Work a real ambiguous assignment, draft questions for the professor, submit an early draft.")],
        rep="Pick one unclear task this week. Fill the card before starting, then note what actually happened."),
    2: dict(
        title="Conflict Resolution & Compromise", meta=STD,
        idea="Disagreement is normal; how you handle it is a skill. Learners separate the problem from the person and look for the need underneath each position.",
        tool=("PAUSE", "Pause and breathe · Ask what happened from their side · Understand the need behind it · Share your side with an \"I\" statement · Explore options that meet both needs."),
        sessions=[("Same Story, Two Sides", "Rewrite a blame sentence as an \"I\" statement."),
                  ("Listen to Understand", "Repeat back what you heard before replying."),
                  ("Needs, Not Positions", "Find the need behind three common arguments."),
                  ("Find the Middle", "Role-play a conflict start to finish using PAUSE.")],
        tiers=[("Sprouts", "Puppet and picture-card role-plays about sharing and taking turns."),
               ("Builders", "Group-chat and lunch-table scenarios, including online misunderstandings."),
               ("Launchers", "Team projects, curfews and playing time; negotiate a written compromise."),
               ("Leaders", "Draft a roommate agreement, plus a coworker scenario.")],
        rep="Use PAUSE in one real disagreement. Note which step was hardest."),
    3: dict(
        title="Absorbing & Applying Feedback", meta=STD,
        idea="Feedback is about the work, not your worth. Learners practice hearing it, sorting it and using it.",
        tool=("Hear it, Sort it, Use it", "Hear it without defending. Sort each comment into use now, ask about or set aside. Use one piece right away."),
        sessions=[("Work ≠ Worth", "Practice \"The feedback is about ___, not about me.\""),
                  ("The Sting Is Normal", "Receive practice feedback and respond only with \"Thanks, tell me more.\""),
                  ("Sort the Pile", "Sort mixed feedback into Use / Ask / Set Aside."),
                  ("Revise and Resubmit", "Revise your own work using one comment; share the before and after.")],
        tiers=[("Sprouts", "\"Two Stars and a Wish\" drawing critique."),
               ("Builders", "Peer review with sentence starters."),
               ("Launchers", "A revision plan for an essay or lab report, plus a mock interview debrief."),
               ("Leaders", "Bring a real graded paper; draft a professional reply and a revision plan.")],
        rep="Ask someone for feedback on one thing you made this week. Use one comment and log the result."),
    4: dict(
        title="Time Management & Prioritizing", meta=STD,
        idea="You can't do everything, so choose on purpose. Learners sort tasks by importance, protect focus time and plan around their real energy.",
        tool=("Big Rocks & the Energy Ledger", "Sort tasks into Must / Should / Could, and check school, social and physical energy before planning."),
        sessions=[("Big Rocks First", "Sort a week of real tasks into Must / Should / Could."),
                  ("Where Did the Time Go?", "Time-log one afternoon and compare guesses to reality."),
                  ("The Phone Problem", "A phone-away focus sprint, then compare output."),
                  ("Plan Backward", "Break one assignment into dated steps on a calendar.")],
        tiers=[("Sprouts", "Picture schedules, first-then boards and sand-timer races."),
               ("Builders", "Planner setup and a 10-minute focus sprint."),
               ("Launchers", "Balance school, work, sports and family with the Energy Ledger."),
               ("Leaders", "Map every syllabus deadline onto one semester calendar.")],
        rep="Run one week with a Big Rocks list each morning. Count how many Musts got done."),
    5: dict(
        title="Self-Direction & Initiative", meta=STD,
        idea="Nobody is going to tell you every step, and that's your chance. Learners set their own goals, start without being told and hold themselves accountable.",
        tool=("The Own-It Loop", "Choose a goal · Set the first step · Start before you feel ready · Check in with yourself · Adjust."),
        sessions=[("Waiting vs. Starting", "List three things you usually wait to be told to do."),
                  ("My Why", "Write a personal \"why\" for one goal."),
                  ("The 2-Minute Start", "Do only the first two minutes of a stalled task."),
                  ("Be Your Own Coach", "Set up a self-check-in routine and an accountability buddy.")],
        tiers=[("Sprouts", "\"Helper who notices\" game and a sticker chart for self-started jobs."),
               ("Builders", "A two-week choose-your-own mini project with a self-made checklist."),
               ("Launchers", "A passion project or application plan with self-set milestones."),
               ("Leaders", "Design a personal semester system with weekly accountability partners.")],
        rep="Start one thing this week before anyone reminds you. Log when you started and what happened."),
    6: dict(
        title="Resilience & Perseverance", meta=STD,
        idea="A setback is data, not a verdict. Learners practice bouncing back so a bad grade or failed try becomes the next attempt, not the end.",
        tool=("The Reset Rep", "Feel it (name the emotion) · Face it (what actually happened?) · Fix one thing · Try again."),
        sessions=[("Everyone Misses", "Share or privately write about one failure and what came after."),
                  ("Name It to Tame It", "Practice a 60-second reset: breathe, name the feeling, one next step."),
                  ("Autopsy, Not Attack", "Analyze a sample failed test: what went wrong and one fix."),
                  ("Attempt Two", "A deliberately hard challenge, logging each attempt and what changed.")],
        tiers=[("Sprouts", "The \"yet\" power word and multi-try building games."),
               ("Builders", "\"Friction Reps\" that get a little harder each round."),
               ("Launchers", "A post-test recovery plan and a rejection role-play."),
               ("Leaders", "A first-semester setback plan, including campus support resources.")],
        rep="Next time something goes wrong, run the Reset Rep and log your second attempt."),
    7: dict(
        title="Critical Thinking & Problem-Solving", meta=STD,
        idea="Knowing facts is step one; using them on a messy real problem is the goal. Learners practice defining problems, checking claims and testing solutions.",
        tool=("IDEAL", "Identify the problem · Define what solved looks like · Explore options and evidence · Act on the best one · Look back and learn."),
        sessions=[("What's the Real Problem?", "Ask \"why?\" five times on a real problem."),
                  ("Check the Claim", "Who says it, what's the evidence, what's missing."),
                  ("Use What You Know", "Solve a real-world problem with a school concept."),
                  ("Solve It Together", "Teams work through IDEAL and pitch a solution in two minutes.")],
        tiers=[("Sprouts", "Detective mysteries and fix-it challenges."),
               ("Builders", "Spot the misleading post; plan a fundraiser with a budget."),
               ("Launchers", "A community problem project with a proposal to a real decision-maker."),
               ("Leaders", "Case-study teams and a written recommendation memo.")],
        rep="Pick one real problem you face. Work it through IDEAL on paper and try your solution."),
    8: dict(
        title="SAT Prep", meta="Grades 10–12 · 6 self-paced modules, about 60–90 minutes each",
        idea="The SAT rewards calm pacing and fixing repeat mistakes more than cramming. This course applies the skills from Courses 1–7 to one high-stakes test on the road to college.",
        tool=("The Error Log", "For every missed question: topic · why I missed it · the fix · retest date."),
        sessions=[("Know the Test", "A timed diagnostic module in the Bluebook app; start the Error Log."),
                  ("Reading & Writing Strategy", "Timed practice; log misses by type."),
                  ("Math Strategy + Desmos", "Timed practice using the built-in calculator where it saves time."),
                  ("Pacing Per Module", "Flag, skip and return across two timed modules."),
                  ("Test-Day Nerves", "A full practice test under real conditions, with the Reset Rep."),
                  ("Personal Study Plan", "Build a 6–8 week plan from your top three mistake types.")],
        tiers=[],
        extra="Uses the free official practice tests in Bluebook and Official Digital SAT Prep on Khan Academy. Families pay nothing extra.",
        rep="Pick a target test date and complete two weeks of your study plan."),
    9: dict(
        title="Entrepreneurship", meta="College & first-year adults · 6 self-paced modules",
        idea="Take a small idea from problem to first paying customer in six weeks, using uncertainty, feedback, resilience and problem-solving as working tools.",
        tool=("The Build–Test–Learn Board", "One page per week: what we believe · what we tested · what customers said or did · what we'll change. A mentor reviews it."),
        sessions=[("Problems Worth Solving", "List ten problems you or classmates face; pick one."),
                  ("Talk to Customers", "Interview five potential customers. No pitching."),
                  ("The Smallest Test", "Design a test for under $50."),
                  ("Money Basics", "Price, cost, margin and break-even."),
                  ("Pivot or Persist", "Keep, change or drop the idea based on what you learned."),
                  ("Pitch Day", "Record a 90-second pitch; a panel of founders sends written feedback.")],
        tiers=[],
        extra="Pick a campus service, a digital product, student-made goods or a social-impact venture.",
        rep="Make one real sale, sign-up or pre-order, and log what it took."),
    10: dict(
        title="Confidence & Self-Worth", meta=STD,
        idea="Confidence is built through reps, not born. Learners separate who they are from grades, likes and wins, and grow confidence through small, repeated acts of courage.",
        tool=("The Evidence File", "A running list of proof: things I tried, things I did while nervous, times I kept going."),
        sessions=[("I Am More Than a Score", "Write five \"I am…\" statements unrelated to grades, looks or wins."),
                  ("The Inner Critic", "Rewrite harsh self-talk the way a coach would say it."),
                  ("Brave Reps", "Pick one small brave act and do it this week."),
                  ("Speak Up", "Give a short talk on something you care about.")],
        tiers=[("Sprouts", "An \"I Can\" jar and strong-voice show-and-tell."),
               ("Builders", "A real-vs.-edited social media check and a confidence playlist."),
               ("Launchers", "An identity map separate from stats, GPA or followers."),
               ("Leaders", "An imposter-feeling lab and a personal introduction for networking.")],
        rep="Complete three brave reps this week and add each one to your Evidence File."),
    11: dict(
        title="Peer Pressure & Independent Choices", meta=STD,
        idea="Fitting in shouldn't cost you who you are. Learners spot pressure in person and online, practice saying no without losing face, and make choices they can own.",
        tool=("The STOP check", "Spot the pressure · Think ahead · Options: name at least two · Pick and own it."),
        sessions=[("Spot the Pressure", "Sort ten scenarios by type of pressure."),
                  ("The Cool No", "Practice five ways to say no."),
                  ("Your Crew", "Map who makes good choices easier and who makes them harder."),
                  ("Stand on Your Own", "Role-play a group scenario using STOP.")],
        tiers=[("Sprouts", "Puppet scenes and a strong \"No thanks\" voice."),
               ("Builders", "Group-chat pressure, online trends and an exit line with a parent."),
               ("Launchers", "Plan ahead for three real situations expected this year."),
               ("Leaders", "A personal values list and one boundary to hold this semester.")],
        rep="Use STOP once this week when you feel pressure. Log what you chose and why."),
    12: dict(
        title="Online Safety & Scam Smarts", meta=STD,
        idea="Scammers count on panic and shame. Learners practice slowing down, spotting red flags and knowing exactly what to do and who to tell.",
        tool=("The 3 Rs", "Recognize the red flags · Refuse to send, pay or click · Report it to a trusted adult and the platform."),
        sessions=[("Too Good to Be True", "Sort realistic messages into safe, suspicious or scam."),
                  ("Who's Really There?", "Check a profile for signs it's fake."),
                  ("Never Pay, Never Panic", "Role-play the first ten minutes after a threat."),
                  ("Your Safety Team", "Build a no-shame family safety plan.")],
        tiers=[("Sprouts", "\"Tricky people online\" picture cards and always telling a grown-up."),
               ("Builders", "Game-chat scams, fake giveaways and privacy settings."),
               ("Launchers", "Sextortion warning signs, fake jobs and how to report."),
               ("Leaders", "Rental, job and payment-app scams; protecting your identity.")],
        rep="Do a privacy checkup on two apps and share your safety plan with a trusted adult."),
    13: dict(
        title="NIL & Recruiting", meta="Grades 9–12 & college athletes, with a parent track · 6 self-paced modules",
        idea="Your name, image and likeness can open doors, or close them if you sign the wrong thing. Learn the rules, the money and the red flags before the first offer.",
        tool=("The Deal Check", "Is it allowed? · What do I give and get? · How am I paid and what will I owe in taxes? · Who reviewed it?"),
        sessions=[("Know Your Rules", "Find your state's NIL policy and the rules that apply to you."),
                  ("Your Brand, Your Story", "Audit your social media and write a brand statement."),
                  ("Reading the Deal", "Mark up a sample NIL agreement."),
                  ("Money & Taxes", "Set aside for taxes and start an income tracker."),
                  ("Recruiting & NIL Together", "Build a recruiting plan that fits your NIL goals."),
                  ("Pitch Day", "Record a pitch to a local business.")],
        tiers=[],
        extra="Education, not legal or tax advice. Rules differ by state, so check with your state athletic association or compliance office.",
        rep="Run one real or sample offer through the Deal Check with a parent or mentor."),
    14: dict(
        title="Real Life Money", meta=STD,
        idea="A first paycheck, a first credit card, a first doctor's bill. Practice the money skills grads say they most wish they'd been taught.",
        tool=("The Money Map", "What comes in · what goes out · what you owe · what protects you."),
        sessions=[("Your First Paycheck", "Read a pay stub: gross, net, taxes, deductions."),
                  ("Filing Your Taxes", "Walk through a simple sample return."),
                  ("How Credit Works", "See how a credit score changes the cost of a loan."),
                  ("Health Insurance Without Panic", "Read an insurance card and benefits statement.")],
        tiers=[("Sprouts", "Needs vs. wants and a save/spend/share game."),
               ("Builders", "First earnings, a simple budget, debit vs. credit."),
               ("Launchers", "A first paycheck, W-4, tax return and credit basics."),
               ("Leaders", "Filing alone, student loans and choosing a health plan.")],
        rep="Build your own Money Map for a real or sample month."),
    15: dict(
        title="Emotional Intelligence", meta=STD,
        idea="Emotions are information. Build a bigger feelings vocabulary, read what others feel, and manage big emotions so you choose how to respond.",
        tool=("The 3 Ns", "Name it · Notice it · Navigate it."),
        sessions=[("More Than Mad, Sad, Glad", "Build a feelings ladder from mild to intense."),
                  ("Read the Room", "Read faces and body language, then check by asking."),
                  ("The Pause Button", "Try three reset moves and pick your go-to."),
                  ("Feelings in Relationships", "Share a feeling with \"I feel… when… I need…\"")],
        tiers=[("Sprouts", "Feelings-face cards and a feelings thermometer."),
               ("Builders", "Reading tone in texts and a calm-down plan."),
               ("Launchers", "Emotions under pressure and empathy in conflict."),
               ("Leaders", "Emotional intelligence at work and in leadership.")],
        rep="Check in with the 3 Ns three times a day for a week."),
    16: dict(
        title="Bullying: Stand Strong, Stand Up", meta=STD,
        idea="No one deserves to be bullied or has to face it alone. Tell bullying apart from conflict, know what to do if it happens to you, and step in safely for others.",
        tool=("The 4 Upstander Moves", "Notice it · Name it · Support the person targeted · Report it."),
        sessions=[("Bullying or Conflict?", "Sort scenarios: conflict, a mean moment or bullying."),
                  ("If It's Happening to You", "Practice a confident response and how to tell an adult."),
                  ("From Bystander to Upstander", "Role-play the 4 Upstander Moves."),
                  ("Online and Offline", "Screenshot, block, report and tell.")],
        tiers=[("Sprouts", "Puppet scenes, a strong voice and telling a grown-up."),
               ("Builders", "Group chats, rumors and exclusion."),
               ("Launchers", "Cyberbullying, hazing and supporting a friend."),
               ("Leaders", "Hazing, harassment and reporting channels.")],
        rep="Make one upstander move this week and log it."),
}


def from_json(n):
    import json as _j
    c = _j.loads((ROOT / "tools" / "courses.json").read_text())[str(n)]
    name, _, rest = (c["tool"] or "").partition(". ")
    return dict(title=c["heading"], meta=STD, idea=c["idea"], tool=(name[0].upper() + name[1:], rest),
                sessions=[(x["title"], x["rep"][0].upper() + x["rep"][1:] + ".") for x in c["sessions"]],
                tiers=[(t["tier"], t["text"]) for t in c["tiers"]], rep=c["rep"])


def course_html(n, c, color):
    s = [f'<article class="course" id="c{n}">',
         f'<div class="course-head"><h3>{e(c["title"])}</h3><span class="course-meta">{e(c["meta"])}</span></div>',
         f'<p class="big-idea">{e(c["idea"])}</p>',
         f'<p class="tool"><strong>Core tool: {e(c["tool"][0])}.</strong> {e(c["tool"][1])}</p>',
         '<ol class="sessions">']
    for i, (t, w) in enumerate(c["sessions"], 1):
        label = "Module" if len(c["sessions"]) == 6 else "Session"
        s.append(f'<li><span class="num">{label} {i}</span><span class="ttl">{e(t)}</span><span class="what">{e(w)}</span></li>')
    s.append('</ol>')
    if c.get("extra"):
        s.append(f'<p class="soft" style="margin-bottom:16px">{e(c["extra"])}</p>')
    if c["tiers"]:
        s.append('<details class="by-age"><summary>How it adapts by age</summary><dl>')
        for t, d in c["tiers"]:
            s.append(f'<dt>{e(t)}</dt><dd>{e(d)}</dd>')
        s.append('</dl></details>')
    s.append(f'<p class="rw-rep"><strong>Real-World Rep:</strong> {e(c["rep"])}</p>')
    s.append(f'<a class="btn btn-primary self-start open-course" href="{course_slug(n)}">Open the course</a>')
    s.append('</article>')
    return "\n".join(s)


def page():
    toc = "".join(f'<a href="#{tid}">{e(name)}</a>' for tid, name, _, _ in TRACKS)
    sections = []
    for i, (tid, name, color, nums) in enumerate(TRACKS):
        bg = " bg-mist" if i % 2 else ""
        body = "\n".join(course_html(n, COURSES.get(n) or from_json(n), color) for n in nums)
        sections.append(f'''
    <section class="track-section{bg}" id="{tid}">
      <div class="container">
        <h2><span class="track-dot" style="background:{color};width:18px;height:18px"></span>{e(name)}</h2>
{body}
      </div>
    </section>''')
    return TEMPLATE.replace("{{TOC}}", toc).replace("{{SECTIONS}}", "".join(sections))


def course_slug(n):
    t = {8: "SAT Prep", 9: "Entrepreneurship"}.get(n, (COURSES.get(n) or from_json(n))["title"])
    return "course-" + re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") + ".html"


TEMPLATE = (ROOT / "tools" / "courses.template.html").read_text()
(ROOT / "courses.html").write_text(page())
print("courses.html built.")
runpy.run_path(str(ROOT / "tools" / "build_course_pages.py"))
