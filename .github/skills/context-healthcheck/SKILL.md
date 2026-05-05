---
name: context-healthcheck
description: Test all configured MCP server connections and report status
user-invocable: true
---

Test all configured MCP server connections to verify the setup works.

## When this runs

- **During the wizard**: Phase 7, after Configure (Phase 6) sets up auth. All servers must respond before Phase 8 (Distill) uses them to analyze docs.
- **Standalone**: Invoke with `/context-healthcheck` anytime to verify connections.

## Process

1. **Read `.mcp.json`** — get the list of all configured MCP servers
2. **For each server**, attempt a lightweight read-only operation:

   | Server type | Test operation |
   |---|---|
   | GitHub (`github-mcp-server`) | List repositories or search code |
   | Jira (`atlassian-jira`) | List projects |
   | M365 read (`workiq`) | Ask a simple question |
   | M365 write (`microsoft-365`) | List recent files |
   | Azure (`azure-mcp-server`) | List resource groups |
   | Generic | Try the first available read-only tool |

3. **Report results** for each server:
   - `✅ {server-name} — connected` (response received)
   - `⚠️ {server-name} — auth expired` (401/403 response)
   - `❌ {server-name} — unreachable` (timeout or connection error)

4. **Handle failures**:
   - If any server fails, use `ask_user`: "Server {name} failed to connect. Want to re-run auth setup for it?"
   - If yes, invoke the `context-configure` skill for that specific server
   - Re-test after reconfiguration

5. **Gate for Phase 8**: During the wizard flow, only the servers needed by Phase 3 doc sources must pass before Distill can proceed. Other server failures are reported but don't block Phase 8. Servers that the user explicitly skips are excluded from this gate.

## Report format

```
🏥 Healthcheck Report
═════════════════════

✅ github-mcp-server    — connected (listed 5 repos)
✅ atlassian-jira        — connected (listed 3 projects)
⚠️ workiq               — auth token expired
✅ microsoft-365         — connected

Result: 3/4 healthy — 1 needs attention
```

## Persist results

Write healthcheck results to the session store for Phase 8 (Distill) and Phase 10 (Feedback):

```sql
INSERT OR REPLACE INTO session_state (key, value) 
VALUES ('healthcheck_results', '{json map of server_name → {status, detail}}');
```

Example JSON: `{"github-mcp-server": {"status": "connected", "detail": "listed 5 repos"}, "workiq": {"status": "auth_expired", "detail": "401 response"}}`

## Important

- Use only **read-only** operations — never modify data during a healthcheck
- Keep test operations lightweight — don't fetch large datasets
- Timeout after 10 seconds per server — don't block indefinitely
- If running standalone, report results and offer to fix issues but don't force the full wizard flow

## Error handling

### Timeout enforcement
- Set a 10-second deadline per server. If no response within 10 seconds, mark as `❌ {server} — unreachable (timeout)`.
- Do NOT retry automatically — offer retry via `ask_user` instead.

### Partial pass semantics
- **During wizard flow**: only servers needed by Phase 8 doc sources are **blocking**. Other server failures are reported but don't prevent progress. If a blocking server fails, offer re-configure then re-test. If it fails again, ask: "Skip this server and proceed without its doc sources?"
- **Standalone invocation**: all failures are reported; none are blocking.

### Server startup failures
- If a server's MCP process fails to start (e.g., `npx` download fails or command not found), report: `❌ {server} — failed to start (check network/npm access)`
- Suggest: "Try running `npx -y @vendor/package@latest` manually to diagnose."
