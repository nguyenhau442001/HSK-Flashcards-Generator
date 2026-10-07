# -*- coding: utf-8 -*-
"""
Authentic items curated from HSK 4 模拟试卷 9 (Mock Test 9).
Source: Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
"""

TEST9_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building 86-95)
    # =========================================================================
    {
        "id": "hsk4_test9_q86",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第86题)",
        "zh": "他观察得很仔细。",
        "pinyin": "tā guān chá de hěn zǐ xì 。",
        "hanviet": "Tha Quan Sát Đắc Hẩn Tử Tế 。",
        "meaning": "Anh ấy quan sát rất tỉ mỉ, cẩn thận.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "观察", "type": "core", "role": "Động từ chính (quan sát)" },
            { "text": "得", "type": "grammar", "role": "Trợ từ kết cấu bổ ngữ trạng thái" },
            { "text": "很", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "仔细", "type": "core", "role": "Tính từ bổ ngữ (tỉ mỉ, cẩn trọng)" }
        ],
        "grammar_point": {
            "name": "Bổ ngữ trạng thái / trình độ miêu tả phong cách hành động: V + 得 + 很 + Tính từ",
            "pattern": "Chủ ngữ + Động từ + 得 + (很/非常) + Tính từ miêu tả",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY TỪ HƯ: '得' nối động từ '观察' với bổ ngữ miêu tả '很仔细'. Tuyệt đối không nhầm sang chữ '的' (định ngữ) hay '地' (trạng ngữ đứng trước động từ).",
            "explanation": "Đánh giá phong thái làm việc hoặc nghiên cứu nghiêm túc, chu đáo của một nhà khoa học hoặc điều tra viên."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Người theo dõi hiện tượng" },
            { "role": "Vị ngữ động từ + Trợ từ", "text": "观察得", "type": "verb", "desc": "Hành vi quan sát kèm trợ từ '得'" },
            { "role": "Bổ ngữ miêu tả chi tiết", "text": "很仔细", "type": "modifier", "desc": "Mức độ tỉ mỉ, không bỏ sót góc khuất" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["很仔细", "观察得", "他"],
            "target_chunks": ["他", "观察得", "很仔细"],
            "hint": "Cấu trúc: 主语 (他) + 观察得 + 很仔细."
        }
    },
    {
        "id": "hsk4_test9_q87",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第87题)",
        "zh": "路上的冰已经化了。",
        "pinyin": "lù shang de bīng yǐ jīng huà le 。",
        "hanviet": "Lộ Thượng Đích Băng Dĩ Kinh Hóa Liễu 。",
        "meaning": "Băng trên mặt đường đã tan ra rồi.",
        "tokens": [
            { "text": "路上的", "type": "normal", "role": "Định ngữ nơi chốn" },
            { "text": "冰", "type": "core", "role": "Chủ ngữ trung tâm (băng tuyết)" },
            { "text": "已经", "type": "normal", "role": "Phó từ hoàn thành" },
            { "text": "化", "type": "core", "role": "Động từ chính (tan chảy, hóa lỏng)" },
            { "text": "了", "type": "grammar", "role": "Trợ từ ngữ khí biến hóa trạng thái" }
        ],
        "grammar_point": {
            "name": "Động từ chỉ sự chuyển biến trạng thái vật lý 化 (Tan chảy) và Trợ từ 了",
            "pattern": "Địa điểm + 的 + Danh từ tự nhiên + 已经 + Động từ trạng thái + 了",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY TỪ VỰNG: Động từ '化' (huà) trong tiếng Trung dùng cho băng tuyết tan chảy. Trợ từ '了' biểu thị sự biến đổi sang trạng thái mới (từ đóng băng sang tan thành nước).",
            "explanation": "Thời tiết ấm dần khiến lớp băng trơn trượt trên mặt đường tan đi, giao thông trở lại an toàn."
        },
        "breakdown": [
            { "role": "Chủ ngữ định-trung", "text": "路上的冰", "type": "subject", "desc": "Lớp băng đọng trên mặt phố" },
            { "role": "Trạng ngữ hoàn thành", "text": "已经", "type": "modifier", "desc": "Đã xảy ra hoàn tất" },
            { "role": "Vị ngữ biến hóa", "text": "化了", "type": "verb", "desc": "Chuyển thể từ rắn sang lỏng" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["已经化了", "路上的", "冰"],
            "target_chunks": ["路上的", "冰", "已经化了"],
            "hint": "Chủ ngữ (路上的冰) + Vị ngữ (已经化了)."
        }
    },
    {
        "id": "hsk4_test9_q88",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第88题)",
        "zh": "老师的笑容很亲切。",
        "pinyin": "lǎo shī de xiào róng hěn qīn qiè 。",
        "hanviet": "Lão Sư Đích Tiếu Dung Hẩn Thân Thiết 。",
        "meaning": "Nụ cười của thầy cô giáo rất thân thương gần gũi.",
        "tokens": [
            { "text": "老师", "type": "normal", "role": "Danh từ" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "笑容", "type": "core", "role": "Chủ ngữ trung tâm (nụ cười, nét mặt cười)" },
            { "text": "很", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "亲切", "type": "core", "role": "Tính từ vị ngữ (thân thiết, ấm áp, gần gũi)" }
        ],
        "grammar_point": {
            "name": "Câu miêu tả thần thái: Cụm định-trung + 很 + Tính từ 亲切",
            "pattern": "Người + 的 + 笑容 / 态度 / 话语 + 很 + 亲切",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY TỪ PHỐI HỢP: '亲切' (thân thiết/ấm áp) là tính từ chuyên dùng miêu tả thái độ, nụ cười ('笑容') hoặc giọng nói của người lớn tuổi/thầy cô đối với học trò.",
            "explanation": "Câu vị ngữ hình dung từ ngợi ca vẻ hiền hậu và sự gần gũi của người thầy."
        },
        "breakdown": [
            { "role": "Chủ ngữ định-trung", "text": "老师的笑容", "type": "subject", "desc": "Nét mặt rạng rỡ của người dạy học" },
            { "role": "Vị ngữ tính từ", "text": "很亲切", "type": "verb", "desc": "Mang lại cảm giác ấm áp như người thân" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["老师的", "很亲切", "笑容"],
            "target_chunks": ["老师的", "笑容", "很亲切"],
            "hint": "Chủ ngữ (老师的笑容) + Vị ngữ (很亲切)."
        }
    },
    {
        "id": "hsk4_test9_q89",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第89题)",
        "zh": "不要把坏心情带到工作中来。",
        "pinyin": "bú yào bǎ huài xīn qíng dài dào gōng zuò zhōng lái 。",
        "hanviet": "Bất Yếu Bả Hoại Tâm Tình Đái Đáo Công Tác Trung Lai 。",
        "meaning": "Đừng đem tâm trạng tồi tệ đưa vào trong công việc.",
        "tokens": [
            { "text": "不要", "type": "grammar", "role": "Phó từ khuyên can (đừng)" },
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "坏心情", "type": "core", "role": "Tân ngữ trừu tượng chịu tác động (tâm trạng xấu)" },
            { "text": "带到", "type": "core", "role": "Động từ + bổ ngữ đích đến (mang đến)" },
            { "text": "工作中", "type": "core", "role": "Phạm vi môi trường làm việc" },
            { "text": "来", "type": "grammar", "role": "Bổ ngữ xu hướng hướng tâm" }
        ],
        "grammar_point": {
            "name": "Câu chữ 把 với tân ngữ trừu tượng và Bổ ngữ xu hướng kép 到...来",
            "pattern": "不要 / 别 + 把 + Tân ngữ trừu tượng + 带到 + Môi trường / Phạm vi + 来 / 去",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Câu chữ 把 hoàn toàn có thể áp dụng cho tân ngữ trừu tượng ('坏心情'). Cụm '带到...来' bao trọn lấy nơi chốn môi trường '工作中'.",
            "explanation": "Lời khuyên răn về thái độ chuyên nghiệp trong công sở, không để cảm xúc tiêu cực cá nhân ảnh hưởng hiệu quả chung."
        },
        "breakdown": [
            { "role": "Lời khuyên ngăn", "text": "不要", "type": "grammar", "desc": "Cảnh báo không nên hành xử như vậy" },
            { "role": "Giới từ 把 + Đối tượng cảm xúc", "text": "把坏心情", "type": "object", "desc": "Đối tượng tiêu cực cần loại bỏ" },
            { "role": "Vị ngữ + Bổ ngữ xu hướng", "text": "带到工作中来", "type": "verb", "desc": "Mang sự bực bội vào môi trường nhiệm sở" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["把坏心情", "不要", "带到工作中来"],
            "target_chunks": ["不要", "把坏心情", "带到工作中来"],
            "hint": "Cấu trúc: 不要 + 把 [坏心情] + 带到工作中来."
        }
    },
    {
        "id": "hsk4_test9_q90",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第90题)",
        "zh": "老师叫山田去取课程表。",
        "pinyin": "lǎo shī jiào shān tián qù qǔ kè chéng biǎo 。",
        "hanviet": "Lão Sư Khiếu Sơn Điền Khứ Thủ Khóa Trình Biểu 。",
        "meaning": "Thầy giáo bảo Yamada đi lấy thời khóa biểu.",
        "tokens": [
            { "text": "老师", "type": "core", "role": "Chủ ngữ ra lệnh" },
            { "text": "叫", "type": "grammar", "role": "Động từ sai khiến kiêm ngữ (bảo/kêu)" },
            { "text": "山田", "type": "normal", "role": "Kiêm ngữ (tên riêng du học sinh)" },
            { "text": "去", "type": "normal", "role": "Động từ liên động di chuyển" },
            { "text": "取", "type": "core", "role": "Động từ hành động (lấy, nhận)" },
            { "text": "课程表", "type": "core", "role": "Tân ngữ trực tiếp (thời khóa biểu)" }
        ],
        "grammar_point": {
            "name": "Câu kiêm ngữ sai khiến 叫 kết hợp Câu liên động: 叫 + Người + 去 + Lấy vật gì",
            "pattern": "Người sai phái + 叫 / 让 + Người thực hiện + 去 + 取 / 拿 + Đồ vật",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY CẤU TRÚC: '叫' ở đây là động từ sai bảo khẩu ngữ tương đương '让' hay '使'. '山田' là kiêm ngữ đứng giữa '叫' và '去取课程表'.",
            "explanation": "Thầy giáo giao một nhiệm vụ vặt cho học trò Yamada đến văn phòng khoa nhận lịch học."
        },
        "breakdown": [
            { "role": "Chủ ngữ sai khiến", "text": "老师", "type": "subject", "desc": "Giáo viên chủ nhiệm" },
            { "role": "Động từ kiêm ngữ", "text": "叫", "type": "verb", "desc": "Giao phó công việc" },
            { "role": "Người thi hành", "text": "山田", "type": "subject", "desc": "Bạn học sinh họ Yamada" },
            { "role": "Nhiệm vụ liên động", "text": "去取课程表", "type": "verb", "desc": "Đến địa điểm nhận bản lịch trình học tập" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["叫山田", "老师", "去取课程表"],
            "target_chunks": ["老师", "叫山田", "去取课程表"],
            "hint": "Cấu trúc kiêm ngữ: 老师 + 叫山田 + 去取课程表."
        }
    },
    {
        "id": "hsk4_test9_q91",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第91题)",
        "zh": "换完衣服再出去玩儿。",
        "pinyin": "huàn wán yī fu zài chū qù wánr 。",
        "hanviet": "Hoán Hoàn Y Phục Tái Xuất Khứ Ngoạn Nhi 。",
        "meaning": "Thay quần áo xong rồi hãy ra ngoài chơi nhé.",
        "tokens": [
            { "text": "换", "type": "core", "role": "Động từ chính 1 (thay)" },
            { "text": "完", "type": "grammar", "role": "Bổ ngữ kết quả (xong)" },
            { "text": "衣服", "type": "normal", "role": "Tân ngữ (quần áo)" },
            { "text": "再", "type": "grammar", "role": "Phó từ biểu thị hành động xảy ra sau khi việc trước hoàn tất (rồi mới/hãy)" },
            { "text": "出去", "type": "normal", "role": "Động từ xu hướng (ra ngoài)" },
            { "text": "玩儿", "type": "core", "role": "Động từ mục đích (chơi)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc liên tiếp điều kiện thời gian: V1 + 完 + (Tân ngữ) + 再 + V2",
            "pattern": "Động từ 1 + 完 + Tân ngữ 1 + 再 + Động từ 2 + (Tân ngữ 2)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ HƯ: '再' ở đây biểu thị thứ tự hành động trước sau ('làm xong việc A rồi MỚI làm việc B'). Tuyệt đối không nhầm lẫn với '又' (đã lặp lại).",
            "explanation": "Câu dặn dò thường ngày của cha mẹ đối với con trẻ khi đi học về hoặc chuẩn bị ra sân dạo chơi."
        },
        "breakdown": [
            { "role": "Hành động tiền đề hoàn tất", "text": "换完衣服", "type": "verb", "desc": "Hoàn tất thao tác thay đồ sạch sẽ" },
            { "role": "Phó từ liên kết thứ tự", "text": "再", "type": "grammar", "desc": "Chỉ hành động sau chỉ được phép bắt đầu khi việc trước xong" },
            { "role": "Hành động kế tiếp", "text": "出去玩儿", "type": "verb", "desc": "Bước ra khỏi nhà vui chơi" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["再出去玩儿", "换完衣服"],
            "target_chunks": ["换完衣服", "再出去玩儿"],
            "hint": "Cấu trúc tuần tự: 换完衣服 + 再出去玩儿."
        }
    },
    {
        "id": "hsk4_test9_q92",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第92题)",
        "zh": "你对纪念邮票感兴趣吗？",
        "pinyin": "nǐ duì jì niàn yóu piào gǎn xìng qù ma ？",
        "hanviet": "Nhĩ Đối Kỷ Niệm Bưu Phiếu Cảm Hứng Thú Ma ？",
        "meaning": "Bạn có hứng thú với tem kỷ niệm không?",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Chủ ngữ" },
            { "text": "对", "type": "grammar", "role": "Giới từ chỉ đối tượng" },
            { "text": "纪念", "type": "core", "role": "Định ngữ (kỷ niệm)" },
            { "text": "邮票", "type": "core", "role": "Tân ngữ của giới từ (con tem)" },
            { "text": "感兴趣", "type": "core", "role": "Cụm vị ngữ mang ý nghĩa say mê, quan tâm" },
            { "text": "吗", "type": "grammar", "role": "Trợ từ nghi vấn" }
        ],
        "grammar_point": {
            "name": "Cấu trúc cố định 対...感兴趣 (Có hứng thú với điều gì)",
            "pattern": "Chủ ngữ + 对 + Đồ vật sưu tầm / Lĩnh vực + 感兴趣 + 吗？",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Cụm '对纪念邮票' làm trạng ngữ bắt buộc phải đứng trước '感兴趣'. '纪念邮票' là tem phát hành nhân dịp đặc biệt.",
            "explanation": "Câu hỏi mở đầu câu chuyện về sở thích sưu tập tem bưu chính cổ truyền."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你", "type": "subject", "desc": "Người được hỏi sở thích" },
            { "role": "Trạng ngữ giới từ chỉ đối tượng", "text": "对纪念邮票", "type": "modifier", "desc": "Hướng về mặt hàng tem sưu tầm" },
            { "role": "Vị ngữ + Ngữ khí", "text": "感兴趣吗", "type": "verb", "desc": "Hỏi về mức độ quan tâm yêu thích" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["感兴趣吗", "对纪念邮票", "你"],
            "target_chunks": ["你", "对纪念邮票", "感兴趣吗"],
            "hint": "Cấu trúc: 你 + 对纪念邮票 + 感兴趣吗？"
        }
    },
    {
        "id": "hsk4_test9_q93",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第93题)",
        "zh": "我一下课就去你的房间。",
        "pinyin": "wǒ yí xià kè jiù qù nǐ de fáng jiān 。",
        "hanviet": "Ngã Nhất Hạ Khóa Tựu Khứ Nhĩ Đích Phòng Gian 。",
        "meaning": "Tôi vừa tan học xong là sẽ sang phòng của bạn ngay.",
        "tokens": [
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "一", "type": "grammar", "role": "Liên từ chỉ sự việc liền kề (vừa mới)" },
            { "text": "下课", "type": "core", "role": "Hành động kết thúc giờ học" },
            { "text": "就", "type": "grammar", "role": "Phó từ biểu thị hành động xảy ra tức thì (là/ngay)" },
            { "text": "去", "type": "normal", "role": "Động từ di chuyển" },
            { "text": "你的房间", "type": "core", "role": "Nơi chốn đích đến" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ 一...就... biểu thị hành động diễn ra liên tiếp khẩn trương",
            "pattern": "Chủ ngữ + 一 + Tan ca / Tan học + 就 + 去 + Địa điểm",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY CẤU TRÚC: '一' đứng ngay trước '下课', '就' đứng ngay trước '去'. Thể hiện sự nhanh chóng và giữ đúng lời hứa của người nói.",
            "explanation": "Lời hẹn ước thân mật giữa hai người bạn cùng ký túc xá sau khi tiết học cuối cùng khép lại."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我", "type": "subject", "desc": "Người đưa ra lời hẹn" },
            { "role": "Mốc thời gian kích hoạt", "text": "一下课", "type": "modifier", "desc": "Vừa vặn lúc tiếng chuông tan học reo" },
            { "role": "Hành động tức thì kế tiếp", "text": "就去你的房间", "type": "verb", "desc": "Trực tiếp đi tới phòng bạn" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["就去你的房间", "一下课", "我"],
            "target_chunks": ["我", "一下课", "就去你的房间"],
            "hint": "Cấu trúc: 我 + 一下课 + 就去你的房间."
        }
    },
    {
        "id": "hsk4_test9_q94",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第94题)",
        "zh": "钥匙在电脑桌上放着呢。",
        "pinyin": "yào shi zài diàn nǎo zhuō shang fàng zhe ne 。",
        "hanviet": "Thược Thi Tại Điện Não Trác Thượng Phóng Trước Nê 。",
        "meaning": "Chìa khóa đang để ở trên bàn máy tính kìa.",
        "tokens": [
            { "text": "钥匙", "type": "core", "role": "Chủ ngữ vật thể (chìa khóa)" },
            { "text": "在", "type": "grammar", "role": "Giới từ chỉ vị trí" },
            { "text": "电脑桌上", "type": "core", "role": "Nơi chốn phương vị (trên bàn vi tính)" },
            { "text": "放", "type": "core", "role": "Động từ chính (đặt, để)" },
            { "text": "着", "type": "grammar", "role": "Trợ từ động thái duy trì trạng thái" },
            { "text": "呢", "type": "grammar", "role": "Trợ từ ngữ khí chỉ vị trí sờ sờ ngay trước mắt" }
        ],
        "grammar_point": {
            "name": "Câu miêu tả trạng thái vị trí: Vật thể + 在 + Địa điểm + V + 着 + 呢",
            "pattern": "Chủ ngữ vật + 在 + Phương vị từ + Động từ (放/挂/摆) + 着 + (呢)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY CẤU TRÚC: Khác với câu tồn hiện không dùng 在 ở đầu câu ('电脑桌上放着钥匙'), cấu trúc này đưa vật thể đã xác định ('钥匙') lên làm chủ ngữ, sau đó dùng '在 + Nơi chốn + 放着呢'.",
            "explanation": "Câu khẩu ngữ chỉ rõ vị trí món đồ đang tìm kiếm cho người thân yên tâm."
        },
        "breakdown": [
            { "role": "Vật thể xác định", "text": "钥匙", "type": "subject", "desc": "Chùm chìa khóa đang được kiếm tìm" },
            { "role": "Trạng ngữ nơi chốn", "text": "在电脑桌上", "type": "modifier", "desc": "Giới từ '在' xác định vị trí mặt bàn" },
            { "role": "Vị ngữ duy trì + Ngữ khí", "text": "放着呢", "type": "verb", "desc": "Đang nằm nguyên vẹn ở đó" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["放着呢", "钥匙", "在电脑桌上"],
            "target_chunks": ["钥匙", "在电脑桌上", "放着呢"],
            "hint": "Cấu trúc: Vật (钥匙) + 在电脑桌上 + 放着呢."
        }
    },
    {
        "id": "hsk4_test9_q95",
        "category": "sentence_building",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 书写 第一部分 (第95题)",
        "zh": "你能不能试着翻译一下？",
        "pinyin": "nǐ néng bu néng shì zhe fān yì yí xià ？",
        "hanviet": "Nhĩ Năng Bất Năng Thí Trước Phiên Dịch Nhất Hạ ？",
        "meaning": "Bạn có thể thử dịch qua một chút được không?",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Chủ ngữ" },
            { "text": "能不能", "type": "grammar", "role": "Hình thức câu hỏi chính phản (có thể hay không)" },
            { "text": "试着", "type": "core", "role": "Động từ + 着 chỉ phương thức (thử làm)" },
            { "text": "翻译", "type": "core", "role": "Động từ chính (dịch thuật)" },
            { "text": "一下", "type": "grammar", "role": "Động lượng từ giảm nhẹ sắc thái (một chút)" }
        ],
        "grammar_point": {
            "name": "Câu hỏi chính phản lịch thiệp 能不能 và Cụm 试着 + V + 一下",
            "pattern": "Chủ ngữ + 能不能 + 试着 + Động từ + 一下？",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ HƯ: '能不能' dùng để thỉnh cầu một cách tế nhị. '试着' đứng trước động từ '翻译' để khuyến khích đối phương thử sức mà không tạo áp lực. '一下' làm nhẹ mức độ công việc.",
            "explanation": "Lời động viên người học ngoại ngữ mạnh dạn bước vào thực hành dịch câu văn."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你", "type": "subject", "desc": "Người bạn được khích lệ" },
            { "role": "Hình thức thỉnh cầu", "text": "能不能", "type": "grammar", "desc": "Dò hỏi khả năng và thái độ sẵn sàng" },
            { "role": "Hành vi thử sức", "text": "试着翻译一下", "type": "verb", "desc": "Thử làm quen với việc chuyển ngữ" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["试着翻译一下", "能不能", "你"],
            "target_chunks": ["你", "能不能", "试着翻译一下"],
            "hint": "Cấu trúc thỉnh cầu: 你 + 能不能 + 试着翻译一下？"
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Logic 56-65)
    # =========================================================================
    {
        "id": "hsk4_test9_q56",
        "category": "sentence_logic",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 阅读 第二部分 (第56题)",
        "zh": "尽管父母反对，她仍然想要嫁给他，这让她的父母非常伤心。",
        "pinyin": "jǐn guǎn fù mǔ fǎn duì ， tā réng rán xiǎng yào jià gěi tā ， zhè ràng tā de fù mǔ fēi cháng shāng xīn 。",
        "hanviet": "Cận Quản Phụ Mẫu Phản Đối ， Tha Vẫn Nhiên Tưởng Yếu Giá Cấp Tha ， Giá Nhượng Tha Đích Phụ Mẫu Phi Thường Thương Tâm 。",
        "meaning": "Cho dù cha mẹ phản đối, cô ấy vẫn muốn lấy anh ta, điều này khiến cha mẹ cô vô cùng đau lòng.",
        "tokens": [
            { "text": "尽管父母反对", "type": "core", "role": "Vế nhượng bộ mở đầu với 尽管 (A)" },
            { "text": "她仍然想要嫁给他", "type": "core", "role": "Hành vi kiên quyết với 仍然 (C)" },
            { "text": "这", "type": "grammar", "role": "Đại từ chỉ định tóm lược sự cố chấp" },
            { "text": "让她的父母非常伤心", "type": "core", "role": "Hệ quả đau lòng cho bậc sinh thành (B)" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ nhượng bộ 尽管...仍然... và Đại từ tóm lược 这",
            "pattern": "尽管 + Trở ngại (A) + 主语 + 仍然 + Quyết định (C) + 这 + 让... (B)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Cặp liên từ '尽管...仍然...' (A trước, C sau). Câu B có đại từ '这' quy chiếu lại toàn bộ quyết định bướng bỉnh ở câu C, nên B bắt buộc phải đứng cuối.",
            "explanation": "A nêu sự ngăn cản từ gia đình. C thể hiện sự kiên quyết đi theo tiếng gọi con tim. B miêu tả nỗi buồn của cha mẹ do hành động đó gây ra."
        },
        "breakdown": [
            { "role": "Vế nhượng bộ (A)", "text": "尽管父母反对", "type": "subject", "desc": "Ý kiến bất đồng của cha mẹ" },
            { "role": "Hành vi kiên định (C)", "text": "她仍然想要嫁给他", "type": "verb", "desc": "Vẫn giữ vững lập trường kết hôn" },
            { "role": "Hệ quả xót xa (B)", "text": "这让她的父母非常伤心", "type": "object", "desc": "Đại từ '这' tóm tắt sự việc và chỉ ra nỗi đau của phụ huynh" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "尽管父母反对" },
                { "id": "B", "text": "这让她的父母非常伤心" },
                { "id": "C", "text": "她仍然想要嫁给他" }
            ],
            "correct_order": "ACB",
            "hint": "Cặp liên từ: 尽管 (A) -> 仍然 (C) -> Tóm lược bằng '这让...' (B)."
        }
    },
    {
        "id": "hsk4_test9_q57",
        "category": "sentence_logic",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 阅读 第二部分 (第57题)",
        "zh": "不管是誰，你都不要告诉他，因为这是我们两个人之间的秘密。",
        "pinyin": "bù guǎn shì shéi ， nǐ dōu bú yào gào su tā ， yīn wèi zhè shì wǒ men liǎng gè rén zhī jiān de mì mì 。",
        "hanviet": "Bất Quản Thị Thùy ， Nhĩ Đô Bất Yếu Cáo Tố Tha ， Nhân Vi Giá Thị Ngã Môn Lưỡng Cá Nhân Chi Gian Đích Bí Mật 。",
        "meaning": "Bất kể là ai, bạn cũng đừng nói cho người đó biết, bởi vì đây là bí mật giữa hai chúng ta.",
        "tokens": [
            { "text": "不管是誰", "type": "core", "role": "Phạm vi điều kiện vô điều kiện với 不管 (B)" },
            { "text": "你都不要告诉他", "type": "core", "role": "Yêu cầu hành động kiên quyết với 都 (A)" },
            { "text": "因为", "type": "grammar", "role": "Liên từ giải thích nguyên nhân" },
            { "text": "这是我们两个人之间的秘密", "type": "core", "role": "Lý do căn bản cần giữ kín (C)" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ vô điều kiện 不管...都... kết hợp Mệnh đề giải thích 因为...",
            "pattern": "不管(是) + Đại từ nghi vấn (B) + 都 + Hành vi ngăn cản (A) + 因为 + Lý do cốt lõi (C)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Cặp liên từ '不管...都...' (B đi trước A). Câu C có '因为' (bởi vì) giải thích nguyên do vì sao lại không được tiết lộ, nên phải đứng cuối.",
            "explanation": "B mở ra sự bao quát mọi đối tượng. A cấm chỉ việc tiết lộ thông tin. C lý giải lý do bảo mật."
        },
        "breakdown": [
            { "role": "Điều kiện bao quát (B)", "text": "不管是誰", "type": "subject", "desc": "Bất kể bất kỳ nhân vật nào" },
            { "role": "Mệnh lệnh giữ miệng (A)", "text": "你都不要告诉他", "type": "verb", "desc": "Cặp từ '都不要' tuyệt đối không hé lộ" },
            { "role": "Căn nguyên lý do (C)", "text": "因为这是我们两个人之间的秘密", "type": "object", "desc": "Khẳng định đây là điều bí mật chỉ hai người biết" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "你都不要告诉他" },
                { "id": "B", "text": "不管是誰" },
                { "id": "C", "text": "因为这是我们两个人之间的秘密" }
            ],
            "correct_order": "BAC",
            "hint": "Cặp từ: 不管 (B) -> 都不要 (A) -> Giải thích '因为' (C)."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test 46-55)
    # =========================================================================
    {
        "id": "hsk4_test9_q51",
        "category": "cloze",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 阅读 第一部分 (第51题)",
        "zh": "怪不得说什么内容你都知道。",
        "pinyin": "guài bu de shuō shén me nèi róng nǐ dōu zhī dào 。",
        "hanviet": "Quái Bất Đắc Thuyết Thập Ma Nội Dung Nhĩ Đô Tri Đáo 。",
        "meaning": "Thảo nào/Hóa ra là vậy, hễ nhắc tới nội dung gì bạn cũng đều biết hết.",
        "tokens": [
            { "text": "怪不得", "type": "grammar", "role": "Liên từ khẩu ngữ biểu thị vỡ lẽ ra nguyên nhân (hèn chi/thảo nào)" },
            { "text": "说", "type": "normal", "role": "Nói, nhắc tới" },
            { "text": "什么内容", "type": "core", "role": "Bất cứ tình tiết nào" },
            { "text": "你都", "type": "normal", "role": "Bạn cũng đều" },
            { "text": "知道", "type": "core", "role": "Hiểu rõ tường tận" }
        ],
        "grammar_point": {
            "name": "Liên từ khẩu ngữ bộc lộ sự hiểu ra: 怪不得 (Thảo nào / Hóa ra là vậy / Hèn chi)",
            "pattern": "Nguyên nhân đã rõ -> 怪不得 + Hiện tượng trước đó thấy lạ lùng",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '怪不得' dùng khi người nói bỗng nhiên hiểu được lý do thực sự đằng sau một sự việc bất thường ('hóa ra bạn đã xem phim này 2-3 lần rồi, hèn chi cái gì cũng biết').",
            "explanation": "Từ khẩu ngữ đặc trưng biểu cảm cao trong các đoạn đối thoại HSK 4."
        },
        "breakdown": [
            { "role": "Liên từ giác ngộ", "text": "怪不得", "type": "grammar", "desc": "Nhận ra nguyên nhân sâu xa" },
            { "role": "Hiện tượng được giải tỏa thắc mắc", "text": "说什么内容你都知道", "type": "verb", "desc": "Nắm vững toàn bộ tình tiết bộ phim" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "（  ）说什么内容你都知道。",
            "options": ["怪不得", "紧张", "放弃", "究竟", "哪儿"],
            "blank_index": 0,
            "correct_answer": "怪不得",
            "hint": "Cần một từ đứng đầu phân câu mang nghĩa 'thảo nào / hèn chi'. Chọn '怪不得'."
        }
    },
    {
        "id": "hsk4_test9_q52",
        "category": "cloze",
        "test_id": 9,
        "source": "HSK 4 模拟试卷 9 阅读 第一部分 (第52题)",
        "zh": "你究竟邀请了多少人来参加婚礼呀？",
        "pinyin": "nǐ jiū jìng yāo qǐng le duō shao rén lái cān jiā hūn lǐ ya ？",
        "hanviet": "Nhĩ Cứu Cánh Yêu Thỉnh Liễu Đa Thiểu Nhân Lai Tham Gia Hôn Lễ Nha ？",
        "meaning": "Rốt cuộc thì bạn đã mời bao nhiêu người đến dự đám cưới thế?",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Chủ ngữ" },
            { "text": "究竟", "type": "grammar", "role": "Phó từ nhấn mạnh ngữ khí truy vấn trong câu hỏi (rốt cuộc)" },
            { "text": "邀请了", "type": "core", "role": "Đã mời" },
            { "text": "多少人", "type": "core", "role": "Bao nhiêu khách" },
            { "text": "来参加婚礼", "type": "normal", "role": "Mục đích đến dự tiệc cưới" },
            { "text": "呀", "type": "grammar", "role": "Trợ từ ngữ khí" }
        ],
        "grammar_point": {
            "name": "Phó từ truy vấn 究竟 (Rốt cuộc là / Cuối cùng thì)",
            "pattern": "Chủ ngữ + 究竟 + Từ nghi vấn (多少/什么/谁/怎么) + ...？",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ HƯ: '究竟' (đồng nghĩa với 到底) dùng trong câu hỏi để tăng cường ngữ khí truy vấn, thể hiện mong muốn người nghe trả lời con số hoặc kết quả chính xác.",
            "explanation": "Thấy số bàn tiệc quá đông đảo (khoảng 30 bàn), người bạn tò mò gặng hỏi con số khách mời thực tế."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你", "type": "subject", "desc": "Cô dâu / chú rể" },
            { "role": "Trạng ngữ truy vấn", "text": "究竟", "type": "modifier", "desc": "Nhấn mạnh tìm kiếm sự thật" },
            { "role": "Vị ngữ liên động hỏi số lượng", "text": "邀请了多少人来参加婚礼呀", "type": "verb", "desc": "Quy mô số lượng khách dự hôn lễ" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "你（  ）邀请了多少人来参加婚礼呀？",
            "options": ["究竟", "怪不得", "紧张", "放弃", "温度"],
            "blank_index": 0,
            "correct_answer": "究竟",
            "hint": "Cần một phó từ đứng trước động từ trong câu nghi vấn để tăng ngữ khí gặng hỏi 'rốt cuộc'. Chọn '究竟'."
        }
    }
]
