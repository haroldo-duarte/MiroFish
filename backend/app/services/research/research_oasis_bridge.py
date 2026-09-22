"""Safe bridge from Research Lab synthetic seeds to the existing OASIS profile model.

The bridge is deterministic: it does not invent demographics, MBTI, names of
real people, or social metrics. Research cohorts remain explicitly synthetic.
"""
import hashlib
import json
from typing import Any, Dict, Iterable, List
from ..oasis_profile_generator import OasisAgentProfile
from .npc_adapter import SyntheticAgentSeed


class ResearchOasisBridge:
    @staticmethod
    def _stable_id(archetype: str, cohort: str, ordinal: int) -> int:
        digest = hashlib.sha256(f"{archetype}:{cohort}:{ordinal}".encode()).hexdigest()
        return int(digest[:8], 16) % 2_000_000_000 + 1

    @classmethod
    def profile(cls, seed: SyntheticAgentSeed, ordinal: int = 0) -> OasisAgentProfile:
        user_id = cls._stable_id(seed.archetype, seed.cohort, ordinal)
        label = f"{seed.archetype} cohort {seed.cohort}"
        evidence = json.dumps(seed.behavioral_signals, ensure_ascii=False, sort_keys=True)
        constraints = "; ".join(seed.constraints) or "none specified"
        goals = "; ".join(seed.goals) or "none specified"
        persona = (
            f"SYNTHETIC RESEARCH AGENT. Archetype: {seed.archetype}. Cohort: {seed.cohort}. "
            f"Observed aggregate behavioral signals: {evidence}. Goals: {goals}. "
            f"Constraints: {constraints}. Never claim to be a specific real person."
        )
        return OasisAgentProfile(
            user_id=user_id,
            user_name=f"research_{seed.archetype}_{user_id}",
            name=label,
            bio=f"Synthetic {seed.archetype} research cohort",
            persona=persona,
            profession=seed.archetype,
            interested_topics=list(seed.goals),
        )

    @classmethod
    def profiles(cls, seeds: Iterable[SyntheticAgentSeed]) -> List[OasisAgentProfile]:
        return [cls.profile(seed, i) for i, seed in enumerate(seeds)]

    @staticmethod
    def memory_payload(seed: SyntheticAgentSeed) -> Dict[str, Any]:
        return {
            "kind": "synthetic_agent_memory_seed",
            "archetype": seed.archetype,
            "cohort": seed.cohort,
            "memory_summary": list(seed.memory_summary),
            "relationship_edges": list(seed.relationship_edges),
            "provenance": [
                {
                    "source": p.source,
                    "source_key": p.source_key,
                    "observed_at": p.observed_at,
                    "extraction_version": p.extraction_version,
                }
                for p in seed.provenance
            ],
            "epistemic_notice": "synthetic memory derived from normalized research sources",
        }
