import os
import sys

import click
from dotenv import load_dotenv

from src.d2_erd import D2Erd
from src.database import Database
from src.mermaid_erd import MermaidErd
from src.plantuml_erd import PlantumlErd
from src.project_config import ProjectConfigError, load_project_config

load_dotenv()


def _resolve_database_url(override_database_url: str | None) -> str | None:
    """
    Runtime database url resolver.
    Precedence: CLI override > env DATABASE_URL
    """
    if override_database_url:
        return override_database_url
    return os.environ.get("DATABASE_URL")


def run_schemas(database_url: str) -> int:
    database = Database()

    if database.connect(database_url):
        schemas = database.get_schemas()
        for schema in schemas:
            click.echo(schema)
        return 0

    click.echo("[error] cannot connect to database")
    return 1


def run_erd(
    database_url: str,
    schema: str,
    engine: str,
    use_table_comment: bool,
    relation_type: str,
    out_filename: str | None,
) -> int:
    if out_filename is not None and os.path.exists(out_filename):
        click.echo(f"[error] File exists - {out_filename}")
        return 1

    database = Database()
    try:
        if not database.connect(database_url):
            click.echo("[error] Cannot connect to database")
            return 1

        if engine == "d2":
            erd = D2Erd(database)
        elif engine == "mermaid":
            erd = MermaidErd(database)
        else:
            erd = PlantumlErd(database)

        schemas = database.get_schemas()
        if not schemas:
            click.echo("[error] No schemas found")
            return 1

        if not schema:
            schema = schemas[0]

        if schema not in schemas:
            click.echo(f'[error] Schema "{schema}" not found')
            return 1
    except Exception as e:
        click.echo(f"[error] {str(e)}")
        return 1

    output = erd.get_erd(schema, use_table_comment, relation_type)
    if out_filename is None:
        click.echo(output)
    else:
        with open(out_filename, "w") as text_file:
            text_file.write(output)
        click.echo("[success] Save to " + out_filename)

    return 0

@click.command()
@click.option("--database_url", default=None, help="SQLAlchemy database url. If omitted, use env DATABASE_URL.")
def schemas(database_url):
    resolved = _resolve_database_url(database_url)
    if not resolved:
        click.echo("[error] DATABASE_URL is not set")
        sys.exit(1)

    sys.exit(run_schemas(resolved))

@click.command()
@click.option("-s", "--schema", default='', help="Database schema name.")
@click.option("-e", "--engine", default='puml', type=click.Choice(['puml', 'd2', 'mermaid']), help="PlantUML, D2 or Mermaid")
@click.option("-c", "--use_table_comment", type=bool, default=False, help="Use table comment as description.")
@click.option("-r", "--relation_type", default='none', type=click.Choice(['none', 'laravel']), help="none: Read database FK, laravel: laravel migration style")
@click.option("-o", "--out_filename", default=None, help="Output filename for the ERD.")
@click.option("--database_url", default=None, help="SQLAlchemy database url. If omitted, use env DATABASE_URL.")
def erd(schema, engine, use_table_comment, relation_type, out_filename, database_url):
    resolved = _resolve_database_url(database_url)
    if not resolved:
        click.echo("[error] DATABASE_URL is not set")
        sys.exit(1)

    sys.exit(run_erd(resolved, schema, engine, use_table_comment, relation_type, out_filename))

        # Generate preview for Mermaid files
        # if engine == 'mermaid' and out_filename.endswith('.mmd'):
        #     svg_filename = out_filename[:-4] + '.svg'
        #     import subprocess
        #     try:
        #         subprocess.run(['mmdc', '-i', out_filename, '-o', svg_filename], check=True)
        #         click.echo("[success] Generated preview: " + svg_filename)
        #     except subprocess.CalledProcessError:
        #         click.echo("[warning] Could not generate preview. Is @mermaid-js/mermaid-cli installed?")
        #     except FileNotFoundError:
        #         click.echo("[warning] Could not generate preview. Please install @mermaid-js/mermaid-cli using: npm install -g @mermaid-js/mermaid-cli")


@click.command()
@click.option("-f", "--file", "project_file", required=True, help="Project TOML file path.")
def project(project_file):
    """
    Run schemas/erd from a project TOML file.
    """
    try:
        cfg = load_project_config(project_file)
    except ProjectConfigError as e:
        click.echo(f"[error] {str(e)}")
        raise SystemExit(1)

    resolved_db = cfg.db.database_url or os.environ.get("DATABASE_URL")
    if not resolved_db:
        click.echo("[error] DATABASE_URL is not set")
        raise SystemExit(1)

    if cfg.command == "schemas":
        raise SystemExit(run_schemas(resolved_db))

    raise SystemExit(
        run_erd(
            resolved_db,
            cfg.erd.schema,
            cfg.erd.engine,
            cfg.erd.use_table_comment,
            cfg.erd.relation_type,
            cfg.erd.out_filename,
        )
    )
