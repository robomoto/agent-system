---
name: agent-system project context
description: Key architecture facts about the agent-system project for future review sessions
type: project
---

Hub-and-spoke multi-agent framework. Lead (Opus) orchestrates specialist subagents (Sonnet/Haiku). Handoffs are structured JSON validated by Pydantic schemas in src/schemas/.

**Why:** Config-driven project; quality depends on prompt contract consistency, not code correctness per se.

**How to apply:** Reviews here focus on schema gaps, protocol ambiguity, circular dispatch risks, and delegation contract drift — not typical code bugs. The "code" is the agent definitions and CLAUDE.md.

Key files:
- .claude/agents/lead.md — orchestrator, owns delegation protocol
- .claude/agents/roster-checker.md — mandatory first dispatch
- src/schemas/ — Pydantic schemas; validate.py is the integration point
- .claude/skills/ — 8 reusable skill bundles
- tests/test_schemas.py — only schema validation, not protocol integration

Known schema-vs-agent-output mismatches (as of 2026-03-21 Pass 2+3 review):
1. accessibility.md: agent says severity=critical|major|minor; schema enforces critical|warning|suggestion
2. accessibility.md: agent output has theme/current/expected/fix fields; schema has description/suggested_fix/automated_test
3. technical-writer.md: agent output has "artifacts" + "style_notes"; schema has "files_changed" + "style_issues"
4. social-psychologist.md: agent output has feature_evaluated/community_context/analysis[]/recommendations[]/trade_offs; schema has findings[]/review_file
5. experimental-psychologist.md: agent output has research_question/measurement_design{}/implementation{}/limitations[]; schema has metrics[]/hypotheses[]
6. trauma-informed-design-specialist.md: agent output recommendations[] have topic/guidance/rationale/risk_level/discovery_test; SafetyFinding schema has feature/risk_level/affected_population/threat_scenario/recommendation

AgentName enum in base.py is missing 7 language specialists (python,javascript,kotlin,android,css,cloudflare-workers,embedded) — they use the generic LanguageSpecialistHandoff.

tracked-run SKILL.md says parse-run-metrics.py "does not exist yet" but scripts/parse-run-metrics.py actually exists (created 2026-03-08).

No last_verified headers in any doc bundle files despite roster-checker.md requiring them.

Pass 3 cross-reference findings (2026-03-21):
- accessibility bundle has patterns.md + idioms.md but agent only says "Read from .claude/docs/accessibility/" — no drift problem, just unspecified
- Skills "Used By" column in CLAUDE.md is metadata-only; no agent file actually declares skill dependencies by name (only qa.md loosely mentions testing-strategy). Mechanism is injection at spawn time by lead — agents don't self-declare. Skills table is descriptive, not enforced.
- dataviz specialist output format uses nested conservative/exploratory structure inside recommendations[] but the Recommendation model (topic/guidance/rationale/version/doc_ref) is flat — schema cannot represent the nested structure
- social-psychologist agent output has feature_evaluated/community_context/analysis[]/recommendations[]/trade_offs which do NOT map to SocialDynamicsFinding schema structure (schema only has findings[]/review_file)
- All 21 specialist JSON schemas are generated and exist in src/schemas/json/

Pass 4 architecture findings (2026-03-21):
- Architect and reviewer overlap on adversarial review — both explicitly claim adversarial thinking as a core responsibility; lead.md dispatch tiebreaker partially handles this
- SRE vs sysadmin overlap is documented and resolved in lead.md dispatch tiebreakers
- css-specialist and ui-designer overlap on color/contrast — ui-designer explicitly defers full WCAG audits to accessibility agent
- Testing-strategy skill is listed as used by implementer+reviewer in CLAUDE.md but no agent file references it; only QA loosely mentions it
- Doc bundles: all files under 300 lines (max observed: 260 lines for accessibility/idioms.md)
