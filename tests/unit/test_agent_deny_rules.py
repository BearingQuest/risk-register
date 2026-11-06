"""CLAUDE.md human gates enforced by Claude Code permission rules (.claude/settings.json)."""

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SETTINGS = REPO_ROOT / ".claude" / "settings.json"

# Rules match command text, so they're a guardrail, not a sandbox (docs/decisions.md 2026-11-05,
# agent mode lock row).
RECURSIVE_DELETE_DENY = {
    "Bash(rm -rf *)",
    "Bash(rm -fr *)",
    "Bash(rm -Rf *)",
    "Bash(rm -fR *)",
}
REQUIRED_DENY = {
    "Bash(gh pr merge:*)",
    "Bash(gh pr review:*)",
    "Bash(gh pr comment:*)",
}
REQUIRED_ASK = {"Bash(git push:*)", "Bash(gh pr:*)", "Bash(gh api:*)", "Bash(python3:*)"}

# Options before the subcommand (`gh --repo … pr merge`) slip past the prefix rules above.
# A trailing `*` matches the bare form only when it's the rule's only wildcard, hence the pairs.
OPTION_FIRST_DENY = {
    "Bash(gh * pr merge)",
    "Bash(gh * pr merge *)",
    "Bash(gh * pr review)",
    "Bash(gh * pr review *)",
    "Bash(gh * pr comment)",
    "Bash(gh * pr comment *)",
}
# Ask, not deny, so a legitimate `git -C … push` still just prompts.
OPTION_FIRST_ASK = {"Bash(git * push)", "Bash(git * push *)"}


def settings() -> dict[str, Any]:
    result: dict[str, Any] = json.loads(SETTINGS.read_text(encoding="utf-8"))
    return result


def rules(kind: str) -> list[str]:
    result: list[str] = settings()["permissions"][kind]
    return result


def test_recursive_force_delete_is_denied() -> None:
    assert set(rules("deny")) >= RECURSIVE_DELETE_DENY


def test_human_gates_are_denied() -> None:
    # Merging, reviewing and replying on PRs stay with Dusten (CLAUDE.md).
    assert set(rules("deny")) >= REQUIRED_DENY | OPTION_FIRST_DENY


def test_outward_facing_commands_ask_first() -> None:
    assert set(rules("ask")) >= REQUIRED_ASK | OPTION_FIRST_ASK


def test_auto_and_bypass_modes_are_disabled() -> None:
    permissions = settings()["permissions"]
    assert permissions["disableAutoMode"] == "disable"
    assert permissions["disableBypassPermissionsMode"] == "disable"


def test_project_settings_grant_no_allow_rules() -> None:
    assert "allow" not in settings()["permissions"]
