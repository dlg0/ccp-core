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

DIR_NAME_BY_KIND = {
    "change_request": "change-requests",
    "decision_record": "decision-records",
    "execution_plan": "execution-plans",
    "evidence_pack": "evidence-packs",
}

ROOT_DIRS = [f"control/{directory}" for directory in DIR_NAME_BY_KIND.values()]

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

DIR_MAP = {kind: f"control/{directory}" for kind, directory in DIR_NAME_BY_KIND.items()}

REQUIRED_PROPERTY_RE = re.compile(r"'([^']+)' is a required property")
KIND_BY_DIR = {directory: kind for kind, directory in DIR_NAME_BY_KIND.items()}
KIND_BY_PREFIX = {
    "CR": "change_request",
    "DR": "decision_record",
    "EP": "execution_plan",
    "EV": "evidence_pack",
}


def repo_root(path: Path) -> Path:
    return path.resolve()


def control_root(root: Path) -> Path:
    embedded = root / "control"
    if embedded.exists():
        return embedded
    if all((root / directory).exists() for directory in DIR_NAME_BY_KIND.values()):
        return root
    return embedded


def schema_root(root: Path) -> Path:
    return root / "schemas"


def object_dir(root: Path, kind: str) -> Path:
    return control_root(root) / DIR_NAME_BY_KIND[kind]


def object_dir_relative_to_repo(root: Path, kind: str) -> str:
    return object_dir(root, kind).relative_to(root).as_posix()


def directory_kind_for_file(root: Path, path: Path) -> str:
    rel_parent = path.parent.relative_to(control_root(root)).as_posix()
    return KIND_BY_DIR[rel_parent]


def kind_for_filename(path: Path) -> str | None:
    return KIND_BY_PREFIX.get(path.stem[:2])


def iter_ccp_files(root: Path):
    for kind in DIR_NAME_BY_KIND:
        d = object_dir(root, kind)
        if not d.exists():
            continue
        yield from sorted(d.glob("*.json"))


def iter_misplaced_ccp_files(root: Path):
    base = control_root(root)
    if not base.exists():
        return

    for path in sorted(base.rglob("*.json")):
        rel = path.relative_to(base)
        if rel.parent.as_posix() in KIND_BY_DIR:
            continue
        if kind_for_filename(path):
            yield path


def load_json(path: Path):
    return json.loads(path.read_text())


def load_schema(root: Path, kind: str):
    return json.loads((schema_root(root) / SCHEMA_MAP[kind]).read_text())


def schema_kind_for_file(root: Path, path: Path, data: dict) -> str:
    kind = data.get("kind")
    if kind in SCHEMA_MAP:
        return kind

    return directory_kind_for_file(root, path)


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
    console.print(
        f"[red]FAIL[/red] {path.relative_to(root)} :: {pointer} :: {reason}",
        soft_wrap=True,
    )


def repo_layout_failures(root: Path) -> list[tuple[Path, str, str]]:
    failures = []
    for kind in DIR_NAME_BY_KIND:
        d = object_dir(root, kind)
        if not d.is_dir():
            failures.append((d, "/", f"missing required directory {d.relative_to(root)}"))

    for path in iter_misplaced_ccp_files(root):
        kind = kind_for_filename(path)
        if kind is None:
            continue
        failures.append(
            (
                path,
                "/",
                f"expected {path.name} under {object_dir_relative_to_repo(root, kind)}",
            )
        )

    return failures


def file_layout_failures(root: Path, path: Path, data: dict) -> list[tuple[str, str]]:
    failures = []
    expected_kind = directory_kind_for_file(root, path)
    actual_kind = data.get("kind")
    if actual_kind in DIR_NAME_BY_KIND and actual_kind != expected_kind:
        failures.append(
            (
                "/kind",
                (
                    f"expected kind '{expected_kind}' for files in "
                    f"{path.parent.relative_to(root).as_posix()}, found '{actual_kind}'"
                ),
            )
        )

    object_id = data.get("id")
    if isinstance(object_id, str) and path.name != f"{object_id}.json":
        failures.append(("/id", f"expected filename {object_id}.json, found {path.name}"))

    return failures


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
    failures = 0

    for layout_path, pointer, reason in repo_layout_failures(root):
        failures += 1
        print_schema_failure(root, layout_path, pointer, reason)

    if not files and not failures:
        console.print("[yellow]No CCP JSON files found.[/yellow]")
        raise typer.Exit(0)

    for f in files:
        try:
            data = load_json(f)
            layout_errors = file_layout_failures(root, f, data)
            schema = load_schema(root, schema_kind_for_file(root, f, data))
            validator = Draft202012Validator(schema)
            errors = sorted_validation_errors(validator, data)
            if errors or layout_errors:
                failures += 1
                for pointer, reason in layout_errors:
                    print_schema_failure(root, f, pointer, reason)
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
