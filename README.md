# Product Factory

**Portable agentic product factory** for turning business intake into high-quality product specifications.

Inspired by [dev-crew](https://github.com/camorazrushimoe/dev-crew) (isolated Hermes agents in Docker + shared message bus) and Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern.

## Core Idea

**Input:** any business request (wish, pain, modernization, support-driven need…)  
**Output:** structured Product Spec ready for engineering teams.

The factory is a small team of specialized technical roles that progressively deepen understanding and produce a clean specification.

## Roles (4)

| Role | Responsibility |
|------|----------------|
| **Technical Product Manager** | Owns the outcome. Intake, constraints, solution shaping, Product Spec, LLM Wiki. |
| **Product Researcher** | Discovers real problems, opportunities and human insights. |
| **System & Domain Analyst** | Owns technical + domain truth about the current system (code, architecture, processes, usage). |
| **Adversarial Reviewer** | Quality gate. Challenges weak thinking and protects the Spec. |

All roles are technical. The Technical Product Manager owns the long-term knowledge (LLM Wiki).

## High-level flow

```
Raw request
    ↓
Technical Product Manager   → structured intake + constraints
    ↓
System & Domain Analyst     → deep AS-IS understanding
    ↓
Product Researcher          → real problems + opportunities + human insights
    ↓
Technical Product Manager   → solution options → Product Spec
    ↓
Adversarial Reviewer        → review
    ↓
Technical Product Manager   → final Spec + wiki update
```

## Memory

- **Short-term:** Redis message bus between agents
- **Long-term:** LLM Wiki per project/client (owned by Technical Product Manager)

## Repository Structure

```
product-factory/
├── agents/
│   ├── technical-product-manager/
│   ├── product-researcher/
│   ├── system-domain-analyst/
│   └── adversarial-reviewer/
├── bus/
├── crew/
├── knowledge/          # LLM Wiki (per project)
├── pipelines/
├── openspec/           # Product Spec template
├── docs/
├── workspace/
└── docker-compose.yml
```

## Status

Specifications updated to the 4-role model.  
SOULs and basic skill sets for all four roles are defined.

See `docs/IMPLEMENTATION-ROADMAP.md` for next implementation steps.

---

Built to learn Product Management by building the tools a strong Technical Product Manager would use.
