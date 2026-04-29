---
name: context-distill
description: Analyze discovered documentation to extract team intent, constraints, and autonomy boundaries
user-invocable: true
---

Analyze the user's Copilot session history and the documentation sources discovered in Phase 3 (Docs) to extract actionable intent and constraints that flow into Phase 9 (Instructions).

This is the **Intent layer** of the ISEE framework — turning implicit organisational knowledge into explicit, machine-readable guardrails. It uses two complementary signals: what the team *documents* (docs) and what the team *actually does* (history).

## Process

### 0. Analyze session history

**Invoke skill:** `context-history`

Before reading any documentation, analyze the user's Copilot session history. This surfaces behavioural patterns — recurring tasks, file hotspots, cross-repo topology, workflow chains — that reveal implicit intent. History-based observations are presented to the user for confirmation before proceeding.

### 1. Gather tagged sources from Phase 3

Review the doc sources discovered earlier, grouped by content tag:
- `[intent]` — team priorities, values, strategy
- `[constraint]` — security policies, compliance rules, approval requirements
- `[process]` — ceremonies, workflows, decision flows, escalation paths
- `[reference]` — API specs, guides (lower priority for distillation)

### 2. Read and analyze documents

For each `[intent]`, `[constraint]`, and `[process]` source:
- Use the appropriate MCP server to read the content (e.g., `workiq` for SharePoint, `atlassian-jira` for Confluence, file tools for repo docs)
- Extract statements that express:
  - **What the team values** — priorities, quality bars, what "done" means
  - **What is not allowed** — security boundaries, compliance rules, forbidden patterns
  - **What requires approval** — deployment gates, merge policies, access escalation
  - **How work flows** — ceremonies, handoff points, escalation paths

### 3. Distill into structured output

Organise findings into four categories:

#### Intent statements
High-level expressions of what the team/org values:
- "This team prioritises reliability over feature velocity"
- "Security reviews are required for all external-facing changes"
- "We follow trunk-based development with short-lived feature branches"

#### Constraints
Explicit rules that agents must respect:
- "Production deployments require manual approval from a team lead"
- "All PRs must reference a Jira ticket"
- "Secrets must be stored in Azure Key Vault, never in environment variables"
- "Database migrations must be backward-compatible"

#### Autonomy boundaries
What agents can and cannot do independently:
- "Agents can create PRs but not merge them"
- "Agents can create Jira tickets but not close them"
- "Agents can query production logs but not modify infrastructure"

#### Team topology (if discoverable)
Who owns what — useful for routing and escalation:
- "Team Alpha owns the payments service"
- "Platform team owns CI/CD pipelines and infrastructure"
- "Security team must approve changes to auth modules"

### 4. Present for confirmation

Show the distilled findings to the user using `ask_user`:
- Present each category separately
- Ask: "Are these accurate? Anything to add or correct?"
- Allow the user to edit, add, or remove statements
- If the user adds new statements, incorporate them

### 5. Pass to Phase 9

The confirmed intent, constraints, autonomy boundaries, and topology flow directly into Phase 9 (Instructions) where they become part of `copilot-instructions.md`.

## Important

- **Read-only**: Only read documents — never modify them
- **Respect access**: If an MCP server can't access a document, note it and move on
- **Don't invent**: Only distill what's actually in the docs and history. If intent isn't documented, flag it: "No explicit deployment policy was found — consider documenting one"
- **Be concise**: Each statement should be one clear sentence that an agent can act on
- **Ask, don't assume**: When a document is ambiguous, ask the user to clarify rather than interpreting
- **History complements docs**: When history contradicts documentation, present both signals to the user — the truth is usually in the gap between them

## Fallback

If no tagged sources are available (Phase 3 was skipped or found nothing):
- Session history from `context-history` may still provide behavioural intent — use it
- If history is also empty, ask the user directly: "I couldn't find documented intent or session history. Can you tell me your team's top 3 priorities and any hard rules agents should follow?"
- Use the answers to populate the same structured output

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-distill';
```
