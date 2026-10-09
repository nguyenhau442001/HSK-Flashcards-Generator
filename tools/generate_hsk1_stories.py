#!/usr/bin/env python3
"""
tools/generate_hsk1_stories.py
Generates and refines HSK1 stories 004 to 010 and updates manifest.json.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_DIR = REPO_ROOT / "database" / "vocabs"
READINGS_DIR = REPO_ROOT / "database" / "readings"

# 1. Load vocabulary database
VOCAB_MAP = {}
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
                        "hanviet": item["hanviet"],
                        "meaning_vi": item["meaning"],
                        "hsk": lvl,
                        "word_id": f"hsk{lvl}_{item['id']}"
                    }

PUNCTUATION = set("，。？！、：；“”‘’（）…— ")

def tokenize_sentence(zh_text, custom_names=None):
    custom_names = custom_names or {}
    tokens = []
    i = 0
    while i < len(zh_text):
        ch = zh_text[i]
        if ch in PUNCTUATION:
            if ch != " ":
                tokens.append({"text": ch})
            i += 1
            continue

        matched_name = False
        for name, meta in custom_names.items():
            if zh_text[i:].startswith(name):
                tok = {"text": name, "is_name": True}
                tok.update(meta)
                tokens.append(tok)
                i += len(name)
                matched_name = True
                break
        if matched_name:
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
            print(f"[!] Warning: Token not found for '{ch}' in '{zh_text}'")
            tokens.append({"text": ch, "unknown": True})
            i += 1

    return tokens

# Stories data definition for HSK1 stories 004 to 010
STORIES_HSK1 = [
    {
        "id": "hsk1_story_004",
        "level": "HSK1",
        "title": {
            "zh": "在学校学习汉语",
            "vi": "Học tiếng Hán ở trường học"
        },
        "topic": "school_study",
        "topic_vi": "Học tập & Trường học",
        "icon": "🏫",
        "estimatedMinutes": 3,
        "description_vi": "Lớp học tiếng Hán vui vẻ với cô giáo Vương và các bạn học.",
        "custom_names": {
            "王老师": {"pinyin": "Wáng lǎoshī", "hanviet": "Vương lão sư", "meaning_vi": "cô giáo Vương"}
        },
        "sentences": [
            ("王老师是我们的汉语老师。", "Wáng lǎoshī shì wǒmen de hànyǔ lǎoshī.", "Cô giáo Vương là giáo viên tiếng Hán của chúng tôi."),
            ("她三十岁，人很好。", "Tā sānshí suì, rén hěn hǎo.", "Cô ba mươi tuổi, tính tình rất tốt."),
            ("学校里有很多学生。", "Xuéxiào lǐ yǒu hěn duō xuésheng.", "Trong trường học có rất nhiều học sinh."),
            ("我们在学校看书，写字。", "Wǒmen zài xuéxiào kàn shū, xiě zì.", "Chúng tôi đọc sách và viết chữ ở trường học."),
            ("学生们都很喜欢王老师。", "Xuéshengmen dōu hěn xǐhuan Wáng lǎoshī.", "Các bạn học sinh đều rất thích cô giáo Vương.")
        ],
        "spotlight": ["老师", "汉语", "学生", "看", "写", "字", "喜欢", "学校"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Cô giáo Vương dạy môn gì?",
                "options_vi": ["Tiếng Hán", "Tiếng Anh", "Toán học"],
                "answer": 0,
                "explanation_vi": "Trong bài có câu: 王老师是我们的汉语老师 (Cô Vương là giáo viên tiếng Hán của chúng tôi)."
            },
            {
                "id": "q2",
                "question_vi": "Cô giáo Vương bao nhiêu tuổi?",
                "options_vi": ["20 tuổi", "30 tuổi", "40 tuổi"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 她三十岁 (Cô ấy ba mươi tuổi)."
            },
            {
                "id": "q3",
                "question_vi": "Các bạn học sinh làm gì ở trường học?",
                "options_vi": ["Đi mua đồ", "Đọc sách và viết chữ", "Xem tivi"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 我们在学校看书，写字 (Chúng tôi ở trường học đọc sách, viết chữ)."
            }
        ]
    },
    {
        "id": "hsk1_story_005",
        "level": "HSK1",
        "title": {
            "zh": "去朋友家做客",
            "vi": "Đến nhà bạn làm khách"
        },
        "topic": "social_life",
        "topic_vi": "Bạn bè & Đời sống",
        "icon": "🍵",
        "estimatedMinutes": 3,
        "description_vi": "Đến thăm nhà bạn Đại Vệ vào buổi chiều, cùng uống trà và trò chuyện.",
        "custom_names": {
            "大卫": {"pinyin": "Dàwèi", "hanviet": "Đại Vệ", "meaning_vi": "Đại Vệ (David)"}
        },
        "sentences": [
            ("昨天下午我去大卫家。", "Zuótiān xiàwǔ wǒ qù Dàwèi jiā.", "Chiều hôm qua tôi đến nhà Đại Vệ."),
            ("大卫的家不大，也很漂亮。", "Dàwèi de jiā bú dà, yě hěn piàoliang.", "Nhà của Đại Vệ không lớn, cũng rất đẹp."),
            ("大卫请我喝中国茶。", "Dàwèi qǐng wǒ hē zhōngguó chá.", "Đại Vệ mời tôi uống trà Trung Quốc."),
            ("中国茶很好，我们都很高兴。", "Zhōngguó chá hěn hǎo, wǒmen dōu hěn gāoxìng.", "Trà Trung Quốc rất ngon, chúng tôi đều rất vui vẻ."),
            ("晚上七点我坐出租车回家。", "Wǎnshang qī diǎn wǒ zuò chūzūchē huí jiā.", "Bảy giờ tối tôi đi taxi về nhà.")
        ],
        "spotlight": ["昨天", "下午", "漂亮", "请", "喝", "茶", "高兴", "出租车"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nhân vật chính đến nhà ai vào chiều hôm qua?",
                "options_vi": ["Nhà cô giáo Vương", "Nhà Đại Vệ", "Nhà bác sĩ"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 昨天下午我去大卫家 (Chiều hôm qua tôi đến nhà Đại Vệ)."
            },
            {
                "id": "q2",
                "question_vi": "Đại Vệ đã mời bạn uống gì?",
                "options_vi": ["Nước lọc", "Cà phê", "Trà Trung Quốc"],
                "answer": 2,
                "explanation_vi": "Trong bài có câu: 大卫请我喝中国茶 (Đại Vệ mời tôi uống trà Trung Quốc)."
            },
            {
                "id": "q3",
                "question_vi": "Nhân vật chính về nhà bằng phương tiện gì lúc 7 giờ tối?",
                "options_vi": ["Đi bộ", "Đi xe taxi", "Đi máy bay"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 晚上七点我坐出租车回家 (Bảy giờ tối tôi đi taxi về nhà)."
            }
        ]
    },
    {
        "id": "hsk1_story_006",
        "level": "HSK1",
        "title": {
            "zh": "我的好朋友李月",
            "vi": "Người bạn tốt Lý Nguyệt của tôi"
        },
        "topic": "people_friends",
        "topic_vi": "Con người & Tình bạn",
        "icon": "👧",
        "estimatedMinutes": 3,
        "description_vi": "Giới thiệu về người bạn thân người Bắc Kinh cùng trường học.",
        "custom_names": {
            "李月": {"pinyin": "Lǐ Yuè", "hanviet": "Lý Nguyệt", "meaning_vi": "Lý Nguyệt"}
        },
        "sentences": [
            ("李月是我的中国朋友。", "Lǐ Yuè shì wǒ de zhōngguó péngyou.", "Lý Nguyệt là người bạn Trung Quốc của tôi."),
            ("她是北京人，在北京学习汉语。", "Tā shì Běijīng rén, zài Běijīng xuéxí hànyǔ.", "Cô ấy là người Bắc Kinh, học tiếng Hán ở Bắc Kinh."),
            ("李月喜欢看电影和看书。", "Lǐ Yuè xǐhuan kàn diànyǐng hé kàn shū.", "Lý Nguyệt thích xem phim điện ảnh và đọc sách."),
            ("她的汉语很好，帮助我学习。", "Tā de hànyǔ hěn hǎo, bāngzhù wǒ xuéxí.", "Tiếng Hán của cô ấy rất giỏi, giúp đỡ tôi học tập."),
            ("我们是好朋友，天天在一起。", "Wǒmen shì hǎo péngyou, tiāntiān zài yìqǐ.", "Chúng tôi là bạn tốt, ngày nào cũng ở bên nhau.")
        ],
        "spotlight": ["朋友", "中国", "北京", "电影", "看", "学习", "好", "喜欢"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Lý Nguyệt là người ở đâu?",
                "options_vi": ["Thượng Hải", "Bắc Kinh", "Hà Nội"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 她是北京人 (Cô ấy là người Bắc Kinh)."
            },
            {
                "id": "q2",
                "question_vi": "Lý Nguyệt có sở thích gì?",
                "options_vi": ["Xem phim và đọc sách", "Nấu ăn và đi ngủ", "Mua sắm quần áo"],
                "answer": 0,
                "explanation_vi": "Trong bài có câu: 李月喜欢看电影和看书 (Lý Nguyệt thích xem phim và đọc sách)."
            },
            {
                "id": "q3",
                "question_vi": "Lý Nguyệt giúp đỡ nhân vật chính việc gì?",
                "options_vi": ["Nấu cơm", "Học tập tiếng Hán", "Đi chợ"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 帮助我学习 (Giúp đỡ tôi học tập)."
            }
        ]
    },
    {
        "id": "hsk1_story_007",
        "level": "HSK1",
        "title": {
            "zh": "在饭馆吃中国菜",
            "vi": "Ăn món Trung Quốc ở nhà hàng"
        },
        "topic": "food_dining",
        "topic_vi": "Ẩm thực & Nhà hàng",
        "icon": "🍜",
        "estimatedMinutes": 3,
        "description_vi": "Bữa trưa ngon miệng tại một nhà hàng Trung Quốc cùng bạn bè.",
        "sentences": [
            ("今天中午我们去饭馆吃中国菜。", "Jīntiān zhōngwǔ wǒmen qù fànguǎn chī zhōngguó cài.", "Trưa hôm nay chúng tôi đến nhà hàng ăn món Trung Quốc."),
            ("服务员请我们坐下。", "Fúwùyuán qǐng wǒmen zuò xià.", "Nhân viên phục vụ mời chúng tôi ngồi xuống."),
            ("我们点了很多中国菜和米饭。", "Wǒmen diǎn le hěn duō zhōngguó cài hé mǐfàn.", "Chúng tôi gọi rất nhiều món ăn Trung Quốc và cơm trắng."),
            ("中国菜太好了，很好吃。", "Zhōngguó cài tài hǎo le, hěn hǎochī.", "Món ăn Trung Quốc tuyệt quá, rất ngon miệng."),
            ("这些菜一百块钱，不贵。", "Zhèxiē cài yībǎi kuài qián, bú guì.", "Chỗ thức ăn này một trăm tệ, không đắt.")
        ],
        "spotlight": ["饭馆", "吃", "中国", "菜", "米饭", "太", "块", "钱"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nhóm bạn đi ăn ở đâu vào buổi trưa?",
                "options_vi": ["Ở trường", "Ở nhà bạn", "Ở nhà hàng"],
                "answer": 2,
                "explanation_vi": "Trong bài có câu: 今天中午我们去饭馆吃中国菜 (Trưa nay chúng tôi đến nhà hàng ăn món Trung Quốc)."
            },
            {
                "id": "q2",
                "question_vi": "Họ nhận xét món ăn như thế nào?",
                "options_vi": ["Rất ngon miệng", "Món ăn quá cay", "Món ăn không ngon"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 很好吃 (Rất ngon miệng)."
            },
            {
                "id": "q3",
                "question_vi": "Bữa ăn hết bao nhiêu tiền?",
                "options_vi": ["50 tệ", "100 tệ", "200 tệ"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 一百块钱 (Một trăm tệ)."
            }
        ]
    },
    {
        "id": "hsk1_story_008",
        "level": "HSK1",
        "title": {
            "zh": "去商店买衣服",
            "vi": "Đi cửa hàng mua quần áo"
        },
        "topic": "shopping",
        "topic_vi": "Mua sắm & Đời sống",
        "icon": "👗",
        "estimatedMinutes": 3,
        "description_vi": "Trải nghiệm đi mua một chiếc áo mới tại cửa hàng vào cuối tuần.",
        "sentences": [
            ("星期六上午我和妈妈去商店。", "Xīngqīliù shàngwǔ wǒ hé māma qù shāngdiàn.", "Sáng thứ bảy tôi và mẹ đi đến cửa hàng."),
            ("商店里有很多漂亮的衣服。", "Shāngdiàn lǐ yǒu hěn duō piàoliang de yīfu.", "Trong cửa hàng có rất nhiều quần áo đẹp."),
            ("我看见了一件漂亮的衣服。", "Wǒ kànjiàn le yí jiàn piàoliang de yīfu.", "Tôi nhìn thấy một chiếc áo rất đẹp."),
            ("我问售货员：这件衣服多少钱？", "Wǒ wèn shòuhuòyuán: Zhè jiàn yīfu duōshao qián?", "Tôi hỏi nhân viên bán hàng: Chiếc áo này bao nhiêu tiền?"),
            ("售货员说：八十块。妈妈买了这个衣服。", "Shòuhuòyuán shuō: Bāshí kuài. Māma mǎi le zhè ge yīfu.", "Nhân viên nói: Tám mươi tệ. Mẹ đã mua chiếc áo này.")
        ],
        "spotlight": ["妈妈", "商店", "衣服", "看见", "多少", "钱", "买", "块"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nhân vật chính đi cửa hàng với ai?",
                "options_vi": ["Bố", "Mẹ", "Bạn học"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 我和妈妈去商店 (Tôi và mẹ đi cửa hàng)."
            },
            {
                "id": "q2",
                "question_vi": "Chiếc áo nhân vật chính nhìn thấy trông thế nào?",
                "options_vi": ["Rất xấu", "Rất đẹp", "Rất to"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 一件漂亮的衣服 (Một chiếc áo rất đẹp)."
            },
            {
                "id": "q3",
                "question_vi": "Chiếc áo có giá bao nhiêu tệ?",
                "options_vi": ["60 tệ", "80 tệ", "100 tệ"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 八十块 (Tám mươi tệ)."
            }
        ]
    },
    {
        "id": "hsk1_story_009",
        "level": "HSK1",
        "title": {
            "zh": "今天下雨了",
            "vi": "Hôm nay trời mưa rồi"
        },
        "topic": "daily_life",
        "topic_vi": "Thời tiết & Sinh hoạt",
        "icon": "🌧️",
        "estimatedMinutes": 3,
        "description_vi": "Một ngày mưa mát mẻ ở nhà đọc sách, uống trà và xem phim.",
        "sentences": [
            ("今天天气不太好，下雨了。", "Jīntiān tiānqì bú tài hǎo, xià yǔ le.", "Thời tiết hôm nay không tốt lắm, trời mưa rồi."),
            ("外面冷，我不想去学校。", "Wàimiàn lěng, wǒ bù xiǎng qù xuéxiào.", "Bên ngoài lạnh, tôi không muốn đến trường học."),
            ("我和爸爸在家里看电视。", "Wǒ hé bàba zài jiā lǐ kàn diànshì.", "Tôi và bố ở trong nhà xem tivi."),
            ("妈妈给我们做热茶和中国菜。", "Māma gěi wǒmen zuò rè chá hé zhōngguó cài.", "Mẹ làm trà nóng và món ăn Trung Quốc cho chúng tôi."),
            ("下雨了，我们在家里很高兴。", "Xià yǔ le, wǒmen zài jiā lǐ hěn gāoxìng.", "Trời mưa rồi, chúng tôi ở trong nhà rất vui vẻ.")
        ],
        "spotlight": ["天气", "下雨", "冷", "想", "爸爸", "家", "看", "电视", "热", "高兴"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Thời tiết hôm nay như thế nào?",
                "options_vi": ["Nắng ấm", "Trời mưa và lạnh", "Có tuyết rơi"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 下雨了... 外面冷 (Trời mưa rồi... bên ngoài lạnh)."
            },
            {
                "id": "q2",
                "question_vi": "Nhân vật chính cùng bố làm gì ở nhà?",
                "options_vi": ["Xem tivi", "Chơi cờ", "Ngủ"],
                "answer": 0,
                "explanation_vi": "Trong bài có câu: 我和爸爸在家里看电视 (Tôi và bố ở trong nhà xem tivi)."
            },
            {
                "id": "q3",
                "question_vi": "Mẹ đã chuẩn bị đồ uống gì cho gia đình?",
                "options_vi": ["Trà nóng", "Nước dừa", "Nước ép táo"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 做热茶 (Làm trà nóng)."
            }
        ]
    },
    {
        "id": "hsk1_story_010",
        "level": "HSK1",
        "title": {
            "zh": "坐飞机去北京",
            "vi": "Đi máy bay đến Bắc Kinh"
        },
        "topic": "travel",
        "topic_vi": "Du lịch & Trải nghiệm",
        "icon": "✈️",
        "estimatedMinutes": 3,
        "description_vi": "Chuyến bay đầu tiên đến Bắc Kinh để du lịch và ngắm nhìn cảnh đẹp.",
        "sentences": [
            ("明天上午我们要坐飞机去北京。", "Míngtiān shàngwǔ wǒmen yào zuò fēijī qù Běijīng.", "Sáng mai chúng tôi sẽ đi máy bay đến Bắc Kinh."),
            ("我坐飞机去北京，我很高兴。", "Wǒ zuò fēijī qù Běijīng, wǒ hěn gāoxìng.", "Tôi đi máy bay đến Bắc Kinh, tôi rất vui mừng."),
            ("爸爸说北京很大，有很多漂亮的地方。", "Bàba shuō Běijīng hěn dà, yǒu hěn duō piàoliang de dìfang.", "Bố nói Bắc Kinh rất lớn, có rất nhiều nơi đẹp."),
            ("我想在北京看中国朋友，吃北京烤鸭。", "Wǒ xiǎng zài Běijīng kàn zhōngguó péngyou, chī Běijīng kǎoyā.", "Tôi muốn gặp bạn bè Trung Quốc và ăn vịt quay ở Bắc Kinh."),
            ("北京的朋友在等我们，太好了。", "Běijīng de péngyou zài děng wǒmen, tài hǎo le.", "Những người bạn ở Bắc Kinh đang đợi chúng tôi, tuyệt vời quá.")
        ],
        "spotlight": ["明天", "上午", "飞机", "去", "北京", "高兴", "爸爸", "大", "漂亮", "想", "朋友", "太"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Gia đình nhân vật chính đi Bắc Kinh bằng phương tiện gì?",
                "options_vi": ["Tàu hỏa", "Máy bay", "Xe khách"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 坐飞机去北京 (Đi máy bay đến Bắc Kinh)."
            },
            {
                "id": "q2",
                "question_vi": "Bố miêu tả Bắc Kinh như thế nào?",
                "options_vi": ["Rất nhỏ", "Rất lớn và có nhiều nơi đẹp", "Rất lạnh và buồn"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 北京很大，有很多漂亮的地方 (Bắc Kinh rất lớn, có rất nhiều nơi đẹp)."
            },
            {
                "id": "q3",
                "question_vi": "Ai đang đợi gia đình ở Bắc Kinh?",
                "options_vi": ["Những người bạn ở Bắc Kinh", "Cô giáo", "Tài xế taxi"],
                "answer": 0,
                "explanation_vi": "Trong câu cuối có viết: 北京的朋友在等我们 (Những người bạn ở Bắc Kinh đang đợi chúng tôi)."
            }
        ]
    }
]

def update_manifest():
    manifest_entries = []
    # Read all story files in all subfolders of database/readings
    story_files = sorted(READINGS_DIR.glob("**/*.json"))
    for sf in story_files:
        if sf.name == "manifest.json":
            continue
        with open(sf, "r", encoding="utf-8") as f:
            story = json.load(f)
            rel_file = f"database/readings/{story['level'].lower()}/{sf.name}"
            
            # Map topic to topic_vi
            topic_vi_map = {
                "daily_life": "Sinh hoạt thường nhật",
                "pets_family": "Thú cưng & Gia đình",
                "shopping": "Mua sắm & Đời sống",
                "school_study": "Học tập & Trường học",
                "social_life": "Bạn bè & Đời sống",
                "people_friends": "Con người & Tình bạn",
                "food_dining": "Ẩm thực & Nhà hàng",
                "travel": "Du lịch & Trải nghiệm"
            }
            
            icon_map = {
                "hsk1_story_001": "☀️",
                "hsk1_story_002": "🐱",
                "hsk1_story_003": "🍎",
                "hsk1_story_004": "🏫",
                "hsk1_story_005": "🍵",
                "hsk1_story_006": "👧",
                "hsk1_story_007": "🍜",
                "hsk1_story_008": "👗",
                "hsk1_story_009": "🌧️",
                "hsk1_story_010": "✈️"
            }

            manifest_entries.append({
                "id": story["id"],
                "level": story["level"],
                "title": story["title"],
                "topic": story["topic"],
                "topic_vi": topic_vi_map.get(story["topic"], "Đời sống"),
                "icon": icon_map.get(story["id"], "📖"),
                "estimatedMinutes": story["estimatedMinutes"],
                "description_vi": story["description_vi"],
                "sentence_count": len(story["sentences"]),
                "spotlight_count": len(story["vocabulary_spotlight"]),
                "quiz_count": len(story["quiz"]),
                "file": rel_file
            })

    # Sort manifest entries by id
    manifest_entries.sort(key=lambda x: x["id"])
    manifest_path = READINGS_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, ensure_ascii=False, indent=2)
    print(f"[✓] Updated manifest.json with {len(manifest_entries)} entries.")

def main():
    hsk1_dir = READINGS_DIR / "hsk1"
    hsk1_dir.mkdir(parents=True, exist_ok=True)

    generated_count = 0
    for sdata in STORIES_HSK1:
        sid = sdata["id"]
        custom_names = sdata.get("custom_names", {})

        sentences_json = []
        words_found_ids = set()

        for sidx, (zh, py, vi) in enumerate(sdata["sentences"]):
            tokens = tokenize_sentence(zh, custom_names)
            for tok in tokens:
                if tok.get("word_id"):
                    words_found_ids.add(tok["word_id"])
            
            sentences_json.append({
                "id": f"s{sidx+1}",
                "zh": zh,
                "pinyin": py,
                "vi": vi,
                "audio_start_ms": None,
                "audio_end_ms": None,
                "tokens": tokens
            })

        # Calculate spotlight
        spotlight_ids = []
        for word in sdata.get("spotlight", []):
            if word in VOCAB_MAP:
                wid = VOCAB_MAP[word]["word_id"]
                if wid in words_found_ids:
                    spotlight_ids.append(wid)
            else:
                print(f"[!] Warning: Spotlight word '{word}' not in VOCAB_MAP")

        # Fallback to found words if spotlight list had any misses
        if len(spotlight_ids) < 4:
            for wid in words_found_ids:
                if wid not in spotlight_ids:
                    spotlight_ids.append(wid)
                if len(spotlight_ids) >= 7:
                    break

        story_obj = {
            "id": sid,
            "level": sdata["level"],
            "title": sdata["title"],
            "topic": sdata["topic"],
            "estimatedMinutes": sdata["estimatedMinutes"],
            "description_vi": sdata["description_vi"],
            "sentences": sentences_json,
            "vocabulary_spotlight": spotlight_ids,
            "quiz": sdata["quiz"]
        }

        out_path = hsk1_dir / f"{sid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(story_obj, f, ensure_ascii=False, indent=2)

        print(f"[✓] Generated {sid} -> {out_path.name} ({len(sentences_json)} sentences, {len(spotlight_ids)} spotlight words)")
        generated_count += 1

    print(f"\nSuccessfully generated {generated_count} HSK1 stories.")
    update_manifest()

if __name__ == "__main__":
    main()
