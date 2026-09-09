"""
Master Agent Core Engine
Acts as the human architect, modeling user thinking, instruction style, 
and operational rules to guide parallel autonomous agents.
"""

from .persona_loader import PersonaLoader
from .transcript_learner import TranscriptLearner
from .decision_emulator import DecisionEmulator
from .self_healing_advisor import SelfHealingAdvisor

__all__ = [
    "PersonaLoader",
    "TranscriptLearner",
    "DecisionEmulator",
    "SelfHealingAdvisor",
]
