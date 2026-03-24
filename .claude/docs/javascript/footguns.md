<!-- last_verified: 2026-03-05 -->
# JavaScript Footguns

## 1. Silent Async Errors

Unhandled promise rejections silently disappear in many runtimes. Every async path must have error handling.

```js
// BAD: rejection vanishes
async function handle(req) {
  doAsyncWork();  // missing await -- fire-and-forget, errors lost
}

// GOOD
async function handle(req) {
  try {
    await doAsyncWork();
  } catch (err) {
    return new Response(err.message, { status: 500 });
  }
}
```

## 2. `typeof null === 'object'`

This is a spec bug that will never be fixed. Use `value === null` explicitly.

## 3. Floating Point Arithmetic

```js
0.1 + 0.2 !== 0.3  // true -- IEEE 754
// Fix: use integer math (cents not dollars) or round: Math.round(x * 100) / 100
```

## 4. `for...in` Iterates Prototype Chain

```js
// BAD: picks up inherited properties
for (const key in obj) { /* ... */ }

// GOOD: use Object.keys/entries or hasOwnProperty check
for (const [key, value] of Object.entries(obj)) { /* ... */ }
```

## 5. Array Sort Mutates and Coerces to String

```js
[10, 9, 80].sort();  // [10, 80, 9] -- string comparison!
// Fix: always pass comparator
[10, 9, 80].sort((a, b) => a - b);  // [9, 10, 80]
// Note: sort() mutates the original array. Use toSorted() (ES2023) for immutable.
```

## 6. `==` Coercion Surprises

```js
'' == false   // true
0 == ''       // true
null == undefined  // true (this one is actually useful -- see idioms.md)
// Rule: use === everywhere EXCEPT for null/undefined checks
```

## 7. `this` Binding in Callbacks

```js
// BAD: `this` is undefined in strict mode, or global in sloppy
class Handler {
  name = 'handler';
  process() {
    items.forEach(function(item) {
      console.log(this.name);  // undefined!
    });
  }
}

// GOOD: arrow functions inherit `this`
items.forEach((item) => {
  console.log(this.name);  // works
});
```

## 8. JSON.parse Without Validation

```js
// BAD: trusts input shape
const data = JSON.parse(body);
return data.quotes[0].text;  // TypeError if shape differs

// GOOD: validate after parsing
const data = JSON.parse(body);
if (!Array.isArray(data?.quotes) || data.quotes.length === 0) {
  throw new AppError('Invalid data format', 400);
}
```

## 9. RegExp with Global Flag is Stateful

```js
const re = /foo/g;
re.test('foo');  // true
re.test('foo');  // false! (lastIndex advanced)
// Fix: create new RegExp each time, or don't use /g with .test()
```

## 10. Object Reference Sharing

```js
// BAD: default parameter is shared across calls
function createConfig(opts = {}) {
  const config = DEFAULT_CONFIG;  // reference, not copy!
  config.port = opts.port;        // mutates DEFAULT_CONFIG
}

// GOOD: spread to create new object
const config = { ...DEFAULT_CONFIG, ...opts };
```

## 11. parseInt Gotchas

```js
parseInt('08');      // 8 (modern engines), was 0 in old engines (octal)
parseInt('123abc');  // 123 (silently ignores trailing chars)
parseInt('');        // NaN

// Prefer Number() for strict parsing:
Number('123abc');    // NaN (correct -- invalid input)
Number('');          // 0 (still a gotcha)
```

## 12. Accidental Global Variables

```js
// BAD: missing declaration
function process() {
  result = compute();  // creates global variable in sloppy mode
}

// Always use 'use strict' or ESM (which is strict by default)
```
