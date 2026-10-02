---
name: context-feedback
description: >-
  AERP FINALIZER. USE FOR: Phase 14, close ISEE, sanitize and validate reports.
  DO NOT USE FOR: earlier phases, pushes,
  credentials, unconfirmed effects, or false success. INVOKES: profile CLIs,
  helper, ask_user, confirmed git/GitHub.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

1. Load state; malformed data blocks.
2. Draft `.github/context-report.md` with tools, Intent, Healthcheck, ADRP/ASRP,
   `CAFE(S)`, ratification, and gaps.
   Replace secrets with `[REDACTED]`; never write unsanitized output. Run:

```bash
python3 <context_artifacts.py> sanitize \
  --input <draft> \
  --output .github/context-report.md \
  --mcp-config .mcp.json
```

3. Capture AERP records: healthcheck `observation`, quality
   `assessment`, ratification `approval`, finalization `outcome`. Run `aerp new`,
   bind decisions with `aerp bind`, bind Structure with
   `aerp bind-structure`, then `aerp validate` and `aerp verify`. Store under
   `.github/evidence/context-bootstrap/`; persist `context_evidence`. Preserve
   failed, skipped, and inconclusive results.
4. Validate and name MCP mismatches, changelog, quality, ratification, ADRP
   imports, ASRP duties, AERP bindings/bytes, counts, and paths.
5. List issues; ask before fixes. Route stale gates to their owning phase.
6. Follow-up requires confirmation. Name both paths: `declines: skip` and
   `confirms: create issue`.
7. Confirm commits. Stage only `.mcp.json`,
   `.github/copilot-instructions.md`, `.github/context-report.md`,
   `.github/intent-changelog.md`, `.github/context-ratification.md`, decisions,
   structures, manifest, and Evidence. Use
   `chore: configure enterprise context layer via context-wizard`.
   Decline means `do not commit`. Never push without separate `push permission`.
8. Remove draft; report validation, paths, and bindings.
Always name the persisted Evidence key literally as `context_evidence`.
