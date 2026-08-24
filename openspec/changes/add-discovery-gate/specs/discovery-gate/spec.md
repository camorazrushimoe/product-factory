# Discovery Gate

## ADDED Requirements

### Requirement: Mandatory checkpoint after intake triage

Every incoming request SHALL pass through a **Discovery Gate** before any deep
work (system analysis, research, spec writing) begins. The gate is a hard stop:
the TPM performs only lightweight triage, then ENDS the turn and returns an
**Intake Brief** to the operator.

#### Scenario: request arrives, TPM does triage only

- **WHEN** a new request reaches the TPM
- **THEN** the TPM SHALL perform ONLY: intake normalization, Linear
  project/ticket lookup or creation, a timeboxed surface scan of available
  material (repo overview, public info), and question preparation
- **AND** the TPM SHALL NOT run `understand-system`, `research`,
  `shape-and-spec`, or delegate those stages before operator approval
- **AND** the turn SHALL end with an Intake Brief posted back to the requester

### Requirement: Intake Brief content

The Intake Brief SHALL contain:

1. **Understanding** — how the TPM understood the request (2–5 sentences)
2. **What was checked** — Linear project state, repo surface scan, external
   facts found, each with provenance and an as-of date
3. **Questions for stakeholders** — each as: question + why it matters + how
   the answer changes the work (so the operator can relay them verbatim)
4. **Depth options** — 2–3 scoped options (e.g. answer-only / light /
   code-aware) with expected effort and what each would produce
5. **Recommendation** — which option the TPM recommends and why
6. **Linear proposal** — existing project reused or new project proposed,
   with ticket list

The Linear ticket comment SHALL be the canonical copy of the brief; the chat
reply and bus event are mirrors. A brief states its validity ("reflects repo/
Linear state as of <date>"); work resuming after material changes SHALL
refresh the affected sections.

#### Scenario: brief ends the turn

- **WHEN** the Intake Brief is composed
- **THEN** the TPM publishes `intake.brief` on the bus and posts the brief as
  the turn response
- **AND** no further pipeline stages are started in that session until an
  operator reply arrives

### Requirement: Escalation threshold (cheap-work bypass)

If the predicted work is trivially cheap — a single lookup or a short factual
answer, bounded by the same ~15 minutes of tool work as triage — the TPM MAY
skip the gate: do the work, then report. The gate is mandatory whenever the
forecast exceeds that bound, anything is ambiguous, stakeholder input is
needed, or cost drivers are unknown. When in doubt, use the gate. Even on
bypass, the request SHALL still be tracked in Linear: an `INVESTIGATION`
ticket is created and immediately closed with the outcome as its comment.

#### Scenario: micro-request bypasses the gate

- **WHEN** a request is a single lookup or a short factual answer within the
  timebox
- **THEN** the TPM MAY complete it immediately and report
- **AND** the report still includes what was done and what was assumed
- **AND** an `INVESTIGATION` ticket records the outcome and is closed

### Requirement: Linear tracks every request

Each request SHALL live under a Linear Project named for the client/product.
On first contact the TPM reuses the matching project or proposes a new one;
the operator confirms creation if ambiguous. Projects are NEVER closed by
agents — closing a project is a human/owner decision.

Ticket conventions per request:

- `INVESTIGATION` — created at the gate; holds the Intake Brief and findings;
  closed when the investigation stage is accepted
- Follow-up tickets (`questions-to-stakeholders`, `spec-draft`, …) are added
  after scope is agreed with the operator
- A small fulfilled request = its ticket closed; project stays open
- All findings and decisions are recorded as ticket comments (visible status
  for stakeholders)

#### Scenario: unknown request creates project + INVESTIGATION ticket

- **WHEN** no matching Linear project exists
- **THEN** the TPM proposes a new project and, upon confirmation (or
  self-serves when unambiguous), creates an `INVESTIGATION` ticket containing
  the Intake Brief
- **AND** the project remains open after the ticket closes

### Requirement: Pipeline wiring

All pipelines SHALL place `discovery-gate` as the first stage after intake
with `human_gate: true`. Stages after the gate SHALL NOT be started until the
operator reply arrives in-session. Existing `review` human gates remain
unchanged.

#### Scenario: pipeline cannot skip the gate

- **WHEN** a pipeline runs
- **THEN** stages after `discovery-gate` depend on it and on an explicit
  operator reply recorded in the session/project
- **AND** skipping the gate without an operator reply is a process violation
