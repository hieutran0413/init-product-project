# Init Product Project

Create a documented product foundation from a brief or integrate missing documentation into an existing repository. Includes one Codex skill and a Python initializer; no MCP service or application dependencies.

## Usage

Invoke `$init-product-project` with the brief, destination, and desired depth: workspace-only, design-ready, code-ready, or explicitly requested implementation.

```sh
python3 skills/init-product-project/scripts/init_product_project.py --name "Example" --type cli --path /absolute/real/path/example --dry-run
```

Inspect the plan, then omit `--dry-run` to create it. For an inspected existing project, `--integrate` preserves all existing files. Prefer its existing documentation layout over generating a parallel one. Destination paths must not contain symlinks; use a verified real path.

The initializer creates documentation only. Readiness remains unassessed until the agent records evidence. It does not install dependencies, create Git history, publish, or implement an application.

## Verification

Python 3.10+ and Git for the ignore-rule test. Tests use the Python standard library.

```sh
python3 -m unittest discover -s skills/init-product-project/tests -v
```

## 0.3.0

- Clarify the requested depth and known decisions before writing.
- Add conditional business rules, operational handoffs, option selection and MVP rationale.
- Separate agreement, specification completeness and validation; support authorized learning prototypes before production readiness.
- Connect risky assumptions to validation plans and concrete acceptance scenarios.
- Add proportionate outcome measurement and review triggers without inventing targets or enabling analytics.
- Explain which documents to use now or defer; the initializer still emits the full compatible template kit.
- Include six behavioral evaluation prompts in `skills/init-product-project/tests/behavior-scenarios.json`. A rubric is not proof of an evaluation pass.

## 0.2.0

- Reject symlinks in the destination and its ancestors before filesystem resolution.
- Report filesystem write failures with partial-scaffold recovery guidance.
- Substitute template tokens once and reject unresolved tokens before writing.
- Add a linked readiness assessment with evidence, applicability, gaps, owners, and next action.
- Explain non-visual consumer journeys for API, CLI, and library projects.
- Cover all 11 supported project types and remove the test suite's undeclared PyYAML dependency.

This source repository is the Git-backed marketplace owner. Publishing the source and refreshing the installed plugin are separate from editing or packaging this directory.
