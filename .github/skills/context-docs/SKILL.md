---
name: context-docs
description: >-
  DOCUMENTATION DISCOVERY SKILL. Identify team docs, policy, compliance/regulatory/audit, API, runbook, architecture, product, and process sources; tag each source for distillation. USE FOR: map docs sources; classify intent/constraint/process/reference material; prepare context-distill. DO NOT USE FOR: reading/analyzing document content, generating instructions, or configuring MCP servers. REQUIRES: user answers or known repo docs. INVOKES: ask_user and SQL persistence.
license: MIT
metadata:
  version: 0.0.1
  user-invocable: true
---

Discover where knowledge lives; do not read or summarize document contents.

## Steps
1. Ask one category at a time: engineering docs, security/compliance/regulatory/audit, API specs, runbooks/incidents, ADRs, product docs, processes/ceremonies.
2. Offer common platforms plus Other: repo path, SharePoint/OneDrive, Confluence, Notion, GitHub Wiki/Discussions, Backstage, API portal, PagerDuty, Google Docs.
3. For each answer capture platform, location/URL/path, whether instructions should reference it, framework/jurisdiction in notes if known, and tag: `[intent]`, `[constraint]`, `[process]`, or `[reference]`.
4. Skip/None is valid; record no source and continue. Other values are accepted with platform=`other` and notes.
5. Persist `tagged_doc_sources` as `[{category,platform,location,tag,url?,notes?}]`.

## Errors and mode
Unavailable platform, missing repo path, or declined answer -> record `notes` and continue. Wizard mode may mark `ctx-docs` done; standalone stops after reporting.

## Safety
Do not fetch private docs, configure tools, or edit repository docs.
