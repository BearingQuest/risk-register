"""Keeps the approved PRD and the design pack intact.

`docs/PRD.md`, `docs/design.md` and `docs/design/` are committed as approved on 15 Nov 2026.
These checks fail if a requirement ID is lost or repeated, if a snapshot file changes without
the hash recorded in `docs/design.md` changing with it, or if a logo gains anything active.
"""

from __future__ import annotations

import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
DESIGN = DOCS / "design"
LOGOS = DESIGN / "logos"
SCREENS = DESIGN / "screens"

PRD_LAST_ID = 106
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
TIER_TOKENS = ["tier-low", "tier-medium", "tier-high", "tier-critical"]
HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _design_section(heading: str) -> str:
    """The text of one `## <heading>` section of docs/design.md, up to the next `## `."""
    text = (DOCS / "design.md").read_text(encoding="utf-8")
    match = re.search(
        rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.DOTALL | re.MULTILINE
    )
    assert match, f"docs/design.md has no '## {heading}' section"
    return match.group(1)


def _logo_hashes() -> dict[str, str]:
    """File name to SHA-256, from the rows of the Logos table in docs/design.md."""
    rows = re.findall(
        r"^\| `([^`]+\.svg)` \| `([0-9a-f]{64})` \|", _design_section("Logos"), re.MULTILINE
    )
    return dict(rows)


def _screen_names() -> list[str]:
    """File names, from the rows of the Screens table in docs/design.md."""
    return re.findall(r"^\| `([^`]+\.png)` \|", _design_section("Screens"), re.MULTILINE)


def _prd_requirement_ids() -> list[int]:
    text = (DOCS / "PRD.md").read_text(encoding="utf-8")
    return [int(n) for n in re.findall(r"^- \*\*R(\d+)\.\*\*", text, re.MULTILINE)]


def test_prd_says_version_1_0() -> None:
    text = (DOCS / "PRD.md").read_text(encoding="utf-8")
    assert re.search(r"^Version 1\.0\b", text, re.MULTILINE)


def test_prd_requirement_ids_are_unique() -> None:
    ids = _prd_requirement_ids()
    duplicates = sorted({n for n in ids if ids.count(n) > 1})
    assert not duplicates, f"requirement IDs defined more than once: {duplicates}"


def test_prd_requirement_ids_run_r1_to_r106_without_gaps() -> None:
    ids = _prd_requirement_ids()
    missing = sorted(set(range(1, PRD_LAST_ID + 1)) - set(ids))
    extra = sorted(set(ids) - set(range(1, PRD_LAST_ID + 1)))
    assert not missing, f"requirement IDs missing from R1 to R{PRD_LAST_ID}: {missing}"
    assert not extra, f"requirement IDs past R{PRD_LAST_ID}: {extra}"


def test_tokens_json_matches_hash_recorded_in_design_md() -> None:
    text = (DOCS / "design.md").read_text(encoding="utf-8")
    match = re.search(r"`docs/design/tokens\.json`[^\n]*?SHA-256 `([0-9a-f]{64})`", text)
    assert match, "docs/design.md records no SHA-256 for docs/design/tokens.json"
    assert _sha256(DESIGN / "tokens.json") == match.group(1)


def test_tokens_json_has_tier_tokens_with_light_and_dark_values() -> None:
    data = json.loads((DESIGN / "tokens.json").read_text(encoding="utf-8"))
    values = {token["name"]: token["value"] for token in data["color"]["tokens"]}
    for name in [*TIER_TOKENS, *(f"on-{tier}" for tier in TIER_TOKENS)]:
        assert name in values, f"tokens.json has no {name}"
        for theme in ("light", "dark"):
            assert HEX_COLOR.fullmatch(values[name].get(theme, "")), f"{name} has no {theme} color"


def test_logo_files_match_hashes_in_design_md() -> None:
    recorded = _logo_hashes()
    actual = {path.name: _sha256(path) for path in LOGOS.iterdir()}
    assert recorded, "the Logos table in docs/design.md has no rows"
    assert actual == recorded


def test_logos_table_lists_no_file_that_is_missing() -> None:
    on_disk = {path.name for path in LOGOS.iterdir()}
    assert not set(_logo_hashes()) - on_disk


@pytest.mark.parametrize("name", sorted(_logo_hashes()))
def test_logo_is_inert_svg(name: str) -> None:
    root = ET.parse(LOGOS / name).getroot()  # noqa: S314  # files are hash-pinned by test_logo_files_match_hashes_in_design_md
    for element in root.iter():
        tag = element.tag.rpartition("}")[2].lower()
        assert tag not in {"script", "foreignobject"}, f"{name} has a <{tag}> element"
        for attribute, value in element.attrib.items():
            local = attribute.rpartition("}")[2].lower()
            assert not local.startswith("on"), f"{name} has an {local} attribute"
            if local == "href":
                assert value.startswith("#"), f"{name} has an href to {value!r}"


def test_screens_are_exactly_the_nine_pngs_in_design_md() -> None:
    listed = _screen_names()
    assert len(listed) == 9
    assert len(set(listed)) == 9
    assert sorted(path.name for path in SCREENS.iterdir()) == sorted(listed)


@pytest.mark.parametrize("name", sorted(_screen_names()))
def test_screen_is_a_valid_png(name: str) -> None:
    data = (SCREENS / name).read_bytes()
    assert data[:8] == PNG_SIGNATURE
    length, kind = struct.unpack(">I4s", data[8:16])
    assert (length, kind) == (13, b"IHDR")
    width, height = struct.unpack(">II", data[16:24])
    assert width > 0
    assert height > 0
