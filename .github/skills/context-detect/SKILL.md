---
name: context-detect
description: >-
  DETECTION SKILL. Read-only scan of languages, frameworks, CI/CD, infra, cloud indicators, existing MCP servers, Copilot config, and tool references. USE FOR: detect project stack; inventory MCP servers; summarize repo tooling; prepare context-wizard discovery. DO NOT USE FOR: installing MCP servers, configuring auth, healthchecking, or editing files. REQUIRES: workspace file access. INVOKES: file search/read tools, git log, and SQL session_state persistence.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

Scan the current workspace without modifying files.

## Steps
1. Read `.github/copilot-instructions.md` if present.
2. Scan package manifests: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`.
3. Scan CI/CD and infra: workflows, Jenkins/GitLab/Azure/CircleCI files, Docker, Kubernetes, Terraform/Bicep/CloudFormation, `.azure/`, serverless, CDK, Pulumi.
4. Read `.mcp.json` if present and list every configured MCP server; these are already installed and must be preserved.
5. Inspect `.github/agents/`, `.github/skills/`, `.vscode/`, and recent git commits for Jira, Linear, ADO, Azure, or security references.
6. Report source control, languages/frameworks, CI/CD, cloud, MCP servers, Copilot config, CLI tools, and conflicts. Missing categories are `none found`.
7. Persist `detected_stack` in `session_state` using this schema:

```json
{"languages":[],"frameworks":[],"ci_cd":[],"cloud":[],"mcp_servers":[],"copilot_config":[],"tool_references":[],"scan_notes":[]}
```

Items include `name`, `source`, and optional `confidence`.

## Errors
Unreadable or malformed files: note them in `scan_notes` and continue. If SQL persistence fails, report it; do not pretend state was saved.

## Safety
Never install, configure, delete, or edit files. If `context-wizard` invoked this skill and todo `ctx-detect` exists, mark it done; standalone runs stop after reporting.
