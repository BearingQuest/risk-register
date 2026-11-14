import pytest

from bearing_register.config import Settings, load_settings
from bearing_register.errors import ConfigError


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BRG_LOG_LEVEL", raising=False)


def test_defaults() -> None:
    assert load_settings().log_level == "INFO"


def test_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BRG_LOG_LEVEL", "DEBUG")
    assert load_settings().log_level == "DEBUG"


def test_only_the_brg_prefix_is_read(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    assert load_settings().log_level == "INFO"


@pytest.mark.parametrize("value", ["TRACE", "info", ""])
def test_invalid_values_raise_config_error(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("BRG_LOG_LEVEL", value)
    with pytest.raises(ConfigError, match="invalid configuration"):
        load_settings()


def test_config_error_names_the_field_but_not_the_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BRG_LOG_LEVEL", "s3cr3t-value")
    with pytest.raises(ConfigError) as info:
        load_settings()
    assert "log_level" in str(info.value)
    assert "s3cr3t-value" not in str(info.value)


def test_settings_are_frozen() -> None:
    settings = Settings()
    with pytest.raises(ValueError, match="frozen"):
        settings.log_level = "DEBUG"  # type: ignore[misc]
