# Understanding Master: Distributed Cognitive Architecture & Graph Memory

An independent, private, distributed cognitive memory repository that captures the **Human Architect's cognitive operating system**, thinking patterns, instruction styles, session rules, and architectural vision.

Engineered with **Dual-Tier Memory Isolation** and **Semantic Graph Memory**, this repository allows any AI assistant in Google Antigravity to understand, think, and execute according to your exacting standards across multiple chats and workspaces—without ever cross-contaminating project-specific memories.

---

## 1. Architectural Highlights

- **Standalone Private Git Ready**: Structured as an independent repository that can be initialized with `git init` and pushed to your own private GitHub repository (`understanding-master`).
- **Strict Cross-Workspace Isolation (Tier 1 vs Tier 2)**:
  - **Tier 1 (Universal Meta-Cognition)**: High-level axioms, empirical proof standards, gatekeeping, and communication styles. Universal across all projects.
  - **Tier 2 (Workspace Episodic Memory)**: Low-level DOM schemas, platform decoupling contracts, and project milestones. Strictly scoped to `workspaces/<workspace_slug>/`. Workspace A facts are cryptographically/URI-blocked from ever bleeding into Workspace B.
- **Deep Cognitive Reflection Engine**: Chronological turn-by-turn analysis explaining *why* the user thought this way, *why* instructions were formatted as such, user satisfaction levels, AI comprehension audits, and permanent evolutionary takeaways.
- **Semantic Graph Memory**: Directed property graph (`nodes.json`, `edges.json`, `graph_index.json`) mapping principles, rules, events, and workspace scopes for sub-millisecond retrieval without token bloat.
- **Antigravity Zero-Prompt Auto-Load**: Includes pre-compiled token-dense system prompt injections (`SYSTEM_PROMPT_INJECTION.md`) and drop-in rule files (`integration/00_user_cognitive_os.md`) for `.agents/rules/`.

---

## 2. Directory Layout

```
master_agent/                                      <-- Standalone Git Repository (Private)
├── .gitignore                                     <-- Local gitignore (excludes OS/temp caches)
├── README.md                                      <-- Complete Architecture & Usage Specification
├── master_agent_config.json                       <-- Path, transcript & workspace settings
├── SYSTEM_PROMPT_INJECTION.md                     <-- Pre-compiled token-dense system prompt block
│
├── meta_cognition/                                <-- TIER 1: UNIVERSAL (Cross-Workspace)
│   ├── thinking_patterns/                         <-- Empirical validation, reverse engineering, surgical diffs
│   ├── instruction_styles/                        <-- Directive dispatch, vigilant feedback, tool synergy
│   ├── universal_rules/                           <-- Gatekeeping, Guardrail P1 purity, git prohibition
│   └── cognitive_axioms/                          <-- Fundamental cognitive axioms of the master user
│
├── workspaces/                                    <-- TIER 2: WORKSPACE-ISOLATED (Strictly Namespaced)
│   └── universal_autonomous_career_agent/         <-- Current Workspace Sandbox
│       ├── workspace_manifest.json                <-- URI, corpus, and domain scope
│       ├── domain_rules/                          <-- Naukri/LinkedIn decoupling, modal scroll isolation
│       ├── platform_schemas/                      <-- Reverse engineered DOM classes & SVG indicators
│       └── task_ledger.json                       <-- Completed session milestones for this repo
│
├── interaction_history/                           <-- DEEP COGNITIVE REFLECTION ENGINE
│   ├── reflections_index.json                     <-- Chronological index of analyzed turns
│   ├── turn_0000_turn-01.json                     <-- Step 0: Developer mode & gatekeeping inception
│   ├── turn_0714_turn-08.json                     <-- Step 714: SRP reverse engineering & match scores
│   ├── turn_0876_turn-09.json                     <-- Step 876: Vigilant tool mandate correction
│   ├── turn_1346_turn-14.json                     <-- Step 1346: Campus & multi-stint duplicate nuance
│   ├── turn_1422_turn-15.json                     <-- Step 1422: Modal background scroll leak feedback
│   ├── turn_1492_turn-16.json                     <-- Step 1492: Candidate privacy & onboarding forms
│   ├── turn_1607_turn-19.json                     <-- Step 1607: Master agent alter-ego creation
│   └── turn_1618_turn-20.json                     <-- Step 1618: Distributed Git & Graph Memory mandate
│
├── graph_memory/                                  <-- SEMANTIC GRAPH MEMORY ENGINE
│   ├── nodes.json                                 <-- 21 Cognitive nodes (Principles, Axioms, Events)
│   ├── edges.json                                 <-- 14 Semantic directed edges with relation types
│   └── graph_index.json                           <-- Adjacency list index for sub-millisecond lookup
│
├── core/                                          <-- Master Cognitive Engine
│   ├── __init__.py                                <-- Package exports
│   ├── workspace_guard.py                         <-- Cross-workspace isolation enforcer
│   ├── graph_memory_engine.py                     <-- Graph query & adjacency traversal engine
│   ├── persona_loader.py                          <-- Ingests and indexes all knowledge cards
│   ├── transcript_learner.py                      <-- Ingests transcript.jsonl & extracts learnings
│   ├── decision_emulator.py                       <-- 'Acts as me': Rule verification & simulated voice
│   ├── self_healing_advisor.py                    <-- Diagnostic directives in authentic user voice
│   ├── antigravity_context_bridge.py              <-- Auto-compiles system prompt injections
│   └── run_master_agent.py                        <-- Unified CLI entry point
│
├── tests/                                         <-- Automated Verification Suite
│   └── test_master_agent_suite.py                 <-- 9-test unit & integration test suite (100% pass)
│
├── integration/                                   <-- Antigravity Brain Hook
│   └── 00_user_cognitive_os.md                    <-- Drop-in global rule file for .agents/rules/
│
└── output/                                        <-- Runtime Audits & Advice
    └── audits/
        └── system_audit_report.json               <-- Generated test audit report
```

---

## 3. How to Push to Your Private Git Repository

This directory is ready to be initialized as its own Git repository:

```powershell
cd "f:\JOB AI AGENT\master_agent"
git init
git add .
git commit -m "feat: initial cognitive memory, graph memory, and cross-workspace isolation"
git branch -M main
git remote add origin https://github.com/<your-username>/understanding-master.git
git push -u origin main
```
*(Keep the remote repository private to protect your personal cognitive patterns.)*

---

## 4. Cross-Workspace Isolation Protocol

To guarantee that Project A instructions (e.g., Naukri/LinkedIn scrapers) never pollute Project B:
1. All general engineering rules live in `meta_cognition/` (**Tier 1**).
2. All project-specific models live under `workspaces/<workspace_slug>/` (**Tier 2**).
3. The runtime engine (`WorkspaceGuard`) validates the active session workspace URI. If a foreign memory is queried, it raises `CrossWorkspaceContaminationError` and strictly blocks the bleed.

---

## 5. CLI Command Reference

Execute from `f:\JOB AI AGENT`:

```powershell
# 1. View current cognitive memory status
python master_agent/core/run_master_agent.py status

# 2. Query Semantic Graph Memory
python master_agent/core/run_master_agent.py graph
python master_agent/core/run_master_agent.py graph --node node_zero_assumptions

# 3. View Deep Cognitive Reflection Interaction History
python master_agent/core/run_master_agent.py reflections

# 4. Verify Cross-Workspace Isolation Boundary
python master_agent/core/run_master_agent.py guard-check --workspace "file:///f:/JOB%20AI%20AGENT"

# 5. Export Token-Dense Antigravity System Prompt Block
python master_agent/core/run_master_agent.py export-prompt

# 6. Audit a Proposed Action
python master_agent/core/run_master_agent.py audit --action "Modify core/04_job_discovery.py" --files "core/04_job_discovery.py"

# 7. Get Troubleshooting Advice in Your Authentic Voice
python master_agent/core/run_master_agent.py advise --error "Background page is scrolling behind modal"

# 8. Run 9-Test Automated Verification Suite
python master_agent/tests/test_master_agent_suite.py
```

---

## 6. Zero-Prompt Antigravity Global Integration

To have Antigravity automatically adopt this cognitive operating system in any new chat or workspace:
1. Copy `master_agent/integration/00_user_cognitive_os.md` into your Antigravity global rules directory:
   `C:\Users\7303150607\.gemini\config\rules\00_user_cognitive_os.md` (or `.agents/rules/`).
2. Alternatively, copy the contents of `master_agent/SYSTEM_PROMPT_INJECTION.md` into the initial prompt of any new chat.
