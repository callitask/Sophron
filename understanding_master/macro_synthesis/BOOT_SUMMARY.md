# SOPHRON BOOT SUMMARY - Updated: 2026-09-27 12:30 IST
# Purpose: Fast cold-start orientation. Read this FIRST at every session.
#          This replaces the need to read 5 separate files before starting.
#          Full files remain as the record - this is the navigation index.
# Update: Write a new BOOT_SUMMARY at the END of every session.

---

## LAST KNOWN STATE
**As of 2026-09-27 12:30 IST | Session TURN-72 (muse-spark via opencode)**

- **Tailoring reframe (TURN-72)**: AI bullet reframing live (`ai_client.reframe_role_bullets`, same-count JSON contract, offline skip) with per-role atomic validation (count/numbers/tech-allowlist) plus marker normalizer; 63/63 proven live; tripwire logs novel Capitalized words; docs v1.2; toggle `target_jobs.resume_bullet_reframing` (default ON).

- **LinkedIn apply loop (TURN-71)**: two stacked silent blackouts fixed with one live probe each — dead title selector replaced by verified link/subtitle/caption map, None-href TypeError blackout fixed via container job-ID fallback. Search-pane apply flow proven live (modal with pre-filled profile in ~2s, first Easy Apply commit observed).
- **Modal intelligence**: bidirectional numeric validation retry, step-progression tracking with broad error capture, hidden file-input handling, checkbox groups, custom dropdown widgets, per-job modal QA audit on every exit.
- **Chatbot honesty**: blind first-option fallback removed from radio path (last refuge of the learned-truth poison class); unanswerable questions abort with manual-review logs.
- **Velocity governors**: daily LinkedIn apply cap from config, in-modal verification-challenge detector (discard + human-gate, never auto-solve).
- **Resume integrity**: forensic diff proved 63/63 bullets preserved with identical text across generations (2 pages each); tailoring is reorder-only by code inspection; structural zero-omission guardrail added and unit-proven both directions.
- **Owner corrections applied**: driving-licence learned truth fixed to Yes with backup; poisoned internship-phrasing truths purged earlier.
- **Session health**: soft-throttle evidence on LinkedIn (detection iframe, armed captcha, swallowed view-page clicks) — cooldown discipline plus governors, never more automation against a flag.
- **Sophron**: TURN-72 | 66 graph nodes | 80 edges | insight card for this session (see below)
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
7. **Silent-Skip Forensics (TURN-71 evolution)**:
   - Zero output with zero errors means dead selectors, None-fed operators in bare try/except, or inert buttons — one live probe per hypothesis, prove UI actions by resulting state, diff artifacts before theorizing drift.

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
- **Latest Insight**: insight_20260927_tailoring_reframe_brain_disposes
- **TURN count**: 72
- **Graph**: 66 nodes, 80 edges
- **Total reflections**: 65
