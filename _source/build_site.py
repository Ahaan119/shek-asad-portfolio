# -*- coding: utf-8 -*-
"""Generates the whole static site from cases.py. Run:  python3 _source/build_site.py
Output goes to the folder above this one (index.html, work.html, case/*.html)."""
import html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cases import CASES, STAGES, SYMPTOMS, BY_SLUG  # noqa: E402

NAME = "Shek Asad"
EMAIL = "ahaankhan119@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/shekh-asad-5267721b3/"
SITE_TITLE = "Shek Asad — Performance marketing for brands where the sale closes off the website"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800'
         '&family=Instrument+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">')

e = html.escape
TOTAL = len(CASES)
STAGE_NAME = {k: n for k, n, _ in STAGES}
SYM_NAME = {k: n for k, n, _ in SYMPTOMS}


def head(title, desc, root="", page=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#EFEAE0">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add('js')</script>
{FONTS}
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(root="", page=""):
    def cur(p):
        return ' aria-current="page"' if page == p else ""
    return f"""<header class="top"><div class="wrap">
  <a class="brand" href="{root}index.html" aria-label="{NAME}, home"><i>SA</i><span>{NAME}</span></a>
  <nav aria-label="Main"><ul>
    <li><a href="{root}work.html"{cur('work')}>Work</a></li>
    <li><a href="{root}index.html#about">About</a></li>
    <li><a href="{root}index.html#contact">Contact</a></li>
    <li><a class="btn" href="mailto:{EMAIL}">Let’s talk</a></li>
  </ul></nav>
</div></header>
"""


def footer(root=""):
    return f"""<footer><div class="wrap">
  <p>© 2026 {NAME}. Performance marketing, Delhi NCR.</p>
  <p><a href="mailto:{EMAIL}">{EMAIL}</a> <a href="{LINKEDIN}" rel="noopener">LinkedIn</a></p>
</div></footer>
<script src="{root}assets/app.js" defer></script>
</body>
</html>
"""


def mini_funnel(stages):
    items = "".join(
        f'<li class="{"on" if k in stages else ""}">{e(n)}</li>' for k, n, _ in STAGES)
    return f'<ul class="mini" aria-label="Funnel stages touched">{items}</ul>'


def dots(stages):
    d = "".join(f'<i class="{"on" if k in stages else ""}"></i>' for k, _, _ in STAGES)
    names = ", ".join(STAGE_NAME[s] for s in stages)
    return f'<span class="dots" role="img" aria-label="Stages: {e(names)}">{d}</span>'


def headline(c):
    v, l = c["results"][0]
    return v, l


# ---------------------------------------------------------------- home
def home():
    nums = [("₹5Cr+", "Ad spend managed"), ("30+", "Brands worked with"),
            ("100K+", "Qualified leads, one clinic"), ("10x", "Revenue growth, same clinic")]
    nums_html = "".join(f'<div data-reveal><div class="num">{e(n)}</div><div class="lab">{e(l)}</div></div>' for n, l in nums)

    stages_html = "".join(
        f'<li class="stage"><span class="node"></span><b>{e(n)}</b><small>{e(d)}</small></li>' for _, n, d in STAGES)

    tickets = "".join(
        f'<a class="ticket" href="work.html#sym-{k}" data-reveal><span class="k">Symptom {i+1:02d}</span>'
        f'<h3>{e(n)}</h3><p>{e(d)}</p><span class="go">See the cases →</span></a>'
        for i, (k, n, d) in enumerate(SYMPTOMS))

    feats = [c for c in CASES if c["featured"]]
    cards = ""
    for c in feats:
        v, l = headline(c)
        n = CASES.index(c) + 1
        cards += f"""<a class="jc" href="case/{c['slug']}.html" data-reveal>
  <div class="jc-top"><span>Job card № {n:02d}</span><span>{e(c['sector'])}</span></div>
  <hr class="perf">
  <div class="jc-body">
    <h3>{e(c['name'])}</h3>
    <div class="big">{e(v)}<small>{e(l)}</small></div>
    <p class="muted">{e(c['summary'])}</p>
    {dots(c['stages'])}
    <span class="more">Open the job card →</span>
  </div>
</a>"""

    off = [("niramaya-soul", "WhatsApp", "Leads qualified in chat before sales sees them."),
           ("noa-studios", "Instagram DM", "An automated first conversation filters serious clients."),
           ("lpu", "Phone call", "Call-only ads, measured by call quality."),
           ("gg-studio", "Boutique visit", "Tying ads to sales that close in store."),
           ("hotel-sunstar", "Booking", "A direct booking engine instead of static pages."),
           ("united-catering", "Event enquiry", "WhatsApp intent screening for catering leads.")]
    chans = "".join(
        f'<a class="chan" href="case/{s}.html" data-reveal><b>{e(t)}</b><span>{e(d)}</span><em>{e(BY_SLUG[s]["name"])} →</em></a>'
        for s, t, d in off)

    wall = "".join(f'<a href="case/{c["slug"]}.html">{e(c["name"].split(" (")[0])}</a>' for c in CASES)

    body = head(SITE_TITLE,
                "Performance marketer in Delhi NCR. ₹5Cr+ in Meta and Google ads across 30+ brands, from luxury couture to healthcare. I fix the whole funnel around the ad.",
                "", "home") + header("", "home") + f"""
<main id="main">
<section class="hero"><div class="wrap">
  <p class="eyebrow">Performance marketing · Delhi NCR · Open to roles and projects</p>
  <h1>I make paid ads profitable, from first click to <em>closed sale.</em></h1>
  <p class="lede">I run Meta and Google ads for premium and high-value brands, <b>where the sale closes on WhatsApp, a call or in a boutique, not only at checkout.</b> Over ₹5 crore managed across 30+ brands, and I work on everything around the ad that decides whether it pays back.</p>
  <div class="cta-row"><a class="btn" href="work.html">See the work</a><a class="btn ghost" href="#contact">Hiring? Let’s talk</a></div>
  <ol class="funnel" aria-label="The funnel I work on">{stages_html}</ol>
  <div class="nums">{nums_html}</div>
</div></section>

<section class="block" id="symptoms"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Start here</p><h2>What’s broken in your ad account?</h2>
  <p>Pick the symptom closest to yours. Every case is a real account I fixed, written up as a job card: the complaint, the diagnosis, the work and the road test.</p></div>
  <div class="tickets">{tickets}</div>
</div></section>

<section class="block" id="selected"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Selected work</p><h2>Three job cards</h2></div>
  <div class="cards">{cards}</div>
  <p style="margin-top:26px"><a class="btn ghost" href="work.html">All {TOTAL} campaigns in the ad account →</a></p>
</div></section>

<div class="band"><div class="wrap">
  <p class="eyebrow">The edge</p>
  <h2>Most ads end at a checkout. Mine often don’t.</h2>
  <p class="lead">Premium brands, clinics, colleges and hotels sell through WhatsApp, calls, boutiques and bookings. Count only what the pixel sees and you’ll cut the campaigns that are actually selling. I build the measurement and follow-up around how your customers really buy.</p>
  <div class="chans">{chans}</div>
</div></div>

<section class="block" id="wall"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Everyone I’ve worked on</p><h2>The client wall</h2></div>
  <div class="wall">{wall}</div>
</div></section>

<section class="block" id="about"><div class="wrap about">
  <div class="mono-card" aria-hidden="true"><div>S<span>A</span></div></div>
  <div>
    <p class="eyebrow">About</p>
    <h2 style="font-size:clamp(32px,5vw,52px);line-height:1;margin:10px 0 18px">Ads rarely fail alone.</h2>
    <p>I’m a performance marketer from Delhi NCR. For nearly four years I’ve run Meta and Google ads for luxury fashion, healthcare, education, hospitality and D2C brands. The pattern I keep finding: the ad is rarely the only problem. Tracking is broken, the page leaks, or nobody follows up on the lead.</p>
    <p>So I work the whole funnel with the ad at the centre. Most recently I was Digital Marketing Manager at GG Studio, a luxury couture house. Before that, nearly four years at AB Media, taking on everything from lead generation for clinics to app installs at crore-level spend.</p>
    <ul class="facts">
      <li><b>Based</b><span>Delhi NCR. Open to remote or hybrid, around Gurugram and Noida.</span></li>
      <li><b>Open to</b><span>Full-time performance or growth marketing roles, and project work.</span></li>
      <li><b>Works with</b><span>Meta Ads, Google Ads, GA4, GTM, Shopify, Zoho CRM, WhatsApp automation.</span></li>
      <li><b>Studying</b><span>MBA in Marketing, Jamia Hamdard University (2027).</span></li>
    </ul>
  </div>
</div></section>

<section class="block" id="contact"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Work with me</p><h2>Three ways to start</h2></div>
  <div class="offers">
    <div class="offer" data-reveal><h3>Hiring?</h3><p>I’m open to performance and growth marketing roles, remote or hybrid, around Gurugram and Noida.</p>
      <a class="btn" href="mailto:{EMAIL}?subject=Role%20at%20your%20company">Email me</a></div>
    <div class="offer" data-reveal><h3>Ad account review</h3><p>Share your account and I’ll tell you the biggest leaks in plain language: tracking, structure, creative and what happens after the click.</p>
      <a class="btn" href="mailto:{EMAIL}?subject=Ad%20account%20review">Ask for a review</a></div>
    <div class="offer" data-reveal><h3>Launch and scale</h3><p>For new e-commerce brands: website, SEO, conversion, automation and ads set up as one system, not five separate jobs.</p>
      <p class="chain">Site → SEO → CRO → Automation → Ads</p>
      <a class="btn" href="mailto:{EMAIL}?subject=Launch%20and%20scale">Talk about a launch</a></div>
  </div>
  <p class="note">Or find me on <a href="{LINKEDIN}" rel="noopener">LinkedIn</a>.</p>
</div></section>
</main>
""" + footer("")
    return body


# ---------------------------------------------------------------- work
def work():
    chips = '<button class="chip" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" data-filter="{k}" aria-pressed="false">{e(n)}</button>' for k, n, _ in SYMPTOMS)
    rows = ""
    for c in CASES:
        v, l = headline(c)
        rows += f"""<li data-sym="{' '.join(c['problems'])}"><a href="case/{c['slug']}.html">
  <div class="c-id"><div class="cid">{e(c['cid'])}</div></div>
  <div class="c-nm"><div class="nm">{e(c['name'])}</div><div class="sub">{e(c['sector'])}</div></div>
  <div class="c-stages">{dots(c['stages'])}</div>
  <div class="c-res"><div class="res">{e(v)} <span class="sub">{e(l)}</span></div></div>
  <div class="c-st"><span class="pill">{e(c['status'])}</span></div>
</a></li>"""
    return head("Work — Shek Asad", "Every engagement as a campaign row in an ad account. Filter by the problem you have and open the job card.",
                "", "work") + header("", "work") + f"""
<main id="main"><div class="wrap">
<div class="page-head"><p class="eyebrow">The ad account</p>
  <h1>{TOTAL} campaigns. Click any row.</h1>
  <p>Each engagement is written up as a job card: the complaint, the diagnosis, the work done and the road test. Filter by the problem you have.</p></div>
<div class="filters" role="group" aria-label="Filter by problem">{chips}</div>
<p class="count" id="count" aria-live="polite">Showing {TOTAL} of {TOTAL} campaigns</p>
<ul class="acct">
  <li class="acct-h" aria-hidden="true"><div>Campaign ID</div><div>Client</div><div>Stages</div><div>Headline result</div><div>Status</div></li>
  {rows}
</ul>
<p class="note">Dots show which funnel stages each project touched: attract, land, convert, measure, compound. Figures come from platform and client reporting during each engagement. Results are mine to report; client revenue is not, so rupee revenue is left out where it wasn’t already public.</p>
</div></main>
""" + footer("")


# ---------------------------------------------------------------- case
def case_page(i, c):
    prev_c = CASES[i - 1] if i > 0 else None
    next_c = CASES[i + 1] if i < TOTAL - 1 else None
    tiles = "".join(
        f'<div><div class="num">{e(v)}</div><div class="lab">{e(l)}</div></div>' for v, l in c["results"])
    diag = "".join(f"<li>{e(x)}</li>" for x in c["diagnosis"])
    work_l = "".join(f"<li>{e(x)}</li>" for x in c["work"])
    syms = ", ".join(SYM_NAME[p] for p in c["problems"])
    period = f" · {e(c['period'])}" if c["period"] else ""
    where = "GG Studio" if c["slug"] == "gg-studio" else "AB Media"
    pn_prev = (f'<a href="{prev_c["slug"]}.html"><small>← Previous</small><b>{e(prev_c["name"].split(" (")[0])}</b></a>'
               if prev_c else '<a href="../work.html"><small>← Back</small><b>All campaigns</b></a>')
    pn_next = (f'<a href="{next_c["slug"]}.html"><small>Next →</small><b>{e(next_c["name"].split(" (")[0])}</b></a>'
               if next_c else '<a href="../work.html"><small>Next →</small><b>All campaigns</b></a>')
    desc = f"{c['name']}: {c['summary']} " + " · ".join(f"{v} {l}" for v, l in c["results"][:2])
    return head(f"{c['name']} — {c['title']} | Shek Asad", desc, "../", "work") + header("../", "work") + f"""
<main id="main"><div class="wrap">
<p class="crumb"><a href="../work.html">Work</a> / {e(c['name'])}</p>
<div class="case-h">
  <p class="eyebrow">{e(c['sector'])}</p>
  <h1>{e(c['title'])}</h1>
  <div class="meta"><span>Client: {e(c['name'])}</span><span>Status: {e(c['status'])}</span><span>Problem: {e(syms)}</span></div>
</div>

<article class="sheet">
  <div class="sheet-top"><span>Job card № {i+1:02d} / {TOTAL}</span><span>{where}{period}</span></div>
  <div class="sheet-fields">
    <div><div class="fl">Client</div><div class="fv">{e(c['name'])}</div></div>
    <div><div class="fl">Category</div><div class="fv">{e(c['sector'])}</div></div>
    <div><div class="fl">The sale closes via</div><div class="fv">{e(c['sale'])}</div></div>
  </div>
  <hr class="perf" style="margin:0">
  <div class="sheet-body">
    <div>
      <h2>The complaint</h2><p class="txt">{e(c['complaint'])}</p>
      <h2>Diagnosis</h2><ul>{diag}</ul>
    </div>
    <div>
      <h2>Work done</h2><ul>{work_l}</ul>
    </div>
  </div>
  <hr class="perf" style="margin:0">
  <div class="sheet-funnel"><span class="fl" style="margin:0">Funnel stages touched</span>{mini_funnel(c['stages'])}</div>
  <hr class="perf" style="margin:0">
  <div class="road">
    <h2>Road test</h2>
    <span class="stamp">Road<br>tested</span>
    <div class="tiles">{tiles}</div>
  </div>
</article>

<div class="lesson"><small>What it taught me</small>{e(c['lesson'])}</div>

<nav class="pn" aria-label="More case studies">{pn_prev}{pn_next}</nav>

<div class="talk"><h2>Got a similar problem? Let’s look at it together.</h2>
  <a class="btn" href="mailto:{EMAIL}?subject={e(c['name'].split(' (')[0])}%20style%20problem">Email me</a></div>
</div></main>
""" + footer("../")


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    write("index.html", home())
    write("work.html", work())
    for i, c in enumerate(CASES):
        write(f"case/{c['slug']}.html", case_page(i, c))
    print(f"built index.html, work.html and {TOTAL} case pages -> {OUT}")
