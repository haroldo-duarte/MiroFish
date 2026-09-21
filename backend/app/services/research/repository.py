"""Simple JSON persistence for Research Lab MVP.

Kept deliberately separate from ProjectManager so the existing MiroFish
project/simulation pipeline remains untouched.
"""
import json
import os
import threading
from typing import Dict, Any, List, Optional
from ...config import Config

class ResearchRepository:
    _lock = threading.RLock()
    ROOT = os.path.join(Config.UPLOAD_FOLDER, "research")
    COLLECTIONS = {"hypotheses", "evidence", "experiments"}

    @classmethod
    def _path(cls, collection: str) -> str:
        if collection not in cls.COLLECTIONS:
            raise ValueError(f"Unknown research collection: {collection}")
        os.makedirs(cls.ROOT, exist_ok=True)
        return os.path.join(cls.ROOT, f"{collection}.json")

    @classmethod
    def _read(cls, collection: str) -> List[Dict[str, Any]]:
        path = cls._path(collection)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def list(cls, collection: str, domain: Optional[str] = None):
        with cls._lock:
            rows = cls._read(collection)
        return [r for r in rows if not domain or r.get("domain") == domain]

    @classmethod
    def create(cls, collection: str, item: Dict[str, Any]):
        with cls._lock:
            rows = cls._read(collection)
            rows.append(item)
            path = cls._path(collection)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)
        return item
