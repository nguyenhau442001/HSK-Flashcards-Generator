#!/usr/bin/env python3
"""
tools/generate_all_450_stories.py
Generates 40 additional stories for each level HSK 1 to HSK 9 (stories 11..50),
bringing the total to 50 stories per level (450 stories across HSK 1..9),
and rebuilds database/readings/manifest.json.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
READINGS_DIR = REPO_ROOT / "database" / "readings"

# 1. Load full vocabulary database HSK 1..9 into tokenizer map
VOCAB_MAP = {}

# 1.1 HSK 2.0 (Levels 1 to 6)
for lvl in range(1, 7):
    p = VOCAB_DIR / f"hsk{lvl}_vocabularies.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                hanzi = item["hanzi"]
                if hanzi not in VOCAB_MAP or lvl < VOCAB_MAP[hanzi]["hsk"]:
                    VOCAB_MAP[hanzi] = {
                        "text": hanzi,
                        "pinyin": item["pinyin"],
                        "hanviet": item.get("hanviet", ""),
                        "meaning_vi": item["meaning"],
                        "hsk": lvl,
                        "word_id": f"hsk{lvl}_{item['id']}"
                    }

# 1.2 HSK 3.0 (Levels 1 to 9)
for lvl in range(1, 10):
    p = VOCAB_DIR / "hsk3_0" / f"level{lvl}_vocabularies.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                hanzi = item["hanzi"]
                if hanzi not in VOCAB_MAP:
                    VOCAB_MAP[hanzi] = {
                        "text": hanzi,
                        "pinyin": item["pinyin"],
                        "hanviet": item.get("hanviet", ""),
                        "meaning_vi": item["meaning"],
                        "hsk": lvl,
                        "word_id": f"hsk{lvl}_{item['id']}"
                    }

print(f"[*] Loaded {len(VOCAB_MAP)} unique vocabulary entries for tokenizer.")

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

def make_story(level, idx, title_zh, title_vi, topic, topic_vi, icon, minutes, desc_vi, sentences, quiz_data):
    sid = f"{level.lower()}_story_{idx:03d}"
    
    sentences_json = []
    words_found_ids = []
    
    for sidx, (zh, py, vi) in enumerate(sentences):
        tokens = tokenize_sentence(zh)
        for tok in tokens:
            if tok.get("word_id") and tok["word_id"] not in words_found_ids:
                words_found_ids.append(tok["word_id"])
        
        sentences_json.append({
            "id": f"s{sidx+1}",
            "zh": zh,
            "pinyin": py,
            "vi": vi,
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": tokens
        })
        
    spotlight_ids = words_found_ids[:15]
    if len(spotlight_ids) < 8:
        spotlight_ids = words_found_ids
        
    formatted_quiz = []
    for qidx, (q_vi, opts_vi, ans_idx, exp_vi) in enumerate(quiz_data):
        formatted_quiz.append({
            "id": f"q{qidx+1}",
            "question_vi": q_vi,
            "options_vi": opts_vi,
            "answer": ans_idx,
            "explanation_vi": exp_vi
        })

    return {
        "id": sid,
        "level": level,
        "title": {"zh": title_zh, "vi": title_vi},
        "topic": topic,
        "topic_vi": topic_vi,
        "icon": icon,
        "estimatedMinutes": minutes,
        "description_vi": desc_vi,
        "sentences": sentences_json,
        "vocabulary_spotlight": spotlight_ids,
        "quiz": formatted_quiz
    }

def main():
    sys.path.insert(0, str(REPO_ROOT / "tools"))
    
    level_modules = [
        ("HSK1", "story_data.hsk1_40_stories", "HSK1_STORIES_40"),
        ("HSK2", "story_data.hsk2_40_stories", "HSK2_STORIES_40"),
        ("HSK3", "story_data.hsk3_40_stories", "HSK3_STORIES_40"),
        ("HSK4", "story_data.hsk4_40_stories", "HSK4_STORIES_40"),
        ("HSK5", "story_data.hsk5_40_stories", "HSK5_STORIES_40"),
        ("HSK6", "story_data.hsk6_40_stories", "HSK6_STORIES_40"),
        ("HSK7", "story_data.hsk7_40_stories", "HSK7_STORIES_40"),
        ("HSK8", "story_data.hsk8_40_stories", "HSK8_STORIES_40"),
        ("HSK9", "story_data.hsk9_40_stories", "HSK9_STORIES_40"),
    ]
    
    total_generated = 0
    for level_name, mod_name, var_name in level_modules:
        try:
            mod = __import__(mod_name, fromlist=[var_name])
            stories_data = getattr(mod, var_name)
        except Exception as e:
            print(f"[!] Warning: Could not import {mod_name}.{var_name}: {e}")
            continue
            
        lvl_dir = READINGS_DIR / level_name.lower()
        lvl_dir.mkdir(parents=True, exist_ok=True)
        
        for item in stories_data:
            idx, title_zh, title_vi, topic, topic_vi, icon, minutes, desc_vi, sents, quiz = item
            story_json = make_story(level_name, idx, title_zh, title_vi, topic, topic_vi, icon, minutes, desc_vi, sents, quiz)
            
            target_path = lvl_dir / f"{story_json['id']}.json"
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(story_json, f, ensure_ascii=False, indent=2)
            total_generated += 1
            
        print(f"[+] Processed {len(stories_data)} stories for {level_name}.")

    print(f"[*] Total new stories generated: {total_generated}")

    # Rebuild manifest.json for ALL readings (HSK 1..9)
    manifest = []
    for lvl_idx in range(1, 10):
        lvl_name = f"hsk{lvl_idx}"
        lvl_dir = READINGS_DIR / lvl_name
        if not lvl_dir.exists():
            continue
        for story_file in sorted(lvl_dir.glob("*.json")):
            with open(story_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                manifest.append({
                    "id": data["id"],
                    "level": data["level"],
                    "title": data["title"],
                    "topic": data.get("topic", "general"),
                    "topic_vi": data.get("topic_vi", "Chung"),
                    "icon": data.get("icon", "📖"),
                    "estimatedMinutes": data.get("estimatedMinutes", 3),
                    "description_vi": data.get("description_vi", ""),
                    "sentence_count": len(data.get("sentences", [])),
                    "sentences_count": len(data.get("sentences", [])),
                    "spotlight_count": len(data.get("vocabulary_spotlight", [])),
                    "words_count": sum(len(s.get("tokens", [])) for s in data.get("sentences", [])),
                    "file": f"database/readings/{lvl_name}/{story_file.name}",
                    "path": f"database/readings/{lvl_name}/{story_file.name}"
                })

    manifest_path = READINGS_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"[+] Rebuilt manifest.json with {len(manifest)} stories total across HSK 1..9.")

if __name__ == "__main__":
    main()
