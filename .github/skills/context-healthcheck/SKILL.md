---
name: context-healthcheck
description: >-
  MCP HEALTHCHECK SKILL. Test configured MCP servers with lightweight read-only operations and persist healthcheck_results for downstream phases. USE FOR: verify MCP connectivity; classify auth failures, timeouts, startup errors, and skipped servers; gate distillation. DO NOT USE FOR: auth setup, server discovery, .mcp.json edits, or external writes. REQUIRES: .mcp.json with servers. INVOKES: read-only MCP tools and SQL persistence.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

Test connectivity only; never mutate external systems.

## Steps
1. Dry-run/simulated prompts: answer in prose only; describe any ask, do not call `ask_user`.
2. Read `.mcp.json`. If missing/empty, report no configured servers, emit `healthcheck_results={}`, and stop.
3. For each server, run one lightweight read-only check: GitHub list/search, Jira projects, WorkIQ ask, M365 files, Azure groups, or first safe read tool.
4. Use a 10-second deadline; no automatic retry.
5. Classify: `connected`, `auth_expired`, `auth_failed`, `unreachable`, `timeout`, `failed_to_start`, or `skipped`.
6. On real failure, ask whether to run `context-configure`; if declined, keep failed status.
7. Persist `healthcheck_results` as `{server:{status,detail,blocking?}}`.

## Gate rules
Standalone reports all failures and does not block. Wizard mode blocks only servers required by tagged doc sources for distillation; skipped servers are non-blocking.

## Errors
401/403 -> auth failure. Timeout/unreachable -> connection issue. Startup failure -> command/package/env issue. Unknown server -> try safest read-only tool and report uncertainty.

## Safety
No writes, deletes, large fetches, retries, installs, commits, or pushes.
