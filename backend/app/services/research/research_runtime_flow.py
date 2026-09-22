"""Runtime orchestration for simulations linked to Research Lab hypotheses."""
from typing import Any, Dict, Optional
from .repository import ResearchRepository
from .research_round_bridge import ResearchRoundBridge, ResearchRoundEnvelope


class ResearchRuntimeFlow:
    @staticmethod
    def link_for(simulation_id: str) -> Optional[Dict[str, Any]]:
        return ResearchRepository.get("simulation_links", simulation_id)

    @classmethod
    def start_policy(cls, simulation_id: str, graph_id: str,
                     requested_max_rounds: Optional[int] = None) -> Optional[Dict[str, Any]]:
        link = cls.link_for(simulation_id)
        if not link:
            return None
        kwargs = ResearchRoundBridge.start_kwargs(graph_id, requested_max_rounds)
        kwargs["research_envelope"] = ResearchRoundEnvelope(
            simulation_id=simulation_id,
            hypothesis_id=link.get("hypothesis_id", ""),
            source_snapshot_id=link.get("source_snapshot_id", ""),
        ).to_dict()
        return kwargs
