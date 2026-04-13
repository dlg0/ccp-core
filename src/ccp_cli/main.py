from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List

import typer
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Reference CLI for CCP")
console = Console()

TRANSITIONS_BY_KIND = {
    "change_request": {
        "draft": {"discussing"},
        "discussing": {"approved"},
        "approved": {"planned"},
        "planned": {"executing"},
        "executing": {"verified"},
        "verified": {"closed", "executing", "discussing"},
        "closed": set(),
    },
    "decision_record": {
        "draft": {"accepted"},
        "accepted": {"superseded"},
        "superseded": set(),
    },
    "execution_plan": {
        "draft": {"planned"},
        "planned": {"executing"},
        "executing": {"blocked", "done"},
        "blocked": {"executing"},
        "done": {"executing"},
    },
    "evidence_pack": {
        "draft": {"submitted"},
        "submitted": {"accepted", "rejected"},
        "rejected": {"draft"},
        "accepted": set(),
    },
}

ROOT_DIRS = [
    "control/change-requests",
    "control/decision-records",
    "control/execution-plans",
    "control/evidence-packs",
]

SCHEMA_MAP = {
    "change_request": "change-request.schema.json",
    "decision_record": "decision-record.schema.json",
    "execution_plan": "execution-plan.schema.json",
    "evidence_pack": "evidence-pack.schema.json",
}

TEMPLATES = {
    "change_request": {
        "id": "CR-0001",
        "kind": "change_request",
        "title": "New Change Request",
        "status": "draft",
        "type": "feature",
        "risk": "medium",
        "problem_statement": "",
        "desired_end_state": "",
        "acceptance_criteria": [""],
        "constraints": [""],
        "required_evidence": [""],
    },
    "decision_record": {
        "id": "DR-0001",
        "kind": "decision_record",
        "title": "New Decision Record",
        "status": "draft",
        "context": "",
        "decision": "",
        "alternatives_considered": [""],
        "consequences": [""],
    },
    "execution_plan": {
        "id": "EP-0001",
        "kind": "execution_plan",
        "change_request": "CR-0001",
        "status": "draft",
        "tasks": [{"id": "TASK-001", "title": "Describe work"}],
        "validation_plan": ["Describe validation"],
    },
    "evidence_pack": {
        "id": "EV-0001",
        "kind": "evidence_pack",
        "change_request": "CR-0001",
        "status": "draft",
        "acceptance_checklist": [{"criterion": "Describe evidence", "result": "partial"}],
        "artifacts": [{"path": "path/to/artifact"}],
        "unresolved_risks": [],
    },
}

DIR_MAP = {
    "change_request": "control/change-requests",
    "decision_record": "control/decision-records",
    "execution_plan": "control/execution-plans",
    "evidence_pack": "control/evidence-packs",
}

REQUIRED_PROPERTY_RE = re.compile(r"'([^']+)' is a required property")
KIND_BY_DIR = {directory: kind for kind, directory in DIR_MAP.items()}


def repo_root(path: Path) -> Path:
    return path.resolve()


def schema_root(root: Path) -> Path:
    return root / "schemas"


def iter_ccp_files(root: Path):
    for rel in DIR_MAP.values():
        d = root / rel
        if not d.exists():
            continue
        yield from sorted(d.glob("*.json"))


def load_json(path: Path):
    return json.loads(path.read_text())


def load_schema(root: Path, kind: str):
    return json.loads((schema_root(root) / SCHEMA_MAP[kind]).read_text())


def schema_kind_for_file(root: Path, path: Path, data: dict) -> str:
    kind = data.get("kind")
    if kind in SCHEMA_MAP:
        return kind

    rel_parent = path.relative_to(root).parent.as_posix()
    if rel_parent in KIND_BY_DIR:
        return KIND_BY_DIR[rel_parent]

    raise KeyError(kind or "missing kind")


def validation_path(error: ValidationError) -> list[str | int]:
    path = list(error.path)
    if error.validator == "required":
        match = REQUIRED_PROPERTY_RE.search(error.message)
        if match:
            path.append(match.group(1))
    return path


def json_pointer(path: list[str | int]) -> str:
    if not path:
        return "/"
    escaped = [
        str(segment).replace("~", "~0").replace("/", "~1")
        for segment in path
    ]
    return "/" + "/".join(escaped)


def sorted_validation_errors(validator: Draft202012Validator, data: dict) -> list[ValidationError]:
    return sorted(
        validator.iter_errors(data),
        key=lambda error: (
            json_pointer(validation_path(error)),
            list(error.schema_path),
            error.message,
        ),
    )


def print_schema_failure(root: Path, path: Path, pointer: str, reason: str) -> None:
    console.print(f"[red]FAIL[/red] {path.relative_to(root)} :: {pointer} :: {reason}")


@app.command()
def init(path: Path = typer.Argument(Path("."), help="Repo path")):
    root = repo_root(path)
    for rel in ROOT_DIRS:
        (root / rel).mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Initialized CCP control-plane directories in {root}[/green]")

@app.command("new")
def new_object(
    kind: str = typer.Argument(..., help="change_request | decision_record | execution_plan | evidence_pack"),
    path: Path = typer.Option(Path("."), "--path", help="Repo path"),
    object_id: str = typer.Option(None, "--id", help="Object ID"),
    title: str = typer.Option(None, "--title", help="Title"),
):
    if kind not in TEMPLATES:
        raise typer.BadParameter(f"Unsupported kind: {kind}")
    root = repo_root(path)
    target_dir = root / DIR_MAP[kind]
    target_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(json.dumps(TEMPLATES[kind]))
    if object_id:
        data["id"] = object_id
    if title:
        data["title"] = title
    out = target_dir / f"{data['id']}.json"
    out.write_text(json.dumps(data, indent=2))
    console.print(f"[green]Created {out}[/green]")

@app.command()
def validate(path: Path = typer.Argument(Path("."), help="Repo path")):
    root = repo_root(path)
    files = list(iter_ccp_files(root))
    if not files:
        console.print("[yellow]No CCP JSON files found.[/yellow]")
        raise typer.Exit(0)

    failures = 0
    for f in files:
        try:
            data = load_json(f)
            schema = load_schema(root, schema_kind_for_file(root, f, data))
            validator = Draft202012Validator(schema)
            errors = sorted_validation_errors(validator, data)
            if errors:
                failures += 1
                for error in errors:
                    print_schema_failure(root, f, json_pointer(validation_path(error)), error.message)
                continue
            console.print(f"[green]OK[/green] {f.relative_to(root)}")
        except Exception as exc:
            failures += 1
            print_schema_failure(root, f, "/", str(exc))
    if failures:
        raise typer.Exit(1)

@app.command()
def index(path: Path = typer.Argument(Path("."), help="Repo path")):
    root = repo_root(path)
    rows: List[Dict[str, str]] = []
    for f in iter_ccp_files(root):
        data = load_json(f)
        rows.append({
            "id": data.get("id", ""),
            "kind": data.get("kind", ""),
            "status": data.get("status", ""),
            "title": data.get("title", ""),
            "path": str(f.relative_to(root)),
        })
    out = root / "control" / "index.json"
    out.write_text(json.dumps(rows, indent=2))
    table = Table(title="CCP Index")
    for col in ["id", "kind", "status", "title", "path"]:
        table.add_column(col)
    for row in rows:
        table.add_row(row["id"], row["kind"], row["status"], row["title"], row["path"])
    console.print(table)
    console.print(f"[green]Wrote {out.relative_to(root)}[/green]")

@app.command()
def render(object_path: Path = typer.Argument(..., help="Path to a CCP object JSON file")):
    data = load_json(object_path)
    console.print(f"[bold]{data.get('id')} — {data.get('title', '(untitled)')}[/bold]")
    for key, value in data.items():
        if key in {"id", "title"}:
            continue
        console.print(f"[cyan]{key}[/cyan]: {json.dumps(value, ensure_ascii=False)}")

@app.command()
def transition(
    object_path: Path = typer.Argument(..., help="Path to a CCP object JSON file"),
    new_status: str = typer.Argument(..., help="Target status"),
):
    data = load_json(object_path)
    kind = data.get("kind")
    current = data.get("status")
    allowed = TRANSITIONS_BY_KIND.get(kind, {}).get(current, set())
    if new_status not in allowed:
        console.print(f"[red]Invalid transition[/red] for {kind}: {current} -> {new_status}")
        raise typer.Exit(1)
    data["status"] = new_status
    object_path.write_text(json.dumps(data, indent=2))
    console.print(f"[green]Updated[/green] {object_path} to status={new_status}")


if __name__ == "__main__":
    app()
