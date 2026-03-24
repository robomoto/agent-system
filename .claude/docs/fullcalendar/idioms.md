<!-- last_verified: 2026-03-05 -->
# FullCalendar v6 — Idioms

## CSS Architecture

FullCalendar renders its own DOM with `.fc-*` class prefixes. All customization targets
`.fc .fc-*` selectors. The `.fc` root class scopes everything — always prefix custom styles
with `.fc` to avoid leaking into the rest of the page.

```css
/* GOOD — scoped to FullCalendar */
.fc .fc-button { ... }

/* BAD — could affect other buttons */
.fc-button { ... }
```

## Toolbar Configuration

```js
headerToolbar: {
  left: 'prev,next today',
  center: 'title',
  right: 'dayGridMonth,listWeek'
}
```

### Button Classes

| Element | Class |
|---------|-------|
| Previous month | `.fc-prev-button` |
| Next month | `.fc-next-button` |
| Today | `.fc-today-button` |
| Month view toggle | `.fc-dayGridMonth-button` |
| List view toggle | `.fc-listWeek-button` |
| Active view button | `.fc-button-active` |
| Toolbar title | `.fc-toolbar-title` |
| Toolbar container | `.fc-toolbar` |

## Button Styling Pattern

Override FullCalendar buttons to match your design system:

```css
.fc .fc-button {
    background-color: var(--pico-primary);
    color: var(--pico-primary-inverse);
    border: 1px solid var(--pico-primary);
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    font-size: 0.85rem;
    cursor: pointer;
    line-height: 1.4;
}

.fc .fc-button:hover {
    background-color: var(--pico-primary-hover);
    border-color: var(--pico-primary-hover);
}

.fc .fc-button:focus {
    outline: 2px solid var(--pico-primary-focus);
    outline-offset: 2px;
}

.fc .fc-button-active {
    background-color: var(--pico-primary-hover);
    border-color: var(--pico-primary-hover);
}
```

## Prev/Next Icon Buttons

These need explicit sizing for touch targets:

```css
.fc .fc-prev-button,
.fc .fc-next-button {
    min-width: 36px;
    min-height: 36px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

/* Mobile: WCAG touch target minimum */
@media (max-width: 768px) {
    .fc .fc-prev-button,
    .fc .fc-next-button {
        min-width: 44px;
        min-height: 44px;
    }
}
```

## Toolbar Spacing

```css
.fc .fc-toolbar {
    margin-bottom: 1rem;
}

.fc .fc-toolbar-title {
    font-size: 1.15rem;
    font-weight: 600;
}
```

## Event Styling

| Selector | Purpose |
|----------|---------|
| `.fc-event` | Base event element |
| `.fc-daygrid-event` | Month-view event |
| `.fc-daygrid-dot-event` | Dot-style event (compact) |
| `.fc-event-title` | Event text label |

Event colors can be set via event data (`backgroundColor`, `borderColor`) or CSS:

```css
.fc-daygrid-event {
    cursor: pointer;
}

.fc-event:focus {
    outline: 2px solid var(--pico-primary);
    outline-offset: 1px;
}

/* Truncate long event titles */
.fc-daygrid-event .fc-event-title {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
```

## "+N more" Link

When `dayMaxEvents: N` truncates events:

```css
.fc-daygrid-more-link {
    color: var(--pico-primary);
    font-weight: 600;
    font-size: 0.85rem;
}

.fc-daygrid-more-link:hover {
    color: var(--pico-primary-hover);
    text-decoration: underline;
}
```

## Popover (clicking "+N more")

```css
.fc-more-popover {
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.fc-more-popover .fc-popover-header {
    background: var(--pico-primary);
    color: var(--pico-primary-inverse);
    border-radius: 6px 6px 0 0;
    padding: 0.5rem 0.75rem;
}
```

## Dark Mode

FullCalendar has no built-in dark mode. Override manually:

```css
[data-theme="dark"] .fc {
    --fc-border-color: var(--pico-muted-border-color);
    --fc-page-bg-color: var(--pico-background-color);
    --fc-neutral-bg-color: var(--pico-card-sectioning-background-color);
}

[data-theme="dark"] .fc .fc-col-header-cell {
    color: var(--pico-color);
}

[data-theme="dark"] .fc .fc-daygrid-day-number {
    color: var(--pico-color);
}
```

## Responsive

- FullCalendar handles its own responsive behavior internally
- On mobile, `listWeek` view is often better than `dayGridMonth`
- Toolbar can wrap: `.fc .fc-toolbar { flex-wrap: wrap; }`
- Consider hiding the view toggle on small screens if only one view is useful
