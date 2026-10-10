#!/usr/bin/env python3
"""
tools/generate_all_450_stories.py
Generates 40 additional stories for each level HSK 1 to HSK 9 (stories 11..50),
bringing the total to 50 stories per level (450 stories across HSK 1..9),
and rebuilds database/readings/manifest.json.
"""

import json
import sys
import re
from pathlib import Path
import pypinyin

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
READINGS_DIR = REPO_ROOT / "database" / "readings"

# 1. Load Sino-Vietnamese (Hán - Việt) dictionary
HV_DICT_PATH = REPO_ROOT / "assets" / "js" / "hanviet-dict.js"
HV_CHARS = {}
if HV_DICT_PATH.exists():
    with open(HV_DICT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'const HANVIET_CHARS\s*=\s*(\{.*?\});', content, re.DOTALL)
    if m:
        try:
            HV_CHARS = json.loads(m.group(1))
        except Exception as e:
            print("[!] Warning parsing HANVIET_CHARS:", e)

# 2. Load full vocabulary database HSK 1..9 into tokenizer map & character index
VOCAB_MAP = {}
VOCAB_BY_ID = {}
CHAR_COMPOUNDS = {}

# 2.1 HSK 3.0 (Levels 1 to 9)
for lvl in range(1, 10):
    p = VOCAB_DIR / "hsk3_0" / f"level{lvl}_vocabularies.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                hanzi = item["hanzi"]
                wid = f"hsk{lvl}_{item['id']}"
                VOCAB_BY_ID[wid] = item
                if hanzi not in VOCAB_MAP:
                    VOCAB_MAP[hanzi] = {
                        "text": hanzi,
                        "pinyin": item["pinyin"],
                        "hanviet": item.get("hanviet", HV_CHARS.get(hanzi, "")),
                        "meaning_vi": item["meaning"],
                        "hsk": lvl,
                        "word_id": wid
                    }
                for ch in hanzi:
                    if ch not in CHAR_COMPOUNDS:
                        CHAR_COMPOUNDS[ch] = []
                    CHAR_COMPOUNDS[ch].append((lvl, len(hanzi), item["hanzi"], item["meaning"], wid))

# 2.2 HSK 2.0 (Levels 1 to 6)
for lvl in range(1, 7):
    p = VOCAB_DIR / f"hsk{lvl}_vocabularies.json"
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            for item in json.load(f):
                hanzi = item["hanzi"]
                wid = f"hsk{lvl}_{item['id']}"
                if wid not in VOCAB_BY_ID:
                    VOCAB_BY_ID[wid] = item
                if hanzi not in VOCAB_MAP or lvl < VOCAB_MAP[hanzi]["hsk"]:
                    VOCAB_MAP[hanzi] = {
                        "text": hanzi,
                        "pinyin": item["pinyin"],
                        "hanviet": item.get("hanviet", HV_CHARS.get(hanzi, "")),
                        "meaning_vi": item["meaning"],
                        "hsk": lvl,
                        "word_id": wid
                    }
                for ch in hanzi:
                    if ch not in CHAR_COMPOUNDS:
                        CHAR_COMPOUNDS[ch] = []
                    CHAR_COMPOUNDS[ch].append((lvl, len(hanzi), item["hanzi"], item["meaning"], wid))

# 2.3 Explicit mappings for common standalone measure words and characters
MEASURE_AND_COMMON = {
    '杯': ('bēi', 'Bôi', 'cốc, ly, chén (lượng từ, danh từ)', 1, 'hsk1_10'),
    '温': ('wēn', 'Ôn', 'ấm, ôn hòa, nhiệt độ', 2, 'hsk4_151'),
    '碗': ('wǎn', 'Oản', 'bát, chén (lượng từ, danh từ)', 3, 'hsk3_948'),
    '盘': ('pán', 'Bàn', 'đĩa, mâm (lượng từ, danh từ)', 3, 'hsk6_970'),
    '瓶': ('píng', 'Bình', 'chai, lọ, bình (lượng từ, danh từ)', 3, 'hsk3_878'),
    '双': ('shuāng', 'Song', 'đôi (lượng từ)', 2, 'hsk3_925'),
    '份': ('fèn', 'Phần', 'phần, suất, bản (lượng từ)', 3, 'hsk4_203'),
    '张': ('zhāng', 'Trương', 'tờ, tấm, chiếc (lượng từ)', 1, 'hsk3_1046'),
    '把': ('bǎ', 'Bả', 'cái, chiếc, nắm (lượng từ)', 3, 'hsk3_606'),
    '架': ('jià', 'Giá', 'chiếc, cỗ (lượng từ máy bay, máy móc)', 4, 'hsk5_560'),
    '辆': ('liàng', 'Lượng', 'chiếc (lượng từ xe cộ)', 3, 'hsk3_836'),
    '条': ('tiáo', 'Điều', 'con, sợi, cái (lượng từ)', 2, 'hsk2_443'),
    '只': ('zhī', 'Chích', 'con, cái, chiếc (lượng từ)', 2, 'hsk1_609'),
    '件': ('jiàn', 'Kiện', 'chiếc, cái, vụ (lượng từ)', 2, 'hsk1_138'),
    '本': ('běn', 'Bổn', 'cuốn, quyển (lượng từ)', 1, 'hsk1_6'),
    '块': ('kuài', 'Khối', 'miếng, cục, đồng (tiền) (lượng từ)', 1, 'hsk1_532'),
    '趟': ('tàng', 'Thảng', 'chuyến, lượt (lượng từ)', 4, 'hsk4_722'),
    '顿': ('dùn', 'Đốn', 'bữa, trận (lượng từ)', 4, 'hsk4_179'),
    '座': ('zuò', 'Tọa', 'tòa, ngọn (lượng từ công trình, núi)', 3, 'hsk4_991'),
    '颗': ('kē', 'Khoả', 'hạt, viên, ngôi (lượng từ)', 4, 'hsk5_662'),
    '朵': ('duǒ', 'Đóa', 'đóa, bông (lượng từ hoa, mây)', 3, 'hsk5_311'),
    '根': ('gēn', 'Căn', 'cọng, que, sợi, rễ (lượng từ, danh từ)', 4, 'hsk5_403'),
    '段': ('duàn', 'Đoạn', 'đoạn, quãng (lượng từ)', 3, 'hsk3_703'),
    '幅': ('fú', 'Bức', 'bức, tấm (lượng từ tranh)', 5, 'hsk4_207'),
    '套': ('tào', 'Thao', 'bộ, bộ đồ (lượng từ)', 4, 'hsk5_1106'),
    '台': ('tái', 'Đài', 'chiếc, cái (lượng từ máy móc)', 3, 'hsk4_714'),
    '场': ('chǎng', 'Trường', 'trận, buổi (lượng từ)', 3, 'hsk4_73'),
    '次': ('cì', 'Thứ', 'lần, chuyến (lượng từ)', 2, 'hsk2_323'),
    '遍': ('biàn', 'Biến', 'lần, lượt (lượng từ)', 3, 'hsk3_627')
}

for ch, (py, hv, mean, lvl, wid) in MEASURE_AND_COMMON.items():
    if wid in VOCAB_BY_ID:
        VOCAB_MAP[ch] = {
            'text': ch,
            'pinyin': py,
            'hanviet': hv,
            'meaning_vi': mean,
            'hsk': lvl,
            'word_id': wid
        }

print(f"[*] Loaded {len(VOCAB_MAP)} unique vocabulary entries for tokenizer.")
print(f"[*] Loaded {len(VOCAB_BY_ID)} valid vocabulary items.")

PUNCTUATION = set("，。？！、：；“”‘’（）《》〈〉【】[]()…—· \t\n")

def tokenize_sentence(zh_text, story_lvl=1):
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
            if '\u4e00' <= ch <= '\u9fff':
                py = pypinyin.lazy_pinyin(ch, style=pypinyin.Style.TONE)[0]
                hv = HV_CHARS.get(ch, '')
                tok = {
                    "text": ch,
                    "pinyin": py,
                    "hanviet": hv,
                    "meaning_vi": f"Âm Hán-Việt: {hv}" if hv else ch,
                    "hsk": story_lvl
                }
                if ch in CHAR_COMPOUNDS:
                    valid_compounds = [c for c in CHAR_COMPOUNDS[ch] if c[4] in VOCAB_BY_ID]
                    if valid_compounds:
                        best = sorted(valid_compounds, key=lambda x: (x[1], x[0]))[0]
                        c_lvl, c_len, c_hanzi, c_meaning, c_wid = best
                        tok["meaning_vi"] = f"{c_meaning} (trong {c_hanzi})" if len(c_hanzi) > 1 else c_meaning
                        tok["hsk"] = c_lvl
                        tok["word_id"] = c_wid
                tokens.append(tok)
            else:
                tokens.append({"text": ch})
            i += 1

    return tokens

def make_story(level, idx, title_zh, title_vi, topic, topic_vi, icon, minutes, desc_vi, sentences, quiz_data):
    sid = f"{level.lower()}_story_{idx:03d}"
    story_lvl = int("".join(filter(str.isdigit, level)) or "1")
    
    sentences_json = []
    words_found_ids = []
    
    for sidx, (zh, py, vi) in enumerate(sentences):
        tokens = tokenize_sentence(zh, story_lvl)
        for tok in tokens:
            wid = tok.get("word_id")
            if wid and wid in VOCAB_BY_ID and wid not in words_found_ids:
                words_found_ids.append(wid)
        
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

    # Ensure existing stories 1..10 in all levels are tokenized with enhanced tokenizer
    retokenized_count = 0
    for lvl_idx in range(1, 10):
        lvl_name = f"hsk{lvl_idx}"
        lvl_dir = READINGS_DIR / lvl_name
        if not lvl_dir.exists():
            continue
        for story_file in sorted(lvl_dir.glob("*.json")):
            stem_num = story_file.stem.split('_')[-1]
            if stem_num.isdigit() and int(stem_num) <= 10:
                with open(story_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                words_found = []
                for s in data["sentences"]:
                    s["tokens"] = tokenize_sentence(s["zh"], lvl_idx)
                    for tok in s["tokens"]:
                        wid = tok.get("word_id")
                        if wid and wid in VOCAB_BY_ID and wid not in words_found:
                            words_found.append(wid)
                if not data.get("vocabulary_spotlight") or len(data["vocabulary_spotlight"]) < 5:
                    data["vocabulary_spotlight"] = words_found[:15]
                with open(story_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                retokenized_count += 1
    print(f"[+] Verified and refreshed {retokenized_count} initial stories (001-010).")

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
