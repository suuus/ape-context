import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProfileBoundaryTests(unittest.TestCase):
    def test_release_versions_match(self):
        plugin = json.loads((ROOT / "plugin.json").read_text())
        marketplace = json.loads(
            (ROOT / ".github" / "plugin" / "marketplace.json").read_text()
        )
        self.assertEqual(plugin["version"], "0.1.0")
        self.assertEqual(marketplace["metadata"]["version"], plugin["version"])
        self.assertEqual(marketplace["plugins"][0]["version"], plugin["version"])

    def test_profile_implementations_are_not_embedded(self):
        self.assertFalse((ROOT / ".github" / "scripts" / "decision_records.py").exists())
        self.assertFalse((ROOT / "schemas" / "ape-decision-record-v1.schema.json").exists())
        self.assertFalse((ROOT / "schemas" / "ape-decision-source-v1.schema.json").exists())

    def test_profile_skills_use_published_clis(self):
        expectations = {
            ".github/skills/context-decisions/SKILL.md": (
                "adrp validate",
                "adrp fingerprint",
                "adrp import",
            ),
            ".github/skills/context-structure/SKILL.md": (
                "asrp validate",
                "asrp fingerprint",
                "asrp bind-intent",
                "asrp compile",
            ),
            ".github/skills/context-feedback/SKILL.md": (
                "aerp bind",
                "aerp bind-structure",
                "aerp validate",
                "aerp verify",
            ),
        }
        for relative, commands in expectations.items():
            text = (ROOT / relative).read_text()
            for command in commands:
                self.assertIn(command, text, f"{relative} must use {command}")

    def test_wizard_contains_closed_loop_state(self):
        text = (ROOT / ".github" / "agents" / "context-wizard.agent.md").read_text()
        for value in (
            "context-structure",
            "structure_candidates",
            "structure_drafts",
            "structure_records",
            "execution_manifest",
            "context_evidence",
        ):
            self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main()
