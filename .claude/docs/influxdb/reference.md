<!-- last_verified: 2026-03-14 -->
# InfluxDB 1.x Reference

This stack runs InfluxDB 1.11 (not 2.x). Use InfluxQL, not Flux.

## Data Model

| Concept | Description |
|---------|-------------|
| **measurement** | Analogous to a table name (e.g., `weight`, `heart_rate`) |
| **tag** | Indexed string key-value, used for filtering/grouping (e.g., `device=garmin`) |
| **field** | Non-indexed numeric or string value (e.g., `value=70.5`) |
| **timestamp** | Nanosecond precision by default |

Tags are indexed and should be used for dimensions you filter or group on.
Fields are not indexed and hold the actual measurements.

## HTTP API Endpoints

Base: `http://influxdb:8086` (internal Docker network) or `http://192.168.50.248:8086` (LAN)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/query` | GET/POST | Run InfluxQL SELECT, SHOW queries |
| `/write` | POST | Write line protocol data |
| `/ping` | GET | Health check (returns 204) |
| `/health` | GET | Health JSON |

### Query

```
GET /query?db=mydb&q=SELECT+*+FROM+measurement
```

With authentication (if enabled):
```
GET /query?db=mydb&u=user&p=pass&q=...
```

Or via Basic Auth header.

### Write (Line Protocol)

```
POST /write?db=mydb&precision=s
Content-Type: text/plain

weight,device=withings value=70.5 1710000000
```

Line protocol format: `measurement[,tag=val ...] field=val[,...] [unix_timestamp]`

## InfluxQL Queries

### Basic SELECT

```sql
SELECT * FROM weight WHERE time > now() - 30d

SELECT mean(value) FROM heart_rate
WHERE time > now() - 7d
GROUP BY time(1h)

SELECT MAX(value), MIN(value), MEAN(value)
FROM weight
WHERE time >= '2025-01-01' AND time < '2025-02-01'
ORDER BY time ASC
```

### Time Range Patterns

```sql
-- Relative
WHERE time > now() - 7d
WHERE time > now() - 24h
WHERE time > now() - 1h

-- Absolute (RFC3339 or epoch)
WHERE time >= '2025-01-01T00:00:00Z' AND time < '2025-02-01T00:00:00Z'
```

### GROUP BY time()

```sql
SELECT mean(value) FROM weight
GROUP BY time(1d) fill(none)

SELECT mean(value) FROM heart_rate
GROUP BY time(1h) fill(null)

-- fill options: none (omit empty), null (null for empty), 0, linear, previous
```

### SHOW Commands

```sql
SHOW DATABASES
SHOW MEASUREMENTS
SHOW FIELD KEYS FROM weight
SHOW TAG KEYS FROM weight
SHOW TAG VALUES FROM weight WITH KEY = "device"
SHOW RETENTION POLICIES
```

## Python Client (influxdb-python)

Package: `influxdb` (1.x client — NOT `influxdb-client` which is 2.x)

```python
from influxdb import InfluxDBClient

client = InfluxDBClient(
    host="influxdb",
    port=8086,
    username="admin",
    password="secret",
    database="health",
)

# Query
result = client.query("SELECT mean(value) FROM weight WHERE time > now() - 30d GROUP BY time(1d)")
points = list(result.get_points())

# Write
client.write_points([
    {
        "measurement": "weight",
        "tags": {"source": "withings"},
        "time": "2025-01-15T08:00:00Z",
        "fields": {"value": 70.5, "fat_ratio": 18.2},
    }
])
```

## Databases in This Stack

| Database | Used By | Key Measurements |
|----------|---------|-----------------|
| `garmin` | garmin-fetch-data | `heart_rate`, `steps`, `sleep`, `stress` |
| `withings` [UNVERIFIED] | withings-bridge | `weight`, `fat_ratio`, `muscle_mass` |

Grafana datasources are provisioned from `garmin-grafana/datasources/`.

## Retention Policies

```sql
-- View current retention policies
SHOW RETENTION POLICIES ON garmin

-- Create (default keeps forever if not set)
CREATE RETENTION POLICY "one_year" ON garmin DURATION 52w REPLICATION 1 DEFAULT
```

Default retention policy is `autogen` with infinite duration unless configured.

## Aggregation Functions

```sql
MEAN(field)     -- arithmetic mean
MEDIAN(field)   -- median value
MODE(field)     -- most frequent value
SUM(field)      -- sum
COUNT(field)    -- number of non-null values
FIRST(field)    -- first value in time range
LAST(field)     -- last value in time range
MAX(field)      -- maximum
MIN(field)      -- minimum
STDDEV(field)   -- standard deviation
SPREAD(field)   -- max - min
```

## Backup

InfluxDB 1.x backup:

```bash
influxd backup -portable /backup/path
# or for a single database:
influxd backup -portable -database garmin /backup/path
```

The stack's `scripts/backup.sh` handles this weekly.
