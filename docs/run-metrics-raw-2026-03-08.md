Using: /Users/chris/.claude/projects/-Users-chris-claude-projects/e895e610-f453-4303-b835-394db7b7a691.jsonl
# Run Metrics (JSONL ground truth)

**Source**: `/Users/chris/.claude/projects/-Users-chris-claude-projects/e895e610-f453-4303-b835-394db7b7a691.jsonl`
**Period**: 2026-03-09T01:35:00.177Z to 2026-03-09T02:41:38.159Z
**Messages**: 402

## Dispatch Metrics

| Metric | Value |
|--------|-------|
| Dispatches (total) | 7 |
| Dispatches (parallel) | 3 (1 batches) |
| Dispatches (sequential) | 4 |
| Dispatches (background) | 1 |
| **Parallel dispatch rate** | **43%** |

### Agent Dispatch Detail

| # | Description | Type | Background | Prompt Size |
|---|-------------|------|------------|-------------|
| 1 | Find email threading code | Explore | no | 692 chars |
| 2 | Roster check for task |  | no | 866 chars |
| 3 | UX designer review |  | no | 2278 chars |
| 4 | UI designer review |  | no | 2094 chars |
| 5 | Social psych review |  | no | 2748 chars |
| 6 | Post-run metrics review |  | yes | 649 chars |
| 7 | Implement digest reply links |  | no | 2106 chars |

### Concurrent Batches (detected by temporal overlap)

**Batch 1** [sequential (1 agent)]:
- Find email threading code (dispatched 01:36:11.537, returned 01:37:01.105)

**Batch 2** [sequential (1 agent)]:
- Roster check for task (dispatched 01:37:23.808, returned 01:37:52.636)

**Batch 3** [PARALLEL (3 agents)]:
- UX designer review (dispatched 01:38:12.386, returned 01:39:30.731)
- UI designer review (dispatched 01:38:22.951, returned 01:39:50.991)
- Social psych review (dispatched 01:38:37.158, returned 02:00:11.492)

**Batch 4** [sequential (1 agent)]:
- Post-run metrics review (dispatched 02:30:15.779, returned 02:30:15.787)

**Batch 5** [sequential (1 agent)]:
- Implement digest reply links (dispatched 02:30:30.363, returned 02:31:34.647)

### Timeline

| Time | Event | Agent |
|------|-------|-------|
| 01:36:11.537 | DISPATCH | Find email threading code |
| 01:37:01.105 | RESULT | Find email threading code |
| 01:37:23.808 | DISPATCH | Roster check for task |
| 01:37:52.636 | RESULT | Roster check for task |
| 01:38:12.386 | DISPATCH | UX designer review |
| 01:38:22.951 | DISPATCH | UI designer review |
| 01:38:37.158 | DISPATCH | Social psych review |
| 01:39:30.731 | RESULT | UX designer review |
| 01:39:50.991 | RESULT | UI designer review |
| 02:00:11.492 | RESULT | Social psych review |
| 02:30:15.779 | DISPATCH | Post-run metrics review |
| 02:30:15.787 | RESULT | Post-run metrics review |
| 02:30:30.363 | DISPATCH | Implement digest reply links |
| 02:31:34.647 | RESULT | Implement digest reply links |

## Read Metrics

| Metric | Value |
|--------|-------|
| Reads (total, lead only) | 15 |
| Reads (unique files) | 10 |
| Reads (duplicate) | 5 |
| **Duplicate read rate** | **33%** |

### Duplicated Files

| File | Times Read |
|------|-----------|
| `SKILL.md` | 3 |
| `lead.md` | 2 |
| `social-psychologist.md` | 2 |
| `CLAUDE.md` | 2 |

## Token Usage (lead only)

| Metric | Value |
|--------|-------|
| Input tokens | 125 |
| Output tokens | 14,005 |
| Cache creation | 249,387 |
| Cache read | 3,688,489 |
| **Total (input+output)** | **14,130** |

## Tool Usage

| Tool | Calls |
|------|-------|
| Read | 15 |
| Bash | 15 |
| Agent | 7 |
| Edit | 7 |
| Glob | 2 |
| Write | 1 |

## Idle Gaps (excluded from lead active time)

Threshold: >120s between messages.

| Start | End | Duration |
|-------|-----|----------|
| 01:40:26 | 01:59:33 | 19.1 min |
| 02:01:22 | 02:30:08 | 28.8 min |
| 02:35:53 | 02:38:42 | 2.8 min |


## Summary

| Metric | Value |
|--------|-------|
| Parallel dispatch rate | 43% |
| Duplicate read rate | 33% |
| Total tokens (lead) | 14,130 |
| Lead active time | ~15.9 min |
| Session duration | ~66.6 min |
