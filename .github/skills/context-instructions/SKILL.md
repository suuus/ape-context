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

Retrieve distilled intent from the session store:

```sql
SELECT value FROM session_state WHERE key = 'distilled_intent';
```

Fall back to conversation context if not available. If neither exists, skip this section and note: "No distilled intent available — run `/context-distill` to generate."

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

Render the classified autonomy boundaries from Phase 8 as a structured table:

> Before performing any action listed below, check its autonomy level. `PROCEED` actions can be taken without confirmation. `ALWAYS ASK` actions require explicit user approval via `ask_user`. `NEVER` actions must not be attempted.

| Action | Level | Notes |
|--------|-------|-------|
| Create pull requests | ✅ PROCEED | — |
| Merge pull requests | 🛑 ALWAYS ASK | Requires team lead approval |
| Create Jira tickets | ✅ PROCEED | Must reference PR |
| Close Jira tickets | 🛑 ALWAYS ASK | — |
| Query production logs | ✅ PROCEED | Read-only |
| Modify infrastructure | ⛔ NEVER | Platform team only |
| Deploy to production | 🛑 ALWAYS ASK | Requires manual approval |

The table above is an example — populate it with the actual classifications confirmed by the user in Phase 8 (Distill). Use the icons consistently:
- ✅ for `PROCEED`
- 🛑 for `ALWAYS ASK`
- ⛔ for `NEVER`

#### Team topology (if available)
Ownership and routing:
- "Team Alpha owns the payments service"
- "Security team must approve changes to auth modules"

#### Intent changelog reference
After writing the intent and constraints sections, add a footer linking to the changelog:

```markdown
> Intent changelog: [.github/intent-changelog.md](intent-changelog.md) | Last updated: {date}
```

This makes the changelog discoverable from the instructions file and provides an audit trail for when and why guardrails changed.

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

### Merge algorithm for existing files

When updating `copilot-instructions.md`:

1. **File doesn't exist** → create it with the full `## Enterprise Context` section
2. **File exists, no `## Enterprise Context` heading** → append the new section at the end of the file
3. **File exists with `## Enterprise Context`** → replace everything from `## Enterprise Context` up to (but not including) the next `## ` heading at the same level, or end of file if no next heading
4. **Preserve user content** — all sections outside `## Enterprise Context` are never modified. Custom instructions, notes, and other headings remain untouched
5. **Manual edit detection** — if the existing Enterprise Context section contains content that doesn't match wizard-generated patterns (e.g., hand-written tool descriptions, custom workflows), warn the user via `ask_user`: "The Enterprise Context section appears to have manual edits. Regenerating will replace them. Proceed?"

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-instructions';
```
