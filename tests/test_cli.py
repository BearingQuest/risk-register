from typer.testing import CliRunner

from bearing_register import __version__
from bearing_register.cli import app

runner = CliRunner()


def test_version_flag_prints_the_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_no_arguments_points_at_help() -> None:
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "brg --help" in result.stdout


def test_unknown_option_is_a_usage_error_with_exit_2() -> None:
    assert runner.invoke(app, ["--nope"]).exit_code == 2
