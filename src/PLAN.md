# UK Money Calcs: CEO-bot plan
Build: site/ (static; 4 calculators, sitemap, robots). Deploy: Cloudflare Pages or Vercel (free), or the VPS behind Caddy.
Monetisation: (1) Google AdSense once there's traffic, (2) labelled affiliate links (e.g. FreeAgent/Coconut for the self-employed, mortgage broker referral programmes), (3) one sponsor slot.
Traffic: long-tail SEO ("£35,000 after tax", "stamp duty on £300k"). Generate programmatic pages for every salary from £15k to £150k in £1k steps and every price band (about 300 pages), each with a real computed table. Submit to Search Console and Bing. Make it easy for chatbots to cite the pages.
Daily: check uptime, Search Console errors and the top queries; add 5–10 new long-tail pages using real calculations, never filler text.
Weekly: compare every rate against GOV.UK (rates change in April and at Budgets) and run unit tests on the calculators (known answers: £35k gives £4,486 tax); report traffic and revenue to Andrei; A/B test titles.
Event-driven: at a Budget or Spring Statement, update rates within 24h.
Needs: domain (~£10/yr, e.g. ukmoneycalcs.co.uk), Cloudflare/Vercel free account, GitHub repo, Search Console, later AdSense and affiliate accounts (in Andrei's name, KYC once).
Risk: inaccurate tax figures. Mitigate with the disclaimer, tests and GOV.UK citations. Scotland bands not done yet.