# Checklists, tasks and documents: review and proposed construct

2026-10-06. Read-only review of `readvise` (RA) and `recontrol` (RC). Nothing in either repo was changed. Paths are relative to each repo root.

**Origin:** Paul's comment on idea 1 (deadlines): "there may be a larger rethinking of the checklists, tasks, upload of docs. interconnecting or reworking to a better construct."

**Constraint:** keep project management light. No change orders, draws or portals.

**Claims checked again against code for this write-up:**
- an amendment scan is filed as a contract (RC `lib/mcp/memory/scanClass.ts` line 29, `amendment: 'contract'`)
- `responsible` is dropped by the materializer (no reference in RC `lib/mcp/memory/obligations.ts`)
- inbound email reads attachments only on the `intel+` path, and only forwarded messages (RA `pages/api/inbound/email.ts` lines 126 to 150)
- no committed DDL for `readvise_staged_actions`
- the ai-op route has no caller outside its own files and test

## The short version

**The problem.** "Something due on a deal" is modeled in six places with four status vocabularies, and there are five places to approve things. The result:
- **Contract dates stop short.** They reach at most a *suggested* task, which:
  - never appears in the daily review
  - never updates the key dates that risk scoring reads
  - does not move when an amendment changes the date
- **Email is a dead end for documents.** Your natural inbox can't file one: a forwarded PDF contract is dropped.

**The fix.** A light construct, one direction of flow:

```
Deal ──> Document ──> Deal Date ──> Task
                          ^
            Template ─────┘  (generates dated tasks: "order inspection = inspection expiry - 5 days")
```

Each step ships alone, smallest first. **Step 1 needs no schema change.**

## 1. Current state

| Object | Table | Written by | Shown in | Notes |
|---|---|---|---|---|
| Task | `readvise_tasks` | RA `pages/api/operate/tasks/index.ts`, `lib/cron-tasks/deal-at-risk.ts`; RC `lib/mcp/readvise/createTask.ts`, `lib/mcp/memory/obligations.ts` | RA `components/tasks/TaskDrawer.tsx` (with a "Suggested" section) | No metadata column. Where a task came from lives in `tags` (`obl:<doc>:<kind>`) and description text |
| Checklist template | `readvise_checklist_templates`, `_template_items` | RA `pages/operate/checklists/templates.tsx` | RA `lib/operate/checklists/materialize.ts` | Items carry no date logic |
| Checklist instance | `readvise_checklists`, `_items` | RA `lib/operate/checklists/materialize.ts`; RC `lib/mcp/readvise/noteEvidence.ts` | Workflow tab via RA `lib/operate/workflow/projection.ts` | Items have their own `due_date` and an OPEN / COMPLETED vocabulary |
| Staged action | `readvise_staged_actions` | RA `lib/checklist/trigger-evaluator.ts`; RC `noteEvidence.ts` | RA `components/operate/tabs/StagedActionsPanel.tsx` (Workflow tab only) | No DDL committed in either repo; exists only in generated types |
| Insight / alert | `readvise_insights` | RA `lib/cron-tasks/deal-at-risk.ts`, `lib/intelligence/competitorOverlap.ts` | RA `components/intelligence/IntelligenceDrawer.tsx` | RC daily review calls these "alerts" |
| Agent event | `core.lane_events` | `forvex_emit_event` | RC `app/(dashboard)/inbox/page.tsx` | Proposed / actioned; outside readvise |
| Notification | `readvise_notifications` | RA `lib/notifications/createNotification.ts` | RA `components/notifications/NotificationBell.tsx` | Assignments and watchlist only |
| Scan artifact | `core.deal_documents` | Phone scan (forVEX Scan) | RA `pages/api/operate/properties/[propertyId]/files.ts` (GET only), `FilesTab.tsx` | No upload in readvise |
| Corpus document | `core.documents` (+ chunks, links) | RC `lib/mcp/memory/registerDocument.ts`, `projectScans.ts` | RA `lib/operate/corpusDocuments.ts` (read only); `forvex_recall` | The one real registry |
| Obligation | no table: `extracted.obligations` JSON on the document | RC `lib/mcp/memory/extractScan.ts` | RC `obligations.ts` | Has `kind`, `date`, `source_clause`, `responsible` |
| Key dates | `readvise_properties.option_expires_at`, `.expected_close_date` | Typed by hand in RA `components/operate/tabs/DetailsTab.tsx`; no MCP path writes them | RA `lib/operate/dealRisk.ts`; RC `dailyReview.ts` | Feed risk scoring |
| Inbound email | `readvise_pulse_entries` (+ raw .eml) | RA `pages/api/inbound/email.ts` | Pulse | Attachments ignored on the pulse path |
| Lead match | `competitive_lead_matches` | RA `lib/intelligence/lead-match.ts` | Insight via competitorOverlap | Non-terminal deals only |

## 2. How it connects today

**(a) Contract scanned on the phone.**
1. Scan to `core.deal_documents`.
2. The 15-minute cron (RC `app/api/cron/scan-projection/route.ts`) runs `projectScans` and `extractScan`. The LLM returns obligations with clause and responsible party.
3. `registerDocument` files it, then `materializeObligations` creates **suggested** tasks.

Then it stops:
- The daily review (RC `lib/mcp/readvise/dailyReview.ts`) shows only OPEN tasks due today or overdue, so suggested deadlines are invisible there.
- Key dates are not updated, so `dealRisk` keeps scoring the hand-typed date.
- `responsible` is dropped, and the clause survives only as description text.

**(b) Checklist trigger.** A status change runs `evaluateTriggers` (RA `lib/checklist/trigger-evaluator.ts`). That either materializes the checklist (ASSISTED / AUTO) or stages a `spawn_checklist` action (MANUAL). Template items have no dates.

**(c) Approvals.** There are five separate "approve this" queues:
1. Suggested tasks (TaskDrawer)
2. Staged actions (Workflow tab only)
3. Insights (Intelligence drawer)
4. Lane events (recontrol /inbox, outside readvise)
5. Lead-match review

**(d) Inbound email.** `readvise+<token>@` becomes a pulse entry. Attachments are never filed: no readvise upload path exists at all.

**(e) Key dates.** Typed by hand. The weekly deal-at-risk cron writes an insight plus a suggested task.

**Six homes for "something due":**
- `readvise_tasks.target_date`
- `readvise_checklist_items.due_date`
- `readvise_staged_actions.execute_after`
- the two key-date columns
- `extracted.obligations`
- risk insights

**Four status vocabularies:**
- pending / done
- OPEN / COMPLETED
- staged / executed / dismissed / expired
- proposed / actioned

## 3. Problems, ranked for a small operator

1. **Dates don't flow.** A contract fact gets no deadline view, no re-dating and no key-date update. You retype dates, and risk scoring runs on stale numbers.
2. **Amendments make it worse.** The existing task is "left alone" by design (RC `obligations.ts` header). A separately scanned amendment is filed as a new *contract* with no link to the original (RC `scanClass.ts`). Its marker is keyed on the new document id, so it creates a **second** closing task while the old date stays live.
3. **Five places to approve things** (list in 2c).
4. **Chat can't act on what it creates.** There is no MCP tool to:
   - accept, re-date or dismiss a task (`readvise_complete_task` only marks done)
   - act on staged actions
   - change checklists or key dates

   Chat can file a document only as pasted text.
5. **Email files nothing.** The phone scan and chat-pasted text are the only document inputs.
6. **Lost provenance.** Clause, responsible party and source document live in free text, so the UI cannot show "from §7(b), Amendment 2".
7. **Duplicate to-do models.** Checklist items with `due_date` overlap tasks with `target_date`. One rule engine is mirrored by hand across repos (RA `lib/checklist/note-evidence-apply.ts`, RC `lib/mcp/readvise/noteEvidence.ts`).

**Dead or leftover code:**
- RA `pages/operate/my-work.tsx` (redirect) and `components/operate/MyWorkView.tsx`
- RA `pages/api/operate/workflow/ai-op.ts` with `lib/operate/workflow/apply-ai-op.ts` (no caller)
- RA `lib/client/filePreview.ts` and `pages/api/files/extract-text.ts`
- the inbound `readvise_knowledge_unified` insert (table being retired)

## 4. Proposed construct

Five objects. Each has one owner and one job.

**1. Document** = `core.documents`, the one registry, written by recontrol.
- `core.deal_documents` stays as the raw scan.
- Add an **`amends`** link between documents. An amendment changes some terms; it does not *supersede* the contract.
- Add doc class `receipt` and capture method `email`. Both are `reecosystem-core` enum changes (SKILL_SYSTEM_CONTRACT §3.7).

**2. Deal Date** (new `readvise_deal_dates`, readvise owns the migration).
- Columns:
  - `property_id`, `kind` (the extractor's slugs: closing, inspection_expiry, earnest_money, ...), `date`
  - `status` (proposed / confirmed), `responsible`
  - `source_document_id`, `source_clause`
  - `superseded_by`, so history is kept
- This is what you see, instead of obligations buried in JSON.
- `option_expires_at` and `expected_close_date` become projections of the confirmed dates. The columns stay, so `dealRisk` and the daily review keep working unchanged.

**3. Task** (`readvise_tasks`, the one work queue).
- Add `deal_date_id`, `offset_days`, `document_id`, `date_pinned`.
- `suggested` becomes the single approval state for anything that turns into work.
- Insights stay signals, and lane events stay a ledger. Neither is a work queue.

**4. Template** (checklist templates).
- Items gain `anchor_kind` and `offset_days`, so a template generates dated tasks bound to Deal Dates.
- Checklist items keep their phase role but stop owning dates.

**5. Watch** (already designed in RA `docs/plans/DEAL_RECORDS_WATCH_PLAN.md`): LOST deals enter the records watch.

**How your wants land:**
- **Amendment moves closing.**
  1. The amendment is extracted and linked to the contract (`amends`).
  2. The closing Deal Date gets a new row, with history, clause and document.
  3. Open tasks bound to that date that you haven't pinned move by their offset. Pinned or hand-edited tasks get a "date moved" suggestion instead.
  4. Under MANUAL autonomy the new date is `proposed` until you accept it.
  5. The view reads: "Closing 11/14 (was 10/31), Amendment 2 §3".
- **Forward an email with a contract attached.**
  1. A `docs+<token>@` address, next to `pulse` / `intel` (RA `lib/inboundEmail/utils.ts`), stores the attachments.
  2. recontrol extracts them through the same projection the phone scan uses.
  3. The property is matched from the email, using the existing analyzer's property identifiers.
  4. Same Deal Date path as above.
- **Receipts.** An email forward or a phone photo becomes a `receipt` document with a `receipt.v1` extraction (vendor, date, total, property). It rolls up per deal only; there is no PM ledger.
- **Lead fate.**
  - Extend lead-match to watched LOST deals.
  - Turn `follow_up_at` into a task.
  - Write the outcome to the deal timeline, per the existing plan.
- **Chat parity.** Each new object gets one read tool and one write tool in recontrol, with outputSchemas and a contract test. The daily review gains deadlines.

## 5. Migration path (each step ships alone)

| Step | What | Touches | MCP contract |
|---|---|---|---|
| 1 | **Deadline view + chat can act on tasks.** No schema change. A "Deadlines" scope in the task drawer unions open and suggested tasks with dates and the key-date columns. New `readvise_update_task` tool (accept, re-date, dismiss, pin). Daily review adds `suggested_deadlines` | RA `components/tasks/TaskDrawer.tsx`; RC `lib/mcp/tools/readvise/`, `lib/mcp/readvise/dailyReview.ts`, `outputSchemas.ts` | Additive |
| 2 | **Clean up.** Remove the dead pieces listed in section 3. Commit the missing DDL for staged actions and workflow tables | RA only | None |
| 3 | **Deal Dates + amendment re-dating.** New table and task columns (RLS in the same migration). Materializer writes the Deal Date first. Extractor emits `amends` (version bump). Key-date columns sync from confirmed dates | RA `supabase/migrations/`; RC `lib/mcp/memory/obligations.ts`, `extractScan.ts`, `registerDocument.ts`, `scanClass.ts` | Additive output keys on `forvex_materialize_obligations`; new `readvise_list_deal_dates`; note in RC `CONTRACTS.md` |
| 4 | **Email forward to Document.** `docs+` address, attachment staging, generalized projection cron, `email` capture method | RA `pages/api/inbound/email.ts`, `lib/inboundEmail/`; RC projection cron; reecosystem-core enum | No signature change; new enum value |
| 5 | **Converge and extend.** Staged `spawn_task` writes suggested tasks. Template items get anchors and offsets. `receipt` class and `receipt.v1` schema. Records watch for LOST deals | RA `pages/operate/checklists/templates.tsx`, `lib/operate/checklists/materialize.ts`; RC `lib/mcp/documents/schemas` | Additive |

**Step 1 is the cheapest real win.** You get one place to see deadlines, and chat gets the ability to accept, re-date and dismiss what it already suggests, without touching the data model.

## 6. Questions for Paul

1. When an amendment moves a date, should matching tasks move automatically on ASSISTED deals, or always ask first?
2. Should a date read from a document ever overwrite one you typed by hand, or always just propose the change?
3. Is one forwarding address per workspace enough (property matched from the email), or do you want per-deal addresses?
4. Your email receipt scanning is not in either repo. Where does it run today, and should receipts roll up per deal only or also feed CapEx (`property_capex_items`)?
5. Can checklist items lose their own due dates, so dates live only on tasks?
6. Should agent proposals in recontrol's /inbox show up in readvise, or stay admin-only?
7. Which LOST reasons enter the records watch? The plan suggests excluding WE_WALKED.
