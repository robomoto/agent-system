<!-- last_verified: 2026-03-05 -->
# Accessibility — Patterns

## Contrast Ratios (WCAG 1.4.3 / 1.4.6 / 1.4.11)

| Requirement | Ratio | Applies to |
|-------------|-------|------------|
| AA normal text | 4.5:1 | Body text, labels, links |
| AA large text | 3:1 | 18pt+ or 14pt+ bold |
| AAA normal text | 7:1 | Enhanced contrast |
| Non-text contrast | 3:1 | Icons, borders, focus indicators, UI components |

### Checking Contrast

Browser devtools show contrast ratios in the color picker. For CSS variables,
inspect the computed value — variables may resolve differently per theme.

Tools:
- Chrome DevTools → Elements → color swatch → contrast ratio
- Firefox → Accessibility Inspector → Check for issues → Contrast
- CLI: `pa11y <url>` or `lighthouse <url> --only-categories=accessibility`

### Theme-Aware Checking

ALWAYS check both light and dark themes. Common failures:
- Primary color that passes on light background fails on dark background
- Muted text that's readable on white becomes invisible on dark gray
- Inverted logos that lose contrast in one theme
- Focus indicators invisible against one theme's background

## Keyboard Navigation (WCAG 2.1.1 / 2.4.3 / 2.4.7)

### Tab Order
- Must follow visual reading order (left→right, top→bottom)
- Don't use positive `tabindex` values (1, 2, 3) — they break natural order
- `tabindex="0"` makes element focusable in natural order
- `tabindex="-1"` makes element programmatically focusable only

### Focus Visibility
```css
/* GOOD — visible focus indicator */
:focus-visible {
    outline: 2px solid var(--pico-primary);
    outline-offset: 2px;
}

/* BAD — removes focus indicator entirely */
:focus { outline: none; }
```

### Skip Links
```html
<a href="#main-content" class="skip-link">Skip to content</a>
```
Must be first focusable element. Hidden until focused:
```css
.skip-link { position: absolute; top: -100%; }
.skip-link:focus { top: 0; }
```

### Keyboard Traps
User must ALWAYS be able to Tab away from any element. Common traps:
- Modals without Escape key handling
- Custom dropdowns that capture focus
- Infinite scrolling regions

## ARIA Patterns

### First Rule: Don't Use ARIA
Native HTML is always better:
- `<button>` not `<div role="button">`
- `<nav>` not `<div role="navigation">`
- `<a href>` not `<span role="link">`

### When ARIA Is Needed
- Live regions: `aria-live="polite"` for dynamic content updates
- Custom widgets: accordion, tabs, combobox (no native equivalent)
- State: `aria-expanded`, `aria-selected`, `aria-checked`
- Labels: `aria-label` when visible text isn't sufficient

### Common ARIA Mistakes
- `aria-label` on a non-interactive `<div>` (screen readers ignore it)
- `role="button"` without keyboard handler (Enter/Space to activate)
- `aria-hidden="true"` on focusable elements (creates ghost focus)
- Redundant: `<button aria-role="button">` (already a button)

## Touch Targets (WCAG 2.5.8)

Minimum 44x44px for touch devices. Check with:
```css
@media (max-width: 768px) {
    button, a[role="button"], input[type="submit"] {
        min-width: 44px;
        min-height: 44px;
    }
}
```

## Forms (WCAG 1.3.1 / 3.3.2)

### Labels
- Every input MUST have a visible `<label>` (not just `placeholder`)
- `placeholder` disappears on input — not a label replacement
- Associate with `for`/`id` or wrap input inside label

### Errors
- Identify the field in error
- Describe what went wrong and how to fix it
- Don't rely on color alone (add icon or text)
- Use `aria-describedby` to link error message to input
- Use `aria-invalid="true"` on the invalid field

## Color Independence (WCAG 1.4.1)

Information must not be conveyed by color alone:
- Links: underline or icon, not just color difference
- Errors: icon + text, not just red border
- Status: text label, not just colored dot
- Charts: patterns/labels, not just colors

## CSS Framework Gotchas

### Classless Frameworks (Pico, Simple.css)
- Global `button` styling may break third-party widget accessibility
- Theme switching via `data-theme` needs to update ALL color variables
- Form element restyling may remove native focus indicators
- `role="button"` on `<a>` tags changes screen reader announcement but
  doesn't add keyboard handling (Enter works on links, but Space doesn't)
