"""Build safe synthetic-agent seeds from normalized NPC records."""
from collections import Counter
from typing import Iterable, List
from .npc_adapter import NormalizedRecord, SyntheticAgentSeed
from .source_semantics import can_infer_agent_behavior


class SyntheticAgentSeedBuilder:
    @staticmethod
    def build(archetype: str, cohort: str, records: Iterable[NormalizedRecord]) -> SyntheticAgentSeed:
        records = list(records)
        behavioral = [r for r in records if can_infer_agent_behavior(r.semantic_class)]
        counts = Counter(r.record_type for r in behavioral)
        provenance = [r.provenance for r in records]
        # Deliberately conservative: raw payload fields are not copied into a persona.
        # Derived behavioral features must be explicitly implemented and reviewed.
        return SyntheticAgentSeed(
            archetype=archetype,
            cohort=cohort,
            behavioral_signals={"observed_behavior_events": len(behavioral), "event_types": dict(counts)},
            provenance=provenance,
        )
