from app.services.research.repository import ResearchRepository
from app.services.research.research_runtime_flow import ResearchRuntimeFlow


def test_non_research_simulation_keeps_existing_runtime(monkeypatch):
    monkeypatch.setattr(ResearchRepository, "get", classmethod(lambda cls, c, i: None))
    assert ResearchRuntimeFlow.start_policy("sim_normal", "graph_1", 12) is None


def test_research_simulation_forces_parallel_rounds_and_graph_memory(monkeypatch):
    link = {"simulation_id": "sim_1", "hypothesis_id": "hyp_1", "source_snapshot_id": "snap_1"}
    monkeypatch.setattr(ResearchRepository, "get", classmethod(lambda cls, c, i: link))
    policy = ResearchRuntimeFlow.start_policy("sim_1", "graph_1", 25)
    assert policy["platform"] == "parallel"
    assert policy["max_rounds"] == 25
    assert policy["enable_graph_memory_update"] is True
    assert policy["graph_id"] == "graph_1"
    assert policy["research_envelope"]["epistemic_type"] == "synthetic_simulation"
    assert policy["research_envelope"]["hypothesis_id"] == "hyp_1"
