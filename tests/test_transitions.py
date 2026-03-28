import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ccp_cli.main import app


runner = CliRunner()


def write_object(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2))


@pytest.mark.parametrize(
    ("data", "valid_status", "invalid_status"),
    [
        (
            {
                "id": "CR-9001",
                "kind": "change_request",
                "title": "Freeze status semantics",
                "status": "approved",
                "type": "architecture",
                "risk": "medium",
                "problem_statement": "Need a per-object transition model.",
                "desired_end_state": "Transitions are frozen by kind.",
                "acceptance_criteria": ["Transitions are validated per kind"],
                "constraints": ["Keep the lifecycle minimal"],
                "required_evidence": ["tests"],
            },
            "planned",
            "executing",
        ),
        (
            {
                "id": "DR-9001",
                "kind": "decision_record",
                "title": "Record transition rules",
                "status": "draft",
                "context": "Shared transitions break DR promotion.",
                "decision": "Use a per-kind transition map.",
                "alternatives_considered": ["One shared transition map"],
                "consequences": ["DR transitions become valid"],
            },
            "accepted",
            "discussing",
        ),
        (
            {
                "id": "EP-9001",
                "kind": "execution_plan",
                "change_request": "CR-9001",
                "status": "draft",
                "tasks": [{"id": "TASK-001", "title": "Implement per-kind transitions"}],
                "validation_plan": ["Run transition regression tests"],
            },
            "planned",
            "discussing",
        ),
        (
            {
                "id": "EP-9002",
                "kind": "execution_plan",
                "change_request": "CR-9001",
                "status": "done",
                "tasks": [{"id": "TASK-002", "title": "Reopen finished work when needed"}],
                "validation_plan": ["Confirm reopen transition works"],
            },
            "executing",
            "closed",
        ),
        (
            {
                "id": "EV-9001",
                "kind": "evidence_pack",
                "change_request": "CR-9001",
                "status": "draft",
                "acceptance_checklist": [
                    {"criterion": "Transitions are validated per kind", "result": "partial"}
                ],
                "artifacts": [{"path": "evidence/transitions.txt"}],
                "unresolved_risks": [],
            },
            "submitted",
            "discussing",
        ),
    ],
)
def test_transition_uses_per_kind_state_machine(tmp_path: Path, data: dict, valid_status: str, invalid_status: str):
    object_path = tmp_path / f"{data['id']}.json"
    write_object(object_path, data)

    invalid = runner.invoke(app, ["transition", str(object_path), invalid_status])
    assert invalid.exit_code == 1
    assert json.loads(object_path.read_text())["status"] == data["status"]

    valid = runner.invoke(app, ["transition", str(object_path), valid_status])
    assert valid.exit_code == 0, valid.stdout
    assert json.loads(object_path.read_text())["status"] == valid_status
