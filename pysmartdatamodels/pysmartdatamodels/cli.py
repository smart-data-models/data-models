from typing import Optional

import typer
from pysmartdatamodels import commands


cli = typer.Typer()


@cli.command(help=commands.list_all_datamodels.__doc__)
def list_all_datamodels():
    for model in commands.list_all_datamodels():
        typer.echo(f"{model}")


if __name__ == "__main__":
    cli()
