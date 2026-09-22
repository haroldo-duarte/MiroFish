import json
from app.services.research.npc_adapter import NormalizedRecord, Provenance
from app.services.research.world_agent_pipeline import WorldAgentPipeline
from app.services.research.graph_source_serializer import world_snapshot_to_graph_text


def record(kind, semantic, source_key, payload=None):
    return NormalizedRecord(kind, semantic, payload or {}, Provenance("npc", source_key, "2026-01-01T00:00:00Z"))


def test_pipeline_separates_world_facts_from_human_behavior():
    snapshot = WorldAgentPipeline.build([
        record("session", "observed_event", "sessions", {"status": "done"}),
        record("allocation_iteration", "algorithmic_process", "remanejamento", {"round": 2}),
        record("response", "human_behavior", "communications", {"latency_bucket": "fast"}),
    ], {"therapists": {"archetype": "therapist", "source_keys": ["communications"]}})
    assert [f.fact_type for f in snapshot.facts] == ["session", "allocation_iteration"]
    assert snapshot.agent_seeds[0].behavioral_signals["observed_behavior_events"] == 1


def test_graph_text_preserves_provenance_and_marks_agents_synthetic():
    snapshot = WorldAgentPipeline.build(
        [record("response", "human_behavior", "communications")],
        {"therapists": {"archetype": "therapist", "source_keys": ["communications"]}},
    )
    text = world_snapshot_to_graph_text(snapshot)
    assert '"epistemic_notice": "synthetic agent; not a real person"' in text
    assert '"source_key": "communications"' in text


def test_algorithmic_process_never_becomes_agent_behavior():
    snapshot = WorldAgentPipeline.build(
        [record("allocation_iteration", "algorithmic_process", "remanejamento")],
        {"managers": {"archetype": "unit_manager", "source_keys": ["remanejamento"]}},
    )
    assert snapshot.agent_seeds[0].behavioral_signals["observed_behavior_events"] == 0
