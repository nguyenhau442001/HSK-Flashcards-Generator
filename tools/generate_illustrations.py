#!/usr/bin/env python3
"""
tools/generate_illustrations.py
Batch AI Illustration Generator for HSK Vocabulary using Google AI Studio.
Generates theme-appropriate, text-free visual mnemonics and saves them directly into assets/images/illustrations/.
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
OUTPUT_DIR = REPO_ROOT / "assets" / "images" / "illustrations"
WORD_ILLUSTRATIONS_JS = REPO_ROOT / "assets" / "js" / "word-illustrations.js"

# POS labels for prompt context
POS_NAMES = {
    'noun': 'noun / physical object or conceptual entity',
    'verb': 'verb / dynamic action, movement or execution',
    'adj': 'adjective / qualitative attribute, emotional or sensory state',
    'adv': 'adverb / degree, manner, or frequency meter',
    'measure': 'measure word / modular counting unit',
    'pron': 'pronoun / connection or reference',
    'prep': 'preposition / spatial or directional relation',
    'conj': 'conjunction / bridge connecting elements'
}

def load_vocabulary():
    """Loads all HSK vocabularies indexed by hanzi."""
    words_by_hanzi = {}
    if not VOCAB_DIR.exists():
        return words_by_hanzi

    for f in sorted(VOCAB_DIR.glob("hsk*_vocabularies.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                if isinstance(data, list):
                    for item in data:
                        h = item.get("hanzi", "").strip()
                        if h and h not in words_by_hanzi:
                            words_by_hanzi[h] = item
        except Exception as e:
            print(f"[!] Warning reading {f.name}: {e}")

    return words_by_hanzi

def guess_pos(meaning):
    """Heuristic POS classifier matching word-illustrations.js rules."""
    m = (meaning or "").lower()
    if re.search(r'^(đẹp|tốt|xấu|to|nhỏ|lớn|cao|thấp|nhanh|chậm|dài|ngắn|nóng|lạnh|mới|cũ|đắt|rẻ|khó|dễ|buồn|vui|sạch|bẩn|ngon|ngọt|đắng|cay|mặn|chua|mệt|đói|no|bận|rảnh|đúng|sai|tiện|phức tạp|đơn giản|quan trọng|an toàn|nguy hiểm|nghiêm túc|cẩn thận|nhiệt tình|tự tin|hạnh phúc|khỏe|yếu|trắng|đen|đỏ|vàng|xanh)\b', m) or 'tính từ' in m:
        return 'adj'
    if re.search(r'^(làm|đi|nói|ăn|uống|xem|mua|bán|học|chạy|bay|đến|rời|giúp|tổ chức|chuẩn bị|phát hiện|tham gia|quyết định|giải quyết|sử dụng|cung cấp|tìm|gặp|nhớ|hiểu|yêu|ghét|thích|lo|nghĩ|biết|mặc|đeo|viết|đọc|nghe|sắp xếp|bố trí|ôm|xin lỗi|đăng ký|tốt nghiệp|biểu thị|thể hiện|biểu diễn|khen ngợi|bảo vệ|đảm bảo|thực hiện|hoàn thành|phát triển|mở rộng|thay đổi|tổng kết|du lịch|trao đổi|kết hôn|kinh doanh|nghiên cứu|chiến đấu|chúc mừng|cảm ơn|kính trọng|mời|chờ|đợi|hy vọng|ước|tin|nghi ngờ|chú ý|quan tâm|giảng|dạy|vẽ|hát|múa|bơi|chơi|sửa|chữa|chọn|chọn lựa)\b', m) or 'động từ' in m:
        return 'verb'
    return 'noun'

def build_prompt(hanzi, meaning, pinyin="", pos="noun"):
    """Constructs prompt strictly banning text/hanzi while enforcing thematic vector art."""
    base_style = (
        "A minimalist, modern 2D flat vector icon illustration, "
        "dark mode aesthetic with deep dark slate background (#0f172a), "
        "crisp geometric contours, vibrant harmonious accent colors, clean negative space, "
        "designed as a language flashcard visual mnemonic memory anchor"
    )

    pos_desc = POS_NAMES.get(pos, "conceptual symbol")

    subject_metaphor = f"Visual metaphor illustrating the core concept and topic of '{meaning}' ({pos_desc})"

    negative_exclusions = (
        "STRICTLY NO text, NO letters, NO words, NO subtitles, NO typography, "
        "NO Chinese characters, NO Hanzi, NO English text, NO pinyin, NO labels, "
        "NO watermarks, NO photographic realism, clean vector shapes only"
    )

    return f"{base_style}. Subject: {subject_metaphor}. {negative_exclusions}."

def call_imagen_api(prompt, api_key):
    """Calls Google Imagen 3 API to generate a high quality 1:1 image."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={api_key}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "1:1",
            "outputOptions": {"mimeType": "image/png"}
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        predictions = data.get("predictions", [])
        if predictions and "bytesBase64Encoded" in predictions[0]:
            return base64.b64decode(predictions[0]["bytesBase64Encoded"])
    return None

def call_gemini_svg_api(word_info, api_key):
    """Calls Gemini Flash API to generate clean inline SVG vector."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    hanzi = word_info.get("hanzi", "")
    meaning = word_info.get("meaning", "")
    pos = word_info.get("pos", "noun")

    prompt = (
        f"Create a minimalist, modern 2D flat vector SVG illustration representing the language concept and topic '{meaning}' "
        f"(Part of speech: {pos}).\n"
        "Requirements:\n"
        "1. Valid standalone SVG: <svg viewBox=\"0 0 200 200\" xmlns=\"http://www.w3.org/2000/svg\">\n"
        "2. Dark mode color theme: deep dark slate/navy background (#0f172a / #1e293b), vibrant modern accent colors (emerald, amber, cyan, indigo).\n"
        "3. STRICTLY NO text, NO letters, NO words, NO Chinese characters inside the graphic.\n"
        "4. Return ONLY raw <svg>...</svg> code without markdown backticks or explanations."
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                text = parts[0]["text"]
                m = re.search(r"<svg[\s\S]*?<\/svg>", text, re.IGNORECASE)
                if m:
                    return m.group(0)
    return None

def update_illustrations_manifest(records):
    """Updates STATIC_ILLUSTRATIONS_INDEX in word-illustrations.js."""
    if not WORD_ILLUSTRATIONS_JS.exists():
        return

    content = WORD_ILLUSTRATIONS_JS.read_text(encoding="utf-8")

    # Check if STATIC_ILLUSTRATIONS_INDEX exists in file
    marker = "const STATIC_ILLUSTRATIONS_INDEX = "
    if marker in content:
        # Extract existing JSON or dict
        match = re.search(r"const STATIC_ILLUSTRATIONS_INDEX = (\{[\s\S]*?\});", content)
        if match:
            try:
                existing = json.loads(match.group(1))
            except Exception:
                existing = {}
            existing.update(records)
            new_block = f"const STATIC_ILLUSTRATIONS_INDEX = {json.dumps(existing, ensure_ascii=False, indent=2)};"
            content = content[:match.start()] + new_block + content[match.end():]
    else:
        # Insert before getWordIllustration
        new_block = f"\n// Pre-generated static illustration assets stored in assets/images/illustrations/\nconst STATIC_ILLUSTRATIONS_INDEX = {json.dumps(records, ensure_ascii=False, indent=2)};\n\n"
        target = "function getWordIllustration"
        if target in content:
            content = content.replace(target, new_block + target, 1)

    WORD_ILLUSTRATIONS_JS.write_text(content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Generate thematic visual mnemonic illustrations using Google AI Studio")
    parser.add_argument("--api-key", default=os.environ.get("GOOGLE_AI_KEY"), help="Google AI Studio API Key (or env GOOGLE_AI_KEY)")
    parser.add_argument("--words", help="Specific Hanzi words (comma or space separated), e.g. '总结,合适,困难'")
    parser.add_argument("--hsk", type=int, choices=[1, 2, 3, 4, 5, 6], help="Target HSK level (1-6)")
    parser.add_argument("--limit", type=int, default=10, help="Max words to generate (default: 10)")
    parser.add_argument("--model", choices=["imagen", "gemini"], default="imagen", help="AI model: 'imagen' (PNG via Imagen 3) or 'gemini' (SVG via Gemini Flash)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing illustration files")

    args = parser.parse_args()

    api_key = (args.api_key or "").strip()
    if not api_key:
        print("[!] Error: Google AI Studio API Key is required.")
        print("    Pass via --api-key AIzaSy... or export GOOGLE_AI_KEY='AIzaSy...'")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_vocab = load_vocabulary()

    targets = []
    if args.words:
        input_words = [w.strip() for w in re.split(r"[,;\s]+", args.words) if w.strip()]
        for w in input_words:
            if w in all_vocab:
                item = dict(all_vocab[w])
                targets.append(item)
            else:
                targets.append({"hanzi": w, "meaning": w, "pinyin": ""})
    elif args.hsk:
        hsk_file = VOCAB_DIR / f"hsk{args.hsk}_vocabularies.json"
        if hsk_file.exists():
            with open(hsk_file, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                targets = data[:args.limit]
    else:
        print("[!] Please specify --words or --hsk")
        sys.exit(1)

    if not targets:
        print("[!] No target words found.")
        sys.exit(0)

    print(f"[*] Processing {len(targets)} word(s) using model: {args.model.upper()}...")
    new_manifest_records = {}

    for idx, item in enumerate(targets, 1):
        hanzi = item.get("hanzi", "").strip()
        meaning = item.get("meaning", "").strip()
        pinyin = item.get("pinyin", "").strip()
        pos = item.get("pos") or guess_pos(meaning)
        item["pos"] = pos

        ext = "png" if args.model == "imagen" else "svg"
        out_filename = f"{hanzi}.{ext}"
        out_path = OUTPUT_DIR / out_filename

        if out_path.exists() and not args.overwrite:
            print(f"[{idx}/{len(targets)}] {hanzi} ({meaning}) -> Already exists: {out_filename} (skip)")
            new_manifest_records[hanzi] = {
                "file": out_filename,
                "src": f"assets/images/illustrations/{out_filename}",
                "caption": meaning
            }
            continue

        print(f"[{idx}/{len(targets)}] Generating illustration for '{hanzi}' ({pinyin} - {meaning})...")

        try:
            if args.model == "imagen":
                prompt = build_prompt(hanzi, meaning, pinyin, pos)
                image_bytes = call_imagen_api(prompt, api_key)
                if image_bytes:
                    out_path.write_bytes(image_bytes)
                    print(f"    ✓ Saved PNG to {out_path.relative_to(REPO_ROOT)}")
                    new_manifest_records[hanzi] = {
                        "file": out_filename,
                        "src": f"assets/images/illustrations/{out_filename}",
                        "caption": meaning
                    }
                else:
                    print(f"    ✗ Failed to generate Imagen image for '{hanzi}'")
            else:
                svg_code = call_gemini_svg_api(item, api_key)
                if svg_code:
                    out_path.write_text(svg_code, encoding="utf-8")
                    print(f"    ✓ Saved SVG to {out_path.relative_to(REPO_ROOT)}")
                    new_manifest_records[hanzi] = {
                        "file": out_filename,
                        "src": f"assets/images/illustrations/{out_filename}",
                        "caption": meaning
                    }
                else:
                    print(f"    ✗ Failed to generate SVG for '{hanzi}'")
        except urllib.error.HTTPError as he:
            err_msg = he.read().decode("utf-8", errors="ignore")
            print(f"    ✗ HTTP {he.code} Error: {err_msg[:200]}")
        except Exception as e:
            print(f"    ✗ Error: {e}")

    if new_manifest_records:
        update_illustrations_manifest(new_manifest_records)
        print(f"[*] Updated illustrations manifest in {WORD_ILLUSTRATIONS_JS.name}")

    print("[*] Done!")

if __name__ == "__main__":
    main()
