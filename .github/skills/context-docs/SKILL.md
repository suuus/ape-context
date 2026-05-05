---
name: context-docs
description: Identify where team documentation, security policies, and knowledge sources live
user-invocable: true
---

Discover where team knowledge, intent, and constraints live. This phase identifies documentation sources and tags them by content type — feeding Phase 8 (Distill) where docs are analyzed to extract actionable intent and guardrails.
Use `ask_user` for each category — one at a time.

## Categories

For each, use `ask_user` with multiple choice + an "Other (specify)" freeform field:

1. **Engineering documentation**: Where do developers find how-to guides, architecture docs, onboarding?
   - Options: Confluence, Notion, GitHub Wiki, repo docs/ folder, SharePoint, Other

2. **Security & compliance policies**: Where are security standards, compliance requirements, audit docs?
   - Options: Dedicated repo, Confluence, SharePoint, Backstage catalog, Other

3. **API specifications**: Where are API contracts and schemas?
   - Options: OpenAPI files in repo, Backstage API catalog, API gateway portal, Confluence, Other

4. **Runbooks & incident procedures**: Where do engineers find operational runbooks?
   - Options: Repo path, Confluence, PagerDuty, Notion, Other

5. **Architecture decisions**: Where are ADRs and design documents?
   - Options: docs/adr/ in repo, Confluence, GitHub Discussions, Other

6. **Product documentation**: Where to find Product and business related documentation, for example: PRD, BRD, BDD, Product strategy
   - Options: Sharepoint/Onedrive, Google Docs, Confluence, repo /docs folder, Other

7. **Processes & ceremonies**: Where are team workflows, ceremonies, and operational processes documented? (sprint rituals, deployment processes, incident response flows, code review policies, escalation paths)
   - Options: Confluence, Notion, GitHub Wiki, repo docs/ folder, SharePoint, Other

For each answer, note:
- The platform (for MCP server matching)
- The specific location (space key, repo path, URL pattern)
- Whether it should be referenced in copilot-instructions.md
- **Content tag** — classify what kind of content lives there:
  - `[intent]` — team priorities, values, strategy, what "done well" looks like
  - `[constraint]` — security policies, compliance rules, approval requirements, deployment rules
  - `[process]` — ceremonies, workflows, decision flows, escalation paths
  - `[reference]` — API specs, onboarding guides, how-to docs

These tags feed Phase 8 (Distill), which uses working MCP connections to analyze the docs and extract actionable intent and constraints.

## Persist results

Write the tagged documentation sources to the session store for Phase 8 (Distill):

```sql
INSERT OR REPLACE INTO session_state (key, value) 
VALUES ('tagged_doc_sources', '{json array}');
```

The JSON should include each source with: category, platform, location, content tag ([intent]/[constraint]/[process]/[reference]), and URL or path where applicable.

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-docs';
```
