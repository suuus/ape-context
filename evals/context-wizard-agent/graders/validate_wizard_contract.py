#!/usr/bin/env python3
"""Validate scenario semantics for the context-wizard dry-run contract."""

from __future__ import annotations

import json
import re
import sys
from typing import Any


PHASES = [
    "context-detect",
    "context-discover",
    "context-docs",
    "context-review",
    "context-install",
    "context-configure",
    "context-healthcheck",
    "context-distill",
    "context-decisions",
    "context-structure",
    "context-instructions",
    "context-quality",
    "context-ratify",
    "context-feedback",
]

TOP_LEVEL_KEYS = {
    "contract_version",
    "scenario",
    "dry_run",
    "phase_order",
    "state_handoffs",
    "gates",
    "service_health",
    "artifact_actions",
    "approvals",
    "side_effects",
}

STATE_CHAIN = {
    "detected_stack": ("context-detect", {"context-discover"}),
    "discovered_servers": ("context-discover", {"context-review", "context-install"}),
    "scoping_decisions": ("context-discover", {"context-install"}),
    "tagged_doc_sources": ("context-docs", {"context-distill"}),
    "healthcheck_results": (
        "context-healthcheck",
        {"context-distill", "context-quality", "context-feedback"},
    ),
    "distilled_intent": (
        "context-distill",
        {
            "context-decisions",
            "context-structure",
            "context-instructions",
            "context-quality",
            "context-ratify",
            "context-feedback",
        },
    ),
    "decision_candidates": ("context-distill", {"context-decisions"}),
    "decision_sources": ("context-distill", {"context-decisions"}),
    "structure_candidates": ("context-distill", {"context-structure"}),
    "decision_drafts": (
        "context-decisions",
        {"context-structure", "context-instructions", "context-quality", "context-ratify"},
    ),
    "imported_decisions": (
        "context-decisions",
        {
            "context-instructions",
            "context-quality",
            "context-ratify",
            "context-feedback",
        },
    ),
    "structure_drafts": (
        "context-structure",
        {"context-instructions", "context-quality", "context-ratify"},
    ),
    "context_quality_review": (
        "context-quality",
        {"context-ratify", "context-feedback"},
    ),
    "decision_records": ("context-ratify", {"context-feedback"}),
    "structure_records": ("context-ratify", {"context-feedback"}),
    "execution_manifest": ("context-ratify", {"context-feedback"}),
    "context_ratification": ("context-ratify", {"context-feedback"}),
    "context_evidence": ("context-feedback", {"context-drift"}),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    require(set(value) == expected, f"{label} keys must be {sorted(expected)}")


def string_list(value: Any, label: str) -> None:
    require(isinstance(value, list), f"{label} must be an array")
    require(all(isinstance(item, str) and item for item in value), f"{label} must contain strings")
    require(len(value) == len(set(value)), f"{label} must not contain duplicates")


def validate_shape(data: dict[str, Any]) -> None:
    exact_keys(data, TOP_LEVEL_KEYS, "top-level")
    require(isinstance(data["contract_version"], str), "contract_version must be a string")
    require(isinstance(data["scenario"], str), "scenario must be a string")
    require(isinstance(data["dry_run"], bool), "dry_run must be a boolean")
    string_list(data["phase_order"], "phase_order")

    require(isinstance(data["state_handoffs"], list), "state_handoffs must be an array")
    for item in data["state_handoffs"]:
        require(isinstance(item, dict), "state_handoffs entries must be objects")
        exact_keys(item, {"key", "writer", "readers"}, "state_handoff")
        require(isinstance(item["key"], str) and item["key"], "state key must be a string")
        require(isinstance(item["writer"], str) and item["writer"], "state writer must be a string")
        string_list(item["readers"], f"{item['key']} readers")

    require(isinstance(data["gates"], list), "gates must be an array")
    valid_gate_statuses = {
        "approved",
        "revise",
        "ready",
        "blocked",
        "pass",
        "pass_with_warnings",
        "fail",
        "incomplete",
        "current",
    }
    for item in data["gates"]:
        require(isinstance(item, dict), "gate entries must be objects")
        exact_keys(item, {"gate", "status", "blocks", "recovery"}, "gate")
        require(isinstance(item["gate"], str) and item["gate"], "gate name must be a string")
        require(item["status"] in valid_gate_statuses, "invalid gate status")
        string_list(item["blocks"], f"{item['gate']} blocks")
        string_list(item["recovery"], f"{item['gate']} recovery")

    require(isinstance(data["service_health"], list), "service_health must be an array")
    for item in data["service_health"]:
        require(isinstance(item, dict), "service_health entries must be objects")
        exact_keys(
            item,
            {"server", "status", "required_for_distill", "classification"},
            "service_health",
        )
        require(isinstance(item["server"], str) and item["server"], "server must be a string")
        require(
            item["status"] in {"connected", "auth_failed", "timeout", "unavailable"},
            "invalid service status",
        )
        require(
            isinstance(item["required_for_distill"], bool),
            "required_for_distill must be a boolean",
        )
        require(
            item["classification"] in {"ready", "blocking", "non_blocking"},
            "invalid service classification",
        )

    require(isinstance(data["artifact_actions"], list), "artifact_actions must be an array")
    for item in data["artifact_actions"]:
        require(isinstance(item, dict), "artifact_actions entries must be objects")
        exact_keys(
            item,
            {"artifact", "action", "allowed", "requires_approval", "sanitized"},
            "artifact_action",
        )
        require(isinstance(item["artifact"], str) and item["artifact"], "artifact must be a string")
        require(
            item["action"] in {"create", "update", "sanitize", "commit", "push", "none"},
            "invalid artifact action",
        )
        require(isinstance(item["allowed"], bool), "allowed must be a boolean")
        require(
            isinstance(item["requires_approval"], bool),
            "requires_approval must be a boolean",
        )
        require(isinstance(item["sanitized"], bool), "sanitized must be a boolean")

    require(isinstance(data["approvals"], dict), "approvals must be an object")
    exact_keys(data["approvals"], {"required", "granted"}, "approvals")
    string_list(data["approvals"]["required"], "approvals.required")
    string_list(data["approvals"]["granted"], "approvals.granted")

    require(isinstance(data["side_effects"], dict), "side_effects must be an object")
    exact_keys(data["side_effects"], {"performed", "planned"}, "side_effects")
    string_list(data["side_effects"]["performed"], "side_effects.performed")
    string_list(data["side_effects"]["planned"], "side_effects.planned")


def ordered_subset(values: list[str], expected: list[str]) -> bool:
    positions = [values.index(value) for value in expected if value in values]
    return len(positions) == len(expected) and positions == sorted(positions)


def gate(data: dict[str, Any], name: str) -> dict[str, Any]:
    matches = [item for item in data["gates"] if item["gate"] == name]
    require(len(matches) == 1, f"expected exactly one {name} gate")
    return matches[0]


def artifact(data: dict[str, Any], path: str, action: str) -> dict[str, Any]:
    matches = [
        item
        for item in data["artifact_actions"]
        if item["artifact"] == path and item["action"] == action
    ]
    require(len(matches) == 1, f"expected exactly one {action} action for {path}")
    return matches[0]


def handoffs(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {item["key"]: item for item in data["state_handoffs"]}
    require(
        len(result) == len(data["state_handoffs"]),
        "state_handoffs contains duplicate keys",
    )
    return result


def require_empty(data: dict[str, Any], *fields: str) -> None:
    for field in fields:
        require(data[field] == [], f"{field} must be empty for {data['scenario']}")


def validate_common(data: dict[str, Any]) -> None:
    require(data["contract_version"] == "wizard-dry-run/v1", "wrong contract version")
    require(data["dry_run"] is True, "dry_run must be true")
    require(data["side_effects"]["performed"] == [], "dry run performed side effects")


def validate_phase_order(data: dict[str, Any]) -> None:
    require(data["phase_order"] == PHASES, "phase order or dependency chain is wrong")
    require_empty(
        data,
        "state_handoffs",
        "gates",
        "service_health",
        "artifact_actions",
    )
    require(data["approvals"] == {"required": [], "granted": []}, "approvals must be empty")
    require(data["side_effects"]["planned"] == [], "planned side effects must be empty")


def validate_review_gate(data: dict[str, Any]) -> None:
    require_empty(data, "phase_order", "state_handoffs", "service_health")
    review = gate(data, "context-review")
    require(review["status"] == "revise", "review must remain in revise state")
    require("context-install" in review["blocks"], "review must block install")
    require("context-review" in review["recovery"], "revision must return to review")
    config = artifact(data, ".mcp.json", "update")
    require(config["allowed"] is False, ".mcp.json update must be blocked")
    require(config["requires_approval"] is True, ".mcp.json update needs approval")
    require(data["approvals"] == {"required": [], "granted": []}, "approvals must be empty")
    require(data["side_effects"]["planned"] == [], "planned side effects must be empty")


def validate_healthcheck(data: dict[str, Any]) -> None:
    require_empty(data, "phase_order", "state_handoffs", "artifact_actions")
    services = {item["server"]: item for item in data["service_health"]}
    require(set(services) == {"workiq", "github-mcp-server", "atlassian-jira"}, "wrong services")
    require(
        services["workiq"] == {
            "server": "workiq",
            "status": "auth_failed",
            "required_for_distill": True,
            "classification": "blocking",
        },
        "workiq must be the blocking required source",
    )
    require(
        services["github-mcp-server"]["status"] == "connected"
        and services["github-mcp-server"]["classification"] == "ready",
        "connected GitHub server must be ready",
    )
    require(
        services["atlassian-jira"]["status"] == "timeout"
        and services["atlassian-jira"]["required_for_distill"] is False
        and services["atlassian-jira"]["classification"] == "non_blocking",
        "optional Jira timeout must be non-blocking",
    )
    health = gate(data, "context-healthcheck")
    require("context-distill" in health["blocks"], "healthcheck must block distill")
    require("context-configure" in health["recovery"], "auth failure must route to configure")
    require(data["approvals"] == {"required": [], "granted": []}, "approvals must be empty")
    require(data["side_effects"]["planned"] == [], "planned side effects must be empty")


def validate_state_handoff(data: dict[str, Any]) -> None:
    require_empty(data, "phase_order", "gates", "service_health", "artifact_actions")
    actual = handoffs(data)
    require(set(actual) == set(STATE_CHAIN), "state chain keys are incomplete or unexpected")
    for key, (writer, readers) in STATE_CHAIN.items():
        require(actual[key]["writer"] == writer, f"{key} has the wrong writer")
        require(readers.issubset(set(actual[key]["readers"])), f"{key} is missing readers")
    require(data["approvals"] == {"required": [], "granted": []}, "approvals must be empty")
    require(data["side_effects"]["planned"] == [], "planned side effects must be empty")


def validate_compliance_flow(data: dict[str, Any]) -> None:
    expected = [
        "context-docs",
        "context-distill",
        "context-decisions",
        "context-structure",
        "context-instructions",
        "context-quality",
        "context-ratify",
        "context-feedback",
    ]
    require(ordered_subset(data["phase_order"], expected), "compliance flow is out of order")
    actual = handoffs(data)
    required_keys = {
        "tagged_doc_sources",
        "distilled_intent",
        "decision_candidates",
        "decision_sources",
        "structure_candidates",
        "decision_drafts",
        "imported_decisions",
        "structure_drafts",
        "context_quality_review",
        "decision_records",
        "structure_records",
        "execution_manifest",
        "context_ratification",
        "context_evidence",
    }
    require(required_keys.issubset(actual), "compliance flow is missing durable state")
    quality = gate(data, "context-quality")
    ratify = gate(data, "context-ratify")
    require("context-ratify" in quality["blocks"], "quality must independently gate ratification")
    require("context-feedback" in ratify["blocks"], "ratification must independently gate feedback")
    require_empty(data, "service_health", "artifact_actions")
    require(data["approvals"] == {"required": [], "granted": []}, "approvals must be empty")
    require(data["side_effects"]["planned"] == [], "planned side effects must be empty")


def validate_quality_ratification(data: dict[str, Any]) -> None:
    require_empty(
        data,
        "phase_order",
        "state_handoffs",
        "service_health",
        "artifact_actions",
    )
    quality = gate(data, "context-quality")
    require(quality["status"] == "fail", "quality status must be fail")
    require(
        {"context-ratify", "context-feedback"}.issubset(quality["blocks"]),
        "failed quality must block ratification and feedback",
    )
    require(
        {
            "context-distill",
            "context-decisions",
            "context-structure",
            "context-instructions",
        }.issubset(quality["recovery"]),
        "fidelity failure must route through distill, decisions, structure, and instructions",
    )
    ratify = gate(data, "context-ratify")
    require(ratify["status"] == "blocked", "ratification must remain blocked")
    require(
        data["approvals"] == {"required": ["human-ratification"], "granted": []},
        "only ungranted human-ratification approval is expected",
    )
    require(data["side_effects"]["planned"] == [], "planned side effects must be empty")


def validate_decision_lifecycle(data: dict[str, Any]) -> None:
    expected = [
        "context-distill",
        "context-decisions",
        "context-structure",
        "context-instructions",
        "context-quality",
        "context-ratify",
    ]
    require(data["phase_order"] == expected, "decision lifecycle is out of order")
    actual = handoffs(data)
    require(
        set(actual)
        == {
            "decision_candidates",
            "decision_sources",
            "decision_drafts",
            "imported_decisions",
            "decision_records",
        },
        "decision lifecycle state is incomplete",
    )
    require(actual["decision_candidates"]["writer"] == "context-distill", "wrong candidate writer")
    require(actual["decision_drafts"]["writer"] == "context-decisions", "wrong draft writer")
    require(actual["decision_sources"]["writer"] == "context-distill", "wrong source writer")
    require(actual["imported_decisions"]["writer"] == "context-decisions", "wrong import writer")
    require(actual["decision_records"]["writer"] == "context-ratify", "wrong record writer")
    decisions = gate(data, "context-decisions")
    require(decisions["status"] == "ready", "decision drafts must be ready")
    require(decisions["blocks"] == [], "validated drafts do not block structure")
    ratify = gate(data, "context-ratify")
    require(ratify["status"] == "blocked", "immutable records require ratification")
    require("context-feedback" in ratify["blocks"], "unratified decisions must block feedback")
    draft = artifact(data, ".github/decisions/drafts/ADR-0001.json", "create")
    immutable = artifact(data, ".github/decisions/ADR-0001/v001.json", "create")
    require(draft["allowed"] is False and draft["requires_approval"] is True, "draft needs confirmation")
    require(immutable["allowed"] is False and immutable["requires_approval"] is True, "immutable record needs ratification")
    require(
        data["approvals"]
        == {"required": ["decision-draft", "human-ratification"], "granted": []},
        "decision approvals are wrong",
    )
    require_empty(data, "service_health")
    require(data["side_effects"]["planned"] == [], "planned side effects must be empty")


def validate_final_safety(data: dict[str, Any]) -> None:
    require_empty(data, "phase_order", "state_handoffs", "service_health")
    require(gate(data, "context-quality")["status"] == "pass", "quality must pass")
    require(gate(data, "context-ratify")["status"] == "current", "ratification must be current")
    report = artifact(data, ".github/context-report.md", "sanitize")
    require(report["allowed"] is True and report["sanitized"] is True, "report must be sanitized")
    require(
        set(data["approvals"]["required"]) == {"commit", "push"},
        "commit and push approvals must be required",
    )
    require(
        set(data["approvals"]["granted"]).issubset({"commit", "push"}),
        "unexpected approval was granted",
    )
    require(
        set(data["side_effects"]["planned"]) == {"commit", "push"},
        "only commit and push may be planned",
    )
    require(
        any(item["action"] == "commit" and item["allowed"] for item in data["artifact_actions"]),
        "commit action must be allowed",
    )
    require(
        any(item["action"] == "push" and item["allowed"] for item in data["artifact_actions"]),
        "push action must be allowed",
    )


VALIDATORS = {
    "phase-order": validate_phase_order,
    "review-gate": validate_review_gate,
    "healthcheck-gate": validate_healthcheck,
    "state-handoff": validate_state_handoff,
    "compliance-regulatory-flow": validate_compliance_flow,
    "quality-ratification-gates": validate_quality_ratification,
    "decision-lifecycle": validate_decision_lifecycle,
    "final-safety": validate_final_safety,
}


def parse_output(raw: str) -> dict[str, Any]:
    text = raw.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fenced:
        text = fenced.group(1)
    data = json.loads(text)
    require(isinstance(data, dict), "output must be one JSON object")
    return data


def validate(data: dict[str, Any]) -> None:
    validate_shape(data)
    validate_common(data)
    scenario = data.get("scenario")
    require(scenario in VALIDATORS, f"unknown scenario: {scenario}")
    VALIDATORS[scenario](data)


def main() -> int:
    try:
        data = parse_output(sys.stdin.read())
        validate(data)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"wizard contract invalid: {exc}", file=sys.stderr)
        return 1
    print(f"wizard contract valid for {data['scenario']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
