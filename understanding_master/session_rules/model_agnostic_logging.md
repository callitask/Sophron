# Model-Agnostic Session Intelligence Logging (Sophron)

> Sophron is general human+AI intelligence, not a JOB AI AGENT subfolder. Every AI session — Antigravity, Muse, Claude, any coding agent — logs here with correct context. Personal intelligence grows smarter each session and can seed future agents (Jarvis-like).

## Required fields on every insight/TURN card
- `agent_model`: e.g. `antigravity-2.0`, `muse-spark`, `claude-opus` (never assume; record the actual model driving the session)
- `software`: e.g. `antigravity-ide`, `opencode`, `cli` + version when known
- `workspace_origin`: `career_agent` | `sophron_architecture` | `new_project_X` | `global`
- `data_subject`, `rule_tier`, `is_cross_project_applicable` (schema v2)
- `CONTEXT_TRANSITION` when the topic switches

## Update rules
- Agent-structure changes (JOB AI AGENT dev) update the `agent_structure` domain mirror only — never personal intelligence.
- Human + AI learning updates `personal_intelligence` only — never agent code graphs.
- Software/model preferences: document every tool used (`/browser`, `chrome-devtools`, `opencode`, IDE version) so future agents know what worked.
- Never copy live `profiles/<candidate>` values into cards. Reference `default_user` schema only.
