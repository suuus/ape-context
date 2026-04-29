---
name: context-drift
description: Re-scan the project and compare against current MCP config to detect drift
user-invocable: true
---

Re-scan the project and compare against the current `.mcp.json` and `copilot-instructions.md` to detect configuration drift.

## What to check

### 1. Stack drift
Run the same detection as Phase 1 (Detect):
- Scan package files, CI/CD, infrastructure, cloud indicators
- Compare detected tools against what's configured in `.mcp.json`
- Flag **new tools** not covered by any MCP server: "You added Terraform since last setup — want to add an MCP server for it?"
- Flag **removed tools** still configured: "The Datadog config is still in `.mcp.json` but no Datadog references were found in the project"

### 2. MCP server health
For each server in `.mcp.json`:
- Attempt a lightweight read-only tool call
- Report: `✅ connected` / `⚠️ auth expired` / `❌ unreachable`

### 3. Instruction staleness
- Compare the tools referenced in `copilot-instructions.md` against `.mcp.json`
- Flag instructions that reference servers no longer configured
- Flag configured servers not mentioned in instructions

### 4. Dependency updates
- Check if any configured MCP server packages have newer versions available
- Report: "atlassian-mcp-server: using @latest (current), github-mcp-server: using @latest (current)"

## Report format

```
🔍 Drift Report
═══════════════

Stack changes detected:
  ➕ Terraform files found — no MCP server configured
  ➕ Redis references found — no MCP server configured
  ➖ Datadog configured but no references in project

Server health:
  ✅ github-mcp-server — connected
  ✅ atlassian-jira — connected
  ⚠️ workiq — auth token expired

Instruction drift:
  ⚠️ copilot-instructions.md references "datadog-mcp-server" — not in .mcp.json

No action needed: 2 servers | Action recommended: 3 items
```

## Actions

After presenting the report, offer to fix each issue:
- For new tools: run the relevant wizard phases (Discover → Install → Configure)
- For removed tools: remove the entry from `.mcp.json` and update instructions
- For auth issues: re-run Configure for that server
- For instruction drift: re-run the Instructions phase

Use `ask_user` for each recommended action — never auto-fix without confirmation.
```