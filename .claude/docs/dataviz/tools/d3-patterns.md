<!-- last_verified: 2026-03-14 -->
# D3.js Patterns

Low-level visualization with D3. Load when custom/bespoke chart types are needed beyond what grammar libraries offer.

## When to Use D3 (vs Grammar Libraries)

Use D3 directly when you need:
- Custom chart types not supported by Vega-Lite/Plot (body map overlays, custom radial layouts)
- Fine-grained animation control (enter/update/exit transitions)
- Complex interaction beyond brushing/clicking (drag, force simulation)
- Integration with existing D3-based codebases
- Performance-critical SVG manipulation

Use grammar libraries (Vega-Lite, Plot) when:
- The chart type is standard (bar, line, scatter, heatmap, etc.)
- You want automatic scales/axes/legends
- The chart is agent-generated (JSON spec is easier to produce than D3 code)
- Speed of implementation matters more than customization

## D3 Core Concepts

### Selections and Data Binding
```javascript
d3.select("#chart").selectAll("rect")
  .data(dataset)
  .join("rect")
  .attr("x", d => xScale(d.date))
  .attr("y", d => yScale(d.value))
  .attr("width", xScale.bandwidth())
  .attr("height", d => height - yScale(d.value));
```

The `.join()` pattern (D3 v6+) replaces the older enter/update/exit boilerplate. It handles creation, updates, and removal in one call.

### Scales
D3 scales map data domains to visual ranges:

| Scale | Data → Visual |
|-------|--------------|
| `scaleLinear` | Continuous → continuous (calories → y position) |
| `scaleTime` | Date → continuous (date → x position) |
| `scaleBand` | Categorical → discrete bands (day names → bar positions) |
| `scaleOrdinal` | Categorical → discrete values (macro type → color) |
| `scaleSequential` | Continuous → color (deviation → blue intensity) |
| `scaleDiverging` | Continuous centered → two-color (baseline deviation → blue/orange) |

### Transitions
```javascript
bars.transition()
  .duration(500)
  .ease(d3.easeQuadOut)
  .attr("height", d => yScale(d.newValue));
```

D3 transitions interpolate between attribute values smoothly. Use `d3.easeQuadOut` for natural deceleration. Chain with `.on("end", callback)` for sequencing.

## Health-Relevant D3 Patterns

### Sparklines
Minimal line chart without axes:
- `d3.line()` with `d3.curveBasis` or `d3.curveMonotoneX` for smooth curves
- Tiny SVG: 80-120px wide, 20-30px tall
- Optional: highlight min/max/last points with small circles

### Bullet Charts
Stephen Few's bullet chart in D3:
- Background rects for qualitative ranges (3 bands of decreasing opacity)
- Thick rect for current value bar
- Thin vertical line for target marker
- Labels: metric name left, value right

### Calendar Heatmap
Grid of small rects, 7 rows (days) × N columns (weeks):
- `d3.scaleSequential(d3.interpolateBlues)` for intensity
- `d3.timeWeek` for column positioning
- Tooltip on hover for specific day data

### Body Map Overlay
SVG paths for muscle groups on a human silhouette:
- Each muscle group is a named SVG path
- Fill color mapped to "days since last trained" using sequential scale
- Hover/tap to show group name + last workout details

## D3 Version Notes

Current: **D3 v7** (2021+, ES modules). Key changes from older tutorials:
- `.join()` replaces `.enter().append()` pattern
- ES module imports: `import * as d3 from "d3"` or cherry-pick `import { select, scaleLinear } from "d3"`
- Most tutorials online still show v3/v4 patterns — verify against v7 API

## D3 + Observable Plot

D3 and Plot are complementary (both by Bostock):
- Use Plot for quick standard charts
- Drop into D3 for custom marks or complex interactions
- Plot's `Plot.marks` accepts custom mark functions that can use D3 internally
