# FullCalendar v6 — Footguns

## CSS Framework Collision (CRITICAL)

Classless CSS frameworks (Pico, Simple.css, Water.css) style ALL `<button>` elements
globally. FullCalendar's toolbar uses `<button>` elements. Result: calendar buttons
inherit the framework's padding, border-radius, and background — looking like form
controls (checkboxes, toggles) instead of navigation buttons.

**Fix:** Override `.fc .fc-button` styles explicitly. The `.fc` prefix gives you higher
specificity than element-level framework selectors.

```css
/* This beats Pico's `button { ... }` selector */
.fc .fc-button {
    background-color: var(--your-primary);
    color: white;
    border: 1px solid var(--your-primary);
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    cursor: pointer;
}
```

**Detection:** If calendar buttons look like checkboxes, form inputs, or have
unexpectedly large padding, this is almost certainly the cause.

## Specificity Wars

FullCalendar uses `.fc-button` (one class). Your CSS framework may use compound
selectors like `button:not([class])` or `:where(button)`. Test by inspecting
computed styles in browser devtools.

If the framework still wins, escalate to `.fc .fc-button` (two classes) or
scope the calendar container: `#calendar .fc .fc-button`.

Never use `!important` as a first resort — it creates maintenance debt.

## Icon/Arrow Disappearance

FullCalendar v6 uses CSS `content` on pseudo-elements for prev/next arrows
(chevrons). If a CSS framework or reset stylesheet overrides `content` on
`::before`/`::after`, the arrows disappear and buttons look empty.

**Check:** Inspect `.fc-icon-chevron-left::before` — it should have a `content`
value. If blank, add:

```css
.fc .fc-icon-chevron-left::before { content: "\2039"; }  /* single left angle */
.fc .fc-icon-chevron-right::before { content: "\203A"; } /* single right angle */
```

Or use more prominent arrows:
```css
.fc .fc-icon-chevron-left::before { content: "\25C0"; }  /* left triangle */
.fc .fc-icon-chevron-right::before { content: "\25B6"; } /* right triangle */
```

## Touch Targets Too Small

FullCalendar's default button sizes may be under 44px, failing WCAG 2.1 AA
touch-target requirements. Always add minimum dimensions for mobile:

```css
@media (max-width: 768px) {
    .fc .fc-prev-button,
    .fc .fc-next-button,
    .fc .fc-today-button {
        min-width: 44px;
        min-height: 44px;
    }
}
```

## dayMaxEvents "+N more" Link Styling

When `dayMaxEvents: N` is set, overflow events show a "+N more" link. If this
link inherits button or anchor styles from the CSS framework, it looks broken
(too large, wrong color, unexpected borders).

Target explicitly:
```css
.fc-daygrid-more-link {
    color: var(--your-primary);
    font-weight: 600;
    font-size: 0.85rem;
    /* Reset any framework overrides */
    background: none;
    border: none;
    padding: 0;
}
```

## Dark Mode — Forgetting Grid Lines

Overriding FullCalendar's background for dark mode without also overriding
border/grid colors results in invisible or barely-visible grid lines (dark
borders on dark background).

**Always override both:**
```css
[data-theme="dark"] .fc {
    --fc-border-color: #3d3f3d;        /* visible on dark bg */
    --fc-page-bg-color: #1a1c1a;       /* match your dark bg */
    --fc-neutral-bg-color: #242624;    /* today/highlight bg */
}
```

Also check: `.fc-scrollgrid`, `.fc td`, `.fc th` — these may use hardcoded
borders that don't respond to CSS variables.

## eventClick vs URL Double Navigation

FullCalendar events can have a `url` property (makes them `<a>` tags) AND an
`eventClick` callback. If you use both, the click fires the callback AND
follows the link.

**Fix:** Always call `info.jsEvent.preventDefault()` in `eventClick` when
you're handling navigation yourself:

```js
eventClick: function(info) {
    info.jsEvent.preventDefault();
    if (info.event.url) {
        window.location.href = info.event.url;
    }
}
```

## Popover Z-Index

The "+N more" popover may render behind modals, sticky headers, or other
positioned elements. FullCalendar uses a modest z-index. If the popover is
hidden behind your nav, add:

```css
.fc-more-popover {
    z-index: 100;  /* above your nav's z-index */
}
```
