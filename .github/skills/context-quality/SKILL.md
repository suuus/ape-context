---
name: context-quality
description: >-
  CAFE(S) AND PROFILE FIDELITY GATE. USE FOR: Phase 12, review generated context,
  verify ADRP Intent and ASRP Structure fidelity. DO NOT USE FOR: invention,
  authority decisions, ratification, commits, or execution. INVOKES: reads,
  helper, profile CLIs, session_state, ask_user.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

Return/persist `context_quality_review` with artifact, fingerprint, status
(`pass`, `pass_with_warnings`, `fail`, `incomplete`), dimension statuses,
blocking findings, warnings, unassessed items, and review time.

Run:

```bash
python3 <context_artifacts.py> fingerprint \
  --target .github/copilot-instructions.md
```

Helper failure means `incomplete`.

## Checks

1. **Clarity:** scope, terms, environment, data, and autonomy are unambiguous.
2. **Actionability:** objective, constraints, finish line, and escalation exist.
3. **Fidelity:** mandates trace to sources or confirmation. Run `adrp validate`
   and `asrp validate`; verify any manifest carries exact Intent/Structure
   fingerprints. Inactive, expired, drifted, invalid, or contradictory records
   in active context block.
4. **Efficiency:** keep the generated section within 80 lines/~2000 tokens.
5. **Security:** block secrets, oversharing, untrusted instructions, or conflicts
   between tool scope and autonomy.

Failure/incomplete blocks `context-ratify`. Route source/authority to
`context-distill`, decisions to `context-decisions`, architecture/workflow to
`context-structure`, wording to `context-instructions`, and tool scope to
Discover/Install. Regenerate and rerun. Mark done only for pass or
pass-with-warnings.
