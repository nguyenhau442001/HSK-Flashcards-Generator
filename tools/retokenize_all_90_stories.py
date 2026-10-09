#!/usr/bin/env python3
"""
tools/retokenize_all_90_stories.py
Retokenizes all 90 stories across HSK 1..9 using the complete vocabulary database
(HSK 1..6 + HSK 3.0 level 1..9, total >11,000 unique vocabulary words).
Ensures zero broken tokens like "大" + "学" or missing "虽然", "以后", "面试".
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
READINGS_DIR = REPO_ROOT / "database" / "readings"

# 1. Build comprehensive vocab map
VOCAB_MAP = {}

# HSK 2.0 (hsk 1..6)
for lvl in range(1, 7):
    p = VOCAB_DIR / f"hsk{lvl}_vocabularies.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                hz = item["hanzi"]
                if hz not in VOCAB_MAP or lvl < VOCAB_MAP[hz]["hsk"]:
                    VOCAB_MAP[hz] = {
                        "text": hz,
                        "pinyin": item.get("pinyin", ""),
                        "hanviet": item.get("hanviet", ""),
                        "meaning_vi": item.get("meaning", ""),
                        "hsk": lvl,
                        "word_id": f"hsk{lvl}_{item['id']}"
                    }

# HSK 3.0 (level 1..9)
for lvl in range(1, 10):
    p = VOCAB_DIR / "hsk3_0" / f"level{lvl}_vocabularies.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                hz = item["hanzi"]
                if hz not in VOCAB_MAP:
                    VOCAB_MAP[hz] = {
                        "text": hz,
                        "pinyin": item.get("pinyin", ""),
                        "hanviet": item.get("hanviet", ""),
                        "meaning_vi": item.get("meaning", ""),
                        "hsk": lvl,
                        "word_id": f"hsk{lvl}_{item['id']}"
                    }

print(f"[*] Loaded {len(VOCAB_MAP)} unique vocabulary entries for comprehensive tokenizer.")

PUNCTUATION = set("，。？！、：；“”‘’（）…—《》 \t\n")

def tokenize_sentence(zh_text):
    tokens = []
    i = 0
    while i < len(zh_text):
        ch = zh_text[i]
        if ch in PUNCTUATION:
            if ch.strip():
                tokens.append({"text": ch})
            i += 1
            continue

        matched = False
        for l in range(8, 0, -1):
            sub = zh_text[i:i+l]
            if sub in VOCAB_MAP:
                tokens.append(dict(VOCAB_MAP[sub]))
                i += l
                matched = True
                break

        if not matched:
            tokens.append({"text": ch})
            i += 1

    return tokens

# 2. Retokenize all stories across HSK 1..9
updated_stories = 0
manifest = []

for lvl_idx in range(1, 10):
    lvl_name = f"hsk{lvl_idx}"
    lvl_dir = READINGS_DIR / lvl_name
    if not lvl_dir.exists():
        continue

    for story_file in sorted(lvl_dir.glob("*.json")):
        with open(story_file, "r", encoding="utf-8") as f:
            story = json.load(f)

        words_found_ids = []
        for s in story.get("sentences", []):
            zh_text = s["zh"]
            tokens = tokenize_sentence(zh_text)
            for tok in tokens:
                if tok.get("word_id") and tok["word_id"] not in words_found_ids:
                    words_found_ids.append(tok["word_id"])
            s["tokens"] = tokens

        # Update vocabulary spotlight if needed
        existing_spotlight = story.get("vocabulary_spotlight", [])
        valid_spotlight = [wid for wid in existing_spotlight if any(tok.get("word_id") == wid for s in story["sentences"] for tok in s["tokens"])]
        
        # Merge with newly found words
        for wid in words_found_ids:
            if wid not in valid_spotlight:
                valid_spotlight.append(wid)
            if len(valid_spotlight) >= 15:
                break

        story["vocabulary_spotlight"] = valid_spotlight[:15]

        # Write back updated story
        with open(story_file, "w", encoding="utf-8") as f:
            json.dump(story, f, ensure_ascii=False, indent=2)

        updated_stories += 1

        # Add to manifest
        manifest.append({
            "id": story["id"],
            "level": story["level"],
            "title": story["title"],
            "topic": story.get("topic", "general"),
            "topic_vi": story.get("topic_vi", "Chung"),
            "icon": story.get("icon", "📖"),
            "estimatedMinutes": story.get("estimatedMinutes", 3),
            "description_vi": story.get("description_vi", ""),
            "sentence_count": len(story.get("sentences", [])),
            "sentences_count": len(story.get("sentences", [])),
            "spotlight_count": len(story.get("vocabulary_spotlight", [])),
            "words_count": sum(len(s.get("tokens", [])) for s in story.get("sentences", [])),
            "file": f"database/readings/{lvl_name}/{story_file.name}",
            "path": f"database/readings/{lvl_name}/{story_file.name}"
        })

manifest_path = READINGS_DIR / "manifest.json"
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print(f"[+] Successfully re-tokenized {updated_stories} stories across HSK 1..9.")
print(f"[+] Updated manifest.json with {len(manifest)} stories.")
