# Plan: Agent System Performance Improvements

Based on critical review of the greenlake-community UX review session (2026-03-05).

## Problem Statement

The lead agent's first real team execution revealed 6 systemic inefficiencies that inflated cost and wall-clock time by ~40-50%. Token waste from duplicate reads alone was ~33 redundant file reads. Serial agent dispatch added ~3 minutes of unnecessary wait time.

---

## Improvements (priority order)

### P0: Parallelize independent agent dispatches

**Problem**: All 7 agents were dispatched sequentially despite being independent.

**Fix**: Update `lead.md` to include explicit parallelization rules:
```
## Dispatch Rules
- Independent research tasks MUST be dispatched in a single message (parallel).
- Independent analysis tasks (UX + UI review) MUST be dispatched in parallel.
- Only dispatch sequentially when Task B depends on Task A's output.
- Use `run_in_background: true` when the lead has its own work to do while waiting.
```

**Expected impact**: Wall-clock time drops from ~7min to ~4min for equivalent work.

### P1: Eliminate duplicate file reads

**Problem**: 33 of 68 Read calls were duplicates (48%). The lead re-read files already reported by specialists.

**Fix**: Add to `lead.md`:
```
## Context Discipline
- After receiving a specialist report, DO NOT re-read files the specialist already summarized
  unless you have specific reason to doubt a finding.
- Spot-check at most 3-5 files per specialist report to verify accuracy.
- If you need to reference a file you already read, use your memory of it — do not re-read.
```

**Expected impact**: ~30 fewer Read calls, ~50K fewer tokens consumed.

### P2: Right-size research phase — merge overlapping researchers

**Problem**: Structure researcher and template researcher had ~40% content overlap.

**Fix**: Use 2 researchers, not 3:
- **Codebase researcher**: project structure, tech stack, templates, CSS, JS — everything about WHAT exists
- **Flow researcher**: user journeys, permissions, email flows, admin workflows — everything about HOW it works

**Expected impact**: 1 fewer agent dispatch, ~50K fewer tokens.

### P3: Use correct subagent types

**Problem**: UX and UI analysis tasks were dispatched as `Explore` agents. Explore is for codebase navigation, not evaluation.

**Fix**:
- Research/discovery tasks -> `Explore` (correct)
- Analysis/evaluation tasks -> `general-purpose` with structured output requirements
- Implementation tasks -> `general-purpose` with write permissions

Update `lead.md` with a subagent type decision table.

### P4: Background agents + lead parallel work

**Problem**: Lead sat idle during all 7 agent dispatches.

**Fix**: After dispatching parallel researchers, the lead should immediately start:
- Reading project CLAUDE.md and key config files
- Drafting the plan skeleton (headings, structure)
- Preparing prompts for Phase 2 specialists

Use `run_in_background: true` for research agents so the lead can work concurrently.

### P5: One session, one project

**Problem**: Session mixed agent-system scaffold work with greenlake UX review. Context from the first project wasted tokens during the second.

**Fix**: Add to lead agent instructions:
```
## Session Hygiene
- Each major task should start in a fresh session.
- If the user switches projects mid-session, acknowledge that prior context will
  compress and may affect performance.
```

This is partly user behavior, but the lead should flag it.

### P6: Reviewer as explicit opt-in, not silent skip

**Problem**: Reviewer was planned but silently deferred.

**Fix**: After plan synthesis, the lead MUST explicitly ask:
```
"Plan complete. Would you like me to dispatch the reviewer for adversarial review
before we proceed to implementation? (Cost: ~30-50K tokens, ~60s)"
```

---

## Metrics to Track

| Metric | Baseline (this session) | Target |
|--------|------------------------|--------|
| Parallel dispatch rate | 0% (0/7) | >80% for independent tasks |
| Duplicate read rate | 48% (33/68) | <10% |
| Researcher overlap | ~40% | <15% |
| Wall-clock time (research+analysis) | ~7 min | ~4 min |
| Lead idle time during dispatches | ~7 min | <2 min |

---

## Fix Ownership

| Fix | File(s) | Rationale |
|-----|---------|-----------|
| P0: Parallel dispatch | `lead.md` | Lead controls dispatch timing |
| P1: No redundant reads | `lead.md` + `CLAUDE.md` + `researcher.md` | Lead re-reads specialist output; all agents re-read their own files; project-level rule |
| P2: Researcher overlap | `researcher.md` + `lead.md` | Researcher declares scope; lead scopes prompts |
| P3: Subagent type routing | `CLAUDE.md` | System-wide routing concern |
| P4: Background agents | `lead.md` | Lead controls its own idle time |
| P5: Session hygiene | `CLAUDE.md` | Project-level discipline |
| P6: Reviewer opt-in | `lead.md` | Lead's synthesis protocol |
| UX overcounting | `ux-designer.md` | UX designer flagged features as missing that existed |
| UI exemplar format | `ui-designer.md` | Codify file:line as required output standard |

## Implementation Order

1. ~~Update `lead.md` with dispatch rules, context discipline, reviewer opt-in (P0, P1, P4, P6)~~ DONE
2. ~~Update `CLAUDE.md` with subagent type routing table, no-redundant-reads rule, session hygiene (P1, P3, P5)~~ DONE
3. ~~Update `researcher.md` with scope declaration and no-reread rules (P1, P2)~~ DONE
4. ~~Update `ux-designer.md` with verify-before-flagging and no-duplicate-issues rules~~ DONE
5. ~~Update `ui-designer.md` with file:line reference requirement~~ DONE
6. Test with a real task and measure improvement (all)
