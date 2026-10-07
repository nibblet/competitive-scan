# Tasks and checklists in an agent-run operation

2026-10-07. This replaces the amendment-focused framing of `checklists-tasks-documents-2026-10-06.md`, after Paul's correction: amendments are rare. The real issue is how tasks and checklists get created and completed, when most of the work is done by agents, started from Grok bot conversations and from contracts arriving by email or scan.

**Method:** read-only.
- **Code:** `readvise` (RA) and `recontrol` (RC). Nothing was changed.
- **Live data:** `readvise_list_tasks` (all 153 tasks), `readvise_list_agent_actions` (since 2026-09-01) and `readvise_get_daily_review` (7-day window, 30-day deadlines), called through forVEX. The review agent also ran read-only SELECTs on the Supabase project for the counts marked (DB).

**Claims checked again for this write-up:**
- `readvise_create_task` has no date input (RC `lib/mcp/tools/readvise/createTask.ts`, lines 22 to 40).
- Staged `spawn_task` writes `source: 'staged_action'` (RA `pages/api/operate/staged-actions/[actionId].ts` line 177).
- Pulse approval writes `source: 'reflect'` (RA `pages/api/pulses/approve-action.ts` line 49).
- The daily review counts only `pending` / `active` as open (RC `lib/mcp/readvise/dailyReview.ts` line 28).

## The short version

Agents are already doing real work. Since 9/21 there have been 19 evidence-backed completions, for example "Buyer accepted seller repair response (DigiSign)" closing two contract deadlines on Blanca. But the plumbing around them leaks in five places:

1. **Agents cannot date a task.** The create tool has no date input. All 37 open agent tasks have no due date, and the date is written into the label ("Fleming: trash-out Thu 10/8, confirm done", "Oct 16: 6711 John Hancock pre-trip listing check"). The daily review only shows dated tasks due today or overdue, so these never reach your morning brief.
2. **Dated deadlines still don't reach the brief.** "Close the sale of 1805 Blanca Ct, due 2026-11-06" is open and dated. Yet the 30-day deadline view returned **0 deadlines**, because it reads only the two hand-typed key-date fields on the property, not tasks. Scan deadlines that arrive as *suggested* are excluded from the review entirely.
3. **The suggestion pile never drains.**
   - 59 of 153 tasks are *suggested*.
   - 41 of those are older than 30 days, including 15 from the retired advisor engine, 272 to 355 days old.
   - 20 are "Check title on ..." competitor openings, 35 days old.
   - 6 are accountability commitments, 99 days old.
   - Agents now run a "Monday cleanup" that closes duplicates *by completing them*, which is not the same as dismissing them.
4. **Agents can create tasks but cannot fix them.** No tool exists to accept, re-date, reassign or dismiss a task. So "refresh a task" creates a new one, and a stale suggestion can only be marked done or left behind.
5. **Two task paths fail silently.**
   - A staged `spawn_task` writes a `source` value the database rejects: 7 live failures, each still marked "executed" (DB).
   - Approving a pulse action item does the same: it flags the item approved, then the insert fails.

**Checklists are a separate world:**
- 1,500 open items across 57 properties, none dated (DB).
- No agent tool reads or writes them.
- An agent's property note can auto-complete them (35 so far) with no evidence link and no undo (DB).
- They never sync with tasks.

**The fix is not a new module.** It is one task lifecycle that agents and you share, with three missing verbs:
- **date it:** a due date on create
- **fix it:** accept, re-date, dismiss
- **find it:** a dedup key, so "create" on an existing item updates it instead of adding a copy

Plus one morning list: what's waiting on you, and what the agents did.

## 1. How tasks get created today

Tasks have `property_id`, `tags`, `target_date`, `source` and `status`. There is no deal link, no document link, no checklist link, no dedup key, and no record of *which agent* made the task: `created_by` is always you.

| Path | Triggered by | Lands as | Dedup | Problem |
|---|---|---|---|---|
| `readvise_create_task` (RC `lib/mcp/readvise/createTask.ts`) | pm-lane, readvise-capture skill, Claude chat | open, or suggested (propose, or MANUAL autonomy) | none | No date, source always `ai`, even when you asked for it. CONTRACTS.md says it accepts `target_date`, `source` and `tags`; the wire schema doesn't |
| Accountability debrief (RC `lib/mcp/readvise/createAccountabilityDebrief.ts`) | CoS / weekly accountability | suggested | first insert of the week only | No property; never expires |
| Scan to obligations (RC `lib/mcp/memory/projectScans.ts`, `obligations.ts`) | Phone scan, 15-minute cron | suggested | marker per document and kind | Dated, but excluded from the daily review. A dismissed deadline comes back when the extractor version changes |
| `forvex_materialize_obligations` from chat | Claude chat | open | same marker | |
| Email (RA `pages/api/inbound/email.ts`) | You forward an email | a pulse entry only | | Attachments never extracted: an emailed contract makes no document and no deadlines |
| Deal-at-risk and decision-revisit crons (RA `lib/cron-tasks/`) | Weekly | suggested | one per insight | 362 generated, all later archived by the insight sweep (DB): churn, not work |
| Competitor openings cron (RA `lib/cron-tasks/competitor-openings.ts`) | Daily | suggested, source stored as `manual` | per listing | 20 "Check title on ..." waiting 35 days, no property |
| Intelligence weekly cron (RA `lib/cron-tasks/intelligence-weekly.ts`) | Weekly | suggested | per digest | Inserts a null owner into a required column; likely fails |
| Staged action `spawn_task` (RA `pages/api/operate/staged-actions/[actionId].ts`) | Checklist rule, then your click | intended open | none | Writes `source='staged_action'`, which the database rejects; marked executed anyway |
| Pulse action approve (RA `pages/api/pulses/approve-action.ts`) | Your approval | intended suggested | none | Writes `source='reflect'`, which is rejected |
| UI (RA `pages/api/tasks/index.ts`, `pages/api/operate/tasks/index.ts`) | You | pending | none | Two create routes with different defaults |

**What the Grok lane skills do** (RC `skills/skills/*/SKILL.md`):
- Only pm-lane and readvise-capture create tasks.
- CoS hands work out as `work_dispatched` ledger events, with ask / done_when / priority. That is a second task system. CoS cannot read tasks: `readvise_list_tasks` is not on its allowlist.
- CFO, CMO, Net, Ops and Platform only log events and memories.
- No skill uses the completion, agent-actions or undo tools that shipped in MCP 0.14 to 0.18. The completions in your log came from Claude chat, not the Grok lanes.

## 2. How tasks get completed today

- **You, in the UI.** One route sets `completed_at`, another sets status only. "Dismiss" is a soft delete.
- **Agents, via `readvise_complete_task`** (RC `lib/mcp/readvise/completeTask.ts`). This is the good part:
  - It requires an outside evidence link, so the agent cannot cite itself.
  - It refuses under MANUAL autonomy.
  - It writes an auditable row, and the action can be undone.

  Your 19 live completions cite Drive files, Gmail threads, property notes and your accountability answers. **Gap:** it will also complete a *suggested* task you never accepted. The Monday duplicate cleanup used exactly that.
- **Checklist items** complete by a different route. A property note at 0.8 confidence or higher auto-completes matching items (RA `lib/checklist/note-evidence-apply.ts`, RC `lib/mcp/readvise/noteEvidence.ts`), with no evidence link and no undo. That is the loophole the task gate closed, still open on checklists.
- **Autonomy:** all 38 live workflows are ASSISTED, and AUTO currently behaves the same as ASSISTED (DB).

## 3. What checklists are actually for

- They are stage templates: Purchase, Financing, Selling, Pending, Post Sale, Rental Purchase (RA `lib/operate/workflow/stage-templates.ts`).
- They are created when a property is added, when its Workflow tab is opened, or when its stage changes (RA `lib/operate/workflow/ensure-populated.ts`).
- They are useful as **"what does this stage require" and a progress view**.
- They fail as a worklist: undated, ownerless, invisible to agents. With 1,500 open items, nobody is working them as a list.

## 4. Proposed model: one task lifecycle for agents and you

**States** (four, mapped from today's values):

```
proposed ──> open ──> done
    └──────────┴────> dismissed
```

- `suggested` becomes **proposed**.
- `pending` / `active` become **open**.
- **dismissed** is new; it replaces soft-delete.

**Every task carries:**
- property, or an explicit "workspace" scope (no silent orphans)
- **due date, or an explicit "no date"**
- **who made it:** an `actor_lane` (cos, pm, cfo, cmo, net, platform, chat, scan, email, cron, human). This uses the lane identity you already have, instead of the shelved per-agent identity plan.
- a **dedup key** (for example `obl:<doc>:<kind>`, `insight:<id>`, `lease:<prop>:<unit>`, `commit:<week>:<hash>`). Creating with an existing key returns and updates the existing task instead of adding a copy.
- a **source link:** the scan, email, conversation event or debrief that caused it
- optionally, the checklist item it fulfils
- on completion: evidence link (required for agents), who completed it, and when

**Who may do what** (your answers to section 6 set the defaults):

| Transition | Who |
|---|---|
| create as **proposed** | Any agent, always |
| create as **open** | When you asked for it in chat; deadlines from a contract you filed; lanes you allowlist |
| proposed to open / dismissed | You, or CoS acting on your stated decision (logged like the daily-review decisions are) |
| open to **done** | You always. An agent only with outside evidence, never from proposed, never under MANUAL |
| re-date | An agent on tasks it created; anything else is proposed to you |
| proposed expires | After 14 days, except contract deadlines, which escalate as the date approaches |

**Checklists become templates plus a stage view.**
- An item becomes a task only when it gets a date or an owner. The task is then linked, and closing either one closes both.
- Note-based auto-completion uses the same evidence rule as tasks.

**Contracts in:**
- **Scan:** unchanged, but dismissed deadlines stay dismissed.
- **Email:** attachments go through the same path as a scan (register the document, extract, create deadlines). The retired knowledge table write goes away.
- **Amendments** (footnote): a later version re-dates the existing task with a note, never a duplicate.

**Two views, one source.** Both live in the CoS brief and in Readvise:
- **Waiting on you:** proposed tasks (contract deadlines first, by date), open tasks due in 7 days, alerts.
- **What agents did:** every task created, completed, re-dated or dismissed by an agent, plus checklist auto-completions, notes and stage moves. 45 of last week's 63 stage moves were by agents.

**Merges and removals:**
- Pulse action items become proposed tasks (fixes the broken approve).
- Staged `spawn_task` becomes a proposed task directly (fixes the rejected insert).
- CoS `work_dispatched` keeps its ledger event and also creates or links a task for the assignee lane.
- Lane events stay as the ledger, not a to-do list. Advisor actions stay notes. Insights stay alerts.
- Remove: the uncalled `/api/tasks/suggest` route and AI-op route, the broken intelligence-weekly task emit, and the separate "active" state.

## 5. Migration (each step ships alone, smallest first)

| Step | What | Files | MCP contract |
|---|---|---|---|
| 1 | **Agents can date tasks; fix the broken writers.** Add `target_date`, `source`, `tags` inputs to `readvise_create_task` (matches what CONTRACTS.md already promises). Update pm-lane and readvise-capture skills to pass dates. Fix `staged_action` and `reflect` sources. Fix the intelligence-weekly owner | RC `lib/mcp/tools/readvise/createTask.ts`, `lib/mcp/readvise/createTask.ts`, `outputSchemas.ts`, contract test, `CONTRACTS.md`, `skills/skills/pm-lane/SKILL.md`; RA `pages/api/operate/staged-actions/[actionId].ts`, `pages/api/pulses/approve-action.ts`, `lib/cron-tasks/intelligence-weekly.ts` | Additive input |
| 2 | **Deadlines reach the brief.** The daily review uses the shared status list; adds "proposed with a date in 7 days", "open dated tasks in the deadline window" and "proposed older than 14 days". Obligation dedup counts dismissed rows | RC `lib/mcp/readvise/dailyReview.ts`, `lib/mcp/memory/obligations.ts` | Additive output |
| 3 | **Agents can fix tasks; no more copies.** New `readvise_update_task` (accept, dismiss, re-date, reassign; not complete). Add `dedup_key` and `actor_lane` columns. Create returns the existing row on a key hit. `readvise_complete_task` refuses proposed tasks. CoS gets list / accept / dismiss on your word. One-time sweep of the 41 stale suggestions | RA new migration; RC new tool, `completeTask.ts`, `skills/skills/cos-lane/SKILL.md` | New tool, additive |
| 4 | **Checklists and tasks link; close the note loophole.** `checklist_item_id` on tasks, two-way completion sync. Notes by agents only *propose* checklist completion. "What agents did" covers task creates, checklist auto-completes and dismissals | RA migration + `lib/checklist/note-evidence-apply.ts`; RC `lib/mcp/readvise/noteEvidence.ts`, `listAgentActions.ts` | Additive enum on agent actions |
| 5 | **Email contracts become documents and deadlines; status names settle.** Attachment extraction to the scan path. `proposed` / `dismissed` through the canonical enum in reecosystem-core and both `taskStatus.ts` mirrors | RA `pages/api/inbound/email.ts`; RC register path; reecosystem-core | Coordinated enum change |

**Step 1 is small and fixes the biggest leak.** Every task your agents create from today on would carry a date the brief can see.

## 6. Questions for Paul

1. **Open vs propose:** which agents may create *open* tasks without your approval, and which only propose? For example, COO / pm for rehab and lease items, CoS for commitments you state.
2. **Completion and evidence:** which agents may mark a task done without approval? Is a Drive file, Gmail thread or scanned document enough evidence, or do money items need your review?
3. **Scan deadlines:** should contract deadlines from a phone scan land as open work immediately, or wait for your glance as now?
4. **Expiry:** how long should an unaccepted suggestion live (7 days, 14, never for deadlines)? And may I propose a one-time sweep of the 41 stale ones: the 15 advisor tasks from the retired engine, 20 title checks and 6 old commitments?
5. **CoS hand-offs:** when CoS hands work to another bot, should it also appear as a task in Readvise, or is the ledger event enough?
6. **Checklists day to day:** do you use the stage checklists, or would a per-stage "what's missing" view built from tasks do?
7. **Morning list:** do you want "waiting on me" plus "what agents did" in Readvise, the CoS brief, or both?
8. **Email:** should a contract you forward by email take exactly the same path as a scan?
