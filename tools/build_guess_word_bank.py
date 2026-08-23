#!/usr/bin/env python3
"""Build a "guess the word" (emoji) game bank from existing vocab files.

Only words with a clear, curated emoji mapping (EMOJI_MAP below) are
included. Reads every database/vocabs/hsk*.json and
database/vocabs/topics/*.json, and writes
database/vocabs/guess_word_bank.json with one entry per matched word:
{ emoji, hanzi, pinyin, meaning }
"""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
OUTPUT_PATH = VOCAB_DIR / "guess_word_bank.json"

# Curated hanzi -> emoji mapping. Only words with an unambiguous visual
# match are included; add more here as new vocab decks are built.
EMOJI_MAP = {
    "爸爸": "👨", "妈妈": "👩", "儿子": "👦", "女儿": "👧",
    "猫": "🐱", "狗": "🐶",
    "杯子": "🥤", "茶": "🍵", "水": "💧", "米饭": "🍚", "苹果": "🍎", "水果": "🍉",
    "书": "📖", "字": "🔤", "桌子": "🪑", "椅子": "🪑",
    "电脑": "💻", "电视": "📺", "电影": "🎬", "飞机": "✈️", "出租车": "🚕",
    "医院": "🏥", "医生": "🧑‍⚕️", "学校": "🏫", "商店": "🏬", "饭店": "🏨",
    "衣服": "👕", "钱": "💰",
    "太阳": "☀️", "下雨": "🌧️", "冷": "🥶", "热": "🥵",
    "中国": "🇨🇳", "北京": "🏯",
    "月": "🌙", "年": "📅",
    "笑": "😄", "哭": "😢",
    "手机": "📱", "软件": "💾", "硬件": "🖥️",
}


def build_entries(vocab_path: Path, source: str) -> list[dict]:
    words = json.loads(vocab_path.read_text(encoding="utf-8"))
    entries = []
    for word in words:
        hanzi = word.get("hanzi")
        emoji = EMOJI_MAP.get(hanzi)
        if not emoji:
            continue
        entries.append({
            "emoji": emoji,
            "hanzi": hanzi,
            "pinyin": word.get("pinyin"),
            "meaning": word.get("meaning"),
            "source": source,
        })
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
