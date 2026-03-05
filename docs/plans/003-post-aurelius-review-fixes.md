# Plan: Post-Aurelius Review Fixes

Based on deficits observed during the aurelius-quote-api holistic review (2026-03-05, Run 2).

## Problem Statement

Eight systemic issues surfaced during Run 2. Seven are process/protocol gaps in agent definitions. One is a missing cultural norm: agents don't proactively script repeatable work. Manual verification steps, smoke tests, and deployment checks are described in prose but never turned into executable scripts.

---

## Fixes

### F1: Add review-only workflow to lead.md

**Problem**: The standard pipeline assumes implementation. For review tasks, the lead improvised — skipping researcher, dispatching 5 analysts in parallel, bolting on implementation after. No documented pattern exists.

**Fix**: Add a `## Review Workflow` section to lead.md:

```
## Review Workflow

For review/audit tasks (no implementation planned upfront):

Phase 1 — Roster check (mandatory, same as standard)
Phase 2 — Parallel analysis: dispatch relevant review agents in one batch
  (reviewer, architect, sre, ux-designer, technical-writer, etc.)
Phase 3 — Synthesis: combine findings, prioritize, present to user
Phase 4 — (Optional) Implementation: if user approves fixes, switch to
  standard pipeline starting at implementer

Skip researcher when the codebase is small enough to read directly (<500 LOC).
Skip QA for review-only tasks (no code changes = no test criteria needed).
Skip validator when no tests exist and no code was changed.

When skipping any agent, note it explicitly in the delegation plan.
```

### F2: Roster-checker fast path for small projects

**Problem**: ~6.5 minutes to audit a 2-file project. The roster-checker reads every agent definition file even when the project is trivial.

**Fix**: Add a fast-path to roster-checker.md:

```
### Fast Path (small projects)

If the project has fewer than 10 source files (excluding node_modules, .git, build artifacts):
1. Skip reading individual agent .md files — use a Glob to get the list of filenames only
2. Match filenames against project signals (e.g., "javascript-specialist.md" exists → JS is covered)
3. Only read agent files when you need to CREATE or MODIFY them
4. Skip doc bundle audit for agents that won't be dispatched in this task

This should complete in under 2 minutes for small projects.
```

### F3: Technical-writer as direct implementer for doc-only tasks

**Problem**: Technical-writer was dispatched as read-only reviewer, then a separate implementer executed the doc fixes. Unnecessary handoff.

**Fix**: Add dispatch guidance to lead.md agent roster entry:

```
| technical-writer | ... For review-only tasks, dispatch as analyst. For doc-fix tasks, dispatch as implementer — the technical-writer has Write/Edit tools and should write docs directly, not hand off to a generic implementer. |
```

### F4: Explicit validator skip rules in lead.md

**Problem**: Validator was silently skipped. Protocol says "always route through validator" but doesn't account for no-test-suite projects.

**Fix**: Add to lead.md under Standard Workflow:

```
### When to Skip Validator

Validator can be skipped when:
- No test suite exists AND no tests were added in this task
- Changes are documentation-only (no code behavior changed)
- The lead performed manual smoke testing (must document what was tested)

When skipping, explicitly note: "Validator skipped: [reason]. Manual verification: [what was tested]."
```

### F5: HTTP method coverage in reviewer adversarial checklist

**Problem**: Five specialists reviewed a web API and none flagged that HEAD requests return 405. The adversarial checklist doesn't cover HTTP method handling.

**Fix**: Add to reviewer.md adversarial checklist:

```
- [ ] For web APIs: Are all expected HTTP methods handled? (HEAD should work on GET endpoints; OPTIONS for CORS preflight)
```

### F6: Team log location

**Problem**: Team log was written to the reviewed project, polluting it with agent metadata.

**Fix**: Add to lead.md output format section:

```
## Team Log Location

Write team logs to the agent-system repo, not the project being reviewed:
  ~/claude_projects/agent-system/docs/team-logs/<project>-<date>.md

Team logs are agent performance metadata — they belong with the agent system,
not the project under review.
```

### F7: Doc bundle review gate

**Problem**: Roster-checker created doc bundles that were immediately trusted with no review.

**Fix**: Add to roster-checker.md:

```
### Doc Bundle Verification

After creating a doc bundle, self-verify by checking 2-3 claims against the
project's actual code or official documentation. Flag any unverified claims
with [UNVERIFIED] so the lead or reviewer can check later.

In your report, include a `doc_bundle_verified` field:
  "doc_bundle_verified": { "checked": 3, "confirmed": 2, "flagged": 1 }
```

### F8: "Script it" principle — the repeatability norm

**Problem**: Agents describe repeatable processes in prose but never produce scripts. The SRE said "add tests," the reviewer said "zero coverage," the lead manually ran curl commands — but nobody created a `scripts/smoke-test.sh`. This is a cultural gap: no agent is told to think about repeatability.

**Fix**: This needs to be encoded at three levels:

**A. System-level principle in CLAUDE.md** (new section):

```
### Repeatability Rule

If a process is performed manually during a task (smoke tests, deployment verification,
data validation, environment setup), it must be scripted before the task is complete.

The script goes in `scripts/` in the target project. Name it descriptively:
  scripts/smoke-test.sh, scripts/verify-deploy.sh, scripts/seed-data.sh

The lead enforces this as a final gate: "Was anything tested manually that isn't scripted?"
```

**B. Implementer operating constraint** (add to implementer.md):

```
- If you perform manual verification (curl commands, CLI checks, visual inspection),
  capture it as a script in `scripts/` before reporting completion. Manual steps that
  aren't scripted will be lost between sessions.
```

**C. SRE operating constraint** (add to sre.md):

```
- When recommending verification steps (health checks, smoke tests, load tests),
  always produce a runnable script — not just prose advice. A recommendation without
  a script is a recommendation that won't be followed.
```

**D. Reviewer checklist item** (add to reviewer.md):

```
- [ ] Were any manual verification steps performed that should be scripted?
```

**E. Lead final gate** (add to lead.md):

```
## Repeatability Gate (Final)

Before marking a task complete, check: "Was anything verified manually during this run?"
If yes, dispatch the implementer (or SRE for infra) to script it. A task is not complete
until repeatable processes are executable, not just documented.
```

---

## Implementation Order

1. lead.md — review workflow, validator skip rules, technical-writer dispatch note, team log location, repeatability gate (F1, F3, F4, F6, F8E)
2. roster-checker.md — fast path, doc bundle verification (F2, F7)
3. reviewer.md — HTTP method checklist item, repeatability checklist item (F5, F8D)
4. implementer.md — script-it constraint (F8B)
5. sre.md — script-it constraint (F8C)
6. CLAUDE.md — repeatability rule (F8A)

## Files Changed

| File | Fixes |
|------|-------|
| `.claude/agents/lead.md` | F1, F3, F4, F6, F8E |
| `.claude/agents/roster-checker.md` | F2, F7 |
| `.claude/agents/reviewer.md` | F5, F8D |
| `.claude/agents/implementer.md` | F8B |
| `.claude/agents/sre.md` | F8C |
| `CLAUDE.md` | F8A |
