<!-- last_verified: 2026-03-04 -->
# Python Standard Library Reference

Modules we commonly use in the agent system.

## pathlib — Path handling

```python
from pathlib import Path

path = Path("src/schemas")
path.exists()
path.is_file()
path.is_dir()
path.read_text(encoding="utf-8")
path.write_text(content, encoding="utf-8")
path.glob("*.py")          # non-recursive
path.rglob("*.py")         # recursive
path.parent                # parent directory
path.stem                  # filename without extension
path.suffix                # extension including dot
path / "subdir" / "file"   # join paths
```

## json — JSON encoding/decoding

```python
import json

# Parse
data = json.loads(json_string)
data = json.load(file_handle)

# Serialize
json_str = json.dumps(data, indent=2, default=str)  # default=str handles datetime etc.
json.dump(data, file_handle, indent=2)

# For Pydantic models, use model methods instead:
model.model_dump_json(indent=2)
Model.model_validate_json(json_string)
```

## logging — Structured logging

```python
import logging

logger = logging.getLogger(__name__)

# Use % formatting in log calls (deferred evaluation)
logger.info("Processing %s items for agent %s", count, agent_name)
logger.error("Failed to validate handoff: %s", error, exc_info=True)

# JSON structured logging with dictConfig
logging.config.dictConfig({
    "version": 1,
    "handlers": {
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json"
        }
    },
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    }
})
```

## typing — Type hints

```python
from typing import (
    Literal,      # constrained string/int values
    TypeAlias,    # readable type aliases (3.10+)
    Protocol,     # structural subtyping
    TypeVar,      # generic type variables
    Annotated,    # attach metadata to types
    Self,         # return type for fluent interfaces (3.11+)
)

# Key Pydantic-compatible types
from pydantic import Field, field_validator, model_validator
from pydantic import ConfigDict  # replaces Config class in v2
```

## enum — Enumerations

```python
from enum import Enum, StrEnum

# StrEnum (3.11+) — values are strings, serialize naturally to JSON
class Severity(StrEnum):
    CRITICAL = "critical"
    WARNING = "warning"
    SUGGESTION = "suggestion"

# Use with Pydantic
class Finding(BaseModel):
    severity: Severity  # validates and serializes as string
```

## subprocess — External commands

```python
import subprocess

# Preferred: capture output, check for errors
result = subprocess.run(
    ["ruff", "check", file_path],
    capture_output=True,
    text=True,
    timeout=30,
)
if result.returncode != 0:
    print(result.stderr)

# NEVER use shell=True with user input (command injection)
```

## Pydantic v2 — Data validation (third-party, core to this project)

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Literal

class HandoffReport(BaseModel):
    agent: str
    task_id: str
    status: Literal["completed", "blocked", "needs-input"]
    summary: str = Field(min_length=1, max_length=1000)
    artifact_refs: list[str] = Field(default_factory=list)

    @field_validator("agent")
    @classmethod
    def agent_must_be_known(cls, v):
        known = {"researcher", "implementer", "reviewer", "validator", ...}
        if v not in known:
            raise ValueError(f"Unknown agent: {v}")
        return v

    # Export JSON Schema for Claude structured outputs
    schema = HandoffReport.model_json_schema()
```
