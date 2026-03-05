# Python Idioms Reference

## Version: Python 3.11+

### Data Modeling

**Pydantic v2 for validated models:**
```python
from pydantic import BaseModel, Field
from typing import Literal

class Handoff(BaseModel):
    status: Literal["completed", "blocked", "needs-input"]
    summary: str = Field(min_length=1, max_length=500)
    artifact_refs: list[str] = Field(default_factory=list)
```

**dataclasses for simple internal structs (no validation needed):**
```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
```

**When to use which:**
- External input / API boundaries → Pydantic (validates)
- Internal data passing → dataclass or NamedTuple (lightweight)
- Config → Pydantic with `model_config = ConfigDict(frozen=True)`

### Type Hints (3.11+)

```python
# Built-in generics (no import needed since 3.9)
items: list[str]
mapping: dict[str, int]
optional: str | None          # 3.10+ union syntax

# Literal for constrained values
from typing import Literal
severity: Literal["critical", "warning", "suggestion"]

# TypeAlias for readability
type FilePath = str            # 3.12+ type statement
from typing import TypeAlias
FilePath: TypeAlias = str      # 3.10-3.11

# Protocol for structural typing (duck typing with type safety)
from typing import Protocol
class Readable(Protocol):
    def read(self) -> str: ...
```

### Error Handling

```python
# Specific exceptions, not bare except
try:
    result = do_thing()
except ValueError as e:
    logger.warning("Invalid input: %s", e)
    return default_value
except (IOError, ConnectionError) as e:
    logger.error("External failure: %s", e)
    raise

# Custom exceptions inherit from domain-specific base
class AgentError(Exception): ...
class HandoffError(AgentError): ...
class ValidationError(AgentError): ...
```

### Iteration

```python
# Comprehensions for transforms
names = [user.name for user in users if user.active]

# Generators for large/lazy sequences
def read_chunks(path, size=8192):
    with open(path, "rb") as f:
        while chunk := f.read(size):
            yield chunk

# enumerate, zip, itertools over manual indexing
for i, item in enumerate(items):
    ...
for a, b in zip(list_a, list_b, strict=True):  # strict=True catches length mismatch
    ...
```

### Context Managers

```python
# For resource cleanup
from contextlib import contextmanager

@contextmanager
def temporary_config(key, value):
    old = config.get(key)
    config[key] = value
    try:
        yield
    finally:
        config[key] = old
```

### String Formatting

```python
# f-strings for interpolation (3.6+)
msg = f"Agent {name} completed task {task_id}"

# f-string debugging (3.8+)
print(f"{variable=}")  # prints "variable=value"

# .format() or % for log messages (avoid f-string evaluation cost)
logger.debug("Processing %s items", count)
```

### Path Handling

```python
from pathlib import Path

config_dir = Path.home() / ".claude" / "agents"
for agent_file in config_dir.glob("*.md"):
    content = agent_file.read_text()
```
