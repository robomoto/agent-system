<!-- last_verified: 2026-03-05 -->
# Accessibility — Footguns

## Dark Mode Contrast Failures

Customizing only `--pico-primary` without checking dark mode contrast is the #1
a11y failure in themed sites. A green that passes on white (#f8f6f3) may fail on
dark gray (#1a1c1a).

**Fix:** Check every text/background pair in BOTH themes. Use browser devtools
contrast checker with each theme active.

## filter: invert(1) for Dark Mode

`filter: invert(1)` on logos/images is unreliable:
- Inverts all colors, may produce unexpected hues
- Can push contrast below WCAG minimums
- Doesn't work on complex images

**Better:** Separate dark-mode assets, SVG with `fill: currentColor`, or
CSS `mask-image`.

## Invisible Focus Indicators

Pico CSS provides focus styles, but custom overrides may remove them:
- `outline: none` without replacement = WCAG 2.4.7 failure
- Custom buttons/links that override all Pico styles may lose focus ring
- Third-party widgets (FullCalendar) may have no focus styles after Pico reset

**Check:** Tab through every interactive element. If you can't see where focus
is, it's a failure.

## role="button" on Links

`<a href="..." role="button">` changes screen reader announcement to "button"
but the element still behaves as a link:
- Space key doesn't activate it (links only respond to Enter)
- Screen reader users expect buttons to perform actions, not navigate

**Fix:** Use `<a>` for navigation, `<button>` for actions. If you must use
`role="button"`, add `onkeydown` handler for Space.

## Placeholder-Only Labels

`<input placeholder="Email">` is NOT accessible:
- Placeholder disappears when user types
- Low contrast in most browsers (gray on white)
- Screen readers may not announce it as a label

**Fix:** Always use `<label>`. Placeholder is supplementary, not primary.

## Color-Only Information

Common failures:
- Status dots with no text label (calendar source filters)
- Error states shown only with red border
- Links distinguished from text only by color (no underline)
- Required fields marked only with red asterisk

**Fix:** Always add a non-color indicator (icon, text, pattern, underline).

## Missing Lang Attribute

`<html>` without `lang="en"` (or appropriate language) causes screen readers
to guess the language, often incorrectly. Always set it.

## Auto-Playing Media

Video or audio that plays automatically with no way to pause = WCAG 1.4.2
failure. Always provide pause/stop controls and never autoplay with sound.

## Keyboard Traps in Modals

A modal that captures focus without an Escape key handler traps keyboard
users. Always:
1. Trap focus INSIDE the modal while open (don't let Tab escape behind it)
2. Handle Escape to close
3. Return focus to the trigger element when closed

## Touch Target Size

Buttons under 44x44px fail WCAG 2.5.8. Common offenders:
- Icon-only buttons (close, menu, arrows)
- Inline action links ("edit", "delete")
- Calendar navigation buttons
- Social media icon links

**Check:** Inspect computed dimensions. `min-width` and `min-height` on
interactive elements, especially in mobile media queries.

## HTMX Dynamic Content

Content swapped in via HTMX (hx-swap) doesn't announce to screen readers
unless you use `aria-live` regions:

```html
<div aria-live="polite" id="results">
  <!-- HTMX swaps content here -->
</div>
```

Without this, screen reader users won't know content changed.
