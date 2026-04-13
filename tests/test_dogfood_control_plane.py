import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "control"
PROTOCOL = ROOT / "protocol" / "version.json"
PROFILES = ROOT / "profiles.md"
POLICY = ROOT / "policy"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_control_plane_is_one_linked_v0_1_scenario():
    cr_paths = sorted((CONTROL / "change-requests").glob("CR-*.json"))
    cr_path = CONTROL / "change-requests" / "CR-0001.json"
    ep_paths = sorted((CONTROL / "execution-plans").glob("EP-*.json"))
    ep_path = CONTROL / "execution-plans" / "EP-0001.json"
    ev_paths = sorted((CONTROL / "evidence-packs").glob("EV-*.json"))
    ev_path = CONTROL / "evidence-packs" / "EV-0001.json"
    dr_paths = sorted((CONTROL / "decision-records").glob("DR-*.json"))

    cr = load_json(cr_path)
    ep = load_json(ep_path)
    ev = load_json(ev_path)
    dr_objects = [load_json(path) for path in dr_paths]
    dr_ids = [item["id"] for item in dr_objects]

    assert [path.name for path in cr_paths] == ["CR-0001.json"]
    assert [path.name for path in ep_paths] == ["EP-0001.json"]
    assert [path.name for path in ev_paths] == ["EV-0001.json"]
    assert cr["status"] == "verified"
    assert ep["status"] == "done"
    assert ev["status"] == "accepted"
    assert dr_ids == ["DR-0001", "DR-0002", "DR-0003", "DR-0004", "DR-0005"]
    assert all(item["status"] == "accepted" for item in dr_objects)

    assert cr["linked_decision_records"] == dr_ids
    assert cr["linked_execution_plans"] == ["EP-0001"]
    assert cr["linked_evidence_packs"] == ["EV-0001"]

    assert ep["change_request"] == cr["id"]
    assert ev["change_request"] == cr["id"]
    assert [item["criterion"] for item in ev["acceptance_checklist"]] == cr["acceptance_criteria"]
    assert all(item["result"] == "pass" for item in ev["acceptance_checklist"])


def test_dogfood_repo_includes_initialized_control_plane_notes():
    version = load_json(PROTOCOL)
    profiles = PROFILES.read_text()
    review_policy = (POLICY / "review.md").read_text()
    evidence_policy = (POLICY / "evidence.md").read_text()

    assert version["protocol"] == "CCP"
    assert version["version"] == "v0.1"
    assert version["repo_local_notes"]["profiles"] == "profiles.md"
    assert version["repo_local_notes"]["policy"] == {
        "review": "policy/review.md",
        "evidence": "policy/evidence.md",
    }
    assert version["portable_control_plane"]["embedded_control_root"] == "control/"

    assert "L1: Local" in profiles
    assert "repo-local `control/` directory" in profiles
    assert "approved Change Request" in review_policy
    assert "merge to `main`" in review_policy
    assert "Evidence Packs should map each acceptance criterion" in evidence_policy
    assert "product-specific tooling" in evidence_policy
