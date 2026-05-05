---
name: context-drift
description: Re-scan the project and compare against current MCP config to detect drift
user-invocable: true
---

Re-scan the project and compare against the current `.mcp.json` and `copilot-instructions.md` to detect configuration drift.

## What to check

### 1. Stack drift
Run the same detection as Phase 1 (Detect):
- Scan package files, CI/CD, infrastructure, cloud indicators
- Compare detected tools against what's configured in `.mcp.json`
- Flag **new tools** not covered by any MCP server: "You added Terraform since last setup — want to add an MCP server for it?"
- Flag **removed tools** still configured: "The Datadog config is still in `.mcp.json` but no Datadog references were found in the project"

### 2. MCP server health
For each server in `.mcp.json`:
- Attempt a lightweight read-only tool call
- Report: `✅ connected` / `⚠️ auth expired` / `❌ unreachable`

### 3. Instruction staleness
- Compare the tools referenced in `copilot-instructions.md` against `.mcp.json`
- Flag instructions that reference servers no longer configured
- Flag configured servers not mentioned in instructions

### 4. Dependency updates
- Check if any configured MCP server packages have newer versions available
- Report: "atlassian-mcp-server: using @latest (current), github-mcp-server: using @latest (current)"

### 5. Intent impact
Assess whether detected changes affect the team's distilled intent, constraints, or autonomy boundaries:
- **Security tools** added or removed (e.g., new scanning tool, removed WAF)
- **Deployment pipeline** changed (e.g., new CI/CD system, changed deploy targets)
- **Cloud platform** changed (e.g., new provider, new services adopted)
- **Monitoring/observability** changed (e.g., switched from Datadog to App Insights)
- **Access control** changed (e.g., new auth provider, changed RBAC model)

If any intent-relevant changes are detected, classify them as `🔴 action-required`.

## Severity classification

Classify each drift item by severity:

| Level | Icon | Meaning | Examples |
|-------|------|---------|----------|
| Info | `ℹ️` | Minor, no action needed | Package version update available |
| Warning | `⚠️` | Should be addressed soon | New tool detected, auth expiring, stale instruction reference |
| Action required | `🔴` | Needs immediate attention | Auth failed, tool removed but still configured, intent-affecting stack changes |

Intent-affecting changes (security tools, deployment pipeline, cloud platform, monitoring, access control) are always `🔴 action-required`.

## Report format

```
🔍 Drift Report
═══════════════

Severity: {N} action-required | {N} warnings | {N} info

🔴 Action required:
  1. Terraform added — no MCP server configured (may affect deployment constraints)
  2. workiq auth expired — M365 doc sources unreachable

⚠️ Warnings:
  3. Redis references found — no MCP server configured
  4. copilot-instructions.md references "datadog-mcp-server" — not in .mcp.json

ℹ️ Info:
  5. atlassian-mcp-server: newer version available

No action needed: 2 servers | Action recommended: 4 items
```

## Actions

After presenting the report, offer to fix each issue in severity order (action-required first):
- For new tools: run the relevant wizard phases (Discover → Install → Configure)
- For removed tools: remove the entry from `.mcp.json` and update instructions
- For auth issues: re-run Configure for that server
- For instruction drift: re-run the Instructions phase

Use `ask_user` for each recommended action — never auto-fix without confirmation.

### Intent re-distillation

When any `🔴 action-required` item is flagged as intent-affecting, after addressing the immediate fixes, ask:

```
ask_user:
  message: "Some changes may affect your team's distilled intent and constraints. Want to review and update them?"
  requestedSchema:
    properties:
      re_distill:
        type: boolean
        title: "Run /context-distill to review intent"
        description: "Re-analyzes your documentation and session history to update intent statements, constraints, and autonomy boundaries. Changes will be logged in .github/intent-changelog.md."
        default: true
```

If accepted, invoke the `context-distill` skill. The trigger will be recorded as "drift-triggered" in the intent changelog.