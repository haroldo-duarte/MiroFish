from app.services.research.npc_adapter import Provenance, NormalizedRecord, SyntheticAgentSeed
from app.services.research.research_oasis_bridge import ResearchOasisBridge
from app.services.research.context_enricher import ResearchContextEnricher


def test_oasis_bridge_is_deterministic_and_explicitly_synthetic():
    seed = SyntheticAgentSeed(archetype="therapist", cohort="fono_40h", behavioral_signals={"events": 3})
    a = ResearchOasisBridge.profile(seed)
    b = ResearchOasisBridge.profile(seed)
    assert a.user_id == b.user_id
    assert "SYNTHETIC RESEARCH AGENT" in a.persona
    assert a.age is None and a.gender is None and a.mbti is None


def test_memory_uses_aggregated_observed_events_not_raw_payload():
    p = Provenance("npc", "sessions", "2026-01-01T00:00:00Z")
    records = [NormalizedRecord("session", "observed_event", {"patient_name": "SHOULD_NOT_COPY"}, p)]
    seed = ResearchContextEnricher.enrich(SyntheticAgentSeed("therapist", "all"), records)
    assert seed.memory_summary == [{"event_type": "session", "observed_count": 1, "source_kind": "observed_event"}]
    assert "SHOULD_NOT_COPY" not in str(seed.memory_summary)


def test_relationships_are_aggregate_not_identity_edges():
    p = Provenance("npc", "groups")
    records = [
        NormalizedRecord("membership", "world_state", {"relationship_type": "works_with", "person": "A"}, p),
        NormalizedRecord("membership", "world_state", {"relationship_type": "works_with", "person": "B"}, p),
    ]
    seed = ResearchContextEnricher.enrich(SyntheticAgentSeed("therapist", "all"), records)
    assert seed.relationship_edges == [{"relationship_type": "works_with", "observed_count": 2, "synthetic": True}]
    assert "person" not in str(seed.relationship_edges)


def test_memory_payload_keeps_provenance_and_synthetic_notice():
    seed = SyntheticAgentSeed("therapist", "all", provenance=[Provenance("npc", "sessions")])
    payload = ResearchOasisBridge.memory_payload(seed)
    assert payload["provenance"][0]["source_key"] == "sessions"
    assert "synthetic" in payload["epistemic_notice"]
