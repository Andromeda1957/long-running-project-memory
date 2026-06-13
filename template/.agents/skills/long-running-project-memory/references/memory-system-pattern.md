# Memory System Pattern

Use this reference when implementing or reviewing a memory system for a
long-running project.

## Recommended Layout

```text
AGENTS.md
CLAUDE.md or other assistant shims
AGENT_HANDOFF.md
PROJECT_MEMORY.md
CHANGELOG.md
docs/runbooks/
docs/memory/
docs/plans/
docs/repo_history/
```

## File Responsibilities

### Agent Contract

Use for behavior that applies to every task:

- startup protocol;
- task classification;
- source-of-truth hierarchy;
- memory discipline;
- universal safety rules;
- links to runbooks.

Keep it small. Do not store domain setup details or history here.

### Assistant Shims

Use for assistant-specific ownership and compatibility notes only. Do not
duplicate the full agent contract.

### Active Handoff

Use only for:

- active objective;
- last known state and timestamp;
- exact next action;
- blockers;
- immediate "do not do this now" facts;
- dirty worktree caveats.

Avoid completed history, broad rules, old verification logs, and changelog
summaries. Target 50-100 lines.

### Project Memory Router

Use as an index. Include topic links and global current facts only. Do not let it
become the encyclopedia.

### Topic Memory

Use one file per domain. Suggested sections:

```markdown
# Topic

## Current Setup
Facts true now.

## Current Rules
Rules agents must follow now.

## Runbooks
Relevant workflow files.

## Lookup Anchors
Code paths, commands, models, templates, logs.

## Deprecated / Historical
Old facts retained for context. Never operative unless promoted.
```

### Plans

Use for deferred or multi-phase implementation work that is not active enough
for `AGENT_HANDOFF.md` and not general enough for a runbook. Plans should use
explicit status values, name resume prompts when useful, and avoid completed
history.

### Repository History

Use `docs/repo_history/` for retired plans, old memory snapshots, large
historical notes, and archived context that should remain available for audit
without loading as current state. Do not let archive files override active
handoff, topic memory current sections, code/config, or fresh command output.

### Runbooks

Use for recurring workflows, for example:

- application/runtime changes;
- docs/repo-maintenance changes;
- deploy and backup;
- verification (UI or behavior);
- production operations;
- data/worker jobs;
- memory maintenance.

Runbooks should be checklists. They preserve global steps that agents must not
forget.

### Changelog

Use as append-only history. Do not require default startup reads. Read it only
for history, audit, or when current memory points to a specific entry.

## Conflict Resolution

For live facts:

1. Fresh command output.
2. Active handoff.
3. Topic memory current sections.
4. Code/config.
5. Project memory router.
6. Plans, when the request or current memory routes to a specific plan.
7. Changelog/repo history.

For required behavior:

1. Agent contract.
2. Relevant runbooks.
3. Enforcing scripts/hooks/tests.
4. Topic memory rules.

## Enforcement Ideas

Add a small check script when the project is stable enough. It can fail if:

- required memory/runbook files are missing;
- handoff exceeds a line limit;
- handoff contains forbidden headings such as `Latest Completed`;
- topic memory files lack required sections;
- project-local skills or memory routers omit the plans layer;
- repo history archive is missing from the source hierarchy;
- project memory stops being a router;
- startup rules begin requiring broad changelog reads again.

Wire the checker into a pre-commit hook when available.

## Anti-Patterns

- One giant memory file loaded every session.
- Handoff as a second changelog.
- Recent behavioral corrections dominating normal work.
- Historical facts sitting beside current facts without labels.
- Deferred implementation plans hiding in handoff, topic memory, or root TODO
  files.
- Retired plans and old memory snapshots left in current startup context.
- Agent entrypoints duplicated across assistants.
- Memory edits triggered by every conversational correction.
- Recovery docs excluded from routine validation.
