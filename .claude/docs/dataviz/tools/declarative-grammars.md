<!-- last_verified: 2026-03-14 -->
# Declarative Visualization Grammars

Spec-based approaches to chart generation. Load for implementation and tool selection tasks.

## Why Declarative Grammars Matter for Agents

Declarative grammars separate *what* to show from *how* to render it. An agent produces a structured spec (JSON/Python); the renderer handles layout, scales, axes, and interaction. This is:
- **LLM-friendly** — Structured output maps directly to a spec
- **Validatable** — Draco design rules can check the spec against perceptual best practices
- **Portable** — Same spec can render in different contexts (web, mobile, static image)

## Vega-Lite (Dominik Moritz, Jeffrey Heer, Arvind Satyanarayan)

**What:** High-level declarative grammar for interactive visualization. JSON spec.
**Status:** Production, actively maintained. Widely used in research and industry.
**Maturity:** Proven.

**Core concepts:**
- `mark`: The geometry (bar, line, point, area, rect, arc, text)
- `encoding`: Maps data fields to visual channels (x, y, color, size, shape, opacity)
- `data`: Inline or URL-referenced dataset
- `transform`: Filter, aggregate, calculate, fold, window, bin
- `selection`: Interactive brushing, clicking, hovering
- `facet`: Small multiples (row, column, or wrapped)

**Strengths:** Concise specs for common chart types. Automatic scale/axis/legend generation. Built-in interaction primitives. JSON Schema for validation.

**Weaknesses:** Limited for highly custom layouts. Performance degrades with large datasets (use Mosaic for scale). Not designed for animation.

**Agent integration:** Ideal for "chart recommender" outputs. Agent generates a Vega-Lite JSON spec; renderer displays it. Draco can validate the spec before rendering.

## Observable Plot (Mike Bostock)

**What:** High-level JS charting library built on D3. Grammar-of-graphics-inspired API.
**Status:** Production, actively maintained as part of Observable Framework.
**Maturity:** Proven.

**Core concepts:**
- Marks: `Plot.barY()`, `Plot.line()`, `Plot.dot()`, `Plot.cell()`, `Plot.text()`, etc.
- Transforms: `Plot.binX()`, `Plot.groupX()`, `Plot.windowY()`, `Plot.normalizeY()`
- Faceting: `fx`, `fy` channels
- Scales: Auto-inferred from data, overridable
- Outputs: SVG (default), Canvas (opt-in for performance)

**Strengths:** Concise API for exploratory charting. Excellent defaults (auto axes, legends, colors). Faceting is first-class. Great for Observable Framework dashboards.

**Weaknesses:** Less flexible than raw D3 for custom layouts. Newer ecosystem (smaller community than D3 or Chart.js). SVG rendering limits scalability.

**vs Vega-Lite:** Plot is JS-native (functions, not JSON). Better for interactive notebooks and dashboards. Vega-Lite is better for agent-generated specs (JSON is easier to produce than JS code).

## Altair (Jake VanderPlas, Brian Granger — Python API for Vega-Lite)

**What:** Python library that generates Vega-Lite specs. "The Python data visualization library for statistical visualization."
**Status:** Production, actively maintained.
**Maturity:** Proven.

**Strengths:** Pythonic API for Vega-Lite. Integrates with pandas DataFrames. Jupyter-native rendering. `chart.save()` exports Vega-Lite JSON, HTML, PNG, SVG.

**Use case:** Python-side data processing → Altair chart → export Vega-Lite JSON → web renderer. Good for data pipeline → dashboard workflows.

## Draco (Dominik Moritz — ML-based Viz Recommendation)

**What:** A formal framework encoding visualization design knowledge as logical constraints. Can score and rank visualization designs.
**Status:** Research → early production.

**How it works:** Defines "soft constraints" (design preferences) and "hard constraints" (expressiveness requirements) as Answer Set Programming (ASP) rules. Given data characteristics, Draco searches for the highest-scoring valid design.

**Agent integration:** Use Draco to validate agent-generated Vega-Lite specs. "Is this encoding effective for this data type?" becomes a formal query.

## Grammar of Graphics Lineage

```
Wilkinson (1999, book) → Wickham/ggplot2 (2009, R) → Vega (2013, JSON)
                                                          ↓
                                                     Vega-Lite (2017, JSON)
                                                          ↓
                                                     Altair (2017, Python)
                                                     Observable Plot (2021, JS)
                                                     Draco (2019, validation)
```

All share the same conceptual model: data → aesthetic mappings → marks → scales → coordinates → facets.
