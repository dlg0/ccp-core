import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = sorted((ROOT / "examples").glob("*.json"))
POSITIVE_FIXTURES = sorted((ROOT / "fixtures" / "positive").rglob("*.json"))

SCHEMA_BY_PREFIX = {
    "CR": "change-request.schema.json",
    "DR": "decision-record.schema.json",
    "EP": "execution-plan.schema.json",
    "EV": "evidence-pack.schema.json",
}


def validate_against_schema(path: Path) -> None:
    data = json.loads(path.read_text())
    schema_name = SCHEMA_BY_PREFIX[path.stem[:2]]
    schema = json.loads((ROOT / "schemas" / schema_name).read_text())
    Draft202012Validator(schema).validate(data)


def test_examples_validate():
    assert EXAMPLES, "expected example CCP objects"
    for example in EXAMPLES:
        validate_against_schema(example)


def test_positive_fixtures_exist():
    assert POSITIVE_FIXTURES, "expected positive CCP fixtures"


@pytest.mark.parametrize(
    "fixture",
    POSITIVE_FIXTURES,
    ids=lambda fixture: str(fixture.relative_to(ROOT)),
)
def test_positive_fixtures_validate(fixture: Path):
    validate_against_schema(fixture)
