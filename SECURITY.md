# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Ape Context, please report it responsibly.

**Do NOT open a public issue for security vulnerabilities.**

Instead, please use [GitHub's private vulnerability reporting](https://github.com/suuus/ape-context/security/advisories/new) to submit your report.

You should receive a response within 48 hours. We will work with you to understand the issue and coordinate a fix.

## What Counts as a Security Issue

Ape Context is a Copilot plugin with Markdown agents/skills, one Python
standard-library context-artifact helper, and explicit ADRP, ASRP, and AERP CLI
dependencies for profile operations. Security concerns include:

- **Credential exposure** — any path where the wizard could log, commit, or expose credentials
- **Prompt injection** — skill instructions that could be manipulated to bypass guardrails
- **Unintended data access** — skills accessing data beyond their documented scope
- **Consent bypass** — any way to skip the session history consent gate

## Security Design Principles

This project enforces the following security invariants:

- Credentials are **never stored directly** — only configured where they go (env vars, `.env`, Key Vault)
- `.env` files are always added to `.gitignore` before writing
- The wizard **never pushes to remote** without explicit user permission
- **Session history analysis requires explicit consent** before any queries run
- All tool selections go through **user confirmation** before installation
- MCP server scoping (read-only vs read+write) is surfaced as an explicit decision
- Generated reports pass through deterministic secret sanitization before reaching
  `.github/context-report.md`
- Enterprise Context changes use an atomic merge helper that refuses unapproved
  replacement of manual sections
- ADRP and ASRP records are validated by their published CLIs; immutable
  versions cannot overwrite an existing record or rendering
- Imported decisions preserve exact source bytes and keep retrieval/trust metadata
  in a separate validated sidecar
- External approval never grants local standing automatically; active use requires
  lifecycle eligibility plus explicit local scope and authority acceptance
- Ratification binds canonical ADRP and ASRP fingerprints to the exact generated
  context fingerprint; AERP binds resulting Evidence back to those exact records
- Source provenance, source authority, approver identity, and organisational
  standing remain separate claims

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | ✅        |
| 0.0.x   | Security fixes only |
