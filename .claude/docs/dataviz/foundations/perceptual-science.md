# Perceptual Science for Visualization

How the human visual system processes marks on screen. Load for encoding decisions, layout design, and color selection.

## Pre-Attentive Processing

Certain visual features are detected in <200ms regardless of distractor count (Treisman, Feature Integration Theory, 1980; Healey & Enns, 1999).

**Pre-attentive features:**
- Color (hue) — a red dot among blue dots pops out instantly
- Orientation — a tilted line among verticals
- Size — a large circle among small circles
- Motion — a moving element among static ones
- Shape (limited — simple forms like circle vs square)

**Critical constraint:** Feature *conjunctions* are NOT pre-attentive. A red circle among red squares and blue circles requires slow serial search. Don't encode two independent variables using hue AND shape simultaneously — one won't pop.

**For dashboards:** Use a single pre-attentive feature to flag anomalies. If today's calorie count is dangerously low, make it a different hue — it pops from surrounding numbers. Don't try to encode "low AND trending down" with color AND an arrow simultaneously.

## Gestalt Principles

How the visual system groups elements (Wertheimer, Koffka, Köhler, 1920s; applied to viz by Colin Ware, *Information Visualization*, 4th ed, 2021):

| Principle | Effect | Viz application |
|-----------|--------|----------------|
| **Proximity** | Close elements → perceived group | Cluster related metrics |
| **Similarity** | Shared visual properties → group | Legend matching (same color = same category) |
| **Continuity** | Eye follows smooth lines | Line charts work because we perceive continuity |
| **Closure** | Mind completes incomplete shapes | Sparklines work without axes (brain infers frame) |
| **Enclosure** | Elements in shared boundary → group | Dashboard cards exploit this |
| **Connection** | Elements linked by line → strongly grouped | Slope charts, connected scatterplots |

**Strength ranking (Ware):** Connection > Enclosure > Proximity > Similarity

**For dashboards:** Group related metrics using proximity and enclosure (cards). Use similarity (shared color) to link the same metric across views. Use connection (lines) for temporal continuity.

## Color Perception

### Opponent Process Theory
After cone processing, signals organize into three opponent channels:
- Red-green
- Blue-yellow
- Black-white (luminance)

Red-green and blue-yellow provide maximum contrast (why diverging scales like red-white-blue work). Luminance channel processes finer spatial detail than chromatic channels — convey fine detail through lightness, not hue.

### Color Blindness
~8% of males, ~0.5% of females have color vision deficiency (primarily deuteranomaly/protanomaly — reduced red-green discrimination).

**Rules:**
- Never rely on red-green as sole distinguishing feature
- Pair hue with luminance variation — colorblind users can still distinguish light from dark
- Use blue-orange as the primary diverging palette
- Test with system color filters (macOS: System Preferences → Accessibility → Display → Color Filters)

### Perceptual Uniformity
A color scale is perceptually uniform if equal data steps produce equal perceived color differences. The rainbow/jet colormap is NOT uniform — it has artificial bands and luminance reversals.

**Use:** Viridis, magma, inferno (perceptually uniform, colorblind-safe). For categorical data: ColorBrewer qualitative palettes (Cynthia Brewer). For diverging data: ColorBrewer diverging palettes.

**Color spaces:** CIELAB and CIECAM02 model perceptual uniformity. When designing custom palettes, work in perceptual color space, not RGB/HSL.

## Working Memory and Cognitive Load

Miller's Law: ~7±2 items in short-term memory. For dashboard design, assume ~4 "chunks" can be held simultaneously (Cowan's revised estimate, 2001).

**Implications:**
- A dashboard with >6-8 metrics visible simultaneously will overwhelm
- Group related metrics into chunks (one card = one chunk)
- Use progressive disclosure to manage information density
- Composite scores reduce N metrics to 1 chunk (then decompose on demand)

## Change Blindness and Object Constancy

Humans fail to detect changes when there's no visual continuity between states (change blindness). Animation provides continuity — the viewer tracks the *same* element as it changes, avoiding change blindness.

**For dashboards:** When data updates or the user switches time periods, animate transitions (bars grow/shrink, lines redraw, points move). Keep animations 300-600ms with ease-out curves. The purpose is object constancy, not decoration.
