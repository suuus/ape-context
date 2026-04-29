---
name: context-configure
description: Guide the user through authentication setup for each MCP server, test connections
user-invocable: true
---

For each installed MCP server that requires authentication, guide the user through credential setup.

## Process

For each server that needs auth:

1. **Explain** what credentials are needed:
   - "The Atlassian MCP server needs your Jira instance URL and an API token"
   - Link to the vendor's token creation page if possible

2. **Ask where to store credentials** (use `ask_user`):
   - Environment variable (recommended for local dev)
   - `.env` file (gitignored, local only)
   - Azure Key Vault (enterprise)
   - System keychain (macOS Keychain / Windows Credential Manager)
   - If an org catalog specifies `credential-storage`, default to that

3. **Guide setup** based on their choice:
   - Env var: tell them which variable name to set and the export command
   - .env: create or update .env file, ensure it's in .gitignore
   - Key Vault: provide az keyvault commands
   - Keychain: provide platform-specific instructions

4. **Update .mcp.json** if the server needs env vars in its config:
   ```json
   "env": {
     "JIRA_URL": "${JIRA_URL}",
     "JIRA_TOKEN": "${JIRA_TOKEN}"
   }
   ```

5. **Test the connection** if possible:
   - Try to invoke a simple read-only tool from the server
   - Report: ✅ Connected or ❌ Auth failed — check credentials

## Important
- We NEVER store credentials directly — only configure where they go
- Never echo or log credential values
- Always ensure .env is in .gitignore before writing to it
- Respect org credential storage policy if one exists

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-configure';
```

When all servers are configured, summarise the auth setup and move to Phase 7 (Healthcheck) — do NOT offer to commit here. Committing happens in Phase 10 (Feedback).
