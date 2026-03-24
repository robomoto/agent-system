# Skill: Project Review

Structured review framework for AI agent systems, prompt frameworks, and config-driven projects where the deliverables are markdown/YAML/JSON orchestration rather than executable code. The counterpart to `code-review` for non-code projects.

## When to Use

- After building or expanding an agent system (new agents, doc bundles, workflows)
- As a quality gate before committing a new configuration-driven feature
- When auditing an existing agent system for drift or decay
- After a significant refactor of agent definitions, doc bundles, or workflow phases
- Lead wants confidence that the system is internally consistent before use

## What This Covers

Agent definitions, doc bundles, prompt templates, workflow orchestration, cache schemas, handoff formats, roster tables, cross-file references — anything that forms the "source code" of an AI agent system.

## Review Protocol

### 1. Preparation

- Identify the project scope: which directories contain agent definitions, doc bundles, workflows, and templates
- Read the project's `CLAUDE.md` (or equivalent) to understand the architecture, roster, and workflow
- If reviewing a change (not a full audit), identify what was added/modified to scope the review
- Note the project's conventions: naming patterns, frontmatter schema, handoff format, doc bundle structure

### 2. First Pass: Consistency

Do the moving parts agree with each other?

- [ ] **Roster alignment**: Agent roster tables match across all files that list them (e.g., CLAUDE.md ↔ lead agent ↔ actual agent files)
- [ ] **Frontmatter accuracy**: Each agent's frontmatter (name, tools, model, description) matches what roster tables claim
- [ ] **Enum completeness**: Enumerated values (document types, status codes, output formats) are complete across all files that reference them
- [ ] **Phase numbering**: Workflow phases are numbered consistently and referenced correctly by agents
- [ ] **Naming conventions**: File names, directory names, and keys follow the project's stated conventions
- [ ] **Count accuracy**: Any stated counts ("6 specialist agents", "4 verification dimensions") match reality

### 3. Second Pass: Completeness

Does every component have all required parts?

- [ ] **Agent definitions**: Every agent has frontmatter, responsibilities, operating constraints, output format
- [ ] **Examples**: Agents with complex output or judgment calls have good/bad examples
- [ ] **Doc bundles**: Every doc bundle covers its domain without gaps
- [ ] **Templates/schemas**: Template files match their schema definitions
- [ ] **Edge cases**: Workflows address what happens when things go wrong (blocked agents, unexpected input, escalation paths)
- [ ] **Disclaimers/guards**: Safety-critical outputs have appropriate disclaimers, escape hatches, and boundary conditions

### 4. Third Pass: Cross-Reference Integrity

Do references between files resolve correctly?

- [ ] **Doc bundle references**: Every `.claude/docs/` path referenced in an agent definition → file exists
- [ ] **Agent references**: Every agent name referenced in a workflow or orchestrator → agent file exists
- [ ] **Schema ↔ template alignment**: Schema definitions match template file structures
- [ ] **Cache/data references**: Any paths to data directories, caches, or templates → directories exist with expected structure
- [ ] **Handoff field coverage**: Handoff format fields cover all the data that agents actually produce

### 5. Fourth Pass: Architecture Quality

Is the system well-designed?

- [ ] **Role clarity**: Each agent has a distinct, non-overlapping responsibility. No agent is doing another's job.
- [ ] **Delegation boundaries**: Orchestrator orchestrates, specialists specialize. No role confusion.
- [ ] **Context efficiency**: Agents receive only what they need. No full-content passing where references suffice.
- [ ] **Parallel opportunities**: Independent tasks are marked as parallelizable. Dependencies are explicit.
- [ ] **Workflow completeness**: Every workflow phase specifies which agent, what input, what output
- [ ] **Escalation paths**: Clear behavior when an agent is blocked, returns unexpected results, or assesses a task as beyond scope
- [ ] **Doc bundle sizing**: Reference files are concise enough to load into context (<300 lines each)

### 6. Fifth Pass: Adversarial

What breaks?

- [ ] **Stale data**: What happens if cached data is outdated? Is there a freshness mechanism?
- [ ] **Phase skip**: What happens if a phase is skipped or an agent returns `blocked`?
- [ ] **Conflicting handoffs**: What happens if two agents return contradictory findings?
- [ ] **Missing input**: What happens if required intake fields are missing or vague?
- [ ] **Scope creep**: Could an agent interpret its role broadly enough to duplicate another agent's work?
- [ ] **Circular dispatch**: Could the orchestrator enter a remediation loop that never terminates?
- [ ] **Output misuse**: Could a user misinterpret or over-rely on the output? Are guards adequate?

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| **critical** | Broken reference (agent/doc doesn't exist), missing safety guard, workflow gap that causes silent failure | Blocks use. Must fix before the system is invoked. |
| **warning** | Inconsistent roster, missing examples, incomplete template, undefined escalation behavior | Fix before next use. System works but has gaps. |
| **suggestion** | Additional examples, doc bundle improvements, naming refinement, architecture optimization | Nice to have. Improves quality incrementally. |

## Finding Format

Each finding must include all fields:

```json
{
  "severity": "critical|warning|suggestion",
  "category": "consistency|completeness|cross-reference|architecture|adversarial",
  "location": "path/to/file:section-or-line",
  "description": "What's wrong or could be better — be specific",
  "suggested_fix": "How to fix it — be actionable",
  "impact": "What breaks or degrades if unfixed — be concrete"
}
```

## Output Structure

The review should produce:

### 1. Executive Summary
- Project name and scope reviewed
- Number of agents, doc bundles, workflows, and templates audited
- Finding counts by severity
- Top 3-5 priority recommendations

### 2. Findings by Category
Group findings under the 5 review passes. Within each category, order by severity (critical → warning → suggestion).

### 3. Positive Findings
Explicitly note what's well-done. This prevents manufacturing findings and calibrates the review. Examples:
- "All cross-references resolve correctly — no broken links"
- "Agent descriptions are specific enough for automatic routing"
- "Handoff format covers all required fields"

### 4. Summary Scorecard

```
| Dimension        | Critical | Warning | Suggestion | Clean |
|------------------|----------|---------|------------|-------|
| Consistency      |          |         |            |       |
| Completeness     |          |         |            |       |
| Cross-reference  |          |         |            |       |
| Architecture     |          |         |            |       |
| Adversarial      |          |         |            |       |
| **Total**        |          |         |            |       |
```

### 5. Priority Recommendations
Ordered list of the most impactful fixes, with brief rationale for ordering.

## Rules

- No finding without a location. "The project has issues" is not a finding.
- No severity without justification. Why is this critical vs. warning?
- No suggested_fix that is just "fix this". Provide the specific fix or a clear approach.
- Read ALL agent files, ALL doc bundles, and ALL templates before writing findings. Spot checks miss systemic issues.
- If no issues found in a category, say so explicitly. Don't manufacture findings to look thorough.
- Positive findings are required. A review with only negatives is incomplete — it doesn't tell the reader what they can trust.
- Scope the review to the project's own conventions. Don't enforce external standards the project hasn't adopted.
- For large projects (>15 agents or >10 doc bundles), the reviewer may split into parallel sub-reviews by subsystem, then merge findings.

## Adaptation Notes

This skill is designed for AI agent system projects but applies to any config-driven system where:
- Behavior is defined by structured documents (markdown, YAML, JSON) rather than executable code
- Multiple files reference each other and must stay in sync
- The system has an orchestrator that dispatches to specialists
- Output quality depends on prompt design, not just logic

For projects that mix code and configuration (e.g., MCP servers with agent definitions), use both `code-review` and `project-review` — they cover different dimensions.
