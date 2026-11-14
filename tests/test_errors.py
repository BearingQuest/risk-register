import pytest

from bearing_register.errors import BearingRegisterError, ConfigError, InputError


@pytest.mark.parametrize("error", [ConfigError, InputError])
def test_specific_errors_are_bearing_register_errors(error: type[BearingRegisterError]) -> None:
    assert issubclass(error, BearingRegisterError)
    assert str(error("boom")) == "boom"


def test_the_specific_errors_are_distinct() -> None:
    assert not issubclass(ConfigError, InputError)
    assert not issubclass(InputError, ConfigError)
