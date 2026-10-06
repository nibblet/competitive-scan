# Discovery scan, 2026-10-06 (Phase 1, test run)

Five capability searches (underwriting, rehab, operate, sense / track, chat and MCP). Seed list excluded: Resideline, iComps, REsimpli, DeedSpring, ChatARV.

**Read this first: confidence.** The session's network policy blocked direct page loads for every vendor site tried (for example `apps.apple.com`, `flipperforce.com`, `housecanary.com`). Every claim below comes from web search result snippets at the URL listed. No page was opened. Treat every row as "seen in search results, not page-confirmed." Anything a snippet did not state is written "not established."

**Cells** use the capability ids from `../capability-map.md`.

**Count:** 27 competitor or pattern candidates, 9 data vendors, 8 ignored, 3 honorable mentions.

## A. Competitor and pattern candidates

### Deal (underwriting, comps, screening)

| Product | What it is | Cells | Group | Source | Recent / notable |
|---|---|---|---|---|---|
| PropLab | AI underwriter for flippers and wholesalers: paste an address or listing link, get comps, ARV, rehab, rent, exits and MAO in about 60 seconds | dl.uw.six, dl.uw.mao, dl.uw.rent, dl.plat.share | direct overlap (AI-native) | https://peerpush.com/p/proplab-ai-real-estate-underwriter , https://ai.g2.com/marketplace/tools/proplab | Free tier per listing. API / MCP not established |
| BatchOffers | Wholesaler offer calculator: upload a CSV of addresses, get ARV, repairs and MAO per row. Listed at $39 to $399 a month | dl.plat.bulk, rv.flow.bulk-csv-underwrite, dl.uw.mao | direct overlap (AI-native) | https://news.bensbites.co/posts/60091-batchoffers-bulk-property-offer-calculator-for-real-estate-wholesalers , https://alternativeto.net/software/batchoffers/about | Launch date not established |
| DealBeast | AI deal analysis: ARV, comps, rent, ROI, a "Deal or No Deal" verdict, and LOI generation | dl.uw.verdict, dl.uw.rent, rv.op.doc-generate | direct overlap (AI-native) | https://www.producthunt.com/products/dealbeast | A "DealBeast API" G2 listing exists (https://www.g2.com/products/dealbeast-api/discuss); scope not established |
| BrrrrSimply | iPhone app for BRRRR, flip, rental and wholesale analysis, with AI insights and comps behind a subscription | dl.uw.six, dl.comps.pane | direct overlap (closest App Store neighbor to Deal) | https://apps.apple.com/app/id6746193115 | Release date not established |
| DealCheck | Incumbent rental / flip / BRRRR analyzer. Shows up to 20 sales comps and 20 rent comps on a list and map; rent estimate sourced from RentCast | dl.comps.map, dl.comps.pick, dl.uw.rent | borrow patterns (incumbent) | https://help.dealcheck.io/articles/3071993-viewing-sales-comps-arv-estimates , https://help.dealcheck.io/en/articles/3106052-viewing-rental-comps-rent-estimates | Not established |
| Privy | Incumbent MLS-integrated deal finding and analysis with LiveCMA comp search | dl.comps.pane, dl.uw.rent | borrow patterns (incumbent) | https://goliathdata.com/deal-modeling-vs-deal-finding-platforms (third party) | Not established |

### REbuild (rehab estimating and project execution)

| Product | What it is | Cells | Group | Source | Recent / notable |
|---|---|---|---|---|---|
| FlipperForce | Incumbent flip software: rehab estimator, SOW with prewritten notes, Bid Manager, comps tool with map and comp selection, flip analyzer with max purchase price | rb.est.calc, rb.sow.build, rb.ex.bids, rb.ex.change-orders, dl.comps.pick, dl.comps.map | direct overlap (incumbent; touches REbuild and Deal) | https://flipperforce.com/software-features/rehab-repair-cost-estimator , https://www.flipperforce.com/house-flipping-blog/new-feature-track-expense-change-orders | AI Receipt Analyzer, early January 2026 (https://flipperforce.com/learn/tools/ai-receipt-analyzer). A public API is claimed in a search summary of the 2025 recap, not confirmed |
| Estimara | iOS AI rehab estimator from photos and video, room-by-room, with ARV / MAO calculators and a deal pipeline | rb.in.photo, rb.in.walkthrough, dl.uw.mao | direct overlap (AI-native) | https://appshunter.io/ios/app/estimara-ai-rehab-estimator/id6760662681 | Released 2026-03-30, updated 2026-07-22; $9.99 a month for 10 analyses (same source) |
| OfferMarket SOW tool | Builds a contractor-ready SOW from photos, or reviews an existing rehab budget for realism | rb.sow.build, rb.in.photo, rb.est.audit | borrow patterns ("review my budget" mode) | https://www.offermarket.us/calculators/scope-of-work | Not established |
| Smart Scope | iOS: describe a job by voice, it writes the scope and matches line items to your price book (built on Claude per listing). Milestone payment schedules, e-sign, branded PDF | rb.in.voice, rb.price.books, rb.ex.draws, rb.rep.pdf | borrow patterns (trade contractor tool) | https://mwm.ai/apps/smart-scope-ai-estimating/6761380768 | Release date not established |
| Storypole | Offline renovation tracker: costs, payments, phases, decisions log, risk register, forecast finish date and cost, PDF / Excel export | rb.ex.budget-actual, rb.rep.pdf, rb.est.scenarios | borrow patterns (homeowner / builder) | https://www.producthunt.com/products/storypole | Recent Product Hunt launch, exact date not established |
| Rabbet | Construction loan draw management for lenders: draw requests, inspections with photos, budget to actual | rb.ex.draws, rb.ex.budget-actual | borrow patterns (what a lender-grade draw package looks like) | https://rabbet.com/lenders/solutions/construction-draw-inspection-software | Not established |

### Readvise > Operate (pipeline, deadlines, documents, reminders)

| Product | What it is | Cells | Group | Source | Recent / notable |
|---|---|---|---|---|---|
| FlipMantis | AI deal management for wholesalers, flippers and holders: CRM, stakeholder portal (lenders, contractors upload docs and submit draws), AI voice agents for seller qualifying, rehab budgets and draws | rv.op.pipeline, rv.doc.client-portal, rb.ex.draws | direct overlap (only investor-native Operate find) | https://www.capterra.ca/software/1086098/FlipMantis | From $99 a month per Capterra. Release dates not established |
| Nekst | AI transaction management: contract upload extracted in about 90 seconds, dates fill linked tasks that shift together, tasks written as "3 days after inspection" | rv.doc.deadline-extract, rv.op.checklists | borrow patterns (agent / TC tool) | https://help.nekst.com/en-us/article/see-it-work-create-your-first-transaction-from-a-contract-18q84ti/ | Not established |
| Paperless Pipeline (Pipeline AI) | Brokerage transaction platform; AI reads contracts, turns "10 days from acceptance" into dates counting holidays, each value links to its source text | rv.doc.deadline-extract | borrow patterns (click-to-source citations) | https://www.paperlesspipeline.com/pipeline-ai | Not established |
| Docs2Dates | Contracts to calendar dates, each tied to its source sentence; critical-date tables; calendar sync to the date owner | rv.doc.deadline-extract, rv.doc.outbound-reminders | borrow patterns, or vendor | https://www.capterra.com/p/10044162/Docs2Dates/ | Capterra page labeled 2026; releases not established |
| Wit | Voice-first AI transaction coordinator app: tracks deadlines and missing docs, sends reminders, generates docs from templates, routes for signature. $30 to $40 per transaction | rv.doc.outbound-reminders, rv.doc.esign, rv.op.doc-generate | borrow patterns (agent tool) | https://apps.apple.com/us/app/id6748923692 | Release date not established |
| ListedKit (Ava) | Incumbent AI TC: reads contracts, extracts dates and parties, builds checklists, email / SMS / in-app deadline alerts | rv.doc.deadline-extract, rv.doc.outbound-reminders | borrow patterns (incumbent) | https://www.listedkit.com/resources/what-is-ai-transaction-coordinator | A ListedKit page reportedly says 5,000+ contracts read as of April 2026; not confirmed |
| Clozze | AI transaction management: one inbox for email and text, AI flags messages needing reply and drafts them | rv.doc.outbound-reminders, rv.pulse.inbound-email | borrow patterns (agent tool) | https://www.capterra.com/p/10036401/Clozze/ | Not established |
| RealPact | YC S26: AI operating system for brokerages; agents pull deed, tax, permit, parcel and MLS data to fill contracts, coordinate signatures, track deadlines | rv.op.doc-generate, rv.doc.esign | borrow patterns (brokerage) | https://www.ycombinator.com/companies/realpact | YC S26 batch, 2026 |
| Open to Close | Incumbent transaction management with automated comms and scheduled reports | rv.op.war, rv.doc.outbound-reminders | borrow patterns (incumbent) | https://opentoclose.com/automation | Not established |

### Readvise > Sense and Track

| Product | What it is | Cells | Group | Source | Recent / notable |
|---|---|---|---|---|---|
| SFR Analytics | Database of active investors from recorded deeds: portfolios, acquisition history, contact data, cash buyer filters, per-investor pages. Sells API and flat files | rv.sense.roundtrips, rv.sense.comp-intel-capture, rv.sense.comp-discovery | direct overlap, also possible vendor | https://sfranalytics.com/products/active-investors | Records show April 2026 purchases; dated feature release not established |
| PropertyRadar | Incumbent owner data platform with a "finding flippers" workflow: repeat sellers, months since prior transfer, estimated competitor flip profit | rv.sense.roundtrips | borrow patterns (incumbent) | https://www.propertyradar.com/blog/finding-flippers-know-your-competition-find-active-investors | Not established |
| DealScanner | AI micro-market analysis (Allegheny County, PA): saved searches, deal alerts, AI chat, condition estimates from public photos | rv.sense.market-explorer, rv.sense.watchlist | borrow patterns (Pittsburgh only) | https://technical.ly/entrepreneurship/ai-tool-dealscanner-pittsburgh-real-estate/ | Founded 2024 per source |
| RentRedi Portfolio Performance | Landlord dashboard rolling up NOI, cash flow, cash-on-cash and equity across properties | rv.rent.portfolio | borrow patterns (incumbent feature) | https://rentredi.com/blog/rentredi-portfolio-performance-dashboard/ | Launched 2026-03-11 per snippet |

### Chat and MCP lens

| Product | What it is | Exposes to chat | Group | Source | Recent / notable |
|---|---|---|---|---|---|
| DealMachine MCP | Remote MCP for the DealMachine lead platform | Read + write: enrichment, property and people search, comps; add lead, tag, assign, note, pause mail sequence (some writes may be via Pipedream / Zapier wrappers) | direct overlap and borrow patterns: the only investor-facing write-capable MCP found | https://dealmachine.com/guides/mcp-server | Launch date not established |
| PropStream Intelligence Assistant | AI chat panel inside PropStream beside its flip analyzer (profit, ROI, MAO) | Inside PropStream only; MCP not established | direct overlap (closed); borrow "chat beside the deal math" | https://www.propstream.com/news/introducing-the-new-propstream-intelligence-assistant-real-estate-research-reimagined-by-ai | Announced 2026-04-07 |

## B. Data vendors (integration watch, like ChatARV)

Candidates to sit behind forVEX tools, not to compete with them.

| Vendor | What it supplies | Fills | Chat / API | Source | Recent |
|---|---|---|---|---|---|
| RentCast | Rent and value estimates with ranged comps | dl.uw.rent, mcp.uw.rent | Official MCP / AI tools page; community MCPs | https://developers.rentcast.io/reference/ai-tools | Not established |
| HouseCanary | AVM, 36-month forecasts, comps, rent, market pulse, portfolio monitoring. Publishes an AVM accuracy white paper | mcp.uw.comps, rv.track.arv-scoreboard | MCP package, 149 endpoints, read only | https://www.housecanary.com/blog/housecanary-mcp-server | Page updated 2026-04-27 |
| ATTOM | Nationwide property profiles, AVMs, comps, sales history | mcp.uw.comps, rv.sense.roundtrips | MCP server, read only | https://www.attomdata.com/solutions/mcp-server/ | Announced 2026-01-27 (https://www.wavgroup.com/2026/01/27/attom-launches-mcp-server-a-milestone-moment-for-ai-native-real-estate-data/) |
| BatchData | Property, owner, mortgage, skip trace, phone verification, cash buyer data | rv.sense.comp-intel-capture | MCP server, 9 tools, mostly read | https://help.batchdata.io/en/articles/12859677-batchdata-mcp-server-now-available-november-2025 | Launched November 2025 |
| Regrid | 160M+ parcels: ownership, values, land use, boundaries | property resolution | MCP, read only | https://support.regrid.com/docs/mcp-server | Not established |
| Realie | 180M parcels, 100+ county fields (REbuild already uses Realie data) | rb.val.enrich | MCP and CLI, read only | https://docs.realie.ai/realie-mcp-server | Not established |
| Altos Research | Weekly market stats for 99% of US ZIPs | rv.sense.market-brief | API not established | https://altos.re/about | Not established |
| 1build | Live material, labor and equipment costs across 3,000+ counties, GraphQL API | rb.price.regional | API | https://www.ycombinator.com/launches/IQo-1build-plaid-for-construction-cost-data | Not established |
| Clear Estimates (CEPIA) | Localized repair and renovation costs for 400+ US areas; AI scope from photos | rb.price.regional, rb.in.photo | Pricing Intelligence API | https://go.clearestimates.com/home | Cherre data partnership 2024-12-05 |

## C. Ignored (with reason)

- **Built Technologies**: lender draw platform. It sells to banks, but your lenders may use it. https://getbuilt.com/blog/author/built-team/
- **GeoData Plus**: NY / NJ broker and appraiser data. Its "sold twice in a year" flip flag is a sanity check for round trips. https://nyrej.com/index.php/commercial-real-estate-guide-technology-geodata-plus
- **Smart Bricks**: institutional and global capital, Dubai-based. https://siliconangle.com/2026/02/10/vcs-back-smart-bricks-plan-automate-real-estate-investing-ai-agents/
- **DealSheet AI**: UK only. https://apps.apple.com/gb/app/dealsheet-ai/id6756220992
- **Zillow app in ChatGPT**: consumer search. https://zillow.mediaroom.com/2025-10-06-Zillow-debuts-the-only-real-estate-app-in-ChatGPT
- **Green Street MCP**: commercial only. https://eu.greenstreet.com/?p=16077
- **NexGenData real estate MCP (Apify)**: scrapes Zillow, Redfin and Realtor.com, which carries terms-of-service risk. https://apify.com/nexgendata/real-estate-mcp-server?fpr=ewv9tm
- **HelloData**: multifamily only. https://www.hellodata.ai/about-us

Seen but unconfirmed, not ranked: ARVnote (https://hunted.space/product/arvnote), FlipAI (https://saasbrowser.com/he/saas/1528077/flipai), CloudCoord (https://www.getapp.com/all-software/a/cloudcoord/), Contract10 MCP (https://www.mcpbundles.com/skills/contract10-mcp-72e49a5283), Goliath Data AI acquisitions (https://goliathdata.com/ai-acquisitions-for-wholesalers), InvestorLift AI ARV (https://intercom.help/investorlift/en/articles/16067857-dispo-day-recap-july-22-2026-a-live-arv-comping-masterclass-on-3-submitted-deals).

## D. Honorable mentions

- **BirdEarly**: AI daily MLS picks for flippers. Pattern for daily deal-flow alerts. https://www.producthunt.com/products/birdearly-ai-for-fix-flips
- **AVMetrics / PP10**: an industry ARV accuracy metric, the share of estimates within plus or minus 10% of sale price. A ready metric if the ARV Accuracy card is turned on. https://clearcapital.com/?p=3558
- **Parcl Labs**: incumbent with an investor activity API for any US market. https://docs.parcllabs.com/reference/investor-metrics-1

## E. Patterns that showed up more than once

1. **Bulk CSV in, offers out** (BatchOffers). Not built anywhere in forVEX.
2. **Each extracted contract date links to its source sentence** (Paperless Pipeline, Docs2Dates). Your extractor already exists; this is about trust in it.
3. **Linked deadlines that move together** (Nekst).
4. **Per-transaction AI coordinator that chases reminders and signatures** (Wit, ListedKit). Matches the reminders, e-sign and portal gaps.
5. **Comp map, comp picking, rent comps** (DealCheck, FlipperForce). Deal lacks all three; readvise has overrides.
6. **Data vendors shipping read-only MCP servers** (ATTOM, HouseCanary, BatchData, RentCast, Regrid, Realie). DealMachine is the only investor tool found that also writes. No product found combines pipeline, underwriting, estimates, documents, tasks and rentals in one MCP.

## F. A starting point for your pick (suggestion only)

If you want 10, this mix covers each app and the MCP lens:

| # | Product | Why this one |
|---|---|---|
| 1 | PropLab | AI-native head-to-head with Deal |
| 2 | BatchOffers | Only bulk CSV screener found |
| 3 | BrrrrSimply | Closest App Store neighbor to Deal |
| 4 | DealCheck | Incumbent reference for comp map and rent comps |
| 5 | FlipperForce | Rehab incumbent; change orders, comp picking, possible API |
| 6 | Estimara | AI photo rehab app, actively updated in 2026 |
| 7 | FlipMantis | Only investor-native Operate find (portal, draws) |
| 8 | Nekst or ListedKit | Deadline extraction patterns |
| 9 | SFR Analytics | Closest outside match to competitor tracking |
| 10 | DealMachine MCP | Only write-capable investor MCP |

Vendor watch, alongside ChatARV: HouseCanary, ATTOM, BatchData, RentCast.

## Questions for Paul

1. Which 8 to 12 go on the watchlist? Do you want the vendor watch tracked too?
2. Phase 2 needs page snapshots, and this environment blocks those sites. Do you want to open network access (see the chat reply), or should Phase 2 run as a Cowork or desktop task with normal web access?
3. Should pure agent / brokerage TC tools (Nekst, ListedKit, Wit) stay on as pattern sources, or is FlipMantis enough for Operate?
