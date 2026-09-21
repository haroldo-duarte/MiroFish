"""Research Lab API."""
from flask import Blueprint, jsonify, request
from ..models.hypothesis import Hypothesis, HypothesisCategory, HypothesisStatus
from ..models.evidence import Evidence
from ..models.experiment import Experiment
from ..models.finding import Finding
from ..services.research.repository import ResearchRepository
from ..services.research.epistemic_evaluator import EpistemicEvaluator
from ..services.research.simulation_adapter import ResearchSimulationAdapter

research_bp = Blueprint("research", __name__)

@research_bp.get("/health")
def health():
    return {"status": "ok", "module": "research-lab", "phase": 2}

@research_bp.get("/hypotheses")
def list_hypotheses():
    return jsonify(ResearchRepository.list("hypotheses", request.args.get("domain")))

@research_bp.get("/hypotheses/<hypothesis_id>")
def get_hypothesis(hypothesis_id):
    item = ResearchRepository.get("hypotheses", hypothesis_id)
    return (jsonify(item), 200) if item else (jsonify({"error": "hypothesis not found"}), 404)

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
    hypothesis_ids = data.get("hypothesis_ids") or []
    for hid in hypothesis_ids:
        if not ResearchRepository.get("hypotheses", hid):
            return {"error": f"hypothesis not found: {hid}"}, 404
    item = Evidence(title=data["title"], evidence_type=str(data["evidence_type"]).lower(),
        summary=data["summary"], domain=str(data.get("domain") or "toyt").lower(),
        source=data.get("source"), confidence=str(data.get("confidence") or "unknown"),
        direction=str(data.get("direction") or "neutral").lower(), hypothesis_ids=hypothesis_ids)
    saved = ResearchRepository.create("evidence", item.to_dict())
    for hid in hypothesis_ids:
        ResearchRepository.append_unique("hypotheses", hid, "hypothesis_id", "evidence_ids", item.evidence_id)
    return jsonify(saved), 201

@research_bp.get("/experiments")
def list_experiments():
    return jsonify(ResearchRepository.list("experiments", request.args.get("domain")))

@research_bp.post("/experiments")
def create_experiment():
    data = request.get_json(silent=True) or {}
    if not str(data.get("name") or "").strip() or not str(data.get("method") or "").strip():
        return {"error": "name and method are required"}, 400
    hypothesis_ids = data.get("hypothesis_ids") or []
    for hid in hypothesis_ids:
        if not ResearchRepository.get("hypotheses", hid):
            return {"error": f"hypothesis not found: {hid}"}, 404
    item = Experiment(name=data["name"], method=data["method"], hypothesis_ids=hypothesis_ids,
        domain=str(data.get("domain") or "toyt").lower(),
        status=str(data.get("status") or "planned"), metric=data.get("metric"))
    saved = ResearchRepository.create("experiments", item.to_dict())
    for hid in hypothesis_ids:
        ResearchRepository.append_unique("hypotheses", hid, "hypothesis_id", "experiment_ids", item.experiment_id)
    return jsonify(saved), 201

@research_bp.get("/findings")
def list_findings():
    return jsonify(ResearchRepository.list("findings", request.args.get("domain")))

@research_bp.post("/findings")
def create_finding():
    data = request.get_json(silent=True) or {}
    hid = str(data.get("hypothesis_id") or "")
    if not ResearchRepository.get("hypotheses", hid):
        return {"error": "hypothesis not found"}, 404
    if not data.get("statement") or not data.get("source_type") or not data.get("source_id"):
        return {"error": "hypothesis_id, statement, source_type and source_id are required"}, 400
    item = Finding(hypothesis_id=hid, statement=data["statement"],
        source_type=str(data["source_type"]).lower(), source_id=str(data["source_id"]),
        direction=str(data.get("direction") or "inconclusive").lower(),
        confidence=str(data.get("confidence") or "unknown"),
        limitations=data.get("limitations") or [])
    saved = item.to_dict()
    saved["domain"] = ResearchRepository.get("hypotheses", hid).get("domain", "toyt")
    return jsonify(ResearchRepository.create("findings", saved)), 201

@research_bp.get("/hypotheses/<hypothesis_id>/assessment")
def assess_hypothesis(hypothesis_id):
    hypothesis = ResearchRepository.get("hypotheses", hypothesis_id)
    if not hypothesis:
        return {"error": "hypothesis not found"}, 404
    evidence = [e for e in ResearchRepository.list("evidence") if hypothesis_id in e.get("hypothesis_ids", [])]
    findings = [f for f in ResearchRepository.list("findings") if f.get("hypothesis_id") == hypothesis_id]
    assessment = EpistemicEvaluator.evaluate(hypothesis, evidence, findings)
    ResearchRepository.update("hypotheses", hypothesis_id, {"status": assessment["status"]})
    return jsonify(assessment)

@research_bp.post("/hypotheses/<hypothesis_id>/simulate")
def simulate_hypothesis(hypothesis_id):
    hypothesis = ResearchRepository.get("hypotheses", hypothesis_id)
    if not hypothesis:
        return {"error": "hypothesis not found"}, 404
    data = request.get_json(silent=True) or {}
    project_id = str(data.get("project_id") or "")
    if not project_id:
        return {"error": "project_id is required; use an existing MiroFish project with a built graph"}, 400
    try:
        link = ResearchSimulationAdapter.create(hypothesis, project_id, data.get("graph_id"),
            bool(data.get("enable_twitter", True)), bool(data.get("enable_reddit", True)))
        return jsonify(link), 201
    except ValueError as exc:
        return {"error": str(exc)}, 400


@research_bp.get("/priorities")
def priorities():
    domain = request.args.get("domain") or "toyt"
    hypotheses = ResearchRepository.list("hypotheses", domain)
    evidence = ResearchRepository.list("evidence", domain)
    experiments = ResearchRepository.list("experiments", domain)
    importance = {"high": 3, "medium": 2, "low": 1}
    status_uncertainty = {"untested": 3, "signal": 2.5, "inconclusive": 2.5, "contradicted": 1.5, "supported": 1}
    rows = []
    for h in hypotheses:
        ev_count = sum(1 for e in evidence if h["hypothesis_id"] in e.get("hypothesis_ids", []))
        planned = sum(1 for e in experiments if h["hypothesis_id"] in e.get("hypothesis_ids", []) and e.get("status") == "planned")
        score = importance.get(h.get("importance"), 2) * status_uncertainty.get(h.get("status"), 3)
        score += 1 / (1 + ev_count)
        if planned:
            score -= 0.25
        rows.append({
            "hypothesis_id": h["hypothesis_id"],
            "statement": h["statement"],
            "category": h["category"],
            "status": h["status"],
            "priority_score": round(score, 2),
            "evidence_count": ev_count,
            "planned_experiments": planned,
        })
    rows.sort(key=lambda x: x["priority_score"], reverse=True)
    return jsonify(rows)

@research_bp.get("/simulation-links")
def list_simulation_links():
    return jsonify(ResearchRepository.list("simulation_links"))
