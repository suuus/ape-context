---
name: context-feedback
description: >-
  FEEDBACK SKILL. Context-wizard finalizer: report evidence, validate artifacts, and gate issue/commit. USE FOR: final report; consistency checks; reminder/commit offers. DO NOT USE FOR: earlier phases, pushes, unconfirmed issues/commits, or credentials. REQUIRES: healthcheck_results, tagged_doc_sources, distilled_intent, .mcp.json, instructions. INVOKES: file tools, ask_user, confirmed git/GitHub.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

## Inputs
Use `healthcheck_results` server statuses/details, `tagged_doc_sources` categories/platforms/locations/tags, and `distilled_intent` intent/constraints/autonomy. Load from state/fixtures; read `.mcp.json`, instructions, and changelog. Missing/malformed inputs are validation issues.

## Steps
1. Write `.github/context-report.md` (dry-runs draft only): MCP servers, docs, intent/constraints/autonomy, healthcheck, generated files. Redact credentials/env values.
2. Validate in order before follow-up/commit: `.mcp.json`/instructions server parity; autonomy table matches; existing changelog linked; report counts match actuals; listed files exist.
3. If issues exist, list each and include "ask before commit"; fix only confirmed generated sections; do not commit until user confirms fix or proceed.
4. Ask whether to create a follow-up issue. Create only after explicit confirmation; dry-runs describe it instead.
5. Ask whether to commit. After confirmation, stage only wizard files: `.mcp.json`, `.github/copilot-instructions.md`, `.github/context-report.md`, `.github/intent-changelog.md`. Commit message: `chore: configure enterprise context layer via context-wizard`. Never push without explicit permission.
6. Summarize counts, validation status, follow-up/commit choices, and report path.

## Examples
- Mismatch: ask fix before commit.
- Declined/dry-run: skip/describe side effects; create nothing.

## Errors
- Missing `.mcp.json`/partial data: partial report, validation issues; no commit until confirmed.
- Standalone: summarize/stop. Wizard todo may mark `ctx-feedback` done.
