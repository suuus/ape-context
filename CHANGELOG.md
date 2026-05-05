# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **Intent changelog** (`.github/intent-changelog.md`) — audit trail tracking every change to distilled intent statements, constraints, and autonomy boundaries with timestamps and triggers
- **Autonomy classifications** — Phase 8 (Distill) classifies agent actions as `PROCEED` / `ALWAYS ASK` / `NEVER`; Phase 9 (Instructions) renders them as a structured table
- **Drift severity classification** — `/context-drift` classifies findings as `ℹ️ info` / `⚠️ warning` / `🔴 action-required` with intent-impact detection
- **Drift → re-distillation loop** — when drift detects intent-affecting changes, suggests re-running Phase 8
- **State persistence** — wizard phases write outputs to `session_state` SQL table so downstream phases and standalone skills can retrieve them reliably
- **Standalone skill fallbacks** — skills check session store for prior phase output and fall back gracefully (inline detection, ask user, or warn)
- **Error handling specifications** — timeout enforcement (10s), partial-pass semantics, consent denial handling, server startup failure guidance
- **Merge algorithm** for `copilot-instructions.md` — create/append/replace logic that preserves user content outside the Enterprise Context section
- **Pre-commit validation** — Phase 10 cross-checks all generated artifacts (instructions ↔ servers, autonomy table, changelog ref, report counts, file existence) before offering to commit
- Contributing guide, Code of Conduct, Security policy, issue/PR templates

## [0.0.1] - 2026-04-29

### Added
- Initial release
- 10-phase wizard aligned to the ISEE framework
- 12 skills: detect, discover, docs, review, install, configure, healthcheck, distill, history, instructions, feedback, drift
- Context wizard orchestrator agent
- MCP server discovery with trust badges (🐙🏢🔰👥)
- Tool scoping (read-only vs read+write)
- Session history analysis with mandatory consent gate
- Copilot instructions generation with enterprise context
- Setup report and follow-up scheduling
