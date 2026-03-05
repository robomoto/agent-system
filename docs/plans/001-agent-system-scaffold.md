# Plan 001: Agent System Scaffold

## Goal

Build a framework of specialist Claude agents that delegate work through a team lead, optimized for context/token efficiency and deterministic outputs.

## Context

This system models a software team:
- A **lead** decomposes tasks and delegates to specialists
- Specialists have scoped tools, models, and system prompts
- All agents return structured handoff reports (not raw output)
- A **validator** independently confirms assertions

## Phase 1: Agent Definitions (this plan)

Create `.claude/agents/*.md` for each specialist. Each agent definition includes:
- YAML frontmatter: name, description, tools, model, memory, permissions
- Markdown body: system prompt with role, constraints, output format, few-shot examples

### Agents to define

1. **lead** — Opus orchestrator. Decomposes tasks, delegates, synthesizes.
2. **researcher** — Haiku explorer. Fast discovery, returns distilled findings.
3. **architect** — Opus designer. System design, API contracts, trade-off analysis.
4. **implementer** — Sonnet builder. Writes code and tests per spec.
5. **reviewer** — Sonnet critic. Code review + adversarial reasoning (challenges assumptions, flags risks).
6. **validator** — Sonnet verifier. Runs tests, checks assertions, confirms conformance.
7. **ui-designer** — Sonnet visual designer. Component design, design systems.
8. **ux-designer** — Sonnet UX researcher. User flows, usability, information architecture.
9. **cost-accountant** — Haiku tracker. Monitors token budgets, recommends model routing.
10. **sre** — Sonnet reliability engineer. Monitoring, alerting, incident response.
11. **sysadmin** — Sonnet infra manager. Deployment, configuration, networking.
12. **create-specialist skill** — Meta-skill for creating new language/domain specialists on demand with local doc bundles.

## Phase 2: Skills (complete)

Reusable skill bundles in `.claude/skills/`:
- [x] code-review — multi-pass review protocol, severity definitions, finding format
- [x] testing-strategy — test pyramid, coverage targets, edge case checklist
- [x] security-audit — OWASP top 10, STRIDE threat modeling, severity framework
- [x] cost-analysis — token estimation templates, cloud service projection, budget format
- [x] design-system — design tokens, component spec format, accessibility (WCAG 2.1 AA), layout patterns

## Phase 3: Schemas & Hooks (complete)

- [x] Pydantic v2 models for all 12 agent handoff reports (`src/schemas/`)
- [x] JSON Schema export script (`scripts/export-schemas.sh`) — 12 schemas exported
- [x] Handoff validation script (`scripts/validate-handoff.sh`) — validates any agent output
- [x] 19 tests covering valid/invalid handoffs, schema export, dynamic specialists
- [x] Claude Code hooks (`.claude/settings.json`) — ruff lint on Python file edit/write
- [x] Python specialist agent + doc bundle (idioms, footguns, reference)
- [x] pyproject.toml with pydantic, pytest, pyright, ruff
- [ ] Agent SDK integration for programmatic orchestration (deferred — test-drive first)

## Success Criteria

- [x] All 12 core agents defined in `.claude/agents/` (11 original + claude-ai-specialist)
- [x] `create-specialist` skill for on-demand language/domain agents
- [x] Each agent has scoped tools, appropriate model, and structured output format
- [x] Reviewer includes adversarial reasoning (replaces standalone devil's advocate)
- [x] Reviewer loads language-specific footgun docs on demand
- [x] Handoff format is consistent across all agents
- [x] Plan is self-contained (another agent can execute without additional context)
- [x] 5 reusable skills defined (code-review, testing-strategy, security-audit, cost-analysis, design-system)
- [x] Claude AI specialist with doc bundle for self-optimization
- [x] Phase 3: Structured output schemas and validation hooks
- [x] Python specialist agent created (first use of create-specialist pattern)
- [x] 19 schema tests passing
- [ ] Agent SDK integration (deferred until after test-drive)

## Decision Log

- **Devil's advocate → folded into reviewer**: Research shows adversarial patterns help for complex decisions but a standalone agent burns tokens disproportionately. Better to embed challenge-reasoning behavior in the reviewer and architect prompts.
- **Hub-and-spoke over peer-to-peer**: Simpler coordination, predictable flow, lower token cost. Upgrade to agent teams only when sustained parallel reasoning is needed.
- **Model routing**: Haiku for discovery/tracking (cheap, fast), Sonnet for implementation/review (balanced), Opus for orchestration/architecture (complex reasoning only).
- **Dedicated specialists over generic parameterized agent**: A `python-specialist` with baked-in idioms and local docs gives higher-signal tokens than a generic agent figuring out "what language am I?" at runtime. The `create-specialist` skill makes new specialists cheap to spin up.
- **Local doc bundles over WebSearch**: Curated docs in `.claude/docs/<domain>/` are faster, cheaper, more deterministic, and offline-capable vs. web searching every time.
- **One reviewer + language doc bundles over per-language reviewers**: 90% of review concerns are universal. Language-specific footguns loaded on demand from doc bundles. Saves maintaining N duplicate reviewer agents.
- **Pydantic v2 for schemas**: Runtime validation + JSON Schema export for Claude structured outputs. Literal types constrain at both Python and generation levels. StrEnum for status fields.
- **SDK integration deferred**: Build and test-drive the system manually first, then add programmatic orchestration once patterns are proven.
