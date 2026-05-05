---
name: context-install
description: Write MCP server configurations to .mcp.json
user-invocable: true
---

Install the approved MCP servers by writing their configuration to `.mcp.json` in the **project's root directory** (the current working directory).

## Process

1. Read the existing `.mcp.json` in the working directory if it exists (preserve existing entries)
2. If no `.mcp.json` exists, create one
2. For each approved MCP server from the review phase:
   - Add the entry to the `mcpServers` object
   - Use the standard format — **both `type` and `tools` are required**:
     ```json
     {
       "mcpServers": {
         "server-name": {
           "command": "npx",
           "args": ["-y", "@vendor/mcp-server@latest"],
           "type": "local",
           "tools": ["*"]
         }
       }
     }
     ```
   - Report: ✅ Added {server-name} or ❌ Failed: {reason}
3. Write the updated `.mcp.json` using the edit or create tool
4. Do NOT run npm install — just write the config. The MCP server will be fetched on first use by npx.

## Critical format requirements
- Every entry MUST have `"type": "local"` — without it the SDK won't discover the server
- Every entry MUST have a `"tools"` field — without it no tools are exposed

## Tool scoping

Retrieve scoping decisions from the session store:

```sql
SELECT value FROM session_state WHERE key = 'scoping_decisions';
```

**Fallback chain** if session state is empty:
1. Check conversation context for Phase 2 (Discover) output
2. If neither available, default to `"tools": ["*"]` for all servers and inform the user: "No scoping decisions found from Phase 2 — installing with full access. Run `/context-discover` first to set read-only scoping, or restrict the `tools` list in `.mcp.json` manually."

Apply the retrieved scoping decisions:
- **Read+Write**: `"tools": ["*"]`
- **Read-only**: scope to specific get/search/list tools for that server, using a concrete allowlist. If the exact read-only tool list isn't known for a server, keep `"tools": ["*"]` and inform the user: "Read-only scoping isn't available for {server} yet — installing with full access. You can restrict the tools list manually later."

## Retrieve server list

Also retrieve the full server list from the session store if available:

```sql
SELECT value FROM session_state WHERE key = 'discovered_servers';
```

Fall back to conversation context if not available.

## Important
- Preserve any existing MCP server entries
- Respect the org blocked list — do not add blocked servers
- Use the install command discovered in Phase 2

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-install';
```
