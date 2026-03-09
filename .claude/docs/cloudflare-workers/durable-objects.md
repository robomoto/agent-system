# Durable Objects Reference

## What They Are

Durable Objects provide strongly consistent, single-instance stateful objects at the edge. Each object:
- Has a unique ID (generated or from name)
- Runs in a single location (migrates as needed)
- Handles requests one at a time (serialized via input gate)
- Can hold in-memory state between requests
- Supports WebSocket hibernation for low-cost persistent connections

## Class Definition

```typescript
export class MyRoom implements DurableObject {
  private state: DurableObjectState;
  private env: Env;
  private connections: Map<WebSocket, ConnectionMeta>;

  constructor(state: DurableObjectState, env: Env) {
    this.state = state;
    this.env = env;
    this.connections = new Map();
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === '/ws') {
      return this.handleWebSocket(request);
    }
    return new Response('Not Found', { status: 404 });
  }
}
```

## wrangler.toml Configuration

```toml
[[durable_objects.bindings]]
name = "ROOMS"
class_name = "Room"

[[migrations]]
tag = "v1"
new_classes = ["Room"]
```

## Getting a Stub (from Worker)

```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // From a name (deterministic)
    const id = env.ROOMS.idFromName(roomCode);
    const stub = env.ROOMS.get(id);
    return stub.fetch(request);
  }
};
```

`idFromName()` always returns the same ID for the same name. `newUniqueId()` generates a random one.

## WebSocket Handling

### Standard (Non-Hibernation)

```typescript
async handleWebSocket(request: Request): Promise<Response> {
  const pair = new WebSocketPair();
  const [client, server] = Object.values(pair);

  server.accept();
  this.connections.set(server, { role: 'player' });

  server.addEventListener('message', (event) => {
    const data = JSON.parse(event.data as string);
    this.handleMessage(server, data);
  });

  server.addEventListener('close', () => {
    this.connections.delete(server);
  });

  return new Response(null, { status: 101, webSocket: client });
}
```

### Hibernation API (Recommended for Scale)

Hibernation lets the DO sleep between messages, saving CPU billing:

```typescript
export class Room implements DurableObject {
  async fetch(request: Request): Promise<Response> {
    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    // Accept with hibernation -- DO can sleep between messages
    this.state.acceptWebSocket(server, ['player']);  // tags for filtering

    return new Response(null, { status: 101, webSocket: client });
  }

  // Called when a message arrives (wakes DO if hibernating)
  async webSocketMessage(ws: WebSocket, message: string): Promise<void> {
    const data = JSON.parse(message);
    this.handleMessage(ws, data);
  }

  // Called when a WebSocket closes
  async webSocketClose(ws: WebSocket, code: number, reason: string): Promise<void> {
    ws.close(code, reason);
    // Clean up connection state
  }

  // Called on WebSocket error
  async webSocketError(ws: WebSocket, error: unknown): Promise<void> {
    ws.close(1011, 'Internal error');
  }
}
```

Get connected sockets: `this.state.getWebSockets('player')` returns all sockets with that tag.

## Storage API

```typescript
// Transactional key-value storage (persists across restarts)
await this.state.storage.put('key', value);
const value = await this.state.storage.get('key');
await this.state.storage.delete('key');

// Batch operations
await this.state.storage.put({ key1: val1, key2: val2 });
const map = await this.state.storage.get(['key1', 'key2']);

// List with prefix
const entries = await this.state.storage.list({ prefix: 'room:' });
```

**Limits**: 128 KiB per value, 2048 bytes per key, 128 KiB total per `put()` call.

## Alarms

```typescript
// Schedule an alarm (only one active at a time)
await this.state.storage.setAlarm(Date.now() + 60_000);  // 60s from now

// Handler
async alarm(): Promise<void> {
  // Clean up stale rooms, send keepalives, etc.
  await this.state.storage.deleteAll();
}
```

## Broadcasting to Connections

```typescript
broadcast(message: string, exclude?: WebSocket): void {
  for (const [ws, meta] of this.connections) {
    if (ws === exclude) continue;
    try {
      ws.send(message);
    } catch {
      this.connections.delete(ws);
      try { ws.close(1011, 'Send failed'); } catch {}
    }
  }
}

// Filtered broadcast (e.g., only to players, not DM)
broadcastToPlayers(message: string, excludeWs?: WebSocket): void {
  for (const [ws, meta] of this.connections) {
    if (ws === excludeWs || meta.role !== 'player') continue;
    try { ws.send(message); } catch { /* cleanup */ }
  }
}
```

## Concurrency Model

- Only ONE request executes at a time within a DO (input gate serialization)
- WebSocket messages are also serialized through the input gate
- This means NO race conditions within a single DO -- no mutexes needed
- But: long-running handlers block all other requests to the same DO

## Limits

| Resource | Limit |
|----------|-------|
| CPU time per request | 30s (paid) |
| Memory per DO | 128 MB |
| Storage per DO | Unlimited (billed per GB-month) |
| WebSocket connections | No hard limit (memory-bound) |
| Subrequests per request | 1,000 |

## Common Patterns

### Room-Based Multiplayer

```typescript
// Worker routes to room by code
const roomId = env.ROOMS.idFromName(roomCode.toUpperCase());
const room = env.ROOMS.get(roomId);

// Forward the upgrade request
return room.fetch(request);
```

### Graceful Shutdown

```typescript
async closeAll(reason: string): void {
  for (const [ws] of this.connections) {
    try { ws.close(1000, reason); } catch {}
  }
  this.connections.clear();
}
```
