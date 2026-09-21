"""Adapter between a Research Lab hypothesis and the existing MiroFish engine."""
from typing import Dict, Any
from ..simulation_manager import SimulationManager
from ...models.project import ProjectManager
from .repository import ResearchRepository

class ResearchSimulationAdapter:
    @staticmethod
    def create(hypothesis: Dict[str, Any], project_id: str, graph_id: str = None,
               enable_twitter: bool = True, enable_reddit: bool = True) -> Dict[str, Any]:
        project = ProjectManager.get_project(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")
        resolved_graph = graph_id or project.graph_id
        if not resolved_graph:
            raise ValueError("Project has no graph. Build the Zep graph before simulating a hypothesis.")

        requirement = (
            "RESEARCH LAB HYPOTHESIS\n"
            f"Domain: {hypothesis.get('domain', 'toyt')}\n"
            f"Category: {hypothesis.get('category')}\n"
            f"Hypothesis: {hypothesis.get('statement')}\n\n"
            "Goal: explore plausible reactions, mechanisms, objections and second-order effects. "
            "Do not treat simulated behavior as empirical proof. Explicitly surface assumptions and uncertainty."
        )
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
