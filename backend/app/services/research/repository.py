"""JSON persistence for Research Lab MVP.

Kept deliberately separate from ProjectManager so the existing MiroFish
project/simulation pipeline remains untouched.
"""
import json
import os
import threading
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from ...config import Config

class ResearchRepository:
    _lock = threading.RLock()
    ROOT = os.path.join(Config.UPLOAD_FOLDER, "research")
    COLLECTIONS = {"hypotheses", "evidence", "experiments", "findings", "simulation_links"}
    ID_FIELDS = {
        "hypotheses": "hypothesis_id", "evidence": "evidence_id",
        "experiments": "experiment_id", "findings": "finding_id",
        "simulation_links": "simulation_id",
    }

    @classmethod
    def _path(cls, collection):
        if collection not in cls.COLLECTIONS:
            raise ValueError(f"Unknown research collection: {collection}")
        os.makedirs(cls.ROOT, exist_ok=True)
        return os.path.join(cls.ROOT, f"{collection}.json")

    @classmethod
    def _read(cls, collection):
        path = cls._path(collection)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _write(cls, collection, rows):
        path = cls._path(collection)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)

    @classmethod
    def list(cls, collection, domain=None):
        with cls._lock:
            rows = cls._read(collection)
        return [r for r in rows if not domain or r.get("domain") == domain]

    @classmethod
    def get(cls, collection, item_id):
        key = cls.ID_FIELDS[collection]
        with cls._lock:
            return next((r for r in cls._read(collection) if r.get(key) == item_id), None)

    @classmethod
    def create(cls, collection, item):
        with cls._lock:
            rows = cls._read(collection)
            rows.append(item)
            cls._write(collection, rows)
        return item

    @classmethod
    def update(cls, collection, item_id, changes):
        key = cls.ID_FIELDS[collection]
        with cls._lock:
            rows = cls._read(collection)
            for row in rows:
                if row.get(key) == item_id:
                    row.update(changes)
                    if "updated_at" in row:
                        row["updated_at"] = datetime.now(timezone.utc).isoformat()
                    cls._write(collection, rows)
                    return row
        return None

    @classmethod
    def append_unique(cls, collection, item_id, id_field, list_field, value):
        with cls._lock:
            rows = cls._read(collection)
            for row in rows:
                if row.get(id_field) == item_id:
                    values = row.setdefault(list_field, [])
                    if value not in values:
                        values.append(value)
                    if "updated_at" in row:
                        row["updated_at"] = datetime.now(timezone.utc).isoformat()
                    cls._write(collection, rows)
                    return row
        return None
