# Ape Context

> The ISEE adoption and context bootstrapper for GitHub Copilot

Ape Context turns scattered organizational knowledge into a governed starting
point for humans and agents. It discovers the project and its documentation,
configures approved MCP access, distills sourced Intent and constraints, hands
consequential decisions to ADRP, hands operational Structure to ASRP, generates
Copilot instructions, evaluates context quality with CAFE(S), requires human
ratification, and captures the completed workflow as AERP Evidence.

It is a first-class tool in the open
[ISEE ecosystem](https://agentile.org/projects), but it is not a fifth ISEE
layer and it does not own the three profiles.

```text
Sources and tools
       |
       v
  Ape Context
  discover + distill
       |
       +----> ADRP Intent
       |
       +----> ASRP Structure ----> external Execution
       |
       +<---- AERP Evidence <-------------+
```

## Product boundary

- [ADRP](https://github.com/suuus/adrp) owns durable, human-ratified Intent.
- [ASRP](https://github.com/suuus/asrp) owns Structure and execution manifests.
- Execution stays external: Git-Ape, CI/CD, coding agents, platforms, or humans.
- [AERP](https://github.com/suuus/aerp) owns verifiable Evidence.
- Ape Context discovers, assembles, quality-checks, and ratifies the context
  connecting those layers.
- [ISEE](https://github.com/suuus/isee) performs deterministic preflight,
  Copilot projection, and Evidence evaluation.
- [ISEE Advisor](https://github.com/suuus/isee-advisor) assesses maturity,
  conformance, and drift without executing changes.

Ape Context never copies or silently reimplements ADRP, ASRP, or AERP schemas,
fingerprints, lifecycle rules, manifests, or Evidence verification.

## Installation

The recommended installation is the unified ISEE marketplace:

```bash
copilot plugin marketplace add suuus/isee-plugins
copilot plugin install isee-suite@isee
```

Then select `/agent context-wizard` for repository onboarding or `/agent isee`
for the complete governed workflow.

To install only Ape Context:

```bash
copilot plugin install ape-context@isee
```

The Copilot plugin loads the agent and skills. Deterministic profile operations
require the `adrp`, `asrp`, and `aerp` CLIs. From the complete suite, use
`isee-setup` to install or diagnose them explicitly; plugin installation never
silently modifies the machine.

## The 14-phase workflow

| # | Phase | Skill | ISEE role | Result |
|---|---|---|---|---|
| 1 | Detect | `context-detect` | Structure | Project stack and existing controls |
| 2 | Discover | `context-discover` | Structure | Candidate MCP servers and tool scope |
| 3 | Docs | `context-docs` | Intent | Tagged knowledge and policy sources |
| 4 | Review | `context-review` | Human gate | Approved setup plan |
| 5 | Install | `context-install` | Structure | Approved `.mcp.json` changes |
| 6 | Configure | `context-configure` | Execution | Authentication guidance |
| 7 | Healthcheck | `context-healthcheck` | Evidence | Connection observations |
| 8 | Distill | `context-distill` | Intent | Sourced Intent, constraints, autonomy, and profile candidates |
| 9 | Decisions | `context-decisions` | ADRP | Validated decision drafts and imports |
| 10 | Structure | `context-structure` | ASRP | Validated Structure drafts |
| 11 | Instructions | `context-instructions` | Execution | Generated Enterprise Context |
| 12 | Quality | `context-quality` | Evidence / CAFE(S) | Context and profile-fidelity review |
| 13 | Ratify | `context-ratify` | Human gate | Immutable ADRP/ASRP records and optional execution manifest |
| 14 | Feedback | `context-feedback` | AERP | Bound Evidence, report, follow-up, and commit offer |

The setup-plan approval at Phase 4 is not ratification. Phase 13 approves the
exact assembled context and profile records after the CAFE(S) review.

## What it creates

Depending on the approved workflow:

- `.mcp.json` — approved MCP configuration and tool scoping;
- `.github/copilot-instructions.md` — generated Enterprise Context;
- `.github/intent-changelog.md` — changes to distilled Intent and autonomy;
- `.github/decisions/drafts/*.json` — inactive ADRP drafts;
- `.github/decisions/<id>/vNNN.json` — immutable ratified ADRP records;
- `.github/structures/drafts/*.json` — inactive ASRP drafts;
- `.github/structures/<id>/vNNN.json` — immutable effective ASRP records;
- `.github/isee/execution-manifest.json` — optional external-execution contract;
- `.github/context-ratification.md` — approval of exact context/profile versions;
- `.github/evidence/context-bootstrap/*.json` — AERP observations, assessments,
  approvals, and outcomes;
- `.github/context-report.md` — sanitized final report.

Drafts are never active policy. External decisions are imported byte-for-byte
with separate source metadata and become active only after lifecycle checks and
explicit local acceptance.

## Deterministic boundaries

Ape Context ships `.github/scripts/context_artifacts.py` for operations it owns:

```bash
python3 .github/scripts/context_artifacts.py merge \
  --target .github/copilot-instructions.md \
  --section-file generated-context.md

python3 .github/scripts/context_artifacts.py fingerprint \
  --target .github/copilot-instructions.md

python3 .github/scripts/context_artifacts.py sanitize \
  --input report.draft.md \
  --output .github/context-report.md \
  --mcp-config .mcp.json
```

Profile operations use published commands:

```bash
adrp validate --target decision.json
adrp fingerprint --target decision.json

asrp validate structure.json
asrp bind-intent structure.json decision.json --output structure.bound.json
asrp compile .github/structures \
  --scope "production deployments" \
  --entry-point production-deployment \
  --output .github/isee/execution-manifest.json

aerp validate evidence.json
aerp bind evidence.json decision.json --output evidence.intent.json
aerp bind-structure evidence.intent.json structure.json \
  --output evidence.isee.json
aerp verify evidence.isee.json --artifact-root .
```

A missing or failing helper or profile CLI blocks the dependent phase. The
agent never substitutes a prose-only success.

## ISEE and CAFE(S)

ISEE and CAFE(S) answer different questions:

- **ISEE standing:** Is the context authorized, attributable, scoped,
  reviewable, and connected to exact Intent and Structure?
- **CAFE(S) fitness:** Is the assembled context clear, actionable, faithful,
  efficient, and secure enough for an agent to use?

Both gates must pass. Quality does not create authority, and authority does not
guarantee usable context. See
[CAFE(S) Integration Architecture](docs/CAFE_INTEGRATION.md).

## Standalone skills

Every skill may be invoked independently:

```text
/context-detect
/context-discover
/context-docs
/context-review
/context-install
/context-configure
/context-healthcheck
/context-distill
/context-decisions
/context-structure
/context-instructions
/context-quality
/context-ratify
/context-feedback
/context-history
/context-drift
```

Standalone skills read prior output from the SQL session store. When required
state is missing, they identify the exact prerequisite instead of fabricating a
fallback result.

## Validation

```bash
python3 -m unittest discover -s tests -v
waza --no-update-check check --format json
waza --no-update-check coverage --format json
waza --no-update-check run --discover --strict --no-summary
waza --no-update-check run evals/context-wizard-agent/eval.yaml --no-summary
```

## Documentation

- [Recording Intent with ADRP](docs/RECORDING_INTENT.md)
- [CAFE(S) integration architecture](docs/CAFE_INTEGRATION.md)
- [ISEE framework and toolchain](https://agentile.org/projects)
- [Security policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## Status

Ape Context `0.1.0` is an alpha implementation for governed repository
onboarding and ISEE adoption. It does not itself establish organizational
authority, architecture fitness, regulatory compliance, producer identity, or
permission to execute.

## License

[MIT](LICENSE)
