"""Contracts for the future Neuropsicocentro Supabase adapter.

No credentials or network calls live here. Runtime implementations must use
server-side, read-only access and emit normalized records with provenance.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Provenance:
    source: str
    source_key: str
    observed_at: Optional[str] = None
    extraction_version: str = "npc-v1"


@dataclass
class NormalizedRecord:
    record_type: str
    semantic_class: str
    payload: Dict[str, Any]
    provenance: Provenance
    pii_removed: bool = True


@dataclass
class SyntheticAgentSeed:
    archetype: str
    cohort: str
    goals: List[str] = field(default_factory=list)
    incentives: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    behavioral_signals: Dict[str, Any] = field(default_factory=dict)
    relationship_edges: List[Dict[str, Any]] = field(default_factory=list)
    memory_summary: List[Dict[str, Any]] = field(default_factory=list)
    provenance: List[Provenance] = field(default_factory=list)


class NPCSourceAdapter:
    """Interface implemented later by snapshot and live Supabase adapters."""

    def health(self) -> Dict[str, Any]:
        raise NotImplementedError

    def snapshot(self, source_key: str, since: Optional[str] = None) -> List[NormalizedRecord]:
        raise NotImplementedError

    def watermark(self, source_key: str) -> Optional[str]:
        raise NotImplementedError
