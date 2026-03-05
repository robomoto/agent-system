"""Base handoff schema shared by all agents."""

from enum import StrEnum

from pydantic import BaseModel, Field


class AgentName(StrEnum):
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
