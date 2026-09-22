"""Persist Research Lab synthetic seeds into the OASIS files actually used by the runner."""
import json
import os
from typing import Iterable
from .npc_adapter import SyntheticAgentSeed
from .research_oasis_bridge import ResearchOasisBridge
from ..oasis_profile_generator import OasisProfileGenerator


class ResearchOasisConfigIntegration:
    @classmethod
    def write_profiles(cls, simulation_dir: str, seeds: Iterable[SyntheticAgentSeed],
                       enable_reddit: bool = True, enable_twitter: bool = True):
        seeds = list(seeds)
        profiles = ResearchOasisBridge.profiles(seeds)
        generator = OasisProfileGenerator.__new__(OasisProfileGenerator)
        os.makedirs(simulation_dir, exist_ok=True)
        if enable_reddit:
            generator.save_profiles(
                profiles, os.path.join(simulation_dir, "reddit_profiles.json"), "reddit"
            )
        if enable_twitter:
            generator.save_profiles(
                profiles, os.path.join(simulation_dir, "twitter_profiles.csv"), "twitter"
            )
        manifest = {
            "epistemic_class": "synthetic",
            "profiles_count": len(profiles),
            "agents": [
                {
                    "user_id": p.user_id,
                    "archetype": seed.archetype,
                    "cohort": seed.cohort,
                    "memory": ResearchOasisBridge.memory_payload(seed),
                }
                for p, seed in zip(profiles, seeds)
            ],
        }
        with open(os.path.join(simulation_dir, "research_agent_manifest.json"), "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
        return profiles, manifest
