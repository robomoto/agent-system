# Animation & Interaction for Data Visualization

When and how to use motion and interaction in dashboards. Load for interaction design and transition questions.

## When Animation Helps

- **Transitioning between time periods:** Bars morph into aggregated bars (day → week)
- **Data refresh:** New data points slide in from the right edge of a line chart
- **Score changes:** Number counter animates from old value to new
- **Progressive disclosure:** Cards expand/collapse smoothly
- **Object constancy:** Tracking the same data element as it changes position/size

**The science:** Animation provides visual continuity between states, preventing change blindness (failure to detect differences without continuity). Object constancy — the viewer tracking a persistent element through transformation — is the key benefit.

## When Animation Hurts

- Decorative spin/bounce on load (meaningless motion)
- Long transitions (>800ms) that delay comprehension
- Animation that blocks interaction (user must wait)
- Too many elements animating simultaneously (can't track any of them)
- Color changes for status updates (should be instant, not transitioned)

## Timing Guidelines

| Duration | Use for |
|----------|---------|
| 150-200ms | Hover state changes, tooltips appearing |
| 300-400ms | Card expand/collapse, panel transitions |
| 400-600ms | Chart data transitions, bar growth, line redraw |
| 600-800ms | Complex multi-element transitions (small multiples reorganizing) |
| >800ms | Almost never — feels sluggish |

**Easing:** Use ease-out (fast start, slow finish) for elements entering. Use ease-in (slow start, fast finish) for elements leaving. Linear feels mechanical.

**Rule of thumb:** Animate position and size to show what changed. Don't animate color for status (instant change communicates urgency better).

## Progressive Disclosure Layers

The architectural pattern for managing information density through interaction:

| Layer | Content | Interaction | Time to comprehend |
|-------|---------|------------|-------------------|
| L0: Glanceable | Scores + status color + sparkline direction | None (passive) | <3s |
| L1: Summary | Score + top contributors + trend | Tap/click card | 10-15s |
| L2: Detail | Full charts, raw data, history | Scroll within expanded card | 30s+ |
| L3: Analysis | Correlations, distributions, comparisons | Filter, zoom, annotate | Minutes |

**Implementation pattern:**
- Default: L0 for all metrics
- Click card → expand to L1 (other cards collapse or dim)
- Click "show chart" within L1 → expand to L2
- Dedicated "review" or "analysis" route for L3

**Who does it well:** Whoop (daily orb → score → metrics → raw data). RISE (debt number → energy curve → stages → habits).
**Who does it poorly:** Garmin (everything L2 simultaneously). Apple Health (inconsistent level transitions).

## Scrollytelling for Health Narratives

From data journalism: narrative unfolds as user scrolls, visualization updates in sync.

**Health application:** Weekly/monthly review experience. As user scrolls:
1. "This week at a glance" → summary scores
2. "Your nutrition" → macro charts animate in
3. "Sleep patterns" → hypnogram appears
4. "How they connect" → cross-domain correlation highlights
5. "What to focus on next week" → actionable recommendations

**Frameworks:** Scrollama (Russell Goldenberg), Intersection Observer API (native).
**Key principle:** Each scroll step makes exactly one change to the visualization. Multiple simultaneous changes overwhelm.

## Direct Manipulation Interactions

Shneiderman's dynamic queries applied to health data:

- **Time range slider:** Drag to select a date range; all charts update in real-time
- **Metric toggle:** Show/hide specific metrics on shared time axis
- **Threshold drag:** Drag the target line on a bullet chart to adjust goals
- **Brush selection:** Highlight a region of one chart; corresponding points highlight in other charts (cross-filtering)
- **Annotation tap:** Tap a point to add/read a note

**Performance requirement:** <100ms response to user input for direct manipulation to feel "direct." Pre-compute or use progressive rendering for larger datasets.

## Responsive Visualization

Health dashboards are primarily mobile. Adaptation patterns:

| Element | Desktop | Mobile |
|---------|---------|--------|
| Tooltip | Hover | Long press |
| Multi-chart view | Side by side | Stacked/swipeable |
| Time navigation | Slider + buttons | Pinch zoom + swipe |
| Data tables | Full table | Collapsed accordion |
| Annotations | Inline labels | Icon markers (tap to expand) |

**Key constraint:** Thumb zone. Primary interactions in the bottom 40% of screen. Score cards and navigation at thumb reach; detailed charts scroll into view.
