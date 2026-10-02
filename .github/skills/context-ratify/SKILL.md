---
name: context-ratify
description: >-
  HUMAN RATIFICATION GATE. USE FOR: Phase 13, approve exact context, ratify ADRP
  Intent, confirm ASRP Structure, compile an approved manifest. DO NOT USE FOR:
  quality review, invention, certification, commits, pushes, or execution.
  REQUIRES: passing quality. INVOKES: ask_user, profile CLIs, helper, state.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

Load context, changelog, Intent, ADRP drafts/imports, ASRP drafts, and
`context_quality_review`. Validate with `adrp` and `asrp`. Only pass or
pass-with-warnings continues; dry-run writes nothing.

Present sources/standing, decision alternatives and trade-offs, imported record
acceptance, Structure ownership/interfaces/boundaries/gates/entry points/
Evidence duties, autonomy, gaps, generated wording, CAFE(S) warnings, and the
notice that approval is not specialist certification. Ask `Approve`, `Revise`,
or `Stop`.

- **Approve:** ask review date; fingerprint context. Run `adrp ratify` and render
  new immutable decision versions. Create confirmed immutable ASRP versions,
  run `asrp validate`, `asrp bind-intent` where needed, and `asrp fingerprint`.
  With confirmed scope/entry point, run `asrp compile` to
  `.github/isee/execution-manifest.json`. Write
  `.github/context-ratification.md` only after every command succeeds. Persist
  `decision_records`, `structure_records`, `execution_manifest`, and
  `context_ratification`.
- **Revise:** write nothing; route to Distill, Decisions, Structure,
  Instructions, or Quality.
- **Stop:** leave drafts inactive.

Record exact context/quality/ADRP/ASRP fingerprints, approval meaning, current
user, scope, warnings, gaps, trigger, and review date. Never invent identity or
authority. Partial ratification fails closed.
