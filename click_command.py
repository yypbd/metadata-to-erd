import os
import sys

import click
from dotenv import load_dotenv

from src.d2_erd import D2Erd
from src.database import Database
from src.mermaid_erd import MermaidErd
from src.plantuml_erd import PlantumlErd

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

@click.command()
def schemas():
    database = Database()

    if database.connect(DATABASE_URL):
        schemas = database.get_schemas()
        for schema in schemas:
            click.echo(schema)
    else:
        click.echo("[error] cannot connect to database")

@click.command()
@click.option("-s", "--schema", default='', help="Database schema name.")
@click.option("-e", "--engine", default='puml', type=click.Choice(['puml', 'd2', 'mermaid']), help="PlantUML, D2 or Mermaid")
@click.option("-c", "--use_table_comment", type=bool, default=False, help="Use table comment as description.")
@click.option("-r", "--relation_type", default='none', type=click.Choice(['none', 'laravel']), help="none: Read database FK, laravel: laravel migration style")
@click.option("-o", "--out_filename", default=None, help="Output filename for the ERD.")
def erd(schema, engine, use_table_comment, relation_type, out_filename):
    if out_filename is not None and os.path.exists(out_filename):
        click.echo(f'[error] File exists - {out_filename}')
        sys.exit(1)

    database = Database()
    try:
        if not database.connect(DATABASE_URL):
            click.echo("[error] Cannot connect to database")
            sys.exit(1)

        if engine == 'd2':
            erd = D2Erd(database)
        elif engine == 'mermaid':
            erd = MermaidErd(database)
        else:
            erd = PlantumlErd(database)

        schemas = database.get_schemas()
        if not schemas:
            click.echo('[error] No schemas found')
            sys.exit(1)

        if not schema:
            schema = schemas[0]

        if schema not in schemas:
            click.echo(f'[error] Schema "{schema}" not found')
            sys.exit(1)
    except Exception as e:
        click.echo(f"[error] {str(e)}")
        sys.exit(1)

    output = erd.get_erd(schema, use_table_comment, relation_type)
    if out_filename is None:
        click.echo(output)
    else:
        with open(out_filename, "w") as text_file:
            text_file.write(output)
        click.echo("[success] Save to " + out_filename)

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
