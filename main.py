import click

from click_command import show_schemas, generate_erd

@click.group()
def cli():
    pass

cli.add_command(show_schemas)
cli.add_command(generate_erd)

if __name__ == '__main__':
    cli()