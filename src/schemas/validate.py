"""Validate a handoff report against its agent's schema.

Usage:
    python -m src.schemas.validate '{"agent": "researcher", ...}'
    echo '{"agent": "reviewer", ...}' | python -m src.schemas.validate

Returns exit code 0 if valid, 1 if invalid (with error details on stderr).
Used by validation hooks to check agent output conformance.
"""

import json
import sys

from pydantic import ValidationError

from src.schemas.agents import (
    ArchitectHandoff,
    ClaudeAISpecialistHandoff,
    CostAccountantHandoff,
    ImplementerHandoff,
    LanguageSpecialistHandoff,
    ResearcherHandoff,
    ReviewerHandoff,
    SREHandoff,
    SysadminHandoff,
    UIDesignerHandoff,
    UXDesignerHandoff,
    ValidatorHandoff,
)

SCHEMA_MAP = {
    "researcher": ResearcherHandoff,
    "architect": ArchitectHandoff,
    "implementer": ImplementerHandoff,
    "reviewer": ReviewerHandoff,
    "validator": ValidatorHandoff,
    "ui-designer": UIDesignerHandoff,
    "ux-designer": UXDesignerHandoff,
    "cost-accountant": CostAccountantHandoff,
    "sre": SREHandoff,
    "sysadmin": SysadminHandoff,
    "claude-ai-specialist": ClaudeAISpecialistHandoff,
    "language-specialist": LanguageSpecialistHandoff,
}


def validate_handoff(raw: str) -> tuple[bool, str]:
    """Validate a JSON handoff report. Returns (is_valid, message)."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"

    agent = data.get("agent")
    if not agent:
        return False, "Missing 'agent' field"

    # Language specialists have dynamic agent names
    model_cls = SCHEMA_MAP.get(agent)
    if model_cls is None and "-specialist" in agent:
        model_cls = LanguageSpecialistHandoff

    if model_cls is None:
        return False, f"Unknown agent: {agent}"

    try:
        model_cls.model_validate(data)
        return True, f"Valid {agent} handoff"
    except ValidationError as e:
        return False, f"Validation errors for {agent}:\n{e}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raw_input = sys.argv[1]
    else:
        raw_input = sys.stdin.read()

    valid, message = validate_handoff(raw_input)
    if valid:
        print(message)
        sys.exit(0)
    else:
        print(message, file=sys.stderr)
        sys.exit(1)
