<!-- last_verified: 2026-03-05 -->
# JavaScript Idioms (ES2020+)

## 1. Nullish Checks

```js
// Prefer nullish coalescing over ||  (|| treats 0, '', false as falsy)
const port = config.port ?? 8080;

// Loose equality for null/undefined check (idiomatic, covers both)
if (value == null) { /* null or undefined */ }
```

## 2. Optional Chaining

```js
const name = user?.profile?.name;
const result = obj?.method?.();  // method call with optional chaining
```

## 3. Destructuring with Defaults

```js
const { method = 'GET', headers = {} } = request;
// Nested destructuring
const { data: { id, name } = {} } = response;
```

## 4. Object Shorthand and Computed Properties

```js
const obj = { name, age, [dynamicKey]: value };
```

## 5. Array Methods over Loops

```js
// Prefer declarative
const active = users.filter(u => u.active);
const names = users.map(u => u.name);
const total = items.reduce((sum, item) => sum + item.price, 0);

// Use for...of when you need break/continue or async/await
for (const item of items) {
  if (item.done) break;
}
```

## 6. Async/Await over .then() Chains

```js
// Prefer
async function fetchData(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

// Parallel execution
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);
```

## 7. Template Literals

```js
const msg = `Hello ${name}, you have ${count} items`;
// Tagged templates for escaping
const query = sql`SELECT * FROM users WHERE id = ${id}`;
```

## 8. Spread and Rest

```js
const merged = { ...defaults, ...overrides };
const [first, ...rest] = items;
function log(message, ...args) { /* rest params */ }
```

## 9. Map/Set for Collections

```js
// Use Map when keys aren't strings or you need size/iteration order
const cache = new Map();
cache.set(objectKey, value);

// Use Set for unique values
const unique = [...new Set(array)];
```

## 10. Error Classes

```js
class AppError extends Error {
  constructor(message, statusCode, code) {
    super(message);
    this.name = 'AppError';
    this.statusCode = statusCode;
    this.code = code;
  }
}
```

## 11. ESM Modules

```js
// Named exports (preferred for tree-shaking)
export function handleRequest(req) { /* ... */ }
export const CONFIG = { /* ... */ };

// Default export (one per module, for the "main thing")
export default class Router { /* ... */ }

// Re-exports
export { handler } from './handler.js';
```

## 12. Guard Clauses (Early Return)

```js
function process(input) {
  if (!input) return null;
  if (!input.valid) throw new AppError('Invalid input', 400);
  // Happy path continues...
}
```

## 13. Object.entries / Object.fromEntries

```js
// Transform object values
const upper = Object.fromEntries(
  Object.entries(headers).map(([k, v]) => [k.toLowerCase(), v])
);
```

## 14. Structured Clone for Deep Copy

```js
const copy = structuredClone(original);  // ES2022, available in Workers
// Replaces JSON.parse(JSON.stringify(x)) which drops undefined, functions, Dates
```

## 15. Logical Assignment Operators (ES2021)

```js
obj.count ??= 0;   // assign if null/undefined
obj.name ||= 'Anonymous';  // assign if falsy
obj.cache &&= updatedCache;  // assign if truthy
```
