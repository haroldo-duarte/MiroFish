import pytest
from app.services.research.npc_adapter import NormalizedRecord, Provenance
from app.services.research.privacy_guard import ResearchPrivacyError, ResearchPrivacyGuard
from app.services.research.world_agent_pipeline import WorldAgentPipeline


def rec(payload, pii_removed=True):
    return NormalizedRecord(
        record_type="session",
        semantic_class="observed_event",
        payload=payload,
        provenance=Provenance(source="npc", source_key="sessions"),
        pii_removed=pii_removed,
    )


def test_rejects_record_not_certified_pii_removed():
    with pytest.raises(ResearchPrivacyError):
        ResearchPrivacyGuard.assert_safe_record(rec({"status": "done"}, False))


def test_rejects_top_level_direct_identifier():
    with pytest.raises(ResearchPrivacyError, match="cpf"):
        ResearchPrivacyGuard.assert_safe_record(rec({"cpf": "00000000000"}))


def test_rejects_nested_identifier_inside_list():
    with pytest.raises(ResearchPrivacyError, match="email"):
        ResearchPrivacyGuard.assert_safe_record(rec({"events": [{"email": "x@example.test"}]}))


def test_safe_operational_fields_reach_world_snapshot():
    record = rec({"status": "done", "unit_id": "unit_1", "duration_minutes": 40})
    snapshot = WorldAgentPipeline.build([record], {})
    assert snapshot.facts[0].data["duration_minutes"] == 40
