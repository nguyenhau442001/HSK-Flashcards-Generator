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
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
OUTPUT_DIR = REPO_ROOT / "assets" / "images" / "illustrations"
WORD_ILLUSTRATIONS_JS = REPO_ROOT / "assets" / "js" / "word-illustrations.js"

# Optional worktree directory to keep in sync
WORKTREE_DIR = Path("/Users/haunguyen/.gemini/antigravity/worktrees/HSK-Flashcards-Generator/add_hsk4_reading_analysis")

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
            print(f"[!] Warning reading {f.name}: {e}", flush=True)

    return words_by_hanzi

def guess_pos(meaning):
    """Heuristic POS classifier matching word-illustrations.js rules."""
    m = (meaning or "").lower()
    if re.search(r'^(đẹp|tốt|xấu|to|nhỏ|lớn|cao|thấp|nhanh|chậm|dài|ngắn|nóng|lạnh|mới|cũ|đắt|rẻ|khó|dễ|buồn|vui|sạch|bẩn|ngon|ngọt|đắng|cay|mặn|chua|mệt|đói|no|bận|rảnh|đúng|sai|tiện|phức tạp|đơn giản|quan trọng|an toàn|nguy hiểm|nghiêm túc|cẩn thận|nhiệt tình|tự tin|hạnh phúc|khỏe|yếu|trắng|đen|đỏ|vàng|xanh)\b', m) or 'tính từ' in m:
        return 'adj'
    if re.search(r'^(làm|đi|nói|ăn|uống|xem|mua|bán|học|chạy|bay|đến|rời|giúp|tổ chức|chuẩn bị|phát hiện|tham gia|quyết định|giải quyết|sử dụng|cung cấp|tìm|gặp|nhớ|hiểu|yêu|ghét|thích|lo|nghĩ|biết|mặc|đeo|viết|đọc|nghe|sắp xếp|bố trí|ôm|xin lỗi|đăng ký|tốt nghiệp|biểu thị|thể hiện|biểu diễn|khen ngợi|bảo vệ|đảm bảo|thực hiện|hoàn thành|phát triển|mở rộng|thay đổi|tổng kết|du lịch|trao đổi|kết hôn|kinh doanh|nghiên cứu|chiến đấu|chúc mừng|cảm ơn|kính trọng|mời|chờ|đợi|hy vọng|ước|tin|nghi ngờ|chú ý|quan tâm|giảng|dạy|vẽ|hát|múa|bơi|chơi|sửa|chữa|chọn|chọn lựa)\b', m) or 'động từ' in m:
        return 'verb'
    return 'noun'

def call_gemini_svg_api(word_info, api_key, max_retries=5):
    """Calls Gemini Flash API to generate clean inline SVG vector with retry on 429."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    hanzi = word_info.get("hanzi", "")
    meaning = word_info.get("meaning", "")
    pos = word_info.get("pos", "noun")
    pinyin = word_info.get("pinyin", "")

    prompt = (
        f"You are a senior graphic designer creating a sleek 2D vector graphic icon for a language flashcard app.\n"
        f"Word: {hanzi} ({pinyin}) - Meaning: '{meaning}' - Part of speech: {pos}.\n\n"
        "Requirements:\n"
        "1. Valid standalone SVG: <svg viewBox=\"0 0 200 200\" xmlns=\"http://www.w3.org/2000/svg\">\n"
        "2. Visual Metaphor: Design a clear, memorable symbolic vector concept representing the core meaning of the word.\n"
        "3. Aesthetic: Modern dark-mode flat vector design. Background: dark slate #0f172a or #1e293b rounded rectangle (<rect x=\"10\" y=\"10\" width=\"180\" height=\"180\" rx=\"24\" fill=\"#1e293b\"/>). Accents: vibrant amber (#f59e0b), emerald (#10b981), sky blue (#38bdf8), or coral (#fb923c).\n"
        "4. STRICT CONSTRAINTS:\n"
        "   - ABSOLUTELY NO text, NO letters, NO words, NO Chinese characters, NO English text, NO pinyin.\n"
        "   - ABSOLUTELY NO Gemini logo, NO brand logos, NO watermarks, NO subtle letter markings.\n"
        "   - Clean geometric paths, circles, rounded rects only.\n"
        "5. Return ONLY the raw <svg>...</svg> code, without markdown backticks, without any explanation."
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    for attempt in range(max_retries):
        try:
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
                            svg_str = m.group(0).strip()
                            if len(svg_str) > 60:
                                return svg_str
            return None
        except urllib.error.HTTPError as he:
            if he.code == 429:
                wait_sec = 15 * (attempt + 1)
                print(f"    [!] Rate limited (HTTP 429). Backing off for {wait_sec}s... (attempt {attempt + 1}/{max_retries})", flush=True)
                time.sleep(wait_sec)
            else:
                err_text = he.read().decode("utf-8", errors="ignore")
                print(f"    [!] HTTP {he.code} error: {err_text[:160]}", flush=True)
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    return None
        except Exception as e:
            print(f"    [!] Request error: {e}", flush=True)
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return None
    return None

def update_illustrations_manifest(records):
    """Updates STATIC_ILLUSTRATIONS_INDEX in word-illustrations.js."""
    if not WORD_ILLUSTRATIONS_JS.exists():
        return

    content = WORD_ILLUSTRATIONS_JS.read_text(encoding="utf-8")

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
        new_block = f"\n// Pre-generated static illustration assets stored in assets/images/illustrations/\nconst STATIC_ILLUSTRATIONS_INDEX = {json.dumps(records, ensure_ascii=False, indent=2)};\n\n"
        target = "function getWordIllustration"
        if target in content:
            content = content.replace(target, new_block + target, 1)

    WORD_ILLUSTRATIONS_JS.write_text(content, encoding="utf-8")

    # Sync to worktree if available
    if WORKTREE_DIR.exists():
        try:
            dest = WORKTREE_DIR / "assets" / "js" / "word-illustrations.js"
            dest.write_text(content, encoding="utf-8")
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(description="Generate thematic visual mnemonic illustrations using Google AI Studio")
    parser.add_argument("--api-key", default=os.environ.get("GOOGLE_AI_KEY"), help="Google AI Studio API Key (or env GOOGLE_AI_KEY)")
    parser.add_argument("--words", help="Specific Hanzi words (comma or space separated), e.g. '总结,合适,困难'")
    parser.add_argument("--hsk", type=int, choices=[1, 2, 3, 4, 5, 6], help="Target HSK level (1-6)")
    parser.add_argument("--limit", type=int, default=None, help="Max words to generate (default: all words in target)")
    parser.add_argument("--delay", type=float, default=3.5, help="Delay in seconds between requests (default: 3.5s to respect 15 RPM limit)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing illustration files")

    args = parser.parse_args()

    api_key = (args.api_key or "").strip()
    if not api_key:
        print("[!] Error: Google AI Studio API Key is required.", flush=True)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if WORKTREE_DIR.exists():
        (WORKTREE_DIR / "assets" / "images" / "illustrations").mkdir(parents=True, exist_ok=True)

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
                if args.limit:
                    targets = data[:args.limit]
                else:
                    targets = data
    else:
        print("[!] Please specify --words or --hsk", flush=True)
        sys.exit(1)

    total = len(targets)
    print(f"[*] Starting batch generation for {total} word(s) [Delay: {args.delay}s]...", flush=True)

    success_count = 0
    skip_count = 0
    fail_count = 0
    pending_records = {}

    for idx, item in enumerate(targets, 1):
        hanzi = item.get("hanzi", "").strip()
        meaning = item.get("meaning", "").strip()
        pinyin = item.get("pinyin", "").strip()
        pos = item.get("pos") or guess_pos(meaning)
        item["pos"] = pos

        out_filename = f"{hanzi}.svg"
        out_path = OUTPUT_DIR / out_filename

        pct = (idx / total) * 100

        # Check if already exists
        if out_path.exists() and out_path.stat().st_size > 60 and not args.overwrite:
            skip_count += 1
            pending_records[hanzi] = {
                "file": out_filename,
                "src": f"assets/images/illustrations/{out_filename}",
                "caption": meaning
            }
            if idx % 20 == 0:
                print(f"[{idx}/{total}] ({pct:.1f}%) Progress check: {skip_count} skipped (already exist), {success_count} newly generated.", flush=True)
            continue

        print(f"[{idx}/{total}] ({pct:.1f}%) Generating '{hanzi}' ({pinyin} - {meaning})...", flush=True)

        svg_code = call_gemini_svg_api(item, api_key)
        if svg_code:
            out_path.write_text(svg_code, encoding="utf-8")
            if WORKTREE_DIR.exists():
                try:
                    wt_path = WORKTREE_DIR / "assets" / "images" / "illustrations" / out_filename
                    wt_path.write_text(svg_code, encoding="utf-8")
                except Exception:
                    pass

            pending_records[hanzi] = {
                "file": out_filename,
                "src": f"assets/images/illustrations/{out_filename}",
                "caption": meaning
            }
            success_count += 1
            print(f"    ✓ Saved SVG ({len(svg_code)} B)", flush=True)
        else:
            fail_count += 1
            print(f"    ✗ Failed to generate SVG for '{hanzi}'", flush=True)

        # Incrementally update manifest every 5 words
        if len(pending_records) >= 5 or idx == total:
            update_illustrations_manifest(pending_records)
            pending_records.clear()

        # Respect API rate limits
        if idx < total:
            time.sleep(args.delay)

    # Final manifest flush
    if pending_records:
        update_illustrations_manifest(pending_records)

    print(f"\n[*] BATCH COMPLETED: {total} total, {success_count} generated, {skip_count} skipped, {fail_count} failed.", flush=True)

if __name__ == "__main__":
    main()
