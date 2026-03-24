<!-- last_verified: 2026-03-14 -->
# Uncertainty Visualization

How to communicate uncertainty, variability, and confidence in health data. Load for any task involving ranges, predictions, or biological variability.

## Why Uncertainty Matters for Health Data

Every health metric has uncertainty:
- **Device accuracy:** Wrist-based HR ±5-10%, scale weight ±0.1-0.5kg, sleep staging is approximate
- **Biological variability:** Daily weight fluctuates 1-3kg from hydration/food; HRV varies 20-40% day-to-day even when healthy
- **Prediction confidence:** Trend extrapolations become less certain further out

Showing a single number without uncertainty context leads to:
- Anxiety from normal fluctuations ("my weight went up 0.5kg!")
- False confidence in predictions
- Misattribution of noise to causes ("I ate bread and gained 2 pounds")

## Lace Padilla — Frequency Framing (VGTC 2025 Award)

**Key finding:** Frequency framing dramatically improves comprehension of uncertain data.

**What it means:** Instead of probability statements, use count-based phrasing:
- Bad: "There's a 30% chance you'll exceed your calorie target"
- Good: "3 out of 10 days this month, you exceeded your calorie target"
- Bad: "Your weight has a 70% probability of being between 80-82kg next week"
- Good: "7 out of 10 weeks, your weight stays within this range"

**Why it works:** Humans intuitively understand frequencies (counts of events) better than probabilities (abstract ratios). This is consistent with evolutionary psychology — our ancestors tracked "how often" not "what percentage."

**Application to health dashboards:**
- Express adherence as "X out of Y days" not percentages
- Show prediction ranges as "most weeks you're within this band"
- Use icon arrays (10 person icons, 3 highlighted) for visual frequency framing

## Visual Uncertainty Encodings

### Confidence Bands (Tried & True)
Shaded region around a trend line showing the confidence interval. Width encodes uncertainty.

**Use for:** Weight trend projections, fitness trajectory, sleep quality trend.
**Implementation:** Two area fills (light shade for 95% CI, darker for 50% CI) behind the trend line.
**Pitfall:** Users often interpret the band as "noise" and ignore it. Add a text label: "Your weight is likely to be in this range."

### Error Bars (Tried & True)
Vertical lines showing range at each data point.

**Use for:** Metric comparisons (this week's average vs last week's), when showing discrete summary statistics.
**Pitfall:** Users don't know if error bars show standard deviation, standard error, or confidence interval. Always label.

### Gradient/Blur Encodings (Experimental)
Instead of sharp confidence bands, use opacity gradient that fades with distance from the central estimate. Intuitively communicates "less certain further out."

**Status:** Research. Padilla's work suggests this can be effective but needs careful calibration.

### Hypothetical Outcome Plots / HOPs (Experimental)
Animated sequence of possible outcomes drawn from the distribution. Each frame shows one plausible scenario.

**Use for:** Communicating prediction uncertainty when static bands are insufficient.
**Implementation:** Cycle through 20-50 draws from the posterior distribution at ~200ms per frame.
**Status:** Research (Hullman, Kay). Effective in studies but computationally heavier.

## Progressive Visualization (IEEE TVCG 2024 Survey)

Comprehensive taxonomy of progressive visualization approaches. Key properties:
- **Uncertainty:** Show how confident the current view is
- **Steering:** Let users guide which part of the data is refined first
- **Visual stability:** Avoid jarring changes as data loads
- **Real-time processing:** Stream results as they compute

**Health application:** When loading a year of data, show the trend immediately (approximate) and refine details progressively. The user sees something useful within 200ms even if full rendering takes 2 seconds.

## Practical Guidelines for Health Dashboards

1. **Always show the trend, not just the point.** A single weight reading is noise. A 14-day rolling average is signal.
2. **Show the baseline band.** Rolling mean ± 1σ as a shaded region. Data inside the band = normal. Data outside = noteworthy.
3. **Use frequency framing for goals.** "You hit your protein target 5 out of 7 days" not "71% adherence."
4. **Label the uncertainty.** "Based on your last 30 days" or "Within normal daily variation" next to any range display.
5. **Don't suppress noise — contextualize it.** Show daily weight AND the trend line. The daily points show the data; the trend shows the signal. Users learn to distinguish them.
