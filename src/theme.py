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

CSS = """/* Shared design system v2 (Impeccable audit + Modern Web Guidance). Accent per site. */
:root{color-scheme:light dark;
--accent-l:%(accent)s;--accent-d:%(accent_dark)s;--soft-l:%(soft)s;--soft-d:%(soft_dark)s;
--accent:var(--accent-l);--accent-soft:var(--soft-l);--on-accent:#ffffff;
--bg:#fbfbfa;--bg-alt:#f2f3f1;--text:#17191c;--muted:#4f5560;--line:#dfe2e0;--card:#ffffff;
--warn-bg:#fff7e6;--warn-line:#e7c27a;--radius:12px;
--shadow:0 1px 2px rgba(20,24,28,.06),0 2px 8px rgba(20,24,28,.05);
--font:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
--measure:68ch;--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:32px;--s7:48px;--s8:64px}
@media (prefers-color-scheme:dark){:root{--accent:var(--accent-d);--accent-soft:var(--soft-d);--on-accent:#0d0f12;
--bg:#0f1113;--bg-alt:#171a1d;--text:#e9ebee;--muted:#a9afb8;--line:#2b3035;--card:#15181b;--warn-bg:#2a2214;--warn-line:#7d6230;
--shadow:0 1px 2px rgba(0,0,0,.5)}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%%;text-size-adjust:100%%;scroll-padding-top:88px;accent-color:var(--accent);scrollbar-color:color-mix(in srgb,var(--muted) 55%%,transparent) transparent}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);font-size:1.0625rem;line-height:1.65;caret-color:var(--accent)}
::selection{background:color-mix(in srgb,var(--accent) 28%%,transparent);color:inherit}
a{color:var(--accent);text-underline-offset:.2em;text-decoration-thickness:1px}
a:hover{text-decoration-thickness:2px}
:focus-visible{outline:3px solid var(--accent);outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:-999px;top:var(--s2);background:var(--accent);color:var(--on-accent);padding:var(--s2) var(--s4);border-radius:8px;z-index:20}.skip:focus{left:var(--s2)}
.wrap,main,footer{width:100%%;max-width:840px;margin-inline:auto;padding-inline:20px}
/* header: solid surface, no decorative blur */
.site-header{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--line)}
.site-header .wrap{max-width:1040px;display:flex;align-items:center;gap:var(--s4);min-height:60px;flex-wrap:wrap;padding-block:var(--s2)}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:700;letter-spacing:-.01em;font-size:1.05rem}
.brand img{display:block;border-radius:8px}
.site-nav{display:flex;gap:2px;margin-left:auto;overflow-x:auto;scrollbar-width:none;max-width:100%%}
.site-nav a{color:var(--muted);text-decoration:none;padding:10px 12px;border-radius:8px;font-size:.95rem;white-space:nowrap;min-height:44px;display:inline-flex;align-items:center}
.site-nav a:hover{color:var(--text);background:var(--bg-alt)}
.site-nav a.btn-nav{background:var(--accent);color:var(--on-accent);font-weight:600;margin-left:var(--s2)}
.site-nav a.btn-nav:hover{background:color-mix(in srgb,var(--accent) 88%%,var(--text))}
@media (max-width:640px){.site-nav{margin-left:0;width:100%%;order:3;mask-image:linear-gradient(90deg,#000 88%%,transparent)}}
/* reading typography */
main{padding-block:var(--s6) var(--s5)}
main>p,main>ul,main>ol,.card p,.card ul,.answer,.note{max-width:var(--measure)}
h1,h2,h3{line-height:1.2;letter-spacing:-.02em;color:var(--text);text-wrap:balance}
h1{font-size:clamp(1.85rem,1.2rem + 2.6vw,2.75rem);margin:0 0 var(--s4);font-weight:800;letter-spacing:-.03em}
h2{font-size:clamp(1.3rem,1.1rem + .8vw,1.6rem);margin:var(--s7) 0 var(--s3);font-weight:700}
h3{font-size:1.125rem;margin:var(--s5) 0 var(--s2);font-weight:650}
p,li{text-wrap:pretty}p,ul,ol{margin:0 0 var(--s4)}li{margin:var(--s1) 0}li::marker{color:var(--muted)}
code{font-family:var(--mono);font-size:.9em;background:var(--bg-alt);padding:.1em .35em;border-radius:5px}
.answer{font-size:1.125rem;line-height:1.6;background:var(--accent-soft);border-radius:var(--radius);padding:var(--s4) var(--s5);margin:0 0 var(--s3)}
#last-updated{color:var(--muted)!important;font-size:.85rem!important;margin-bottom:var(--s5)}
.small{font-size:.85rem;color:var(--muted)}
.note{background:var(--bg-alt);border:1px solid var(--line);padding:var(--s3) var(--s4);border-radius:var(--radius);font-size:.92rem;color:var(--muted)}
.note b{color:var(--text)}
.anchor{display:block;scroll-margin-top:88px}
/* home hero: open layout, no box, no eyebrow */
.hero{margin:0 0 var(--s6);padding:var(--s4) 0 var(--s5);border-bottom:1px solid var(--line)}
.hero h1{font-size:clamp(2.1rem,1.3rem + 3.4vw,3.25rem);max-width:20ch}
.hero .answer{background:none;padding:0;font-size:1.2rem;color:var(--text)}
.hero>p:last-child{font-size:1.05rem;color:var(--muted);max-width:var(--measure);margin:0}
/* panels */
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:var(--s4) var(--s5);margin:var(--s4) 0}
.card>b:first-child{display:block;margin-bottom:var(--s1)}
.card ul{padding-left:1.2em}
/* link lists instead of identical card grids */
.grid,#l{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%%,320px),1fr));column-gap:var(--s6);margin:var(--s3) 0 var(--s5);border-top:1px solid var(--line)}
.grid .card,#l .card{margin:0;padding:var(--s4) 0;border:0;border-bottom:1px solid var(--line);border-radius:0;background:none;box-shadow:none;color:var(--muted);font-size:.95rem;line-height:1.5}
.grid .card a,#l .card b a{text-decoration:none;font-size:1.05rem}
.grid .card a b,#l .card b{color:var(--text)}
.grid .card a:hover b,#l .card b a:hover{color:var(--accent);text-decoration:underline;text-decoration-thickness:1px}
#l .card b a{color:var(--text)}
.sp{background:var(--warn-bg);border:1px solid var(--warn-line)}
.kit-cta{background:var(--accent-soft);border:1px solid color-mix(in srgb,var(--accent) 30%%,transparent);padding:var(--s5)}
.kit-cta b:first-child{display:inline}
.kit-cta a:last-child{display:inline-flex;align-items:center;min-height:44px;margin-top:var(--s3);background:var(--accent);color:var(--on-accent);padding:0 var(--s4);border-radius:10px;text-decoration:none;font-weight:600}
.kit-cta a:last-child:hover{background:color-mix(in srgb,var(--accent) 88%%,var(--text))}
.tag{display:inline-block;background:var(--bg-alt);color:var(--muted);border-radius:999px;padding:2px 10px;margin:2px 4px 2px 0;font-size:.8rem;text-decoration:none;border:1px solid var(--line);font-weight:500;vertical-align:.1em}
a.tag{color:var(--text);padding:6px 12px;font-size:.88rem}a.tag:hover{border-color:var(--accent);color:var(--accent)}
/* forms and calculators */
label{display:inline-flex;flex-wrap:wrap;align-items:center;gap:var(--s2);margin:var(--s2) var(--s4) var(--s2) 0;font-weight:500}
input,select,button{font:inherit;font-size:1rem;padding:9px 12px;border-radius:10px;border:1px solid color-mix(in srgb,var(--muted) 45%%,var(--line));background:var(--bg);color:var(--text);min-height:44px}
input:hover,select:hover{border-color:var(--muted)}
input[type=number]{max-width:11rem;font-variant-numeric:tabular-nums}
input[type=radio],input[type=checkbox]{min-height:auto;width:20px;height:20px}
input#q{width:100%%;max-width:none;margin:var(--s2) 0 0}
button,.btn{background:var(--accent);color:var(--on-accent);border:0;cursor:pointer;font-weight:600;padding:0 var(--s5)}
button:hover{background:color-mix(in srgb,var(--accent) 88%%,var(--text))}
button:active{transform:translateY(1px)}
#o{margin-top:var(--s4);font-variant-numeric:tabular-nums}#o:empty{display:none}
h2#o{font-size:1.4rem;margin-bottom:0}
/* tables */
.table-wrap{overflow-x:auto;margin:var(--s3) 0 var(--s5);border:1px solid var(--line);border-radius:var(--radius);background:var(--card)}
table{border-collapse:collapse;width:100%%;font-size:.95rem;font-variant-numeric:tabular-nums}
th{background:var(--bg-alt);font-weight:600;font-size:.88rem;color:var(--muted)}td,th{border-bottom:1px solid var(--line);padding:10px 14px;text-align:left;vertical-align:top}
tr:last-child td{border-bottom:0}
/* footer */
footer{margin-top:var(--s7);padding-block:var(--s5) var(--s7);border-top:1px solid var(--line);font-size:.88rem;color:var(--muted)}
footer a{color:var(--muted);display:inline-block;padding:var(--s2) 0}footer a:hover{color:var(--accent)}
.foot-brand{display:flex;align-items:center;gap:var(--s2);font-weight:700;color:var(--text);margin-bottom:var(--s2)}
@media (prefers-reduced-motion:no-preference){a,button,.site-nav a{transition:color .15s ease-out,background-color .15s ease-out}}
@media print{.site-header,.kit-cta,footer,.skip{display:none}}
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
            h = re.sub(r"(<table.*?</table>)", r'<div class="table-wrap" role="region" tabindex="0" aria-label="Table (scrolls sideways on small screens)">\1</div>', h, flags=re.S)
            h = re.sub(r"id=o>", 'id=o aria-live="polite">', h)
            if fn == "index.html":
                h = re.sub(r'<h1>(.*?)</h1>((?:<p class="note">.*?</p>)?)<p>(.*?)</p>', lambda m: f'<section class="hero"><h1>{m.group(1)}</h1><p>{m.group(3)}</p></section>{m.group(2)}', h, count=1, flags=re.S)
                # group runs of simple link cards into a responsive grid
                h = re.sub(r'((?:<div class=card><a href="[^"]+"><b>[^<]*</b></a><br>[^<]*</div>)+)', r'<div class="grid">\1</div>', h)
                h = h.replace('<section class="hero">', '<section class="hero" id="top">', 1)
                if site == "uk-money-calcs":
                    h = h.replace('<div class="grid">', '<h2 id="calculators">All calculators</h2><div class="grid">', 1)
                if site == "selfhost-ai-dir":
                    h = h.replace('<input id=q', '<h2 id="directory">Directory</h2><input id=q aria-label="Filter tools"', 1)
                if site == "uk-freelancer-kit":
                    h = h.replace("<h2>Free guides</h2>", '<span class="anchor" id="free-guides"></span><h2>Free guides</h2>', 1)
            open(p, "w").write(h)
