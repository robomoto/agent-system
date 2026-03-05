# Cloudflare Workers Reference

## Runtime Model

Workers run on V8 isolates (not Node.js). No file system, no native modules, no `process` object. Each request gets a fresh execution context within a shared isolate.

### Key Differences from Node.js

| Feature | Workers | Node.js |
|---------|---------|---------|
| Module system | ESM (default) or Service Worker syntax | CJS or ESM |
| File system | None | Full `fs` access |
| `process` | Not available | Available |
| `Buffer` | Not available (use `ArrayBuffer`/`Uint8Array`) | Available |
| `setTimeout` | Available but no `setInterval` in some contexts | Both available |
| `fetch` | Global (Web standard) | `node-fetch` or `undici` (global in 18+) |
| Streams | Web Streams API | Node Streams (Web Streams in 18+) |

## Handler Patterns

### Module Worker (Recommended, ESM)

```js
export default {
  async fetch(request, env, ctx) {
    return new Response('Hello');
  },

  async scheduled(event, env, ctx) {
    // Cron trigger handler
  },
};
```

### Environment Bindings (`env`)

```js
// wrangler.toml binds KV, R2, D1, Durable Objects, secrets, vars
export default {
  async fetch(request, env, ctx) {
    const value = await env.MY_KV.get('key');
    const secret = env.API_KEY;  // from [vars] or secrets
    return new Response(value);
  },
};
```

## Request / Response

Both follow the Web standard (Fetch API):

```js
// Request
const url = new URL(request.url);
const method = request.method;
const path = url.pathname;
const params = url.searchParams;
const body = await request.json();
const header = request.headers.get('Authorization');

// Response
return new Response(JSON.stringify(data), {
  status: 200,
  headers: { 'Content-Type': 'application/json' },
});

// Response helpers
return Response.json(data);                    // shorthand (newer runtimes)
return Response.redirect(url, 301);
return new Response(null, { status: 204 });    // no body
```

## URL Routing (Manual)

Workers have no built-in router. Common pattern:

```js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (path === '/api/quotes' && request.method === 'GET') {
      return handleGetQuotes(env);
    }
    if (path.startsWith('/api/quotes/') && request.method === 'GET') {
      const id = path.split('/')[3];
      return handleGetQuote(id, env);
    }
    return new Response('Not Found', { status: 404 });
  },
};
```

## Storage Options

| Service | Use Case | Binding |
|---------|----------|---------|
| KV | Read-heavy key-value (eventually consistent) | `env.MY_KV` |
| R2 | Object/file storage (S3-compatible) | `env.MY_BUCKET` |
| D1 | SQLite database | `env.MY_DB` |
| Durable Objects | Strongly consistent, stateful, single-instance | `env.MY_DO` |
| Workers AI | ML inference | `env.AI` |

## Wrangler CLI

```bash
wrangler dev              # Local dev server (port 8787)
wrangler deploy           # Deploy to Cloudflare
wrangler secret put NAME  # Set a secret
wrangler kv:namespace create NAME  # Create KV namespace
wrangler d1 create NAME   # Create D1 database
wrangler tail             # Live logs from production
```

### wrangler.toml

```toml
name = "my-worker"
main = "src/index.js"
compatibility_date = "2024-12-01"

[vars]
ENVIRONMENT = "production"

[[kv_namespaces]]
binding = "MY_KV"
id = "abc123"

[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"

[[d1_databases]]
binding = "MY_DB"
database_name = "my-db"
database_id = "def456"
```

## Limits

| Resource | Free | Paid |
|----------|------|------|
| Requests/day | 100,000 | Unlimited |
| CPU time/request | 10ms | 30s |
| Worker size | 1 MB | 10 MB (after compression) |
| KV reads/day | 100,000 | 10M+ |
| Subrequests/request | 50 | 1,000 |
| Environment variables | 64 | 128 |

## CORS Pattern

```js
function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin || '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

// Handle preflight
if (request.method === 'OPTIONS') {
  return new Response(null, { status: 204, headers: corsHeaders(origin) });
}
```
