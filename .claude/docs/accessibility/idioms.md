<!-- last_verified: 2026-03-21 -->
# Accessibility — Idioms

## First Rule of ARIA

Use native HTML elements when possible. No ARIA is better than bad ARIA.

```html
<!-- Bad: div with ARIA -->
<div role="button" tabindex="0" aria-pressed="false">Save</div>

<!-- Good: native element -->
<button type="button">Save</button>
```

## Landmark Roles

Every page needs a clear landmark structure:

```html
<header role="banner">...</header>      <!-- site header, once per page -->
<nav role="navigation" aria-label="Main">...</nav>
<main role="main">...</main>            <!-- once per page -->
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

Multiple `<nav>` elements need distinct `aria-label` values.

## Heading Hierarchy

- One `<h1>` per page (the page title)
- Never skip levels (h1 → h3 without h2)
- Use headings for structure, not styling

```html
<!-- Screen readers use headings for navigation -->
<h1>Settings</h1>
  <h2>Notifications</h2>
    <h3>Email</h3>
    <h3>Push</h3>
  <h2>Privacy</h2>
```

## Skip Navigation

First focusable element should be a skip link:

```html
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>
  <nav>...</nav>
  <main id="main-content">...</main>
</body>
```

```css
.skip-link {
  position: absolute;
  left: -9999px;
}
.skip-link:focus {
  position: static;
}
```

## Live Regions

For dynamic content updates that screen readers should announce:

```html
<!-- Polite: waits for user to finish current task -->
<div aria-live="polite">3 results found</div>

<!-- Assertive: interrupts immediately (use sparingly) -->
<div role="alert">Session expiring in 2 minutes</div>

<!-- Status: polite + implicit role -->
<div role="status">Changes saved</div>
```

**Gotcha:** The live region element must exist in the DOM *before* content changes. Dynamically inserting an element with `aria-live` won't work.

## Dialog / Modal Focus Management

```javascript
// 1. Store the trigger element
const trigger = document.activeElement;

// 2. Open modal, move focus to first focusable element inside
modal.showModal(); // <dialog> handles focus trap natively
// Or for custom modals:
modal.querySelector('[autofocus], button, [href], input').focus();

// 3. Trap focus inside (Tab/Shift+Tab cycle within modal)
// <dialog> does this automatically

// 4. On close, return focus to trigger
modal.close();
trigger.focus();
```

```html
<dialog aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm delete</h2>
  <p>This cannot be undone.</p>
  <button autofocus>Cancel</button>
  <button>Delete</button>
</dialog>
```

## Form Labeling

Every input needs a programmatic label:

```html
<!-- Explicit label (preferred) -->
<label for="email">Email address</label>
<input id="email" type="email" required>

<!-- Group related inputs -->
<fieldset>
  <legend>Notification preferences</legend>
  <label><input type="checkbox" name="notify-email"> Email</label>
  <label><input type="checkbox" name="notify-push"> Push</label>
</fieldset>
```

### Error Association

```html
<label for="password">Password</label>
<input id="password" type="password"
       aria-describedby="password-error password-hint"
       aria-invalid="true">
<p id="password-hint">Must be at least 8 characters</p>
<p id="password-error" role="alert">Password is too short</p>
```

## Keyboard Interaction Patterns

### Tabs (role="tablist")

```
Tab       → moves focus into/out of tab group
Arrow L/R → selects previous/next tab
Home/End  → first/last tab
```

```html
<div role="tablist" aria-label="Settings">
  <button role="tab" aria-selected="true" aria-controls="panel-1">General</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" tabindex="-1">Privacy</button>
</div>
<div role="tabpanel" id="panel-1">...</div>
```

**Key pattern:** Only the active tab has `tabindex="0"`. Others have `tabindex="-1"`. Arrow keys move selection (roving tabindex).

### Menu (role="menu")

```
Enter/Space → activate item
Arrow Up/Down → navigate items
Escape → close menu, return focus to trigger
Home/End → first/last item
```

### Combobox (autocomplete)

```
Arrow Down → open listbox / next option
Arrow Up → previous option
Enter → select highlighted option
Escape → close listbox
Type → filter options
```

### Toggle / Switch

```html
<button role="switch" aria-checked="false" aria-label="Dark mode">
  <span aria-hidden="true">Off</span>
</button>
```

`Space` toggles the switch.

## Visually Hidden (screen reader only)

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

Use for: icon-only buttons, extra context, skip links when unfocused.

```html
<button>
  <svg aria-hidden="true">...</svg>
  <span class="sr-only">Close dialog</span>
</button>
```

## Images

```html
<!-- Informative: describe content -->
<img src="chart.png" alt="Monthly revenue up 12% from $40K to $45K">

<!-- Decorative: hide from AT -->
<img src="divider.png" alt="" role="presentation">

<!-- Complex: link to long description -->
<figure>
  <img src="architecture.png" alt="System architecture diagram" aria-describedby="arch-desc">
  <figcaption id="arch-desc">Three-tier architecture with...</figcaption>
</figure>
```

## Focus Indicators

Never remove focus outlines without replacement:

```css
/* Bad */
*:focus { outline: none; }

/* Good: custom focus indicator */
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

`:focus-visible` shows outline for keyboard users but not mouse clicks.

## SPA Route Changes

When navigating in a single-page app:

1. Update `document.title`
2. Move focus to the new page's `<h1>` or main content area
3. Announce the navigation via a live region

```javascript
function navigateTo(route) {
  renderPage(route);
  document.title = `${pageTitle} - App Name`;
  document.querySelector('h1').focus();
}
```
