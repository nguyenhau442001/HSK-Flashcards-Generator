#!/usr/bin/env python3
"""
tools/generate_hsk4_stories.py
Generates 10 HSK4 Graded Reading stories and updates manifest.json.
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
            tokens.append({"text": ch, "unknown": True})
            i += 1

    return tokens

# 10 HSK4 Stories Definitions
STORIES_HSK4 = [
    {
        "id": "hsk4_story_001",
        "level": "HSK4",
        "title": {
            "zh": "大学毕业与求职面试",
            "vi": "Tốt nghiệp đại học và phỏng vấn xin việc"
        },
        "topic": "career_growth",
        "topic_vi": "Sự nghiệp & Việc làm",
        "icon": "🎓",
        "estimatedMinutes": 5,
        "description_vi": "Hành trình nỗ lực chuẩn bị hồ sơ và vượt qua buổi phỏng vấn xin việc đầu tiên.",
        "sentences": [
            ("大学毕业以后，我开始积极准备找工作。", "Dàxué bìyè yǐhòu, wǒ kāishǐ jījí zhǔnbèi zhǎo gōngzuò.", "Sau khi tốt nghiệp đại học, tôi bắt đầu tích cực chuẩn bị tìm việc làm."),
            ("按照招聘要求，我认真填写了表格和个人材料。", "Ànzhào zhāopìn yāoqiú, wǒ rènzhēn tiánxiě le biǎogé hé gèrén cáiliào.", "Theo yêu cầu tuyển dụng, tôi cẩn thận điền vào biểu mẫu và hồ sơ cá nhân."),
            ("面试那天我很紧张，但是面试官态度非常友好。", "Miànshì nà tiān wǒ hěn jǐnzhāng, dànshì miànshìguān tàidu fēicháng yǒuhǎo.", "Ngày phỏng vấn tôi rất căng thẳng, nhưng người phỏng vấn thái độ rất thân thiện."),
            ("他提出的问题虽然专业，但我回答得很流利。", "Tā tíchū de wèntí suīrán zhuānyè, dàn wǒ huídá de hěn liúlì.", "Các câu hỏi ông ấy đưa ra tuy chuyên môn, nhưng tôi trả lời rất lưu loát."),
            ("三天后，公司通知我正式被录取了，我充满了信心。", "Sān tiān hòu, gōngsī tōngzhī wǒ zhèngshì bèi lùqǔ le, wǒ chōngmǎn le xìnxīn.", "Ba ngày sau, công ty thông báo tôi chính thức được trúng tuyển, tôi tràn đầy tự tin.")
        ],
        "spotlight": ["毕业", "积极", "按照", "招聘", "要求", "表格", "材料", "紧张", "态度", "友好", "专业", "流利", "通知", "正式", "信心"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Sau khi tốt nghiệp đại học, nhân vật chính làm gì?",
                "options_vi": ["Đi du lịch", "Tích cực chuẩn bị tìm việc làm", "Ở nhà nghỉ ngơi"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 开始积极准备找工作 (Bắt đầu tích cực chuẩn bị tìm việc làm)."
            },
            {
                "id": "q2",
                "question_vi": "Thái độ của người phỏng vấn như thế nào?",
                "options_vi": ["Lạnh lùng", "Rất thân thiện", "Tức giận"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 面试官态度非常友好 (Người phỏng vấn thái độ rất thân thiện)."
            },
            {
                "id": "q3",
                "question_vi": "Kết quả buổi phỏng vấn ra sao?",
                "options_vi": ["Bị từ chối", "Được thông báo chính thức trúng tuyển", "Phải thi lại"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 公司通知我正式被录取了 (Công ty thông báo tôi chính thức trúng tuyển)."
            }
        ]
    },
    {
        "id": "hsk4_story_002",
        "level": "HSK4",
        "title": {
            "zh": "旅行中的难忘经历",
            "vi": "Trải nghiệm khó quên trong chuyến du lịch"
        },
        "topic": "travel_adventure",
        "topic_vi": "Du lịch & Trải nghiệm",
        "icon": "🎒",
        "estimatedMinutes": 5,
        "description_vi": "Lạc đường ở một thành phố xa lạ và nhận được sự giúp đỡ ấm áp từ người bản địa.",
        "sentences": [
            ("去年放暑假的时候，我一个人去了云南旅游。", "Qùnián fàng shǔjià de shíhou, wǒ yí gè rén qù le Yúnnán lǚyóu.", "Vào kỳ nghỉ hè năm ngoái, tôi một mình đến Vân Nam du lịch."),
            ("在古城里散步时，我不小心迷路了，手机也没有信号。", "Zài gǔchéng lǐ sànbù shí, wǒ bù xiǎoxīn mílù le, shǒujī yě méiyǒu xìnhào.", "Khi đi dạo trong cổ trấn, tôi chẳng may bị lạc đường, điện thoại cũng không có sóng."),
            ("正在我着急的时候，一位当地的导游主动走过来。", "Zhèngzài wǒ zháojí de shíhou, yí wèi dāngdì de dǎoyóu zhǔdòng zǒu guòlái.", "Đúng lúc tôi đang sốt ruột, một hướng dẫn viên địa phương chủ động bước tới."),
            ("他耐心地给我指路，还详细解释了当地的历史文化。", "Tā nàixīn de gěi wǒ zhǐ lù, hái xiángxì jiěshì le dāngdì de lìshǐ wénhuà.", "Anh ấy kiên nhẫn chỉ đường cho tôi, còn giải thích tường tận lịch sử văn hóa nơi đây."),
            ("这次意外的经历，让我深深感受到了人们的热情。", "Zhè cì yìwài de jīnglì, ràng wǒ shēnshēn gǎnshòu dào le rénmen de rèqíng.", "Trải nghiệm bất ngờ lần này khiến tôi cảm nhận sâu sắc sự ấm áp của con người.")
        ],
        "spotlight": ["放暑假", "散步", "迷路", "着急", "导游", "主动", "耐心", "详细", "解释", "经历", "热情"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nhân vật chính đi du lịch một mình vào thời gian nào?",
                "options_vi": ["Kỳ nghỉ đông", "Kỳ nghỉ hè năm ngoái", "Dịp Tết"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 去年放暑假的时候 (Vào kỳ nghỉ hè năm ngoái)."
            },
            {
                "id": "q2",
                "question_vi": "Sự cố gì đã xảy ra trong lúc đi dạo?",
                "options_vi": ["Bị mất ví", "Bị lạc đường và điện thoại mất sóng", "Bị ngã"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 不小心迷路了，手机也没有信号 (Bất cẩn lạc đường, điện thoại không có sóng)."
            },
            {
                "id": "q3",
                "question_vi": "Người hướng dẫn viên địa phương đã giúp đỡ điều gì?",
                "options_vi": ["Cho mượn tiền", "Kiên nhẫn chỉ đường và giải thích lịch sử", "Gọi xe đưa về"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 耐心地给我指路，还详细解释了当地的历史文化 (Kiên nhẫn chỉ đường, giải thích lịch sử văn hóa)."
            }
        ]
    },
    {
        "id": "hsk4_story_003",
        "level": "HSK4",
        "title": {
            "zh": "现代生活与环境保护",
            "vi": "Đời sống hiện đại và bảo vệ môi trường"
        },
        "topic": "environment_society",
        "topic_vi": "Môi trường & Xã hội",
        "icon": "🌱",
        "estimatedMinutes": 5,
        "description_vi": "Hành động nhỏ hàng ngày để giảm bớt rác thải và giữ gìn màu xanh cho Trái Đất.",
        "sentences": [
            ("随着经济的发展，环境保护已经成为全球的重要任务。", "Suízhe jīngjì de fāzhǎn, huánjìng bǎohù yǐjīng chéngwéi quánqiú de zhòngyào rènwù.", "Cùng với sự phát triển kinh tế, bảo vệ môi trường đã trở thành nhiệm vụ quan trọng toàn cầu."),
            ("在日常生活中，我们应该减少使用一次性塑料袋。", "Zài rìcháng shēnghuó zhōng, wǒmen yīnggāi jiǎnshǎo shǐyòng yícìxìng sùliàodài.", "Trong đời sống thường nhật, chúng ta nên giảm bớt sử dụng túi ni-lông dùng một lần."),
            ("平时出门购物，最好自己准备环保袋子。", "Píngshí chūmén gòuwù, zuì hǎo zìjǐ zhǔnbèi huánbǎo dàizi.", "Ngày thường ra ngoài mua sắm, tốt nhất nên tự chuẩn bị túi thân thiện môi trường."),
            ("垃圾分类不仅能保护森林，还能节约大量宝贵资源。", "Lājī fēnlèi bùjǐn néng bǎohù sēnlín, hái néng jiéyuē dàliàng bǎoguì zīyuán.", "Phân loại rác không chỉ bảo vệ rừng xanh mà còn tiết kiệm lượng lớn tài nguyên quý giá."),
            ("保护地球环境，是每个人都必须承担的共同责任。", "Bǎohù dìqiú huánjìng, shì měi gè rén dōu bìxū chéngdān de gòngtóng zérèn.", "Bảo vệ môi trường Trái Đất là trách nhiệm chung mà mỗi người đều phải gánh vác.")
        ],
        "spotlight": ["经济", "发展", "保护", "成为", "任务", "减少", "使用", "塑料袋", "平时", "购物", "垃圾桶", "不仅…而且…", "节约", "地球", "责任"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Bài viết khuyên nên giảm bớt thứ gì trong sinh hoạt?",
                "options_vi": ["Nước uống", "Túi ni-lông dùng một lần", "Quần áo"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 减少使用一次性塑料袋 (Giảm bớt sử dụng túi ni-lông dùng một lần)."
            },
            {
                "id": "q2",
                "question_vi": "Việc phân loại rác mang lại lợi ích gì?",
                "options_vi": ["Làm tốn thời gian", "Bảo vệ rừng xanh và tiết kiệm tài nguyên", "Không có tác dụng"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 保护森林，还能节约大量宝贵资源 (Bảo vệ rừng, tiết kiệm tài nguyên)."
            },
            {
                "id": "q3",
                "question_vi": "Bảo vệ Trái Đất là trách nhiệm của ai?",
                "options_vi": ["Chỉ của các nhà khoa học", "Trách nhiệm chung của mỗi người", "Chỉ của chính phủ"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 是每个人都必须承担的共同责任 (Là trách nhiệm chung của mỗi người)."
            }
        ]
    },
    {
        "id": "hsk4_story_004",
        "level": "HSK4",
        "title": {
            "zh": "欣赏中国传统京剧",
            "vi": "Thưởng thức nghệ thuật Kinh kịch truyền thống"
        },
        "topic": "art_culture",
        "topic_vi": "Nghệ thuật & Văn hóa",
        "icon": "🎭",
        "estimatedMinutes": 5,
        "description_vi": "Sức hấp dẫn độc đáo của nghệ thuật Kinh kịch qua trang phục, âm nhạc và vũ đạo điêu luyện.",
        "sentences": [
            ("昨天晚上，留学生朋友邀请我一起去大剧院看京剧。", "Zuótiān wǎnshang, liúxuéshēng péngyou yāoqǐng wǒ yìqǐ qù dà jùyuàn kàn jīngjù.", "Tối hôm qua, người bạn du học sinh mời tôi cùng đến đại nhà hát xem Kinh kịch."),
            ("京剧是中国著名的传统艺术，有着两百多年的历史。", "Jīngjù shì zhōngguó zhùmíng de chuántǒng yìshù, yǒu zhe liǎng bǎi duō nián de lìshǐ.", "Kinh kịch là nghệ thuật truyền thống nổi tiếng của Trung Quốc với hơn hai trăm năm lịch sử."),
            ("舞台上的演员们动作优美，衣服颜色非常丰富。", "Wǔtái shang de yǎnyuánmen dòngzuò yōuměi, yīfu yánsè fēicháng fēngfù.", "Các diễn viên trên sân khấu động tác thanh thoát, màu sắc trang phục vô cùng phong phú."),
            ("精彩的表演深深吸引了场内的所有观众。", "Jīngcǎi de biǎoyǎn shēnshēn xīyǐn le chǎng nèi de suǒyǒu guānzhòng.", "Màn biểu diễn đặc sắc đã lôi cuốn sâu sắc tất cả khán giả trong khán phòng."),
            ("这次演出让我对博大精深的中国文化产生了极大兴趣。", "Zhè cì yǎnchū ràng wǒ duì bódà-jīngshēn de zhōngguó wénhuà chǎnshēng le jídà xìngqù.", "Buổi biểu diễn lần này khiến tôi nảy sinh niềm say mê lớn với văn hóa Trung Hoa.")
        ],
        "spotlight": ["留学", "邀请", "京剧", "著名", "艺术", "演员", "动作", "丰富", "精彩", "表演", "吸引", "观众", "演出"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Kinh kịch có bề dày lịch sử khoảng bao nhiêu năm?",
                "options_vi": ["50 năm", "Hơn 200 năm", "1000 năm"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 有着两百多年的历史 (Có hơn 200 năm lịch sử)."
            },
            {
                "id": "q2",
                "question_vi": "Khán giả ấn tượng nhất với điều gì ở các diễn viên?",
                "options_vi": ["Nói chuyện hài hước", "Động tác uyển chuyển và trang phục rực rỡ phong phú", "Hát rất nhanh"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 演员们动作优美，衣服颜色非常丰富 (Diễn viên động tác đẹp, màu trang phục phong phú)."
            },
            {
                "id": "q3",
                "question_vi": "Buổi biểu diễn mang lại cảm xúc gì cho nhân vật chính?",
                "options_vi": ["Cảm thấy nhàm chán", "Nảy sinh niềm say mê lớn với văn hóa Trung Hoa", "Buồn ngủ"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 产生了极大兴趣 (Nảy sinh niềm hứng thú cực kỳ lớn)."
            }
        ]
    },
    {
        "id": "hsk4_story_005",
        "level": "HSK4",
        "title": {
            "zh": "坚持运动与健康习惯",
            "vi": "Kiên trì vận động và thói quen lành mạnh"
        },
        "topic": "health_habits",
        "topic_vi": "Sức khỏe & Rèn luyện",
        "icon": "🏃",
        "estimatedMinutes": 5,
        "description_vi": "Ý chí kiên trì vượt qua lười biếng để rèn luyện thói quen chạy bộ mỗi buổi sáng.",
        "sentences": [
            ("过去我总觉得工作太忙，几乎没有时间锻炼身体。", "Guòqù wǒ zǒng juéde gōngzuò tài máng, jīhū méiyǒu shíjiān duànliàn shēntǐ.", "Trước đây tôi luôn cảm thấy công việc quá bận, hầu như không có thời gian rèn luyện thân thể."),
            ("后来因为经常生病，我不得不改变自己的生活习惯。", "Hòulái yīnwèi jīngcháng shēngbìng, wǒ bùdébù gǎibiàn zìjǐ de shēnghuó xíguàn.", "Về sau do thường xuyên đổ bệnh, tôi bất đắc dĩ phải thay đổi thói quen sinh hoạt."),
            ("每天早晨六点半，我按时起床去公园慢跑半小时。", "Měitiān zǎochén liù diǎn bàn, wǒ ànshí qǐchuáng qù gōngyuán mànpǎo bàn xiǎoshí.", "Mỗi buổi sáng sáu giờ rưỡi, tôi đúng giờ thức dậy ra công viên chạy bộ nửa tiếng."),
            ("坚持了三个月以后，我的体重减轻了，精神也好了很多。", "Jiānchí le sān gè yuè yǐhòu, wǒ de tǐzhòng jiǎnqīng le, jīngshén yě hǎo le hěn duō.", "Sau khi kiên trì suốt ba tháng, cân nặng của tôi đã giảm, tinh thần cũng tốt hơn nhiều."),
            ("只要有恒心，保持健康并不是一件困难的事情。", "Zhǐyào yǒu héngxīn, bǎochí jiànkāng bìng bú shì yí jiàn kùnnan de shìqing.", "Chỉ cần có lòng kiên định, giữ gìn sức khỏe hoàn toàn không phải việc khó khăn.")
        ],
        "spotlight": ["几乎", "锻炼", "经常", "后来", "不得不", "改变", "习惯", "按时", "坚持", "精神", "只要…就…", "困难"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Lý do gì khiến nhân vật chính quyết định thay đổi thói quen?",
                "options_vi": ["Vì có nhiều tiền", "Vì thường xuyên đau ốm", "Vì bạn bè rủ rê"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 因为经常生病，我不得不改变自己的生活习惯 (Do thường bị ốm, tôi buộc phải thay đổi thói quen)."
            },
            {
                "id": "q2",
                "question_vi": "Nhân vật chính chạy bộ vào khung giờ nào mỗi ngày?",
                "options_vi": ["Trưa 12 giờ", "Sáng 6 giờ rưỡi", "Tối 9 giờ"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 每天早晨六点半，我按时起床去公园慢跑 (Mỗi sáng 6h30 tôi đúng giờ thức dậy chạy bộ)."
            },
            {
                "id": "q3",
                "question_vi": "Sau 3 tháng kiên trì, kết quả đạt được là gì?",
                "options_vi": ["Cân nặng giảm và tinh thần sảng khoái hơn nhiều", "Bị ốm nặng hơn", "Không có thay đổi gì"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 体重减轻了，精神也好了很多 (Cân nặng giảm, tinh thần tốt hơn rất nhiều)."
            }
        ]
    },
    {
        "id": "hsk4_story_006",
        "level": "HSK4",
        "title": {
            "zh": "签订租房合同",
            "vi": "Ký kết hợp đồng thuê nhà"
        },
        "topic": "life_skills",
        "topic_vi": "Kỹ năng sống & Pháp lý",
        "icon": "📝",
        "estimatedMinutes": 5,
        "description_vi": "Kiểm tra kỹ lưỡng các điều khoản hợp đồng thuê nhà để đảm bảo an toàn và quyền lợi cá nhân.",
        "sentences": [
            ("为了离公司更近一些，我和朋友打算重新租一套公寓。", "Wèile lí gōngsī gèng jìn yìxiē, wǒ hé péngyou dǎsuàn chóngxīn zū yí tào gōngyù.", "Để ở gần công ty hơn, tôi và bạn dự định thuê lại một căn hộ chung cư."),
            ("昨天下午，房东带我们详细参观了房间的客厅和厨房。", "Zuótiān xiàwǔ, fángdōng dài wǒmen xiángxì cānguān le fángjiān de kètīng hé chúfáng.", "Chiều hôm qua, chủ nhà đưa chúng tôi đi xem kỹ phòng khách và phòng bếp."),
            ("这里的家具齐全，卫生间也很干净，条件完全符合我们的要求。", "Zhèlǐ de jiājù qíquán, wèishēngjiān yě hěn gānjìng, tiáojiàn wánquán fúhé wǒmen de yāoqiú.", "Nội thất ở đây đầy đủ, nhà vệ sinh sạch sẽ, điều kiện hoàn toàn khớp yêu cầu."),
            ("签字之前，我们仔细阅读了合同上的每一个关键条款。", "Qiānzì zhīqián, wǒmen zǐxì yuèdú le hétong shang de měi yí gè guānjiàn tiáokuǎn.", "Trước khi ký tên, chúng tôi đọc kỹ từng điều khoản then chốt trong hợp đồng."),
            ("双方同意后顺利付款，下周就可以正式搬进来了。", "Shuāngfāng tóngyì hòu shùnlì fùkuǎn, xià zhōu jiù kěyǐ zhèngshì bān jìnlái le.", "Hai bên thống nhất sau đó thanh toán thuận lợi, tuần sau có thể chính thức dọn vào.")
        ],
        "spotlight": ["重新", "租", "房东", "详细", "参观", "客厅", "厨房", "家具", "卫生间", "完全", "符合", "仔细", "阅读", "关键", "付款", "正式"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Lý do hai bạn muốn thuê nhà mới là gì?",
                "options_vi": ["Để ở gần công ty hơn", "Để mở cửa hàng", "Để nuôi thú cưng"],
                "answer": 0,
                "explanation_vi": "Trong câu đầu có viết: 为了离公司更近一些 (Để ở gần công ty hơn)."
            },
            {
                "id": "q2",
                "question_vi": "Họ đánh giá căn hộ thế nào sau khi đi xem phòng?",
                "options_vi": ["Rất bẩn và thiếu thốn", "Đầy đủ nội thất, sạch sẽ và phù hợp yêu cầu", "Quá đắt đỏ"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 家具齐全，卫生间也很干净，条件完全符合要求 (Đồ đạc đầy đủ, vệ sinh sạch sẽ, đáp ứng yêu cầu)."
            },
            {
                "id": "q3",
                "question_vi": "Họ đã làm gì trước khi đặt bút ký hợp đồng?",
                "options_vi": ["Đi ngủ", "Đọc kỹ từng điều khoản then chốt", "Không đọc gì cả"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 仔细阅读了合同上的每一个关键条款 (Đọc kỹ từng điều khoản then chốt trên hợp đồng)."
            }
        ]
    },
    {
        "id": "hsk4_story_007",
        "level": "HSK4",
        "title": {
            "zh": "朋友间的理解与包容",
            "vi": "Sự thấu hiểu và bao dung giữa bạn bè"
        },
        "topic": "interpersonal_relation",
        "topic_vi": "Tình bạn & Ứng xử",
        "icon": "💬",
        "estimatedMinutes": 5,
        "description_vi": "Cách giải quyết hiểu lầm chân thành giúp tình bạn càng thêm gắn bó và bền chặt.",
        "sentences": [
            ("上个星期，我和最好的朋友之间发生了一点儿误会。", "Shàng gè xīngqī, wǒ hé zuì hǎo de péngyou zhījiān fāshēng le yìdiǎnr wùhuì.", "Tuần trước, giữa tôi và người bạn thân nhất đã nảy sinh một chút hiểu lầm."),
            ("因为缺少及时的交流沟通，两个人一连几天都不说话。", "Yīnwèi quēshǎo jíshí de jiāoliú gōutōng, liǎng gè rén yìlián jǐ tiān dōu bù shuōhuà.", "Do thiếu đi sự trao đổi kịp thời, cả hai người mấy ngày liền không nói chuyện."),
            ("后来我觉得很后悔，主动约他出来面对面谈心。", "Hòulái wǒ juéde hěn hòuhuǐ, zhǔdòng yuē tā chūlái miànduìmiàn tánxīn.", "Về sau tôi thấy rất hối hận, chủ động hẹn cậu ấy ra mặt đối mặt tâm sự."),
            ("我们诚实地把心里的想法讲出来，误会立刻解除了。", "Wǒmen chéngshí de bǎ xīnlǐ de xiǎngfǎ jiǎng chūlái, wùhuì lìkè jiěchú le.", "Chúng tôi chân thành nói ra suy nghĩ trong lòng, hiểu lầm lập tức được xóa bỏ."),
            ("真正的友谊需要互相尊重和包容，这让我更加珍惜这段感情。", "Zhēnzhèng de yǒuyì xūyào hùxiāng zūnzhòng hé bāoróng, zhè ràng wǒ gèngjiā zhēnxī zhè duàn gǎnqíng.", "Tình bạn thực sự cần sự tôn trọng và bao dung lẫn nhau, điều này khiến tôi càng trân quý tình bạn.")
        ],
        "spotlight": ["发生", "误会", "缺少", "及时", "交流", "后来", "后悔", "主动", "诚实", "真正", "友谊", "互相", "尊重", "感情"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nguyên nhân khiến hai người không nói chuyện mấy ngày là gì?",
                "options_vi": ["Bị mất đồ", "Thiếu sự trao đổi kịp thời dẫn đến hiểu lầm", "Không thích nhau nữa"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 因为缺少及时的交流沟通 (Vì thiếu sự giao lưu trao đổi kịp thời)."
            },
            {
                "id": "q2",
                "question_vi": "Ai là người chủ động hẹn gặp để giải quyết khúc mắc?",
                "options_vi": ["Người thứ ba", "Nhân vật chính cảm thấy hối hận và chủ động hẹn gặp", "Không ai cả"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 我觉得很后悔，主动约他出来面对面谈心 (Tôi thấy hối hận, chủ động hẹn cậu ấy ra nói chuyện)."
            },
            {
                "id": "q3",
                "question_vi": "Theo câu chuyện, tình bạn chân chính cần điều gì nhất?",
                "options_vi": ["Nhiều tiền bạc", "Sự tôn trọng và bao dung lẫn nhau", "Sự im lặng"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 真正的友谊需要互相尊重和包容 (Tình bạn thực sự cần tôn trọng và bao dung lẫn nhau)."
            }
        ]
    },
    {
        "id": "hsk4_story_008",
        "level": "HSK4",
        "title": {
            "zh": "健康饮食与科学减压",
            "vi": "Ăn uống lành mạnh và giảm stress khoa học"
        },
        "topic": "wellness_nutrition",
        "topic_vi": "Sức khỏe & Ẩm thực",
        "icon": "🥗",
        "estimatedMinutes": 5,
        "description_vi": "Bí quyết cân bằng giữa áp lực công việc bận rộn và chế độ dinh dưỡng giàu chất xơ.",
        "sentences": [
            ("现代人的生活节奏很快，经常面临着巨大的压力。", "Xiàndàirén de shēnghuó jiézòu hěn kuài, jīngcháng miànlín zhe jùdà de yālì.", "Nhịp sống của con người hiện đại rất nhanh, thường xuyên đối mặt áp lực to lớn."),
            ("如果不重视营养健康，身体就会容易出现各种毛病。", "Rúguǒ bú zhòngshì yíngyǎng jiànkāng, shēntǐ jiù huì róngyì chūxiàn gèzhǒng máobìng.", "Nếu không coi trọng dinh dưỡng sức khỏe, cơ thể sẽ dễ xuất hiện đủ thứ bệnh tật."),
            ("医生建议我们平时多吃新鲜蔬菜和水果，少吃油腻食物。", "Yīshēng jiànyì wǒmen píngshí duō chī xīnxian shūcài hé shuǐguǒ, shǎo chī yóunì shíwù.", "Bác sĩ khuyên chúng ta nên ăn nhiều rau củ và hoa quả tươi, ít ăn đồ dầu mỡ."),
            ("同时，保证充足的睡眠和适当放松也是减压的好方法。", "Tóngshí, bǎozhèng chōngzú de shuìmián hé shìdàng fàngsōng yě shì jiǎnyā de hǎo fāngfǎ.", "Đồng thời, đảm bảo ngủ đủ giấc và thư giãn hợp lý cũng là biện pháp giảm áp lực tốt."),
            ("保持良好的心情，才能积极面对生活中的各种挑战。", "Bǎochí liánghǎo de xīnqíng, cái néng jījí miànduì shēnghuó zhōng de gèzhǒng tiǎozhàn.", "Giữ cho tâm trạng tươi vui, mới có thể tích cực đối mặt mọi thử thách cuộc sống.")
        ],
        "spotlight": ["经常", "压力", "如果", "重视", "出现", "建议", "平时", "新鲜", "同时", "保证", "放松", "方法", "心情", "积极"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Bác sĩ khuyên chúng ta nên có thói quen ăn uống như thế nào?",
                "options_vi": ["Ăn nhiều đồ ngọt", "Ăn nhiều rau tươi và hoa quả, giảm đồ dầu mỡ", "Bỏ bữa sáng"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 多吃新鲜蔬菜和水果，少吃油腻食物 (Ăn nhiều rau quả tươi, ít ăn dầu mỡ)."
            },
            {
                "id": "q2",
                "question_vi": "Phương pháp giảm áp lực tốt được nhắc đến là gì?",
                "options_vi": ["Uống cà phê liên tục", "Đảm bảo ngủ đủ giấc và thư giãn thích hợp", "Làm việc thâu đêm"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 保证充足的睡眠和适当放松也是减压的好方法 (Đảm bảo ngủ đủ giấc và thư giãn là cách tốt)."
            },
            {
                "id": "q3",
                "question_vi": "Lợi ích của việc giữ gìn tâm trạng tốt là gì?",
                "options_vi": ["Có thể tích cực đối mặt mọi thử thách", "Không cần làm việc nữa", "Luôn may mắn"],
                "answer": 0,
                "explanation_vi": "Trong câu cuối có viết: 保持良好的心情，才能积极面对生活中的各种挑战 (Giữ tâm trạng tốt mới có thể đối diện thử thách)."
            }
        ]
    },
    {
        "id": "hsk4_story_009",
        "level": "HSK4",
        "title": {
            "zh": "关于成功的思考",
            "vi": "Những suy ngẫm về thành công"
        },
        "topic": "philosophy_mindset",
        "topic_vi": "Tư duy & Thành công",
        "icon": "💡",
        "estimatedMinutes": 5,
        "description_vi": "Thất bại là mẹ thành công: Tích lũy kinh nghiệm và giữ vững niềm tin trên đường đời.",
        "sentences": [
            ("许多人都希望自己能早日取得令人羡慕的成功。", "Xǔduō rén dōu xīwàng zìjǐ néng zǎorì qǔdé lìngrén-xiànmù de chénggōng.", "Nhiều người đều mong bản thân có thể sớm ngày gặt hái thành công đáng ngưỡng mộ."),
            ("然而在追求理想的过程中，谁都有可能遇到挫折和失败。", "Rán'ér zài zhuīqiú lǐxiǎng de guòchéng zhōng, shéi dōu yǒu kěnéng yù dào cuòzhé hé shībài.", "Thế nhưng trong quá trình theo đuổi lý tưởng, ai cũng có thể gặp trắc trở và thất bại."),
            ("真正聪明的人，懂得从错误中总结经验教训。", "Zhēnzhèng cōngming de rén, dǒngde cóng cuòwù zhōng zǒngjié jīngyàn jiàoxùn.", "Người thực sự thông minh là người biết đúc kết kinh nghiệm bài học từ sai lầm."),
            ("只要不轻言放弃，每一次困难都是提升能力的绝好机会。", "Zhǐyào bù qīngyán fàngqì, měi yí cì kùnnan dōu shì tíshēng nénglì de juéhǎo jīhuì.", "Chỉ cần không dễ dàng bỏ cuộc, mỗi lần khó khăn đều là cơ hội tuyệt vời để nâng cao năng lực."),
            ("坚定的态度和长期的努力，才是通向成功唯一的钥匙。", "Jiāndìng de tàidu hé chángqī de nǔlì, cái shì tōng xiàng chénggōng wéiyī de yàoshi.", "Thái độ kiên định và nỗ lực lâu dài mới là chiếc chìa khóa duy nhất dẫn tới thành công.")
        ],
        "spotlight": ["许多", "希望", "成功", "然而", "理想", "过程", "可能", "失败", "真正", "聪明", "错误", "总结", "经验", "放弃", "能力", "机会", "态度", "钥匙"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Trong quá trình theo đuổi lý tưởng, điều gì ai cũng có thể gặp phải?",
                "options_vi": ["Trắc trở và thất bại", "Sự giàu có ngay lập tức", "Không có khó khăn nào"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 谁都有可能遇到挫折和失败 (Ai cũng có thể gặp trắc trở và thất bại)."
            },
            {
                "id": "q2",
                "question_vi": "Người thực sự thông minh sẽ làm gì khi mắc sai lầm?",
                "options_vi": ["Trốn tránh", "Đúc kết bài học kinh nghiệm từ sai lầm", "Đổ lỗi cho người khác"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 懂得从错误中总结经验教训 (Biết đúc kết kinh nghiệm bài học từ sai lầm)."
            },
            {
                "id": "q3",
                "question_vi": "Yếu tố cốt lõi nào là chìa khóa dẫn tới thành công?",
                "options_vi": ["May mắn ngẫu nhiên", "Thái độ kiên định và sự nỗ lực bền bỉ", "Dựa dẫm vào người khác"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 坚定的态度和长期的努力，才是通向成功唯一的钥匙 (Thái độ kiên định và nỗ lực lâu dài là chìa khóa)."
            }
        ]
    },
    {
        "id": "hsk4_story_010",
        "level": "HSK4",
        "title": {
            "zh": "中国茶道与待客之礼",
            "vi": "Trà đạo Trung Hoa và lễ nghi đãi khách"
        },
        "topic": "culture_etiquette",
        "topic_vi": "Văn hóa & Lễ nghi",
        "icon": "🍵",
        "estimatedMinutes": 5,
        "description_vi": "Nét đẹp tinh tế của văn hóa trà đạo và sự tôn trọng khách quý trong nếp sống phương Đông.",
        "sentences": [
            ("在中国传统文化中，请客人喝茶是一种非常重要的礼貌。", "Zài zhōngguó chuántǒng wénhuà zhōng, qǐng kèrén hē chá shì yì zhǒng fēicháng zhòngyào de lǐmào.", "Trong văn hóa truyền thống Trung Hoa, mời khách uống trà là một phép lịch sự vô cùng quan trọng."),
            ("泡茶的师傅动作十分熟练，每一步都严格按照规矩进行。", "Pào chá de shīfu dòngzuò shífēn shúliàn, měi yí bù dōu yángé ànzhào guīju jìnxíng.", "Người nghệ nhân pha trà động tác rất thành thục, mỗi bước đều nghiêm ngặt làm theo quy tắc."),
            ("刚泡好的茶水香气扑鼻，味道稍微带有一点儿苦味，但回味甘甜。", "Gāng pào hǎo de cháshuǐ xiāngqì pūbí, wèidào shāowēi dài yǒu yìdiǎnr kǔwèi, dàn huíwèi gāntián.", "Nước trà mới pha tỏa hương thơm ngát, vị hơi đắng một chút nhưng hậu vị ngọt ngào."),
            ("大家一边品尝香浓的清茶，一边轻松愉快地谈论生活。", "Dàjiā yìbiān pǐncháng xiāngnóng de qīngchá, yìbiān qīngsōng yúkuài de tánlùn shēnghuó.", "Mọi người vừa thưởng thức trà thơm, vừa thoải mái vui vẻ bàn luận chuyện đời."),
            ("小小的茶杯里，蕴含着中国人对自然与和谐的深刻理解。", "Xiǎoxiǎo de chábēi lǐ, yùnhán zhe zhōngguórén duì zìrán yǔ héxié de shēnkè lǐjiě.", "Trong chén trà nhỏ nhắn, ẩn chứa sự thấu hiểu sâu sắc của người Trung Quốc về tự nhiên và hòa hợp.")
        ],
        "spotlight": ["传统", "文化", "礼貌", "师傅", "动作", "十分", "严格", "按照", "规矩", "进行", "味道", "稍微", "苦", "品尝", "轻松", "愉快", "理解"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Trong văn hóa Trung Hoa, hành động mời khách uống trà thể hiện điều gì?",
                "options_vi": ["Sự khoe khoang", "Một phép lịch sự hết sức quan trọng", "Sự ép buộc"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 请客人喝茶是一种非常重要的礼貌 (Mời khách uống trà là phép lịch sự quan trọng)."
            },
            {
                "id": "q2",
                "question_vi": "Hương vị của tách trà vừa pha xong được miêu tả thế nào?",
                "options_vi": ["Rất chua", "Thơm ngát, hơi đắng nhẹ nhưng hậu vị ngọt", "Không có mùi vị"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 香气扑鼻，味道稍微带有一点儿苦味，但回味甘甜 (Thơm ngát, vị hơi đắng nhưng hậu vị ngọt)."
            },
            {
                "id": "q3",
                "question_vi": "Chén trà nhỏ ẩn chứa triết lý gì của người Trung Hoa?",
                "options_vi": ["Sự giàu sang", "Sự thấu hiểu sâu sắc về tự nhiên và hòa hợp", "Chiến tranh"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 蕴含着中国人对自然与和谐的深刻理解 (Ẩn chứa sự thấu hiểu sâu sắc về tự nhiên và hòa hợp)."
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
                "lifestyle_leisure": "Thư giãn & Đời sống",
                "housing_lifestyle": "Nhà cửa & Đời sống",
                "nature_outdoors": "Thiên nhiên & Ngoài trời",
                "study_learning": "Học tập & Tri thức",
                "urban_life": "Đô thị & Đi lại",
                "competition_achievement": "Thi cử & Thành tích",
                "shopping_daily": "Mua sắm & Đời sống",
                "health_recovery": "Sức khỏe & Chăm sóc",
                "family_love": "Gia đình & Tình thân",
                "seasons_weather": "Bốn mùa & Thiên nhiên",
                "friendship_culture": "Tình bạn & Văn hóa",
                "career_growth": "Sự nghiệp & Việc làm",
                "travel_adventure": "Du lịch & Trải nghiệm",
                "environment_society": "Môi trường & Xã hội",
                "art_culture": "Nghệ thuật & Văn hóa",
                "health_habits": "Sức khỏe & Rèn luyện",
                "life_skills": "Kỹ năng sống & Pháp lý",
                "interpersonal_relation": "Tình bạn & Ứng xử",
                "wellness_nutrition": "Sức khỏe & Ẩm thực",
                "philosophy_mindset": "Tư duy & Thành công",
                "culture_etiquette": "Văn hóa & Lễ nghi"
            }

            icon_map = {
                "hsk1_story_001": "☀️", "hsk1_story_002": "🐱", "hsk1_story_003": "🍎",
                "hsk1_story_004": "🏫", "hsk1_story_005": "🍵", "hsk1_story_006": "👧",
                "hsk1_story_007": "🍜", "hsk1_story_008": "👗", "hsk1_story_009": "🌧️",
                "hsk1_story_010": "✈️",
                "hsk2_story_001": "🏥", "hsk2_story_002": "🏀", "hsk2_story_003": "🚆",
                "hsk2_story_004": "🐶", "hsk2_story_005": "🏨", "hsk2_story_006": "⌚",
                "hsk2_story_007": "💼", "hsk2_story_008": "🍉", "hsk2_story_009": "🌟",
                "hsk2_story_010": "☕",
                "hsk3_story_001": "🏠", "hsk3_story_002": "⛰️", "hsk3_story_003": "📚",
                "hsk3_story_004": "🚇", "hsk3_story_005": "🏆", "hsk3_story_006": "🛒",
                "hsk3_story_007": "🤒", "hsk3_story_008": "🎂", "hsk3_story_009": "🌸",
                "hsk3_story_010": "🤝",
                "hsk4_story_001": "🎓", "hsk4_story_002": "🎒", "hsk4_story_003": "🌱",
                "hsk4_story_004": "🎭", "hsk4_story_005": "🏃", "hsk4_story_006": "📝",
                "hsk4_story_007": "💬", "hsk4_story_008": "🥗", "hsk4_story_009": "💡",
                "hsk4_story_010": "🍵"
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

    def sort_key(item):
        lvl_num = int("".join([c for c in item["level"] if c.isdigit()]) or "1")
        return (lvl_num, item["id"])

    manifest_entries.sort(key=sort_key)
    manifest_path = READINGS_DIR / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, ensure_ascii=False, indent=2)
    print(f"[✓] Updated manifest.json with {len(manifest_entries)} total entries.")

def main():
    hsk4_dir = READINGS_DIR / "hsk4"
    hsk4_dir.mkdir(parents=True, exist_ok=True)

    generated_count = 0
    for sdata in STORIES_HSK4:
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
                if len(spotlight_ids) >= 12:
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

        out_path = hsk4_dir / f"{sid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(story_obj, f, ensure_ascii=False, indent=2)

        print(f"[✓] Generated {sid} -> {out_path.name} ({len(sentences_json)} sentences, {len(spotlight_ids)} spotlight words)")
        generated_count += 1

    print(f"\nSuccessfully generated {generated_count} HSK4 stories.")
    update_manifest()

if __name__ == "__main__":
    main()
