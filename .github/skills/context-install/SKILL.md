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

Apply the scoping decisions from Phase 2 (Discover):
- **Read+Write**: `"tools": ["*"]`
- **Read-only**: scope to specific get/search/list tools for that server, using a concrete allowlist. If the exact read-only tool list isn't known for a server, keep `"tools": ["*"]` and inform the user: "Read-only scoping isn't available for {server} yet — installing with full access. You can restrict the tools list manually later."

## Important
- Preserve any existing MCP server entries
- Respect the org blocked list — do not add blocked servers
- Use the install command discovered in Phase 2

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-install';
```
