<!-- last_verified: 2026-03-08 -->
# Browser APIs Reference — Vanilla JS Web Client

## WebSocket API

```javascript
const ws = new WebSocket('wss://example.com/ws');

ws.onopen = () => { /* connected */ };
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
};
ws.onclose = (event) => {
  // event.code: 1000=normal, 1006=abnormal, 1001=going away
  // event.reason: string
  // event.wasClean: boolean
};
ws.onerror = () => { /* usually followed by onclose */ };

// Send (must check readyState)
if (ws.readyState === WebSocket.OPEN) {
  ws.send(JSON.stringify(msg));
}

// Close codes: 1000 (normal), 3000-4999 (app-defined)
ws.close(1000, 'Leaving');
```

**Reconnect pattern**: Exponential backoff with jitter. Base delay doubles each attempt (1s, 2s, 4s, 8s, 16s cap). Add +/-20% jitter to prevent thundering herd.

## DOM Manipulation (No Framework)

```javascript
// Query
const el = document.getElementById('id');
const el = document.querySelector('.class');
const els = document.querySelectorAll('.class');

// Create
const div = document.createElement('div');
div.className = 'roll-card';
div.dataset.rollId = id;  // data-roll-id attribute
div.innerHTML = `<span>${escaped}</span>`;  // XSS risk -- sanitize!
div.textContent = text;  // safe, no HTML parsing

// Insert
parent.appendChild(child);
parent.insertBefore(newNode, referenceNode);
el.insertAdjacentHTML('beforeend', html);  // fast, but sanitize input

// Remove
el.remove();

// Update
el.setAttribute('data-theme', 'arcane');
el.classList.add('active');
el.classList.remove('active');
el.classList.toggle('active');
el.style.setProperty('--glow-color', 'rgba(212,168,69,0.25)');
```

## Event Handling

```javascript
// Add listener
el.addEventListener('click', handler);
el.addEventListener('click', handler, { once: true });  // auto-removes

// Event delegation (preferred for dynamic lists)
document.getElementById('roll-list').addEventListener('click', (e) => {
  const card = e.target.closest('.roll-card');
  if (!card) return;
  const rollId = card.dataset.rollId;
});

// Keyboard
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') { e.preventDefault(); submitRoll(); }
});
```

## localStorage

```javascript
localStorage.setItem('blindroll_name', name);
const name = localStorage.getItem('blindroll_name');  // null if missing
localStorage.removeItem('blindroll_name');

// JSON storage
localStorage.setItem('key', JSON.stringify(obj));
const obj = JSON.parse(localStorage.getItem('key') ?? 'null');
```

**Limits**: ~5MB per origin. Synchronous (blocks main thread). No expiry -- manual cleanup required.

## Page Visibility API

```javascript
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    // Tab regained focus -- catch up on missed events
  } else {
    // Tab hidden -- pause non-essential work
  }
});
```

## Notifications API

```javascript
// Request permission (do this on user gesture, not page load)
const permission = await Notification.requestPermission();
// 'granted', 'denied', 'default'

// Show notification (only when tab is not focused)
if (document.visibilityState !== 'visible' && Notification.permission === 'granted') {
  new Notification('Roll Revealed!', {
    body: 'You rolled a 17 on 1d20',
    icon: '/icon.png',
    tag: 'roll-reveal',  // replaces previous with same tag
  });
}
```

## beforeunload

```javascript
window.addEventListener('beforeunload', (e) => {
  if (hasActiveSession) {
    e.preventDefault();
    // Modern browsers ignore custom messages, just show generic prompt
  }
});
```

**Important**: Only set this during active sessions. Remove when session ends. Browsers throttle/ignore if overused.

## History / URL

```javascript
// Read path
const roomCode = location.pathname.split('/')[2];  // /play/ABCD -> ABCD

// No navigation needed for SPA-like behavior -- just update title
document.title = `(3) Blind Roll - Session`;
```

## Vibration API

```javascript
// Haptic feedback on roll (graceful degradation)
if (navigator.vibrate) {
  navigator.vibrate(10);  // 10ms buzz
}
```

**iOS Safari**: Does NOT support Vibration API. Always check `navigator.vibrate` exists.

## requestAnimationFrame

```javascript
// Smooth animation loop
function updateTimers() {
  // Update time-since-roll displays
  document.querySelectorAll('[data-completed-at]').forEach(el => {
    const elapsed = Date.now() - parseInt(el.dataset.completedAt);
    el.textContent = formatElapsed(elapsed);
  });
  setTimeout(updateTimers, 15000);  // every 15s is fine for relative time
}
```

## Template Rendering (No Framework)

```javascript
// Simple render function pattern
function renderRollCard(roll) {
  const card = document.createElement('div');
  card.className = `roll-card ${getCritClass(roll)}`;
  card.dataset.rollId = roll.id;
  card.innerHTML = `
    <div class="roll-card__total">${escapeHtml(getTotal(roll))}</div>
    <div class="roll-card__details">
      <span class="expression-badge">${escapeHtml(roll.expression)}</span>
    </div>
  `;
  return card;
}

// XSS prevention
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
```

## Performance: Batch DOM Updates

```javascript
// BAD: multiple reflows
items.forEach(item => {
  container.appendChild(renderItem(item));
});

// GOOD: single reflow with fragment
const fragment = document.createDocumentFragment();
items.forEach(item => {
  fragment.appendChild(renderItem(item));
});
container.appendChild(fragment);
```
