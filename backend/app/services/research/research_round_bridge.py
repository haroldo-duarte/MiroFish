"""Research simulation-round contract over the existing OASIS runner.

Keeps OASIS as the execution engine while adding research provenance and an
explicit synthetic-output boundary.
"""
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from ..simulation_runner import SimulationRunState


@dataclass
class ResearchRoundEnvelope:
    simulation_id: str
    hypothesis_id: str = ""
    question_id: str = ""
    study_id: str = ""
    source_snapshot_id: str = ""
    epistemic_type: str = "synthetic_simulation"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ResearchRoundBridge:
    @staticmethod
    def start_kwargs(graph_id: str, max_rounds: Optional[int] = None) -> Dict[str, Any]:
        """Safe arguments for SimulationRunner.start_simulation."""
        return {
            "platform": "parallel",
            "max_rounds": max_rounds,
            "enable_graph_memory_update": True,
            "graph_id": graph_id,
        }

    @staticmethod
    def summarize(state: SimulationRunState, envelope: ResearchRoundEnvelope) -> Dict[str, Any]:
        """Research projection of runner state; actions remain synthetic."""
        return {
            "envelope": envelope.to_dict(),
            "runner": state.to_dict(),
            "rounds": [
                {
                    "round_num": r.round_num,
                    "simulated_hour": r.simulated_hour,
                    "actions_count": len(r.actions),
                    "active_agents_count": len(set(r.active_agents)),
                }
                for r in state.rounds
            ],
            "epistemic_notice": (
                "All agent actions and round outcomes are synthetic simulation outputs. "
                "They are not empirical observations and cannot independently validate a hypothesis."
            ),
        }

    @staticmethod
    def finding_source_type() -> str:
        return "simulation"
