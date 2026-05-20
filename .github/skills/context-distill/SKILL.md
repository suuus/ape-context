---
name: context-distill
description: >-
  DISTILL SKILL. Build distilled_intent from docs/history incl. regulatory constraints. USE FOR: context-wizard distillation, manual/drift re-distill. DO NOT USE FOR: discovery, live history queries, policy invention, code/infra edits. REQUIRES: tagged_doc_sources/history_observations; else ask. INVOKES: ask_user, doc reads, session_state, changelog.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

## Contracts
Inputs: `tagged_doc_sources`=`[{category,platform,location,tag,url?,notes?}]`; `history_observations`=`{intent[],constraints[],topology[],gaps[],sources[]}`.
Output: `distilled_intent`=`{intent[],constraints[],autonomy[],topology[],history_observations?}`.

## Procedure
1. For dry-run prompts: use fixtures; skip live M365/Jira/history and edits.
2. Load inputs. If none exist, only ask for priorities/rules/autonomy; return no inferred facts or example policies. If one source is missing, proceed and note it.
3. Read supplied intent/constraint/process docs incl. regulatory/audit via files, `workiq`, or Jira; skip inaccessible sources.
4. Extract sourced/user-confirmed intent, obligations, evidence needs, autonomy limits, and gaps only; do not invent.
5. Autonomy uses `level/action/reason/source`: `PROCEED`=no ask; `ALWAYS ASK`=confirm; `NEVER`=forbidden. Defaults: read-only `PROCEED`; destructive `ALWAYS ASK`; out-of-domain `NEVER`/`ALWAYS ASK`.
6. Ask user to confirm/edit; no interaction sets `needs_confirmation`.
7. Diff previous/new as `added`, `modified`, `removed`, `unchanged`; trigger `initial setup`, `manual re-distill`, or `drift-triggered`. Append changelog only for changes.
8. Persist to `session_state`; report write failures. Mark `ctx-distill` done only when `context-wizard` invoked and todo exists.

## Side effects
External docs/history reads are read-only. Local writes: `.github/intent-changelog.md`, `session_state`; never claim fully read-only.
