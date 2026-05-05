# Contributing to Ape Context

Thanks for your interest in contributing! Ape Context is a pure-markdown Copilot plugin — no runtime code, just agent and skill definitions. This makes contributing accessible to anyone comfortable with markdown and prompt engineering.

## How to Contribute

### Reporting Issues

- Use the **Bug Report** or **Feature Request** issue templates
- For security vulnerabilities, see [SECURITY.md](SECURITY.md)

### Suggesting Changes

1. **Fork** the repository
2. **Create a branch** from `main` (`git checkout -b feature/my-improvement`)
3. **Make your changes** — see guidelines below
4. **Test manually** — run the wizard or invoke the skill you changed to verify it works
5. **Submit a PR** using the pull request template

### What You Can Contribute

| Area | Where | Examples |
|------|-------|---------|
| **New MCP server support** | `context-discover/SKILL.md` | Add vendor-specific servers to the discovery chain |
| **New doc categories** | `context-docs/SKILL.md` | Add categories that match your org's knowledge structure |
| **Bug fixes in skills** | `.github/skills/*/SKILL.md` | Fix incorrect guidance, broken references, edge cases |
| **Wizard improvements** | `.github/agents/context-wizard.agent.md` | Phase ordering, state management, UX improvements |
| **Documentation** | `README.md`, skill files | Clarify instructions, add examples, fix typos |

### Guidelines

- **Keep skills self-contained** — each skill should work standalone with graceful degradation
- **Use `ask_user` for decisions** — never assume; always confirm with the user
- **Preserve existing behavior** — don't break the wizard flow when editing individual skills
- **Follow the ISEE framework** — map changes to Intent, Structure, Execution, or Evidence
- **No credentials in code** — never store secrets directly; only configure where they go
- **Test your changes** — invoke the skill or run the wizard to verify

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
