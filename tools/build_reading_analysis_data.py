#!/usr/bin/env python3
"""
build_reading_analysis_data.py

Extracts, structures, and compiles authentic HSK 4 Reading & Analysis dataset
from standard Hanban/CTI mock tests ("Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf").

Generates:
  database/reading/hsk4_reading_analysis.json
"""

import json
import os
import re
from pypinyin import pinyin, Style, lazy_pinyin

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE_DIR, "database", "reading")
OUT_FILE = os.path.join(OUT_DIR, "hsk4_reading_analysis.json")
HANVIET_FILE = os.path.join(BASE_DIR, "assets", "js", "hanviet-dict.js")

# Load HSK 1-4 Vocabularies
HSK_VOCAB = {}
for lvl in ["hsk1", "hsk2", "hsk3", "hsk4"]:
    vpath = os.path.join(BASE_DIR, "database", "vocabs", f"{lvl}_vocabularies.json")
    if os.path.exists(vpath):
        with open(vpath, "r", encoding="utf-8") as f:
            for item in json.load(f):
                w = item.get("hanzi", "").strip()
                if w:
                    HSK_VOCAB[w] = {
                        "level": lvl,
                        "meaning": item.get("meaning", ""),
                        "pinyin": item.get("pinyin", ""),
                        "hanviet": item.get("hanviet", "")
                    }

# Load Han-Viet dictionary
HANVIET_COMPOUNDS = {}
HANVIET_CHARS = {}
if os.path.exists(HANVIET_FILE):
    with open(HANVIET_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    c_match = re.search(r"const HANVIET_COMPOUNDS = (\{.*?\});", content, re.DOTALL)
    ch_match = re.search(r"const HANVIET_CHARS = (\{.*?\});", content, re.DOTALL)
    if c_match:
        HANVIET_COMPOUNDS = json.loads(c_match.group(1))
    if ch_match:
        HANVIET_CHARS = json.loads(ch_match.group(1))

def get_hanviet(text):
    if not text:
        return ""
    if text in HANVIET_COMPOUNDS:
        return HANVIET_COMPOUNDS[text]
    parts = []
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            parts.append(HANVIET_CHARS.get(ch, ch))
        else:
            parts.append(ch)
    return " ".join(parts).replace("  ", " ").strip()

def get_pinyin_str(text):
    if not text:
        return ""
    # Use tone marks
    py_list = pinyin(text, style=Style.TONE)
    res = []
    for p in py_list:
        res.append(p[0])
    return " ".join(res).strip()

# Authentic entries curated directly from Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
RAW_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building / Word Order)
    # =========================================================================
    {
        "id": "hsk4_b1_86",
        "category": "sentence_building",
        "title": "运动对健康有好处",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第86题)",
        "zh": "运动对健康有好处。",
        "vietnamese": "Vận động có lợi cho sức khỏe.",
        "grammar_point": {
            "name": "Cấu trúc giới từ: 对……有好处 (Có lợi đối với...)",
            "pattern": "Chủ ngữ + 对 + Đối tượng + 有好处 / 有帮助",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Thí sinh Việt Nam thường có xu hướng dịch xuôi 'Vận động có lợi cho sức khỏe' thành '运动有好处对健康' (SAI). Trong ngữ pháp tiếng Trung chuẩn, cụm giới từ '对 + Đối tượng' bắt buộc phải đứng TRƯỚC vị ngữ '有好处'.",
            "explanation": "Cấu trúc '对……有好处/有坏处' biểu thị mức độ tác động tích cực hoặc tiêu cực đến một đối tượng cụ thể. '对健康' đóng vai trò trạng ngữ bổ nghĩa cho '有好处'."
        },
        "tokens": [
            { "text": "运动", "type": "core", "role": "S", "meaning": "vận động, thể thao" },
            { "text": "对", "type": "grammar", "role": "Prep", "meaning": "đối với (giới từ chỉ đối tượng)" },
            { "text": "健康", "type": "core", "role": "O_prep", "meaning": "sức khỏe" },
            { "text": "有", "type": "normal", "role": "V", "meaning": "có" },
            { "text": "好处", "type": "core", "role": "O", "meaning": "điểm tốt, lợi ích" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "运动", "type": "subject", "desc": "Đối tượng thực hiện / hành vi vận động" },
            { "role": "Trạng ngữ giới từ", "text": "对健康", "type": "prep", "desc": "Giới từ '对' dẫn dắt đối tượng chịu tác động '健康'" },
            { "role": "Vị ngữ (V)", "text": "有", "type": "predicate", "desc": "Động từ biểu thị sự tồn tại" },
            { "role": "Tân ngữ (O)", "text": "好处", "type": "object", "desc": "Lợi ích, tác dụng tốt" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["对", "健康", "有", "运动", "好处"],
            "target_chunks": ["运动", "对", "健康", "有", "好处"],
            "hint": "Chủ ngữ '运动' đứng đầu, tiếp theo là cụm giới từ '对健康', kết thúc bằng '有好处'."
        }
    },
    {
        "id": "hsk4_b1_87",
        "category": "sentence_building",
        "title": "他从来没有来过北京",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第87题)",
        "zh": "他从来没有来过北京。",
        "vietnamese": "Anh ấy từ trước đến nay chưa từng đến Bắc Kinh.",
        "grammar_point": {
            "name": "Phó từ phủ định kinh nghiệm: 从来没有……过 (Chưa bao giờ...)",
            "pattern": "S + 从来 + 没有/不 + V + (过) + O",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: 1. '从来' (từ trước đến giờ) chỉ đứng trước phủ định ('没有' hoặc '不'), không dùng trong câu khẳng định đơn thuần. 2. Trợ từ động thái '过' (từng) đi kèm với '没有' để nhấn mạnh kinh nghiệm trong quá khứ.",
            "explanation": "'从来' là phó từ chỉ thời gian liên tục từ quá khứ đến hiện tại. '从来没有 + V + 过' là cấu trúc cố định cực kỳ phổ biến trong các đề thi HSK 4 để diễn tả chưa từng trải qua việc gì."
        },
        "tokens": [
            { "text": "他", "type": "normal", "role": "S", "meaning": "anh ấy" },
            { "text": "从来", "type": "core", "role": "Adv", "meaning": "từ trước tới nay (phó từ)" },
            { "text": "没有", "type": "grammar", "role": "Adv", "meaning": "chưa (phủ định)" },
            { "text": "来", "type": "normal", "role": "V", "meaning": "đến" },
            { "text": "过", "type": "grammar", "role": "Part", "meaning": "từng (trợ từ động thái)" },
            { "text": "北京", "type": "normal", "role": "O", "meaning": "Bắc Kinh" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "他", "type": "subject", "desc": "Người được nói đến" },
            { "role": "Trạng ngữ phủ định", "text": "从来没有", "type": "adv", "desc": "Phó từ '从来' kết hợp phủ định '没有'" },
            { "role": "Vị ngữ + Trợ từ", "text": "来过", "type": "predicate", "desc": "Động từ '来' + trợ từ kinh nghiệm '过'" },
            { "role": "Tân ngữ nơi chốn (O)", "text": "北京", "type": "object", "desc": "Địa danh đích đến" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["从来", "他", "来", "北京", "过", "没有"],
            "target_chunks": ["他", "从来", "没有", "来", "过", "北京"],
            "hint": "Cấu trúc: 他 + 从来没有 + 来过 + 北京."
        }
    },
    {
        "id": "hsk4_b1_88",
        "category": "sentence_building",
        "title": "办公室的门关着呢",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第88题)",
        "zh": "办公室的门关着呢。",
        "vietnamese": "Cửa văn phòng đang đóng kìa.",
        "grammar_point": {
            "name": "Câu biểu thị trạng thái duy trì: V + 着 + 呢",
            "pattern": "Chủ ngữ + Động từ + 着 + (呢)",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI: Khác với '正在...呢' (đang thực hiện hành động), 'V + 着呢' nhấn mạnh vào TRẠNG THÁI đang duy trì của sự vật (cửa đã được đóng và đang ở trạng thái khép lại). '呢' đặt ở cuối câu để tăng ngữ khí xác nhận.",
            "explanation": "Động từ '关' kết hợp với trợ từ động thái '着' miêu tả trạng thái tĩnh của cánh cửa văn phòng đang được giữ nguyên."
        },
        "tokens": [
            { "text": "办公室", "type": "core", "role": "Attr", "meaning": "văn phòng" },
            { "text": "的", "type": "normal", "role": "Part", "meaning": "của (trợ từ kết cấu)" },
            { "text": "门", "type": "normal", "role": "S", "meaning": "cửa" },
            { "text": "关", "type": "normal", "role": "V", "meaning": "đóng" },
            { "text": "着", "type": "grammar", "role": "Part", "meaning": "đang giữ trạng thái (trợ từ)" },
            { "text": "呢", "type": "grammar", "role": "Part", "meaning": "kìa, đấy (trợ từ ngữ khí)" }
        ],
        "breakdown": [
            { "role": "Cụm chủ ngữ (S)", "text": "办公室的门", "type": "subject", "desc": "Định ngữ '办公室的' bổ nghĩa cho trung tâm ngữ '门'" },
            { "role": "Vị ngữ trạng thái", "text": "关着", "type": "predicate", "desc": "Động từ '关' mang trợ từ động thái '着'" },
            { "role": "Trợ từ ngữ khí", "text": "呢", "type": "part", "desc": "Đứng cuối câu nhấn mạnh thực tế đang diễn ra" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["门", "呢", "办公室", "关", "的", "着"],
            "target_chunks": ["办公室", "的", "门", "关", "着", "呢"],
            "hint": "Cụm danh từ '办公室的门' làm chủ ngữ, sau đó là động từ '关着', cuối cùng là '呢'."
        }
    },
    {
        "id": "hsk4_b1_89",
        "category": "sentence_building",
        "title": "这场比赛吸引了很多观众",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第89题)",
        "zh": "这场比赛吸引了很多观众。",
        "vietnamese": "Trận đấu này đã thu hút rất nhiều khán giả.",
        "grammar_point": {
            "name": "Cấu trúc S + V + 了 + Số lượng + O",
            "pattern": "Chủ ngữ (Lượng từ + Danh từ) + Động từ + 了 + Định ngữ số lượng + Tân ngữ",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI: Lượng từ '场' (cháng) dùng chuyên biệt cho các trận thi đấu, vở kịch, cơn mưa ('一场比赛', '一场雨'). '吸引' (thu hút) là động từ cao tần HSK 4.",
            "explanation": "Trợ từ động thái '了' đứng ngay sau động từ '吸引' biểu thị hành động đã hoàn tất và đạt được kết quả là thu hút đông đảo người xem."
        },
        "tokens": [
            { "text": "这", "type": "normal", "role": "Attr", "meaning": "này" },
            { "text": "场", "type": "core", "role": "Clf", "meaning": "trận, hồi (lượng từ)" },
            { "text": "比赛", "type": "core", "role": "S", "meaning": "trận đấu, cuộc thi" },
            { "text": "吸引", "type": "core", "role": "V", "meaning": "thu hút, lôi cuốn" },
            { "text": "了", "type": "normal", "role": "Part", "meaning": "đã (trợ từ hoàn tất)" },
            { "text": "很多", "type": "normal", "role": "Attr", "meaning": "rất nhiều" },
            { "text": "观众", "type": "core", "role": "O", "meaning": "khán giả, người xem" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "这场比赛", "type": "subject", "desc": "Chỉ từ + Lượng từ + Danh từ '比赛'" },
            { "role": "Vị ngữ (V)", "text": "吸引了", "type": "predicate", "desc": "Động từ '吸引' + Trợ từ hoàn tất '了'" },
            { "role": "Cụm tân ngữ (O)", "text": "很多观众", "type": "object", "desc": "Định ngữ '很多' + Danh từ '观众'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["这场", "观众", "比赛", "了", "吸引", "很多"],
            "target_chunks": ["这场", "比赛", "吸引", "了", "很多", "观众"],
            "hint": "Ghép cụm chủ ngữ '这场比赛', vị ngữ '吸引了', cụm tân ngữ '很多观众'."
        }
    },
    {
        "id": "hsk4_b1_90",
        "category": "sentence_building",
        "title": "把作业写完再去打球",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第90题)",
        "zh": "把作业写完再去打球。",
        "vietnamese": "Làm xong bài tập rồi hãy đi chơi bóng.",
        "grammar_point": {
            "name": "Câu chữ 把 kết hợp liên từ hành động: 把 + O + V完 + 再 + V2",
            "pattern": "把 + Tân ngữ + Động từ + Bổ ngữ kết quả (完) + 再 + V2",
            "level": "HSK 4 Điểm ngữ pháp bẫy hàng đầu",
            "trap_note": "BẪY THI CỰC QUAN TRỌNG: 1. Động từ trong câu chữ 把 không bao giờ được đứng trơ trọi một mình, bắt buộc phải có thành phần kèm theo (ở đây là bổ ngữ kết quả '完'). 2. Phó từ thời gian liên kết '再' (rồi mới) phải đứng trước động từ thứ hai '去', tuyệt đối không đặt trước '把'.",
            "explanation": "Câu chữ 把 nhấn mạnh việc tác động và giải quyết triệt để đối tượng '作业' (viết cho xong) trước khi chuyển sang hành động giải trí tiếp theo là '去打球'."
        },
        "tokens": [
            { "text": "把", "type": "grammar", "role": "Prep", "meaning": "đem, lấy (giới từ câu chữ 把)" },
            { "text": "作业", "type": "core", "role": "O_prep", "meaning": "bài tập" },
            { "text": "写", "type": "normal", "role": "V", "meaning": "viết, làm" },
            { "text": "完", "type": "normal", "role": "Comp", "meaning": "xong (bổ ngữ kết quả)" },
            { "text": "再", "type": "grammar", "role": "Adv", "meaning": "rồi mới (phó từ liên kết)" },
            { "text": "去", "type": "normal", "role": "V", "meaning": "đi" },
            { "text": "打球", "type": "normal", "role": "O", "meaning": "chơi bóng" }
        ],
        "breakdown": [
            { "role": "Cụm giới từ 把", "text": "把作业", "type": "prep", "desc": "Giới từ 把 đưa đối tượng bị xử lý '作业' lên trước" },
            { "role": "Vị ngữ 1 + Bổ ngữ", "text": "写完", "type": "predicate", "desc": "Động từ '写' + Bổ ngữ kết quả '完'" },
            { "role": "Trạng ngữ nối", "text": "再", "type": "adv", "desc": "Phó từ biểu thị thứ tự trước sau" },
            { "role": "Vị ngữ 2", "text": "去打球", "type": "predicate", "desc": "Cụm động từ liên tiếp" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["作业", "把", "写完", "去", "再", "打球"],
            "target_chunks": ["把", "作业", "写完", "再", "去", "打球"],
            "hint": "Cấu trúc 把 + tân ngữ + động từ + kết quả. Nhớ '再' đứng trước '去'."
        }
    },
    {
        "id": "hsk4_b1_91",
        "category": "sentence_building",
        "title": "墙上贴着一张成绩单",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第91题)",
        "zh": "墙上贴着一张成绩单。",
        "vietnamese": "Trên tường có dán một bảng điểm.",
        "grammar_point": {
            "name": "Câu tồn hiện (存现句): Nơi chốn + V + 着 + Tân ngữ vô định",
            "pattern": "Từ chỉ nơi chốn/vị trí + Động từ + 着 + Số lượng từ + Danh từ",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI: 1. Tân ngữ trong câu tồn hiện bắt buộc phải là 'vô định' (chưa xác định, thường có số lượng từ '一张...', không dùng '这张'). 2. Trước từ chỉ nơi chốn '墙上' KHÔNG ĐƯỢC thêm giới từ '在'. Viết '在墙上贴着...' là sai ngữ pháp thi HSK!",
            "explanation": "Câu tồn hiện miêu tả sự xuất hiện hoặc trạng thái tồn tại của sự vật ở một địa điểm xác định. '墙上' là chủ ngữ vị trí, '贴着' là vị ngữ trạng thái."
        },
        "tokens": [
            { "text": "墙上", "type": "core", "role": "Place", "meaning": "trên tường" },
            { "text": "贴", "type": "core", "role": "V", "meaning": "dán" },
            { "text": "着", "type": "grammar", "role": "Part", "meaning": "đang (trợ từ trạng thái tồn tại)" },
            { "text": "一张", "type": "normal", "role": "Num_Clf", "meaning": "một tờ/tấm" },
            { "text": "成绩单", "type": "core", "role": "O", "meaning": "bảng điểm, phiếu kết quả" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ nơi chốn", "text": "墙上", "type": "subject", "desc": "Địa điểm diễn ra sự tồn hiện" },
            { "role": "Vị ngữ tồn hiện", "text": "贴着", "type": "predicate", "desc": "Động từ '贴' + trợ từ trạng thái '着'" },
            { "role": "Tân ngữ vô định", "text": "一张成绩单", "type": "object", "desc": "Số lượng từ '一张' + danh từ '成绩单'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["一张", "墙上", "着", "成绩单", "贴"],
            "target_chunks": ["墙上", "贴", "着", "一张", "成绩单"],
            "hint": "Nơi chốn '墙上' đứng đầu, động từ '贴着', theo sau là số lượng tân ngữ '一张成绩单'."
        }
    },
    {
        "id": "hsk4_b1_92",
        "category": "sentence_building",
        "title": "麦克汉语说得很流利",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第92题)",
        "zh": "麦克汉语说得很流利。",
        "vietnamese": "Mike nói tiếng Hán rất lưu loát.",
        "grammar_point": {
            "name": "Bổ ngữ trạng thái / trình độ (程度补语) với '得'",
            "pattern": "S + (Tân ngữ) + V + 得 + Cụm tính từ (很/非常 + Adj)",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI: Khi động từ có tân ngữ ('说汉语'), có 2 cách sắp xếp chuẩn: 1. Đưa tân ngữ lên trước động từ: '麦克汉语说得很流利'; 2. Lặp lại động từ: '麦克说汉语说得很流利'. Tuyệt đối không được nói '麦克说很流利汉语' (sai quy tắc ngữ pháp).",
            "explanation": "Bổ ngữ trạng thái '很流利' đứng sau trợ từ kết cấu '得' dùng để đánh giá, nhận xét trình độ phát âm nói tiếng Hán của Mike."
        },
        "tokens": [
            { "text": "麦克", "type": "normal", "role": "S", "meaning": "Mike (tên riêng)" },
            { "text": "汉语", "type": "normal", "role": "O_topic", "meaning": "tiếng Hán" },
            { "text": "说", "type": "normal", "role": "V", "meaning": "nói" },
            { "text": "得", "type": "grammar", "role": "Part", "meaning": "được, đến mức (trợ từ kết cấu)" },
            { "text": "很", "type": "normal", "role": "Adv", "meaning": "rất" },
            { "text": "流利", "type": "core", "role": "Comp", "meaning": "lưu loát, trôi chảy" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "麦克", "type": "subject", "desc": "Chủ thể thực hiện hành động" },
            { "role": "Khởi ngữ / Tân ngữ trước", "text": "汉语", "type": "object", "desc": "Chủ đề / ngôn ngữ được nói" },
            { "role": "Vị ngữ (V)", "text": "说", "type": "predicate", "desc": "Động từ hành động" },
            { "role": "Bổ ngữ trình độ", "text": "得很流利", "type": "comp", "desc": "Trợ từ '得' + tính từ '很流利'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["汉语", "麦克", "说", "很", "流利", "得"],
            "target_chunks": ["麦克", "汉语", "说", "得", "很", "流利"],
            "hint": "Chủ ngữ 麦克 + tân ngữ 汉语 + động từ 说 + 得 + 很流利."
        }
    },
    {
        "id": "hsk4_b1_93",
        "category": "sentence_building",
        "title": "他没有一天不迟到的",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第93题)",
        "zh": "他没有一天不迟到的。",
        "vietnamese": "Không có ngày nào là anh ấy không đi muộn (ngày nào anh ấy cũng đi muộn).",
        "grammar_point": {
            "name": "Cấu trúc phủ định kép nhấn mạnh: 没有……不……的",
            "pattern": "S + 没有 + Danh từ thời gian/đơn vị + 不 + V + (的)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Hai từ phủ định '没有' và '不' kết hợp với nhau tạo thành nghĩa khẳng định tuyệt đối cực mạnh (không ngày nào không muộn = ngày nào cũng muộn 100%). Thí sinh thường lúng túng khi xếp thứ tự của hai từ phủ định.",
            "explanation": "'没有一天' phủ định số lượng thời gian, '不迟到' phủ định hành vi. '的' cuối câu mang sắc thái nhấn mạnh sự việc là hiển nhiên."
        },
        "tokens": [
            { "text": "他", "type": "normal", "role": "S", "meaning": "anh ấy" },
            { "text": "没有", "type": "grammar", "role": "V_neg", "meaning": "không có" },
            { "text": "一天", "type": "normal", "role": "Time", "meaning": "một ngày" },
            { "text": "不", "type": "grammar", "role": "Adv_neg", "meaning": "không (phó từ phủ định)" },
            { "text": "迟到", "type": "core", "role": "V", "meaning": "đến muộn, trễ giờ" },
            { "text": "的", "type": "normal", "role": "Part", "meaning": "trợ từ ngữ khí nhấn mạnh" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "他", "type": "subject", "desc": "Đối tượng được nói đến" },
            { "role": "Phủ định 1", "text": "没有一天", "type": "predicate", "desc": "Động từ '没有' + lượng thời gian '一天'" },
            { "role": "Phủ định 2 + Nhấn mạnh", "text": "不迟到的", "type": "adv", "desc": "'不' + động từ '迟到' + trợ từ '的'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["他", "一天", "迟到", "不", "的", "没有"],
            "target_chunks": ["他", "没有", "一天", "不", "迟到", "的"],
            "hint": "Cấu trúc phủ định kép: 他 + 没有一天 + 不迟到的."
        }
    },
    {
        "id": "hsk4_b1_94",
        "category": "sentence_building",
        "title": "照相机叫李力借走了",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第94题)",
        "zh": "照相机叫李力借走了。",
        "vietnamese": "Máy ảnh đã bị Lý Lực mượn đi rồi.",
        "grammar_point": {
            "name": "Câu bị động khẩu ngữ dùng chữ 叫 (叫字句)",
            "pattern": "Chủ ngữ (vật bị tác động) + 叫 + Tác nhân gây ra + V + Bổ ngữ (走了/去了...)",
            "level": "HSK 4 Điểm bẫy ngữ pháp",
            "trap_note": "BẪY THI CẦN NHỚ: Trong văn nói tiếng Trung, '叫' và '让' có thể dùng tương tự như '被' để tạo câu bị động. Tuy nhiên, khác với '被' có thể lược bỏ tác nhân (ví dụ: '照相机被借走了'), chữ '叫' và '让' BẮT BUỘC PHẢI CÓ TÁC NHÂN theo sau (ở đây là '李力'). Không bao giờ nói '照相机叫借走了'!",
            "explanation": "'照相机' là vật bị mượn, '李力' là người mượn, '借走' gồm động từ '借' và bổ ngữ xu hướng '走', kết thúc bằng trợ từ biến đổi '了'."
        },
        "tokens": [
            { "text": "照相机", "type": "core", "role": "S_patient", "meaning": "máy chụp ảnh" },
            { "text": "叫", "type": "grammar", "role": "Prep_passive", "meaning": "bị, được (giới từ bị động)" },
            { "text": "李力", "type": "normal", "role": "Agent", "meaning": "Lý Lực (tác nhân)" },
            { "text": "借", "type": "core", "role": "V", "meaning": "mượn, vay" },
            { "text": "走", "type": "normal", "role": "Comp", "meaning": "đi (bổ ngữ xu hướng)" },
            { "text": "了", "type": "normal", "role": "Part", "meaning": "rồi (trợ từ ngữ khí)" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ chịu tác động", "text": "照相机", "type": "subject", "desc": "Đồ vật bị hành động tác động lên" },
            { "role": "Cụm bị động", "text": "叫李力", "type": "prep", "desc": "Giới từ '叫' + Tác nhân '李力'" },
            { "role": "Vị ngữ + Bổ ngữ", "text": "借走了", "type": "predicate", "desc": "Động từ '借' + Bổ ngữ xu hướng '走' + '了'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["走", "照相机", "李力", "借", "叫", "了"],
            "target_chunks": ["照相机", "叫", "李力", "借", "走", "了"],
            "hint": "Cấu trúc bị động chữ 叫: 照相机 + 叫李力 + 借走了."
        }
    },
    {
        "id": "hsk4_b1_95",
        "category": "sentence_building",
        "title": "这顶帽子的颜色深了一点儿",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "书写 第一部分 (完成句子 第95题)",
        "zh": "这顶帽子的颜色深了一点儿。",
        "vietnamese": "Màu của chiếc mũ này hơi đậm một chút.",
        "grammar_point": {
            "name": "Biểu thị mức độ chênh lệch: Tính từ + 了 + 一点儿",
            "pattern": "Chủ ngữ + Tính từ + (了) + 一点儿",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI KINH ĐIỂN: Phân biệt '有点儿 + Adj' và 'Adj + 一点儿': 1. '有点儿' đứng TRƯỚC tính từ biểu thị sự không hài lòng ('有点儿深'); 2. '一点儿' đứng SAU tính từ biểu thị mức độ so sánh hoặc chênh lệch ('深了一点儿'). Đề thi HSK 4 rất hay đưa '一点儿' để kiểm tra vị trí đứng sau tính từ!",
            "explanation": "Lượng từ '顶' (dǐng) dùng cho nón, mũ. '深了一点儿' mang cấu trúc tính từ chỉ độ đậm nhạt '深' cộng với '一点儿' để diễn tả màu đậm hơn kỳ vọng một chút."
        },
        "tokens": [
            { "text": "这", "type": "normal", "role": "Attr", "meaning": "này" },
            { "text": "顶", "type": "core", "role": "Clf", "meaning": "chiếc, cái (lượng từ của mũ)" },
            { "text": "帽子", "type": "core", "role": "Noun", "meaning": "cái mũ, nón" },
            { "text": "的", "type": "normal", "role": "Part", "meaning": "của (trợ từ kết cấu)" },
            { "text": "颜色", "type": "normal", "role": "S", "meaning": "màu sắc" },
            { "text": "深", "type": "core", "role": "Adj", "meaning": "đậm, sâu" },
            { "text": "了", "type": "normal", "role": "Part", "meaning": "rồi" },
            { "text": "一点儿", "type": "core", "role": "Comp", "meaning": "một chút, một ít" }
        ],
        "breakdown": [
            { "role": "Cụm chủ ngữ", "text": "这顶帽子的颜色", "type": "subject", "desc": "Định ngữ đa tầng + trung tâm ngữ '颜色'" },
            { "role": "Vị ngữ tính từ", "text": "深了", "type": "predicate", "desc": "Tính từ '深' + '了'" },
            { "role": "Bổ ngữ số lượng", "text": "一点儿", "type": "comp", "desc": "Biểu thị mức độ chênh lệch nhỏ" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["颜色", "一点儿", "的", "帽子", "这顶", "深了"],
            "target_chunks": ["这顶", "帽子", "的", "颜色", "深了", "一点儿"],
            "hint": "Chủ ngữ là '这顶帽子的颜色', vị ngữ là '深了一点儿'."
        }
    },
    {
        "id": "hsk4_b2_90",
        "category": "sentence_building",
        "title": "不要把这个消息告诉别人",
        "source": "HSK 4 模拟试卷 2",
        "exam_part": "书写 第一部分 (完成句子 第90题)",
        "zh": "不要把这个消息告诉别人。",
        "vietnamese": "Đừng đem tin này nói cho người khác biết.",
        "grammar_point": {
            "name": "Phủ định của câu chữ 把: 别 / 不要 / 没 + 把 + O + V...",
            "pattern": "(S) + 别 / 不要 / 没 + 把 + O + Động từ + Tân ngữ gián tiếp",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI ĐẶC BIỆT: Từ phủ định ('不要', '别', '没') BẮT BUỘC PHẢI ĐỨNG TRƯỚC GIỚI TỪ '把'. Tuyệt đối không được đặt sau '把' (ví dụ: viết '把这个消息不要告诉别人' là hoàn toàn sai ngữ pháp).",
            "explanation": "Câu chữ 把 dạng mệnh lệnh phủ định dùng '不要' đứng trước giới từ để yêu cầu người nghe ngăn chặn việc truyền đạt thông tin '这个消息' tới '别人'."
        },
        "tokens": [
            { "text": "不要", "type": "grammar", "role": "Adv_neg", "meaning": "đừng, không được" },
            { "text": "把", "type": "grammar", "role": "Prep", "meaning": "đem (giới từ)" },
            { "text": "这个", "type": "normal", "role": "Attr", "meaning": "này" },
            { "text": "消息", "type": "core", "role": "O_prep", "meaning": "tin tức, thông tin" },
            { "text": "告诉", "type": "normal", "role": "V", "meaning": "nói cho, bảo" },
            { "text": "别人", "type": "core", "role": "O", "meaning": "người khác" }
        ],
        "breakdown": [
            { "role": "Trạng ngữ phủ định", "text": "不要", "type": "adv", "desc": "Từ phủ định đứng trước giới từ '把'" },
            { "role": "Cụm giới từ 把", "text": "把这个消息", "type": "prep", "desc": "Giới từ 把 + đối tượng thông tin" },
            { "role": "Vị ngữ động từ", "text": "告诉", "type": "predicate", "desc": "Động từ trao đổi thông tin" },
            { "role": "Tân ngữ gián tiếp", "text": "别人", "type": "object", "desc": "Người tiếp nhận thông tin" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["这个", "别人", "不要", "把", "告诉", "消息"],
            "target_chunks": ["不要", "把", "这个", "消息", "告诉", "别人"],
            "hint": "Từ phủ định '不要' đứng trước '把', tiếp theo là '这个消息', sau đó là '告诉别人'."
        }
    },
    {
        "id": "hsk4_b2_94",
        "category": "sentence_building",
        "title": "桌子被学生们搬走了",
        "source": "HSK 4 模拟试卷 2",
        "exam_part": "书写 第一部分 (完成句子 第94题)",
        "zh": "桌子被学生们搬走了。",
        "vietnamese": "Cái bàn đã bị các bạn học sinh khiêng đi rồi.",
        "grammar_point": {
            "name": "Câu bị động chuẩn với chữ 被 (被字句)",
            "pattern": "Chủ ngữ (chịu tác động) + 被 + Tác nhân + Động từ + Bổ ngữ (走/掉/完) + 了",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI: Câu chữ 被 cũng giống câu chữ 把, động từ không được đứng đơn độc, phải có bổ ngữ kết quả hoặc xu hướng phía sau (ở đây là '走了'). Tác nhân '学生们' đứng giữa '被' và động từ '搬'.",
            "explanation": "Câu chữ 被 dùng để nhấn mạnh kết quả hoặc sự thay đổi vị trí của cái bàn dưới tác động của nhóm học sinh."
        },
        "tokens": [
            { "text": "桌子", "type": "normal", "role": "S_patient", "meaning": "cái bàn" },
            { "text": "被", "type": "grammar", "role": "Prep_passive", "meaning": "bị (giới từ bị động)" },
            { "text": "学生们", "type": "normal", "role": "Agent", "meaning": "các bạn học sinh" },
            { "text": "搬", "type": "core", "role": "V", "meaning": "khiêng, dọn, chuyển" },
            { "text": "走", "type": "normal", "role": "Comp", "meaning": "đi (bổ ngữ xu hướng)" },
            { "text": "了", "type": "normal", "role": "Part", "meaning": "rồi" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ chịu tác động", "text": "桌子", "type": "subject", "desc": "Sự vật bị chuyển dịch vị trí" },
            { "role": "Cụm bị động", "text": "被学生们", "type": "prep", "desc": "Giới từ '被' + tác nhân hành động" },
            { "role": "Vị ngữ + Bổ ngữ", "text": "搬走了", "type": "predicate", "desc": "Động từ '搬' + Bổ ngữ '走' + '了'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["学生们", "被", "搬", "桌子", "走了"],
            "target_chunks": ["桌子", "被", "学生们", "搬", "走了"],
            "hint": "Sự vật chịu tác động '桌子' đứng đầu câu, theo sau là '被学生们搬走了'."
        }
    },
    {
        "id": "hsk4_b2_91",
        "category": "sentence_building",
        "title": "经理让我快点儿交计划书",
        "source": "HSK 4 模拟试卷 2",
        "exam_part": "书写 第一部分 (完成句子 第91题)",
        "zh": "经理让我快点儿交计划书。",
        "vietnamese": "Giám đốc bảo tôi nộp bản kế hoạch nhanh lên một chút.",
        "grammar_point": {
            "name": "Câu kiêm ngữ (兼语句) với 让 / 请 / 叫 / 使",
            "pattern": "S1 + 让/请/叫 + Kiêm ngữ (O1/S2) + Trạng ngữ (快点儿) + V2 + O2",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI: Trong câu kiêm ngữ, từ '我' vừa làm tân ngữ của động từ cầu khiến '让', vừa làm chủ ngữ thực hiện hành động nộp '交计划书'. Trạng từ chỉ tốc độ '快点儿' bổ nghĩa cho động từ '交'.",
            "explanation": "Câu kiêm ngữ là dạng câu đặc trưng tiếng Trung khi một danh từ giữ đồng thời hai vai trò ngữ pháp nối tiếp giữa hai động từ."
        },
        "tokens": [
            { "text": "经理", "type": "core", "role": "S", "meaning": "giám đốc, quản lý" },
            { "text": "让", "type": "grammar", "role": "V_causative", "meaning": "bảo, khiến, cho phép (động từ kiêm ngữ)" },
            { "text": "我", "type": "normal", "role": "Pivot", "meaning": "tôi (kiêm ngữ)" },
            { "text": "快点儿", "type": "normal", "role": "Adv", "meaning": "nhanh một chút" },
            { "text": "交", "type": "core", "role": "V2", "meaning": "nộp, giao" },
            { "text": "计划书", "type": "core", "role": "O2", "meaning": "bản kế hoạch" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ chính", "text": "经理", "type": "subject", "desc": "Người đưa ra yêu cầu" },
            { "role": "Động từ sai khiến", "text": "让", "type": "predicate", "desc": "Động từ thứ nhất mang kiêm ngữ" },
            { "role": "Thành phần kiêm ngữ", "text": "我", "type": "object", "desc": "Vừa là tân ngữ của '让', vừa là chủ ngữ của '交'" },
            { "role": "Vị ngữ thứ hai", "text": "快点儿交计划书", "type": "predicate", "desc": "Hành động được yêu cầu thực hiện" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["计划书", "让我", "快点儿", "经理", "交"],
            "target_chunks": ["经理", "让我", "快点儿", "交", "计划书"],
            "hint": "Chủ ngữ 经理 + động từ sai khiến 让我 + trạng từ 快点儿 + 交计划书."
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Order Logic A-B-C)
    # =========================================================================
    {
        "id": "hsk4_r1_56",
        "category": "sentence_logic",
        "title": "电影院离这儿很远，如果你想去的话，我就开车送你",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第二部分 (排列顺序 第56题)",
        "zh": "电影院离这儿很远，如果你想去的话，我就开车送你。",
        "vietnamese": "Rạp chiếu phim cách đây rất xa, nếu bạn muốn đi thì tôi sẽ lái xe đưa bạn đi.",
        "grammar_point": {
            "name": "Liên từ giả thiết: 如果……（的话），就……",
            "pattern": "Tiền đề tình huống (B) -> Giả thiết (A: 如果……的话) -> Hệ quả/Hành động (C: 就……)",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "MẸO LÀM BÀI HSK 4: Câu B giới thiệu bối cảnh thực tế ('电影院离这儿很远'), làm tiền đề cho câu giả thiết A ('如果你想去的话'), và câu C đưa ra cách giải quyết đi kèm phó từ '就' ('我就开车送你'). Thứ tự chuẩn logic là B - A - C.",
            "explanation": "Cặp liên từ '如果……就……' biểu thị mối quan hệ điều kiện - giả thiết. '离……远' là cấu trúc biểu thị khoảng cách không gian."
        },
        "tokens": [
            { "text": "电影院", "type": "core", "role": "S", "meaning": "rạp chiếu phim" },
            { "text": "离", "type": "core", "role": "Prep", "meaning": "cách (giới từ khoảng cách)" },
            { "text": "这儿", "type": "normal", "role": "Place", "meaning": "đây, chỗ này" },
            { "text": "很远", "type": "normal", "role": "Adj", "meaning": "rất xa" },
            { "text": "如果", "type": "grammar", "role": "Conj", "meaning": "nếu (liên từ giả thiết)" },
            { "text": "你想去", "type": "normal", "role": "Clause", "meaning": "bạn muốn đi" },
            { "text": "的话", "type": "grammar", "role": "Part", "meaning": "thì, nếu mà" },
            { "text": "我就", "type": "grammar", "role": "Adv", "meaning": "tôi liền" },
            { "text": "开车", "type": "normal", "role": "V", "meaning": "lái xe" },
            { "text": "送你", "type": "core", "role": "V_O", "meaning": "đưa đón bạn" }
        ],
        "breakdown": [
            { "role": "Bối cảnh tiền đề (B)", "text": "电影院离这儿很远", "type": "prep", "desc": "Nêu rõ khoảng cách xa xôi" },
            { "role": "Mệnh đề giả thiết (A)", "text": "如果你想去的话", "type": "conj", "desc": "Giả định mong muốn của đối phương" },
            { "role": "Mệnh đề kết quả (C)", "text": "我就开车送你", "type": "predicate", "desc": "Giải pháp đưa ra tương ứng" }
        ],
        "practice": {
            "type": "sentence_logic",
            "scrambled_items": [
                { "key": "A", "text": "如果你想去的话" },
                { "key": "B", "text": "电影院离这儿很远" },
                { "key": "C", "text": "我就开车送你" }
            ],
            "correct_order": "BAC",
            "explanation": "B nêu tình huống khách quan -> A đưa ra giả thiết '如果……的话' -> C là lời đề nghị giải quyết với '就'."
        }
    },
    {
        "id": "hsk4_r1_63",
        "category": "sentence_logic",
        "title": "随着生活节奏的加快，人们的压力越来越大，因此更要放松心情",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第二部分 (排列顺序 第63题)",
        "zh": "随着生活节奏的加快，人们的压力越来越大，因此更要放松心情。",
        "vietnamese": "Cùng với nhịp sống ngày càng gấp gáp, áp lực của con người ngày càng lớn, vì vậy càng cần phải thư giãn tinh thần.",
        "grammar_point": {
            "name": "Mối quan hệ phát triển & nhân quả: 随着……，越来越……，因此……",
            "pattern": "随着 + Xu hướng biến đổi (A) -> Hiện trạng (C: 越来越...) -> Kết luận hành động (B: 因此...)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "MẸO LÀM BÀI HSK 4: 1. Câu bắt đầu bằng '随着' (cùng với...) thường đứng đầu để mở ra xu hướng xã hội. 2. Câu tiếp theo diễn tả kết quả tự nhiên với '越来越'. 3. Câu bắt đầu bằng liên từ kết luận '因此' (do đó, vì thế) đứng cuối cùng. Thứ tự logic: A - C - B.",
            "explanation": "'随着' dẫn dắt trạng ngữ biến đổi thời đại, '越来越' thể hiện mức độ gia tăng, '因此' làm liên từ liên kết nhân quả để đưa ra lời khuyên."
        },
        "tokens": [
            { "text": "随着", "type": "grammar", "role": "Prep", "meaning": "cùng với, đi cùng (giới từ xu hướng)" },
            { "text": "生活节奏", "type": "advanced", "role": "Noun", "meaning": "nhịp sống" },
            { "text": "的", "type": "normal", "role": "Part", "meaning": "của" },
            { "text": "加快", "type": "advanced", "role": "V", "meaning": "nhanh hơn, tăng tốc" },
            { "text": "人们的", "type": "normal", "role": "Attr", "meaning": "của con người" },
            { "text": "压力", "type": "core", "role": "S", "meaning": "áp lực" },
            { "text": "越来越", "type": "grammar", "role": "Adv", "meaning": "ngày càng (phó từ tăng tiến)" },
            { "text": "大", "type": "normal", "role": "Adj", "meaning": "lớn" },
            { "text": "因此", "type": "grammar", "role": "Conj", "meaning": "vì vậy, do đó (liên từ kết luận)" },
            { "text": "更要", "type": "normal", "role": "Adv", "meaning": "càng phải" },
            { "text": "放松", "type": "core", "role": "V", "meaning": "thư giãn, thả lỏng" },
            { "text": "心情", "type": "core", "role": "O", "meaning": "tâm trạng, tinh thần" }
        ],
        "breakdown": [
            { "role": "Xu hướng thời đại (A)", "text": "随着生活节奏的加快", "type": "prep", "desc": "Giới từ '随着' nêu bối cảnh chuyển biến" },
            { "role": "Hậu quả thực tế (C)", "text": "人们的压力越来越大", "type": "subject", "desc": "Hiện tượng gia tăng áp lực cuộc sống" },
            { "role": "Kết luận giải pháp (B)", "text": "因此更要放松心情", "type": "conj", "desc": "Liên từ '因此' dẫn dắt lời khuyên thư giãn" }
        ],
        "practice": {
            "type": "sentence_logic",
            "scrambled_items": [
                { "key": "A", "text": "随着生活节奏的加快" },
                { "key": "B", "text": "因此更要放松心情" },
                { "key": "C", "text": "人们的压力越来越大" }
            ],
            "correct_order": "ACB",
            "explanation": "A nêu bối cảnh xu thế '随着……' -> C nêu hiện trạng '越来越大' -> B kết luận với liên từ '因此'."
        }
    },
    {
        "id": "hsk4_r1_65",
        "category": "sentence_logic",
        "title": "吸烟不仅影响自己的健康，还会使周围的人不舒服，青少年最好不要接触",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第二部分 (排列顺序 第65题)",
        "zh": "吸烟不仅影响自己的健康，还会使周围的人不舒服，青少年最好不要接触。",
        "vietnamese": "Hút thuốc không những ảnh hưởng đến sức khỏe của bản thân, mà còn khiến người xung quanh khó chịu, thanh thiếu niên tốt nhất không nên tiếp xúc.",
        "grammar_point": {
            "name": "Cấu trúc tăng tiến & kiêm ngữ: 不仅……还……，使……",
            "pattern": "Chủ đề + 不仅 (A) + 还 / 而且 (C) -> Lời khuyên kết luận (B)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "MẸO LÀM BÀI HSK 4: Cặp liên từ '不仅……还……' (không những...mà còn...) bắt buộc vế '不仅' đi trước vế '还'. Vế B là lời khuyên cho thanh thiếu niên được rút ra từ hai tác hại trên, nên đứng ở vị trí cuối cùng. Thứ tự: A - C - B.",
            "explanation": "'不仅……还……' liên kết hai mức độ tác hại từ gần (bản thân) đến xa (người xung quanh). '使' là động từ kiêm ngữ biểu thị sự tác động gây ra trạng thái."
        },
        "tokens": [
            { "text": "吸烟", "type": "advanced", "role": "S", "meaning": "hút thuốc" },
            { "text": "不仅", "type": "grammar", "role": "Conj", "meaning": "không những (liên từ tăng tiến)" },
            { "text": "影响", "type": "core", "role": "V", "meaning": "ảnh hưởng" },
            { "text": "自己的", "type": "normal", "role": "Attr", "meaning": "của bản thân" },
            { "text": "健康", "type": "core", "role": "O", "meaning": "sức khỏe" },
            { "text": "还会", "type": "grammar", "role": "Conj", "meaning": "còn có thể, lại còn" },
            { "text": "使", "type": "grammar", "role": "V_causative", "meaning": "khiến cho, làm cho (kiêm ngữ)" },
            { "text": "周围的", "type": "core", "role": "Attr", "meaning": "xung quanh" },
            { "text": "人不舒服", "type": "normal", "role": "Predicate", "meaning": "người ta khó chịu" },
            { "text": "青少年", "type": "advanced", "role": "S2", "meaning": "thanh thiếu niên" },
            { "text": "最好", "type": "core", "role": "Adv", "meaning": "tốt nhất" },
            { "text": "不要接触", "type": "core", "role": "V2", "meaning": "đừng tiếp xúc" }
        ],
        "breakdown": [
            { "role": "Tác hại thứ nhất (A)", "text": "吸烟不仅影响自己的健康", "type": "subject", "desc": "Vế '不仅' chỉ tác hại đối với bản thân" },
            { "role": "Tác hại tăng tiến (C)", "text": "还会使周围的人不舒服", "type": "predicate", "desc": "Vế '还' mở rộng tác hại sang cộng đồng" },
            { "role": "Lời khuyên kết luận (B)", "text": "青少年最好不要接触", "type": "adv", "desc": "Khuyên thanh thiếu niên tránh xa" }
        ],
        "practice": {
            "type": "sentence_logic",
            "scrambled_items": [
                { "key": "A", "text": "吸烟不仅影响自己的健康" },
                { "key": "B", "text": "青少年最好不要接触" },
                { "key": "C", "text": "还会使周围的人不舒服" }
            ],
            "correct_order": "ACB",
            "explanation": "Cặp liên từ '不仅' (A) đi trước '还会' (C), sau đó mới tới câu đưa ra định hướng khuyên nhủ (B)."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test In Living Context)
    # =========================================================================
    {
        "id": "hsk4_c1_46",
        "category": "cloze",
        "title": "房子的价格始终降不下来",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第一部分 (选词填空 第46题)",
        "zh": "房子的价格始终降不下来，我只好等几年再买了。",
        "vietnamese": "Giá nhà từ đầu đến cuối vẫn không giảm xuống được, tôi đành phải đợi vài năm nữa mới mua vậy.",
        "grammar_point": {
            "name": "Phó từ diễn tả tính liên tục bền bỉ: 始终 (Thủy chung / Từ đầu đến cuối)",
            "pattern": "Chủ ngữ + 始终 + Động từ / Bổ ngữ khả năng phủ định (降不下来)",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI CẦN LƯU Ý: Phân biệt '始终' và '一直': '始终' mang sắc thái từ đầu chí cuối không hề thay đổi bản chất, thường đi kèm với những tình huống kéo dài mang tính quy luật hoặc khó đảo ngược. '降不下来' là bổ ngữ khả năng phủ định.",
            "explanation": "'始终' đóng vai trò trạng ngữ đứng trước cụm vị ngữ '降不下来'. '只好' (đành phải) diễn tả sự lựa chọn bắt buộc khi hoàn cảnh không như ý."
        },
        "tokens": [
            { "text": "房子", "type": "normal", "role": "Attr", "meaning": "nhà cửa" },
            { "text": "的", "type": "normal", "role": "Part", "meaning": "của" },
            { "text": "价格", "type": "core", "role": "S", "meaning": "giá cả" },
            { "text": "始终", "type": "core", "role": "Adv", "meaning": "từ đầu đến cuối, luôn luôn" },
            { "text": "降", "type": "core", "role": "V", "meaning": "hạ, giảm" },
            { "text": "不下来", "type": "normal", "role": "Comp", "meaning": "không xuống được (bổ ngữ khả năng)" },
            { "text": "我只好", "type": "core", "role": "Adv", "meaning": "tôi đành phải" },
            { "text": "等几年", "type": "normal", "role": "Time", "meaning": "đợi vài năm" },
            { "text": "再买", "type": "normal", "role": "V", "meaning": "mới mua" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "房子的价格", "type": "subject", "desc": "Đối tượng chính là giá nhà" },
            { "role": "Trạng ngữ phó từ", "text": "始终", "type": "adv", "desc": "Từ cần điền: biểu thị sự việc không thay đổi từ trước đến nay" },
            { "role": "Vị ngữ + Bổ ngữ khả năng", "text": "降不下来", "type": "comp", "desc": "Không thể giảm xuống được" },
            { "role": "Vế kết quả đành chịu", "text": "我只好等几年再买了", "type": "predicate", "desc": "Giải pháp lựa chọn bắt buộc" }
        ],
        "practice": {
            "type": "cloze",
            "blank_sentence": "房子的价格（ ____ ）降不下来，我只好等几年再买了。",
            "target_word": "始终",
            "options": [
                { "word": "始终", "pinyin": "shǐzhōng", "hanviet": "Thủy Chung", "meaning": "từ đầu đến cuối, luôn luôn" },
                { "word": "坚持", "pinyin": "jiānchí", "hanviet": "Kiên Trì", "meaning": "kiên trì, giữ vững" },
                { "word": "负责", "pinyin": "fùzé", "hanviet": "Phụ Trách", "meaning": "chịu trách nhiệm" },
                { "word": "遵守", "pinyin": "zūnshǒu", "hanviet": "Tuân Thủ", "meaning": "tuân theo, tôn trọng" }
            ],
            "clue": "Chỗ trống đứng giữa chủ ngữ '房子的价格' và vị ngữ '降不下来', cần một phó từ chỉ trạng thái liên tục không đổi từ trước tới giờ."
        }
    },
    {
        "id": "hsk4_c1_48",
        "category": "cloze",
        "title": "王芳对工作很负责",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第一部分 (选词填空 第48题)",
        "zh": "王芳对工作很负责，这个任务你可以放心交给她。",
        "vietnamese": "Vương Phương đối với công việc rất có trách nhiệm, nhiệm vụ này bạn có thể yên tâm giao cho cô ấy.",
        "grammar_point": {
            "name": "Tính từ chỉ thái độ: 对……负责 (Có trách nhiệm với...)",
            "pattern": "Chủ ngữ + 对 + Đối tượng + (很/非常) + 负责",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI: Từ '负责' trong tiếng Trung vừa là động từ ('phụ trách việc gì'), vừa là tính từ ('rất có tinh thần trách nhiệm'). Trong câu này, đứng sau phó từ mức độ '很', '负责' đóng vai trò là TÍNH TỪ vị ngữ.",
            "explanation": "'对工作很负责' miêu tả phẩm chất làm việc tận tụy, làm tiền đề tin cậy để '放心交给她'."
        },
        "tokens": [
            { "text": "王芳", "type": "normal", "role": "S", "meaning": "Vương Phương (tên riêng)" },
            { "text": "对", "type": "grammar", "role": "Prep", "meaning": "đối với" },
            { "text": "工作", "type": "normal", "role": "O_prep", "meaning": "công việc" },
            { "text": "很", "type": "normal", "role": "Adv", "meaning": "rất" },
            { "text": "负责", "type": "core", "role": "Adj", "meaning": "có trách nhiệm, tận tụy" },
            { "text": "这个任务", "type": "core", "role": "O_front", "meaning": "nhiệm vụ này" },
            { "text": "你可以", "type": "normal", "role": "S2", "meaning": "bạn có thể" },
            { "text": "放心", "type": "normal", "role": "Adv", "meaning": "yên tâm" },
            { "text": "交给她", "type": "normal", "role": "V_prep", "meaning": "giao cho cô ấy" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "王芳", "type": "subject", "desc": "Người được đánh giá" },
            { "role": "Trạng ngữ giới từ", "text": "对工作", "type": "prep", "desc": "Lĩnh vực được hướng tới" },
            { "role": "Vị ngữ tính từ", "text": "很负责", "type": "predicate", "desc": "Phó từ '很' + Tính từ '负责'" },
            { "role": "Vế đề xuất tin cậy", "text": "这个任务你可以放心交给她", "type": "predicate", "desc": "Kết luận cho sự tin tưởng" }
        ],
        "practice": {
            "type": "cloze",
            "blank_sentence": "王芳对工作很（ ____ ），这个任务你可以放心交给她。",
            "target_word": "负责",
            "options": [
                { "word": "负责", "pinyin": "fùzé", "hanviet": "Phụ Trách", "meaning": "có trách nhiệm, tận tâm" },
                { "word": "始终", "pinyin": "shǐzhōng", "hanviet": "Thủy Chung", "meaning": "luôn luôn" },
                { "word": "遵守", "pinyin": "zūnshǒu", "hanviet": "Tuân Thủ", "meaning": "chấp hành" },
                { "word": "替", "pinyin": "tì", "hanviet": "Thế", "meaning": "thay thế, giúp" }
            ],
            "clue": "Đứng sau phó từ mức độ '很', cần một tính từ miêu tả thái độ làm việc tốt để có thể 'yên tâm giao phó'."
        }
    },
    {
        "id": "hsk4_c1_50",
        "category": "cloze",
        "title": "有些司机不遵守交通规则",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第一部分 (选词填空 第50题)",
        "zh": "有些司机不遵守交通规则，这也是造成交通拥挤的一个原因。",
        "vietnamese": "Một số tài xế không tuân thủ luật giao thông, đây cũng là một nguyên nhân gây ra ùn tắc giao thông.",
        "grammar_point": {
            "name": "Cụm kết hợp cố định (Collocation): 遵守 + 规则 / 法律 / 纪律",
            "pattern": "Chủ ngữ + (不) + 遵守 + Quy định / Luật lệ",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI CỤM TỪ CỐ ĐỊNH: Trong tiếng Trung thi cử, danh từ '交通规则' (luật lệ giao thông) hoặc '规定' (quy định) luôn đi kèm với động từ '遵守' (tuân thủ). '造成' (gây nên) thường đi với hậu quả xấu như '交通拥挤' (kẹt xe), '麻烦' (phiền phức).",
            "explanation": "'遵守' là động từ hành động chuẩn mực. Cụm '这也是造成……的一个原因' là mẫu câu tổng kết kết quả phổ biến trong bài đọc hiểu HSK 4."
        },
        "tokens": [
            { "text": "有些", "type": "normal", "role": "Attr", "meaning": "một số" },
            { "text": "司机", "type": "core", "role": "S", "meaning": "tài xế, người lái xe" },
            { "text": "不", "type": "normal", "role": "Adv_neg", "meaning": "không" },
            { "text": "遵守", "type": "core", "role": "V", "meaning": "tuân thủ, chấp hành" },
            { "text": "交通规则", "type": "core", "role": "O", "meaning": "quy tắc giao thông, luật lệ" },
            { "text": "这也", "type": "normal", "role": "S2", "meaning": "điều này cũng" },
            { "text": "是", "type": "normal", "role": "V2", "meaning": "là" },
            { "text": "造成", "type": "core", "role": "V3", "meaning": "gây ra, tạo thành" },
            { "text": "交通拥挤", "type": "advanced", "role": "O3", "meaning": "ùn tắc giao thông" },
            { "text": "的一个原因", "type": "core", "role": "O2", "meaning": "một trong những nguyên nhân" }
        ],
        "breakdown": [
            { "role": "Chủ ngữ (S)", "text": "有些司机", "type": "subject", "desc": "Đối tượng gây ra tình trạng" },
            { "role": "Vị ngữ + Phủ định", "text": "不遵守", "type": "predicate", "desc": "Hành vi vi phạm: không tuân thủ" },
            { "role": "Tân ngữ luật lệ", "text": "交通规则", "type": "object", "desc": "Quy tắc bị vi phạm" },
            { "role": "Mệnh đề giải thích", "text": "这也是造成交通拥挤的一个原因", "type": "predicate", "desc": "Hậu quả dẫn đến kẹt xe" }
        ],
        "practice": {
            "type": "cloze",
            "blank_sentence": "有些司机不（ ____ ）交通规则，这也是造成交通拥挤的一个原因。",
            "target_word": "遵守",
            "options": [
                { "word": "遵守", "pinyin": "zūnshǒu", "hanviet": "Tuân Thủ", "meaning": "tuân thủ, chấp hành" },
                { "word": "负责", "pinyin": "fùzé", "hanviet": "Phụ Trách", "meaning": "có trách nhiệm" },
                { "word": "坚持", "pinyin": "jiānchí", "hanviet": "Kiên Trì", "meaning": "kiên trì" },
                { "word": "表达", "pinyin": "biǎodá", "hanviet": "Biểu Đạt", "meaning": "bày tỏ" }
            ],
            "clue": "Đứng trước danh từ '交通规则' (quy tắc giao thông), động từ kết hợp chuẩn xác nhất là '遵守'."
        }
    },
    {
        "id": "hsk4_c1_54",
        "category": "cloze",
        "title": "要想自由地用汉语表达情感",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第一部分 (选词填空 第54题)",
        "zh": "可要想自由地用汉语表达情感，还需要很长一段时间。",
        "vietnamese": "Nhưng muốn tự do dùng tiếng Hán để biểu đạt tình cảm, thì vẫn cần một khoảng thời gian rất dài nữa.",
        "grammar_point": {
            "name": "Cụm từ phối hợp: 表达 + 情感 / 观点 / 意见",
            "pattern": "自由地 + 用 + Ngôn ngữ + 表达 + Cảm xúc/Suy nghĩ",
            "level": "HSK 4 Cốt lõi",
            "trap_note": "BẪY THI PHÂN BIỆT: Phân biệt '表达' (biểu đạt, bộc lộ tình cảm/ý kiến ra bên ngoài bằng lời nói hoặc nét mặt) và '表示' (biểu thị, ra dấu hiệu hoặc thái độ). Đi cùng với '情感' (tình cảm, cảm xúc) thì bắt buộc phải dùng '表达'.",
            "explanation": "'自由地' mang trợ từ kết cấu '地' làm trạng ngữ cho động từ '表达'. '用汉语' là trạng ngữ chỉ công cụ phương tiện."
        },
        "tokens": [
            { "text": "可", "type": "normal", "role": "Conj", "meaning": "nhưng mà" },
            { "text": "要想", "type": "normal", "role": "V", "meaning": "muốn" },
            { "text": "自由地", "type": "core", "role": "Adv", "meaning": "một cách tự do" },
            { "text": "用汉语", "type": "normal", "role": "Prep_phrase", "meaning": "bằng tiếng Hán" },
            { "text": "表达", "type": "core", "role": "V", "meaning": "diễn đạt, bày tỏ" },
            { "text": "情感", "type": "core", "role": "O", "meaning": "tình cảm, cảm xúc" },
            { "text": "还", "type": "normal", "role": "Adv", "meaning": "vẫn" },
            { "text": "需要", "type": "normal", "role": "V2", "meaning": "cần" },
            { "text": "很长", "type": "normal", "role": "Attr", "meaning": "rất dài" },
            { "text": "一段时间", "type": "normal", "role": "Time", "meaning": "một khoảng thời gian" }
        ],
        "breakdown": [
            { "role": "Trạng ngữ cách thức", "text": "自由地", "type": "adv", "desc": "Tính từ + '地' bổ nghĩa cho hành động" },
            { "role": "Trạng ngữ công cụ", "text": "用汉语", "type": "prep", "desc": "Phương tiện ngôn ngữ được sử dụng" },
            { "role": "Vị ngữ động từ", "text": "表达", "type": "predicate", "desc": "Từ cần điền: truyền tải cảm xúc" },
            { "role": "Tân ngữ cảm xúc", "text": "情感", "type": "object", "desc": "Đối tượng được diễn đạt" }
        ],
        "practice": {
            "type": "cloze",
            "blank_sentence": "可要想自由地用汉语（ ____ ）情感，还需要很长一段时间。",
            "target_word": "表达",
            "options": [
                { "word": "表达", "pinyin": "biǎodá", "hanviet": "Biểu Đạt", "meaning": "diễn đạt, bày tỏ" },
                { "word": "以及", "pinyin": "yǐjí", "hanviet": "Dĩ Cập", "meaning": "cũng như, và" },
                { "word": "看不起", "pinyin": "kànbuqǐ", "hanviet": "Khán Bất Khởi", "meaning": "coi thường" },
                { "word": "说明书", "pinyin": "shuōmíngshū", "hanviet": "Thuyết Minh Thư", "meaning": "sách hướng dẫn" }
            ],
            "clue": "Đứng sau giới từ công cụ '用汉语' và đứng trước danh từ '情感', cần một động từ mang nghĩa diễn đạt tình cảm."
        }
    },

    # =========================================================================
    # PART D: 阅读 第三部分 - 篇章阅读 (Reading Passage Context Breakdown)
    # =========================================================================
    {
        "id": "hsk4_p1_66",
        "category": "paragraph",
        "title": "现代家庭的生活现状与反差",
        "source": "HSK 4 模拟试卷 1",
        "exam_part": "阅读 第三部分 (短文阅读 第66题)",
        "zh": "现在很多家庭夫妻都工作，不仅没有时间照顾父母，相反，大多数还要请父母帮忙照顾孩子，每天接送孩子上下学。",
        "vietnamese": "Hiện nay ở rất nhiều gia đình cả hai vợ chồng đều đi làm, không những không có thời gian chăm sóc bố mẹ, mà ngược lại, đa số còn phải nhờ bố mẹ hỗ trợ trông nom con cái, hàng ngày đưa đón con đi học.",
        "grammar_point": {
            "name": "Liên từ tương phản & nghịch lý: 相反 (Ngược lại / Trái lại)",
            "pattern": "Vế thực tế A + 不仅没有……，相反 (B: sự việc ngược lại hoàn toàn)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI ĐỌC HIỂU: Từ '相反' (xiāngfǎn) dùng để chuyển ý sang một tình huống hoàn toàn trái ngược với lẽ thường. Đề thi thường hỏi câu hỏi suy luận: Bố mẹ có con đi làm thì ai chăm sóc con cái? Người học phải chú ý câu sau chữ '相反' để chọn đáp án đúng ('由老人照顾').",
            "explanation": "Đoạn văn phản ánh chân thực nhịp sống đô thị hiện đại. '夫妻都工作' (hai vợ chồng đều đi làm), '不仅没有……' (không những không...), '相反' tạo nên bước ngoặt thông tin quan trọng nhất."
        },
        "tokens": [
            { "text": "现在", "type": "normal", "role": "Time", "meaning": "hiện nay" },
            { "text": "很多", "type": "normal", "role": "Attr", "meaning": "nhiều" },
            { "text": "家庭", "type": "core", "role": "Noun", "meaning": "gia đình" },
            { "text": "夫妻", "type": "core", "role": "S", "meaning": "vợ chồng" },
            { "text": "都", "type": "normal", "role": "Adv", "meaning": "đều" },
            { "text": "工作", "type": "normal", "role": "V", "meaning": "làm việc" },
            { "text": "不仅", "type": "grammar", "role": "Conj", "meaning": "không những" },
            { "text": "没有时间", "type": "normal", "role": "Predicate", "meaning": "không có thời gian" },
            { "text": "照顾", "type": "core", "role": "V", "meaning": "chăm sóc" },
            { "text": "父母", "type": "core", "role": "O", "meaning": "bố mẹ" },
            { "text": "相反", "type": "grammar", "role": "Conj", "meaning": "ngược lại, trái lại" },
            { "text": "大多数", "type": "core", "role": "S2", "meaning": "đại đa số" },
            { "text": "还要", "type": "normal", "role": "Adv", "meaning": "còn phải" },
            { "text": "请", "type": "normal", "role": "V_causative", "meaning": "nhờ, mời" },
            { "text": "帮忙", "type": "normal", "role": "V", "meaning": "giúp đỡ" },
            { "text": "孩子", "type": "normal", "role": "O2", "meaning": "con cái" },
            { "text": "每天", "type": "normal", "role": "Time", "meaning": "mỗi ngày" },
            { "text": "接送", "type": "core", "role": "V_compound", "meaning": "đưa đón" }
        ],
        "breakdown": [
            { "role": "Bối cảnh xã hội", "text": "现在很多家庭夫妻都工作", "type": "subject", "desc": "Cả vợ và chồng đều tham gia lao động" },
            { "role": "Hạn chế thực tế", "text": "不仅没有时间照顾父母", "type": "predicate", "desc": "Không thể phụng dưỡng chăm nom cha mẹ" },
            { "role": "Nghịch lý đảo ngược", "text": "相反，大多数还要请父母帮忙照顾孩子", "type": "conj", "desc": "Điểm chốt: nhờ cậy lại thế hệ ông bà" },
            { "role": "Công việc thường nhật", "text": "每天接送孩子上下学", "type": "predicate", "desc": "Đưa đón con đi học hàng ngày" }
        ],
        "practice": {
            "type": "cloze",
            "blank_sentence": "不仅没有时间照顾父母，（ ____ ），大多数还要请父母帮忙照顾孩子。",
            "target_word": "相反",
            "options": [
                { "word": "相反", "pinyin": "xiāngfǎn", "hanviet": "Tương Phản", "meaning": "ngược lại, trái lại" },
                { "word": "随着", "pinyin": "suízhe", "hanviet": "Tùy Trứ", "meaning": "cùng với" },
                { "word": "即使", "pinyin": "jíshǐ", "hanviet": "Tức Sử", "meaning": "cho dù" },
                { "word": "因此", "pinyin": "yīncǐ", "hanviet": "Nhân Thử", "meaning": "do đó" }
            ],
            "clue": "Vế trước không chăm sóc được cha mẹ, vế sau lại nhờ cha mẹ chăm sóc con. Mối quan hệ tương phản đối lập cần liên từ '相反'."
        }
    },
    {
        "id": "hsk4_p2_78",
        "category": "paragraph",
        "title": "Hiếu thuận cha mẹ và cách đối nhân xử thế",
        "source": "HSK 4 模拟试卷 2",
        "exam_part": "阅读 第三部分 (短文阅读 第78题)",
        "zh": "一个孝顺父母的人，一定值得别人尊重。一个连自己的父母都不尊敬的人，又怎么能真正地对别人好呢？",
        "vietnamese": "Một người hiếu thảo với cha mẹ, nhất định xứng đáng nhận được sự tôn trọng của người khác. Một người mà ngay cả cha mẹ của mình cũng không tôn kính, thì làm sao có thể thực lòng đối xử tốt với người khác được?",
        "grammar_point": {
            "name": "Cấu trúc nhấn mạnh kết hợp phản vấn: 连……都……，又怎么能……呢？",
            "pattern": "连 + Đối tượng tối thiểu + 都/也 + Phủ định -> 又 + 怎么能 + V + 呢？",
            "level": "HSK 4 Đỉnh cao ngữ pháp",
            "trap_note": "BẪY THI PHẢN VẤN: '又怎么能……呢？' là câu hỏi tu từ (phản vấn), hình thức tuy là câu hỏi nhưng mang nội dung khẳng định mạnh mẽ phủ định tuyệt đối: 'chắc chắn không bao giờ có thể đối xử tốt với người khác được!'. Người làm bài thi đọc hiểu HSK 4 không được hiểu lầm thành người nói đang thắc mắc.",
            "explanation": "Cấu trúc '连……都……' đặt đối tượng thiêng liêng nhất là cha mẹ lên bàn cân để chứng minh rằng nếu việc cơ bản nhất không làm được thì không thể kỳ vọng việc cao xa hơn."
        },
        "tokens": [
            { "text": "一个", "type": "normal", "role": "Attr", "meaning": "một" },
            { "text": "孝顺", "type": "advanced", "role": "Adj_V", "meaning": "hiếu thảo, hiếu thuận" },
            { "text": "父母", "type": "core", "role": "O_attr", "meaning": "cha mẹ" },
            { "text": "的人", "type": "normal", "role": "S", "meaning": "người..." },
            { "text": "一定", "type": "core", "role": "Adv", "meaning": "nhất định" },
            { "text": "值得", "type": "core", "role": "V", "meaning": "xứng đáng" },
            { "text": "别人", "type": "core", "role": "Noun", "meaning": "người khác" },
            { "text": "尊重", "type": "core", "role": "V2", "meaning": "tôn trọng" },
            { "text": "连", "type": "grammar", "role": "Prep", "meaning": "ngay cả, đến cả (cấu trúc 连)" },
            { "text": "自己的", "type": "normal", "role": "Attr", "meaning": "của chính mình" },
            { "text": "都", "type": "grammar", "role": "Adv", "meaning": "cũng, đều" },
            { "text": "不尊敬", "type": "core", "role": "Predicate", "meaning": "không tôn kính" },
            { "text": "又", "type": "grammar", "role": "Adv", "meaning": "lại (tăng cường ngữ khí)" },
            { "text": "怎么能", "type": "grammar", "role": "Modal", "meaning": "làm sao có thể (câu hỏi tu từ)" },
            { "text": "真正地", "type": "core", "role": "Adv", "meaning": "một cách chân chính" },
            { "text": "对别人好", "type": "normal", "role": "Predicate", "meaning": "đối tốt với người khác" },
            { "text": "呢", "type": "grammar", "role": "Part", "meaning": "sao, ư (trợ từ phản vấn)" }
        ],
        "breakdown": [
            { "role": "Mệnh đề khẳng định", "text": "一个孝顺父母的人，一定值得别人尊重", "type": "subject", "desc": "Người hiếu thuận ắt được nể trọng" },
            { "role": "Cấu trúc 连……都", "text": "一个连自己的父母都不尊敬的人", "type": "prep", "desc": "Đưa ra giới hạn đạo đức tối thiểu" },
            { "role": "Câu hỏi phản vấn", "text": "又怎么能真正地对别人好呢？", "type": "predicate", "desc": "Khẳng định tuyệt đối: không thể đối xử tốt với ai" }
        ],
        "practice": {
            "type": "cloze",
            "blank_sentence": "一个（ ____ ）自己的父母都不尊敬的人，又怎么能真正地对别人好呢？",
            "target_word": "连",
            "options": [
                { "word": "连", "pinyin": "lián", "hanviet": "Liên", "meaning": "ngay cả, đến cả" },
                { "word": "把", "pinyin": "bǎ", "hanviet": "Bả", "meaning": "đem" },
                { "word": "被", "pinyin": "bèi", "hanviet": "Bị", "meaning": "bị" },
                { "word": "向", "pinyin": "xiàng", "hanviet": "Hướng", "meaning": "về phía" }
            ],
            "clue": "Đi cùng với từ '都' phía sau ('都不尊敬') để nhấn mạnh mức độ cực đoan, chọn từ '连'."
        }
    }
]

def enrich_entry(entry):
    # Full pinyin and hanviet
    zh_text = entry["zh"]
    if "pinyin" not in entry or not entry["pinyin"]:
        entry["pinyin"] = get_pinyin_str(zh_text)
    if "hanviet" not in entry or not entry["hanviet"]:
        entry["hanviet"] = get_hanviet(zh_text)
        
    # Enrich tokens
    for token in entry.get("tokens", []):
        t_text = token["text"]
        if "pinyin" not in token or not token["pinyin"]:
            token["pinyin"] = get_pinyin_str(t_text)
        if "hanviet" not in token or not token["hanviet"]:
            token["hanviet"] = get_hanviet(t_text)
            
        # Match HSK vocab
        if t_text in HSK_VOCAB:
            v_info = HSK_VOCAB[t_text]
            if not token.get("meaning"):
                token["meaning"] = v_info["meaning"]
            if token.get("type") not in ["grammar", "advanced"]:
                token["type"] = "core" if v_info["level"] == "hsk4" else "normal"
                
    return entry

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    enriched = [enrich_entry(e) for e in RAW_ENTRIES]
    
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated {len(enriched)} reading analysis items in {OUT_FILE}")

if __name__ == "__main__":
    main()
