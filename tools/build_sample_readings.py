#!/usr/bin/env python3
"""
tools/build_sample_readings.py
Generates the 3 sample HSK1 Graded Reading stories with strict vocabulary mapping.
Every word_id is directly derived from the database vocabs.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
OUTPUT_DIR = REPO_ROOT / "database" / "readings" / "hsk1"

# Load vocabulary lookups from database
VOCAB_BY_HANZI = {}
VOCAB_BY_ID = {}

for lvl in range(1, 7):
    path = VOCAB_DIR / f"hsk{lvl}_vocabularies.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            for item in json.load(f):
                wid = f"hsk{lvl}_{item['id']}"
                data = {
                    "text": item["hanzi"],
                    "pinyin": item.get("pinyin", ""),
                    "hanviet": item.get("hanviet", "").lower(),
                    "meaning_vi": item.get("meaning", ""),
                    "hsk": lvl,
                    "word_id": wid
                }
                if item["hanzi"] not in VOCAB_BY_HANZI:
                    VOCAB_BY_HANZI[item["hanzi"]] = data
                VOCAB_BY_ID[wid] = data

# Handle special classifiers / multi-meaning entries in HSK3
if "只（量词）" in VOCAB_BY_HANZI:
    VOCAB_BY_HANZI["只_classifier"] = {
        "text": "只",
        "pinyin": "zhī",
        "hanviet": "chích",
        "meaning_vi": "con (lượng từ chỉ động vật)",
        "hsk": 3,
        "word_id": VOCAB_BY_HANZI["只（量词）"]["word_id"]
    }
if "只（副词）" in VOCAB_BY_HANZI:
    VOCAB_BY_HANZI["只_adverb"] = {
        "text": "只",
        "pinyin": "zhǐ",
        "hanviet": "chỉ",
        "meaning_vi": "chỉ, chỉ có",
        "hsk": 3,
        "word_id": VOCAB_BY_HANZI["只（副词）"]["word_id"]
    }

def get_token(key):
    if key in [",", "。", "，", "？", "！", "：", "“", "”", "、"]:
        return {"text": key}
    if key == "小白":
        # Proper noun (character name)
        return {
            "text": "小白",
            "pinyin": "Xiǎobái",
            "hanviet": "tiểu bạch",
            "meaning_vi": "Tiểu Bạch (tên chú mèo)",
            "is_name": True
        }
    if key in VOCAB_BY_HANZI:
        return dict(VOCAB_BY_HANZI[key])
    raise ValueError(f"Unknown vocabulary key: {key}")

def get_spotlight(hanzi):
    if hanzi in VOCAB_BY_HANZI:
        return VOCAB_BY_HANZI[hanzi]["word_id"]
    raise ValueError(f"Unknown spotlight word: {hanzi}")

# ==============================================================================
# Story 1: 我的一天 (Một ngày của tôi)
# ==============================================================================
story_1 = {
    "id": "hsk1_story_001",
    "level": "HSK1",
    "title": {
        "zh": "我的一天",
        "vi": "Một ngày của tôi"
    },
    "topic": "daily_life",
    "estimatedMinutes": 3,
    "description_vi": "Một câu chuyện ngắn về lịch sinh hoạt và học tập hằng ngày.",
    "sentences": [
        {
            "id": "s1",
            "zh": "今天天气很好。",
            "pinyin": "Jīntiān tiānqì hěn hǎo.",
            "vi": "Hôm nay thời tiết rất đẹp.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("今天"),
                get_token("天气"),
                get_token("很"),
                get_token("好"),
                get_token("。")
            ]
        },
        {
            "id": "s2",
            "zh": "我上午八点去学校。",
            "pinyin": "Wǒ shàngwǔ bā diǎn qù xuéxiào.",
            "vi": "Buổi sáng tám giờ tôi đi đến trường học.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("我"),
                get_token("上午"),
                get_token("八"),
                get_token("点"),
                get_token("去"),
                get_token("学校"),
                get_token("。")
            ]
        },
        {
            "id": "s3",
            "zh": "我和朋友看书，学习汉语。",
            "pinyin": "Wǒ hé péngyou kàn shū, xuéxí Hànyǔ.",
            "vi": "Tôi và bạn bè đọc sách, học tiếng Hán.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("我"),
                get_token("和"),
                get_token("朋友"),
                get_token("看"),
                get_token("书"),
                get_token("，"),
                get_token("学习"),
                get_token("汉语"),
                get_token("。")
            ]
        },
        {
            "id": "s4",
            "zh": "中午我们在饭店吃中国菜。",
            "pinyin": "Zhōngwǔ wǒmen zài fàndiàn chī Zhōngguó cài.",
            "vi": "Buổi trưa chúng tôi ăn món Trung Quốc ở quán ăn.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("中午"),
                get_token("我们"),
                get_token("在"),
                get_token("饭店"),
                get_token("吃"),
                get_token("中国"),
                get_token("菜"),
                get_token("。")
            ]
        },
        {
            "id": "s5",
            "zh": "下午三点我想回家喝茶。",
            "pinyin": "Xiàwǔ sān diǎn wǒ xiǎng huí jiā hē chá.",
            "vi": "Ba giờ chiều tôi muốn về nhà uống trà.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("下午"),
                get_token("三"),
                get_token("点"),
                get_token("我"),
                get_token("想"),
                get_token("回"),
                get_token("家"),
                get_token("喝"),
                get_token("茶"),
                get_token("。")
            ]
        },
        {
            "id": "s6",
            "zh": "爸爸妈妈都在家看电视。",
            "pinyin": "Bàba māma dōu zài jiā kàn diànshì.",
            "vi": "Bố mẹ đều ở nhà xem tivi.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("爸爸"),
                get_token("妈妈"),
                get_token("都"),
                get_token("在"),
                get_token("家"),
                get_token("看"),
                get_token("电视"),
                get_token("。")
            ]
        },
        {
            "id": "s7",
            "zh": "今天我很高兴。",
            "pinyin": "Jīntiān wǒ hěn gāoxìng.",
            "vi": "Hôm nay tôi rất vui vẻ.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("今天"),
                get_token("我"),
                get_token("很"),
                get_token("高兴"),
                get_token("。")
            ]
        }
    ],
    "vocabulary_spotlight": [
        get_spotlight("今天"),
        get_spotlight("天气"),
        get_spotlight("学校"),
        get_spotlight("朋友"),
        get_spotlight("饭店"),
        get_spotlight("电视"),
        get_spotlight("高兴")
    ],
    "quiz": [
        {
            "id": "q1",
            "question_vi": "Nhân vật đi đến trường học vào lúc mấy giờ?",
            "options_vi": ["7 giờ sáng", "8 giờ sáng", "9 giờ sáng"],
            "answer": 1,
            "explanation_vi": "Trong câu 2 nêu rõ: 我上午八点去学校 (Buổi sáng 8 giờ tôi đi đến trường học)."
        },
        {
            "id": "q2",
            "question_vi": "Buổi trưa nhân vật và bạn bè ăn món gì ở đâu?",
            "options_vi": ["Ăn món Trung Quốc ở nhà", "Ăn cơm ở trường học", "Ăn món Trung Quốc ở quán ăn"],
            "answer": 2,
            "explanation_vi": "Trong câu 4: 中午我们在饭店吃中国菜 (Buổi trưa chúng tôi ăn món Trung Quốc ở quán ăn)."
        },
        {
            "id": "q3",
            "question_vi": "Bố mẹ đang làm gì ở nhà?",
            "options_vi": ["Xem tivi", "Đọc sách", "Uống trà"],
            "answer": 0,
            "explanation_vi": "Trong câu 6: 爸爸妈妈都在家看电视 (Bố mẹ đều ở nhà xem tivi)."
        }
    ]
}

# ==============================================================================
# Story 2: 我的猫叫小白 (Con mèo của tôi tên Tiểu Bạch)
# ==============================================================================
story_2 = {
    "id": "hsk1_story_002",
    "level": "HSK1",
    "title": {
        "zh": "我的猫叫小白",
        "vi": "Con mèo của tôi tên Tiểu Bạch"
    },
    "topic": "pets_family",
    "estimatedMinutes": 3,
    "description_vi": "Câu chuyện đáng yêu về chú mèo nhỏ trong gia đình.",
    "sentences": [
        {
            "id": "s1",
            "zh": "我家有一只猫，它叫小白。",
            "pinyin": "Wǒ jiā yǒu yī zhī māo, tā jiào Xiǎobái.",
            "vi": "Nhà tôi có một con mèo, nó tên là Tiểu Bạch.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("我"),
                get_token("家"),
                get_token("有"),
                get_token("一"),
                get_token("只_classifier"),
                get_token("猫"),
                get_token("，"),
                get_token("它"),
                get_token("叫"),
                get_token("小白"),
                get_token("。")
            ]
        },
        {
            "id": "s2",
            "zh": "小白很小，也很漂亮。",
            "pinyin": "Xiǎobái hěn xiǎo, yě hěn piàoliang.",
            "vi": "Tiểu Bạch rất nhỏ, và cũng rất đẹp.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("小白"),
                get_token("很"),
                get_token("小"),
                get_token("，"),
                get_token("也"),
                get_token("很"),
                get_token("漂亮"),
                get_token("。")
            ]
        },
        {
            "id": "s3",
            "zh": "它喜欢在椅子上睡觉。",
            "pinyin": "Tā xǐhuan zài yǐzi shang shuìjiào.",
            "vi": "Nó thích ngủ ở trên ghế.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("它"),
                get_token("喜欢"),
                get_token("在"),
                get_token("椅子"),
                get_token("上"),
                get_token("睡觉"),
                get_token("。")
            ]
        },
        {
            "id": "s4",
            "zh": "今天小白不吃东西，只喝水。",
            "pinyin": "Jīntiān Xiǎobái bù chī dōngxi, zhǐ hē shuǐ.",
            "vi": "Hôm nay Tiểu Bạch không ăn đồ ăn, chỉ uống nước.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("今天"),
                get_token("小白"),
                get_token("不"),
                get_token("吃"),
                get_token("东西"),
                get_token("，"),
                get_token("只_adverb"),
                get_token("喝"),
                get_token("水"),
                get_token("。")
            ]
        },
        {
            "id": "s5",
            "zh": "我问它：“你怎么了？”",
            "pinyin": "Wǒ wèn tā: “Nǐ zěnme le?”",
            "vi": "Tôi hỏi nó: “Mày làm sao thế?”",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("我"),
                get_token("问"),
                get_token("它"),
                get_token("："),
                get_token("“"),
                get_token("你"),
                get_token("怎么"),
                get_token("了"),
                get_token("？"),
                get_token("”")
            ]
        },
        {
            "id": "s6",
            "zh": "下午小白看见一只小狗，它很高兴。",
            "pinyin": "Xiàwǔ Xiǎobái kànjiàn yī zhī xiǎo gǒu, tā hěn gāoxìng.",
            "vi": "Buổi chiều Tiểu Bạch nhìn thấy một chú chó con, nó rất vui vẻ.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("下午"),
                get_token("小白"),
                get_token("看见"),
                get_token("一"),
                get_token("只_classifier"),
                get_token("小"),
                get_token("狗"),
                get_token("，"),
                get_token("它"),
                get_token("很"),
                get_token("高兴"),
                get_token("。")
            ]
        }
    ],
    "vocabulary_spotlight": [
        get_spotlight("猫"),
        get_spotlight("小"),
        get_spotlight("漂亮"),
        get_spotlight("喜欢"),
        get_spotlight("椅子"),
        get_spotlight("睡觉"),
        get_spotlight("看见"),
        get_spotlight("狗")
    ],
    "quiz": [
        {
            "id": "q1",
            "question_vi": "Con mèo của nhân vật thích làm gì?",
            "options_vi": ["Ngủ ở trên ghế", "Chạy ngoài sân", "Uống trà"],
            "answer": 0,
            "explanation_vi": "Trong câu 3: 它喜欢在椅子上睡觉 (Nó thích ngủ ở trên ghế)."
        },
        {
            "id": "q2",
            "question_vi": "Hôm nay chú mèo Tiểu Bạch ăn uống thế nào?",
            "options_vi": ["Ăn rất nhiều đồ ăn", "Không ăn đồ ăn, chỉ uống nước", "Không uống nước"],
            "answer": 1,
            "explanation_vi": "Trong câu 4: 今天小白不吃东西，只喝水 (Hôm nay Tiểu Bạch không ăn đồ ăn, chỉ uống nước)."
        },
        {
            "id": "q3",
            "question_vi": "Buổi chiều khi nhìn thấy chú chó con, Tiểu Bạch cảm thấy thế nào?",
            "options_vi": ["Sợ hãi", "Buồn bã", "Rất vui vẻ"],
            "answer": 2,
            "explanation_vi": "Trong câu 6: 下午小白看见一只小狗，它很高兴 (Buổi chiều nhìn thấy một chú chó con, nó rất vui vẻ)."
        }
    ]
}

# ==============================================================================
# Story 3: 去商店买水果 (Đi cửa hàng mua hoa quả)
# ==============================================================================
story_3 = {
    "id": "hsk1_story_003",
    "level": "HSK1",
    "title": {
        "zh": "去商店买水果",
        "vi": "Đi cửa hàng mua hoa quả"
    },
    "topic": "shopping",
    "estimatedMinutes": 3,
    "description_vi": "Tập giao tiếp hỏi giá và mua hoa quả ở cửa hàng.",
    "sentences": [
        {
            "id": "s1",
            "zh": "今天下午我和朋友去商店。",
            "pinyin": "Jīntiān xiàwǔ wǒ hé péngyou qù shāngdiàn.",
            "vi": "Chiều hôm nay tôi và bạn bè đi đến cửa hàng.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("今天"),
                get_token("下午"),
                get_token("我"),
                get_token("和"),
                get_token("朋友"),
                get_token("去"),
                get_token("商店"),
                get_token("。")
            ]
        },
        {
            "id": "s2",
            "zh": "这个商店很大，商店里有很多东西。",
            "pinyin": "Zhè ge shāngdiàn hěn dà, shāngdiàn lǐ yǒu hěn duō dōngxi.",
            "vi": "Cửa hàng này rất to, trong cửa hàng có rất nhiều đồ.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("这"),
                get_token("个"),
                get_token("商店"),
                get_token("很"),
                get_token("大"),
                get_token("，"),
                get_token("商店"),
                get_token("里"),
                get_token("有"),
                get_token("很"),
                get_token("多"),
                get_token("东西"),
                get_token("。")
            ]
        },
        {
            "id": "s3",
            "zh": "我想买一些苹果。",
            "pinyin": "Wǒ xiǎng mǎi yī xiē píngguǒ.",
            "vi": "Tôi muốn mua một ít táo.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("我"),
                get_token("想"),
                get_token("买"),
                get_token("一"),
                get_token("些"),
                get_token("苹果"),
                get_token("。")
            ]
        },
        {
            "id": "s4",
            "zh": "我问：“请问，苹果多少钱？”",
            "pinyin": "Wǒ wèn: “Qǐng wèn, píngguǒ duōshao qián?”",
            "vi": "Tôi hỏi: “Xin hỏi, táo bao nhiêu tiền?”",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("我"),
                get_token("问"),
                get_token("："),
                get_token("“"),
                get_token("请"),
                get_token("问"),
                get_token("，"),
                get_token("苹果"),
                get_token("多少"),
                get_token("钱"),
                get_token("？"),
                get_token("”")
            ]
        },
        {
            "id": "s5",
            "zh": "服务员说：“三块钱一个。”",
            "pinyin": "Fúwùyuán shuō: “Sān kuài qián yī ge.”",
            "vi": "Người phục vụ nói: “Ba đồng một quả.”",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("服务员"),
                get_token("说"),
                get_token("："),
                get_token("“"),
                get_token("三"),
                get_token("块"),
                get_token("钱"),
                get_token("一"),
                get_token("个"),
                get_token("。"),
                get_token("”")
            ]
        },
        {
            "id": "s6",
            "zh": "我们买了六个苹果，太好吃了。",
            "pinyin": "Wǒmen mǎi le liù ge píngguǒ, tài hǎochī le.",
            "vi": "Chúng tôi đã mua sáu quả táo, ngon quá.",
            "audio_start_ms": None,
            "audio_end_ms": None,
            "tokens": [
                get_token("我们"),
                get_token("买"),
                get_token("了"),
                get_token("六"),
                get_token("个"),
                get_token("苹果"),
                get_token("，"),
                get_token("太"),
                get_token("好吃"),
                get_token("了"),
                get_token("。")
            ]
        }
    ],
    "vocabulary_spotlight": [
        get_spotlight("商店"),
        get_spotlight("大"),
        get_spotlight("东西"),
        get_spotlight("买"),
        get_spotlight("苹果"),
        get_spotlight("多少"),
        get_spotlight("钱"),
        get_spotlight("块")
    ],
    "quiz": [
        {
            "id": "q1",
            "question_vi": "Nhân vật muốn mua thứ gì ở cửa hàng?",
            "options_vi": ["Trà", "Táo", "Sách"],
            "answer": 1,
            "explanation_vi": "Trong câu 3: 我想买一些苹果 (Tôi muốn mua một ít táo)."
        },
        {
            "id": "q2",
            "question_vi": "Giá của một quả táo là bao nhiêu?",
            "options_vi": ["Hai đồng", "Ba đồng", "Sáu đồng"],
            "answer": 1,
            "explanation_vi": "Trong câu 5: 服务员说：“三块钱一个。” (Người phục vụ nói: 'Ba đồng một quả')."
        },
        {
            "id": "q3",
            "question_vi": "Họ đã mua tổng cộng bao nhiêu quả táo?",
            "options_vi": ["3 quả", "4 quả", "6 quả"],
            "answer": 2,
            "explanation_vi": "Trong câu 6: 我们买了六个苹果 (Chúng tôi đã mua sáu quả táo)."
        }
    ]
}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

stories = [story_1, story_2, story_3]
for s in stories:
    file_path = OUTPUT_DIR / f"{s['id']}.json"
    file_path.write_text(json.dumps(s, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[✓] Saved {file_path.name} ({len(s['sentences'])} sentences, {len(s['vocabulary_spotlight'])} spotlight words)")

print("\n[*] Sample readings created successfully.")
