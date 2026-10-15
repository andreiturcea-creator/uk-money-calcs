import os,json,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import seo_pages
from seo_pages import DOMAINS, SB
B=os.environ.get("BUILD_DIR","/workspace/research/agent-biz")
CSS="""body{font-family:system-ui,sans-serif;max-width:860px;margin:0 auto;padding:24px;color:#1a1a2e;line-height:1.55}
header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #ddd;margin-bottom:24px}
a{color:#2b59c3}.card{border:1px solid #e3e3ea;border-radius:12px;padding:16px;margin:12px 0;background:#fafbff}
input,select,button{font-size:1rem;padding:8px;border-radius:8px;border:1px solid #bbb}button{background:#2b59c3;color:#fff;border:0;cursor:pointer}
table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #eee;padding:6px;text-align:left}
.tag{display:inline-block;background:#e8eefc;border-radius:6px;padding:2px 8px;margin:2px;font-size:.85rem}
.sp{border:2px dashed #f0a500;background:#fff8e6}footer{margin-top:40px;font-size:.85rem;color:#666}"""
def page(d,fn,title,desc,body,nav):
    os.makedirs(d,exist_ok=True)
    open(f"{d}/{fn}","w").write(f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><meta name="google-site-verification" content="4ClukxyHFtP7GSHUR0D75dGuQpNh220_u6YMPQ5exTw" /><link rel="stylesheet" href="style.css"></head><body>
<header><h3><a href="index.html" style="text-decoration:none">{nav}</a></h3></header>{body}
<footer><b>Disclaimer:</b> estimates for information only, not financial, tax or legal advice. Rates last checked against GOV.UK on 15 October 2026 (2026/27 tax year). Confirm with GOV.UK or a qualified adviser before acting. · <a href="about.html">About & disclosures</a></footer></body></html>""")
    open(f"{d}/style.css","w").write(CSS)

# ---------- 1. UK calculators ----------
d=f"{B}/uk-money-calcs/site"; N="UK Money Calcs"
calcs={
"take-home-pay.html":("UK Take-Home Pay Calculator 2026/27","Work out your take-home pay after income tax, National Insurance, pension and student loan (England, Wales and NI).","""
<h1>UK take-home pay calculator 2026/27</h1><div class="card">
<label>Gross annual salary £ <input id=s type=number value=35000></label><br><br>
<label>Pension (salary sacrifice) % <input id=p type=number value=5 style="width:70px"></label>
<label>Student loan <select id=sl><option value=0>None</option><option value=1>Plan 1</option><option value=2>Plan 2</option><option value=4>Plan 4 (Scotland)</option><option value=5>Plan 5</option><option value=9>Postgrad</option></select></label><br><br>
<button onclick=calc()>Calculate</button><div id=o></div></div>
<h2>How it works</h2><p>Personal allowance £12,570 (tapered by £1 per £2 above £100,000). Basic rate 20% to £50,270, higher 40% to £125,140, additional 45% above. Employee Class 1 NI: 8% between £12,570 and £50,270, 2% above. Thresholds are frozen until April 2031. Scotland uses different income tax bands, which this version does not cover yet.</p><p>Sources: <a href="https://www.gov.uk/income-tax-rates" rel="nofollow">GOV.UK Income Tax rates</a> · <a href="https://www.gov.uk/national-insurance-rates-letters" rel="nofollow">GOV.UK NI rates</a> · <a href="https://www.gov.uk/repaying-your-student-loan/what-you-pay" rel="nofollow">GOV.UK student loan thresholds</a>. Related: <a href="self-employed-tax-calculator.html">self-employed tax</a> · <a href="dividend-tax-calculator.html">dividend tax</a> · <a href="student-loan-repayment-calculator.html">student loan</a> · <a href="income-tax-bands-2026-27.html">2026/27 rates</a></p>
<script>
const SL={1:[26900,.09],2:[29385,.09],4:[33795,.09],5:[25000,.09],9:[21000,.06]};
function tax(t){let pa=12570;if(t>100000)pa=Math.max(0,pa-(t-100000)/2);let x=Math.max(0,t-pa),b=Math.min(x,37700),h=Math.min(Math.max(0,x-37700),125140-37700-pa>0?125140-pa-37700:0),a=Math.max(0,x-b-h);return b*.2+h*.4+a*.45}
function calc(){let s=+S('s'),p=s*(+S('p'))/100,g=s-p,t=tax(g),ni=Math.max(0,Math.min(g,50270)-12570)*.08+Math.max(0,g-50270)*.02,k=S('sl'),l=k>0?Math.max(0,g-SL[k][0])*SL[k][1]:0,n=g-t-ni-l;
o.innerHTML=`<table><tr><th></th><th>Year</th><th>Month</th></tr>${[['Pension',p],['Income tax',t],['National Insurance',ni],['Student loan',l],['<b>Take-home</b>',n]].map(r=>`<tr><td>${r[0]}</td><td>£${r[1].toFixed(0)}</td><td>£${(r[1]/12).toFixed(0)}</td></tr>`).join('')}</table>`}
function S(i){return document.getElementById(i).value}calc()</script>"""),
"stamp-duty.html":("Stamp Duty Calculator England 2026","Stamp Duty Land Tax calculator for England and Northern Ireland, covering first-time buyer relief and the 5% surcharge on additional properties.","""
<h1>Stamp Duty (SDLT) calculator: England & NI</h1><div class=card>
<label>Property price £ <input id=v type=number value=300000></label><br><br>
<label><input type=radio name=b value=m checked> Moving home</label> <label><input type=radio name=b value=f> First-time buyer</label> <label><input type=radio name=b value=a> Additional property (+5%)</label><br><br>
<button onclick=c()>Calculate</button><h2 id=o></h2></div>
<p>Rates from 1 April 2025: 0% up to £125k, 2% £125k–£250k, 5% £250k–£925k, 10% £925k–£1.5m, 12% above. First-time buyers pay 0% up to £300k and 5% from £300k to £500k; relief is lost above £500k. Additional homes pay 5% on top of each band.</p>
<script>function band(v,B){let t=0,prev=0;for(const[cap,r]of B){if(v>prev)t+=(Math.min(v,cap)-prev)*r;prev=cap}return t}
const STD=[[125000,0],[250000,.02],[925000,.05],[1500000,.10],[1e12,.12]];
function c(){let v=+document.getElementById('v').value,b=document.querySelector('[name=b]:checked').value,t;
if(b=='f'&&v<=500000)t=band(v,[[300000,0],[500000,.05]]);else if(b=='a')t=band(v,STD.map(([c,r])=>[c,r+.05]));else t=band(v,STD);
o.textContent='Stamp duty: £'+Math.round(t).toLocaleString('en-GB')}c()</script>"""),
"vat.html":("VAT Calculator UK: Add or Remove 20% VAT","Add VAT to a price or take it off, at 20%, 5% or 0%.","""
<h1>UK VAT calculator</h1><div class=card><label>Amount £ <input id=a type=number value=100></label>
<select id=r><option value=.2>20% standard</option><option value=.05>5% reduced</option><option value=0>0% zero</option></select>
<button onclick=v(1)>Add VAT</button> <button onclick=v(0)>Remove VAT</button><h2 id=o></h2></div>
<p>To take VAT out of a gross price at 20%, divide by 1.2. Don't just subtract 20%.</p><p>Checking whether you need to register? Use the <a href="vat-threshold-checker.html">VAT threshold checker (£90,000)</a>. Source: <a href="https://www.gov.uk/vat-registration/when-to-register" rel="nofollow">GOV.UK</a>.</p>
<script>function v(add){let a=+document.getElementById('a').value,r=+document.getElementById('r').value;let net=add?a:a/(1+r),gross=add?a*(1+r):a;
o.textContent=`Net £${net.toFixed(2)} · VAT £${(gross-net).toFixed(2)} · Gross £${gross.toFixed(2)}`}</script>"""),
"pro-rata-salary.html":("Pro Rata Salary Calculator UK","Turn a full-time salary into a part-time one, by hours or days per week.","""
<h1>Pro rata salary calculator</h1><div class=card><label>Full-time salary £ <input id=f type=number value=30000></label>
<label>FT hours/week <input id=fh type=number value=37.5 style="width:70px"></label> <label>Your hours/week <input id=h type=number value=22.5 style="width:70px"></label>
<button onclick="o.textContent='Pro rata salary: £'+Math.round(f.value*h.value/fh.value).toLocaleString('en-GB')+' a year'">Calculate</button><h2 id=o></h2></div>
<p>Holiday entitlement is pro-rated in the same way: 5.6 weeks × your days per week.</p>"""),
}
idx='<h1>Free, accurate UK money calculators</h1><p>Fast and private: everything runs in your browser and nothing is stored.</p>'+''.join(f'<div class=card><a href="{k}"><b>{v[0]}</b></a><br>{v[1]}</div>' for k,v in calcs.items())
idx+='<h2>New for 2026/27</h2>'+''.join(f'<div class=card><a href="{k}"><b>{t}</b></a><br>{ds}</div>' for k,t,ds in [("self-employed-tax-calculator.html","Self-employed tax calculator 2026/27","Income Tax and Class 4 NI on sole trader profits."),("dividend-tax-calculator.html","Dividend tax calculator 2026/27","£500 allowance; 10.75%, 35.75% and 39.35% rates."),("student-loan-repayment-calculator.html","Student loan repayment calculator","Plans 1, 2, 4, 5 and Postgraduate."),("vat-threshold-checker.html","VAT threshold checker","Rolling 12-month £90,000 test."),("income-tax-bands-2026-27.html","Income Tax and NI rates 2026/27","All the bands on one page, with GOV.UK sources.")])
idx+='<div class=card><b>Self-employed?</b> Free guides on <a href="https://kit.andreiturcea.com/guide-mtd.html">Making Tax Digital for Income Tax</a>, <a href="https://kit.andreiturcea.com/guide-payments-on-account.html">payments on account</a> and the <a href="https://kit.andreiturcea.com/">UK Sole Trader Kit</a>.</div>'
idx+='<div class="card sp"><b>Partner offers: coming soon.</b> Any sponsored or affiliate link will be clearly labelled.</div>'
page(d,"index.html","UK Money Calculators: take-home pay, stamp duty, VAT","Free UK calculators for salary, tax, stamp duty and VAT.",idx,N)
for k,(t,ds,b) in calcs.items(): page(d,k,t+" | "+N,ds,b,N)
page(d,"about.html","About | "+N,"About","<h1>About</h1><p>An independent site with calculators that are maintained and checked automatically against GOV.UK rates. Affiliate links are labelled, and they never change the results. </p>",N)

# ---------- 2. Self-hosted AI tools directory ----------
d=f"{B}/selfhost-ai-dir/site"; N="SelfHostAI"
tools=[("Ollama","Run LLMs locally with a single command.","ollama/ollama","LLM runtime","MIT"),("Open WebUI","ChatGPT-style interface for local and API models.","open-webui/open-webui","Chat UI","BSD-3"),
("LocalAI","OpenAI-compatible API server for local models.","mudler/LocalAI","LLM runtime","MIT"),("vLLM","High-throughput LLM serving engine.","vllm-project/vllm","LLM runtime","Apache-2.0"),
("llama.cpp","LLM inference in C/C++, runs on CPU.","ggml-org/llama.cpp","LLM runtime","MIT"),("n8n","Workflow automation with AI agent nodes; fair-code licence.","n8n-io/n8n","Automation","Sustainable Use"),
("Dify","LLM app and agent builder platform.","langgenius/dify","Agent builder","Apache-2.0 (modified)"),("Flowise","Drag-and-drop LLM flows.","FlowiseAI/Flowise","Agent builder","Apache-2.0"),
("AnythingLLM","All-in-one RAG desktop and Docker app.","Mintplex-Labs/anything-llm","RAG","MIT"),("ComfyUI","Node-based image and video diffusion UI.","comfyanonymous/ComfyUI","Image gen","GPL-3.0"),
("Whisper.cpp","Local speech-to-text.","ggml-org/whisper.cpp","Speech","MIT"),("LibreChat","Multi-provider chat UI with agents.","danny-avila/LibreChat","Chat UI","MIT"),
("Langfuse","LLM observability and evals.","langfuse/langfuse","Observability","MIT (core)"),("Qdrant","Vector database.","qdrant/qdrant","Vector DB","Apache-2.0"),
("Jan","Offline ChatGPT alternative desktop app.","janhq/jan","Chat UI","Apache-2.0"),("Perplexica","Self-hosted AI search engine.","ItzCrazyKns/Perplexica","Search","MIT")]
os.makedirs(f"{B}/selfhost-ai-dir/data",exist_ok=True)
json.dump([dict(name=a,desc=b,repo=c,cat=e,license=f,stars=None,last_commit=None) for a,b,c,e,f in tools],open(f"{B}/selfhost-ai-dir/data/tools.json","w"),indent=1)
cats=sorted({t[3] for t in tools})
body='<h1>Self-hostable AI tools, ranked and kept fresh</h1><p>Open-source AI you can run on your own VPS or laptop. Stars and activity refresh every day from GitHub.</p><div class="card sp"><b>Featured listings: coming soon</b> (£49/month, always labelled). <a href="advertise.html">Advertise</a></div><input id=q placeholder="Filter…" oninput="f()" style="width:100%"><div id=l>'
body+=''.join(f'<div class=card data-t="{(a+b+e).lower()}"><b><a href="tool-{c.split("/")[1].lower()}.html">{a}</a></b> <span class=tag>{e}</span><span class=tag>{f}</span><br>{b} · <a href="https://github.com/{c}" rel="nofollow">GitHub</a></div>' for a,b,c,e,f in tools)
body+='</div><script>function f(){let v=q.value.toLowerCase();document.querySelectorAll("#l .card").forEach(c=>c.style.display=c.dataset.t.includes(v)?"":"none")}</script>'
body+='<h2>Guides</h2><a class=tag href="best-self-hosted-chatgpt-alternatives.html">Best self-hosted ChatGPT alternatives</a><a class=tag href="ollama-vs-llama-cpp-vs-vllm.html">Ollama vs llama.cpp vs vLLM</a><a class=tag href="open-webui-vs-librechat-vs-anythingllm.html">Open WebUI vs LibreChat vs AnythingLLM</a>'
body+='<h2>Categories</h2>'+''.join(f'<a class=tag href="cat-{x.lower().replace(" ","-")}.html">{x}</a>' for x in cats)
page(d,"index.html","Self-Hosted AI Tools Directory | SelfHostAI","A curated directory of open-source AI tools you can self-host, refreshed every day.",body,N)
for a,b,c,e,f in tools:
    alts=[t[0] for t in tools if t[3]==e and t[0]!=a]
    page(d,f"tool-{c.split('/')[1].lower()}.html",f"{a}: self-hosting guide & alternatives | SelfHostAI",f"How to self-host {a}: requirements, licence and alternatives.",
    f"<h1>{a}</h1><p>{b}</p><table><tr><td>Category</td><td>{e}</td></tr><tr><td>Licence</td><td>{f}</td></tr><tr><td>Repo</td><td><a href='https://github.com/{c}'>{c}</a></td></tr></table><h2>Quick start</h2><p>See the official README for Docker or binary install. A 2 vCPU / 4 GB VPS runs most UIs; LLM runtimes need a GPU or must run small quantised models on CPU.</p><h2>Alternatives</h2><p>{', '.join(alts) or '-'}</p>",N)
for x in cats:
    page(d,f"cat-{x.lower().replace(' ','-')}.html",f"Best self-hosted {x} tools | SelfHostAI",f"Open-source {x} tools you can self-host.","<h1>Self-hosted "+x+"</h1>"+''.join(f'<div class=card><b>{a}</b>: {b}</div>' for a,b,c,e,f in tools if e==x),N)
page(d,"advertise.html","Advertise | SelfHostAI","Sponsor","<h1>Featured listing</h1><p>£49/month: pinned, labelled 'Featured', plus one newsletter mention. Payments coming soon. Bookings are not open yet. Open-source tools only. We reserve the right to decline.</p>",N)
page(d,"about.html","About | SelfHostAI","About","<h1>About</h1><p>Agent-maintained. Data comes from the public GitHub API. Sponsored listings are always labelled.</p>",N)

# ---------- 3. UK freelancer templates ----------
d=f"{B}/uk-freelancer-kit/site"
page(d,"index.html","UK Sole Trader Tax & Invoice Kit (Google Sheets) | £9","Self-assessment income and expense tracker, MTD-ready categories, invoice template and tax estimate for UK sole traders.",
"""<h1>The UK Sole Trader Kit: £9</h1><p>A spreadsheet that tracks income and allowable expenses using HMRC SA103 categories, estimates your tax and Class 4 NI, and includes an invoice template. Works in Google Sheets and Excel.</p>
<div class=card><ul><li>Income log, plus expenses mapped to SA103 boxes</li><li>Live tax and NI estimate for 2026/27</li><li>Payments-on-account reminder</li><li>Invoice template</li><li>MTD for Income Tax: who it applies to from April 2026 (£50k+) and April 2027 (£30k+)</li></ul>
<a href="sample.csv">Download a free sample sheet (CSV)</a><br><br><a href="https://turceapaul.gumroad.com/l/bmykeg"><button>Buy the kit, £9</button></a></div>
<h2>Free guides</h2><ul><li><a href="guide-mtd.html">Making Tax Digital for Income Tax: who needs it and when</a></li><li><a href="guide-mtd-quarterly-deadlines.html">MTD quarterly update deadlines</a></li><li><a href="guide-mtd-software.html">MTD software: spreadsheets and bridging</a></li><li><a href="guide-self-assessment-deadlines.html">Self Assessment deadlines 2026/27</a></li><li><a href="guide-payments-on-account.html">Payments on account explained</a></li><li><a href="guide-mileage-allowance.html">Mileage allowance 2026/27 (55p)</a></li><li><a href="guide-allowable-expenses.html">Allowable expenses for sole traders</a></li></ul><h2>Free calculators</h2><a href="https://calcs.andreiturcea.com/self-employed-tax-calculator.html">Self-employed tax 2026/27</a> · <a href="https://calcs.andreiturcea.com/vat-threshold-checker.html">VAT threshold checker</a> · <a href="https://calcs.andreiturcea.com/dividend-tax-calculator.html">Dividend tax</a>""","UK Freelancer Kit")
page(d,"about.html","About","About","<h1>About</h1><p>Templates only. Not tax advice.</p>","UK Freelancer Kit")
open(f"{d}/sample.csv","w").write("Date,Description,Type,SA103 category,Amount\n2026-04-10,Client A invoice 001,Income,Turnover,1200\n2026-04-12,Adobe subscription,Expense,Office costs,19.97\n2026-04-15,Train to client,Expense,Travel,34.50\n2026-04-30,Accountancy software,Expense,Financial costs,12.00\n")
seo_pages.build(B)
import monetise
monetise.build(B)
for s in ["uk-money-calcs","selfhost-ai-dir","uk-freelancer-kit"]:
    dd=f"{B}/{s}/site"; urls=[f for f in os.listdir(dd) if f.endswith(".html")]
    open(f"{dd}/sitemap.xml","w").write('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f"<url><loc>{SB(s)}/{'' if u=='index.html' else u}</loc><lastmod>2026-10-15</lastmod></url>" for u in sorted(urls))+"</urlset>")
    open(f"{dd}/CNAME","w").write(DOMAINS[s]+"\n")
    open(f"{dd}/robots.txt","w").write("User-agent: *\nAllow: /\nSitemap: https://"+DOMAINS[s]+"/sitemap.xml\n")

import agent_ready
agent_ready.build(B)
