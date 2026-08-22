# LLM Wiki Protocol

This factory uses a persistent, interlinked markdown knowledge base (inspired by Karpathy’s LLM Wiki) instead of pure RAG.

## Location

```
knowledge/projects/<project-id>/
├── index.md
├── entities/
├── processes/
├── architecture/
├── problems/
├── decisions/
├── sources/
└── wiki-log.md
```

## Rules for all agents

1. **Never treat the wiki as a chat log.**  
   Write durable, well-structured pages.

2. **Prefer update over recreate.**  
   If a page already exists, improve it and note what changed.

3. **Always link.**  
   When you mention an entity, process, or previous decision — link to its page.

4. **Record provenance.**  
   At the bottom of significant pages or in wiki-log.md note which intake and which agent contributed the information.

5. **Handle contradictions explicitly.**  
   If new data conflicts with existing knowledge, do not silently overwrite. Add a “Contradictions / Open tensions” section and update the synthesis.

6. **Small focused pages > giant documents.**

7. **index.md is the map.**  
   Keep it current so any agent (or human) can orient quickly.

## knowledge-memory agent

Is the primary steward. Other agents may:
- propose new pages
- propose edits
- publish `wiki.updated` events

knowledge-memory is responsible for consistency of the overall graph.

## Human role

Humans may freely edit the wiki. Agents should treat human edits as high-priority ground truth unless clearly outdated.
