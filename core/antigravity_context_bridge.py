"""
AntigravityContextBridge: Generates token-optimized system prompt injection blocks
and workspace rules to allow any Antigravity chat or workspace to automatically
adopt the user's cognitive operating system without cross-task hallucination.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

MASTER_DIR = Path(__file__).resolve().parent.parent
META_DIR = MASTER_DIR / "meta_cognition"
INTEGRATION_DIR = MASTER_DIR / "integration"


class AntigravityContextBridge:
    """
    Compiles Tier 1 meta-cognition and isolated Tier 2 workspace context
    into an optimized system prompt block.
    """

    def __init__(self, current_workspace_uri: Optional[str] = None):
        self.current_workspace_uri = current_workspace_uri

    def compile_system_prompt_injection(self) -> str:
        """Generates a compressed, highly dense Markdown system prompt."""
        axioms_file = META_DIR / "cognitive_axioms" / "master_axioms.json"
        axioms = []
        if axioms_file.exists():
            with open(axioms_file, "r", encoding="utf-8") as f:
                axioms = json.load(f).get("axioms", [])

        prompt = []
        prompt.append("<!-- USER COGNITIVE OPERATING SYSTEM (AUTONOMOUS LOAD) -->")
        prompt.append("## USER COGNITIVE OPERATING SYSTEM: MANDATORY OPERATING PROTOCOLS\n")
        prompt.append("You are acting as the execution arm under the Human Master Architect. Follow these axioms globally:\n")

        for ax in axioms:
            prompt.append(f"- **{ax.split(':')[0]}**: {ax.split(':', 1)[-1].strip()}")

        prompt.append("\n### 1. Zero Assumptions & Empirical Proof")
        prompt.append("- NEVER guess selectors, UI layouts, or data structures. Connect to live tools (/browser, /chrome-devtools, CDP port 9222) and inspect live DOM before making any claim.")
        prompt.append("- When user shares visual screenshots, reverse engineer them down to exact HTML tags and classes.")

        prompt.append("\n### 2. Developer Mode Gatekeeping")
        prompt.append("- Report -> Review -> Manual Approval -> Execution. You are strictly forbidden from editing production code without prior approval.")
        prompt.append("- Never run automated git commands (git commit, git push, etc.).")

        prompt.append("\n### 3. Strict Workspace Isolation")
        prompt.append("- Task memory, domain rules, and platform schemas from other workspaces must NEVER bleed into this workspace.")
        prompt.append("- Apply meta-cognitive rigor universally, but keep project-specific facts strictly isolated.")

        prompt.append("\n### 4. Nuanced Real-World Reasoning")
        prompt.append("- Deduplication requires multi-attribute composite checking (e.g. Company + Role + Tenure Years). Different years represent distinct legitimate stints.")
        prompt.append("- Scope all scrolls and clicks inside active dialog/modal containers.")

        return "\n".join(prompt)

    def write_prompt_file(self, target_file: Optional[Path] = None) -> Path:
        out_path = target_file if target_file else INTEGRATION_DIR / "SYSTEM_PROMPT_INJECTION.md"
        content = self.compile_system_prompt_injection()
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        return out_path

    def write_global_rule_file(self, target_file: Optional[Path] = None) -> Path:
        out_path = target_file if target_file else INTEGRATION_DIR / "00_user_cognitive_os.md"
        rule_content = f"""# User Cognitive Operating System (Global Antigravity Rule)

This rule establishes the permanent, cross-workspace behavioral standards of the Human Architect. It must be loaded automatically in all Antigravity chats.

{self.compile_system_prompt_injection()}
"""
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(rule_content.strip() + "\n")
        return out_path
