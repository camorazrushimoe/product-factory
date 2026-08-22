# Implementation Roadmap

This document turns the current specifications into a practical build order.

## Phase 0 — Skeleton (done)

- [x] Repository structure
- [x] Agent list + SOUL.md for every agent
- [x] Pipeline definitions (light, code-aware, full-discovery, support-driven)
- [x] Bus event schema
- [x] Product Spec template
- [x] Wiki protocol + Agent contract
- [x] Architecture overview

## Phase 1 — Minimal runnable core

Goal: be able to send a raw intake and get a light-pipeline result.

1. Implement Redis bus helpers (publish / subscribe with the schema).
2. Implement `crew/crew-send.py` (HMAC entry point, similar to dev-crew).
3. Bring up 3–4 agents first:  
   `intake-classifier` → `discovery` → `solution-shaper` → `spec-writer` → `critic`
4. Simple sequential orchestrator that can run `pipelines/light.yaml`.
5. Human gate stub (pause + continue).
6. Write results into `workspace/` and a basic project wiki.

**Exit criteria:** one end-to-end light run on a real or synthetic intake produces a usable Product Spec draft.

## Phase 2 — Code & Context depth

1. Add `context-ingester`, `codebase-analyst`, `architecture-analyst`, `domain-process-analyst`.
2. Implement `code-aware` pipeline.
3. Give Codebase Analyst the ability to work with mounted repos or git clones.
4. Start proper wiki updates via `knowledge-memory`.

## Phase 3 — Full Discovery

1. Add remaining agents (`data-usage-analyst`, `human-insight`, `constraints`).
2. Implement `full-discovery` and `support-driven` pipelines.
3. Parallel stage support in the orchestrator.
4. Better human-in-the-loop UX (dashboard or simple CLI).

## Phase 4 — Hardening & Observability

1. Dashboard (agent status, current pipeline, costs).
2. Token / cost tracking.
3. Better error handling and retries.
4. Optional `analysis-env` network if agents need to run temporary tools.
5. OpenSpec evolution process (how we change the factory itself).

## Phase 5 — Real usage

- Run the factory on real client intakes.
- Continuously improve SOULs and skills based on observed weaknesses.
- Grow the per-project wikis.

---

Recommended first concrete coding tasks:

1. `bus/` Python client (publish/subscribe + schema validation)
2. `crew/crew-send.py`
3. Minimal orchestrator that can execute `light.yaml`
4. Docker Compose entries for the first 5 agents
5. First real SOUL + skill experiments with Hermes
