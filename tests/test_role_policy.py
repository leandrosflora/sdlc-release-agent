"""Role-specific authorization checks against the canonical OPA policy.

These only run when `opa` is on PATH and the sibling
agentic-sdlc-reference-architecture checkout is resolvable -- otherwise they are
skipped rather than failing CI environments that don't have that layout.
"""
from __future__ import annotations

import shutil

import pytest

from sdlc_release_agent import authorization

ROLE = "release"


def _integration_available() -> bool:
    if shutil.which("opa") is None:
        return False
    try:
        authorization._resolve_policy_path()
    except authorization.PolicyUnavailableError:
        return False
    return True


pytestmark = pytest.mark.skipif(
    not _integration_available(), reason="opa CLI or sibling reference-architecture checkout not available"
)


def _production_deploy_input(*, author_id: str, approver_id: str, human: bool = True, valid: bool = True) -> dict:
    return {
        "action": "production.deploy",
        "identity": {"agent_role": ROLE, "project_id": "example-project"},
        "change": {
            "artifact_digest": "sha256:abc123",
            "author_id": author_id,
            "rollback_verified": True,
            "security_gate_passed": True,
            "test_gate_passed": True,
            "risk": "R2",
        },
        "approval": {
            "artifact_digest": "sha256:abc123",
            "valid": valid,
            "human": human,
            "actor_id": approver_id,
        },
    }


def test_production_deploy_allowed_with_independent_human_approval():
    result = authorization.check_authorization(
        _production_deploy_input(author_id="developer-agent-1", approver_id="human-approver-1")
    )
    assert result.allowed is True


def test_production_deploy_denied_when_approver_is_the_author():
    result = authorization.check_authorization(
        _production_deploy_input(author_id="human-approver-1", approver_id="human-approver-1")
    )
    assert result.allowed is False


def test_production_deploy_denied_without_human_approval():
    result = authorization.check_authorization(
        _production_deploy_input(author_id="developer-agent-1", approver_id="human-approver-1", human=False)
    )
    assert result.allowed is False


def test_production_deploy_denied_when_approval_invalid():
    result = authorization.check_authorization(
        _production_deploy_input(author_id="developer-agent-1", approver_id="human-approver-1", valid=False)
    )
    assert result.allowed is False
