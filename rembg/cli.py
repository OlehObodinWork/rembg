import click
from dotenv import load_dotenv




from . import _version
from .commands import command_functions


@click.group()
@click.version_option(version=_version.get_versions()["version"])
def _main() -> None:
    load_dotenv()


for command in command_functions:
    _main.add_command(command)

_main()
