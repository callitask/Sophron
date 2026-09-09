"""
DecisionEmulator: Models and emulates the user's decision-making process.
Given a proposed action, plan, or question, answers:
'Would the User approve this? How would the User direct this?'
"""

from typing import Dict, Any, List, Optional
from .persona_loader import PersonaLoader


class DecisionEmulator:
    """
    Evaluates actions against the user's core thinking patterns,
    session rules, and quality gates to predict user acceptance or rejection.
    """

    def __init__(self, loader: Optional[PersonaLoader] = None):
        self.loader = loader if loader else PersonaLoader()

    def evaluate_action(
        self,
        action_description: str,
        target_files: Optional[List[str]] = None,
        is_empirically_verified: bool = True,
        is_pre_approved_by_user: bool = False,
        involves_git: bool = False,
        involves_candidate_pii_in_core: bool = False,
        involves_global_window_scroll_in_modal: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluates a proposed action against the user's strict rules.
        Returns a decision dictionary: status ('APPROVED', 'REJECTED', 'NEEDS_REVISION'),
        violations list, and the user's simulated voice rationale.
        """
        violations = []
        recommendations = []

        # Rule 1: Developer Mode Gatekeeping (SR-001)
        if not is_pre_approved_by_user and target_files:
            py_targets = [f for f in target_files if f.endswith(".py")]
            if py_targets:
                violations.append(
                    "VIOLATION [SR-001 Developer Mode Gatekeeping]: Attempted to modify production code "
                    f"({py_targets}) without prior report submission and manual user approval."
                )
                recommendations.append("Generate an implementation plan / report first and wait for explicit manual user approval.")

        # Rule 2: Codebase Purity Guardrail P1 (SR-002)
        if involves_candidate_pii_in_core:
            violations.append(
                "VIOLATION [SR-002 Guardrail P1 Codebase Purity]: Attempted to hardcode candidate PII, "
                "salary numbers, or profile directory names into core/*.py."
            )
            recommendations.append("Keep core engine files 100% generic; store candidate data strictly in profiles/<candidate>/.")

        # Rule 3: Git Command Prohibition (SR-004)
        if involves_git or "git " in action_description.lower():
            violations.append(
                "VIOLATION [SR-004 Git Command Prohibition]: Attempted to execute automated git commands."
            )
            recommendations.append("Never run git commit, push, or checkout. Leave all version control to the human user.")

        # Rule 4: Empirical Verification / Zero Assumptions (TP-001)
        if not is_empirically_verified:
            violations.append(
                "VIOLATION [TP-001 Zero Assumptions]: Proposed action relies on unverified guesses rather than live CDP inspection."
            )
            recommendations.append("Connect to CDP on port 9222 and verify live DOM elements before proceeding.")

        # Rule 5: Modal Scroll Isolation (SR-005)
        if involves_global_window_scroll_in_modal:
            violations.append(
                "VIOLATION [SR-005 Modal Scroll Isolation]: Attempted global window scroll while modal or drawer is active."
            )
            recommendations.append("Scope scroll strictly inside the active modal container (.chatbot_MessageContainer, #internshipDetails_Modal).")

        # Determine Status & User Voice
        if violations:
            status = "REJECTED"
            rationale = (
                "Hold on. You are violating established operating standards. "
                + " ".join(recommendations)
                + " Address these violations before moving forward."
            )
        else:
            status = "APPROVED"
            rationale = "Action aligns with established architectural rules, empirical standards, and codebase purity."

        return {
            "status": status,
            "violations": violations,
            "recommendations": recommendations,
            "user_voice_rationale": rationale
        }

    def evaluate_duplicate_tenure(
        self,
        exp1_company: str,
        exp1_role: str,
        exp1_years: tuple,
        exp2_company: str,
        exp2_role: str,
        exp2_years: tuple
    ) -> Dict[str, Any]:
        """
        Emulates user's nuanced multi-attribute duplicate evaluation (Rule C16 & DP-003).
        """
        comp_match = exp1_company.strip().lower() == exp2_company.strip().lower()
        role_match = exp1_role.strip().lower() == exp2_role.strip().lower()
        years_match = exp1_years == exp2_years

        if comp_match and role_match and not years_match:
            return {
                "is_duplicate": False,
                "reasoning": "Distinct tenures at the same company across different years (e.g. intern then full-time).",
                "action": "ADD_NEW / PRESERVE_BOTH",
                "user_voice": "A person can work twice or more in the same post at multiple times. Preserve both stints as distinct!"
            }
        elif comp_match and role_match and years_match:
            return {
                "is_duplicate": True,
                "reasoning": "Identical company, role, and tenure years.",
                "action": "SKIP / DEDUPLICATE",
                "user_voice": "Exact match across company, designation, and years. This is a duplicate."
            }
        else:
            return {
                "is_duplicate": False,
                "reasoning": "Different company or different role.",
                "action": "PRESERVE",
                "user_voice": "Independent records."
            }
