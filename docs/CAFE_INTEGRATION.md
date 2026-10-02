# CAFE(S) Integration Architecture

## Purpose

Ape Context uses ISEE to discover, interpret, and operationalize organizational
Intent, Structure, Execution boundaries, and Evidence. CAFE(S) adds a separate
quality discipline for the assembled context that an agent will actually receive.

The combined workflow must answer two independent questions:

1. **ISEE standing:** Is this an authorized, attributable, scoped, and reviewable
   representation of organizational Intent?
2. **CAFE(S) fitness:** Is the resulting context clear, actionable, faithful,
   efficient, and secure enough for an agent to use?

Neither question can replace the other. High-quality context can encode a decision
that nobody was authorized to make. Legitimate policy can also be translated into
ambiguous, stale, noisy, or unsafe instructions.

## Deterministic Artifact Boundary

Prompt instructions are not a sufficient control for byte-preserving merges,
secret redaction, artifact identity, profile validation, or immutable
ratification. Ape Context ships one Python 3 standard-library helper for its own
generated context artifacts: `.github/scripts/context_artifacts.py`. The
standalone ADRP, ASRP, and AERP CLIs remain authoritative for their profiles.

It is the required implementation boundary for:

- atomic create/append/replace of `## Enterprise Context`;
- refusal to overwrite an unmarked manual section without explicit approval;
- canonical SHA-256 fingerprints after line-ending and trailing-space
  normalization;
- sanitization of reports using sensitive-name patterns, known MCP environment
  values, and sensitive process environment values;
- fail-closed behavior when input is malformed or sanitization cannot be proven.

Skills generate semantic content. The helper performs deterministic artifact
operations. Skills must not reproduce these operations through free-form editing.

The published `adrp` CLI is the required boundary for:

- strict structural and semantic validation of canonical ADRP JSON;
- canonical SHA-256 fingerprints excluding the ratification envelope;
- selected-alternative and provenance-reference integrity;
- immutable draft-to-ratified version creation without overwrite;
- binding each approved decision to the exact Enterprise Context fingerprint;
- deterministic Markdown rendering from canonical JSON;
- tamper detection for ratified records;
- lifecycle/expiry/authority assessment of encountered ADRP documents;
- verbatim immutable imports with separately validated source sidecars.

The published `asrp` CLI owns Structure validation, fingerprints, Intent
bindings, graph resolution, and `isee-execution-manifest/v1` compilation. The
published `aerp` CLI owns Evidence records, ADRP/ASRP bindings, artifact-byte
verification, and interoperability exports.

Resolve the Ape Context helper in this order:

1. `.github/scripts/context_artifacts.py` for copied installations;
2. `.ape-context/.github/scripts/context_artifacts.py` for submodules;
3. `$HOME/.copilot/installed-plugins/isee/ape-context/.github/scripts/context_artifacts.py`
   for unified marketplace installations;
4. the legacy direct-plugin path for older installations.

Resolve `adrp`, `asrp`, and `aerp` as executable commands and verify each with
`--version`. If a required helper or CLI does not exist or fails, the dependent
phase fails closed and points the user to `isee-setup`.

## Source Framework

CAFE(S), introduced in *CAFE(S): Your Agent Is Only As Good As Its Context*,
defines five properties of assembled context:

| Dimension | Evaluation question | Typical failure |
|-----------|---------------------|-----------------|
| Clarity | Can the agent interpret the request as intended? | The agent silently chooses between plausible interpretations. |
| Actionability | Can the agent proceed and know when it is done? | The agent invents an objective, constraint, or finish line. |
| Fidelity | Can the agent trust that the context is true? | The agent follows stale, conflicting, unsupported, or unattributed guidance. |
| Efficiency | Can the agent focus on what matters? | Governing information is buried in irrelevant context or repeated at the wrong scope. |
| Security | Should the agent have this context at all? | Untrusted content becomes instruction, or sensitive information is overshared. |

CAFE(S) defines context quality; it is not currently a validated measurement
system. Ape Context therefore uses categorical findings and evidence, not a
synthetic numeric score.

## Combined ISEE and CAFE(S) Model

The CAFE(S) paper places its framework in this pipeline:

```text
Intent -> Context -> Harness -> Model
```

Ape Context expands that pipeline through ISEE:

```text
Authoritative sources
    |
    v
ISEE discovery and standing
    |
    v
Intent and constraints distilled with provenance
    |
    v
Canonical decision drafts with alternatives, authority, and trade-offs
    |
    v
Eligible imports with explicit local scope and authority acceptance
    |
    v
ASRP Structure drafts with ownership, interfaces, gates, and Evidence obligations
    |
    v
Context assembled into Copilot instructions
    |
    v
CAFE(S) quality review
    |
    v
ISEE human ratification
    |
    v
Immutable ADRP and ASRP records plus optional execution manifest
    |
    v
Published context used by the harness and agent
    |
    v
AERP Evidence, drift, challenge, and re-distillation
```

The output of distillation is not automatically authoritative merely because it was
found in an organizational system. Likewise, generated instructions are not ready
for use merely because they are syntactically correct. The workflow must preserve
source provenance, evaluate translation quality, and obtain explicit human
ratification after the final context has been assembled.

## Two Human Gates

Ape Context has two different approval moments.

### Setup-plan approval

The existing `context-review` skill runs before installation. It approves:

- proposed MCP servers;
- tool scopes;
- authentication approach;
- source systems to inspect;
- files the wizard expects to create or modify.

This gate authorizes the setup operation. It does not approve extracted Intent or
the generated interpretation of policy.

### Context and decision ratification

The new `context-ratify` skill runs after instructions have been generated and
reviewed through CAFE(S). It approves:

- the extracted Intent statements;
- constraints and regulatory obligations;
- autonomy boundaries;
- source and authority metadata;
- decision alternatives, rationale, security/cost/compliance/operations
  trade-offs, consequences, relationships, and review conditions;
- the wording and scope of generated agent instructions;
- accepted CAFE(S) warnings and residual risks.

This gate authorizes the context artifact itself. Ratification must be durable so
later users can distinguish reviewed context from an unapproved draft.

## Revised Wizard Lifecycle

The wizard uses 14 ordered phases.

| Phase | Skill | Primary purpose |
|-------|-------|-----------------|
| 1. Detect | `context-detect` | Discover stack, current controls, and existing context configuration. |
| 2. Discover | `context-discover` | Identify approved context and tool integrations with minimum necessary scope. |
| 3. Docs | `context-docs` | Locate candidate sources of Intent, Structure, process, and reference material. |
| 4. Review | `context-review` | Obtain approval for the setup plan before making changes. |
| 5. Install | `context-install` | Write approved MCP configuration and tool scope. |
| 6. Configure | `context-configure` | Establish authentication without storing credentials. |
| 7. Healthcheck | `context-healthcheck` | Verify source accessibility and connection health. |
| 8. Distill | `context-distill` | Extract sourced Intent, constraints, autonomy, topology, and governance metadata. |
| 9. Decisions | `context-decisions` | Convert confirmed decision candidates into ADRP-validated drafts or imports. |
| 10. Structure | `context-structure` | Convert confirmed ownership, interfaces, boundaries, gates, and Evidence obligations into ASRP-validated drafts. |
| 11. Instructions | `context-instructions` | Assemble Enterprise Context with applicable ADRP and ASRP references. |
| 12. Quality | `context-quality` | Evaluate context fitness and fidelity to Intent and Structure. |
| 13. Ratify | `context-ratify` | Jointly approve context and create immutable ADRP/ASRP versions plus an optional execution manifest. |
| 14. Feedback | `context-feedback` | Capture AERP Evidence, validate all artifacts, report results, and offer follow-up and commit actions. |

Phase 12 is a blocking quality gate. Phase 13 is a blocking authority gate.
Feedback and commit cannot proceed until both gates have passed.

## Decision Record Contract

Distillation persists `decision_candidates` separately from ordinary Intent and
constraints. A constraint is not automatically a decision. A candidate qualifies
when the workflow must preserve a choice among alternatives, rationale, authority,
consequences, or material trade-offs.

`context-decisions` writes validated canonical drafts under:

```text
.github/decisions/drafts/<decision-id>.json
```

Drafts use `ape-decision-record/v1`, have `ratification: null`, and are never
active policy. On approval, `context-ratify` creates:

```text
.github/decisions/<decision-id>/vNNN.json
.github/decisions/<decision-id>/vNNN.md
```

The JSON is canonical. Markdown is a generated view, never the signing source.
The immutable JSON contains both its decision-payload fingerprint and the exact
Enterprise Context fingerprint approved in the same human act. A digest proves
integrity, not approver identity or legitimate organizational standing; the
ratification envelope records those separately.

External ADRP records use
`.github/decisions/imported/<decision-id>/vNNN.json`. The snapshot preserves the
source bytes exactly. Adjacent `vNNN.source.json` stores the literal URI,
digest/ETag, retrieval time, lifecycle assessment, and explicit local acceptance.
This supports refresh and drift checks without changing source provenance or
fingerprints.

## Distilled Intent Contract

Distilled items should preserve enough metadata to support both quality review and
ratification. Existing simple string fixtures remain valid, but newly generated
items should prefer this shape:

```json
{
  "statement": "Production deployment requires explicit human approval.",
  "kind": "constraint",
  "source": "docs/production-policy.md",
  "authority_status": "authoritative",
  "owner": "Platform Engineering",
  "scope": "production deployments",
  "effective_date": "2026-05-01",
  "review_by": "2026-11-01"
}
```

Metadata rules:

- `source` is required for extracted claims and uses `user-confirmed` for a
  statement supplied directly during the wizard.
- `authority_status` is `authoritative`, `advisory`, `conflicting`, `unknown`, or
  `user-confirmed`.
- `owner`, `scope`, `effective_date`, and `review_by` are included only when the
  source states them or the user confirms them.
- Missing governance metadata is recorded as a gap. It must never be invented.
- A source proves provenance, not authority. A document can exist and still have
  unknown standing.

## CAFE(S) Review Contract

`context-quality` produces a `context_quality_review` state object:

```json
{
  "artifact": ".github/copilot-instructions.md#enterprise-context",
  "artifact_fingerprint": "sha256:<digest>",
  "status": "pass_with_warnings",
  "dimensions": {
    "clarity": {"status": "pass", "findings": []},
    "actionability": {"status": "warning", "findings": []},
    "fidelity": {"status": "pass", "findings": []},
    "efficiency": {"status": "pass", "findings": []},
    "security": {"status": "pass", "findings": []}
  },
  "blocking_findings": [],
  "warnings": [],
  "unassessed": [],
  "reviewed_at": "ISO-8601 timestamp"
}
```

Allowed dimension statuses are:

- `pass`
- `warning`
- `fail`
- `not_assessed`

Overall status is:

- `pass` when every dimension passes;
- `pass_with_warnings` when there are warnings but no blocking findings;
- `fail` when any blocking finding exists;
- `incomplete` when a required dimension cannot be assessed.

The review must cite the exact section, statement, or missing artifact behind each
finding. It must not infer source authority or claim that external facts were
verified when they were not.

The fingerprint is the SHA-256 digest of the generated Enterprise Context section
after normalizing line endings to LF and removing trailing whitespace. Quality
review is incomplete when a reliable fingerprint cannot be created.

The canonical command is:

```bash
python3 <resolved-context_artifacts.py> fingerprint \
  --target .github/copilot-instructions.md
```

## Dimension-Specific Checks

### Clarity

Check that:

- material terms identify the system, environment, data class, domain, and policy
  they concern;
- pronouns and references have a single plausible target;
- autonomy actions are concrete rather than broad labels;
- conflicts are presented as conflicts rather than silently resolved;
- scope is explicit where an instruction could apply at more than one altitude.

A material ambiguity that could change an action is blocking. Minor wording
ambiguity is a warning.

### Actionability

Check that:

- objectives and required outcomes are explicit;
- constraints say what the agent should do, not only what it must avoid;
- completion criteria are present where the workflow has a defined finish line;
- `ALWAYS ASK` rules identify the decision or action requiring approval;
- `NEVER` rules identify a safe stop or escalation route where relevant;
- gaps and impossible tasks cause escalation rather than guessing.

Missing stopping criteria for an autonomous or costly workflow is blocking.

### Fidelity

Check that:

- generated statements trace to distilled sources or explicit user confirmation;
- authoritative and advisory material are distinguishable;
- conflicting sources remain visible;
- changelog and generated instructions agree;
- dates, owners, scope, and review cadence are preserved when available;
- generated instructions reference the applicable decision IDs and do not
  contradict their selected alternatives, authority, trade-offs, or autonomy;
- every decision draft passes deterministic validation before it can be reviewed;
- unknown or stale sources are not presented as current fact.

An unsourced mandatory constraint or a material contradiction hidden from the user
is blocking.

### Efficiency

Check that:

- the generated Enterprise Context remains within the existing 80-line or
  approximately 2,000-token budget unless constraints require more;
- repeated guidance is consolidated;
- local instructions are not promoted to repository-wide context without reason;
- constraints are retained before optional guidance;
- the artifact contains links to detailed sources instead of reproducing them
  wholesale;
- each instruction is placed at the narrowest useful scope.

Efficiency findings normally warn. Removing a constraint merely to meet the budget
is prohibited.

### Security

Check that:

- credentials and secret values are absent;
- sensitive source content is minimized and referenced rather than copied;
- untrusted content such as tickets, email, pull requests, and retrieved prose is
  treated as data rather than instruction;
- tool scope is compatible with autonomy boundaries;
- generated context does not grant capabilities;
- regulatory or personal data is not reproduced unnecessarily.

Credential disclosure, unsafe treatment of untrusted content, or instructions that
contradict configured tool scope are blocking.

## Remediation and Re-review

`context-quality` does not silently rewrite the generated context. It reports
findings and asks before invoking remediation.

The expected loop is:

```text
Quality review fails
    |
    +-> source or authority problem -> return to context-distill
    |
    +-> wording, scope, or placement problem -> return to context-instructions
    |
    +-> tool-scope or access problem -> return to context-discover/install
    |
    +-> missing information -> ask the user or record an unresolved gap
    |
    v
Regenerate and rerun context-quality
```

Warnings may proceed to ratification, but the ratification record must list them as
accepted residual risk. Failures and incomplete reviews cannot proceed.

## Ratification Record

`context-ratify` writes `.github/context-ratification.md` only after explicit user
approval. The record contains:

- status: `ratified`;
- ratification timestamp;
- artifact reviewed;
- SHA-256 fingerprint of the reviewed Enterprise Context;
- overall CAFE(S) result;
- distilled Intent and constraints covered by the approval;
- autonomy boundary summary;
- unresolved warnings accepted by the user;
- source and authority gaps that remain visible;
- trigger: initial setup, manual re-ratification, or drift-triggered;
- next review date when supplied or derived from confirmed source metadata.

The record must not claim legal, security, or compliance approval unless the user
explicitly states that an authorized reviewer supplied it. Generic user approval is
recorded as workflow ratification, not specialist certification.

If the user selects Revise, no ratification record is written and the selected phase
is reopened. If the user selects Stop, generated context remains a draft and
Feedback must not offer to commit it as active context.

## Evidence and Drift

CAFE(S) is not a one-time check. Drift can invalidate each dimension:

| Drift | Affected dimension |
|-------|--------------------|
| Renamed service, environment, or team | Clarity |
| Changed deployment or approval workflow | Actionability |
| Stale policy, schema, owner, or source | Fidelity |
| Accumulated duplicate instructions | Efficiency |
| New data source, capability, or trust boundary | Security |

`context-drift` should recommend re-running:

1. `context-distill` when Intent, authority, constraints, or sources changed;
2. `context-instructions` after an accepted distillation change;
3. `context-quality` for every regenerated artifact;
4. `context-ratify` before the changed context is treated as active.

The current ratification becomes stale when a material Intent, constraint, autonomy,
source-authority, or CAFE(S)-relevant change is detected.

## Feedback and Commit Gate

`context-feedback` must validate:

- MCP configuration and instruction server references match;
- generated autonomy rules match distilled autonomy;
- the intent changelog is linked when present;
- a non-failing `context_quality_review` exists;
- `.github/context-ratification.md` exists and covers the current generated
  artifact, proven by a matching fingerprint;
- accepted warnings in ratification match the quality review;
- report counts and file lists match actual artifacts.

Only then may it offer a commit. The ratification file is included in the staged
wizard artifacts.

The report is drafted outside its final path and reaches
`.github/context-report.md` only through:

```bash
python3 <resolved-context_artifacts.py> sanitize \
  --input <temporary-draft> \
  --output .github/context-report.md \
  --mcp-config .mcp.json
```

An unsanitized report must never be written to the repository.

## Failure Semantics

The workflow fails closed:

- missing quality state -> no ratification;
- `fail` or `incomplete` quality status -> no ratification;
- missing explicit approval -> no ratification record;
- stale or missing ratification -> no commit offer;
- credential or sensitive-data finding -> block and redact;
- unknown authority -> preserve the gap and require explicit human treatment;
- dry-run -> describe all gates and artifacts without writing or claiming approval.

No skill may turn a missing source, unknown owner, ambiguous rule, or absent
approval into a success-shaped default.

## Design Principle

CAFE(S) makes the context usable. ISEE makes it legitimate and accountable.

Ape Context must require both:

```text
Operational fitness + institutional standing = ratified agent context
```

Anything less remains a draft.
