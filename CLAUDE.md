# Agent System

A framework for building specialist Claude agents that delegate work through a team lead, optimized for context efficiency and deterministic results.

## Architecture

**Hub-and-spoke** — a lead agent (Opus) decomposes tasks and delegates to specialist subagents. All communication flows through the lead. Subagents return lightweight structured handoffs, not raw context dumps.

### Agent Roster

| Agent | Model | Role | Tools |
|-------|-------|------|-------|
| **lead** | opus | Task decomposition, synthesis, final decisions | All (including Agent) |
| **researcher** | haiku | Fast codebase/web discovery | Read, Glob, Grep, Bash (read-only), WebFetch, WebSearch |
| **architect** | opus | System design, API contracts, technical decisions | Read, Glob, Grep, Bash (read-only), WebFetch |
| **implementer** | sonnet | Code writing and test authoring | Read, Write, Edit, Bash, Glob, Grep |
| **reviewer** | sonnet | Code review, security audit, quality checks, adversarial challenge | Read, Glob, Grep, Bash (read-only) |
| **validator** | sonnet | Assertion verification, test execution, output conformance | Read, Bash, Glob, Grep |
| **ui-designer** | sonnet | Visual design, component architecture, design systems | Read, Write, Edit, Glob, Grep |
| **ux-designer** | sonnet | User flows, information architecture, usability heuristics | Read, Glob, Grep, WebFetch |
| **cost-accountant** | haiku | Token budget tracking, model routing optimization | Read, Glob, Grep, Bash (read-only) |
| **sre** | sonnet | Reliability, monitoring, incident response, observability | Read, Write, Edit, Bash, Glob, Grep |
| **sysadmin** | sonnet | Infrastructure, deployment, configuration, networking | Read, Write, Edit, Bash, Glob, Grep |
| **claude-ai-specialist** | sonnet | Agent system optimization: prompts, tokens, model routing, determinism | Read, Glob, Grep, WebFetch, WebSearch |
| **python-specialist** | sonnet | Python idioms, Pydantic, typing, Django, performance | Read, Glob, Grep, WebFetch, WebSearch |
| ***-specialist** | varies | Created on demand per language/domain (see `create-specialist` skill) | Read, Glob, Grep + domain-appropriate |

### Delegation Protocol

1. Lead receives task and enters plan mode
2. Lead decomposes into subtasks with dependency graph
3. Lead delegates to specialists via structured task assignments
4. Specialists work independently, return structured handoff reports
5. Lead synthesizes results and routes follow-up work
6. Validator confirms assertions before lead marks complete

### Handoff Format

Agents return structured reports, not raw output:

```json
{
  "agent": "researcher",
  "task_id": "task-001",
  "status": "completed|blocked|needs-input",
  "summary": "One-paragraph finding",
  "artifact_refs": ["path/to/file-or-section"],
  "decisions": ["Key decision made and why"],
  "next_steps": ["What should happen next"],
  "token_usage": 12400
}
```

### Context Efficiency Rules

- Pass references, not content. Say `see src/auth/handler.ts:45-80`, not the code itself.
- Scope agent prompts tightly — each agent gets only what it needs for its task.
- Route discovery to Haiku, implementation to Sonnet, orchestration to Opus.
- Use agent memory (`.claude/agent-memory/`) for cross-session learning.
- Parallel execution for independent subtasks (up to 7 concurrent).

### Determinism Rules

- Structured output schemas for all agent responses (see `src/schemas/`).
- Temperature 0.0-0.2 for decision-critical agents (architect, reviewer, validator).
- Validator agent runs independently — never trust self-reported success.
- Few-shot examples in every agent prompt (3-5 canonical cases).
- Pre-tool-use hooks for linting/type-checking before edits land.

## Skills

Skills are reusable prompt bundles in `.claude/skills/`. Agents declare which skills they need; skill content is injected into their context at spawn time.

### Available Skills

| Skill | Used By | Purpose |
|-------|---------|---------|
| `create-specialist` | lead | Create new language/domain specialist agents with local doc bundles on demand |
| `code-review` | reviewer | Structured review protocol: severity checklist, finding format, multi-pass review |
| `testing-strategy` | implementer, reviewer | Test pyramid, coverage targets, edge case checklist, anti-patterns |
| `security-audit` | reviewer, architect | OWASP top 10 checklist, STRIDE threat modeling, severity framework |
| `cost-analysis` | cost-accountant, lead | Token cost estimation, cloud service projection, budget templates |
| `design-system` | ui-designer, reviewer | Design tokens, component spec format, accessibility checklist, layout patterns |

### Specialist Doc Bundles

Language and domain specialists read curated reference docs from `.claude/docs/<domain>/` instead of searching the web. This is faster, cheaper, and more deterministic. Docs are kept concise (<300 lines per file) and updated as agents encounter new patterns or footguns.

## Project Structure

```
agent-system/
├── CLAUDE.md                  # This file
├── .claude/
│   ├── agents/                # Agent definitions (YAML frontmatter + markdown)
│   ├── docs/                  # Curated reference docs for specialists
│   │   └── <domain>/          # e.g., python/, go/, kubernetes/
│   │       ├── idioms.md      # Idiomatic patterns
│   │       ├── footguns.md    # Common mistakes and gotchas
│   │       └── reference.md   # Key APIs and features
│   └── skills/                # Reusable skill bundles
│       └── create-specialist/ # Skill for creating new specialist agents
├── docs/
│   └── plans/                 # PRDs and execution plans
├── src/
│   └── schemas/               # Structured output schemas
├── tests/                     # Agent consistency and flow tests
└── scripts/                   # Orchestration and validation scripts
```
