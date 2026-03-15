# MCP Idioms — FastMCP Patterns

Patterns from the health-stack wger-mcp server and FastMCP best practices.

## Basic Server Setup

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("server-name")

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
```

The server name appears in Claude Desktop's tool picker. Use a short descriptive slug.

## Lifespan Pattern (Dependency Injection)

Use `lifespan` to initialize shared state once per server process. This is the correct
way to manage HTTP clients, database handles, and loaded config files.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(server: FastMCP):
    # Setup: runs once at startup
    client = httpx.AsyncClient(
        base_url=os.environ["WGER_URL"],
        headers={"Authorization": f"Token {os.environ['WGER_TOKEN']}"},
        timeout=15.0,
    )
    food_db = FoodDB()          # YAML-backed, loads on init
    standards_db = StandardsDB()

    yield {
        "client": client,
        "food_db": food_db,
        "standards_db": standards_db,
    }

    # Teardown: runs on server shutdown
    await client.aclose()

mcp = FastMCP("wger-nutrition", lifespan=lifespan)
```

The dict yielded from lifespan is available as `ctx.request_context.lifespan_context`.

## Context Parameter

Inject `Context` as the last parameter of any tool. FastMCP passes it automatically;
Claude never sees it in the tool schema.

```python
@mcp.tool()
async def log_meal(items: list[dict], meal_name: str = "Logged", ctx: Context = None) -> str:
    lc = ctx.request_context.lifespan_context
    wger = lc["client"]
    food_db = lc["food_db"]
    ...
```

Helper function to destructure lifespan context (from wger-mcp):

```python
def _state(ctx: Context) -> tuple[WgerClient, FoodDB, StandardsDB]:
    lc = ctx.request_context.lifespan_context
    return lc["wger"], lc["food_db"], lc["standards_db"]
```

## @tool Decorator

The `@mcp.tool()` decorator registers a function as an MCP tool. The function's
docstring becomes the tool description Claude sees.

```python
@mcp.tool()
async def search_food(query: str, ctx: Context = None) -> str:
    """Search for food — checks local DB first, then wger's ingredient database.

    Use this to find foods before logging. If a food isn't in the local DB,
    pick a result from wger and use add_food to cache it locally.
    """
    ...
```

Rules:
- All parameters (except `ctx`) appear in the tool's JSON schema
- Type annotations determine the schema types: `str`, `int`, `float`, `bool`, `list[dict]`, `list[str]`
- Default values make parameters optional
- `Optional[X]` or `X | None` marks a parameter as nullable

## Tool Return Types

Tools should return `str` for prose responses. FastMCP wraps them in `TextContent`.
Return plain text or markdown — Claude renders both well.

```python
# Good: markdown for structured output
return "\n".join(["## Today's Diary", "", f"  - {name}: {amount}g"])

# Good: simple status string
return f"Deleted diary entry {entry_id}."

# Avoid: returning raw dicts — they become JSON blobs Claude has to parse
```

## YAML-Backed Persistence

For local state that must survive process restarts (food database, meal templates),
use YAML files loaded at startup and written on mutation.

```python
# Load at startup (in lifespan or __init__)
with open(self._path) as f:
    raw = yaml.safe_load(f)

# Save after every mutation
def _save(self) -> None:
    with open(self._path, "w") as f:
        yaml.dump(out, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
```

The YAML file lives adjacent to the server script (e.g., `data/foods.yaml`).

## httpx Async Client

Use `httpx.AsyncClient` for all outbound HTTP. Initialize in lifespan, close in teardown.

```python
# In lifespan setup
client = httpx.AsyncClient(
    base_url=base_url,
    headers={
        "Authorization": f"Token {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    timeout=15.0,
)

# In lifespan teardown
await client.aclose()
```

Pagination helper (from wger-mcp):

```python
async def _get_all(self, path: str, params: dict | None = None) -> list[dict]:
    params = {**(params or {}), "format": "json", "limit": 100}
    results: list[dict] = []
    url = path
    while url:
        resp = await self._client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        next_url = data.get("next")
        if next_url:
            url = next_url.replace(self._base_url, "")
            params = {}
        else:
            url = None
    return results
```

## stdio Transport Config

Claude Desktop uses stdio transport exclusively. The server is launched as a subprocess;
stdin/stdout carry the MCP protocol. Never write to stdout for logging — use stderr.

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    stream=sys.stderr,   # CRITICAL: not stdout
)
```

## Claude Desktop config.json Registration

File location: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "wger-nutrition": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/server.py"],
      "env": {
        "WGER_URL": "http://192.168.50.248:8080",
        "WGER_TOKEN": "your-token-here"
      }
    }
  }
}
```

Use the venv Python, not a system Python, to ensure deps are available. Claude Desktop
must be restarted after any config change.

## Error Handling in Tools

Tools should return error strings rather than raise exceptions. Exceptions crash the
tool call and Claude gets a generic error message.

```python
@mcp.tool()
async def delete_entry(entry_id: int, ctx: Context = None) -> str:
    wger, _, _ = _state(ctx)
    try:
        await wger.delete_diary_entry(entry_id)
        return f"Deleted diary entry {entry_id}."
    except Exception as e:
        return f"Failed to delete entry {entry_id}: {e}"
```

Exception during lifespan setup (missing required env var) is acceptable — it prevents
a broken server from registering at all.

## Logging

Log to stderr at INFO level. FastMCP captures and forwards stderr to Claude Desktop's
MCP server logs (accessible via Claude Desktop developer tools).

```python
logger = logging.getLogger("wger-mcp")
logger.info("Server starting (wger_url=%s, foods=%d)", wger_url, len(food_db.all()))
logger.error("WGER_TOKEN environment variable is required")
```
