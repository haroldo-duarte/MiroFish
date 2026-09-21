"""Research Lab evidence domain model."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Optional
import uuid

@dataclass
class Evidence:
    title: str
    evidence_type: str
    summary: str
    domain: str = "toyt"
    source: Optional[str] = None
    confidence: str = "unknown"
    direction: str = "neutral"
    hypothesis_ids: List[str] = field(default_factory=list)
    evidence_id: str = field(default_factory=lambda: f"ev_{uuid.uuid4().hex[:12]}")
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self):
        return asdict(self)
