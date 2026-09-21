"""Research Lab hypothesis domain model."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import List
import uuid

class HypothesisStatus(str, Enum):
    UNTESTED = "untested"
    SIGNAL = "signal"
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    INCONCLUSIVE = "inconclusive"

class HypothesisCategory(str, Enum):
    PRODUCT = "product"
    UX = "ux"
    CLINICAL = "clinical"
    BEHAVIOR = "behavior"
    MARKET = "market"
    PRICING = "pricing"
    DISTRIBUTION = "distribution"
    ECONOMICS = "economics"

@dataclass
class Hypothesis:
    statement: str
    category: str
    domain: str = "toyt"
    importance: str = "medium"
    status: str = HypothesisStatus.UNTESTED.value
    hypothesis_id: str = field(default_factory=lambda: f"hyp_{uuid.uuid4().hex[:12]}")
    evidence_ids: List[str] = field(default_factory=list)
    simulation_ids: List[str] = field(default_factory=list)
    experiment_ids: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self):
        return asdict(self)
