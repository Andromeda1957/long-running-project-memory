# Task Memory Triage Runbook

Use before editing files or launching long-running work. The goal is to decide
whether the task needs durable tracking before implementation starts, not to
force memory edits for every small change.

## Decision

Create or update tracking memory before implementation when the task is likely
to be:

- multi-phase or cross-session;
- architecture, migration, toolchain, or workflow work;
- risky runtime work where partial progress matters;
- long-running, billable, deploy, recovery, or production-state work;
- dependent on owner approval or a deferred decision;
- useful for future agents to resume with a status checklist.

Skip tracking-memory edits when the task is:

- a question, status check, or narrow inspection;
- a typo, wording, or tiny one-file fix;
- a self-contained bug fix with immediate verification;
- already covered by an active handoff entry or existing topic-memory plan.

## Where To Record

- `AGENT_HANDOFF.md`: active state only, such as in-progress jobs, blockers,
  deploy state, or work that must be resumed soon.
- `docs/memory/<topic>.md`: durable setup, rules, gotchas, decisions, or
  multi-phase status plans.
- `docs/runbooks/<workflow>.md`: reusable workflow steps and completion
  checklists.
- `docs/repo_history/`: retired plans, archived context, and large historical
  records that are not current authority.
- `CHANGELOG.md`: completed history only, after the work is done.

Do not put completed task history in `AGENT_HANDOFF.md`. Do not put broad
workflow rules only in a topic-memory note when a runbook should enforce them.

At closeout, place memory by state:

- Completed-work narratives, verification logs, commit IDs, CI summaries, and
  audit trails go in `CHANGELOG.md`.
- Durable current setup, rules, gotchas, and recurring operational facts go in
  the relevant `docs/memory/<topic>.md` file.
- Deferred, multi-phase, blocked, or intentionally postponed implementation
  work goes in `docs/plans/<plan>.md` unless it must be resumed immediately.
- Retired plans and historical context that no longer describe current project
  status go in `docs/repo_history/`, with only active rules promoted to topic
  memory.
- `AGENT_HANDOFF.md` keeps only active work, exact next actions, blockers,
  immediate "do not do this now" facts, or dirty worktree caveats.

## Status Values

When a task needs a status plan, use these exact values:

- `Complete`: finished, verified, documented, and changeloged.
- `Incomplete`: planned but not started or not finished.
- `Wait Not Yet`: intentionally deferred until a listed prerequisite or owner
  decision is satisfied.
- `Blocked`: cannot proceed because an external dependency or unresolved
  decision prevents useful progress.
- `Skipped`: deliberately abandoned with a short reason.

## Loop

1. Read the relevant handoff, memory index, runbook, topic memory, and
   implementation context needed to scope the task.
2. Decide whether the task needs durable tracking before editing files or
   launching long-running work.
3. If tracking is warranted, create or update the smallest appropriate memory
   or runbook file first.
4. Implement the scoped task.
5. Verify directly.
6. Deploy and live-verify when the selected runbook requires it.
7. Update status memory, changelog, handoff, and commits according to the
   selected runbook.

Do not mark a tracked phase `Complete` from code inspection alone. It must meet
the documented completion gate.
