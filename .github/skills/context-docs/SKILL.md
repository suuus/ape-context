---
name: context-docs
description: Identify where team documentation, security policies, and knowledge sources live
user-invocable: true
---

Ask the user where their team's knowledge lives. Use `ask_user` for each category — one at a time.

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

6  **Product documentation**: Where to find Product and business related documentation, for example: PRD, BRD, BDD, Product strategy
   -Options: Sharepoint/Onedrive, Google Docs, Confluence, repo /docs folder, Other

For each answer, note:
- The platform (for MCP server matching)
- The specific location (space key, repo path, URL pattern)
- Whether it should be referenced in copilot-instructions.md

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-docs';
```
