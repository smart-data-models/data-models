from typing import Optional

from typing import Callable
import typer
import rich
from . import function_tools

from pysmartdatamodels import commands


cli = typer.Typer()


def main(name: str, lastname: str = typer.Option(...)):
    print(f"Hello {name} {lastname}")


# WIP how to definne global option
# pretty_json: bool = (cli.typer.Option(False,name='--pretty_json', help="Print JSON with Nested format"),)

CLI_COMMAND_LIST = [
    commands.list_all_datamodels,
    commands.list_all_subjects,
    commands.datamodels_subject,
    commands.description_attribute,
    commands.datatype_attribute,
    commands.model_attribute,
    commands.units_attribute,
    commands.attributes_datamodel,
    commands.ngsi_datatype_attribute,
    commands.validate_data_model_schema,
    commands.print_datamodel,
]


class CLI_Command:
    def __init__(self, command: Callable) -> None:
        self._command = command
        self.name = command.__name__
        pass

    def generate(self):
        """creates the cli command against a wrapped command
        generates a wrapper function with same signature as the command

        """

        def command_cli_func(*args, **kwargs):
            """The wrapper for commands to output in CLI freindly format
            use preferably rich.print then typer.echo and least desireable print
            """
            # rich.print(f'{{"args":{args},"kwargs":{kwargs}}}')
            rich.print(self._command(*args, **kwargs))

            return

        self._cloned_cli_func = function_tools.create_function(
            f"cli_{self.name}",
            function_tools.get_function_signature(self._command),
            command_cli_func,
        )
        cli.command(name=f"{self.name}", help=self._command.__doc__)(
            self._cloned_cli_func
        )


def cli_command_factory():
    """Factory to build CLI commands"""
    for cmd in CLI_COMMAND_LIST:
        # typer.echo(f"building command:{cmd.__name__}, {cmd}")
        CLI_Command(cmd).generate()


cli_command_factory()


if __name__ == "__main__":
    cli()
