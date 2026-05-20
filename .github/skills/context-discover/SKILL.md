---
name: context-discover
description: >-
  DISCOVERY SKILL. Recommend MCP servers for detected_stack. Reuse .mcp.json coverage and persist scoped candidates. USE FOR: find MCP servers; map tools; avoid duplicates; prepare context-install. DO NOT USE FOR: stack detection, .mcp.json writes, auth, or healthchecks. REQUIRES: detected_stack or fallback scan. INVOKES: ask_user, file reads, catalog search.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

## Inputs
`detected_stack` comes from `context-detect`. If absent, quick-scan only manifests, workflows, `.mcp.json`, and cloud files.

## Steps
1. Read `.mcp.json` first. Preserve installed servers. Known coverage: GitHub, M365 read (`workiq`), browser, Atlassian, Datadog, Azure. Verify uncertain coverage; never duplicate.
2. Batch-confirm tools with `ask_user`; if headless, use detected defaults and mark `needs_confirmation`.
3. For gaps, search trust order: official/GitHub 🐙, org catalog 🏢, vendor docs 🔰, community 👥. Org catalog supplies approved/blocked lists; prefer approved and exclude blocked.
4. If installed read-only coverage exists but writes are needed, ask whether to add a write-capable server; otherwise reuse it.
5. Scope recommended servers only: `read-write` -> `tools:["*"]`; `read-only` -> known get/list/search allowlist, else note manual restriction.

## Output
Report installed, recommended, and unresolved items. Persist `discovered_servers[]` with `name,badge,scope,category,install_cmd,status`; `scoping_decisions{server:read-only|read-write}`; `unresolved_tools[]`.

## Errors and mode
No org catalog -> use public/vendor sources. Unreachable source -> try next. No match or only blocked servers -> unresolved. SQL failure -> state unsaved. Wizard may mark `ctx-discover` done; standalone only reports.

## Safety
Do not install, configure auth, or edit `.mcp.json`.
