---
name: context-review
description: >-
  REVIEW GATE SKILL. Present the proposed context-wizard setup plan for explicit user approval before installation or file changes. USE FOR: review MCP recommendations; confirm scoping and generated files; approve, revise, or stop setup. DO NOT USE FOR: discovering servers, editing .mcp.json, configuring auth, or generating instructions. REQUIRES: discovered_servers or a plan summary. INVOKES: ask_user only.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

Present a confirmation gate; do not make changes.

## Steps
1. Show planned MCP servers with badge, coverage, scope, auth needs, install command, and whether already installed.
2. Show skills/agents to enable, instruction sections to generate, `.mcp.json` entries, files to create/modify, and org-policy status.
3. Empty states are valid; explicitly say "no recommended MCP servers", "no org catalog", and "no file changes" when true.
4. Ask with `ask_user`: Approve, Revise, or Stop.
5. Approve -> pass the plan forward. Revise -> name the phase to revisit (`context-discover`, `context-docs`, etc.). Stop -> say "do not proceed".

## Output
Return `{decision:"approve|revise|stop", revise_phase?, notes?}`. Wizard mode may mark `ctx-review` done only after Approve; standalone stops after reporting.

## Safety
Never install, configure, edit, commit, or push.
