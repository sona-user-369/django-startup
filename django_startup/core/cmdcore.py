import click
from .utils import install_env


@click.group()
def django_startup():
    """Main command for django-startup"""
    pass


@django_startup.command()
@click.argument('name',)
def project(name):
    """Command for starting the project"""
    install_env(name)
    click.echo(f"Successfully created project {name}")


