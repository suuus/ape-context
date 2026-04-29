---
name: context-history
description: Analyze Copilot session history to discover intent patterns, recurring workflows, and team topology
user-invocable: true
---

Analyze the user's Copilot session history to extract behavioural patterns that reveal implicit intent, recurring workflows, and areas of focus. This complements documentation-based analysis — docs tell you what the team *says* they value, history tells you what they *actually do*.

## Data Source

Use the `session_store_sql` tool to query the cloud session store. This contains all past Copilot sessions with:

- **sessions** — id, repository, branch, summary, timestamps
- **turns** — user messages and assistant responses per session
- **session_files** — files edited/created per session
- **session_refs** — commits, PRs, and issues linked to sessions

Use `scope: "personal"` for individual patterns, `scope: "repository"` for team-wide patterns when the user wants a broader view.

## Analysis Steps

### 1. Session themes (last 30 days)

```sql
-- What has the user been working on?
SELECT summary, repository, created_at
FROM sessions
WHERE summary IS NOT NULL
  AND created_at > now() - INTERVAL '30 days'
ORDER BY created_at DESC
```

Cluster session summaries by theme. Look for:
- **Recurring tasks** — "Deploy to Azure" appearing weekly = deployment velocity matters
- **Dominant repos** — which repos get the most sessions = areas of ownership
- **Task types** — fix, build, deploy, investigate, onboard = work profile

### 2. File edit hotspots

```sql
-- Which files get touched most across sessions?
SELECT file_path, tool_name, COUNT(*) as touches
FROM session_files
WHERE first_seen_at > now() - INTERVAL '30 days'
GROUP BY file_path, tool_name
ORDER BY touches DESC
LIMIT 20
```

Identify:
- **Hot files** — files edited in many sessions = high-priority areas
- **Config vs code ratio** — lots of config edits = infrastructure focus; lots of source edits = feature focus
- **Agent/skill files** — editing `.agent.md` or `SKILL.md` files = meta-work on the AI layer itself

### 3. Cross-repo topology

```sql
-- Which repos are worked on together?
SELECT repository, COUNT(*) as session_count
FROM sessions
WHERE created_at > now() - INTERVAL '30 days'
  AND repository IS NOT NULL
GROUP BY repository
ORDER BY session_count DESC
```

Map:
- **Repo clusters** — repos that appear in sessions close together are likely coupled
- **Ownership signals** — repos with the most sessions = primary ownership
- **Cross-cutting work** — sessions that reference multiple repos = integration points

### 4. Workflow patterns

```sql
-- What references (PRs, issues) appear in sessions?
SELECT ref_type, ref_value, COUNT(*) as cnt
FROM session_refs
WHERE created_at > now() - INTERVAL '30 days'
GROUP BY ref_type, ref_value
ORDER BY cnt DESC
LIMIT 15
```

Reconstruct:
- **Issue → session → PR** chains = actual workflow
- **Recurring issue patterns** = persistent problem areas
- **PR frequency** = delivery cadence

### 5. User message patterns

```sql
-- What does the user ask about most?
SELECT substr(COALESCE(user_message, ''), 1, 200) as message
FROM turns
WHERE user_message IS NOT NULL
  AND timestamp > now() - INTERVAL '30 days'
ORDER BY timestamp DESC
LIMIT 50
```

Extract:
- **Recurring requests** — same type of question across sessions = unmet need or priority
- **Frustration signals** — error investigation sessions, retries = pain points
- **Decision patterns** — what the user approves vs rejects = implicit preferences

## Output Format

Distill findings into the same categories as `context-distill`:

### Observed intent
What the history shows the user/team values:
- "You deploy to Azure frequently — deployment speed and reliability appear to be priorities"
- "Most sessions involve agent/skill files — the AI development layer is a primary focus"

### Observed constraints
Implicit rules visible in behaviour:
- "You always edit copilot-instructions.md after changing agent files — instructions and agents are kept in sync"
- "PR-linked sessions always follow issue-linked sessions — you follow an issue-first workflow"

### Observed topology
Ownership and coupling:
- "You primarily work across 3 repos: demogod, ape-context, Squad-IRL"
- "demogod and ape-context are often worked on in the same day — they may be coupled"

### Gaps and suggestions
Where history reveals missing structure:
- "No session refs link to Jira tickets — consider enforcing ticket references"
- "Config files are edited frequently but no drift detection is configured"

## Presenting Results

Use `ask_user` to present findings and confirm:
- "Based on your session history, here's what I observed about your work patterns. Are these accurate?"
- Allow the user to correct, add, or dismiss observations
- Confirmed observations feed into `context-distill` (Phase 8) or directly into `copilot-instructions.md`

## Scope Selection

When invoked standalone, ask the user:
- "Should I analyze just your personal history, or the full repository history (all contributors)?"
- Personal = individual workflow patterns
- Repository = team-wide patterns and topology

## Important

- **Read-only** — only query the session store, never modify it
- **Privacy-aware** — when using `repository` scope, focus on aggregate patterns, not individual user messages
- **Don't overfit** — 30 days is a window, not a permanent truth. Flag observations as "recent patterns" not "team rules"
- **Complement, don't replace** — history-based intent supplements documentation-based intent; it doesn't override it
