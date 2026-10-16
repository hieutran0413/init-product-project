# Product Project Quality Gates

## Contents

1. Discovery
2. Design-ready
3. Code-ready
4. Implementation
5. Execution admission
6. Verification and release
7. Universal checks

## Applicability

Apply gates to the requested scope and product type. For APIs, CLIs, and libraries, replace visual and screen criteria with consumer journeys, contracts, output, errors, compatibility, and usage examples. Mark irrelevant criteria Not applicable with a reason. Release checks apply only to release work. Existing user choices count as authority; document them instead of asking again. Readiness records evidence, not authorization.

## Discovery

Required:

- named user and primary job;
- problem and successful outcome;
- project type and distribution target;
- evidence separated from assumptions;
- explicit scope and non-goals;
- major privacy, safety, data, entitlement, and platform constraints;
- for an existing product, visual strategy, design-system source of truth, owner, and preserve/evolve/replace posture;
- unresolved decisions and owners.

Output status: `discovery`.

## Design-ready

Required:

- information architecture and complete primary flow;
- visual target or accepted native/system direction for new work, or an audited existing presentation strategy for an established product;
- system-chrome and product-surface boundaries, including any accepted bespoke components;
- empty, loading, populated, error, partial, offline, editing, and destructive states where applicable;
- responsive/adaptive platform behavior;
- content/copy and recovery;
- interaction priority and cancellation;
- accessibility and input behavior;
- intentional differences from references.

Output status: `design-ready`.

Do not use one happy-path mock as design-ready evidence.

## Code-ready

Required:

- accepted design-ready gate;
- local and remote sources of truth;
- data/API capability contract and owner;
- architecture/stack decision;
- privacy/security and entitlement behavior;
- migrations and destructive consequences;
- acceptance scenarios;
- deterministic fixtures/previews;
- test/check commands;
- files/modules in scope and forbidden shortcuts;
- custom controls with material behavior or accessibility tradeoffs, if any: user outcome, why an adequate standard control is insufficient, source owner, accessibility route, adaptive/platform fallback, performance budget, and validation method;
- no implementation-blocking `TBD`.

Output status: `code-ready`.

## Implementation

Required:

- inspect current repository before edits;
- preserve useful existing behavior;
- implement one scoped feature packet;
- keep presentation separate from infrastructure;
- handle cancellation, repeated input, partial failure, stale results, and recovery;
- remove placeholders and migrated legacy callers;
- record assumptions and intentional differences.
- preserve accepted bespoke identity unless a documented decision authorizes replacement.

Output status: `in-progress` or `verification`.

## Execution admission

Before implementation:

- identify the feature packet’s critical path and highest-risk assumptions;
- group work into a small number of product-specific priorities such as P0/P1/P2;
- define a measurable exit condition for every priority or dependency gate;
- keep only tasks whose prerequisites have evidence `active`;
- mark dependency-blocked tasks `gated`, not `in-progress`;
- distinguish scaffolding or premature code as `prototype exists`, never verified progress;
- define an interaction-critical performance budget when latency, rendering, media, synchronization, safety, or device control is material;
- record known implementation differences and technical debt in the owning packet.

Prefer one complete vertical journey over many simultaneously started layers. A task may be active in parallel only when its dependencies are satisfied and the work does not hide the critical path.

Suggested task states:

| State | Meaning |
| --- | --- |
| `pending` | Authorized but not admitted |
| `gated` | Blocked by named prerequisite evidence |
| `active` | Prerequisites passed and implementation is underway |
| `verification` | Behavior is complete; acceptance evidence is being collected |
| `accepted` | Owning gates passed with recorded evidence |

Prototype code can inform a later task, but it cannot advance that task’s status until its prerequisites and acceptance checks pass.

## Verification and release

Required:

- full journey works, not only isolated screens;
- unit/integration/UI checks appropriate to risk;
- accessibility runtime checks;
- responsive/adaptive destinations;
- security/privacy review;
- performance evidence for material claims;
- validation of bespoke exceptions against their accessibility, adaptive-layout, performance, and visual acceptance criteria;
- build/package/archive;
- deployment and rollback plan;
- verified status updated from evidence only.

Output status: `accepted` or `released`.

## Universal checks

At every gate:

- one document owns each decision;
- evidence is traceable;
- plan is not reported as status;
- temporary artifacts are not committed;
- secrets and customer data are absent;
- destructive and external actions require authority;
- preserve accepted visual identity and document material custom-control tradeoffs;
- the next action and owner are explicit.
