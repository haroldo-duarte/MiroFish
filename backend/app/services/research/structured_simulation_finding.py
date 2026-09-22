"""Validated structured assessment boundary for synthetic reports.

Direction is never inferred from arbitrary prose. It must be explicitly
provided as structured output and is constrained to the Research Lab enum.
"""
from typing import Any, Dict

ALLOWED_DIRECTIONS = {"supports", "contradicts", "inconclusive"}
ALLOWED_CONFIDENCE = {"low", "medium", "high", "unknown"}


class StructuredSimulationFinding:
    @staticmethod
    def validate(payload: Dict[str, Any]) -> Dict[str, Any]:
        direction = str(payload.get("direction") or "inconclusive").lower()
        confidence = str(payload.get("confidence") or "low").lower()
        if direction not in ALLOWED_DIRECTIONS:
            raise ValueError("invalid simulation finding direction")
        if confidence not in ALLOWED_CONFIDENCE:
            raise ValueError("invalid simulation finding confidence")
        limitations = payload.get("limitations") or []
        if not isinstance(limitations, list):
            raise ValueError("simulation finding limitations must be a list")
        return {
            "direction": direction,
            "confidence": confidence,
            "limitations": [str(x) for x in limitations if str(x).strip()],
        }
