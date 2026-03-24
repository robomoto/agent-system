<!-- last_verified: 2026-03-14 -->
# wger REST API v2 Reference

wger is the workout + nutrition tracking service running at `http://192.168.50.248:8080`.

## Authentication

Token authentication. Get a token from the wger UI under Account → API.

```http
Authorization: Token <token>
Accept: application/json
Content-Type: application/json
```

## Base URL

`http://192.168.50.248:8080/api/v2/`

All endpoints are under `/api/v2/`. The UI is at `:8080`.

## Pagination

All list endpoints return paginated responses:

```json
{
  "count": 142,
  "next": "http://192.168.50.248:8080/api/v2/nutritiondiary/?limit=100&offset=100",
  "previous": null,
  "results": [...]
}
```

Fetch all pages:

```python
params = {"format": "json", "limit": 100}
results = []
url = "/api/v2/endpoint/"
while url:
    resp = await client.get(url, params=params)
    data = resp.json()
    results.extend(data["results"])
    next_url = data.get("next")
    url = next_url.replace(base_url, "") if next_url else None
    params = {}  # next_url already has query params encoded
```

## Key Endpoints

### Nutrition Plan

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v2/nutritionplan/` | List all plans |
| POST | `/api/v2/nutritionplan/` | Create a plan |
| GET | `/api/v2/nutritionplan/{id}/` | Get single plan |

Plan fields: `id`, `description`, `only_logging`, `goal_energy`, `goal_protein`,
`goal_carbohydrates`, `goal_fat`, `goal_fiber`.

Important: `plans[-1]` is the most recently created plan — use as "active" plan.

### Meal (grouping construct within a plan)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v2/meal/` | List meals across all plans |
| POST | `/api/v2/meal/` | Create a meal |

Meal fields: `id`, `plan` (int, plan ID), `name` (str), `time` (nullable).

Meals are grouping labels for diary entries (e.g., "Breakfast", "Lunch"). The wger-mcp
server creates meals on demand and caches their IDs.

### Nutrition Diary

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v2/nutritiondiary/` | List diary entries |
| POST | `/api/v2/nutritiondiary/` | Create an entry |
| DELETE | `/api/v2/nutritiondiary/{id}/` | Delete an entry |

POST body:

```json
{
  "plan": 1,
  "meal": 5,
  "ingredient": 1234,
  "amount": "150.0",
  "weight_unit": null,
  "datetime": "2025-01-15T08:30:00+00:00"
}
```

Response fields include `energy`, `protein`, `carbohydrates`, `fat`, `fiber` (computed
from ingredient macros × amount/100).

Filter by date: `?ordering=-datetime` then filter client-side by `datetime` prefix.

### Ingredient (food item)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v2/ingredient/` | Search/list ingredients |
| GET | `/api/v2/ingredient/{id}/` | Get single ingredient |

Search parameters:

```python
params = {
    "name__search": "greek yogurt",  # full-text search on name
    "language__code": "en",          # filter to English entries
    "format": "json",
    "limit": 10,
}
```

Ingredient fields: `id`, `name`, `energy` (kcal per 100g), `protein`, `carbohydrates`,
`fat`, `fiber`, `sugar`, `saturated_fat`.

Note: `energy` is the field name (not `calories`). Map it:

```python
{
    "wger_id": r["id"],
    "calories": float(r.get("energy") or 0),
    "protein": float(r.get("protein") or 0),
    "carbs": float(r.get("carbohydrates") or 0),
    "fat": float(r.get("fat") or 0),
    "fiber": float(r.get("fiber") or 0),
}
```

### Exercise

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v2/exercise/` | List exercises |
| GET | `/api/v2/exerciseinfo/{id}/` | Get exercise with translations |
| GET | `/api/v2/exercisecategory/` | List categories |

Exercise translation pattern: exercises have a separate `ExerciseTranslation` model.
Use `/api/v2/exerciseinfo/{id}/` which returns translations inline.

For English: `language=2` (language ID for English on wger.de; may differ on local
instances after sync).

### Workout + Workout Log

| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/api/v2/workout/` | Workout sessions |
| GET/POST | `/api/v2/workoutsession/` | Session with date, notes, impression |
| GET/POST | `/api/v2/workoutlog/` | Individual exercise log entries |

Workout log fields: `exercise`, `reps`, `sets`, `weight`, `workout`.

### Measurement

| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/api/v2/measurement-category/` | Measurement categories |
| GET/POST | `/api/v2/measurement/` | Individual measurements |

Must create a category first, then log measurements to it.

### Body Weight

| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/api/v2/weightentry/` | Body weight entries |

Fields: `date` (YYYY-MM-DD), `weight` (decimal string).

The withings-bridge writes to this endpoint when syncing scale data.

## Common Patterns

### Ensure active plan exists

```python
plans = await get_all("/api/v2/nutritionplan/")
if plans:
    plan_id = plans[-1]["id"]
else:
    plan = await post("/api/v2/nutritionplan/", {"description": "MCP log", "only_logging": True})
    plan_id = plan["id"]
```

### Get or create a named meal

```python
meals = await get_all("/api/v2/meal/")
existing = next((m for m in meals if m["name"].lower() == name.lower()), None)
if existing:
    meal_id = existing["id"]
else:
    meal = await post("/api/v2/meal/", {"plan": plan_id, "name": name})
    meal_id = meal["id"]
```

### Filter diary entries to today

```python
today = datetime.now().strftime("%Y-%m-%d")
all_entries = await get_all("/api/v2/nutritiondiary/", {"ordering": "-datetime"})
today_entries = [e for e in all_entries if e["datetime"].startswith(today)]
```
