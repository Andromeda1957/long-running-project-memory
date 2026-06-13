# Documentation And Repo-Maintenance Runbook

Use for docs-only, memory-system, runbook, handoff, changelog, or repo
maintenance changes that do not affect the running system.

## Steps

1. Read `AGENT_HANDOFF.md`.
2. Read relevant topic memory/runbooks only.
3. Before editing files, use `docs/runbooks/task-memory-triage.md`; for
   self-contained docs fixes, proceed without tracking-memory churn.
4. Make the scoped docs or repo-maintenance change.
5. Run appropriate verification:
   - `git diff --check`
   - syntax/lint checks for any changed scripts
   - `python3 tools/check_memory_system.py` when touching memory-system files
6. Update `CHANGELOG.md`.
7. Update `AGENT_HANDOFF.md` only if active state changed or the task remains
   incomplete.
8. Commit locally.

## No Deploy

Documentation-only and repo-maintenance changes do not require deployment unless
they affect runtime files or the user explicitly requests it.

## No Backup Sync By Default

If your project has a recovery-backup workflow, reserve it for runtime or
deployed-system changes. Docs-only and memory-system changes do not need backup
sync unless the user asks or the change also affects deployed behavior.
