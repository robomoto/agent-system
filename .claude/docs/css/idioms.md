# CSS Idioms (Modern CSS, 2023+)

## 1. Design Tokens via Custom Properties

```css
:root {
  --color-background: #0F1923;
  --color-surface: #1C2B3A;
  --color-on-surface: #E8EDF2;
  --color-primary: #7EB8D4;
  --space-sm: 8px;
  --space-md: 12px;
  --radius-md: 8px;
}
```

Use semantic names (`--color-on-surface`) not raw values. Components reference tokens, never hardcode colors.

## 2. Theme Switching with Data Attributes

```css
/* Default theme on :root */
:root { --color-background: #0F1923; }

/* Theme overrides -- only redeclare changed values */
[data-theme="arcane"] { --color-background: #12091F; }
[data-theme="forest"] { --color-background: #0A1A12; }
```

JS: `document.documentElement.setAttribute('data-theme', 'arcane');`

Custom properties cascade, so child elements automatically pick up overrides.

## 3. Color Scheme Declaration

```css
html { color-scheme: dark; }
```

Tells the browser to use dark scrollbars, form controls, and selection colors natively. Set `dark light` if you support both.

## 4. Mobile-First Responsive

```css
/* Base: mobile styles (no media query) */
.container { padding: 16px; }

/* Enhancement: larger screens */
@media (min-width: 481px) {
  .container { max-width: 480px; margin: 0 auto; }
}
```

Always use `min-width` for mobile-first. Never use `max-width` unless specifically targeting small screens only.

## 5. Safe Area Insets (iOS)

```css
.sticky-bar {
  padding-bottom: max(12px, env(safe-area-inset-bottom));
}
```

Required for `position: fixed` elements on iOS to avoid the home indicator. Requires `<meta name="viewport" content="viewport-fit=cover">`.

## 6. Dynamic Viewport Units

```css
body { min-height: 100dvh; }  /* dvh = dynamic viewport height */
```

`dvh` accounts for mobile browser chrome (address bar show/hide). `svh` = smallest (chrome visible), `lvh` = largest (chrome hidden). Prefer `dvh` for full-height layouts.

## 7. Focus Styles

```css
/* Remove default, add custom */
:focus { outline: none; }
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

`:focus-visible` only shows for keyboard navigation, not mouse clicks. Always provide visible focus for accessibility.

## 8. Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Place at the end of your animation stylesheet. WCAG 2.1 SC 2.3.3 requires respecting this preference.

## 9. GPU-Composited Animations

```css
/* GOOD: composited (transform, opacity) -- runs on GPU */
.card { transition: transform 200ms ease, opacity 200ms ease; }

/* BAD: triggers layout (width, height, top, left) -- janky */
.card { transition: width 200ms ease; }
```

Only `transform` and `opacity` are reliably GPU-composited. Use `will-change: transform` sparingly as a hint.

## 10. BEM-ish Naming

```css
.roll-card { }                    /* Block */
.roll-card__total { }             /* Element */
.roll-card--nat20 { }             /* Modifier */
.roll-card__total--revealing { }  /* Element + modifier */
```

Flat selectors, no nesting depth. Each class is self-documenting.

## 11. Logical Properties

```css
/* Prefer logical over physical for internationalization */
.card { margin-inline: auto; padding-block: 16px; }
/* Instead of: margin-left/right, padding-top/bottom */
```

## 12. Reset / Normalize Pattern

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html { -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
img, picture, video { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
```

Minimal reset -- only override what causes cross-browser inconsistency.

## 13. Sticky Positioning

```css
.header { position: sticky; top: 0; z-index: 10; }
```

Sticky requires a scroll container ancestor. Unlike `position: fixed`, it stays in flow.

## 14. Custom Property Fallbacks

```css
.card {
  background: var(--color-surface, #1C2B3A); /* fallback if unset */
}
```

Always provide a fallback for tokens that themes might not define.

## 15. Container Queries (Progressive Enhancement)

```css
@container (min-width: 400px) {
  .card { flex-direction: row; }
}
```

Container queries scope responsive styles to the parent container, not the viewport. Supported in all modern browsers (2023+).
