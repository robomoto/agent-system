# MCP Footguns — Common Mistakes

## 1. Writing to stdout

**Problem:** Any `print()` or `logging` to stdout corrupts the MCP protocol stream. The
stdio transport uses stdout exclusively for JSON-RPC messages.

**Fix:** Always log to stderr.

```python
# WRONG
print("Server starting")
logging.basicConfig(stream=sys.stdout)

# RIGHT
logging.basicConfig(stream=sys.stderr)
```

## 2. Blocking I/O in async tools

**Problem:** Calling synchronous blocking functions (file I/O, `requests`, `time.sleep`)
inside async tool handlers blocks the event loop and freezes the MCP server.

**Fix:** Use async equivalents or run blocking code in a thread pool.

```python
# WRONG
@mcp.tool()
async def fetch_data(url: str) -> str:
    import requests
    return requests.get(url).text  # blocks the event loop

# RIGHT
@mcp.tool()
async def fetch_data(url: str) -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.text
```

File I/O in `FoodDB._save()` is synchronous but is fast (small YAML file) — acceptable
for this use case. For large files, use `asyncio.to_thread()`.

## 3. Missing type hints on tool parameters

**Problem:** FastMCP derives the JSON schema from type annotations. Missing annotations
mean Claude receives `{}` (any) for that parameter — it will guess wrong types.

**Fix:** Always annotate every non-`ctx` parameter.

```python
# WRONG — Claude doesn't know what type 'amount' is
@mcp.tool()
async def log_meal(items, amount=None, ctx: Context = None) -> str: ...

# RIGHT
@mcp.tool()
async def log_meal(items: list[dict], amount: float | None = None, ctx: Context = None) -> str: ...
```

## 4. Oversized tool results

**Problem:** Claude Desktop has a context window. Tool results that return large JSON
dumps (hundreds of items, full API responses) waste context and slow responses.

**Fix:** Summarize, paginate, or truncate in the tool itself.

```python
# WRONG — returns all 500 diary entries
return str(await wger.get_all_diary_entries())

# RIGHT — filter to today, return formatted summary
entries = await wger.get_diary_today()  # already filtered
return "\n".join([f"  - {e['name']}: {e['amount']}g" for e in entries])
```

## 5. Tool name collisions across servers

**Problem:** If two MCP servers (registered in config.json) expose a tool with the same
name, Claude will call one unpredictably or refuse both.

**Fix:** Use server-scoped names or namespace the tools.

```json
{
  "mcpServers": {
    "wger-nutrition": { ... },
    "influx-health": { ... }
  }
}
```

If both servers had a `search` tool, rename them `search_food` and `search_metrics`.

## 6. Creating a new HTTP client per tool call

**Problem:** Instantiating `httpx.AsyncClient` inside a tool handler creates a new
connection pool on every call. This is slow and leaks resources.

**Fix:** Create the client once in `lifespan`, inject via `Context`.

```python
# WRONG
@mcp.tool()
async def get_data(ctx: Context = None) -> str:
    async with httpx.AsyncClient() as client:  # new client per call
        ...

# RIGHT — client created in lifespan, reused across calls
@mcp.tool()
async def get_data(ctx: Context = None) -> str:
    client = ctx.request_context.lifespan_context["client"]
    ...
```

## 7. Missing error context in tool returns

**Problem:** Returning bare `"Error"` or `str(e)` gives Claude nothing to act on.

**Fix:** Include what failed, what was attempted, and what the user can try.

```python
# WRONG
except Exception as e:
    return "Error"

# RIGHT
except Exception as e:
    return f"Failed to fetch ingredient {wger_id} from wger: {e}. Check that WGER_URL is reachable."
```

## 8. Not validating required env vars at startup

**Problem:** A server that starts without required secrets will fail on the first tool
call with a confusing error. Claude reports it as a tool failure, not a config issue.

**Fix:** Validate in lifespan and raise early.

```python
@asynccontextmanager
async def lifespan(server: FastMCP):
    token = os.environ.get("WGER_TOKEN", "")
    if not token:
        logger.error("WGER_TOKEN environment variable is required")
        raise RuntimeError("WGER_TOKEN not set")
    ...
```

## 9. Forgetting that Desktop relaunches the server per session

**Problem:** Claude Desktop starts the MCP server process fresh for each conversation
(or on demand). Any in-memory state that isn't persisted to disk is lost between sessions.

**Fix:** Persist anything that should survive process restarts. The wger-mcp pattern:
- `data/foods.yaml` — food cache (write on `add_food`)
- `data/standards.yaml` — meal templates (write on `create_standard` / `update_standard`)
- wger API itself — authoritative diary state

## 10. Docstring quality determines Claude's tool selection

**Problem:** Vague or missing docstrings cause Claude to call the wrong tool or skip a
tool that would have been perfect.

**Fix:** Write docstrings from Claude's perspective — what does this do, when should it
be used, what are the key parameters?

```python
# WRONG
async def log_meal(items: list[dict], ctx: Context = None) -> str:
    """Log meal."""
    ...

# RIGHT
async def log_meal(items: list[dict], meal_name: str = "Logged", ctx: Context = None) -> str:
    """Log food items to the wger nutrition diary.

    Each item needs: {"food": "food_key_from_local_db", "amount_g": grams}.
    If amount_g is omitted, the food's default_amount_g is used.
    The meal_name groups entries (e.g. "Breakfast", "Lunch", "Snack").
    """
    ...
```
