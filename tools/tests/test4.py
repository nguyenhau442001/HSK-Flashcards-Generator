# -*- coding: utf-8 -*-
"""
Authentic items curated from HSK 4 模拟试卷 4 (Mock Test 4).
Source: Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
"""

TEST4_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building 86-95)
    # =========================================================================
    {
        "id": "hsk4_test4_q86",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第86题)",
        "zh": "从上午到下午工作八个小时。",
        "pinyin": "cóng shàng wǔ dào xià wǔ gōng zuò bā gè xiǎo shí 。",
        "hanviet": "Tùng Thượng Ngọ Đáo Hạ Ngọ Công Tác Bát Cá Tiểu Thời 。",
        "meaning": "Làm việc suốt tám tiếng từ sáng đến chiều.",
        "tokens": [
            { "text": "从", "type": "grammar", "role": "Giới từ chỉ mốc bắt đầu" },
            { "text": "上午", "type": "normal", "role": "Mốc thời gian buổi sáng" },
            { "text": "到", "type": "grammar", "role": "Giới từ chỉ mốc kết thúc" },
            { "text": "下午", "type": "normal", "role": "Mốc thời gian buổi chiều" },
            { "text": "工作", "type": "core", "role": "Động từ chính (làm việc)" },
            { "text": "八个小时", "type": "core", "role": "Bổ ngữ thời lượng" }
        ],
        "grammar_point": {
            "name": "Cấu trúc giới từ kép 从...到... và Bổ ngữ thời lượng",
            "pattern": "从 + Mốc A + 到 + Mốc B + Động từ + (Khoảng thời lượng)",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: '从上午到下午' làm trạng ngữ chỉ khoảng thời gian bắt đầu - kết thúc đứng trước động từ. Bổ ngữ thời lượng '八个小时' trả lời cho câu hỏi 'làm việc bao lâu' bắt buộc phải đứng SAU động từ '工作'.",
            "explanation": "Cấu trúc '从...到...' biểu thị phạm vi thời gian hoặc không gian. Khi đi với động từ có bổ ngữ thời lượng, trật tự chuẩn là Trạng ngữ thời gian + V + Bổ ngữ thời lượng."
        },
        "breakdown": [
            { "role": "Trạng ngữ thời gian", "text": "从上午到下午", "type": "subject", "desc": "Giới từ kép chỉ mốc thời gian bắt đầu và kết thúc" },
            { "role": "Vị ngữ động từ", "text": "工作", "type": "verb", "desc": "Hành vi làm việc" },
            { "role": "Bổ ngữ thời lượng", "text": "八个小时", "type": "complement", "desc": "Tổng thời gian kéo dài của hành động" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["八个小时", "到", "下午", "从", "工作", "上午"],
            "target_chunks": ["从", "上午", "到", "下午", "工作", "八个小时"],
            "hint": "Cấu trúc: 从 [上午] 到 [下午] + Động từ (工作) + Bổ ngữ thời lượng (八个小时)."
        }
    },
    {
        "id": "hsk4_test4_q87",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第87题)",
        "zh": "我想学会三种语言。",
        "pinyin": "wǒ xiǎng xué huì sān zhǒng yǔ yán 。",
        "hanviet": "Ngã Tưởng Học Hội Tam Chủng Ngữ Ngôn 。",
        "meaning": "Tôi muốn học thành thạo ba loại ngôn ngữ.",
        "tokens": [
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "想", "type": "grammar", "role": "Động từ năng nguyện (muốn)" },
            { "text": "学", "type": "normal", "role": "Động từ chính" },
            { "text": "会", "type": "grammar", "role": "Bổ ngữ kết quả (thành thạo)" },
            { "text": "三种", "type": "core", "role": "Số từ + lượng từ làm định ngữ" },
            { "text": "语言", "type": "core", "role": "Tân ngữ trực tiếp" }
        ],
        "grammar_point": {
            "name": "Bổ ngữ kết quả 会 và Cụm số lượng từ làm định ngữ",
            "pattern": "Chủ ngữ + Động từ năng nguyện (想/要) + Động từ + 会 + (Số lượng + Danh từ)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: '会' ở đây đóng vai trò bổ ngữ kết quả gắn liền sau động từ '学' tạo thành cụm '学会' (học thành thạo/nắm được bí quyết), không phải là trợ động từ đứng riêng.",
            "explanation": "Động từ năng nguyện '想' đứng trước cụm vị ngữ '学会', '三种' làm định ngữ hạn định cho danh từ '语言'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我", "type": "subject", "desc": "Người có ý định" },
            { "role": "Trợ động từ", "text": "想", "type": "grammar", "desc": "Biểu thị nguyện vọng, ý muốn" },
            { "role": "Vị ngữ + Bổ ngữ", "text": "学会", "type": "verb", "desc": "Động từ '学' đi kèm bổ ngữ kết quả '会' biểu thị làm chủ kỹ năng" },
            { "role": "Định ngữ", "text": "三种", "type": "modifier", "desc": "Lượng từ chủng loại số lượng" },
            { "role": "Tân ngữ", "text": "语言", "type": "object", "desc": "Đối tượng được tiếp thu" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["三种", "想", "学会", "语言", "我"],
            "target_chunks": ["我", "想", "学会", "三种", "语言"],
            "hint": "Chủ ngữ (我) + Nguyện vọng (想) + Động từ mang kết quả (学会) + Số lượng định ngữ (三种) + Tân ngữ (语言)."
        }
    },
    {
        "id": "hsk4_test4_q88",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第88题)",
        "zh": "他刚刚从北京回来。",
        "pinyin": "tā gāng gang cóng běi jīng huí lái 。",
        "hanviet": "Tha Cương Cương Tùng Bắc Kinh Hồi Lai 。",
        "meaning": "Anh ấy vừa mới từ Bắc Kinh trở về.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "刚刚", "type": "core", "role": "Phó từ thời gian (vừa mới)" },
            { "text": "从", "type": "grammar", "role": "Giới từ chỉ xuất phát điểm" },
            { "text": "北京", "type": "normal", "role": "Địa điểm nơi chốn" },
            { "text": "回来", "type": "core", "role": "Động từ xu hướng (trở về)" }
        ],
        "grammar_point": {
            "name": "Giới từ chỉ xuất phát điểm 从 và Phó từ thời gian 刚刚",
            "pattern": "Chủ ngữ + Phó từ thời gian (刚/刚刚) + 从 + Địa điểm + Động từ xu hướng",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: Cụm giới từ '从北京' làm trạng ngữ bắt buộc đứng TRƯỚC động từ '回来', không được dịch theo ngữ pháp phương Tây thành '回来从北京'.",
            "explanation": "'刚刚' là phó từ thời gian đứng trước cụm giới từ vị ngữ. '回来' là động từ xu hướng hướng về phía người nói."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Chủ thể thực hiện hành động" },
            { "role": "Trạng ngữ thời gian", "text": "刚刚", "type": "modifier", "desc": "Chỉ sự việc vừa mới xảy ra tức thì" },
            { "role": "Trạng ngữ nơi chốn", "text": "从北京", "type": "modifier", "desc": "Cụm giới từ chỉ nguồn gốc nơi chốn xuất phát" },
            { "role": "Vị ngữ động từ", "text": "回来", "type": "verb", "desc": "Động từ xu hướng biểu thị quay về" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["北京", "他", "回来", "从", "刚刚"],
            "target_chunks": ["他", "刚刚", "从", "北京", "回来"],
            "hint": "Trật tự: Chủ ngữ (他) + Phó từ (刚刚) + Giới từ nơi chốn (从北京) + Động từ xu hướng (回来)."
        }
    },
    {
        "id": "hsk4_test4_q89",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第89题)",
        "zh": "北方的天气变化比较快。",
        "pinyin": "běi fāng de tiān qì biàn huà bǐ jiào kuài 。",
        "hanviet": "Bắc Phương Đích Thiên Khí Biến Hóa Bỉ Giảo Khoái 。",
        "meaning": "Thời tiết ở phương Bắc biến đổi tương đối nhanh.",
        "tokens": [
            { "text": "北方", "type": "normal", "role": "Phương vị / nơi chốn" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "天气", "type": "core", "role": "Trung tâm ngữ chủ ngữ" },
            { "text": "变化", "type": "core", "role": "Vị ngữ động từ (biến đổi)" },
            { "text": "比较", "type": "grammar", "role": "Phó từ mức độ (tương đối)" },
            { "text": "快", "type": "normal", "role": "Tính từ bổ nghĩa / miêu tả" }
        ],
        "grammar_point": {
            "name": "Câu miêu tả diễn tiến: V + Phó từ mức độ + Tính từ",
            "pattern": "Chủ ngữ (A 的 B) + Động từ + 比较 / 很 + Tính từ",
            "level": "HSK 4 Phổ biến",
            "trap_note": "BẪY THI: '北方的天气' đóng vai trò toàn bộ cụm chủ ngữ. '变化' ở đây là động từ vị ngữ, và '比较快' miêu tả đặc tính/mức độ diễn ra của sự biến đổi đó.",
            "explanation": "Câu có cấu trúc Chủ ngữ (北方的天气) + Vị ngữ phức hợp (变化比较快)."
        },
        "breakdown": [
            { "role": "Định ngữ", "text": "北方", "type": "modifier", "desc": "Địa điểm hạn định khu vực" },
            { "role": "Chủ ngữ chính", "text": "天气", "type": "subject", "desc": "Hiện tượng thời tiết" },
            { "role": "Vị ngữ", "text": "变化", "type": "verb", "desc": "Sự thay đổi trạng thái" },
            { "role": "Bổ ngữ/Trạng thái miêu tả", "text": "比较快", "type": "modifier", "desc": "Phó từ '比较' bổ nghĩa tính từ '快'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["比较快", "的天气", "变化", "北方"],
            "target_chunks": ["北方", "的天气", "变化", "比较快"],
            "hint": "Chủ ngữ (北方的天气) + Động từ (变化) + Mức độ tính chất (比较快)."
        }
    },
    {
        "id": "hsk4_test4_q90",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第90题)",
        "zh": "我们要按照学校的规定做。",
        "pinyin": "wǒ men yào àn zhào xué xiào de guī dìng zuò 。",
        "hanviet": "Ngã Môn Yếu Án Chiếu Học Hiệu Đích Quy Định Tác 。",
        "meaning": "Chúng ta phải làm theo đúng quy định của nhà trường.",
        "tokens": [
            { "text": "我们", "type": "normal", "role": "Chủ ngữ" },
            { "text": "要", "type": "grammar", "role": "Động từ năng nguyện (phải/cần)" },
            { "text": "按照", "type": "grammar", "role": "Giới từ (theo/căn cứ)" },
            { "text": "学校", "type": "normal", "role": "Định ngữ danh từ" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "规定", "type": "core", "role": "Tân ngữ của giới từ 按照" },
            { "text": "做", "type": "normal", "role": "Động từ chính" }
        ],
        "grammar_point": {
            "name": "Giới từ 按照 (Căn cứ theo/chiếu theo tiêu chuẩn)",
            "pattern": "Chủ ngữ + (要/应该) + 按照 + Tiêu chuẩn/Quy định + Động từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Cụm '按照 + Danh từ quy định' bắt buộc đứng TRƯỚC động từ hành động '做', không được đặt ở cuối câu như tiếng Việt ('làm theo quy định').",
            "explanation": "Giới từ '按照' dẫn dắt căn cứ, quy chuẩn của hành động, đóng vai trò trạng ngữ bổ nghĩa cho động từ chính đứng sau."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我们", "type": "subject", "desc": "Chủ thể chịu quy định" },
            { "role": "Trợ động từ", "text": "要", "type": "grammar", "desc": "Nghĩa vụ, tính cần thiết" },
            { "role": "Trạng ngữ giới từ", "text": "按照学校的规定", "type": "modifier", "desc": "Căn cứ theo quy định của trường học" },
            { "role": "Vị ngữ động từ", "text": "做", "type": "verb", "desc": "Thực hiện hành động" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["做", "按照", "我们", "要", "学校的规定"],
            "target_chunks": ["我们", "要", "按照", "学校的规定", "做"],
            "hint": "Cấu trúc: Chủ ngữ (我们) + 要 + 按照 [学校的规定] + Động từ (做)."
        }
    },
    {
        "id": "hsk4_test4_q91",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第91题)",
        "zh": "苏杭一带人的口味清淡。",
        "pinyin": "sū háng yí dài rén de kǒu wèi qīng dàn 。",
        "hanviet": "Tô Hàng Nhất Đái Nhân Đích Khẩu Vị Thanh Đạm 。",
        "meaning": "Khẩu vị của người dân vùng Tô Châu - Hàng Châu rất thanh đạm.",
        "tokens": [
            { "text": "苏杭", "type": "normal", "role": "Tên địa danh (Tô Châu, Hàng Châu)" },
            { "text": "一带", "type": "core", "role": "Danh từ vùng ven / khu vực" },
            { "text": "人", "type": "normal", "role": "Danh từ nhân xưng" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "口味", "type": "core", "role": "Danh từ trung tâm (khẩu vị)" },
            { "text": "清淡", "type": "core", "role": "Tính từ vị ngữ (thanh đạm, ít dầu mỡ)" }
        ],
        "grammar_point": {
            "name": "Cụm định ngữ chỉ xuất xứ nơi chốn và Câu vị ngữ tính từ",
            "pattern": "Địa danh + 一带 + Danh từ người + 的 + Danh từ đặc điểm + Tính từ",
            "level": "HSK 4 Nâng cao",
            "trap_note": "BẪY THI: '一带' biểu thị 'dải đất/vùng khu vực lân cận'. Cụm '苏杭一带人' là định ngữ sở hữu đứng trước '的口味'. '清淡' (thanh đạm) trực tiếp làm vị ngữ miêu tả.",
            "explanation": "Câu vị ngữ tính từ miêu tả đặc trưng ẩm thực địa phương. '苏杭' là viết tắt của hai thành phố nổi tiếng Tô Châu (苏州) và Hàng Châu (杭州)."
        },
        "breakdown": [
            { "role": "Định ngữ nguồn gốc", "text": "苏杭一带人的", "type": "modifier", "desc": "Người dân thuộc toàn bộ vùng Tô - Hàng" },
            { "role": "Chủ ngữ trung tâm", "text": "口味", "type": "subject", "desc": "Thói quen ăn uống, vị giác" },
            { "role": "Vị ngữ tính từ", "text": "清淡", "type": "verb", "desc": "Mùi vị tao nhã, nhẹ nhàng, không béo cay" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["口味", "苏杭一带", "清淡", "人的"],
            "target_chunks": ["苏杭一带", "人的", "口味", "清淡"],
            "hint": "Địa danh kèm vùng (苏杭一带) + Định ngữ (人的) + Chủ ngữ (口味) + Tính từ (清淡)."
        }
    },
    {
        "id": "hsk4_test4_q92",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第92题)",
        "zh": "他想去美国留学。",
        "pinyin": "tā xiǎng qù měi guó liú xué 。",
        "hanviet": "Tha Tưởng Khứ Mỹ Quốc Lưu Học 。",
        "meaning": "Anh ấy muốn đi Mỹ du học.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "想", "type": "grammar", "role": "Động từ năng nguyện" },
            { "text": "去", "type": "normal", "role": "Động từ 1 (di chuyển)" },
            { "text": "美国", "type": "normal", "role": "Tân ngữ nơi chốn" },
            { "text": "留学", "type": "core", "role": "Động từ 2 (mục đích: du học)" }
        ],
        "grammar_point": {
            "name": "Câu liên động biểu thị mục đích (连动句)",
            "pattern": "Chủ ngữ + Trợ động từ + 去/来 + Nơi chốn + Động từ mục đích",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: Hành động di chuyển đến địa điểm (去美国) phải xảy ra trước hành động mục đích (留学). Không được đảo lộn trật tự hai động từ này.",
            "explanation": "Câu liên động có hai động từ cùng chia sẻ một chủ ngữ '他'. Động từ thứ hai '留学' chỉ mục đích của hành động di chuyển '去美国'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Người có kế hoạch học tập" },
            { "role": "Trợ động từ", "text": "想", "type": "grammar", "desc": "Dự định, mong muốn" },
            { "role": "Động từ liên kết 1 + Địa điểm", "text": "去美国", "type": "verb", "desc": "Hành vi đi đến quốc gia đích" },
            { "role": "Động từ liên kết 2", "text": "留学", "type": "verb", "desc": "Mục đích thực hiện là du học" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["美国", "想", "留学", "他", "去"],
            "target_chunks": ["他", "想", "去", "美国", "留学"],
            "hint": "Chủ ngữ (他) + Nguyện vọng (想) + Đi đâu (去美国) + Để làm gì (留学)."
        }
    },
    {
        "id": "hsk4_test4_q93",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第93题)",
        "zh": "请把手机送给叔叔。",
        "pinyin": "qǐng bǎ shǒu jī sòng gěi shū shu 。",
        "hanviet": "Thỉnh Bả Thủ Cơ Tống Cấp Thúc Thúc 。",
        "meaning": "Xin hãy đem chiếc điện thoại di động này tặng cho chú.",
        "tokens": [
            { "text": "请", "type": "normal", "role": "Từ lịch sự (xin/hãy)" },
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "手机", "type": "core", "role": "Tân ngữ chịu tác động" },
            { "text": "送", "type": "normal", "role": "Động từ chính (tặng)" },
            { "text": "给", "type": "grammar", "role": "Bổ ngữ kết quả / giới từ hướng đối tượng" },
            { "text": "叔叔", "type": "core", "role": "Đối tượng thụ hưởng (chú)" }
        ],
        "grammar_point": {
            "name": "Câu chữ 把 kết hợp Động từ mang bổ ngữ 給: 把 + Vật + V + 给 + Người",
            "pattern": "请 / Chủ ngữ + 把 + Vật tác động + 送 / 交 / 寄 + 给 + Người tiếp nhận",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Khi động từ kèm theo '给' (như 送给, 交给, 借给), đối tượng người nhận bắt buộc phải đứng ngay sau '给', không được để người nhận đứng trước động từ.",
            "explanation": "Câu chữ 把 diễn tả sự chuyển dịch quyền sở hữu hoặc vị trí của đồ vật '手机' sang cho người tiếp nhận là '叔叔'."
        },
        "breakdown": [
            { "role": "Lời thỉnh cầu", "text": "请", "type": "subject", "desc": "Lời yêu cầu lịch sự mở đầu" },
            { "role": "Giới từ 把 + Vật tác động", "text": "把手机", "type": "object", "desc": "Đưa đồ vật chịu tác động lên trước động từ" },
            { "role": "Vị ngữ + Bổ ngữ kết quả", "text": "送给", "type": "verb", "desc": "Hành vi tặng quà và chuyển giao" },
            { "role": "Đối tượng tiếp nhận", "text": "叔叔", "type": "object", "desc": "Người thân được nhận điện thoại" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["送给", "手机", "请", "叔叔", "把"],
            "target_chunks": ["请", "把", "手机", "送给", "叔叔"],
            "hint": "Cấu trúc: 请 + 把 [手机] + 送给 + [叔叔]."
        }
    },
    {
        "id": "hsk4_test4_q94",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第94题)",
        "zh": "我对这件事很感兴趣。",
        "pinyin": "wǒ duì zhè jiàn shì hěn gǎn xìng qù 。",
        "hanviet": "Ngã Đối Giá Kiện Sự Hẩn Cảm Hứng Thú 。",
        "meaning": "Tôi rất có hứng thú đối với sự việc này.",
        "tokens": [
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "对", "type": "grammar", "role": "Giới từ chỉ đối tượng hướng tới" },
            { "text": "这件事", "type": "normal", "role": "Tân ngữ của giới từ 对" },
            { "text": "很", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "感", "type": "core", "role": "Động từ (cảm thấy)" },
            { "text": "兴趣", "type": "core", "role": "Danh từ (hứng thú)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc cố định 对...感兴趣 (Có hứng thú với điều gì)",
            "pattern": "Chủ ngữ + 对 + Sự vật / Sự việc + (很 / 不 / 非常) + 感兴趣",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Cụm giới từ '对这件事' bắt buộc phải đứng TRƯỚC vị ngữ '感兴趣'. Không được dịch kiểu từ đối từ tiếng Việt 'Tôi hứng thú đối với việc này'.",
            "explanation": "'感兴趣' là kết cấu động tân (V-O). Khi muốn thêm phó từ mức độ, thường đặt trước toàn cụm '很感兴趣' hoặc '感很大兴趣'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我", "type": "subject", "desc": "Chủ thể mang cảm xúc" },
            { "role": "Trạng ngữ giới từ", "text": "对这件事", "type": "modifier", "desc": "Chỉ định đối tượng gây hứng thú" },
            { "role": "Phó từ mức độ", "text": "很", "type": "modifier", "desc": "Tăng cường mức độ cảm xúc" },
            { "role": "Vị ngữ động tân", "text": "感兴趣", "type": "verb", "desc": "Nảy sinh sự quan tâm thích thú" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["很感兴趣", "这件事", "对", "我"],
            "target_chunks": ["我", "对", "这件事", "很感兴趣"],
            "hint": "Cấu trúc: 主语 (我) + 对 [这件事] + 很感兴趣."
        }
    },
    {
        "id": "hsk4_test4_q95",
        "category": "sentence_building",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 书写 第一部分 (第95题)",
        "zh": "墙上挂着一幅画儿。",
        "pinyin": "qiáng shang guà zhe yì fú huàr 。",
        "hanviet": "Tường Thượng Quải Trước Nhất Bức Họa Nhi 。",
        "meaning": "Trên tường đang treo một bức tranh.",
        "tokens": [
            { "text": "墙上", "type": "core", "role": "Trạng ngữ nơi chốn / Chủ ngữ tồn hiện" },
            { "text": "挂", "type": "core", "role": "Động từ chính (treo)" },
            { "text": "着", "type": "grammar", "role": "Trợ từ động thái chỉ sự duy trì trạng thái" },
            { "text": "一幅", "type": "core", "role": "Lượng từ (bức, tấm - chuyên dùng cho tranh)" },
            { "text": "画儿", "type": "normal", "role": "Tân ngữ tồn tại (bức tranh)" }
        ],
        "grammar_point": {
            "name": "Câu tồn hiện trạng thái tĩnh: Địa điểm + V + 着 + Lượng từ + Danh từ",
            "pattern": "Nơi chốn / Phương vị + Động từ (挂/摆/放/写) + 着 + Số lượng + Danh từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Câu tồn hiện biểu thị trạng thái tĩnh không được thêm giới từ '在' trước nơi chốn ('墙上', KHÔNG nói '在墙上挂着...'). Lượng từ của tranh '画儿' chuẩn xác là '幅' (一幅画儿).",
            "explanation": "'着' đóng vai trò duy trì liên tục kết quả của hành động treo tranh. Danh từ tồn tại '一幅画儿' đứng sau động từ là đối tượng chưa xác định."
        },
        "breakdown": [
            { "role": "Vị trí không gian", "text": "墙上", "type": "subject", "desc": "Mặt phẳng tường đứng đầu câu làm vị trí khởi phát" },
            { "role": "Vị ngữ + Duy trì trạng thái", "text": "挂着", "type": "verb", "desc": "Động từ '挂' gắn kết trợ từ '着'" },
            { "role": "Lượng từ cụ thể", "text": "一幅", "type": "modifier", "desc": "Lượng từ quy chuẩn cho tranh vẽ" },
            { "role": "Thực thể tồn tại", "text": "画儿", "type": "object", "desc": "Bức họa đang được lưu giữ trên tường" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["一幅", "挂着", "画儿", "墙上"],
            "target_chunks": ["墙上", "挂着", "一幅", "画儿"],
            "hint": "Cấu trúc tồn hiện: Nơi chốn (墙上) + V+着 (挂着) + Số lượng (一幅) + Danh từ (画儿)."
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Logic 56-65)
    # =========================================================================
    {
        "id": "hsk4_test4_q56",
        "category": "sentence_logic",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 阅读 第二部分 (第56题)",
        "zh": "这儿的房子离车站很近，价钱也不太贵，所以我决定租下来。",
        "pinyin": "zhèr de fáng zi lí chē zhàn hěn jìn ， jià qian yě bú tài guì ， suǒ yǐ wǒ jué dìng zū xià lai 。",
        "hanviet": "Giá Nhi Đích Phòng Tử Ly Xa Trạm Hẩn Cận ， Giá Tiền Dã Bất Thái Quý ， Sở Dĩ Ngã Quyết Định Tô Hạ Lai 。",
        "meaning": "Căn phòng ở đây rất gần bến xe, giá cả cũng không quá đắt, vì vậy tôi quyết định thuê lại.",
        "tokens": [
            { "text": "这儿的房子", "type": "normal", "role": "Chủ ngữ câu" },
            { "text": "离", "type": "grammar", "role": "Giới từ cự ly" },
            { "text": "车站", "type": "normal", "role": "Bến xe" },
            { "text": "很近", "type": "normal", "role": "Ưu điểm 1" },
            { "text": "价钱", "type": "core", "role": "Giá tiền" },
            { "text": "也不太贵", "type": "normal", "role": "Ưu điểm 2 (Liên từ 也)" },
            { "text": "所以", "type": "grammar", "role": "Liên từ kết quả" },
            { "text": "我", "type": "normal", "role": "Chủ thể ra quyết định" },
            { "text": "决定", "type": "core", "role": "Quyết định" },
            { "text": "租下来", "type": "core", "role": "Thuê lại" }
        ],
        "grammar_point": {
            "name": "Cấu trúc nhân quả nhiều điều kiện: Điều kiện 1 + yě + Điều kiện 2 + suǒyǐ + Kết luận",
            "pattern": "Vế A (nguyên nhân 1) + Vế B (nguyên nhân 2 kèm 也) + 所以 + Vế C (hệ quả)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Câu có liên từ '也' (cũng) bắt buộc phải đứng sau một điều kiện đã được nêu ra trước đó. Liên từ '所以' (vì vậy) luôn nằm ở vế kết luận cuối cùng.",
            "explanation": "Câu B nêu đối tượng chính và ưu điểm địa lý (离车站很近). Câu A bổ sung ưu điểm thứ hai về giá thành (价钱也不太贵). Câu C là quyết định logic tất yếu (所以我决定租下来)."
        },
        "breakdown": [
            { "role": "Mở đầu / Nguyên nhân 1 (B)", "text": "这儿的房子离车站很近", "type": "subject", "desc": "Giới thiệu căn nhà và vị trí địa lý thuận lợi" },
            { "role": "Bổ sung điều kiện 2 (A)", "text": "价钱也不太贵", "type": "verb", "desc": "Dùng '也' để tiếp nối mặt tích cực thứ hai" },
            { "role": "Kết quả cuối cùng (C)", "text": "所以我决定租下来", "type": "object", "desc": "Dùng liên từ '所以' chốt lại hành động thuê nhà" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "价钱也不太贵" },
                { "id": "B", "text": "这儿的房子离车站很近" },
                { "id": "C", "text": "所以我决定租下来" }
            ],
            "correct_order": "BAC",
            "hint": "Tìm câu giới thiệu đối tượng (B) -> câu bổ sung ưu điểm bằng '也' (A) -> câu kết luận bằng '所以' (C)."
        }
    },
    {
        "id": "hsk4_test4_q58",
        "category": "sentence_logic",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 阅读 第二部分 (第58题)",
        "zh": "小时候我很爱看书，只要手中有本书，就不去外边玩儿。",
        "pinyin": "xiǎo shí hou wǒ hěn ài kàn shū ， zhǐ yào shǒu zhōng yǒu běn shū ， jiù bú qù wài bian wánr 。",
        "hanviet": "Tiểu Thời Hậu Ngã Hẩn Ái Khán Thư ， Chỉ Yếu Thủ Trung Hữu Bổn Thư ， Tựu Bất Khứ Ngoại Biên Ngoạn Nhi 。",
        "meaning": "Lúc nhỏ tôi rất thích đọc sách, chỉ cần trong tay có một cuốn sách là sẽ không ra ngoài chơi nữa.",
        "tokens": [
            { "text": "小时候", "type": "normal", "role": "Trạng ngữ thời gian bối cảnh" },
            { "text": "我很爱看书", "type": "core", "role": "Mệnh đề chủ đề (sở thích đọc sách)" },
            { "text": "只要", "type": "grammar", "role": "Cặp liên từ điều kiện (chỉ cần)" },
            { "text": "手中", "type": "normal", "role": "Trong tay" },
            { "text": "有本书", "type": "normal", "role": "Điều kiện đủ" },
            { "text": "就", "type": "grammar", "role": "Phó từ liên kết (thì/là)" },
            { "text": "不去外边玩儿", "type": "core", "role": "Hành vi kết quả" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ điều kiện 只要...就... (Chỉ cần... thì...)",
            "pattern": "Chủ đề bối cảnh + 只要 + Điều kiện đủ + 就 + Kết quả tương ứng",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Cặp liên từ '只要...就...' luôn đi liền nhau theo thứ tự: vế điều kiện (只要) đi trước, vế kết quả (就) đi sau. Câu C giới thiệu bối cảnh tổng quát '小时候我很爱看书' phải đứng đầu.",
            "explanation": "Câu C mở đầu với thời gian và sở thích cá nhân. Câu B đưa ra điều kiện tối thiểu '只要手中有本书'. Câu A khép lại bằng hành động đi kèm '就不去外边玩儿'."
        },
        "breakdown": [
            { "role": "Bối cảnh chủ đề (C)", "text": "小时候我很爱看书", "type": "subject", "desc": "Giới thiệu sở thích từ thuở nhỏ" },
            { "role": "Vế điều kiện (B)", "text": "只要手中有本书", "type": "verb", "desc": "Dùng '只要' đưa ra điều kiện đủ" },
            { "role": "Vế kết quả (A)", "text": "就不去外边玩儿", "type": "object", "desc": "Dùng '就' chỉ hệ quả trực tiếp" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "就不去外边玩儿" },
                { "id": "B", "text": "只要手中有本书" },
                { "id": "C", "text": "小时候我很爱看书" }
            ],
            "correct_order": "CBA",
            "hint": "Cặp liên từ '只要...就...' (B trước A). Bối cảnh thời gian '小时候' (C) đứng đầu."
        }
    },
    {
        "id": "hsk4_test4_q62",
        "category": "sentence_logic",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 阅读 第二部分 (第62题)",
        "zh": "如果生活中没有朋友，就会感到寂寞和孤独，也就不会有欢声笑语。",
        "pinyin": "rú guǒ shēng huó zhōng méi yǒu péng you ， jiù huì gǎn dào jì mò hé gū dú ， yě jiù bú huì yǒu huān shēng xiào yǔ 。",
        "hanviet": "Như Quả Sinh Hoạt Trung Một Hữu Bằng Hữu ， Tựu Hội Cảm Đáo Tịch Mịch Hòa Cô Độc ， Dã Tựu Bất Hội Hữu Hoan Thanh Tiếu Ngữ 。",
        "meaning": "Nếu trong cuộc sống không có bạn bè, ta sẽ cảm thấy tịch mịch và cô đơn, cũng sẽ không thể có được tiếng cười vui vẻ.",
        "tokens": [
            { "text": "如果", "type": "grammar", "role": "Liên từ giả thiết (nếu như)" },
            { "text": "生活中", "type": "normal", "role": "Trong cuộc sống" },
            { "text": "没有朋友", "type": "core", "role": "Giả thiết tiêu cực" },
            { "text": "就会", "type": "grammar", "role": "Phó từ liên kết hệ quả 1 (thì sẽ)" },
            { "text": "感到", "type": "normal", "role": "Cảm nhận" },
            { "text": "寂寞和孤独", "type": "core", "role": "Trạng thái tâm lý cô đơn" },
            { "text": "也就不会", "type": "grammar", "role": "Hệ quả 2 tăng tiến (cũng sẽ không)" },
            { "text": "欢声笑语", "type": "core", "role": "Thành ngữ: tiếng cười nói rộn rã" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ giả thiết 如果...就... và Tăng tiến 也",
            "pattern": "如果 + Giả thiết + 就会 + Kết quả 1 + 也就不会 + Kết quả 2",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Vế '如果' nêu tình huống giả định luôn đứng đầu (B). Vế '就会' là hệ quả trực tiếp thứ nhất (A). Vế '也就不会' mang phó từ '也' bổ sung hệ quả song song thứ hai (C).",
            "explanation": "B mở đầu bằng giả định '如果生活中没有朋友'. A tiếp nối trạng thái cảm xúc nảy sinh '就会感到寂寞和孤独'. C kết lại bằng việc đánh mất niềm vui '也就不会有欢声笑语'."
        },
        "breakdown": [
            { "role": "Giả thiết mở đầu (B)", "text": "如果生活中没有朋友", "type": "subject", "desc": "Đặt ra giả định thiếu vắng bạn bè" },
            { "role": "Hệ quả trực tiếp (A)", "text": "就会感到寂寞和孤独", "type": "verb", "desc": "Cảm giác cô đơn phát sinh" },
            { "role": "Hệ quả bổ sung (C)", "text": "也就不会有欢声笑语", "type": "object", "desc": "Mất đi tiếng cười vui cuộc sống" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "就会感到寂寞和孤独" },
                { "id": "B", "text": "如果生活中没有朋友" },
                { "id": "C", "text": "也就不会有欢声笑语" }
            ],
            "correct_order": "BAC",
            "hint": "Bắt đầu với giả định '如果' (B) -> Hệ quả '就会' (A) -> Bổ sung '也就' (C)."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test 46-55)
    # =========================================================================
    {
        "id": "hsk4_test4_q46",
        "category": "cloze",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 阅读 第一部分 (第46题)",
        "zh": "大熊猫是世界上最珍贵的动物之一。",
        "pinyin": "dà xióng māo shì shì jiè shang zuì zhēn guì de dòng wù zhī yī 。",
        "hanviet": "Đại Hùng Miêu Thị Thế Giới Thượng Tối Trân Quý Đích Động Vật Chi Nhất 。",
        "meaning": "Gấu trúc lớn là một trong những loài động vật quý hiếm nhất trên thế giới.",
        "tokens": [
            { "text": "大熊猫", "type": "core", "role": "Chủ ngữ (gấu trúc lớn)" },
            { "text": "是", "type": "grammar", "role": "Động từ hệ từ" },
            { "text": "世界上", "type": "normal", "role": "Phạm vi không gian toàn cầu" },
            { "text": "最珍贵", "type": "core", "role": "Định ngữ chỉ phẩm chất quý báu" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "动物", "type": "normal", "role": "Danh từ phân loại" },
            { "text": "之一", "type": "grammar", "role": "Kết cấu Hán cổ: một trong số..." }
        ],
        "grammar_point": {
            "name": "Kết cấu ...之一 (Một trong những...)",
            "pattern": "Phạm vi số nhiều / Danh từ tập hợp + 之一",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY NGỮ PHÁP: Trong tiếng Trung, '之一' bắt buộc phải đứng SAU danh từ số nhiều hoặc cụm danh từ phân loại ('动物之一'), ngược lại hoàn toàn so với tiếng Việt ('một trong những...').",
            "explanation": "'之一' là cấu trúc cố định rất thường gặp trong HSK 4 để chỉ một cá thể tiêu biểu thuộc về một tập hợp hoặc danh hiệu."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "大熊猫", "type": "subject", "desc": "Quốc bảo của Trung Quốc" },
            { "role": "Vị ngữ hệ từ", "text": "是", "type": "verb", "desc": "Khẳng định danh tính" },
            { "role": "Cụm định ngữ danh từ", "text": "世界上最珍贵的动物", "type": "modifier", "desc": "Tập hợp các loài động vật trân quý nhất hành tinh" },
            { "role": "Thành phần biểu thị cá thể", "text": "之一", "type": "object", "desc": "Một thành viên trong tập hợp đó" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "大熊猫是世界上最珍贵的动物（  ）。",
            "options": ["之一", "坚持", "主动", "与", "快乐"],
            "blank_index": 0,
            "correct_answer": "之一",
            "hint": "Đứng cuối câu sau cụm danh từ '最珍贵的动物' chỉ có thể là cấu trúc '...之一' (một trong những)."
        }
    },
    {
        "id": "hsk4_test4_q50",
        "category": "cloze",
        "test_id": 4,
        "source": "HSK 4 模拟试卷 4 阅读 第一部分 (第50题)",
        "zh": "与别人交流的时候，要看着对方的眼睛，这是最基本的礼貌。",
        "pinyin": "yǔ bié rén jiāo liú de shí hou ， yào kàn zhe duì fāng de yǎn jing ， zhè shì zuì jī běn de lǐ mào 。",
        "hanviet": "Dữ Biệt Nhân Giao Lưu Đích Thời Hậu ， Yếu Khán Trước Đối Phương Đích Nhãn Tinh ， Giá Thị Tối Cơ Bản Đích Lễ Mạo 。",
        "meaning": "Khi giao tiếp với người khác, cần nhìn vào mắt đối phương, đây là phép lịch sự cơ bản nhất.",
        "tokens": [
            { "text": "与", "type": "grammar", "role": "Giới từ trang trọng (cùng/với)" },
            { "text": "别人", "type": "normal", "role": "Tân ngữ giới từ (người khác)" },
            { "text": "交流", "type": "core", "role": "Động từ giao tiếp" },
            { "text": "的时候", "type": "normal", "role": "Thời điểm diễn ra sự việc" },
            { "text": "要", "type": "grammar", "role": "Cần/phải" },
            { "text": "看着", "type": "core", "role": "Hành vi nhìn duy trì" },
            { "text": "对方的眼睛", "type": "normal", "role": "Ánh mắt đối phương" },
            { "text": "这是", "type": "normal", "role": "Đây là" },
            { "text": "最基本的礼貌", "type": "core", "role": "Phép lịch thiệp căn bản" }
        ],
        "grammar_point": {
            "name": "Giới từ 与 (Cùng / với đối tượng nào đó)",
            "pattern": "与 + Đối tượng + Động từ tương tác (交流 / 合作 / 讨论)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '与' mang sắc thái văn viết, trang trọng hơn '跟' và '和'. Khi đứng đầu phân câu làm giới từ mở đầu cho đối tượng giao tiếp '与别人交流', '与' là từ duy nhất phù hợp trong các lựa chọn.",
            "explanation": "'与' kết hợp với danh từ chỉ đối tượng '别人' tạo thành cụm giới từ trạng ngữ chỉ đối tác của hành vi giao tiếp '交流'."
        },
        "breakdown": [
            { "role": "Trạng ngữ chỉ đối tượng tương tác", "text": "与别人交流的时候", "type": "modifier", "desc": "Giới từ '与' kết nối hành vi giao tiếp cùng người khác" },
            { "role": "Hành vi yêu cầu", "text": "要看着对方的眼睛", "type": "verb", "desc": "Duy trì ánh mắt tôn trọng" },
            { "role": "Đánh giá nhận định", "text": "这是最基本的礼貌", "type": "object", "desc": "Khẳng định chuẩn mực ứng xử tối thiểu" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "（  ）别人交流的时候，要看着对方的眼睛，这是最基本的礼貌。",
            "options": ["之一", "坚持", "主动", "与", "快乐"],
            "blank_index": 0,
            "correct_answer": "与",
            "hint": "Cần một giới từ đi với '别人交流' mang nghĩa 'cùng với người khác'. Lựa chọn phù hợp nhất là '与'."
        }
    }
]
