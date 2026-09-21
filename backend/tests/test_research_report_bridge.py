"""Tests for Research Lab report bridge and priority behavior."""
from app.services.research.epistemic_evaluator import EpistemicEvaluator

def test_simulation_report_is_not_empirical_support():
    h = {"hypothesis_id": "h1"}
    result = EpistemicEvaluator.evaluate(h, [], [{
        "source_type": "simulation_report",
        "direction": "supports",
    }])
    assert result["status"] == "signal"

def test_real_evidence_outranks_simulated_signal():
    h = {"hypothesis_id": "h1"}
    result = EpistemicEvaluator.evaluate(h, [{
        "evidence_type": "experiment",
        "direction": "contradicts",
    }], [{
        "source_type": "simulation_report",
        "direction": "supports",
    }])
    assert result["status"] == "inconclusive"
    assert result["contradiction_score"] > result["support_score"]
