# Topic Memory

One file per domain topic (`accounts.md`, `deployment.md`, `frontend.md`, ...).
Each holds **current durable facts** for that topic, with history kept separate.

Copy `_topic-template.md` to start a new topic, then add a line for it in
`PROJECT_MEMORY.md`'s topic index.

Every topic file must contain these five sections (the validator enforces it):

- `## Current Setup`
- `## Current Rules`
- `## Runbooks`
- `## Lookup Anchors`
- `## Deprecated / Historical`

`README.md` and any file beginning with `_` are skipped by the validator, so the
template itself is not required to follow the shape.

Keep `Current` sections operative and move outdated facts down into
`Deprecated / Historical` rather than deleting them. If the historical context
is large, cross-topic, or a retired plan, move it to `docs/repo_history/` and
leave only a short pointer in the relevant topic file.
