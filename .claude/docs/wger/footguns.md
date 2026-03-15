# wger API Footguns

## 1. Single active nutrition plan per user

**Problem:** wger doesn't have a concept of a "currently active" plan — it just has a
list of plans. If you create a new plan on every server restart, you'll accumulate plans
and diary entries will scatter across them.

**Fix:** Always check for existing plans first. The wger-mcp pattern: take `plans[-1]`
(most recently created) as the active plan and cache its ID in-process.

```python
plans = await get_all("/api/v2/nutritionplan/")
plan_id = plans[-1]["id"] if plans else (await create_plan())["id"]
```

The MCP server caches `_plan_id` in the `WgerClient` instance — valid for the process
lifetime. On restart, re-fetches once.

## 2. Diary entry requires a Meal object, not just a name

**Problem:** `POST /api/v2/nutritiondiary/` requires a `meal` field with a Meal object
ID. You can't just pass a meal name string. A Meal object must be created under the
nutrition plan first.

**Fix:** Always `get_or_create_meal(name)` before logging a diary entry.

```python
# WRONG — meal is a name string
await post("/api/v2/nutritiondiary/", {"plan": plan_id, "meal": "Breakfast", ...})

# RIGHT — meal is a Meal object ID
meal_id = await get_or_create_meal("Breakfast")  # creates if not exists
await post("/api/v2/nutritiondiary/", {"plan": plan_id, "meal": meal_id, ...})
```

## 3. Ingredient energy field is named "energy", not "calories"

**Problem:** The API uses `energy` for the calorie field, not `calories`. Callers who
guess `calories` get `None` and silently log 0 kcal.

```python
# WRONG
calories = ingredient["calories"]

# RIGHT
calories = float(ingredient.get("energy") or 0)
```

Similarly, carbohydrates is `carbohydrates` (not `carbs`), and there's no top-level
`macros` object.

## 4. Ingredient IDs are instance-specific after sync

**Problem:** Ingredient IDs on a local wger instance are assigned during the
`sync-ingredients` import and differ from IDs on wger.de or other instances. A
`wger_id` hard-coded from wger.de will fail on your instance.

**Fix:** Always verify IDs against your instance. The `scripts/verify_foods.py` script
does this. Never copy IDs from wger.de documentation or other instances.

The `data/foods.yaml` in wger-mcp stores instance-specific IDs. Run
`scripts/verify_foods.py` after any re-sync or fresh instance setup.

## 5. Exercise search vs exercise list

**Problem:** `/api/v2/exercise/` returns Exercise base objects without translations
(just IDs). The `name` field is absent at this level.

**Fix:** Use `/api/v2/exerciseinfo/{id}/` to get an exercise with translations, or
search via the translated exercise endpoint.

```python
# WRONG — returns Exercise objects without human-readable names
exercises = await get_all("/api/v2/exercise/")

# RIGHT — returns exercises with names via translations
info = await get(f"/api/v2/exerciseinfo/{exercise_id}/")
name = info["translations"][0]["name"]  # first translation
```

## 6. Measurement categories must exist before logging

**Problem:** Like Meals for diary entries, Measurements require a MeasurementCategory
to exist first. You cannot log a measurement without a category ID.

```python
# WRONG — category doesn't exist yet
await post("/api/v2/measurement/", {"category": "Body Fat", "value": 18.2})

# RIGHT — create category first, then log
cat = await post("/api/v2/measurement-category/", {"name": "Body Fat", "unit": "%"})
await post("/api/v2/measurement/", {"category": cat["id"], "date": "2025-01-15", "value": 18.2})
```

## 7. Pagination: don't assume one page returns everything

**Problem:** List endpoints return at most 100 items per page (with `limit=100`).
Fetching only the first page silently misses older entries.

**Fix:** Always paginate with `get_all()` helper. The wger-mcp implementation follows
the `next` URL until it's null.

```python
# WRONG — gets only first 20 diary entries (default limit)
resp = await client.get("/api/v2/nutritiondiary/")
entries = resp.json()["results"]

# RIGHT — follows all pages
entries = await get_all("/api/v2/nutritiondiary/", {"ordering": "-datetime"})
```

## 8. amount in diary entry must be a string, not a float

**Problem:** The `amount` field in `POST /api/v2/nutritiondiary/` expects a decimal
string, not a float. Sending a float may cause validation errors or rounding issues.

```python
# WRONG
{"amount": 150.0}

# RIGHT
{"amount": str(round(amount_g, 1))}  # e.g. "150.0"
```

## 9. Meal cache is per-process, not per-plan

**Problem:** If meals from a previous plan have the same name as meals in a new plan,
a stale meal cache will serve the wrong meal ID.

**Fix:** Cache meals by `(plan_id, name)` key, or clear the cache when the plan ID
changes.

```python
# FRAGILE — if plan_id changes, cache returns wrong meal IDs
self._meal_cache: dict[str, int] = {}

# SAFER — scope cache to plan
self._meal_cache: dict[tuple[int, str], int] = {}
# key: (plan_id, meal_name.lower())
```

## 10. Token auth vs session auth

**Problem:** wger supports both token auth and session (cookie) auth. The REST API
uses token auth. The Django admin and some UI endpoints use session auth. Mixing them
won't work.

**Fix:** For all API calls, always pass the `Authorization: Token <token>` header.
Never try to use session cookies for API calls.

```python
headers = {
    "Authorization": f"Token {token}",
    "Accept": "application/json",
}
```

Get your API token from: wger UI → Account (top right) → Switch to API tab → Token.
Or generate one via `manage.py drf_create_token <username>`.
