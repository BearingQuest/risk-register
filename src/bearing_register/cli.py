"""The `brg` command line."""

from typing import Annotated

import typer

from bearing_register import __version__

app = typer.Typer(
    add_completion=False,
    pretty_exceptions_enable=False,
    help="Bearing Register: an open-source, GRC-as-code risk register.",
)


def print_version(show: bool) -> None:
    if show:
        typer.echo(__version__)
        raise typer.Exit


@app.command()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=print_version,
            is_eager=True,
            help="Print the package version and exit.",
        ),
    ] = False,
) -> None:
    """Bearing Register. Nothing else is available yet."""
    typer.echo(f"brg {__version__}: run `brg --help`")
