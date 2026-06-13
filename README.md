# long-running-project-memory

**A repo-backed memory system that keeps AI coding agents continuous across
hundreds of sessions** — without relying on hidden model memory or chat-only
notes.

The core idea: durable agent context lives in **version-controlled files, split
into separate layers, each with exactly one job.** A small, dependency-free
validator enforces the shape so the system stays small and usable instead of
decaying into one giant `NOTES.md` that nobody trusts. It's strict about file
*shape* precisely so your content, workflow, and runtime can stay loose —
**opinionated about structure, agnostic about everything else.**

**Per-project memory, not per-user memory.** The repo is the boundary — an agent
working in one project can't see another's context, because isolation here is
[the substrate, not a setting](#per-project-not-per-user).

**No API key, no VPS, no daemon, no vector database, no custom harness.** It
rides the [Claude Code](https://claude.com/claude-code) / Codex CLI you already
run — `cp` a folder, `chmod +x`, run one stdlib Python script. Works with any
agent that can read files in your repo. This is a generic export of the memory
system that runs [andromeda1957.com](https://andromeda1957.com), a long-lived
chess archive, across hundreds of agent sessions.

---

## Why

Agents forget everything between sessions. The usual fixes each fail in their
own way:

- **One big notes file** grows without bound, mixes current truth with stale
  history, and becomes too long and contradictory to trust.
- **Hidden / model memory** isn't in the repo, can't be reviewed in a PR, and
  silently drifts from what the code actually does.
- **Memory daemons and vector vaults** (auto-capture + embeddings + a SQLite
  store) add real infrastructure to chase the same goal — and optimize *recall*
  when the problem is *truth*. ([Why not a vault](#why-not-a-vault).)

The differentiator here is **enforcement**. Most "agent memory" projects are a
`NOTES.md` convention with nothing stopping the decay. This system makes memory
**layered, repo-backed, and self-limiting**: each fact lives in the smallest
file that owns it, current state is kept separate from history, and a
dependency-free validator **[fails CI when the shape rots](#watch-it-catch-drift)**.
The hard part
everyone else skips is the forcing function — that's the part this ships.

## The six layers

No single file carries more than one of these:

| # | Layer | File(s) | Holds |
|---|-------|---------|-------|
| 1 | Agent contract | `AGENTS.md` (+ `CLAUDE.md` mirror) | Small, stable behavior rules and the source-of-truth order |
| 2 | Runbooks | `docs/runbooks/*.md` | Repeatable task workflows and completion checklists |
| 3 | Active handoff | `AGENT_HANDOFF.md` | Current in-progress state only — short-lived, replaceable |
| 4 | Topic memory | `docs/memory/<topic>.md` | Current durable facts, `Current` split from `Deprecated / Historical` |
| 5 | Plans | `docs/plans/*.md` | Deferred or multi-phase implementation plans |
| 6 | History | `CHANGELOG.md`, `docs/repo_history/` | Append-only completed history plus archived context; never overrides current state |

One file ties the layers together without being one of them: **`PROJECT_MEMORY.md`
is the router** — a thin index into the topic memory (layer 4), kept small on
purpose. It's injected at session start so the agent boots with a table of
contents, not the whole encyclopedia, and the validator fails it the moment it
stops being an index.

Three rules tie them together:

- **Live command output beats stored memory.** Verify before claiming current state.
- **Current sections beat historical ones.** `Deprecated / Historical`,
  `CHANGELOG.md`, and `docs/repo_history/` are context, not authority.
- **External notes and model memory are leads, not authority.** Check them against the repo.

## Per-project, not per-user

Assistant-style agents that pool everything into one identity — projects,
devices, calendars, chats — get cross-domain context bleed by default, and have
to *add* isolation back with profiles or separate instances. This inverts that:
the unit of memory is the **project**, not the user, and isolation is the
substrate rather than a setting.

It's one rule — *scope memory to the smallest unit that owns it* — at two zoom
levels:

- **Across projects:** the repo is the wall. Another project's memory is files in
  a directory that were never injected, so an agent here can't be poisoned by
  them — there's no shared pool to leak from in the first place.
- **Within a project:** the six layers and the thin router keep even a large
  monorepo from drowning in its own context; only the topic files a task needs
  get pulled in.

The pooled-memory approach separates by configuration. This separates by
construction.

## Quickstart

From the root of the repo you want to add memory to:

```sh
# 1. Copy the scaffold in (replace the path with this clone's location)
cp -r /path/to/long-running-project-memory/template/. .

# 2. Make the hook and validator executable
chmod +x .claude/hooks/session-start-context.sh tools/check_memory_system.py

# 3. Confirm the shape is valid
python3 tools/check_memory_system.py
# -> memory-system check passed
```

Then customize (see [Adopt it](#adopt-it-into-your-project) below) and commit.

## Or just hand it to your agent

The heavyweight memory tools distribute as **software** — so you inherit their
install surface, upgrade path, and breakage. This distributes as a **spec your
agent can satisfy.** The installer is the agent you already have.

It works because of what the artifact is made of: the files are **markdown** (an
agent reads and writes them natively) and the success condition is a **stdlib
validator** (a hard pass/fail the agent can target). So "set this up for project
X" isn't a vague ask — it's a well-formed, *verifiable* task. Point your agent
at this repo and say:

> Adapt this memory system to fit my project, then make
> `python3 tools/check_memory_system.py` pass.

None of the daemon/vault/embedding stacks can be installed that way — you can't
hand an agent "run my SQLite vault and observer model" and have it be done and
verifiable in one pass.

## What's in this repo

```
README.md                                      You are here
LICENSE                                        MIT
.gitignore
.github/workflows/memory-system.yml            CI that validates the shipped template
template/                                       Drop-in scaffold — the whole system lives here
├── AGENTS.md                                  Agent contract (canonical)
├── CLAUDE.md                                  Byte-for-byte mirror of AGENTS.md
├── AGENT_HANDOFF.md                           Active-state template
├── PROJECT_MEMORY.md                          Router / topic index
├── CHANGELOG.md                               Append-only history (seed)
├── .github/workflows/memory-system.yml        Ready-to-copy CI (runs the validator)
├── .claude/
│   ├── settings.json                          Registers the SessionStart hook
│   ├── hooks/session-start-context.sh         Injects contract + handoff + router
│   └── skills/long-running-project-memory/    Claude skill (SKILL.md), bundled in-repo
├── .agents/
│   └── skills/long-running-project-memory/    Codex skill (SKILL.md + agents/ + references/)
├── docs/
│   ├── memory/README.md
│   ├── memory/workflow.md                     Starter topic for the memory system itself
│   ├── memory/_topic-template.md              Topic shape with the 5 required sections
│   ├── plans/README.md
│   ├── repo_history/README.md                 Archive layer for retired context
│   └── runbooks/                              task-memory-triage, docs-change,
│                                              memory-maintenance, memory-review
└── tools/check_memory_system.py              Shape validator (stdlib only, no deps)
```

The runbooks shipped here are the **memory-system** ones. Add your own project
runbooks (build, deploy, release, verification...) beside them and list them in
`AGENTS.md`.

## Adopt it into your project

After the [Quickstart](#quickstart) copy, do the project-specific part:

1. **Write your contract.** The four core files work zero-edit as generic
   defaults, with customization hints left in HTML comments. Edit `AGENTS.md` —
   set the "Project Engineering Rules" and "Core Runbooks" sections to your
   stack, conventions, and hard constraints. Keep it small; it's the one file
   every session reads.
2. **Mirror it.** `cp AGENTS.md CLAUDE.md` (they must stay byte-for-byte
   identical; the validator enforces this).
3. **Add real topics.** The scaffold includes `docs/memory/workflow.md` for the
   memory system itself. Copy `docs/memory/_topic-template.md` to
   `docs/memory/<topic>.md` for each project domain (e.g. `deployment.md`,
   `frontend.md`), and list each one in the topic index in `PROJECT_MEMORY.md`.
4. **Add project runbooks.** Drop `docs/runbooks/<workflow>.md` files for your
   recurring tasks and reference them from `AGENTS.md`.
5. **Validate, then let CI enforce it** so the handoff can't bloat and required
   files can't silently disappear. Run it locally:
   ```sh
   python3 tools/check_memory_system.py
   ```
   A ready-to-copy GitHub Actions workflow ships at
   `.github/workflows/memory-system.yml` — it runs the same check on every push
   and PR, no dependencies to install.

> **Not using Claude Code?** Skip `.claude/` entirely — the file layout,
> runbooks, and validator stand on their own. The `SessionStart` hook is just
> the Claude-specific glue that auto-injects the contract at session start.

### Retrofitting an existing (messy) repo

Don't migrate everything at once — that just moves the big-ball-of-notes from
one place to another. Convert lazily, in this order:

- [ ] **Drop in the contract.** Add `AGENTS.md`, trim it to your real rules,
      `cp AGENTS.md CLAUDE.md`. This alone gives agents a stable starting point.
- [ ] **Sort your existing notes by *layer*, not by topic.** Current facts →
      `docs/memory/<topic>.md`; deferred work → `docs/plans/`; finished work →
      `CHANGELOG.md`; retired plans and large old context →
      `docs/repo_history/`. Small topic-specific outdated facts go under that
      topic file's `Deprecated / Historical` section, not deleted.
- [ ] **Create topic files only for domains you actually touch.** Leave the rest
      until a task needs them — an empty topic is better than a stale one.
- [ ] **Put just the in-flight state in `AGENT_HANDOFF.md`** and clear everything
      else out of it.
- [ ] **Add a runbook the first time you repeat a workflow,** not before.
- [ ] **Turn on CI** and let `check_memory_system.py` tell you what's still out
      of shape. Fix what it flags; ignore the rest until it matters.

## How agents use it

- **At session start**, the Claude Code `SessionStart` hook injects `AGENTS.md`,
  `AGENT_HANDOFF.md`, and `PROJECT_MEMORY.md` so the agent boots with the
  contract, current state, and an index — not the whole encyclopedia.
- **The skill** — methodology for designing, auditing, and repairing the system
  — is bundled **in the repo, never installed globally**, so it only loads where
  the system is actually used. Claude Code auto-loads it from `.claude/skills/`;
  Codex auto-discovers repo-scoped skills from `.agents/skills/` when launched
  inside the repository. Nothing is copied into `~` — per-project, by
  construction, exactly like the memory it manages.
- **During work**, the agent routes through `PROJECT_MEMORY.md` to the one or
  two topic files it needs, and follows a runbook for recurring tasks.

## The validator

`tools/check_memory_system.py` is pure Python stdlib (no install) and enforces
the invariants that keep the system honest:

- all required contract / runbook / skill / archive files exist;
- `CLAUDE.md` is a byte-for-byte mirror of `AGENTS.md`;
- `AGENT_HANDOFF.md` uses only the standard active-state heading, stays under
  the line limit, and contains **no** completed history (`Latest Completed` /
  `Changelog` / `Completed History` headings and common completed-work phrases
  are rejected);
- every `docs/memory/*.md` topic file has the five required sections;
- `PROJECT_MEMORY.md` stays a thin router and includes `docs/plans/` plus
  `docs/repo_history/`;
- `docs/plans/` contains resumable plans, not retired historical records;
- the `SessionStart` hook is registered, executable, and injects the right files;
- the memory-review runbook keeps its anti-churn language.

### Watch it catch drift

Say an agent starts parking completed work in the handoff — exactly the rot a
`NOTES.md` would swallow silently:

```diff
  # AGENT_HANDOFF.md
  ## Active State Summary
  - Mid-migration: opening-explorer rebuild in progress.

+ ## Latest Completed
+ - 2026-06-10 Shipped the opening-explorer rebuild; backfilled 23,706 games.
+ - 2026-06-09 Migrated the public DB to Postgres.
```

CI goes red:

```console
$ python3 tools/check_memory_system.py
memory-system check failed: AGENT_HANDOFF.md contains forbidden heading '## Latest Completed'
$ echo $?
1
```

The handoff is forced to stay current-state-only; that completed work belongs in
`CHANGELOG.md`. Same for a `CLAUDE.md` that drifts from `AGENTS.md`:

```console
$ python3 tools/check_memory_system.py
memory-system check failed: CLAUDE.md must be an exact byte-for-byte mirror of AGENTS.md
```

Run it locally, as a pre-commit hook (`python3 tools/check_memory_system.py`),
and in CI — the scaffold ships a GitHub Actions workflow at
`.github/workflows/memory-system.yml` that runs it on every push and PR with no
dependencies to install.

## Why not a vault

The vector-vault approach (auto-capture + embeddings + a SQLite store, shared
across runtimes) is the popular answer, and it's solving the wrong problem.

- **A vault optimizes recall, not truth — and rot is a truth problem.**
  Auto-capture ingests indiscriminately, so every stale, superseded, and
  contradictory fact goes in too. Retrieval is by similarity, and similarity is
  blind to currency: a deprecated fact is still *relevant*, so the vault happily
  surfaces it with a high score and presents it as current. There is no way to
  encode "this used to be true." This system's *Current beats Deprecated /
  Historical* rule is an explicit authority hierarchy a vector store
  structurally cannot represent.
- **Rot stays visible.** Rot in a markdown file shows up as a line in a PR diff
  a human catches. Rot in a vault shows up as a subtly wrong retrieval six
  sessions downstream that you can't trace back to a cause — invisible and
  unauditable, which is strictly *worse* than the `NOTES.md` it replaced.
- **What actually kills rot** isn't storage or retrieval — it's **legibility**
  (you can read it), **separation** (current split from historical), and a
  **forcing function** (CI that fails when the shape rots). This repo is built
  entirely from those three.

## Honest tradeoffs

Stated up front, because they're the real shape of the deal — not "set and
forget," but "cheap to adopt, honest by construction":

- **The validator checks shape, not substance.** It guarantees structure, not
  truth — an agent can produce six structurally-valid files that are
  semantically hollow. The session-start hook, the runbooks, and a human in the
  PR loop are what keep the *content* honest.
- **Capture and retrieval are manual.** The agent has to write to the right file;
  there's no background extraction. That's a feature for people who distrust
  automatic memory and a dealbreaker for people who don't want to think about it.
- **It caps volume in exchange for legibility.** Grep-plus-router over markdown
  has a ceiling; the topic split, thin router, and preserve-don't-delete rules
  push it far out, but they don't remove it. For one long-lived codebase that's
  the right trade every time. "Remember everything across my whole org/life" is
  a different product — don't reach for this there.
- **`CLAUDE.md` is a strict mirror by design.** The byte-for-byte rule buys
  zero drift between the contract and what Claude reads, at the cost of putting
  assistant-specific shims *in* that file. They don't go there: per-assistant
  behavior belongs in agent config (`.claude/` settings, skills) or a section of
  `AGENTS.md` that applies to everyone — not a diverging `CLAUDE.md`.
- **Agent-specific glue differs.** Claude has the SessionStart hook under
  `.claude/`; Codex uses repo-scoped skills under `.agents/skills/` plus the
  shared `AGENTS.md` contract. Both stay inside the project.

## Design rules worth keeping

- **One concern per file.** Behavior, workflow, active state, durable fact, and
  history never mix.
- **The handoff is disposable.** Current state only — no completed-work history.
- **The router stays thin.** `PROJECT_MEMORY.md` indexes; it is not the encyclopedia.
- **Reviews are self-limiting.** When the automated check and the fixed rubric
  pass, the system is healthy — don't reopen the whole design every session.
- **Preserve, don't delete.** Move stale facts to `Deprecated / Historical`
  sections or `docs/repo_history/` instead of dropping them.

## License

MIT — see [LICENSE](LICENSE).
