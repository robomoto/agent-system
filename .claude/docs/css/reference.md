<!-- last_verified: 2026-03-08 -->
# CSS Reference — Key APIs for Web Client Work

## Custom Properties API

```css
/* Declaration */
:root { --token-name: value; }

/* Usage with fallback */
.element { color: var(--token-name, #fallback); }

/* JS access */
document.documentElement.style.setProperty('--token-name', 'newValue');
getComputedStyle(element).getPropertyValue('--token-name');
```

## Viewport Units

| Unit | Meaning | Mobile behavior |
|------|---------|-----------------|
| `vh` | 1% of viewport height | Fixed to largest viewport (bar hidden) |
| `dvh` | Dynamic viewport height | Changes with address bar show/hide |
| `svh` | Small viewport height | Viewport with all chrome visible |
| `lvh` | Large viewport height | Viewport with all chrome hidden |
| `vw` | 1% of viewport width | Includes scrollbar on some browsers |

## Media Queries

```css
/* Responsive breakpoints (mobile-first) */
@media (min-width: 481px) { /* tablet+ */ }
@media (min-width: 769px) { /* desktop+ */ }

/* User preferences */
@media (prefers-reduced-motion: reduce) { }
@media (prefers-color-scheme: dark) { }
@media (prefers-contrast: more) { }

/* Interaction */
@media (hover: hover) { /* device has hover capability */ }
@media (pointer: coarse) { /* touch device */ }
```

## Safe Area Environment Variables

```css
env(safe-area-inset-top)
env(safe-area-inset-right)
env(safe-area-inset-bottom)
env(safe-area-inset-left)
```

Requires `viewport-fit=cover` in meta tag. Returns `0` otherwise.

## Flexbox Quick Reference

```css
.container {
  display: flex;
  flex-direction: row | column;
  justify-content: flex-start | center | space-between | space-around;
  align-items: stretch | center | flex-start | flex-end;
  gap: 8px;
  flex-wrap: wrap;
}
.child {
  flex: 1;            /* grow to fill */
  flex: 0 0 auto;     /* don't grow or shrink */
  align-self: center; /* override parent's align-items */
}
```

## Grid Quick Reference

```css
.container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
```

## Keyframe Animations

```css
@keyframes name {
  0% { transform: scale(0.5); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.element {
  animation: name 400ms ease-out;
  animation: name 400ms ease-out forwards; /* keeps final state */
  animation: name 2s ease-in-out infinite; /* loops */
}
```

## Transitions

```css
.element {
  transition: property duration timing-function delay;
  transition: transform 200ms ease, opacity 200ms ease;
  transition: all 200ms ease; /* avoid in production -- too broad */
}
```

## Position Types

| Value | Behavior | Scroll | z-index |
|-------|----------|--------|---------|
| `static` | Normal flow | Scrolls with page | Ignored |
| `relative` | Flow + offset | Scrolls with page | Works |
| `absolute` | Relative to positioned ancestor | Scrolls with ancestor | Works |
| `fixed` | Relative to viewport | Does not scroll | Works |
| `sticky` | Flow until threshold, then fixed | Context-dependent | Works |

## Selector Specificity

| Selector | Specificity |
|----------|-------------|
| `*` | 0,0,0 |
| `div` | 0,0,1 |
| `.class` | 0,1,0 |
| `#id` | 1,0,0 |
| `[data-theme="x"]` | 0,1,0 (same as class) |
| `:root` | 0,1,0 (pseudo-class) |
| Inline style | 1,0,0,0 |

## WCAG Contrast Requirements

| Text size | Minimum ratio (AA) | Enhanced (AAA) |
|-----------|-------------------|----------------|
| Normal (<18px bold, <24px) | 4.5:1 | 7:1 |
| Large (>=18px bold, >=24px) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | N/A |

## Touch Target Sizing

WCAG 2.5.8 (Target Size): interactive elements should be at least 24x24px (AA), ideally 44x44px (AAA / Apple HIG).

```css
button, a, input {
  min-height: 44px;
  min-width: 44px;
}
```
