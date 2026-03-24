<!-- last_verified: 2026-03-14 -->
# Color Safety for Data Visualization

Colorblind-safe palettes, perceptual uniformity, and redundant encoding. Load for any task involving color decisions.

## The Problem

~8% of males and ~0.5% of females have color vision deficiency. Predominantly deuteranomaly (reduced green sensitivity) and protanomaly (reduced red sensitivity). In a health context, misinterpreting "danger" as "good" is genuinely harmful.

## Rule 1: Never Rely on Red-Green Alone

The standard health traffic light (red = bad, yellow = caution, green = good) fails for ~1 in 12 male users.

**Accessible alternative palette:**
- Positive: Blue (#0173B2)
- Warning: Orange (#DE8F05)
- Negative: Dark red (#D55E00) with pattern overlay or icon
- Neutral: Grey (#888888)

**Why blue-orange works:** Blue and orange are distinguishable across all common color vision deficiencies. They also have sufficient luminance contrast between them.

## Rule 2: Redundant Encoding

Never use color as the *sole* distinguishing feature. Always pair with at least one additional channel:

| Color encoding | Redundant pair |
|---------------|---------------|
| Status color (blue/orange/red) | + Icon (✓, ⚠, ✕) |
| Status color | + Text label ("Good," "Low," "Critical") |
| Category color | + Pattern (solid, dashed, dotted lines) |
| Heatmap intensity | + Text value in each cell |
| Alert background | + Border style or weight |

**Test:** Cover the color and ask "can I still tell these apart?" If not, add redundancy.

## Rule 3: Perceptual Uniformity for Sequential Data

A color scale is perceptually uniform if equal data steps produce equal perceived color differences.

**Bad:** Rainbow/jet colormap — artificial bands, luminance reversals, misleading patterns.

**Good sequential palettes (all colorblind-safe and perceptually uniform):**
- **Viridis** — Yellow to blue-green to deep purple. Best general-purpose sequential palette.
- **Magma** — Yellow to pink to dark purple. Good for dark backgrounds.
- **Inferno** — Yellow to orange to dark purple. High contrast.
- **Cividis** — Yellow to blue. Specifically optimized for deuteranopia.

**Source:** Developed by Stéfan van der Walt and Nathaniel Smith for matplotlib. Available in D3, Observable Plot, most viz libraries.

## Rule 4: Diverging Palettes for Baseline Deviation

When data centers on a meaningful midpoint (e.g., deviation from personal baseline):

- **Blue-White-Orange** — Blue for below baseline, white/light for at baseline, orange for above
- **Blue-White-Red** — Classic diverging. Works for most people but problematic for red-green deficiency. Use blue-orange instead.

**Important:** The center (zero/baseline) should be the lightest/most neutral color. Extremes should be the most saturated.

## Rule 5: Categorical Palettes

For distinct categories (e.g., protein/fat/carbs, different exercise types):

**ColorBrewer qualitative palettes** (Cynthia Brewer) — tested for distinguishability:
- **Set2** or **Dark2** — 8 colors, colorblind-safe
- Limit to ≤7 categories. Beyond 7, humans can't reliably distinguish colors.
- If >7 categories, use grouping + a legend, not more colors.

## Testing Tools

- **macOS:** System Preferences → Accessibility → Display → Color Filters (Protanopia, Deuteranopia, Tritanopia simulation)
- **Chrome DevTools:** Rendering panel → Emulate vision deficiency
- **Figma:** Vision Simulator plugin
- **Online:** Coblis (Color Blindness Simulator), Viz Palette (Susie Lu)
- **Automated:** axe-core, Lighthouse accessibility audit

## Minimum Contrast Requirements (WCAG 2.1)

| Element | Ratio required | Standard |
|---------|---------------|----------|
| Normal text (<18px) | 4.5:1 | AA |
| Large text (≥18px bold or ≥24px) | 3:1 | AA |
| UI components and graphical objects | 3:1 | AA |
| Chart data marks against background | 3:1 | AA (graphical objects) |

**Chart-specific:** Data marks (bars, lines, points) must have 3:1 contrast against their background. Adjacent data categories must be distinguishable — test with color vision simulations.

## Color for Health Dashboards Specifically

**Avoid anxiety-inducing palettes.** Aggressive red for "bad" metrics creates stress. Consider:
- Muted/desaturated tones for negative status instead of bright red
- Blue-purple range for "needs attention" (calm urgency)
- Save high-saturation colors for actionable alerts only

**Cultural considerations:** Red = danger is Western-centric. In some East Asian contexts, red = positive/lucky. For personal dashboards, let users customize the status color mapping.
