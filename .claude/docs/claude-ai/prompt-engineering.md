<!-- last_verified: 2026-03-04 -->
# Claude Prompt Engineering Reference

## Core Principles

### Signal-to-Token Ratio
Every token in a prompt should increase the probability of the desired output. Remove tokens that don't change behavior.

Test: Delete a sentence from the prompt. If output quality doesn't change, the sentence was noise.

### Prompt Structure (order matters)

1. **Role** — Who the agent is (1-2 sentences)
2. **Responsibilities** — What it does (bulleted list)
3. **Constraints** — What it must/must not do (bulleted list)
4. **Output format** — Exact schema with field definitions
5. **Examples** — 3-5 canonical cases in `<example>` tags

Claude weighs the beginning and end of system prompts most heavily. Put critical constraints early.

### Few-Shot Examples

- Use 3-5 examples, not more (diminishing returns after 5)
- Examples should be diverse — cover different scenarios, not variations of the same one
- Include one "bad" example showing what NOT to do (Claude learns from contrast)
- Wrap in `<example>` tags so Claude distinguishes from instructions
- Examples should demonstrate the principle, not enumerate every case

### Temperature

| Setting | Use Case |
|---------|----------|
| 0.0 | Classification, structured extraction, yes/no decisions |
| 0.1-0.2 | Code review, technical analysis, factual responses |
| 0.3-0.5 | Code generation, balanced creative+analytical |
| 0.7-1.0 | Creative writing, brainstorming, diverse suggestions |

Note: Temperature 0.0 is not fully deterministic due to sampling implementation, but combined with structured outputs it gets close.

## Structured Outputs

### JSON Schema Constraints
- Use `enum` for fields with known values (not `string`)
- Use `required` for all fields that must appear
- Use `minimum`/`maximum` for numeric bounds
- Use `strict: true` on tool definitions for guaranteed conformance

### Schema constrains at generation time
Claude's structured outputs compile schemas to grammars that constrain token generation. This is not post-hoc validation — invalid tokens are blocked during inference. This is the strongest determinism mechanism available.

## Context Efficiency Patterns

### Just-in-Time vs. Always-Loaded
- **Always-loaded** (system prompt): Role, constraints, output format — things needed every invocation
- **Just-in-time** (tool reads): Reference docs, examples, large context — loaded only when relevant

Rule of thumb: If it's used <50% of invocations, load it on demand.

### Reference Passing
Pass `src/auth/handler.ts:45-80` instead of the code itself. The receiving agent can Read the file if needed. This saves tokens when the reference isn't needed (agent already knows the pattern) and costs one tool call when it is.

### Handoff Compression
Agent output should be summaries with references, not raw dumps. A 50K token exploration should compress to a 500 token handoff report with artifact_refs pointing to files.

## Claude-Specific Behaviors

### Strengths
- Excellent at following structured output schemas
- Strong at multi-step reasoning when steps are explicit
- Good at adversarial thinking when explicitly prompted
- Reliable tool use with well-defined schemas
- Strong code generation across languages

### Known Tendencies
- Will over-help if not constrained (adds features, refactors adjacent code)
- Tends toward verbosity in explanations — constrain with "be concise" or output schemas
- May hedge with "it depends" — counter with "make a recommendation and state your confidence"
- Can be sycophantic — counter with explicit permission to disagree/challenge
- Will sometimes repeat instructions back — counter with "skip preamble, go straight to output"

### Working With (not against) Claude
- Give explicit permission to say "I don't know" or "I'm not sure"
- Use checklists for adversarial review (Claude follows checklists reliably)
- Constrain output format when you need consistency, leave free when you need creativity
- Break complex reasoning into explicit steps rather than hoping for implicit chain-of-thought
