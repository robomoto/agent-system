<!-- last_verified: 2026-03-05 -->
# Cloudflare Workers Footguns

## 1. No Node.js APIs

Workers run on V8 isolates, not Node.js. Common traps:

```js
// FAILS: no process object
const env = process.env.API_KEY;
// CORRECT: use env parameter
export default { async fetch(req, env) { env.API_KEY; } };

// FAILS: no Buffer
const buf = Buffer.from(str);
// CORRECT: use TextEncoder
const buf = new TextEncoder().encode(str);

// FAILS: no require()
const fs = require('fs');
// CORRECT: ESM imports only
import { something } from './module.js';
```

## 2. Response/Request Body Can Only Be Read Once

```js
// BAD: body already consumed
const text = await request.text();
const json = JSON.parse(text);
const text2 = await request.text();  // TypeError: body already used

// GOOD: clone if you need to read twice
const clone = request.clone();
const json = await request.json();
const text = await clone.text();
```

## 3. CPU Time Limits (Not Wall Clock)

The 10ms free / 30s paid limit is CPU time, not wall clock time. `await fetch()` doesn't count against it (I/O wait is free). But JSON parsing large payloads, crypto operations, and loops DO count.

```js
// This is fine -- I/O wait doesn't count
const resp = await fetch('https://slow-api.com/data');  // 5 seconds wall clock, ~0ms CPU

// This can hit limits -- CPU-intensive
const huge = JSON.parse(await resp.text());  // large payload = CPU time
```

## 4. `waitUntil` for Fire-and-Forget Work

If you return a Response before async work finishes, the runtime may kill pending promises. Use `ctx.waitUntil()`:

```js
export default {
  async fetch(request, env, ctx) {
    const response = new Response('OK');
    // BAD: this may never complete
    logToAnalytics(request);
    // GOOD: keeps the worker alive until this resolves
    ctx.waitUntil(logToAnalytics(request));
    return response;
  },
};
```

## 5. KV is Eventually Consistent

KV writes take up to 60 seconds to propagate globally. Don't read-after-write and expect the new value:

```js
await env.MY_KV.put('key', 'value');
const val = await env.MY_KV.get('key');  // might return OLD value!
```

If you need strong consistency, use Durable Objects or D1.

## 6. Subrequest Limit

Free plan: 50 subrequests per invocation. Paid: 1,000. Each `fetch()` call counts. Loops that fan out can hit this:

```js
// BAD: 200 fetch calls = over limit
const results = await Promise.all(urls.map(u => fetch(u)));

// GOOD: batch or paginate
```

## 7. No `__dirname` or File Paths

There's no file system. Static assets must be:
- Inlined as JS objects/strings
- Stored in KV or R2
- Served via Workers Sites or Pages

```js
// FAILS
import data from './data.json';  // Only works if bundler supports it
// WORKS with wrangler (uses esbuild under the hood)
import data from './data.json';  // Actually works! wrangler bundles JSON imports
```

Note: Wrangler's esbuild bundler DOES support JSON imports. This works.

## 8. CORS Preflight Handling

Browsers send OPTIONS requests before cross-origin requests. If you don't handle them, the actual request never arrives:

```js
// BAD: 404 on OPTIONS kills the real request
if (path === '/api/data') return handleData(request);

// GOOD: handle OPTIONS explicitly
if (request.method === 'OPTIONS') {
  return new Response(null, { status: 204, headers: corsHeaders() });
}
```

## 9. Headers Are Immutable on Incoming Request

```js
// FAILS
request.headers.set('X-Custom', 'value');  // TypeError: immutable

// GOOD: create new Headers
const newHeaders = new Headers(request.headers);
newHeaders.set('X-Custom', 'value');
```

## 10. `crypto.randomUUID()` is Available

Workers support Web Crypto API. No need for uuid packages:

```js
const id = crypto.randomUUID();
const hash = await crypto.subtle.digest('SHA-256', data);
```

## 11. Large Worker Bundles

Workers have a 1 MB (free) / 10 MB (paid, after gzip) size limit. Large `node_modules` or inlined data can exceed this. Solutions:
- Move data to KV or R2
- Use dynamic imports for cold paths
- Audit bundle with `wrangler deploy --dry-run --outdir=dist`

## 12. compatibility_date Matters

The `compatibility_date` in `wrangler.toml` controls which runtime features and breaking changes are active. Old dates miss new APIs; jumping forward may break things. Advance incrementally and test.
