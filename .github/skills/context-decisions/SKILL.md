---
name: context-decisions
description: >-
  ADRP INTENT GATE. Convert confirmed decision candidates into validated ADRP drafts or import eligible external ADRP records. USE FOR: Phase 9 or decision renewal. DO NOT USE FOR: inventing policy, ratification, activation, commits, or pushes. REQUIRES: decision_candidates and distilled_intent. INVOKES: ask_user, adrp CLI, session_state.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

Load `decision_candidates`, `decision_sources`, and intent. Ordinary facts and
constraints are not decisions. Location proves provenance, not authority.

For candidates present statement, standing, alternatives, four-domain trade-offs,
autonomy, gaps, review trigger; ask `Draft`, `Revise`, or `Skip`. Draft canonical
`ape-decision-record/v1` at `.github/decisions/drafts/<id>.json` with stable ID,
UUID/version, provenance, authority, lifecycle, relationships, and
`ratification:null`. Never invent missing data.

For ADRP sources present ID/version/fingerprint, URI, status, lifecycle, authority,
scope, and helper assessment; ask `Accept`, `Preserve`, or `Ignore`. Accept requires
eligibility and explicit local scope/authority confirmation. Preserve is inactive.
Future, expired, review-due, terminal, invalid, or untrusted records cannot activate.

Resolve `adrp` and run `adrp --version`. Validate with
`adrp validate --target` and fingerprint with `adrp fingerprint --target`;
persist `decision_drafts`. For Accept/Preserve run `adrp import`,
creating verbatim immutable
`.github/decisions/imported/<id>/vNNN.json` plus `vNNN.source.json`. Never inject
retrieval metadata into canonical JSON. Accept supplies basis and confirming
identity. Persist `imported_decisions` with paths, URI, fingerprint, assessment,
and disposition. Reuse existing record ID/fingerprint; never duplicate.

Drafts and unaccepted imports are not active policy. Failure blocks. Dry-run writes
nothing and claims no approval. ADRP owns the schema and deterministic lifecycle;
Ape Context must not copy, fork, or silently reimplement it.
