# CSS Footguns

## 1. iOS Safari `position: fixed` in Scrollable Contexts

`position: fixed` elements can jump or disappear when the iOS Safari address bar shows/hides. The virtual keyboard also pushes fixed elements up.

```css
/* BAD: fixed bottom bar gets obscured by home indicator */
.bar { position: fixed; bottom: 0; padding-bottom: 12px; }

/* GOOD: account for safe area */
.bar {
  position: fixed;
  bottom: 0;
  padding-bottom: max(12px, env(safe-area-inset-bottom));
}
```

Requires `<meta name="viewport" content="viewport-fit=cover">` for `env()` to work.

## 2. `100vh` on Mobile Browsers

`100vh` is the LARGEST viewport height (address bar hidden). Content overflows when the address bar is visible.

```css
/* BAD: overflows on mobile */
body { height: 100vh; }

/* GOOD: dynamic viewport height */
body { min-height: 100dvh; }

/* FALLBACK for older browsers */
body { min-height: 100vh; min-height: 100dvh; }
```

## 3. Custom Property Inheritance Surprises

Custom properties inherit through the DOM tree, not the CSS cascade. A property set on `.parent` is visible to `.child` even if `.child` doesn't declare it.

```css
/* This overrides --color for ALL descendants, not just .card */
.card { --color-primary: red; }
.card .button { color: var(--color-primary); } /* red */
.card .nested .deep { color: var(--color-primary); } /* also red! */
```

## 4. `z-index` Stacking Context

`z-index` only works within a stacking context. Common stacking context creators: `position` (non-static), `opacity < 1`, `transform`, `filter`, `will-change`.

```css
/* BAD: z-index ignored because no positioning */
.overlay { z-index: 999; } /* does nothing! */

/* GOOD */
.overlay { position: fixed; z-index: 999; }
```

## 5. Contrast Ratio Failures

WCAG AA requires 4.5:1 for normal text (<18px bold / <24px regular), 3:1 for large text. Common failure: light gray text on slightly-less-light gray background.

```css
/* FAILS: #9BAEC0 on #253545 = 2.9:1 ratio */
.muted { color: #9BAEC0; background: #253545; }

/* PASSES: #B8C8D8 on #253545 = 4.6:1 ratio */
.muted { color: #B8C8D8; background: #253545; }
```

Tool: use `contrast-ratio.com` or browser DevTools to check.

## 6. Animation Performance Traps

Animating `box-shadow` is expensive (triggers paint on every frame). Use `::after` with opacity trick:

```css
/* BAD: repaints every frame */
.card { transition: box-shadow 300ms; }
.card:hover { box-shadow: 0 0 24px rgba(0,0,0,0.5); }

/* GOOD: composited opacity change */
.card { position: relative; }
.card::after {
  content: '';
  position: absolute; inset: 0;
  box-shadow: 0 0 24px rgba(0,0,0,0.5);
  opacity: 0;
  transition: opacity 300ms;
}
.card:hover::after { opacity: 1; }
```

Exception: `box-shadow` in `@keyframes` is acceptable for decorative glows that don't need 60fps.

## 7. `-webkit-font-smoothing` Only Works on macOS

`-webkit-font-smoothing: antialiased` only affects macOS rendering. It's harmless elsewhere but don't rely on it for cross-platform consistency.

## 8. `overflow: hidden` Kills `position: sticky`

If any ancestor has `overflow: hidden`, `sticky` positioning breaks silently.

```css
/* BAD: sticky header won't work */
.wrapper { overflow: hidden; }
.wrapper .header { position: sticky; top: 0; } /* broken! */
```

## 9. Missing `box-sizing: border-box`

Without it, padding and border add to the element's width, causing layout overflow.

```css
/* Always set globally */
*, *::before, *::after { box-sizing: border-box; }
```

## 10. `gap` in Flexbox Browser Support

`gap` in flexbox is supported in all modern browsers (2021+), but older Safari versions (pre-14.1) don't support it. Use margin fallback if targeting older devices:

```css
.flex { display: flex; gap: 8px; }
/* Fallback: .flex > * + * { margin-left: 8px; } */
```

## 11. `env(safe-area-inset-*)` Requires `viewport-fit=cover`

The `env()` function returns `0` unless the viewport meta tag includes `viewport-fit=cover`:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

## 12. Dark Theme Scrollbar Styling

`color-scheme: dark` handles scrollbars automatically. Don't manually style scrollbars with `::-webkit-scrollbar` unless you have a strong reason -- it's fragile and non-standard.
