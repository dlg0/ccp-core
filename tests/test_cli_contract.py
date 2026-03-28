import json
from pathlib import Path

from typer.testing import CliRunner

from ccp_cli.main import app


runner = CliRunner()


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
