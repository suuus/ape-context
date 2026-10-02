import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    ROOT
    / "evals"
    / "context-wizard-agent"
    / "graders"
    / "validate_wizard_contract.py"
)
SPEC = importlib.util.spec_from_file_location("wizard_contract", VALIDATOR_PATH)
assert SPEC and SPEC.loader
wizard_contract = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wizard_contract)


def base_contract(scenario):
    return {
        "contract_version": "wizard-dry-run/v1",
        "scenario": scenario,
        "dry_run": True,
        "phase_order": [],
        "state_handoffs": [],
        "gates": [],
        "service_health": [],
        "artifact_actions": [],
        "approvals": {"required": [], "granted": []},
        "side_effects": {"performed": [], "planned": []},
    }


class WizardEvalContractTests(unittest.TestCase):
    def test_parser_accepts_single_json_code_fence(self):
        data = base_contract("phase-order")
        data["phase_order"] = wizard_contract.PHASES
        raw = "```json\n" + __import__("json").dumps(data) + "\n```"
        self.assertEqual(wizard_contract.parse_output(raw), data)

    def test_shape_rejects_alternate_state_keys(self):
        data = base_contract("phase-order")
        data["phase_order"] = wizard_contract.PHASES
        data["state_handoffs"] = [
            {"state_key": "detected_stack", "from_phase": 1, "to_phases": [2]}
        ]
        with self.assertRaisesRegex(ValueError, "state_handoff keys"):
            wizard_contract.validate(data)

    def test_phase_order_accepts_exact_chain(self):
        data = base_contract("phase-order")
        data["phase_order"] = wizard_contract.PHASES
        wizard_contract.validate(data)

    def test_phase_order_rejects_swapped_phases(self):
        data = base_contract("phase-order")
        data["phase_order"] = copy.copy(wizard_contract.PHASES)
        data["phase_order"][9:11] = reversed(data["phase_order"][9:11])
        with self.assertRaisesRegex(ValueError, "phase order"):
            wizard_contract.validate(data)

    def test_dry_run_rejects_performed_side_effect(self):
        data = base_contract("phase-order")
        data["phase_order"] = wizard_contract.PHASES
        data["side_effects"]["performed"] = ["commit"]
        with self.assertRaisesRegex(ValueError, "performed side effects"):
            wizard_contract.validate(data)

    def test_failed_quality_blocks_ratification_and_feedback(self):
        data = base_contract("quality-ratification-gates")
        data["gates"] = [
            {
                "gate": "context-quality",
                "status": "fail",
                "blocks": ["context-ratify", "context-feedback"],
                "recovery": [
                    "context-distill",
                    "context-decisions",
                    "context-structure",
                    "context-instructions",
                ],
            },
            {
                "gate": "context-ratify",
                "status": "blocked",
                "blocks": ["context-feedback"],
                "recovery": [],
            },
        ]
        data["approvals"]["required"] = ["human-ratification"]
        wizard_contract.validate(data)

    def test_final_safety_requires_sanitization(self):
        data = base_contract("final-safety")
        data["gates"] = [
            {
                "gate": "context-quality",
                "status": "pass",
                "blocks": [],
                "recovery": [],
            },
            {
                "gate": "context-ratify",
                "status": "current",
                "blocks": [],
                "recovery": [],
            },
        ]
        data["artifact_actions"] = [
            {
                "artifact": ".github/context-report.md",
                "action": "sanitize",
                "allowed": True,
                "requires_approval": False,
                "sanitized": False,
            },
            {
                "artifact": "git",
                "action": "commit",
                "allowed": True,
                "requires_approval": True,
                "sanitized": True,
            },
            {
                "artifact": "git",
                "action": "push",
                "allowed": True,
                "requires_approval": True,
                "sanitized": True,
            },
        ]
        data["approvals"]["granted"] = ["commit", "push"]
        data["side_effects"]["planned"] = ["commit", "push"]
        with self.assertRaisesRegex(ValueError, "sanitized"):
            wizard_contract.validate(data)


if __name__ == "__main__":
    unittest.main()
