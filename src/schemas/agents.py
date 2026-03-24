"""Agent-specific handoff schemas.

Each schema extends HandoffReport with fields specific to that agent's output.
Use .model_json_schema() on any model to export JSON Schema for Claude's
structured outputs with strict: true.
"""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

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

    @model_validator(mode="after")
    def enforce_test_gate(self) -> "ImplementerHandoff":
        """Completed implementation must include tests (Test Gate enforcement)."""
        if self.status == Status.COMPLETED and not self.tests_added:
            raise ValueError(
                "Test Gate: completed implementation must include tests_added "
                "(non-empty). Re-dispatch implementer with explicit test instructions."
            )
        return self


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
    # Generic schema for dynamically created *-specialist agents.
    # Agents with dedicated schemas (mcp-specialist, dataviz-specialist, etc.)
    # are routed via SCHEMA_MAP in validate.py before this fallback is used.
    agent: str = Field(pattern=r"^[a-z][a-z0-9-]*-specialist$")
    domain: str
    recommendations: list[Recommendation] = Field(default_factory=list)
    footguns: list[str] = Field(default_factory=list)


# --- QA ---


class CoverageGap(BaseModel):
    location: str
    risk: Literal["critical", "high", "medium", "low"]
    gap_type: Literal[
        "no-test", "shallow-test", "missing-edge-case", "missing-error-path"
    ]
    description: str
    recommendation: str
    business_impact: str


class TestQualityIssue(BaseModel):
    location: str
    issue: Literal[
        "tests-implementation",
        "over-mocked",
        "no-assertion",
        "shared-state",
        "happy-path-only",
    ]
    description: str
    suggestion: str


class RegressionRisk(BaseModel):
    area: str
    reason: str
    mitigation: str


class TestLandscape(BaseModel):
    frameworks: list[str] = Field(default_factory=list)
    coverage_percent: int | None = None
    test_count: int = Field(default=0, ge=0)
    pyramid_balance: Literal[
        "healthy", "top-heavy", "bottom-heavy", "missing-middle"
    ]


class QAHandoff(HandoffReport):
    agent: Literal["qa"] = "qa"
    test_landscape: TestLandscape | None = None
    coverage_gaps: list[CoverageGap] = Field(default_factory=list)
    test_quality_issues: list[TestQualityIssue] = Field(default_factory=list)
    regression_risks: list[RegressionRisk] = Field(default_factory=list)


# --- Technical Writer ---


class TechnicalWriterHandoff(HandoffReport):
    agent: Literal["technical-writer"] = "technical-writer"
    files_changed: list[FileChange] = Field(default_factory=list)
    style_issues: list[str] = Field(default_factory=list)


# --- Roster Checker ---


class ProjectSignals(BaseModel):
    languages: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    platforms: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    task_type: str = ""


class AgentGap(BaseModel):
    needed: str
    reason: str
    created: bool


class DocBundleGap(BaseModel):
    needed: str
    reason: str
    created: bool
    files: list[str] = Field(default_factory=list)


class DocBundleVerification(BaseModel):
    checked: int = Field(ge=0)
    confirmed: int = Field(ge=0)
    flagged: int = Field(ge=0)


class RosterCheckerHandoff(HandoffReport):
    agent: Literal["roster-checker"] = "roster-checker"
    project_signals: ProjectSignals | None = None
    existing_specialists: list[str] = Field(default_factory=list)
    agent_gaps: list[AgentGap] = Field(default_factory=list)
    doc_bundle_gaps: list[DocBundleGap] = Field(default_factory=list)
    no_action_needed: list[str] = Field(default_factory=list)
    doc_bundle_verified: DocBundleVerification | None = None
    roster_hash: str = ""


# --- Social Psychologist ---


class CommunityContext(BaseModel):
    size: str
    type: str
    key_dynamics: str = ""


class SocialAnalysisDimension(BaseModel):
    dimension: str
    finding: str
    confidence: Literal["established", "suggestive", "extrapolation"]
    source_ref: str = ""
    implication: str = ""


class SocialRecommendation(BaseModel):
    option: str
    prosocial_effects: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    mitigations: list[str] = Field(default_factory=list)
    confidence: Literal["high", "medium", "low"]


class SocialPsychologistHandoff(HandoffReport):
    agent: Literal["social-psychologist"] = "social-psychologist"
    feature_evaluated: str = ""
    community_context: CommunityContext | None = None
    analysis: list[SocialAnalysisDimension] = Field(default_factory=list)
    recommendations: list[SocialRecommendation] = Field(default_factory=list)
    trade_offs: str = ""
    review_file: str = ""


# --- Experimental Psychologist ---


class ExperimentalHypothesis(BaseModel):
    hypothesis: str
    testable: bool = True
    minimum_n: str = ""
    feasible_with_current_community: bool = True


class MeasureSpec(BaseModel):
    name: str
    operationalization: str
    data_source: str = ""
    frequency: str = ""
    baseline: str = ""


class MeasurementDesign(BaseModel):
    method: str
    measures: list[MeasureSpec] = Field(default_factory=list)
    confounds: list[str] = Field(default_factory=list)
    timeline: str = ""
    ethical_considerations: list[str] = Field(default_factory=list)


class ImplementationSpec(BaseModel):
    complexity: Literal["trivial", "moderate", "significant"]
    requires_new_tracking: bool = False
    suggested_queries_or_tools: str = ""


class ExperimentalPsychologistHandoff(HandoffReport):
    agent: Literal["experimental-psychologist"] = "experimental-psychologist"
    research_question: str = ""
    hypotheses: list[ExperimentalHypothesis] = Field(default_factory=list)
    measurement_design: MeasurementDesign | None = None
    implementation: ImplementationSpec | None = None
    limitations: list[str] = Field(default_factory=list)
    review_file: str = ""


# --- Accessibility ---


class A11yFinding(BaseModel):
    severity: Literal["critical", "warning", "suggestion"]
    wcag_criterion: str
    issue: str
    location: str
    theme: str = ""
    current: str = ""
    expected: str = ""
    fix: str = ""


class AutomatedScanResults(BaseModel):
    tool: str
    violations: int = Field(default=0, ge=0)
    passes: int = Field(default=0, ge=0)
    incomplete: int = Field(default=0, ge=0)


class ContrastPair(BaseModel):
    foreground: str
    background: str
    ratio: str
    passed: bool = Field(alias="pass", default=True)


class AccessibilityHandoff(HandoffReport):
    agent: Literal["accessibility"] = "accessibility"
    wcag_level: Literal["A", "AA", "AAA"] = "AA"
    findings: list[A11yFinding] = Field(default_factory=list)
    automated_results: AutomatedScanResults | None = None
    contrast_pairs_checked: list[ContrastPair] = Field(default_factory=list)


# --- MCP Specialist ---


class MCPSpecialistHandoff(HandoffReport):
    agent: Literal["mcp-specialist"] = "mcp-specialist"
    domain: str = "mcp"
    recommendations: list[Recommendation] = Field(default_factory=list)
    footguns: list[str] = Field(default_factory=list)
    tool_schemas_reviewed: list[str] = Field(default_factory=list)


# --- Dataviz Specialist ---


class DatavizOption(BaseModel):
    recommendation: str
    rationale: str
    precedent: str = ""
    tradeoff: str = ""


class DatavizRecommendation(BaseModel):
    topic: str
    approach: Literal["conservative", "exploratory", "both"] = "conservative"
    conservative: DatavizOption | None = None
    exploratory: DatavizOption | None = None
    doc_ref: str = ""


class DatavizSpecialistHandoff(HandoffReport):
    agent: Literal["dataviz-specialist"] = "dataviz-specialist"
    domain: str = "dataviz"
    recommendations: list[DatavizRecommendation] = Field(default_factory=list)
    footguns: list[str] = Field(default_factory=list)


# --- Trauma-Informed Design Specialist ---


class TraumaRecommendation(BaseModel):
    topic: str
    guidance: str
    rationale: str
    risk_level: Literal["critical", "high", "medium", "low"]
    discovery_test: str = ""


class TraumaInformedDesignHandoff(HandoffReport):
    agent: Literal["trauma-informed-design-specialist"] = (
        "trauma-informed-design-specialist"
    )
    domain: str = "trauma-informed-design"
    recommendations: list[TraumaRecommendation] = Field(default_factory=list)
    footguns: list[str] = Field(default_factory=list)
    requires_real_world_review: list[str] = Field(default_factory=list)
    review_file: str = ""
