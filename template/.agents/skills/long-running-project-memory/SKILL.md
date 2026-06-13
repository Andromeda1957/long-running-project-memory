---
name: long-running-project-memory
description: Design, audit, or repair scalable memory systems for long-lived software projects. Use when Codex needs to organize agent instructions, runbooks, handoffs, project memory, changelogs, recovery docs, or multi-agent continuity; prevent stale facts from overriding current state; reduce startup context; or add enforcement for project memory discipline.
---

# Long-Running Project Memory

Use this skill to turn a growing project from ad hoc notes into a durable,
low-friction operational memory system.

## Core Model

Separate six layers:

1. **Agent contract**: small, stable behavior rules.
2. **Runbooks**: repeatable task workflows and completion checklists.
3. **Active handoff**: current state only, short-lived and replaceable.
4. **Topic memory**: current durable facts by domain.
5. **Plans**: deferred or multi-phase implementation plans.
6. **History**: append-only changelog plus archived/deprecated context.

Do not let one file carry all six layers.

## Workflow

1. Inspect the existing memory files, docs, runbooks, plans, changelog, and
   handoff.
2. Identify where current facts, historical facts, behavior rules, and task
   checklists are mixed together.
3. Propose a source-of-truth hierarchy before editing.
4. Preserve old memory as historical context instead of deleting it.
5. Move required workflows into runbooks.
6. Move current durable facts into topic memory files.
7. Move deferred or multi-phase implementation work into plans.
8. Move retired plans, old memory snapshots, and large archived context into
   `docs/repo_history/`.
9. Slim agent entrypoints to behavior and lookup rules.
10. Slim handoff to active state only.
11. Add lightweight enforcement when possible.
12. Verify references, line limits, and check scripts.

For detailed patterns and templates, read
`references/memory-system-pattern.md`.

## Operating Rules

- Current state beats history.
- Fresh command output beats repo memory for live facts.
- Changelog is audit history, not startup context.
- User corrections update working assumptions immediately; memory edits happen
  at end-of-task unless the user asked for memory maintenance or stale memory
  would cause imminent risky action.
- Runbooks preserve global steps so agents do not need huge startup context.
- Topic memory must separate `Current` from `Deprecated / Historical`.
- Plans preserve deferred implementation detail without making it active state.
- Repo history preserves old context without making it startup context or
  current authority.

## Good Outputs

- A small agent contract.
- A short current-state handoff.
- A topic index.
- Domain-specific memory files.
- Deferred implementation plans.
- Workflow runbooks.
- A preserved historical archive.
- Optional validation scripts or hooks that keep the system from regressing.
