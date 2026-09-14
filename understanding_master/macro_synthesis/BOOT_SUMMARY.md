# SOPHRON BOOT SUMMARY - Updated: 2026-09-14 18:40 IST
# Purpose: Fast cold-start orientation. Read this FIRST at every session.
#          This replaces the need to read 5 separate files before starting.
#          Full files remain as the record - this is the navigation index.
# Update: Write a new BOOT_SUMMARY at the END of every session.

---

## LAST KNOWN STATE
- **Active profiles**: anshika_garg (Finance/Audit, Noida + Gurugram only, >=8 LPA)
- **Second profile**: udaysagar_kandpal (Java Backend Architect, Bangalore, CDP port 9223)
- **CDP port registry**: 9222 = anshika_garg, 9223 = udaysagar_kandpal
- **Daemon status**: Last known - anshika_garg had zero applications in last hour (ledger saturation: 5,487 entries blocking finance titles)
- **Last Sophron sync**: 2026-09-14 (this session - rule adherence + Sophron architecture upgrade)

---

## TOP OPEN ISSUES (Do Not Ignore)
1. **Ledger saturation**: processed_ledger.json has 5,487+ entries blocking re-evaluation of finance titles. Domain-gated/low-score entries should be soft-gated, not permanently blocked. Need a flush strategy.
2. **Rule amnesia post turn ~12**: AI stops following rules after extended sessions. Mitigation now in place (ACTIVE_CONSTRAINT_BLOCK.md + SCAR_TISSUE.md). Monitor effectiveness.
3. **Sophron context-switch blindness**: Fixed in schema upgrade today - new insight cards must include CONTEXT_TRANSITION fields.
4. **Cross-project data blur in Sophron**: Fixed - new CONTEXT_CLASSIFICATION fields added to schema. Apply going forward.

---

## CRITICAL RULES IN EFFECT (Top 5 Most Violated)
1. **Zero heuristics in Python** - AG Brain decides all roles. Python = actuator only.
2. **Sophron writes via guard only** - guard.safe_write_json(), never open()+json.dump()
3. **Numeric IPC answers** - integer string only ("1", "2"), never a sentence
4. **Milestone cards mandatory** - write Sophron card after every task, correction, topic switch
5. **Guard.register_session() first** - instantiate SophronWriteGuard before anything else

---

## SOPHRON ARCHITECTURE STATE
- **Graph nodes**: 45 (as of 2026-09-13) + new UserBehavioralPattern nodes added 2026-09-14
- **Turn reflections**: 52 files in interaction_history/ through TURN-60
- **Latest insight**: insight_20260913_ag_brain_talent_strategist_decoupling
- **Schema version**: v2 (with CONTEXT_CLASSIFICATION + CONTEXT_TRANSITION) - applies from 2026-09-14 onwards
- **Write guard**: SophronWriteGuard v2 (concurrency-safe, multi-session detection)
- **New files added 2026-09-14**: ACTIVE_CONSTRAINT_BLOCK.md, SCAR_TISSUE.md, BOOT_SUMMARY.md

---

## WHAT I AM WALKING INTO (Context at Last Update)
- User is hardening rule-adherence architecture across all AI sessions
- Problem: Rules loaded at session start get forgotten mid-session
- Solution built: ACTIVE_CONSTRAINT_BLOCK.md (10 gates) + SCAR_TISSUE.md (failure memory) + BOOT_SUMMARY (this file) + Sophron schema v2 upgrade
- User mood: Architectural, investigatory, decisive. Wants structural solutions, not reminders.
- User work pattern: Identifies rule violations -> root-causes them -> codifies permanent structural fixes. This is a meta-corrective session.

---

## NEW SESSIONS: HOW TO ORIENT IN 30 SECONDS
1. Read this file (done)
2. Read .agents/rules/SCAR_TISSUE.md for known failure modes
3. Check Sophron/graph_memory/graph_index.json for adjacency lookup
4. Instantiate SophronWriteGuard with current session UUID
5. Update Sophron/master_agent_config.json -> paths -> transcript_path with current session UUID
6. Proceed with user request

---
## HOW TO UPDATE THIS FILE
At the end of every session, overwrite this file with:
- Updated LAST KNOWN STATE section
- Updated TOP OPEN ISSUES (add new, mark resolved ones)
- Updated WHAT I AM WALKING INTO with current context
