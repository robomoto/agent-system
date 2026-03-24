<!-- last_verified: 2026-03-14 -->
# Visual Encoding Theory

Core references for mapping data to visual channels. Load for every visualization question.

## Bertin's Retinal Variables (1967)

Jacques Bertin, *Sémiologie Graphique*. Identified the fundamental visual channels:

| Variable | Best for | Poor for |
|----------|----------|----------|
| **Position** (x, y) | Quantitative, ordinal | — (universally strong) |
| **Size** | Quantitative (approximate) | Nominal distinctions |
| **Shape** | Nominal (≤7 categories) | Quantitative, ordinal |
| **Value** (lightness) | Ordinal, sequential quantitative | Nominal with many categories |
| **Color** (hue) | Nominal distinctions | Ordered/quantitative data |
| **Orientation** | Nominal (limited) | Quantitative |
| **Texture** | Nominal (limited) | Quantitative |

**Key principle:** Match the variable type to the data type. Hue is *nominal* — use it for categories (protein vs fat vs carbs), not for ordered data (low → high). Position is *quantitative* — use it for continuous values.

## Cleveland & McGill Perception Hierarchy (1984)

Ranked by accuracy of human quantitative decoding (empirically validated, replicated by Heer & Bostock 2010):

1. **Position on a common scale** — most accurate (bar chart, dot plot, line chart)
2. **Position on non-aligned scales** — good (small multiples with independent axes)
3. **Length** — good (bar chart without common baseline)
4. **Tilt/angle/slope** — moderate (pie chart, slope chart)
5. **Area** — moderate (bubble chart, treemap)
6. **Luminance (lightness)** — moderate (choropleth, heatmap)
7. **Color saturation** — poor for precise reading
8. **Volume/curvature** — poor (3D charts almost always worse than 2D)

**Design rule:** Use the highest-ranked channel available for the primary comparison task. Reserve lower-ranked channels for secondary encodings.

**For categorical (nominal) data**, the ranking differs:
1. Spatial region (separate panels/axes)
2. Color hue (distinct colors for distinct categories)
3. Motion (effective but distracting)
4. Shape (limited to ~5-7 distinguishable shapes)

## Mackinlay's APT Framework (1986)

Formalized Bertin + Cleveland & McGill into automated design rules:

- **Expressiveness:** A visualization is expressive if it shows all the data and only the data (no visual artifacts implying nonexistent data).
- **Effectiveness:** A visualization is effective if it uses the most accurate visual channel for each data type.

Ancestor of Tableau's "Show Me" and Vega-Lite's encoding recommendations. For agent-generated charts, this framework lets you validate encoding choices mechanically.

## Munzner's Nested Model (2014)

Four levels, each validated differently:

| Level | Question | Validated by |
|-------|----------|-------------|
| 1. Domain situation | Who are the users? What are their goals? | Observation, interviews |
| 2. Data/task abstraction | What data types and tasks in viz terms? | User testing |
| 3. Visual encoding/interaction idiom | What chart type and interaction? | Perceptual principles |
| 4. Algorithm | How is it computed/rendered? | Performance benchmarks |

**A design can fail at any level.** A beautiful chart (L3) answering the wrong question (L2) is a failure. Apply this model systematically: start at L1 (who's looking at this and why?), work down.

## Wilkinson's Grammar of Graphics (1999)

Decomposes a chart into composable layers:

- **Data** — the dataset
- **Aesthetics** — mappings from data columns to visual properties (x, y, color, size)
- **Geometry** — mark type (point, line, bar, area)
- **Statistics** — transformations (bin, smooth, count)
- **Coordinates** — system (Cartesian, polar, geographic)
- **Facets** — small multiples (split by a variable)

Implemented by: ggplot2 (R), Vega-Lite (JSON), Altair (Python), Observable Plot (JS). This grammar is the foundation for agent-generated chart specs — describe data + aesthetics + geometry, and the renderer handles the rest.

## Stevens' Power Law — Perceptual Compression

Perceived magnitude = k × (physical intensity)^n

| Channel | Exponent (n) | Implication |
|---------|-------------|-------------|
| Length | ~1.0 | Perceived proportionally to actual (accurate) |
| Area | ~0.7 | Areas systematically underestimated |
| Brightness | ~0.5 | Brightness heavily compressed |

If encoding data as circle area (bubble chart), users will underestimate larger values. Consider Flannery correction (scale radius by ~0.57) for proportional symbols.

## Weber's Law — Just-Noticeable Differences

The minimum detectable difference is proportional to the base magnitude:

- **Length:** ~3-5% change needed to notice a difference
- **Area:** ~5-10% change needed
- **Brightness:** ~1-2% change needed

Implication: Use position/length when precise comparison matters. Area encodings (rings, bubbles) are fine for approximate "bigger/smaller" judgments.
