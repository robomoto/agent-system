# Post-Run Review

Reference doc for reviewing a tracked agent run. This review verifies the lead's self-reported metrics against ground truth and assesses execution quality.

## How This Gets Invoked

The lead spawns you automatically at the end of a tracked run, or a user can invoke you manually in a fresh session. Either way, you receive only file paths — no pre-digested context from the lead.

## Ground-Truth Metrics

The script `scripts/parse-run-metrics.py` extracts metrics directly from the JSONL session log. If the lead hasn't already run it, run it yourself:

```bash
python3 scripts/parse-run-metrics.py latest
# or with a specific file:
python3 scripts/parse-run-metrics.py ~/.claude/projects/-Users-chris-claude-projects/<SESSION_ID>.jsonl
```

This gives you dispatch counts, parallelization, duplicate reads, token usage, and timing — all from the raw log, independent of anything the lead reported.

### Scoping Rules

**What counts as a task dispatch:**
- Agents dispatched to accomplish the user's original request (roster-checker, researchers, reviewers, designers, etc.)

**What does NOT count:**
- The post-run reviewer itself (meta-instrumentation, not task work)
- Agents dispatched for follow-up work the user requested separately (e.g., "now implement it" after a review task)
- Background metric-parsing agents

When comparing JSONL ground truth against self-reported metrics, exclude these meta-dispatches from both the actual and expected counts.

### Timing Metric

The primary timing metric is **lead active time**, not session duration or wall-clock time. Lead active time excludes idle gaps >2 min (user think time, AFK, etc.). The `parse-run-metrics.py` script computes this automatically. Session duration (total wall-clock) is informational only — it reflects user behavior, not lead performance.

## What to Analyze

### 1. Get Ground-Truth Metrics

Run the script (or read its output if the lead already saved it):

```bash
python3 scripts/parse-run-metrics.py latest
```

The script extracts: dispatch counts, parallel vs sequential batching, duplicate reads, token usage, and wall-clock time — all directly from the JSONL.

### 2. Compare Against Self-Reported Metrics

Read the team log's `## Run Metrics` section (written by the lead using the `tracked-run` skill). Compare every number against the JSONL ground truth.

Flag any discrepancy as one of:
- **Honest error**: lead miscounted (e.g., off by 1-2)
- **Optimistic reporting**: lead claimed parallel dispatch that was actually sequential
- **Missing data**: lead didn't report a metric at all

### 3. Assess Dispatch Quality

For each Agent dispatch in the JSONL:

1. **Was it parallel when it could have been?** Look at sequential dispatches — did the next dispatch depend on the previous result, or could they have been batched?
2. **Was the subagent type appropriate?** Discovery tasks should use `Explore`, analysis/evaluation should use `general-purpose`, implementation should use `general-purpose`.
3. **Were researcher scopes distinct?** If multiple researchers were dispatched, read their prompts (`input.prompt`) and check for overlapping scope.

### 4. Assess Read Discipline

For each duplicate file read:

1. **Was it re-reading after a specialist report?** If a subagent already reported on the file, the lead shouldn't re-read it.
2. **Was it re-reading its own earlier read?** Context compression may cause this — note it but don't flag it as harshly.
3. **Was the re-read justified?** Sometimes a file changes mid-session (after an Edit/Write). That's a valid re-read.

### 5. Check Specialist Output Quality

For each Agent dispatch, check the result that came back:

1. **Did researchers include file:line references?** (required)
2. **Did designers include actionable fixes?** (required for ui-designer)
3. **Did the UX designer verify before flagging?** Look for false "missing feature" reports.
4. **Was there researcher overlap?** Compare findings across researcher reports for duplicated content.

## Output Format

Write findings as a review report:

```markdown
# Post-Run Review: [task name]

## Session
- JSONL: `<path>`
- Team log: `<path>`
- Date: YYYY-MM-DD

## Metrics Verification

| Metric | Self-Reported | Actual (JSONL) | Match? |
|--------|--------------|----------------|--------|
| Dispatches (total) | N | N | Y/N |
| Dispatches (parallel) | N | N | Y/N |
| Duplicate read rate | X% | X% | Y/N |
| Total tokens | ~NK | ~NK | Y/N |
| Lead active time | ~N min | ~N min | Y/N |

## Discrepancies
[List any mismatches with severity and likely cause]

## Dispatch Quality
[Assessment of parallelization decisions, subagent type choices, researcher scoping]

## Read Discipline
[List of unjustified duplicate reads with file paths]

## Specialist Output Quality
[Assessment of each specialist's report quality]

## Comparison vs Baseline

| Metric | Baseline | This Run | Delta | Trend |
|--------|----------|----------|-------|-------|
| Parallel dispatch rate | X% | Y% | +/-Z% | better/worse/same |
| Duplicate read rate | X% | Y% | +/-Z% | better/worse/same |
| Total tokens | ~NK | ~NK | +/-NK | better/worse/same |
| Lead active time | ~N min | ~N min | +/-N min | better/worse/same |

## Verdict

[One of:]
- IMPROVED: 3+ metrics better, none significantly worse
- MIXED: Some better, some worse
- REGRESSED: 3+ metrics worse
- BASELINE: First tracked run, no comparison available

## Recommendations
[Concrete changes to agent definitions or lead behavior for next run]
```

## Baseline Reference

The current baseline (Run 1, greenlake UX review, 2026-03-05):

| Metric | Value |
|--------|-------|
| Parallel dispatch rate | 0% (0/7 dispatches) |
| Duplicate read rate | 48% (33/68 reads) |
| Researcher overlap | ~40% |
| Lead active time | ~7 min |
| Total tokens | ~267K |

Source: `docs/plans/002-performance-improvements.md` and MEMORY.md.
Update this section when a new baseline is established.
