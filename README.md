# 🧙 Ape Context

> Enterprise context setup wizard for GitHub Copilot

**Ape Context** is a Copilot agent that onboards your project into the AI-assisted development workflow. It scans your codebase, discovers the right MCP servers for your toolchain, configures them, generates Copilot instructions, and sets up authentication — all through a guided, interactive wizard.

Drop the `.github/` folder into any repo and you're ready to go.

## Quick Start

### Option 1: Copy into your repo

```bash
# Clone this repo
git clone https://github.com/suuus/ape-context.git

# Copy the .github folder into your project
cp -r ape-context/.github/ /path/to/your-repo/.github/
```

### Option 2: Use as a Git submodule

```bash
cd your-repo
git submodule add https://github.com/suuus/ape-context.git .ape-context
# Then symlink or copy what you need into .github/
```

### Then just ask Copilot:

```
@context-wizard Set up my project
```

## What It Does

The wizard runs **7 phases** in order, each backed by a dedicated skill:

| # | Phase | Skill | What Happens |
|---|-------|-------|-------------|
| 1 | **Detect** | `context-detect` | Scans package files, CI/CD, infra, `.mcp.json`, git history |
| 2 | **Discover** | `context-discover` | Finds MCP servers via GitHub catalog, org catalog, vendor docs |
| 3 | **Docs** | `context-docs` | Identifies where engineering docs, policies, and runbooks live |
| 4 | **Review** | `context-review` | Presents the full setup plan for your confirmation |
| 5 | **Install** | `context-install` | Writes MCP server configs to `.mcp.json` |
| 6 | **Instructions** | `context-instructions` | Generates `.github/copilot-instructions.md` with enterprise context |
| 7 | **Configure** | `context-configure` | Guides auth setup, tests connections, offers to commit |

## What Gets Created

After a full run:

- **`.mcp.json`** — MCP server configurations (with `"type": "local"` and `"tools": ["*"]`)
- **`.github/copilot-instructions.md`** — Enterprise context with per-tool instructions, cross-tool workflows, and documentation sources

## Progress Tracking

The agent uses the **built-in todo mechanism** (SQL `todos` table) for real-time progress tracking. At startup it creates all 7 todos with dependencies:

```
☐ Phase 1: Detect project stack
☐ Phase 2: Discover MCP servers
☐ Phase 3: Locate team documentation
☐ Phase 4: Review setup plan
☐ Phase 5: Install MCP servers
☐ Phase 6: Generate Copilot instructions
☐ Phase 7: Configure auth & test
```

This works natively in **VS Code**, **GitHub.com**, and **Copilot CLI** — the todo panel shows progress as each phase completes.

## Using Skills Individually

Each skill can be invoked on its own without running the full wizard:

```
/context-detect          # Just scan the project
/context-discover        # Just find MCP servers for your stack
/context-docs            # Just identify documentation sources
/context-install         # Just write .mcp.json
/context-instructions    # Just generate copilot-instructions.md
```

## MCP Server Discovery

The wizard searches for MCP servers in this priority order:

| Source | Badge | Example |
|--------|-------|---------|
| GitHub / Official MCP catalog | 🐙 | `github-mcp-server`, `playwright` |
| Organization catalog (`{org}/.github/mcp-catalog.json`) | 🏢 | Org-approved servers |
| Vendor documentation | 🔰 | Official vendor MCP servers |
| Community | 👥 | Community-built servers |

### Known MCP Server Coverage

| Server | Covers |
|--------|--------|
| `github-mcp-server` | GitHub Issues, PRs, code search, Actions |
| `workiq` | Microsoft 365 (SharePoint, Outlook, OneDrive, Teams) — read-only |
| `playwright` | Browser automation, E2E testing |
| `atlassian-mcp-server` | Jira, Confluence |
| `datadog-mcp-server` | Monitoring, logs, metrics |
| `azure-mcp-server` | Azure resources, deployments |

The wizard automatically detects already-installed servers and won't duplicate them.

## Repository Structure

```
.github/
├── agents/
│   └── context-wizard.agent.md       # Main orchestrator agent
└── skills/
    ├── context-detect/SKILL.md        # Phase 1: Scan project stack
    ├── context-discover/SKILL.md      # Phase 2: Find MCP servers
    ├── context-docs/SKILL.md          # Phase 3: Locate team docs
    ├── context-review/SKILL.md        # Phase 4: Review plan
    ├── context-install/SKILL.md       # Phase 5: Write .mcp.json
    ├── context-instructions/SKILL.md  # Phase 6: Generate instructions
    └── context-configure/SKILL.md     # Phase 7: Auth & test connections
```

## Customization

| What | How |
|------|-----|
| Add tools to discovery | Edit `context-discover/SKILL.md` — add vendor-specific MCP servers |
| Change doc categories | Edit `context-docs/SKILL.md` — match your org's knowledge structure |
| Org catalog | Create `{org}/.github/mcp-catalog.json` with approved/blocked server lists |
| Custom phases | Add a new skill under `.github/skills/` and reference it in the agent |

## Security

- Credentials are **never stored directly** — the wizard only configures where they go (env vars, `.env`, Key Vault, etc.)
- `.env` files are always added to `.gitignore` before writing
- The wizard **never pushes to remote** without explicit user permission
- All tool selections go through user confirmation before installation

## Requirements

- GitHub Copilot with agent/skill support (VS Code, GitHub.com, or Copilot CLI)
- No additional dependencies — the agent and skills are pure markdown prompts

## License

MIT — see [LICENSE](LICENSE)
