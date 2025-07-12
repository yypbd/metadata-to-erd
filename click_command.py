import os

import click
from dotenv import load_dotenv

from src.d2_erd import D2Erd
from src.database import Database
from src.plantuml_erd import PlantumlErd

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

@click.command()
def show_schemas():
    database = Database()

    if database.connect(DATABASE_URL):
        schemas = database.get_schemas()
        for schema in schemas:
            click.echo(schema)
    else:
        click.echo("[error] cannot connect to database")

@click.command()
@click.option("-s", "--schema", default='', help="Database schema name.")
@click.option("-e", "--engine", default='puml', type=click.Choice(['puml', 'd2']), help="PlantUML or D2")
@click.option("-c", "--use_table_comment", type=bool, default=False, help="Use table comment as description.")
@click.option("-r", "--relation_type", default='none', type=click.Choice(['none', 'laravel']), help="none: Read database FK, laravel: laravel migration style")
@click.option("-o", "--out_filename", default=None, help="Output filename for the ERD.")
def generate_erd(schema, engine, use_table_comment, relation_type, out_filename):
    if out_filename is not None and os.path.exists(out_filename):
        click.echo('[error] Exists - ' + out_filename)
        return

    database = Database()
    if not database.connect(DATABASE_URL):
        click.echo("[error] cannot connect to database")
        return

    if engine == 'd2':
        erd = D2Erd(database)
    else:
        erd = PlantumlErd(database)

    schemas = database.get_schemas()
    if not schemas:
        click.echo('[error] Schema is empty')
        return

    if not schema:
        schema = schemas[0]

    if schema not in schemas:
        click.echo('[error] Not exists schemas')
        return

    output = erd.get_erd(schema, use_table_comment, relation_type)
    if out_filename is None:
        click.echo(output)
    else:
        with open(out_filename, "w") as text_file:
            text_file.write(output)
        click.echo("[success] Save puml to " + out_filename)