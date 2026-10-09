#!/usr/bin/env python3
"""
tools/generate_hsk3_stories.py
Generates 10 HSK3 Graded Reading stories and updates manifest.json.
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

# 10 HSK3 Stories Definitions
STORIES_HSK3 = [
    {
        "id": "hsk3_story_001",
        "level": "HSK3",
        "title": {
            "zh": "搬到新家",
            "vi": "Chuyển đến nhà mới"
        },
        "topic": "housing_lifestyle",
        "topic_vi": "Nhà cửa & Đời sống",
        "icon": "🏠",
        "estimatedMinutes": 4,
        "description_vi": "Trải nghiệm chuyển sang một căn nhà mới yên tĩnh và gần trạm tàu điện ngầm.",
        "sentences": [
            ("上个周末，我和家人搬到了新房子。", "Shàng gè zhōumò, wǒ hé jiārén bān dào le xīn fángzi.", "Cuối tuần trước, tôi và gia đình đã chuyển đến căn nhà mới."),
            ("这里的环境很好，周围非常安静。", "Zhèlǐ de huánjìng hěn hǎo, zhōuwéi fēicháng ānjìng.", "Môi trường ở đây rất tốt, xung quanh vô cùng yên tĩnh."),
            ("新房子离地铁站很近，交通特别方便。", "Xīn fángzi lí dìtiězhàn hěn jìn, jiāotōng tèbié fāngbiàn.", "Nhà mới cách trạm tàu điện ngầm rất gần, giao thông đặc biệt thuận tiện."),
            ("我们的邻居也很热情，经常过来帮忙。", "Wǒmen de línjū yě hěn rèqíng, jīngcháng guòlái bāngmáng.", "Hàng xóm của chúng tôi cũng rất nhiệt tình, thường qua giúp đỡ."),
            ("大家一起把房间打扫得干干净净。", "Dàjiā yìqǐ bǎ fángjiān dǎsǎo de gāngānjìngjìng.", "Mọi người cùng nhau dọn dẹp phòng ốc sạch sẽ tinh tươm.")
        ],
        "spotlight": ["周末", "搬", "环境", "安静", "地铁", "特别", "方便", "邻居", "热情", "帮忙", "干净"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Gia đình nhân vật chính đã làm gì vào cuối tuần trước?",
                "options_vi": ["Đi du lịch xa", "Chuyển đến nhà mới", "Đi mua sắm"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 搬到了新房子 (Đã chuyển đến căn nhà mới)."
            },
            {
                "id": "q2",
                "question_vi": "Vị trí của ngôi nhà mới có ưu điểm gì?",
                "options_vi": ["Gần sân bay", "Gần trạm tàu điện ngầm, đi lại tiện lợi", "Ở nông thôn"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 离地铁站很近，交通特别方便 (Cách trạm tàu điện ngầm rất gần, giao thông đặc biệt thuận tiện)."
            },
            {
                "id": "q3",
                "question_vi": "Những người hàng xóm ở đây như thế nào?",
                "options_vi": ["Khó tính", "Nhiệt tình và thường sang giúp đỡ", "Không tiếp xúc"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 邻居也很热情，经常过来帮忙 (Hàng xóm rất nhiệt tình, thường qua giúp đỡ)."
            }
        ]
    },
    {
        "id": "hsk3_story_002",
        "level": "HSK3",
        "title": {
            "zh": "周末去爬山",
            "vi": "Cuối tuần đi leo núi"
        },
        "topic": "nature_outdoors",
        "topic_vi": "Thiên nhiên & Ngoài trời",
        "icon": "⛰️",
        "estimatedMinutes": 4,
        "description_vi": "Chuyến dã ngoại leo núi cùng bạn bè ngắm nhìn phong cảnh và chụp ảnh kỷ niệm.",
        "sentences": [
            ("今天天气晴朗，我和朋友决定去爬山。", "Jīntiān tiānqì qínglǎng, wǒ hé péngyou juédìng qù páshān.", "Hôm nay thời tiết nắng ráo, tôi và bạn bè quyết định đi leo núi."),
            ("山上的空气非常新鲜，树木很绿。", "Shān shang de kōngqì fēicháng xīnxian, shùmù hěn lǜ.", "Không khí trên núi vô cùng trong lành, cây cối xanh tươi."),
            ("我们带了照相机，拍了许多美丽的照片。", "Wǒmen dài le zhàoxiàngjī, pāi le xǔduō měilì de zhàopiàn.", "Chúng tôi mang theo máy ảnh, chụp rất nhiều bức ảnh đẹp."),
            ("虽然爬到了山顶很累，但是风景极了。", "Suīrán pá dào le shāndǐng hěn lèi, dànshì fēngjǐng jí le.", "Tuy leo lên đến đỉnh núi rất mệt, nhưng phong cảnh tuyệt vời."),
            ("运动让我们感到很健康，很快乐。", "Yùndòng ràng wǒmen gǎndào hěn jiànkāng, hěn kuàilè.", "Vận động làm cho chúng tôi cảm thấy rất khỏe khoắn và vui vẻ.")
        ],
        "spotlight": ["决定", "爬山", "空气", "新鲜", "绿", "照相机", "照片", "累", "极", "健康", "快乐"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Nhóm bạn quyết định làm gì vào ngày thời tiết đẹp?",
                "options_vi": ["Ở nhà xem phim", "Đi leo núi", "Đi bơi"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 决定去爬山 (Quyết định đi leo núi)."
            },
            {
                "id": "q2",
                "question_vi": "Họ đã mang theo đồ vật gì để lưu giữ kỷ niệm?",
                "options_vi": ["Sách vở", "Máy ảnh để chụp ảnh", "Đồng hồ"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 带了照相机，拍了许多美丽的照片 (Mang máy ảnh, chụp nhiều bức ảnh đẹp)."
            },
            {
                "id": "q3",
                "question_vi": "Cảm giác của họ khi leo lên đỉnh núi như thế nào?",
                "options_vi": ["Mệt nhưng thấy phong cảnh cực kỳ đẹp", "Thất vọng", "Muốn về ngay"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 虽然爬到了山顶很累，但是风景极了 (Tuy mệt nhưng phong cảnh tuyệt đẹp)."
            }
        ]
    },
    {
        "id": "hsk3_story_003",
        "level": "HSK3",
        "title": {
            "zh": "在图书馆借书",
            "vi": "Mượn sách ở thư viện"
        },
        "topic": "study_learning",
        "topic_vi": "Học tập & Tri thức",
        "icon": "📚",
        "estimatedMinutes": 4,
        "description_vi": "Tìm kiếm tài liệu và sách lịch sử Trung Quốc để nâng cao trình độ tiếng Hán.",
        "sentences": [
            ("大学里的图书馆又大又安静。", "Dàxué lǐ de túshūguǎn yòu dà yòu ānjìng.", "Thư viện trong trường đại học vừa to lớn vừa yên tĩnh."),
            ("为了提高汉语水平，我常常来这里看书。", "Wèile tígāo hànyǔ shuǐpíng, wǒ chángcháng lái zhèlǐ kàn shū.", "Để nâng cao trình độ tiếng Hán, tôi thường đến đây đọc sách."),
            ("今天我借了两本关于中国历史的书。", "Jīntiān wǒ jiè le liǎng běn guānyú zhōngguó lìshǐ de shū.", "Hôm nay tôi mượn hai cuốn sách viết về lịch sử Trung Quốc."),
            ("图书馆阿姨告诉我：一个月之内必须还书。", "Túshūguǎn āyí gàosu wǒ: Yí gè yuè zhī nèi bìxū huán shū.", "Cô thủ thư dặn tôi: Trong vòng một tháng phải trả sách."),
            ("认真阅读能让我们学到很多新知识。", "Rènzhēn yuèdú néng ràng wǒmen xué dào hěn duō xīn zhīshi.", "Đọc sách chăm chỉ giúp chúng ta học thêm nhiều kiến thức mới.")
        ],
        "spotlight": ["图书馆", "安静", "为了", "提高", "水平", "借", "关于", "历史", "阿姨", "必须", "还", "认真"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Mục đích nhân vật chính đến thư viện đọc sách là gì?",
                "options_vi": ["Để ngủ trưa", "Để nâng cao trình độ tiếng Hán", "Để tìm bạn chơi"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 为了提高汉语水平 (Để nâng cao trình độ tiếng Hán)."
            },
            {
                "id": "q2",
                "question_vi": "Hôm nay nhân vật chính mượn sách về chủ đề gì?",
                "options_vi": ["Toán học", "Nấu ăn", "Lịch sử Trung Quốc"],
                "answer": 2,
                "explanation_vi": "Trong bài có câu: 关于中国历史的书 (Sách về lịch sử Trung Quốc)."
            },
            {
                "id": "q3",
                "question_vi": "Thời hạn mượn sách là bao lâu?",
                "options_vi": ["Một tuần", "Một tháng", "Một năm"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 一个月之内必须还书 (Trong vòng một tháng phải trả sách)."
            }
        ]
    },
    {
        "id": "hsk3_story_004",
        "level": "HSK3",
        "title": {
            "zh": "第一次坐地铁",
            "vi": "Lần đầu đi tàu điện ngầm"
        },
        "topic": "urban_life",
        "topic_vi": "Đô thị & Đi lại",
        "icon": "🚇",
        "estimatedMinutes": 4,
        "description_vi": "Trải nghiệm phương tiện giao thông công cộng hiện đại và nhanh chóng trong thành phố.",
        "sentences": [
            ("北京的地铁网络非常大，到哪里都方便。", "Běijīng de dìtiě wǎngluò fēicháng dà, dào nǎlǐ dōu fāngbiàn.", "Mạng lưới tàu điện ngầm Bắc Kinh rất lớn, đi đâu cũng thuận tiện."),
            ("今天是我第一次自己坐地铁去火车站。", "Jīntiān shì wǒ dì-yī cì zìjǐ zuò dìtiě qù huǒchēzhàn.", "Hôm nay là lần đầu tiên tôi tự mình đi tàu điện ngầm ra ga tàu."),
            ("地铁站里有很多人，大家都在排队刷卡。", "Dìtiězhàn lǐ yǒu hěn duō rén, dàjiā dōu zài páiduì shuākǎ.", "Trong ga tàu có rất đông người, mọi người đều xếp hàng quẹt thẻ."),
            ("地铁跑得极快，而且从来不堵车。", "Dìtiě pǎo de jí kuài, érqiě cónglái bù dǔchē.", "Tàu điện chạy cực nhanh, hơn nữa không bao giờ bị tắc đường."),
            ("只用了二十分钟，我就顺利到达了目的地。", "Zhǐ yòng le èrshí fēnzhōng, wǒ jiù shùnlì dàodá le mùdìdì.", "Chỉ mất có hai mươi phút, tôi đã thuận lợi đến nơi.")
        ],
        "spotlight": ["地铁", "方便", "自己", "火车站", "极", "快", "经过", "到", "用"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Hôm nay nhân vật chính tự mình đi đâu bằng tàu điện ngầm?",
                "options_vi": ["Đi sân bay", "Đi ga tàu hỏa", "Đi bệnh viện"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 自己坐地铁去火车站 (Tự đi tàu điện ngầm ra ga tàu hỏa)."
            },
            {
                "id": "q2",
                "question_vi": "Đi tàu điện ngầm có ưu điểm gì nổi bật?",
                "options_vi": ["Rất chậm", "Cực kỳ nhanh và không bị tắc đường", "Rất đắt đỏ"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 地铁跑得极快，而且从来不堵车 (Chạy cực nhanh và không tắc đường)."
            },
            {
                "id": "q3",
                "question_vi": "Chuyến đi mất bao nhiêu thời gian?",
                "options_vi": ["Hai mươi phút", "Một tiếng", "Hai tiếng"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 只用了二十分钟 (Chỉ mất có hai mươi phút)."
            }
        ]
    },
    {
        "id": "hsk3_story_005",
        "level": "HSK3",
        "title": {
            "zh": "参加汉语演讲比赛",
            "vi": "Tham gia cuộc thi hùng biện tiếng Hán"
        },
        "topic": "competition_achievement",
        "topic_vi": "Thi cử & Thành tích",
        "icon": "🏆",
        "estimatedMinutes": 4,
        "description_vi": "Nỗ lực tập luyện chăm chỉ và niềm vui khi hoàn thành xuất sắc bài thi hùng biện.",
        "sentences": [
            ("上个星期五，我参加了学校的汉语比赛。", "Shàng gè xīngqīwǔ, wǒ cānjiā le xuéxiào de hànyǔ bǐsài.", "Thứ Sáu tuần trước, tôi đã tham gia cuộc thi tiếng Hán của trường."),
            ("上台之前，我心里有点儿担心和害怕。", "Shàngtái zhīqián, wǒ xīnlǐ yǒudiǎnr dānxīn hé hàipà.", "Trước khi lên sân khấu, trong lòng tôi có chút lo lắng và sợ hãi."),
            ("老师微笑着鼓励我：相信自己，你准备得很充分！", "Lǎoshī wēixiào zhe gǔlì wǒ: Xiāngxìn zìjǐ, nǐ zhǔnbèi de hěn chōngfèn!", "Thầy giáo mỉm cười động viên tôi: Hãy tin vào chính mình, em chuẩn bị rất kỹ!"),
            ("我认真地讲完了关于我的中国故事。", "Wǒ rènzhēn de jiǎng wán le guānyú wǒ de zhōngguó gùshi.", "Tôi chăm chú kể xong câu chuyện Trung Quốc của mình."),
            ("大家为我热烈鼓掌，我拿到了最好的成绩。", "Dàjiā wèi wǒ rèliè gǔzhǎng, wǒ ná dào le zuì hǎo de chéngjì.", "Mọi người nhiệt liệt vỗ tay, tôi đã đạt được thành tích xuất sắc nhất.")
        ],
        "spotlight": ["参加", "比赛", "担心", "害怕", "相信", "自己", "准备", "认真", "完", "关于", "故事", "拿"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Trước khi lên sân khấu, tâm trạng nhân vật chính như thế nào?",
                "options_vi": ["Rất tự tin", "Có chút lo lắng và sợ hãi", "Buồn ngủ"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 我心里有点儿担心和害怕 (Trong lòng tôi hơi lo lắng và sợ hãi)."
            },
            {
                "id": "q2",
                "question_vi": "Thầy giáo đã động viên điều gì?",
                "options_vi": ["Hãy bỏ cuộc", "Hãy tin vào bản thân vì đã chuẩn bị rất kỹ", "Đi về nhà"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 相信自己，你准备得很充分 (Hãy tin vào chính mình, em chuẩn bị rất tốt)."
            },
            {
                "id": "q3",
                "question_vi": "Kết quả của cuộc thi ra sao?",
                "options_vi": ["Bị trượt", "Mọi người vỗ tay và đạt thành tích xuất sắc", "Không thi được"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 大家为我热烈鼓掌，我拿到了最好的成绩 (Mọi người vỗ tay, tôi đạt thành tích tốt nhất)."
            }
        ]
    },
    {
        "id": "hsk3_story_006",
        "level": "HSK3",
        "title": {
            "zh": "在超市买生活用品",
            "vi": "Mua đồ dùng sinh hoạt ở siêu thị"
        },
        "topic": "shopping_daily",
        "topic_vi": "Mua sắm & Đời sống",
        "icon": "🛒",
        "estimatedMinutes": 4,
        "description_vi": "Chuyến đi siêu thị mua thực phẩm tươi ngon và bánh mì cho bữa sáng gia đình.",
        "sentences": [
            ("今天下午我和妈妈一起去附近的超市。", "Jīntiān xiàwǔ wǒ hé māma yìqǐ qù fùjìn de chāoshì.", "Chiều hôm nay tôi và mẹ cùng nhau đến siêu thị gần nhà."),
            ("超市里的水果非常新鲜，还打折便宜。", "Chāoshì lǐ de shuǐguǒ fēicháng xīnxian, hái dǎzhé piányi.", "Hoa quả trong siêu thị vô cùng tươi mới, lại còn giảm giá rẻ."),
            ("妈妈选了香蕉、苹果和一大瓶牛奶。", "Māma xuǎn le xiāngjiāo, píngguǒ hé yí dà píng niúnǎi.", "Mẹ chọn chuối tiêu, táo tây và một bình sữa tươi lớn."),
            ("我还买了一些面包，准备明天早餐吃。", "Wǒ hái mǎi le yìxiē miànbāo, zhǔnbèi míngtiān zǎocān chī.", "Tôi còn mua thêm ít bánh mì, chuẩn bị ăn cho bữa sáng ngày mai."),
            ("超市服务员热情地帮我们装好袋子。", "Chāoshì fúwùyuán rèqíng de bāng wǒmen zhuāng hǎo dàizi.", "Nhân viên siêu thị nhiệt tình giúp chúng tôi gói đồ vào túi.")
        ],
        "spotlight": ["附近", "超市", "新鲜", "便宜", "香蕉", "苹果", "牛奶", "面包", "准备", "服务员", "热情"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Hai mẹ con đi đâu vào chiều nay?",
                "options_vi": ["Đi rạp chiếu phim", "Đi siêu thị gần nhà", "Đi công viên"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 去附近的超市 (Đi siêu thị gần nhà)."
            },
            {
                "id": "q2",
                "question_vi": "Hoa quả ở siêu thị có đặc điểm gì?",
                "options_vi": ["Cũ và đắt", "Vô cùng tươi mới và giảm giá rẻ", "Không ngon"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 水果非常新鲜，还打折便宜 (Hoa quả rất tươi, lại giảm giá rẻ)."
            },
            {
                "id": "q3",
                "question_vi": "Nhân vật chính mua bánh mì để làm gì?",
                "options_vi": ["Để ăn bữa sáng ngày mai", "Để cho chim ăn", "Để tặng bạn"],
                "answer": 0,
                "explanation_vi": "Trong câu có viết: 准备明天早餐吃 (Chuẩn bị ăn bữa sáng ngày mai)."
            }
        ]
    },
    {
        "id": "hsk3_story_007",
        "level": "HSK3",
        "title": {
            "zh": "感冒发烧的一天",
            "vi": "Một ngày cảm cúm phát sốt"
        },
        "topic": "health_recovery",
        "topic_vi": "Sức khỏe & Chăm sóc",
        "icon": "🤒",
        "estimatedMinutes": 4,
        "description_vi": "Sự quan tâm chăm sóc ấm áp của mẹ khi con bị cảm lạnh và sốt cao.",
        "sentences": [
            ("昨天晚上我开始头疼，身上发烧。", "Zuótiān wǎnshang wǒ kāishǐ tóuténg, shēnshang fāshāo.", "Tối hôm qua tôi bắt đầu đau đầu, người phát sốt."),
            ("妈妈很担心，马上找出了感冒药给我吃。", "Māma hěn dānxīn, mǎshàng zhǎo chū le gǎnmàoyào gěi wǒ chī.", "Mẹ rất lo lắng, liền lập tức tìm thuốc cảm cho tôi uống."),
            ("她倒了一杯温水，让我躺在床上休息。", "Tā dào le yì bēi wēnshuǐ, ràng wǒ tǎng zài chuáng shang xiūxi.", "Mẹ rót một ly nước ấm, bảo tôi nằm trên giường nghỉ ngơi."),
            ("今天早上量了体温，已经退烧了，感觉舒服多了。", "Jīntiān zǎoshang liáng le tǐwēn, yǐjīng tuìshāo le, gǎnjué shūfu duō le.", "Sáng nay đo lại thân nhiệt, đã hạ sốt rồi, cảm giác dễ chịu hơn nhiều."),
            ("有妈妈的细心照顾，我好得非常快。", "Yǒu māma de xìxīn zhàogù, wǒ hǎo de fēicháng kuài.", "Nhờ có sự chăm sóc chu đáo của mẹ, tôi bình phục rất nhanh.")
        ],
        "spotlight": ["开始", "疼", "发烧", "担心", "马上", "感冒", "药", "休息", "已经", "舒服", "照顾", "快"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Tối hôm qua nhân vật chính có triệu chứng gì?",
                "options_vi": ["Đau chân", "Đau đầu và phát sốt", "Đau răng"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 开始头疼，身上发烧 (Bắt đầu đau đầu, người phát sốt)."
            },
            {
                "id": "q2",
                "question_vi": "Mẹ đã làm gì để chăm sóc?",
                "options_vi": ["Bắt đi học", "Tìm thuốc cảm và rót nước ấm cho uống", "Đi mua đồ chơi"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 找出了感冒药给我吃... 倒了一杯温水 (Tìm thuốc cảm cho uống, rót nước ấm)."
            },
            {
                "id": "q3",
                "question_vi": "Tình trạng sức khỏe sáng hôm nay ra sao?",
                "options_vi": ["Sốt nặng hơn", "Đã hạ sốt và thấy dễ chịu hơn nhiều", "Phải đi viện cấp cứu"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 已经退烧了，感觉舒服多了 (Đã hạ sốt, cảm giác dễ chịu hơn nhiều)."
            }
        ]
    },
    {
        "id": "hsk3_story_008",
        "level": "HSK3",
        "title": {
            "zh": "给奶奶过生日",
            "vi": "Mừng sinh nhật bà nội"
        },
        "topic": "family_love",
        "topic_vi": "Gia đình & Tình thân",
        "icon": "🎂",
        "estimatedMinutes": 4,
        "description_vi": "Bữa tiệc sinh nhật ấm cúng sum vầy mừng thọ bà nội bảy mươi tuổi.",
        "sentences": [
            ("今天是奶奶七十岁的生日，全家都很高兴。", "Jīntiān shì nǎinai qīshí suì de shēngrì, quán jiā dōu hěn gāoxìng.", "Hôm nay là sinh nhật bảy mươi tuổi của bà nội, cả nhà đều rất vui mừng."),
            ("叔叔买了一个又大又漂亮的水果蛋糕。", "Shūshu mǎi le yí gè yòu dà yòu piàoliang de shuǐguǒ dàngāo.", "Chú đã mua một chiếc bánh gato hoa quả vừa to vừa đẹp."),
            ("我送给奶奶一条红色的暖和围巾。", "Wǒ sòng gěi nǎinai yì tiáo hóngsè de nuǎnhuo wéijīn.", "Tôi tặng bà nội một chiếc khăn quàng cổ màu đỏ ấm áp."),
            ("我们大家一起祝奶奶身体健康，生活愉快！", "Wǒmen dàjiā yìqǐ zhù nǎinai shēntǐ jiànkāng, shēnghuó yúkuài!", "Tất cả chúng tôi cùng chúc bà nội dồi dào sức khỏe, sống vui tươi!"),
            ("奶奶开心地笑着，吹灭了生日蜡烛。", "Nǎinai kāixīn de xiào zhe, chuī miè le shēngrì làzhú.", "Bà nội cười vui vẻ, thổi tắt những ngọn nến sinh nhật.")
        ],
        "spotlight": ["奶奶", "生日", "蛋糕", "送", "红", "条", "大家", "祝", "身体", "健康", "笑"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Hôm nay bà nội tròn bao nhiêu tuổi?",
                "options_vi": ["60 tuổi", "70 tuổi", "80 tuổi"],
                "answer": 1,
                "explanation_vi": "Trong câu đầu có viết: 奶奶七十岁的生日 (Sinh nhật 70 tuổi của bà nội)."
            },
            {
                "id": "q2",
                "question_vi": "Nhân vật chính đã tặng món quà gì cho bà?",
                "options_vi": ["Một chiếc đồng hồ", "Một chiếc khăn quàng cổ màu đỏ ấm áp", "Một đôi giày"],
                "answer": 1,
                "explanation_vi": "Trong bài có câu: 送给奶奶一条红色的暖和围巾 (Tặng bà một chiếc khăn đỏ ấm áp)."
            },
            {
                "id": "q3",
                "question_vi": "Cả nhà đã cùng chúc bà điều gì?",
                "options_vi": ["Mau giàu có", "Sức khỏe dồi dào, sống vui vẻ hạnh phúc", "Đi du lịch nhiều"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 祝奶奶身体健康，生活愉快 (Chúc bà sức khỏe dồi dào, cuộc sống vui vẻ)."
            }
        ]
    },
    {
        "id": "hsk3_story_009",
        "level": "HSK3",
        "title": {
            "zh": "美丽的春天",
            "vi": "Mùa xuân tươi đẹp"
        },
        "topic": "seasons_weather",
        "topic_vi": "Bốn mùa & Thiên nhiên",
        "icon": "🌸",
        "estimatedMinutes": 4,
        "description_vi": "Cảnh sắc thiên nhiên tươi mới và tràn đầy sức sống khi mùa xuân trở lại.",
        "sentences": [
            ("一年四个季节里，我最喜欢春天。", "Yì nián sì gè jìjié lǐ, wǒ zuì xǐhuan chūntiān.", "Trong bốn mùa của một năm, tôi thích nhất là mùa xuân."),
            ("春天来了，天气渐渐变得暖和起来。", "Chūntiān lái le, tiānqì jiànjiàn biàn de nuǎnhuo qǐlái.", "Mùa xuân đến rồi, thời tiết dần dần trở nên ấm áp."),
            ("公园里的花儿都开了，小草也变绿了。", "Gōngyuán lǐ de huār dōu kāi le, xiǎocǎo yě biàn lǜ le.", "Hoa trong công viên đều đã nở, cỏ non cũng đã chuyển sang màu xanh."),
            ("小鸟在树上快乐地唱歌，到处充满生机。", "Xiǎoniǎo zài shù shang kuàilè de chànggē, dàochù chōngmǎn shēngjī.", "Những chú chim nhỏ hót ca vui vẻ trên cây, khắp nơi tràn ngập sức sống."),
            ("我和朋友经常去公园散步，享受阳光。", "Wǒ hé péngyou jīngcháng qù gōngyuán sànbù, xiǎngshòu yángguāng.", "Tôi và bạn bè thường đến công viên đi dạo, tận hưởng ánh nắng chan hòa.")
        ],
        "spotlight": ["季节", "最", "喜欢", "春天", "草", "绿", "鸟", "树", "快乐", "唱歌", "经常"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Trong bốn mùa, nhân vật chính yêu thích mùa nào nhất?",
                "options_vi": ["Mùa hè", "Mùa thu", "Mùa xuân"],
                "answer": 2,
                "explanation_vi": "Trong câu đầu có viết: 我最喜欢春天 (Tôi thích nhất là mùa xuân)."
            },
            {
                "id": "q2",
                "question_vi": "Thời tiết mùa xuân thay đổi như thế nào?",
                "options_vi": ["Trở nên rất lạnh", "Dần dần trở nên ấm áp", "Mưa tuyết nhiều"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 天气渐渐变得暖和起来 (Thời tiết dần trở nên ấm áp)."
            },
            {
                "id": "q3",
                "question_vi": "Nhân vật chính thường làm gì cùng bạn bè ở công viên?",
                "options_vi": ["Chơi game", "Đi dạo và tắm nắng", "Làm bài thi"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 经常去公园散步，享受阳光 (Thường đến công viên đi dạo, tận hưởng ánh nắng)."
            }
        ]
    },
    {
        "id": "hsk3_story_010",
        "level": "HSK3",
        "title": {
            "zh": "我的中国室友",
            "vi": "Người bạn cùng phòng Trung Quốc"
        },
        "topic": "friendship_culture",
        "topic_vi": "Tình bạn & Văn hóa",
        "icon": "🤝",
        "estimatedMinutes": 4,
        "description_vi": "Sự sẻ chia văn hóa thú vị và tình bạn gắn bó giữa hai người bạn cùng phòng.",
        "sentences": [
            ("我的大学室友张伟是一个热情的北京人。", "Wǒ de dàxué shìyǒu Zhāng Wěi shì yí gè rèqíng de Běijīng rén.", "Bạn cùng phòng đại học của tôi Trương Vĩ là một người Bắc Kinh nhiệt tình."),
            ("他教我用筷子吃面条，了解中国文化。", "Tā jiāo wǒ yòng kuàizi chī miàntiáo, liǎojiě zhōngguó wénhuà.", "Cậu ấy dạy tôi dùng đũa ăn mì sợi, tìm hiểu văn hóa Trung Quốc."),
            ("我遇到难题的时候，他总是耐心地给我讲明白。", "Wǒ yù dào nántí de shíhou, tā zǒngshì nàixīn de gěi wǒ jiǎng míngbai.", "Khi tôi gặp bài khó, cậu ấy luôn kiên nhẫn giảng cho tôi hiểu rõ."),
            ("两个人虽然来自不同国家，但是相处得像兄弟一样。", "Liǎng gè rén suīrán láizì bùtóng guójiā, dànshì xiāngchǔ de xiàng xiōngdì yíyàng.", "Hai người tuy đến từ hai quốc gia khác nhau, nhưng thân thiết như anh em."),
            ("我们约定以后要一起去更多的地方旅游。", "Wǒmen yuēdìng yǐhòu yào yìqǐ qù gèng duō de dìfang lǚyóu.", "Chúng tôi hẹn nhau sau này sẽ cùng đi du lịch nhiều nơi hơn nữa.")
        ],
        "spotlight": ["热情", "北京", "筷子", "面条", "了解", "文化", "难", "总是", "明白", "虽然…但是…", "像", "旅游"],
        "quiz": [
            {
                "id": "q1",
                "question_vi": "Người bạn cùng phòng Trương Vĩ là người ở đâu?",
                "options_vi": ["Bắc Kinh", "Thượng Hải", "Quảng Đông"],
                "answer": 0,
                "explanation_vi": "Trong câu đầu có viết: 热情的北京人 (Người Bắc Kinh nhiệt tình)."
            },
            {
                "id": "q2",
                "question_vi": "Trương Vĩ đã dạy nhân vật chính điều gì?",
                "options_vi": ["Dạy bơi", "Dạy dùng đũa ăn mì và tìm hiểu văn hóa Trung Quốc", "Dạy lái xe"],
                "answer": 1,
                "explanation_vi": "Trong câu có viết: 教我用筷子吃面条，了解中国文化 (Dạy dùng đũa ăn mì, tìm hiểu văn hóa Trung Quốc)."
            },
            {
                "id": "q3",
                "question_vi": "Hai người đã có hẹn ước gì cho tương lai?",
                "options_vi": ["Cùng nhau mở công ty", "Cùng nhau đi du lịch nhiều nơi hơn", "Không gặp lại nhau"],
                "answer": 1,
                "explanation_vi": "Trong câu cuối có viết: 约定以后要一起去更多的地方旅游 (Hẹn sau này cùng đi du lịch nhiều nơi hơn)."
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
                "friendship_culture": "Tình bạn & Văn hóa"
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
                "hsk3_story_010": "🤝"
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
    hsk3_dir = READINGS_DIR / "hsk3"
    hsk3_dir.mkdir(parents=True, exist_ok=True)

    generated_count = 0
    for sdata in STORIES_HSK3:
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
                if len(spotlight_ids) >= 10:
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

        out_path = hsk3_dir / f"{sid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(story_obj, f, ensure_ascii=False, indent=2)

        print(f"[✓] Generated {sid} -> {out_path.name} ({len(sentences_json)} sentences, {len(spotlight_ids)} spotlight words)")
        generated_count += 1

    print(f"\nSuccessfully generated {generated_count} HSK3 stories.")
    update_manifest()

if __name__ == "__main__":
    main()
