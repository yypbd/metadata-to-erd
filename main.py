import click

from click_command import schemas, erd, project

@click.group()
def cli():
    pass

cli.add_command(schemas)
cli.add_command(erd)
cli.add_command(project)

if __name__ == '__main__':
    cli()