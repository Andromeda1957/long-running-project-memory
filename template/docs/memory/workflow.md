# Workflow Memory

## Current Setup

- This repo uses a layered, repo-backed memory system:
  `AGENTS.md` / `CLAUDE.md`, `docs/runbooks/`, `AGENT_HANDOFF.md`,
  `PROJECT_MEMORY.md`, `docs/memory/`, `docs/plans/`, `CHANGELOG.md`, and
  `docs/repo_history/`.
- `PROJECT_MEMORY.md` is the router. It should stay short and point agents to
  topic memory, plans, runbooks, and archives instead of becoming an
  encyclopedia.
- `tools/check_memory_system.py` validates the memory-system shape and should
  run before committing memory-system changes.
- Claude-specific startup glue lives under `.claude/`. Codex repo-scoped skills
  live under `.agents/skills/`.

## Current Rules

- Keep current facts separate from history. Current setup/rules live in topic
  memory; retired context lives in `docs/repo_history/`; completed audit history
  lives in `CHANGELOG.md`.
- Do not read `CHANGELOG.md` or `docs/repo_history/` at startup by default.
- Keep `AGENT_HANDOFF.md` current-state-only and under the validator line limit.
- Keep `AGENTS.md` and `CLAUDE.md` byte-for-byte identical.
- Do not propose structural memory revisions when
  `python3 tools/check_memory_system.py` passes and the fixed review rubric in
  `docs/runbooks/memory-review.md` has no failures.

## Accepted Baseline / Known Tradeoffs

- The system intentionally favors explicit repo-backed markdown over hidden
  model memory, automatic capture, embeddings, or external memory daemons.
- The validator checks shape, not semantic truth. Human review and direct
  verification still matter.
- The handoff is intentionally disposable. Completed work belongs elsewhere.
- The archive layer preserves context without making old facts authoritative.

## Runbooks

- `docs/runbooks/task-memory-triage.md`
- `docs/runbooks/docs-change.md`
- `docs/runbooks/memory-maintenance.md`
- `docs/runbooks/memory-review.md`

## Lookup Anchors

- `AGENTS.md`
- `CLAUDE.md`
- `PROJECT_MEMORY.md`
- `AGENT_HANDOFF.md`
- `tools/check_memory_system.py`
- `.claude/hooks/session-start-context.sh`
- `.agents/skills/`

## Deprecated / Historical

- None yet. Move large retired context to `docs/repo_history/` and leave a
  targeted pointer here only when it remains useful.
