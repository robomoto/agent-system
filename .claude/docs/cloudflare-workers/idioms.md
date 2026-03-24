<!-- last_verified: 2026-03-05 -->
# Cloudflare Workers Idioms

## 1. Module Worker Export Pattern

```js
export default {
  async fetch(request, env, ctx) {
    // All request handling here
  },
};
```

This is the standard ESM pattern. Avoid the legacy Service Worker `addEventListener('fetch', ...)` syntax.

## 2. URL-Based Routing

```js
const url = new URL(request.url);
const { pathname, searchParams } = url;

// Simple router
const routes = {
  'GET /api/items': handleList,
  'GET /api/items/:id': handleGet,
  'POST /api/items': handleCreate,
};

// Match with method + path
const routeKey = `${request.method} ${pathname}`;
```

## 3. JSON Response Helper

```js
function jsonResponse(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...extraHeaders,
    },
  });
}
```

## 4. Error Response Pattern

```js
function errorResponse(message, status = 500) {
  return jsonResponse({ error: message }, status);
}

// Usage
if (!id) return errorResponse('Missing ID', 400);
```

## 5. Environment Variable Access

```js
// Secrets and vars come through the env parameter, not process.env
export default {
  async fetch(request, env) {
    const apiKey = env.API_KEY;       // from wrangler secret
    const mode = env.ENVIRONMENT;     // from [vars] in wrangler.toml
  },
};
```

## 6. Request Validation

```js
async function parseBody(request) {
  const contentType = request.headers.get('Content-Type') || '';
  if (!contentType.includes('application/json')) {
    return { error: 'Expected JSON', data: null };
  }
  try {
    const data = await request.json();
    return { error: null, data };
  } catch {
    return { error: 'Invalid JSON', data: null };
  }
}
```

## 7. Cache-Control Headers

```js
// Static/rarely-changing data
const headers = {
  'Cache-Control': 'public, max-age=3600',  // 1 hour
  'Content-Type': 'application/json',
};

// Dynamic data
const headers = {
  'Cache-Control': 'no-store',
  'Content-Type': 'application/json',
};
```

## 8. CORS Middleware Pattern

```js
function withCORS(response, origin = '*') {
  const headers = new Headers(response.headers);
  headers.set('Access-Control-Allow-Origin', origin);
  headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  headers.set('Access-Control-Allow-Headers', 'Content-Type');
  return new Response(response.body, {
    status: response.status,
    headers,
  });
}

// Usage
return withCORS(jsonResponse(data));
```

## 9. Path Parameter Extraction

```js
function matchPath(pattern, pathname) {
  // pattern: '/api/quotes/:id'
  // pathname: '/api/quotes/42'
  const patternParts = pattern.split('/');
  const pathParts = pathname.split('/');
  if (patternParts.length !== pathParts.length) return null;

  const params = {};
  for (let i = 0; i < patternParts.length; i++) {
    if (patternParts[i].startsWith(':')) {
      params[patternParts[i].slice(1)] = decodeURIComponent(pathParts[i]);
    } else if (patternParts[i] !== pathParts[i]) {
      return null;
    }
  }
  return params;
}
```

## 10. Structured Logging

```js
function log(level, message, data = {}) {
  console.log(JSON.stringify({
    level,
    message,
    timestamp: Date.now(),
    ...data,
  }));
}
// View with: wrangler tail --format=json
```

## 11. Health Check Endpoint

```js
if (pathname === '/health') {
  return jsonResponse({ status: 'ok', timestamp: Date.now() });
}
```

## 12. Random Item Selection

```js
// Common for quote/joke/tip APIs
function randomItem(array) {
  return array[Math.floor(Math.random() * array.length)];
}
```
