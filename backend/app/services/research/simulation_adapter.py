"""Adapter between Research Lab hypotheses and the existing MiroFish engine."""
from typing import Dict, Any, Optional
from ..simulation_manager import SimulationManager
from ...models.project import ProjectManager
from .repository import ResearchRepository

class ResearchSimulationAdapter:
    @staticmethod
    def build_requirement(hypothesis: Dict[str, Any]) -> str:
        return (
            "RESEARCH LAB HYPOTHESIS\n"
            f"Domain: {hypothesis.get('domain', 'toyt')}\n"
            f"Category: {hypothesis.get('category')}\n"
            f"Hypothesis: {hypothesis.get('statement')}\n\n"
            "Goal: explore plausible reactions, mechanisms, objections and second-order effects. "
            "Separate observed facts from assumptions and simulated behavior. "
            "Do not treat simulated behavior as empirical proof. Explicitly surface uncertainty."
        )

    @staticmethod
    def create(hypothesis: Dict[str, Any], project_id: str, graph_id: Optional[str] = None,
               enable_twitter: bool = True, enable_reddit: bool = True) -> Dict[str, Any]:
        project = ProjectManager.get_project(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        resolved_graph = graph_id or project.graph_id
        if not resolved_graph:
            raise ValueError("Project has no graph. Build the Zep graph before simulating a hypothesis.")

        requirement = ResearchSimulationAdapter.build_requirement(hypothesis)
        manager = SimulationManager()
        state = manager.create_simulation(project_id, resolved_graph, enable_twitter, enable_reddit)
        link = {
            "simulation_id": state.simulation_id,
            "hypothesis_id": hypothesis["hypothesis_id"],
            "project_id": project_id,
            "graph_id": resolved_graph,
            "simulation_requirement": requirement,
            "status": state.status.value,
        }
        ResearchRepository.create("simulation_links", link)
        ResearchRepository.append_unique("hypotheses", hypothesis["hypothesis_id"], "hypothesis_id", "simulation_ids", state.simulation_id)
        return link

    @staticmethod
    def get_link(simulation_id: str):
        return ResearchRepository.get("simulation_links", simulation_id)

    @staticmethod
    def requirement_for(simulation_id: str, fallback: str = "") -> str:
        link = ResearchSimulationAdapter.get_link(simulation_id)
        return (link or {}).get("simulation_requirement") or fallback
