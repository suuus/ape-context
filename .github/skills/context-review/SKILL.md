---
name: context-review
description: Present the full setup plan for user confirmation before making changes
user-invocable: true
---

Present a complete summary of everything that will be configured. The user must confirm before you proceed.

## What to show

### MCP Servers to install
For each server, show:
- Name and trust badge (🏢 🐙 🔰 👥)
- What it covers (e.g., "Jira + Confluence")
- Key tools it provides
- Auth requirements (e.g., "needs API token")

### Skills to enable
List any skills that match the detected stack.

### Copilot instructions to generate
Preview the sections that will be added to `.github/copilot-instructions.md`:
- Enterprise context section
- Per-tool instructions
- Cross-tool workflows

### Configuration changes
- Entries to add to `.mcp.json`
- Files to create or modify

### Org policy compliance (if org catalog was found)
- All servers on the approved list? ✅
- Any blocked servers avoided? ✅
- Credential storage matches org policy?

## Confirmation

Use `ask_user` with a clear yes/no: "Ready to proceed with this setup?"

If the user wants changes, go back to the relevant phase.

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-review';
```
