"""Research Lab finding and epistemic assessment models."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Optional
import uuid

@dataclass
class Finding:
    hypothesis_id: str
    statement: str
    source_type: str
    source_id: str
    direction: str = "inconclusive"
    confidence: str = "unknown"
    limitations: List[str] = field(default_factory=list)
    finding_id: str = field(default_factory=lambda: f"find_{uuid.uuid4().hex[:12]}")
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self):
        return asdict(self)
