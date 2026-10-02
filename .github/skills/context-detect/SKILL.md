---
name: context-detect
description: >-
  READ-ONLY DETECTION. USE FOR: detect project stack, inventory MCP servers,
  summarize repository tooling, prepare wizard discovery. DO NOT USE FOR:
  installation, authentication, healthchecks, or edits. INVOKES: workspace
  search/read, git history, session_state persistence.
license: MIT
metadata:
  version: 0.1.0
  user-invocable: true
---

## Steps
1. Read `.github/copilot-instructions.md` if present.
2. Scan package manifests: `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`.
3. Scan CI/CD and infra: workflows, Jenkins/GitLab/Azure/CircleCI files, Docker, Kubernetes, Terraform/Bicep/CloudFormation, `.azure/`, serverless, CDK, Pulumi.
4. Read `.mcp.json` if present and list every configured MCP server; these are already installed and must be preserved.
5. Inspect agents, skills, editor config, and recent git history for tool references.
6. Report source control, stack, CI/CD, cloud, MCP, Copilot config, CLI tools,
   and conflicts. Missing categories are `none found`.
7. Persist `detected_stack` in `session_state` using this schema:

```json
{"languages":[],"frameworks":[],"ci_cd":[],"cloud":[],"mcp_servers":[],"copilot_config":[],"tool_references":[],"scan_notes":[]}
```

Always name the output and persistence key literally as `detected_stack`, even
when every category is empty or SQL persistence is unavailable.

## Errors
Put unreadable/malformed files in `scan_notes`. Report SQL failure; never claim
state was saved.

## Safety
Never modify files. Wizard mode may mark `ctx-detect` done; standalone stops.
