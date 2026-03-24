"""Base handoff schema shared by all agents."""

from enum import StrEnum

from pydantic import BaseModel, Field


class AgentName(StrEnum):
    """Core agents with dedicated schemas.

    Language/domain specialists (python-specialist, kotlin-specialist, etc.)
    are intentionally excluded — they use LanguageSpecialistHandoff via the
    dynamic '-specialist' suffix routing in validate.py.
    """

    LEAD = "lead"
    RESEARCHER = "researcher"
    ARCHITECT = "architect"
    IMPLEMENTER = "implementer"
    REVIEWER = "reviewer"
    VALIDATOR = "validator"
    UI_DESIGNER = "ui-designer"
    UX_DESIGNER = "ux-designer"
    COST_ACCOUNTANT = "cost-accountant"
    SRE = "sre"
    SYSADMIN = "sysadmin"
    CLAUDE_AI_SPECIALIST = "claude-ai-specialist"
    QA = "qa"
    TECHNICAL_WRITER = "technical-writer"
    ROSTER_CHECKER = "roster-checker"
    SOCIAL_PSYCHOLOGIST = "social-psychologist"
    EXPERIMENTAL_PSYCHOLOGIST = "experimental-psychologist"
    ACCESSIBILITY = "accessibility"
    MCP_SPECIALIST = "mcp-specialist"
    DATAVIZ_SPECIALIST = "dataviz-specialist"
    TRAUMA_INFORMED_DESIGN_SPECIALIST = "trauma-informed-design-specialist"


class Status(StrEnum):
    COMPLETED = "completed"
    BLOCKED = "blocked"
    NEEDS_INPUT = "needs-input"


class HandoffReport(BaseModel):
    """Base handoff report. Every agent's output extends this."""

    agent: str
    task_id: str
    status: Status
    summary: str = Field(min_length=1, max_length=2000)
    artifact_refs: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    token_usage: int = Field(default=0, ge=0)
