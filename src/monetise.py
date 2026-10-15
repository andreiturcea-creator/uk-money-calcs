# Monetisation and compliance layer, added 15 Oct 2026.
# Runs after seo_pages.build() and before agent_ready.build(), so new pages get .md twins,
# llms.txt entries and sitemap entries automatically.
# Adds: privacy, cookies and affiliate disclosure pages; a shared footer linking to them;
# a 'general information, not tax or financial advice' note on the tax sites; calm £9 kit
# call-to-action boxes near the top and at the end of each guide page on the tax sites;
# referral slots read from referrals.json (hidden while the url is empty).
import os, re, json, html
import seo_pages
R = seo_pages.R
BUY = seo_pages.BUY
KIT = seo_pages.KIT
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {"uk-money-calcs": "UK Money Calcs", "uk-freelancer-kit": "UK Freelancer Kit", "selfhost-ai-dir": "SelfHostAI"}
TAX = ("uk-money-calcs", "uk-freelancer-kit")
LEGAL = ("privacy.html", "cookies.html", "affiliate-disclosure.html")
DATE_H = "15 October 2026"

def slots(site):
    try:
        cfg = json.load(open(os.path.join(HERE, "referrals.json")))
    except Exception:
        return []
    return [s for s in cfg.get("slots", []) if site in s.get("sites", []) and str(s.get("url", "")).startswith("https://")]

def partner_box(site):
    live = slots(site)
    if not live:
        return ""
    items = "".join(f'<li><a href="{html.escape(s["url"])}" rel="sponsored noopener">{html.escape(s["name"])}</a> <span class=tag>Affiliate link</span>: {html.escape(s["blurb"])}</li>' for s in live)
    return (f'<div class=card id="partners"><b>Tools some readers use</b> <span class=tag>Contains affiliate links</span><ul>{items}</ul>'
            f'<p class="small">If you sign up through these links we may earn a commission, at no extra cost to you. It never changes our figures or guides. <a href="affiliate-disclosure.html">How affiliate links work here</a>.</p></div>')

NOTE = '<p class="note"><b>General information, not tax or financial advice.</b> Check GOV.UK or speak to a qualified adviser about your own situation.</p>'
CTA_TOP = (f'<div class="card sp kit-cta" id="kit-top"><b>Keeping your own records?</b> The UK Sole Trader Kit is a £9 spreadsheet for Google Sheets and Excel: '
           f'an income log, expenses mapped to SA103 boxes, a live 2026/27 tax and Class 4 NI estimate, and an invoice template. '
           f'<a href="{KIT}">See what is inside</a> · <a href="{BUY}">Get the kit (£9)</a></div>')
CTA_END = (f'<div class="card sp kit-cta" id="kit-end"><b>Want this in a spreadsheet?</b> If you would rather not build your own tracker, the UK Sole Trader Kit (£9, Google Sheets and Excel) '
           f'logs income, maps expenses to SA103 boxes, estimates your 2026/27 Income Tax and Class 4 NI, reminds you about payments on account and includes an invoice template. '
           f'It is a template, not advice, and the free guides here stay free. <a href="{KIT}">See what is inside</a> · <a href="{BUY}">Get the kit (£9)</a></div>')

def footer(site):
    if site in TAX:
        lead = "<b>General information, not tax or financial advice.</b> Estimates for information only, not financial, tax or legal advice. " + seo_pages.FOOT["tax"]
    else:
        lead = "<b>Disclaimer:</b> information only. " + seo_pages.FOOT["ai"]
    links = ' · '.join(f'<a href="{u}">{t}</a>' for u, t in [("about.html", "About"), ("privacy.html", "Privacy"), ("cookies.html", "Cookies"), ("affiliate-disclosure.html", "Affiliate disclosure")])
    return f'<footer>{lead}<br>{links}</footer>'

def is_guide(site, fn):
    if fn in LEGAL or fn in ("index.html", "about.html", "advertise.html"):
        return False
    if site == "uk-freelancer-kit":
        return fn.startswith("guide-")
    return site == "uk-money-calcs"

def legal_pages(site):
    n = NAMES[site]; repo = f"https://github.com/andreiturcea-creator/{site}"
    tax = site in TAX
    sold = (f'<li><b>Buying the kit.</b> The UK Sole Trader Kit is sold on Gumroad. If you click through to buy, Gumroad handles the payment and your details under <a href="https://gumroad.com/privacy" rel="nofollow">its own privacy policy</a>. We only receive what Gumroad passes to sellers to fulfil an order.</li>' if tax else "")
    privacy = f"""<h1>Privacy</h1><p>Last updated {DATE_H}. This notice explains what happens to your information when you use {n}.</p>
<h2>The short version</h2><p>We do not ask for your name or email, we do not run analytics or advertising, and we do not set cookies. Anything you type into a calculator or filter box stays in your browser and is not sent to us.</p>
<h2>What is collected</h2><ul><li><b>Hosting.</b> The site is a static site hosted on GitHub Pages. Like any web host, GitHub receives technical data such as your IP address and browser details when your browser requests a page, and may keep it in server logs for security. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="nofollow">GitHub Privacy Statement</a>. We cannot see those logs.</li>
<li><b>Calculators and filters.</b> These run entirely in your browser with JavaScript. Nothing is stored or transmitted.</li>{sold}
<li><b>Links to other sites.</b> When you follow a link to another site (for example GOV.UK, GitHub or a partner), that site's own privacy policy applies.</li></ul>
<h2>Changes</h2><p>If we ever add analytics, a newsletter, ads or anything else that collects personal data, we will update this page and the <a href="cookies.html">cookies page</a> first, and ask for consent where the law requires it.</p>
<h2>Your rights and contact</h2><p>Under UK GDPR you have rights over your personal data, including access and deletion. As we hold no personal data from browsing, there is normally nothing for us to give you. To get in touch, open an issue on the site's <a href="{repo}/issues" rel="nofollow">GitHub repository</a> (issues are public, so do not include private details). You can also complain to the <a href="https://ico.org.uk/make-a-complaint/" rel="nofollow">Information Commissioner's Office</a>.</p>"""
    cookies = f"""<h1>Cookies</h1><p>Last updated {DATE_H}.</p>
<p><b>{n} does not set any cookies</b> and does not use similar technologies such as local storage, tracking pixels or fingerprinting. There is no analytics or advertising code on the site, so there is no cookie banner.</p>
<p>The site is hosted on GitHub Pages, which serves static files and does not set cookies on these pages. If you click through to another site (for example Gumroad, GitHub or a partner), that site may set its own cookies under its own policy once you are there.</p>
<p>If this ever changes, for example if we add analytics or ads, we will list every cookie here and ask for your consent before setting any that are not strictly necessary, as the Privacy and Electronic Communications Regulations (PECR) require. See also our <a href="privacy.html">privacy notice</a>.</p>"""
    own = ("<li><b>Our own product.</b> The UK Sole Trader Kit (£9, sold on Gumroad) is made by us. Links to it are links to our own product, not affiliate links.</li>" if tax else
           "<li><b>Featured listings.</b> If we sell featured listings in future, they will be labelled 'Featured' or 'Sponsored'.</li>")
    aff = f"""<h1>Affiliate disclosure</h1><p>Last updated {DATE_H}.</p>
<p>{n} is free to use. To help pay for it, some links may be <b>affiliate or referral links</b>. If you click one and sign up or buy, we may earn a commission or credit, at no extra cost to you.</p>
<h2>How we label them</h2><ul><li>Every affiliate or referral link is marked <span class=tag>Affiliate link</span> next to the link itself, not only on this page.</li>
<li>These links carry <code>rel="sponsored"</code> so search engines know they are paid links.</li>{own}</ul>
<h2>What it does not change</h2><p>Commissions never change calculator results, figures, rankings or what we write.{" Tax figures come from GOV.UK." if tax else " Tool details come from each project's public GitHub repository."} We only link to services we think are relevant, and you can always go to a provider directly instead.</p>
<h2>Current partners</h2><p>{"We list partner links only once a programme has approved us. " + ("Right now there are none." if not slots(site) else "Current partners: " + ", ".join(html.escape(s["name"]) for s in slots(site)) + ".")}</p>
<p>This follows the UK CAP Code and ASA guidance that marketing must be obviously identifiable. See also our <a href="privacy.html">privacy notice</a>.</p>"""
    return {"privacy.html": (f"Privacy | {n}", f"Privacy notice for {n}: no analytics, no ads, no personal data collected.", privacy),
            "cookies.html": (f"Cookies | {n}", f"Cookie notice for {n}: the site sets no cookies.", cookies),
            "affiliate-disclosure.html": (f"Affiliate disclosure | {n}", f"How {n} labels affiliate and referral links.", aff)}

def build(B):
    for site in NAMES:
        d = f"{B}/{site}/site"
        if not os.path.isdir(d):
            continue
        for fn, (t, ds, body) in legal_pages(site).items():
            seo_pages.wpage(d, fn, t, ds, body, NAMES[site], None, foot="ai")
        pb = partner_box(site)
        for fn in sorted(f for f in os.listdir(d) if f.endswith(".html")):
            p = f"{d}/{fn}"; h = open(p).read()
            if 'class="kit-cta"' in h or 'id="kit-end"' in h:
                continue
            h = re.sub(r"<footer>.*?</footer>", lambda m: footer(site), h, count=1, flags=re.S)
            guide = site in TAX and is_guide(site, fn)
            top = ""
            if site in TAX and fn not in LEGAL:
                top += NOTE
            if guide:
                h = h.replace(seo_pages.KITBOX, "")
                top += CTA_TOP
            if top:
                h = re.sub(r"(</h1>)", lambda m: m.group(1) + top, h, count=1)
            end = ""
            if pb and fn not in LEGAL and fn != "about.html" and (guide or site == "selfhost-ai-dir" or fn == "index.html"):
                end += pb
            if guide:
                end += CTA_END
            if end:
                h = h.replace("\n<footer>", end + "\n<footer>", 1)
            open(p, "w").write(h)
