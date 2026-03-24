"""Tests for agent handoff schemas.

Verifies that schemas accept valid handoffs, reject invalid ones,
and export to JSON Schema correctly.
"""

import json

import pytest
from pydantic import ValidationError

from src.schemas.agents import (
    AccessibilityHandoff,
    ArchitectHandoff,
    ClaudeAISpecialistHandoff,
    CostAccountantHandoff,
    DatavizSpecialistHandoff,
    ExperimentalPsychologistHandoff,
    ImplementerHandoff,
    LanguageSpecialistHandoff,
    MCPSpecialistHandoff,
    QAHandoff,
    ResearcherHandoff,
    ReviewerHandoff,
    RosterCheckerHandoff,
    SocialPsychologistHandoff,
    SREHandoff,
    SysadminHandoff,
    TechnicalWriterHandoff,
    TraumaInformedDesignHandoff,
    UIDesignerHandoff,
    UXDesignerHandoff,
    ValidatorHandoff,
)
from src.schemas.base import HandoffReport, Status
from src.schemas.export import SCHEMAS
from src.schemas.validate import validate_handoff


class TestBaseHandoff:
    def test_valid_minimal(self):
        report = HandoffReport(
            agent="researcher",
            task_id="task-001",
            status=Status.COMPLETED,
            summary="Found 3 auth modules",
        )
        assert report.status == "completed"
        assert report.token_usage == 0

    def test_rejects_empty_summary(self):
        with pytest.raises(ValidationError):
            HandoffReport(
                agent="researcher",
                task_id="task-001",
                status=Status.COMPLETED,
                summary="",
            )

    def test_rejects_invalid_status(self):
        with pytest.raises(ValidationError):
            HandoffReport(
                agent="researcher",
                task_id="task-001",
                status="mostly-done",
                summary="Found things",
            )

    def test_rejects_negative_token_usage(self):
        with pytest.raises(ValidationError):
            HandoffReport(
                agent="researcher",
                task_id="task-001",
                status=Status.COMPLETED,
                summary="Found things",
                token_usage=-1,
            )


class TestResearcherHandoff:
    def test_valid(self):
        report = ResearcherHandoff(
            task_id="task-001",
            status="completed",
            summary="Found JWT auth in src/auth/",
            patterns_found=["JWT with RS256", "Role-based middleware"],
            artifact_refs=["src/auth/jwt.ts:12-45"],
        )
        assert report.agent == "researcher"

    def test_agent_field_locked(self):
        with pytest.raises(ValidationError):
            ResearcherHandoff(
                agent="implementer",
                task_id="task-001",
                status="completed",
                summary="Found things",
            )


class TestReviewerHandoff:
    def test_valid_approval(self):
        report = ReviewerHandoff(
            task_id="task-001",
            status="approved",
            summary="Code looks good",
        )
        assert report.agent == "reviewer"
        assert report.findings == []

    def test_valid_with_findings(self):
        report = ReviewerHandoff(
            task_id="task-001",
            status="changes-requested",
            summary="Found 2 issues",
            findings=[
                {
                    "severity": "critical",
                    "category": "security",
                    "location": "src/auth.py:23",
                    "description": "SQL injection via string concat",
                    "suggested_fix": "Use parameterized query",
                    "adversarial_note": "Attacker can dump entire DB",
                }
            ],
        )
        assert len(report.findings) == 1
        assert report.findings[0].severity == "critical"

    def test_rejects_invalid_severity(self):
        with pytest.raises(ValidationError):
            ReviewerHandoff(
                task_id="task-001",
                status="approved",
                summary="Review done",
                findings=[
                    {
                        "severity": "minor",
                        "category": "security",
                        "location": "src/auth.py:1",
                        "description": "Issue",
                        "suggested_fix": "Fix it",
                    }
                ],
            )

    def test_rejects_invalid_status(self):
        with pytest.raises(ValidationError):
            ReviewerHandoff(
                task_id="task-001",
                status="completed",
                summary="Review done",
            )


class TestImplementerHandoff:
    def test_valid(self):
        report = ImplementerHandoff(
            task_id="task-001",
            status="completed",
            summary="Implemented auth middleware",
            files_changed=[
                {
                    "path": "src/auth.py",
                    "action": "created",
                    "description": "JWT middleware",
                }
            ],
            tests_added=[
                {
                    "path": "tests/test_auth.py",
                    "count": 5,
                    "description": "Auth middleware tests",
                }
            ],
            test_results={"passed": 5, "failed": 0, "skipped": 0},
        )
        assert report.files_changed[0].action == "created"

    def test_rejects_invalid_action(self):
        with pytest.raises(ValidationError):
            ImplementerHandoff(
                task_id="task-001",
                status="completed",
                summary="Done",
                files_changed=[
                    {
                        "path": "src/auth.py",
                        "action": "updated",
                        "description": "Changed",
                    }
                ],
                tests_added=[
                    {"path": "tests/test.py", "count": 1, "description": "Test"}
                ],
            )

    def test_test_gate_rejects_completed_without_tests(self):
        """Test Gate: completed status requires non-empty tests_added."""
        with pytest.raises(ValidationError, match="Test Gate"):
            ImplementerHandoff(
                task_id="task-001",
                status="completed",
                summary="Done",
                files_changed=[
                    {
                        "path": "src/auth.py",
                        "action": "created",
                        "description": "Auth",
                    }
                ],
            )

    def test_test_gate_allows_blocked_without_tests(self):
        """Blocked status does not require tests."""
        report = ImplementerHandoff(
            task_id="task-001",
            status="blocked",
            summary="Cannot proceed without API key",
        )
        assert report.tests_added == []


class TestValidatorHandoff:
    def test_valid(self):
        report = ValidatorHandoff(
            task_id="task-001",
            status="validated",
            summary="All assertions pass",
            assertions=[
                {
                    "claim": "Expired tokens are rejected",
                    "test_method": "curl with expired JWT",
                    "expected": "401",
                    "actual": "401",
                    "passed": True,
                    "evidence": "HTTP 401 Unauthorized",
                }
            ],
        )
        assert report.assertions[0].passed is True


class TestAccessibilityHandoff:
    def test_valid_with_agent_output_format(self):
        """Validates against the agent's documented output format."""
        report = AccessibilityHandoff(
            task_id="task-001",
            status="completed",
            summary="Found 2 contrast issues",
            wcag_level="AA",
            findings=[
                {
                    "severity": "critical",
                    "wcag_criterion": "1.4.3 Contrast (Minimum)",
                    "issue": "Text contrast too low in dark theme",
                    "location": "base.html:51",
                    "theme": "dark",
                    "current": "2.1:1 ratio",
                    "expected": "4.5:1 ratio",
                    "fix": "Change color to #e0ddd5",
                }
            ],
            automated_results={
                "tool": "axe-core",
                "violations": 2,
                "passes": 45,
                "incomplete": 3,
            },
        )
        assert report.findings[0].severity == "critical"
        assert report.automated_results.violations == 2


class TestSocialPsychologistHandoff:
    def test_valid_with_agent_output_format(self):
        """Validates against the agent's documented output format."""
        report = SocialPsychologistHandoff(
            task_id="task-001",
            status="completed",
            summary="Blocking feature analysis",
            feature_evaluated="User blocking",
            community_context={
                "size": "~100 active members",
                "type": "neighborhood",
                "key_dynamics": "High interconnection, mutual friends",
            },
            analysis=[
                {
                    "dimension": "Group size",
                    "finding": "Blocking creates visible fractures in small groups",
                    "confidence": "established",
                    "source_ref": ".claude/docs/social-psychology/small-group-dynamics.md",
                    "implication": "Consider muting before blocking",
                }
            ],
            recommendations=[
                {
                    "option": "Implement muting first",
                    "prosocial_effects": ["Reduces conflict visibility"],
                    "risks": ["Harassment may continue unseen"],
                    "mitigations": ["Staff-mediated escalation path"],
                    "confidence": "high",
                }
            ],
            trade_offs="Protection vs. social cohesion",
            review_file="docs/reviews/social-psychology-review-2026-03-21.md",
        )
        assert report.feature_evaluated == "User blocking"
        assert report.analysis[0].confidence == "established"


class TestExperimentalPsychologistHandoff:
    def test_valid_with_agent_output_format(self):
        """Validates against the agent's documented output format."""
        report = ExperimentalPsychologistHandoff(
            task_id="task-001",
            status="completed",
            summary="Measurement design for private channels",
            research_question="Does adding private channels reduce public channel activity?",
            hypotheses=[
                {
                    "hypothesis": "Public posting decreases >10% within 30 days",
                    "testable": True,
                    "minimum_n": "100 users observed over 60 days",
                    "feasible_with_current_community": True,
                }
            ],
            measurement_design={
                "method": "natural-experiment",
                "measures": [
                    {
                        "name": "Weekly post count",
                        "operationalization": "Count posts per public channel per week",
                        "data_source": "Database query",
                        "frequency": "Weekly",
                        "baseline": "30-day pre-launch average",
                    }
                ],
                "confounds": ["Seasonal effects", "New member onboarding"],
                "timeline": "90 days minimum",
                "ethical_considerations": ["Informed consent for analytics"],
            },
            implementation={
                "complexity": "moderate",
                "requires_new_tracking": True,
                "suggested_queries_or_tools": "SQL count query on posts table",
            },
            limitations=["Cannot isolate causation from correlation"],
            review_file="docs/reviews/experimental-psychology-review-2026-03-21.md",
        )
        assert report.research_question != ""
        assert report.measurement_design.method == "natural-experiment"


class TestDatavizSpecialistHandoff:
    def test_valid_with_agent_output_format(self):
        """Validates against the agent's nested recommendation structure."""
        report = DatavizSpecialistHandoff(
            task_id="task-001",
            status="completed",
            summary="Chart recommendations for macro tracking",
            recommendations=[
                {
                    "topic": "Daily macronutrient progress",
                    "approach": "both",
                    "conservative": {
                        "recommendation": "Bullet charts (Stephen Few)",
                        "rationale": "Position-on-common-scale ranks #1",
                        "precedent": "Clinical dashboards",
                    },
                    "exploratory": {
                        "recommendation": "Waffle charts",
                        "rationale": "Better part-to-whole perception",
                        "tradeoff": "Less precise for goal progress",
                    },
                    "doc_ref": ".claude/docs/dataviz/health/chart-selection.md",
                }
            ],
            footguns=["Don't use pie charts for macro comparison"],
        )
        assert report.recommendations[0].approach == "both"
        assert report.recommendations[0].conservative.precedent == "Clinical dashboards"


class TestTraumaInformedDesignHandoff:
    def test_valid_with_agent_output_format(self):
        """Validates against the agent's documented output format."""
        report = TraumaInformedDesignHandoff(
            task_id="task-001",
            status="completed",
            summary="Quick-wipe feature analysis",
            recommendations=[
                {
                    "topic": "Quick-wipe feature",
                    "guidance": "Implement with cloud sync first",
                    "rationale": "Evidence must leave device before wipe",
                    "risk_level": "high",
                    "discovery_test": "Ambiguous — app could be a cleaner utility",
                }
            ],
            footguns=["Wipe that destroys evidence before sync"],
            requires_real_world_review=["Consult DV advocate on wipe UX"],
            review_file="docs/reviews/trauma-review-2026-03-21.md",
        )
        assert report.recommendations[0].risk_level == "high"
        assert len(report.requires_real_world_review) == 1


class TestTechnicalWriterHandoff:
    def test_valid_with_agent_output_format(self):
        """Validates field names match agent output format."""
        report = TechnicalWriterHandoff(
            task_id="task-001",
            status="completed",
            summary="Wrote project README",
            files_changed=[
                {
                    "path": "README.md",
                    "action": "created",
                    "description": "Project README with architecture overview",
                }
            ],
            style_issues=["Used imperative mood consistently"],
        )
        assert report.files_changed[0].action == "created"


class TestQAHandoff:
    def test_valid(self):
        report = QAHandoff(
            task_id="task-001",
            status="completed",
            summary="Test landscape analyzed",
            test_landscape={
                "frameworks": ["pytest"],
                "coverage_percent": 78,
                "test_count": 42,
                "pyramid_balance": "healthy",
            },
            coverage_gaps=[
                {
                    "location": "src/auth.py",
                    "risk": "critical",
                    "gap_type": "no-test",
                    "description": "No tests for token refresh",
                    "recommendation": "Add token refresh test",
                    "business_impact": "Auth failures in production",
                }
            ],
        )
        assert report.test_landscape.pyramid_balance == "healthy"


class TestRosterCheckerHandoff:
    def test_valid(self):
        report = RosterCheckerHandoff(
            task_id="task-001",
            status="completed",
            summary="Created 1 specialist",
            project_signals={
                "languages": ["Kotlin"],
                "frameworks": ["Jetpack Compose"],
                "platforms": ["Android"],
                "services": [],
                "task_type": "feature",
            },
            existing_specialists=["python-specialist"],
            agent_gaps=[
                {
                    "needed": "kotlin-specialist",
                    "reason": "Project is Kotlin",
                    "created": True,
                }
            ],
            roster_hash="abc123",
        )
        assert report.agent_gaps[0].created is True


class TestSREHandoff:
    def test_valid(self):
        report = SREHandoff(
            task_id="task-001",
            status="completed",
            summary="SLOs defined",
            slos=[
                {
                    "metric": "p99 latency",
                    "target": "<200ms",
                    "measurement": "Prometheus histogram",
                }
            ],
            alerts=[
                {
                    "name": "high-latency",
                    "condition": "p99 > 500ms for 5m",
                    "severity": "page",
                }
            ],
        )
        assert report.slos[0].target == "<200ms"


class TestSysadminHandoff:
    def test_valid(self):
        report = SysadminHandoff(
            task_id="task-001",
            status="completed",
            summary="Deployment configured",
            infrastructure={
                "services_configured": ["fly.io app"],
                "networking": ["internal DNS"],
                "secrets": ["DATABASE_URL"],
            },
            deployment={
                "method": "fly deploy",
                "rollback": "fly deploy --image previous",
                "verification": "curl health endpoint",
            },
        )
        assert report.infrastructure.services_configured == ["fly.io app"]


class TestMCPSpecialistHandoff:
    def test_valid(self):
        report = MCPSpecialistHandoff(
            task_id="task-001",
            status="completed",
            summary="Tool schema reviewed",
            recommendations=[
                {
                    "topic": "Tool naming",
                    "guidance": "Use verb-noun pattern",
                    "rationale": "Matches Claude's tool selection heuristics",
                }
            ],
            tool_schemas_reviewed=["get-user", "create-post"],
        )
        assert report.tool_schemas_reviewed == ["get-user", "create-post"]


class TestLanguageSpecialistHandoff:
    def test_valid_dynamic_specialist(self):
        report = LanguageSpecialistHandoff(
            agent="rust-specialist",
            task_id="task-001",
            status="completed",
            summary="Rust guidance",
            domain="rust",
            recommendations=[],
        )
        assert report.agent == "rust-specialist"

    def test_rejects_invalid_agent_name_pattern(self):
        """Agent name must match *-specialist pattern."""
        with pytest.raises(ValidationError):
            LanguageSpecialistHandoff(
                agent="lead",
                task_id="task-001",
                status="completed",
                summary="Spoofed",
                domain="fake",
            )


class TestJsonSchemaExport:
    @pytest.mark.parametrize("name,model", list(SCHEMAS.items()))
    def test_schema_exports(self, name, model):
        """Every schema in SCHEMAS dict exports valid JSON Schema."""
        schema = model.model_json_schema()
        assert "properties" in schema
        json_str = json.dumps(schema)
        assert len(json_str) > 0


class TestValidateHandoff:
    def test_valid_researcher(self):
        raw = json.dumps(
            {
                "agent": "researcher",
                "task_id": "task-001",
                "status": "completed",
                "summary": "Found auth patterns",
            }
        )
        valid, msg = validate_handoff(raw)
        assert valid

    def test_invalid_json(self):
        valid, msg = validate_handoff("not json")
        assert not valid
        assert "Invalid JSON" in msg

    def test_missing_agent(self):
        valid, msg = validate_handoff('{"task_id": "1", "status": "completed"}')
        assert not valid
        assert "Missing" in msg

    def test_unknown_agent(self):
        raw = json.dumps(
            {
                "agent": "wizard",
                "task_id": "task-001",
                "status": "completed",
                "summary": "Magic",
            }
        )
        valid, msg = validate_handoff(raw)
        assert not valid
        assert "Unknown agent" in msg

    def test_dynamic_specialist(self):
        raw = json.dumps(
            {
                "agent": "python-specialist",
                "task_id": "task-001",
                "domain": "python",
                "status": "completed",
                "summary": "Use Pydantic v2",
                "recommendations": [],
                "footguns": [],
            }
        )
        valid, msg = validate_handoff(raw)
        assert valid

    def test_rejects_non_specialist_suffix(self):
        """Agent names without -specialist suffix should not route to fallback."""
        raw = json.dumps(
            {
                "agent": "wizard-specialist-fake",
                "task_id": "task-001",
                "status": "completed",
                "summary": "Spoofed",
                "domain": "fake",
            }
        )
        valid, msg = validate_handoff(raw)
        assert not valid
