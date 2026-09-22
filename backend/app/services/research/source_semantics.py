"""Semantic guardrails for real-world research sources.

The central rule is that system-generated algorithmic output must never be
silently promoted to evidence of human behavior.
"""
from enum import Enum


class SourceSemanticClass(str, Enum):
    WORLD_STATE = "world_state"
    WORLD_RULE = "world_rule"
    OBSERVED_EVENT = "observed_event"
    HUMAN_BEHAVIOR = "human_behavior"
    ALGORITHMIC_PROCESS = "algorithmic_process"


AGENT_BEHAVIOR_ALLOWED = {
    SourceSemanticClass.HUMAN_BEHAVIOR,
}


def can_infer_agent_behavior(semantic_class: str) -> bool:
    """Return True only for sources explicitly classified as human behavior."""
    try:
        value = SourceSemanticClass(semantic_class)
    except ValueError:
        return False
    return value in AGENT_BEHAVIOR_ALLOWED


def assert_agent_behavior_source(semantic_class: str) -> None:
    """Fail closed when a source is not valid behavioral evidence."""
    if not can_infer_agent_behavior(semantic_class):
        raise ValueError(
            f"Source class '{semantic_class}' cannot be used as evidence of "
            "human agent behavior."
        )
