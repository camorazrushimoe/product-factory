# Product Factory

**Portable agentic product factory** for turning business intake into high-quality product specifications.

Inspired by [dev-crew](https://github.com/camorazrushimoe/dev-crew) (isolated Hermes agents in Docker + shared message bus) and Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern for compounding knowledge.

## Core Idea

Input: any business request (wish, pain, modernization request, support-driven need, etc.)  
Output: structured Product Spec ready for engineering teams / third-party engineering factories.

Between them — a team of specialized, isolated agents that progressively deepen understanding of the problem, the current system, the domain, the people, and the constraints.

## High-level Architecture

```
Human / Manager
       │
       ▼
┌──────────────────┐
│  crew-send.py    │  ← single entry point
└──────────┬─────────┘
         │
         ▼
┌───────────────────────────────────────────────────────────┐
│                     product-factory                         │
│  (one Docker Compose project)                               │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Agents    │  │ Shared Bus  │  │  Knowledge  │         │
│  │ (Hermes +   │←→│   (Redis)   │  │  (LLM Wiki) │         │
│  │  Docker)    │  │             │  │ per-project │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  Pipelines (Light / Code-aware / Full Discovery / ...)      │
└───────────────────────────────────────────────────────────┘
         │
         ▼
   Product Spec (for engineering)
```

### Key principles

1. **Isolation** — each agent runs in its own Docker container with its own Hermes home and skills.
2. **Shared bus** — Redis message bus for tasks, events, outputs between agents.
3. **Compounding memory** — LLM Wiki style knowledge base per client/project (markdown + links). Agents continuously update it.
4. **Progressive enrichment** — start with whatever data is available; deepen when code, data, or people become accessible.
5. **Human-in-the-loop** — critical points (after Discovery, before final Spec) allow human intervention.
6. **Spec-first** — everything ends in a clean, engineering-ready Product Spec.

## Agents

| Agent                    | Role                                                                 | Typical inputs                          | Typical outputs                     |
|--------------------------|----------------------------------------------------------------------|-----------------------------------------|-------------------------------------|
| **intake-classifier**    | Normalize any raw request, classify type, extract entities           | Raw email/ticket/message                | Structured Intake + Problem Hypothesis |
| **context-ingester**     | Collect & clean all available context (docs, tickets, notes...)     | Files, tickets, transcripts             | Context Pack                        |
| **codebase-analyst**     | Understand system through source code                               | Repo access / code dump                 | Code map, modules, tech debt, flows |
| **data-usage-analyst**   | Understand real usage patterns                                      | Logs, metrics, DB samples               | Usage insights, bottlenecks         |
| **domain-process-analyst**| Reconstruct business domain & AS-IS processes                       | Context + interviews + code             | Domain model, process maps          |
| **architecture-analyst** | High-level architecture, boundaries, constraints                    | Code + docs + diagrams                  | Architecture view + risks           |
| **discovery**            | Find the real problem & opportunities (JTBD, root causes)           | All previous outputs                    | Problem Statements, Opportunities   |
| **human-insight**        | Work with people (prepare questions, synthesize meetings)           | Meeting notes / transcripts             | Insights, hidden needs, politics    |
| **constraints**          | Collect all non-functional & organizational constraints             | Everything                              | Constraints list                    |
| **solution-shaper**      | Propose solution options with trade-offs                            | Discovery + Constraints                 | 2–4 solution directions             |
| **spec-writer**          | Produce the final Product Spec                                      | All of the above                        | Product Spec (PRD-like)             |
| **critic**               | Quality gate — find holes, contradictions, magic thinking           | Draft Spec                              | Review + verdict                    |
| **knowledge-memory**     | Maintain the per-project LLM Wiki                                   | Any agent output                        | Updated wiki pages + links          |

## Pipelines

Defined in `pipelines/`. Orchestrator chooses or composes them based on available data.

- `light.yaml` — only intake (first contact)
- `code-aware.yaml` — intake + code & architecture
- `full-discovery.yaml` — code + data + people
- `support-driven.yaml` — starts from tickets / pain signals
- custom — orchestrator can compose on the fly

## Memory Model

### 1. Short-term / Inter-agent (Bus)
Redis message bus (`bus/`).  
Agents publish events and structured outputs.  
Schema in `bus/action-schema.json`.

### 2. Long-term / Compounding (LLM Wiki)
Located in `knowledge/projects/<project-id>/`.

Inspired by Karpathy’s LLM Wiki:
- Persistent markdown pages
- Interlinked (entities, processes, architecture, problems, decisions…)
- Agents **update** the wiki instead of just retrieving
- Knowledge compounds over time across multiple intakes for the same client/system

Recommended structure inside a project:

```
knowledge/projects/<id>/
├── index.md                 # entry point + map
├── entities/                # key domain objects
├── processes/               # AS-IS and TO-BE processes
├── architecture/            # system views, constraints
├── problems/                # discovered problems & opportunities
├── decisions/               # important product decisions
├── sources/                 # raw or cleaned source material
└── wiki-log.md              # what agents changed and when
```

### 3. Workspace
`workspace/` — temporary working area for the current intake (mounted into agents).

## Repository Structure

```
product-factory/
├── agents/                      # one folder per agent
│   ├── <agent-name>/
│   │   ├── hermes-home/         # config.yaml, SOUL.md, memory, etc.
│   │   └── skills/              # agent-specific skills
├── bus/                         # Redis bus + message schema
├── crew/                        # entry points, orchestrator, agent registry
├── knowledge/                   # LLM Wiki (per project)
│   └── projects/
├── pipelines/                   # pipeline definitions (YAML / Python)
├── openspec/                    # product spec templates & contracts
├── workspace/                   # current intake working area
├── dashboard/                   # optional observability
├── docs/                        # architecture decisions, guides
├── tokens/                      # token / cost templates
├── docker-compose.yml
├── Dockerfile.agent
├── .env.example
└── README.md
```

## Quick Start (planned)

```bash
cp .env.example .env
# fill secrets / API keys

docker compose up -d

# send first intake
python3 crew/crew-send.py intake-classifier "Клиент хочет модернизировать систему X..."
```

## Status

**Specifications are finalized and ready for implementation.**

Completed:
- Full agent roster with SOUL.md for every agent
- Four pipelines (light, code-aware, full-discovery, support-driven)
- Bus event schema
- Product Spec template (`openspec/product-spec-template.md`)
- Wiki protocol + Agent contract
- Architecture overview + Implementation Roadmap
- Agent registry example

See `docs/IMPLEMENTATION-ROADMAP.md` for the recommended build order.

---

Built for learning Product Management by building the tools that a strong Technical Product Manager would use.
