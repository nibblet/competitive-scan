# competitive-scan

Internal idea engine for Paul (CRG / CRG Holdings). It watches the real estate investor software market and maps what ships against the capabilities in Readvise, REbuild and Deal. The test for every idea is "does this make CRG run better", not "match the market". Paul makes every roadmap call; the scan only proposes.

| Path | What |
|---|---|
| `capability-map.md` / `.json` | App > Module > Capability, status, file-path evidence, chat (MCP) access. Phase 0, approved 2026-10-06. |
| `mcp-coverage.json` | Which capabilities chat can read / write through the forVEX MCP. |
| `watchlist.json` | Watched products and vendors, plus Paul's standing guidance. |
| `snapshots/<product>/<date>/` | `snapshot.json` + raw pages. 2026-10-06 is the baseline. |
| `discovery/` | Monthly candidate lists. |
| `briefs/` | Weekly briefs. |
| `ideas.json` | Every idea card, with Paul's decision. |
| `reviews/` | One-off design reviews. |
| `ROUTINE.md` | What the Monday run does. |
| `tools/build_capability_map.py` | Regenerates the capability map. |

App repos are read-only to this scan. Nothing here is written into them.
