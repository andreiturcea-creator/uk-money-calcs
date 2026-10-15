# Shared design system, added 15 Oct 2026. Runs after monetise.build() and before agent_ready.build().
# One stylesheet with a per-site accent, an SVG logo and favicon per site, a proper header and nav,
# a hero on each home page, card grids and scrollable tables. No web fonts, no trackers, no frameworks.
import os, re, html
SITES = {
 "uk-money-calcs": dict(name="UK Money Calcs", glyph="£", accent="#0f766e", accent_dark="#2dd4bf", soft="#e6f4f1", soft_dark="#0f2a27",
    tagline="Free UK tax and money calculators",
    nav=[("index.html#calculators", "Calculators"), ("take-home-pay.html", "Take-home pay"), ("self-employed-tax-calculator.html", "Self-employed"), ("income-tax-bands-2026-27.html", "2026/27 rates")],
    cta=("https://kit.andreiturcea.com/", "Sole trader guides")),
 "uk-freelancer-kit": dict(name="UK Freelancer Kit", glyph="K", accent="#4338ca", accent_dark="#a5b4fc", soft="#eef0fd", soft_dark="#1c1f3d",
    tagline="Guides and templates for UK sole traders",
    nav=[("index.html#free-guides", "Guides"), ("guide-mtd.html", "MTD"), ("guide-self-assessment-deadlines.html", "Deadlines"), ("guide-allowable-expenses.html", "Expenses")],
    cta=("https://turceapaul.gumroad.com/l/bmykeg", "Get the kit (£9)")),
 "selfhost-ai-dir": dict(name="SelfHostAI", glyph="AI", accent="#7c3aed", accent_dark="#c4b5fd", soft="#f3eefe", soft_dark="#251a3d",
    tagline="Open-source AI you can run yourself",
    nav=[("index.html#directory", "Directory"), ("best-self-hosted-chatgpt-alternatives.html", "Guides"), ("cat-llm-runtime.html", "Runtimes"), ("cat-chat-ui.html", "Chat UIs")],
    cta=("advertise.html", "Advertise")),
}

CSS = """/* Shared design system. Accent colours are set per site below. */
:root{--accent:%(accent)s;--accent-soft:%(soft)s;--bg:#ffffff;--bg-alt:#f6f7f9;--text:#16181d;--muted:#5b6170;--line:#e3e6eb;--card:#ffffff;
--warn-bg:#fff8eb;--warn-line:#f2c46d;--radius:14px;--shadow:0 1px 2px rgba(16,24,40,.05),0 4px 16px rgba(16,24,40,.06);
--font:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color-scheme:light dark}
@media (prefers-color-scheme:dark){:root{--accent:%(accent_dark)s;--accent-soft:%(soft_dark)s;--bg:#0f1115;--bg-alt:#161920;--text:#e8eaef;--muted:#a3a9b6;--line:#2a2f3a;--card:#161920;
--warn-bg:#2a2112;--warn-line:#8a6a2c;--shadow:0 1px 2px rgba(0,0,0,.4)}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%;scroll-padding-top:80px}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:1.0625rem;line-height:1.65;text-rendering:optimizeLegibility}
a{color:var(--accent);text-underline-offset:.18em;text-decoration-thickness:1px}a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px;border-radius:4px}
.skip{position:absolute;left:-999px;top:8px;background:var(--accent);color:#fff;padding:8px 14px;border-radius:8px;z-index:20}.skip:focus{left:8px}
.wrap,main,footer{width:100%%;max-width:880px;margin:0 auto;padding-left:20px;padding-right:20px}
/* header */
.site-header{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.site-header .wrap{max-width:1080px;display:flex;align-items:center;gap:16px;min-height:60px;flex-wrap:wrap;padding-top:8px;padding-bottom:8px}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:700;letter-spacing:-.01em;font-size:1.05rem}
.brand img{display:block;border-radius:9px}
.site-nav{display:flex;gap:4px;margin-left:auto;overflow-x:auto;scrollbar-width:none;max-width:100%%}
.site-nav a{color:var(--muted);text-decoration:none;padding:6px 10px;border-radius:8px;font-size:.95rem;white-space:nowrap}
.site-nav a:hover{color:var(--text);background:var(--bg-alt)}
.site-nav a.btn-nav{background:var(--accent);color:#fff;font-weight:600}
@media (prefers-color-scheme:dark){.site-nav a.btn-nav,.btn,button{color:#0f1115!important}}
@media (max-width:640px){.site-nav{margin-left:0;width:100%%;order:3}}
/* main typography */
main{padding-top:28px;padding-bottom:24px}
h1,h2,h3{line-height:1.25;letter-spacing:-.015em;color:var(--text)}
h1{font-size:clamp(1.75rem,4.5vw,2.5rem);margin:.2em 0 .5em;font-weight:800}
h2{font-size:clamp(1.3rem,3vw,1.6rem);margin:1.8em 0 .6em}h3{font-size:1.15rem;margin:1.4em 0 .4em}
p,ul,ol{margin:0 0 1em}li{margin:.25em 0}
code{font-family:var(--mono);font-size:.9em;background:var(--bg-alt);padding:.1em .35em;border-radius:5px}
.answer{font-size:1.1rem;background:var(--accent-soft);border-radius:var(--radius);padding:14px 18px;border:1px solid color-mix(in srgb,var(--accent) 25%%,transparent)}
#last-updated{color:var(--muted)!important;font-size:.85rem!important}
.small{font-size:.85rem;color:var(--muted)}
.note{background:var(--bg-alt);border-left:4px solid var(--accent);padding:10px 14px;border-radius:0 10px 10px 0;font-size:.92rem}
/* hero */
.hero{margin:8px 0 28px;padding:36px 28px;border-radius:20px;background:linear-gradient(135deg,var(--accent-soft),var(--bg-alt));border:1px solid var(--line)}
.hero h1{margin-top:0}.hero p{font-size:1.15rem;color:var(--muted);max-width:60ch}
.hero .eyebrow{display:inline-block;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);margin-bottom:8px}
@media (max-width:640px){.hero{padding:24px 18px}}
/* cards */
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;margin:14px 0;box-shadow:var(--shadow)}
.card>b:first-child,.card>a:first-child b{font-size:1.02rem}
.grid,#l{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:14px 0}
.grid .card,#l .card{margin:0;transition:border-color .15s,transform .15s}
.grid .card:hover,#l .card:hover{border-color:var(--accent);transform:translateY(-2px)}
.grid .card a,#l .card b a{text-decoration:none}
.sp{background:var(--warn-bg);border:1px solid var(--warn-line);box-shadow:none}
.kit-cta{background:var(--accent-soft);border:1px solid color-mix(in srgb,var(--accent) 35%%,transparent);border-left:5px solid var(--accent)}
.kit-cta a:last-child{display:inline-block;margin-top:8px;background:var(--accent);color:#fff;padding:7px 14px;border-radius:9px;text-decoration:none;font-weight:600}
@media (prefers-color-scheme:dark){.kit-cta a:last-child{color:#0f1115}}
.tag{display:inline-block;background:var(--accent-soft);color:var(--text);border-radius:999px;padding:3px 10px;margin:3px 4px 3px 0;font-size:.82rem;text-decoration:none;border:1px solid var(--line)}
a.tag:hover{border-color:var(--accent)}
/* forms and calculators */
label{display:inline-flex;flex-wrap:wrap;align-items:center;gap:8px;margin:6px 14px 6px 0;font-weight:500}
input,select,button{font:inherit;font-size:1rem;padding:9px 12px;border-radius:10px;border:1px solid var(--line);background:var(--bg);color:var(--text);min-height:44px}
input[type=number]{max-width:170px}input[type=radio],input[type=checkbox]{min-height:auto;accent-color:var(--accent);width:18px;height:18px}
input#q{width:100%%;max-width:none;margin:10px 0}
button,.btn{background:var(--accent);color:#fff;border:0;cursor:pointer;font-weight:600;padding:10px 18px}
button:hover{filter:brightness(1.08)}
#o{margin-top:14px}#o:empty{display:none}
/* tables */
.table-wrap{overflow-x:auto;margin:12px 0 20px;border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%%;font-size:.95rem;font-variant-numeric:tabular-nums}
th{background:var(--bg-alt);font-weight:600}td,th{border-bottom:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}
tr:last-child td{border-bottom:0}
.table-wrap table{margin:0}
/* footer */
footer{margin-top:40px;padding-top:24px;padding-bottom:40px;border-top:1px solid var(--line);font-size:.88rem;color:var(--muted)}
footer a{color:var(--muted)}footer a:hover{color:var(--accent)}
footer br+a{display:inline-block;margin-top:10px}
.foot-brand{display:flex;align-items:center;gap:8px;font-weight:700;color:var(--text);margin-bottom:8px}
@media print{.site-header,.kit-cta,footer{display:none}}
"""

def logo(s):
    g = s["glyph"]; fs = 34 if len(g) == 1 else 24
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="{html.escape(s["name"])}">'
            f'<rect width="64" height="64" rx="14" fill="{s["accent"]}"/>'
            f'<path d="M0 46 L64 30 L64 50 Q64 64 50 64 L14 64 Q0 64 0 50Z" fill="#fff" opacity=".14"/>'
            f'<text x="32" y="{43 if len(g)==1 else 41}" text-anchor="middle" font-family="system-ui,-apple-system,Segoe UI,Arial,sans-serif" font-weight="800" font-size="{fs}" fill="#fff">{html.escape(g)}</text></svg>')

def header(site, s):
    nav = "".join(f'<a href="{u}">{t}</a>' for u, t in s["nav"])
    nav += f'<a class="btn-nav" href="{s["cta"][0]}">{s["cta"][1]}</a>'
    return (f'<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap">'
            f'<a class="brand" href="index.html"><img src="logo.svg" alt="" width="34" height="34"><span>{html.escape(s["name"])}</span></a>'
            f'<nav class="site-nav" aria-label="Main">{nav}</nav></div></header><main id="main">')

def build(B):
    for site, s in SITES.items():
        d = f"{B}/{site}/site"
        if not os.path.isdir(d):
            continue
        open(f"{d}/style.css", "w").write(CSS % s)
        open(f"{d}/logo.svg", "w").write(logo(s))
        open(f"{d}/favicon.svg", "w").write(logo(s))
        headx = (f'<link rel="icon" href="favicon.svg" type="image/svg+xml"><meta name="theme-color" content="{s["accent"]}">'
                 f'<meta name="color-scheme" content="light dark">')
        for fn in sorted(f for f in os.listdir(d) if f.endswith(".html")):
            p = f"{d}/{fn}"; h = open(p).read()
            if 'class="site-header"' in h:
                continue
            h = h.replace("</head>", headx + "</head>", 1)
            h = re.sub(r"<header>.*?</header>", lambda m: header(site, s), h, count=1, flags=re.S)
            h = h.replace("\n<footer>", "</main>\n<footer>", 1)
            h = h.replace("<footer>", f'<footer><div class="foot-brand"><img src="logo.svg" alt="" width="22" height="22">{html.escape(s["name"])}</div>', 1)
            h = re.sub(r"(<table.*?</table>)", r'<div class="table-wrap">\1</div>', h, flags=re.S)
            if fn == "index.html":
                h = re.sub(r'<h1>(.*?)</h1>((?:<p class="note">.*?</p>)?)<p>(.*?)</p>', lambda m: f'<section class="hero"><span class="eyebrow">{html.escape(s["tagline"])}</span><h1>{m.group(1)}</h1><p>{m.group(3)}</p></section>{m.group(2)}', h, count=1, flags=re.S)
                # group runs of simple link cards into a responsive grid
                h = re.sub(r'((?:<div class=card><a href="[^"]+"><b>[^<]*</b></a><br>[^<]*</div>)+)', r'<div class="grid">\1</div>', h)
                h = h.replace("<h2>New for 2026/27</h2>", '<h2 id="more-calculators">New for 2026/27</h2>')
                h = h.replace('<section class="hero">', '<section class="hero" id="top">', 1)
                if site == "uk-money-calcs":
                    h = h.replace('</section><div class="grid">', '</section><h2 id="calculators">Calculators</h2><div class="grid">', 1)
                if site == "selfhost-ai-dir":
                    h = h.replace('<input id=q', '<h2 id="directory">Directory</h2><input id=q aria-label="Filter tools"', 1)
                if site == "uk-freelancer-kit":
                    h = h.replace("<h2>Free guides</h2>", '<h2 id="free-guides">Free guides</h2>', 1)
            open(p, "w").write(h)
