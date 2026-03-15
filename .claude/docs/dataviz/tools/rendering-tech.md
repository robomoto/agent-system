# Rendering Technologies for Visualization

SVG vs Canvas vs WebGL selection guide. Load for performance and implementation decisions.

## Technology Comparison

| Technology | Best for | Limits | Interactivity |
|-----------|---------|--------|---------------|
| **SVG** | <1,000 elements, styled charts, accessibility | DOM overhead at scale | Native (CSS hover, click events per element) |
| **Canvas** | 1,000-100,000 elements, animations | No DOM = manual hit detection | Manual (track mouse position, calculate which element) |
| **WebGL** | >100,000 elements, 3D, GPU-accelerated | Steep learning curve, no text rendering | Manual (picking shaders or overlay DOM) |
| **WebGPU** | Emerging successor to WebGL | Limited browser support (2025: Chrome, Edge) | Same as WebGL |

## Performance Crossover Points

**Rules of thumb:**
- <500 data points: SVG (simpler development, full CSS/DOM features)
- 500-5,000: SVG with virtualization, or Canvas for animations
- 5,000-100,000: Canvas (2D context for charts, OffscreenCanvas for workers)
- >100,000: WebGL (Deck.gl, Regl, Three.js)

**For personal health dashboards:** SVG is almost always sufficient. A year of daily data = 365 points. Even a year of hourly data = 8,760 points — Canvas handles this easily but SVG can manage with careful rendering.

## SVG Details

**Strengths:**
- DOM-based: every element is selectable, styleable, inspectable
- Native CSS: hover states, transitions, responsive sizing
- Accessibility: `<title>`, `<desc>`, ARIA attributes per element
- Screen reader compatible with proper labeling
- Resolution-independent (vector)

**Weaknesses:**
- Each element is a DOM node → performance degrades >1,000 elements
- Complex animations require many reflows
- Large SVGs increase page weight

**Best practice:** Use SVG for all standard health dashboard charts. Only switch to Canvas for high-frequency data (continuous glucose, second-by-second HR).

## Canvas Details

**Strengths:**
- Single DOM element regardless of data size
- Pixel-based rendering is fast for many elements
- Good animation performance (requestAnimationFrame loop)
- OffscreenCanvas for web worker rendering

**Weaknesses:**
- No built-in interactivity (must implement hit detection)
- No accessibility without a parallel hidden DOM
- Rasterized (blurry on zoom without redraw)

**Hybrid approach:** Render the chart on Canvas; overlay a thin SVG layer for interactive elements (tooltips, annotations, hover zones). Chart.js uses this pattern.

## WebGL / GPU-Accelerated

**Frameworks:**
- **Deck.gl** — Geospatial + large dataset visualization. Layer-based architecture.
- **Regl** — Lightweight WebGL wrapper. Good for custom shaders.
- **Three.js** — 3D scenes. Overkill for 2D charts but useful for data physicalization mockups.
- **PixiJS** — 2D GPU-accelerated rendering. Game-engine approach to viz.

**When needed for health data:** GPS-tracked exercise routes on maps (Deck.gl), continuous wearable data streams with 100K+ points, 3D body composition models.

## Mosaic + DuckDB (Scalable Interactive Viz)

Architecture from Heer + Moritz (Best Demo, SIGMOD 2025):
- **DuckDB** runs in-browser (WASM) as the query engine
- **Mosaic** links database queries to interactive visualizations
- Cross-filtering and brushing work at scale because the database handles aggregation, not the renderer

**Relevance:** If your health data grows large (years of minute-level data from wearables), Mosaic's architecture lets you query and visualize without loading everything into memory. The browser becomes a thin rendering layer over a local database.

## Framework Comparison for Health Dashboards

| Framework | Level | Rendering | Best for |
|-----------|-------|-----------|----------|
| **Observable Plot** | High-level grammar | SVG | Quick standard charts, dashboards |
| **Vega-Lite** | High-level grammar | SVG/Canvas | Agent-generated charts, validation |
| **Chart.js** | Mid-level library | Canvas | Existing codebases, quick setup |
| **D3.js** | Low-level toolkit | SVG/Canvas | Custom chart types, fine control |
| **Recharts** | React wrapper | SVG | React apps, standard charts |
| **visx** (Airbnb) | React + D3 primitives | SVG | React apps needing D3-level control |
| **Nivo** | React wrapper | SVG/Canvas | React apps, rich chart gallery |
| **ECharts** | Mid-level library | Canvas/SVG | Large datasets, rich interactions |
| **Deck.gl** | WebGL framework | WebGL | Maps, large datasets |

**Recommendation for a new health dashboard:** Start with Observable Plot or Vega-Lite for standard charts. Drop to D3 for custom types (body map, radial time). Use Canvas only if performance demands it.
