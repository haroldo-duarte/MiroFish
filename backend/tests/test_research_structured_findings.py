from app.services.research.structured_simulation_finding import StructuredSimulationFinding
from app.services.research.epistemic_evaluator import EpistemicEvaluator


def test_structured_finding_defaults_conservatively():
    value = StructuredSimulationFinding.validate({})
    assert value["direction"] == "inconclusive"
    assert value["confidence"] == "low"


def test_simulation_finding_is_counted_in_simulation_provenance_but_not_proof():
    h = {"hypothesis_id": "h1"}
    findings = [{"source_type": "simulation_report", "direction": "supports"}]
    result = EpistemicEvaluator.evaluate(h, [], findings)
    assert result["provenance"]["simulation"] == 1
    assert result["status"] == "signal"


def test_real_evidence_plus_simulation_can_be_supported():
    h = {"hypothesis_id": "h1"}
    evidence = [{"evidence_type": "measurement", "direction": "supports"}]
    findings = [{"source_type": "simulation_report", "direction": "supports"}]
    result = EpistemicEvaluator.evaluate(h, evidence, findings)
    assert result["provenance"]["real"] == 1
    assert result["provenance"]["simulation"] == 1
    assert result["status"] == "supported"
