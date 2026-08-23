# Product Factory as an Agent Office template

This repository is the **template** for Spec team instances under [Agent Office](https://github.com/camorazrushimoe/agent-office).

Agent Office is a multi-repo system:

- **agent-office** — shell (Office agents, shared Redis bus, shared pre-prod, composition)
- **product-factory** (this repo) — template for spec teams
- **lab-crew** — template for research teams
- **dev-crew** — template for implementation teams

Operators clone Office, then spawn as many Spec instances as they need from pinned refs of this template.

Full composition model: [agent-office/docs/composition.md](https://github.com/camorazrushimoe/agent-office/blob/main/docs/composition.md)

## Where the Spec team sits in the pipeline

```
Lab Crew (validate the idea)
    → Research Package via Office handoff
        → Product Factory (this template): intake → Product Spec
            → Dev Crew: build from the approved Spec
                → shared Office pre-prod (Super DevOps promotion)
```

The Spec team consumes validated research (or raw business intake when there is
no Lab instance upstream) and produces **Product Specs ready for engineering**.
It does not implement software and does not route work to Dev instances —
under Office, that routing is owned by the Office layer, mirroring how
[Lab Crew hands off](https://github.com/camorazrushimoe/lab-crew/blob/main/docs/office-template.md).

## What changes when running under Office

| Standalone Product Factory (today) | Under Agent Office |
|------------------------------------|--------------------|
| Own Redis (`shared-memory`, port 6379 published) | **Office shared Redis bus** (no local publish) |
| Agents always-on once implemented (`restart: unless-stopped`) | **Idle stop + wake-on-demand** (lifecycle controller) |
| Human gate = pause inside the pipeline | Same + gate events visible to **Office agents** (escalation surface) |
| Self-contained factory | **Instance** of a template, registered in Office |

What **stays** in this template:

- Roles: technical-product-manager, product-researcher, system-domain-analyst, adversarial-reviewer
- SOULs, skills, pipelines, human-gate semantics
- **LLM Wiki per project** (long-term knowledge, owned by the Technical PM)
- Webhook doors + send client (must become wake-aware)
- Workspace / knowledge volume layout

Spec teams typically need **no private dev-cluster**: their artifacts are
documents (specs, wiki, workspace drafts), not running systems. An optional
analysis environment may be attached later if code-aware analysis requires it.

## Template contract (Office-compatible mode)

When composed under Office, this template MUST:

1. Connect all agents to the **external** Office Redis URL (no default private inter-agent bus; drop the `6379:6379` host publish).
2. Keep HMAC webhook doors; send path MUST **wake** a stopped target before POST.
3. Emit Office-compatible bus events (`agent.started` / `agent.stopped`, task signals, `human.gate.required`), with team-qualified actor ids when multiple instances exist (e.g. `spec-1/technical-product-manager`).
4. Run a **lifecycle controller** for this instance's agent containers (idle ~40m, wake on demand). See Office `docs/agent-lifecycle.md`.
5. Use controller-managed restart policy for agents (`restart: "no"`).
6. Deliver finished Product Specs to **Office** (spec-ready event with artifact pointer); Office routes them to Dev instances — Spec does not own implementation routing.
7. Be registrable: name, type=`spec`, door/health/lifecycle endpoints, template ref.
8. Keep human gates as first-class bus events so Office can surface them to human operators.

Migration detail (Office side): [migration-teams-to-office-bus.md](https://github.com/camorazrushimoe/agent-office/blob/main/docs/migration-teams-to-office-bus.md)

## Standalone mode

This repo MAY support standalone operation (local Redis, always-on agents) for developing the template itself — it is currently in this stage (see `docs/IMPLEMENTATION-ROADMAP.md`).

**Default for Office operators is Office-attached mode.**

## Implementation roadmap (spec → code)

Product Factory is at design/Phase 0 for Docker runtime. When implementing Phases 1–2, Office-compatible mode should be the default design:

- [ ] Compose without a private `shared-memory` service when `OFFICE_REDIS_URL` is set
- [ ] Lifecycle controller + agent `restart: "no"`
- [ ] Wake-aware door client
- [ ] Team-qualified actors on the bus when `TEAM_NAME` is set
- [ ] `spec.ready` handoff event aimed at Office (artifact pointer, not full text)
- [ ] Env vars documented for Office attach (bus, team name)
- [ ] Align `human.gate.required` events with Office escalation surface

## Versioning

- Pin instances to **tags** of this repo in production compositions.
- Note breaking protocol needs: `Office compatibility: requires agent-office ≥ x.y`.

## Related

- [Agent Office](https://github.com/camorazrushimoe/agent-office)
- [Lab Crew template](https://github.com/camorazrushimoe/lab-crew)
- [Dev Crew template](https://github.com/camorazrushimoe/dev-crew)
