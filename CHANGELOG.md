# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/) and
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-02

### Added

- First-class ISEE adoption workflow spanning discovery, ADRP Intent, ASRP
  Structure, external Execution, and AERP Evidence.
- Fourteen-phase context wizard with a dedicated `context-structure` handoff.
- CAFE(S) quality review and separate human ratification gates.
- Deterministic context merge, fingerprint, and report-sanitization helper.
- AERP Evidence capture for healthcheck observations, quality assessments,
  ratification approvals, and final outcomes.
- Explicit session-state handoffs for Structure drafts, execution manifests,
  and Evidence records.
- Compliance and regulatory source discovery, autonomy classifications, and
  drift severity.
- Source-linked ADRP imports with verbatim snapshots and separate local
  acceptance metadata through the published ADRP CLI.
- Waza skill and agent evaluation coverage plus deterministic dry-run contracts.
- Contribution, security, issue, and pull-request governance.

### Changed

- Ape Context is now positioned as the ISEE context bootstrapper rather than an
  owner of decision or Evidence standards.
- ADRP, ASRP, and AERP profile operations use their published deterministic
  CLIs; copied schemas and the embedded decision helper were removed.
- The recommended installation is the unified `suuus/isee-plugins`
  marketplace.
- Generated instructions include exact ADRP and ASRP references and optional
  execution-manifest gates.
- Drift checks include profile fingerprints, required Evidence, artifact bytes,
  and binding mismatches.

## [0.0.1] - 2026-04-29

### Added

- Initial ten-phase wizard aligned to the ISEE framework.
- MCP discovery and tool scoping.
- Session-history analysis with mandatory consent.
- Enterprise Context generation.
