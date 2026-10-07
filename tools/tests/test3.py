# -*- coding: utf-8 -*-
"""
Authentic items curated from HSK 4 模拟试卷 3 (Mock Test 3).
Source: Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
"""

TEST3_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building 86-95)
    # =========================================================================
    {
        "id": "hsk4_test3_q86",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第86题)",
        "zh": "把这篇课文读一遍。",
        "pinyin": "bǎ zhè piān kè wén dú yí biàn 。",
        "hanviet": "Bả Giá Thiên Khóa Văn Độc Nhất Biến 。",
        "meaning": "Hãy đọc bài khóa này một lượt.",
        "tokens": [
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "这", "type": "normal", "role": "Đại từ chỉ định" },
            { "text": "篇", "type": "core", "role": "Lượng từ (bài văn)" },
            { "text": "课文", "type": "core", "role": "Danh từ (bài khóa)" },
            { "text": "读", "type": "normal", "role": "Động từ (đọc)" },
            { "text": "一遍", "type": "core", "role": "Bổ ngữ động lượng" }
        ],
        "grammar_point": {
            "name": "Cấu trúc câu chữ 把: 把 + Tân ngữ + Động từ + Bổ ngữ động lượng (一遍)",
            "pattern": "Chủ ngữ (ẩn) + 把 + Tân ngữ chịu tác động + Động từ + Bổ ngữ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Bổ ngữ động lượng '一遍' (một lượt/lần) bắt buộc phải đứng SAU động từ '读', không được đặt trước động từ.",
            "explanation": "Câu chữ 把 dùng để nhấn mạnh hành động xử lý đối tượng cụ thể ('这篇课文') với số lần thực hiện là '一遍'."
        },
        "breakdown": [
            { "role": "Giới từ 把", "text": "把", "type": "grammar", "desc": "Đưa tân ngữ chịu tác động lên trước động từ" },
            { "role": "Tân ngữ trực tiếp", "text": "这篇课文", "type": "object", "desc": "Bài khóa được chỉ định cụ thể" },
            { "role": "Vị ngữ động từ", "text": "读", "type": "verb", "desc": "Hành vi đọc" },
            { "role": "Bổ ngữ động lượng", "text": "一遍", "type": "complement", "desc": "Số lần hoàn thành trọn vẹn hành động" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["把", "读", "一遍", "这篇课文"],
            "target_chunks": ["把", "这篇课文", "读", "一遍"],
            "hint": "Cấu trúc: 把 + Tân ngữ (这篇课文) + Động từ (读) + Bổ ngữ (一遍)."
        }
    },
    {
        "id": "hsk4_test3_q87",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第87题)",
        "zh": "会议室里走出来一个人。",
        "pinyin": "huì yì shì lǐ zǒu chū lái yí gè rén 。",
        "hanviet": "Hội Nghị Thất Lý Tẩu Xuất Lai Nhất Cá Nhân 。",
        "meaning": "Từ trong phòng họp có một người bước ra.",
        "tokens": [
            { "text": "会议室", "type": "core", "role": "Danh từ (phòng họp)" },
            { "text": "里", "type": "normal", "role": "Phương vị từ" },
            { "text": "走", "type": "normal", "role": "Động từ chính" },
            { "text": "出来", "type": "grammar", "role": "Bổ ngữ xu hướng kép" },
            { "text": "一个", "type": "normal", "role": "Số lượng từ" },
            { "text": "人", "type": "normal", "role": "Chủ ngữ thực chất" }
        ],
        "grammar_point": {
            "name": "Câu tồn hiện (Cử động xuất hiện): Nơi chốn + Động từ + Bổ ngữ xu hướng + Tân ngữ không xác định",
            "pattern": "Nơi chốn/Phương vị + Động từ + 出来/下来/进来 + Số lượng + Danh từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Câu tồn hiện biểu thị sự xuất hiện/biến mất đòi hỏi từ chỉ nơi chốn đứng đầu câu làm vị trí khởi phát, và chủ thể xuất hiện là danh từ phiếm chỉ (一个人) đứng sau động từ.",
            "explanation": "'会议室里' làm trạng ngữ nơi chốn khởi đầu, '走出来' miêu tả hướng di chuyển hướng về phía người nói."
        },
        "breakdown": [
            { "role": "Trạng ngữ nơi chốn", "text": "会议室里", "type": "subject", "desc": "Vị trí không gian xảy ra sự việc" },
            { "role": "Vị ngữ + Bổ ngữ", "text": "走出来", "type": "verb", "desc": "Động từ '走' kết hợp bổ ngữ xu hướng kép '出来'" },
            { "role": "Chủ thể xuất hiện", "text": "一个人", "type": "object", "desc": "Đối tượng mới xuất hiện (danh từ phiếm chỉ)" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["一个人", "走出来", "会议室里"],
            "target_chunks": ["会议室里", "走出来", "一个人"],
            "hint": "Câu tồn hiện: Nơi chốn (会议室里) đứng trước, sau đó là động từ (走出来), cuối cùng là tân ngữ (一个人)."
        }
    },
    {
        "id": "hsk4_test3_q88",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第88题)",
        "zh": "是谁丢了钥匙？",
        "pinyin": "shì shéi diū le yào shi ？",
        "hanviet": "Thị Thùy Đao Liễu Thược Thi ？",
        "meaning": "Là ai đã làm mất chìa khóa thế?",
        "tokens": [
            { "text": "是", "type": "grammar", "role": "Động từ phán đoán nhấn mạnh" },
            { "text": "谁", "type": "normal", "role": "Đại từ nghi vấn (ai)" },
            { "text": "丢", "type": "core", "role": "Động từ (làm mất)" },
            { "text": "了", "type": "normal", "role": "Trợ từ động thái" },
            { "text": "钥匙", "type": "core", "role": "Danh từ (chìa khóa)" }
        ],
        "grammar_point": {
            "name": "Câu hỏi nhấn mạnh chủ thể với chữ 是",
            "pattern": "是 + Đại từ nghi vấn (谁) + Vị ngữ động từ + Tân ngữ",
            "level": "HSK 4",
            "trap_note": "BẪY THI: Chữ '是' đặt đầu câu dùng để truy vấn nhấn mạnh danh tính đối tượng chịu trách nhiệm cho hành động đã hoàn tất.",
            "explanation": "'钥匙' (chìa khóa) là từ vựng HSK 4 then chốt, '丢' là làm rơi/mất."
        },
        "breakdown": [
            { "role": "Thành phần nhấn mạnh", "text": "是", "type": "grammar", "desc": "Hệ từ mở đầu truy vấn" },
            { "role": "Chủ ngữ nghi vấn", "text": "谁", "type": "subject", "desc": "Đối tượng nghi vấn" },
            { "role": "Vị ngữ", "text": "丢了", "type": "verb", "desc": "Hành động đã xảy ra" },
            { "role": "Tân ngữ", "text": "钥匙", "type": "object", "desc": "Vật bị mất" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["钥匙", "是谁", "丢了"],
            "target_chunks": ["是谁", "丢了", "钥匙"],
            "hint": "Trật tự câu hỏi: 是谁 + 丢了 + 钥匙."
        }
    },
    {
        "id": "hsk4_test3_q89",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第89题)",
        "zh": "他想去商店买生日礼物。",
        "pinyin": "tā xiǎng qù shāng diàn mǎi shēng rì lǐ wù 。",
        "hanviet": "Tha Tưởng Khứ Thương Điếm Mãi Sinh Nhật Lễ Vật 。",
        "meaning": "Anh ấy muốn đến cửa hàng mua quà sinh nhật.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "想", "type": "normal", "role": "Năng nguyện động từ" },
            { "text": "去", "type": "normal", "role": "Động từ 1 (đi)" },
            { "text": "商店", "type": "normal", "role": "Tân ngữ địa điểm của V1" },
            { "text": "买", "type": "normal", "role": "Động từ 2 (mua)" },
            { "text": "生日礼物", "type": "core", "role": "Cụm danh từ tân ngữ của V2" }
        ],
        "grammar_point": {
            "name": "Câu liên động biểu thị mục đích (去 + Nơi chốn + Hành động)",
            "pattern": "Chủ ngữ + 想 + 去 + Địa điểm (商店) + Động từ (买) + Tân ngữ",
            "level": "HSK 4",
            "trap_note": "BẪY THI: Tiếng Trung luôn đặt hành động di chuyển trước hành động mục đích (đi tới nơi trước rồi mới mua), không đảo ngược trật tự.",
            "explanation": "Cấu trúc liên động 去...买... rất phổ biến trong giao tiếp và đề thi HSK."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Người thực hiện" },
            { "role": "Động từ năng nguyện", "text": "想", "type": "grammar", "desc": "Ý muốn, dự định" },
            { "role": "Hành động 1 (Đi đến nơi)", "text": "去商店", "type": "verb", "desc": "Di chuyển đến cửa hàng" },
            { "role": "Hành động 2 (Mục đích)", "text": "买生日礼物", "type": "verb", "desc": "Mua quà tặng sinh nhật" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["买生日礼物", "他想", "去商店"],
            "target_chunks": ["他想", "去商店", "买生日礼物"],
            "hint": "Trật tự câu liên động: Ai (他想) + Đi đâu (去商店) + Làm gì (买生日礼物)."
        }
    },
    {
        "id": "hsk4_test3_q90",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第90题)",
        "zh": "哥哥比弟弟大三岁。",
        "pinyin": "gē ge bǐ dì di dà sān suì 。",
        "hanviet": "Ca Ca Bỉ Đệ Đệ Đại Tam Tuế 。",
        "meaning": "Anh trai lớn hơn em trai 3 tuổi.",
        "tokens": [
            { "text": "哥哥", "type": "normal", "role": "Chủ ngữ A" },
            { "text": "比", "type": "grammar", "role": "Giới từ so sánh" },
            { "text": "弟弟", "type": "normal", "role": "Đối tượng so sánh B" },
            { "text": "大", "type": "normal", "role": "Tính từ so sánh" },
            { "text": "三岁", "type": "core", "role": "Bổ ngữ số lượng chỉ chênh lệch" }
        ],
        "grammar_point": {
            "name": "Cấu trúc so sánh chữ 比: A 比 B + Tính từ + Số lượng chênh lệch",
            "pattern": "A + 比 + B + Tính từ + Cụm số lượng",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI CỰC NGUY HIỂM: Người học Việt Nam thường nhầm lẫn đưa số lượng ra trước tính từ (*比弟弟三岁大* - SAI HOÀN TOÀN). Trong tiếng Trung chuẩn, mức chênh lệch bắt buộc phải đặt SAU tính từ.",
            "explanation": "Mẫu câu so sánh tuổi tác kinh điển: '大 + số tuổi' hoặc '小 + số tuổi'."
        },
        "breakdown": [
            { "role": "Chủ thể so sánh (A)", "text": "哥哥", "type": "subject", "desc": "Người được so sánh" },
            { "role": "Giới từ 比 + B", "text": "比弟弟", "type": "grammar", "desc": "Mốc so sánh đối chiếu" },
            { "role": "Vị ngữ tính từ", "text": "大", "type": "verb", "desc": "Đặc tính so sánh (lớn hơn)" },
            { "role": "Bổ ngữ chênh lệch", "text": "三岁", "type": "complement", "desc": "Khoảng cách chênh lệch cụ thể" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["大三岁", "比弟弟", "哥哥"],
            "target_chunks": ["哥哥", "比弟弟", "大三岁"],
            "hint": "Cấu trúc: A (哥哥) + 比 B (比弟弟) + Tính từ + Chênh lệch (大三岁)."
        }
    },
    {
        "id": "hsk4_test3_q92",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第92题)",
        "zh": "这种生活让人向往。",
        "pinyin": "zhè zhǒng shēng huó ràng rén xiàng wǎng 。",
        "hanviet": "Giá Chủng Sinh Hoạt Nhượng Nhân Hướng Vãng 。",
        "meaning": "Cuộc sống này khiến người ta khao khát, hướng tới.",
        "tokens": [
            { "text": "这", "type": "normal", "role": "Đại từ chỉ định" },
            { "text": "种", "type": "core", "role": "Lượng từ (loại, kiểu)" },
            { "text": "生活", "type": "core", "role": "Danh từ chủ ngữ (cuộc sống)" },
            { "text": "让", "type": "grammar", "role": "Động từ kiêm ngữ (khiến cho)" },
            { "text": "人", "type": "normal", "role": "Tân ngữ kiêm chủ ngữ V2" },
            { "text": "向往", "type": "advanced", "role": "Động từ HSK 4 (khao khát, hướng về)" }
        ],
        "grammar_point": {
            "name": "Câu kiêm ngữ với động từ cầu khiến 让 (S + 让 + O + V)",
            "pattern": "Chủ ngữ (Tác nhân) + 让 + Đối tượng chịu tác động + Động từ/Tính từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: '向往' (xiàngwǎng - ngưỡng mộ/khao khát) là động từ cao cấp trong list HSK 4. '人' đóng vai trò tân ngữ của '让' đồng thời là chủ ngữ của '向往'.",
            "explanation": "Cấu trúc '让 + 人 + [động từ tâm lý / tính từ]' là cách diễn đạt tự nhiên nhất trong tiếng Trung để nói 'khiến người khác cảm thấy...'"
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "这种生活", "type": "subject", "desc": "Kiểu cuộc sống này" },
            { "role": "Động từ kiêm ngữ", "text": "让", "type": "grammar", "desc": "Gây ra, làm cho" },
            { "role": "Kiêm ngữ", "text": "人", "type": "object", "desc": "Mọi người nói chung" },
            { "role": "Vị ngữ thứ hai", "text": "向往", "type": "verb", "desc": "Mơ ước, khao khát" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["让人向往", "这种", "生活"],
            "target_chunks": ["这种", "生活", "让人向往"],
            "hint": "Ghép cụm danh từ chủ ngữ '这种生活' trước, sau đó là cụm kiêm ngữ '让人向往'."
        }
    },
    {
        "id": "hsk4_test3_q93",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第93题)",
        "zh": "公司派我去上海考察。",
        "pinyin": "gōng sī pài wǒ qù shàng hǎi kǎo chá 。",
        "hanviet": "Công Ty Phái Ngã Khứ Thượng Hải Khảo Sát 。",
        "meaning": "Công ty phái tôi đến Thượng Hải khảo sát.",
        "tokens": [
            { "text": "公司", "type": "core", "role": "Danh từ chủ ngữ" },
            { "text": "派", "type": "grammar", "role": "Động từ sai khiến (cử, phái)" },
            { "text": "我", "type": "normal", "role": "Kiêm ngữ" },
            { "text": "去", "type": "normal", "role": "Động từ liên động 1" },
            { "text": "上海", "type": "normal", "role": "Địa danh" },
            { "text": "考察", "type": "advanced", "role": "Động từ HSK 4 (khảo sát, nghiên cứu thực địa)" }
        ],
        "grammar_point": {
            "name": "Câu kiêm ngữ kết hợp liên động: S + 派 + O + 去 + Nơi chốn + Động từ mục đích",
            "pattern": "Tổ chức/Cấp trên + 派 + Nhân sự + 去 + Địa phương + Công tác",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Động từ '派' (phái cử) bắt buộc người được cử phải đứng ngay liền sau '派' (派我), sau đó mới tới lộ trình '去上海' và nhiệm vụ '考察'.",
            "explanation": "Đây là mẫu câu công sở cực kỳ thường gặp trong đề thi HSK 4."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "公司", "type": "subject", "desc": "Cơ quan, công ty" },
            { "role": "Động từ phái cử", "text": "派", "type": "grammar", "desc": "Hành động cử người" },
            { "role": "Kiêm ngữ", "text": "我", "type": "object", "desc": "Người được phái đi" },
            { "role": "Địa điểm đến", "text": "去上海", "type": "verb", "desc": "Đến thành phố Thượng Hải" },
            { "role": "Mục đích công tác", "text": "考察", "type": "verb", "desc": "Thực hiện khảo sát" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["我去上海", "考察", "公司派"],
            "target_chunks": ["公司派", "我去上海", "考察"],
            "hint": "Cấu trúc: Công ty cử (公司派) + Tôi đi đâu (我去上海) + Làm gì (考察)."
        }
    },
    {
        "id": "hsk4_test3_q94",
        "category": "sentence_building",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 书写 第一部分 (第94题)",
        "zh": "约翰被老师批评了。",
        "pinyin": "yuē hàn bèi lǎo shī pī píng le 。",
        "hanviet": "Ước Hàn Bị Lão Sư Phê Bình Liễu 。",
        "meaning": "John đã bị thầy giáo phê bình rồi.",
        "tokens": [
            { "text": "约翰", "type": "normal", "role": "Tên riêng (Chủ ngữ bị động)" },
            { "text": "被", "type": "grammar", "role": "Giới từ câu bị động" },
            { "text": "老师", "type": "normal", "role": "Tác nhân gây ra hành động" },
            { "text": "批评", "type": "core", "role": "Động từ HSK 4 (phê bình, chỉ trích)" },
            { "text": "了", "type": "normal", "role": "Trợ từ ngữ khí" }
        ],
        "grammar_point": {
            "name": "Cấu trúc câu bị động chữ 被: A + 被 + B + Động từ + 了",
            "pattern": "Người chịu tác động (A) + 被 + Người thực hiện (B) + Động từ + Thành phần khác",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Câu chữ 被 thường dùng cho các kết quả không mong muốn hoặc tiêu cực (như '批评' - phê bình, '罚' - phạt, '偷' - trộm). Tác nhân (老师) phải đứng ngay sau chữ 被.",
            "explanation": "Khác với tiếng Việt 'bị phê bình bởi thầy giáo', tiếng Trung chuẩn là 'bị thầy giáo phê bình' (被老师批评)."
        },
        "breakdown": [
            { "role": "Chủ thể bị động", "text": "约翰", "type": "subject", "desc": "Đối tượng chịu hậu quả" },
            { "role": "Giới từ 被 + Tác nhân", "text": "被老师", "type": "grammar", "desc": "Bởi thầy giáo" },
            { "role": "Vị ngữ động từ", "text": "批评了", "type": "verb", "desc": "Đã bị khiển trách/phê bình" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["批评了", "约翰", "被老师"],
            "target_chunks": ["约翰", "被老师", "批评了"],
            "hint": "Cấu trúc bị động: Ai (约翰) + Bị ai (被老师) + Làm sao (批评了)."
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Logic A-B-C 56-65)
    # =========================================================================
    {
        "id": "hsk4_test3_q56",
        "category": "sentence_logic",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 阅读 第二部分 (第56题)",
        "zh": "我去超市买方便面，可是因为着急，忘带钱了，只好又回家来取。",
        "pinyin": "wǒ qù chāo shì mǎi fāng biàn miàn ， kě shì yīn wèi zháo jí ， wàng dài qián le ， zhǐ hǎo yòu huí jiā lái qǔ 。",
        "hanviet": "Ngã Khứ Siêu Thị Mãi Phương Tiện Diện ， Khả Thị Nhân Vị Trước Cấp ， Vong Đới Tiền Liễu ， Chỉ Hảo Hựu Hồi Gia Lai Thủ 。",
        "meaning": "Tôi đi siêu thị mua mì ăn liền, nhưng vì vội vàng nên quên mang tiền, đành phải về nhà lấy lại.",
        "tokens": [
            { "text": "超市", "type": "core", "role": "Danh từ (siêu thị)" },
            { "text": "方便面", "type": "advanced", "role": "Danh từ (mì ăn liền)" },
            { "text": "可是", "type": "grammar", "role": "Liên từ chuyển ý" },
            { "text": "因为", "type": "grammar", "role": "Liên từ nguyên nhân" },
            { "text": "着急", "type": "core", "role": "Tính từ (vội vã)" },
            { "text": "忘", "type": "normal", "role": "Động từ (quên)" },
            { "text": "只好", "type": "grammar", "role": "Phó từ (đành phải)" },
            { "text": "回家", "type": "normal", "role": "Động từ" },
            { "text": "取", "type": "core", "role": "Động từ (lấy)" }
        ],
        "grammar_point": {
            "name": "Chuỗi liên từ logic thời gian & chuyển ý: 可是……因为……只好……",
            "pattern": "Hành động ban đầu -> Chuyển ý phát sinh vấn đề (可是) -> Giải pháp bắt buộc (只好)",
            "level": "HSK 4",
            "trap_note": "BẪY THI: Câu C mở đầu nêu bối cảnh đi siêu thị. Câu B dùng '可是' chuyển ý giải thích sự cố quên tiền. Câu A dùng '只好' (đành phải) đưa ra kết quả xử lý cuối cùng.",
            "explanation": "Thứ tự mạch lạc logic sự việc diễn biến tự nhiên theo thời gian."
        },
        "breakdown": [
            { "role": "Bối cảnh xuất phát", "text": "我去超市买方便面", "type": "subject", "desc": "Mục tiêu ban đầu" },
            { "role": "Sự cố phát sinh", "text": "可是因为着急忘带钱了", "type": "grammar", "desc": "Tình huống bất ngờ" },
            { "role": "Giải pháp ứng biến", "text": "只好又回家来取", "type": "verb", "desc": "Hành động khắc phục" }
        ],
        "practice": {
            "type": "sentence_logic",
            "scrambled_items": [
                { "key": "A", "text": "只好又回家来取" },
                { "key": "B", "text": "可是因为着急，忘带钱了" },
                { "key": "C", "text": "我去超市买方便面" }
            ],
            "correct_order": "CBA",
            "explanation": "C (Đi siêu thị) -> B (Phát hiện quên tiền) -> A (Đành quay về nhà lấy)."
        }
    },
    {
        "id": "hsk4_test3_q58",
        "category": "sentence_logic",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 阅读 第二部分 (第58题)",
        "zh": "登机前要先托运行李，然后再领登机牌。",
        "pinyin": "dēng jī qián yào xiān tuō yùn xíng li ， rán hòu zài lǐng dēng jī pái 。",
        "hanviet": "Đăng Cơ Tiền Yếu Tiên Thác Vận Hành Lý ， Nhiên Hậu Tái Lãnh Đăng Cơ Bài 。",
        "meaning": "Trước khi lên máy bay cần phải gửi hành lý trước, sau đó mới lấy thẻ lên máy bay.",
        "tokens": [
            { "text": "登机", "type": "advanced", "role": "Động từ (lên máy bay)" },
            { "text": "前", "type": "normal", "role": "Từ chỉ thời gian" },
            { "text": "先", "type": "grammar", "role": "Phó từ (trước tiên)" },
            { "text": "托运", "type": "advanced", "role": "Động từ HSK 4 (ký gửi hành lý)" },
            { "text": "行李", "type": "core", "role": "Danh từ (hành lý)" },
            { "text": "然后", "type": "grammar", "role": "Liên từ (sau đó)" },
            { "text": "再", "type": "grammar", "role": "Phó từ (mới/tiếp tục)" },
            { "text": "登机牌", "type": "advanced", "role": "Danh từ HSK 4 (thẻ lên máy bay)" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ trình tự thao tác kinh điển: 先……然后（再）……",
            "pattern": "Mốc thời gian quy định + 先 + Bước 1 + 然后再 + Bước 2",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Khi thấy '先' và '然后', chắc chắn mệnh đề có chữ '先' phải đứng trước mệnh đề có '然后'. '登机前' nêu mốc thời gian lớn nên luôn đứng ở đầu câu.",
            "explanation": "Quy trình sân bay chuẩn: Check-in ký gửi hành lý trước, nhận boarding pass sau."
        },
        "breakdown": [
            { "role": "Mốc thời gian", "text": "登机前", "type": "subject", "desc": "Thời điểm thực hiện chuỗi quy trình" },
            { "role": "Bước 1 (Ưu tiên)", "text": "要先托运行李", "type": "verb", "desc": "Ký gửi kiện hàng" },
            { "role": "Bước 2 (Tiếp theo)", "text": "然后再领登机牌", "type": "verb", "desc": "Nhận vé thẻ lên tàu" }
        ],
        "practice": {
            "type": "sentence_logic",
            "scrambled_items": [
                { "key": "A", "text": "要先托运行李" },
                { "key": "B", "text": "登机前" },
                { "key": "C", "text": "然后再领登机牌" }
            ],
            "correct_order": "BAC",
            "explanation": "B (Mốc thời gian '登机前') -> Cặp liên từ '先……然后……' (A -> C)."
        }
    },
    {
        "id": "hsk4_test3_q63",
        "category": "sentence_logic",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 阅读 第二部分 (第63题)",
        "zh": "无论是在家里还是在公共场所，老年人都应该受到尊敬。",
        "pinyin": "wú lùn shì zài jiā lǐ hái shì zài gōng gòng chǎng suǒ ， lǎo nián rén dōu yīng gāi shòu dào zūn jìng 。",
        "hanviet": "Vô Luận Thị Tại Gia Lý Hoàn Thị Tại Công Cộng Tràng Sở ， Lão Niên Nhân Đô Ưng Cai Thụ Đáo Tôn Kính 。",
        "meaning": "Bất luận là ở trong nhà hay ở nơi công cộng, người cao tuổi đều nên nhận được sự tôn kính.",
        "tokens": [
            { "text": "无论", "type": "grammar", "role": "Liên từ vô điều kiện (dù cho/bất luận)" },
            { "text": "还是", "type": "grammar", "role": "Liên từ lựa chọn (hay là)" },
            { "text": "公共场所", "type": "core", "role": "Cụm danh từ (nơi công cộng)" },
            { "text": "老年人", "type": "core", "role": "Danh từ (người già)" },
            { "text": "都", "type": "grammar", "role": "Phó từ chỉ phạm vi toàn thể" },
            { "text": "受到", "type": "core", "role": "Động từ (nhận được)" },
            { "text": "尊敬", "type": "core", "role": "Động từ/Danh từ HSK 4 (kính trọng)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc liên từ điều kiện vô hạn: 无论……还是……都……",
            "pattern": "无论 + Phương án 1 + 还是 + Phương án 2, Chủ ngữ + 都 + Vị ngữ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: '无论' luôn đi đôi với '还是' ở vế phụ và bắt buộc phải có '都' (hoặc '也') ở vế chính để biểu thị mọi trường hợp đều áp dụng một kết luận duy nhất.",
            "explanation": "'尊敬' (tôn kính) là từ đạo đức truyền thống thường xuất hiện trong các bài đọc HSK 4."
        },
        "breakdown": [
            { "role": "Điều kiện liệt kê 1", "text": "无论是在家里", "type": "grammar", "desc": "Môi trường gia đình" },
            { "role": "Điều kiện liệt kê 2", "text": "还是在公共场所", "type": "grammar", "desc": "Môi trường xã hội bên ngoài" },
            { "role": "Kết luận phổ quát", "text": "老年人都应该受到尊敬", "type": "verb", "desc": "Đạo lý tôn kính người lớn tuổi" }
        ],
        "practice": {
            "type": "sentence_logic",
            "scrambled_items": [
                { "key": "A", "text": "无论是在家里" },
                { "key": "B", "text": "还是在公共场所" },
                { "key": "C", "text": "老年人都应该受到尊敬" }
            ],
            "correct_order": "ABC",
            "explanation": "Cặp liên từ cố định '无论 (A) ……还是 (B) ……' dẫn tới kết luận với '都' (C)."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test 46-55)
    # =========================================================================
    {
        "id": "hsk4_test3_q46",
        "category": "cloze",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 阅读 第一部分 (选词填空 第46题)",
        "zh": "美国总统奥巴马应中国国家主席胡锦涛的邀请来华进行国事访问。",
        "pinyin": "měi guó zǒng tǒng ào bā mǎ yīng zhōng guó guó jiā zhǔ xí hú jǐn tāo de yāo qǐng lái huá jìn xíng guó shì fǎng wèn 。",
        "hanviet": "Mỹ Quốc Tổng Thống Áo Ba Mã Ứng Trung Quốc Quốc Gia Chủ Tịch Hồ Cẩm Đào Đích Yêu Thỉnh Lai Hoa Tiến Hành Quốc Sự Phóng Vấn 。",
        "meaning": "Tổng thống Mỹ Obama nhận lời mời của Chủ tịch nước Trung Quốc Hồ Cẩm Đào đến thăm Trung Quốc trong chuyến thăm cấp nhà nước.",
        "tokens": [
            { "text": "应", "type": "grammar", "role": "Giới từ cố định (nhận theo, đáp ứng)" },
            { "text": "邀请", "type": "core", "role": "Danh từ/Động từ HSK 4 (lời mời)" },
            { "text": "进行", "type": "core", "role": "Động từ chính (tiến hành)" },
            { "text": "访问", "type": "core", "role": "Danh từ (chuyến thăm)" }
        ],
        "grammar_point": {
            "name": "Cụm giới từ cố định ngoại giao: 应……的邀请 (Nhận lời mời của...)",
            "pattern": "应 + Nhân vật / Cơ quan + 的邀请 + Hành động",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Khi thấy cấu trúc '应……的 [ ? ]', 99% đáp án đúng trong đề HSK là từ '邀请' (lời mời) hoặc '要求' (yêu cầu). Ở ngữ cảnh này là chuyến thăm nên bắt buộc chọn '邀请'.",
            "explanation": "'应……的邀请' là cấu trúc văn phong trang trọng chuẩn trong tiếng Trung báo chí và đề thi."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "美国总统奥巴马", "type": "subject", "desc": "Chủ thể thực hiện chuyến thăm" },
            { "role": "Trạng ngữ nguyên cớ", "text": "应……的邀请", "type": "grammar", "desc": "Theo lời mời chính thức" },
            { "role": "Vị ngữ mục đích", "text": "来华进行国事访问", "type": "verb", "desc": "Đến Trung Quốc thăm chính thức" }
        ],
        "practice": {
            "type": "cloze",
            "target_word": "邀请",
            "blank_sentence": "美国总统奥巴马应中国国家主席胡锦涛的（ ____ ）来华进行国事访问。",
            "options": [
                { "word": "邀请", "pinyin": "yāoqǐng", "hanviet": "Yêu Thỉnh", "meaning": "lời mời, mời" },
                { "word": "抽", "pinyin": "chōu", "hanviet": "Trừu", "meaning": "rút ra, trích ra" },
                { "word": "坚持", "pinyin": "jiānchí", "hanviet": "Kiên Trì", "meaning": "kiên trì" },
                { "word": "方便", "pinyin": "fāngbiàn", "hanviet": "Phương Tiện", "meaning": "thuận tiện" }
            ],
            "clue": "Cụm từ cố định trong văn phong ngoại giao: '应……的邀请' (nhận lời mời của ai đó)."
        }
    },
    {
        "id": "hsk4_test3_q47",
        "category": "cloze",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 阅读 第一部分 (选词填空 第47题)",
        "zh": "我家虽然离市中心比较远，但是交通很方便。",
        "pinyin": "wǒ jiā suī rán lí shì zhōng xīn bǐ jiào yuǎn ， dàn shì jiāo tōng hěn fāng biàn 。",
        "hanviet": "Ngã Gia Tuy Nhiên Ly Thị Trung Tâm Bỉ Giảo Viễn ， Đãn Thị Giao Thông Ngận Phương Tiện 。",
        "meaning": "Nhà tôi tuy cách trung tâm thành phố khá xa, nhưng giao thông rất thuận tiện.",
        "tokens": [
            { "text": "虽然", "type": "grammar", "role": "Liên từ nhượng bộ" },
            { "text": "离", "type": "grammar", "role": "Giới từ cự ly" },
            { "text": "市中心", "type": "core", "role": "Danh từ (trung tâm thành phố)" },
            { "text": "但是", "type": "grammar", "role": "Liên từ tương phản" },
            { "text": "交通", "type": "core", "role": "Danh từ (giao thông)" },
            { "text": "方便", "type": "core", "role": "Tính từ HSK 4 (tiện lợi, thuận tiện)" }
        ],
        "grammar_point": {
            "name": "Cụm danh - tính cố định: 交通 + 方便 (Giao thông thuận tiện)",
            "pattern": "虽然……但是……, 交通 + 很 + 方便",
            "level": "HSK 4",
            "trap_note": "BẪY THI: '交通' (giao thông) đi kèm với tính từ miêu tả điều kiện di chuyển thì từ chuẩn xác nhất luôn là '方便' (thuận tiện) hoặc '拥挤' (tắc nghẽn).",
            "explanation": "Cặp liên từ '虽然……但是……' đối lập giữa nhược điểm 'xa trung tâm' và ưu điểm 'giao thông tiện lợi'."
        },
        "breakdown": [
            { "role": "Vế nhượng bộ", "text": "我家虽然离市中心比较远", "type": "subject", "desc": "Khoảng cách địa lý" },
            { "role": "Vế chuyển ý", "text": "但是交通很方便", "type": "verb", "desc": "Ưu điểm bù lại" }
        ],
        "practice": {
            "type": "cloze",
            "target_word": "方便",
            "blank_sentence": "我家虽然离市中心比较远，但是交通很（ ____ ）。",
            "options": [
                { "word": "方便", "pinyin": "fāngbiàn", "hanviet": "Phương Tiện", "meaning": "thuận tiện, tiện lợi" },
                { "word": "到处", "pinyin": "dàochù", "hanviet": "Đáo Xứ", "meaning": "khắp nơi" },
                { "word": "下来", "pinyin": "xiàlái", "hanviet": "Hạ Lai", "meaning": "xuống đây" },
                { "word": "坚持", "pinyin": "jiānchí", "hanviet": "Kiên Trì", "meaning": "kiên trì" }
            ],
            "clue": "Từ thích hợp nhất đứng sau phó từ chỉ mức độ '很' để bổ nghĩa cho '交通' là tính từ '方便'."
        }
    },
    {
        "id": "hsk4_test3_q51",
        "category": "cloze",
        "test_id": 3,
        "source": "HSK 4 模拟试卷 3 阅读 第一部分 (选词填空 第51题)",
        "zh": "李师傅，您看我这套房子要装修的话，大概需要多少钱？",
        "pinyin": "lǐ shī fu ， nín kàn wǒ zhè tào fáng zi yào zhuāng xiū de huà ， dà gài xū yào duō shao qián ？",
        "hanviet": "Lý Sư Phó ， Nẫm Khán Ngã Giá Sáo Phòng Tử Yếu Trang Tu Đích Thoại ， Đại Khái Nhu Yếu Đa Thiểu Tiền ？",
        "meaning": "Bác Lý, bác xem căn nhà này của cháu nếu sửa sang nội thất thì khoảng chừng cần bao nhiêu tiền?",
        "tokens": [
            { "text": "师傅", "type": "core", "role": "Từ xưng hô tôn kính (thợ/bác tài)" },
            { "text": "装修", "type": "advanced", "role": "Động từ HSK 4 (trang trí nội thất)" },
            { "text": "的话", "type": "grammar", "role": "Trợ từ giả thiết" },
            { "text": "大概", "type": "core", "role": "Phó từ ước lượng (khoảng chừng)" },
            { "text": "需要", "type": "core", "role": "Động từ (cần)" }
        ],
        "grammar_point": {
            "name": "Phó từ ước tính số lượng: 大概 (Khoảng chừng / Áng chừng)",
            "pattern": "大概 + 需要 / 有 / 达到 + Số lượng ước tính",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Khi hỏi dự toán kinh phí chưa có con số chính xác ('多少钱'), phó từ đi cùng động từ '需要' thích hợp nhất là '大概' (đại khái/khoảng chừng).",
            "explanation": "Câu trả lời ở vế sau ('至少也得三四万' - ít nhất cũng 30-40 ngàn) càng khẳng định tính chất ước chừng của '大概'."
        },
        "breakdown": [
            { "role": "Lời chào mở đầu", "text": "李师傅", "type": "subject", "desc": "Người được hỏi ý kiến" },
            { "role": "Mệnh đề giả thiết", "text": "这套房子要装修的话", "type": "grammar", "desc": "Điều kiện đặt ra" },
            { "role": "Truy vấn ước lượng", "text": "大概需要多少钱", "type": "verb", "desc": "Hỏi kinh phí ước tính" }
        ],
        "practice": {
            "type": "cloze",
            "target_word": "大概",
            "blank_sentence": "李师傅，您看我这套房子要装修的话，（ ____ ）需要多少钱？",
            "options": [
                { "word": "大概", "pinyin": "dàgài", "hanviet": "Đại Khái", "meaning": "khoảng chừng, đại khái" },
                { "word": "温度", "pinyin": "wēndù", "hanviet": "Ôn Độ", "meaning": "nhiệt độ" },
                { "word": "答案", "pinyin": "dá'àn", "hanviet": "Đáp Án", "meaning": "đáp án" },
                { "word": "决定", "pinyin": "juédìng", "hanviet": "Quyết Định", "meaning": "quyết định" }
            ],
            "clue": "Đứng trước động từ '需要' và từ để hỏi '多少钱', cần một phó từ chỉ sự ước lượng."
        }
    }
]
