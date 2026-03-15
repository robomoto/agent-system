# Experimental Chart Types & Approaches

Novel visualization techniques beyond standard charts. Load when exploring "what's possible."

## Radial / Circular Time Visualizations

Map time to angle — a 24-hour clock face where activities, sleep, eating windows, and energy levels are arcs or filled regions.

**Who does it:** Oura Body Clock, RISE (linear, not radial), research prototypes.
**Strengths:** Shows daily rhythm and pattern. Wrapping midnight-to-midnight reveals sleep/wake patterns that linear charts obscure. Multiple days as concentric rings.
**Weaknesses:** Humans read linear time better than circular. Area at outer ring disproportionately larger. Precise time reading harder.
**Best for:** Eating window visualization (intermittent fasting), sleep timing, activity distribution across day. Secondary view, not primary.

## Body Map Overlays

Human body silhouette with muscle groups colored/highlighted by training status (recently worked, recovery status, soreness).

**Who does it:** JEFIT, Hevy (basic). Research prototypes go further with heat-mapped recovery.
**Strengths:** Immediately answers "what should I train today?" Visceral and intuitive.
**Requirements:** Muscle-group-level tracking (exercise-to-muscle-group mappings). Recovery modeling per group is approximate.
**Implementation:** Even a simple "days since last trained" heatmap on a body outline is useful and achievable.

## Horizon Charts

Area chart sliced into bands at thresholds, bands layered with increasing color intensity. Compresses y-axis 4-8× while preserving patterns.

**How:** Values above baseline in one hue (e.g., blue bands of increasing intensity). Values below in another hue (e.g., orange). Each band represents one threshold increment.
**Best for:** Comparing many time series in minimal vertical space (5-10 metrics stacked). Deviation from personal baseline visualization.
**Barrier:** Unfamiliar to most users. Needs explanatory onboarding.
**Health use:** HR, HRV, weight, body temp deviations from rolling baseline. Color intensity = how far from normal.

## Ridgeline / Joy Plots

Overlapping density curves stacked vertically, each for a different time period or category. Named after Joy Division's *Unknown Pleasures* album cover.

**Best for:** How a metric's *distribution* changes over time (not just the average). Revealing bimodal patterns (e.g., Monday sleep is either great or terrible).
**Health use:** Sleep duration distribution by day-of-week. HR distribution per workout type shifting over months (fitness improvement visible as distribution shift).
**Barrier:** Requires familiarity with density plots. Best for data review mode.

## Sankey Diagrams

Flow/allocation visualization. Width of flows encodes quantity between nodes.

**Health use cases:**
- Meal → Macro allocation: Breakfast(600cal) + Lunch(800cal) + Dinner(700cal) → Protein(160g) + Fat(80g) + Carbs(250g)
- Energy balance: Total calories → BMR + Exercise + NEAT + TEF
**Barrier:** Complex, space-hungry. Novel for nutrition analysis mode, overkill for daily tracking.

## Bump Charts

Show ranking changes over time. Items connected by lines that cross as rankings shift.

**Health use:** Exercise type ranking by volume per week. Nutrient deficiency ranking over time. Which metrics are improving vs declining.
**Limit:** >8-10 items gets cluttered. Works for categorical ranking, not continuous data.

## Connected Scatterplots

A scatterplot where points are connected in temporal order, creating a trajectory through 2D space.

**Health use:** Weight (x) vs body fat % (y) over months — the trajectory shows recomposition. Sleep duration (x) vs HRV (y) over weeks — reveals the relationship's evolution.
**Strengths:** Shows two-variable relationships AND temporal direction simultaneously.
**Barrier:** Can be confusing if the trajectory crosses itself repeatedly.

## Micro-Interactions & Progressive Disclosure

Not a chart type but a design pattern for making complex viz accessible:

- **Hover/tap to reveal:** Detailed data point on interaction
- **Expand/collapse:** Cards that grow to show full charts
- **Drag to compare:** Pull two time periods side by side
- **Pinch to zoom:** Time axis navigation
- **Long press for context:** Annotation overlay

**Principle:** Every layer of interaction reveals one more level of detail. Never require interaction to understand the overview.

## Data Physicalization (Frontier)

Physical objects encoding data. Academic but worth tracking:

- **Squishicalization** (TU Vienna, 2024) — Elastic 3D-printed data sculptures where squishiness encodes density
- **Augmented Dynamic Data Physicalization** (TU Dresden, 2025) — Shape-changing sculptures + AR overlays
- **Tactile Charts** (U. Utah, 2026) — 3D-printed chart templates for blind/low-vision users
- **Dear Data postcards** — Analog "physicalization" (Lupi + Posavec)

**Timeline:** 3-5 years from consumer health application. Exception: Apple Watch haptics is already deployed haptic health feedback.

## Sonification (Data as Sound)

Mapping data values to audio properties. Research-stage:

- Natural sound mapping (bird songs, water) for data values — BLV user studies show effectiveness
- Screen reader + sonification hybrid for chart access
- Audio data narratives (narrated insights, ACM CHI)

**Health potential:** Heart rate → tempo; sleep stages → tonal shifts; activity levels → rhythm complexity. Speculative but grounded in accessibility research.
