"""
SelfHealingAdvisor: Provides supervisory advice and troubleshooting protocols
modeled after the user's standards to help the Job Agent self-heal.
"""

from typing import Dict, Any, List, Optional
from .persona_loader import PersonaLoader


class SelfHealingAdvisor:
    """
    Translates observed agent errors or UI anomalies into prescriptive,
    fact-based diagnostic directives reflecting the user's troubleshooting style.
    """

    def __init__(self, loader: Optional[PersonaLoader] = None):
        self.loader = loader if loader else PersonaLoader()

    def diagnose_error(self, error_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Diagnoses a failure and returns actionable advice in the user's voice."""
        lower_err = error_text.lower()
        advice: List[str] = []
        tools_recommended: List[str] = []

        if "scroll" in lower_err or "backdrop" in lower_err or "behind" in lower_err:
            advice.append("Check for background page scroll bleed. Never use page-level window.scrollTo() when a dialog or chatbot is open.")
            advice.append("Identify the exact modal container and scope the scroll directly within it.")
            advice.append("Use element.click(force=True) to bypass backdrop or sticky header overlay traps.")
            tools_recommended.extend(["/chrome-devtools", "/troubleshooting"])

        elif "selector" in lower_err or "element not found" in lower_err or "timeout" in lower_err:
            advice.append("Do not guess selectors! Connect to live Chrome on port 9222 and inspect the live DOM tree.")
            advice.append("Check if the container is lazy-mounted (e.g. #lazyEmployment, #lazyKeySkills) — scroll it into viewport and wait 1500ms for hydration.")
            advice.append("Check if this is Naukri Campus (input#jobType present) vs standard Naukri.")
            tools_recommended.extend(["/browser", "/chrome-devtools"])

        elif "purity" in lower_err or "guardrail p1" in lower_err:
            advice.append("Guardrail P1 Violation! You hardcoded candidate PII or specific profile paths in core/*.py.")
            advice.append("Strip out all hardcoded strings immediately. Use ctx.config or input parameters instead.")
            tools_recommended.append("AST / grep scan")

        elif "duplicate" in lower_err:
            advice.append("Apply the 3-way duplicate check: Company + Designation + Years.")
            advice.append("If years differ (e.g. 2022 vs 2024), treat them as separate stints, not duplicates!")
            tools_recommended.append("Multi-attribute comparison")

        else:
            advice.append("Perform root cause analysis using empirical evidence from logs rather than making assumptions.")
            advice.append("Verify pre-flight CDP connection and review screenshot artifacts.")
            tools_recommended.extend(["/troubleshooting", "/chrome-devtools"])

        return {
            "error_summary": error_text,
            "advisory_directive": "\n".join(f"- {a}" for a in advice),
            "tools_to_invoke": tools_recommended,
            "simulated_user_prompt": f"I saw an issue: {error_text}. Use {' '.join(tools_recommended)} to inspect the live state and fix it properly."
        }
