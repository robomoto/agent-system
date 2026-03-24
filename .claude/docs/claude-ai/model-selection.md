<!-- last_verified: 2026-03-04 -->
# Claude Model Selection Guide

## Current Models (verify pricing before quoting)

| Model | Input/1M | Output/1M | Context | Best For |
|-------|----------|-----------|---------|----------|
| Haiku 4.5 | $0.80 | $4.00 | 200K | Fast read-only tasks, discovery, classification, tracking |
| Sonnet 4.6 | $3.00 | $15.00 | 200K | Balanced work: implementation, review, analysis, code generation |
| Opus 4.6 | $15.00 | $75.00 | 200K | Complex reasoning, orchestration, architecture, novel problem-solving |

## Selection Heuristics

### Use Haiku when:
- Task is read-only (no code generation)
- Output is short and structured (classification, routing, scoring)
- Speed matters more than depth (discovery, initial scanning)
- Task is highly constrained (fill-in-the-blank, template completion)
- Cost sensitivity is high and quality bar is moderate

### Use Sonnet when:
- Task requires code generation or modification
- Task requires multi-step reasoning but with clear structure
- Review work with explicit checklists
- Test authoring
- Moderate complexity analysis with good prompt guidance

### Use Opus when:
- Task requires novel problem-solving without clear templates
- Architectural decisions with ambiguous trade-offs
- Orchestration across multiple agents (understanding delegation)
- Tasks where getting it wrong is expensive (security design, data model)
- Adversarial reasoning without explicit checklists to follow

## Anti-patterns

- **Opus for boilerplate**: Using Opus to generate CRUD endpoints, config files, or test scaffolding. Sonnet handles these fine.
- **Haiku for code review**: Haiku misses subtle bugs. Use Sonnet minimum for security-relevant review.
- **Sonnet for orchestration**: Multi-agent delegation benefits from Opus's ability to reason about task decomposition.
- **Any model without structured output**: Free-text responses waste tokens on formatting variance. Always use schemas.

## Cost Multipliers

Relative to Haiku (1x):
- Sonnet: ~3.75x input, ~3.75x output
- Opus: ~18.75x input, ~18.75x output

A task that costs $0.01 on Haiku costs ~$0.04 on Sonnet and ~$0.19 on Opus.
