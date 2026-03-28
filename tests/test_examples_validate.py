from pathlib import Path
import json

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_BY_PREFIX = {
    "CR": "change-request.schema.json",
    "DR": "decision-record.schema.json",
    "EP": "execution-plan.schema.json",
    "EV": "evidence-pack.schema.json",
}

def test_examples_validate():
    examples = sorted((ROOT / "examples").glob("*.json"))
    assert examples, "expected example CCP objects"
    for example in examples:
        data = json.loads(example.read_text())
        schema_name = SCHEMA_BY_PREFIX[example.stem[:2]]
        schema = json.loads((ROOT / "schemas" / schema_name).read_text())
        Draft202012Validator(schema).validate(data)
