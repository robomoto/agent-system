<!-- last_verified: 2026-03-14 -->
# Clinical Dashboard Translation

What translates from medical informatics to personal health dashboards, and what doesn't.

## What Translates Well

### Structured Layouts
Clinical dashboards use rigid position grammar: vitals top-left, labs center, trends right. Consistency across patients reduces error.

**Translation:** Adopt a rigid layout grammar. Same position for same data type, always. Users build spatial memory — weight is always top-left, nutrition always center, etc.

### Alert Hierarchies
Clinical: Critical alerts interrupt; warnings are visible but non-blocking; normal values are suppressed.

**Translation:** Only surface metrics that deviate from baseline. Don't show "HRV: normal" — show nothing (or a tiny green dot). Show "HRV: 22% below baseline" prominently. Suppress the unremarkable.

### Temporal Alignment
All metrics on the same time axis so clinicians can spot co-occurring events.

**Translation:** Align all charts to the same x-axis in review mode. When weight dips and sleep improves on the same days, the visual correlation is immediate.

### Sparkline Tables
ICU dashboards embed sparklines in tables: metric name | current value | 24h trend sparkline | status. Directly applicable to personal dashboards.

## What Doesn't Translate

- **Dense data tables** — Clinicians are trained to parse them; consumers aren't
- **Multi-patient views** — Personal dashboards serve one person
- **Real-time monitoring** — Personal health changes on hours/days scale, not seconds. 5-minute refresh is fine.
- **Jargon-heavy labels** — Clinical shorthand (SpO2, SBP, GCS) needs consumer-friendly naming

## Patient-Facing Research Findings (JMIR 2024-2025)

- Well-designed visualizations reduce anxiety and improve self-management
- Patients describe effective designs as ones that "attract your eyes and brain"
- **Trend visualization is the most valued feature** across conditions
- Nearly half of patient-facing tools studied were never tested with actual patients — participatory design is critical
- Integration matters more than depth: users with data in 3+ silos struggle to form holistic understanding. A unified dashboard connecting domains is more valuable than deep single-domain tools.

## Personal Baseline Comparison

**Implementation pattern:**
1. Compute rolling mean and standard deviation (14-30 day window)
2. Flag deviations >1σ as "notable," >2σ as "anomaly"
3. Display as: "Your RHR is 8bpm higher than your 14-day average"
4. Color intensity encodes deviation magnitude

**Strengths:** Makes data personally meaningful. An HRV of 45ms means nothing in absolute terms; "15ms below your baseline" is immediately actionable.

**Weaknesses:** Needs enough historical data to establish baseline (cold start). Rolling baselines drift — gradual fitness decline stops alarming.

**Precedent:** Whoop (personal baseline for RHR, HRV, respiratory rate, skin temp), Garmin Body Battery, Oura readiness contributors.

## Quantified Self Research: Key Findings

1. **Reflection requires context, not just data** (Li et al., CHI 2010). Raw numbers without comparison or narrative don't support reflection.
2. **Actionability is the bottleneck** (Oura UX: only 30% felt they could act on data). Pair observations with suggestions.
3. **Lapse and abandonment are the norm.** Most self-trackers quit within 6 months. Design for missing/sparse data as the default state.
4. **Integration > depth.** Unified cross-domain view beats deep single-domain tools.

## Contextual Annotations

Types of annotations for health dashboards:

- **Auto-detected:** Workout days, travel (timezone changes), illness (elevated RHR + reduced activity), alcohol (HRV drop), poor sleep → next-day performance
- **Manual:** Free-text notes, life events, injuries, supplements, medication changes
- **Inferred correlations:** "When you eat after 9pm, your deep sleep % drops 18% on average"

Auto-annotation from existing data (workout days on weight/HRV charts) is the highest-ROI starting point. Simple vertical line markers for workouts on a weight trend chart add enormous context.
