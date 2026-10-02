# Recording Intent in Ape Context

Ape Context discovers and distills organizational context. It does not define a
decision-record standard. Consequential decisions are handed to the standalone
[Ape Decision Record Profile (ADRP)](https://github.com/suuus/adrp), which owns
the canonical schema, lifecycle, fingerprints, imports, resolution, autonomy,
and immutable ratification behavior.

## Boundary

Broad context remains broad context:

- goals and desired outcomes;
- facts and observations;
- policies and constraints;
- topology and ownership clues;
- recommendations and guidance;
- unresolved gaps.

Only an explicit or strongly evidenced choice becomes a decision candidate.
Location proves provenance, not authority. Missing authority, scope,
alternatives, trade-offs, or Evidence requirements remain gaps.

## Workflow

1. `context-docs` discovers sources.
2. `context-distill` extracts sourced Intent and separates decision candidates.
3. Existing `ape-decision-record/v1` documents are validated and assessed with
   the published `adrp` CLI. They are never redrafted as new candidates.
4. `context-decisions` presents each candidate for human confirmation.
5. Confirmed candidates become inactive ADRP drafts under
   `.github/decisions/drafts/`.
6. Eligible external ADRP records may be imported verbatim with separate source
   sidecars and explicit local acceptance.
7. `context-ratify` uses `adrp ratify` to create immutable versions bound to the
   exact generated context fingerprint.
8. `context-feedback` binds resulting AERP Evidence to those exact ADRP records.

## Required CLI operations

```bash
adrp --version
adrp validate --target .github/decisions/drafts/ADR-0001.json
adrp fingerprint --target .github/decisions/drafts/ADR-0001.json
adrp assess --target external-decision.json
adrp import --target external-decision.json \
  --snapshot .github/decisions/imported/ADR-0042/v003.json \
  --metadata-output .github/decisions/imported/ADR-0042/v003.source.json \
  --source-uri https://example.org/decisions/ADR-0042.json
adrp ratify \
  --target .github/decisions/drafts/ADR-0001.json \
  --output .github/decisions/ADR-0001/v001.json \
  --confirmed-by "current user" \
  --approval-meaning "Approved for the recorded scope." \
  --context-fingerprint sha256:<digest>
```

A missing or failing CLI blocks the dependent phase. Ape Context must not
replace deterministic ADRP behavior with prompt-only logic or copied schemas.

## Continue through Structure and Evidence

Ratified Intent is not the end of the workflow:

- `context-structure` binds confirmed ownership, interfaces, boundaries, gates,
  entry points, and Evidence obligations into ASRP Structure records.
- `context-ratify` may compile an `isee-execution-manifest/v1` for external
  execution systems.
- `context-feedback` captures AERP observations, assessments, approvals, and
  outcomes with exact ADRP and ASRP bindings.

Read the normative ADRP documentation in the
[ADRP repository](https://github.com/suuus/adrp).
