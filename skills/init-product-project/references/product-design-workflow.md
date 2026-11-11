# Product and design decisions

Read for design-ready/code-ready foundations or requested product exploration. Reuse existing documents; these sections do not require new files. Apply only what changes a decision in the current scope.

## Problem and evidence

In the brief, identify the actor, situation/trigger, job, current workaround, friction, and desired outcome. Distinguish user, buyer/payer, decision-maker and operator only when their needs differ. Capture the business or organizational outcome without assuming revenue is relevant.

For each material claim, link evidence with source, date, context, population where known, limitations and conflicting findings. A stakeholder-approved brief is agreement, not user validation. Unknowns remain hypotheses. Select the uncertainty most likely to change the solution or scope as the next learning question; do not require broad research before a small workspace setup.

## Business behavior

When rules, permissions, transactions or multiple actors affect behavior, capture in the brief or owning feature packet:

- actors and authority;
- entities and business lifecycle;
- trigger, preconditions, rule, permitted state transition, outcome and exception;
- operator or service responsible for recovery and any known response expectation.

Use IDs for rules that acceptance needs to reference. UI loading/error states and business states serve different purposes. Do not invent thresholds, eligibility, deadlines or policy. Mark unknown rules and what they block. Simple content websites may mark this section not applicable.

## Options and first scope

If the solution is unsettled, compare meaningful alternatives, including improving an existing process when relevant. Use user value, organizational outcome, evidence confidence, effort, dependencies and risk; no mandatory scoring formula or number of options. Respect a user-selected solution unless a material contradiction needs surfacing.

Record the selected approach and why, rejected/deferred options, and the smallest complete journey worth delivering or testing. Technical foundations are dependencies, not the reason a feature is valuable. Separate MVP scope from a learning prototype. Link the owning decision from the roadmap.

## Experience and operations

Describe entry, successful outcome, intermediate steps, relevant alternate paths, content and recovery. Cover accessibility/input and adaptive behavior for actual platforms. For multi-party services, show what the user, system and operator each do, handoff points and who handles failure. Do not require a service blueprint for a simple single-user tool.

Reuse accepted design systems. Make intentional changes explicit; do not require a formal exception for ordinary branding.

## Validate the risky assumption

In the research register, define the question, relevant people/context, method, task or stimulus, observable success/failure signal, decision threshold where justified, and evidence needed. Methods may include existing research, expert walkthrough, feasibility experiment, prototype or user sessions. State limitations: a desk review does not demonstrate user success; synthetic responses are not research participants.

Run only feasible, authorized checks. Otherwise record a plan and pending evidence, not a result. After a check, record actual observations, contradictions, limitations and whether to continue, revise or stop. Failed validation reopens the affected decision and readiness claim, not every unrelated feature.

A learning prototype can be explicitly scoped before production code-ready. Record mock data, unsupported states, safety boundaries and what must be revisited before reuse. Do not publish, recruit or contact participants without authorization.

## Acceptance and measurement

Translate important rules and design decisions into concrete scenarios: initial state/data, action, expected observable outcome and linked rule/decision. Include material negative and recovery cases. Given/When/Then is optional; vague category checkboxes alone are insufficient for code-ready.

Define a proportionate outcome measure: meaning, population/context, baseline (unknown if absent), target or learning signal, time window, data source, owner and guardrail. Do not invent targets or enable analytics. Identify the review trigger and what would prompt continuation, revision or stopping. Existing observations or manual review may be sufficient.

## Keep ownership clear

Brief owns problem, outcomes and product constraints. Feature packet owns scoped rules and acceptance. Decision record owns a substantial choice. Research register owns validation evidence. Readiness links these sources and states what next action they support. Reuse equivalent existing owners rather than duplicating text.
