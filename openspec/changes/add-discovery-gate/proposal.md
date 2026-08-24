# Why

Today a request that hits the product factory triggers the full pipeline
immediately: the TPM silently picks the depth, burns tokens on research and
spec drafting, and the operator first sees meaningful output at the end —
when it is expensive to correct. The first e2e run (vk-monitoring-service,
2026-08-24) showed the failure mode: half the work was done against wrong
assumptions before any human checkpoint.

Clients/stakeholders also have no visible frame: requests are not tracked as
work items, so "what are they doing about X?" has no answer surface.

# What Changes

- **Discovery Gate** — new mandatory stage right after intake: lightweight
  triage ONLY, then the TPM ends its turn and returns an **Intake Brief**
  (understanding, what was checked, stakeholder questions, 2–3 depth options
  with effort, Linear proposal). Deep stages wait for an explicit operator
  reply.
- **Escalation threshold** — trivially cheap requests (single lookup/answer)
  bypass the gate; anything ambiguous or multi-stage goes through it.
- **Linear as the request frame** — every request lives in a client/product
  Linear Project. First contact = reuse existing project or propose a new one
  + create an `INVESTIGATION` ticket holding the brief and findings. Agents
  NEVER close projects; project closure is a human decision. Small fulfilled
  request = ticket closed, project stays open.
- Pipeline wiring: `discovery-gate` stage with `human_gate: true` added to all
  four pipelines as the first post-intake stage.

# Capabilities

### New Capability
- `discovery-gate`

# Impact

- Affected specs: discovery-gate (new)
- Affected code:
  - `agents/technical-product-manager/hermes-home/SOUL.md` — gate rules +
    Linear ownership
  - `pipelines/*.yaml` — gate stage wiring
- Instance rollout (spec-1) mirrors the same changes via agent-office PRs
