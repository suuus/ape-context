---
name: context-distill
description: >-
  INTENT DISTILLATION. USE FOR: Phase 8, re-distill sourced Intent, identify
  ADRP decisions, identify ASRP Structure candidates. DO NOT USE FOR: source
  discovery, invented policy, profile drafting, ratification, or code edits.
  INVOKES: reads, ask_user, adrp CLI, changelog, session_state.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

Load `tagged_doc_sources` and optional `history_observations`. Persist:

- `distilled_intent`: `{intent[],constraints[],autonomy[],topology[],gaps[]}`;
- `decision_candidates`: explicit/strongly evidenced choices;
- `decision_sources`: detected ADRP records;
- `structure_candidates`: sourced ownership, components, responsibilities,
  interfaces, boundaries, gates, entry points, artifacts, and Evidence duties.

Always name those keys literally, including in dry runs.

## Procedure

1. Use fixtures only in dry-run. Ask about missing priorities, rules, or gaps.
2. Read accessible sources. Source location proves provenance, not authority.
3. For `ape-decision-record/v1`, run `adrp --version`,
   `adrp validate --target`, and `adrp assess --target`. Preserve identity,
   fingerprint, lifecycle, scope, authority, and gaps; never redraft it.
4. Extract only sourced/user-confirmed Intent, obligations, autonomy, topology,
   and candidates. Use authority states `authoritative`, `advisory`,
   `conflicting`, `unknown`, or `user-confirmed`.
5. A constraint is not automatically a decision. ASRP candidates are not active
   Structure until `context-structure` validates them.
6. Classify autonomy as `PROCEED`, `ALWAYS ASK`, or `NEVER`.
7. Confirm accuracy; without interaction mark `needs_confirmation`.
8. Diff as `added`, `modified`, `removed`, and `unchanged`. Real changes append
   to `.github/intent-changelog.md` with trigger `initial setup`,
   `manual re-distill`, or `drift-triggered`; dry runs describe the entry only.

Missing/failing ADRP CLI blocks ADRP source processing. Never claim persisted
state when SQL fails.
