# Discovery Gate — operator-facing checkpoint after intake triage

## When to use
A request arrived. Before ANY deep work (system analysis, research, spec
writing), do ONLY lightweight triage and come back with an Intake Brief.
Deep work starts only after the operator replies.

## Procedure

### 1. Triage (timebox: ~15 min of tool work total)
- Normalize the request; extract entities and the Problem Hypothesis.
- **Linear lookup**: search for an existing project matching this
  client/product. If none: propose a new one in the brief. NEVER close a
  project — project closure is a human decision only.
- **Surface scan** of available material: repo README/structure overview,
  public facts. NO cloning-and-auditing, NO full research.
- Prepare stakeholder questions.

### 2. Intake Brief (this ENDS your turn)
Structure:

```
INTAKE BRIEF — <project>
1. UNDERSTANDING      how I understood the request (2–5 sentences)
2. WHAT I CHECKED     Linear state / repo surface / external facts (+sources)
3. QUESTIONS FOR YOU  question + why it matters + how the answer changes work
4. DEPTH OPTIONS      option A/B/C: what I'd do, effort, expected output
5. LINEAR             reuse project X | propose new project Y + INVESTIGATION ticket
```

Publish `intake.brief` on the office bus, post the brief as your reply,
create/update the `INVESTIGATION` Linear ticket with the brief as a comment.

Then STOP. Do not run understand-system / research / shape-and-spec, do not
delegate them, until the operator replies in this session.

### 3. Cheap-work bypass
If the request is trivially cheap (one lookup, one short answer): just do it
and report what was done and assumed. Gate is mandatory when anything is
ambiguous, multi-stage, needs stakeholder input, or cost drivers are unknown.

## Anti-patterns (violations)
- Running the full pipeline "to save a roundtrip"
- Writing spec drafts before scope agreement
- Closing or archiving Linear projects yourself
- Asking zero questions when material facts are missing
