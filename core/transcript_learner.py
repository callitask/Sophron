"""
TranscriptLearner: Reads interaction transcripts (transcript.jsonl),
extracts user directives, patterns, corrections, and tool instructions,
and continuously enriches the knowledge cards in understanding_master/.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

MASTER_DIR = Path(__file__).resolve().parent.parent
UNDERSTANDING_MASTER_DIR = MASTER_DIR / "understanding_master"
LEARNED_INSIGHTS_DIR = UNDERSTANDING_MASTER_DIR / "learned_insights"


class TranscriptLearner:
    """
    Parses conversation transcripts to extract behavioral insights about the user
    and updates or creates incremental knowledge cards.
    """

    def __init__(self, transcript_path: Optional[Path] = None, insights_dir: Optional[Path] = None):
        self.transcript_path = Path(transcript_path) if transcript_path else None
        self.insights_dir = Path(insights_dir) if insights_dir else LEARNED_INSIGHTS_DIR
        self.insights_dir.mkdir(parents=True, exist_ok=True)

    def extract_user_turns(self, path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Extracts all user input events from transcript.jsonl."""
        target_path = Path(path) if path else self.transcript_path
        if not target_path or not target_path.exists():
            return []

        user_turns = []
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data.get("type") == "USER_INPUT" or data.get("source") == "USER_EXPLICIT":
                        user_turns.append({
                            "step_index": data.get("step_index"),
                            "created_at": data.get("created_at"),
                            "content": data.get("content", "")
                        })
                except Exception:
                    pass
        return user_turns

    def analyze_patterns(self, user_turns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes user turns to extract behavioral and instructional trends."""
        tool_mentions: Dict[str, int] = {}
        constraints_detected: List[str] = []
        corrections_detected: List[str] = []
        rule_keywords = ["not allowed", "ensure not to", "developer mode", "rule", "restriction", "purity", "duplicate"]
        tool_regex = re.compile(r"/(browser|chrome-devtools|flutter-setup-declarative-routing|debug-optimize-lcp|troubleshooting|a11y-debugging|goal|grill-me)", re.IGNORECASE)

        for turn in user_turns:
            content = turn["content"]
            # Detect slash tools
            matches = tool_regex.findall(content)
            for m in matches:
                tool_key = f"/{m.lower()}"
                tool_mentions[tool_key] = tool_mentions.get(tool_key, 0) + 1

            # Detect constraints
            for kw in rule_keywords:
                if kw in content.lower():
                    snippet = content[:150].replace("\n", " ")
                    constraints_detected.append(f"[Step {turn['step_index']}] Keyword '{kw}': {snippet}...")

            # Detect corrective feedback
            if any(phrase in content.lower() for phrase in ["i saw you did not", "i saw that", "error", "failure", "fix"]):
                corrections_detected.append(f"[Step {turn['step_index']}] {content[:160].replace(chr(10), ' ')}...")

        analysis = {
            "total_user_prompts": len(user_turns),
            "tool_dispatch_frequency": tool_mentions,
            "sample_constraints": constraints_detected[:5],
            "sample_corrections": corrections_detected[:5],
            "analysis_timestamp": datetime.now().isoformat()
        }
        return analysis

    def persist_learning_session(self, session_id: str, analysis: Dict[str, Any]) -> Path:
        """Saves a structured learning session card into learned_insights/."""
        card_id = f"INSIGHT-{session_id}"
        card_path = self.insights_dir / f"session_{session_id}.json"
        
        card_data = {
            "id": card_id,
            "category": "learned_insights",
            "title": f"Learned Insights from Session {session_id}",
            "generated_at": datetime.now().isoformat(),
            "analysis": analysis
        }
        
        with open(card_path, "w", encoding="utf-8") as f:
            json.dump(card_data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        return card_path
