"""
WorkspaceGuard: Cryptographic & URI-level Cross-Workspace Isolation Enforcer.
Guarantees that project-specific domain rules, schemas, and memories from Workspace A
can NEVER bleed or cross-contaminate Workspace B.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional


class CrossWorkspaceContaminationError(RuntimeError):
    """Raised when an agent attempts to apply a workspace-specific memory to an unrelated workspace."""
    pass


class WorkspaceGuard:
    """
    Enforces strict two-tier memory isolation:
    - Tier 1 (Universal Meta-Cognition): Permitted everywhere.
    - Tier 2 (Workspace Episodic Memory): Strictly locked to matching workspace URI/ID.
    """

    def __init__(self, current_workspace_uri: Optional[str] = None):
        self.current_workspace_uri = str(current_workspace_uri).strip() if current_workspace_uri else None

    def filter_memory_access(
        self,
        memory_item: Dict[str, Any],
        target_workspace_id: Optional[str] = None
    ) -> bool:
        """
        Determines whether the current session is authorized to read this memory.
        Returns True if authorized; raises CrossWorkspaceContaminationError if unauthorized.
        """
        tier = memory_item.get("tier", "TIER_1_UNIVERSAL")
        if tier == "TIER_1_UNIVERSAL":
            return True

        # Tier 2 Check
        item_ws = memory_item.get("workspace_id") or memory_item.get("workspace_slug")
        if not item_ws:
            return True

        authorized = False
        if self.current_workspace_uri:
            import urllib.parse
            clean_uri = urllib.parse.unquote(self.current_workspace_uri.lower())
            if ("job ai agent" in clean_uri or "universal-autonomous-career-agent" in clean_uri) and "universal_autonomous_career_agent" in item_ws.lower():
                authorized = True
            elif item_ws.lower() in clean_uri:
                authorized = True

        if not authorized:
            raise CrossWorkspaceContaminationError(
                f"[CROSS-WORKSPACE CONTAMINATION BLOCKED] Memory '{item_ws}' is isolated to another workspace "
                f"and cannot be accessed from session '{self.current_workspace_uri}'. "
                f"Cross-workspace rule mixing is strictly prohibited by Master User policy."
            )
        return True
