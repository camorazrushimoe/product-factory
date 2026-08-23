# Product Factory — Architecture

## Goals

- Turn any business intake into a high-quality Product Spec.
- Support progressive deepening of understanding.
- Keep agents isolated (Docker + Hermes) while allowing rich collaboration.
- Maintain compounding project knowledge (LLM Wiki).
- Use clear professional roles instead of many tiny specialists.

## Roles

### 1. Technical Product Manager
Owns the outcome: intake → constraints → solution options → Product Spec → LLM Wiki.

### 2. Product Researcher
Owns discovery of real problems, opportunities and human insights.

### 3. System & Domain Analyst
Owns the factual AS-IS understanding of the system and domain (code, architecture, processes, usage).

### 4. Adversarial Reviewer
Owns quality. Challenges weak thinking and protects the final Spec.

## Components

- **Agents**: 4 isolated Hermes containers, one per role.
- **Shared Message Bus**: Redis (`bus/action-schema.json`).
- **Knowledge**: LLM Wiki per project, owned by Technical Product Manager.
- **Pipelines**: Declarative sequences of the 4 roles (`pipelines/`).
- **Entry point**: `crew/crew-send.py` + agent registry.

## Typical Full Discovery flow

1. Technical Product Manager — intake & initial framing
2. System & Domain Analyst — deep AS-IS understanding
3. Product Researcher — problems, opportunities, human insights (human gate possible)
4. Technical Product Manager — solution options + Product Spec
5. Adversarial Reviewer — review (human gate)
6. Technical Product Manager — finalize Spec + update wiki

## Memory

| Type | Technology | Owner |
|------|------------|-------|
| Inter-agent | Redis bus | all |
| Project knowledge | Markdown LLM Wiki | Technical Product Manager |
| Agent private | hermes-home | each agent |
| Temporary | workspace/ | current intake |
