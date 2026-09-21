# Toyt Research Lab — Phase 1

This branch introduces the epistemic layer around MiroFish without changing
the existing simulation engine.

## Goal

Represent research as a traceable cycle:

Hypothesis -> Evidence / Experiment / Simulation -> Finding -> revised hypothesis.

Phase 1 implements the first three durable concepts:

- Hypothesis
- Evidence
- Experiment

The existing Project, graph/Zep, OASIS simulation and ReportAgent pipeline is
left intact.

## API

Base path: `/api/research`

- `GET /health`
- `GET|POST /hypotheses`
- `GET|POST /evidence`
- `GET|POST /experiments`

All records have a `domain` field; the MVP defaults to `toyt`. GET endpoints
accept `?domain=toyt`.

## Next milestone

1. Link evidence bidirectionally to hypotheses.
2. Add Finding and epistemic evaluation.
3. Add a simulation adapter that invokes the existing MiroFish pipeline from a hypothesis.
4. Add Research Lab routes/views to the Vue frontend.
5. Add tests before generalizing OASIS beyond social-network agents.
