"""Convert completed MiroFish reports into traceable Research Lab findings."""
from typing import Dict, Any, Optional
from ...models.finding import Finding
from .repository import ResearchRepository

class ReportFindingBridge:
    @staticmethod
    def import_report(simulation_id: str, report_id: str, markdown_content: str,
                      direction: str = "inconclusive", confidence: str = "low") -> Optional[Dict[str, Any]]:
        link = ResearchRepository.get("simulation_links", simulation_id)
        if not link:
            return None
        hid = link["hypothesis_id"]
        # Idempotency: a report can only generate one bridge finding.
        existing = [
            f for f in ResearchRepository.list("findings")
            if f.get("source_type") == "simulation_report" and f.get("source_id") == report_id
        ]
        if existing:
            return existing[0]

        compact = " ".join((markdown_content or "").split())
        statement = compact[:1200] if compact else "Simulation report completed; review report for details."
        item = Finding(
            hypothesis_id=hid,
            statement=statement,
            source_type="simulation_report",
            source_id=report_id,
            direction=direction,
            confidence=confidence,
            limitations=[
                "Derived from synthetic simulation, not empirical observation.",
                "Sensitive to agent personas, graph context and simulation assumptions.",
            ],
        ).to_dict()
        hypothesis = ResearchRepository.get("hypotheses", hid) or {}
        item["domain"] = hypothesis.get("domain", "toyt")
        return ResearchRepository.create("findings", item)
