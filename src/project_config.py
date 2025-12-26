from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Optional

import os

try:
    import tomllib  # py>=3.11
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None  # type: ignore[assignment]


ProjectCommand = Literal["schemas", "erd"]


class ProjectConfigError(ValueError):
    pass


@dataclass(frozen=True)
class DbConfig:
    database_url: Optional[str] = None


@dataclass(frozen=True)
class ErdConfig:
    schema: str = ""
    engine: Literal["puml", "d2", "mermaid"] = "puml"
    use_table_comment: bool = False
    relation_type: Literal["none", "laravel"] = "none"
    out_filename: Optional[str] = None


@dataclass(frozen=True)
class ProjectConfig:
    command: ProjectCommand
    db: DbConfig
    erd: ErdConfig
    project_file: Path


def _require_type(value: Any, expected_type: type, path: str) -> Any:
    if value is None:
        return None
    if not isinstance(value, expected_type):
        raise ProjectConfigError(f'Invalid type for "{path}": expected {expected_type.__name__}')
    return value


def _coerce_bool(value: Any, path: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"true", "1", "yes", "y"}:
            return True
        if v in {"false", "0", "no", "n"}:
            return False
    raise ProjectConfigError(f'Invalid boolean for "{path}"')


def _resolve_out_filename(project_file: Path, out_filename: Optional[str]) -> Optional[str]:
    if out_filename is None or out_filename == "":
        return None
    p = Path(out_filename)
    if p.is_absolute():
        return str(p)
    return str((project_file.parent / p).resolve())


def load_project_config(project_file: str | os.PathLike[str]) -> ProjectConfig:
    project_path = Path(project_file).expanduser().resolve()
    if not project_path.exists():
        raise ProjectConfigError(f"Project file not found: {project_path}")
    if not project_path.is_file():
        raise ProjectConfigError(f"Project path is not a file: {project_path}")

    if tomllib is None:  # pragma: no cover
        raise ProjectConfigError(
            "TOML parser not available. Use Python 3.11+ (tomllib) or install 'tomli'."
        )

    try:
        data = tomllib.loads(project_path.read_text(encoding="utf-8"))
    except Exception as e:
        raise ProjectConfigError(f"Failed to parse TOML: {e}") from e

    if not isinstance(data, dict):
        raise ProjectConfigError("Invalid project file root (expected TOML table).")

    command = data.get("command")
    command = _require_type(command, str, "command")
    if command not in ("schemas", "erd"):
        raise ProjectConfigError('Project "command" must be "schemas" or "erd".')

    db_table = data.get("db") or {}
    if not isinstance(db_table, dict):
        raise ProjectConfigError('Invalid type for "db" (expected table).')
    database_url = db_table.get("database_url")
    database_url = _require_type(database_url, str, "db.database_url")

    erd_table = data.get("erd") or {}
    if not isinstance(erd_table, dict):
        raise ProjectConfigError('Invalid type for "erd" (expected table).')

    schema = erd_table.get("schema", "")
    schema = _require_type(schema, str, "erd.schema") or ""

    engine = erd_table.get("engine", "puml")
    engine = _require_type(engine, str, "erd.engine") or "puml"
    if engine not in ("puml", "d2", "mermaid"):
        raise ProjectConfigError('Invalid "erd.engine" (expected puml|d2|mermaid).')

    use_table_comment = _coerce_bool(erd_table.get("use_table_comment", False), "erd.use_table_comment")

    relation_type = erd_table.get("relation_type", "none")
    relation_type = _require_type(relation_type, str, "erd.relation_type") or "none"
    if relation_type not in ("none", "laravel"):
        raise ProjectConfigError('Invalid "erd.relation_type" (expected none|laravel).')

    out_filename = erd_table.get("out_filename")
    out_filename = _require_type(out_filename, str, "erd.out_filename")
    out_filename = _resolve_out_filename(project_path, out_filename)

    return ProjectConfig(
        command=command,  # type: ignore[arg-type]
        db=DbConfig(database_url=database_url),
        erd=ErdConfig(
            schema=schema,
            engine=engine,  # type: ignore[arg-type]
            use_table_comment=use_table_comment,
            relation_type=relation_type,  # type: ignore[arg-type]
            out_filename=out_filename,
        ),
        project_file=project_path,
    )


