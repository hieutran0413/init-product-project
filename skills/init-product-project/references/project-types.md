# Project Types and Routing

## Contents

1. Selection rule
2. Type matrix
3. Stack decision
4. Platform cautions

## Selection rule

Choose the product form from the user's job, distribution, input, offline, device integration, performance, and maintenance needs. Do not choose from visual resemblance alone.

## Type matrix

| Type | Use when | Resolve before code | Typical downstream route |
| --- | --- | --- | --- |
| `website` | Content, marketing, documentation, campaign, portfolio | audience, conversion, content owner, SEO, CMS, analytics, hosting | Product Design → web/Sites |
| `web-app` | Authenticated or stateful browser workflow | roles, data ownership, responsive breakpoints, offline, browser support, API | Product Design → web implementation |
| `ios-app` | Apple-native mobile/tablet behavior or system integration | iPhone/iPad scope, minimum OS, persistence, sync, entitlements, App Review | Product Design → SwiftUI native design |
| `android-app` | Android-native distribution or platform integration | device range, minimum SDK, Material/native conventions, Play policy | Product Design → Android implementation |
| `cross-platform-app` | Shared mobile product with justified common layer | native gaps, platform divergences, offline, modules, release pipelines | Product Design → selected cross-platform skill |
| `desktop-app` | Windowed, keyboard/pointer-heavy, local-file, or OS-integrated work | operating systems, window model, files, updates, sandbox | Product Design → platform-native desktop route |
| `internal-tool` | Known team workflow and controlled users | roles, permissions, auditability, data sources, deployment, support owner | Product Design → web/tool implementation |
| `api` | Machine-to-machine capability | consumers, contract, auth, versioning, errors, limits, observability | Architecture/API implementation |
| `cli` | Scriptable developer/operator workflow | platforms, shell behavior, config, output schema, exit codes, packaging | CLI implementation |
| `library` | Reusable code consumed by other projects | public API, compatibility, versioning, package registry, test matrix | Library/package implementation |
| `other` | The product does not fit a standard type | lifecycle, users, distribution, interfaces, persistence | Write a decision record first |

## Stack decision

Score candidates against:

1. Native product behavior and accessibility.
2. Existing team/repository capability.
3. Required integrations and platform APIs.
4. Deployment and operational ownership.
5. Offline, data, privacy, and security requirements.
6. Performance and expected scale.
7. Testability and release pipeline.
8. Long-term maintenance and ecosystem stability.

Reject a stack when its main benefit is familiarity but it weakens a material product requirement.

Record:

```text
Decision:
Product constraints:
Alternatives:
Why selected:
Known gaps:
Validation:
Revisit trigger:
```

## Platform cautions

- Do not turn a native-app request into a website without approval.
- Do not require an account, cloud service, analytics, or monetization without product authority.
- Do not infer responsive behavior from one desktop or mobile frame.
- Do not copy another platform's navigation/control presentation literally.
- Do not create a design system before inspecting existing tokens and components.
- Do not deploy, publish, purchase services, or create remote repositories without authorization.

