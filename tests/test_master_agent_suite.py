"""
Comprehensive Verification Test Suite for Master Persona Agent.
Validates:
1. PersonaLoader: Card indexing, category counts, card integrity.
2. TranscriptLearner: Extraction from live transcript.jsonl.
3. DecisionEmulator: 5 core session rules + multi-attribute duplicate arbitration.
4. SelfHealingAdvisor: Error diagnosis, tooling directives, simulated user voice.
5. System Audit Report generation in master_agent/output/audits/.
"""

import sys
import json
import unittest
from pathlib import Path
from datetime import datetime

# Setup project root
TEST_DIR = Path(__file__).resolve().parent
MASTER_DIR = TEST_DIR.parent
PROJECT_ROOT = MASTER_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from master_agent.core.persona_loader import PersonaLoader
from master_agent.core.transcript_learner import TranscriptLearner
from master_agent.core.decision_emulator import DecisionEmulator
from master_agent.core.self_healing_advisor import SelfHealingAdvisor


class TestMasterPersonaAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = PersonaLoader()
        cls.learner = TranscriptLearner()
        cls.emulator = DecisionEmulator(loader=cls.loader)
        cls.advisor = SelfHealingAdvisor(loader=cls.loader)
        cls.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "details": []
        }

    def record_test(self, name: str, passed: bool, notes: str = ""):
        self.audit_results["tests_run"] += 1
        if passed:
            self.audit_results["tests_passed"] += 1
        self.audit_results["details"].append({
            "test_name": name,
            "passed": passed,
            "notes": notes
        })

    def test_01_persona_loader_card_counts(self):
        """Verify that PersonaLoader loads all categories and cards."""
        summary = self.loader.get_master_summary()
        self.assertGreaterEqual(summary["total_cards"], 20, "Should load at least 20 cards")
        self.assertIn("session_rules", summary["categories"])
        self.assertIn("thinking_patterns", summary["categories"])
        self.assertIn("instruction_styles", summary["categories"])
        self.assertIn("debugging_protocols", summary["categories"])
        self.assertIn("goals_and_vision", summary["categories"])
        self.assertIn("profile_preferences", summary["categories"])
        
        # Verify individual card lookup
        card = self.loader.get_card("TP-001")
        self.assertIsNotNone(card)
        self.assertEqual(card["title"], "Zero Assumptions & Empirical Fact-Based Validation")
        self.record_test("test_01_persona_loader_card_counts", True, f"Loaded {summary['total_cards']} cards across {len(summary['categories'])} categories")

    def test_02_transcript_learning_engine(self):
        """Verify TranscriptLearner parses live session transcript."""
        cfg_path = MASTER_DIR / "master_agent_config.json"
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        t_path = Path(cfg["paths"]["transcript_path"])
        
        turns = self.learner.extract_user_turns(t_path)
        self.assertGreaterEqual(len(turns), 1, "Should extract at least one user turn")
        analysis = self.learner.analyze_patterns(turns)
        self.assertIn("tool_dispatch_frequency", analysis)
        self.assertIn("total_user_prompts", analysis)
        
        # Persist test card
        out_card = self.learner.persist_learning_session("test_verification", analysis)
        self.assertTrue(out_card.exists())
        self.record_test("test_02_transcript_learning_engine", True, f"Parsed {len(turns)} turns and saved {out_card.name}")

    def test_03_decision_emulator_rejections(self):
        """Verify DecisionEmulator catches and rejects rule violations."""
        # Unapproved python edit -> Rejected
        res1 = self.emulator.evaluate_action(
            action_description="Edit 04_job_discovery.py directly",
            target_files=["core/04_job_discovery.py"],
            is_pre_approved_by_user=False
        )
        self.assertEqual(res1["status"], "REJECTED")
        self.assertTrue(any("SR-001" in v for v in res1["violations"]))

        # Git command -> Rejected
        res2 = self.emulator.evaluate_action(
            action_description="Execute git commit -m 'save changes'",
            involves_git=True
        )
        self.assertEqual(res2["status"], "REJECTED")
        self.assertTrue(any("SR-004" in v for v in res2["violations"]))

        # Hardcoded PII in core -> Rejected
        res3 = self.emulator.evaluate_action(
            action_description="Add candidate phone number to 05_apply_jobs.py",
            involves_candidate_pii_in_core=True
        )
        self.assertEqual(res3["status"], "REJECTED")
        self.assertTrue(any("SR-002" in v for v in res3["violations"]))

        # Window scroll during modal -> Rejected
        res4 = self.emulator.evaluate_action(
            action_description="Execute window.scrollTo(0, 500) while chatbot drawer is open",
            involves_global_window_scroll_in_modal=True
        )
        self.assertEqual(res4["status"], "REJECTED")
        self.assertTrue(any("SR-005" in v for v in res4["violations"]))

        self.record_test("test_03_decision_emulator_rejections", True, "All 4 violation types correctly rejected")

    def test_04_decision_emulator_approvals(self):
        """Verify DecisionEmulator approves compliant actions."""
        res = self.emulator.evaluate_action(
            action_description="Generate detailed walkthrough artifact after empirical CDP test",
            target_files=["docs/walkthrough.md"],
            is_empirically_verified=True,
            is_pre_approved_by_user=True
        )
        self.assertEqual(res["status"], "APPROVED")
        self.assertEqual(len(res["violations"]), 0)
        self.record_test("test_04_decision_emulator_approvals", True, "Compliant pre-approved action approved")

    def test_05_nuanced_duplicate_arbitration(self):
        """Verify multi-stint tenure duplicate logic."""
        # Case A: Same company, same title, different years -> NOT a duplicate
        res_diff = self.emulator.evaluate_duplicate_tenure(
            "Acme Corp", "Backend Engineer", (2021, 2022),
            "Acme Corp", "Backend Engineer", (2023, 2024)
        )
        self.assertFalse(res_diff["is_duplicate"])
        self.assertEqual(res_diff["action"], "ADD_NEW / PRESERVE_BOTH")

        # Case B: Same company, same title, same years -> DUPLICATE
        res_same = self.emulator.evaluate_duplicate_tenure(
            "Acme Corp", "Backend Engineer", (2023, 2024),
            "Acme Corp", "Backend Engineer", (2023, 2024)
        )
        self.assertTrue(res_same["is_duplicate"])
        self.assertEqual(res_same["action"], "SKIP / DEDUPLICATE")

        self.record_test("test_05_nuanced_duplicate_arbitration", True, "Multi-stint duplicate logic verified")

    def test_06_self_healing_advisor(self):
        """Verify SelfHealingAdvisor generates correct directives in user voice."""
        res_scroll = self.advisor.diagnose_error("Background page is getting scrolled behind the modal")
        self.assertIn("/chrome-devtools", res_scroll["tools_to_invoke"])
        self.assertIn("modal", res_scroll["advisory_directive"].lower())

        res_purity = self.advisor.diagnose_error("Guardrail P1 violation: hardcoded phone found")
        self.assertIn("Guardrail P1 Violation", res_purity["advisory_directive"])

        self.record_test("test_06_self_healing_advisor", True, "SelfHealingAdvisor diagnosed scroll and purity errors")

    def test_07_workspace_guard_isolation(self):
        """Verify WorkspaceGuard strictly blocks cross-workspace memory bleeding."""
        from master_agent.core.workspace_guard import WorkspaceGuard, CrossWorkspaceContaminationError
        guard = WorkspaceGuard(current_workspace_uri="file:///f:/JOB%20AI%20AGENT")

        # Tier 1 global memory: Allowed
        t1_allowed = guard.filter_memory_access({"id": "m1", "tier": "TIER_1_UNIVERSAL"})
        self.assertTrue(t1_allowed)

        # Matching Tier 2 memory: Allowed
        t2_match = guard.filter_memory_access({"id": "m2", "tier": "TIER_2_WORKSPACE_SPECIFIC", "workspace_slug": "universal_autonomous_career_agent"})
        self.assertTrue(t2_match)

        # Foreign Tier 2 memory: Must raise CrossWorkspaceContaminationError
        t2_foreign = {"id": "m3", "tier": "TIER_2_WORKSPACE_SPECIFIC", "workspace_slug": "unrelated_banking_app"}
        with self.assertRaises(CrossWorkspaceContaminationError):
            guard.filter_memory_access(t2_foreign)

        self.record_test("test_07_workspace_guard_isolation", True, "Strict two-tier workspace isolation confirmed")

    def test_08_semantic_graph_memory(self):
        """Verify Semantic Graph Memory traversal and node relations."""
        from master_agent.core.graph_memory_engine import GraphMemoryEngine
        engine = GraphMemoryEngine()
        self.assertGreaterEqual(len(engine.nodes), 15)
        self.assertGreaterEqual(len(engine.edges), 10)

        # Query outgoing edges from node_zero_assumptions
        related = engine.get_related_nodes("node_zero_assumptions")
        self.assertGreaterEqual(len(related), 1)
        relations = [r["relation"] for r in related]
        self.assertIn("MANDATES", relations)

        self.record_test("test_08_semantic_graph_memory", True, f"Graph traversed: {len(engine.nodes)} nodes, {len(engine.edges)} edges")

    def test_09_context_bridge_prompt_export(self):
        """Verify AntigravityContextBridge generates token-dense system prompt."""
        from master_agent.core.antigravity_context_bridge import AntigravityContextBridge
        bridge = AntigravityContextBridge(current_workspace_uri="file:///f:/JOB%20AI%20AGENT")
        prompt = bridge.compile_system_prompt_injection()
        self.assertIn("USER COGNITIVE OPERATING SYSTEM", prompt)
        self.assertIn("Zero Assumptions", prompt)
        self.assertIn("Strict Workspace Isolation", prompt)

        self.record_test("test_09_context_bridge_prompt_export", True, f"Prompt compiled successfully ({len(prompt)} chars)")

    @classmethod
    def tearDownClass(cls):
        audit_dir = MASTER_DIR / "output" / "audits"
        audit_dir.mkdir(parents=True, exist_ok=True)
        report_path = audit_dir / "system_audit_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(cls.audit_results, f, indent=2, ensure_ascii=False)
        print(f"\n[TestMasterPersonaAgent] Successfully generated audit report: {report_path}")
        print(f"Total Tests Run: {cls.audit_results['tests_run']} | Passed: {cls.audit_results['tests_passed']}")


if __name__ == "__main__":
    unittest.main()
