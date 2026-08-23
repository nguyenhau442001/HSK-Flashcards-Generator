#!/usr/bin/env python3
"""Build a word-order game sentence bank from existing vocab example sentences.

Reads every database/vocabs/hsk*.json and database/vocabs/topics/*.json,
strips the <u> markup from example_zh, segments it into words with jieba,
and writes database/vocabs/sentence_bank.json with one entry per sentence:
{ zh_tokens: [...], pinyin_tokens: [...], meaning: "...", source: "hsk1" }
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import jieba
from pypinyin import Style, pinyin

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
OUTPUT_PATH = VOCAB_DIR / "sentence_bank.json"
TAG_RE = re.compile(r"</?u>")
END_PUNCT = "。！？!?"


def strip_tags(text: str) -> str:
    return TAG_RE.sub("", text)


def tokenize(sentence: str) -> list[str]:
    sentence = sentence.rstrip(END_PUNCT)
    return [tok for tok in jieba.cut(sentence) if tok.strip()]


def pinyin_for(token: str) -> str:
    syllables = pinyin(token, style=Style.TONE, strict=False)
    return "".join(s[0] for s in syllables)


def build_entries(vocab_path: Path, source: str) -> list[dict]:
    words = json.loads(vocab_path.read_text(encoding="utf-8"))
    seen: set[str] = set()
    entries = []
    for word in words:
        raw = word.get("example_zh")
        meaning = word.get("example_vi")
        if not raw or not meaning:
            continue
        sentence = strip_tags(raw)
        if sentence in seen:
            continue
        seen.add(sentence)
        tokens = tokenize(sentence)
        if len(tokens) < 3:
            continue
        entries.append({
            "zh_tokens": tokens,
            "pinyin_tokens": [pinyin_for(tok) for tok in tokens],
            "meaning": strip_tags(meaning),
            "source": source,
        })
    return entries


def main() -> None:
    all_entries: list[dict] = []

    for level_num in range(1, 7):
        path = VOCAB_DIR / f"hsk{level_num}_vocabularies.json"
        if path.exists():
            all_entries.extend(build_entries(path, f"hsk{level_num}"))

    topics_dir = VOCAB_DIR / "topics"
    if topics_dir.exists():
        for topic_path in sorted(topics_dir.glob("*.json")):
            all_entries.extend(build_entries(topic_path, f"topic_{topic_path.stem}"))

    OUTPUT_PATH.write_text(
        json.dumps(all_entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(all_entries)} sentences to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
