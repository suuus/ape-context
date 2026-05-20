---
name: context-install
description: >-
  MCP INSTALL CONFIG SKILL. Write approved MCP server entries to .mcp.json from discovered_servers and scoping_decisions while preserving existing config. USE FOR: install approved MCP config; apply read-only/read-write tool scopes; merge server entries. DO NOT USE FOR: discovering servers, auth setup, healthchecks, npm install, or blocked/unresolved servers. REQUIRES: approved discovered_servers. INVOKES: file read/write and SQL session_state reads.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

Write config only; never run packages.

## Inputs
Read `discovered_servers`, `scoping_decisions`, and `unresolved_tools` from session_state or conversation context.

## Steps
1. Read existing `.mcp.json`; create only if absent. Malformed JSON -> report parse error and ask before overwriting.
2. Preserve every existing `mcpServers` entry.
3. Add only approved `recommended` servers; skip `installed`, `blocked`, `needs_confirmation`, and `unresolved_tools`.
4. Every entry must include `type:"local"` and `tools`.
5. Scope from `scoping_decisions`: `read-write` -> `["*"]`; `read-only` -> known get/list/search allowlist, else warn and use discovered scope.
6. Write merged `.mcp.json` and report added, skipped, preserved, and failed servers.

## Errors and mode
No approved server list -> stop and tell user to run `context-discover`/`context-review`. Wizard may mark `ctx-install` done after a successful write.

## Safety
Do not run `npm`, `npx`, auth flows, healthchecks, commits, or pushes.
