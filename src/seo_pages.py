# SEO pages added 15 Oct 2026. Figures checked against GOV.UK on 15 Oct 2026.
import os, json, html
R = "https://andreiturcea-creator.github.io"  # legacy, use SB(site)
DOMAINS = {"uk-money-calcs": "calcs.andreiturcea.com", "uk-freelancer-kit": "kit.andreiturcea.com", "selfhost-ai-dir": "ai.andreiturcea.com"}
def SB(site): return "https://" + DOMAINS[site]
CALCS, KIT, AI = SB("uk-money-calcs")+"/", SB("uk-freelancer-kit")+"/", SB("selfhost-ai-dir")+"/"
BUY = "https://turceapaul.gumroad.com/l/bmykeg"
G = {
 "it": "https://www.gov.uk/income-tax-rates",
 "seni": "https://www.gov.uk/self-employed-national-insurance-rates",
 "ni": "https://www.gov.uk/national-insurance-rates-letters",
 "div": "https://www.gov.uk/tax-on-dividends",
 "sl": "https://www.gov.uk/repaying-your-student-loan/what-you-pay",
 "vat": "https://www.gov.uk/vat-registration/when-to-register",
 "mtd": "https://www.gov.uk/guidance/check-if-youre-eligible-for-making-tax-digital-for-income-tax",
 "qi": "https://www.gov.uk/guidance/work-out-your-qualifying-income-for-making-tax-digital-for-income-tax",
 "qu": "https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/send-quarterly-updates",
 "sw": "https://www.gov.uk/guidance/find-software-thats-compatible-with-making-tax-digital-for-income-tax",
 "sa": "https://www.gov.uk/self-assessment-tax-returns/deadlines",
 "poa": "https://www.gov.uk/understand-self-assessment-bill/payments-on-account",
 "mi": "https://www.gov.uk/simpler-income-tax-simplified-expenses/vehicles",
}
def src(*k):
    return '<div class=card><b>GOV.UK sources (checked 15 October 2026):</b><ul>' + ''.join(f'<li><a href="{G[x]}" rel="nofollow">{G[x]}</a></li>' for x in k) + '</ul></div>'
def faq_html(faq):
    return '<h2>FAQs</h2>' + ''.join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>' for q, a in faq)
def ld(faq):
    j = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False).replace("</", "<\\/") + '</script>'
def related(links):
    return '<div class=card><b>Related</b><ul>' + ''.join(f'<li><a href="{u}">{t}</a></li>' for u, t in links) + '</ul></div>'
FOOT = {"tax": "Rates last checked against GOV.UK on 15 October 2026 (2026/27 tax year). Confirm with GOV.UK or a qualified adviser before acting.",
        "ai": "Tool details are taken from each project's public GitHub repository; check the official docs before deploying."}
def wpage(d, fn, title, desc, body, nav, faq=None, foot="tax"):
    os.makedirs(d, exist_ok=True)
    extra = ld(faq) if faq else ""
    canon = f'{SB(d.split("/")[-2])}/{"" if fn=="index.html" else fn}'
    open(f"{d}/{fn}", "w").write(f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canon}"><meta name="google-site-verification" content="4ClukxyHFtP7GSHUR0D75dGuQpNh220_u6YMPQ5exTw" /><link rel="stylesheet" href="style.css">{extra}</head><body>
<header><h3><a href="index.html" style="text-decoration:none">{nav}</a></h3></header>{body}{faq_html(faq) if faq else ""}
<footer><b>Disclaimer:</b> estimates for information only, not financial, tax or legal advice. {FOOT[foot]} · <a href="about.html">About &amp; disclosures</a></footer></body></html>""")

KITBOX = f'<div class="card sp"><b>UK Sole Trader Kit (£9):</b> income log, expenses mapped to SA103 boxes, a live 2026/27 tax and Class 4 NI estimate, payments-on-account reminder and an invoice template, for Google Sheets and Excel. <a href="{KIT}">See what is inside</a> · <a href="{BUY}">Buy, £9</a></div>'

# ---------------- uk-money-calcs ----------------
CALC_PAGES = {}
def build_calcs(B):
    d = f"{B}/uk-money-calcs/site"; N = "UK Money Calcs"
    TAXJS = "function tx(t){let pa=12570;if(t>100000)pa=Math.max(0,pa-(t-100000)/2);let x=Math.max(0,t-pa),b=Math.min(x,37700),a=Math.max(0,t-125140),h=Math.max(0,x-b-a);return [b*.2+h*.4+a*.45,pa]}function V(i){return +document.getElementById(i).value}function F(n){return '£'+Math.round(n).toLocaleString('en-GB')}"
    pages = {}
    faq = [("How much tax does a self-employed person pay in 2026/27?", "In England, Wales and Northern Ireland you pay Income Tax on profits above the £12,570 Personal Allowance at 20% up to £50,270, 40% up to £125,140 and 45% above. You also pay Class 4 National Insurance of 6% on profits between £12,570 and £50,270 and 2% above £50,270."),
           ("Do I still pay Class 2 National Insurance?", "No, not if your profits are £7,105 or more. GOV.UK says Class 2 is treated as paid to protect your National Insurance record. Below £7,105 you can choose to pay voluntary Class 2 at £3.65 a week in 2026/27."),
           ("Is tax worked out on turnover or profit?", "On profit: your self-employed income minus allowable expenses. You can use the £1,000 trading allowance instead of claiming expenses."),
           ("Does this cover Scotland?", "No. Scotland has different Income Tax bands. Class 4 National Insurance is the same across the UK.")]
    pages["self-employed-tax-calculator.html"] = ("Self-Employed Tax Calculator 2026/27 (Income Tax + Class 4 NI)", "Estimate Income Tax and Class 4 National Insurance on your sole trader profits for 2026/27 (England, Wales and NI).", f"""
<h1>Self-employed tax calculator 2026/27</h1><p>Enter your expected profit (income minus allowable expenses) for 6 April 2026 to 5 April 2027.</p><div class=card>
<label>Annual turnover £ <input id=t type=number value=45000></label> <label>Allowable expenses £ <input id=e type=number value=5000></label><br><br>
<label>Other taxable income (e.g. a salary) £ <input id=o2 type=number value=0></label><br><br><button onclick=c()>Calculate</button><div id=o></div></div>
<script>{TAXJS}
function c(){{let p=Math.max(0,V('t')-V('e')),oth=V('o2'),all=tx(p+oth)[0],base=tx(oth)[0],it=all-base,c4=Math.max(0,Math.min(p,50270)-12570)*.06+Math.max(0,p-50270)*.02;
o.innerHTML=`<table><tr><td>Profit</td><td>${{F(p)}}</td></tr><tr><td>Income Tax on profit</td><td>${{F(it)}}</td></tr><tr><td>Class 4 NI</td><td>${{F(c4)}}</td></tr><tr><td><b>Total tax and NI</b></td><td><b>${{F(it+c4)}}</b></td></tr><tr><td>Set aside per month</td><td>${{F((it+c4)/12)}}</td></tr></table><p>Turnover over £30,000? You may need <a href="{KIT}guide-mtd.html">Making Tax Digital for Income Tax</a> from April 2027.</p>`}}c()</script>
<h2>2026/27 rates used</h2><table><tr><th>Item</th><th>2026/27</th></tr><tr><td>Personal Allowance</td><td>£12,570 (reduced by £1 for every £2 of adjusted net income over £100,000)</td></tr><tr><td>Basic / higher / additional rate</td><td>20% to £50,270 · 40% to £125,140 · 45% above</td></tr><tr><td>Class 4 NI</td><td>6% on £12,570–£50,270 · 2% above</td></tr><tr><td>Class 2 NI</td><td>Treated as paid if profits £7,105+; voluntary £3.65/week below</td></tr></table>
<p>Simplification: Class 4 is worked out on profit alone. When you have a salary too, the extra Income Tax is shown as the tax on (salary + profit) minus the tax on salary alone. Payments on account are not included.</p>
{src("it","seni")}{KITBOX}{related([("take-home-pay.html","Take-home pay calculator (employees)"),("dividend-tax-calculator.html","Dividend tax calculator"),("vat-threshold-checker.html","VAT threshold checker (£90,000)"),(KIT+"guide-payments-on-account.html","Payments on account explained"),(KIT+"guide-mtd.html","Making Tax Digital for Income Tax: who and when")])}""", faq)

    faq = [("What is the dividend allowance for 2026/27?", "£500. You pay no tax on the first £500 of dividends, though they still count towards your tax band."),
           ("What are the dividend tax rates for 2026/27?", "GOV.UK lists 10.75% for the basic rate, 35.75% for the higher rate and 39.35% for the additional rate, from 6 April 2026 to 5 April 2027."),
           ("Do I pay tax on dividends in an ISA?", "No. Dividends from shares held in an ISA are tax-free."),
           ("Do I pay National Insurance on dividends?", "No. National Insurance is not charged on dividends, which is why many company directors take a small salary and the rest as dividends.")]
    pages["dividend-tax-calculator.html"] = ("Dividend Tax Calculator 2026/27 UK", "Work out tax on dividends for 2026/27 using the £500 allowance and the 10.75%, 35.75% and 39.35% rates.", f"""
<h1>Dividend tax calculator 2026/27</h1><div class=card>
<label>Salary and other non-dividend income £ <input id=s type=number value=12570></label><br><br><label>Dividends £ <input id=dv type=number value=30000></label><br><br><button onclick=c()>Calculate</button><div id=o></div></div>
<script>{TAXJS}
function c(){{let s=V('s'),dv=V('dv'),pa=tx(s+dv)[1],nt=Math.max(0,s-pa),dt=Math.max(0,dv-Math.max(0,pa-s)),bb=37700,ab=125140-pa,pos=nt,t=0,rem=dt;
let al=Math.min(500,rem);pos+=al;rem-=al;
let seg=(cap,r)=>{{let x=Math.max(0,Math.min(rem,cap-pos));t+=x*r;pos+=x;rem-=x}};seg(bb,.1075);seg(Math.max(bb,ab),.3575);seg(1e12,.3935);
o.innerHTML=`<h2>Dividend tax: ${{F(t)}}</h2><p>Personal Allowance used: ${{F(pa)}}. Taxable dividends after allowance: ${{F(Math.max(0,dt-500))}}. Effective rate on dividends: ${{dv?(t/dv*100).toFixed(1):0}}%.</p>`}}c()</script>
<h2>How it works</h2><p>Your Personal Allowance is used against salary first, then dividends. The first £500 of dividends is taxed at 0% but still uses up band. Dividends that fall in the basic band are taxed at 10.75%, the higher band at 35.75% and the additional band at 39.35%. This does not work out the Income Tax on your salary itself. Scotland: dividend rates are UK-wide, but this tool uses the rUK bands to decide which band applies.</p>
<p>Example from GOV.UK: £29,570 wages and £3,000 dividends gives £0 on £500 and 10.75% on £2,500 of dividends.</p>
{src("div","it")}{related([("self-employed-tax-calculator.html","Self-employed tax calculator"),("take-home-pay.html","Take-home pay calculator"),(KIT,"UK Sole Trader Kit (spreadsheet)")])}""", faq)

    faq = [("What are the student loan repayment thresholds?", "GOV.UK currently shows yearly thresholds of £26,900 (Plan 1), £29,385 (Plan 2), £33,795 (Plan 4), £25,000 (Plan 5) and £21,000 (Postgraduate Loan). The page does not label these with a tax year, so check GOV.UK if you are planning for a later year."),
           ("How much do I repay?", "9% of income over the threshold on Plans 1, 2, 4 and 5, and 6% over the threshold on a Postgraduate Loan."),
           ("I have a plan and a Postgraduate Loan. Do I pay both?", "Yes. The Postgraduate Loan 6% is charged on top of the 9% for your undergraduate plan."),
           ("Does the amount I owe change my repayments?", "No. Repayments depend only on your income, not on your balance.")]
    pages["student-loan-repayment-calculator.html"] = ("Student Loan Repayment Calculator UK (Plan 1, 2, 4, 5, Postgrad)", "Work out your student loan repayments per year and per month from your income and plan type.", f"""
<h1>Student loan repayment calculator</h1><div class=card>
<label>Annual income before tax £ <input id=s type=number value=40000></label><br><br>
<label>Plan <select id=p><option value=0>None</option><option value=1>Plan 1</option><option value=2 selected>Plan 2</option><option value=4>Plan 4 (Scotland)</option><option value=5>Plan 5</option></select></label>
<label><input type=checkbox id=pg> Also a Postgraduate Loan</label><br><br><button onclick=c()>Calculate</button><div id=o></div></div>
<script>function F(n){{return '£'+Math.round(n).toLocaleString('en-GB')}}const T={{1:26900,2:29385,4:33795,5:25000}};
function c(){{let s=+document.getElementById('s').value,p=+document.getElementById('p').value,u=p?Math.max(0,s-T[p])*.09:0,g=document.getElementById('pg').checked?Math.max(0,s-21000)*.06:0;
o.innerHTML=`<table><tr><th></th><th>Year</th><th>Month</th></tr><tr><td>Undergraduate plan</td><td>${{F(u)}}</td><td>${{F(u/12)}}</td></tr><tr><td>Postgraduate Loan</td><td>${{F(g)}}</td><td>${{F(g/12)}}</td></tr><tr><td><b>Total</b></td><td><b>${{F(u+g)}}</b></td><td><b>${{F((u+g)/12)}}</b></td></tr></table>`}}c()</script>
<table><tr><th>Plan</th><th>Yearly threshold</th><th>Rate</th></tr><tr><td>Plan 1</td><td>£26,900</td><td>9%</td></tr><tr><td>Plan 2</td><td>£29,385</td><td>9%</td></tr><tr><td>Plan 4</td><td>£33,795</td><td>9%</td></tr><tr><td>Plan 5</td><td>£25,000</td><td>9%</td></tr><tr><td>Postgraduate</td><td>£21,000</td><td>6%</td></tr></table>
<p><b>Note:</b> these are the thresholds GOV.UK shows today. The GOV.UK page does not label them with a tax year, so we have not been able to confirm them as 2026/27 figures. Employers deduct repayments based on each pay period, so a bonus month can cost more than this annual estimate. If you have more than one undergraduate plan, you repay 9% over the lowest threshold.</p>
{src("sl")}{related([("take-home-pay.html","Take-home pay calculator"),("self-employed-tax-calculator.html","Self-employed tax calculator")])}""", faq)

    faq = [("What is the VAT registration threshold?", "£90,000 of taxable turnover. You must register if your total taxable turnover for the last 12 months goes over £90,000, or if you expect it to go over £90,000 in the next 30 days alone."),
           ("Is it a rolling 12 months or the tax year?", "It is a rolling 12 months, not the tax year or your accounting year. Check it at the end of every month."),
           ("Can I register voluntarily below £90,000?", "Yes. GOV.UK allows voluntary registration if your turnover is under £90,000."),
           ("What counts as taxable turnover?", "The total value of everything you sell that is not VAT exempt, including zero-rated sales.")]
    pages["vat-threshold-checker.html"] = ("VAT Threshold Checker UK: Rolling 12-Month £90,000 Test", "Enter your last 12 months of sales to check whether you have gone over the £90,000 VAT registration threshold.", f"""
<h1>VAT threshold checker (£90,000)</h1><p>Enter your taxable turnover for each of the last 12 months, newest last.</p><div class=card id=m></div><div class=card><button onclick=c()>Check</button><div id=o></div></div>
<script>let h='';for(let i=1;i<=12;i++)h+=`<label>M${{i}} £ <input class=mm type=number value=6000 style="width:100px"></label> `;m.innerHTML=h;
function c(){{let v=[...document.querySelectorAll('.mm')].map(x=>+x.value),s=v.reduce((a,b)=>a+b,0),left=90000-s;
o.innerHTML=s>90000?`<h2>Over the threshold: £${{s.toLocaleString('en-GB')}}</h2><p>You must register for VAT. GOV.UK says to register within 30 days of the end of the month you went over.</p>`:`<h2>£${{s.toLocaleString('en-GB')}} in the last 12 months</h2><p>£${{left.toLocaleString('en-GB')}} below the threshold. Check again at each month end. If you expect more than £90,000 in the next 30 days alone, you must register straight away.</p>`}}c()</script>
{src("vat")}<p>Need to add or remove VAT from a price? Use the <a href="vat.html">VAT calculator</a>.</p>{related([("vat.html","VAT calculator"),("self-employed-tax-calculator.html","Self-employed tax calculator"),(KIT,"UK Sole Trader Kit")])}""", faq)

    faq = [("What are the Income Tax bands for 2026/27?", "In England, Wales and Northern Ireland: Personal Allowance up to £12,570 at 0%, basic rate £12,571 to £50,270 at 20%, higher rate £50,271 to £125,140 at 40%, and additional rate over £125,140 at 45%."),
           ("What are employee National Insurance rates for 2026/27?", "For category A employees: 8% on earnings between £242.01 and £967 a week (£1,048.01 to £4,189 a month), and 2% above £967 a week."),
           ("What happens to the Personal Allowance over £100,000?", "It goes down by £1 for every £2 of adjusted net income over £100,000, so it is zero at £125,140 or above."),
           ("Are Scottish bands different?", "Yes. Scotland has its own Income Tax bands; this page covers the rest of the UK.")]
    pages["income-tax-bands-2026-27.html"] = ("Income Tax and National Insurance Rates 2026/27 (UK)", "2026/27 Income Tax bands, Personal Allowance, employee and self-employed National Insurance and dividend rates, with GOV.UK sources.", f"""
<h1>Income Tax and NI rates 2026/27</h1><p>The 2026/27 tax year runs from 6 April 2026 to 5 April 2027.</p>
<h2>Income Tax (England, Wales, NI)</h2><table><tr><th>Band</th><th>Taxable income</th><th>Rate</th></tr><tr><td>Personal Allowance</td><td>Up to £12,570</td><td>0%</td></tr><tr><td>Basic</td><td>£12,571–£50,270</td><td>20%</td></tr><tr><td>Higher</td><td>£50,271–£125,140</td><td>40%</td></tr><tr><td>Additional</td><td>Over £125,140</td><td>45%</td></tr></table>
<h2>Employee National Insurance (category A)</h2><table><tr><th>Weekly earnings</th><th>Monthly</th><th>Rate</th></tr><tr><td>£129–£242</td><td>£559–£1,048</td><td>0%</td></tr><tr><td>£242.01–£967</td><td>£1,048.01–£4,189</td><td>8%</td></tr><tr><td>Over £967</td><td>Over £4,189</td><td>2%</td></tr></table>
<h2>Self-employed National Insurance</h2><p>Class 4: 6% on profits £12,570–£50,270, 2% above. Class 2 is treated as paid at profits of £7,105 or more; the voluntary rate is £3.65 a week.</p>
<h2>Dividends</h2><p>£500 allowance; 10.75% basic, 35.75% higher, 39.35% additional.</p>
<h2>Calculators</h2><p><a href="take-home-pay.html">Take-home pay</a> · <a href="self-employed-tax-calculator.html">Self-employed tax</a> · <a href="dividend-tax-calculator.html">Dividend tax</a> · <a href="student-loan-repayment-calculator.html">Student loan</a> · <a href="vat-threshold-checker.html">VAT threshold</a></p>
{src("it","ni","seni","div")}""", faq)
    for k, (t, ds, b, f) in pages.items(): wpage(d, k, t + " | " + N, ds, b, N, f)
    return pages

# ---------------- uk-freelancer-kit ----------------
def build_kit(B):
    d = f"{B}/uk-freelancer-kit/site"; N = "UK Freelancer Kit"; P = {}
    mtdrel = related([("guide-mtd.html","MTD for Income Tax: who needs it and when"),("guide-mtd-quarterly-deadlines.html","MTD quarterly update deadlines"),("guide-mtd-software.html","MTD software: spreadsheets and bridging"),("guide-self-assessment-deadlines.html","Self Assessment deadlines 2026/27"),(CALCS+"self-employed-tax-calculator.html","Self-employed tax calculator 2026/27")])
    faq = [("Who needs Making Tax Digital for Income Tax?", "Sole traders and landlords registered for Self Assessment whose qualifying income (self-employment plus property income before expenses) is over the threshold for the relevant tax year."),
           ("When do I have to start MTD for Income Tax?", "From 6 April 2026 if your qualifying income was over £50,000 in 2024/25; from 6 April 2027 if over £30,000 in 2025/26; and from 6 April 2028 if over £20,000 in 2026/27."),
           ("Is qualifying income my profit or turnover?", "Turnover. GOV.UK defines qualifying income as total self-employment and property income before expenses, based on the tax return for the earlier tax year."),
           ("Does MTD apply to partnerships?", "Not yet. GOV.UK says partnerships will need to use it in future and HMRC will set out the timeline later."),
           ("Do I still file a tax return?", "Yes. You still submit a Self Assessment tax return for the year before you start, and the quarterly updates are summaries, not tax returns."),
           ("Can I be exempt?", "Possibly, for example if you are digitally excluded. Exempt people still file a normal Self Assessment return. Check the GOV.UK exemptions guidance.")]
    P["guide-mtd.html"] = ("Making Tax Digital for Income Tax 2026: who needs it and when", "MTD for Income Tax thresholds and start dates: £50,000 from April 2026, £30,000 from April 2027, £20,000 from April 2028.", f"""
<h1>Making Tax Digital for Income Tax: who needs it and when</h1>
<p>Making Tax Digital (MTD) for Income Tax means keeping digital records and sending HMRC a quarterly update from compatible software. It applies to sole traders and landlords registered for Self Assessment.</p>
<h2>Start dates and thresholds</h2><table><tr><th>Qualifying income over</th><th>Measured in tax year</th><th>Must use MTD from</th></tr><tr><td>£50,000</td><td>2024/25</td><td>6 April 2026</td></tr><tr><td>£30,000</td><td>2025/26</td><td>6 April 2027</td></tr><tr><td>£20,000</td><td>2026/27</td><td>6 April 2028</td></tr></table>
<p><b>Qualifying income is turnover, not profit:</b> your total self-employment and property income before expenses. Example: £32,000 freelance turnover plus £8,000 rent is £40,000 qualifying income, so you would be in scope from April 2027 if that was your 2025/26 position.</p>
<h2>What you need to do</h2><ol><li>Keep digital records of income and expenses.</li><li>Send a quarterly update for each business (see <a href="guide-mtd-quarterly-deadlines.html">deadlines</a>).</li><li>Submit your tax return by 31 January after the tax year.</li><li>Use <a href="guide-mtd-software.html">compatible software</a>; spreadsheets plus bridging software are allowed.</li></ol>
<p>To sign up you must be registered for Self Assessment and have submitted a return in the last 2 years. HMRC will not give penalty points for late quarterly updates during 2026/27.</p>
{src("mtd","qi","qu")}{KITBOX}{mtdrel}""", faq)
    faq = [("What are the MTD quarterly update deadlines?", "7 August, 7 November, 7 February and 7 May (the following tax year). The deadlines are the same whether you use standard or calendar update periods."),
           ("What periods do the updates cover?", "Standard periods are cumulative from 6 April: to 5 July, 5 October, 5 January and 5 April. Calendar periods run from 1 April and end on 30 June, 30 September, 31 December and 31 March."),
           ("What if I miss a quarterly deadline?", "From 2027/28 each late update gets a penalty point, and 4 points brings a £200 penalty. HMRC will not apply penalty points for late quarterly updates in 2026/27."),
           ("Can I send updates early or more often?", "Yes. You can send one any time between the end of the period and the deadline, and you can send more often as long as each update covers the full period from the start of the year.")]
    P["guide-mtd-quarterly-deadlines.html"] = ("MTD for Income Tax quarterly update deadlines 2026/27", "Making Tax Digital quarterly update dates: 7 August, 7 November, 7 February and 7 May, with standard and calendar periods.", f"""
<h1>MTD quarterly update deadlines</h1><table><tr><th>Standard period (tax year)</th><th>Calendar period</th><th>Deadline</th></tr>
<tr><td>6 April – 5 July</td><td>1 April – 30 June</td><td>7 August</td></tr><tr><td>6 April – 5 October</td><td>1 April – 30 September</td><td>7 November</td></tr><tr><td>6 April – 5 January</td><td>1 April – 31 December</td><td>7 February</td></tr><tr><td>6 April – 5 April</td><td>1 April – 31 March</td><td>7 May (following tax year)</td></tr></table>
<p>For 2026/27 that means 7 August 2026, 7 November 2026, 7 February 2027 and 7 May 2027. Updates are cumulative summaries of income and expenses, not tax returns. You cannot switch between standard and calendar periods after sending a quarterly update for that year. Your return is still due by <a href="guide-self-assessment-deadlines.html">31 January</a>.</p>
<p>A monthly habit makes this easy: log income and expenses every month in one sheet with SA103 categories, and each quarter is a copy-and-submit job.</p>
{src("qu")}{KITBOX}{mtdrel}""", faq)
    faq = [("Do I have to buy accounting software for MTD?", "No. You need software that is compatible with MTD for Income Tax. That can be bookkeeping software or bridging software connected to your spreadsheets."),
           ("What is bridging software?", "Software that connects to records you already keep in spreadsheets or other tools and sends your submissions to HMRC."),
           ("Is free MTD software available?", "GOV.UK says free products are available for people with simple tax affairs, though they may have limits, such as a cap on transactions."),
           ("Where do I find a list of compatible software?", "On the GOV.UK page 'Find software that's compatible with Making Tax Digital for Income Tax', which includes a filter tool.")]
    P["guide-mtd-software.html"] = ("MTD for Income Tax software: can I use a spreadsheet?", "Yes, with bridging software. How to choose MTD-compatible software for Income Tax as a sole trader or landlord.", f"""
<h1>MTD software: spreadsheets, bridging and free options</h1>
<p>HMRC does not provide its own software for MTD for Income Tax. You choose a product from the GOV.UK list. There are two main types:</p>
<ul><li><b>Bookkeeping software</b> holds your records and sends your updates to HMRC.</li><li><b>Bridging software</b> connects to records you keep in spreadsheets and sends the updates. GOV.UK says this explicitly: if you use spreadsheets to record income and expenses, bridging software can connect to them and make your submissions.</li></ul>
<h2>How to choose</h2><ul><li>Does it support your income types: self-employment, UK property, or both?</li><li>Can it send quarterly updates <i>and</i> the end-of-year return?</li><li>Price: GOV.UK notes free products exist for simple tax affairs, but they may cap transactions.</li><li>Does it work with how you keep records today?</li></ul>
<p>If you prefer spreadsheets, keep income and expenses in consistent SA103 categories so the bridging tool can map them cleanly.</p>
{src("sw","mtd")}{KITBOX}{mtdrel}""", faq)
    faq = [("When is the 2025/26 Self Assessment deadline?", "Paper returns by 31 October 2026, online returns by 11:59pm on 31 January 2027, and any tax owed paid by 31 January 2027."),
           ("When must I register for Self Assessment?", "By 5 October after the end of the tax year you need to file for, for example 5 October 2026 for 2025/26."),
           ("Is there a July payment?", "Yes, if you make payments on account. The second payment is due by 31 July."),
           ("I registered late. When is my deadline?", "If you register after 5 October 2026, you must still pay what you owe by 31 January 2027.")]
    P["guide-self-assessment-deadlines.html"] = ("Self Assessment deadlines 2026/27: 31 January 2027 and more", "Self Assessment key dates: register by 5 October 2026, paper return 31 October 2026, online return and payment 31 January 2027, payment on account 31 July.", f"""
<h1>Self Assessment deadlines (2025/26 return)</h1><table><tr><th>What</th><th>Deadline</th></tr><tr><td>Register for Self Assessment (new)</td><td>5 October 2026</td></tr><tr><td>Paper tax return</td><td>31 October 2026</td></tr><tr><td>Online tax return</td><td>11:59pm, 31 January 2027</td></tr><tr><td>Pay tax owed + 1st payment on account for 2026/27</td><td>31 January 2027</td></tr><tr><td>2nd payment on account</td><td>31 July 2027</td></tr></table>
<p>Miss the online deadline and you can get a late filing penalty. If you are in MTD for Income Tax, quarterly updates also apply: see the <a href="guide-mtd-quarterly-deadlines.html">MTD deadlines</a>.</p>
{src("sa","poa")}{KITBOX}{related([("guide-payments-on-account.html","Payments on account explained"),(CALCS+"self-employed-tax-calculator.html","Self-employed tax calculator"),("guide-allowable-expenses.html","Allowable expenses")])}""", faq)
    faq = [("What are payments on account?", "Advance payments towards your next tax bill, each normally half of last year's bill, due by 31 January and 31 July."),
           ("Who does not have to make payments on account?", "You do not if last year's Self Assessment bill was less than £1,000, or if you paid more than 80% of the tax you owed through your tax code or other deductions."),
           ("What is a balancing payment?", "If your tax for the year is more than your 2 payments on account, you pay the difference by 31 January the following year."),
           ("Why is my first January bill so big?", "In your first year with a bill over £1,000, the 31 January payment includes the full bill for last year plus the first payment on account for this year.")]
    P["guide-payments-on-account.html"] = ("Payments on account explained (UK sole traders, 2026)", "How Self Assessment payments on account work, when they are due (31 January and 31 July) and the £1,000 and 80% exemptions.", f"""
<h1>Payments on account explained</h1><p>Payments on account are 2 advance payments towards your tax bill, each normally half of your previous year's bill. They are due by midnight on <b>31 January</b> and <b>31 July</b>. They do not apply if last year's bill was under £1,000, or if more than 80% of your tax was already collected at source.</p>
<h2>Worked example</h2><p>Your 2025/26 bill is £4,000 and you have not paid on account before. By 31 January 2027 you pay £4,000 plus a £2,000 first payment on account for 2026/27, so £6,000. By 31 July 2027 you pay another £2,000. If your 2026/27 bill turns out to be £5,000, you pay a £1,000 balancing payment by 31 January 2028, plus the first payment on account for 2027/28.</p>
<p>Work out your likely bill with the <a href="{CALCS}self-employed-tax-calculator.html">self-employed tax calculator</a>, then set aside a monthly amount.</p>
{src("poa","sa")}{KITBOX}{related([("guide-self-assessment-deadlines.html","Self Assessment deadlines"),("guide-mtd.html","MTD for Income Tax")])}""", faq)
    faq = [("What is the mileage rate for self-employed people in 2026/27?", "55p per mile for the first 10,000 business miles in a car or goods vehicle, then 25p. Motorcycles are 24p. Before 6 April 2026 the first-10,000-miles rate was 45p."),
           ("Can I claim the mileage rate and fuel costs too?", "No. The flat rate replaces actual vehicle costs such as fuel, insurance and repairs, and you cannot use it for a vehicle you have already claimed capital allowances on."),
           ("Is commuting allowed?", "No. Normal commuting is not a business journey."),
           ("What records do I need?", "A log of your business miles: date, journey, purpose and miles.")]
    P["guide-mileage-allowance.html"] = ("Self-employed mileage rate 2026/27: 55p per mile", "Simplified expenses for vehicles in 2026/27: 55p a mile for the first 10,000 business miles, then 25p; motorcycles 24p.", f"""
<h1>Self-employed mileage allowance 2026/27</h1><table><tr><th>Vehicle</th><th>2026/27</th><th>Before 6 April 2026</th></tr><tr><td>Car or goods vehicle, first 10,000 miles</td><td>55p</td><td>45p</td></tr><tr><td>Car or goods vehicle, after 10,000 miles</td><td>25p</td><td>25p</td></tr><tr><td>Motorcycle</td><td>24p</td><td>24p</td></tr></table>
<p>Example from GOV.UK: 11,000 business miles = 10,000 × 55p (£5,500) + 1,000 × 25p (£250) = £5,750.</p>
<p>The flat rate covers all running costs. You cannot also claim fuel or repairs, or use it for a vehicle you have claimed capital allowances on.</p>
{src("mi")}{KITBOX}{related([("guide-allowable-expenses.html","Allowable expenses for sole traders"),(CALCS+"self-employed-tax-calculator.html","Self-employed tax calculator")])}""", faq)
    faq = [("What expenses can sole traders claim?", "Costs incurred wholly and exclusively for the business: office costs, business travel (not commuting), uniforms, staff, stock, financial costs, premises, marketing and training for your current business."),
           ("What is the trading allowance?", "Your first £1,000 of self-employment income is tax-free. You can claim it instead of your actual expenses, but not both."),
           ("Can I use flat rates instead of actual costs?", "Yes, simplified expenses cover vehicles (55p a mile for the first 10,000 miles in 2026/27), working from home and living at your business premises.")]
    P["guide-allowable-expenses.html"] = ("Allowable expenses for UK sole traders (2026 guide)", "Which costs you can claim on Self Assessment, simplified expenses and the £1,000 trading allowance.", f"""
<h1>Allowable expenses for sole traders</h1><p>Common categories: office costs, travel (not commuting), clothing (uniforms only), staff, stock, financial costs, premises, marketing, and training related to your current business. Instead of actual costs you can use simplified expenses: <a href="guide-mileage-allowance.html">55p a mile</a> for the first 10,000 business miles in 2026/27 (45p before 6 April 2026), then 25p, plus flat-rate working-from-home allowances. Or you can claim the £1,000 trading allowance instead of expenses.</p>
<div class=card><b>GOV.UK sources (checked 15 October 2026):</b><ul><li><a href="https://www.gov.uk/expenses-if-youre-self-employed" rel="nofollow">https://www.gov.uk/expenses-if-youre-self-employed</a></li><li><a href="{G['mi']}" rel="nofollow">{G['mi']}</a></li><li><a href="{G['it']}" rel="nofollow">{G['it']}</a></li></ul></div>{KITBOX}{related([(CALCS+"self-employed-tax-calculator.html","Self-employed tax calculator"),("guide-mtd.html","MTD for Income Tax")])}""", faq)
    for k, (t, ds, b, f) in P.items(): wpage(d, k, t, ds, b, N, f)
    return P

# ---------------- selfhost-ai-dir ----------------
def build_ai(B):
    d = f"{B}/selfhost-ai-dir/site"; N = "SelfHostAI"; P = {}
    gh = lambda r, n: f'<a href="https://github.com/{r}" rel="nofollow">{n}</a>'
    faq = [("What is the easiest self-hosted ChatGPT alternative?", "For a single machine, Ollama to run models plus Open WebUI as the chat interface is the most common setup. Jan is a desktop app if you do not want Docker."),
           ("Do I need a GPU?", "Not for small quantised models: llama.cpp and Ollama can run them on CPU, but slowly. For larger models or several users, a GPU makes a big difference."),
           ("Can I use cloud APIs from the same interface?", "Yes. Open WebUI, LibreChat and AnythingLLM can connect to OpenAI-compatible APIs as well as local models.")]
    P["best-self-hosted-chatgpt-alternatives.html"] = ("Best self-hosted ChatGPT alternatives (2026)", "Open-source, self-hostable ChatGPT alternatives: Open WebUI, LibreChat, AnythingLLM, Jan and the runtimes behind them.", f"""
<h1>Best self-hosted ChatGPT alternatives</h1><p>A self-hosted ChatGPT setup needs two parts: a <b>model runtime</b> and a <b>chat interface</b>.</p>
<table><tr><th>Tool</th><th>Type</th><th>Licence</th><th>Best for</th></tr>
<tr><td><a href="tool-open-webui.html">Open WebUI</a></td><td>Chat UI</td><td>BSD-3</td><td>ChatGPT-style UI for Ollama and APIs</td></tr>
<tr><td><a href="tool-librechat.html">LibreChat</a></td><td>Chat UI</td><td>MIT</td><td>Multi-provider chat with agents</td></tr>
<tr><td><a href="tool-anything-llm.html">AnythingLLM</a></td><td>RAG app</td><td>MIT</td><td>Chat with your documents</td></tr>
<tr><td><a href="tool-jan.html">Jan</a></td><td>Desktop app</td><td>Apache-2.0</td><td>Offline, no server</td></tr>
<tr><td><a href="tool-ollama.html">Ollama</a></td><td>Runtime</td><td>MIT</td><td>One-command local models</td></tr></table>
<h2>Typical stack</h2><p>Laptop: Jan, or Ollama + Open WebUI. Small team on a VPS: Ollama or <a href="tool-vllm.html">vLLM</a> + LibreChat or Open WebUI, with <a href="tool-langfuse.html">Langfuse</a> for observability. See <a href="ollama-vs-llama-cpp-vs-vllm.html">Ollama vs llama.cpp vs vLLM</a>.</p>""", faq)
    faq = [("Should I use Ollama or llama.cpp?", "Ollama is easier: one command to pull and run models, with an API. llama.cpp is the lower-level C/C++ engine, which gives more control and runs well on CPU."),
           ("When should I use vLLM?", "When you serve many concurrent requests on a GPU. vLLM is built for high-throughput serving rather than single-user desktop use."),
           ("Do they offer an OpenAI-compatible API?", "All three can expose an HTTP API that many OpenAI-compatible clients can use. Check each project's docs for the exact endpoints.")]
    P["ollama-vs-llama-cpp-vs-vllm.html"] = ("Ollama vs llama.cpp vs vLLM: which local LLM runtime?", "Compare Ollama, llama.cpp and vLLM for running LLMs locally or on a server.", f"""
<h1>Ollama vs llama.cpp vs vLLM</h1><table><tr><th></th><th><a href="tool-ollama.html">Ollama</a></th><th><a href="tool-llama.cpp.html">llama.cpp</a></th><th><a href="tool-vllm.html">vLLM</a></th></tr>
<tr><td>Best for</td><td>Easiest local setup</td><td>CPU, edge devices, full control</td><td>High-throughput GPU serving</td></tr><tr><td>Hardware</td><td>CPU or GPU</td><td>CPU or GPU</td><td>GPU</td></tr><tr><td>Licence</td><td>MIT</td><td>MIT</td><td>Apache-2.0</td></tr><tr><td>Repo</td><td>{gh("ollama/ollama","ollama/ollama")}</td><td>{gh("ggml-org/llama.cpp","ggml-org/llama.cpp")}</td><td>{gh("vllm-project/vllm","vllm-project/vllm")}</td></tr></table>
<p>Rule of thumb: start with Ollama, drop to llama.cpp when you need fine control or very low resources, and move to vLLM when many users hit one GPU server. <a href="tool-localai.html">LocalAI</a> is another OpenAI-compatible option. Add a UI from the <a href="best-self-hosted-chatgpt-alternatives.html">ChatGPT alternatives</a> list.</p>""", faq)
    faq = [("Open WebUI or LibreChat?", "Open WebUI is the usual choice alongside Ollama for a polished single-team UI. LibreChat is strong when you mix many API providers and want agents."),
           ("What about chatting with my documents?", "AnythingLLM is built around RAG over your files. Open WebUI also offers document features. For a vector database, see Qdrant."),
           ("Which is fully MIT licensed?", "LibreChat and AnythingLLM are listed as MIT. Open WebUI is listed as BSD-3; check its repository for any branding terms.")]
    P["open-webui-vs-librechat-vs-anythingllm.html"] = ("Open WebUI vs LibreChat vs AnythingLLM (self-hosted chat UIs)", "Compare three popular self-hosted AI chat interfaces by use case and licence.", f"""
<h1>Open WebUI vs LibreChat vs AnythingLLM</h1><table><tr><th></th><th><a href="tool-open-webui.html">Open WebUI</a></th><th><a href="tool-librechat.html">LibreChat</a></th><th><a href="tool-anything-llm.html">AnythingLLM</a></th></tr>
<tr><td>Focus</td><td>ChatGPT-style UI, Ollama-friendly</td><td>Multi-provider chat + agents</td><td>All-in-one RAG over documents</td></tr><tr><td>Licence (as listed)</td><td>BSD-3</td><td>MIT</td><td>MIT</td></tr><tr><td>Repo</td><td>{gh("open-webui/open-webui","open-webui")}</td><td>{gh("danny-avila/LibreChat","LibreChat")}</td><td>{gh("Mintplex-Labs/anything-llm","anything-llm")}</td></tr></table>
<p>All three run in Docker on a modest VPS. The model runtime is the heavy part: see <a href="ollama-vs-llama-cpp-vs-vllm.html">runtimes compared</a>. For document search at scale add <a href="tool-qdrant.html">Qdrant</a>.</p>""", faq)
    for k, (t, ds, b, f) in P.items(): wpage(d, k, t + " | " + N, ds, b, N, f, foot="ai")
    return P

def build(B):
    return build_calcs(B), build_kit(B), build_ai(B)
