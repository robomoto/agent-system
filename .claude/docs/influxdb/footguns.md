# InfluxDB 1.x Footguns

## 1. Using influxdb-client (2.x) instead of influxdb (1.x)

**Problem:** There are two Python packages. `influxdb-client` is for InfluxDB 2.x and
uses Flux query language. This stack runs 1.11 — use the `influxdb` package (1.x client).

```bash
# WRONG — installs 2.x client
pip install influxdb-client

# RIGHT — installs 1.x client
pip install influxdb
```

The 2.x client uses `write_api`, `query_api`, bucket/org concepts. None of these exist
in 1.x.

## 2. Writing Flux queries against 1.x

**Problem:** InfluxDB 1.x does not support Flux. All queries must be InfluxQL.

```python
# WRONG — Flux syntax, doesn't work on 1.x
q = 'from(bucket: "health") |> range(start: -7d) |> filter(fn: (r) => r._measurement == "weight")'

# RIGHT — InfluxQL
q = "SELECT mean(value) FROM weight WHERE time > now() - 7d"
```

## 3. No UPDATE or DELETE by field value

**Problem:** InfluxDB 1.x has no `UPDATE` statement and cannot delete by field value —
only by time range or series.

```sql
-- This does NOT exist in InfluxQL
UPDATE weight SET value = 70.5 WHERE time = '...'

-- You can only delete entire series or time ranges
DROP SERIES FROM weight WHERE source = 'manual'
DELETE FROM weight WHERE time < now() - 365d
```

To correct a bad data point: write a new point at the same timestamp — InfluxDB 1.x
will overwrite it (last write wins for same measurement + tag set + timestamp).

## 4. Tag vs field: wrong choice kills query performance

**Problem:** Fields are not indexed. Filtering on a field requires a full scan.
Tags are indexed but must be strings and can't store high-cardinality values efficiently.

```python
# WRONG — device is used in WHERE clauses but stored as a field
{"fields": {"value": 70.5, "device": "withings"}}

# RIGHT — device is a tag (used for filtering/grouping)
{"tags": {"device": "withings"}, "fields": {"value": 70.5}}
```

Rules of thumb:
- Tag: dimensions you filter/group on (device, source, user_id)
- Field: the actual measured value (weight, heart_rate, steps)
- Never put high-cardinality values (timestamps, UUIDs) in tags

## 5. Time precision mismatch

**Problem:** InfluxDB defaults to nanosecond precision. Writing epoch seconds without
specifying precision creates wildly wrong timestamps.

```bash
# WRONG — InfluxDB interprets 1710000000 as nanoseconds (~1970-01-01 00:00:01)
POST /write?db=health
weight value=70.5 1710000000

# RIGHT — specify precision
POST /write?db=health&precision=s
weight value=70.5 1710000000
```

In the Python client:

```python
client.write_points(points, time_precision="s")  # or "ms", "u", "ns"
```

When querying, returned timestamps are also in nanoseconds by default. Use `epoch=s`
to get seconds back:

```
GET /query?db=health&epoch=s&q=SELECT+*+FROM+weight
```

## 6. GROUP BY time() requires WHERE time filter

**Problem:** `GROUP BY time()` without a `WHERE time` clause tries to aggregate all
time from epoch 0 to now, which is extremely slow and may hang.

```sql
-- WRONG — no time filter, will scan everything
SELECT mean(value) FROM weight GROUP BY time(1d)

-- RIGHT — always bound the time range
SELECT mean(value) FROM weight WHERE time > now() - 90d GROUP BY time(1d)
```

## 7. Missing fill() causes sparse data gaps in Grafana

**Problem:** When no data exists in a time bucket, `GROUP BY time()` omits that bucket
entirely. Grafana interprets this as a gap rather than connecting the line.

```sql
-- Gap in data = null in chart = broken line
SELECT mean(value) FROM weight GROUP BY time(1d)

-- fill(previous) carries forward the last known value
SELECT mean(value) FROM weight GROUP BY time(1d) fill(previous)

-- fill(none) omits empty buckets — correct for sparse event data
SELECT count(steps) FROM activity GROUP BY time(1d) fill(none)
```

## 8. Retention policy not set = data kept forever

**Problem:** The default retention policy (`autogen`) has infinite duration. On a home
server with limited disk, health metrics accumulate indefinitely.

**Fix:** Set retention policies when creating the database or afterwards:

```sql
ALTER RETENTION POLICY autogen ON garmin DURATION 52w REPLICATION 1
```

## 9. Confusing 1.x measurement with 2.x bucket

**Problem:** In 2.x documentation (which is everywhere), the equivalent of a 1.x
measurement+database is a "bucket". Don't use 2.x terminology or API patterns.

| 1.x concept | 2.x equivalent |
|-------------|----------------|
| database | bucket |
| measurement | measurement |
| retention policy | bucket retention |
| InfluxQL | Flux |
| `/query` HTTP endpoint | `/api/v2/query` |

## 10. HTTP API auth errors are silent 401s

**Problem:** If the InfluxDB HTTP API has auth enabled but the client sends no
credentials, it returns `401 Unauthorized` with a body that may look like success.
The Python client may silently return an empty result set rather than raising.

**Fix:** Always check `result.error` after queries, and configure auth explicitly.

```python
result = client.query("SELECT * FROM weight")
if result.error:
    raise RuntimeError(f"InfluxDB query failed: {result.error}")
```
