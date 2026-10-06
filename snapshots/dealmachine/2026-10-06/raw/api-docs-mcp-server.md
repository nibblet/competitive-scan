> Agent-readable docs index: /llms.txt. Full docs in one file: /llms-full.txt. Download /docs.zip to grep all markdown files locally.

---
title: MCP Server
description: 'Connect AI agents to DealMachine with the remote Model Context Protocol server'
---

# MCP Server

DealMachine runs a remote MCP server at:

```text
https://mcp.dealmachine.com
```

Use it when an AI agent needs live property intelligence, owner contact data, comps, property and people search, exports, account usage, or location lookup.

## Authentication

MCP clients authenticate with a DealMachine API key in the `Authorization` header:

```text
Authorization: Bearer dm_sk_live_xxx
```

Get an API key from [Developer Settings](https://dealmachine.com/settings/developer). OAuth-aware MCP clients can also discover authorization metadata from:

```text
https://mcp.dealmachine.com/.well-known/oauth-protected-resource
```

## Connect Claude Code

```bash
claude mcp add dealmachine --transport http https://mcp.dealmachine.com \
  --header "Authorization: Bearer dm_sk_live_xxxxxxxxxxxxxxxxxxxxxxxx"
```

## Connect Claude Desktop

Add this to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dealmachine": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.dealmachine.com",
        "--header",
        "Authorization: Bearer dm_sk_live_xxxxxxxxxxxxxxxxxxxxxxxx"
      ]
    }
  }
}
```

## Connect Cursor

Add this to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "dealmachine": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.dealmachine.com",
        "--header",
        "Authorization: Bearer dm_sk_live_xxxxxxxxxxxxxxxxxxxxxxxx"
      ]
    }
  }
}
```

## Direct HTTP Check

```bash
curl -X POST https://mcp.dealmachine.com \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dm_sk_live_YOUR_API_KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}'
```

## MCP Tools

DealMachine currently exposes 37 MCP Tools.

<Warning>
  Use `dealmachine_enrich_name` for a specific person by name. Use `dealmachine_people_search` only
  for audiences defined by filters and locations. The people search MCP Tool does not accept a
  person's name as a filter.
</Warning>

### Enrichment

| MCP Tool                     | Description                                          | Cost                                                                               |
| ---------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `dealmachine_enrich_address` | Look up a property by street address.                | 1 property data credit per match                                                   |
| `dealmachine_enrich_latlng`  | Look up the closest property by GPS coordinates.     | 1 property data credit per match                                                   |
| `dealmachine_enrich_apn`     | Look up a property by Assessor's Parcel Number.      | 1 property data credit per match                                                   |
| `dealmachine_enrich_email`   | Look up a person by email address.                   | 1 people data credit per matched person                                            |
| `dealmachine_enrich_phone`   | Look up a person by phone number.                    | 1 people data credit per matched person                                            |
| `dealmachine_enrich_name`    | Look up people by name. Always narrow with location. | Free with `estimate_cost=true`. Otherwise 1 people data credit per person returned |

### Search, Export, Comps, And Locations

| MCP Tool                        | Description                                                       | Cost                                               |
| ------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------- |
| `dealmachine_property_search`   | Search properties by location and filters.                        | Credit-consuming unless `estimate_cost=true`       |
| `dealmachine_property_count`    | Count matching properties before a search or export.              | Free                                               |
| `dealmachine_property_export`   | Export matching property-owner contacts as CSV.                   | Credit-consuming export                            |
| `dealmachine_property_get`      | Fetch one property by ID.                                         | 1 property data credit unless `enrich=false`       |
| `dealmachine_property_get_many` | Fetch up to 25 properties by ID.                                  | 1 property data credit per property unless deduped |
| `dealmachine_comps`             | Find comparable sales and active listings for subject properties. | 1 property data credit per subject found           |
| `dealmachine_people_search`     | Search people by location and filters.                            | Credit-consuming unless `estimate_cost=true`       |
| `dealmachine_people_count`      | Count matching people before a search or export.                  | Free                                               |
| `dealmachine_people_get`        | Fetch one person by ID.                                           | Credit-consuming unless deduped                    |
| `dealmachine_people_get_many`   | Fetch up to 25 people by ID.                                      | Credit-consuming unless deduped                    |
| `dealmachine_location_search`   | Look up FIPS codes, ZIP codes, and location IDs by name.          | Free                                               |

### Lists and prospects

| MCP Tool                        | Description                                                                                                                        | Cost |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---- |
| `dealmachine_list_create`       | Create a list, optionally pre-filled with up to 250 record IDs. Filed records become prospects unless `add_as_prospects` is false. | Free |
| `dealmachine_list_add_items`    | Add up to 10,000 property or person IDs to a list.                                                                                 | Free |
| `dealmachine_prospect_add`      | Track up to 1,000 records as prospects.                                                                                            | Free |
| `dealmachine_prospect_get`      | One prospect by ID or by the record it tracks.                                                                                     | Free |
| `dealmachine_prospect_search`   | List prospects by lifecycle, source, list, tag, or search words.                                                                   | Free |
| `dealmachine_prospect_update`   | Move a prospect between active, opportunity, and archived, or star it.                                                             | Free |
| `dealmachine_prospect_note_add` | Add a note to a prospect.                                                                                                          | Free |
| `dealmachine_prospect_tags_set` | Replace the tags on a prospect.                                                                                                    | Free |
| `dealmachine_tags_list`         | The prospect tag catalog with usage counts.                                                                                        | Free |
| `dealmachine_webhook_list`      | Outbound webhooks with delivery health, optionally the event catalog.                                                              | Free |
| `dealmachine_webhook_create`    | Register an https URL that receives prospect and list events.                                                                      | Free |

### Driving

| MCP Tool                   | Description                                                                                 | Cost |
| -------------------------- | ------------------------------------------------------------------------------------------- | ---- |
| `dealmachine_driving_read` | List recorded drives or get one drive with its route, visits, events, and linked Prospects. | Free |

Driving uses one compact read-only MCP Tool with `list_drives` and `get_drive` operations. Use the
Prospect MCP Tools for lifecycle, notes, and tags. Filter `dealmachine_prospect_search` with
`source=driving` to find Prospects added during drives.

### Mail

| MCP Tool                           | Description                                                                                 | Cost                                         |
| ---------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `dealmachine_mail_read`            | Read campaigns, recipients, analytics, cost estimates, designs, pricing, or wallet balance. | Free                                         |
| `dealmachine_mail_campaign_draft`  | Create or update a draft, or pause or resume a campaign.                                    | Free                                         |
| `dealmachine_mail_campaign_send`   | Launch a draft campaign.                                                                    | Wallet dollars based on recipients and steps |
| `dealmachine_mail_campaign_cancel` | Cancel a campaign and stop future sends.                                                    | Free                                         |

Read a campaign's cost estimate and get the user's approval before sending. Sending and cancelling
require `confirmed: true`.

### Discovery And Account

| MCP Tool              | Description                                                       | Cost |
| --------------------- | ----------------------------------------------------------------- | ---- |
| `dealmachine_filters` | List available search filters with types, operators, and options. | Free |
| `dealmachine_fields`  | List available result fields.                                     | Free |
| `dealmachine_usage`   | Get credit usage for the current billing cycle.                   | Free |
| `dealmachine_whoami`  | Check the authenticated account and organization.                 | Free |

Address autocomplete is intentionally not exposed as an MCP Tool. Use
`dealmachine_location_search` to normalize a city, county, state, or ZIP, and use
`dealmachine_enrich_address` for a property address.

### Parameters Added Across MCP Tools

| MCP Tools                                                  | Parameters and output                                                            |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `dealmachine_property_get`                                 | Accepts `fields` and `contact_audience`, including `none` for property-only data |
| Property enrichment tools                                  | Accept `fields` and `contact_audience`, including `none`                         |
| Email, phone, and name enrichment                          | Accept `fields` and return free `property_count` metadata                        |
| `dealmachine_people_get` and `dealmachine_people_get_many` | Accept `fields` and `property_limit`, default 20 and max 100                     |

Phone output types use `wireless`, `landline`, `voip`, or `unknown`.
`dealmachine_enrich_name` estimates include associated property totals and page-aware property
credits when both `estimate_cost=true` and `include_properties=true` are passed.

## Credit-Safe Agent Defaults

* Call `dealmachine_filters` and `dealmachine_fields` before constructing searches.
* Call `dealmachine_property_count` or `dealmachine_people_count` before any large search or export.
* Call `dealmachine_usage` before batch work.
* Use `contact_audience: "none"` for property lookup or enrichment when contacts are not needed.
* Confirm with the user before exporting or returning a large credit-consuming result set.
* Default property exports to owner contact rows unless the user explicitly asks for property-only rows.
