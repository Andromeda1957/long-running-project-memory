---
name: long-running-project-memory
description: >-
  Design, audit, or repair a repo-backed memory system for long-lived agent
  continuity. Use when the user asks about agent instructions, runbooks,
  handoffs, topic memory, changelogs, cross-session continuity, stale facts, or
  memory-system enforcement.
---

# Long-running project memory

Use this skill to keep a project's memory system durable, small, and usable by
any agent (Claude, Codex, or otherwise) across many sessions. The goal is
repo-backed continuity, not hidden model memory or chat-only notes.

## Core model

Keep six layers separate. No single file should carry more than one:

1. Agent contract: small, stable behavior rules.
2. Runbooks: repeatable task workflows and completion checklists.
3. Active handoff: current state only, short-lived and replaceable.
4. Topic memory: current durable facts by domain.
5. Plans: deferred or multi-phase implementation plans.
6. History: append-only changelog plus archived/deprecated context.

## Source hierarchy

Use the repo-backed hierarchy:

- `AGENTS.md` for the canonical agent contract.
- `CLAUDE.md` as an exact byte-for-byte mirror of `AGENTS.md` (for Claude Code).
- `docs/runbooks/` for required workflows.
- `AGENT_HANDOFF.md` for current active state only.
- `PROJECT_MEMORY.md` as the memory router and topic index.
- `docs/memory/` for current durable facts.
- `docs/plans/` for deferred implementation plans.
- Code, config, and command output for implementation truth.
- `CHANGELOG.md` for completed history only.
- `docs/repo_history/` for retired plans, old memory snapshots, and archived
  context that should not load as current state.

Fresh command output beats stored memory for live facts. Current sections beat
deprecated or historical sections. External notes and agent memories are leads,
not authority.

## Workflow

1. Follow the startup contract in `AGENTS.md`.
2. Read `PROJECT_MEMORY.md` only as an index, then read the relevant topic
   memory and runbook files.
3. For memory reviews, use `docs/runbooks/memory-review.md`; if the automated
   check and fixed rubric pass, report the system healthy instead of proposing
   speculative redesigns.
4. For actual memory changes, use `docs/runbooks/memory-maintenance.md` and
   `docs/runbooks/docs-change.md`.
5. Before edits or long-running work, apply
   `docs/runbooks/task-memory-triage.md` and create tracking memory only when
   the triage warrants it.
6. Identify whether the change belongs to behavior, workflow, active state,
   durable fact, plan, or history before editing.
7. Edit the smallest appropriate repo-backed file.
8. Preserve useful old context as historical context instead of deleting it.
9. Verify with `git diff --check` and `python3 tools/check_memory_system.py`.
10. Record completed maintenance in `CHANGELOG.md` and commit locally.

## Placement rules

- Put behavior and source-of-truth rules in `AGENTS.md`, then mirror exactly to
  `CLAUDE.md`.
- Put reusable task steps in `docs/runbooks/*.md`.
- Put active resumable state only in `AGENT_HANDOFF.md`.
- Put durable current facts, setup, decisions, and gotchas in
  `docs/memory/<topic>.md`.
- Put deferred implementation plans in `docs/plans/*.md`.
- Put completed-work audit entries in `CHANGELOG.md`.
- Put retired plans, old memory snapshots, and large archived context in
  `docs/repo_history/`.
- Do not put completed history in `AGENT_HANDOFF.md`.
- Do not expand `AGENTS.md` or `CLAUDE.md` for ordinary topic-memory changes.

## Good outputs

- A small agent contract.
- A short current-state handoff.
- A topic index instead of an encyclopedia.
- Domain-specific memory files with current and historical sections separated.
- A preserved historical archive for retired context.
- Workflow runbooks with direct completion gates.
- Lightweight validation that catches memory-system drift.
