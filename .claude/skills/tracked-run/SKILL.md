# Skill: Tracked Run

Self-review framework for measuring team execution quality. Instruments a run with metrics collection so performance can be compared across sessions. Used by the lead agent.

## When to Use

- The user requests a tracked run (e.g., "track this run", "measure performance")
- The lead wants to benchmark a new workflow or compare against a previous run
- After making changes to agent definitions or delegation rules and validating improvement

## Setup

### 1. Read the Baseline

Before starting any work, read the performance baseline:
- `docs/plans/002-performance-improvements.md` for target metrics
- Any previous team logs referenced in the plan or memory

If no baseline exists yet, this run becomes the baseline. Note that in the team log.

### 2. Initialize Counters

Track these metrics throughout the run. You don't need tooling — maintain them as mental counters and report them in the team log at the end.

| Metric | What to count |
|--------|---------------|
| `dispatches_total` | Total Agent tool calls |
| `dispatches_parallel` | Agent calls sent in the same message (count the message as 1, agents as N) |
| `dispatches_sequential` | Agent calls sent alone in a message |
| `dispatches_background` | Agent calls with `run_in_background: true` |
| `reads_total` | Total Read tool calls (lead only, not subagents) |
| `reads_unique` | Distinct file paths read |
| `reads_duplicate` | `reads_total - reads_unique` |
| `agent_tokens` | Token usage per agent (from handoff reports) |
| `wall_clock_per_phase` | Approximate time per phase (use timestamps or estimates) |

### 3. Instrument Dispatch Decisions

Every time you dispatch agents, log a one-line note in your working memory:

```
Dispatch: [parallel|sequential] N agents (reason: <why parallel or why sequential>)
```

This forces you to justify sequential dispatches. If you can't justify it, make it parallel.

## During the Run

### Parallel Dispatch Checkpoint

Before every Agent tool call, ask yourself:
1. Does this agent depend on a result I haven't received yet?
   - **Yes** -> Sequential is justified. Log the dependency.
   - **No** -> It MUST be parallel with other independent dispatches.
2. Am I dispatching only one agent when I could batch more?
   - Check if the next phase's agents are also ready to go.

### Read Discipline Checkpoint

Before every Read tool call, ask yourself:
1. Did a specialist already report on this file's contents?
   - **Yes** -> Don't read it. Use the specialist's report.
   - **No** -> Read it, but only once.
2. Did I already read this file earlier in this session?
   - **Yes** -> Use your memory of it. Don't re-read.
   - **No** -> Read it.

### Researcher Overlap Checkpoint

When dispatching multiple researchers in parallel:
1. Write each researcher's scope explicitly in its prompt.
2. Scopes must not overlap. If researcher A covers "project structure and tech stack", researcher B must NOT also report on tech stack.
3. Two well-scoped researchers beat three fuzzy ones.

## After the Run

### Write the Metrics Section

Add a `## Run Metrics` section to the team log with this exact format:

```markdown
## Run Metrics

| Metric | Value |
|--------|-------|
| Dispatches (total) | N |
| Dispatches (parallel) | N (M batches) |
| Dispatches (sequential) | N |
| Dispatches (background) | N |
| Reads (total, lead only) | N |
| Reads (unique files) | N |
| Reads (duplicate) | N |
| Duplicate read rate | X% |
| Parallel dispatch rate | X% |
| Total tokens (all agents) | ~NK |
| Lead active time | ~N min |
| Session duration | ~N min |
```

**Lead active time** measures the lead's performance — time spent working, excluding idle
gaps >2 min (user think time, AFK, etc.). The `parse-run-metrics.py` script computes this
automatically by subtracting gaps >120s between consecutive messages.

**Session duration** is the full wall-clock span from first to last message. This includes
user interaction time and is NOT a measure of lead performance.

### Rates

```
Parallel dispatch rate = dispatches_parallel / dispatches_total * 100
Duplicate read rate = reads_duplicate / reads_total * 100
```

### Preserve Researcher Findings

If a researcher was dispatched, include a `## Researcher Findings` section in the team log summarizing the key discoveries (architecture, file paths, patterns found). Researcher output is lost when the session ends — the team log is the only durable record. Keep it to 10-15 bullet points covering what was discovered and where.

### Write the Comparison Section (if baseline exists)

```markdown
## Comparison vs Baseline

| Metric | Baseline (Run N) | This Run | Delta |
|--------|-----------------|----------|-------|
| Parallel dispatch rate | X% | Y% | +/-Z% |
| Duplicate read rate | X% | Y% | +/-Z% |
| Total tokens | ~NK | ~NK | +/-NK |
| Lead active time | ~N min | ~N min | +/-N min |
```

### Self-Critique

After writing metrics, add a `## Self-Critique` section answering:

1. **What dispatches were sequential that could have been parallel?** List each with the reason it happened.
2. **What files were read redundantly?** List each duplicate and why it happened.
3. **What specialist output did I re-verify unnecessarily?** List files you re-read despite having a specialist report.
4. **What would I do differently next time?** Concrete changes, not vague intentions.

### Update the Baseline

If this run is better than the baseline on 3+ metrics, it becomes the new baseline. Update the memory entry with the new numbers.

If this run is worse, note why in the self-critique (was the task harder? did something go wrong? did a rule get ignored?).

## Example

<example>
Task: "Review the auth system for security issues"

Dispatch log:
- Dispatch: parallel 2 agents (researcher: codebase structure, researcher: auth flow mapping) -- independent discovery
- Dispatch: sequential 1 agent (reviewer: security audit) -- depends on researcher output
- Dispatch: background 1 agent (validator: run existing tests) -- independent, lead synthesizing in parallel

Run Metrics:
| Metric | Value |
|--------|-------|
| Dispatches (total) | 4 |
| Dispatches (parallel) | 2 (1 batch) |
| Dispatches (sequential) | 1 |
| Dispatches (background) | 1 |
| Reads (total, lead only) | 8 |
| Reads (unique files) | 7 |
| Reads (duplicate) | 1 |
| Duplicate read rate | 12.5% |
| Parallel dispatch rate | 50% |

Self-Critique:
1. The validator could have been dispatched in the same batch as the reviewer (both depend on researcher output, neither depends on the other). That would have raised parallel rate to 75%.
2. Re-read `auth/handler.ts` after the researcher already summarized it. Should have trusted the report.
</example>

## Post-Run Review (automated)

After writing the team log, spawn a **reviewer agent** to independently verify your self-reported metrics. This is mandatory for tracked runs.

**Important:** The post-run reviewer dispatch is NOT counted in the run metrics. It is meta-instrumentation — overhead for measuring the run, not part of the task itself. Similarly, any implementer or other agent dispatched AFTER the user requests follow-up work (e.g., "now implement it") is a separate task, not part of the original tracked run.

### Dispatch Rules

1. Run the metrics script first to generate ground-truth data. Use `--project` to filter to the correct project's JSONL (avoids grabbing a different project's session):
   ```
   python3 scripts/parse-run-metrics.py latest --project greenlake
   ```
   Replace `greenlake` with a substring matching the project directory name. Save the output to a file (e.g., `docs/run-metrics-raw.md`).

2. Spawn the reviewer with **only file references** — no summaries, no context, no editorializing. Use this exact prompt template:

   ```
   You are performing a post-run review of an agent team execution.

   Read the review protocol at:
     agent-system/docs/post-run-review.md

   Artifacts to analyze:
     - Ground-truth metrics: <path to script output file>
     - Team log (self-reported): <path to team-log.md>

   Follow the review protocol exactly. Write your report to:
     <project>/docs/post-run-review-<date>.md
   ```

3. Do NOT include any of the following in the prompt:
   - Your own summary of what happened
   - Which metrics you think are good or bad
   - Explanations or justifications for your decisions
   - Any content from the team log

   The reviewer must form its own conclusions from the raw artifacts.

### Why This Works

Subagents start with a blank conversation — they don't inherit your context. By passing only file paths, the reviewer gets an unbiased view. The script provides ground-truth numbers that can't be influenced by self-reporting.

## Checklist

- [ ] Baseline read (or declared as first run)
- [ ] Dispatch decisions logged with parallel/sequential justification
- [ ] Run Metrics section written with all fields
- [ ] Comparison table included (if baseline exists)
- [ ] Self-Critique section written with concrete answers
- [ ] Baseline updated in memory if this run improved on 3+ metrics
- [ ] `parse-run-metrics.py latest` run and output saved
- [ ] Reviewer spawned with locked-down prompt (file refs only, no context)
