---
name: context-drift
description: >-
  READ-ONLY DRIFT CHECK. USE FOR: stale tools, changed policy, mismatched ADRP or
  ASRP bindings, missing AERP Evidence, changed artifact bytes. DO NOT USE FOR:
  setup, fixes, execution, or re-ratification. INVOKES: reads, health checks,
  profile CLIs, ask_user.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

1. Load stack, MCP, instructions, ADRP decisions/imports, ASRP Structure,
   execution manifest, ratification, and AERP Evidence. Missing required state is
   drift.
2. Flag uncovered/removed tools, stale references, health/auth failures, and
   instruction bloat above 80 lines or 25% growth.
3. Run `context_artifacts.py fingerprint`; mismatch or material source,
   authority, autonomy, trust, or scope change invalidates ratification.
4. Use ADRP to validate decisions, imports, sidecars, lifecycle, source drift,
   supersession, contradiction, and tampering. Never overwrite imports.
5. Use ASRP to validate Structure and manifest fingerprints. Changed ownership,
   responsibility, interfaces, boundaries, gates, entry points, or Evidence
   duties is action-required.
6. Use AERP to validate required Evidence, exact ADRP/ASRP bindings, and artifact
   bytes. Missing Evidence, mismatch, or unverifiable artifacts is
   action-required.

Return exactly:

```json
{"drift_report":{"action_required":[],"warnings":[],"info":[],"intent_affecting":[]}}
```

Items contain title, source, evidence, severity, and fix. Material changes are
both `action_required` and `intent_affecting`. Clean means all arrays are empty.
Use `ask_user` before any fix. Never edit or claim re-ratification. Route fixes through `context-distill` → Decisions →
Structure → Instructions → Quality → Ratify → Evidence/Feedback.
