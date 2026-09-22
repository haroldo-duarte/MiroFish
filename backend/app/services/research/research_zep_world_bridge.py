"""Zep ingestion boundary for Research Lab WorldSnapshot data.

Uses the existing GraphBuilderService Batch API while preserving epistemic
class and provenance in each independently submitted graph episode.
"""
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, List
from ..graph_builder import GraphBuilderService, BatchSubmission
from .world_agent_pipeline import WorldSnapshot


@dataclass(frozen=True)
class ResearchGraphEpisode:
    data: str
    metadata: Dict[str, Any]


class ResearchZepWorldBridge:
    @staticmethod
    def episodes(snapshot: WorldSnapshot) -> List[ResearchGraphEpisode]:
        episodes: List[ResearchGraphEpisode] = []
        for fact in snapshot.facts:
            provenance = {
                "source": fact.source,
                "source_key": fact.source_key,
                "observed_at": fact.observed_at,
            }
            envelope = {
                "kind": "observed_world_fact",
                "fact_type": fact.fact_type,
                "semantic_class": fact.semantic_class,
                "data": fact.data,
                "provenance": provenance,
            }
            data = json.dumps(envelope, ensure_ascii=False, sort_keys=True)
            episodes.append(ResearchGraphEpisode(data=data, metadata={
                "mirofish_kind": "observed_world_fact",
                "epistemic_class": fact.semantic_class,
                "source": fact.source,
                "source_key": fact.source_key,
                "observed_at": fact.observed_at,
                "payload_sha256": hashlib.sha256(data.encode("utf-8")).hexdigest(),
            }))
        for seed in snapshot.agent_seeds:
            provenance = [
                {
                    "source": p.source, "source_key": p.source_key,
                    "observed_at": p.observed_at,
                    "extraction_version": p.extraction_version,
                } for p in seed.provenance
            ]
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
                "provenance": provenance,
                "epistemic_notice": "synthetic agent; not a real person",
            }
            data = json.dumps(envelope, ensure_ascii=False, sort_keys=True)
            episodes.append(ResearchGraphEpisode(data=data, metadata={
                "mirofish_kind": "synthetic_agent_seed",
                "epistemic_class": "synthetic",
                "archetype": seed.archetype,
                "cohort": seed.cohort,
                "payload_sha256": hashlib.sha256(data.encode("utf-8")).hexdigest(),
            }))
        return episodes

    @classmethod
    def ingest(cls, builder: GraphBuilderService, graph_id: str,
               snapshot: WorldSnapshot, batch_size: int = 350) -> BatchSubmission:
        episodes = cls.episodes(snapshot)
        return builder.add_research_episodes(graph_id, episodes, batch_size=batch_size)
