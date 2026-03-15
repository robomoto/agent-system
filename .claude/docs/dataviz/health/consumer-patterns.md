# Consumer Health Product Visualization Patterns

What works (and doesn't) in shipped health/fitness products. Load for health dashboard design tasks.

## Recurring Winning Patterns

| Pattern | Products | Why it works |
|---------|----------|-------------|
| Single-number score (0-100) | Whoop, Oura, Fitbit, Garmin | Reduces cognitive load to one glance |
| Traffic-light color coding | Whoop, Levels, Garmin, Fitbit | Maps to universal good/warning/bad |
| Progress rings/arcs | Apple, Fitbit | Completion is viscerally satisfying |
| Horizontal progress bars | MFP, Cronometer, Fitbit | Goal progress in minimal vertical space |
| Stacked sleep stage bars | Oura, Garmin, Fitbit | Sleep composition at a glance |
| Trend sparklines | All | Change over time in minimal space |
| Progressive disclosure | Whoop, Oura, Apple | Score first → contributors → raw data |
| Personal baseline comparison | Whoop, Garmin, Oura | "Different from YOUR normal" > absolute thresholds |

## Universal Gaps (Opportunities)

- **Cross-domain correlation** — No product connects nutrition inputs to sleep/recovery outputs well
- **Temporal context** — Products show "today" well; navigating weeks/months is clunky everywhere
- **Data export/ownership** — Most products lock data in silos
- **Annotation** — Users can't mark "sick this week" or "traveling" to contextualize anomalies

## Product-Specific Lessons

### Apple Watch — Activity Rings
Three concentric rings (Move, Exercise, Stand). Works because of binary daily goal framing (did I close it?), arc-length progress encoding, and streak gamification. Minimal cognitive load: 3 metrics, 3 colors, one glance. Deep screens suffer from inconsistent navigation and overwhelming metric density.

**Takeaway:** Rings for 3-5 daily goals max. Don't replicate the drill-down chaos.

### Whoop — Strain/Recovery/Sleep
Single-number scores with traffic-light color. Strain (0-21), Recovery (0-100%), Sleep Performance (0-100%). Progressive disclosure: orbs first → drill into HRV, RHR, respiratory rate, skin temp. Contextual: "recovery low because strain high yesterday and sleep short."

**Takeaway:** Percentage-based scores (0-100) are more intuitive than arbitrary scales. Always explain the score.

### Oura — Readiness Score
Hypnogram for sleep stages (clean clinical viz adapted for consumers). Body Clock (24-hour radial comparing actual vs optimal sleep window). Contributor decomposition makes scores feel explainable. Only 30% of users feel they can *act* on the data — score decomposition needs actionable interpretation, not just numbers.

### Garmin — Body Battery / Training Load
Body Battery (0-100): energy that depletes with activity/stress, recharges with rest/sleep. Displayed as continuous 24-hour area chart — immediately legible "energy as depleting resource" metaphor. Training Load separates anaerobic/high aerobic/low aerobic in stacked viz. App itself is notoriously cluttered — dozens of widgets, no hierarchy.

**Takeaway:** Energy-as-resource metaphor is brilliant. Stacked load decomposition strong for exercise.

### MyFitnessPal / Cronometer — Nutrition
MFP: horizontal progress bars for macros + calorie remaining hero metric. Simple and effective. Cronometer: 80+ nutrients with horizontal bars showing % of daily target. Green when met, yellow approaching, empty when deficient.

**Takeaway:** For macros, horizontal progress bars (simplified bullet charts) are the standard. For micronutrients, group by category, collapse by default, highlight only deficiencies.

### Levels / Nutrisense — Continuous Glucose
Real-time glucose line chart with "stability zone" band (70-120 mg/dL target). Meal scoring (1-10) based on spike height, rise speed, area under curve. Color zones applied to line chart.

**Takeaway:** Continuous line charts with target-range bands are gold standard for any biomarker with a healthy range. Meal-response overlays are a powerful correlation viz.

### RISE — Circadian Energy
24-hour energy curve — a *predictive* viz showing future energy peaks and dips. Sleep inertia → morning peak → afternoon dip → evening peak → melatonin window. Calendar-integrated for day planning.

**Takeaway:** Predictive energy curves are novel and actionable. High-value if combining sleep + nutrition + exercise data.

### Strava — Fitness & Freshness
Banister's impulse-response model: Fitness (slow-building), Fatigue (fast-rising/falling), Form (fitness minus fatigue). Powerful for serious athletes but too complex for glanceable view. Three-line chart confusing for non-athletes.

**Takeaway:** Compute fitness/fatigue/form but display summary: "Fitness: trending up, Form: ready to perform" with a sparkline.
