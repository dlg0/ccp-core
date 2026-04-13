import json
import shutil
from pathlib import Path

from jsonschema import Draft202012Validator
from typer.testing import CliRunner

from ccp_cli.main import app


runner = CliRunner()
ROOT = Path(__file__).resolve().parents[1]


def seed_repo(tmp_path: Path) -> None:
    shutil.copytree(ROOT / "schemas", tmp_path / "schemas")
    init = runner.invoke(app, ["init", str(tmp_path)])
    assert init.exit_code == 0, init.stdout


def test_init_and_new_follow_v0_repo_contract(tmp_path: Path):
    init = runner.invoke(app, ["init", str(tmp_path)])
    assert init.exit_code == 0, init.stdout

    assert (tmp_path / "control" / "change-requests").is_dir()
    assert (tmp_path / "control" / "decision-records").is_dir()
    assert (tmp_path / "control" / "execution-plans").is_dir()
    assert (tmp_path / "control" / "evidence-packs").is_dir()
    assert not (tmp_path / "control" / "events").exists()

    new_dr = runner.invoke(
        app,
        [
            "new",
            "decision_record",
            "--path",
            str(tmp_path),
            "--id",
            "DR-9002",
            "--title",
            "Portable default JSON contract",
        ],
    )
    assert new_dr.exit_code == 0, new_dr.stdout

    dr_path = tmp_path / "control" / "decision-records" / "DR-9002.json"
    data = json.loads(dr_path.read_text())

    assert data["id"] == "DR-9002"
    assert data["kind"] == "decision_record"
    assert "supersedes" not in data


def test_new_execution_plan_omits_empty_optional_fields(tmp_path: Path):
    init = runner.invoke(app, ["init", str(tmp_path)])
    assert init.exit_code == 0, init.stdout

    new_ep = runner.invoke(
        app,
        [
            "new",
            "execution_plan",
            "--path",
            str(tmp_path),
            "--id",
            "EP-9003",
        ],
    )
    assert new_ep.exit_code == 0, new_ep.stdout

    ep_path = tmp_path / "control" / "execution-plans" / "EP-9003.json"
    data = json.loads(ep_path.read_text())

    assert data["id"] == "EP-9003"
    assert data["kind"] == "execution_plan"
    assert "dependencies" not in data
    assert "rollout_plan" not in data

    schema = json.loads((ROOT / "schemas" / "execution-plan.schema.json").read_text())
    Draft202012Validator(schema).validate(data)


def test_validate_reports_missing_required_field_with_pointer(tmp_path: Path):
    seed_repo(tmp_path)

    invalid_cr = {
        "id": "CR-9001",
        "kind": "change_request",
        "title": "Schema failure fixture",
        "status": "draft",
        "type": "feature",
        "risk": "low",
        "problem_statement": "Exercise validator output for missing fields.",
        "acceptance_criteria": ["Show the missing desired_end_state pointer"],
        "constraints": ["Keep the failure focused on one required property."],
        "required_evidence": ["cli-output"],
    }
    target = tmp_path / "control" / "change-requests" / "CR-9001.json"
    target.write_text(json.dumps(invalid_cr, indent=2))

    result = runner.invoke(app, ["validate", str(tmp_path)])

    assert result.exit_code == 1
    assert "control/change-requests/CR-9001.json :: /desired_end_state ::" in result.stdout
    assert "'desired_end_state' is a required property" in result.stdout


def test_validate_reports_all_schema_failures_for_a_file(tmp_path: Path):
    seed_repo(tmp_path)

    invalid_cr = {
        "id": "CR-90A2",
        "kind": "change_request",
        "title": "Schema failure fixture",
        "status": "draft",
        "type": "feature",
        "risk": "low",
        "problem_statement": "Exercise validator output for multiple failures.",
        "acceptance_criteria": [""],
        "constraints": ["Keep multiple failures in one object."],
        "required_evidence": ["cli-output"],
    }
    target = tmp_path / "control" / "change-requests" / "CR-9002.json"
    target.write_text(json.dumps(invalid_cr, indent=2))

    result = runner.invoke(app, ["validate", str(tmp_path)])

    assert result.exit_code == 1
    assert "control/change-requests/CR-9002.json :: /acceptance_criteria/0 ::" in result.stdout
    assert "control/change-requests/CR-9002.json :: /desired_end_state ::" in result.stdout
    assert "control/change-requests/CR-9002.json :: /id ::" in result.stdout
