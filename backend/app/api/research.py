"""Research Lab API.

Phase 1 intentionally adds an epistemic layer without changing the existing
MiroFish graph, OASIS, simulation or report endpoints.
"""
from flask import Blueprint, jsonify, request
from ..models.hypothesis import Hypothesis, HypothesisCategory, HypothesisStatus
from ..models.evidence import Evidence
from ..models.experiment import Experiment
from ..services.research.repository import ResearchRepository

research_bp = Blueprint("research", __name__)

@research_bp.get("/health")
def health():
    return {"status": "ok", "module": "research-lab", "phase": 1}

@research_bp.get("/hypotheses")
def list_hypotheses():
    return jsonify(ResearchRepository.list("hypotheses", request.args.get("domain")))

@research_bp.post("/hypotheses")
def create_hypothesis():
    data = request.get_json(silent=True) or {}
    statement = str(data.get("statement") or "").strip()
    category = str(data.get("category") or "").strip().lower()
    if not statement:
        return {"error": "statement is required"}, 400
    if category not in {x.value for x in HypothesisCategory}:
        return {"error": "invalid category", "allowed": [x.value for x in HypothesisCategory]}, 400
    status = str(data.get("status") or HypothesisStatus.UNTESTED.value)
    if status not in {x.value for x in HypothesisStatus}:
        return {"error": "invalid status"}, 400
    item = Hypothesis(statement=statement, category=category,
        domain=str(data.get("domain") or "toyt").lower(),
        importance=str(data.get("importance") or "medium").lower(), status=status)
    return jsonify(ResearchRepository.create("hypotheses", item.to_dict())), 201

@research_bp.get("/evidence")
def list_evidence():
    return jsonify(ResearchRepository.list("evidence", request.args.get("domain")))

@research_bp.post("/evidence")
def create_evidence():
    data = request.get_json(silent=True) or {}
    required = ("title", "evidence_type", "summary")
    missing = [k for k in required if not str(data.get(k) or "").strip()]
    if missing:
        return {"error": "missing required fields", "fields": missing}, 400
    item = Evidence(title=data["title"], evidence_type=data["evidence_type"],
        summary=data["summary"], domain=str(data.get("domain") or "toyt").lower(),
        source=data.get("source"), confidence=str(data.get("confidence") or "unknown"))
    return jsonify(ResearchRepository.create("evidence", item.to_dict())), 201

@research_bp.get("/experiments")
def list_experiments():
    return jsonify(ResearchRepository.list("experiments", request.args.get("domain")))

@research_bp.post("/experiments")
def create_experiment():
    data = request.get_json(silent=True) or {}
    if not str(data.get("name") or "").strip() or not str(data.get("method") or "").strip():
        return {"error": "name and method are required"}, 400
    item = Experiment(name=data["name"], method=data["method"],
        hypothesis_ids=data.get("hypothesis_ids") or [],
        domain=str(data.get("domain") or "toyt").lower(),
        status=str(data.get("status") or "planned"), metric=data.get("metric"))
    return jsonify(ResearchRepository.create("experiments", item.to_dict())), 201
