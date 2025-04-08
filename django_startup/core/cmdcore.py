import click
from .utils import install_env


@click.group()
def django_startup():
    """Main commands for django-startup setup environment"""
    pass


@django_startup.command()
@click.argument('name',)
def project(name):
    """Command for starting a project by his name"""
    install_env(name)
    click.echo(click.style(f"Successfully created project {name}", fg="green"))


