# Dashboard Architecture

Structural principles for organizing data displays. Load for layout, hierarchy, and interaction design questions.

## Shneiderman's Visual Information-Seeking Mantra (1996)

"Overview first, zoom and filter, then details on demand."

1. **Overview** — Show the full dataset at a glance (e.g., a year of weight data)
2. **Zoom and filter** — Let the user narrow to a region of interest (e.g., last 3 months, or only days with >2000 calories)
3. **Details on demand** — Click a specific data point for full detail (e.g., exact meals on a given day)

This three-stage pattern is the default interaction architecture for dashboards. A health app: year-view timeline (overview) → pinch to zoom into a week (zoom/filter) → tap a day for meal-by-meal breakdown (details).

## Stephen Few's Dashboard Principles

From *Information Dashboard Design* (2006, 2nd ed 2013):

- **A dashboard is a single screen.** If it scrolls, it's a report. (Challenged by mobile, but the principle — show the essential state in one view — holds.)
- **Glanceable in 3-5 seconds.** The dashboard should convey essential state at a glance.
- **Bullet graphs over gauges.** Few invented the bullet graph: horizontal bar (current value) + vertical marker (target) + background bands (qualitative ranges: poor/satisfactory/good). Far more information-dense than circular gauges.
- **Sparklines for context.** Embed sparklines next to summary stats for temporal context without consuming space.
- **Alert-driven design.** Subtle color/position encoding draws attention to out-of-range metrics. Suppress what's normal; highlight what needs attention.
- **Minimize decoration.** No 3D effects, gratuitous gradients, useless icons.

### Few's Common Dashboard Failures
1. Too much data without hierarchy
2. Perceptually inefficient elements (gauges, pie charts)
3. No context (number without trend or target is meaningless)
4. Aesthetic priority over communication

## Progressive Disclosure Pattern

Reveal detail in layers. Each layer answers a different question:

| Layer | Shows | Answers | Comprehension time |
|-------|-------|---------|-------------------|
| **Glanceable** | Scores + color status + sparkline direction | "How am I doing?" | <3 seconds |
| **Summary** | Score + top contributors + short trend | "What's going on?" | 10-15 seconds |
| **Detail** | Full charts, raw data, historical comparison | "Show me the data" | 30+ seconds |
| **Analysis** | Correlations, distributions, statistical context | "Why is this happening?" | Minutes |

**Who does it well:** Whoop (daily orb → score breakdown → individual metrics → raw HRV). RISE (sleep debt number → energy curve → sleep stages).
**Who does it poorly:** Garmin (everything visible at once). Apple Health deeper screens (inconsistent disclosure).

## Information Density Targets

Research-backed guidelines (JMIR 2024 systematic review, 46 health dashboard studies):

1. **Gestalt grouping** — Visually cluster related metrics
2. **Reduction** — Show only what's changed or noteworthy; suppress the normal
3. **Organization** — Consistent layout grammar (score → trend → detail, always in that order)
4. **Abstraction** — Composite scores as entry points, raw data behind them
5. **Task alignment** — Design for what the user *does* with the data, not what data exists

**Practical density:**
- Glanceable: 4-6 cards, 1-2 numbers + sparkline each ≈ 12-15 data points
- Summary: 6-8 cards, 3-4 metrics each ≈ 24-32 data points
- Analysis: Full charts, tables, correlations — unlimited but paged/tabbed

## Sparkline Table Pattern

Borrowed from clinical dashboards (ICU monitoring). A compact table:

```
Metric Name | Current Value | Δ from baseline | 14-day sparkline | Status
────────────┼───────────────┼─────────────────┼──────────────────┼────────
Weight      | 82.1 kg       | −0.4 kg         | [tiny line]      | ● (blue)
RHR         | 58 bpm        | +3 bpm          | [tiny line]      | ▲ (orange)
Sleep       | 7.2 hr        | +0.1 hr         | [tiny line]      | ● (blue)
Protein     | 148/160 g     | —               | [tiny line]      | ● (blue)
```

Extremely dense, extremely glanceable. Each row is a self-contained unit. Status column uses color + icon (redundant encoding for accessibility).

## Temporal Navigation

Health metrics have natural time scales:

| Metric | Primary | Secondary |
|--------|---------|-----------|
| Calories / macros | Day | Week |
| Sleep | Night | Week |
| Weight | Week | Month |
| Body composition | Month | Quarter |
| RHR / HRV | Day | Month |
| Training volume | Week | Month |
| VO2 max / fitness | Month | Year |

**Pattern:** Global time-range selector (Day/Week/Month/Year) controlling all charts. Individual charts can override when their natural scale differs. Horizontal swipe for "previous/next period."

## Score → Contributors → Raw Data Stack

The dominant pattern from Whoop, Oura, Garmin:

```
Score (big number, color-coded)
  └── Top contributor ("HRV was 20% below baseline")
       └── Contributing factors (HRV, RHR, sleep, strain)
            └── Raw time series (full HRV chart)
```

Always show the score AND offer immediate decomposition. Score answers "how am I?"; decomposition answers "why?"; raw data answers "show me."
