# Contributing to Ape Context

Thanks for your interest in contributing! Ape Context is primarily a Markdown
Copilot plugin, with a Python standard-library helper for deterministic context
artifact handling and explicit dependencies on the ADRP, ASRP, and AERP CLIs.

## How to Contribute

### Reporting Issues

- Use the **Bug Report** or **Feature Request** issue templates
- For security vulnerabilities, see [SECURITY.md](SECURITY.md)

### Suggesting Changes

1. **Fork** the repository
2. **Create a branch** from `main` (`git checkout -b feature/my-improvement`)
3. **Make your changes** — see guidelines below
4. **Test** — run helper unit tests plus the relevant Waza skill/wizard evaluations
5. **Submit a PR** using the pull request template

### What You Can Contribute

| Area | Where | Examples |
|------|-------|---------|
| **New MCP server support** | `context-discover/SKILL.md` | Add vendor-specific servers to the discovery chain |
| **New doc categories** | `context-docs/SKILL.md` | Add categories that match your org's knowledge structure |
| **Bug fixes in skills** | `.github/skills/*/SKILL.md` | Fix incorrect guidance, broken references, edge cases |
| **Wizard improvements** | `.github/agents/context-wizard.agent.md` | Phase ordering, state management, UX improvements |
| **Documentation** | `README.md`, skill files | Clarify instructions, add examples, fix typos |
| **Artifact safety** | `.github/scripts/context_artifacts.py` | Merge preservation, fingerprints, redaction |
| **Profile integration** | `context-decisions`, `context-structure`, `context-feedback` | ADRP Intent, ASRP Structure, and AERP Evidence orchestration |

### Guidelines

- **Keep skills self-contained** — each skill should work standalone with graceful degradation
- **Use `ask_user` for decisions** — never assume; always confirm with the user
- **Preserve existing behavior** — don't break the wizard flow when editing individual skills
- **Follow the ISEE framework** — map changes to Intent, Structure, Execution, or Evidence
- **No credentials in code** — never store secrets directly; only configure where they go
- **Test your changes** — invoke the skill or run the wizard to verify
- **Keep artifact operations deterministic** — use `context_artifacts.py` for
  context merge, fingerprint, and sanitization; use the published ADRP, ASRP,
  and AERP CLIs for profile operations
- **Do not fork profile ownership** — no copied ADRP/ASRP/AERP schemas or
  prompt-only fingerprint, lifecycle, manifest, or Evidence logic
- **Preserve decision boundaries** — drafts are not policy; ratified versions are
  immutable and must remain bound to their approved context fingerprint
- **Preserve imported bytes** — put source URI, ETag, retrieval, and local trust in
  the sidecar; never rewrite an imported canonical record

### Validation

```bash
python3 -m unittest discover -s tests -v
waza --no-update-check check --format json
waza --no-update-check coverage --format json
```

### Skill File Structure

Every skill follows this pattern:

```markdown
---
name: context-{name}
description: {one-line description}
user-invocable: true
---

{Detailed instructions for the agent}

## Process / What to check
{Step-by-step guidance}

## Persist results (if applicable)
{Write output to session_state}

## Error handling (if applicable)
{Explicit failure modes and fallbacks}

## Important
{Guardrails and constraints}

Then mark this phase done:
```sql
UPDATE todos SET status = 'done' WHERE id = 'ctx-{name}';
```
```

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add Terraform MCP server to discovery`
- `fix: correct changelog link path in instructions`
- `docs: clarify standalone invocation behavior`
- `chore: update MCP server coverage table`

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## Questions?

Open a [Discussion](https://github.com/suuus/ape-context/discussions) or file an issue.
