"""Agent-specific handoff schemas.

Each schema extends HandoffReport with fields specific to that agent's output.
Use .model_json_schema() on any model to export JSON Schema for Claude's
structured outputs with strict: true.
"""

from typing import Literal

from pydantic import BaseModel, Field

from src.schemas.base import HandoffReport, Status


# --- Researcher ---


class ResearcherHandoff(HandoffReport):
    agent: Literal["researcher"] = "researcher"
    patterns_found: list[str] = Field(default_factory=list)


# --- Architect ---


class DesignOption(BaseModel):
    option: str
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    risk: Literal["low", "medium", "high"]


class DesignSpec(BaseModel):
    approach: str
    components: list[str] = Field(default_factory=list)
    contracts: list[str] = Field(default_factory=list)
    data_flow: str = ""


class ArchitectHandoff(HandoffReport):
    agent: Literal["architect"] = "architect"
    design: DesignSpec
    options_considered: list[DesignOption] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


# --- Implementer ---


class FileChange(BaseModel):
    path: str
    action: Literal["created", "modified", "deleted"]
    description: str


class TestInfo(BaseModel):
    path: str
    count: int = Field(ge=0)
    description: str


class TestResults(BaseModel):
    passed: int = Field(ge=0)
    failed: int = Field(ge=0)
    skipped: int = Field(ge=0)


class ImplementerHandoff(HandoffReport):
    agent: Literal["implementer"] = "implementer"
    files_changed: list[FileChange] = Field(default_factory=list)
    tests_added: list[TestInfo] = Field(default_factory=list)
    test_results: TestResults | None = None
    spec_deviations: list[str] = Field(default_factory=list)


# --- Reviewer ---


class ReviewFinding(BaseModel):
    severity: Literal["critical", "warning", "suggestion"]
    category: Literal[
        "security", "correctness", "performance", "maintainability", "testing"
    ]
    location: str
    description: str
    suggested_fix: str
    adversarial_note: str = ""


class TestVerification(BaseModel):
    passed: bool
    details: str


class ReviewerHandoff(HandoffReport):
    agent: Literal["reviewer"] = "reviewer"
    status: Literal["approved", "changes-requested", "blocked"]  # type: ignore[assignment]
    findings: list[ReviewFinding] = Field(default_factory=list)
    tests_verified: TestVerification | None = None


# --- Validator ---


class Assertion(BaseModel):
    claim: str
    test_method: str
    expected: str
    actual: str
    passed: bool
    evidence: str = ""


class TestSuiteResults(BaseModel):
    command: str
    passed: int = Field(ge=0)
    failed: int = Field(ge=0)
    skipped: int = Field(ge=0)
    duration_ms: int = Field(ge=0)


class ValidatorHandoff(HandoffReport):
    agent: Literal["validator"] = "validator"
    status: Literal["validated", "failed", "blocked"]  # type: ignore[assignment]
    assertions: list[Assertion] = Field(default_factory=list)
    test_suite_results: TestSuiteResults | None = None
    regressions_found: list[str] = Field(default_factory=list)


# --- UI Designer ---


class ComponentSpec(BaseModel):
    name: str
    variants: list[str] = Field(default_factory=list)
    states: list[str] = Field(default_factory=list)
    props: dict[str, str] = Field(default_factory=dict)
    responsive: str = ""


class UIDesignerHandoff(HandoffReport):
    agent: Literal["ui-designer"] = "ui-designer"
    components: list[ComponentSpec] = Field(default_factory=list)
    design_tokens: list[str] = Field(default_factory=list)
    accessibility: list[str] = Field(default_factory=list)
    files_changed: list[FileChange] = Field(default_factory=list)


# --- UX Designer ---


class UserFlow(BaseModel):
    name: str
    steps: list[str] = Field(default_factory=list)
    happy_path: str = ""
    error_paths: list[str] = Field(default_factory=list)
    edge_cases: list[str] = Field(default_factory=list)


class HeuristicViolation(BaseModel):
    heuristic: str
    issue: str
    recommendation: str


class UXDesignerHandoff(HandoffReport):
    agent: Literal["ux-designer"] = "ux-designer"
    flows: list[UserFlow] = Field(default_factory=list)
    heuristic_violations: list[HeuristicViolation] = Field(default_factory=list)


# --- Cost Accountant ---


class AgentCostEstimate(BaseModel):
    agent: str
    model: Literal["haiku", "sonnet", "opus"]
    est_tokens: int = Field(ge=0)
    est_cost_usd: float = Field(ge=0)


class AICosts(BaseModel):
    by_agent: list[AgentCostEstimate] = Field(default_factory=list)
    total_est_usd: float = Field(ge=0)
    optimization_recommendations: list[str] = Field(default_factory=list)


class CloudService(BaseModel):
    service: str
    purpose: str
    tier: str = ""
    pricing_model: str = ""
    projected_monthly_usd: float = Field(ge=0)
    free_tier: str = ""
    confidence: Literal["high", "medium", "low"]
    source: str = ""


class CloudCosts(BaseModel):
    services: list[CloudService] = Field(default_factory=list)
    total_monthly_usd: float = Field(ge=0)
    total_annual_usd: float = Field(ge=0)
    risks: list[str] = Field(default_factory=list)


class CostAccountantHandoff(HandoffReport):
    agent: Literal["cost-accountant"] = "cost-accountant"
    ai_costs: AICosts | None = None
    cloud_costs: CloudCosts | None = None


# --- SRE ---


class SLO(BaseModel):
    metric: str
    target: str
    measurement: str


class Alert(BaseModel):
    name: str
    condition: str
    severity: Literal["page", "ticket"]
    runbook: str = ""


class SREHandoff(HandoffReport):
    agent: Literal["sre"] = "sre"
    slos: list[SLO] = Field(default_factory=list)
    alerts: list[Alert] = Field(default_factory=list)
    monitoring: list[str] = Field(default_factory=list)
    reliability_patterns: list[str] = Field(default_factory=list)
    files_changed: list[FileChange] = Field(default_factory=list)


# --- Sysadmin ---


class InfrastructureSpec(BaseModel):
    services_configured: list[str] = Field(default_factory=list)
    networking: list[str] = Field(default_factory=list)
    secrets: list[str] = Field(default_factory=list)


class DeploymentSpec(BaseModel):
    method: str
    rollback: str
    verification: str


class SysadminHandoff(HandoffReport):
    agent: Literal["sysadmin"] = "sysadmin"
    infrastructure: InfrastructureSpec | None = None
    deployment: DeploymentSpec | None = None
    files_changed: list[FileChange] = Field(default_factory=list)
    runbook_refs: list[str] = Field(default_factory=list)


# --- Claude AI Specialist ---


class Optimization(BaseModel):
    target: str
    category: Literal[
        "token-efficiency",
        "determinism",
        "model-selection",
        "prompt-quality",
        "architecture",
    ]
    current: str
    recommended: str
    rationale: str
    estimated_savings: str = ""
    risk: Literal["low", "medium", "high"]
    doc_ref: str = ""


class ModelRoutingReview(BaseModel):
    agent: str
    current_model: Literal["opus", "sonnet", "haiku"]
    recommended_model: Literal["opus", "sonnet", "haiku"]
    rationale: str


class ClaudeAISpecialistHandoff(HandoffReport):
    agent: Literal["claude-ai-specialist"] = "claude-ai-specialist"
    optimizations: list[Optimization] = Field(default_factory=list)
    model_routing_review: list[ModelRoutingReview] = Field(default_factory=list)


# --- Language Specialist (generic, extended per language) ---


class Recommendation(BaseModel):
    topic: str
    guidance: str
    rationale: str
    version: str = ""
    doc_ref: str = ""


class LanguageSpecialistHandoff(HandoffReport):
    domain: str
    recommendations: list[Recommendation] = Field(default_factory=list)
    footguns: list[str] = Field(default_factory=list)
