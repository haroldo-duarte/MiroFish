"""Research Lab experiment domain model."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Optional
import uuid

@dataclass
class Experiment:
    name: str
    hypothesis_ids: List[str]
    method: str
    domain: str = "toyt"
    status: str = "planned"
    metric: Optional[str] = None
    result: Optional[str] = None
    experiment_id: str = field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:12]}")
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self):
        return asdict(self)
