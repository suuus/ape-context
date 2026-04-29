---
name: context-discover
description: Find the best MCP servers for each tool in the user's stack using existing config, GitHub catalog, org catalog, and vendor docs
user-invocable: true
---

Based on the detected stack, find the best MCP servers for each tool category.

## FIRST: Check already-installed MCP servers

Before searching for anything, check what's already in .mcp.json. Many tools are already covered:

**Known MCP server coverage:**
- `github-mcp-server` → GitHub (issues, PRs, code search, actions, repos) — read + write
- `workiq` → Microsoft 365 (SharePoint, Outlook, OneDrive, Teams, Calendar) — **read-only** (search, query, retrieve). If write access is needed (create pages, send emails, update items), suggest an additional M365/Graph MCP server
- `playwright` → Browser automation, testing, screenshots — read + write
- `atlassian-mcp-server` → Jira, Confluence — read + write
- `datadog-mcp-server` → Monitoring, logs, metrics — read-only
- `azure-mcp-server` → Azure resources, deployments — read + write

When an existing server covers a category in read-only mode, ask the user: "workiq already lets you search SharePoint docs. Do you also need to create/edit content there?" If yes, search for a write-capable MCP server too.

## Discovery Chain (for tools NOT already covered)

### 1. GitHub / Official MCP Catalog
- Search GitHub: `topic:mcp-server` + the vendor/tool name
- Check github.com/modelcontextprotocol/servers for official listings
- These get the 🐙 badge

### 2. Organization Catalog
- Try to read `{org}/.github/mcp-catalog.json` using `get_file_contents`
- If it exists, prefer org-approved servers and respect the blocked list
- These get the 🏢 badge

If no org catalog exists, inform the user:
> "No org-level MCP catalog was found at `{org}/.github/mcp-catalog.json`. An org catalog lets your security team maintain approved/blocked server lists and credential storage policies that apply across all repos. Consider creating one as your MCP adoption grows."

Do not scaffold or create the catalog — just make the recommendation and move on.

### 3. Vendor Documentation
- Use `web_search` to find: "{tool name} MCP server official"
- Use `web_fetch` to read install instructions from vendor docs
- These get the 🔰 badge

### 4. Community
- Other GitHub results
- These get the 👥 badge

## Tool Scoping

When presenting each recommended MCP server, ask the user whether they need **read-only** or **read+write** access. This determines the `tools` list in `.mcp.json`:

- **Read+write** (default): `"tools": ["*"]`
- **Read-only**: scope to get/search/list tools only

Use `ask_user` for each server:
```
"Do you need write access to {tool} (create/update/delete), or is read-only enough?"
→ Choices: ["Read + Write (Recommended)", "Read-only"]
```

Pass the scoping decision forward to Phase 5 (Install) so it can set the appropriate `tools` list.

## Categories to cover

For each category, use `ask_user` with **multi-select** (checkboxes, not radio buttons) so users can pick multiple tools. Always include an "Other (specify)" freeform option.

Example schema for ask_user:
```json
{
  "properties": {
    "tools": {
      "type": "array",
      "title": "Which monitoring tools does your team use?",
      "items": { "type": "string", "enum": ["Datadog", "Grafana", "App Insights", "PagerDuty", "None"] }
    },
    "other": {
      "type": "string",
      "title": "Other (specify)",
      "description": "Any tools not listed above"
    }
  }
}
```

Categories:
- Source control
- Project management (Jira, Linear, GitHub Issues, Azure Boards)
- CI/CD
- Cloud platform
- Monitoring / observability
- Documentation / wiki (SharePoint → workiq, Confluence → atlassian-mcp-server)
- Security scanning
- Communication (Teams → workiq, Slack → slack-mcp-server)

**Important**: When the user selects a service like SharePoint, Teams, Outlook, OneDrive — check if `workiq` is already installed. If so, it already covers that service. Same logic for all multi-service MCP servers.

For each confirmed tool, present the best match with its trust badge and whether it's already installed.

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-discover';
```
