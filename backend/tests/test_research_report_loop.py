from app.services.research.repository import ResearchRepository
from app.services.research.research_report_loop import ResearchReportLoop


def test_report_loop_creates_finding_and_reassesses_as_signal(tmp_path, monkeypatch):
    monkeypatch.setattr(ResearchRepository, "ROOT", str(tmp_path))
    ResearchRepository.create("hypotheses", {
        "hypothesis_id": "hyp_1", "status": "untested", "domain": "npc"
    })
    ResearchRepository.create("simulation_links", {
        "simulation_id": "sim_1", "hypothesis_id": "hyp_1"
    })
    result = ResearchReportLoop.process("sim_1", "report_1", "Synthetic result suggests a pattern.")
    assert result["finding"]["source_type"] == "simulation_report"
    assert result["assessment"]["status"] == "untested"
    assert ResearchRepository.get("hypotheses", "hyp_1")["status"] == "untested"


def test_report_loop_is_idempotent_for_same_report(tmp_path, monkeypatch):
    monkeypatch.setattr(ResearchRepository, "ROOT", str(tmp_path))
    ResearchRepository.create("hypotheses", {
        "hypothesis_id": "hyp_1", "status": "untested", "domain": "npc"
    })
    ResearchRepository.create("simulation_links", {
        "simulation_id": "sim_1", "hypothesis_id": "hyp_1"
    })
    ResearchReportLoop.process("sim_1", "report_1", "one")
    ResearchReportLoop.process("sim_1", "report_1", "two")
    assert len(ResearchRepository.list("findings")) == 1


def test_real_evidence_can_promote_status_after_simulation(tmp_path, monkeypatch):
    monkeypatch.setattr(ResearchRepository, "ROOT", str(tmp_path))
    ResearchRepository.create("hypotheses", {
        "hypothesis_id": "hyp_1", "status": "untested", "domain": "npc"
    })
    ResearchRepository.create("simulation_links", {
        "simulation_id": "sim_1", "hypothesis_id": "hyp_1"
    })
    ResearchRepository.create("evidence", {
        "evidence_id": "ev_1", "evidence_type": "measurement",
        "direction": "supports", "hypothesis_ids": ["hyp_1"]
    })
    result = ResearchReportLoop.process("sim_1", "report_1", "synthetic")
    assert result["assessment"]["status"] == "supported"
