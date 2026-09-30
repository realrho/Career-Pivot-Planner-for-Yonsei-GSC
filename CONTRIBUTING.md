# Working on the eight-week portfolio

Jira owns execution acceptance criteria; Notion contains the learning narrative; GitHub contains implementation and reproducible evidence. Keep the same W1–W8 identifiers in all three.

1. Read the weekly course and its prerequisite gate.
2. Work in task order Wn.1→Wn.2→Wn.3→Wn.4, using codex/wNN-<topic> branches.
3. Make a minimal implementation; test the behavior that could be wrong, including failure and permission boundaries.
4. Record expected/actual results, run configuration, commit, environment and limitations.
5. Open a PR that references the weekly issue and SCRUM key; update Notion Evidence with links.
6. Mark the task complete only after its AC is met. Documentation edits alone do not complete future features.

Use public or synthetic data. Do not commit .env, provider keys, company documents, personal data or confidential screenshots. Distinguish fixture, CPU, real model, cloud and GPU results. Read-only stubs cannot be presented as real integrations.

Function/class docstrings explain inputs, outputs and exceptions; non-obvious logic comments explain why. Prefer explicit contracts and small replaceable adapters over unnecessary class hierarchies.

Choose checks appropriate to the change: unit/contract for logic, integration for real stores/adapters, eval for retrieval/generation, restart/permission/duplicate tests for review, benchmark for performance. Avoid adding tests that simply repeat implementation details.
