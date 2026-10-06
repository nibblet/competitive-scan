"""Build competitive-scan/capability-map.{json,md} and verify every evidence path exists."""
import json, os, subprocess, sys

ROOT = "/home/user"
OUT = os.path.join(ROOT, "competitive-scan")
REPOS = {
    "readvise": "REadvise",
    "recontrol": "REcontrol",
    "rebuild3": "rebuild3",
    "forvex-underwrite": "forvex-underwrite",
}

def sha(repo):
    d = os.path.join(ROOT, REPOS[repo])
    s = subprocess.check_output(["git", "-C", d, "rev-parse", "--short", "HEAD"], text=True).strip()
    b = subprocess.check_output(["git", "-C", d, "branch", "--show-current"], text=True).strip()
    return {"commit": s, "branch": b}

def C(cid, name, status, ev, note="", where=None):
    return {"id": cid, "capability": name, "status": status,
            "evidence": [{"path": p, "shows": s} for p, s in ev],
            **({"location": where} if where else {}),
            **({"note": note} if note else {})}

APPS = [
 {
  "app": "Readvise", "repo": "readvise",
  "rule": "System of record for pipeline, tasks, notes. Consumes underwriting, does not own it. MCP tools live in recontrol, not here.",
  "rule_source": "readvise:CLAUDE.md",
  "modules": [
   {"module": "Sense", "capabilities": [
    C("rv.sense.market-explorer", "Tract / ZIP / neighborhood market explorer", "built", [
      ("readvise:pages/operate/sense.tsx", "Sense page mounting the market views"),
      ("readvise:components/operate/sense/views/MarketMemoryTab.tsx", "one of the Sense view tabs (Tracts, Zips, Neighborhoods, MarketForces alongside)"),
      ("readvise:pages/api/operate/sense", "about 60 routes for ACS, HUD, SAFMR, Zillow history, FRED, choropleths")]),
    C("rv.sense.market-brief", "Weekly market memory / AI market brief", "built", [
      ("readvise:pages/api/sense/market-memory/generate-week.ts", "generates the weekly narrative, signals and deltas"),
      ("readvise:components/operate/sense/views/MarketMemoryTab.tsx", "UI for the brief")]),
    C("rv.sense.news", "Local news brief", "built", [
      ("readvise:components/dashboard/LocalNewsBrief.tsx", "dashboard card"),
      ("readvise:pages/api/operate/sense/news/serpapi.ts", "SerpAPI news fetch")]),
    C("rv.sense.watchlist", "Tract / ZIP watchlist alerts", "built", [
      ("readvise:pages/api/sense/watchlist/index.ts", "watchlist CRUD"),
      ("readvise:lib/cron-tasks/sense-watchlist-check.ts", "daily cron writes in-app notifications")]),
    C("rv.sense.comp-intel-capture", "Competitor listing capture (daily SERP collector + manual paste)", "built", [
      ("readvise:lib/cron-tasks/competitive-intel.ts", "daily SERP ingest, persist, fuzzy match"),
      ("readvise:pages/api/sense/competitive-intel/capture.ts", "pasted text to competitive_listings")]),
    C("rv.sense.comp-intel-brief", "Competitive landscape brief (deal board, buyer registry, overlap, operators) with share link", "built", [
      ("readvise:pages/sense/competitive-intel/index.tsx", "brief and panels"),
      ("readvise:pages/share/intel/[token].tsx", "read-only share link")]),
    C("rv.sense.roundtrips", "Competitor buy / resell round trips from public records (plus self-audit)", "built", [
      ("readvise:pages/api/sense/competitive-intel/roundtrips.ts", "round-trip and hold-time computation")]),
    C("rv.sense.comp-discovery", "Competitor discovery review queue", "built", [
      ("readvise:pages/sense/competitive-intel/discoveries.tsx", "pending_review to active / archived / friendly_franchise"),
      ("readvise:pages/api/sense/competitive-intel/discoveries.ts", "API")]),
    C("rv.sense.comp-marketing", "Competitor mail-effort upload and marketing profile", "built", [
      ("readvise:pages/api/sense/competitive-intel/effort-upload.ts", "ZIP / weight CSV upload")]),
    C("rv.sense.openings", "Competitor openings (failed competitor listings as a lead list)", "partial", [
      ("readvise:lib/cron-tasks/competitor-openings.ts", "backend cron only")], note="Backend cron; no dedicated UI confirmed."),
    C("rv.sense.density", "Competitor density per neighborhood", "built", [
      ("readvise:components/operate/sense/views/CompetitorsTab.tsx", "density view")]),
    C("rv.sense.lost-deal-watch", "Records watch on deals we did not get", "not built", [
      ("readvise:docs/plans/DEAL_RECORDS_WATCH_PLAN.md", "says design agreed, not built")]),
   ]},
   {"module": "Operate", "capabilities": [
    C("rv.op.pipeline", "Pipeline / stage board, property list, map", "built", [
      ("readvise:pages/operate/index.tsx", "pipeline board"),
      ("readvise:pages/operate/map.tsx", "map view")]),
    C("rv.op.bulk-status", "Bulk status update across many properties", "built", [
      ("readvise:pages/api/operate/properties/bulk-update.ts", "multi-property status / update")]),
    C("rv.op.property-workspace", "Property detail workspace (overview, financials, comps, underwriting, workflow, notes, files)", "built", [
      ("readvise:components/operate/PropertyDetail.tsx", "workspace shell"),
      ("readvise:components/operate/tabs", "per-tab components")]),
    C("rv.op.comps-evidence", "Comps / ARV evidence with overrides (reads recontrol comp traces)", "built", [
      ("readvise:pages/api/operate/properties/[propertyId]/comps.ts", "reads comp trace"),
      ("readvise:pages/api/operate/properties/[propertyId]/comps/override.ts", "operator override")]),
    C("rv.op.reanalyze", "Re-underwrite one property (proxied to recontrol)", "built", [
      ("readvise:pages/api/operate/properties/[propertyId]/reanalyze.ts", "proxies to recontrol engine")]),
    C("rv.op.tasks", "Tasks and My Work (manual, AI-suggested, checklist, advisor)", "built", [
      ("readvise:pages/tasks.tsx", "task list"),
      ("readvise:pages/operate/my-work.tsx", "My Work view"),
      ("readvise:pages/api/operate/tasks/index.ts", "tasks API")]),
    C("rv.op.checklists", "Checklists and templates with trigger evaluator", "built", [
      ("readvise:pages/operate/checklists/templates.tsx", "template editor"),
      ("readvise:lib/operate/checklists/materialize.ts", "materialize into workflow nodes"),
      ("readvise:lib/checklist/trigger-evaluator.ts", "trigger evaluation")]),
    C("rv.op.staged-actions", "Staged AI actions the operator approves", "built", [
      ("readvise:components/operate/tabs/StagedActionsPanel.tsx", "approval panel"),
      ("readvise:pages/api/operate/workflow/ai-op.ts", "AI op endpoint")]),
    C("rv.op.daily-review", "Daily review queue (readvise_get_daily_review / decide_review_items)", "partial", [
      ("recontrol:lib/mcp/tools/readvise/dailyReview.ts", "MCP tool implementation")],
      note="No table, route or UI in readvise. Exists only as recontrol MCP tools. Paul (2026-10-06): in active use, needs validation."),
    C("rv.op.assignments", "Assignments and in-app notifications", "built", [
      ("readvise:pages/api/operate/assignments/index.ts", "assignment API"),
      ("readvise:components/notifications/NotificationBell.tsx", "in-app bell")]),
    C("rv.op.doc-generate", "Generate offer letter / purchase contract (.docx)", "built", [
      ("readvise:pages/api/operate/properties/[propertyId]/document.ts", "docx generation"),
      ("readvise:components/operate/DocumentGenerateModal.tsx", "UI")]),
    C("rv.op.dispo", "Dispo: wholesale sheet, presentation packet, voice brief", "built", [
      ("readvise:components/operate/dispo/WholesaleSheetModal.tsx", "wholesale sheet"),
      ("readvise:components/operate/presentation/PresentationPacketMenu.tsx", "presentation packet"),
      ("readvise:components/operate/tabs/underwriting/VoiceBriefListen.tsx", "voice brief")]),
    C("rv.op.exit-reasons", "Exit / lost reasons (closed lists mirrored from recontrol)", "built", [
      ("readvise:lib/operate/dispositionReasons.ts", "closed reason list")]),
    C("rv.op.war", "Weekly Activity Report (generate, edit, AI polish, mark sent)", "built", [
      ("readvise:pages/api/operate/reports/generate.ts", "generation"),
      ("readvise:components/operate/summary/WeeklyActivityReportCard.tsx", "UI")]),
   ]},
   {"module": "Operate > Documents and deadlines", "capabilities": [
    C("rv.doc.storage", "Deal document storage and listing", "partial", [
      ("readvise:lib/operate/dealDocuments.ts", "doc types: purchaseContract, settlementStatement, deed, titleCommitment"),
      ("readvise:pages/api/operate/properties/[propertyId]/files.ts", "GET only"),
      ("readvise:components/operate/tabs/FilesTab.tsx", "lists docs and closing figures")],
      note="Read-only in readvise. Uploads are written by recontrol (forVEX Scan / forvex_register_document)."),
    C("rv.doc.deadline-extract", "Contract contingency date extraction into deadline tasks", "partial", [
      ("recontrol:lib/mcp/memory/extractScan.ts", "LLM extractor over phone-OCR text: parties, dates, dated obligations"),
      ("recontrol:lib/mcp/memory/obligations.ts", "turns inspection, financing, earnest money, closing into tasks, idempotent"),
      ("readvise:supabase/migrations/20260921160000_readvise_tasks_source_document_obligation.sql", "readvise accepts source='document_obligation' tasks with target_date")],
      note="Extraction and task creation are built (recontrol). Gap: no deadline-specific UI in readvise; obligations show up as ordinary tasks. OCR happens on the phone; no server-side OCR found."),
    C("rv.doc.key-date-alerts", "Key-date risk alerts (option expiry, expected close)", "built", [
      ("readvise:lib/operate/dealRisk.ts", "scores key dates (around lines 199 to 226)"),
      ("readvise:lib/cron-tasks/deal-at-risk.ts", "weekly cron writes insights and follow-up task"),
      ("readvise:pages/api/workspaces/[workspaceId]/alert-settings.ts", "per-workspace thresholds")]),
    C("rv.doc.settlement-actuals", "Apply settlement statement actuals to deal outcome", "built", [
      ("recontrol:lib/mcp/documents/applyDocumentFacts.ts", "writes actual purchase / sale price with fill / match / conflict preview")],
      note="MCP only (forvex_apply_document_facts)."),
    C("rv.doc.esign", "E-signature / signature chasing", "not built", [],
      note="Explorer found no DocuSign, e-sign or signature-tracking code in readvise."),
    C("rv.doc.client-portal", "Client / seller portal", "not built", [
      ("readvise:pages/share/intel/[token].tsx", "only read-only share link that exists (competitive brief)")]),
    C("rv.doc.outbound-reminders", "Outbound email / SMS reminders", "not built", [
      ("readvise:lib/notifications/createNotification.ts", "notifications are in-app only"),
      ("readvise:docs/plans/REFLECT2_WHATSAPP_CAPTURE_PLAN.md", "WhatsApp capture planned only")]),
   ]},
   {"module": "Operate > Local deal flow", "capabilities": [
    C("rv.flow.marketplace-triage", "Marketplace Stage 0 triage (paste many emails, rule-scored KILL / WATCH / PULL_ADDRESS)", "built", [
      ("readvise:components/operate/marketplace/MarketplaceIntakePanel.tsx", "paste-many intake"),
      ("readvise:lib/marketplace/ingest.ts", "batch ingest"),
      ("readvise:docs/MARKETPLACE_TRIAGE_STAGE0_RULESET_V0.1.md", "DRAFT ruleset, market-level, zero-address")],
      note="Property-level Stage 1 not built."),
    C("rv.flow.chatarv-pull", "Pull ChatARV comps on won lead", "built", [
      ("readvise:lib/marketplace/triggerChatarvPull.ts", "calls chatarv-run-comps edge function")]),
    C("rv.flow.bulk-csv-underwrite", "CSV import of many addresses with bulk underwriting", "not built", [
      ("recontrol:app/api/operate/reanalyze/route.ts", "server re-runs one property at a time")],
      note="No bulk route in readvise or recontrol. Only CSV imports are rent roll, competitor mail effort, mailer segments, market data."),
   ]},
   {"module": "Track", "capabilities": [
    C("rv.track.dashboards", "Metrics dashboards (funnel, cycle time, profit by exit / lead source)", "built", [
      ("readvise:pages/track/index.tsx", "Track page"),
      ("readvise:pages/api/track/metrics", "metrics APIs"),
      ("readvise:lib/track/chartRegistry.tsx", "chart registry")]),
    C("rv.track.capital", "Capital runway / pool planner", "built", [
      ("readvise:components/track/CapitalView.tsx", "UI"),
      ("readvise:pages/api/track/capital/runway.ts", "API")]),
    C("rv.track.cfo", "CFO insight and AI explore", "built", [
      ("readvise:pages/api/track/cfo-insight.ts", "CFO insight"),
      ("readvise:pages/api/track/ai/explore.ts", "AI explore")]),
    C("rv.track.planned-vs-actual", "Per-deal planned vs actual (ARV vs sale price, rehab estimate vs actual)", "built", [
      ("readvise:components/operate/tabs/overview/OutcomeReview.tsx", "mounted in OverviewTab"),
      ("readvise:lib/checklist/outcome-capture.ts", "writes core.deal_outcomes on SOLD"),
      ("recontrol:lib/mcp/deals/recordDealOutcome.ts", "returns arv_error_pct and rehab_error_pct")]),
    C("rv.track.arv-scoreboard", "ARV accuracy scoreboard (estimated vs actual, by band, over time)", "partial", [
      ("readvise:lib/track/templates/arvAccuracyProfile.server.ts", "server computation built"),
      ("readvise:components/track/drivers/ARVAccuracyCard.tsx", "card built"),
      ("readvise:lib/track/chartRegistry.tsx", "card registered enabled: false (line 114)")],
      note="Also an aggregate mean_arv_error_pct on recontrol admin page recontrol:app/(dashboard)/learning/page.tsx. Internal only; nothing public-facing."),
    C("rv.track.decision-revisit", "Revisit stale or drifted underwriting decisions", "built", [
      ("readvise:lib/operate/decisionRevisit.ts", "cron logic")]),
    C("rv.track.cost-per-x", "Marketing efficiency (cost per lead / contract / close)", "partial", [
      ("readvise:lib/track/chartRegistry.tsx", "cards registered enabled: false"),
      ("readvise:pages/api/operate/metrics/marketing-capital-bridge.ts", "bridge metric API")]),
    C("rv.track.postmortem", "Deal postmortems", "not built", [
      ("readvise:docs/roadmap/Roadmap_next.md", "mentioned in roadmap only")],
      note="A postmortem Claude skill exists outside the repos (forvex-postmortem)."),
   ]},
   {"module": "Portfolio / Rentals", "capabilities": [
    C("rv.rent.portfolio", "Rental portfolio dashboard with CSV import / export and AI review", "built", [
      ("readvise:pages/operate/rentals.tsx", "page"),
      ("readvise:components/operate/rentals/RentalPortfolioView.tsx", "view, import / export"),
      ("readvise:pages/api/operate/rentals/analyze.ts", "AI review")]),
    C("rv.rent.per-property", "Per-rental tabs (ops, debt, equity, value)", "built", [
      ("readvise:components/operate/tabs/rental", "tab components")]),
    C("rv.rent.rent-roll", "Rent roll / lease snapshots", "partial", [
      ("readvise:supabase/migrations/20260924120000_rental_lease_snapshots.sql", "table"),
      ("readvise:lib/operate/hooks/rental/attachLeaseUnits.ts", "read into rollups"),
      ("recontrol:lib/mcp/tools/readvise/parseRentRoll.ts", "written via MCP")]),
    C("rv.rent.capex", "CapEx watch list", "partial", [
      ("readvise:supabase/migrations/20260915180000_property_capex_items.sql", "data only, comment says CapEx UI removed")]),
    C("rv.rent.posture", "Portfolio posture and badges", "built", [
      ("readvise:components/operate/summary/PortfolioPostureCard.tsx", "card")]),
    C("rv.rent.cross-workspace", "Cross-workspace portfolio metrics", "partial", [
      ("readvise:pages/api/portfolio/metrics.ts", "API exists, no UI consumer found")]),
   ]},
   {"module": "Pulse / Reflect / Knowledge", "capabilities": [
    C("rv.pulse.capture", "Pulse capture with AI enrich / normalize / property resolution", "built", [
      ("readvise:components/reflect/PulseCaptureModal.tsx", "capture"),
      ("readvise:pages/api/pulse/analyze.ts", "AI analyze")]),
    C("rv.pulse.reflect", "Reflect timeline and weekly rollup", "built", [
      ("readvise:pages/reflect/index.tsx", "page"),
      ("readvise:pages/api/reflect/week.ts", "weekly rollup")]),
    C("rv.pulse.debrief", "Debriefs (from pulse, accountability)", "built", [
      ("readvise:pages/api/debrief/pulse/[pulse_id].ts", "debrief from pulse")]),
    C("rv.pulse.inbound-email", "Inbound email to pulse", "built", [
      ("readvise:pages/api/inbound/email.ts", "Postmark inbound"),
      ("readvise:lib/inboundEmail/adapters/postmark.ts", "adapter")]),
    C("rv.pulse.search", "Global search", "built", [
      ("readvise:pages/api/search/index.ts", "search_global RPC")]),
    C("rv.pulse.cmo", "CMO social command center (read-only snapshot)", "partial", [
      ("readvise:components/social/SocialCommandCenter.tsx", "UI"),
      ("readvise:pages/api/cmo/snapshot.ts", "reads snapshot written by recontrol")]),
   ]},
  ]},
 {
  "app": "REbuild", "repo": "rebuild3",
  "rule": "Estimate logic lives in the pure engine package (packages/rebuild-engine). Changes there move CONTRACT_VERSION (currently 0.3.0) and affect recontrol and readvise.",
  "rule_source": "rebuild3:CLAUDE.md, rebuild3:packages/rebuild-engine/src/contract-version.ts",
  "modules": [
   {"module": "Estimates", "capabilities": [
    C("rb.est.calc", "Rule-based estimate calculation (quantity drivers, rounding, overrides)", "built", [
      ("rebuild3:packages/rebuild-engine/src/engine/calculator/calculate-estimate.ts", "calculateEstimate"),
      ("rebuild3:packages/rebuild-engine/src/engine/calculator/quantity.ts", "quantity from sqft / rooms / fixed")], where="engine"),
    C("rb.est.condition", "Condition (severity) pricing per category", "built", [
      ("rebuild3:packages/rebuild-engine/src/category-scope.ts", "scope depth per category"),
      ("rebuild3:rebuild3/app/actions/profile-rules.ts", "profile rule CRUD")], where="engine + app"),
    C("rb.est.triangulation", "Triangulation: $/sqft band vs severity vs bottom-up, variance flag", "partial", [
      ("rebuild3:packages/rebuild-engine/src/rehab-summary.ts", "computeSqftBandCrossCheck, isVarianceFlagged"),
      ("rebuild3:rebuild3/components/field/estimate-triangulation-panel.tsx", "UI panel"),
      ("rebuild3:ESTIMATE_MODEL_V2.md", "three stored modes planned, partly wired")], where="engine + app"),
    C("rb.est.scenarios", "Multiple scenarios side by side", "partial", [
      ("rebuild3:rebuild3/components/field/profile-selector.tsx", "switch rehab profile"),
      ("rebuild3:packages/rebuild-engine/src/wholetail-scope.ts", "wholetail vs full rehab read")],
      note="No general scenario object or side-by-side comparison.", where="engine + app"),
    C("rb.est.allowances", "Contingency, allowance and free-text lines", "built", [
      ("rebuild3:supabase/migrations/20260322000000_estimate_model_v2_phase9.sql", "schema"),
      ("rebuild3:rebuild3/lib/estimates/v2-line-item.ts", "line shape")], where="app"),
    C("rb.est.audit", "Deal audit / risk flags (AI + rules)", "built", [
      ("rebuild3:rebuild3/app/actions/ai/audit-deal.ts", "AI audit"),
      ("rebuild3:rebuild3/lib/logic/auditor.ts", "rules")], where="app"),
   ]},
   {"module": "Pricing", "capabilities": [
    C("rb.price.library", "Line-item cost library", "built", [
      ("rebuild3:rebuild3/app/(dashboard)/library/page.tsx", "library page"),
      ("rebuild3:rebuild3/app/actions/library.ts", "actions")], where="app"),
    C("rb.price.books", "Named, duplicable price books", "built", [
      ("rebuild3:rebuild3/app/actions/price-books.ts", "actions"),
      ("rebuild3:rebuild3/components/dashboard/price-book-editor.tsx", "editor")], where="app"),
    C("rb.price.regional", "Regional / ZIP cost index", "partial", [
      ("rebuild3:supabase/migrations/20260321000000_builder_preferences.sql", "per-user $/sqft baselines only")],
      note="No ZIP or market cost index.", where="app"),
    C("rb.price.nec", "National Estimator Cloud cost comparison", "partial", [
      ("rebuild3:rebuild3/lib/nec/client.ts", "sandbox API client"),
      ("rebuild3:rebuild3/components/dashboard/nec-compare-panel.tsx", "only in price-book header")], where="app"),
    C("rb.price.curation", "Catalog curation queue", "built", [
      ("rebuild3:rebuild3/components/dashboard/curation-queue.tsx", "queue"),
      ("rebuild3:rebuild3/app/actions/approve-catalog-item.ts", "approve")], where="app"),
   ]},
   {"module": "Intake", "capabilities": [
    C("rb.in.walkthrough", "Room-by-room walkthrough with condition signals", "built", [
      ("rebuild3:rebuild3/app/(field)/field/projects/[id]/walkthrough/page.tsx", "page"),
      ("rebuild3:rebuild3/components/walkthrough/walkthrough-container.tsx", "container")], where="app"),
    C("rb.in.inference", "Rule-based condition inference", "built", [
      ("rebuild3:rebuild3/lib/inference/run-inference.ts", "signals to severity to tier")], where="app"),
    C("rb.in.voice", "Voice intake (transcribe + AI extraction)", "built", [
      ("rebuild3:rebuild3/app/actions/voice/transcribe-audio.ts", "transcribe"),
      ("rebuild3:rebuild3/app/actions/voice/analyze-intake.ts", "extract")], where="app"),
    C("rb.in.photo", "Photo analysis", "built", [
      ("rebuild3:rebuild3/app/actions/ai/analyze-image.ts", "image analysis"),
      ("rebuild3:rebuild3/components/ai/photo-analyzer.tsx", "UI")], where="app"),
    C("rb.in.text", "Free-text multi-agent extraction", "built", [
      ("rebuild3:rebuild3/lib/ai/text-estimate-swarm.ts", "swarm")], where="app"),
    C("rb.in.sku", "SKU mapping, autoscope, gap detection", "built", [
      ("rebuild3:packages/rebuild-engine/src/intake/autoscope.ts", "AI items to SKUs"),
      ("rebuild3:packages/rebuild-engine/src/intake/gap-detector.ts", "gap detection")], where="engine"),
    C("rb.in.eval", "Intake eval harness (golden set, hallucination check)", "built", [
      ("rebuild3:packages/rebuild-engine/src/eval/scorers.ts", "pure scorers"),
      ("rebuild3:rebuild3/lib/eval/intake/run.ts", "runner")], where="engine + app"),
   ]},
   {"module": "Scope of work and reports", "capabilities": [
    C("rb.sow.build", "Build SoW from estimate, with scope sentences", "built", [
      ("rebuild3:rebuild3/lib/sow/buildSOW.ts", "builder"),
      ("rebuild3:rebuild3/lib/catalog/scope-copy.ts", "scope sentences")], where="app"),
    C("rb.sow.export", "SoW DOCX / Excel export", "built", [
      ("rebuild3:rebuild3/lib/reports/exportSOWDocx.ts", "docx"),
      ("rebuild3:rebuild3/lib/reports/exportMasterSOWExcel.ts", "xlsx")], where="app"),
    C("rb.rep.reports", "Lender, master scope, contractor, bid-request reports", "built", [
      ("rebuild3:rebuild3/components/reports/lender-report.tsx", "lender"),
      ("rebuild3:rebuild3/components/reports/bid-request-report.tsx", "bid request")], where="app"),
    C("rb.rep.budget-xlsx", "Branded renovation budget workbook", "built", [
      ("rebuild3:rebuild3/lib/reports/exportSilverHillBudget.ts", "XLSX template")], where="app"),
    C("rb.rep.pdf", "True PDF generation", "partial", [
      ("rebuild3:rebuild3/components/field/field-action-hub.tsx", "Share PDF is preview + window.print()")], where="app"),
    C("rb.rep.share-link", "Client / contractor share link", "not built", [
      ("rebuild3:rebuild3/app/api/workspaces/[workspaceId]/invites/route.ts", "only workspace invites exist")], where="app"),
   ]},
   {"module": "Project execution", "capabilities": [
    C("rb.ex.finalize", "Finalize estimate into a project (and retract)", "built", [
      ("rebuild3:rebuild3/app/actions/finalize-estimate.ts", "action"),
      ("rebuild3:supabase/migrations/20260316000000_finalize_estimate_to_execution.sql", "RPCs")], where="app"),
    C("rb.ex.budget-actual", "Budget vs actual with variance notes", "built", [
      ("rebuild3:rebuild3/app/actions/project-execution.ts", "recordProjectActualCost"),
      ("rebuild3:rebuild3/components/dashboard/project-budget-tab.tsx", "UI")], where="app"),
    C("rb.ex.bids", "Contractors, bids, bid groups", "built", [
      ("rebuild3:rebuild3/app/actions/contractors.ts", "contractors"),
      ("rebuild3:supabase/migrations/20260319000000_add_bid_groups.sql", "bid groups")], where="app"),
    C("rb.ex.updates", "Status / progress updates", "built", [
      ("rebuild3:rebuild3/components/dashboard/project-updates-tab.tsx", "updates tab")], where="app"),
    C("rb.ex.unexpected", "Unexpected-scope bucket, deferred / cancelled lines", "built", [
      ("rebuild3:supabase/migrations/20260923140000_unexpected_scope_and_removed_status.sql", "schema")], where="app"),
    C("rb.ex.change-orders", "Formal change orders", "not built", [],
      note="No code or docs match. Unexpected-scope bucket is the closest. A forvex-change-order Claude skill exists outside the repos.", where="app"),
    C("rb.ex.draws", "Draw schedules", "not built", [], note="No code or docs match."),
    C("rb.ex.debrief", "AI project debrief and insights", "built", [
      ("rebuild3:rebuild3/lib/projects/debrief-report.ts", "debrief"),
      ("rebuild3:rebuild3/app/actions/ai/generate-project-insights.ts", "insights")], where="app"),
   ]},
   {"module": "Valuation and platform", "capabilities": [
    C("rb.val.arv", "ARV / comps computation", "not built", [
      ("rebuild3:rebuild3/components/reports/master/FinancialBreakdown.tsx", "ARV and offer price displayed only")],
      note="By design: comps and ARV are owned by recontrol."),
    C("rb.val.enrich", "Property enrichment and project from deal", "built", [
      ("rebuild3:rebuild3/lib/projects/flattenRealieNested.ts", "Realie data"),
      ("rebuild3:rebuild3/app/actions/projects/create-project-from-deal.ts", "project from deal")], where="app"),
    C("rb.plat.offline", "Offline-first sync with conflict UI", "built", [
      ("rebuild3:rebuild3/lib/db/sync-manager-v2.ts", "outbox sync"),
      ("rebuild3:rebuild3/components/sync/sync-conflicts-panel.tsx", "conflict UI")], where="app"),
    C("rb.plat.pwa", "Installable PWA field mode", "built", [
      ("rebuild3:rebuild3/app/manifest.ts", "manifest")], where="app"),
    C("rb.plat.mcp", "Estimate RPCs for the forVEX MCP", "built", [
      ("rebuild3:rebuild3/lib/rpc/rebuild-mcp-rpcs.ts", "RPC wrappers"),
      ("recontrol:lib/mcp/tools/preview_estimate.ts", "MCP tool")], where="app + recontrol"),
   ]},
  ]},
 {
  "app": "Deal iOS", "repo": "forvex-underwrite",
  "rule": "No MCP, no LLM, no chat. No API keys on device. Server resolves, client recomputes, server persists. Not a comp tool, no map, not offline.",
  "rule_source": "forvex-underwrite:CLAUDE.md, forvex-underwrite:CONTRACTS.md, forvex-underwrite:README.md",
  "modules": [
   {"module": "Intake", "capabilities": [
    C("dl.in.places", "Address autocomplete (Places proxied through recontrol)", "built", [
      ("forvex-underwrite:src/api/places.ts", "proxy calls with session token"),
      ("forvex-underwrite:src/screens/AddressScreen.tsx", "New deal tab")]),
    C("dl.in.resolve", "Resolve property (physicals, ARV estimate, condition, flood)", "built", [
      ("forvex-underwrite:src/api/property.ts", "POST /api/operate/property/resolve"),
      ("forvex-underwrite:src/screens/PropertyBriefCard.tsx", "pre-save brief"),
      ("forvex-underwrite:src/api/flood.ts", "FEMA flood")]),
   ]},
   {"module": "Underwriting", "capabilities": [
    C("dl.uw.six", "Six strategies side by side (flip, wholetail, wholesale, rental, BRRRR, assignment)", "built", [
      ("forvex-underwrite:src/strategies.ts", "order and labels"),
      ("forvex-underwrite:src/screens/UnderwritingSummary.tsx", "strategy rows, best strategy, buy-box fit")]),
    C("dl.uw.verdict", "Verdict and deal score", "built", [
      ("forvex-underwrite:src/screens/UnderwritingSummary.tsx", "verdict and score out of 10")]),
    C("dl.uw.knobs", "Live knobs with on-device recompute and parity gate", "built", [
      ("forvex-underwrite:src/screens/DealScreen.tsx", "sliders re-run engine from effective_input"),
      ("forvex-underwrite:src/engine/index.ts", "checkParity disables knobs on mismatch"),
      ("forvex-underwrite:src/screens/knobRanges.ts", "ranges centred on server run")]),
    C("dl.uw.mao", "MAO, target entry, breakeven", "built", [
      ("forvex-underwrite:src/offerPrices.ts", "read from run, not solved on device")]),
    C("dl.uw.rehab", "Rehab input (pick saved estimate or tier total)", "built", [
      ("forvex-underwrite:src/screens/RehabSheet.tsx", "tier picker, link to REbuild")],
      note="No line-item estimator on device by design; REbuild owns that."),
    C("dl.uw.costs", "Cost breakdown per strategy", "built", [
      ("forvex-underwrite:src/costLines.ts", "cost lines from engine rows")]),
    C("dl.uw.rent", "Rent estimate with rent comps", "partial", [
      ("forvex-underwrite:src/engine/index.ts", "rent knob starts from server rent")],
      note="No rent-comps display."),
    C("dl.uw.buybox", "Buy box check", "built", [
      ("forvex-underwrite:src/screens/UnderwritingSummary.tsx", "fit and excluded_reason per row")],
      note="Display only; buy boxes edited in recontrol."),
   ]},
   {"module": "Comps", "capabilities": [
    C("dl.comps.pane", "ARV confidence pane (anchor ARV, median, grid, regression, AVM, not-used reasons)", "built", [
      ("forvex-underwrite:src/screens/CompsPane.tsx", "pane"),
      ("forvex-underwrite:src/api/comps.ts", "GET /api/operate/comps"),
      ("forvex-underwrite:src/charts/compChart.ts", "price vs size scatter with server-fit line")]),
    C("dl.comps.pick", "Operator include / exclude comps", "not built", [
      ("forvex-underwrite:src/screens/CompsPane.tsx", "included is server decision, read-only")],
      note="Readvise has overrides (rv.op.comps-evidence)."),
    C("dl.comps.map", "Comp map", "not built", [
      ("forvex-underwrite:README.md", "\"There is no map.\"")], note="By design."),
   ]},
   {"module": "Pipeline and platform", "capabilities": [
    C("dl.pipe.save", "Save deal to shared pipeline (idempotent)", "built", [
      ("forvex-underwrite:src/api/underwrite.ts", "POST /api/operate/deals"),
      ("forvex-underwrite:src/screens/DealScreen.tsx", "Save $X offer")]),
    C("dl.pipe.list", "Deal list with stage chips, search, stale filter", "built", [
      ("forvex-underwrite:src/screens/DealsScreen.tsx", "list"),
      ("forvex-underwrite:src/api/deals.ts", "GET /api/operate/deals")]),
    C("dl.pipe.reopen", "Reopen saved record and re-underwrite on today's comps", "built", [
      ("forvex-underwrite:src/api/deal.ts", "GET saved analysis")]),
    C("dl.pipe.stage", "Change stage / disposition", "not built", [], note="Done in readvise / readvise-mobile per forvex-underwrite:CONTRACTS.md."),
    C("dl.plat.market", "Market Sense pane", "built", [
      ("forvex-underwrite:src/screens/MarketPane.tsx", "pane"),
      ("forvex-underwrite:src/api/market.ts", "API")]),
    C("dl.plat.strategies-pref", "Choose which strategies show", "built", [
      ("forvex-underwrite:src/prefs/PrefsProvider.tsx", "per-device prefs")]),
    C("dl.plat.dark", "Light / dark appearance", "built", [
      ("forvex-underwrite:src/theme/appearance.ts", "Auto / Day / Night")]),
    C("dl.plat.auth", "Sign in (no sign-up, no SSO)", "built", [
      ("forvex-underwrite:src/auth/AuthProvider.tsx", "Supabase email + password"),
      ("forvex-underwrite:src/auth/secureStorage.ts", "Keychain chunked session")]),
    C("dl.plat.share", "Share / export (PDF, CSV, link)", "not built", [], note="No Share API, PDF or CSV code found."),
    C("dl.plat.bulk", "Bulk / list screening", "not built", [], note="One address at a time; no bulk code."),
    C("dl.plat.offline", "Offline use", "not built", [("forvex-underwrite:README.md", "\"Not offline.\"")], note="By decision."),
    C("dl.plat.ai", "AI / LLM / chat", "not built", [("forvex-underwrite:CLAUDE.md", "No MCP, no LLM, no chat")], note="By design. Route AI ideas to Readvise or recontrol MCP."),
   ]},
  ]},
 {
  "app": "MCP layer (reference)", "repo": "recontrol",
  "rule": "Owns the forvex_* / readvise_* MCP tools and the authoritative comp + underwriting engines (@nibblet/underwrite-engine 0.8.0). Tool name / input / output changes must be flagged to consumers.",
  "rule_source": "recontrol:CLAUDE.md",
  "modules": [
   {"module": "Underwriting engine and comps", "capabilities": [
    C("mcp.uw.engine", "Underwrite engine (six strategies)", "built", [
      ("recontrol:lib/mcp/underwrite/runUnderwrite.ts", "MCP wrapper"),
      ("recontrol:packages/underwrite-engine/package.json", "@nibblet/underwrite-engine 0.8.0")]),
    C("mcp.uw.comps", "Comps, expanded comps, comp detail, overrides", "built", [
      ("recontrol:lib/mcp/tools/get_comps.ts", "tool")]),
    C("mcp.uw.chatarv", "ChatARV cross-check (vendor integration)", "built", [
      ("recontrol:lib/mcp/tools/get_chatarv_comps.ts", "cached report or refresh (spends credit)"),
      ("recontrol:lib/mcp/chatarv/crossCheck.ts", "divergence_pct; never averaged into ARV")]),
    C("mcp.uw.rent", "Rent estimate", "built", [("recontrol:lib/mcp/tools/get_rent_estimate.ts", "tool")]),
   ]},
   {"module": "Outcomes and learning", "capabilities": [
    C("mcp.out.record", "Record deal outcome with predicted vs actual error", "built", [
      ("recontrol:lib/mcp/deals/recordDealOutcome.ts", "arv_error_pct, rehab_error_pct"),
      ("recontrol:lib/mcp/deals/listDealOutcomes.ts", "missing_only finds deals lacking outcome")]),
    C("mcp.out.learning", "Admin learning page with mean ARV error", "built", [
      ("recontrol:lib/admin/learning.ts", "mean_arv_error_pct"),
      ("recontrol:app/(dashboard)/learning/page.tsx", "admin page")]),
   ]},
   {"module": "Sense pipeline", "capabilities": [
    C("mcp.sense.ingest", "Market data ingest and scoring (Redfin, Zillow, ACS, SAFMR, HUD)", "built", [
      ("recontrol:lib/sense/redfin-ingest.ts", "ingest"),
      ("recontrol:lib/sense/scoring/market-scores-v2.ts", "scoring"),
      ("recontrol:lib/sense/backtest/evaluate.ts", "backtest")]),
   ]},
   {"module": "Presentations", "capabilities": [
    C("mcp.pres", "Presentation, wholesale sheet, voice brief rendering", "built", [
      ("recontrol:lib/mcp/tools/render_presentation.ts", "presentation"),
      ("recontrol:lib/mcp/tools/build_wholesale_sheet.ts", "wholesale sheet")]),
   ]},
  ]},
]

HYPOTHESES = [
 {"hypothesis": "DeedSpring contract deadline extraction vs our document flow",
  "finding": "Partly built, as you guessed. The LLM extractor and forvex_materialize_obligations already turn inspection, financing, earnest money and closing dates into tasks (recontrol). Missing: a deadline view in readvise (they show as ordinary tasks), any outbound reminder (in-app only), e-signature, and a client portal. OCR happens on the phone only.",
  "cells": ["rv.doc.deadline-extract", "rv.doc.key-date-alerts", "rv.doc.outbound-reminders", "rv.doc.esign", "rv.doc.client-portal"]},
 {"hypothesis": "Resideline accuracy scoreboard vs our outcomes data",
  "finding": "Closer than expected. Per-deal ARV and rehab error is already computed and stored (core.deal_outcomes), there is an admin mean ARV error in recontrol, and readvise has a fully built ARV Accuracy card that is switched off (enabled: false). The data foundation exists; it is internal only.",
  "cells": ["rv.track.planned-vs-actual", "rv.track.arv-scoreboard", "mcp.out.record", "mcp.out.learning"]},
 {"hypothesis": "Resideline bulk CSV screening vs Deal one-address flow",
  "finding": "Not built anywhere. Deal's rules do not forbid it (it is not AI). Open question: does a bulk screen belong in Deal, or as a readvise / recontrol server job on the same engine, given Deal is built for one address on a driveway? Readvise's Marketplace Stage 0 triage is the nearest existing pattern (paste many, rule-scored), but it is market-level, not address-level.",
  "cells": ["rv.flow.bulk-csv-underwrite", "rv.flow.marketplace-triage", "dl.plat.bulk"]},
]

def check(path):
    repo, rel = path.split(":", 1)
    return os.path.exists(os.path.join(ROOT, REPOS[repo], rel))

missing = []
counts = {}
for app in APPS:
    app["repo_state"] = sha(app["repo"])
    for m in app["modules"]:
        for c in m["capabilities"]:
            counts[c["status"]] = counts.get(c["status"], 0) + 1
            for e in c["evidence"]:
                if not check(e["path"]):
                    missing.append((c["id"], e["path"]))
for src in ["readvise:CLAUDE.md"]:
    pass

COV = json.load(open(os.path.join(OUT, "mcp-coverage.json")))["coverage"]
all_ids = [c["id"] for a in APPS for m in a["modules"] for c in m["capabilities"]]
for cid in all_ids:
    if cid not in COV: missing.append((cid, "NO MCP COVERAGE ENTRY"))
for cid in COV:
    if cid not in all_ids: missing.append((cid, "COVERAGE FOR UNKNOWN ID"))
    elif not check(COV[cid]["evidence"]): missing.append((cid, COV[cid]["evidence"]))
chat_counts = {}
for a in APPS:
    a["chat_counts"] = {}
    for m in a["modules"]:
        for c in m["capabilities"]:
            cv = COV.get(c["id"])
            if cv:
                c["chat"] = cv
                chat_counts[cv["access"]] = chat_counts.get(cv["access"], 0) + 1
                a["chat_counts"][cv["access"]] = a["chat_counts"].get(cv["access"], 0) + 1

if missing:
    print("MISSING EVIDENCE PATHS:")
    for m in missing: print(" ", *m)
    sys.exit(1)

doc = {
  "generated": "2026-10-06",
  "phase": "0",
  "status_values": ["built", "partial", "not built"],
  "status_definitions": {
    "built": "UI (or tool), API and data path all present in code",
    "partial": "some layer missing, flagged off, stubbed, or backend only",
    "not built": "absent from code, or in docs / plans only"},
  "evidence_format": "<repo>:<path relative to repo root>",
  "repos": {r: sha(r) for r in REPOS},
  "counts": counts,
  "chat_access_counts": chat_counts,
  "chat_access_source": "mcp-coverage.json",
  "apps": APPS,
  "seed_hypotheses": HYPOTHESES,
}
with open(os.path.join(OUT, "capability-map.json"), "w") as f:
    json.dump(doc, f, indent=2)

# ---------- markdown ----------
L = []
L.append("# Capability map (Phase 0)\n")
L.append("Generated 2026-10-06 from code, read-only. Every evidence path below was checked to exist on disk at the commits listed. Machine-readable copy: `capability-map.json`.\n")
L.append("**Status:** `built` = UI (or tool), API and data path present. `partial` = a layer missing, flagged off, or backend only. `not built` = absent from code or in plans only.\n")
L.append("**Evidence format:** `repo:path`.\n")
L.append("| Repo | Branch | Commit |\n|---|---|---|")
for r, s in doc["repos"].items():
    L.append(f"| {r} | {s['branch']} | {s['commit']} |")
total = sum(counts.values())
ORDER = ["read+write", "read", "write", "none", "n/a"]
L.append(f"\n**Chat access through MCP** (column \"Chat\", detail in `mcp-coverage.json`): " + ", ".join(f"{chat_counts.get(k,0)} {k}" for k in ORDER) + ". `n/a` = not built, or is the MCP layer itself.\n")
L.append("| App | " + " | ".join(ORDER) + " |\n|---|" + "---|" * len(ORDER))
for a in APPS:
    L.append(f"| {a['app']} | " + " | ".join(str(a['chat_counts'].get(k,0)) for k in ORDER) + " |")
L.append(f"\n**{total} capabilities:** {counts.get('built',0)} built, {counts.get('partial',0)} partial, {counts.get('not built',0)} not built.\n")

L.append("## Seed hypotheses, checked against code\n")
for h in HYPOTHESES:
    L.append(f"**{h['hypothesis']}.** {h['finding']} Cells: {', '.join('`'+c+'`' for c in h['cells'])}.\n")

for app in APPS:
    L.append(f"## {app['app']} (`{app['repo']}`)\n")
    L.append(f"**App filter:** {app['rule']} *Source: {app['rule_source']}.*\n")
    for m in app["modules"]:
        L.append(f"### {m['module']}\n")
        L.append("| Capability | Status | Chat | Evidence | Note |\n|---|---|---|---|---|")
        for c in m["capabilities"]:
            ev = "<br>".join(f"`{e['path']}` ({e['shows']})" for e in c["evidence"]) or "none (absence finding)"
            note = c.get("note", "")
            if c.get("location"):
                note = (f"Lives in: {c['location']}. " + note).strip()
            st = {"built": "built", "partial": "**partial**", "not built": "*not built*"}[c["status"]]
            cv = c.get("chat", {})
            chat = cv.get("access", "")
            if cv.get("tools"): chat += "<br><sub>" + ", ".join(cv["tools"][:3]) + ("..." if len(cv["tools"]) > 3 else "") + "</sub>"
            L.append(f"| {c['capability']} <sub>`{c['id']}`</sub> | {st} | {chat} | {ev} | {note} |")
        L.append("")

L.append("## Notes for review\n")
L.append("- \"Not built\" rows with no evidence path are absence findings: a search of the repo found nothing. They cannot carry a file path by nature.")
L.append("- Retired in readvise, not counted above: advisor chat engine and AI Ask (REBUILD_PLAN.md Phase 1b), weekly cross-lane synthesis cron, Advise CapEx UI, mobile web view (frozen).")
L.append("- Some gaps map to Claude skills that live outside these repos (forvex-postmortem, forvex-change-order). Those are skills, not app capabilities, so they do not change the status here.")
L.append("- Paul (2026-10-06): Readvise is the primary focus; mobile apps are extensions. redeal-mobile is superseded by forvex-underwrite (Deal) and is not mapped. readvise-mobile is not mapped in this pass.")
L.append("- Paul (2026-10-06): the MCP layer stays in the map. It is the link between apps and the stand-in for what chat can do, so chat read / write coverage is tracked as its own lens.")
L.append("- Phase 0 gate: status calls approved by Paul on 2026-10-06.")
with open(os.path.join(OUT, "capability-map.md"), "w") as f:
    f.write("\n".join(L) + "\n")
print("ok", counts, "total", total)
