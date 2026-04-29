---
name: context-instructions
description: Generate Copilot instructions with enterprise context, tool references, and cross-tool workflows
user-invocable: true
---

Generate or update `.github/copilot-instructions.md` with enterprise context based on everything configured so far.

## Important: Include ALL configured MCP servers

List every MCP server from .mcp.json — both newly installed and pre-existing ones. For each, document:
- What services it covers
- Key tools and when to use them
- Example: workiq covers M365 — "When user asks about emails, meetings, SharePoint docs, or Teams messages, use the workiq MCP server's ask_work_iq tool"

## What to generate

Add an `## Enterprise Context` section (or update it if it exists) with:

### Per-tool blocks
For each configured MCP server/tool:
- MCP server name
- Key tools it provides (list the actual tool names agents should use)
- When to use this tool vs. alternatives
- Team conventions (project keys, space names, URLs)
- Prefer MCP tools over CLI equivalents when available

### Skills and agents
Reference any relevant skills or agents:
- "Use the `azure-deploy` skill for deployments"
- "The `context-wizard` agent can reconfigure this setup"

### Cross-tool workflows
Based on the tools configured, describe common workflows:
- Bug triage: issue tracker → monitoring → fix → PR
- Deployment: PR merge → CI/CD → cloud deploy → monitoring verify
- Security: scanning tool → issue tracker ticket → fix → rescan
- Documentation: code change → update docs → review

### Documentation sources
Reference the locations identified in Phase 3:
- "Engineering docs are in Confluence space ENG"
- "Security policies are in the compliance repo"
- "When asked about 'how we do X', search Confluence first"

## Important
- Read the existing file first — preserve non-enterprise sections
- Use the edit tool to add/update the Enterprise Context section
- Keep instructions actionable — tell Copilot WHEN to use each tool
- Reference actual tool names that Copilot can invoke

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-instructions';
```
