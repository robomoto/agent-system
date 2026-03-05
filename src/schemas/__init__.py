"""Agent handoff schemas.

Pydantic models defining the exact structure of every agent's output.
Use model_json_schema() to export JSON Schema for Claude's structured outputs.
"""

from src.schemas.base import HandoffReport, AgentName, Status
from src.schemas.agents import (
    ResearcherHandoff,
    ArchitectHandoff,
    ImplementerHandoff,
    ReviewerHandoff,
    ValidatorHandoff,
    UIDesignerHandoff,
    UXDesignerHandoff,
    CostAccountantHandoff,
    SREHandoff,
    SysadminHandoff,
    ClaudeAISpecialistHandoff,
    LanguageSpecialistHandoff,
)

__all__ = [
    "HandoffReport",
    "AgentName",
    "Status",
    "ResearcherHandoff",
    "ArchitectHandoff",
    "ImplementerHandoff",
    "ReviewerHandoff",
    "ValidatorHandoff",
    "UIDesignerHandoff",
    "UXDesignerHandoff",
    "CostAccountantHandoff",
    "SREHandoff",
    "SysadminHandoff",
    "ClaudeAISpecialistHandoff",
    "LanguageSpecialistHandoff",
]
