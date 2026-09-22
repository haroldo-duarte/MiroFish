from app.services.research.agent_seed_builder import SyntheticAgentSeedBuilder
from app.services.research.npc_adapter import NormalizedRecord, Provenance


def rec(kind, semantic):
    return NormalizedRecord(kind, semantic, {"secret": "must-not-leak"}, Provenance("test", "anon"))


def test_agent_seed_uses_only_human_behavior_for_behavioral_signals():
    seed = SyntheticAgentSeedBuilder.build("therapist", "cohort-a", [
        rec("message_response", "human_behavior"),
        rec("remanejamento_round", "algorithmic_process"),
        rec("session", "observed_event"),
    ])
    assert seed.behavioral_signals["observed_behavior_events"] == 1
    assert seed.behavioral_signals["event_types"] == {"message_response": 1}


def test_agent_seed_does_not_copy_raw_payload_into_persona():
    seed = SyntheticAgentSeedBuilder.build("therapist", "cohort-a", [rec("x", "human_behavior")])
    assert "secret" not in str(seed.behavioral_signals)
