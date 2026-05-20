---
name: context-configure
description: >-
  CONFIGURATION SKILL. Configure authentication for installed MCP servers by choosing safe credential storage, adding .mcp.json env references, and testing read-only connectivity. USE FOR: set up MCP credentials; fix broken or expired MCP auth; reconnect after token expiry; add env vars to .mcp.json. DO NOT USE FOR: discovering or installing MCP servers, healthcheck-only requests, or writing or committing secrets. REQUIRES: .mcp.json already contains server entries. INVOKES: ask_user for storage choice, file tools for config edits, and read-only checks for connectivity.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

Configure auth only for MCP servers already present in `.mcp.json`.

## Steps
1. Read `.mcp.json`. If missing, report that no installed MCP servers can be configured and stop.
2. Determine which servers need auth from known requirements, existing `env` placeholders, or vendor docs. Skip no-auth servers; if none remain, report that and stop.
3. Explain needed credential names and token-source links when known; otherwise point to vendor docs.
4. Ask with `ask_user` where to store credentials. Default to org policy when present; otherwise prefer shell env vars. If unavailable, ask for another option.
5. Configure references only: export commands, gitignored `.env` placeholders, Key Vault/keychain commands, and `.mcp.json` entries like `"JIRA_TOKEN": "${JIRA_TOKEN}"`.
6. Test one lightweight read-only operation per configured server. On failure, report auth failed, ask whether to retry setup once or leave it for healthcheck, and do not mark it connected.
7. Summarize configured, skipped, and failed servers. Standalone runs stop there. If `context-wizard` invoked this skill and its todo exists, mark it done and continue to `context-healthcheck`.

## Examples
- "Set up Jira MCP auth" -> ask storage, add env refs, test read-only.
- "401 after setup" -> offer one retry or healthcheck handoff.

## Error handling and safety
Never store or echo secrets. Before editing `.env`, confirm `.gitignore` excludes `.env` and `.env.*`; add those ignore rules first if missing.
