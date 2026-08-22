# Product Factory — Architecture

## Goals

- Turn any business intake into a high-quality Product Spec.
- Support progressive deepening (from pure wish → full code + data + people understanding).
- Keep agents isolated (Docker + Hermes) while allowing rich collaboration.
- Maintain compounding project knowledge (LLM Wiki style).
- Stay close to the proven pattern of [dev-crew](https://github.com/camorazrushimoe/dev-crew).

## Components

### 1. Agents (isolated Hermes containers)

Each agent:
- Has its own Docker service.
- Has private `hermes-home/` (config, SOUL, local state).
- Has private `skills/`.
- Listens on a webhook “door”.
- Can publish/subscribe to the shared Redis bus.
- Can read/write the shared `workspace/` and the project’s LLM Wiki (with permissions).

### 2. Shared Message Bus (`bus/`)

- Redis.
- Schema: `bus/action-schema.json`.
- Used for:
  - Task hand-off
  - Event broadcasting (`intake.classified`, `code.analyzed`, `problem.framed`, `spec.ready`, …)
  - Structured outputs between agents

### 3. Knowledge Layer (`knowledge/`)

LLM Wiki pattern (Karpathy):

- One folder per client/project: `knowledge/projects/<project-id>/`
- Agents do not just RAG — they **maintain** the wiki:
  - create/update entity pages
  - link related concepts
  - note contradictions
  - keep an evolving synthesis
- `knowledge-memory` agent is the primary steward, but any agent can propose updates.

### 4. Pipelines (`pipelines/`)

Declarative or code-defined sequences of agents.

Examples:
- `light.yaml` — first contact
- `code-aware.yaml`
- `full-discovery.yaml`
- `support-pain.yaml`

Orchestrator (in `crew/`) selects or composes a pipeline based on:
- What data is already available
- Classification from Intake Classifier
- Human overrides

### 5. Entry Point & Orchestration (`crew/`)

- `crew-send.py` — human/manager entry point (HMAC-signed like in dev-crew).
- Agent registry (`agents.json` / `agents.example.json`).
- Simple orchestrator that can run a pipeline and wait for intermediate human gates.

### 6. Environments

For now we keep it lighter than full engineering staging:

- `crew` network — agents + bus talk to each other.
- Optional `analysis-env` network — for agents that need to spin temporary analysis tools (code parsers, local DBs, etc.).
- Most agents can do their work inside their own container + mounted volumes.

If later we need a full “dev cluster” for research agents to deploy temporary pipelines — we can add it the same way dev-crew does with `dev-env` / `staging-env`.

## Data flow (typical Full Discovery)

1. Human → `crew-send.py` → **intake-classifier**
2. Classifier publishes `intake.classified` + structured intake
3. Orchestrator starts pipeline → **context-ingester**
4. Parallel or sequential:
   - **codebase-analyst**
   - **data-usage-analyst**
   - **architecture-analyst**
   - **domain-process-analyst**
5. Results go to bus + wiki updates
6. **human-insight** (after meetings)
7. **discovery** synthesizes real problems & opportunities
8. **constraints**
9. **solution-shaper**
10. **spec-writer** produces draft
11. **critic** reviews
12. Human gate → final Spec
13. **knowledge-memory** folds everything useful into the project wiki

## Memory strategy summary

| Type              | Technology          | Scope              | Purpose                          |
|-------------------|---------------------|--------------------|----------------------------------|
| Inter-agent       | Redis bus           | Current run        | Coordination & structured hand-off |
| Project knowledge | Markdown LLM Wiki   | Per client/project | Compounding understanding        |
| Agent private     | hermes-home         | Per agent          | Local state, preferences         |
| Temporary         | workspace/          | Current intake     | Scratch files, drafts            |

## Open questions (to decide later)

- Exact message schema on the bus
- How strictly we enforce human gates
- Whether Codebase Analyst gets Docker-out-of-Docker or only volume mounts
- Token / cost tracking per agent (see `tokens/`)
- Integration with Linear / GitHub Issues for tracking intakes
