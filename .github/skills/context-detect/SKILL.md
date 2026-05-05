---
name: context-detect
description: Scan the current project to detect the development stack, tools, and existing configuration
user-invocable: true
---

Scan the project in the current working directory and report what you find.

## What to scan

0. **Read current instructions**: Analyze the .github/copilot-instructions.md
1. **Package files**: package.json, requirements.txt, go.mod, Cargo.toml, pom.xml, build.gradle
2. **CI/CD**: .github/workflows/, Jenkinsfile, .gitlab-ci.yml, azure-pipelines.yml, .circleci/
3. **Infrastructure**: bicep/terraform/cloudformation files, Dockerfile, docker-compose.yml, kubernetes manifests
4. **Existing MCP config**: Read .mcp.json — list ALL currently configured MCP servers. These are already installed and should be preserved.
5. **Existing Copilot config**: .github/copilot-instructions.md, .github/agents/, .github/skills/, and other relevant files under .github/ , .vscode/
6. **Git history**: check recent commit messages for tool references (JIRA-123, LINEAR-456, ADO-789, etc.)
7. **Cloud indicators**: .azure/, serverless.yml, cdk.json, pulumi files

## Critical: existing MCP servers

Read .mcp.json and list every server that's already configured. These are ALREADY WORKING and must be:
- Preserved in all future phases
- Recognized when matching tools to categories (e.g., "workiq" covers M365/SharePoint/Outlook)
- Not duplicated by installing alternatives

## What to report

Summarize your findings in a clear list:
- Source control platform
- Languages and frameworks detected
- CI/CD system
- Cloud platform (if any)
- Tool references found in git history
- **Already configured MCP servers** (from .mcp.json)
- Existing Copilot configuration
- cli tools & scripts that are relevant in this context

## Persist results

Write the detected stack to the session store so downstream phases can retrieve it:

```sql
INSERT OR REPLACE INTO session_state (key, value) 
VALUES ('detected_stack', '{json summary}');
```

The JSON should include: languages detected, frameworks, CI/CD system, cloud platform, existing MCP servers from `.mcp.json`, and any tool references found in git history.

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-detect';
```
