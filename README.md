# Ava's Place Foundation — Website

Live at **https://the-nextrep.github.io/avas-place-website/** (GitHub Pages, `main` branch).

A plain static site, no build step needed to publish. Open `index.html` in a browser to preview.

## Files

- `index.html` — homepage (hero marquee, resources, course tracks, tiers, access/pricing, Bella books, get involved)
- `courses.html` — full course catalog (**generated**, see below)
- `styles.css` — all styling; brand colors and fonts are set at the top under `:root` (logo navy `#0B3A5C`, logo gold `#E0A93B`)
- `site.js` — mobile menu and the marquee pause button
- `images/` — logo (transparent `.webp`), Bella book covers, favicon, social share image
- `tools/` — small scripts that generate parts of the site

## Updating the course catalog

Course content lives in `tools/build_courses.py`. Edit it, then run:

```
python3 tools/build_courses.py
```

## Adding photos to the hero marquee

Put photos in `images/marquee/`, named by audience: `youth-1.jpg`, `families-1.jpg`, `disability-1.jpg`, `athletes-1.jpg` (as many of each as you like), then run:

```
python3 tools/build_marquee.py
```

Audiences without photos show branded tiles.

## Still to fill in

Search for `[` in `index.html` and `tools/courses.template.html`:

- Contact email, city, nonprofit status / EIN
- Donation link and Amazon links for the Bella books
- Founder story behind the name
- Local support directory, adaptive programs & partners, advocacy & benefits guides
- Newsletter form `action` URL (from your email provider)
