# Ava's Place Foundation — Website

Live at **https://avasplace.org** (GitHub Pages, `main` branch; also the-nextrep.github.io/avas-place-website).

A plain static site, no build step needed to publish. Open `index.html` in a browser to preview.

## Files

- `index.html` — homepage (hero marquee, resources, course tracks, tiers, access/pricing, Bella books, get involved)
- `courses.html` — course catalog (**generated**, see below)
- `course-*.html` — one full page per course (**generated**)
- `rep-card.html` — printable Rep Card (**generated**)
- `start.html` — Start learning free: suggested course paths by age (generated)
- `certificate.html` — printable completion certificate (generated)
- `schools.html` — school/district/college licenses, Title I, and the request form (generated; requests email the address in `CONTACT` in `tools/build_course_pages.py`)
- `naythan.html` — Naythan Mulugeta athlete fundraiser
- `styles.css` — all styling; brand colors and fonts are set at the top under `:root` (logo navy `#0B3A5C`, logo gold `#E0A93B`)
- `site.js` — mobile menu and the marquee pause button
- `images/` — logo (transparent `.webp`), Bella book covers, favicon, social share image
- `tools/` — small scripts that generate parts of the site

## Updating the courses

The catalog summaries live in `tools/build_courses.py`; the full course pages (sessions, tools, age adaptations, self-checks) come from `tools/courses.json`. Edit either, then run:

```
python3 tools/build_courses.py
```

## Adding photos to the hero marquee

Put photos in `images/marquee/`, named by audience: `youth-1.jpg`, `families-1.jpg`, `disability-1.jpg`, `athletes-1.jpg` (as many of each as you like), then run:

```
python3 tools/build_marquee.py
```

Audiences without photos use the illustrated scenes in `images/marquee/*.svg` (redraw them with `python3 tools/make_marquee_art.py`).

## Still to fill in

Search for `[` in `index.html` and `tools/courses.template.html`:

- Contact email, city, nonprofit status / EIN
- Donation link and Amazon links for the Bella books
- Founder story behind the name
- Local support directory, adaptive programs & partners, advocacy & benefits guides
- Newsletter form `action` URL (from your email provider)
