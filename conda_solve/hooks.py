"""
Insert your plugin hook definitions

We have illustrated how this is done by defining a simple "hello conda"
subcommand for you.
"""

from conda.plugins import hookimpl, CondaSubcommand

from .main import solve_subcommand


@hookimpl
def conda_subcommands() -> None:
    yield CondaSubcommand(
        name="solve",
        action=solve_subcommand,
        summary="Solve an environment",
    )
