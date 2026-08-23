# Implementation Roadmap

## Phase 0 — Design (done)

- [x] 4 clear roles defined
- [x] SOUL.md for each role
- [x] Basic skill sets for each role
- [x] Pipelines updated
- [x] Architecture & README updated

## Phase 1 — Minimal runnable core

Goal: send a raw intake and get a usable Product Spec via the light pipeline.

1. Redis bus helpers
2. `crew/crew-send.py`
3. Bring up the 4 agents (start with Technical Product Manager + Adversarial Reviewer + Product Researcher)
4. Simple sequential orchestrator for `light.yaml`
5. Human gate stub
6. Basic wiki updates

**Exit criteria:** one end-to-end light run produces a Product Spec draft.

## Phase 2 — Full depth

1. Full System & Domain Analyst capabilities (code + architecture + domain + usage)
2. `code-aware` and `full-discovery` pipelines
3. Proper LLM Wiki maintenance
4. Better human-in-the-loop

## Phase 3 — Hardening

- Dashboard / observability
- Token tracking
- Error handling
- Optional analysis environment

## Phase 4 — Real usage

Run on real intakes and continuously improve SOULs and skills.
