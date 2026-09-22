"""Close the Research Lab loop after a completed synthetic report."""
from typing import Any, Dict, Optional
from .report_finding_bridge import ReportFindingBridge
from .epistemic_evaluator import EpistemicEvaluator
from .repository import ResearchRepository


class ResearchReportLoop:
    @staticmethod
    def process(simulation_id: str, report_id: str, markdown_content: str) -> Optional[Dict[str, Any]]:
        finding = ReportFindingBridge.import_report(
            simulation_id=simulation_id,
            report_id=report_id,
            markdown_content=markdown_content,
        )
        link = ResearchRepository.get("simulation_links", simulation_id)
        if not link:
            return None
        hypothesis_id = link["hypothesis_id"]
        hypothesis = ResearchRepository.get("hypotheses", hypothesis_id)
        if not hypothesis:
            return None
        evidence = [
            e for e in ResearchRepository.list("evidence")
            if hypothesis_id in e.get("hypothesis_ids", [])
        ]
        findings = [
            f for f in ResearchRepository.list("findings")
            if f.get("hypothesis_id") == hypothesis_id
        ]
        assessment = EpistemicEvaluator.evaluate(hypothesis, evidence, findings)
        ResearchRepository.update("hypotheses", hypothesis_id, {"status": assessment["status"]})
        return {
            "finding": finding,
            "assessment": assessment,
            "epistemic_notice": (
                "The report and its finding are synthetic outputs. "
                "Hypothesis status is recalculated conservatively; simulation alone cannot establish support."
            ),
        }
