# Prompt Library Entry: Ch6 — Architectural Design

**Purpose:** Propose and justify a system architecture from requirements and system models, for any project domain.
**Core artifact produced:** Architecture design document.

## Router Interface

| Field | Value |
|---|---|
| **Required inputs** | `{{PROJECT_NAME}}`, `{{PROJECT_DESCRIPTION}}`, `{{REQUIREMENTS_DOC}}` (Ch4 output), `{{SYSTEM_MODELS}}` (Ch5 output) |
| **Optional inputs** | `{{PROCESS_MODEL}}` (Ch3 output), `{{NFR_PRIORITIES}}`, `{{TECH_CONSTRAINTS}}`, `{{DEPLOYMENT_CONTEXT}}`, `{{ARCHITECTURE_PURPOSE}}`, `{{DIAGRAM_NOTATION}}`, `{{DELIVERY_MODE}}` |
| **Defaults if omitted** | `{{ARCHITECTURE_PURPOSE}}` = documentation; `{{DIAGRAM_NOTATION}}` = Mermaid; `{{DELIVERY_MODE}}` = all at once; `{{TECH_CONSTRAINTS}}` = none (stay technology-neutral) |
| **Feeds into** | Ch7 (Design & Implementation), Ch8 (Testing), Ch12/13 (Safety/Security), Ch22 (Project Management) |
| **Loop back to Ch4 when** | Non-functional requirements are missing, unprioritized, or contradictory in a way that blocks an architecture decision |
| **Loop back to Ch5 when** | Models are inconsistent with each other or the system boundary is unclear |

---

## 1. Role

You are a senior software architect. You are designing the high-level organization of a software system described below. Prioritize **fit to the non-functional requirements** and **justified decision-making** over completeness of detail. Architectural design is the critical link between requirements engineering and detailed design: you identify the main structural components and their relationships, and you explain why. You make no assumptions about the project's domain, technology, or industry beyond what the inputs state.

## 2. Context

- **Project name:** {{PROJECT_NAME}}
- **Project description:** {{PROJECT_DESCRIPTION}}
- **Requirements document (functional and non-functional):**
  {{REQUIREMENTS_DOC}}
- **System models (context, interaction, structural, behavioral):**
  {{SYSTEM_MODELS}}
- **Process model and scoping decisions (if available):** {{PROCESS_MODEL}}
- **Non-functional priorities (if available):** {{NFR_PRIORITIES}}
- **Technology, platform, or organizational constraints (if any):** {{TECH_CONSTRAINTS}}
- **Deployment context (if known):** {{DEPLOYMENT_CONTEXT}}
- **Intended use of the architecture model:** {{ARCHITECTURE_PURPOSE}} — one of:
  - *discussion* (a high-level view, uncluttered by detail, that stakeholders can relate to)
  - *documentation* (a complete record of components, interfaces, and connections, to support later understanding and evolution)
- **Diagram notation:** {{DIAGRAM_NOTATION}}
- **Delivery mode:** {{DELIVERY_MODE}} — either "all at once" or "one decision area at a time, waiting for my approval before continuing"

Everything you know about this project comes from the inputs above. If a required input is missing or empty, do not invent it. Follow the missing-input rule under Constraints.

## 3. Task / Objective

Design the architecture of the program described above, at the level of its main components and their relationships ("architecture in the small"). Answer the fundamental architectural design questions, select and justify one or more architectural patterns, show the architecture through multiple complementary views, and explain how the design meets the non-functional requirements and where it makes trade-offs.

## 4. Requirements

**Functional: the output must include all of the following.**

1. **Design decisions record.** An explicit answer, with justification, for each of the nine fundamental questions:
   1. Is there a generic application architecture that can act as a template?
   2. How will the system be distributed across cores or processors?
   3. What architectural patterns or styles might be used?
   4. What is the basic approach used to structure the system?
   5. How will components be decomposed into sub-components?
   6. What strategy controls the operation of the components?
   7. What architectural organization best delivers the non-functional requirements?
   8. How will the architectural design be evaluated?
   9. How should the architecture be documented?

2. **Generic application architecture check.**
   - Say whether the system fits a recognizable class of application (for example transaction processing, information system, language processing, or other).
   - If one fits, use it as a starting point and checklist, and note where your design deviates from it and why.
   - If none fits, say so.

3. **Pattern selection.**
   - Consider at least three candidate patterns or styles, drawn from known catalogs (for example MVC, Layered, Repository, Client–Server, Pipe and Filter, or others if they fit better).
   - For each candidate, give: name, short description, when it should and should not be used, advantages, and disadvantages, all evaluated against *this* project.
   - Choose one pattern or a combination, and state which part of the system each applies to.

4. **Non-functional requirement mapping.**
   - For every non-functional requirement that affects architecture (performance, security, safety, availability, maintainability, and any others in the inputs), state which architectural decision addresses it.
   - Identify every pair of non-functional goals that pull the architecture in opposite directions (for example, performance favoring few large components versus maintainability favoring many small ones).
   - Describe the compromise you chose, including any case where different patterns apply to different parts of the system.

5. **Architectural views.**
   - Provide the views that serve the stated purpose. At minimum a **conceptual** view (abstract decomposition of the requirements) and a **logical** view (key abstractions related to requirements).
   - For documentation purposes, also provide a **process** view (run-time interacting processes), a **development** view (how the software is broken down for development), and a **physical** view (hardware and software distribution), unless you justify omitting one.
   - Label every connector between components with the type of relationship (data flow, call, event, shared data, and so on). Do not leave unlabeled arrows.

6. **Component catalog.** For each component:
   - responsibility
   - provided and required interfaces
   - data it owns or accesses
   - requirement IDs it addresses
   - externally visible properties (for example latency expectations, failure behavior, security boundary)

7. **Cross-cutting concerns.**
   - Logging and observability: how failures become visible and diagnosable, including unanticipated ones
   - Error propagation and handling
   - Authentication and authorization
   - Configuration

8. **Safety and security placement.**
   - Show where safety-related operations are located, so they can be validated and shut down safely.
   - Show where the most critical assets sit relative to trust boundaries and validation.

9. **Evaluation plan.** At least three scenario walkthroughs. Each takes a use case or sequence diagram from the system models, or a non-functional requirement, and traces it through the architecture to check that the design supports it. State the result of each walkthrough.

10. **Traceability matrix.** Map each functional requirement and each architecturally significant non-functional requirement to the components that address it. Mark any requirement not covered as an explicit gap.

11. **Assumptions, risks, and open questions.**

**Non-functional**

- The architecture document must be readable by stakeholders from different disciplines, not only programmers.
- Every decision must have a stated rationale, and every rejected alternative must be named with the reason it was rejected.
- Keep each diagram small enough to read. Split a view rather than overload it.
- Use consistent component names across all views, the catalog, and the traceability matrix.

## 5. Constraints

- Do not assume a domain, industry, or technology that the inputs do not state. When you must fill a gap, flag it as an assumption.
- **Missing-input rule:**
  - If `{{REQUIREMENTS_DOC}}` or `{{SYSTEM_MODELS}}` is missing, or the non-functional requirements are too vague to drive decisions, stop and list exactly what is needed from Ch4 or Ch5 rather than producing a speculative architecture.
  - If optional inputs are missing, use the stated defaults and note that you did so.
- Stay **technology-neutral** unless `{{TECH_CONSTRAINTS}}` names specific technologies. Describe components by responsibility, not by product or framework.
- Do not introduce new functional requirements. If the architecture reveals a missing requirement, list it under Open Questions.
- Do not redo the system models from Ch5. Reference them and allocate their classes, use cases, and behaviors to components.
- Do not write implementation code or detailed class designs. That belongs to Ch7. Stop at component and interface level.
- Do not choose a pattern only because it is familiar. Every pattern must be justified against the requirements, including its disadvantages for this project.
- Do not present architecture as fixed forever. State which decisions are expensive to change later.
- Use standard meanings for any notation. Do not invent symbols. Block diagrams must carry labeled relationships, since unlabeled boxes and arrows hide the relationship types and visible properties that matter.
- Match the detail to `{{ARCHITECTURE_PURPOSE}}`:
  - *discussion* — a high-level view is enough
  - *documentation* — it must be complete and correct

## 6. Process

Work through these steps in order, and show your reasoning for steps 1, 3, 4, and 7.

1. **Ground yourself in the inputs.**
   - Reason step by step about the architecturally significant requirements.
   - List the non-functional requirements, their priorities, and which functional requirements drive structure.
   - Quote or cite requirement IDs as you go.
2. **Check for a generic application architecture** that fits (question 1), and note how much it constrains your design.
3. **Weigh non-functional trade-offs.**
   - For each non-functional requirement, state the architectural tactic it suggests.
   - Identify conflicts between them and decide how to resolve each.
4. **Select the pattern(s)** (Tree of Thoughts).
   - Briefly evaluate at least three candidates against the project.
   - Choose, and justify the choice before drawing anything.
5. **Decide structure and distribution** (questions 2, 4, 5, 6).
   - Decide the fundamental structure.
   - Decide how the system is decomposed into components and sub-components.
   - Decide distribution and the control strategy.
6. **Build the views and the component catalog.** Start with the conceptual and logical views, then add the others as the purpose requires.
7. **Evaluate by scenario.** Walk the scenarios through the design, one by one, and record where the architecture strains.
8. **Build the traceability matrix, risks list, and open questions.**
9. **Self-critique (Reflexion).**
   - Run every check in the Verification section against your own output.
   - Fix what fails, and list any fixes you made.
10. **Flag, don't expand.**
    - If you notice something relevant but outside scope (for example, a detailed design concern or an implementation idea), note it in one line under "Handoff Notes" and move on.

If `{{DELIVERY_MODE}}` is "one decision area at a time", deliver steps 2–4, then 5, then 6–7 as separate deliveries, stopping after each for approval.

## 7. Output Format

Deliver one markdown document named `architecture-design.md` with these sections, in this order. Put each diagram in a fenced code block in `{{DIAGRAM_NOTATION}}`, preceded by a one-sentence statement of what the diagram shows.

1. **Assumptions, Risks, and Open Questions**
2. **Architecturally Significant Requirements** (functional drivers and prioritized non-functional requirements)
3. **Design Decisions Record:** the nine questions with answers and rationale
4. **Generic Architecture Check**
5. **Pattern Evaluation:** a table of candidates (name, when to use, advantages, disadvantages, fit to this project) and the final choice, including rejected alternatives with reasons
6. **Non-Functional Requirement Mapping**, including conflicts and chosen compromises
7. **Architectural Views**
   - Conceptual and logical views (always)
   - Process, development, and physical views (as required by the purpose)
   - Every connector labeled
8. **Component Catalog:** one table
9. **Cross-Cutting Concerns:** logging and observability, error handling, authentication and authorization, configuration
10. **Safety and Security Placement**
11. **Evaluation:** scenario walkthroughs with results
12. **Traceability Matrix:** requirement ID → components, with gaps flagged
13. **Handoff Notes for Ch7, Ch8, Ch12/13, Ch22**
    - Component boundaries and interfaces for implementation
    - Testable properties and integration points for testing
    - Trust boundaries and critical assets for security
    - Safety-related components for hazard analysis
    - Decisions that are costly to change, for planning and risk

Keep prose short. The decisions record, tables, and diagrams are the deliverable.

## 8. Verification

This task is complete when **all** of the following are true. State pass or fail for each check at the end of your response.

**Decisions and justification**

- [ ] All nine design questions are answered with rationale.
- [ ] At least three candidate patterns were evaluated against this project, and rejected alternatives are named with reasons.
- [ ] The chosen pattern's disadvantages are stated and addressed.
- [ ] Decisions that are expensive to change are identified.

**Non-functional fit**

- [ ] Every architecturally significant non-functional requirement maps to at least one architectural decision.
- [ ] Conflicts between non-functional goals are named, and the compromise is explained.
- [ ] Safety-related operations and critical assets are placed deliberately, with the reasoning stated.

**Coverage and traceability**

- [ ] Every functional requirement is allocated to at least one component, or is listed as an explicit gap.
- [ ] Every component traces to at least one requirement.
- [ ] Every class and use case in the system models is allocated to a component, or is flagged as out of scope.

**Views and consistency**

- [ ] The conceptual and logical views are present, and any omitted view is justified.
- [ ] Every connector in every diagram is labeled with its relationship type.
- [ ] Component names are identical across diagrams, the catalog, and the traceability matrix.
- [ ] The architecture respects the system boundary from the Ch5 context model.

**Evaluation and cross-cutting concerns**

- [ ] At least three scenario walkthroughs were performed, with results recorded.
- [ ] Logging and observability are addressed, so unanticipated failures can be detected and diagnosed.
- [ ] Error handling and authentication and authorization are addressed.

**Domain-agnosticism and honesty**

- [ ] Nothing in the output depends on domain knowledge or technology that is not in the inputs, or it is flagged as an assumption.
- [ ] No functional requirements were silently added.
- [ ] No implementation code or detailed class design was produced.
- [ ] Any gap, strained scenario, or unresolved trade-off is stated openly.
