# Toyt Research Lab — Phase 2

The Research Lab is an epistemic layer around MiroFish. Existing graph/Zep,
OASIS simulation and ReportAgent behavior remains intact.

## Core cycle

Hypothesis -> Evidence / Experiment / Simulation -> Finding -> Assessment.

## API

Base: `/api/research`

- `GET /health`
- `GET|POST /hypotheses`
- `GET /hypotheses/<id>`
- `GET /hypotheses/<id>/assessment`
- `POST /hypotheses/<id>/simulate`
- `GET|POST /evidence`
- `GET|POST /experiments`
- `GET|POST /findings`
- `GET /simulation-links`

Evidence can link to hypotheses with `hypothesis_ids` and a direction:
`supports`, `contradicts`, or `neutral`.

## Epistemic safety

Simulation is not empirical proof. The evaluator down-weights simulated
evidence and simulation alone can only move an untested hypothesis to
`signal`, never to `supported`.

## Simulation adapter

`POST /hypotheses/<id>/simulate` accepts an existing MiroFish `project_id`
(and optionally `graph_id`). It creates a normal MiroFish SimulationState and
stores a Research Lab link plus a generated research-oriented simulation
requirement. Preparation/running continues through the existing MiroFish
pipeline, keeping this integration intentionally non-invasive.

## Next milestone

Build the Vue Research Lab UI (uncertainty map and hypothesis detail), expose
the generated requirement to the existing prepare flow, and convert completed
ReportAgent output into traceable Findings.
