# Skill: Create Skill

Create a new reusable skill for the agent system. Use this when a process is performed often enough — by one agent or many — that documenting it once and loading it on demand beats re-deriving it each time.

## Skill vs. Specialist (pick the right tool)

| | Skill | Specialist |
|---|---|---|
| **What it is** | A reusable prompt bundle injected into a calling agent's context | A separate agent with its own context window |
| **Cost** | Tokens added to caller's context when invoked | A full subagent dispatch (its own input/output tokens) |
| **Best for** | Repeatable processes, checklists, formats, protocols | Deep domain knowledge, multi-step work needing isolation |
| **Created via** | This skill | `create-specialist` skill |

Rule of thumb: if the work is "follow these steps in this order" → skill. If the work is "go think about this and come back with a report" → specialist.

## When to Use

- A multi-step process is being performed ad-hoc by multiple agents (e.g., security review, cost estimation, design audit)
- A specific output format / protocol needs to be consistent across invocations
- A recurring user request would benefit from a documented trigger phrase (e.g., `/loop`, `code review`)
- The lead notices that the same instructions are being repeated across task assignments

## Process

### 1. Define the Skill

Determine:
- **Name**: lowercase, hyphenated (e.g., `parse-declarations-page`, `compare-coverage`, `prefill-quote-form`). Match the user's vocabulary if it's user-invocable.
- **Scope**: One specific outcome. Skills that try to "do X or Y or Z" become unfocused — split them.
- **Audience**: Which agents will use this? The lead? A specialist? End-user via slash command?
- **Trigger**: When should it be invoked automatically? When does it require explicit invocation?

### 2. Decide the Structure

**Single-file skill** (`<name>/SKILL.md` only) — use when the full skill fits in <300 lines.

**Multi-file skill** — use progressive disclosure when the skill has heavy reference material:

```
.claude/skills/<name>/
├── SKILL.md              # Trigger description, when-to-use, process outline, links to references
├── reference/
│   ├── checklist.md      # Detailed checklists loaded on demand
│   ├── examples.md       # Worked examples
│   └── templates/        # Output templates
└── scripts/              # Optional: helper scripts the skill invokes
```

The SKILL.md should stay lean — it loads every time the skill is invoked. Heavy content lives in `reference/` and is read only when the relevant step needs it.

### 3. Write the SKILL.md

Required sections (in this order):

```markdown
# Skill: <Title>

<One sentence describing the outcome. This is what shows up in the skill list.>

## When to Use

- <specific trigger condition>
- <specific trigger condition>
- <when NOT to use, if there's an obvious confusion>

## Process

### 1. <First step>
<concrete instructions, not aspirational>

### 2. <Second step>
...

## Checklist

- [ ] <verifiable criterion>
- [ ] <verifiable criterion>
```

Optional sections, in roughly this order: **Inputs** (what the caller provides), **Output Format** (schema or template the skill produces), **Examples** (1-3 concrete cases in `<example>` tags), **Anti-patterns** (common misuses), **References** (links to `reference/` files).

### 4. Frontmatter (only for user-invocable skills)

If the skill is invoked via the Skill tool by the user (slash command), add YAML frontmatter at the top:

```yaml
---
name: <skill-name>
description: <One-line description for the skill picker. Include trigger keywords the user might type.>
---
```

If the skill is only used internally by agents (loaded by reference in agent prompts), no frontmatter is needed — it's just a markdown file.

### 5. Token Efficiency Discipline

Skills get loaded into the caller's context every invocation. Be ruthless:

- **Progressive disclosure**: Move reference material out of SKILL.md into `reference/<topic>.md`. The SKILL.md links to them: "see `reference/owasp-checklist.md` for the full list." The caller only loads them when needed.
- **No redundant examples**: 1-3 examples max in SKILL.md. Diverse, not variations of the same case.
- **No restating what agents already know**: Don't re-explain what Read/Grep/Edit do. Don't re-explain the project structure.
- **No filler**: Drop sentences that don't change behavior. Every line should change what the agent does.
- **Tables over prose**: For comparison data, structured guidance, or enumerations, use tables.
- **Cite, don't quote**: Reference `.claude/docs/<domain>/file.md:section` instead of copying content.

### 6. Register the Skill

For agent-system skills:
1. Add the skill to the **Available Skills** table in `agent-system/CLAUDE.md`
2. If a specific agent should use it, add the skill to that agent's prompt under a "Skills" section

For project-local skills (e.g., `insurance-team/.claude/skills/`):
1. Add to that project's CLAUDE.md skill table (if it has one)
2. If user-invocable, ensure the trigger phrase is documented in the project's CLAUDE.md

For user-global skills (`~/.claude/skills/`):
1. Document the trigger in `~/.claude/CLAUDE.md` if it's a phrase, or rely on slash-command discovery if it has frontmatter

### 7. Test the Skill

Before considering it done:
- Have an agent invoke it cold (no prior context). Does the SKILL.md alone provide enough to act?
- Check token weight: roughly count lines × ~10 tokens. SKILL.md should be <200 lines (≈2K tokens) for typical skills, <400 for heavyweight.
- Confirm reference files are actually read on demand, not loaded preemptively.

## Checklist

- [ ] Skill directory created at the right location (`agent-system/.claude/skills/`, project-local, or user-global)
- [ ] SKILL.md has When-to-Use, Process, Checklist
- [ ] Reference material moved to `reference/` if SKILL.md exceeds ~200 lines
- [ ] Frontmatter added if the skill is user-invocable
- [ ] Skill registered in the appropriate CLAUDE.md
- [ ] Token weight checked — SKILL.md is lean, heavy content deferred
- [ ] At least one concrete example or trigger phrase documented
- [ ] Anti-patterns or "when NOT to use" called out if confusion is likely

## Anti-patterns

- **Skill that should be a specialist**: If the process needs to "go think and report back," it needs a context window of its own — make it an agent, not a skill.
- **Skill that should be a CLAUDE.md rule**: One-line rules ("always use Bun, never npm") belong in project CLAUDE.md, not as a skill.
- **Skill duplicating an existing one**: Check `.claude/skills/` first. Often the right move is to extend an existing skill's reference material.
- **All content in SKILL.md**: If it's >300 lines, you're paying that cost on every invocation. Split.
- **Vague triggers**: "Use this for code stuff" doesn't help routing. Be specific about the outcome.

## Examples

<example>
Good: `parse-declarations-page` skill (lean SKILL.md)

```
.claude/skills/parse-declarations-page/
├── SKILL.md                      # 80 lines: when-to-use, process outline, output schema
└── reference/
    ├── carrier-formats/          # Loaded only when matching that carrier
    │   ├── geico.md
    │   ├── state-farm.md
    │   └── progressive.md
    └── coverage-glossary.md      # Loaded once if terms need lookup
```

Why this works: SKILL.md stays small. Carrier-specific quirks load only when needed.
</example>

<example>
Bad: `do-insurance-stuff` skill

A 600-line SKILL.md that covers parsing, comparing, quoting, and reviewing all in one. Loaded into context every time any of those four tasks runs. Should be four skills (or three skills + one specialist for the comparison reasoning).
</example>
