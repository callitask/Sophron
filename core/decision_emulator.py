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

    def predict_user_response(self, stimulus_text: str) -> Dict[str, Any]:
        """
        Uses the Neural Behavioral Prediction Matrix (PRE-001 & PRE-003) to forecast
        how the user's brain will react emotionally, cognitively, and behaviorally.
        """
        text_lower = stimulus_text.lower()
        
        # Check PRE-001 pairs
        matrix_card = self.loader.get_card("PRE-001")
        pairs = matrix_card.get("stimulus_response_pairs", []) if matrix_card else []

        best_score = 0
        matched_prediction = None
        for pair in pairs:
            action_desc = pair.get("ai_action", "").lower()
            keywords = [w for w in action_desc.split() if len(w) > 3 and w not in ["with", "without", "that", "from", "into"]]
            match_count = sum(1 for k in keywords if k in text_lower)
            if match_count > best_score:
                best_score = match_count
                matched_prediction = pair

        if not matched_prediction:
            # Default prediction based on sentiment/action
            if any(w in text_lower for w in ["guess", "assume", "speculate", "without running", "3 pages", "orphan", "tcs", "git commit"]):
                matched_prediction = {
                    "predicted_cognitive_state": "Cognitive friction; violation of established quality or safety axioms.",
                    "predicted_emotional_response": "Sharp irritation, loss of trust, demanding immediate correction.",
                    "predicted_user_behavior": "Immediate corrective directive or reprimand.",
                    "mitigation_protocol": "Adhere strictly to empirical verification, 2-page document limits, and gatekeeping rules."
                }
            else:
                matched_prediction = {
                    "predicted_cognitive_state": "Cognitive resonance; actions match architectural standards.",
                    "predicted_emotional_response": "Satisfaction, calm confidence in system throughput.",
                    "predicted_user_behavior": "Green-lights progress or issues next strategic goal.",
                    "mitigation_protocol": "Maintain verified empirical rigor."
                }

        # Calculate resonance vs friction score from PRE-003
        score = 0
        if "verified" in text_lower or "empirical" in text_lower: score += 10
        if "2 page" in text_lower or "two page" in text_lower: score += 9
        if "commit" in text_lower and ("authorized" in text_lower or "checkpoint" in text_lower): score += 8
        if "sophron" in text_lower: score += 10
        
        if "guess" in text_lower or "assume" in text_lower: score -= 15
        if "3 page" in text_lower or "orphan" in text_lower: score -= 12
        if "tcs" in text_lower or "blacklisted" in text_lower: score -= 20
        if "unauthorized git" in text_lower: score -= 25

        return {
            "stimulus": stimulus_text,
            "predicted_cognitive_state": matched_prediction.get("predicted_cognitive_state"),
            "predicted_emotional_response": matched_prediction.get("predicted_emotional_response"),
            "predicted_user_behavior": matched_prediction.get("predicted_user_behavior"),
            "mitigation_protocol": matched_prediction.get("mitigation_protocol"),
            "resonance_score": score,
            "resonance_zone": "RESONANCE" if score >= 0 else "FRICTION"
        }
