# Non-Visual Data Access

Screen readers, sonification, and tactile approaches for chart accessibility. Load for accessibility reviews.

## Screen Reader Support for Charts

### ARIA for Data Visualization

**Minimum viable accessibility:**
```html
<svg role="img" aria-label="Weight trend over 30 days, currently 82.1kg, trending down 0.4kg">
  <title>Weight Trend: 30 Days</title>
  <desc>Line chart showing daily weight from Feb 12 to Mar 14. 
        Weight decreased from 82.5kg to 82.1kg with normal daily fluctuation.</desc>
  <!-- chart elements -->
</svg>
```

**Key ARIA attributes for charts:**
- `role="img"` on `<svg>` — announces as a single image
- `aria-label` — concise summary (what the chart shows + key takeaway)
- `<title>` — chart title (announced by some screen readers)
- `<desc>` — detailed description of trends and patterns

### Rich Screen Reader Experiences (UW Interactive Data Lab)

Three dimensions for chart accessibility:
1. **Structure** — Describe the chart type, axes, and data structure
2. **Navigation** — Let users explore chart entities at varying granularities (overview → trend → individual points)
3. **Description** — Auto-generate text descriptions of patterns and outliers

**Implementation pattern:**
- Hidden data table behind the chart (screen readers can navigate table cells)
- Keyboard navigation: arrow keys to move between data points, Enter to hear detail
- Announce trends and anomalies, not just individual values

### WCAG 2.1 Requirements for Interactive Charts

| Requirement | Spec | Implementation |
|------------|------|---------------|
| Min font size | 16px | All chart labels, tooltips, values |
| Touch target | 44×44px | Tappable areas on data points, controls |
| ARIA attributes | role, label, describedby | All interactive elements |
| Keyboard navigation | Tab + arrows | All interactive features accessible without mouse |
| Live regions | aria-live="polite" | Announce dynamic updates (new data, filter changes) |
| Focus indicators | Visible focus ring | 2px+ contrasting border on focused elements |
| Alternative text | For all non-decorative images | Summary + detail for every chart |

## Sonification (Data as Sound)

### Approaches

**Pitch mapping:** Map data values to musical pitch. Higher values = higher pitch. Works well for single time series — the "shape" of the melody mirrors the shape of the line chart.

**Natural sound mapping:** Map values to ambient sounds (bird songs, water flow). User studies with blind/low-vision users show effectiveness. More pleasant for extended listening than pure tones.

**Rhythm mapping:** Map categories or time intervals to rhythm patterns. Activity levels → rhythm complexity (rest = slow pulse, exercise = fast complex rhythm).

**Screen reader + sonification hybrid:** Combine spoken structure ("this is a bar chart of your weekly calories") with sonified data (ascending tones for each day's value). Provides both context and data.

### Health-Specific Sonification Potential

| Data | Sound mapping | Feasibility |
|------|--------------|-------------|
| Heart rate trend | Pulse tempo | Natural and intuitive |
| Sleep stages | Tonal shifts (deep=low, REM=mid, light=high) | Experimental |
| Activity level | Rhythm complexity | Experimental |
| Weight trend | Ascending/descending pitch | Standard |
| Goal completion | Chime vs silence for each metric | Simple |

**Maturity:** Research-stage for health. No consumer products offer data sonification for health dashboards. Opportunity for differentiation + accessibility.

## Tactile Charts (University of Utah, IEEE TVCG 2026)

3D-printed chart templates for blind/low-vision (BLV) users:
- UpSet plots, violin plots, heatmaps as raised-surface templates
- Study with 12 BLV participants: tactile models were preferred learning method
- Consumer 3D printers can produce templates from chart data

**Health relevance:** 3D-printed weekly activity heatmaps or body composition distributions as physical objects. Mostly relevant for BLV users, but also interesting as data physicalization.

## Audio Data Narratives (ACM CHI)

Narrated data insights for non-visual consumption. Structure:
1. Context: "Here's your weekly health summary"
2. Highlights: "Sleep was your strongest metric this week at 92%"
3. Concerns: "Protein fell below target 4 out of 7 days"
4. Trend: "Your weight has been stable over the past 3 weeks"
5. Suggestion: "Consider adding a protein-rich snack to close the gap"

**Implementation:** LLM generates narrative from data; text-to-speech delivers it. Could integrate with morning routine (smart speaker, notification).

## Practical Accessibility Checklist for Health Dashboards

1. [ ] Every chart has `role="img"`, `aria-label`, `<title>`, and `<desc>`
2. [ ] Hidden data table behind each chart for screen reader navigation
3. [ ] All interactive elements reachable via keyboard (Tab + Arrow keys)
4. [ ] Focus indicators visible (2px+ contrasting ring)
5. [ ] Touch targets ≥44×44px on mobile
6. [ ] Font size ≥16px for all chart text
7. [ ] Color never sole distinguishing feature (redundant encoding)
8. [ ] All color combinations pass 3:1 contrast for graphical objects
9. [ ] `aria-live="polite"` on dynamic content areas
10. [ ] `prefers-reduced-motion` respected (disable animations when set)
11. [ ] Alternative text summaries include trends and key takeaways, not just "chart of weight data"
