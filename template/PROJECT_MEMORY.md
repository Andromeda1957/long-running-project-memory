# Project Memory

This file is the memory router. It is intentionally short. Use it to choose the
right runbook and topic memory file; do not turn it back into the project
encyclopedia.

## Source Layers

- Agent behavior: `AGENTS.md`.
- Required workflows: `docs/runbooks/`.
- Active state: `AGENT_HANDOFF.md`.
- Current durable facts: `docs/memory/`.
- Deferred implementation plans: `docs/plans/`.
- Historical audit trail: `CHANGELOG.md`.
- Archived context and retired plans: `docs/repo_history/`.

## Topic Index

- Workflow and memory system: `docs/memory/workflow.md`

<!-- Add one line per project topic memory file as you create them under
docs/memory/, e.g. "- Deployment and CI: `docs/memory/deployment.md`". -->

## Lookup Rules

- Read `AGENT_HANDOFF.md` for active work and live job state.
- Read only the topic file(s) relevant to the user's request.
- Read `docs/plans/` only when the request, handoff, or a topic memory file
  routes to a specific plan.
- Use search and code/config inspection for implementation truth.
- Use `CHANGELOG.md` only for history, audit, or when a topic file points there.
- Use `docs/repo_history/` only for archived context, retired plans, audit, or
  when a current memory file points to a specific historical entry.
- Treat `Deprecated / Historical` sections as non-operative.

## Global Current Facts

<!-- A short list of project-wide facts every agent should know up front (stack,
deploy target, hard constraints). Keep it small; details live in topic memory. -->

- Current active work, if any, is in `AGENT_HANDOFF.md`.
