# Agent-readiness layer, added 15 Oct 2026. Runs after gen.py + seo_pages.py.
# Adds: llms.txt, llms-full.txt, page.html.md twins, JSON-LD graph, direct answers, formula/examples
# blocks on calculators, static rates JSON + OpenAPI, AI-crawler robots.txt and a full sitemap.
# Standard library only (runs on the plain Actions runner).
import os, re, json, html
from html.parser import HTMLParser
R = "https://andreiturcea-creator.github.io"
DATE, DATE_H = "2026-10-15", "15 October 2026"
BUY = "https://turceapaul.gumroad.com/l/bmykeg"
SITES = {
 "uk-money-calcs": dict(name="UK Money Calcs", gov=True, summary="Free UK personal-finance calculators for the 2026/27 tax year (England, Wales and Northern Ireland): take-home pay, self-employed tax, dividend tax, student loan repayments, Stamp Duty Land Tax, VAT and the VAT registration threshold. Each calculator page states its formula, rates and worked examples in plain text, with GOV.UK sources."),
 "uk-freelancer-kit": dict(name="UK Freelancer Kit", gov=True, summary="Free guides for UK sole traders on Making Tax Digital for Income Tax, Self Assessment deadlines, payments on account, mileage and allowable expenses (2026/27), plus the UK Sole Trader Kit, a £9 Google Sheets/Excel income, expenses and tax-estimate spreadsheet sold on Gumroad."),
 "selfhost-ai-dir": dict(name="SelfHostAI", gov=False, summary="A curated directory of open-source AI tools you can self-host (LLM runtimes, chat UIs, agent builders, RAG, vector databases, speech and image generation), with licence, category, GitHub repository and alternatives for each tool, plus comparison guides."),
}
G = {"it":"https://www.gov.uk/income-tax-rates","ni":"https://www.gov.uk/national-insurance-rates-letters","seni":"https://www.gov.uk/self-employed-national-insurance-rates",
 "div":"https://www.gov.uk/tax-on-dividends","sl":"https://www.gov.uk/repaying-your-student-loan/what-you-pay","vat":"https://www.gov.uk/vat-registration/when-to-register",
 "vatr":"https://www.gov.uk/vat-rates","sdlt":"https://www.gov.uk/stamp-duty-land-tax/residential-property-rates","hol":"https://www.gov.uk/holiday-entitlement-rights",
 "mtd":"https://www.gov.uk/guidance/check-if-youre-eligible-for-making-tax-digital-for-income-tax","qi":"https://www.gov.uk/guidance/work-out-your-qualifying-income-for-making-tax-digital-for-income-tax",
 "qu":"https://www.gov.uk/guidance/use-making-tax-digital-for-income-tax/send-quarterly-updates","sa":"https://www.gov.uk/self-assessment-tax-returns/deadlines",
 "poa":"https://www.gov.uk/understand-self-assessment-bill/payments-on-account","mi":"https://www.gov.uk/simpler-income-tax-simplified-expenses/vehicles","exp":"https://www.gov.uk/expenses-if-youre-self-employed"}

# ---------- direct answers (1-2 sentences, shown first under the H1) ----------
ANS = {
 "uk-money-calcs": {
  "index.html":"Free UK calculators for 2026/27: take-home pay, self-employed tax, dividend tax, student loan, Stamp Duty and VAT. Every calculator states its formula, rates and worked examples in plain text, with GOV.UK sources.",
  "take-home-pay.html":"On a £35,000 salary in 2026/27 (England, Wales, NI, no pension or student loan) you take home about £28,720 a year (£2,393 a month) after £4,486 Income Tax and £1,794 National Insurance. Tax is 20% from £12,570 to £50,270, 40% to £125,140 and 45% above; employee NI is 8% then 2%.",
  "stamp-duty.html":"In England and Northern Ireland, Stamp Duty Land Tax is 0% up to £125,000, 2% to £250,000, 5% to £925,000, 10% to £1.5 million and 12% above; a £295,000 home costs £4,750. First-time buyers pay nothing up to £300,000 and 5% from £300,001 to £500,000; additional homes pay 5% on top of each band.",
  "vat.html":"UK VAT is 20% standard, 5% reduced and 0% zero-rated. To add 20% VAT multiply by 1.2; to remove it divide by 1.2 (so £120 gross is £100 net plus £20 VAT).",
  "pro-rata-salary.html":"Pro rata salary = full-time salary × your hours ÷ full-time hours. A £30,000 full-time salary at 22.5 of 37.5 hours a week is £18,000 a year.",
  "self-employed-tax-calculator.html":"In 2026/27 a sole trader in England, Wales or NI pays Income Tax of 20% on profit from £12,570 to £50,270 (40% to £125,140, 45% above) plus Class 4 NI of 6% on £12,570 to £50,270 and 2% above. On £40,000 profit that is £5,486 tax plus £1,646 Class 4 NI, £7,132 in total.",
  "dividend-tax-calculator.html":"For 2026/27 the first £500 of dividends is tax-free, then dividends are taxed at 10.75% (basic band), 35.75% (higher) and 39.35% (additional). GOV.UK's example of £29,570 wages and £3,000 dividends gives £268.75 of dividend tax.",
  "student-loan-repayment-calculator.html":"You repay 9% of income above your plan threshold (Plan 1 £26,900, Plan 2 £29,385, Plan 4 £33,795, Plan 5 £25,000) and 6% above £21,000 for a Postgraduate Loan. These are the thresholds GOV.UK shows today; GOV.UK does not label them with a tax year, so they are not confirmed as 2026/27 figures.",
  "vat-threshold-checker.html":"You must register for VAT if your taxable turnover over the last rolling 12 months goes over £90,000, or you expect more than £90,000 in the next 30 days alone. Add up the last 12 months at every month end.",
  "income-tax-bands-2026-27.html":"For 2026/27 (6 April 2026 to 5 April 2027) in England, Wales and NI: Personal Allowance £12,570, basic rate 20% to £50,270, higher rate 40% to £125,140, additional rate 45% above. Employee NI is 8% then 2%, Class 4 NI 6% then 2%, and dividends are taxed at 10.75%, 35.75% and 39.35% after a £500 allowance.",
  "about.html":"UK Money Calcs is an independent site of free UK tax and money calculators, with rates checked against GOV.UK. It is not financial advice; affiliate links, if any, are labelled.",
 },
 "uk-freelancer-kit": {
  "index.html":"The UK Sole Trader Kit is a £9 spreadsheet (Google Sheets and Excel) with an income log, expenses mapped to HMRC SA103 categories, a 2026/27 tax and Class 4 NI estimate, a payments-on-account reminder and an invoice template. Buy it on Gumroad; the free guides below cover MTD, deadlines and expenses.",
  "guide-mtd.html":"Making Tax Digital for Income Tax applies from 6 April 2026 if your qualifying income (self-employment plus property income before expenses) was over £50,000 in 2024/25, from 6 April 2027 if over £30,000 in 2025/26, and from 6 April 2028 if over £20,000 in 2026/27.",
  "guide-mtd-quarterly-deadlines.html":"MTD for Income Tax quarterly updates are due by 7 August, 7 November, 7 February and 7 May. For 2026/27 that is 7 August 2026, 7 November 2026, 7 February 2027 and 7 May 2027.",
  "guide-mtd-software.html":"Yes, you can keep using a spreadsheet for MTD for Income Tax if you connect it to HMRC-compatible bridging software. HMRC does not provide its own software; pick a product from the GOV.UK compatible-software list.",
  "guide-self-assessment-deadlines.html":"For the 2025/26 tax return: register by 5 October 2026, file a paper return by 31 October 2026, and file online and pay by 31 January 2027. The second payment on account is due by 31 July 2027.",
  "guide-payments-on-account.html":"Payments on account are 2 advance payments towards your next tax bill, each normally half of last year's bill, due by 31 January and 31 July. You do not make them if last year's bill was under £1,000 or more than 80% of your tax was collected at source.",
  "guide-mileage-allowance.html":"For 2026/27 self-employed people can claim 55p a mile for the first 10,000 business miles in a car or van and 25p after that (motorcycles 24p). The first-10,000-miles rate was 45p before 6 April 2026.",
  "guide-allowable-expenses.html":"Sole traders can deduct costs incurred wholly and exclusively for the business, such as office costs, business travel, stock, staff, premises, marketing and financial costs. Alternatively use simplified expenses, or the £1,000 trading allowance instead of actual expenses.",
  "about.html":"UK Freelancer Kit sells a £9 spreadsheet template for UK sole traders and publishes free guides. Templates only, not tax advice.",
 },
 "selfhost-ai-dir": {
  "index.html":"SelfHostAI lists 16 open-source AI tools you can run on your own machine or VPS, such as Ollama, Open WebUI, vLLM, llama.cpp, n8n, Dify and Qdrant, with licence, category and GitHub link for each.",
  "best-self-hosted-chatgpt-alternatives.html":"The most common self-hosted ChatGPT alternative is Ollama (to run models) plus Open WebUI (the chat interface); LibreChat suits multi-provider setups, AnythingLLM chatting with documents, and Jan a desktop app with no server.",
  "ollama-vs-llama-cpp-vs-vllm.html":"Use Ollama for the easiest local setup, llama.cpp for CPU, edge devices and fine control, and vLLM for high-throughput GPU serving to many users.",
  "open-webui-vs-librechat-vs-anythingllm.html":"Open WebUI is the usual ChatGPT-style UI for Ollama, LibreChat is best for mixing many API providers with agents, and AnythingLLM is built around chatting with your documents (RAG).",
  "about.html":"SelfHostAI is an agent-maintained directory of self-hostable open-source AI tools, using data from the public GitHub API. Sponsored listings are always labelled.",
  "advertise.html":"Featured listings will cost £49 a month and are always labelled 'Featured'. Bookings are not open yet.",
 },
}
H2MAP = {"How it works":"How is it calculated?","2026/27 rates used":"What 2026/27 rates does it use?","Start dates and thresholds":"When does MTD for Income Tax start, and at what income?",
 "What you need to do":"What do you need to do?","Worked example":"How do payments on account work in practice?","Typical stack":"What does a typical self-hosted stack look like?",
 "How to choose":"How do you choose MTD software?","Quick start":"How do you self-host it?","Alternatives":"What are the alternatives?",
 "Income Tax (England, Wales, NI)":"What are the Income Tax bands for 2026/27?","Employee National Insurance (category A)":"What are employee National Insurance rates for 2026/27?",
 "Self-employed National Insurance":"What National Insurance do self-employed people pay?","Dividends":"What are the dividend tax rates for 2026/27?","Calculators":"Which calculators use these rates?",
 "Free guides":"Which free guides are available?","Free calculators":"Which free calculators go with the kit?","Guides":"Which comparison guides are available?","Categories":"Which tool categories are covered?",
 "New for 2026/27":"Which 2026/27 calculators are new?","FAQs":"Frequently asked questions"}

# ---------- calculator maths (mirrors the page JavaScript) ----------
def it_tax(t):
    pa=12570
    if t>100000: pa=max(0,pa-(t-100000)/2)
    x=max(0,t-pa); b=min(x,37700); a=max(0,t-125140); h=max(0,x-b-a)
    return b*.2+h*.4+a*.45, pa
def ee_ni(g): return max(0,min(g,50270)-12570)*.08+max(0,g-50270)*.02
def c4(p): return max(0,min(p,50270)-12570)*.06+max(0,p-50270)*.02
def band(v,B):
    t=prev=0
    for cap,r in B:
        if v>prev: t+=(min(v,cap)-prev)*r
        prev=cap
    return t
STD=[(125000,0),(250000,.02),(925000,.05),(1500000,.10),(1e12,.12)]
def sdlt(v,k):
    if k=="f" and v<=500000: return band(v,[(300000,0),(500000,.05)])
    if k=="a": return band(v,[(c,r+.05) for c,r in STD])
    return band(v,STD)
def divtax(s,dv):
    pa=it_tax(s+dv)[1]; pos=max(0,s-pa); dt=max(0,dv-max(0,pa-s)); ab=125140-pa; rem=dt; t=0
    al=min(500,rem); pos+=al; rem-=al
    for cap,r in [(37700,.1075),(max(37700,ab),.3575),(1e12,.3935)]:
        x=max(0,min(rem,cap-pos)); t+=x*r; pos+=x; rem-=x
    return t
SLT={"Plan 1":26900,"Plan 2":29385,"Plan 4":33795,"Plan 5":25000}
def gbp(n,dp=0): return f"£{n:,.{dp}f}"
def tbl(head,rows): return "<table><tr>"+"".join(f"<th>{h}</th>" for h in head)+"</tr>"+"".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)+"</table>"
def srcs(*k): return "<p>GOV.UK sources (checked "+DATE_H+"): "+" · ".join(f'<a href="{G[x]}" rel="nofollow">{G[x]}</a>' for x in k)+"</p>"
def calc_block(fn):
    F,RT,EX,NOTE,S=None,None,None,"",()
    if fn=="take-home-pay.html":
        F="Take-home = gross salary − pension (salary sacrifice) − Income Tax − employee National Insurance − student loan. Income Tax = 20% of income from £12,570 to £50,270 + 40% from £50,270 to £125,140 + 45% above (the £12,570 Personal Allowance falls by £1 for every £2 over £100,000). Employee NI = 8% of earnings from £12,570 to £50,270 + 2% above. Student loan = 9% (6% Postgraduate) of income above the plan threshold."
        RT=tbl(["Item","2026/27 (England, Wales, NI)"],[["Personal Allowance","£12,570 (tapered above £100,000)"],["Basic rate","20% on £12,571–£50,270"],["Higher rate","40% on £50,271–£125,140"],["Additional rate","45% over £125,140"],["Employee NI (category A)","8% on £12,570–£50,270 a year; 2% above"]])
        rows=[]
        for s in [20000,35000,50000,60000,100000]:
            t=it_tax(s)[0]; n=ee_ni(s); rows.append([gbp(s),gbp(t),gbp(n),gbp(s-t-n),gbp((s-t-n)/12)])
        EX=tbl(["Gross salary","Income Tax","Employee NI","Take-home a year","Take-home a month"],rows)
        NOTE="Examples assume no pension, no student loan, tax code 1257L and an even annual salary. NI is worked out on annual thresholds (£12,570 / £50,270); payroll uses weekly or monthly thresholds (£242 / £967 a week), so real payslips can differ by a few pounds. Scotland is not covered."; S=("it","ni","sl")
    elif fn=="stamp-duty.html":
        F="SDLT is charged in slices: 0% on the first £125,000, 2% on £125,001–£250,000, 5% on £250,001–£925,000, 10% on £925,001–£1.5m and 12% above. First-time buyers (price up to £500,000): 0% up to £300,000 and 5% on £300,001–£500,000. Additional residential property: add 5 percentage points to every slice."
        RT=tbl(["Portion of price","Standard rate","Additional property","First-time buyer (price ≤ £500,000)"],[["Up to £125,000","0%","5%","0%"],["£125,001–£250,000","2%","7%","0%"],["£250,001–£300,000","5%","10%","0%"],["£300,001–£500,000","5%","10%","5%"],["£500,001–£925,000","5%","10%","relief not available"],["£925,001–£1.5m","10%","15%","relief not available"],["Over £1.5m","12%","17%","relief not available"]])
        EX=tbl(["Price","Buyer","SDLT"],[[gbp(v),lab,gbp(sdlt(v,k))] for v,k,lab in [(295000,"m","Moving home (GOV.UK example)"),(500000,"f","First-time buyer (GOV.UK example)"),(400000,"m","Moving home"),(250000,"a","Additional property"),(1000000,"m","Moving home")]])
        NOTE="Rates in force from 1 April 2025, checked against GOV.UK on "+DATE_H+". Not covered: the 2% non-UK-resident surcharge, leasehold rent (net present value), companies, and Scotland (LBTT) or Wales (LTT)."; S=("sdlt",)
    elif fn=="vat.html":
        F="Add VAT: gross = net × (1 + rate). Remove VAT: net = gross ÷ (1 + rate); VAT = gross − net. At 20%, divide a VAT-inclusive price by 1.2 (do not subtract 20%)."
        RT=tbl(["Rate","Applies to"],[["20% standard","Most goods and services"],["5% reduced","Some goods and services, e.g. home energy, children's car seats"],["0% zero","Zero-rated goods, e.g. most food and children's clothes"]])
        EX=tbl(["Starting amount","Action","Net","VAT","Gross"],[["£100.00","Add 20%","£100.00","£20.00","£120.00"],["£120.00","Remove 20%","£100.00","£20.00","£120.00"],["£99.99","Remove 20%","£83.33","£16.67","£99.99"],["£200.00","Add 5%","£200.00","£10.00","£210.00"]])
        NOTE="VAT registration threshold: £90,000 taxable turnover over a rolling 12 months (see the VAT threshold checker)."; S=("vatr","vat")
    elif fn=="pro-rata-salary.html":
        F="Pro rata salary = full-time salary × (your hours per week ÷ full-time hours per week). The same works with days: full-time salary × (your days ÷ full-time days). Statutory holiday = 5.6 weeks × your working days per week."
        RT=tbl(["Item","Value"],[["Statutory holiday entitlement","5.6 weeks a year (capped at 28 days)"]])
        EX=tbl(["Full-time salary","Full-time week","Your week","Pro rata salary"],[["£30,000","37.5 hours","22.5 hours","£18,000"],["£25,000","5 days","3 days","£15,000"],["£42,000","40 hours","30 hours","£31,500"],["£36,000","37.5 hours","15 hours","£14,400"]])
        NOTE="Holiday example: 3 days a week × 5.6 = 16.8 days. The 5.6-week figure is long-standing statutory entitlement but was not part of tonight's GOV.UK rate check; confirm on GOV.UK."; S=("hol",)
    elif fn=="self-employed-tax-calculator.html":
        F="Profit = turnover − allowable expenses. Income Tax = 20% of profit from £12,570 to £50,270 + 40% to £125,140 + 45% above (Personal Allowance tapers by £1 per £2 over £100,000). Class 4 NI = 6% of profit from £12,570 to £50,270 + 2% above. With other income, the extra Income Tax = tax on (other income + profit) − tax on other income alone."
        rows=[]
        for p in [20000,30000,40000,60000,110000]:
            t=it_tax(p)[0]; n=c4(p); rows.append([gbp(p),gbp(t),gbp(n),gbp(t+n),gbp((t+n)/12)])
        RT=None; EX=tbl(["Profit (no other income)","Income Tax","Class 4 NI","Total","Set aside a month"],rows)
        NOTE="Class 2 NI is treated as paid at profits of £7,105 or more (voluntary £3.65 a week below). Payments on account are not included. Scotland Income Tax bands are not covered."; S=("it","seni")
    elif fn=="dividend-tax-calculator.html":
        F="Personal Allowance is used against salary first, then dividends. The first £500 of dividends is taxed at 0% but still uses band. Remaining dividends are taxed at 10.75% within the basic band (first £37,700 of taxable income), 35.75% up to £125,140 total income and 39.35% above."
        RT=tbl(["Item","2026/27"],[["Dividend allowance","£500"],["Basic rate","10.75%"],["Higher rate","35.75%"],["Additional rate","39.35%"]])
        EX=tbl(["Salary / other income","Dividends","Dividend tax"],[[gbp(s),gbp(d),gbp(divtax(s,d),2)] for s,d in [(29570,3000),(12570,30000),(50270,10000),(0,20000),(12570,60000)]])
        NOTE="First row is GOV.UK's own example. Tax on the salary itself is not included."; S=("div","it")
    elif fn=="student-loan-repayment-calculator.html":
        F="Yearly repayment = 9% × (income − plan threshold) for Plans 1, 2, 4 and 5, plus 6% × (income − £21,000) for a Postgraduate Loan. Nothing is due below the threshold. The balance owed does not affect repayments."
        RT=None
        EX=tbl(["Income","Plan","Yearly","Monthly"],[[gbp(s),pl,gbp(r),gbp(r/12)] for s,pl,r in [(40000,"Plan 2",(40000-29385)*.09),(30000,"Plan 1",(30000-26900)*.09),(50000,"Plan 5",(50000-25000)*.09),(35000,"Postgraduate only",(35000-21000)*.06),(25000,"Plan 2",0)]])
        NOTE="UNCONFIRMED FOR 2026/27: thresholds are as shown on GOV.UK on "+DATE_H+", but GOV.UK does not label them with a tax year."; S=("sl",)
    elif fn=="vat-threshold-checker.html":
        F="Add up taxable turnover (everything not VAT-exempt, including zero-rated sales) for the last 12 months. If the total is over £90,000 you must register within 30 days of the end of that month. You must also register straight away if you expect more than £90,000 in the next 30 days alone."
        RT=tbl(["Rule","2026/27"],[["Registration threshold","£90,000 rolling 12 months"],["Forward-look test","more than £90,000 in the next 30 days alone"],["Voluntary registration","allowed below £90,000"]])
        EX=tbl(["Last 12 months","Total","Result"],[["£6,000 every month","£72,000","Below: £18,000 headroom"],["£7,500 every month","£90,000","Not over (must go over £90,000)"],["£8,000 every month","£96,000","Over: register within 30 days of month end"],["£5,000 × 11, then £40,000","£95,000","Over: register within 30 days of month end"]])
        S=("vat",)
    if not F: return ""
    o=f'<section id="formula-and-rates"><h2 id="how-is-it-calculated-plain-text">What is the formula, in plain text?</h2><p>{F}</p>'
    if RT: o+=f'<h2 id="rates-and-thresholds">What rates and thresholds apply?</h2>{RT}'
    o+=f'<h2 id="worked-examples">What are some worked examples?</h2>{EX}'
    if NOTE: o+=f"<p>{NOTE}</p>"
    return o+srcs(*S)+'<p>Machine-readable rates: <a href="api/rates-2026-27.json">api/rates-2026-27.json</a>.</p></section>'

# ---------- rates JSON ----------
def money_json():
    return {"name":"UK Money Calcs rates and thresholds 2026/27","tax_year":"2026/27","tax_year_start":"2026-04-06","tax_year_end":"2027-04-05","scope":"England, Wales and Northern Ireland unless stated","checked_against_govuk":DATE,"last_modified":DATE,
     "income_tax":{"personal_allowance":12570,"personal_allowance_taper":{"starts_above_adjusted_net_income":100000,"reduction":"£1 for every £2","zero_at":125140},
       "bands":[{"name":"basic","from":12571,"to":50270,"rate":0.20},{"name":"higher","from":50271,"to":125140,"rate":0.40},{"name":"additional","from":125141,"to":None,"rate":0.45}],"source":G["it"],"status":"confirmed"},
     "employee_ni_class1_category_a":{"weekly":{"primary_threshold":242,"upper_earnings_limit":967,"main_rate":0.08,"upper_rate":0.02},"monthly":{"primary_threshold":1048,"upper_earnings_limit":4189},"annual_approximation_used_by_calculator":{"from":12570,"to":50270},"source":G["ni"],"status":"confirmed"},
     "self_employed_ni":{"class4":{"lower_profits_limit":12570,"upper_profits_limit":50270,"main_rate":0.06,"upper_rate":0.02},"class2":{"small_profits_threshold":7105,"treated_as_paid_at_or_above_threshold":True,"voluntary_weekly_rate":3.65},"source":G["seni"],"status":"confirmed"},
     "dividends":{"allowance":500,"basic_rate":0.1075,"higher_rate":0.3575,"additional_rate":0.3935,"source":G["div"],"status":"confirmed"},
     "student_loans":{"thresholds_yearly":{"plan_1":26900,"plan_2":29385,"plan_4":33795,"plan_5":25000,"postgraduate":21000},"rates":{"plans_1_2_4_5":0.09,"postgraduate":0.06},"source":G["sl"],"status":"UNCONFIRMED for 2026/27: shown on GOV.UK on "+DATE+" but not labelled with a tax year"},
     "vat":{"registration_threshold":90000,"test":"rolling 12 months, or expected to exceed in next 30 days alone","rates":{"standard":0.20,"reduced":0.05,"zero":0.0},"sources":[G["vat"],G["vatr"]],"status":"confirmed"},
     "sdlt_england_ni_residential":{"effective_from":"2025-04-01","bands":[{"to":125000,"rate":0},{"to":250000,"rate":0.02},{"to":925000,"rate":0.05},{"to":1500000,"rate":0.10},{"to":None,"rate":0.12}],
       "first_time_buyer":{"max_price":500000,"bands":[{"to":300000,"rate":0},{"to":500000,"rate":0.05}]},"additional_property_surcharge":0.05,"non_uk_resident_surcharge":0.02,"note":"Non-resident surcharge not applied by the calculator","source":G["sdlt"],"status":"confirmed"},
     "disclaimer":"Estimates for information only, not financial or tax advice."}
def kit_json():
    return {"name":"UK Freelancer Kit sole-trader rates, thresholds and deadlines 2026/27","tax_year":"2026/27","checked_against_govuk":DATE,"last_modified":DATE,
     "mtd_income_tax":{"qualifying_income":"self-employment plus property income before expenses (turnover)","phases":[{"threshold_over":50000,"measured_tax_year":"2024/25","start":"2026-04-06"},{"threshold_over":30000,"measured_tax_year":"2025/26","start":"2027-04-06"},{"threshold_over":20000,"measured_tax_year":"2026/27","start":"2028-04-06"}],
       "quarterly_update_deadlines_2026_27":["2026-08-07","2026-11-07","2027-02-07","2027-05-07"],"penalty_points":"not applied for late quarterly updates in 2026/27; from 2027/28 4 points = £200","sources":[G["mtd"],G["qi"],G["qu"]],"status":"confirmed"},
     "self_assessment_2025_26_return":{"register_by":"2026-10-05","paper_return":"2026-10-31","online_return_and_payment":"2027-01-31","second_payment_on_account":"2027-07-31","source":G["sa"],"status":"confirmed"},
     "payments_on_account":{"due":["31 January","31 July"],"each":"half of previous year's bill","not_required_if":["previous bill under £1,000","more than 80% of tax collected at source"],"source":G["poa"],"status":"confirmed"},
     "mileage_simplified_expenses":{"car_or_goods_vehicle_first_10000_miles":0.55,"car_or_goods_vehicle_after_10000_miles":0.25,"motorcycle":0.24,"first_10000_rate_before_2026_04_06":0.45,"source":G["mi"],"status":"confirmed"},
     "trading_allowance":{"amount":1000,"source":G["exp"],"status":"confirmed"},
     "income_tax":{"personal_allowance":12570,"basic":{"to":50270,"rate":0.20},"higher":{"to":125140,"rate":0.40},"additional_rate":0.45,"source":G["it"],"status":"confirmed"},
     "class4_ni":{"from":12570,"to":50270,"main_rate":0.06,"upper_rate":0.02,"source":G["seni"],"status":"confirmed"},
     "product":{"name":"UK Sole Trader Kit","price":9,"currency":"GBP","url":BUY}}

def openapi(site,name,path,desc):
    return {"openapi":"3.1.0","info":{"title":name+" static data","version":DATE,"description":"Static, read-only JSON files. No authentication, no parameters."},
     "servers":[{"url":f"{R}/{site}"}],"paths":{"/"+path:{"get":{"operationId":"getData","summary":desc,"responses":{"200":{"description":"JSON document","content":{"application/json":{}}}}}}}}

# ---------- HTML -> Markdown ----------
class MD(HTMLParser):
    def __init__(s,base):
        super().__init__(convert_charrefs=True); s.base=base; s.o=[]; s.skip=0; s.href=[]; s.lst=[]; s.tbl=None; s.cell=None; s.ina=0
    def w(s,t):
        if s.cell is not None: s.cell.append(t)
        else: s.o.append(t)
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in("script","style","select","label","noscript") or (t=="input"): 
            if t!="input": s.skip+=1
            return
        if s.skip: return
        if t=="button" and not s.ina: s.skip+=1; s._btn=True; return
        if t in("h1","h2","h3"): s.w("\n\n"+"#"*int(t[1])+" ")
        elif t in("p","div","section"): s.w("\n\n")
        elif t=="br": s.w("  \n")
        elif t in("ul","ol"): s.lst.append([t,0]); s.w("\n")
        elif t=="li":
            l=s.lst[-1] if s.lst else ["ul",0]; l[1]+=1; s.w("\n"+("  "*(len(s.lst)-1))+(f"{l[1]}. " if l[0]=="ol" else "- "))
        elif t in("b","strong"): s.w("**")
        elif t=="i": s.w("_")
        elif t=="a":
            h=a.get("href",""); 
            if h and not re.match(r"https?:|mailto:",h): h=s.base+h
            s.href.append(h); s.ina+=1; s.w("[")
        elif t=="table": s.tbl=[]
        elif t=="tr" and s.tbl is not None: s.tbl.append([])
        elif t in("td","th") and s.tbl is not None: s.cell=[]
    def handle_endtag(s,t):
        if t in("script","style","select","label","noscript"):
            s.skip=max(0,s.skip-1); return
        if t=="button" and getattr(s,"_btn",False): s.skip=max(0,s.skip-1); s._btn=False; return
        if s.skip: return
        if t in("h1","h2","h3","p"): s.w("\n")
        elif t in("ul","ol"):
            if s.lst: s.lst.pop()
            s.w("\n")
        elif t in("b","strong"): s.w("**")
        elif t=="i": s.w("_")
        elif t=="a":
            h=s.href.pop() if s.href else ""; s.ina=max(0,s.ina-1); s.w(f"]({h})")
        elif t in("td","th") and s.tbl is not None and s.cell is not None:
            c=re.sub(r"\s+"," ","".join(s.cell)).strip().replace("|","\\|"); s.cell=None
            if s.tbl: s.tbl[-1].append(c)
        elif t=="table" and s.tbl is not None:
            rows=[r for r in s.tbl if r]; s.tbl=None
            if rows:
                n=max(len(r) for r in rows); rows=[r+[""]*(n-len(r)) for r in rows]
                s.o.append("\n\n| "+" | ".join(rows[0])+" |\n|"+"---|"*n+"\n"+"".join("| "+" | ".join(r)+" |\n" for r in rows[1:])+"\n")
    def handle_data(s,d):
        if s.skip: return
        if s.cell is None and s.tbl is not None: return
        s.w(re.sub(r"\s+"," ",d))
def to_md(body,base):
    p=MD(base); p.feed(body); t="".join(p.o)
    t=re.sub(r"\[\s*\]\([^)]*\)","",t); t=re.sub(r"[ \t]+\n","\n",t); t=re.sub(r"\n[ \t]+(?=[^\s-]|\d)","\n",t); t=re.sub(r"\n{3,}","\n\n",t)
    return t.strip()+"\n"

def slug(s): return re.sub(r"-+","-",re.sub(r"[^a-z0-9]+","-",html.unescape(re.sub("<[^>]+>","",s)).lower())).strip("-")[:60]
def nonscript(h,f):
    parts=re.split(r"(<script.*?</script>)",h,flags=re.S)
    return "".join(p if p.startswith("<script") else f(p) for p in parts)
def fix_heads(h):
    seen=set()
    def rep(m):
        tag,attrs,txt=m.group(1),m.group(2),m.group(3)
        if "id=" in attrs or not txt.strip(): return m.group(0)
        txt=H2MAP.get(txt,txt) if tag=="h2" else txt
        i=slug(txt) or tag; base=i; n=2
        while i in seen: i=f"{base}-{n}"; n+=1
        seen.add(i); return f'<{tag} id="{i}"{attrs}>{txt}</{tag}>'
    return nonscript(h,lambda p: re.sub(r"<(h[23])((?:\s[^>]*)?)>(.*?)</\1>",rep,p,flags=re.S))

def kind(site,fn):
    if site=="uk-money-calcs" and fn not in("index.html","about.html","income-tax-bands-2026-27.html"): return "calc"
    if fn.startswith("guide-") or fn in("income-tax-bands-2026-27.html","best-self-hosted-chatgpt-alternatives.html","ollama-vs-llama-cpp-vs-vllm.html","open-webui-vs-librechat-vs-anythingllm.html"): return "article"
    return "page"

def graph(site,fn,title,desc,h1,k):
    S=SITES[site]; base=f"{R}/{site}/"; url=base+("" if fn=="index.html" else fn)
    org={"@type":"Organization","@id":base+"#org","name":S["name"],"url":base}
    g=[{"@type":"WebSite","@id":base+"#website","name":S["name"],"url":base,"description":S["summary"],"inLanguage":"en-GB","publisher":{"@id":base+"#org"}},org,
       {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"en-GB","isPartOf":{"@id":base+"#website"},"datePublished":DATE,"dateModified":DATE,"lastReviewed":DATE,
        "breadcrumb":{"@id":url+"#breadcrumb"},"encoding":{"@type":"MediaObject","contentUrl":base+fn+".md","encodingFormat":"text/markdown"}},
       {"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":[{"@type":"ListItem","position":1,"name":S["name"],"item":base}]+([] if fn=="index.html" else [{"@type":"ListItem","position":2,"name":h1,"item":url}])}]
    if k=="calc":
        g.append({"@type":"WebApplication","@id":url+"#app","name":h1,"url":url,"description":desc,"applicationCategory":"FinanceApplication","operatingSystem":"Any (runs in a web browser)","browserRequirements":"Requires JavaScript",
                  "isAccessibleForFree":True,"offers":{"@type":"Offer","price":"0","priceCurrency":"GBP"},"publisher":{"@id":base+"#org"},"dateModified":DATE})
    if k=="article":
        g.append({"@type":"Article","@id":url+"#article","headline":h1[:110],"description":desc,"url":url,"mainEntityOfPage":{"@id":url+"#webpage"},"datePublished":DATE,"dateModified":DATE,"author":{"@id":base+"#org"},"publisher":{"@id":base+"#org"},"inLanguage":"en-GB"})
    if site=="uk-freelancer-kit" and fn=="index.html":
        g.append({"@type":"Product","@id":base+"#product","name":"UK Sole Trader Kit","description":"Google Sheets and Excel kit for UK sole traders: income log, expenses mapped to HMRC SA103 categories, 2026/27 tax and Class 4 NI estimate, payments-on-account reminder and invoice template.",
                  "brand":{"@type":"Brand","name":"UK Freelancer Kit"},"category":"Spreadsheet template","url":base,
                  "offers":{"@type":"Offer","price":"9.00","priceCurrency":"GBP","url":BUY,"availability":"https://schema.org/InStock","seller":{"@id":base+"#org"}}})
    j={"@context":"https://schema.org","@graph":g}
    return '<script type="application/ld+json">'+json.dumps(j,ensure_ascii=False).replace("</","<\\/")+'</script>'

def process_site(B,site):
    d=f"{B}/{site}/site"; S=SITES[site]; base=f"{R}/{site}/"; pages=[]
    checked=(f"Last checked against GOV.UK: <time datetime=\"{DATE}\">{DATE_H}</time>" if S["gov"] else "No tax figures on this site, so no GOV.UK check applies; tool details come from each project's public GitHub repository")
    for fn in sorted(f for f in os.listdir(d) if f.endswith(".html")):
        h=open(f"{d}/{fn}").read()
        title=html.unescape(re.search(r"<title>(.*?)</title>",h,re.S).group(1))
        m=re.search(r'<meta name="description" content="(.*?)">',h); desc=html.unescape(m.group(1)) if m else title
        h1=html.unescape(re.sub("<[^>]+>","",re.search(r"<h1[^>]*>(.*?)</h1>",h,re.S).group(1)))
        k=kind(site,fn); url=base+("" if fn=="index.html" else fn)
        head=f'<link rel="alternate" type="text/markdown" href="{fn}.md" title="Markdown version"><meta property="article:modified_time" content="{DATE}">'+graph(site,fn,title,desc,h1,k)
        if 'rel="canonical"' not in h: head=f'<link rel="canonical" href="{url}">'+head
        h=h.replace("</head>",head+"</head>",1)
        ans=ANS[site].get(fn) or desc
        top=(f'<p id="answer" class="answer"><b>Short answer:</b> {html.escape(ans)}</p>'
             f'<p id="last-updated" style="font-size:.85rem;color:#555">Last updated: <time datetime="{DATE}">{DATE_H}</time> · {checked} · <a href="{fn}.md">Markdown version</a></p>')
        h=re.sub(r"(</h1>)",r"\1"+top.replace("\\","\\\\"),h,count=1)
        cb=calc_block(fn) if k=="calc" else ""
        if cb:
            h=h.replace("<h2>FAQs</h2>",cb+"<h2>FAQs</h2>",1) if "<h2>FAQs</h2>" in h else h.replace("\n<footer>",cb+"\n<footer>",1)
        h=fix_heads(h)
        open(f"{d}/{fn}","w").write(h)
        body=h.split("</header>",1)[1].split("<footer>",1)[0]
        md=f"# {title}\n\nSource: {url}\nLast updated: {DATE}"+(f" · Last checked against GOV.UK: {DATE}" if S["gov"] else "")+"\n\n"+re.sub(r"^# .*\n","",to_md(body,base),count=1)
        md=md+"\n---\nDisclaimer: estimates for information only, not financial, tax or legal advice.\n" if S["gov"] else md
        open(f"{d}/{fn}.md","w").write(md)
        pages.append((fn,title,desc,k,md))
    os.makedirs(f"{d}/api",exist_ok=True); extra=[]
    if site=="uk-money-calcs": data,jp,jd=money_json(),"api/rates-2026-27.json","UK 2026/27 Income Tax, NI, dividend, student loan, VAT and SDLT rates and thresholds with GOV.UK sources and checked date"
    elif site=="uk-freelancer-kit": data,jp,jd=kit_json(),"api/rates-2026-27.json","Sole trader 2026/27 MTD thresholds, quarterly and Self Assessment deadlines, payments on account, mileage rates, with GOV.UK sources and checked date"
    else:
        tools=json.load(open(f"{B}/selfhost-ai-dir/data/tools.json"))
        data,jp,jd={"name":"SelfHostAI tools","last_modified":DATE,"source":"public GitHub repositories","count":len(tools),"tools":[dict(t,page=f"{base}tool-{t['repo'].split('/')[1].lower()}.html",github=f"https://github.com/{t['repo']}") for t in tools]},"api/tools.json","All listed self-hostable AI tools with category, licence, GitHub repo and page URL"
    json.dump(data,open(f"{d}/{jp}","w"),indent=1,ensure_ascii=False)
    json.dump(openapi(site,S["name"],jp,jd),open(f"{d}/openapi.json","w"),indent=1)
    # llms.txt
    groups={"calc":"Calculators","article":"Guides","page":"Pages"}
    L=[f"# {S['name']}","",f"> {S['summary']}","",f"Last updated {DATE}."+(f" Tax figures checked against GOV.UK on {DATE} (2026/27 tax year). Student loan thresholds are as shown on GOV.UK but not confirmed as 2026/27 figures." if site=="uk-money-calcs" else (f" Figures checked against GOV.UK on {DATE}." if S["gov"] else ""))+" Every page has a Markdown twin at the same URL plus `.md`. Information only, not financial or tax advice.",""]
    if site=="uk-freelancer-kit": L+=[f"Product: UK Sole Trader Kit, £9 GBP, buy at {BUY}",""]
    for kk in ("calc","article","page"):
        it=[p for p in pages if p[3]==kk and p[0] not in ("about.html","privacy.html","cookies.html","affiliate-disclosure.html") and not (site=="selfhost-ai-dir" and kk=="page" and (p[0].startswith("tool-") or p[0].startswith("cat-")))]
        if it: L+=[f"## {groups[kk]}",""]+[f"- [{p[1].split(' | ')[0]}]({base}{p[0]}.md): {p[2]}" for p in it]+[""]
    if site=="selfhost-ai-dir":
        L+=["## Tools",""]+[f"- [{p[1].split(':')[0]}]({base}{p[0]}.md): {p[2]}" for p in pages if p[0].startswith("tool-")]+["","## Categories",""]+[f"- [{p[1].split('|')[0].strip()}]({base}{p[0]}.md): {p[2]}" for p in pages if p[0].startswith("cat-")]+[""]
    L+=["## Data",""f"",f"- [{jp}]({base}{jp}): {jd}",f"- [openapi.json]({base}openapi.json): OpenAPI 3.1 description of the static JSON file",f"- [llms-full.txt]({base}llms-full.txt): full plain-text content of every page",""]
    L+=["## Optional","",f"- [About]({base}about.html.md): who runs the site and disclosures",f"- [Privacy]({base}privacy.html.md): privacy notice (no analytics, no ads, no personal data collected)",f"- [Cookies]({base}cookies.html.md): cookie notice (no cookies set)",f"- [Affiliate disclosure]({base}affiliate-disclosure.html.md): how affiliate and referral links are labelled",f"- [Sitemap]({base}sitemap.xml): all URLs",""]
    open(f"{d}/llms.txt","w").write("\n".join(L))
    open(f"{d}/llms-full.txt","w").write(f"# {S['name']}: full content\n\n> {S['summary']}\n\nGenerated {DATE}. Each section below is one page.\n\n"+"\n\n".join(f"<!-- {base}{p[0]} -->\n"+p[4] for p in pages))
    # sitemap + robots
    urls=[("" if f=="index.html" else f) for f in sorted(x for x in os.listdir(d) if x.endswith(".html"))]+[p[0]+".md" for p in pages]+["llms.txt","llms-full.txt",jp,"openapi.json"]
    open(f"{d}/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{base}{u}</loc><lastmod>{DATE}</lastmod></url>" for u in urls)+"</urlset>\n")
    bots=["GPTBot","OAI-SearchBot","ChatGPT-User","ClaudeBot","Claude-User","Claude-SearchBot","PerplexityBot","Perplexity-User","Google-Extended","Applebot","Applebot-Extended","CCBot","Bingbot","Googlebot"]
    open(f"{d}/robots.txt","w").write("# AI assistants and search crawlers are welcome. Plain-text versions: llms.txt, llms-full.txt and <page>.html.md\n\n"+"".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)+"User-agent: *\nAllow: /\n\n"+f"Sitemap: {base}sitemap.xml\n")

def build(B):
    for s in SITES: process_site(B,s)
