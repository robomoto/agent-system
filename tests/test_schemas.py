"""Tests for agent handoff schemas.

Verifies that schemas accept valid handoffs, reject invalid ones,
and export to JSON Schema correctly.
"""

import json

import pytest
from pydantic import ValidationError

from src.schemas.agents import (
    ArchitectHandoff,
    ClaudeAISpecialistHandoff,
    CostAccountantHandoff,
    ImplementerHandoff,
    ResearcherHandoff,
    ReviewerHandoff,
    ValidatorHandoff,
)
from src.schemas.base import HandoffReport, Status
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
            )


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


class TestJsonSchemaExport:
    def test_all_schemas_export(self):
        schemas = [
            ResearcherHandoff,
            ArchitectHandoff,
            ImplementerHandoff,
            ReviewerHandoff,
            ValidatorHandoff,
            CostAccountantHandoff,
            ClaudeAISpecialistHandoff,
        ]
        for model in schemas:
            schema = model.model_json_schema()
            assert "properties" in schema
            assert "agent" in schema["properties"]
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
