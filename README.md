# Shek Asad: portfolio site

A static site (no framework, no build step needed to view it). Open `index.html` in a browser to see it.

## Structure
- `index.html`: home (hero, funnel, "What's broken?" picker, selected work, the offline-sale edge, client wall, about, work with me)
- `work.html`: the "ad account" table of every campaign, filterable by problem
- `case/*.html`: one job card per client (15 so far)
- `assets/`: style.css, app.js, favicon
- `_source/cases.py`: **all case-study content lives here**. `_source/build_site.py` regenerates every page from it.

## Edit or add a case
1. Open `_source/cases.py`, copy any block in `CASES`, and change the text and numbers.
2. Run `python3 _source/build_site.py`
3. Refresh the browser. The work table, home page links and previous/next buttons update on their own.

Change the email, LinkedIn link or site title at the top of `_source/build_site.py`.

## Put it online (free)
**GitHub Pages:** create a repo (e.g. `shek-asad-portfolio`) under your personal GitHub, upload this folder's contents, then Settings → Pages → Deploy from branch → `main` / root. The link will be `https://<your-username>.github.io/shek-asad-portfolio/`. All links in the site are relative, so it works in a sub-folder.

**Own domain (optional):** buy one (about ₹1,000 a year), then Settings → Pages → Custom domain.

## Before publishing
- Replace the "Portrait goes here" block in the About section with a photo (`.mono-card` in `assets/style.css`).
- Check each number against your own records. Everything on the site comes from client or platform reporting at the time.
- Keep GG Studio to ratios and scope, with no rupee spend or revenue.
