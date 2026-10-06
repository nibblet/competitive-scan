# Capability map (Phase 0)

Generated 2026-10-06 from code, read-only. Every evidence path below was checked to exist on disk at the commits listed. Machine-readable copy: `capability-map.json`.

**Status:** `built` = UI (or tool), API and data path present. `partial` = a layer missing, flagged off, or backend only. `not built` = absent from code or in plans only.

**Evidence format:** `repo:path`.

| Repo | Branch | Commit |
|---|---|---|
| readvise | claude/competitive-capability-scan-4p48kt | 8520a20 |
| recontrol | claude/competitive-capability-scan-4p48kt | f05d778 |
| rebuild3 | claude/competitive-capability-scan-4p48kt | 41913c3 |
| forvex-underwrite | claude/competitive-capability-scan-4p48kt | cee40b8 |

**Chat access through MCP** (column "Chat", detail in `mcp-coverage.json`): 34 read+write, 26 read, 4 write, 44 none, 18 n/a. `n/a` = not built, or is the MCP layer itself.

| App | read+write | read | write | none | n/a |
|---|---|---|---|---|---|
| Readvise | 21 | 6 | 3 | 20 | 6 |
| REbuild | 6 | 4 | 0 | 22 | 5 |
| Deal iOS | 4 | 12 | 0 | 2 | 7 |
| MCP layer (reference) | 3 | 4 | 1 | 0 | 0 |

**126 capabilities:** 93 built, 16 partial, 17 not built.

## Seed hypotheses, checked against code

**DeedSpring contract deadline extraction vs our document flow.** Partly built, as you guessed. The LLM extractor and forvex_materialize_obligations already turn inspection, financing, earnest money and closing dates into tasks (recontrol). Missing: a deadline view in readvise (they show as ordinary tasks), any outbound reminder (in-app only), e-signature, and a client portal. OCR happens on the phone only. Cells: `rv.doc.deadline-extract`, `rv.doc.key-date-alerts`, `rv.doc.outbound-reminders`, `rv.doc.esign`, `rv.doc.client-portal`.

**Resideline accuracy scoreboard vs our outcomes data.** Closer than expected. Per-deal ARV and rehab error is already computed and stored (core.deal_outcomes), there is an admin mean ARV error in recontrol, and readvise has a fully built ARV Accuracy card that is switched off (enabled: false). The data foundation exists; it is internal only. Cells: `rv.track.planned-vs-actual`, `rv.track.arv-scoreboard`, `mcp.out.record`, `mcp.out.learning`.

**Resideline bulk CSV screening vs Deal one-address flow.** Not built anywhere. Deal's rules do not forbid it (it is not AI). Open question: does a bulk screen belong in Deal, or as a readvise / recontrol server job on the same engine, given Deal is built for one address on a driveway? Readvise's Marketplace Stage 0 triage is the nearest existing pattern (paste many, rule-scored), but it is market-level, not address-level. Cells: `rv.flow.bulk-csv-underwrite`, `rv.flow.marketplace-triage`, `dl.plat.bulk`.

## Readvise (`readvise`)

**App filter:** System of record for pipeline, tasks, notes. Consumes underwriting, does not own it. MCP tools live in recontrol, not here. *Source: readvise:CLAUDE.md.*

### Sense

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Tract / ZIP / neighborhood market explorer <sub>`rv.sense.market-explorer`</sub> | built | read<br><sub>forvex_get_market_intelligence</sub> | `readvise:pages/operate/sense.tsx` (Sense page mounting the market views)<br>`readvise:components/operate/sense/views/MarketMemoryTab.tsx` (one of the Sense view tabs (Tracts, Zips, Neighborhoods, MarketForces alongside))<br>`readvise:pages/api/operate/sense` (about 60 routes for ACS, HUD, SAFMR, Zillow history, FRED, choropleths) |  |
| Weekly market memory / AI market brief <sub>`rv.sense.market-brief`</sub> | built | read<br><sub>forvex_get_market_brief</sub> | `readvise:pages/api/sense/market-memory/generate-week.ts` (generates the weekly narrative, signals and deltas)<br>`readvise:components/operate/sense/views/MarketMemoryTab.tsx` (UI for the brief) |  |
| Local news brief <sub>`rv.sense.news`</sub> | built | none | `readvise:components/dashboard/LocalNewsBrief.tsx` (dashboard card)<br>`readvise:pages/api/operate/sense/news/serpapi.ts` (SerpAPI news fetch) |  |
| Tract / ZIP watchlist alerts <sub>`rv.sense.watchlist`</sub> | built | none | `readvise:pages/api/sense/watchlist/index.ts` (watchlist CRUD)<br>`readvise:lib/cron-tasks/sense-watchlist-check.ts` (daily cron writes in-app notifications) |  |
| Competitor listing capture (daily SERP collector + manual paste) <sub>`rv.sense.comp-intel-capture`</sub> | built | read+write<br><sub>readvise_record_competitor_listing, readvise_list_competitor_work</sub> | `readvise:lib/cron-tasks/competitive-intel.ts` (daily SERP ingest, persist, fuzzy match)<br>`readvise:pages/api/sense/competitive-intel/capture.ts` (pasted text to competitive_listings) |  |
| Competitive landscape brief (deal board, buyer registry, overlap, operators) with share link <sub>`rv.sense.comp-intel-brief`</sub> | built | none | `readvise:pages/sense/competitive-intel/index.tsx` (brief and panels)<br>`readvise:pages/share/intel/[token].tsx` (read-only share link) |  |
| Competitor buy / resell round trips from public records (plus self-audit) <sub>`rv.sense.roundtrips`</sub> | built | write<br><sub>readvise_record_instrument, readvise_upsert_records_entity, readvise_resolve_listing</sub> | `readvise:pages/api/sense/competitive-intel/roundtrips.ts` (round-trip and hold-time computation) |  |
| Competitor discovery review queue <sub>`rv.sense.comp-discovery`</sub> | built | none | `readvise:pages/sense/competitive-intel/discoveries.tsx` (pending_review to active / archived / friendly_franchise)<br>`readvise:pages/api/sense/competitive-intel/discoveries.ts` (API) |  |
| Competitor mail-effort upload and marketing profile <sub>`rv.sense.comp-marketing`</sub> | built | none | `readvise:pages/api/sense/competitive-intel/effort-upload.ts` (ZIP / weight CSV upload) |  |
| Competitor openings (failed competitor listings as a lead list) <sub>`rv.sense.openings`</sub> | **partial** | none | `readvise:lib/cron-tasks/competitor-openings.ts` (backend cron only) | Backend cron; no dedicated UI confirmed. |
| Competitor density per neighborhood <sub>`rv.sense.density`</sub> | built | none | `readvise:components/operate/sense/views/CompetitorsTab.tsx` (density view) |  |
| Records watch on deals we did not get <sub>`rv.sense.lost-deal-watch`</sub> | *not built* | n/a | `readvise:docs/plans/DEAL_RECORDS_WATCH_PLAN.md` (says design agreed, not built) |  |

### Operate

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Pipeline / stage board, property list, map <sub>`rv.op.pipeline`</sub> | built | read+write<br><sub>forvex_list_deals, forvex_save_deal, forvex_update_deal_disposition</sub> | `readvise:pages/operate/index.tsx` (pipeline board)<br>`readvise:pages/operate/map.tsx` (map view) |  |
| Bulk status update across many properties <sub>`rv.op.bulk-status`</sub> | built | write<br><sub>forvex_update_deal_disposition</sub> | `readvise:pages/api/operate/properties/bulk-update.ts` (multi-property status / update) |  |
| Property detail workspace (overview, financials, comps, underwriting, workflow, notes, files) <sub>`rv.op.property-workspace`</sub> | built | read+write<br><sub>forvex_get_deal, forvex_get_deal_history, forvex_get_property...</sub> | `readvise:components/operate/PropertyDetail.tsx` (workspace shell)<br>`readvise:components/operate/tabs` (per-tab components) |  |
| Comps / ARV evidence with overrides (reads recontrol comp traces) <sub>`rv.op.comps-evidence`</sub> | built | read+write<br><sub>forvex_get_comps, forvex_get_comp_detail, forvex_set_comp_override</sub> | `readvise:pages/api/operate/properties/[propertyId]/comps.ts` (reads comp trace)<br>`readvise:pages/api/operate/properties/[propertyId]/comps/override.ts` (operator override) |  |
| Re-underwrite one property (proxied to recontrol) <sub>`rv.op.reanalyze`</sub> | built | read+write<br><sub>forvex_underwrite, forvex_save_deal</sub> | `readvise:pages/api/operate/properties/[propertyId]/reanalyze.ts` (proxies to recontrol engine) |  |
| Tasks and My Work (manual, AI-suggested, checklist, advisor) <sub>`rv.op.tasks`</sub> | built | read+write<br><sub>readvise_list_tasks, readvise_create_task, readvise_complete_task...</sub> | `readvise:pages/tasks.tsx` (task list)<br>`readvise:pages/operate/my-work.tsx` (My Work view)<br>`readvise:pages/api/operate/tasks/index.ts` (tasks API) |  |
| Checklists and templates with trigger evaluator <sub>`rv.op.checklists`</sub> | built | none | `readvise:pages/operate/checklists/templates.tsx` (template editor)<br>`readvise:lib/operate/checklists/materialize.ts` (materialize into workflow nodes)<br>`readvise:lib/checklist/trigger-evaluator.ts` (trigger evaluation) |  |
| Staged AI actions the operator approves <sub>`rv.op.staged-actions`</sub> | built | read+write<br><sub>readvise_get_daily_review, readvise_decide_review_items</sub> | `readvise:components/operate/tabs/StagedActionsPanel.tsx` (approval panel)<br>`readvise:pages/api/operate/workflow/ai-op.ts` (AI op endpoint) |  |
| Daily review queue (readvise_get_daily_review / decide_review_items) <sub>`rv.op.daily-review`</sub> | **partial** | read+write<br><sub>readvise_get_daily_review, readvise_decide_review_items</sub> | `recontrol:lib/mcp/tools/readvise/dailyReview.ts` (MCP tool implementation) | No table, route or UI in readvise. Exists only as recontrol MCP tools. Paul (2026-10-06): in active use, needs validation. |
| Assignments and in-app notifications <sub>`rv.op.assignments`</sub> | built | none | `readvise:pages/api/operate/assignments/index.ts` (assignment API)<br>`readvise:components/notifications/NotificationBell.tsx` (in-app bell) |  |
| Generate offer letter / purchase contract (.docx) <sub>`rv.op.doc-generate`</sub> | built | none | `readvise:pages/api/operate/properties/[propertyId]/document.ts` (docx generation)<br>`readvise:components/operate/DocumentGenerateModal.tsx` (UI) |  |
| Dispo: wholesale sheet, presentation packet, voice brief <sub>`rv.op.dispo`</sub> | built | write<br><sub>forvex_build_wholesale_sheet, forvex_render_presentation, forvex_create_voice_brief</sub> | `readvise:components/operate/dispo/WholesaleSheetModal.tsx` (wholesale sheet)<br>`readvise:components/operate/presentation/PresentationPacketMenu.tsx` (presentation packet)<br>`readvise:components/operate/tabs/underwriting/VoiceBriefListen.tsx` (voice brief) |  |
| Exit / lost reasons (closed lists mirrored from recontrol) <sub>`rv.op.exit-reasons`</sub> | built | read+write<br><sub>forvex_update_deal_disposition, forvex_get_deal_history</sub> | `readvise:lib/operate/dispositionReasons.ts` (closed reason list) |  |
| Weekly Activity Report (generate, edit, AI polish, mark sent) <sub>`rv.op.war`</sub> | built | none | `readvise:pages/api/operate/reports/generate.ts` (generation)<br>`readvise:components/operate/summary/WeeklyActivityReportCard.tsx` (UI) |  |

### Operate > Documents and deadlines

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Deal document storage and listing <sub>`rv.doc.storage`</sub> | **partial** | read+write<br><sub>forvex_get_deal_documents, forvex_get_document_text, forvex_register_document...</sub> | `readvise:lib/operate/dealDocuments.ts` (doc types: purchaseContract, settlementStatement, deed, titleCommitment)<br>`readvise:pages/api/operate/properties/[propertyId]/files.ts` (GET only)<br>`readvise:components/operate/tabs/FilesTab.tsx` (lists docs and closing figures) | Read-only in readvise. Uploads are written by recontrol (forVEX Scan / forvex_register_document). |
| Contract contingency date extraction into deadline tasks <sub>`rv.doc.deadline-extract`</sub> | **partial** | read+write<br><sub>forvex_materialize_obligations, forvex_project_scan, readvise_list_tasks</sub> | `recontrol:lib/mcp/memory/extractScan.ts` (LLM extractor over phone-OCR text: parties, dates, dated obligations)<br>`recontrol:lib/mcp/memory/obligations.ts` (turns inspection, financing, earnest money, closing into tasks, idempotent)<br>`readvise:supabase/migrations/20260921160000_readvise_tasks_source_document_obligation.sql` (readvise accepts source='document_obligation' tasks with target_date) | Extraction and task creation are built (recontrol). Gap: no deadline-specific UI in readvise; obligations show up as ordinary tasks. OCR happens on the phone; no server-side OCR found. |
| Key-date risk alerts (option expiry, expected close) <sub>`rv.doc.key-date-alerts`</sub> | built | read<br><sub>readvise_get_daily_review</sub> | `readvise:lib/operate/dealRisk.ts` (scores key dates (around lines 199 to 226))<br>`readvise:lib/cron-tasks/deal-at-risk.ts` (weekly cron writes insights and follow-up task)<br>`readvise:pages/api/workspaces/[workspaceId]/alert-settings.ts` (per-workspace thresholds) |  |
| Apply settlement statement actuals to deal outcome <sub>`rv.doc.settlement-actuals`</sub> | built | read+write<br><sub>forvex_apply_document_facts, forvex_list_closing_statements</sub> | `recontrol:lib/mcp/documents/applyDocumentFacts.ts` (writes actual purchase / sale price with fill / match / conflict preview) | MCP only (forvex_apply_document_facts). |
| E-signature / signature chasing <sub>`rv.doc.esign`</sub> | *not built* | n/a | none (absence finding) | Explorer found no DocuSign, e-sign or signature-tracking code in readvise. |
| Client / seller portal <sub>`rv.doc.client-portal`</sub> | *not built* | n/a | `readvise:pages/share/intel/[token].tsx` (only read-only share link that exists (competitive brief)) |  |
| Outbound email / SMS reminders <sub>`rv.doc.outbound-reminders`</sub> | *not built* | n/a | `readvise:lib/notifications/createNotification.ts` (notifications are in-app only)<br>`readvise:docs/plans/REFLECT2_WHATSAPP_CAPTURE_PLAN.md` (WhatsApp capture planned only) |  |

### Operate > Local deal flow

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Marketplace Stage 0 triage (paste many emails, rule-scored KILL / WATCH / PULL_ADDRESS) <sub>`rv.flow.marketplace-triage`</sub> | built | none | `readvise:components/operate/marketplace/MarketplaceIntakePanel.tsx` (paste-many intake)<br>`readvise:lib/marketplace/ingest.ts` (batch ingest)<br>`readvise:docs/MARKETPLACE_TRIAGE_STAGE0_RULESET_V0.1.md` (DRAFT ruleset, market-level, zero-address) | Property-level Stage 1 not built. |
| Pull ChatARV comps on won lead <sub>`rv.flow.chatarv-pull`</sub> | built | read+write<br><sub>forvex_get_chatarv_comps</sub> | `readvise:lib/marketplace/triggerChatarvPull.ts` (calls chatarv-run-comps edge function) |  |
| CSV import of many addresses with bulk underwriting <sub>`rv.flow.bulk-csv-underwrite`</sub> | *not built* | n/a | `recontrol:app/api/operate/reanalyze/route.ts` (server re-runs one property at a time) | No bulk route in readvise or recontrol. Only CSV imports are rent roll, competitor mail effort, mailer segments, market data. |

### Track

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Metrics dashboards (funnel, cycle time, profit by exit / lead source) <sub>`rv.track.dashboards`</sub> | built | none | `readvise:pages/track/index.tsx` (Track page)<br>`readvise:pages/api/track/metrics` (metrics APIs)<br>`readvise:lib/track/chartRegistry.tsx` (chart registry) |  |
| Capital runway / pool planner <sub>`rv.track.capital`</sub> | built | none | `readvise:components/track/CapitalView.tsx` (UI)<br>`readvise:pages/api/track/capital/runway.ts` (API) |  |
| CFO insight and AI explore <sub>`rv.track.cfo`</sub> | built | none | `readvise:pages/api/track/cfo-insight.ts` (CFO insight)<br>`readvise:pages/api/track/ai/explore.ts` (AI explore) |  |
| Per-deal planned vs actual (ARV vs sale price, rehab estimate vs actual) <sub>`rv.track.planned-vs-actual`</sub> | built | read+write<br><sub>forvex_record_deal_outcome, forvex_update_deal_outcome, forvex_list_deal_outcomes</sub> | `readvise:components/operate/tabs/overview/OutcomeReview.tsx` (mounted in OverviewTab)<br>`readvise:lib/checklist/outcome-capture.ts` (writes core.deal_outcomes on SOLD)<br>`recontrol:lib/mcp/deals/recordDealOutcome.ts` (returns arv_error_pct and rehab_error_pct) |  |
| ARV accuracy scoreboard (estimated vs actual, by band, over time) <sub>`rv.track.arv-scoreboard`</sub> | **partial** | read<br><sub>forvex_list_deal_outcomes</sub> | `readvise:lib/track/templates/arvAccuracyProfile.server.ts` (server computation built)<br>`readvise:components/track/drivers/ARVAccuracyCard.tsx` (card built)<br>`readvise:lib/track/chartRegistry.tsx` (card registered enabled: false (line 114)) | Also an aggregate mean_arv_error_pct on recontrol admin page recontrol:app/(dashboard)/learning/page.tsx. Internal only; nothing public-facing. |
| Revisit stale or drifted underwriting decisions <sub>`rv.track.decision-revisit`</sub> | built | none | `readvise:lib/operate/decisionRevisit.ts` (cron logic) |  |
| Marketing efficiency (cost per lead / contract / close) <sub>`rv.track.cost-per-x`</sub> | **partial** | none | `readvise:lib/track/chartRegistry.tsx` (cards registered enabled: false)<br>`readvise:pages/api/operate/metrics/marketing-capital-bridge.ts` (bridge metric API) |  |
| Deal postmortems <sub>`rv.track.postmortem`</sub> | *not built* | n/a | `readvise:docs/roadmap/Roadmap_next.md` (mentioned in roadmap only) | A postmortem Claude skill exists outside the repos (forvex-postmortem). |

### Portfolio / Rentals

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Rental portfolio dashboard with CSV import / export and AI review <sub>`rv.rent.portfolio`</sub> | built | read+write<br><sub>readvise_list_rental_ops, readvise_list_rental_debt, readvise_list_lease_status...</sub> | `readvise:pages/operate/rentals.tsx` (page)<br>`readvise:components/operate/rentals/RentalPortfolioView.tsx` (view, import / export)<br>`readvise:pages/api/operate/rentals/analyze.ts` (AI review) |  |
| Per-rental tabs (ops, debt, equity, value) <sub>`rv.rent.per-property`</sub> | built | read+write<br><sub>readvise_list_rental_ops, readvise_upsert_rental_ops, readvise_list_rental_debt...</sub> | `readvise:components/operate/tabs/rental` (tab components) |  |
| Rent roll / lease snapshots <sub>`rv.rent.rent-roll`</sub> | **partial** | read+write<br><sub>readvise_parse_rent_roll, readvise_upsert_lease_status, readvise_list_lease_status</sub> | `readvise:supabase/migrations/20260924120000_rental_lease_snapshots.sql` (table)<br>`readvise:lib/operate/hooks/rental/attachLeaseUnits.ts` (read into rollups)<br>`recontrol:lib/mcp/tools/readvise/parseRentRoll.ts` (written via MCP) |  |
| CapEx watch list <sub>`rv.rent.capex`</sub> | **partial** | read+write<br><sub>readvise_list_property_capex, readvise_upsert_property_capex</sub> | `readvise:supabase/migrations/20260915180000_property_capex_items.sql` (data only, comment says CapEx UI removed) |  |
| Portfolio posture and badges <sub>`rv.rent.posture`</sub> | built | none | `readvise:components/operate/summary/PortfolioPostureCard.tsx` (card) |  |
| Cross-workspace portfolio metrics <sub>`rv.rent.cross-workspace`</sub> | **partial** | none | `readvise:pages/api/portfolio/metrics.ts` (API exists, no UI consumer found) |  |

### Pulse / Reflect / Knowledge

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Pulse capture with AI enrich / normalize / property resolution <sub>`rv.pulse.capture`</sub> | built | read+write<br><sub>readvise_append_pulse_today, readvise_create_advisor_action, readvise_get_today_summary</sub> | `readvise:components/reflect/PulseCaptureModal.tsx` (capture)<br>`readvise:pages/api/pulse/analyze.ts` (AI analyze) |  |
| Reflect timeline and weekly rollup <sub>`rv.pulse.reflect`</sub> | built | read<br><sub>forvex_recall, readvise_get_today_summary</sub> | `readvise:pages/reflect/index.tsx` (page)<br>`readvise:pages/api/reflect/week.ts` (weekly rollup) |  |
| Debriefs (from pulse, accountability) <sub>`rv.pulse.debrief`</sub> | built | read+write<br><sub>readvise_create_accountability_debrief, readvise_get_prior_context</sub> | `readvise:pages/api/debrief/pulse/[pulse_id].ts` (debrief from pulse) |  |
| Inbound email to pulse <sub>`rv.pulse.inbound-email`</sub> | built | none | `readvise:pages/api/inbound/email.ts` (Postmark inbound)<br>`readvise:lib/inboundEmail/adapters/postmark.ts` (adapter) |  |
| Global search <sub>`rv.pulse.search`</sub> | built | read<br><sub>forvex_recall</sub> | `readvise:pages/api/search/index.ts` (search_global RPC) |  |
| CMO social command center (read-only snapshot) <sub>`rv.pulse.cmo`</sub> | **partial** | read+write<br><sub>readvise_get_cmo_snapshot, readvise_upsert_cmo_snapshot</sub> | `readvise:components/social/SocialCommandCenter.tsx` (UI)<br>`readvise:pages/api/cmo/snapshot.ts` (reads snapshot written by recontrol) |  |

## REbuild (`rebuild3`)

**App filter:** Estimate logic lives in the pure engine package (packages/rebuild-engine). Changes there move CONTRACT_VERSION (currently 0.3.0) and affect recontrol and readvise. *Source: rebuild3:CLAUDE.md, rebuild3:packages/rebuild-engine/src/contract-version.ts.*

### Estimates

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Rule-based estimate calculation (quantity drivers, rounding, overrides) <sub>`rb.est.calc`</sub> | built | read+write<br><sub>forvex_preview_estimate, forvex_save_draft_estimate, forvex_update_estimate...</sub> | `rebuild3:packages/rebuild-engine/src/engine/calculator/calculate-estimate.ts` (calculateEstimate)<br>`rebuild3:packages/rebuild-engine/src/engine/calculator/quantity.ts` (quantity from sqft / rooms / fixed) | Lives in: engine. |
| Condition (severity) pricing per category <sub>`rb.est.condition`</sub> | built | read+write<br><sub>forvex_preview_estimate, forvex_get_builder_prefs, forvex_save_builder_prefs</sub> | `rebuild3:packages/rebuild-engine/src/category-scope.ts` (scope depth per category)<br>`rebuild3:rebuild3/app/actions/profile-rules.ts` (profile rule CRUD) | Lives in: engine + app. |
| Triangulation: $/sqft band vs severity vs bottom-up, variance flag <sub>`rb.est.triangulation`</sub> | **partial** | read+write<br><sub>forvex_save_draft_estimate, forvex_preview_estimate</sub> | `rebuild3:packages/rebuild-engine/src/rehab-summary.ts` (computeSqftBandCrossCheck, isVarianceFlagged)<br>`rebuild3:rebuild3/components/field/estimate-triangulation-panel.tsx` (UI panel)<br>`rebuild3:ESTIMATE_MODEL_V2.md` (three stored modes planned, partly wired) | Lives in: engine + app. |
| Multiple scenarios side by side <sub>`rb.est.scenarios`</sub> | **partial** | none | `rebuild3:rebuild3/components/field/profile-selector.tsx` (switch rehab profile)<br>`rebuild3:packages/rebuild-engine/src/wholetail-scope.ts` (wholetail vs full rehab read) | Lives in: engine + app. No general scenario object or side-by-side comparison. |
| Contingency, allowance and free-text lines <sub>`rb.est.allowances`</sub> | built | read+write<br><sub>forvex_preview_estimate, forvex_save_draft_estimate</sub> | `rebuild3:supabase/migrations/20260322000000_estimate_model_v2_phase9.sql` (schema)<br>`rebuild3:rebuild3/lib/estimates/v2-line-item.ts` (line shape) | Lives in: app. |
| Deal audit / risk flags (AI + rules) <sub>`rb.est.audit`</sub> | built | none | `rebuild3:rebuild3/app/actions/ai/audit-deal.ts` (AI audit)<br>`rebuild3:rebuild3/lib/logic/auditor.ts` (rules) | Lives in: app. |

### Pricing

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Line-item cost library <sub>`rb.price.library`</sub> | built | read<br><sub>forvex_get_workspace_context, forvex_map_observations_to_skus</sub> | `rebuild3:rebuild3/app/(dashboard)/library/page.tsx` (library page)<br>`rebuild3:rebuild3/app/actions/library.ts` (actions) | Lives in: app. |
| Named, duplicable price books <sub>`rb.price.books`</sub> | built | read<br><sub>forvex_get_workspace_context</sub> | `rebuild3:rebuild3/app/actions/price-books.ts` (actions)<br>`rebuild3:rebuild3/components/dashboard/price-book-editor.tsx` (editor) | Lives in: app. |
| Regional / ZIP cost index <sub>`rb.price.regional`</sub> | **partial** | read+write<br><sub>forvex_get_builder_prefs, forvex_save_builder_prefs</sub> | `rebuild3:supabase/migrations/20260321000000_builder_preferences.sql` (per-user $/sqft baselines only) | Lives in: app. No ZIP or market cost index. |
| National Estimator Cloud cost comparison <sub>`rb.price.nec`</sub> | **partial** | none | `rebuild3:rebuild3/lib/nec/client.ts` (sandbox API client)<br>`rebuild3:rebuild3/components/dashboard/nec-compare-panel.tsx` (only in price-book header) | Lives in: app. |
| Catalog curation queue <sub>`rb.price.curation`</sub> | built | none | `rebuild3:rebuild3/components/dashboard/curation-queue.tsx` (queue)<br>`rebuild3:rebuild3/app/actions/approve-catalog-item.ts` (approve) | Lives in: app. |

### Intake

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Room-by-room walkthrough with condition signals <sub>`rb.in.walkthrough`</sub> | built | none | `rebuild3:rebuild3/app/(field)/field/projects/[id]/walkthrough/page.tsx` (page)<br>`rebuild3:rebuild3/components/walkthrough/walkthrough-container.tsx` (container) | Lives in: app. |
| Rule-based condition inference <sub>`rb.in.inference`</sub> | built | none | `rebuild3:rebuild3/lib/inference/run-inference.ts` (signals to severity to tier) | Lives in: app. |
| Voice intake (transcribe + AI extraction) <sub>`rb.in.voice`</sub> | built | none | `rebuild3:rebuild3/app/actions/voice/transcribe-audio.ts` (transcribe)<br>`rebuild3:rebuild3/app/actions/voice/analyze-intake.ts` (extract) | Lives in: app. |
| Photo analysis <sub>`rb.in.photo`</sub> | built | none | `rebuild3:rebuild3/app/actions/ai/analyze-image.ts` (image analysis)<br>`rebuild3:rebuild3/components/ai/photo-analyzer.tsx` (UI) | Lives in: app. |
| Free-text multi-agent extraction <sub>`rb.in.text`</sub> | built | none | `rebuild3:rebuild3/lib/ai/text-estimate-swarm.ts` (swarm) | Lives in: app. |
| SKU mapping, autoscope, gap detection <sub>`rb.in.sku`</sub> | built | read<br><sub>forvex_map_observations_to_skus, forvex_get_missing_inputs</sub> | `rebuild3:packages/rebuild-engine/src/intake/autoscope.ts` (AI items to SKUs)<br>`rebuild3:packages/rebuild-engine/src/intake/gap-detector.ts` (gap detection) | Lives in: engine. |
| Intake eval harness (golden set, hallucination check) <sub>`rb.in.eval`</sub> | built | none | `rebuild3:packages/rebuild-engine/src/eval/scorers.ts` (pure scorers)<br>`rebuild3:rebuild3/lib/eval/intake/run.ts` (runner) | Lives in: engine + app. |

### Scope of work and reports

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Build SoW from estimate, with scope sentences <sub>`rb.sow.build`</sub> | built | none | `rebuild3:rebuild3/lib/sow/buildSOW.ts` (builder)<br>`rebuild3:rebuild3/lib/catalog/scope-copy.ts` (scope sentences) | Lives in: app. |
| SoW DOCX / Excel export <sub>`rb.sow.export`</sub> | built | none | `rebuild3:rebuild3/lib/reports/exportSOWDocx.ts` (docx)<br>`rebuild3:rebuild3/lib/reports/exportMasterSOWExcel.ts` (xlsx) | Lives in: app. |
| Lender, master scope, contractor, bid-request reports <sub>`rb.rep.reports`</sub> | built | read<br><sub>forvex_render_presentation</sub> | `rebuild3:rebuild3/components/reports/lender-report.tsx` (lender)<br>`rebuild3:rebuild3/components/reports/bid-request-report.tsx` (bid request) | Lives in: app. |
| Branded renovation budget workbook <sub>`rb.rep.budget-xlsx`</sub> | built | none | `rebuild3:rebuild3/lib/reports/exportSilverHillBudget.ts` (XLSX template) | Lives in: app. |
| True PDF generation <sub>`rb.rep.pdf`</sub> | **partial** | none | `rebuild3:rebuild3/components/field/field-action-hub.tsx` (Share PDF is preview + window.print()) | Lives in: app. |
| Client / contractor share link <sub>`rb.rep.share-link`</sub> | *not built* | n/a | `rebuild3:rebuild3/app/api/workspaces/[workspaceId]/invites/route.ts` (only workspace invites exist) | Lives in: app. |

### Project execution

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Finalize estimate into a project (and retract) <sub>`rb.ex.finalize`</sub> | built | none | `rebuild3:rebuild3/app/actions/finalize-estimate.ts` (action)<br>`rebuild3:supabase/migrations/20260316000000_finalize_estimate_to_execution.sql` (RPCs) | Lives in: app. |
| Budget vs actual with variance notes <sub>`rb.ex.budget-actual`</sub> | built | none | `rebuild3:rebuild3/app/actions/project-execution.ts` (recordProjectActualCost)<br>`rebuild3:rebuild3/components/dashboard/project-budget-tab.tsx` (UI) | Lives in: app. |
| Contractors, bids, bid groups <sub>`rb.ex.bids`</sub> | built | none | `rebuild3:rebuild3/app/actions/contractors.ts` (contractors)<br>`rebuild3:supabase/migrations/20260319000000_add_bid_groups.sql` (bid groups) | Lives in: app. |
| Status / progress updates <sub>`rb.ex.updates`</sub> | built | none | `rebuild3:rebuild3/components/dashboard/project-updates-tab.tsx` (updates tab) | Lives in: app. |
| Unexpected-scope bucket, deferred / cancelled lines <sub>`rb.ex.unexpected`</sub> | built | none | `rebuild3:supabase/migrations/20260923140000_unexpected_scope_and_removed_status.sql` (schema) | Lives in: app. |
| Formal change orders <sub>`rb.ex.change-orders`</sub> | *not built* | n/a | none (absence finding) | Lives in: app. No code or docs match. Unexpected-scope bucket is the closest. A forvex-change-order Claude skill exists outside the repos. |
| Draw schedules <sub>`rb.ex.draws`</sub> | *not built* | n/a | none (absence finding) | No code or docs match. |
| AI project debrief and insights <sub>`rb.ex.debrief`</sub> | built | none | `rebuild3:rebuild3/lib/projects/debrief-report.ts` (debrief)<br>`rebuild3:rebuild3/app/actions/ai/generate-project-insights.ts` (insights) | Lives in: app. |

### Valuation and platform

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| ARV / comps computation <sub>`rb.val.arv`</sub> | *not built* | n/a | `rebuild3:rebuild3/components/reports/master/FinancialBreakdown.tsx` (ARV and offer price displayed only) | By design: comps and ARV are owned by recontrol. |
| Property enrichment and project from deal <sub>`rb.val.enrich`</sub> | built | read+write<br><sub>forvex_resolve_property, forvex_open_or_create_project</sub> | `rebuild3:rebuild3/lib/projects/flattenRealieNested.ts` (Realie data)<br>`rebuild3:rebuild3/app/actions/projects/create-project-from-deal.ts` (project from deal) | Lives in: app. |
| Offline-first sync with conflict UI <sub>`rb.plat.offline`</sub> | built | none | `rebuild3:rebuild3/lib/db/sync-manager-v2.ts` (outbox sync)<br>`rebuild3:rebuild3/components/sync/sync-conflicts-panel.tsx` (conflict UI) | Lives in: app. |
| Installable PWA field mode <sub>`rb.plat.pwa`</sub> | built | none | `rebuild3:rebuild3/app/manifest.ts` (manifest) | Lives in: app. |
| Estimate RPCs for the forVEX MCP <sub>`rb.plat.mcp`</sub> | built | n/a | `rebuild3:rebuild3/lib/rpc/rebuild-mcp-rpcs.ts` (RPC wrappers)<br>`recontrol:lib/mcp/tools/preview_estimate.ts` (MCP tool) | Lives in: app + recontrol. |

## Deal iOS (`forvex-underwrite`)

**App filter:** No MCP, no LLM, no chat. No API keys on device. Server resolves, client recomputes, server persists. Not a comp tool, no map, not offline. *Source: forvex-underwrite:CLAUDE.md, forvex-underwrite:CONTRACTS.md, forvex-underwrite:README.md.*

### Intake

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Address autocomplete (Places proxied through recontrol) <sub>`dl.in.places`</sub> | built | none | `forvex-underwrite:src/api/places.ts` (proxy calls with session token)<br>`forvex-underwrite:src/screens/AddressScreen.tsx` (New deal tab) |  |
| Resolve property (physicals, ARV estimate, condition, flood) <sub>`dl.in.resolve`</sub> | built | read<br><sub>forvex_get_property, forvex_get_flood_data</sub> | `forvex-underwrite:src/api/property.ts` (POST /api/operate/property/resolve)<br>`forvex-underwrite:src/screens/PropertyBriefCard.tsx` (pre-save brief)<br>`forvex-underwrite:src/api/flood.ts` (FEMA flood) |  |

### Underwriting

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Six strategies side by side (flip, wholetail, wholesale, rental, BRRRR, assignment) <sub>`dl.uw.six`</sub> | built | read<br><sub>forvex_underwrite</sub> | `forvex-underwrite:src/strategies.ts` (order and labels)<br>`forvex-underwrite:src/screens/UnderwritingSummary.tsx` (strategy rows, best strategy, buy-box fit) |  |
| Verdict and deal score <sub>`dl.uw.verdict`</sub> | built | read<br><sub>forvex_underwrite</sub> | `forvex-underwrite:src/screens/UnderwritingSummary.tsx` (verdict and score out of 10) |  |
| Live knobs with on-device recompute and parity gate <sub>`dl.uw.knobs`</sub> | built | read<br><sub>forvex_underwrite</sub> | `forvex-underwrite:src/screens/DealScreen.tsx` (sliders re-run engine from effective_input)<br>`forvex-underwrite:src/engine/index.ts` (checkParity disables knobs on mismatch)<br>`forvex-underwrite:src/screens/knobRanges.ts` (ranges centred on server run) |  |
| MAO, target entry, breakeven <sub>`dl.uw.mao`</sub> | built | read<br><sub>forvex_underwrite</sub> | `forvex-underwrite:src/offerPrices.ts` (read from run, not solved on device) |  |
| Rehab input (pick saved estimate or tier total) <sub>`dl.uw.rehab`</sub> | built | read<br><sub>forvex_underwrite, forvex_get_estimate</sub> | `forvex-underwrite:src/screens/RehabSheet.tsx` (tier picker, link to REbuild) | No line-item estimator on device by design; REbuild owns that. |
| Cost breakdown per strategy <sub>`dl.uw.costs`</sub> | built | read<br><sub>forvex_underwrite</sub> | `forvex-underwrite:src/costLines.ts` (cost lines from engine rows) |  |
| Rent estimate with rent comps <sub>`dl.uw.rent`</sub> | **partial** | read<br><sub>forvex_get_rent_estimate</sub> | `forvex-underwrite:src/engine/index.ts` (rent knob starts from server rent) | No rent-comps display. |
| Buy box check <sub>`dl.uw.buybox`</sub> | built | read+write<br><sub>forvex_get_buy_box, forvex_save_buy_box</sub> | `forvex-underwrite:src/screens/UnderwritingSummary.tsx` (fit and excluded_reason per row) | Display only; buy boxes edited in recontrol. |

### Comps

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| ARV confidence pane (anchor ARV, median, grid, regression, AVM, not-used reasons) <sub>`dl.comps.pane`</sub> | built | read<br><sub>forvex_get_comps, forvex_get_comps_expanded, forvex_get_comp_detail</sub> | `forvex-underwrite:src/screens/CompsPane.tsx` (pane)<br>`forvex-underwrite:src/api/comps.ts` (GET /api/operate/comps)<br>`forvex-underwrite:src/charts/compChart.ts` (price vs size scatter with server-fit line) |  |
| Operator include / exclude comps <sub>`dl.comps.pick`</sub> | *not built* | n/a<br><sub>forvex_set_comp_override</sub> | `forvex-underwrite:src/screens/CompsPane.tsx` (included is server decision, read-only) | Readvise has overrides (rv.op.comps-evidence). |
| Comp map <sub>`dl.comps.map`</sub> | *not built* | n/a | `forvex-underwrite:README.md` ("There is no map.") | By design. |

### Pipeline and platform

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Save deal to shared pipeline (idempotent) <sub>`dl.pipe.save`</sub> | built | read+write<br><sub>forvex_save_deal, forvex_get_deal</sub> | `forvex-underwrite:src/api/underwrite.ts` (POST /api/operate/deals)<br>`forvex-underwrite:src/screens/DealScreen.tsx` (Save $X offer) |  |
| Deal list with stage chips, search, stale filter <sub>`dl.pipe.list`</sub> | built | read<br><sub>forvex_list_deals</sub> | `forvex-underwrite:src/screens/DealsScreen.tsx` (list)<br>`forvex-underwrite:src/api/deals.ts` (GET /api/operate/deals) |  |
| Reopen saved record and re-underwrite on today's comps <sub>`dl.pipe.reopen`</sub> | built | read+write<br><sub>forvex_get_deal, forvex_underwrite, forvex_save_deal</sub> | `forvex-underwrite:src/api/deal.ts` (GET saved analysis) |  |
| Change stage / disposition <sub>`dl.pipe.stage`</sub> | *not built* | n/a<br><sub>forvex_update_deal_disposition</sub> | none (absence finding) | Done in readvise / readvise-mobile per forvex-underwrite:CONTRACTS.md. |
| Market Sense pane <sub>`dl.plat.market`</sub> | built | read<br><sub>forvex_get_market_intelligence</sub> | `forvex-underwrite:src/screens/MarketPane.tsx` (pane)<br>`forvex-underwrite:src/api/market.ts` (API) |  |
| Choose which strategies show <sub>`dl.plat.strategies-pref`</sub> | built | read+write<br><sub>forvex_get_buy_box, forvex_save_buy_box</sub> | `forvex-underwrite:src/prefs/PrefsProvider.tsx` (per-device prefs) |  |
| Light / dark appearance <sub>`dl.plat.dark`</sub> | built | none | `forvex-underwrite:src/theme/appearance.ts` (Auto / Day / Night) |  |
| Sign in (no sign-up, no SSO) <sub>`dl.plat.auth`</sub> | built | read<br><sub>forvex_whoami</sub> | `forvex-underwrite:src/auth/AuthProvider.tsx` (Supabase email + password)<br>`forvex-underwrite:src/auth/secureStorage.ts` (Keychain chunked session) |  |
| Share / export (PDF, CSV, link) <sub>`dl.plat.share`</sub> | *not built* | n/a | none (absence finding) | No Share API, PDF or CSV code found. |
| Bulk / list screening <sub>`dl.plat.bulk`</sub> | *not built* | n/a | none (absence finding) | One address at a time; no bulk code. |
| Offline use <sub>`dl.plat.offline`</sub> | *not built* | n/a | `forvex-underwrite:README.md` ("Not offline.") | By decision. |
| AI / LLM / chat <sub>`dl.plat.ai`</sub> | *not built* | n/a | `forvex-underwrite:CLAUDE.md` (No MCP, no LLM, no chat) | By design. Route AI ideas to Readvise or recontrol MCP. |

## MCP layer (reference) (`recontrol`)

**App filter:** Owns the forvex_* / readvise_* MCP tools and the authoritative comp + underwriting engines (@nibblet/underwrite-engine 0.8.0). Tool name / input / output changes must be flagged to consumers. *Source: recontrol:CLAUDE.md.*

### Underwriting engine and comps

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Underwrite engine (six strategies) <sub>`mcp.uw.engine`</sub> | built | read<br><sub>forvex_underwrite</sub> | `recontrol:lib/mcp/underwrite/runUnderwrite.ts` (MCP wrapper)<br>`recontrol:packages/underwrite-engine/package.json` (@nibblet/underwrite-engine 0.8.0) |  |
| Comps, expanded comps, comp detail, overrides <sub>`mcp.uw.comps`</sub> | built | read+write<br><sub>forvex_get_comps, forvex_get_comps_expanded, forvex_get_comp_detail...</sub> | `recontrol:lib/mcp/tools/get_comps.ts` (tool) |  |
| ChatARV cross-check (vendor integration) <sub>`mcp.uw.chatarv`</sub> | built | read+write<br><sub>forvex_get_chatarv_comps</sub> | `recontrol:lib/mcp/tools/get_chatarv_comps.ts` (cached report or refresh (spends credit))<br>`recontrol:lib/mcp/chatarv/crossCheck.ts` (divergence_pct; never averaged into ARV) |  |
| Rent estimate <sub>`mcp.uw.rent`</sub> | built | read<br><sub>forvex_get_rent_estimate</sub> | `recontrol:lib/mcp/tools/get_rent_estimate.ts` (tool) |  |

### Outcomes and learning

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Record deal outcome with predicted vs actual error <sub>`mcp.out.record`</sub> | built | read+write<br><sub>forvex_record_deal_outcome, forvex_update_deal_outcome, forvex_list_deal_outcomes</sub> | `recontrol:lib/mcp/deals/recordDealOutcome.ts` (arv_error_pct, rehab_error_pct)<br>`recontrol:lib/mcp/deals/listDealOutcomes.ts` (missing_only finds deals lacking outcome) |  |
| Admin learning page with mean ARV error <sub>`mcp.out.learning`</sub> | built | read<br><sub>forvex_list_deal_outcomes, forvex_capture_deal_brief</sub> | `recontrol:lib/admin/learning.ts` (mean_arv_error_pct)<br>`recontrol:app/(dashboard)/learning/page.tsx` (admin page) |  |

### Sense pipeline

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Market data ingest and scoring (Redfin, Zillow, ACS, SAFMR, HUD) <sub>`mcp.sense.ingest`</sub> | built | read<br><sub>forvex_get_market_intelligence, forvex_get_market_brief</sub> | `recontrol:lib/sense/redfin-ingest.ts` (ingest)<br>`recontrol:lib/sense/scoring/market-scores-v2.ts` (scoring)<br>`recontrol:lib/sense/backtest/evaluate.ts` (backtest) |  |

### Presentations

| Capability | Status | Chat | Evidence | Note |
|---|---|---|---|---|
| Presentation, wholesale sheet, voice brief rendering <sub>`mcp.pres`</sub> | built | write<br><sub>forvex_render_presentation, forvex_build_wholesale_sheet, forvex_create_voice_brief</sub> | `recontrol:lib/mcp/tools/render_presentation.ts` (presentation)<br>`recontrol:lib/mcp/tools/build_wholesale_sheet.ts` (wholesale sheet) |  |

## Notes for review

- "Not built" rows with no evidence path are absence findings: a search of the repo found nothing. They cannot carry a file path by nature.
- Retired in readvise, not counted above: advisor chat engine and AI Ask (REBUILD_PLAN.md Phase 1b), weekly cross-lane synthesis cron, Advise CapEx UI, mobile web view (frozen).
- Some gaps map to Claude skills that live outside these repos (forvex-postmortem, forvex-change-order). Those are skills, not app capabilities, so they do not change the status here.
- Paul (2026-10-06): Readvise is the primary focus; mobile apps are extensions. redeal-mobile is superseded by forvex-underwrite (Deal) and is not mapped. readvise-mobile is not mapped in this pass.
- Paul (2026-10-06): the MCP layer stays in the map. It is the link between apps and the stand-in for what chat can do, so chat read / write coverage is tracked as its own lens.
- Phase 0 gate: status calls approved by Paul on 2026-10-06.
