<!-- last_verified: 2026-03-05 -->
# Pico CSS — Idioms

## Philosophy

Pico is classless-first: semantic HTML gets styled automatically. Pico styles `<article>`,
`<nav>`, `<button>`, `<table>`, `<input>`, `<details>` etc. directly via element selectors.
You write clean HTML, Pico makes it look good.

Customization is via CSS custom properties (`--pico-*`), not utility classes.
Theme switching uses `data-theme="light|dark"` on `<html>` (or per-element).

## Key CSS Variables

### Typography & Spacing

| Variable | Default | Controls |
|----------|---------|----------|
| `--pico-font-size` | `100%` (~16px) | Base font size for entire page |
| `--pico-line-height` | `1.6` | Base line height |
| `--pico-font-family` | system font stack | Body font |
| `--pico-typography-spacing-vertical` | `1.5rem` | Vertical space between text elements (p, h1-h6) |

### Block Elements (Cards, Articles)

| Variable | Default | Controls |
|----------|---------|----------|
| `--pico-block-spacing-vertical` | `1rem` | Vertical padding inside `<article>`, cards |
| `--pico-block-spacing-horizontal` | `1.25rem` | Horizontal padding inside `<article>`, cards |
| `--pico-border-radius` | `0.25rem` | Border radius on cards, inputs, buttons |

### Navigation

| Variable | Default | Controls |
|----------|---------|----------|
| `--pico-nav-element-spacing-vertical` | `1rem` | Vertical padding on nav items |
| `--pico-nav-element-spacing-horizontal` | `0.5rem` | Horizontal padding on nav items |

### Forms

| Variable | Default | Controls |
|----------|---------|----------|
| `--pico-form-element-spacing-vertical` | `0.75rem` | Vertical padding inside inputs, selects |
| `--pico-form-element-spacing-horizontal` | `1rem` | Horizontal padding inside inputs, selects |

### Colors

| Variable | Purpose |
|----------|---------|
| `--pico-background-color` | Page background |
| `--pico-card-background-color` | Article/card background |
| `--pico-card-sectioning-background-color` | Card header/footer background |
| `--pico-color` | Body text color |
| `--pico-muted-color` | Secondary/muted text |
| `--pico-muted-border-color` | Borders, dividers |
| `--pico-primary` | Primary action color (links, buttons) |
| `--pico-primary-hover` | Primary hover state |
| `--pico-primary-focus` | Primary focus ring (usually rgba with alpha) |
| `--pico-primary-inverse` | Text color on primary background |
| `--pico-secondary` | Secondary action color |
| `--pico-secondary-hover` | Secondary hover |
| `--pico-secondary-focus` | Secondary focus ring |
| `--pico-secondary-inverse` | Text on secondary background |

## Compact/Dense Layout Recipe

Pico defaults are generous (designed for docs/marketing). For apps, forums, dashboards,
reduce density with these tested overrides (from community discussion #482):

```css
:root {
    --pico-font-size: 93.75%;                        /* 15px base instead of 16px */
    --pico-line-height: 1.5;                         /* down from 1.6 */
    --pico-typography-spacing-vertical: 0.75rem;     /* tighter text rhythm */
    --pico-block-spacing-vertical: 0.75rem;          /* tighter card padding */
    --pico-block-spacing-horizontal: 1rem;           /* tighter horizontal padding */
    --pico-nav-element-spacing-vertical: 0.5rem;     /* tighter nav */
    --pico-nav-element-spacing-horizontal: 0.75rem;
    --pico-form-element-spacing-vertical: 0.5rem;    /* tighter form inputs */
    --pico-form-element-spacing-horizontal: 0.75rem;
}

/* Tighter heading scale to match */
h1 { font-size: 1.75rem; }
h2 { font-size: 1.35rem; }
h3 { font-size: 1.1rem; }
h4 { font-size: 1rem; }
```

For even more aggressive density (87.5% = 14px base), test carefully on mobile — touch
targets may fall below the 44px WCAG minimum.

## Theming — Coordinated Light/Dark

Always define both themes together. Dark mode often needs different primary colors
(lighter, for contrast against dark backgrounds).

```css
:root {
    /* Light theme */
    --pico-primary: #2d6a4f;
    --pico-background-color: #f8f6f3;
    --pico-color: #2c2c2c;
}

[data-theme="dark"] {
    /* Dark theme — brighter primary, warm surfaces */
    --pico-primary: #52b788;
    --pico-background-color: #1a1c1a;
    --pico-color: #e0ddd5;
}
```

Key principle: keep surface colors consistently warm or cool across both themes.
A warm green primary with cool blue-gray backgrounds looks uncoordinated.

## Color Workflow

1. **Explore** with [Realtime Colors](https://realtimecolors.com) — previews palette on
   real layouts, has light/dark toggle built in
2. **Generate shade ramps** with [Atmos.style](https://atmos.style/playground) — OKLCH-based,
   perceptually uniform lightness
3. **Validate contrast** — WCAG AA requires 4.5:1 for normal text, 3:1 for large text.
   Use browser devtools or [Paletton](https://paletton.com)
4. **Map to `--pico-*` variables** — export as CSS custom properties

## Component Patterns

| HTML | Pico renders as |
|------|----------------|
| `<article>` | Card with padding, border, shadow |
| `<nav>` | Flexbox bar with space-between |
| `<details>` | Accordion |
| `<dialog>` | Modal overlay |
| `a[role="button"]` | Full button styling on a link |
| `<progress>` | Styled progress bar |
| `<fieldset>` | Grouped form section |

## Container & Layout

```html
<main class="container">
  <!-- Centered, max-width content -->
</main>
```

Default max-width is ~1200px at large breakpoints. For text-heavy pages (forums, articles),
this creates uncomfortably long line lengths. Override per-page:

```css
.content-narrow { max-width: 48rem; }  /* ~768px, good for reading */
```

Or globally: `--pico-container-max-width: 900px;`
