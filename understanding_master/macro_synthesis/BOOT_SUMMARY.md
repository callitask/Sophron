# SOPHRON BOOT SUMMARY - Updated: 2026-09-24 14:00 IST
# Purpose: Fast cold-start orientation. Read this FIRST at every session.
#          This replaces the need to read 5 separate files before starting.
#          Full files remain as the record - this is the navigation index.
# Update: Write a new BOOT_SUMMARY at the END of every session.

---

## LAST KNOWN STATE
**As of 2026-09-24 14:00 IST | Session TURN-70 (muse-spark via opencode)**

- **Live ops (TURN-70)**: 15 single-cycles run and judged one by one. Tracker: Expian 85% APPLIED_1CLICK live; Nasu 92% + Apptad 85% earlier. Chatbot path 0/3 (2 drawer-drops incl. Tekshapers 95%, 1 C9 platform rejection at Sixt) vs 1-click 5/5 — portal friction is the binding constraint, not scoring.
- **Forensic fixes**: Gate 2 word-boundary (Nous Infosystems was killed by "infosys" substring); bare `Support` removed (was killing Java backend lead); full 154-term exclusion arming (was silently [:30]-truncated, azure idx 101); lite-first model order; intra-batch URL dedupe; IPC gate aligned to documented 40-65 window then evidence-scoped to LLM-failure fallback (Gemini early-return means Gemini verdicts ARE the borderline arbitration in API mode).
- **C23 tuning**: dead designations swapped (Microservices→Java Backend Developer, Lead Java Developer→Kafka Developer, Java→Senior Backend Engineer) with backups; rotation parked on new terms to test in budget. New terms delivered: Kafka Developer→Pyramid 90% deep scan, Senior Backend Engineer→Sixt 85% deep scan.
- **Seniority**: cognitive profile retuned Principal/Staff/Lead Architect → Senior/Lead Engineer (no code depended on the literal).
- **Ledger**: 972 entries; 13-entry audit reset + Tekshapers retry reset (backups kept); company gates + qualified history preserved.
- **Quota**: lite-first + dedupe holding; no full Exhausted stalls in the 15-cycle window (only per-cycle 3.8/3.7 instant 503s, lite answering).
- **Sophron**: TURN-70 | 62 graph nodes | 74 edges | insight card for this session (see below)
- **Git**: Repo A changes uncommitted (owner commits); Repo B writes uncommitted (push pending owner approval). No joint commits, no cross-imports.

## TOP OPEN ISSUES & USER DIRECTIVES
1. **Chat Signal-to-Noise Ratio (Critical User Mandate)**:
   - User explicitly requested: Do NOT dump every micro-polling log into chat. Live logs are inspected directly by user from the local terminal.
   - Reserve chat exclusively for: Cognitive IPC questions, verified application milestones, and actionable directives.
2. **Zero-Trust Purity (Guardrail P1)**:
   - Zero hardcoding of candidate details or CTC in `core/*.py`, `scripts/*.py`, `CompanySiteApply/`, `tests/`. Verified `(True, [])`.
3. **Config JSON = Directly Editable Data**:
   - Never create throwaway .py scripts to mutate `candidate_config.json` or any JSON config. Edit directly via replace_file_content.
4. **AIClient @property Invariant**:
   - `self.gemini_client` is PERMANENTLY a `@property`. Never assign to it. Use `self._gemini_clients` and `self._current_client_idx`.
5. **Verification-First Discipline (TURN-69 evolution)**:
   - On any supplied audit: `git diff` first, verify each claim with `file:line`, list rejected claims. On god-file growth: extract micro-libs, never split engine contracts. On past-entry corrections: redact + append evolved-thinking refs, never rewrite history.
6. **Forensics-First Operations (TURN-70 evolution)**:
   - On dry spells: scan the outcome ledger before re-reading logs; audit exclusion lists against the 4-term blueprint; never slice config lists for prompts without stating it; company identity is always word-boundary.

---

## CRITICAL OPERATIONAL PROTOCOLS
1. **Low-Frequency Chat Reporting**: High-signal summaries only. Live technical logs stay in terminal.
2. **Zero Heuristics in Core**: AG Brain resolves screening and tailoring via IPC; Python is an actuator.
3. **Minimal Footprint → Shared-Lib Doctrine (evolved TURN-69)**: No throwaway scripts; no duplicated inline logic — one importable helper under `core/utils/*` or `CompanySiteApply/utils/*` with AI CONTEXT header.
4. **After Any AIClient Refactor**: Run git diff to verify no init-time code was displaced into a method.
5. **gemini_credentials.json / colab_credentials.json**: Hold API keys. Git-ignored. Never committed. Indexer excludes `*credentials*`.
6. **Sophron Sync (append-only)**: New TURN card + insight card per session; append `reflections_index.json`, `current_week_trend.md`; extend graph nodes/edges/index with counts in sync; workspace `task_ledger.json` milestone; never rewrite past cards — reference them as evolved thinking.

---

## SOPHRON ARCHITECTURE STATE
- **Schema version**: v2 (with CONTEXT_CLASSIFICATION + CONTEXT_TRANSITION; TURN cards also carry `agent_model` + `software`)
- **Latest Insight**: insight_20260924_live15_funnel_remediation_and_batch_arbitration_truth
- **TURN count**: 70
- **Graph**: 62 nodes, 74 edges
- **Total reflections**: 63
