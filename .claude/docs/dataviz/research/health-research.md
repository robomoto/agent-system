<!-- last_verified: 2026-03-14 -->
# Health Dashboard Research (CHI/UbiComp 2024-2026)

Recent academic findings directly applicable to personal health dashboards. Load for evidence-based design decisions.

## MIND — LLM-Powered Narrative Dashboard (CHI 2026)

**arXiv: 2601.14641**

Multimodal health dashboard for mental health clinicians. Combines patient data (activity, sleep, mood, social interaction) with LLM-generated natural language narratives alongside charts.

**Results (N=16 clinicians):**
- Significantly improved insight discovery (p<.001) vs charts alone
- Improved decision-making (p=.004) vs charts alone
- Clinicians used narratives as orientation before examining charts
- Narratives reduced the "cold start" problem of interpreting unfamiliar data

**Takeaway:** Add LLM-generated daily/weekly summaries alongside charts. Even simple summaries ("Weight trending down 0.3kg/week. Protein hit target 5/7 days. Sleep disrupted Tuesday — RHR elevated Wednesday.") significantly improve data comprehension.

## Vital Insight — Human-in-the-Loop LLM Agents (CHI 2025)

**arXiv: 2410.14879**

Combines visualization with human-in-the-loop LLM agents for multi-modal passive sensing data. Developed "expert sensemaking model": users navigate between direct data representation (charts) and AI-supported inference (pattern identification, anomaly explanation).

**Three rounds of user studies (N=21 experts):**
- Experts want BOTH raw data views AND AI interpretation
- Trust requires transparency: "AI thinks your sleep dipped because..." with the evidence shown
- The hybrid model (charts for reading, AI for pattern detection) outperforms either alone

**Takeaway:** The emerging standard for personal health data: charts for direct reading + AI for pattern detection and explanation. Don't replace charts with AI summaries — augment them.

## CounterStress — Counterfactual Explanations (CHI 2025, KAIST)

Uses counterfactual reasoning for stress coping: "If you had slept 7.5 hours instead of 6, your stress score would likely have been 12 points lower."

**Key innovation:** Moves beyond descriptive ("your stress was high") to prescriptive ("here's what would have changed it"). Counterfactuals make abstract correlations concrete and actionable.

**Takeaway:** Counterfactual/what-if reasoning is the next frontier. "If you'd hit your protein target yesterday, your recovery score would likely be 8 points higher." Requires a causal model, not just correlations.

## CareQOL — Contextual Personalization (UbiComp 2025)

Found that dashboards without contextual detail hindered self-reflection. Personalization based solely on passive sensing was insufficient.

**Key findings:**
- Users needed to annotate and contextualize their own data
- "Data-prompted interview" approach: the dashboard asks the user questions about their data
- Enable user-initiated personalization, not just algorithm-driven

**Takeaway:** Add annotation capability. A simple "add note to this day" feature dramatically improves data utility. Consider prompting: "Your HRV dropped 20% on Tuesday. Anything unusual happen?"

## PAIRcolator — Collaborative Data Reflection (CHI 2025)

Tangible visualization toolkit for collaborative personal data reflection.

**Key finding:** People understand their health data better when they explain it to someone else. Pair collaboration (two people reviewing each other's data) produced deeper reflection than solo review.

**Takeaway:** Consider a "share/compare" feature or a "coach view" where a trainer/partner/friend can see a dashboard summary. Social accountability improves both data engagement and behavior change.

## Quantified Self: Stage-Based Model (Li et al., CHI 2010 — Still Foundational)

Five stages of personal informatics:
1. **Preparation** — Deciding to track
2. **Collection** — Gathering data
3. **Integration** — Combining data from multiple sources
4. **Reflection** — Making sense of patterns
5. **Action** — Changing behavior based on insights

Most systems focus on collection (stages 1-2) and neglect reflection and action (stages 4-5). Dashboards should prioritize reflection support and actionable recommendations.

**Common failure modes:**
- Lapse and abandonment (most trackers quit within 6 months)
- Data overload without synthesis
- No connection between what's measured and what's actionable
- Missing data creates gaps that break continuity

**Design implications:**
- Design for missing/sparse data as the default state
- Reduce logging friction
- Make the dashboard useful even with incomplete data
- Pair every insight with a potential action

## Design Principles from Health Research (Consolidated)

1. **Narrative + charts > charts alone** — LLM-generated summaries improve insight discovery significantly (MIND)
2. **Charts + AI > either alone** — Hybrid approach is the emerging standard (Vital Insight)
3. **Counterfactuals > descriptions** — "What would have happened if..." is more actionable than "what happened" (CounterStress)
4. **User annotation is essential** — Passive sensing alone is insufficient for reflection (CareQOL)
5. **Social context improves reflection** — Explaining data to someone else deepens understanding (PAIRcolator)
6. **Design for stages 4-5** — Reflection and action, not just collection and display (Li et al.)
7. **Frequency framing for uncertainty** — "3 out of 10 days" not "30%" (Padilla)
8. **Integration > depth** — Cross-domain unified view beats deep single-domain (QS research)
