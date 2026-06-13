# Memory Maintenance Runbook

Use only when the user asks to update memory/docs, when the active task is memory
maintenance, or when stale memory would cause imminent risky action.

## Principles

- Keep `AGENTS.md` small and stable.
- Keep `AGENT_HANDOFF.md` current-state-only.
- Put current durable facts in `docs/memory/<topic>.md`.
- Put required workflow steps in `docs/runbooks/<workflow>.md`.
- Put audit history in `CHANGELOG.md`.
- Put retired plans, archived context, and large historical records in
  `docs/repo_history/`.
- Put small topic-specific old facts in `Deprecated / Historical` sections.
- Preserve old context instead of deleting it when it may be useful later.

## Steps

1. Identify whether the change is behavior, workflow, current fact, active
   state, plan, audit history, or archived context.
2. Use `docs/runbooks/task-memory-triage.md` before editing if the maintenance
   task creates or changes a multi-phase plan, recurring workflow, or active
   handoff state.
3. Edit the smallest appropriate file.
4. Do not update agent entrypoints (`AGENTS.md` / `CLAUDE.md`) for ordinary
   topic-memory changes.
5. If you changed `AGENTS.md`, mirror it to `CLAUDE.md` (`cp AGENTS.md
   CLAUDE.md`).
6. Run `git diff --check`.
7. Run `python3 tools/check_memory_system.py`.
8. Run any syntax/lint checks for touched scripts.
9. Commit and record the maintenance change in `CHANGELOG.md`.

## Handoff Limit

Target `AGENT_HANDOFF.md` at 50-100 lines. It must not contain:

- `Latest Completed` sections;
- completed task history;
- long verification logs;
- broad durable rules that belong in topic memory or runbooks.

Wire `tools/check_memory_system.py` into a pre-commit hook or CI so it fails
when the handoff grows past the hard limit or required memory/runbook files
disappear.
