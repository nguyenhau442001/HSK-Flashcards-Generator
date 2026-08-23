#!/usr/bin/env python3
"""Build a word bank for the memory-matching (flip-card) game.

Reads every database/vocabs/hsk*.json and database/vocabs/topics/*.json
and writes database/vocabs/memory_game_bank.json with one entry per word:
{ hanzi, meaning, source }. The game picks a random subset per round.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
OUTPUT_PATH = VOCAB_DIR / "memory_game_bank.json"


def build_entries(vocab_path: Path, source: str) -> list[dict]:
    words = json.loads(vocab_path.read_text(encoding="utf-8"))
    entries = []
    for word in words:
        hanzi = word.get("hanzi")
        meaning = word.get("meaning")
        if not hanzi or not meaning:
            continue
        entries.append({"hanzi": hanzi, "meaning": meaning, "source": source})
    return entries


def main() -> None:
    all_entries: list[dict] = []
    seen_hanzi: set[str] = set()

    for level_num in range(1, 7):
        path = VOCAB_DIR / f"hsk{level_num}_vocabularies.json"
        if path.exists():
            for entry in build_entries(path, f"hsk{level_num}"):
                if entry["hanzi"] in seen_hanzi:
                    continue
                seen_hanzi.add(entry["hanzi"])
                all_entries.append(entry)

    topics_dir = VOCAB_DIR / "topics"
    if topics_dir.exists():
        for topic_path in sorted(topics_dir.glob("*.json")):
            for entry in build_entries(topic_path, f"topic_{topic_path.stem}"):
                if entry["hanzi"] in seen_hanzi:
                    continue
                seen_hanzi.add(entry["hanzi"])
                all_entries.append(entry)

    OUTPUT_PATH.write_text(
        json.dumps(all_entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(all_entries)} words to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
