#!/usr/bin/env python3
"""Add machine-readable, syllable-separated pinyin to an HSK vocabulary JSON."""

from __future__ import annotations

import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import tempfile
from typing import Any

from pypinyin import Style, load_phrases_dict, pinyin


REPO_ROOT = Path(__file__).resolve().parents[1]
HANZI_RE = re.compile(r"[\u3400-\u9fff]")
BOUNDARY_RE = re.compile(r"[，。！？；,.!?;]")
# Canonical readings used by this course where pypinyin's default differs.
READING_OVERRIDES = {"谁": "shei"}
load_phrases_dict({"很长": [["hen"], ["chang"]]})
TONE_MARKS = {
    "ā": ("a", 1), "á": ("a", 2), "ǎ": ("a", 3), "à": ("a", 4),
    "ē": ("e", 1), "é": ("e", 2), "ě": ("e", 3), "è": ("e", 4),
    "ī": ("i", 1), "í": ("i", 2), "ǐ": ("i", 3), "ì": ("i", 4),
    "ō": ("o", 1), "ó": ("o", 2), "ǒ": ("o", 3), "ò": ("o", 4),
    "ū": ("u", 1), "ú": ("u", 2), "ǔ": ("u", 3), "ù": ("u", 4),
    "ǖ": ("v", 1), "ǘ": ("v", 2), "ǚ": ("v", 3), "ǜ": ("v", 4),
    "ü": ("v", 0),
}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def visible_text(value: Any) -> str:
    parser = _TextExtractor()
    parser.feed(html.unescape(str(value or "")))
    parser.close()
    return "".join(parser.parts).strip()


def roman_letter(character: str) -> tuple[str, int] | None:
    lowered = character.lower()
    if lowered in TONE_MARKS:
        return TONE_MARKS[lowered]
    if "a" <= lowered <= "z":
        return lowered, 0
    return None


def normalize_expected_pinyin(example_zh: str, example_py: str) -> str:
    chinese = visible_text(example_zh)
    displayed_pinyin = visible_text(example_py)
    roman = [parsed for character in displayed_pinyin if (parsed := roman_letter(character))]

    bases: list[tuple[str, int]] = []
    tokens = pinyin(chinese, style=Style.NORMAL, heteronym=False, errors=lambda text: list(text))
    for character, token in zip(chinese, tokens, strict=True):
        value = token[0].lower().replace("ü", "v")
        value = READING_OVERRIDES.get(character, value)
        if re.fullmatch(r"[a-zv]+", value):
            bases.append((value, 1))

    expected_letters = "".join(base for base, _hanzi_count in bases)
    actual_letters = "".join(letter for letter, _tone in roman)
    if expected_letters != actual_letters:
        contracted: list[tuple[str, int]] = []
        index = 0
        while index < len(bases):
            if index + 1 < len(bases) and bases[index + 1][0] == "er":
                contracted.append((f"{bases[index][0]}r", 2))
                index += 2
            else:
                contracted.append(bases[index])
                index += 1
        if "".join(base for base, _hanzi_count in contracted) == actual_letters:
            bases = contracted
            expected_letters = actual_letters
    if expected_letters != actual_letters:
        raise ValueError(
            f"Pinyin does not align with Chinese: {chinese!r} / {displayed_pinyin!r}\n"
            f"expected letters: {expected_letters}\nactual letters:   {actual_letters}"
        )

    syllables: list[str] = []
    offset = 0
    for base, _hanzi_count in bases:
        chunk = roman[offset:offset + len(base)]
        tones = {tone for _letter, tone in chunk if tone}
        if len(tones) > 1:
            raise ValueError(f"Multiple tone marks in syllable {base!r}: {displayed_pinyin!r}")
        tone = tones.pop() if tones else 0
        syllables.append(f"{base}{tone}")
        offset += len(base)

    output: list[str] = []
    syllable_index = 0
    remaining_hanzi = 0
    for character in chinese:
        if HANZI_RE.fullmatch(character):
            if remaining_hanzi:
                remaining_hanzi -= 1
            else:
                output.append(syllables[syllable_index])
                remaining_hanzi = bases[syllable_index][1] - 1
                syllable_index += 1
        elif BOUNDARY_RE.fullmatch(character) and output and output[-1] != "|":
            output.append("|")
    while output and output[-1] == "|":
        output.pop()
    if syllable_index != len(syllables):
        raise ValueError(f"Could not map every syllable for {chinese!r}")
    return " ".join(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", default="hsk1", choices=[f"hsk{i}" for i in range(1, 7)])
    parser.add_argument("--check", action="store_true", help="Validate without changing the JSON file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = REPO_ROOT / "database" / "vocabs" / f"{args.level}_vocabularies.json"
    rows = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for row in rows:
        expected = normalize_expected_pinyin(row["example_zh"], row["example_py"])
        if row.get("expected_pinyin") != expected:
            changed += 1
        reordered: dict[str, Any] = {}
        for key, value in row.items():
            if key != "expected_pinyin":
                reordered[key] = value
            if key == "example_py":
                reordered["expected_pinyin"] = expected
        row.clear()
        row.update(reordered)

    if args.check:
        if changed:
            raise ValueError(f"{path} has {changed} missing or stale expected_pinyin values")
        print(f"Validated {len(rows)} rows in {path.relative_to(REPO_ROOT)}")
        return 0

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)
    print(f"Updated {changed} of {len(rows)} rows in {path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
