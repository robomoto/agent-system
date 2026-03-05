# Python Footguns

Common mistakes that silently produce wrong results or cause subtle bugs.

## Mutable Default Arguments

```python
# BAD — list is shared across all calls
def add_item(item, items=[]):
    items.append(item)
    return items

# GOOD
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

# GOOD (Pydantic/dataclass)
items: list[str] = Field(default_factory=list)
```

## Late Binding Closures

```python
# BAD — all lambdas capture i=4
funcs = [lambda: i for i in range(5)]
[f() for f in funcs]  # [4, 4, 4, 4, 4]

# GOOD — capture current value
funcs = [lambda i=i: i for i in range(5)]
[f() for f in funcs]  # [0, 1, 2, 3, 4]
```

## is vs ==

```python
# BAD — `is` checks identity, not equality
if x is True:    # fails for truthy non-True values
if x is 1:       # CPython caches small ints, but this is implementation detail

# GOOD
if x == 1:       # value comparison
if x is None:    # None is a singleton, `is` is correct here
```

## Dictionary Iteration During Modification

```python
# BAD — RuntimeError: dictionary changed size during iteration
for key in d:
    if should_remove(key):
        del d[key]

# GOOD
keys_to_remove = [k for k in d if should_remove(k)]
for key in keys_to_remove:
    del d[key]

# GOOD (Python 3.12+ or any version with copy)
for key in list(d):
    if should_remove(key):
        del d[key]
```

## Shallow Copy Surprises

```python
# BAD — nested lists are shared
original = [[1, 2], [3, 4]]
copy = original.copy()  # or original[:]
copy[0].append(5)
print(original)  # [[1, 2, 5], [3, 4]] — modified!

# GOOD
import copy
deep = copy.deepcopy(original)
```

## Global Interpreter Lock (GIL)

```python
# BAD — threads don't help CPU-bound work
from threading import Thread
# These run sequentially due to GIL
threads = [Thread(target=cpu_heavy, args=(chunk,)) for chunk in data]

# GOOD — use multiprocessing for CPU-bound
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as pool:
    results = pool.map(cpu_heavy, data)

# Threads ARE useful for I/O-bound work (network, file I/O)
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as pool:
    results = pool.map(fetch_url, urls)
```

## except Exception vs except BaseException

```python
# BAD — catches KeyboardInterrupt and SystemExit
try:
    work()
except:           # bare except = except BaseException
    pass

# BAD — also catches KeyboardInterrupt
try:
    work()
except BaseException:
    pass

# GOOD — lets KeyboardInterrupt and SystemExit propagate
try:
    work()
except Exception as e:
    handle(e)
```

## String Concatenation in Loops

```python
# BAD — O(n^2) because strings are immutable
result = ""
for item in items:
    result += str(item) + ", "

# GOOD — O(n)
result = ", ".join(str(item) for item in items)
```

## datetime Timezone Pitfalls

```python
# BAD — naive datetime, ambiguous timezone
from datetime import datetime
now = datetime.now()  # no timezone info

# GOOD — always use timezone-aware datetimes
from datetime import datetime, timezone
now = datetime.now(timezone.utc)

# GOOD (3.11+ with zoneinfo)
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("America/New_York"))
```

## Pydantic v2 Migration Gotchas

```python
# v1 → v2 breaking changes:
# .dict() → .model_dump()
# .json() → .model_dump_json()
# .schema() → .model_json_schema()
# .parse_obj() → .model_validate()
# @validator → @field_validator (with mode="before"|"after")
# Config class → model_config = ConfigDict(...)
# orm_mode → from_attributes
```
