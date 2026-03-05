# Skill: Create Specialist Agent

Create a new specialist agent and its supporting doc bundle. Use this when the team encounters work requiring expertise not covered by the existing agent roster.

## When to Use

- A task requires deep knowledge of a language, framework, domain, or toolchain not covered by an existing agent
- The lead identifies a recurring need that would benefit from a dedicated specialist
- An existing generic approach is burning tokens on discovery that could be baked into a specialist

## Process

### 1. Define the Specialist

Determine:
- **Name**: lowercase, hyphenated (e.g., `python-specialist`, `kubernetes-specialist`, `oauth-specialist`)
- **Scope**: What specific knowledge domain does this agent cover? Be precise — `django-specialist` is better than `web-framework-specialist`
- **Model**: Haiku if read-only/advisory, Sonnet if it writes code or does deep analysis, Opus only if it makes architectural decisions
- **Tools**: Minimum viable set. Read-only agents don't get Write/Edit. Always include Read, Glob, Grep for doc access
- **Memory**: `user` if knowledge transfers across projects, `project` if project-specific

### 2. Create the Agent Definition

Write `.claude/agents/<name>.md` following this template:

```markdown
---
name: <name>
description: <When the lead should delegate to this agent. Be specific — this controls automatic routing.>
tools: <comma-separated tool list>
model: <haiku|sonnet|opus>
memory: <user|project>
---

You are a <role> specialist. Your job is to provide deep, authoritative knowledge about <domain>.

## Expertise

<3-5 bullet points defining what this agent knows deeply>

## Operating Constraints

- Read from `.claude/docs/<domain>/` for reference material before answering.
- Cite specific doc sections or file references, not vague generalizations.
- Distinguish between "language/framework guarantees" and "community conventions".
- Flag version-specific behavior — always specify which version you're referencing.
- If unsure, say so. Never guess at semantics.
- <2-3 domain-specific constraints>

## Output Format

Always return a structured handoff report:

\```json
{
  "agent": "<name>",
  "task_id": "<assigned task id>",
  "domain": "<language|framework|platform>",
  "status": "completed|blocked|needs-input",
  "summary": "Key guidance provided",
  "recommendations": [
    {
      "topic": "Specific topic",
      "guidance": "What to do",
      "rationale": "Why",
      "version": "Version this applies to",
      "doc_ref": ".claude/docs/<domain>/file.md or external URL"
    }
  ],
  "footguns": ["Common mistake and how to avoid it"],
  "artifact_refs": [],
  "decisions": [],
  "next_steps": [],
  "token_usage": 0
}
\```

## Examples

<example>
Task: "<realistic task for this specialist>"

Good output:
- <specific, referenced, version-aware guidance>

Bad output:
- <vague, unverified, or generic advice>
</example>
```

### 3. Create the Doc Bundle

Create `.claude/docs/<domain>/` with curated reference material:

```
.claude/docs/<domain>/
├── idioms.md          # Idiomatic patterns and conventions
├── footguns.md        # Common mistakes, gotchas, surprising behavior
├── reference.md       # Key APIs, stdlib, or platform features we use
└── <framework>.md     # Framework-specific notes (if applicable)
```

**Doc curation rules:**
- Keep each file under 300 lines — these get loaded into context
- Focus on what we actually use, not exhaustive coverage
- Include version numbers for all referenced behavior
- Add entries when agents encounter new footguns or patterns (system evolution)
- Prefer concrete examples over abstract descriptions

### 4. Register the Agent

Add the new agent to the roster table in the project's `CLAUDE.md` and to the lead agent's roster table in `.claude/agents/lead.md`.

### 5. Seed Initial Docs

For language specialists, start with:

**idioms.md** — 10-15 most important idiomatic patterns:
- How to handle errors
- Iteration patterns
- String handling
- Concurrency primitives
- Testing conventions

**footguns.md** — 5-10 most common mistakes:
- Things that silently do the wrong thing
- Performance traps
- Security-relevant gotchas
- Version-migration pitfalls

**reference.md** — Key APIs and features:
- Standard library modules we use
- Built-in types and their behavior
- Package management conventions

For domain specialists (e.g., `oauth-specialist`, `kubernetes-specialist`), adapt the doc structure to the domain — replace "idioms" with "patterns", "footguns" with "pitfalls", etc.

## Checklist

- [ ] Agent definition created in `.claude/agents/<name>.md`
- [ ] Doc bundle created in `.claude/docs/<domain>/` with at least idioms + footguns
- [ ] Agent added to lead's roster table
- [ ] Agent added to project CLAUDE.md roster table
- [ ] Agent description is specific enough for automatic routing
- [ ] Tools are scoped to minimum viable set
- [ ] Output format matches the standard handoff schema
- [ ] At least one concrete example in the agent prompt
