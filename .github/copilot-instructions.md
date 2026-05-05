# Copilot Instructions

## Enterprise Context

This project uses **GitHub** for source control, **Jira** for project management, **Azure** as the cloud platform, and **Microsoft 365** (SharePoint, Teams, Outlook) for documentation and communication. CI/CD runs on **GitHub Actions**. Security scanning uses **GitHub Advanced Security** (Dependabot, CodeQL).

---

### MCP Servers

#### GitHub (`github-mcp-server`) 🐙
- **Covers**: Repositories, pull requests, issues, code search, Actions workflows, security alerts
- **Key tools**: `github-mcp-server-search_code`, `github-mcp-server-list_issues`, `github-mcp-server-list_pull_requests`, `github-mcp-server-pull_request_read`, `github-mcp-server-actions_list`, `github-mcp-server-get_job_logs`
- **When to use**: For any GitHub operation — searching code, reading PRs, checking CI status, browsing issues. Prefer these tools over `gh` CLI commands.

#### Jira (`atlassian-jira`) 👥
- **Covers**: Jira projects, issues, sprints, JQL search, dev info (commits, PRs linked to issues)
- **When to use**: When the user mentions Jira tickets, sprint planning, issue tracking, or project management. Use JQL for complex queries.
- **Conventions**: Always reference issues with the full project key (e.g., `PROJ-123`).

#### M365 Read — WorkIQ (`workiq`) 🐙
- **Covers**: SharePoint search, Outlook email queries, OneDrive files, Teams messages, Calendar — **read-only**
- **Key tool**: `workiq-ask_work_iq` — ask natural-language questions about M365 data
- **When to use**: When the user asks about emails, meetings, SharePoint documents, Teams messages, or calendar events. This is the primary tool for finding information across Microsoft 365.

#### M365 Write (`microsoft-365`) 👥
- **Covers**: SharePoint page creation/editing, sending emails, creating calendar events, managing files, contacts, groups
- **When to use**: When the user needs to **create, edit, or send** content in M365 (e.g., "create a SharePoint page", "send an email", "schedule a meeting"). For **read/search** operations, prefer `workiq` instead.

#### Azure (Built-in Skills)
- Azure is covered by built-in skills rather than a separate MCP server.
- Use `azure-deploy` for deployments, `azure-diagnostics` for troubleshooting, `azure-prepare` for new apps.
- Use `appinsights-instrumentation` for Application Insights SDK guidance.
- For resource queries use `azure-resource-lookup`, for cost use `azure-cost-optimization`.

---

### Documentation Sources

| Category | Platform | Location |
|---|---|---|
| **Engineering docs** | SharePoint | `engineering` site — search via `workiq` |
| **Security & compliance** | Backstage | Backstage service catalog |
| **API specifications** | Repo | OpenAPI files in the repository |
| **Runbooks & incidents** | Repo | `docs/runbooks/` directory |
| **Architecture decisions** | SharePoint | Search via `workiq` |
| **Product docs (PRDs, BRDs)** | SharePoint / OneDrive | Search via `workiq` |

When asked "how do we do X" or "where is the doc for Y":
1. Search SharePoint first using `workiq-ask_work_iq`
2. Check repo `docs/` directory for runbooks and API specs
3. Check Backstage for security policies and service catalog

---

### Cross-Tool Workflows

#### Bug Triage
1. Find the Jira ticket with the bug report (`atlassian-jira`)
2. Check Azure Monitor / App Insights for error details (`azure-diagnostics`)
3. Search codebase for the relevant code (`github-mcp-server-search_code`)
4. Create a fix branch, open a PR (`github-mcp-server`)
5. Link the PR back to the Jira issue

#### Deployment
1. PR is merged on GitHub → GitHub Actions CI/CD runs (`github-mcp-server-actions_list`)
2. Deploy to Azure (`azure-deploy` skill)
3. Verify in Azure Monitor (`azure-diagnostics` skill)
4. Update Jira ticket status

#### Security Remediation
1. GitHub Advanced Security flags a vulnerability (Dependabot / CodeQL)
2. Create or link a Jira issue for tracking
3. Fix in code, open PR with security review
4. Verify the alert is resolved after merge

#### Documentation Updates
1. After a code change, check if docs need updating
2. For API changes: update OpenAPI spec in repo
3. For architecture changes: update SharePoint docs via `microsoft-365`
4. For runbook changes: update `docs/runbooks/` in repo

---

### Skills & Agents

- **`context-wizard`** agent — reconfigure this setup, add new MCP servers, update instructions
- **Azure skills** — `azure-deploy`, `azure-diagnostics`, `azure-prepare`, `azure-validate`, `azure-cost-optimization`, `azure-resource-lookup`, `azure-rbac`, `appinsights-instrumentation`
- **`workiq`** skill — query Microsoft 365 data with natural language
