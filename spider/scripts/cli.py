#!/usr/bin/env python
import click

from .create_dev_vpc import create_dev_vpc
from ..vpc import delete_vpc


__version__ = '0.0.1'


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command(help="Create a development VPC in AWS")
def launch_dev_vpc():
    create_dev_vpc()


@cli.command(help="Delete a VPC in AWS")
@click.option('--force', '-f', is_flag=True, default=False, help='Force the deletion of all sub-resources')
@click.argument('vpc_id')
def remove_vpc(force, vpc_id):
    delete_vpc(vpc_id=vpc_id, force=force)


if __name__ == '__main__':
    cli()
