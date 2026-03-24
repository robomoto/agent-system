<!-- last_verified: 2026-03-05 -->
# Pico CSS — Footguns

## Global Button Styling Conflict

Pico styles ALL `<button>` elements globally via element selectors. This breaks
third-party widgets (FullCalendar, date pickers, rich text editors, map controls)
whose buttons inherit Pico's padding, border-radius, and background.

**Symptoms:** Widget buttons look like form controls, checkboxes, or oversized pills.

**Fix:** Override with the widget's class prefix for higher specificity:
```css
.fc .fc-button { /* FullCalendar */ }
.ql-toolbar button { /* Quill editor */ }
.mapboxgl-ctrl button { /* Mapbox */ }
```

Element selectors (Pico) lose to class selectors (your overrides) automatically.

## Dark Mode Color Mismatch

If you only customize `--pico-primary` in `:root` without adding a `[data-theme="dark"]`
block, dark mode inherits Pico's default cool blue-gray surfaces (`#11191f` background)
with your custom primary color.

Warm primary + cool background = visual clash.

**Fix:** Always define both themes together:
```css
:root { --pico-primary: #2d6a4f; --pico-background-color: #f8f6f3; }
[data-theme="dark"] { --pico-primary: #52b788; --pico-background-color: #1a1c1a; }
```

## Article Padding in Lists

Every `<article>` gets generous Pico padding (~1rem vertical, ~1.25rem horizontal)
plus margin-bottom. In list views (channels, threads, search results), this creates
low information density — only 3-4 items fit per viewport.

**Fix options:**
1. Use a custom class to reduce padding: `.compact-card { --pico-block-spacing-vertical: 0.5rem; }`
2. Avoid `<article>` for list items — use `<div>` with custom styling instead
3. Reduce Pico's default spacing globally (see compact layout recipe in idioms.md)

**Benchmark:** Forum/channel list should show 8+ items per 1080p viewport without scrolling.

## role="button" Surprise

Adding `role="button"` to an `<a>` tag makes Pico render it as a full button — padded,
bordered, block-level on mobile. This is by design but often overkill.

```html
<!-- Renders as a FULL BUTTON — often too prominent for secondary actions -->
<a href="/manage" role="button" class="outline">Manage</a>

<!-- Renders as a normal link — appropriate for secondary navigation -->
<a href="/manage">Manage &rsaquo;</a>
```

**Rule of thumb:** Reserve `role="button"` for primary page actions. Use plain `<a>` for
secondary navigation. Removing `role="button"` is also more semantically correct for
links that navigate to a new page.

## Container Width for Text

Default container max-width is ~1200px. For body text, optimal line length is 60-80
characters (~600-700px). At 1200px, text is hard to track across the line.

**Fix:** Add a narrower content wrapper for text-heavy pages:
```css
.content-narrow { max-width: 48rem; margin: 0 auto; }
```

Or reduce the global container: `--pico-container-max-width: 900px;`

## Form Element Sizing

Pico form elements are large by default (generous padding for touch targets). For
desktop-optimized UIs, override spacing variables:

```css
:root {
    --pico-form-element-spacing-vertical: 0.5rem;
    --pico-form-element-spacing-horizontal: 0.75rem;
}
```

**Warning:** Don't go below 44px total element height on mobile (WCAG 2.1 AA touch
target minimum). Test with mobile device inspector.

## filter: invert(1) for Dark Mode Images

Using `filter: invert(1)` to flip logos/icons in dark mode is fragile:
- It inverts ALL colors — a green logo becomes magenta
- Semi-transparent areas produce unexpected results
- Photos/complex images look completely wrong

**Better alternatives:**
1. Separate dark-mode asset: `[data-theme="dark"] .logo { content: url('logo-dark.png'); }`
2. For monochrome icons: `filter: brightness(0) invert(1)` (forces white)
3. CSS `mask-image` with `currentColor` (icon inherits text color automatically)
4. SVG with `fill: currentColor` (best option for icons)

## Specificity

Pico uses low-specificity selectors (element selectors like `button`, `a`, `article`).
Custom classes easily override Pico without needing `!important`.

```css
/* This naturally beats Pico's `article { padding: ... }` */
.compact-card { padding: 0.5rem; }
```

**Avoid `!important`** — it's almost never needed with Pico and creates maintenance debt.
If you think you need it, check for a more specific selector first.

## Heading Scale

Pico's default headings are large (h1 ~2rem, h2 ~1.75rem). On content-dense pages
(forums, dashboards), this wastes vertical space.

Override with a tighter scale:
```css
h1 { font-size: 1.75rem; }
h2 { font-size: 1.35rem; }
h3 { font-size: 1.1rem; }
h4 { font-size: 1rem; }
```

Pairs with the compact layout recipe in idioms.md.
