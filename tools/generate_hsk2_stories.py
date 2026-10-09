#!/usr/bin/env python3
"""
tools/generate_hsk2_stories.py
Generates 10 HSK2 Graded Reading stories and updates manifest.json.
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

# 10 HSK2 Stories Definitions
STORIES_HSK2 = [
    {
        "id": "hsk2_story_001",
        "level": "HSK2",
        "title": {
            "zh": "生病看医生",
            "vi": "Bị ốm đi khám bác sĩ"
        },
        "topic": "health_daily",
        "topic_vi": "Sức khỏe & Đời sống",
        "icon": "🏥",
        "estimatedMinutes": 3,
        "description_vi": "Tiểu Minh cảm thấy không khỏe và đến bệnh viện gặp bác sĩ khám bệnh.",
        "sentences": [
            ("今天早上我觉得身体不舒服。", "Jīntiān zǎoshang wǒ juéde shēntǐ bù shūfu.", "Sáng hôm nay tôi cảm thấy cơ thể không thoải mái."),
            ("妈妈带我去医院看医生。", "Māma dài wǒ qù yīyuàn kàn yīshēng.", "Mẹ đưa tôi đến bệnh viện gặp bác sĩ."),
            ("医生告诉我：你生病了，要多喝水。", "Yīshēng gàosu wǒ: Nǐ shēngbìng le, yào duō hē shuǐ.", "Bác sĩ nói với tôi: Cháu bị ốm rồi, cần uống nhiều nước."),
            ("医生给我开了一些药。", "Yīshēng gěi wǒ kāi le yìxiē yào.", "Bác sĩ kê cho tôi một ít thuốc."),
            ("吃了药以后，我在家好好休息。", "Chī le yào yǐhòu, wǒ zài jiā hǎohāo xiūxi.", "Sau khi uống thuốc, tôi ở nhà nghỉ ngơi thật tốt.")
        ],
        "spotlight": ["身体", "觉得", "医院", "医生", "告诉", "生病", "药", "休息"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Buổi sáng nhân vật chính cảm thấy thế nào?",
                "options_vi": ["Rất khỏe mạnh", "Cơ thể không thoải mái", "Rất đói bụng"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 觉得身体不舒服 (Cảm thấy cơ thể không thoải mái)."
            },
            {
                "id": "q2",
                "question_vi": "Bác sĩ khuyên bệnh nhân điều gì?",
                "options_vi": ["Đi chạy bộ", "Uống nhiều nước", "Đi du lịch"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 要多喝水 (Cần uống nhiều nước)."
            },
            {
                "id": "q3",
                "question_vi": "Sau khi uống thuốc, nhân vật chính làm gì?",
                "options_vi": ["Đi bơi", "Ở nhà nghỉ ngơi", "Đi học"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 在家好好休息 (Ở nhà nghỉ ngơi thật tốt)."
            }
        ]
    },
    {
        "id": "hsk2_story_002",
        "level": "HSK2",
        "title": {
            "zh": "周末去打篮球",
            "vi": "Cuối tuần đi chơi bóng rổ"
        },
        "topic": "sports_hobby",
        "topic_vi": "Thể thao & Sở thích",
        "icon": "🏀",
        "estimatedMinutes": 3,
        "description_vi": "Hoạt động thể thao rèn luyện sức khỏe cùng bạn bè vào chiều thứ Bảy.",
        "sentences": [
            ("星期六下午，天气很晴朗。", "Xīngqīliù xiàwǔ, tiānqì hěn qínglǎng.", "Chiều thứ bảy, thời tiết rất nắng ráo."),
            ("我和哥哥一起去学校打篮球。", "Wǒ hé gēge yìqǐ qù xuéxiào dǎ lánqiú.", "Tôi và anh trai cùng nhau đến trường chơi bóng rổ."),
            ("我们在学校打了一个小时篮球。", "Wǒmen zài xuéxiào dǎ le yí gè xiǎoshí lánqiú.", "Chúng tôi chơi bóng rổ ở trường suốt một tiếng đồng hồ."),
            ("运动以后，我们觉得很累，但是很高兴。", "Yùndòng yǐhòu, wǒmen juéde hěn lèi, dànshì hěn gāoxìng.", "Sau khi vận động, chúng tôi cảm thấy rất mệt, nhưng rất vui."),
            ("多运动对身体非常好。", "Duō yùndòng duì shēntǐ fēicháng hǎo.", "Vận động nhiều rất tốt cho sức khỏe.")
        ],
        "spotlight": ["哥哥", "一起", "打篮球", "小时", "运动", "累", "身体", "非常"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nhân vật chính đi chơi thể thao cùng với ai?",
                "options_vi": ["Bố", "Anh trai", "Thầy giáo"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 我和哥哥一起去学校打篮球 (Tôi và anh trai cùng nhau đến trường chơi bóng rổ)."
            },
            {
                "id": "q2",
                "question_vi": "Họ đã chơi bóng rổ trong bao lâu?",
                "options_vi": ["30 phút", "Một tiếng đồng hồ", "Ba tiếng đồng hồ"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 打了一个小时篮球 (Chơi bóng rổ một tiếng đồng hồ)."
            },
            {
                "id": "q3",
                "question_vi": "Lợi ích của việc vận động thể thao là gì?",
                "options_vi": ["Rất tốt cho cơ thể", "Làm cho mệt mỏi mãi", "Tốn tiền"],
                "answer": 0,
                "explanation_vi": "Trong câu cuối có viết: 多运动对身体非常好 (Vận động nhiều rất tốt cho sức khỏe)."
            }
        ]
    },
    {
        "id": "hsk2_story_003",
        "level": "HSK2",
        "title": {
            "zh": "在火车站买票",
            "vi": "Mua vé ở ga xe lửa"
        },
        "topic": "travel",
        "topic_vi": "Du lịch & Đi lại",
        "icon": "🚆",
        "estimatedMinutes": 3,
        "description_vi": "Chuẩn bị cho chuyến đi du lịch xa bằng tàu hỏa cùng gia đình.",
        "sentences": [
            ("下个月我们准备去上海旅游。", "Xià gè yuè wǒmen zhǔnbèi qù Shànghǎi lǚyóu.", "Tháng sau chúng tôi chuẩn bị đi Thượng Hải du lịch."),
            ("今天我和爸爸去火车站买票。", "Jīntiān wǒ hé bàba qù huǒchēzhàn mǎi piào.", "Hôm nay tôi và bố đến ga tàu hỏa để mua vé."),
            ("火车站里人很多，大家都在等车。", "Huǒchēzhàn lǐ rén hěn duō, dàjiā dōu zài děng chē.", "Trong ga tàu rất đông người, mọi người đều đang chờ xe."),
            ("服务员告诉我们，火车票不贵，很便宜。", "Fúwùyuán gàosu wǒmen, huǒchēpiào bú guì, hěn piányi.", "Nhân viên phục vụ nói với chúng tôi vé tàu không đắt, rất rẻ."),
            ("我们买了三张票，高高兴兴地回家了。", "Wǒmen mǎi le sān zhāng piào, gāogāoxìngxìng de huí jiā le.", "Chúng tôi đã mua ba vé, vui vẻ trở về nhà.")
        ],
        "spotlight": ["准备", "旅游", "火车站", "票", "大家", "等", "服务员", "便宜"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Gia đình chuẩn bị đi đâu vào tháng sau?",
                "options_vi": ["Bắc Kinh", "Thượng Hải", "Quảng Châu"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 准备去上海旅游 (Chuẩn bị đi Thượng Hải du lịch)."
            },
            {
                "id": "q2",
                "question_vi": "Giá vé tàu hỏa như thế nào?",
                "options_vi": ["Rất đắt", "Không đắt, rất rẻ", "Miễn phí"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 火车票不贵，很便宜 (Vé tàu không đắt, rất rẻ)."
            },
            {
                "id": "q3",
                "question_vi": "Họ đã mua bao nhiêu vé tàu?",
                "options_vi": ["Một vé", "Hai vé", "Ba vé"],
                "answer": 2,
                "explanation_vi": "Trong câu có viết: 买了三张票 (Đã mua ba vé)."
            }
        ]
    },
    {
        "id": "hsk2_story_004",
        "level": "HSK2",
        "title": {
            "zh": "可爱的小狗",
            "vi": "Chú chó nhỏ đáng yêu"
        },
        "topic": "pets_nature",
        "topic_vi": "Thú cưng & Đời sống",
        "icon": "🐶",
        "estimatedMinutes": 3,
        "description_vi": "Chú chó nhỏ lông trắng chạy nhảy vui đùa trong sân nhà.",
        "sentences": [
            ("我家有一只白色的小狗。", "Wǒ jiā yǒu yì zhī báisè de xiǎogǒu.", "Nhà tôi có một chú chó nhỏ màu trắng."),
            ("它的眼睛很大，黑黑的，真漂亮。", "Tā de yǎnjing hěn dà, hēihēi de, zhēn piàoliang.", "Mắt của nó rất to, đen láy, thật là đẹp."),
            ("今天天气很晴，小狗在外面玩。", "Jīntiān tiānqì hěn qíng, xiǎogǒu zài wàimiàn wán.", "Hôm nay trời nắng đẹp, chú chó chơi ở bên ngoài."),
            ("它跑得真快，喜欢跟我一起跑。", "Tā pǎo de zhēn kuài, xǐhuan gēn wǒ yìqǐ pǎo.", "Nó chạy thật là nhanh, thích chạy cùng với tôi."),
            ("我们全家都很喜欢它。", "Wǒmen quán jiā dōu hěn xǐhuan tā.", "Cả nhà chúng tôi đều rất yêu quý nó.")
        ],
        "spotlight": ["白", "它", "眼睛", "真", "晴", "玩", "跑", "跑步", "快"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Chú chó nhỏ có bộ lông màu gì?",
                "options_vi": ["Màu đen", "Màu trắng", "Màu vàng"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 白色的小狗 (Chú chó nhỏ màu trắng)."
            },
            {
                "id": "q2",
                "question_vi": "Đôi mắt của chú chó trông như thế nào?",
                "options_vi": ["Rất nhỏ", "Rất to và đen, rất đẹp", "Màu xanh"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 它的眼睛很大，黑黑的，真漂亮 (Mắt của nó rất to, đen láy, thật đẹp)."
            },
            {
                "id": "q3",
                "question_vi": "Chú chó thích làm gì cùng nhân vật chính?",
                "options_vi": ["Ngủ", "Chạy cùng nhau", "Xem tivi"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 喜欢跟我一起跑 (Thích chạy cùng với tôi)."
            }
        ]
    },
    {
        "id": "hsk2_story_005",
        "level": "HSK2",
        "title": {
            "zh": "去宾馆找朋友",
            "vi": "Đến khách sạn tìm bạn"
        },
        "topic": "social_life",
        "topic_vi": "Giao tiếp & Bạn bè",
        "icon": "🏨",
        "estimatedMinutes": 3,
        "description_vi": "Đến khách sạn đón người bạn phương xa vừa đến thành phố du lịch.",
        "sentences": [
            ("我的外国朋友昨天到了北京。", "Wǒ de wàiguó péngyou zuótiān dào le Běijīng.", "Người bạn nước ngoài của tôi hôm qua đã đến Bắc Kinh."),
            ("他住在一所大宾馆里。", "Tā zhù zài yì suǒ dà bīnguǎn lǐ.", "Anh ấy sống ở một khách sạn lớn."),
            ("宾馆离我家不太远，很近。", "Bīnguǎn lí wǒ jiā bú tài yuǎn, hěn jìn.", "Khách sạn cách nhà tôi không xa lắm, rất gần."),
            ("我走到宾馆门口，看见他在等我。", "Wǒ zǒu dào bīnguǎn ménkǒu, kànjiàn tā zài děng wǒ.", "Tôi đi đến cổng khách sạn, nhìn thấy anh ấy đang chờ tôi."),
            ("我们高高兴兴地进了一家咖啡馆。", "Wǒmen gāogāoxìngxìng de jìn le yì jiā kāfēiguǎn.", "Chúng tôi vui vẻ bước vào một quán cà phê.")
        ],
        "spotlight": ["到", "宾馆", "离", "远", "近", "走", "门", "咖啡"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Người bạn nước ngoài đang ở đâu?",
                "options_vi": ["Ở trường học", "Ở một khách sạn lớn", "Ở nhà nhân vật chính"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 他住在一所大宾馆里 (Anh ấy ở tại một khách sạn lớn)."
            },
            {
                "id": "q2",
                "question_vi": "Khoảng cách từ khách sạn tới nhà nhân vật chính ra sao?",
                "options_vi": ["Rất xa", "Không xa lắm, rất gần", "Cùng một tòa nhà"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 离我家不太远，很近 (Cách nhà tôi không quá xa, rất gần)."
            },
            {
                "id": "q3",
                "question_vi": "Sau khi gặp nhau, hai người đi đâu?",
                "options_vi": ["Đi quán cà phê", "Đi bệnh viện", "Đi sân bay"],
                "answer": 0,
                "explanation_vi": "Trong câu cuối có viết: 进了一家咖啡馆 (Bước vào một quán cà phê)."
            }
        ]
    },
    {
        "id": "hsk2_story_006",
        "level": "HSK2",
        "title": {
            "zh": "生日快乐，送你手表",
            "vi": "Sinh nhật vui vẻ, tặng bạn đồng hồ"
        },
        "topic": "family_celebration",
        "topic_vi": "Gia đình & Lễ kỷ niệm",
        "icon": "⌚",
        "estimatedMinutes": 3,
        "description_vi": "Món quà sinh nhật ý nghĩa dành cho người thân yêu trong gia đình.",
        "sentences": [
            ("今天是妻子的生日。", "Jīntiān shì qīzi de shēngrì.", "Hôm nay là sinh nhật của vợ tôi."),
            ("早上我起床以后，对她说：生日快乐！", "Zǎoshang wǒ qǐchuáng yǐhòu, duì tā shuō: Shēngrì kuàilè!", "Buổi sáng sau khi thức dậy, tôi nói với cô ấy: Chúc mừng sinh nhật!"),
            ("我送给她一块漂亮的手表。", "Wǒ sòng gěi tā yí kuài piàoliang de shǒubiǎo.", "Tôi tặng cho cô ấy một chiếc đồng hồ đeo tay rất đẹp."),
            ("妻子戴上新手表，非常高兴。", "Qīzi dài shàng xīn shǒubiǎo, fēicháng gāoxìng.", "Vợ đeo chiếc đồng hồ mới vào, vô cùng vui sướng."),
            ("她说这是她最喜欢的礼物。", "Tā shuō zhè shì tā zuì xǐhuan de lǐwù.", "Cô ấy nói đây là món quà cô thích nhất.")
        ],
        "spotlight": ["妻子", "生日", "起床", "快乐", "送", "手表", "新", "最", "非常"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Hôm nay là ngày gì đặc biệt?",
                "options_vi": ["Ngày Tết", "Sinh nhật của vợ", "Ngày cưới"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 今天是妻子的生日 (Hôm nay là sinh nhật của vợ)."
            },
            {
                "id": "q2",
                "question_vi": "Món quà sinh nhật được tặng là gì?",
                "options_vi": ["Điện thoại", "Đồng hồ đeo tay", "Quần áo"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 送给她一块漂亮的手表 (Tặng cô ấy một chiếc đồng hồ đẹp)."
            },
            {
                "id": "q3",
                "question_vi": "Người vợ cảm thấy thế nào khi nhận quà?",
                "options_vi": ["Không thích", "Vô cùng vui vẻ", "Bình thường"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 非常高兴 (Vô cùng vui vẻ)."
            }
        ]
    },
    {
        "id": "hsk2_story_007",
        "level": "HSK2",
        "title": {
            "zh": "在公司的新工作",
            "vi": "Công việc mới ở công ty"
        },
        "topic": "work_office",
        "topic_vi": "Công sở & Nghề nghiệp",
        "icon": "💼",
        "estimatedMinutes": 3,
        "description_vi": "Ngày đầu đi làm tại công ty mới và nhận được sự giúp đỡ của đồng nghiệp.",
        "sentences": [
            ("这是我第一天在这家公司上班。", "Zhè shì wǒ dì-yī tiān zài zhè jiā gōngsī shàngbān.", "Đây là ngày đầu tiên tôi đi làm tại công ty này."),
            ("公司很大，大家都在认真做事情。", "Gōngsī hěn dà, dàjiā dōu zài rènzhēn zuò shìqing.", "Công ty rất lớn, mọi người đều đang chăm chỉ làm việc."),
            ("一开始我有很多问题不懂。", "Yì kāishǐ wǒ yǒu hěn duō wèntí bù dǒng.", "Mới đầu tôi có rất nhiều vấn đề không hiểu."),
            ("旁边的同事很热情，常常帮助我。", "Pángbiān de tóngshì hěn rèqíng, chángcháng bāngzhù wǒ.", "Đồng nghiệp bên cạnh rất nhiệt tình, thường xuyên giúp đỡ tôi."),
            ("我觉得这里的工作环境非常好。", "Wǒ juéde zhèlǐ de gōngzuò huánjìng fēicháng hǎo.", "Tôi cảm thấy môi trường làm việc ở đây rất tốt.")
        ],
        "spotlight": ["第一", "公司", "上班", "事情", "开始", "问题", "懂", "旁边", "帮助"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Hôm nay là ngày thứ mấy nhân vật chính đi làm ở công ty?",
                "options_vi": ["Ngày đầu tiên", "Ngày thứ hai", "Đã làm một năm"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 这是我第一天在这家公司上班 (Đây là ngày đầu tiên tôi đi làm ở công ty này)."
            },
            {
                "id": "q2",
                "question_vi": "Lúc mới bắt đầu, nhân vật chính gặp khó khăn gì?",
                "options_vi": ["Không có xe", "Có nhiều vấn đề không hiểu", "Không có bạn bè"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 有很多问题不懂 (Có nhiều vấn đề không hiểu)."
            },
            {
                "id": "q3",
                "question_vi": "Đồng nghiệp bên cạnh đối xử với nhân vật chính như thế nào?",
                "options_vi": ["Lạnh nhạt", "Nhiệt tình giúp đỡ", "Không nói chuyện"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 常常帮助我 (Thường xuyên giúp đỡ tôi)."
            }
        ]
    },
    {
        "id": "hsk2_story_008",
        "level": "HSK2",
        "title": {
            "zh": "买西瓜和牛奶",
            "vi": "Mua dưa hấu và sữa tươi"
        },
        "topic": "shopping_market",
        "topic_vi": "Đi chợ & Mua sắm",
        "icon": "🍉",
        "estimatedMinutes": 3,
        "description_vi": "Đi mua hoa quả tươi và đồ uống thơm ngon cho cả nhà thưởng thức.",
        "sentences": [
            ("今天下午我和妹妹去市场买东西。", "Jīntiān xiàwǔ wǒ hé mèimei qù shìchǎng mǎi dōngxi.", "Chiều nay tôi và em gái đi chợ mua đồ."),
            ("这里的西瓜又大又甜，还很便宜。", "Zhèlǐ de xīguā yòu dà yòu tián, hái hěn piányi.", "Dưa hấu ở đây vừa to vừa ngọt, lại còn rất rẻ."),
            ("我们买了一个大西瓜和两瓶牛奶。", "Wǒmen mǎi le yí gè dà xīguā hé liǎng píng niúnǎi.", "Chúng tôi đã mua một quả dưa hấu to và hai chai sữa tươi."),
            ("妹妹还想买一些鸡蛋，妈妈做菜用。", "Mèimei hái xiǎng mǎi yìxiē jīdàn, māma zuò cài yòng.", "Em gái còn muốn mua một ít trứng gà cho mẹ nấu ăn."),
            ("卖东西的人笑着对我们说：欢迎再来！", "Mài dōngxi de rén xiào zhe duì wǒmen shuō: Huānyíng zài lái!", "Người bán hàng cười nói với chúng tôi: Hoan nghênh lần sau lại ghé!")
        ],
        "spotlight": ["妹妹", "西瓜", "便宜", "两", "牛奶", "鸡蛋", "卖", "笑", "再"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nhân vật chính đi chợ cùng ai?",
                "options_vi": ["Chị gái", "Em gái", "Bố"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 我和妹妹去市场买东西 (Tôi và em gái đi chợ mua đồ)."
            },
            {
                "id": "q2",
                "question_vi": "Dưa hấu ở chợ được miêu tả ra sao?",
                "options_vi": ["Vừa to vừa ngọt, rất rẻ", "Đắt và chua", "Rất nhỏ"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 西瓜又大又甜，还很便宜 (Dưa hấu vừa to vừa ngọt, lại rất rẻ)."
            },
            {
                "id": "q3",
                "question_vi": "Người bán hàng có thái độ thế nào khi tạm biệt?",
                "options_vi": ["Khó chịu", "Cười và mời lần sau lại ghé", "Không nhìn khách"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 笑着对我们说：欢迎再来 (Cười nói với chúng tôi: Hoan nghênh lại đến)."
            }
        ]
    },
    {
        "id": "hsk2_story_009",
        "level": "HSK2",
        "title": {
            "zh": "虽然累，但是很高兴",
            "vi": "Tuy mệt nhưng rất vui"
        },
        "topic": "daily_reflection",
        "topic_vi": "Sinh hoạt & Tâm trạng",
        "icon": "🌟",
        "estimatedMinutes": 3,
        "description_vi": "Một ngày bận rộn dọn dẹp và chuẩn bị cho kỳ thi sắp tới.",
        "sentences": [
            ("今天从早上到晚上我都很忙。", "Jīntiān cóng zǎoshang dào wǎnshang wǒ dōu hěn máng.", "Hôm nay từ sáng đến tối tôi đều rất bận."),
            ("明天学校有考试，我要认真准备。", "Míngtiān xuéxiào yǒu kǎoshì, wǒ yào rènzhēn zhǔnbèi.", "Ngày mai trường có bài thi, tôi phải chăm chỉ chuẩn bị."),
            ("我看了三个小时的书，做完了所有练习。", "Wǒ kàn le sān gè xiǎoshí de shū, zuò wán le suǒyǒu liànxí.", "Tôi đã đọc sách ba tiếng đồng hồ và làm xong bài tập."),
            ("虽然今天觉得很累，但是心里很高兴。", "Suīrán jīntiān juéde hěn lèi, dànshì xīnlǐ hěn gāoxìng.", "Tuy hôm nay cảm thấy rất mệt, nhưng trong lòng rất vui."),
            ("我相信明天一定能考好。", "Wǒ xiāngxìn míngtiān yídìng néng kǎo hǎo.", "Tôi tin ngày mai nhất định sẽ thi tốt.")
        ],
        "spotlight": ["从", "到", "晚上", "忙", "考试", "准备", "完", "累", "虽然…但是…", "高兴"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Tại sao hôm nay nhân vật chính lại bận rộn như vậy?",
                "options_vi": ["Đi mua sắm", "Chuẩn bị cho bài thi ngày mai", "Đi chơi xa"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 明天学校有考试，我要认真准备 (Ngày mai trường có thi, tôi phải chuẩn bị kỹ)."
            },
            {
                "id": "q2",
                "question_vi": "Nhân vật chính đã học bài trong bao lâu?",
                "options_vi": ["1 tiếng", "3 tiếng đồng hồ", "Cả đêm"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 看了三个小时的书 (Đã đọc sách suốt ba tiếng)."
            },
            {
                "id": "q3",
                "question_vi": "Tâm trạng cuối ngày của nhân vật chính thế nào?",
                "options_vi": ["Buồn bã", "Rất mệt nhưng trong lòng rất vui", "Lo sợ"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 虽然今天觉得很累，但是心里很高兴 (Tuy cảm thấy mệt nhưng trong lòng rất vui)."
            }
        ]
    },
    {
        "id": "hsk2_story_010",
        "level": "HSK2",
        "title": {
            "zh": "在咖啡馆喝咖啡",
            "vi": "Uống cà phê ở quán cà phê"
        },
        "topic": "lifestyle_leisure",
        "topic_vi": "Thư giãn & Đời sống",
        "icon": "☕",
        "estimatedMinutes": 3,
        "description_vi": "Buổi chiều bình yên gặp gỡ bạn bè trò chuyện bên ly cà phê thơm nồng.",
        "sentences": [
            ("学校旁边新开了一家小咖啡馆。", "Xuéxiào pángbiān xīn kāi le yì jiā xiǎo kāfēiguǎn.", "Bên cạnh trường học mới mở một quán cà phê nhỏ."),
            ("这里的咖啡很好喝，很多人喜欢来。", "Zhèlǐ de kāfēi hěn hǎohē, hěn duō rén xǐhuan lái.", "Cà phê ở đây rất thơm ngon, nhiều người thích ghé thăm."),
            ("今天下午我和朋友坐在窗户旁边说话。", "Jīntiān xiàwǔ wǒ hé péngyou zuò zài chuānghu pángbiān shuōhuà.", "Chiều hôm nay tôi và bạn ngồi bên cạnh cửa sổ trò chuyện."),
            ("大家一边喝咖啡，一边高兴地笑着。", "Dàjiā yìbiān hē kāfēi, yìbiān gāoxìng de xiào zhe.", "Mọi người vừa uống cà phê, vừa vui vẻ cười nói."),
            ("希望每个周末都能来这里休息。", "Xīwàng měi gè zhōumò dōu néng lái zhèlǐ xiūxi.", "Hy vọng mỗi cuối tuần đều có thể đến đây thư giãn.")
        ],
        "spotlight": ["旁边", "新", "咖啡", "说话", "大家", "笑", "希望", "每", "休息"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Quán cà phê mới mở nằm ở vị trí nào?",
                "options_vi": ["Ở bệnh viện", "Bên cạnh trường học", "Ở sân bay"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 学校旁边新开了一家小咖啡馆 (Bên cạnh trường học mới mở quán cà phê nhỏ)."
            },
            {
                "id": "q2",
                "question_vi": "Hai người bạn ngồi ở vị trí nào trong quán?",
                "options_vi": ["Bên cửa sổ", "Ở ngoài cửa", "Trên gác xép"],
                "answer": 0,
                "explanation_vi": "Trong bài có câu: 坐在窗户旁边说话 (Ngồi cạnh cửa sổ trò chuyện)."
            },
            {
                "id": "q3",
                "question_vi": "Nhân vật chính có mong muốn gì?",
                "options_vi": ["Mở quán cà phê riêng", "Mỗi cuối tuần đều có thể đến đây nghỉ ngơi", "Đi ngủ"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 希望每个周末都能来这里休息 (Hy vọng mỗi cuối tuần đều có thể đến đây nghỉ ngơi)."
            }
        ]
    }
]

def update_manifest():
    manifest_entries = []
    story_files = sorted(READINGS_DIR.glob("**/*.json"))
    for sf in story_files:
        if sf.name == "manifest.json":
            continue
        with open(sf, "r", encoding="utf-8") as f:
            story = json.load(f)
            lvl_lower = story["level"].lower()
            rel_file = f"database/readings/{lvl_lower}/{sf.name}"

            topic_vi_map = {
                "daily_life": "Sinh hoạt thường nhật",
                "pets_family": "Thú cưng & Gia đình",
                "pets_nature": "Thú cưng & Đời sống",
                "shopping": "Mua sắm & Đời sống",
                "shopping_market": "Đi chợ & Mua sắm",
                "school_study": "Học tập & Trường học",
                "social_life": "Bạn bè & Đời sống",
                "people_friends": "Con người & Tình bạn",
                "food_dining": "Ẩm thực & Nhà hàng",
                "travel": "Du lịch & Đi lại",
                "health_daily": "Sức khỏe & Đời sống",
                "sports_hobby": "Thể thao & Sở thích",
                "family_celebration": "Gia đình & Lễ kỷ niệm",
                "work_office": "Công sở & Nghề nghiệp",
                "daily_reflection": "Sinh hoạt & Tâm trạng",
                "lifestyle_leisure": "Thư giãn & Đời sống"
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
                "hsk1_story_010": "✈️",
                "hsk2_story_001": "🏥",
                "hsk2_story_002": "🏀",
                "hsk2_story_003": "🚆",
                "hsk2_story_004": "🐶",
                "hsk2_story_005": "🏨",
                "hsk2_story_006": "⌚",
                "hsk2_story_007": "💼",
                "hsk2_story_008": "🍉",
                "hsk2_story_009": "🌟",
                "hsk2_story_010": "☕"
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

    # Sort manifest entries by level then id
    def sort_key(item):
        lvl_num = int("".join([c for c in item["level"] if c.isdigit()]) or "1")
        return (lvl_num, item["id"])

    manifest_entries.sort(key=sort_key)
    manifest_path = READINGS_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, ensure_ascii=False, indent=2)
    print(f"[✓] Updated manifest.json with {len(manifest_entries)} total entries.")

def main():
    hsk2_dir = READINGS_DIR / "hsk2"
    hsk2_dir.mkdir(parents=True, exist_ok=True)

    generated_count = 0
    for sdata in STORIES_HSK2:
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
                if len(spotlight_ids) >= 8:
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

        out_path = hsk2_dir / f"{sid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(story_obj, f, ensure_ascii=False, indent=2)

        print(f"[✓] Generated {sid} -> {out_path.name} ({len(sentences_json)} sentences, {len(spotlight_ids)} spotlight words)")
        generated_count += 1

    print(f"\nSuccessfully generated {generated_count} HSK2 stories.")
    update_manifest()

if __name__ == "__main__":
    main()
