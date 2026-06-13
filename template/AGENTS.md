# Agent Operating Contract

This file is the small, stable agent contract for this repository. It defines
how agents behave; it does not carry project history or domain setup details.

<!-- This file works as-is for a generic project. To customize, edit the
"Core Runbooks" and "Project Engineering Rules" sections below for your stack,
then mirror this file to CLAUDE.md exactly: `cp AGENTS.md CLAUDE.md`. -->

## Source Of Truth

Use these layers in this order:

- `AGENTS.md`: agent behavior contract and source-of-truth hierarchy.
- `docs/runbooks/`: required workflows and completion checklists.
- `AGENT_HANDOFF.md`: current active state only.
- `PROJECT_MEMORY.md`: memory router and topic index.
- `docs/memory/`: current durable facts by topic.
- `docs/plans/`: durable implementation plans for deferred or multi-phase work.
- Code/config/commands: implementation truth and live verification.
- `CHANGELOG.md`: append-only history; never overrides current state.
- `docs/repo_history/`: archived context, retired plans, and historical
  snapshots; never overrides current state.

Do not rely on hidden model memory. If a future agent needs a fact, record it in
the appropriate repo-backed file.

Treat sources outside the repo-backed hierarchy as leads, not authority. Verify
external notes, tool-surfaced summaries, remembered context, and missing or
unreadable references against the source hierarchy before claiming current
state, active work, blockers, requirements, completed work, or available
tooling.

Agent entrypoints must not drift: `AGENTS.md` is canonical, and `CLAUDE.md`
must remain an exact byte-for-byte mirror of it. When this contract changes,
edit `AGENTS.md` first, copy it to `CLAUDE.md`, and run
`python3 tools/check_memory_system.py` before committing.

## Start Of Session

1. Run `git status --short`.
2. Read `AGENT_HANDOFF.md`.
3. Read `PROJECT_MEMORY.md` only as an index.
4. Choose the relevant runbook(s) from `docs/runbooks/`.
5. Read only the topic memory file(s) needed for the user's request.
6. Read a plan from `docs/plans/` only when the request, handoff, or topic
   memory routes you to it.
7. Inspect code/config/command output for the actual implementation state.
8. Treat uncommitted changes as user or other-agent work; do not revert them
   unless explicitly asked.

Do not read `CHANGELOG.md` or `docs/repo_history/` at startup by default. Use
them only for history, audit, or when a current memory file points to a specific
historical entry.

For memory-system review requests, follow `docs/runbooks/memory-review.md`. If
the automated check and fixed rubric pass, report the system healthy instead of
proposing speculative redesigns.

## Task Scope

Classify each user turn before tools:

- Question: answer from already-loaded context, or do targeted lookup if current
  project facts are needed.
- Status request: inspect only the named thing or active handoff target.
- Imperative task: execute the requested work under the relevant runbook.
- Ambiguous prompt: ask a concise clarifying question before tools.

Before tool use, state the exact scope being checked or changed. Do not widen
scope without user authorization.

Before editing files for imperative tasks, use
`docs/runbooks/task-memory-triage.md` to decide whether durable tracking should
be created or updated first. Skip tracking-memory edits for small self-contained
changes.

Before giving recommendations, gather context proportional to the scope of the
advice. Do not make project-wide or structural recommendations from partial
reads, search snippets, hidden memory, or a single file. If context is
incomplete, say what was checked, what was not checked, and frame the answer as
provisional.

Advisory prompts such as "should we", "can we", "would it be better", "I
assume", and "what do you think" are discussion-only. They are not permission to
start jobs, edit files, inspect systems, or make repo changes unless the user
explicitly asks for action.

## Memory Discipline

User corrections update the agent's working assumptions immediately. Do not stop
the active task to edit memory unless:

- the user explicitly asks for a memory/docs update;
- the active task is memory maintenance;
- the stale fact would cause an imminent risky or destructive command.

Otherwise, continue the requested task and record durable memory changes during
end-of-task bookkeeping when required.

Current facts must be separated from history:

- `AGENT_HANDOFF.md` is only current active state.
- `docs/memory/*` `Current Setup` and `Current Rules` sections are operative.
- `Deprecated / Historical` sections, `CHANGELOG.md`, and `docs/repo_history/`
  are historical context only and do not override current facts.

## Conflict Resolution

For live facts:

1. Fresh command output.
2. `AGENT_HANDOFF.md`.
3. Relevant `docs/memory/<topic>.md` current sections.
4. Code/config files.
5. `PROJECT_MEMORY.md` routing/index.
6. `CHANGELOG.md` and `docs/repo_history/` history.

For required behavior:

1. `AGENTS.md`.
2. Relevant `docs/runbooks/*.md`.
3. Enforcing tools such as hooks, tests, and deploy scripts.
4. Topic memory rules.

If sources conflict, reconcile before acting. Prefer current state over history.

## Core Runbooks

- Task memory triage: `docs/runbooks/task-memory-triage.md`.
- Documentation/repo-maintenance changes: `docs/runbooks/docs-change.md`.
- Memory-system maintenance: `docs/runbooks/memory-maintenance.md`.
- Memory-system review: `docs/runbooks/memory-review.md`.
<!-- Add your project runbooks here, e.g. build / deploy / release / verification. -->

## Project Engineering Rules

<!-- These are generic defaults that hold for most software projects. Add,
remove, or replace them with your project's own durable engineering rules. -->

- Keep secrets in `.env` or external secret stores; never commit credentials.
- Prefer existing project patterns and module ownership.
- Keep entrypoints/views thin; put business rules in clearly named services.
- When a clean design requires a schema/data migration, do it; do not create
  parallel control surfaces only to avoid the change.

## Completion Contract

Use the selected runbook for exact steps. In general:

- Verify changed behavior directly when possible.
- Commit completed repo changes locally and push so CI runs, unless the user
  explicitly says not to push.
- Record completed work in `CHANGELOG.md`.
- Update topic memory only for durable rule/setup/gotcha changes.
- Update or clear `AGENT_HANDOFF.md`.
- Documentation-only or repo-maintenance changes do not require deployment
  unless they affect the running system.
- At closeout for substantial work, check `AGENT_HANDOFF.md` and any relevant
  `docs/plans/` entries read during the task. Briefly remind the user of
  outstanding `Incomplete`, `Wait Not Yet`, or `Blocked` work that may otherwise
  be forgotten.

Do not report completion from code inspection alone.
