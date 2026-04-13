import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = sorted((ROOT / "examples").glob("*.json"))
POSITIVE_FIXTURES = sorted((ROOT / "fixtures" / "positive").rglob("*.json"))
NEGATIVE_SCHEMA_FIXTURES = sorted((ROOT / "fixtures" / "negative" / "schema").glob("*.json"))
NEGATIVE_SEMANTIC_FIXTURES = sorted((ROOT / "fixtures" / "negative" / "semantic").glob("*.json"))

SCHEMA_BY_PREFIX = {
    "CR": "change-request.schema.json",
    "DR": "decision-record.schema.json",
    "EP": "execution-plan.schema.json",
    "EV": "evidence-pack.schema.json",
}

EXPECTED_SCHEMA_FAILURES = {
    "CR-3001": {"validator": "required", "message": "'desired_end_state'"},
    "CR-3002": {"validator": "pattern", "path": ["id"]},
    "DR-3001": {"validator": "enum", "path": ["status"]},
    "EP-3001": {"validator": "pattern", "path": ["dependencies", 0]},
    "EV-3001": {"validator": "minLength", "path": ["acceptance_checklist", 0, "result"]},
}

EXPECTED_SEMANTIC_FAILURES = {
    "CR-4001": {"code": "missing_linked_decision_record", "message": "DR-9999"},
    "DR-4001": {"code": "missing_superseded_decision_record", "message": "DR-9999"},
    "EP-4001": {"code": "missing_change_request", "message": "CR-9999"},
    "EP-4002": {"code": "missing_task_dependency", "message": "TASK-999"},
    "EV-4001": {"code": "missing_change_request", "message": "CR-9999"},
}


class SemanticValidationError(ValueError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def validate_against_schema(path: Path) -> None:
    data = load_json(path)
    schema_name = SCHEMA_BY_PREFIX[path.stem[:2]]
    schema = load_json(ROOT / "schemas" / schema_name)
    Draft202012Validator(schema).validate(data)


def positive_fixture_catalog() -> dict[str, set[str]]:
    known_ids = {prefix: set() for prefix in SCHEMA_BY_PREFIX}
    for fixture in POSITIVE_FIXTURES:
        known_ids[fixture.stem[:2]].add(load_json(fixture)["id"])
    return known_ids


def require_known_id(
    known_ids: dict[str, set[str]],
    prefix: str,
    object_id: str,
    code: str,
    message: str,
) -> None:
    if object_id not in known_ids[prefix]:
        raise SemanticValidationError(code, message)


def validate_fixture_semantics(path: Path) -> None:
    data = load_json(path)
    known_ids = positive_fixture_catalog()
    kind = data["kind"]

    if kind == "change_request":
        for linked_id in data.get("linked_decision_records", []):
            require_known_id(
                known_ids,
                "DR",
                linked_id,
                "missing_linked_decision_record",
                f"{data['id']} links to missing Decision Record {linked_id}",
            )
        for linked_id in data.get("linked_execution_plans", []):
            require_known_id(
                known_ids,
                "EP",
                linked_id,
                "missing_linked_execution_plan",
                f"{data['id']} links to missing Execution Plan {linked_id}",
            )
        for linked_id in data.get("linked_evidence_packs", []):
            require_known_id(
                known_ids,
                "EV",
                linked_id,
                "missing_linked_evidence_pack",
                f"{data['id']} links to missing Evidence Pack {linked_id}",
            )
        return

    if kind == "decision_record" and "supersedes" in data:
        require_known_id(
            known_ids,
            "DR",
            data["supersedes"],
            "missing_superseded_decision_record",
            f"{data['id']} supersedes missing Decision Record {data['supersedes']}",
        )
        return

    if kind == "execution_plan":
        require_known_id(
            known_ids,
            "CR",
            data["change_request"],
            "missing_change_request",
            f"{data['id']} references missing Change Request {data['change_request']}",
        )

        task_ids = {task["id"] for task in data["tasks"]}
        for dependency in data.get("dependencies", []):
            task_id, _, depends_on = dependency.partition(" depends_on ")
            if task_id not in task_ids:
                raise SemanticValidationError(
                    "missing_task",
                    f"{data['id']} dependency starts from missing task {task_id}",
                )
            if depends_on not in task_ids:
                raise SemanticValidationError(
                    "missing_task_dependency",
                    f"{data['id']} dependency references missing task {depends_on}",
                )
        return

    if kind == "evidence_pack":
        require_known_id(
            known_ids,
            "CR",
            data["change_request"],
            "missing_change_request",
            f"{data['id']} references missing Change Request {data['change_request']}",
        )


def test_examples_validate():
    assert EXAMPLES, "expected example CCP objects"
    for example in EXAMPLES:
        validate_against_schema(example)


def test_positive_fixtures_exist():
    assert POSITIVE_FIXTURES, "expected positive CCP fixtures"


def test_negative_schema_fixtures_exist():
    assert NEGATIVE_SCHEMA_FIXTURES, "expected schema-invalid CCP fixtures"


def test_negative_semantic_fixtures_exist():
    assert NEGATIVE_SEMANTIC_FIXTURES, "expected semantic-invalid CCP fixtures"


@pytest.mark.parametrize(
    "fixture",
    POSITIVE_FIXTURES,
    ids=lambda fixture: str(fixture.relative_to(ROOT)),
)
def test_positive_fixtures_validate(fixture: Path):
    validate_against_schema(fixture)


@pytest.mark.parametrize(
    "fixture",
    NEGATIVE_SCHEMA_FIXTURES,
    ids=lambda fixture: str(fixture.relative_to(ROOT)),
)
def test_negative_schema_fixtures_fail_for_expected_reason(fixture: Path):
    expectation = EXPECTED_SCHEMA_FAILURES[fixture.stem]

    with pytest.raises(ValidationError) as exc_info:
        validate_against_schema(fixture)

    assert exc_info.value.validator == expectation["validator"]
    if "path" in expectation:
        assert list(exc_info.value.path) == expectation["path"]
    if "message" in expectation:
        assert expectation["message"] in exc_info.value.message


@pytest.mark.parametrize(
    "fixture",
    NEGATIVE_SEMANTIC_FIXTURES,
    ids=lambda fixture: str(fixture.relative_to(ROOT)),
)
def test_negative_semantic_fixtures_fail_for_expected_reason(fixture: Path):
    expectation = EXPECTED_SEMANTIC_FAILURES[fixture.stem]

    validate_against_schema(fixture)

    with pytest.raises(SemanticValidationError) as exc_info:
        validate_fixture_semantics(fixture)

    assert exc_info.value.code == expectation["code"]
    assert expectation["message"] in str(exc_info.value)
