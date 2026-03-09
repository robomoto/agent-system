# Agent System

A team of specialist AI agents that work together on your software projects, orchestrated through [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

Instead of one AI doing everything, this system gives you a **team lead** that breaks down tasks and delegates to specialists — a researcher, architect, implementer, code reviewer, QA analyst, and more. Each specialist has focused expertise and curated reference docs, so you get better results with less wasted effort.

## What You Need

1. **Claude Code** — Anthropic's CLI tool for working with Claude. Install it:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
   You'll need an Anthropic API key or a Claude Pro/Max subscription. See the [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for setup.

2. **This repo** — Clone it somewhere convenient:
   ```bash
   git clone https://github.com/yourusername/agent-system.git ~/claude_projects/agent-system
   ```

3. **Global instructions** — Tell Claude Code where to find the agent system by adding this to your `~/.claude/CLAUDE.md` file (create it if it doesn't exist):

   ```markdown
   ## Agent System

   The agent framework lives at `~/claude_projects/agent-system/`. It provides a hub-and-spoke team of specialist agents orchestrated by a lead.

   ### Trigger Phrases

   When the user invokes any of these, read the corresponding files from the agent-system repo and follow their instructions:

   | Phrase | Read | Purpose |
   |--------|------|---------|
   | "team lead" / "use lead" | `.claude/agents/lead.md` + `CLAUDE.md` | Orchestrate work through specialist delegation |
   | "tracked run" / "track this" | `.claude/skills/tracked-run/SKILL.md` | Instrument run with metrics |
   | "create specialist" | `.claude/skills/create-specialist/SKILL.md` | Create a new specialist agent on demand |
   | "code review" | `.claude/skills/code-review/SKILL.md` | Structured multi-pass review |
   | "security audit" | `.claude/skills/security-audit/SKILL.md` | OWASP/STRIDE security review |
   | "cost analysis" | `.claude/skills/cost-analysis/SKILL.md` | Token/cloud cost estimation |
   | "design system" | `.claude/skills/design-system/SKILL.md` | Design tokens, components, accessibility |
   | "testing strategy" | `.claude/skills/testing-strategy/SKILL.md` | Test pyramid, coverage, edge cases |
   ```

   The full global instructions block is in this repo's `CLAUDE.md` under "How It Works" — copy the whole section if you want all the details.

## Quick Start

Once installed, open any project with Claude Code and use the trigger phrases:

### Use the team lead

```
you: team lead — add authentication to this API
```

The lead will:
1. **Check the roster** — ensure the right specialists exist for your project's tech stack
2. **Research** — discover your codebase structure and patterns
3. **Design** — have the architect plan the approach
4. **Implement** — delegate code writing to the implementer
5. **Review** — run code review and QA checks
6. **Validate** — independently verify everything works

You'll see agents being spawned in real time. The lead coordinates everything and reports back with a structured summary.

### Run a code review

```
you: code review
```

Gets you a structured multi-pass review of your recent changes, covering correctness, security, performance, and maintainability.

### Run a security audit

```
you: security audit
```

OWASP Top 10 checklist and STRIDE threat modeling against your codebase.

### Get a cost estimate

```
you: cost analysis
```

Estimates token costs for your agent usage and projects cloud service costs.

## How It Works

### The Hub-and-Spoke Model

```
                    ┌──────────┐
                    │   Lead   │  (Opus — orchestrates everything)
                    └────┬─────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────┴─────┐  ┌────┴────┐  ┌─────┴─────┐
    │ Researcher │  │Architect│  │Implementer│
    │  (Haiku)   │  │ (Opus)  │  │ (Sonnet)  │
    └───────────┘  └─────────┘  └───────────┘
          │              │              │
    ┌─────┴─────┐  ┌────┴────┐  ┌─────┴─────┐
    │ Reviewer   │  │   QA    │  │ Validator  │
    │ (Sonnet)   │  │(Sonnet) │  │ (Sonnet)   │
    └───────────┘  └─────────┘  └───────────┘
```

- **Lead** (Opus) — Decomposes tasks, delegates, synthesizes results. Never does specialist work itself.
- **Researcher** (Haiku) — Fast codebase and web discovery. Finds files, patterns, dependencies.
- **Architect** (Opus) — System design, API contracts, trade-off analysis.
- **Implementer** (Sonnet) — Writes code and tests.
- **Reviewer** (Sonnet) — Code review, security audit, adversarial challenge.
- **QA** (Sonnet) — Test strategy, coverage gaps, edge cases, acceptance criteria.
- **Validator** (Sonnet) — Independently runs tests and verifies assertions.

Plus domain specialists: Python, JavaScript, Kotlin, Android, CSS, Cloudflare Workers, and more. New specialists are created on demand when needed.

### Specialist Doc Bundles

Each specialist reads from curated reference docs in `.claude/docs/<domain>/` instead of searching the web every time. This makes answers faster, cheaper, and more consistent. Docs include:

- **idioms.md** — Idiomatic patterns and conventions
- **footguns.md** — Common mistakes and gotchas
- **reference.md** — Key APIs and features

### Creating New Specialists

If the team encounters a language or framework it doesn't have a specialist for, it creates one automatically. You can also trigger this manually:

```
you: create specialist for Ruby
```

This creates an agent definition, seeds reference docs, and registers the specialist with the team.

## Project Structure

```
agent-system/
├── CLAUDE.md                  # System configuration and agent roster
├── README.md                  # This file
├── .claude/
│   ├── agents/                # Agent definitions (one per specialist)
│   │   ├── lead.md
│   │   ├── researcher.md
│   │   ├── architect.md
│   │   ├── implementer.md
│   │   ├── reviewer.md
│   │   ├── python-specialist.md
│   │   └── ...
│   ├── docs/                  # Curated reference docs for specialists
│   │   ├── python/
│   │   ├── javascript/
│   │   ├── kotlin/
│   │   └── ...
│   └── skills/                # Reusable skill bundles
│       ├── code-review/
│       ├── security-audit/
│       ├── create-specialist/
│       └── ...
├── docs/                      # Plans, team logs, metrics
├── scripts/                   # Validation and utility scripts
└── src/                       # Schemas and supporting code
```

## Available Skills

| Trigger Phrase | What It Does |
|----------------|-------------|
| `team lead` | Full team orchestration for complex tasks |
| `code review` | Structured multi-pass code review |
| `security audit` | OWASP/STRIDE security analysis |
| `testing strategy` | Test pyramid and coverage analysis |
| `design system` | Design tokens, components, accessibility |
| `cost analysis` | Token and cloud cost estimation |
| `tracked run` | Instruments a run with performance metrics |
| `create specialist` | Creates a new domain specialist on demand |

## Current Specialist Roster

| Specialist | Domain |
|-----------|--------|
| python-specialist | Python idioms, Pydantic, typing, Django |
| javascript-specialist | JS idioms, async, modules, error handling |
| kotlin-specialist | Coroutines, Flow, sealed classes, serialization |
| android-specialist | Jetpack Compose, ViewModel, Room, Gradle |
| css-specialist | Custom properties, responsive layout, animations |
| cloudflare-workers-specialist | Workers, Durable Objects, wrangler, storage APIs |
| claude-ai-specialist | Agent prompts, token optimization, model routing |
| social-psychologist | Group dynamics, moderation, onboarding |
| experimental-psychologist | Measurement design, metrics, surveys |
| technical-writer | READMEs, API docs, guides, changelogs |
| accessibility | WCAG compliance, ARIA, keyboard nav |
| ui-designer | Component design, layouts, design systems |
| ux-designer | User flows, information architecture |
| sre | Monitoring, alerting, reliability |
| sysadmin | Infrastructure, deployment, networking |

## Tips

- **Start with "team lead"** for any non-trivial task. It handles decomposition and delegation for you.
- **The system works across projects.** Navigate to any project directory and invoke the team lead — it reads both the agent system framework and your project's own CLAUDE.md.
- **Specialists are created on demand.** If your project uses Go, Rust, or anything else not listed above, the roster-checker will create a specialist automatically.
- **Track your runs** with `tracked run` to compare agent performance across sessions.
- **Each skill works standalone.** You don't have to use the full team — `code review` or `security audit` work great on their own for focused tasks.
