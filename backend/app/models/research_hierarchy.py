"""Research hierarchy: Domain → Study → Research Question → Hypothesis."""
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Optional
import uuid


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ResearchDomain:
    name: str
    slug: str
    description: str = ""
    domain_id: str = field(default_factory=lambda: _id("dom"))
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self):
        return asdict(self)


@dataclass
class Study:
    domain_id: str
    title: str
    problem: str = ""
    status: str = "active"
    study_id: str = field(default_factory=lambda: _id("study"))
    source_keys: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self):
        return asdict(self)


@dataclass
class ResearchQuestion:
    study_id: str
    question: str
    question_id: str = field(default_factory=lambda: _id("rq"))
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self):
        return asdict(self)
