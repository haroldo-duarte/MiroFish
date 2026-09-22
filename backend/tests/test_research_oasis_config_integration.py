import json
from app.services.research.npc_adapter import SyntheticAgentSeed, Provenance
from app.services.research.research_oasis_config_integration import ResearchOasisConfigIntegration


def test_writes_profiles_consumed_by_oasis_runner(tmp_path):
    seed = SyntheticAgentSeed(
        archetype="therapist", cohort="fono",
        goals=["resolve pending work"],
        provenance=[Provenance(source="npc", source_key="professionals")],
    )
    profiles, manifest = ResearchOasisConfigIntegration.write_profiles(str(tmp_path), [seed])
    assert (tmp_path / "reddit_profiles.json").exists()
    assert (tmp_path / "twitter_profiles.csv").exists()
    reddit = json.loads((tmp_path / "reddit_profiles.json").read_text())
    assert reddit[0]["user_id"] == profiles[0].user_id
    assert "SYNTHETIC RESEARCH AGENT" in reddit[0]["persona"]
    assert manifest["epistemic_class"] == "synthetic"


def test_manifest_preserves_research_memory_provenance(tmp_path):
    seed = SyntheticAgentSeed(
        archetype="unit_manager", cohort="unit_a",
        memory_summary=[{"event_type": "pending_item", "count": 3}],
        provenance=[Provenance(source="npc", source_key="pending_work", extraction_version="npc-v1")],
    )
    _, manifest = ResearchOasisConfigIntegration.write_profiles(
        str(tmp_path), [seed], enable_twitter=False
    )
    agent = manifest["agents"][0]
    assert agent["memory"]["provenance"][0]["source_key"] == "pending_work"
    assert agent["memory"]["epistemic_notice"].startswith("synthetic memory")
    assert not (tmp_path / "twitter_profiles.csv").exists()
