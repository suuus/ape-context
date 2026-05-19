---
name: context-history
description: >-
  HISTORY SKILL. Analyze consented Copilot session history into history_observations. USE FOR: recent intent patterns, recurring workflows, repo topology, gaps, and context-distill/context-wizard input. DO NOT USE FOR: live monitoring, audits, or file edits. REQUIRES: explicit consent and session_store_sql. INVOKES: ask_user first; read-only session_store_sql/DuckDB only after consent.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

Produce behavioral observations from recent Copilot history.

## Steps
1. Ask consent first, before scope selection or any history query. Use `ask_user` boolean consent. Explain last-30-day read-only access to summaries, files, refs, messages, purpose, and privacy limits. If declined or cancelled, stop with "session history analysis skipped" and do not query.
2. Choose scope. Standalone asks `personal` vs `repository` when missing; wizard uses requested scope or defaults to `personal`. Personal may summarize the current user's messages truncated to 200 chars. Repository must aggregate team patterns and never surface individual messages from other contributors.
3. Query only with `session_store_sql`, which uses DuckDB. Every query must include a time filter such as `now() - INTERVAL '30 days'`, a `LIMIT`, and nullable-column guards (`IS NOT NULL` or `COALESCE`). Prefer summaries, file aggregates, refs, and counts.
4. Cluster recent signals into intent, constraints, topology, and gaps. Treat findings as recent patterns, not permanent rules.
5. Output exactly:
```json
{"history_observations":{"intent":[],"constraints":[],"topology":[],"gaps":[],"sources":[]}}
```
Populate arrays with concise observations and source labels like `sessions.summary`, `session_files aggregate`, `session_refs aggregate`, or notes. Standalone reports the object; downstream `context-distill` may consume it.

## Errors
If `session_store_sql` is unavailable, blocked, or fails, report skipped. If no rows return, state "no recent patterns". Then produce empty observations with notes in `sources`; do not fabricate.

## Safety
Read only. Do not edit files or persist secrets. In explicit dry-run eval prompts, use the provided simulated consent/results and do not query live history.
