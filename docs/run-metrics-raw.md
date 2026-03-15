# Run Metrics (JSONL ground truth)

**Source**: `/Users/chris/.claude/projects/-Users-chris-claude-projects/04757753-ee5e-412a-81e5-2d4fdab4c8d1.jsonl`
**Period**: 2026-03-09T01:06:03.186Z to 2026-03-09T01:43:58.517Z
**Messages**: 519

## Dispatch Metrics

| Metric | Value |
|--------|-------|
| Dispatches (total) | 6 |
| Dispatches (parallel) | 5 (2 batches) |
| Dispatches (sequential) | 1 |
| Dispatches (background) | 0 |
| **Parallel dispatch rate** | **83%** |

### Agent Dispatch Detail

| # | Description | Type | Background | Prompt Size |
|---|-------------|------|------------|-------------|
| 1 | Roster check for blind-roll | general-purpose | no | 1506 chars |
| 2 | UX review of Blind Roll | general-purpose | no | 3117 chars |
| 3 | UI review of Blind Roll | general-purpose | no | 3074 chars |
| 4 | Social psych review Blind Roll | general-purpose | no | 4434 chars |
| 5 | Architect web client plan | Plan | no | 5543 chars |
| 6 | Design DM-selectable themes | general-purpose | no | 3639 chars |

### Concurrent Batches (detected by temporal overlap)

**Batch 1** [sequential (1 agent)]:
- Roster check for blind-roll (dispatched 01:06:50.333, returned 01:07:23.265)

**Batch 2** [PARALLEL (3 agents)]:
- UX review of Blind Roll (dispatched 01:08:13.965, returned 01:13:33.963)
- UI review of Blind Roll (dispatched 01:08:27.952, returned 01:14:46.888)
- Social psych review Blind Roll (dispatched 01:08:52.545, returned 01:13:58.418)

**Batch 3** [PARALLEL (2 agents)]:
- Architect web client plan (dispatched 01:32:43.550, returned 01:37:28.231)
- Design DM-selectable themes (dispatched 01:33:05.258, returned 01:36:16.773)

### Timeline

| Time | Event | Agent |
|------|-------|-------|
| 01:06:50.333 | DISPATCH | Roster check for blind-roll |
| 01:07:23.265 | RESULT | Roster check for blind-roll |
| 01:08:13.965 | DISPATCH | UX review of Blind Roll |
| 01:08:27.952 | DISPATCH | UI review of Blind Roll |
| 01:08:52.545 | DISPATCH | Social psych review Blind Roll |
| 01:13:33.963 | RESULT | UX review of Blind Roll |
| 01:13:58.418 | RESULT | Social psych review Blind Roll |
| 01:14:46.888 | RESULT | UI review of Blind Roll |
| 01:32:43.550 | DISPATCH | Architect web client plan |
| 01:33:05.258 | DISPATCH | Design DM-selectable themes |
| 01:36:16.773 | RESULT | Design DM-selectable themes |
| 01:37:28.231 | RESULT | Architect web client plan |

## Read Metrics

| Metric | Value |
|--------|-------|
| Reads (total, lead only) | 15 |
| Reads (unique files) | 14 |
| Reads (duplicate) | 1 |
| **Duplicate read rate** | **7%** |

### Duplicated Files

| File | Times Read |
|------|-----------|
| `remote-play-plan.md` | 2 |

## Token Usage (lead only)

| Metric | Value |
|--------|-------|
| Input tokens | 1,108 |
| Output tokens | 20,445 |
| Cache creation | 272,200 |
| Cache read | 3,297,479 |
| **Total (input+output)** | **21,553** |

## Tool Usage

| Tool | Calls |
|------|-------|
| Read | 15 |
| Bash | 7 |
| Glob | 6 |
| Agent | 6 |
| Write | 2 |
| Edit | 1 |

## Summary

| Metric | Value |
|--------|-------|
| Parallel dispatch rate | 83% |
| Duplicate read rate | 7% |
| Total tokens (lead) | 21,553 |
| Wall-clock time | ~37.9 min |
