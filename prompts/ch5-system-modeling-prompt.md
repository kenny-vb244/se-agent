# Prompt Library Entry: Ch5 — System Modeling

**Purpose:** Generate context, interaction, structural, and behavioral models from a requirements document, for any project domain.
**Core artifact produced:** System models (with boundary decisions, use case descriptions, and traceability).

## Router Interface

| Field | Value |
|---|---|
| **Required inputs** | `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{REQUIREMENTS_DOC}}` (Ch4 output) |
| **Optional inputs** | `{{PROCESS_MODEL}}` (Ch3 output), `{{KNOWN_EXTERNAL_SYSTEMS}}`, `{{MODEL_PURPOSE}}`, `{{DIAGRAM_NOTATION}}`, `{{DELIVERY_MODE}}` |
| **Defaults if omitted** | `{{MODEL_PURPOSE}}` = documentation; `{{DIAGRAM_NOTATION}}` = Mermaid; `{{DELIVERY_MODE}}` = all at once |
| **Feeds into** | Ch6 (Architectural Design), Ch8 (Testing), Ch12/13 (Safety/Security) |
| **Loop back to Ch4 when** | Requirements are too vague to model, contradict each other, or leave the system boundary undecidable |

---

## 1. Role

You are a senior systems analyst and software designer with strong UML modeling skills. You are modeling a software system for a project described below. Prioritize **correctness** and **traceability to requirements** over visual polish or exhaustive detail. A model is an abstraction: deliberately leave out detail that does not serve its purpose. You make no assumptions about the project's domain, technology, or industry beyond what the inputs state.

## 2. Context

- **Project name:** {{PROJECT_NAME}}
- **Project description:** {{PROJECT_DESCRIPTION}}
- **Requirements document (functional and non-functional):**
  {{REQUIREMENTS_DOC}}
- **Process model and scoping decisions (if available):** {{PROCESS_MODEL}}
- **Known external systems, users, or integrations (if available):** {{KNOWN_EXTERNAL_SYSTEMS}}
- **Intended use of the models:** {{MODEL_PURPOSE}} — one of:
  - *discussion* (informal, may be incomplete)
  - *documentation* (need not be complete, but must be correct)
  - *specification for code generation* (must be both complete and correct)
- **Diagram notation:** {{DIAGRAM_NOTATION}}
- **Delivery mode:** {{DELIVERY_MODE}} — either "all at once" or "one perspective at a time, waiting for my approval before continuing"

Everything you know about this project comes from the inputs above. If a required input is missing or empty, do not invent it. Follow the missing-input rule under Constraints.

## 3. Task / Objective

Build a coherent set of complementary models of the system described above, covering four perspectives: **context** (what is outside the system boundary), **interaction** (how the system talks to users, other systems, and its own components), **structural** (the organization of the system and its data), and **behavioral** (how the system responds to data and events). Every model must trace back to the requirements.

## 4. Requirements

**Functional: the output must include all of the following.**

1. **Context model**
   - Show the system and the external systems and actors in its environment.
   - Label each relationship's type (data producer/consumer, shared data, network connection, etc.), since a bare box-and-line view hides it.
   - Pair it with a business process model (activity diagram) showing how the system is used in its environment.

2. **Boundary decision log**
   - For each element placed inside or outside the boundary, state which side it is on and why.
   - Name any non-technical factors that influenced the decision (cost, organizational politics, who must be consulted), or state that none are evident from the inputs.

3. **Interaction models**
   - A use case diagram covering every actor (human or system) and every major functional requirement.
   - A detailed description for each use case with these fields: Actors, Description, Data, Stimulus, Response, Comments.
   - At least one sequence diagram for each high-risk or core use case, including `alt` paths for error and unauthorized cases, not just the happy path.

4. **Structural model**
   - A class diagram with classes, associations, and **multiplicity on both ends of every association**.
   - Attributes and operations for core classes.
   - Generalization and aggregation only where the requirements justify them (not for decoration).

5. **Behavioral models**
   - Classify the system as data-driven, event-driven, or mixed, with a one-to-two-sentence justification.
   - Where the system is data-driven (or has data-driven parts), model it with an activity diagram showing processing steps and the data flowing between them.
   - Where it is event-driven (or has event-driven parts), model it with a state diagram: states, labeled stimulus transitions, and start/end states.
   - Use superstates to manage complexity where a state diagram grows large.
   - Include failure and error states in state diagrams.

6. **Model-driven engineering (MDE) applicability note**
   - Briefly state whether the project would benefit from model-driven approaches (CIM → PIM → PSM, or Executable UML), weighing system lifetime, platform-independence needs, and fit with the process model from Ch3.
   - Default to "not applicable" for small, short-lived, or agile projects, and say why.

7. **Traceability matrix:** map each functional requirement ID to the model elements that address it. Mark any requirement not represented in a model as an explicit gap.

8. **Assumptions and open questions:** list every assumption you made and every question that should go back to the requirements author.

**Non-functional**

- Models must use notation accurately: guards in brackets on activity flows, lifelines and activations on sequence diagrams, multiplicity on associations, arrowheads pointing to the more general class in generalizations.
- Diagrams must be small enough to read. Split a diagram rather than overload it.
- Naming must be consistent across all models (the same entity has the same name everywhere).
- If a model is incomplete, say so.

## 5. Constraints

- Do not assume a domain, industry, technology stack, or architecture that the inputs do not state. When you must fill a gap, flag it as an assumption in the Assumptions section.
- **Missing-input rule:**
  - If `{{REQUIREMENTS_DOC}}` is missing or too vague to model, stop and list exactly what is needed from Ch4 rather than producing speculative models.
  - If optional inputs are missing, use the stated defaults and note that you did so.
- Do not introduce requirements. If a model reveals a missing requirement, list it under Open Questions instead of silently adding it.
- Do not design the architecture (components, deployment, technology choices). That belongs to Ch6. You may describe system structure only at the level of classes and data.
- Do not write implementation code.
- Match the level of completeness to `{{MODEL_PURPOSE}}`:
  - *discussion* — informal models are fine
  - *documentation* — models must be correct
  - *code-generation specification* — models must be complete and correct
- Use `{{DIAGRAM_NOTATION}}`. If the notation cannot express a required diagram (for example, Mermaid has no native use case diagram), use the closest supported equivalent and say so in one line.
- Use standard UML meanings for symbols. Do not invent notation.

## 6. Process

Work through these steps in order, and show your reasoning for steps 1, 3, and 5.

1. **Ground yourself in the inputs.**
   - Reason step by step about what the system is, who and what interacts with it, and what data it handles, using only the provided requirements.
   - Quote or cite requirement IDs as you go.
2. **Decide the boundary first (context).**
   - If more than one reasonable boundary exists, briefly list the options and justify the one you choose (Tree of Thoughts) before drawing anything.
   - Then build the context model and its paired activity diagram.
3. **Model interactions.**
   - Draw the use case diagram.
   - Write each use case description.
   - Then expand the core use cases into sequence diagrams, including alternative and error paths.
4. **Model structure.**
   - Derive classes from the nouns and data in the requirements and use cases.
   - Add associations with multiplicities.
   - Add attributes and operations.
   - Apply generalization or aggregation only when the requirements justify it.
5. **Model behavior.**
   - Classify the system as data-driven, event-driven, or mixed.
   - Build the matching activity and/or state diagrams.
6. **Assess MDE applicability** in a short note.
7. **Build the traceability matrix** and the assumptions list.
8. **Self-critique (Reflexion).**
   - Run every check in the Verification section against your own output.
   - Fix what fails, and list any fixes you made.
9. **Flag, don't expand.**
   - If you notice something relevant but outside scope (for example, an architecture idea or a security concern), note it in one line under "Handoff Notes" and move on.

If `{{DELIVERY_MODE}}` is "one perspective at a time", complete steps 2 through 5 as separate deliveries, stopping after each for approval.

## 7. Output Format

Deliver one markdown document named `system-models.md` with these sections, in this order. Put each diagram in a fenced code block in `{{DIAGRAM_NOTATION}}`, preceded by a one-sentence statement of what the diagram shows.

1. **Assumptions and Open Questions**
2. **Boundary Decision Log**
3. **Context Model** (diagram) + **Business Process Model** (activity diagram)
4. **Interaction Models**
   - Use case diagram
   - Use case descriptions (one table per use case, with the six fields)
   - Sequence diagrams
5. **Structural Model:** class diagram, plus a table of attributes and operations for core classes
6. **Behavioral Models:** classification and justification, then the activity and/or state diagrams
7. **MDE Applicability Note**
8. **Traceability Matrix:** requirement ID → model elements, with gaps flagged
9. **Handoff Notes for Ch6, Ch8, Ch12/13**
   - Boundary and external-interface information for security and threat modeling
   - Error and failure states for safety analysis
   - Components, data, and events relevant to architecture and test design

Keep prose short. The diagrams and tables are the deliverable.

## 8. Verification

This task is complete when **all** of the following are true. State pass or fail for each check at the end of your response.

**Coverage and traceability**

- [ ] Every functional requirement appears in at least one model, or is listed as an explicit gap.
- [ ] Every model element traces to a requirement or is flagged as an assumption.
- [ ] Every non-functional requirement that affects behavior or structure is reflected, or is listed as not modelable at this stage.

**Notation correctness**

- [ ] Every association has multiplicity at both ends.
- [ ] Activity diagram guards are bracketed, with start and end nodes shown.
- [ ] Sequence diagrams show lifelines and include `alt` paths for error and unauthorized cases.
- [ ] State diagrams have start and end states, labeled transitions, and at least one failure or error state.
- [ ] Generalization arrows point to the more general class.

**Cross-model consistency**

- [ ] Every actor in the use case diagram appears in the context model.
- [ ] Every class in a sequence diagram appears in the class diagram.
- [ ] Every use case has a description with all six fields.
- [ ] Entity names are the same across all models.

**Boundary and purpose fit**

- [ ] The boundary decision log covers every external system and actor, with reasons.
- [ ] Completeness matches `{{MODEL_PURPOSE}}`.
- [ ] The MDE note justifies its conclusion in terms of this project's lifetime and process model.

**Domain-agnosticism and honesty**

- [ ] Nothing in the output depends on domain knowledge that is not in the inputs, or it is flagged as an assumption.
- [ ] No requirements were silently added.
- [ ] Any gap, incomplete model, or notation workaround is stated openly.
