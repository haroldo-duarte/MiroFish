from types import SimpleNamespace
from app.services.research.npc_adapter import Provenance, SyntheticAgentSeed
from app.services.research.world_agent_pipeline import WorldFact, WorldSnapshot
from app.services.research.research_zep_world_bridge import ResearchZepWorldBridge


def test_episode_metadata_preserves_fact_epistemics_and_provenance():
    snapshot = WorldSnapshot(facts=[WorldFact(
        fact_type="session", semantic_class="observed_event",
        data={"status": "done"}, source="npc", source_key="sessions",
        observed_at="2026-09-01T10:00:00Z"
    )])
    episode = ResearchZepWorldBridge.episodes(snapshot)[0]
    assert episode.metadata["epistemic_class"] == "observed_event"
    assert episode.metadata["source"] == "npc"
    assert episode.metadata["source_key"] == "sessions"
    assert '"semantic_class": "observed_event"' in episode.data


def test_synthetic_seed_is_explicitly_synthetic():
    seed = SyntheticAgentSeed(
        archetype="therapist", cohort="fono",
        provenance=[Provenance(source="npc", source_key="professionals")]
    )
    episode = ResearchZepWorldBridge.episodes(WorldSnapshot(agent_seeds=[seed]))[0]
    assert episode.metadata["epistemic_class"] == "synthetic"
    assert episode.metadata["mirofish_kind"] == "synthetic_agent_seed"
    assert "synthetic agent; not a real person" in episode.data


def test_bridge_delegates_to_existing_graph_builder():
    class Builder:
        def add_research_episodes(self, graph_id, episodes, batch_size=350):
            return (graph_id, episodes, batch_size)
    result = ResearchZepWorldBridge.ingest(Builder(), "graph_1", WorldSnapshot(), 10)
    assert result[0] == "graph_1"
    assert result[2] == 10
