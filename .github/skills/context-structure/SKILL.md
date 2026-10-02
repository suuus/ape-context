---
name: context-structure
description: >-
  ASRP STRUCTURE HANDOFF. Convert confirmed structure candidates into validated
  ASRP drafts and an optional execution manifest. USE FOR: Phase 10 or
  structure renewal. DO NOT USE FOR: inventing architecture, activating drafts,
  execution, commits, or pushes. REQUIRES: structure_candidates and ADRP
  decision references. INVOKES: ask_user, asrp CLI, session_state.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

Load `structure_candidates`, `decision_drafts`, `imported_decisions`, and
`distilled_intent`. Missing or uncertain ownership, boundaries, gates, entry
points, or Evidence obligations remain explicit gaps.

For each coherent scope, present the proposed actors, components, responsibilities,
interfaces, dependencies, boundaries, gates, entry points, artifacts, and Evidence
requirements. Ask `Draft`, `Revise`, or `Skip`.

On `Draft`, author canonical `ape-structure-record/v1` JSON under
`.github/structures/drafts/<structure-id>.json`. Resolve `asrp`, run
`asrp --version`, `asrp validate`, and `asrp fingerprint`. Where the exact ADRP
record is known, run `asrp bind-intent` and validate the bound output. Persist
`structure_drafts` with paths, IDs, versions, fingerprints, Intent bindings, gaps,
and status.

Do not mark a Structure draft effective. During ratification, explicit human
confirmation may produce an effective immutable record under
`.github/structures/<structure-id>/vNNN.json`. After effective records exist,
`asrp compile` may create `.github/isee/execution-manifest.json` for a
user-confirmed scope and entry point. Persist `execution_manifest` with its path,
schema version, Intent fingerprints, Structure fingerprints, gates, and Evidence
requirements. Execution remains external.

ASRP owns the schema, fingerprints, and manifest contract. Ape Context only
discovers candidates and orchestrates the handoff. Missing/failing CLI or
validation blocks. Dry-run writes nothing and claims no active Structure.
