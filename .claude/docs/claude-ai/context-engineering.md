# Context Engineering for Claude Agents

## Core Principle

Find the smallest set of high-signal tokens that maximize the probability of the desired output.

## Context Budget Framework

### Per-Agent Budget Guidelines

| Agent Type | Target Context | Rationale |
|------------|---------------|-----------|
| Discovery (Haiku) | <40K tokens | Fast, cheap, scoped reads |
| Implementation (Sonnet) | <150K tokens | Needs full file context for edits |
| Review (Sonnet) | <80K tokens | Reads code + checklist, reports findings |
| Orchestration (Opus) | <50K tokens per synthesis | Handoff reports, not raw data |
| Validation (Sonnet) | <60K tokens | Runs tests, checks outputs |

### Where Tokens Go (typical breakdown)

- System prompt: 200-500 tokens (keep tight)
- Task assignment from lead: 100-300 tokens
- Tool calls (reads, searches): 5K-50K tokens (biggest variable)
- Agent reasoning: 2K-10K tokens
- Output/handoff: 200-800 tokens

Optimization leverage is highest on tool call results — scope reads to specific line ranges, use Grep before Read.

## Techniques

### 1. Scope Tool Calls
Bad: `Read entire 2000-line file`
Good: `Read src/auth/handler.ts lines 40-85` (researcher already identified the range)

### 2. Grep Before Read
Bad: Read 5 files looking for the auth logic
Good: `Grep "authenticate" src/` → find exact files/lines → Read only those ranges

### 3. Structured Handoffs
Bad: Pass 50K of raw exploration output to next agent
Good: Pass 500-token structured report with `artifact_refs` pointing to files

### 4. Parallel Independent Work
Run independent subagents concurrently (up to 7). Total wall-clock time ≈ slowest agent, not sum of all agents.

### 5. Local Docs Over Web Search
Web search: query tokens + fetch tokens + HTML parsing noise + result variance
Local docs: single Read call, curated content, deterministic

### 6. Prompt Caching (API-level)
When multiple agents share the same large context prefix (e.g., architecture docs), prompt caching reduces input token costs by up to 90% on cache hits. Cache key is the prompt prefix — keep shared context at the start.

### 7. Memory for Cross-Session Learning
Agents with `memory: user` or `memory: project` persist knowledge across sessions. This avoids re-discovering patterns that were learned before. Check memory before searching.

### 8. Auto-Compaction
Long conversations auto-compact at ~95% context capacity. This preserves decisions but discards verbose exploration. For long research tasks, save key findings to files before compaction erases them.

## Anti-Patterns

- **Context stuffing**: Loading every potentially-relevant file "just in case"
- **Echo context**: Repeating the task description in the output
- **Redundant reads**: Multiple agents reading the same files independently (have researcher read once, pass refs)
- **Unscoped delegation**: "Research everything about auth" vs. "Find which files handle JWT validation"
- **Over-fetching web results**: Fetching 10 URLs when 2 would suffice
