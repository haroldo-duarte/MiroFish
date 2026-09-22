from app.services.simulation_runner import SimulationRunState, RoundSummary, RunnerStatus
from app.services.research.research_round_bridge import ResearchRoundBridge, ResearchRoundEnvelope


def test_round_bridge_enables_existing_graph_memory_and_parallel_oasis():
    kwargs = ResearchRoundBridge.start_kwargs("graph_123", max_rounds=12)
    assert kwargs == {
        "platform": "parallel",
        "max_rounds": 12,
        "enable_graph_memory_update": True,
        "graph_id": "graph_123",
    }


def test_round_summary_is_explicitly_synthetic_and_aggregated():
    state = SimulationRunState("sim_1", runner_status=RunnerStatus.RUNNING)
    state.rounds.append(RoundSummary(
        round_num=1, start_time="x", simulated_hour=1,
        active_agents=[1, 1, 2], actions=[]
    ))
    env = ResearchRoundEnvelope("sim_1", hypothesis_id="hyp_1", source_snapshot_id="snap_1")
    result = ResearchRoundBridge.summarize(state, env)
    assert result["envelope"]["epistemic_type"] == "synthetic_simulation"
    assert result["rounds"][0]["active_agents_count"] == 2
    assert "not empirical observations" in result["epistemic_notice"]


def test_simulation_finding_source_remains_simulation():
    assert ResearchRoundBridge.finding_source_type() == "simulation"
