import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parents[1]


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schemas" / name).read_text())


@pytest.mark.parametrize(
    ("schema_name", "data"),
    [
        (
            "change-request.schema.json",
            {
                "id": "CR-9001",
                "kind": "change_request",
                "title": "Tighten CR schema",
                "status": "approved",
                "type": "architecture",
                "risk": "low",
                "sponsor": "",
                "problem_statement": "Optional strings should be omitted, not blank.",
                "desired_end_state": "The schema rejects blank optional strings.",
                "acceptance_criteria": ["Validation fails for blank optional fields"],
                "constraints": ["Keep the v0.1 field matrix intact"],
                "required_evidence": ["schema-validation"],
            },
        ),
        (
            "change-request.schema.json",
            {
                "id": "CR-9002",
                "kind": "change_request",
                "title": "Tighten CR link lists",
                "status": "approved",
                "type": "architecture",
                "risk": "low",
                "problem_statement": "Optional lists should be omitted when empty.",
                "desired_end_state": "The schema rejects empty optional arrays.",
                "acceptance_criteria": ["Validation fails for empty optional lists"],
                "constraints": ["Keep the v0.1 field matrix intact"],
                "required_evidence": ["schema-validation"],
                "linked_decision_records": [],
            },
        ),
        (
            "decision-record.schema.json",
            {
                "id": "DR-9001",
                "kind": "decision_record",
                "title": "Tighten DR schema",
                "status": "accepted",
                "context": "Decision record lists should not contain blank entries.",
                "decision": "Reject blank list items.",
                "alternatives_considered": [""],
                "consequences": ["Cleaner serialized objects"],
            },
        ),
        (
            "evidence-pack.schema.json",
            {
                "id": "EV-9001",
                "kind": "evidence_pack",
                "change_request": "CR-9001",
                "status": "submitted",
                "acceptance_checklist": [{"criterion": "Criterion text", "result": ""}],
                "artifacts": [{"path": "artifacts/report.txt"}],
                "unresolved_risks": [],
            },
        ),
        (
            "evidence-pack.schema.json",
            {
                "id": "EV-9002",
                "kind": "evidence_pack",
                "change_request": "CR-9001",
                "status": "submitted",
                "acceptance_checklist": [{"criterion": "Criterion text", "result": "needs_followup"}],
                "artifacts": [{"path": "artifacts/report.txt"}],
                "unresolved_risks": [""],
            },
        ),
    ],
)
def test_schema_rejects_blank_or_empty_optional_shapes(schema_name: str, data: dict):
    schema = load_schema(schema_name)

    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(data)


def test_evidence_pack_schema_allows_non_enum_result_values():
    schema = load_schema("evidence-pack.schema.json")
    data = {
        "id": "EV-9003",
        "kind": "evidence_pack",
        "change_request": "CR-9001",
        "status": "submitted",
        "acceptance_checklist": [{"criterion": "Criterion text", "result": "needs_followup"}],
        "artifacts": [{"path": "artifacts/report.txt"}],
        "unresolved_risks": [],
    }

    Draft202012Validator(schema).validate(data)
