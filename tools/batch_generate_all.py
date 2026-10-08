#!/usr/bin/env python3
"""
tools/batch_generate_all.py
Automated End-to-End Batch Illustration Generator for All HSK Levels.
Order:
  1. Complete remaining HSK 4
  2. Remaining HSK 2.0 (HSK 1, 2, 3, 5, 6)
  3. HSK 3.0 (Levels 1 through 9)

Features:
  - Automatically skips words that already have valid SVGs.
  - Automatically commits and pushes to git every 100 newly generated SVGs (or at end of each level).
  - Uses Google Gemini API with fallback cascade and 4.0s delay.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
HSK3_DIR = VOCAB_DIR / "hsk3_0"
OUTPUT_DIR = REPO_ROOT / "assets" / "images" / "illustrations"
WORD_ILLUSTRATIONS_JS = REPO_ROOT / "assets" / "js" / "word-illustrations.js"
WORKTREE_DIR = Path("/Users/haunguyen/.gemini/antigravity/worktrees/HSK-Flashcards-Generator/add_hsk4_reading_analysis")

MODELS_TO_TRY = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-2.5-flash"
]

def guess_pos(meaning):
    m = (meaning or "").lower()
    if re.search(r'^(đẹp|tốt|xấu|to|nhỏ|lớn|cao|thấp|nhanh|chậm|dài|ngắn|nóng|lạnh|mới|cũ|đắt|rẻ|khó|dễ|buồn|vui|sạch|bẩn|ngon|ngọt|đắng|cay|mặn|chua|mệt|đói|no|bận|rảnh|đúng|sai|tiện|phức tạp|đơn giản|quan trọng|an toàn|nguy hiểm|nghiêm túc|cẩn thận|nhiệt tình|tự tin|hạnh phúc|khỏe|yếu|trắng|đen|đỏ|vàng|xanh)\b', m) or 'tính từ' in m:
        return 'adj'
    if re.search(r'^(làm|đi|nói|ăn|uống|xem|mua|bán|học|chạy|bay|đến|rời|giúp|tổ chức|chuẩn bị|phát hiện|tham gia|quyết định|giải quyết|sử dụng|cung cấp|tìm|gặp|nhớ|hiểu|yêu|ghét|thích|lo|nghĩ|biết|mặc|đeo|viết|đọc|nghe|sắp xếp|bố trí|ôm|xin lỗi|đăng ký|tốt nghiệp|biểu thị|thể hiện|biểu diễn|khen ngợi|bảo vệ|đảm bảo|thực hiện|hoàn thành|phát triển|mở rộng|thay đổi|tổng kết|du lịch|trao đổi|kết hôn|kinh doanh|nghiên cứu|chiến đấu|chúc mừng|cảm ơn|kính trọng|mời|chờ|đợi|hy vọng|ước|tin|nghi ngờ|chú ý|quan tâm|giảng|dạy|vẽ|hát|múa|bơi|chơi|sửa|chữa|chọn|chọn lựa)\b', m) or 'động từ' in m:
        return 'verb'
    return 'noun'

def call_gemini_svg_api(word_info, api_key, max_retries=3):
    hanzi = word_info.get("hanzi", "")
    meaning = word_info.get("meaning", "")
    pos = word_info.get("pos") or guess_pos(meaning)
    pinyin = word_info.get("pinyin", "")

    ex_vi = (word_info.get("example_vi") or "").replace("<u>", "").replace("</u>", "").strip()
    ex_zh = (word_info.get("example_zh") or word_info.get("example") or "").replace("<u>", "").replace("</u>", "").strip()
    context_note = ""
    if ex_vi:
        context_note = f"\nContextual Example: '{ex_vi}'"
    elif ex_zh:
        context_note = f"\nContextual Example: '{ex_zh}'"

    if pos == "verb":
        action_guidance = (
            f"Depict a RICH, DETAILED SCENE-BASED REAL-WORLD HUMAN ACTION representing the exact action of '{meaning}'. "
            "Show a stylized, expressive character actively performing the action with authentic body language and posture. "
            "Crucially, include ENVIRONMENT DETAILS and PROPS (e.g., room setting, stage, desk, tools, background lighting, foreground elements) "
            "that immediately establish the real-world context of this action. DO NOT draw abstract symbols, geometric badges, or floating icons."
        )
    elif pos == "noun":
        action_guidance = (
            f"Depict a VIVID, SCENE-BASED REAL-WORLD ENVIRONMENT or PHYSICAL OBJECT representing '{meaning}'. "
            "Place the subject in an authentic, tangible context with surrounding props, realistic surfaces, atmospheric depth, and spatial details. "
            "DO NOT draw generic isolated icons, abstract shapes, or simplistic geometric glyphs."
        )
    elif pos == "adj":
        action_guidance = (
            f"Depict a RICH REAL-WORLD SCENARIO with an EXPRESSIVE CHARACTER vividly embodying the state or emotion of '{meaning}'. "
            "Show dynamic facial expression, communicative body posture, and immersive atmospheric environment (e.g. dramatic lighting, weather, or room ambiance) "
            "that makes the feeling immediately intuitive. DO NOT draw abstract shapes or emojis."
        )
    else:
        action_guidance = (
            f"Depict an engaging, scene-based real-world scenario illustrating the communicative context of '{meaning}'. "
            "Include relatable characters, props, and environment."
        )

    prompt = (
        "You are an expert 2D vector illustrator and art director creating scene-based, action-packed illustrations for an HSK language learning app.\n"
        f"Target Vocabulary: {hanzi} ({pinyin}) - Meaning: '{meaning}' - Part of Speech: {pos}.{context_note}\n\n"
        "CRITICAL ART DIRECTION RULES:\n"
        f"1. SCENE & SUBJECT: {action_guidance}\n"
        "2. STYLE: Clean, friendly 2D flat cartoon or minimalist vector art with expressive contours and rich narrative depth.\n"
        "3. COMPOSITION & CANVAS:\n"
        "   - Valid SVG with viewBox=\"0 0 240 240\" xmlns=\"http://www.w3.org/2000/svg\".\n"
        "   - Full-bleed container: <rect width=\"240\" height=\"240\" rx=\"24\" fill=\"#1e293b\"/> (or gradient from #0f172a to #1e293b).\n"
        "   - The illustration must fill the canvas space, featuring the main subject prominently with context props.\n"
        "4. COLOR PALETTE:\n"
        "   - Dark-mode harmonious: Deep slate navy (#0f172a, #1e293b) background, muted blues, warm golden/amber glows (#f59e0b, #fbbf24), and energetic modern accents (#38bdf8, #10b981, #ec4899, #fb923c).\n"
        "5. STRICT NEGATIVE CONSTRAINTS:\n"
        f"   - ABSOLUTELY NO abstract symbols, logos, minimalist icons, or generic badges.\n"
        f"   - ABSOLUTELY NO text, NO letters, NO words, NO subtitles, NO Chinese characters (NO {hanzi}), NO English words, NO pinyin.\n"
        "   - ABSOLUTELY NO Gemini logo, NO brand logos, NO watermarks.\n"
        "6. Return ONLY the raw <svg>...</svg> code, without markdown backticks, without any explanation."
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4}
    }

    for attempt in range(max_retries):
        for model in MODELS_TO_TRY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=35) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and "text" in parts[0]:
                            text = parts[0]["text"]
                            m = re.search(r"<svg[\s\S]*?<\/svg>", text, re.IGNORECASE)
                            if m:
                                svg_str = m.group(0).strip()
                                if len(svg_str) > 100:
                                    return svg_str
            except urllib.error.HTTPError as he:
                if he.code == 429:
                    continue
                elif he.code in (404, 503):
                    continue
                else:
                    err_text = he.read().decode("utf-8", errors="ignore")
                    print(f"    [!] {model} HTTP {he.code}: {err_text[:100]}", flush=True)
            except Exception:
                continue

        if attempt < max_retries - 1:
            wait_sec = 15 * (attempt + 1)
            print(f"    [!] Models busy. Waiting {wait_sec}s before retry...", flush=True)
            time.sleep(wait_sec)

    return None

def update_illustrations_manifest(records):
    if not WORD_ILLUSTRATIONS_JS.exists() or not records:
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

    if WORKTREE_DIR.exists():
        try:
            dest = WORKTREE_DIR / "assets" / "js" / "word-illustrations.js"
            dest.write_text(content, encoding="utf-8")
        except Exception:
            pass

def git_commit_and_push(batch_count, level_label):
    try:
        print(f"\n[>>> GIT] Committing and pushing batch of {batch_count} newly generated SVGs for {level_label}...", flush=True)
        subprocess.run(["git", "add", "assets/images/illustrations", "assets/js/word-illustrations.js"], cwd=REPO_ROOT, check=True)
        commit_msg = f"feat(illustrations): batch generate scene-based SVGs ({level_label}: +{batch_count} words)"
        res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_ROOT, capture_output=True, text=True)
        print(f"[>>> GIT] {res.stdout.strip()}", flush=True)
        push_res = subprocess.run(["git", "push", "origin", "main"], cwd=REPO_ROOT, capture_output=True, text=True)
        print(f"[>>> GIT] Push result: {push_res.stdout.strip() or 'OK'}", flush=True)
    except Exception as e:
        print(f"[!] Warning git push failed: {e}", flush=True)

def load_level_data(file_path):
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[!] Error loading {file_path}: {e}", flush=True)
        return []

def main():
    parser = argparse.ArgumentParser(description="Master batch generator for all HSK 2.0 & HSK 3.0 levels")
    parser.add_argument("--api-key", default=os.environ.get("GOOGLE_AI_KEY"), required=True, help="Google AI Studio API Key")
    parser.add_argument("--delay", type=float, default=4.0, help="Delay between API calls in seconds (default: 4.0s)")
    parser.add_argument("--batch-size", type=int, default=100, help="Commit and push every N generated items (default: 100)")
    args = parser.parse_args()

    api_key = args.api_key.strip()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if WORKTREE_DIR.exists():
        (WORKTREE_DIR / "assets" / "images" / "illustrations").mkdir(parents=True, exist_ok=True)

    # Define curriculum order
    curriculum = [
        # Phase 1: Complete HSK 4 first
        ("HSK 4", VOCAB_DIR / "hsk4_vocabularies.json"),
        # Phase 2: Remaining HSK 2.0
        ("HSK 1", VOCAB_DIR / "hsk1_vocabularies.json"),
        ("HSK 2", VOCAB_DIR / "hsk2_vocabularies.json"),
        ("HSK 3", VOCAB_DIR / "hsk3_vocabularies.json"),
        ("HSK 5", VOCAB_DIR / "hsk5_vocabularies.json"),
        ("HSK 6", VOCAB_DIR / "hsk6_vocabularies.json"),
        # Phase 3: HSK 3.0 (9 levels)
        ("HSK 3.0 Level 1", HSK3_DIR / "level1_vocabularies.json"),
        ("HSK 3.0 Level 2", HSK3_DIR / "level2_vocabularies.json"),
        ("HSK 3.0 Level 3", HSK3_DIR / "level3_vocabularies.json"),
        ("HSK 3.0 Level 4", HSK3_DIR / "level4_vocabularies.json"),
        ("HSK 3.0 Level 5", HSK3_DIR / "level5_vocabularies.json"),
        ("HSK 3.0 Level 6", HSK3_DIR / "level6_vocabularies.json"),
        ("HSK 3.0 Level 7", HSK3_DIR / "level7_vocabularies.json"),
        ("HSK 3.0 Level 8", HSK3_DIR / "level8_vocabularies.json"),
        ("HSK 3.0 Level 9", HSK3_DIR / "level9_vocabularies.json"),
    ]

    total_generated_session = 0
    batch_new_count = 0
    pending_manifest = {}

    print("==================================================================", flush=True)
    print("  HSK Flashcards: Master Scene-Based Illustration Pipeline", flush=True)
    print(f"  Target: HSK 4 -> HSK 1..6 (HSK 2.0) -> Levels 1..9 (HSK 3.0)", flush=True)
    print(f"  Batch commit threshold: Every {args.batch_size} newly generated SVGs", flush=True)
    print("==================================================================\n", flush=True)

    for level_label, file_path in curriculum:
        words = load_level_data(file_path)
        if not words:
            continue

        print(f"\n[*] Starting {level_label} ({len(words)} words) from {file_path.name}...", flush=True)
        level_new = 0
        level_skipped = 0

        for idx, item in enumerate(words, 1):
            hanzi = item.get("hanzi", "").strip()
            if not hanzi:
                continue

            meaning = item.get("meaning", "").strip()
            pinyin = item.get("pinyin", "").strip()
            pos = item.get("pos") or guess_pos(meaning)
            item["pos"] = pos

            out_filename = f"{hanzi}.svg"
            out_path = OUTPUT_DIR / out_filename

            # Check if SVG already exists and has substantive content (> 200 bytes)
            if out_path.exists() and out_path.stat().st_size > 200:
                level_skipped += 1
                pending_manifest[hanzi] = {
                    "file": out_filename,
                    "src": f"assets/images/illustrations/{out_filename}",
                    "caption": meaning
                }
                if idx % 50 == 0:
                    print(f"    [{idx}/{len(words)}] Progress: {level_skipped} existing skipped, {level_new} newly generated.", flush=True)
                continue

            print(f"    [{idx}/{len(words)}] Generating '{hanzi}' ({pinyin} - {meaning})...", flush=True)
            svg_code = call_gemini_svg_api(item, api_key)
            if svg_code:
                out_path.write_text(svg_code, encoding="utf-8")
                if WORKTREE_DIR.exists():
                    try:
                        (WORKTREE_DIR / "assets" / "images" / "illustrations" / out_filename).write_text(svg_code, encoding="utf-8")
                    except Exception:
                        pass

                pending_manifest[hanzi] = {
                    "file": out_filename,
                    "src": f"assets/images/illustrations/{out_filename}",
                    "caption": meaning
                }
                level_new += 1
                batch_new_count += 1
                total_generated_session += 1
                print(f"        ✓ Saved scene SVG ({len(svg_code)} B) [Total this session: {total_generated_session}]", flush=True)
            else:
                print(f"        ✗ Failed to generate '{hanzi}'", flush=True)

            # Flush manifest periodically every 5 words
            if len(pending_manifest) >= 5:
                update_illustrations_manifest(pending_manifest)
                pending_manifest.clear()

            # Batch commit & push check (every 100 new SVGs)
            if batch_new_count >= args.batch_size:
                if pending_manifest:
                    update_illustrations_manifest(pending_manifest)
                    pending_manifest.clear()
                git_commit_and_push(batch_new_count, level_label)
                batch_new_count = 0

            time.sleep(args.delay)

        # End of level: flush manifest and commit if any new images were created
        if pending_manifest:
            update_illustrations_manifest(pending_manifest)
            pending_manifest.clear()

        if batch_new_count > 0:
            git_commit_and_push(batch_new_count, level_label)
            batch_new_count = 0

        print(f"[*] Completed {level_label}: {level_new} newly generated, {level_skipped} skipped.", flush=True)

    print("\n==================================================================", flush=True)
    print(f"[*] ALL CURRICULUM LEVELS COMPLETED! Total newly generated: {total_generated_session}", flush=True)
    print("==================================================================", flush=True)

if __name__ == "__main__":
    main()
