"""Serialize a safe world snapshot into source text for the existing Zep graph builder."""
import json
from typing import Dict, Any
from .world_agent_pipeline import WorldSnapshot


def world_snapshot_to_graph_text(snapshot: WorldSnapshot) -> str:
    lines = ["MIROFISH RESEARCH WORLD SNAPSHOT"]
    for fact in snapshot.facts:
        envelope: Dict[str, Any] = {
            "kind": "observed_world_fact",
            "fact_type": fact.fact_type,
            "semantic_class": fact.semantic_class,
            "data": fact.data,
            "provenance": {
                "source": fact.source,
                "source_key": fact.source_key,
                "observed_at": fact.observed_at,
            },
        }
        lines.append(json.dumps(envelope, ensure_ascii=False, sort_keys=True))
    for seed in snapshot.agent_seeds:
        envelope = {
            "kind": "synthetic_agent_seed",
            "archetype": seed.archetype,
            "cohort": seed.cohort,
            "goals": seed.goals,
            "incentives": seed.incentives,
            "constraints": seed.constraints,
            "behavioral_signals": seed.behavioral_signals,
            "relationship_edges": seed.relationship_edges,
            "memory_summary": seed.memory_summary,
            "provenance": [
                {"source": p.source, "source_key": p.source_key, "observed_at": p.observed_at,
                 "extraction_version": p.extraction_version}
                for p in seed.provenance
            ],
            "epistemic_notice": "synthetic agent; not a real person",
        }
        lines.append(json.dumps(envelope, ensure_ascii=False, sort_keys=True))
    return "\n".join(lines)
