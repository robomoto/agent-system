<!-- last_verified: 2026-03-14 -->
# Chart Types for Health Data

Chart type × health metric selection guide. Rates each as tried-and-true, experimental, or skip.

## Selection Matrix

| Chart Type | Daily Glance | Weekly Review | Monthly/Yearly | Complexity | Rating |
|-----------|:---:|:---:|:---:|:---:|:---:|
| Sparklines | ✅ | ✅ | — | Low | **Tried & true** |
| Bullet charts | ✅ | — | — | Low | **Tried & true** |
| Horizontal progress bars | ✅ | — | — | Low | **Tried & true** |
| Stacked bar (sleep stages) | ✅ | — | — | Low | **Tried & true** |
| Small multiples | — | ✅ | ✅ | Medium | **Tried & true** |
| Slope charts | — | ✅ | — | Low | **Tried & true** |
| Calendar heatmaps | — | — | ✅ | Medium | **Tried & true** |
| Waffle charts | ✅ | — | — | Low | **Tried & true** |
| Horizon charts | — | ✅ | ✅ | High | **Experimental** |
| Ridgeline plots | — | — | ✅ | High | **Experimental** |
| Radar/spider charts | — | — | — | Medium | **Skip** |
| Sankey diagrams | — | — | ✅ | High | **Experimental** |
| Bump charts | — | — | ✅ | Medium | **Experimental** |

## Tried & True — Details

### Sparklines
Tufte's invention. Tiny word-sized time-series inline with text/numbers. No axes, no labels, no gridlines. Optionally highlight first/last/min/max points. Every stat should optionally show a sparkline.

**Best for:** Inline trend context — "82 kg ↓ [tiny 30-day line]"
**Bad for:** Precise value reading, cross-metric comparison

### Bullet Charts (Stephen Few)
Horizontal bar (current value) + vertical marker (target) + background bands (qualitative ranges: deficient/adequate/optimal). Stacks vertically for multiple metrics.

**Health application:** Daily macros (protein: 140/160g with low/adequate/high bands), hydration, steps, sleep duration. Can encode body fat % with athletic/fit/average bands.
**Upgrade path:** If your dashboard has horizontal progress bars with targets, add qualitative range bands to make them proper bullet charts.

### Small Multiples (Tufte)
Same chart structure repeated across a grid, varying one dimension (e.g., one panel per week). Same axes, same scale across all panels. Label minimally.

**Health application:** Week-over-week sleep staging comparison, month-over-month weight trends, training volume by week.
**Limit:** >12 panels gets noisy. Best for weekly/monthly review.

### Calendar Heatmaps
Days-of-week on y-axis, weeks on x-axis. Color intensity maps to a single metric or goal completion %. Immediately reveals weekly patterns ("I always skip Sundays").

**Health application:** Workout frequency, nutrition compliance, sleep quality over months/year.
**Not for:** Daily dashboard or precise values.

### Slope Charts
Two vertical axes (Period A, Period B), lines connecting each metric's value. Crossing lines show which improved/declined.

**Health application:** This week's macro averages vs last week's. Body comp changes. Monthly review.
**Limit:** Only 2 periods. >8-10 lines gets cluttered.

### Waffle Charts
10×10 grid where filled squares represent percentages. More accurate for part-to-whole than pie charts (humans judge square areas better than wedge angles).

**Health application:** Macronutrient composition (protein/fat/carbs %). Sleep stage composition.
**Alternative to:** Pie/donut charts (superior for area perception).

## Experimental — Details

### Horizon Charts
Area chart sliced into bands at thresholds, layered with increasing color intensity. Compresses y-axis 4-8× while preserving patterns. Positive in one hue, negative in another.

**Health application:** Showing deviations from personal baselines — HR, HRV, weight, body temp. Color intensity = deviation magnitude.
**Barrier:** Requires user education. Consider for power-user view only.

### Ridgeline / Joy Plots
Overlapping density curves stacked vertically, each for a different time period. Shows how distributions change over time, not just averages.

**Health application:** Sleep duration distribution by day-of-week. HR distribution per workout type shifting over months (fitness visible as distribution shift).
**Barrier:** Unfamiliar to most users. Best for data review, not daily glance.

### Sankey Diagrams
Flow/allocation visualization. Width encodes quantity flowing between nodes.

**Health application:** Breakfast(600cal) + Lunch(800cal) + Dinner(700cal) → Protein + Fat + Carbs. Or: Total calories → BMR + Exercise + NEAT + TEF.
**Barrier:** Complex, overkill for daily use. Novel for nutrition analysis mode.

## Skip

### Radar / Spider Charts
Experts (Few, Tufte) actively recommend against. The enclosed polygon area is meaningless. Reordering axes produces completely different shapes from identical data. Polar-coordinate area perception is poor.

**Use instead:** Parallel coordinates, grouped dot charts, or a simple table with baseline comparison. These encode multi-dimensional profiles more accurately.
