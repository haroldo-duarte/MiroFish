"""Deterministic bridge from normalized real sources to MiroFish world inputs.

This layer does not call an LLM and does not create empirical claims. It
preserves provenance and keeps observed data separate from synthetic state.
"""
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Iterable, List
from .npc_adapter import NormalizedRecord, SyntheticAgentSeed
from .agent_seed_builder import SyntheticAgentSeedBuilder
from .source_semantics import SourceSemanticClass
from .privacy_guard import ResearchPrivacyGuard


@dataclass
class WorldFact:
    fact_type: str
    semantic_class: str
    data: Dict[str, Any]
    source: str
    source_key: str
    observed_at: str | None = None

    def to_dict(self):
        return asdict(self)


@dataclass
class WorldSnapshot:
    facts: List[WorldFact] = field(default_factory=list)
    agent_seeds: List[SyntheticAgentSeed] = field(default_factory=list)

    def to_dict(self):
        return {
            "facts": [f.to_dict() for f in self.facts],
            "agent_seeds": [asdict(a) for a in self.agent_seeds],
        }


class WorldAgentPipeline:
    WORLD_CLASSES = {
        SourceSemanticClass.WORLD_STATE.value,
        SourceSemanticClass.WORLD_RULE.value,
        SourceSemanticClass.OBSERVED_EVENT.value,
        SourceSemanticClass.ALGORITHMIC_PROCESS.value,
    }

    @classmethod
    def build(cls, records: Iterable[NormalizedRecord], cohorts: Dict[str, Dict[str, str]]) -> WorldSnapshot:
        records = list(records)
        ResearchPrivacyGuard.assert_safe_records(records)
        facts = [
            WorldFact(
                fact_type=r.record_type,
                semantic_class=r.semantic_class,
                data=dict(r.payload),
                source=r.provenance.source,
                source_key=r.provenance.source_key,
                observed_at=r.provenance.observed_at,
            )
            for r in records if r.semantic_class in cls.WORLD_CLASSES
        ]
        seeds = []
        for cohort, config in cohorts.items():
            allowed_sources = set(config.get("source_keys") or [])
            scoped = [r for r in records if not allowed_sources or r.provenance.source_key in allowed_sources]
            seeds.append(SyntheticAgentSeedBuilder.build(config["archetype"], cohort, scoped))
        return WorldSnapshot(facts=facts, agent_seeds=seeds)
