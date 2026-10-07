# -*- coding: utf-8 -*-
"""
Authentic items curated from HSK 4 模拟试卷 7 (Mock Test 7).
Source: Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
"""

TEST7_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building 86-95)
    # =========================================================================
    {
        "id": "hsk4_test7_q86",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第86题)",
        "zh": "你想去南方工作吗？",
        "pinyin": "nǐ xiǎng qù nán fāng gōng zuò ma ？",
        "hanviet": "Nhĩ Tưởng Khứ Nam Phương Công Tác Ma ？",
        "meaning": "Bạn có muốn đi miền nam làm việc không?",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Chủ ngữ" },
            { "text": "想", "type": "grammar", "role": "Động từ năng nguyện (muốn)" },
            { "text": "去", "type": "normal", "role": "Động từ di chuyển" },
            { "text": "南方", "type": "core", "role": "Nơi chốn (miền nam)" },
            { "text": "工作", "type": "core", "role": "Động từ mục đích (làm việc)" },
            { "text": "吗", "type": "grammar", "role": "Trợ từ nghi vấn" }
        ],
        "grammar_point": {
            "name": "Câu liên động biểu thị nguyện vọng đi nơi khác làm việc: 想 + 去 + Nơi chốn + Động từ + 吗",
            "pattern": "Chủ ngữ + 想 / 要 + 去 + Địa điểm + Động từ mục đích + 吗？",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: Hành động di chuyển địa lý '去南方' phải đứng trước hành động mục đích nghề nghiệp '工作'. Không được đảo ngược thành '工作去南方'.",
            "explanation": "Câu nghi vấn đơn giản nhưng kiểm tra vững chắc trật tự từ trong câu liên động kèm trợ từ năng nguyện '想'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你", "type": "subject", "desc": "Đối tượng giao tiếp" },
            { "role": "Trợ động từ", "text": "想", "type": "grammar", "desc": "Hỏi về ý muốn, nguyện vọng" },
            { "role": "Động từ 1 + Địa điểm", "text": "去南方", "type": "verb", "desc": "Chuyển tới khu vực phía nam" },
            { "role": "Động từ 2 (Mục đích)", "text": "工作", "type": "verb", "desc": "Mục tiêu công tác, lập nghiệp" },
            { "role": "Trợ từ nghi vấn", "text": "吗", "type": "grammar", "desc": "Tạo câu hỏi Có/Không" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["工作", "想", "吗", "去南方", "你"],
            "target_chunks": ["你", "想", "去南方", "工作", "吗"],
            "hint": "Cấu trúc: 你 + 想 + 去南方 + 工作 + 吗？"
        }
    },
    {
        "id": "hsk4_test7_q87",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第87题)",
        "zh": "校长派张老师去上海开会。",
        "pinyin": "xiào zhǎng pài zhāng lǎo shī qù shàng hǎi kāi huì 。",
        "hanviet": "Hiệu Trưởng Phái Trương Lão Sư Khứ Thượng Hải Khai Hội 。",
        "meaning": "Hiệu trưởng cử thầy Trương đi Thượng Hải dự họp.",
        "tokens": [
            { "text": "校长", "type": "core", "role": "Chủ ngữ (hiệu trưởng)" },
            { "text": "派", "type": "grammar", "role": "Động từ chỉ định kiêm ngữ (cử, phái)" },
            { "text": "张老师", "type": "core", "role": "Kiêm ngữ (tân ngữ của 派, chủ ngữ của 去上海开会)" },
            { "text": "去", "type": "normal", "role": "Động từ liên động di chuyển" },
            { "text": "上海", "type": "normal", "role": "Nơi chốn" },
            { "text": "开会", "type": "core", "role": "Động từ mục đích (họp)" }
        ],
        "grammar_point": {
            "name": "Câu kiêm ngữ với động từ cử phái: 派 + Người + Đi đâu làm gì",
            "pattern": "Người ra lệnh (Chủ ngữ 1) + 派 / 请 / 让 + Người thực hiện (Kiêm ngữ) + 去 + Địa điểm + Hành động",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Động từ '派' (phái, cử) chỉ thẩm quyền cấp trên điều động cấp dưới. Người được điều động '张老师' đứng ngay sau '派', sau đó mới đến nhiệm vụ công tác '去上海开会'.",
            "explanation": "'张老师' vừa nhận tác động của lệnh điều động từ '校长', vừa là chủ thể trực tiếp đi Thượng Hải họp."
        },
        "breakdown": [
            { "role": "Cấp trên điều động", "text": "校长", "type": "subject", "desc": "Người có thẩm quyền quyết định" },
            { "role": "Động từ sai khiến/cử phái", "text": "派", "type": "verb", "desc": "Ra lệnh phân công nhiệm vụ" },
            { "role": "Người nhận lệnh (Kiêm ngữ)", "text": "张老师", "type": "subject", "desc": "Cán bộ được giao trọng trách" },
            { "role": "Nhiệm vụ thực hiện", "text": "去上海开会", "type": "verb", "desc": "Cụm liên động đến Thượng Hải dự hội nghị" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["开会", "去上海", "校长", "张老师", "派"],
            "target_chunks": ["校长", "派", "张老师", "去上海", "开会"],
            "hint": "Cấu trúc câu kiêm ngữ: 校长 + 派 + 张老师 + 去上海 + 开会."
        }
    },
    {
        "id": "hsk4_test7_q88",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第88题)",
        "zh": "这次的成绩让我很高兴。",
        "pinyin": "zhè cì de chéng jì ràng wǒ hěn gāo xìng 。",
        "hanviet": "Giá Thứ Đích Thành Tích Nhượng Ngã Hẩn Cao Hứng 。",
        "meaning": "Thành tích lần này khiến tôi vô cùng vui mừng.",
        "tokens": [
            { "text": "这次的", "type": "normal", "role": "Định ngữ chỉ thị" },
            { "text": "成绩", "type": "core", "role": "Chủ ngữ trung tâm (kết quả/thành tích)" },
            { "text": "让", "type": "grammar", "role": "Động từ kiêm ngữ gây khiến (khiến cho/làm cho)" },
            { "text": "我", "type": "normal", "role": "Kiêm ngữ (tân ngữ của 让, chủ thể của 高兴)" },
            { "text": "很", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "高兴", "type": "core", "role": "Tính từ trạng thái cảm xúc" }
        ],
        "grammar_point": {
            "name": "Câu kiêm ngữ biểu thị sự tác động tâm lý: Sự vật / Sự việc + 让 / 使 + Ai đó + Tính từ cảm xúc",
            "pattern": "Chủ ngữ (Nguyên nhân) + 让 / 使 + Đối tượng tiếp nhận + (很 / 非常) + Tính từ trạng thái",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '让' mang nghĩa gây khiến ('làm cho tôi...'). Tính từ miêu tả cảm xúc '高兴' đứng ở vị trí cuối cùng vị ngữ.",
            "explanation": "Kết quả thi tốt '这次的成绩' là nguyên nhân trực tiếp kích thích cảm xúc phấn khởi '很高兴' của nhân vật '我'."
        },
        "breakdown": [
            { "role": "Nguyên nhân kích thích", "text": "这次的成绩", "type": "subject", "desc": "Kết quả kiểm tra đạt được" },
            { "role": "Động từ gây khiến", "text": "让", "type": "verb", "desc": "Tác động làm chuyển biến tâm trạng" },
            { "role": "Người tiếp nhận tâm lý", "text": "我", "type": "subject", "desc": "Chủ thể cảm nhận niềm vui" },
            { "role": "Trạng thái cảm xúc", "text": "很高兴", "type": "modifier", "desc": "Mức độ vui sướng, hài lòng" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["很", "高兴", "让", "这次的成绩", "我"],
            "target_chunks": ["这次的成绩", "让", "我", "很", "高兴"],
            "hint": "Cấu trúc: Chủ ngữ nguyên nhân (这次的成绩) + 让 + 我 + 很高兴."
        }
    },
    {
        "id": "hsk4_test7_q89",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第89题)",
        "zh": "我终于把作业做完了。",
        "pinyin": "wǒ zhōng yú bǎ zuò yè zuò wán le 。",
        "hanviet": "Ngã Chung Vu Bả Tác Nghiệp Tác Hoàn Liễu 。",
        "meaning": "Cuối cùng thì tôi cũng đã làm xong bài tập rồi.",
        "tokens": [
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "终于", "type": "core", "role": "Phó từ biểu thị sự việc chờ đợi đã thành hiện thực (cuối cùng)" },
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "作业", "type": "core", "role": "Tân ngữ chịu xử lý (bài tập)" },
            { "text": "做", "type": "normal", "role": "Động từ chính" },
            { "text": "完", "type": "grammar", "role": "Bổ ngữ kết quả (xong, hết)" },
            { "text": "了", "type": "normal", "role": "Trợ từ hoàn thành" }
        ],
        "grammar_point": {
            "name": "Câu chữ 把 kết hợp Phó từ 终于 và Bổ ngữ kết quả 完",
            "pattern": "Chủ ngữ + 终于 + 把 + Đối tượng cụ thể + Động từ + 完 + 了",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Phó từ '终于' bắt buộc phải đứng TRƯỚC giới từ '把'. Động từ trong câu chữ 把 bắt buộc phải có bổ ngữ hoàn tất (ở đây là '完了').",
            "explanation": "'终于' giải tỏa tâm lý căng thẳng sau quá trình nỗ lực kéo dài để giải quyết toàn bộ bài tập '把作业做完了'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我", "type": "subject", "desc": "Người hoàn thành bài" },
            { "role": "Trạng ngữ mong đợi", "text": "终于", "type": "modifier", "desc": "Nhấn mạnh kết quả sau thời gian dài mong ngóng" },
            { "role": "Giới từ 把 + Đối tượng", "text": "把作业", "type": "object", "desc": "Đưa đối tượng bài tập lên trước động từ" },
            { "role": "Vị ngữ + Bổ ngữ kết quả", "text": "做完了", "type": "verb", "desc": "Động từ '做' kết hợp bổ ngữ '完' và trợ từ '了'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["做完了", "终于", "我", "把作业"],
            "target_chunks": ["我", "终于", "把作业", "做完了"],
            "hint": "Cấu trúc: Chủ ngữ (我) + 终于 + 把作业 + 做完了."
        }
    },
    {
        "id": "hsk4_test7_q90",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第90题)",
        "zh": "那个孩子太不听话了。",
        "pinyin": "nà ge hái zi tài bù tīng huà le 。",
        "hanviet": "Na Cá Hài Tử Thái Bất Thính Thoại Liễu 。",
        "meaning": "Đứa bé đó quá không biết nghe lời rồi.",
        "tokens": [
            { "text": "那个", "type": "normal", "role": "Đại từ chỉ định" },
            { "text": "孩子", "type": "core", "role": "Chủ ngữ (đứa trẻ)" },
            { "text": "太", "type": "grammar", "role": "Phó từ mức độ cực điểm (quá/lắm)" },
            { "text": "不", "type": "grammar", "role": "Phó từ phủ định chèn sau 太" },
            { "text": "听话", "type": "core", "role": "Tính từ / Động từ ly hợp (ngoan ngoãn, nghe lời)" },
            { "text": "了", "type": "grammar", "role": "Trợ từ ngữ khí cảm thán đi kèm 太" }
        ],
        "grammar_point": {
            "name": "Cấu trúc cảm thán phủ định: 太 + 不 + Tính từ + 了",
            "pattern": "Chủ ngữ + 太 + 不 + Tính từ / Động từ tâm lý + 了",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY CẤU TRÚC: Cấu trúc cảm thán '太...了' khi muốn phủ định thì từ phủ định '不' phải đặt ở GIỮA '太' và tính từ ('太不听话了'), không được nói '不太听话了' (vì 不太... mang nghĩa 'không... lắm', sắc thái nhẹ hơn nhiều).",
            "explanation": "'太不听话了' mang sắc thái trách cứ, phê phán gay gắt tính khí bướng bỉnh của đứa bé."
        },
        "breakdown": [
            { "role": "Chủ ngữ định-trung", "text": "那个孩子", "type": "subject", "desc": "Đứa trẻ được quan sát" },
            { "role": "Cấu trúc cảm thán cực điểm", "text": "太...了", "type": "grammar", "desc": "Biểu đạt mức độ quá giới hạn" },
            { "role": "Trọng tâm tính chất phủ định", "text": "不听话", "type": "verb", "desc": "Không chịu vâng lời người lớn" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["太不听话了", "那个", "孩子"],
            "target_chunks": ["那个", "孩子", "太不听话了"],
            "hint": "Chủ ngữ (那个孩子) + Cụm cảm thán phủ định (太不听话了)."
        }
    },
    {
        "id": "hsk4_test7_q91",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第91题)",
        "zh": "有什么意见就提出来吧。",
        "pinyin": "yǒu shén me yì jiàn jiù tí chū lái ba 。",
        "hanviet": "Hữu Thập Ma Ý Kiến Tựu Đề Xuất Lai Ba 。",
        "meaning": "Có ý kiến gì thì cứ nêu ra đi.",
        "tokens": [
            { "text": "有", "type": "normal", "role": "Động từ sở hữu" },
            { "text": "什么", "type": "grammar", "role": "Đại từ phiếm chỉ (bất cứ điều gì)" },
            { "text": "意见", "type": "core", "role": "Tân ngữ (ý kiến, đề xuất, phản ánh)" },
            { "text": "就", "type": "grammar", "role": "Phó từ liên kết nối vế (thì)" },
            { "text": "提", "type": "core", "role": "Động từ chính (nêu, đưa ra)" },
            { "text": "出来", "type": "grammar", "role": "Bổ ngữ xu hướng kép (ra)" },
            { "text": "吧", "type": "normal", "role": "Trợ từ ngữ khí khích lệ" }
        ],
        "grammar_point": {
            "name": "Đại từ phiếm chỉ 什么 và Bổ ngữ xu hướng 出来",
            "pattern": "有 + 什么 + Danh từ + 就 + Động từ + 出来 / 下去 + 吧",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ HƯ: '什么' ở đây là cách dùng phiếm chỉ (bất kỳ ý kiến nào), không mang nghĩa hỏi 'cái gì'. '提出来' dùng bổ ngữ xu hướng kép để chỉ việc biến ý nghĩ trong đầu thành lời nói rõ ràng.",
            "explanation": "Câu nói khích lệ mọi người thẳng thắn đóng góp quan điểm trong buổi họp hoặc thảo luận."
        },
        "breakdown": [
            { "role": "Tiền đề điều kiện", "text": "有什么意见", "type": "subject", "desc": "Nếu có bất kỳ quan điểm hoặc góp ý nào" },
            { "role": "Liên từ phản ứng", "text": "就", "type": "modifier", "desc": "Nối trực tiếp hành động tương ứng" },
            { "role": "Vị ngữ + Bổ ngữ xu hướng", "text": "提出来吧", "type": "verb", "desc": "Động từ '提' kết hợp '出来' và trợ từ ngữ khí '吧'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["就提出来吧", "意见", "有", "什么"],
            "target_chunks": ["有", "什么", "意见", "就提出来吧"],
            "hint": "Cấu trúc: 有 + 什么 + 意见 + 就提出来吧."
        }
    },
    {
        "id": "hsk4_test7_q92",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第92题)",
        "zh": "你不要太伤心了。",
        "pinyin": "nǐ bú yào tài shāng xīn le 。",
        "hanviet": "Nhĩ Bất Yếu Thái Thương Tâm Liễu 。",
        "meaning": "Bạn đừng nên quá đau lòng nữa.",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Chủ ngữ" },
            { "text": "不要", "type": "grammar", "role": "Phó từ khuyên răn/ngăn cản (đừng/không nên)" },
            { "text": "太", "type": "normal", "role": "Phó từ mức độ (quá)" },
            { "text": "伤心", "type": "core", "role": "Tính từ biểu cảm (đau buồn/thương tâm)" },
            { "text": "了", "type": "grammar", "role": "Trợ từ ngữ khí biến hóa (nữa)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc khuyên can, an ủi: 不要 + 太 + Tính từ + 了",
            "pattern": "Chủ ngữ + 不要 / 别 + (太) + Tính từ / Động từ + 了",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY NGỮ DỤNG: '不要...了' mang hàm ý chấm dứt một trạng thái đang diễn ra ('đừng... nữa'). '伤心' là tính từ chỉ nỗi buồn sâu sắc.",
            "explanation": "Câu khẩu ngữ thân tình dùng để vỗ về người thân hoặc bạn bè vừa trải qua chuyện không vui."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你", "type": "subject", "desc": "Người bạn đang buồn bã" },
            { "role": "Khuyên can ngăn trở", "text": "不要", "type": "grammar", "desc": "Khuyên chấm dứt trạng thái tiêu cực" },
            { "role": "Vị ngữ tính từ cảm xúc", "text": "太伤心了", "type": "verb", "desc": "Nỗi đau buồn quá mức cho phép" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["太伤心了", "不要", "你"],
            "target_chunks": ["你", "不要", "太伤心了"],
            "hint": "Cấu trúc an ủi: 主语 (你) + 不要 + 太伤心了."
        }
    },
    {
        "id": "hsk4_test7_q93",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第93题)",
        "zh": "我数到3就可以开始了。",
        "pinyin": "wǒ shǔ dào sān jiù kě yǐ kāi shǐ le 。",
        "hanviet": "Ngã Số Đáo Tam Tựu Khả Dĩ Khai Thủy Liễu 。",
        "meaning": "Tôi đếm đến 3 là có thể bắt đầu được rồi.",
        "tokens": [
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "数", "type": "core", "role": "Động từ phát âm shǔ (đếm)" },
            { "text": "到", "type": "grammar", "role": "Bổ ngữ kết quả đạt mốc" },
            { "text": "3", "type": "normal", "role": "Con số mốc đích (tam)" },
            { "text": "就", "type": "grammar", "role": "Phó từ liên kết thời điểm (là/thì)" },
            { "text": "可以", "type": "normal", "role": "Động từ năng nguyện (có thể)" },
            { "text": "开始", "type": "core", "role": "Động từ chính" },
            { "text": "了", "type": "normal", "role": "Trợ từ ngữ khí" }
        ],
        "grammar_point": {
            "name": "Bổ ngữ kết quả 到 chỉ mốc đạt được và Liên từ 就",
            "pattern": "Chủ ngữ + Động từ + 到 + Mốc số lượng + 就 + 可以 + Hành động tiếp theo",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY ĐỌC ÂM: Chữ '数' ở đây là động từ mang thanh 3 (shǔ - đếm), không phải danh từ thanh 4 (shù - con số). '数到3' là mốc điều kiện kích hoạt hành vi sau '就'.",
            "explanation": "Câu khẩu ngữ vô cùng quen thuộc trong các trò chơi, chụp ảnh, hoặc cuộc thi xuất phát."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我", "type": "subject", "desc": "Người đếm hiệu lệnh" },
            { "role": "Hành vi đạt mốc", "text": "数到3", "type": "verb", "desc": "Động từ đếm đạt tới con số quy định" },
            { "role": "Mệnh đề kích hoạt", "text": "就可以开始了", "type": "verb", "desc": "Chuyển sang trạng thái hành động kế tiếp" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["就可以开始了", "数到3", "我"],
            "target_chunks": ["我", "数到3", "就可以开始了"],
            "hint": "Ai (我) + Làm gì tới đâu (数到3) + Thì làm sao (就可以开始了)."
        }
    },
    {
        "id": "hsk4_test7_q94",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第94题)",
        "zh": "这位就是我的大学老师。",
        "pinyin": "zhè wèi jiù shì wǒ de dà xué lǎo shī 。",
        "hanviet": "Giá Vị Tựu Thị Ngã Đích Đại Học Lão Sư 。",
        "meaning": "Vị này chính là giáo viên thời đại học của tôi.",
        "tokens": [
            { "text": "这位", "type": "core", "role": "Chủ ngữ đại từ chỉ thị kèm lượng từ kính trọng" },
            { "text": "就是", "type": "grammar", "role": "Phó từ nhấn mạnh + hệ từ (chính là)" },
            { "text": "我", "type": "normal", "role": "Đại từ sở hữu" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "大学", "type": "normal", "role": "Cấp bậc trường học" },
            { "text": "老师", "type": "core", "role": "Tân ngữ danh từ trung tâm (thầy cô giáo)" }
        ],
        "grammar_point": {
            "name": "Lượng từ kính cẩn 位 và Phó từ xác định 就是",
            "pattern": "这 / 那 + 位 + 就是 + Định ngữ sở hữu + Danh từ thân phận",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY TỪ XƯNG HÔ: '位' là lượng từ thể hiện sự tôn trọng đặc biệt khi giới thiệu người khác ('这位'). '就是' nhấn mạnh sự xác định tuyệt đối không thể nhầm lẫn.",
            "explanation": "Câu giới thiệu trang trọng danh tính của người thầy đại học trước mặt các vị khách hoặc đồng nghiệp."
        },
        "breakdown": [
            { "role": "Chủ ngữ kính cẩn", "text": "这位", "type": "subject", "desc": "Nhân vật đang đứng gần được tôn kính" },
            { "role": "Khẳng định danh tính", "text": "就是", "type": "verb", "desc": "Xác nhận chính xác 100%" },
            { "role": "Cụm danh từ định-trung", "text": "我的大学老师", "type": "object", "desc": "Thầy giáo thời còn theo học đại học" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["大学老师", "就是", "我的", "这位"],
            "target_chunks": ["这位", "就是", "我的", "大学老师"],
            "hint": "Chỉ định (这位) + Khẳng định (就是) + Sở hữu (我的大学老师)."
        }
    },
    {
        "id": "hsk4_test7_q95",
        "category": "sentence_building",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 书写 第一部分 (第95题)",
        "zh": "我怎么没听说过呢？",
        "pinyin": "wǒ zěn me méi tīng shuō guo ne ？",
        "hanviet": "Ngã Chẩm Ma Một Thính Thuyết Quá Nê ？",
        "meaning": "Sao tôi lại chưa từng nghe nói qua chuyện này nhỉ?",
        "tokens": [
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "怎么", "type": "grammar", "role": "Đại từ nghi vấn biểu thị sự ngạc nhiên thắc mắc (sao/thế nào)" },
            { "text": "没", "type": "grammar", "role": "Phó từ phủ định" },
            { "text": "听说", "type": "core", "role": "Động từ (nghe nói)" },
            { "text": "过", "type": "grammar", "role": "Trợ từ động thái chỉ kinh nghiệm" },
            { "text": "呢", "type": "grammar", "role": "Trợ từ ngữ khí nghi vấn tự hỏi" }
        ],
        "grammar_point": {
            "name": "Câu hỏi ngạc nhiên với đại từ nghi vấn: 怎么 + 没 + Động từ + 过 + 呢？",
            "pattern": "Chủ ngữ + 怎么 + 没 + Động từ + 过 + (Tân ngữ) + 呢？",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY NGỮ DỤNG: '怎么' ở đây kết hợp với phủ định kinh nghiệm '没...过' để thể hiện sự bất ngờ tột độ về một tin tức lẽ ra mình phải biết nhưng lại hoàn toàn chưa từng nghe thấy.",
            "explanation": "Trợ từ ngữ khí '呢' ở cuối câu tạo âm điệu tự vấn và khơi gợi người đối thoại giải thích thêm thông tin."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我", "type": "subject", "desc": "Người tiếp nhận thông tin bất ngờ" },
            { "role": "Trạng ngữ nghi vấn", "text": "怎么", "type": "modifier", "desc": "Hỏi lý do kèm sắc thái khó hiểu" },
            { "role": "Vị ngữ phủ định kinh nghiệm", "text": "没听说过", "type": "verb", "desc": "Chưa từng một lần nghe ai nhắc tới" },
            { "role": "Trợ từ ngữ khí", "text": "呢", "type": "grammar", "desc": "Làm mềm câu nghi vấn" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["没听说过", "怎么", "呢", "我"],
            "target_chunks": ["我", "怎么", "没听说过", "呢"],
            "hint": "Chủ ngữ (我) + Đại từ nghi vấn (怎么) + Phủ định kinh nghiệm (没听说过) + 呢？"
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Logic 56-65)
    # =========================================================================
    {
        "id": "hsk4_test7_q56",
        "category": "sentence_logic",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 阅读 第二部分 (第56题)",
        "zh": "如果明天下大雪，飞机无法起飞，那我就不能去开会了。",
        "pinyin": "rú guǒ míng tiān xià dà xuě ， fēi jī wú fǎ qǐ fēi ， nà wǒ jiù bù néng qù kāi huì le 。",
        "hanviet": "Như Quả Minh Thiên Hạ Đại Tuyết ， Phi Cơ Vô Pháp Khởi Phi ， Na Ngã Tựu Bất Năng Khứ Khai Hội Liễu 。",
        "meaning": "Nếu ngày mai tuyết rơi lớn, máy bay không thể cất cánh, thế thì tôi sẽ không thể đi họp được rồi.",
        "tokens": [
            { "text": "如果明天下大雪", "type": "core", "role": "Giả thiết thời tiết khởi đầu (A)" },
            { "text": "飞机无法起飞", "type": "core", "role": "Hệ quả trực tiếp về chuyến bay (B)" },
            { "text": "那我就不能去开会了", "type": "core", "role": "Hệ quả cuối cùng về lịch trình (C)" }
        ],
        "grammar_point": {
            "name": "Chuỗi liên hoàn giả thiết nhân quả: 如果... (A) -> Hệ quả 1 (B) -> 那...就... Hệ quả 2 (C)",
            "pattern": "如果 + Tình huống giả định + Hệ quả trung gian + 那 + 就 + Kết quả cuối cùng",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Giả thiết thời tiết '如果明天下大雪' dẫn tới máy bay bị ảnh hưởng '无法起飞', từ đó dẫn đến việc người nói không thể đến cuộc họp '那我就不能去开会了'. Trật tự logic tuần tự là A -> B -> C.",
            "explanation": "A đặt tiền đề thiên nhiên. B là tác động vật lý lên phương tiện. C là liên từ '那...就' rút ra kết luận đối với cá nhân."
        },
        "breakdown": [
            { "role": "Giả thiết thời tiết (A)", "text": "如果明天下大雪", "type": "subject", "desc": "Giả định về trận bão tuyết ngày mai" },
            { "role": "Hệ quả phương tiện (B)", "text": "飞机无法起飞", "type": "verb", "desc": "Hàng không bị đình trệ" },
            { "role": "Kết luận lịch trình (C)", "text": "那我就不能去开会了", "type": "object", "desc": "Lỡ dở công việc hội nghị" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "如果明天下大雪" },
                { "id": "B", "text": "飞机无法起飞" },
                { "id": "C", "text": "那我就不能去开会了" }
            ],
            "correct_order": "ABC",
            "hint": "Giả thiết '如果' (A) -> Hậu quả máy bay (B) -> Kết luận '那我就...' (C)."
        }
    },
    {
        "id": "hsk4_test7_q58",
        "category": "sentence_logic",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 阅读 第二部分 (第58题)",
        "zh": "她的服务热情周到，介绍情况时也很诚恳，这让人感到非常放心。",
        "pinyin": "tā de fú wù rè qíng zhōu dào ， jiè shào qíng kuàng shí yě hěn chéng kěn ， zhè ràng rén gǎn dào fēi cháng fàng xīn 。",
        "hanviet": "Tha Đích Phục Vụ Nhiệt Tình Chu Đáo ， Giới Thiệu Tình Huống Thời Dã Hẩn Thành Khẩn ， Giá Nhượng Nhân Cảm Đáo Phi Thường Phóng Tâm 。",
        "meaning": "Dịch vụ của cô ấy rất nhiệt tình chu đáo, khi giới thiệu tình hình cũng rất chân thành, điều này khiến người ta cảm thấy vô cùng yên tâm.",
        "tokens": [
            { "text": "她的服务热情周到", "type": "core", "role": "Đánh giá tổng quan ưu điểm 1 (C)" },
            { "text": "介绍情况时", "type": "normal", "role": "Thời điểm cụ thể" },
            { "text": "也很诚恳", "type": "core", "role": "Ưu điểm 2 với liên từ 也 (A)" },
            { "text": "这", "type": "grammar", "role": "Đại từ quy chiếu tóm lược toàn bộ hai ưu điểm trước" },
            { "text": "让人感到非常放心", "type": "core", "role": "Hệ quả tâm lý khách hàng (B)" }
        ],
        "grammar_point": {
            "name": "Đại từ chỉ thị 这 tóm lược tiền đề và Cấu trúc cũng 也",
            "pattern": "Đặc điểm 1 (C) + Đặc điểm 2 (với 也) (A) + 这 + 让 + Người + Cảm xúc (B)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Câu C giới thiệu chủ ngữ gốc '她的服务' và thái độ tổng thể. Câu A tiếp nối một hành vi chi tiết có phó từ '也' (cũng rất chân thành). Câu B bắt đầu bằng '这' (điều này) để tóm lược tất cả và đưa ra cảm giác yên tâm.",
            "explanation": "Trật tự bắt buộc: C (nêu phẩm chất) -> A (bổ sung bằng 也) -> B (dùng 这 kết luận tác động)."
        },
        "breakdown": [
            { "role": "Phẩm chất tổng thể (C)", "text": "她的服务热情周到", "type": "subject", "desc": "Giới thiệu nhân viên và phong cách phục vụ" },
            { "role": "Chi tiết bổ sung (A)", "text": "介绍情况时也很诚恳", "type": "verb", "desc": "Thái độ thành thực khi tư vấn" },
            { "role": "Quy nạp hệ quả (B)", "text": "这让人感到非常放心", "type": "object", "desc": "Đại từ '这' quy chiếu lại hai ưu điểm trên và chốt lại sự tin tưởng" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "介绍情况时也很诚恳" },
                { "id": "B", "text": "这让人感到非常放心" },
                { "id": "C", "text": "她的服务热情周到" }
            ],
            "correct_order": "CAB",
            "hint": "Chủ thể (C) -> Bổ sung có '也' (A) -> Tóm lược bằng '这' (B)."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test 46-55)
    # =========================================================================
    {
        "id": "hsk4_test7_q51",
        "category": "cloze",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 阅读 第一部分 (第51题)",
        "zh": "好，下楼的时候顺便把垃圾带下去。",
        "pinyin": "hǎo ， xià lóu de shí hou shùn biàn bǎ lā jī dài xià qu 。",
        "hanviet": "Hảo ， Hạ Lâu Đích Thời Hậu Thuận Tiện Bả Lạp Cáp Đái Hạ Khứ 。",
        "meaning": "Được rồi, khi xuống lầu thì tiện thể mang rác xuống luôn nhé.",
        "tokens": [
            { "text": "下楼的时候", "type": "normal", "role": "Thời điểm" },
            { "text": "顺便", "type": "core", "role": "Phó từ (tiện thể)" },
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "垃圾", "type": "core", "role": "Tân ngữ (rác)" },
            { "text": "带", "type": "core", "role": "Động từ chính (mang theo, xách theo)" },
            { "text": "下去", "type": "grammar", "role": "Bổ ngữ xu hướng kép (xuống dưới)" }
        ],
        "grammar_point": {
            "name": "Động từ 带 kết hợp Bổ ngữ xu hướng kép 下去 trong câu chữ 把",
            "pattern": "顺便 + 把 + Rác / Đồ vật + 带 + 下去 / 上去",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: Động từ '带' kết hợp với '下去' tạo thành hành động mang đồ vật rời xa người nói xuống dưới tầng trệt.",
            "explanation": "'把垃圾带下去' là câu khẩu ngữ sinh hoạt hàng ngày quen thuộc nhất trong các gia đình người Trung Quốc."
        },
        "breakdown": [
            { "role": "Cơ hội tiện lợi", "text": "下楼的时候顺便", "type": "modifier", "desc": "Tranh thủ việc bước xuống cầu thang" },
            { "role": "Hành vi xử lý rác", "text": "把垃圾带下去", "type": "verb", "desc": "Giới từ '把' phối hợp động từ '带' và bổ ngữ xu hướng '下去'" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "好，下楼的时候顺便把垃圾（  ）下去。",
            "options": ["带", "恐怕", "恢复", "精彩", "往"],
            "blank_index": 0,
            "correct_answer": "带",
            "hint": "Cần một động từ đi với '把垃圾...下去' có nghĩa là 'mang vứt rác'. Chọn '带'."
        }
    },
    {
        "id": "hsk4_test7_q53",
        "category": "cloze",
        "test_id": 7,
        "source": "HSK 4 模拟试卷 7 阅读 第一部分 (第53题)",
        "zh": "这么晚了，小王恐怕不能来了。",
        "pinyin": "zhè me wǎn le ， xiǎo wáng kǒng pà bù néng lái le 。",
        "hanviet": "Giá Ma Vãn Liễu ， Tiểu Vương Khủng Phạ Bất Năng Lai Liễu 。",
        "meaning": "Muộn thế này rồi, e rằng Tiểu Vương không thể đến được nữa đâu.",
        "tokens": [
            { "text": "这么晚了", "type": "normal", "role": "Bối cảnh thời gian muộn" },
            { "text": "小王", "type": "normal", "role": "Chủ ngữ" },
            { "text": "恐怕", "type": "grammar", "role": "Phó từ phỏng đoán tình huống tiêu cực (e rằng/lo rằng)" },
            { "text": "不能来了", "type": "core", "role": "Không thể tới nơi" }
        ],
        "grammar_point": {
            "name": "Phó từ ước lượng phỏng đoán 恐怕 (E rằng / Lo ngại rằng)",
            "pattern": "Chủ ngữ + 恐怕 + 不能 / 不会 + Động từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '恐怕' biểu thị sự phỏng đoán dựa trên lý lẽ nhưng luôn hướng về một kết quả không như ý muốn hoặc mang tính tiêu cực.",
            "explanation": "Thời gian đã quá muộn '这么晚了', người nói đưa ra nhận định có khả năng lớn là bạn mình sẽ lỡ hẹn."
        },
        "breakdown": [
            { "role": "Tiền đề thời gian", "text": "这么晚了", "type": "modifier", "desc": "Nhận định trời đã về khuya" },
            { "role": "Ước đoán lo lắng", "text": "小王恐怕", "type": "subject", "desc": "Phó từ '恐怕' thể hiện tâm lý e ngại" },
            { "role": "Sự việc không như ý", "text": "不能来了", "type": "verb", "desc": "Khả năng vắng mặt thực tế" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "这么晚了，小王（  ）不能来了。",
            "options": ["恐怕", "恢复", "精彩", "带", "往"],
            "blank_index": 0,
            "correct_answer": "恐怕",
            "hint": "Cần một phó từ phỏng đoán thể hiện sự lo ngại 'e rằng'. Chọn '恐怕'."
        }
    }
]
