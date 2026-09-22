# SOPHRON BOOT SUMMARY - Updated: 2026-09-23 00:10 IST
# Purpose: Fast cold-start orientation. Read this FIRST at every session.
#          This replaces the need to read 5 separate files before starting.
#          Full files remain as the record - this is the navigation index.
# Update: Write a new BOOT_SUMMARY at the END of every session.

---

## LAST KNOWN STATE
**As of 2026-09-23 00:10 IST | Session 2488a2da**

- **ai_client.py**: Multi-key round-robin architecture v2.0. 7 API keys in gemini_credentials.json. self.gemini_client is a @property (no setter). _rotate_gemini_client() cycles clients. Colab init block restored to __init__. AttributeError regression repaired.
- **ai_rate_manager.py**: NEW — SmartRateManager with 3.5s global floor + 120s model ban on 429/503.
- **Gemini Inline Batch Engine**: _gemini_batch_evaluate_inline() — 40 cards/chunk, bypasses batch IPC.
- **Profile status**: udaysagar_kandpal — target roles updated to mid-senior Java (Senior Software Engineer, Lead Engineer, Microservices Lead, Java). Architect/Principal roles removed.
- **Docs**: ARCHITECTURE_REFERENCE.md v5.3 | SCAR_TISSUE.md (+2 entries: @property regression + throwaway script anti-pattern)
- **Active candidate**: udaysagar_kandpal | Salary floor: 25 LPA+ | Target: Senior Java / Lead / Microservices roles
- **Sophron**: TURN-68 | 58 graph nodes | 68 edges | insight card written for this session
- **Git**: Committed 9e0526a and pushed to origin/main. gemini_credentials.json git-ignored (confirmed untracked).

## TOP OPEN ISSUES & USER DIRECTIVES
1. **Chat Signal-to-Noise Ratio (Critical User Mandate)**:
   - User explicitly requested: Do NOT dump every micro-polling log into chat. Live logs are inspected directly by user from the local terminal.
   - Reserve chat exclusively for: Cognitive IPC questions, verified application milestones, and actionable directives.
2. **Zero-Trust Purity (Guardrail P1)**:
   - Zero hardcoding of candidate details or CTC in core/*.py or scripts/*.py.
3. **Config JSON = Directly Editable Data**:
   - Never create throwaway .py scripts to mutate candidate_config.json or any JSON config. Edit directly via replace_file_content.
4. **AIClient @property Invariant**:
   - self.gemini_client is PERMANENTLY a @property. Never assign to it. Use self._gemini_clients and self._current_client_idx.

---

## CRITICAL OPERATIONAL PROTOCOLS
1. **Low-Frequency Chat Reporting**: High-signal summaries only. Live technical logs stay in terminal.
2. **Zero Heuristics in Core**: AG Brain resolves screening and tailoring via IPC; Python is an actuator.
3. **Minimal Footprint**: Every file created must be justified. No throwaway scripts.
4. **After Any AIClient Refactor**: Run git diff to verify no init-time code was displaced into a method.
5. **gemini_credentials.json**: Holds api_keys array. Git-ignored. Never committed.

---

## SOPHRON ARCHITECTURE STATE
- **Schema version**: v2 (with CONTEXT_CLASSIFICATION + CONTEXT_TRANSITION)
- **Latest Insight**: insight_20260923_multi_key_gemini_rotation_and_agent_integrity
- **TURN count**: 68
- **Graph**: 58 nodes, 68 edges
- **Total reflections**: 61
