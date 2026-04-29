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

### Team Intent & Constraints

Include the distilled output from Phase 8 (Distill). This is the **Intent layer** of ISEE — codified so every agent inherits it.

#### Intent statements
Express what the team values as clear directives:
- "This team prioritises reliability over feature velocity"
- "Security reviews are required for all external-facing changes"

#### Constraints
Hard rules that agents must always respect:
- "Production deployments require manual approval from a team lead"
- "All PRs must reference a Jira ticket"
- "Secrets must be stored in Azure Key Vault, never in environment variables"

#### Autonomy boundaries
What agents can and cannot do independently:
- "Agents can create PRs but not merge them"
- "Agents can query production logs but not modify infrastructure"

#### Team topology (if available)
Ownership and routing:
- "Team Alpha owns the payments service"
- "Security team must approve changes to auth modules"

### Cross-tool workflows
Based on the tools configured AND the processes discovered in Phase 3/8, describe common workflows:
- Bug triage: issue tracker → monitoring → fix → PR
- Deployment: PR merge → CI/CD → cloud deploy → monitoring verify
- Security: scanning tool → issue tracker ticket → fix → rescan
- Documentation: code change → update docs → review
- Add any team-specific workflows discovered during distillation (e.g., incident response, change advisory, release ceremonies)

### Documentation sources
Reference the locations identified in Phase 3, using the content tags:
- `[intent]` sources: "Team strategy and priorities are in SharePoint — search via workiq"
- `[constraint]` sources: "Security policies are in the compliance repo"
- `[process]` sources: "Deployment process is documented in Confluence space ENG"
- `[reference]` sources: "API specs are in the repo under docs/api/"
- "When asked about 'how we do X', search documentation sources tagged `[process]` first"

## Important
- Read the existing file first — preserve non-enterprise sections
- Use the edit tool to add/update the Enterprise Context section
- Keep instructions actionable — tell Copilot WHEN to use each tool
- Reference actual tool names that Copilot can invoke
- Intent statements and constraints should be written as directives, not descriptions — they tell agents what to do, not what the team thinks about

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-instructions';
```
