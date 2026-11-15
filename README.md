# Bearing Register

Open-source, GRC-as-code risk register. Planning stage; not yet usable.

Requires Python 3.14 and [uv](https://docs.astral.sh/uv/).

```console
$ uv sync
$ uv run brg --version
```

## Configuration

Settings are read from environment variables with the `BRG_` prefix, only in
`src/bearing_register/config.py`. An invalid value stops the command with an
error that names the setting, not its value.

| Variable | Default | Allowed values |
| --- | --- | --- |
| `BRG_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

Logs are JSON, one object per line, on stderr, each with a request ID. They
never include secrets or free text from users.

## Checks

```console
$ make help    # list the targets
$ make check   # ruff lint, ruff format check, mypy (strict), pytest with an 85% coverage floor
$ make audit   # pip-audit every package locked in uv.lock, as CI does
$ make hooks   # use .githooks/pre-push, which runs gitleaks on the commits being pushed
```

CI (`.github/workflows/ci.yml`) runs five jobs on every pull request and every
push to `main`: `check`, `gitleaks`, `semgrep`, `pip-audit` and `zizmor`.
`.github/rulesets/main.json` requires all five. The ruleset files are for the
owner to apply; nothing in this repository applies them.

Four more workflows and a Dependabot config run alongside CI; none is a required
check. `pip-audit-daily.yml` audits `uv.lock` every day, `scorecard.yml` runs OpenSSF
Scorecard on `main` and weekly, `claude-review.yml` leaves an automated review on each
non-draft pull request, and `dependabot.yml` proposes weekly updates for `uv` and
GitHub Actions with a 7-day cooldown.

Dependencies are exact-pinned and locked in `uv.lock`. `[tool.uv] exclude-newer =
"7 days"` makes `uv lock` ignore releases newer than seven days.

## Licence

Apache-2.0. See [LICENSE](LICENSE).
