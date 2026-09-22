"""Build relationship and memory inputs without turning raw rows into personas."""
from collections import Counter
from typing import Iterable, List
from .npc_adapter import NormalizedRecord, SyntheticAgentSeed


class ResearchContextEnricher:
    @staticmethod
    def enrich(seed: SyntheticAgentSeed, records: Iterable[NormalizedRecord]) -> SyntheticAgentSeed:
        records = list(records)
        relation_counts = Counter()
        memory_counts = Counter()
        for record in records:
            payload = record.payload or {}
            relation = payload.get("relationship_type")
            if relation:
                relation_counts[str(relation)] += 1
            if record.semantic_class == "observed_event":
                memory_counts[record.record_type] += 1
        seed.relationship_edges = [
            {"relationship_type": key, "observed_count": count, "synthetic": True}
            for key, count in sorted(relation_counts.items())
        ]
        seed.memory_summary = [
            {"event_type": key, "observed_count": count, "source_kind": "observed_event"}
            for key, count in sorted(memory_counts.items())
        ]
        return seed
