"""
Unified CLI Entry Point for Master Persona Agent.
Commands:
  python run_master_agent.py status
  python run_master_agent.py learn [--transcript-path <path>]
  python run_master_agent.py audit --action "<action description>" [--file <path>]
  python run_master_agent.py advise --error "<error text>"
  python run_master_agent.py graph [--node <node_id>]
  python run_master_agent.py reflections
  python run_master_agent.py export-prompt [--out <file_path>]
  python run_master_agent.py guard-check --workspace <workspace_id_or_uri>
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
MASTER_AGENT_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = MASTER_AGENT_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from Sophron.core.persona_loader import PersonaLoader
    from Sophron.core.transcript_learner import TranscriptLearner
    from Sophron.core.decision_emulator import DecisionEmulator
    from Sophron.core.self_healing_advisor import SelfHealingAdvisor
    from Sophron.core.graph_memory_engine import GraphMemoryEngine
    from Sophron.core.workspace_guard import WorkspaceGuard, CrossWorkspaceContaminationError
    from Sophron.core.antigravity_context_bridge import AntigravityContextBridge
except ImportError:
    from persona_loader import PersonaLoader
    from transcript_learner import TranscriptLearner
    from decision_emulator import DecisionEmulator
    from self_healing_advisor import SelfHealingAdvisor
    from graph_memory_engine import GraphMemoryEngine
    from workspace_guard import WorkspaceGuard, CrossWorkspaceContaminationError
    from antigravity_context_bridge import AntigravityContextBridge



def main():
    parser = argparse.ArgumentParser(description="Master Persona Agent CLI & Cognitive Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Status Command
    subparsers.add_parser("status", help="Show current persona knowledge stats")

    # Learn Command
    learn_parser = subparsers.add_parser("learn", help="Ingest transcript and learn user patterns")
    learn_parser.add_argument("--transcript-path", type=str, default=None, help="Path to transcript.jsonl")

    # Audit Command
    audit_parser = subparsers.add_parser("audit", help="Audit a proposed action against user rules")
    audit_parser.add_argument("--action", type=str, required=True, help="Description of proposed action")
    audit_parser.add_argument("--files", nargs="*", default=[], help="Target files to be modified")
    audit_parser.add_argument("--approved", action="store_true", help="Whether user explicitly approved")
    audit_parser.add_argument("--git", action="store_true", help="Whether action involves git commands")
    audit_parser.add_argument("--pii", action="store_true", help="Whether action hardcodes PII in core")

    # Advise Command
    advise_parser = subparsers.add_parser("advise", help="Get troubleshooting advice in the user's voice")
    advise_parser.add_argument("--error", type=str, required=True, help="Error message or issue description")

    # Graph Command
    graph_parser = subparsers.add_parser("graph", help="Query the Semantic Graph Memory")
    graph_parser.add_argument("--node", type=str, default=None, help="Query specific node by ID")

    # Reflections Command
    subparsers.add_parser("reflections", help="View deep cognitive reflection interaction history")

    # Export Prompt Command
    export_parser = subparsers.add_parser("export-prompt", help="Export token-dense Antigravity system prompt block")
    export_parser.add_argument("--out", type=str, default=None, help="Output file path")

    # Guard Check Command
    guard_parser = subparsers.add_parser("guard-check", help="Verify workspace isolation boundary")
    guard_parser.add_argument("--workspace", type=str, required=True, help="Target workspace ID or URI to test")

    args = parser.parse_args()

    loader = PersonaLoader()

    if args.command == "status" or not args.command:
        summary = loader.get_master_summary()
        graph_engine = GraphMemoryEngine()
        reflections_idx_file = MASTER_AGENT_DIR / "interaction_history" / "reflections_index.json"
        reflections_count = 0
        if reflections_idx_file.exists():
            with open(reflections_idx_file, "r", encoding="utf-8") as f:
                reflections_count = json.load(f).get("total_reflections", 0)

        print("\n=======================================================")
        print("     MASTER COGNITIVE REPOSITORY: STATUS REPORT        ")
        print("=======================================================")
        print(f"Total Knowledge Cards Ingested : {summary['total_cards']}")
        print(f"Graph Memory Nodes Indexed    : {len(graph_engine.nodes)}")
        print(f"Graph Memory Semantic Edges   : {len(graph_engine.edges)}")
        print(f"Deep Cognitive Reflections    : {reflections_count} turns analyzed")
        print(f"Active Universal Rules        : {summary['active_rules_count']}")
        print(f"Cross-Workspace Isolation     : STRICT_CONTAINMENT ACTIVE")
        print("=======================================================\n")

    elif args.command == "learn":
        t_path = args.transcript_path
        if not t_path:
            cfg_path = MASTER_AGENT_DIR / "master_agent_config.json"
            if cfg_path.exists():
                try:
                    with open(cfg_path, "r", encoding="utf-8") as f:
                        cfg = json.load(f)
                        cfg_t = cfg.get("paths", {}).get("transcript_path")
                        if cfg_t and Path(cfg_t).exists():
                            t_path = Path(cfg_t)
                except Exception:
                    pass
        if not t_path:
            candidate_logs = list(Path(r"C:\Users\7303150607\.gemini\antigravity\brain").glob("*/.system_generated/logs/transcript.jsonl"))
            if candidate_logs:
                t_path = candidate_logs[-1]

        learner = TranscriptLearner(transcript_path=t_path)
        turns = learner.extract_user_turns()
        print(f"[MasterLearner] Ingested {len(turns)} user turns from transcript.")
        analysis = learner.analyze_patterns(turns)
        out_card = learner.persist_learning_session("current_session", analysis)
        print(f"[MasterLearner] Saved incremental learning card: {out_card}")
        print(f"  - Total Prompts Analyzed: {analysis['total_user_prompts']}")
        print(f"  - Tools Dispatched      : {analysis['tool_dispatch_frequency']}")

    elif args.command == "audit":
        emulator = DecisionEmulator(loader=loader)
        res = emulator.evaluate_action(
            action_description=args.action,
            target_files=args.files,
            is_pre_approved_by_user=args.approved,
            involves_git=args.git,
            involves_candidate_pii_in_core=args.pii
        )
        print("\n=======================================================")
        print(f"          DECISION EMULATION: {res['status']}          ")
        print("=======================================================")
        print(f"Rationale: {res['user_voice_rationale']}")
        if res["violations"]:
            print("\nViolations Detected:")
            for v in res["violations"]:
                print(f"  - {v}")
        if res["recommendations"]:
            print("\nActionable Directives:")
            for r in res["recommendations"]:
                print(f"  - {r}")
        print("=======================================================\n")

    elif args.command == "advise":
        advisor = SelfHealingAdvisor(loader=loader)
        res = advisor.diagnose_error(args.error)
        print("\n=======================================================")
        print("          SELF-HEALING ADVICE (USER VOICE)             ")
        print("=======================================================")
        print(f"Issue: {res['error_summary']}")
        print("\nDirectives:")
        print(res['advisory_directive'])
        print(f"\nTools Recommended: {', '.join(res['tools_to_invoke'])}")
        print(f"\nSimulated User Prompt:\n  \"{res['simulated_user_prompt']}\"")
        print("=======================================================\n")

    elif args.command == "graph":
        engine = GraphMemoryEngine()
        if args.node:
            node = engine.nodes.get(args.node)
            if not node:
                print(f"Node '{args.node}' not found.")
                return
            print(f"\n[Graph Node] {node['id']} ({node['type']}): {node['name']}")
            rel = engine.get_related_nodes(args.node)
            print(f"Connected Outgoing Nodes ({len(rel)}):")
            for r in rel:
                print(f"  --[{r['relation']}]--> {r['node']['id']}: {r['node']['name']}")
        else:
            print(f"\nGraph Memory: {len(engine.nodes)} Nodes, {len(engine.edges)} Directed Edges.")
            for n in list(engine.nodes.values())[:10]:
                print(f"  * [{n.get('type', 'Node')}] {n['id']}: {n['name']}")
            print("  ... (use --node <node_id> to inspect connections)")

    elif args.command == "reflections":
        reflections_dir = MASTER_AGENT_DIR / "interaction_history"
        idx_file = reflections_dir / "reflections_index.json"
        if not idx_file.exists():
            print("No reflections index found.")
            return
        with open(idx_file, "r", encoding="utf-8") as f:
            idx = json.load(f)
        print("\n=======================================================")
        print("       DEEP COGNITIVE REFLECTION: INTERACTION LOG      ")
        print("=======================================================")
        print(f"Total Analyzed Turns: {idx['total_reflections']}\n")
        for f in sorted(reflections_dir.glob("turn_*.json")):
            with open(f, "r", encoding="utf-8") as rfile:
                card = json.load(rfile)
                print(f"[{card.get('turn_id', 'TURN')}] Step {card.get('step_index', 0)}:")
                print(f"  User Intent: {card.get('user_intent', '')[:100]}...")
                print(f"  Why User Thought This Way: {card.get('why_user_made_such_thinking', '')[:100]}...")
                print(f"  AI Understanding Audit  : {card.get('did_ai_actually_understand', '')[:100]}...\n")
        print("=======================================================\n")

    elif args.command == "export-prompt":
        bridge = AntigravityContextBridge(current_workspace_uri="file:///f:/JOB%20AI%20AGENT")
        out_file = Path(args.out) if args.out else MASTER_AGENT_DIR / "SYSTEM_PROMPT_INJECTION.md"
        written = bridge.write_prompt_file(out_file)
        print(f"[ContextBridge] Successfully exported prompt injection to: {written}")

    elif args.command == "guard-check":
        guard = WorkspaceGuard(current_workspace_uri=args.workspace)
        print(f"[WorkspaceGuard] Testing isolation for session URI: '{args.workspace}'")
        
        # Test 1: Tier 1 memory access (Must always succeed)
        tier1_mem = {"id": "test_t1", "tier": "TIER_1_UNIVERSAL", "name": "Empirical Verification"}
        t1_allowed = guard.filter_memory_access(tier1_mem)
        print(f"  - Tier 1 Universal Memory Access: {'ALLOWED' if t1_allowed else 'DENIED'}")

        # Test 2: Matching workspace memory (Must succeed)
        t2_match = {"id": "test_t2", "tier": "TIER_2_WORKSPACE_SPECIFIC", "workspace_slug": "universal_autonomous_career_agent"}
        t2_match_allowed = guard.filter_memory_access(t2_match, target_workspace_id="universal_autonomous_career_agent")
        print(f"  - Matching Workspace Memory Access: {'ALLOWED' if t2_match_allowed else 'DENIED'}")

        # Test 3: Foreign workspace memory (Must raise CrossWorkspaceContaminationError)
        t2_foreign = {"id": "test_foreign", "tier": "TIER_2_WORKSPACE_SPECIFIC", "workspace_slug": "unrelated_ecommerce_app"}
        try:
            guard.filter_memory_access(t2_foreign, target_workspace_id="unrelated_ecommerce_app")
            print("  - Foreign Workspace Memory Access: ERROR (Contamination allowed!)")
        except CrossWorkspaceContaminationError:
            print("  - Foreign Workspace Memory Access: BLOCKED (Strict cross-workspace isolation verified!)")


if __name__ == "__main__":
    main()
