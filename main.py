import click

from click_command import schemas, erd

@click.group()
def cli():
    pass

cli.add_command(schemas)
cli.add_command(erd)

if __name__ == '__main__':
    cli()