# Skill: Design System

Framework for building and maintaining consistent UI components. Used by the ui-designer when creating components and the reviewer when checking visual consistency.

## When to Use

- Creating new UI components
- Evaluating visual consistency of an implementation
- Establishing or extending a design system for a project
- Reviewing accessibility compliance

## Design Token Hierarchy

### 1. Primitive Tokens (raw values, never use directly in components)

```
color-blue-500: #3b82f6
spacing-4: 1rem
font-size-base: 1rem
radius-md: 0.375rem
```

### 2. Semantic Tokens (reference primitives, use in components)

```
color-primary: color-blue-500
color-danger: color-red-500
color-text: color-gray-900
color-text-muted: color-gray-500
color-surface: color-white
color-border: color-gray-200

spacing-component-gap: spacing-4
spacing-section-gap: spacing-8
spacing-page-padding: spacing-6

font-size-body: font-size-base
font-size-heading: font-size-xl
font-size-caption: font-size-sm

radius-button: radius-md
radius-card: radius-lg
radius-input: radius-md
```

### 3. Component Tokens (specific to a component, reference semantic tokens)

```
button-padding-x: spacing-4
button-padding-y: spacing-2
button-radius: radius-button
button-font-size: font-size-body

card-padding: spacing-6
card-radius: radius-card
card-border: 1px solid color-border
```

## Component Specification Format

Every component should document:

```markdown
## ComponentName

### Purpose
One sentence describing what this component does.

### Variants
- `primary` — Main action (filled background, high contrast)
- `secondary` — Secondary action (outlined, medium contrast)
- `ghost` — Tertiary action (no border, low contrast)

### States
| State | Visual Change |
|-------|--------------|
| default | Base appearance |
| hover | Slightly darker background, cursor: pointer |
| active | Darker background, slight inset |
| focus | Focus ring (2px outline, offset 2px, color-primary) |
| disabled | 50% opacity, cursor: not-allowed, no interactions |
| loading | Spinner replaces content, disabled state |
| error | Border color-danger, error message below |

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | "primary" \| "secondary" \| "ghost" | "primary" | Visual style |
| size | "sm" \| "md" \| "lg" | "md" | Component size |
| disabled | boolean | false | Disable interactions |
| loading | boolean | false | Show loading state |

### Responsive Behavior
- Below 640px: full-width, stacked if in a group
- Above 640px: intrinsic width, inline if in a group

### Accessibility
- Role: `button`
- Keyboard: Enter/Space to activate, Tab to focus
- ARIA: `aria-disabled` when disabled, `aria-busy` when loading
- Contrast: minimum 4.5:1 for text on background (WCAG AA)
```

## Accessibility Checklist (WCAG 2.1 AA)

### Perceivable
- [ ] Text contrast ratio >= 4.5:1 (3:1 for large text)
- [ ] Non-text contrast ratio >= 3:1 (icons, borders, focus indicators)
- [ ] Information not conveyed by color alone (icons, text, patterns)
- [ ] Images have alt text (decorative images have empty alt)
- [ ] Video has captions, audio has transcripts

### Operable
- [ ] All functionality available via keyboard
- [ ] Focus order is logical and predictable
- [ ] Focus indicators are visible (not removed with outline: none)
- [ ] No keyboard traps (user can always Tab away)
- [ ] Touch targets >= 44x44px on mobile

### Understandable
- [ ] Language is set on the document (`lang` attribute)
- [ ] Form inputs have visible labels (not just placeholders)
- [ ] Error messages identify the field and describe the fix
- [ ] Navigation is consistent across pages

### Robust
- [ ] Valid HTML structure
- [ ] ARIA roles and properties used correctly
- [ ] Custom components announce state changes to screen readers
- [ ] Works across major browsers and assistive technologies

## Layout Patterns

### Spacing Scale (8px base)

```
xs:  4px   (0.25rem)  — tight element spacing
sm:  8px   (0.5rem)   — related element spacing
md:  16px  (1rem)     — component internal spacing
lg:  24px  (1.5rem)   — component gap spacing
xl:  32px  (2rem)     — section spacing
2xl: 48px  (3rem)     — page section spacing
3xl: 64px  (4rem)     — major section spacing
```

### Responsive Breakpoints

```
sm:  640px   — mobile landscape / large phone
md:  768px   — tablet portrait
lg:  1024px  — tablet landscape / small desktop
xl:  1280px  — desktop
2xl: 1536px  — large desktop
```

### Common Layouts

- **Stack**: Vertical flow with consistent gap. Default for mobile.
- **Cluster**: Horizontal wrapping flow. For tags, badges, button groups.
- **Sidebar**: Fixed sidebar + fluid main content. Collapses to stack on mobile.
- **Grid**: Equal columns with gap. 1-col mobile, 2-col tablet, 3-4 col desktop.

## Anti-Patterns

- **Magic numbers**: `padding: 13px` — use tokens from the spacing scale
- **Color strings**: `color: #3b82f6` — use semantic tokens (`color-primary`)
- **Missing states**: Component only has default + hover. What about focus, disabled, error, loading?
- **Placeholder-only labels**: Screen readers can't reliably read placeholders. Use visible labels.
- **Removing focus outlines**: `outline: none` without a replacement makes keyboard navigation impossible
- **Fixed dimensions**: `width: 400px` breaks on mobile. Use max-width, percentage, or container queries.
- **Z-index wars**: Random z-index values. Define a z-index scale (dropdown: 100, modal: 200, toast: 300).
