"""Tests for Research Lab epistemic rules."""
from app.services.research.epistemic_evaluator import EpistemicEvaluator

def _hypothesis():
    return {"hypothesis_id": "hyp_test", "statement": "Test"}

def test_simulation_alone_is_only_signal():
    result = EpistemicEvaluator.evaluate(
        _hypothesis(),
        [{"evidence_type": "simulation", "direction": "supports"}],
        [],
    )
    assert result["status"] == "signal"

def test_real_experiment_can_support():
    result = EpistemicEvaluator.evaluate(
        _hypothesis(),
        [{"evidence_type": "experiment", "direction": "supports"}],
        [],
    )
    assert result["status"] == "supported"

def test_conflicting_evidence_is_inconclusive():
    result = EpistemicEvaluator.evaluate(
        _hypothesis(),
        [
            {"evidence_type": "experiment", "direction": "supports"},
            {"evidence_type": "literature", "direction": "contradicts"},
        ],
        [],
    )
    assert result["status"] == "inconclusive"
