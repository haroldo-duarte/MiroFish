"""Conservative epistemic evaluation for Research Lab.

This evaluator deliberately does not let a simulation become "proof".
It aggregates traceable findings/evidence and keeps provenance explicit.
"""
from typing import Dict, Any, List

REAL_EVIDENCE = {"experiment", "observational", "measurement"}
EXTERNAL_EVIDENCE = {"literature", "external_research"}
SIMULATED_EVIDENCE = {"simulation"}

class EpistemicEvaluator:
    @staticmethod
    def evaluate(hypothesis: Dict[str, Any], evidence: List[Dict[str, Any]], findings: List[Dict[str, Any]]):
        support = 0.0
        contradict = 0.0
        provenance = {"real": 0, "external": 0, "simulation": 0, "other": 0}

        for item in evidence:
            et = str(item.get("evidence_type", "")).lower()
            direction = str(item.get("direction", "neutral")).lower()
            weight = 3.0 if et in REAL_EVIDENCE else 2.0 if et in EXTERNAL_EVIDENCE else 0.5 if et in SIMULATED_EVIDENCE else 1.0
            bucket = "real" if et in REAL_EVIDENCE else "external" if et in EXTERNAL_EVIDENCE else "simulation" if et in SIMULATED_EVIDENCE else "other"
            provenance[bucket] += 1
            if direction == "supports":
                support += weight
            elif direction == "contradicts":
                contradict += weight

        for item in findings:
            direction = str(item.get("direction", "inconclusive")).lower()
            source_type = str(item.get("source_type", "")).lower()
            weight = 0.5 if source_type in {"simulation", "simulation_report"} else 1.0
            if direction == "supports":
                support += weight
            elif direction == "contradicts":
                contradict += weight

        if support == 0 and contradict == 0:
            status = "untested"
        elif support > 0 and contradict > 0:
            status = "inconclusive"
        elif support > 0:
            # Simulation-only support remains a signal, never "supported".
            status = "signal" if provenance["real"] == 0 and provenance["external"] == 0 else "supported"
        else:
            status = "contradicted" if provenance["real"] > 0 or provenance["external"] > 0 else "signal"

        return {
            "hypothesis_id": hypothesis["hypothesis_id"],
            "status": status,
            "support_score": support,
            "contradiction_score": contradict,
            "provenance": provenance,
            "note": "Simulation evidence is intentionally down-weighted and cannot alone mark a hypothesis as supported.",
        }
