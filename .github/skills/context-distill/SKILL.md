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

**If history consent is denied or history returns empty:**
- Tell the user: "Session history analysis was skipped — I'll work from your documentation sources instead."
- This is a valid choice, not a failure. Continue to step 1 normally.
- If doc sources are also unavailable (Phase 3 was skipped), the Fallback section at the end of this skill will activate.

### 1. Gather tagged sources from Phase 3

Review the doc sources discovered earlier, grouped by content tag:
- `[intent]` — team priorities, values, strategy
- `[constraint]` — security policies, compliance rules, approval requirements
- `[process]` — ceremonies, workflows, decision flows, escalation paths
- `[reference]` — API specs, guides (lower priority for distillation)

Retrieve tagged sources from the session store:

```sql
SELECT value FROM session_state WHERE key = 'tagged_doc_sources';
```

If no state exists, check conversation context for Phase 3 output. If neither is available, inform the user: "No documentation sources found from Phase 3. Run `/context-docs` first, or I'll ask you directly about your team's intent."

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

**Classify each boundary explicitly.** After extracting boundaries from docs and history, present them to the user with autonomy levels using `ask_user`:

For each action type discovered (creating PRs, merging code, deploying, creating tickets, closing tickets, modifying infrastructure, accessing production data, sending emails, creating pages, etc.), ask the user to classify:

- **`PROCEED`** — agents can do this without asking
- **`ALWAYS ASK`** — agents must get human confirmation first
- **`NEVER`** — agents must not attempt this at all

```yaml
ask_user:
  message: "For each action, how much autonomy should agents have? Defaults are based on what I found in your docs."
  requestedSchema:
    properties:
      {action_key}:
        type: string
        title: "{Human-readable action}"
        enum: ["PROCEED", "ALWAYS ASK", "NEVER"]
        default: "{default based on docs/history}"
```

Set sensible defaults:
- Read-only operations → `PROCEED`
- Creating draft artifacts (PRs, tickets, branches) → `PROCEED`
- Destructive or irreversible actions (merge, deploy, delete) → `ALWAYS ASK`
- Actions outside the team's domain (modify infra, change auth) → `NEVER` or `ALWAYS ASK`

Store the confirmed classifications as structured autonomy boundaries with their level, to be rendered as a table in Phase 9.

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

### 4.5. Log intent changes

Before passing to Phase 9, diff the previous and new intent to maintain an auditable changelog.

**Read previous state:**
- Read the existing `.github/copilot-instructions.md` and extract current intent statements, constraints, autonomy boundaries, and topology
- If the file doesn't exist or has no intent section, treat all confirmed statements as `added`

**Classify each change:**
- `added` — new statement not in previous version
- `modified` — statement exists but wording or scope changed
- `removed` — previous statement not in confirmed set
- `unchanged` — no change

**Write to `.github/intent-changelog.md`:**

If changes exist (any added, modified, or removed), append an entry:

```markdown
## {YYYY-MM-DD} — {trigger}

**Trigger:** {initial setup | manual re-distill | drift-triggered}

### Added
- {new statement}

### Modified
- **Was:** {old statement}
  **Now:** {new statement}

### Removed
- ~~{removed statement}~~

### Unchanged
{count} statements unchanged
```

If the file doesn't exist, create it with this header first:

```markdown
# Intent Changelog

> Tracks changes to distilled intent statements, constraints, and autonomy boundaries.
> Generated by the Context Setup Wizard. See [ISEE framework](https://agentile.com/agents).
```

If this is the first run with no previous statements, log everything as `added` with trigger `initial setup`.

**Determine trigger:**
- If invoked as Phase 8 of the wizard: `initial setup` (first run) or `manual re-distill` (subsequent)
- If invoked after `context-drift` suggested re-distillation: `drift-triggered`
- If invoked standalone by the user: `manual re-distill`

**Persist results:**

Write the confirmed distilled statements to the session store for Phase 9 and Phase 10:

```sql
INSERT OR REPLACE INTO session_state (key, value) 
VALUES ('distilled_intent', '{json with intent[], constraints[], autonomy[], topology[]}');
```

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
