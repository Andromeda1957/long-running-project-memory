"""Validate the project memory-system shape.

Generic, dependency-free shape check for the long-running-project-memory
layout. Run from anywhere; it resolves the repo root as the parent of this
file's directory (this script lives in <repo>/tools/).

Exit code 0 and "memory-system check passed" mean the structural invariants
hold. Any failure raises SystemExit(1) with a message naming the problem.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    'AGENTS.md',
    'CLAUDE.md',
    '.claude/settings.json',
    '.claude/hooks/session-start-context.sh',
    '.claude/skills/long-running-project-memory/SKILL.md',
    '.agents/skills/long-running-project-memory/SKILL.md',
    '.agents/skills/long-running-project-memory/agents/openai.yaml',
    '.agents/skills/long-running-project-memory/references/memory-system-pattern.md',
    'PROJECT_MEMORY.md',
    'AGENT_HANDOFF.md',
    'docs/memory/workflow.md',
    'docs/plans/README.md',
    'docs/repo_history/README.md',
    'docs/runbooks/task-memory-triage.md',
    'docs/runbooks/docs-change.md',
    'docs/runbooks/memory-maintenance.md',
    'docs/runbooks/memory-review.md',
]

FORBIDDEN_HANDOFF_HEADINGS = [
    '## Latest Completed',
    '## Changelog',
    '## Completed History',
    '## Deferred Follow-ups',
]

ALLOWED_HANDOFF_HEADINGS = {
    '# Agent Handoff',
    '## Active State Summary',
}

HANDOFF_HISTORY_PATTERNS = [
    r'\bdone\s*\+\s*deployed\b',
    r'\bcomplete\s*/\s*deployed\b',
    r'\bcompleted\s*/\s*deployed\b',
    r'\bdeployed\s*\+\s*live-verified\b',
    r'\blive-verified\b',
    r'\bdeployed via\b',
    r'\bshipped latest\b',
    r'\bdetail(?:s)? in changelog\b',
    r'\bsee changelog\b',
    r'\bcommit(?:ted)?\s+(?:repo\s+)?state\b',
]

REQUIRED_TOPIC_SECTIONS = [
    '## Current Setup',
    '## Current Rules',
    '## Runbooks',
    '## Lookup Anchors',
    '## Deprecated / Historical',
]

MAX_HANDOFF_LINES = 120

REQUIRED_MEMORY_REVIEW_PHRASES = [
    'Do not propose structural memory revisions when checks pass',
    'If the automated check passes and no rubric item fails',
    'whole relevant memory system',
]

STARTUP_HOOK_COMMAND = '"$CLAUDE_PROJECT_DIR"/.claude/hooks/session-start-context.sh'


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding='utf-8')


def compact(text: str) -> str:
    return ' '.join(text.split())


def fail(message: str) -> None:
    raise SystemExit(f'memory-system check failed: {message}')


def require_startup_hook() -> None:
    settings_path = ROOT / '.claude' / 'settings.json'
    try:
        settings = json.loads(settings_path.read_text(encoding='utf-8'))
    except json.JSONDecodeError as exc:
        fail(f'.claude/settings.json is invalid JSON: {exc}')

    session_hooks = settings.get('hooks', {}).get('SessionStart', [])
    if not isinstance(session_hooks, list):
        fail('.claude/settings.json SessionStart hooks must be a list')

    has_startup_hook = False
    for entry in session_hooks:
        if not isinstance(entry, dict):
            continue
        for hook in entry.get('hooks', []):
            if not isinstance(hook, dict):
                continue
            if (
                hook.get('type') == 'command'
                and hook.get('command') == STARTUP_HOOK_COMMAND
            ):
                has_startup_hook = True

    if not has_startup_hook:
        fail('.claude/settings.json must register the SessionStart context hook')

    script_path = ROOT / '.claude' / 'hooks' / 'session-start-context.sh'
    if not script_path.stat().st_mode & 0o111:
        fail('.claude/hooks/session-start-context.sh must be executable')

    script = script_path.read_text(encoding='utf-8')
    for required_file in ('AGENTS.md', 'AGENT_HANDOFF.md', 'PROJECT_MEMORY.md'):
        if required_file not in script:
            fail(f'SessionStart hook must inject {required_file}')
    if 'Before any tool use' not in script:
        fail('SessionStart hook must remind the agent to classify before tool use')


def require_handoff_current_state(handoff: str) -> None:
    handoff_lines = handoff.splitlines()
    if len(handoff_lines) > MAX_HANDOFF_LINES:
        fail(f'AGENT_HANDOFF.md has {len(handoff_lines)} lines; max is {MAX_HANDOFF_LINES}')

    for line in handoff_lines:
        if not line.startswith('#'):
            continue
        if line not in ALLOWED_HANDOFF_HEADINGS:
            fail(
                'AGENT_HANDOFF.md must use only the standard active-state '
                f'headings; found {line!r}'
            )

    for heading in FORBIDDEN_HANDOFF_HEADINGS:
        if heading in handoff:
            fail(f'AGENT_HANDOFF.md contains forbidden heading {heading!r}')

    compacted = compact(handoff).lower()
    for pattern in HANDOFF_HISTORY_PATTERNS:
        if re.search(pattern, compacted):
            fail(
                'AGENT_HANDOFF.md appears to contain completed-work history '
                f'matching /{pattern}/'
            )


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        fail(f'missing required memory/runbook files: {", ".join(missing)}')

    handoff = read('AGENT_HANDOFF.md')
    require_handoff_current_state(handoff)

    project_memory = read('PROJECT_MEMORY.md')
    if 'This file is the memory router' not in project_memory:
        fail('PROJECT_MEMORY.md must remain a routing/index file')
    if 'docs/plans/' not in project_memory:
        fail('PROJECT_MEMORY.md must route deferred implementation plans')
    if 'docs/repo_history/' not in project_memory:
        fail('PROJECT_MEMORY.md must route archived repository history')

    memory_dir = ROOT / 'docs' / 'memory'
    if memory_dir.is_dir():
        for topic_path in memory_dir.glob('*.md'):
            # README and underscore-prefixed templates are not topic files.
            if topic_path.name == 'README.md' or topic_path.name.startswith('_'):
                continue
            text = topic_path.read_text(encoding='utf-8')
            missing_sections = [s for s in REQUIRED_TOPIC_SECTIONS if s not in text]
            if missing_sections:
                fail(f'{topic_path.relative_to(ROOT)} missing sections: {", ".join(missing_sections)}')

    agents = read('AGENTS.md')
    if 'Do not read `CHANGELOG.md` or `docs/repo_history/` at startup by default.' not in agents:
        fail('AGENTS.md must keep changelog and repo history out of default startup reads')
    if 'docs/repo_history/' not in agents:
        fail('AGENTS.md must include the archived repository history layer')
    if 'docs/runbooks/memory-review.md' not in agents:
        fail('AGENTS.md must route memory reviews to docs/runbooks/memory-review.md')
    if 'Do not make project-wide or structural recommendations from partial reads' not in compact(agents):
        fail('AGENTS.md must require proportional context before broad advice')
    if 'Treat sources outside the repo-backed hierarchy as leads' not in agents:
        fail('AGENTS.md must keep the repo-backed source authority rule')

    claude = read('CLAUDE.md')
    if claude != agents:
        fail('CLAUDE.md must be an exact byte-for-byte mirror of AGENTS.md')

    require_startup_hook()

    memory_review = read('docs/runbooks/memory-review.md')
    for phrase in REQUIRED_MEMORY_REVIEW_PHRASES:
        if phrase not in memory_review:
            fail(f'memory-review runbook missing anti-churn phrase: {phrase!r}')
    if 'whole relevant memory system' not in memory_review:
        fail('memory-review runbook must require full relevant context for structural advice')
    if 'docs/repo_history/' not in memory_review:
        fail('memory-review runbook must route retired records to docs/repo_history/')

    workflow = read('docs/memory/workflow.md')
    if '## Accepted Baseline / Known Tradeoffs' not in workflow:
        fail('workflow memory must record accepted baseline/tradeoffs')
    if 'docs/plans/' not in workflow:
        fail('workflow memory must include the plans layer')
    if 'docs/repo_history/' not in workflow:
        fail('workflow memory must include the repo-history archive layer')

    local_claude_skill = read('.claude/skills/long-running-project-memory/SKILL.md')
    if 'docs/plans/' not in local_claude_skill:
        fail('Claude long-running memory skill must include docs/plans/')
    if 'docs/repo_history/' not in local_claude_skill:
        fail('Claude long-running memory skill must include docs/repo_history/')

    local_codex_skill = read('.agents/skills/long-running-project-memory/SKILL.md')
    if 'docs/repo_history/' not in local_codex_skill:
        fail('Codex long-running memory skill must include docs/repo_history/')

    if (ROOT / '.codex').exists():
        fail('Codex repo-scoped skills belong under .agents/skills/, not .codex/')

    for plan_path in (ROOT / 'docs/plans').glob('*.md'):
        text = plan_path.read_text(encoding='utf-8')
        if 'historical record only' in text.lower():
            fail(
                f'{plan_path.relative_to(ROOT)} is a historical record; '
                'move it to docs/repo_history/'
            )
        if plan_path.name == 'README.md' and '## Completed Records' in text:
            fail('docs/plans/README.md must not keep a Completed Records section')

    print('memory-system check passed')


if __name__ == '__main__':
    main()
