"""
PersonaLoader: Ingests, indexes, and queries the user knowledge cards
stored in master_agent/understanding_master/.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional

MASTER_DIR = Path(__file__).resolve().parent.parent
UNDERSTANDING_MASTER_DIR = MASTER_DIR / "understanding_master"


class PersonaLoader:
    """
    Loads all JSON knowledge cards representing the user's thinking patterns,
    instruction styles, session rules, debugging protocols, and goals.
    """

    def __init__(self, cards_dir: Optional[Path] = None):
        self.cards_dir = Path(cards_dir) if cards_dir else UNDERSTANDING_MASTER_DIR
        self.cards: Dict[str, Dict[str, Any]] = {}
        self.categories: Dict[str, List[Dict[str, Any]]] = {}
        self.reload()

    def reload(self) -> None:
        """Scans the understanding_master directory and reloads all JSON cards."""
        self.cards.clear()
        self.categories.clear()

        if not self.cards_dir.exists():
            return

        for json_file in self.cards_dir.rglob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    card_data = json.load(f)
                    card_id = card_data.get("id") or json_file.stem
                    cat = card_data.get("category") or json_file.parent.name
                    card_data["_file_path"] = str(json_file)
                    card_data["_category"] = cat

                    self.cards[card_id] = card_data
                    if cat not in self.categories:
                        self.categories[cat] = []
                    self.categories[cat].append(card_data)
            except Exception as e:
                print(f"[PersonaLoader] Warning: Failed to parse {json_file.name}: {e}")

    def get_card(self, card_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific card by its ID or stem."""
        return self.cards.get(card_id)

    def get_cards_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Retrieve all cards belonging to a specific category."""
        return self.categories.get(category, [])

    def get_all_rules(self) -> List[Dict[str, Any]]:
        """Retrieve all session rules enforced by the user."""
        return self.get_cards_by_category("session_rules")

    def get_all_thinking_patterns(self) -> List[Dict[str, Any]]:
        """Retrieve all thinking patterns guiding the user."""
        return self.get_cards_by_category("thinking_patterns")

    def get_all_debugging_protocols(self) -> List[Dict[str, Any]]:
        """Retrieve all debugging protocols established by the user."""
        return self.get_cards_by_category("debugging_protocols")

    def get_master_summary(self) -> Dict[str, Any]:
        """Returns high-level statistics and meta-summary of loaded knowledge."""
        summary = {
            "total_cards": len(self.cards),
            "categories": {cat: len(cards) for cat, cards in self.categories.items()},
            "active_rules_count": len(self.get_all_rules()),
            "root_directory": str(self.cards_dir)
        }
        return summary
