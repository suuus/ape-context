---
name: context-drift
description: >-
  DRIFT SKILL. Rescan workspace read-only for context drift. Compare stack, .mcp.json, Copilot instructions, MCP health/auth, and dependency notes. USE FOR: new/removed tools, stale instructions, auth failures, and intent-affecting cloud, security, deploy, monitoring, or access-control changes. DO NOT USE FOR: initial setup, install/configure, file edits, or live fixes. REQUIRES: workspace access; .mcp.json/instructions optional. INVOKES: file reads, optional read-only health checks, ask_user for fixes/re-distill.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

## Steps
1. Use persisted `detected_stack` if available; otherwise scan manifests, workflows, infra files, `.mcp.json`, and instructions. Missing/unreadable config is drift, not failure.
2. Compare detected tools to MCP servers: flag new uncovered tools, removed tools still configured, stale instruction references, and configured servers absent from instructions.
3. Check MCP health/auth with read-only calls unless the prompt says dry-run/fixture-only or supplies health facts; then cite fixtures and make no live calls.
4. Note visible dependency/package updates; skip unavailable lookups as `info`.
5. Mark cloud, security, deploy pipeline, monitoring/observability, or access-control changes as intent-affecting.

## Output
```json
{"drift_report":{"action_required":[],"warnings":[],"info":[],"intent_affecting":[]}}
```

Items include `title`, `source`, `evidence`, `severity`, `proposed_fix`. Severities: `info`, `warning`, `action_required`; intent-affecting items are `action_required` and listed in `intent_affecting`. Clean run: all arrays empty.

## Safety
Never edit, install, remove, or configure. For any non-empty report, include `ask_user` fixes in severity order: discover/install, remove stale config, rerun configure, or regenerate instructions. If `intent_affecting` is non-empty, ask about `context-distill`.
