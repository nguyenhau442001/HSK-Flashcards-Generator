# -*- coding: utf-8 -*-
"""
Authentic items curated from HSK 4 模拟试卷 5 (Mock Test 5).
Source: Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
"""

TEST5_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building 86-95)
    # =========================================================================
    {
        "id": "hsk4_test5_q86",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第86题)",
        "zh": "警察提醒司机朋友要注意安全。",
        "pinyin": "jǐng chá tí xǐng sī jī péng you yào zhù yì ān quán 。",
        "hanviet": "Cảnh Sát Đề Tỉnh Ty Cơ Bằng Hữu Yếu Chú Ý An Toàn 。",
        "meaning": "Cảnh sát nhắc nhở các bạn tài xế phải chú ý an toàn.",
        "tokens": [
            { "text": "警察", "type": "core", "role": "Chủ ngữ (cảnh sát)" },
            { "text": "提醒", "type": "core", "role": "Động từ kiêm ngữ (nhắc nhở)" },
            { "text": "司机朋友", "type": "core", "role": "Kiêm ngữ (vừa là tân ngữ của 提醒 vừa là chủ ngữ của 要注意)" },
            { "text": "要", "type": "grammar", "role": "Động từ năng nguyện (phải/cần)" },
            { "text": "注意", "type": "core", "role": "Động từ vị ngữ thứ hai" },
            { "text": "安全", "type": "normal", "role": "Tân ngữ trực tiếp" }
        ],
        "grammar_point": {
            "name": "Câu kiêm ngữ với động từ 提醒 (Nhắc nhở ai đó làm gì)",
            "pattern": "Chủ ngữ 1 + 提醒 / 请 / 让 + Kiêm ngữ (Tân ngữ 1 đồng thời là Chủ ngữ 2) + Động từ 2 + Tân ngữ 2",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: '司机朋友' là từ thân mật (các bác tài xế). Động từ '提醒' đòi hỏi người được nhắc nhở đứng liền kề, sau đó mới đến điều cần nhắc nhở ('要注意安全').",
            "explanation": "Câu kiêm ngữ là dạng câu đặc biệt trong tiếng Trung. '司机朋友' vừa nhận tác động của '提醒', vừa là chủ thể của hành động '注意安全'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "警察", "type": "subject", "desc": "Lực lượng chức năng ra hiệu lệnh" },
            { "role": "Động từ kiêm ngữ", "text": "提醒", "type": "verb", "desc": "Hành vi nhắc nhở, cảnh báo" },
            { "role": "Kiêm ngữ", "text": "司机朋友", "type": "subject", "desc": "Đối tượng được nhắc nhở" },
            { "role": "Mệnh đề vị ngữ kiêm ngữ", "text": "要注意安全", "type": "verb", "desc": "Hành động được căn dặn thực hiện" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["司机朋友", "提醒", "安全", "要注意", "警察"],
            "target_chunks": ["警察", "提醒", "司机朋友", "要注意", "安全"],
            "hint": "Chủ thể (警察) + Nhắc nhở (提醒) + Ai (司机朋友) + Điều gì (要注意安全)."
        }
    },
    {
        "id": "hsk4_test5_q87",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第87题)",
        "zh": "姐姐经常去健身房锻炼。",
        "pinyin": "jiě jie jīng cháng qù jiàn shēn fáng duàn liàn 。",
        "hanviet": "Tỷ Tỷ Kinh Thường Khứ Kiện Thân Phòng Đoán Luyện 。",
        "meaning": "Chị gái thường xuyên đến phòng tập thể dục để rèn luyện sức khỏe.",
        "tokens": [
            { "text": "姐姐", "type": "normal", "role": "Chủ ngữ" },
            { "text": "经常", "type": "core", "role": "Phó từ tần suất (thường xuyên)" },
            { "text": "去", "type": "normal", "role": "Động từ di chuyển 1" },
            { "text": "健身房", "type": "core", "role": "Nơi chốn (phòng gym)" },
            { "text": "锻炼", "type": "core", "role": "Động từ mục đích 2 (tập luyện rèn luyện)" }
        ],
        "grammar_point": {
            "name": "Câu liên động biểu thị mục đích và Phó từ tần suất 经常",
            "pattern": "Chủ ngữ + Phó từ tần suất + 去 + Nơi chốn + Động từ mục đích",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: Phó từ chỉ tần suất '经常' bắt buộc đứng trước động từ liên động đầu tiên ('去'), và địa điểm '健身房' phải đứng ngay sau '去'.",
            "explanation": "Hành vi đi tới phòng tập '去健身房' xảy ra trước để phục vụ mục đích '锻炼'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "姐姐", "type": "subject", "desc": "Chủ thể hành động" },
            { "role": "Trạng ngữ tần suất", "text": "经常", "type": "modifier", "desc": "Biểu thị tính đều đặn, định kỳ" },
            { "role": "Động từ 1 + Nơi chốn", "text": "去健身房", "type": "verb", "desc": "Di chuyển đến cơ sở thể thao" },
            { "role": "Động từ 2 (Mục đích)", "text": "锻炼", "type": "verb", "desc": "Mục tiêu tập luyện thân thể" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["健身房", "锻炼", "去", "姐姐", "经常"],
            "target_chunks": ["姐姐", "经常", "去", "健身房", "锻炼"],
            "hint": "Ai (姐姐) + Tần suất (经常) + Đi đâu (去健身房) + Làm gì (锻炼)."
        }
    },
    {
        "id": "hsk4_test5_q88",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第88题)",
        "zh": "王明的画儿画得非常好。",
        "pinyin": "wáng míng de huàr huà de fēi cháng hǎo 。",
        "hanviet": "Vương Minh Đích Họa Nhi Họa Đắc Phi Thường Hảo 。",
        "meaning": "Tranh của Vương Minh vẽ vô cùng đẹp.",
        "tokens": [
            { "text": "王明", "type": "normal", "role": "Tên riêng" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "画儿", "type": "core", "role": "Danh từ chủ ngữ (bức tranh)" },
            { "text": "画", "type": "core", "role": "Động từ chính (vẽ)" },
            { "text": "得", "type": "grammar", "role": "Trợ từ kết cấu bổ ngữ trạng thái" },
            { "text": "非常", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "好", "type": "normal", "role": "Hình dung từ biểu thị kết quả đánh giá" }
        ],
        "grammar_point": {
            "name": "Bổ ngữ trình độ/trạng thái với Trợ từ 得: V + 得 + Cụm tính từ",
            "pattern": "Chủ ngữ (Tác phẩm) + Động từ + 得 + Phó từ mức độ + Tính từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ LOẠI: Phân biệt rõ danh từ '画儿' (bức tranh có âm cuốn lưỡi) làm chủ ngữ với động từ '画' (vẽ tranh) đứng trước trợ từ '得'. Không nhầm lẫn '的' và '得'.",
            "explanation": "'得' kết nối giữa hành vi thực hiện '画' và lời nhận xét đánh giá chất lượng '非常好'."
        },
        "breakdown": [
            { "role": "Chủ ngữ định-trung", "text": "王明的画儿", "type": "subject", "desc": "Các tác phẩm hội họa của Vương Minh" },
            { "role": "Vị ngữ động từ", "text": "画", "type": "verb", "desc": "Thao tác sáng tác hội họa" },
            { "role": "Trợ từ bổ ngữ", "text": "得", "type": "grammar", "desc": "Kết nối thành phần đánh giá" },
            { "role": "Bổ ngữ trạng thái", "text": "非常好", "type": "modifier", "desc": "Lời khen ngợi mức độ cao" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["非常好", "王明的画儿", "画得"],
            "target_chunks": ["王明的画儿", "画得", "非常好"],
            "hint": "Chủ ngữ (王明的画儿) + Động từ kèm trợ từ (画得) + Bổ ngữ (非常好)."
        }
    },
    {
        "id": "hsk4_test5_q89",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第89题)",
        "zh": "还是明天再干吧。",
        "pinyin": "hái shì míng tiān zài gàn ba 。",
        "hanviet": "Hoàn Thị Minh Thiên Tái Can Ba 。",
        "meaning": "Hay là để ngày mai hãy làm tiếp đi.",
        "tokens": [
            { "text": "还是", "type": "grammar", "role": "Phó từ biểu thị sự lựa chọn tối ưu (hay là/nên chăng)" },
            { "text": "明天", "type": "normal", "role": "Trạng ngữ thời gian" },
            { "text": "再", "type": "grammar", "role": "Phó từ biểu thị hành động hoãn lại/lặp lại sau" },
            { "text": "干", "type": "core", "role": "Động từ khẩu ngữ (làm việc)" },
            { "text": "吧", "type": "normal", "role": "Trợ từ ngữ khí đề xuất" }
        ],
        "grammar_point": {
            "name": "Phó từ 还是 biểu thị kiến nghị lựa chọn và Phó từ 再 chỉ hành động tương lai",
            "pattern": "还是 + Trạng ngữ thời gian + 再 + Động từ + 吧",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY NGỮ DỤNG: '还是' ở đây không phải câu hỏi lựa chọn 'hay là' (A 还是 B), mà là phó từ thể hiện phương án được người nói cho là tốt nhất sau khi suy xét.",
            "explanation": "'再' đứng trước động từ '干' nhấn mạnh hành động được lùi lại đến mốc '明天'. Trợ từ '吧' làm nhẹ giọng điệu gợi ý."
        },
        "breakdown": [
            { "role": "Thái độ đề xuất", "text": "还是", "type": "grammar", "desc": "Lựa chọn phương án thỏa đáng hơn" },
            { "role": "Trạng ngữ thời gian", "text": "明天", "type": "modifier", "desc": "Mốc thời gian hoãn lại" },
            { "role": "Vị ngữ + Ngữ khí", "text": "再干吧", "type": "verb", "desc": "Động từ '干' đi kèm '再' và trợ từ ngữ khí '吧'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["干吧", "明天", "再", "还是"],
            "target_chunks": ["还是", "明天", "再", "干吧"],
            "hint": "Cấu trúc: 还是 + Thời gian (明天) + 再 + Động từ kèm trợ từ (干吧)."
        }
    },
    {
        "id": "hsk4_test5_q90",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第90题)",
        "zh": "不是已经告诉你了吗？",
        "pinyin": "bú shì yǐ jīng gào su nǐ le ma ？",
        "hanviet": "Bất Thị Dĩ Kinh Cáo Tố Nhĩ Liễu Ma ？",
        "meaning": "Chẳng phải đã nói cho bạn biết rồi sao?",
        "tokens": [
            { "text": "不是", "type": "grammar", "role": "Cấu trúc câu hỏi tu từ / phản vấn" },
            { "text": "已经", "type": "normal", "role": "Phó từ thời gian hoàn thành" },
            { "text": "告诉", "type": "core", "role": "Động từ (bảo, cho biết)" },
            { "text": "你", "type": "normal", "role": "Tân ngữ trực tiếp" },
            { "text": "了", "type": "normal", "role": "Trợ từ ngữ khí hoàn thành" },
            { "text": "吗", "type": "normal", "role": "Trợ từ nghi vấn" }
        ],
        "grammar_point": {
            "name": "Câu hỏi phản vấn nhấn mạnh: 不是...吗？",
            "pattern": "不是 + (Chủ ngữ) + 已经 + Động từ + (Tân ngữ) + 了吗？",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY NGỮ KHÍ: Cấu trúc '不是...吗？' tuy mang hình thức phủ định nghi vấn nhưng thực chất mang nghĩa khẳng định tuyệt đối ('đã nói rồi đấy thôi!').",
            "explanation": "'不是' đứng đầu phân câu phối hợp nhịp nhàng với '吗' ở cuối câu để tạo ngữ điệu nhắc nhở trách móc nhẹ nhàng."
        },
        "breakdown": [
            { "role": "Cụm phản vấn đầu câu", "text": "不是", "type": "grammar", "desc": "Mở đầu cấu trúc câu hỏi tu từ" },
            { "role": "Trạng ngữ hoàn thành", "text": "已经", "type": "modifier", "desc": "Biểu thị sự việc đã hoàn tất trước đó" },
            { "role": "Vị ngữ động tân", "text": "告诉了你", "type": "verb", "desc": "Động từ '告诉' mang tân ngữ '你' và trợ từ '了'" },
            { "role": "Trợ từ nghi vấn", "text": "吗", "type": "grammar", "desc": "Chốt câu hỏi phản vấn" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["了吗", "不是", "告诉你", "已经"],
            "target_chunks": ["不是", "已经", "告诉你", "了吗"],
            "hint": "Cấu trúc phản vấn: 不是 + 已经 + 告诉你 + 了吗？"
        }
    },
    {
        "id": "hsk4_test5_q91",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第91题)",
        "zh": "请把钥匙放到服务台。",
        "pinyin": "qǐng bǎ yào shi fàng dào fú wù tái 。",
        "hanviet": "Thỉnh Bả Thược Thi Phóng Đáo Phục Vụ Đài 。",
        "meaning": "Xin vui lòng để chìa khóa ở quầy lễ tân.",
        "tokens": [
            { "text": "请", "type": "normal", "role": "Từ lịch sự mở đầu" },
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "钥匙", "type": "core", "role": "Tân ngữ chịu tác động (chìa khóa)" },
            { "text": "放", "type": "normal", "role": "Động từ chính (đặt, để)" },
            { "text": "到", "type": "grammar", "role": "Bổ ngữ kết quả định vị nơi chốn" },
            { "text": "服务台", "type": "core", "role": "Tân ngữ chỉ vị trí nơi chốn (quầy dịch vụ/lễ tân)" }
        ],
        "grammar_point": {
            "name": "Câu chữ 把 kết hợp Bổ ngữ nơi chốn 到: 把 + Vật + 放/摆/送 + 到 + Nơi chốn",
            "pattern": "请 / Chủ ngữ + 把 + Tân ngữ vật + Động từ + 到 + Nơi chốn",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Khi động từ mang bổ ngữ kết quả chỉ nơi chốn '到', tân ngữ chỉ nơi chốn ('服务台') bắt buộc phải đứng SAU '到'. Không được nói '把钥匙在服务台放'.",
            "explanation": "Câu chữ 把 thể hiện sự dịch chuyển vị trí không gian của chiếc chìa khóa ('钥匙') đến điểm dừng chân là quầy phục vụ ('服务台')."
        },
        "breakdown": [
            { "role": "Từ thỉnh cầu", "text": "请", "type": "subject", "desc": "Lời đề nghị nhã nhặn" },
            { "role": "Giới từ 把 + Vật tác động", "text": "把钥匙", "type": "object", "desc": "Đưa đối tượng chìa khóa lên trước động từ" },
            { "role": "Vị ngữ + Bổ ngữ kết quả", "text": "放到", "type": "verb", "desc": "Hành vi đặt để kèm đích đến" },
            { "role": "Tân ngữ nơi chốn", "text": "服务台", "type": "object", "desc": "Quầy lễ tân đón tiếp" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["放到", "把钥匙", "服务台", "请"],
            "target_chunks": ["请", "把钥匙", "放到", "服务台"],
            "hint": "Cấu trúc: 请 + 把钥匙 + 放到 + 服务台."
        }
    },
    {
        "id": "hsk4_test5_q92",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第92题)",
        "zh": "小王已经三天没上班了。",
        "pinyin": "xiǎo wáng yǐ jīng sān tiān méi shàng bān le 。",
        "hanviet": "Tiểu Vương Dĩ Kinh Tam Thiên Một Thượng Ban Liễu 。",
        "meaning": "Tiểu Vương đã ba ngày nay không đi làm rồi.",
        "tokens": [
            { "text": "小王", "type": "normal", "role": "Chủ ngữ" },
            { "text": "已经", "type": "normal", "role": "Phó từ hoàn thành" },
            { "text": "三天", "type": "core", "role": "Thời lượng trạng ngữ" },
            { "text": "没", "type": "grammar", "role": "Phó từ phủ định" },
            { "text": "上班", "type": "core", "role": "Động từ (đi làm)" },
            { "text": "了", "type": "normal", "role": "Trợ từ ngữ khí biến hóa" }
        ],
        "grammar_point": {
            "name": "Bổ ngữ thời lượng trong câu phủ định (Khoảng thời gian không diễn ra việc gì)",
            "pattern": "Chủ ngữ + (已经) + Khoảng thời gian + 没 / 不 + Động từ + (了)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Khi biểu thị một hành động KHÔNG diễn ra trong bao lâu, khoảng thời lượng ('三天') bắt buộc phải đứng TRƯỚC '没 + Động từ'. Đây là điểm rất dễ nhầm lẫn với bổ ngữ thời lượng khẳng định.",
            "explanation": "Câu khẳng định: 上了三天班 (đi làm được 3 ngày). Câu phủ định: 三天没上班 (3 ngày chưa đi làm). '了' ở cuối câu biểu thị trạng thái này vẫn đang tiếp diễn."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "小王", "type": "subject", "desc": "Đối tượng được đề cập" },
            { "role": "Trạng ngữ thời gian hoàn thành", "text": "已经", "type": "modifier", "desc": "Nhấn mạnh mốc thời gian" },
            { "role": "Khoảng thời lượng gián đoạn", "text": "三天", "type": "modifier", "desc": "Số ngày liên tục không xuất hiện" },
            { "role": "Vị ngữ phủ định", "text": "没上班了", "type": "verb", "desc": "Hành vi vắng mặt tại nơi làm việc" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["没上班了", "三天", "已经", "小王"],
            "target_chunks": ["小王", "已经", "三天", "没上班了"],
            "hint": "Quy tắc câu phủ định thời lượng: Chủ ngữ (小王) + 已经 + Thời lượng (三天) + 没上班了."
        }
    },
    {
        "id": "hsk4_test5_q93",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第93题)",
        "zh": "你怎么这么晚才来？",
        "pinyin": "nǐ zěn me zhè me wǎn cái lái ？",
        "hanviet": "Nhĩ Chẩm Ma Giá Ma Vãn Tài Lai ？",
        "meaning": "Sao bạn lại đến muộn thế này mới tới?",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Chủ ngữ" },
            { "text": "怎么", "type": "grammar", "role": "Đại từ nghi vấn (sao/tại sao)" },
            { "text": "这么晚", "type": "core", "role": "Cụm trạng ngữ mức độ thời gian trễ" },
            { "text": "才", "type": "grammar", "role": "Phó từ biểu thị hành động diễn ra muộn/chậm" },
            { "text": "来", "type": "normal", "role": "Động từ chính" }
        ],
        "grammar_point": {
            "name": "Phó từ 才 biểu thị hành động diễn ra chậm trễ, muộn màng",
            "pattern": "Chủ ngữ + 怎么 + 这么 + Tính từ thời gian (晚/迟) + 才 + Động từ",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY TỪ HƯ: '才' dùng để nhấn mạnh người nói cảm thấy hành động xảy ra quá muộn hoặc tốn nhiều thời gian. Không được nhầm lẫn với '就' (nhấn mạnh nhanh chóng).",
            "explanation": "'怎么' hỏi về lý do kèm sắc thái ngạc nhiên hoặc trách yêu. '这么晚才来' tạo thành cụm vị ngữ miêu tả sự xuất hiện chậm chạp."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你", "type": "subject", "desc": "Người được hỏi" },
            { "role": "Trạng ngữ nghi vấn", "text": "怎么", "type": "modifier", "desc": "Dò hỏi căn nguyên sự việc" },
            { "role": "Trạng ngữ thời gian trễ", "text": "这么晚", "type": "modifier", "desc": "Mức độ muộn quá kỳ vọng" },
            { "role": "Vị ngữ nhấn mạnh chậm trễ", "text": "才来", "type": "verb", "desc": "Phó từ '才' đi cùng động từ '来'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["这么晚", "你", "才来", "怎么"],
            "target_chunks": ["你", "怎么", "这么晚", "才来"],
            "hint": "Trật tự: Chủ ngữ (你) + Đại từ nghi vấn (怎么) + Thời gian trễ (这么晚) + 才来."
        }
    },
    {
        "id": "hsk4_test5_q94",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第94题)",
        "zh": "我能克服任何困难。",
        "pinyin": "wǒ néng kè fú rèn hé kùn nan 。",
        "hanviet": "Ngã Năng Khắc Phục Nhiệm Hà Khốn Nan 。",
        "meaning": "Tôi có thể khắc phục bất kỳ khó khăn nào.",
        "tokens": [
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "能", "type": "grammar", "role": "Động từ năng nguyện (có thể)" },
            { "text": "克服", "type": "core", "role": "Động từ chính (vượt qua/khắc phục)" },
            { "text": "任何", "type": "core", "role": "Đại từ hạn định (bất kỳ)" },
            { "text": "困难", "type": "core", "role": "Danh từ tân ngữ (khó khăn, trở ngại)" }
        ],
        "grammar_point": {
            "name": "Đại từ phiếm chỉ 任何 làm định ngữ và Động từ 克服",
            "pattern": "Chủ ngữ + (能/可以) + Động từ + 任何 + Danh từ tân ngữ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '任何' (bất kỳ) là đại từ phiếm chỉ mang tính khái quát toàn diện, làm định ngữ đứng ngay trước danh từ mà nó bổ nghĩa ('任何困难'). Cặp từ phối hợp chuẩn: 克服困难.",
            "explanation": "Động từ năng nguyện '能' đứng trước động từ '克服' thể hiện ý chí và năng lực vượt qua mọi gian truân thử thách."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我", "type": "subject", "desc": "Chủ thể mang ý chí tự tin" },
            { "role": "Trợ động từ", "text": "能", "type": "grammar", "desc": "Năng lực, khả năng" },
            { "role": "Vị ngữ động từ", "text": "克服", "type": "verb", "desc": "Hành vi chiến thắng nghịch cảnh" },
            { "role": "Cụm định-tân ngữ", "text": "任何困难", "type": "object", "desc": "Mọi khó khăn trắc trở không ngoại lệ" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["任何困难", "能", "我", "克服"],
            "target_chunks": ["我", "能", "克服", "任何困难"],
            "hint": "Cấu trúc: Chủ ngữ (我) + 能 + Động từ (克服) + Tân ngữ phiếm chỉ (任何困难)."
        }
    },
    {
        "id": "hsk4_test5_q95",
        "category": "sentence_building",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 书写 第一部分 (第95题)",
        "zh": "桌子上摆着两盆花儿。",
        "pinyin": "zhuō zi shang bǎi zhe liǎng pén huàr 。",
        "hanviet": "Trác Tử Thượng Bãi Trước Lưỡng Bồn Họa Nhi 。",
        "meaning": "Trên bàn có bày biện hai chậu hoa.",
        "tokens": [
            { "text": "桌子上", "type": "core", "role": "Trạng ngữ nơi chốn làm vị trí khởi đầu" },
            { "text": "摆", "type": "core", "role": "Động từ (bày biện, sắp đặt)" },
            { "text": "着", "type": "grammar", "role": "Trợ từ động thái duy trì trạng thái" },
            { "text": "两盆", "type": "core", "role": "Số từ + Lượng từ chuyên dụng cho chậu cây" },
            { "text": "花儿", "type": "normal", "role": "Tân ngữ tồn tại (hoa)" }
        ],
        "grammar_point": {
            "name": "Câu tồn hiện tĩnh trạng thái: Nơi chốn + 摆着 / 放着 + Lượng từ + Danh từ",
            "pattern": "Nơi chốn + Động từ tư thế/sắp đặt + 着 + Số lượng + Danh từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LƯỢNG TỪ: Lượng từ chuẩn xác cho hoa trồng trong chậu là '盆' (pén), tuyệt đối không dùng '个' hay '朵' trong ngữ cảnh này.",
            "explanation": "'摆着' diễn tả trạng thái của các chậu hoa sau khi đã được ai đó sắp đặt chỉn chu trên mặt bàn."
        },
        "breakdown": [
            { "role": "Nơi chốn tồn tại", "text": "桌子上", "type": "subject", "desc": "Bề mặt đồ vật làm bối cảnh không gian" },
            { "role": "Vị ngữ + Duy trì trạng thái", "text": "摆着", "type": "verb", "desc": "Động từ '摆' đi kèm trợ từ '着'" },
            { "role": "Số lượng từ", "text": "两盆", "type": "modifier", "desc": "Số lượng và lượng từ quy chuẩn" },
            { "role": "Thực thể tồn tại", "text": "花儿", "type": "object", "desc": "Hai chậu hoa tươi" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["两盆花儿", "桌子上", "摆着"],
            "target_chunks": ["桌子上", "摆着", "两盆花儿"],
            "hint": "Cấu trúc tồn hiện: Nơi chốn (桌子上) + Động từ kèm 着 (摆着) + Lượng từ và danh từ (两盆花儿)."
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Logic 56-65)
    # =========================================================================
    {
        "id": "hsk4_test5_q56",
        "category": "sentence_logic",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 阅读 第二部分 (第56题)",
        "zh": "我经常跟中国人做生意，不会说汉语很不方便，于是我开始学习汉语。",
        "pinyin": "wǒ jīng cháng gēn zhōng guó rén zuò shēng yi ， bú huì shuō hàn yǔ hěn bù fāng biàn ， yú shì wǒ kāi shǐ xué xí hàn yǔ 。",
        "hanviet": "Ngã Kinh Thường Căn Trung Quốc Nhân Tác Sanh Ý ， Bất Hội Thuyết Hán Ngữ Hẩn Bất Phương Tiện ， Vu Thị Ngã Khai Thủy Học Tập Hán Ngữ 。",
        "meaning": "Tôi thường làm ăn buôn bán với người Trung Quốc, không biết nói tiếng Trung rất bất tiện, thế là tôi bắt đầu học tiếng Trung.",
        "tokens": [
            { "text": "我经常跟中国人做生意", "type": "core", "role": "Hoàn cảnh tiền đề (C)" },
            { "text": "不会说汉语", "type": "normal", "role": "Khó khăn trở ngại" },
            { "text": "很不方便", "type": "normal", "role": "Tác động tiêu cực (A)" },
            { "text": "于是", "type": "grammar", "role": "Liên từ kết quả liên tiếp (thế là/do đó)" },
            { "text": "我开始学习汉语", "type": "core", "role": "Hành động giải quyết tiếp nối (B)" }
        ],
        "grammar_point": {
            "name": "Liên từ 于是 biểu thị hành vi tiếp nối xuất phát từ nguyên do trước đó",
            "pattern": "Hoàn cảnh (C) + Vấn đề phát sinh (A) + 于是 + Hành động ứng phó (B)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: '于是' (thế là/do đó) luôn đứng đầu phân câu biểu thị hành động nảy sinh ngay sau một tình huống, do đó câu B bắt buộc phải đứng cuối cùng.",
            "explanation": "C mở đầu bằng công việc thường nhật. A chỉ ra bất cập nảy sinh từ việc rào cản ngôn ngữ. B đưa ra giải pháp khắc phục bằng cách học tập."
        },
        "breakdown": [
            { "role": "Bối cảnh mở đầu (C)", "text": "我经常跟中国人做生意", "type": "subject", "desc": "Giới thiệu môi trường công việc thực tế" },
            { "role": "Vấn đề nảy sinh (A)", "text": "不会说汉语很不方便", "type": "verb", "desc": "Khó khăn giao tiếp gây trở ngại" },
            { "role": "Hành động giải pháp (B)", "text": "于是我开始学习汉语", "type": "object", "desc": "Liên từ '于是' khởi đầu hành động học tiếng Trung" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "不会说汉语很不方便" },
                { "id": "B", "text": "于是我开始学习汉语" },
                { "id": "C", "text": "我经常跟中国人做生意" }
            ],
            "correct_order": "CAB",
            "hint": "Hoàn cảnh (C) -> Khó khăn phát sinh (A) -> '于是' đưa ra hành động (B)."
        }
    },
    {
        "id": "hsk4_test5_q58",
        "category": "sentence_logic",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 阅读 第二部分 (第58题)",
        "zh": "一个人只要有了目标，并懂得为那个目标而奋斗，那他就一定会成功。",
        "pinyin": "yí gè rén zhǐ yào yǒu le mù biāo ， bìng dǒng de wèi nà gè mù biāo ér fèn dòu ， nà tā jiù yí dìng huì chéng gōng 。",
        "hanviet": "Nhất Cá Nhân Chỉ Yếu Hữu Liễu Mục Tiêu ， Tịnh Hiểu Đắc Vị Na Cá Mục Tiêu Nhi Phấn Đấu ， Na Tha Tựu Nhất Định Hội Thành Công 。",
        "meaning": "Một người chỉ cần có mục tiêu, đồng thời biết nỗ lực phấn đấu vì mục tiêu ấy, thì người đó nhất định sẽ thành công.",
        "tokens": [
            { "text": "一个人", "type": "normal", "role": "Chủ thể khái quát" },
            { "text": "只要有了目标", "type": "core", "role": "Điều kiện cần thứ nhất (A)" },
            { "text": "并懂得", "type": "grammar", "role": "Liên từ tăng tiến (đồng thời/và)" },
            { "text": "为那个目标而奋斗", "type": "core", "role": "Điều kiện cần thứ hai (C)" },
            { "text": "那他就一定会成功", "type": "core", "role": "Hệ quả tất yếu chốt lại (B)" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ điều kiện 只要...那...就... kết hợp Liên từ tăng tiến 并",
            "pattern": "Chủ ngữ + 只要 + Điều kiện 1 + 并 + Điều kiện 2 + 那...就... + Kết quả",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: '那个目标' ở câu C sử dụng đại từ chỉ thị thay thế cho '目标' đã nhắc ở câu A, do đó C bắt buộc phải đứng sau A. Vế '那他就一定会成功' có '那...就...' kết lại kết quả.",
            "explanation": "A đặt tiền đề mục tiêu bằng '只要'. C bổ sung hành động cụ thể hóa mục tiêu bằng liên từ '并'. B rút ra kết luận thành công bằng '那...就'."
        },
        "breakdown": [
            { "role": "Điều kiện tiên quyết (A)", "text": "一个人只要有了目标", "type": "subject", "desc": "Khởi xướng điều kiện bằng '只要'" },
            { "role": "Bổ sung hành động (C)", "text": "并懂得为那个目标而奋斗", "type": "verb", "desc": "Dùng '并' kết nối hành động phấn đấu vì '那个目标'" },
            { "role": "Kết quả tất yếu (B)", "text": "那他就一定会成功", "type": "object", "desc": "Dùng '那...就...' khẳng định sự thành công" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "一个人只要有了目标" },
                { "id": "B", "text": "那他就一定会成功" },
                { "id": "C", "text": "并懂得为那个目标而奋斗" }
            ],
            "correct_order": "ACB",
            "hint": "A có '只要有了目标' -> C có '那个目标' nối tiếp bằng '并' -> B có '那他就...' kết luận."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test 46-55)
    # =========================================================================
    {
        "id": "hsk4_test5_q52",
        "category": "cloze",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 阅读 第一部分 (第52题)",
        "zh": "别着急，只要你多听、多练，听力水平一定会逐渐提高的。",
        "pinyin": "bié zháo jí ， zhǐ yào nǐ duō tīng 、 duō liàn ， tīng lì shuǐ píng yí dìng huì zhú jiàn tí gāo de 。",
        "hanviet": "Biệt Trước Cấp ， Chỉ Yếu Nhĩ Đa Thính 、 Đa Luyện ， Thính Lực Thủy Bình Nhất Định Hội Trục Tiệm Đề Cao Đích 。",
        "meaning": "Đừng lo lắng, chỉ cần bạn nghe nhiều, luyện nhiều, trình độ nghe nhất định sẽ từng bước được nâng cao.",
        "tokens": [
            { "text": "别着急", "type": "normal", "role": "Lời an ủi" },
            { "text": "只要", "type": "grammar", "role": "Liên từ điều kiện" },
            { "text": "多听、多练", "type": "normal", "role": "Hành vi tích lũy" },
            { "text": "听力水平", "type": "core", "role": "Chủ ngữ phân câu sau (kỹ năng nghe)" },
            { "text": "一定会", "type": "grammar", "role": "Khẳng định chắc chắn" },
            { "text": "逐渐", "type": "grammar", "role": "Phó từ diễn tiến (từng bước, dần dần)" },
            { "text": "提高", "type": "core", "role": "Động từ vị ngữ (nâng cao)" },
            { "text": "的", "type": "normal", "role": "Trợ từ nhấn mạnh cuối câu" }
        ],
        "grammar_point": {
            "name": "Phó từ chỉ sự tiến triển tuần tự 逐渐 (Dần dần / Từng bước một)",
            "pattern": "Chủ ngữ (Trình độ/Môi trường) + (会) + 逐渐 + Động từ biến hóa (提高/改变/适应)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '逐渐' biểu thị quá trình thay đổi từ từ theo thời gian, phù hợp tuyệt đối khi bổ nghĩa cho động từ '提高' (nâng cao trình độ).",
            "explanation": "'逐渐' đứng trước động từ '提高' làm trạng ngữ miêu tả nhịp độ thăng tiến tiệm tiến của trình độ nghe."
        },
        "breakdown": [
            { "role": "Lời khuyên nhủ", "text": "别着急", "type": "subject", "desc": "Giảm bớt áp lực tâm lý" },
            { "role": "Điều kiện rèn luyện", "text": "只要你多听、多练", "type": "modifier", "desc": "Phương pháp học tích lũy" },
            { "role": "Khẳng định kết quả tiệm tiến", "text": "听力水平一定会逐渐提高的", "type": "verb", "desc": "Phó từ '逐渐' miêu tả năng lực thăng tiến vững chắc" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "别着急，只要你多听、多练，听力水平一定会（  ）提高的。",
            "options": ["逐渐", "几乎", "害羞", "不要紧", "考虑"],
            "blank_index": 0,
            "correct_answer": "逐渐",
            "hint": "Cần một phó từ bổ nghĩa cho '提高' (nâng cao dần dần theo thời gian). Chọn '逐渐'."
        }
    },
    {
        "id": "hsk4_test5_q54",
        "category": "cloze",
        "test_id": 5,
        "source": "HSK 4 模拟试卷 5 阅读 第一部分 (第54题)",
        "zh": "现在这个公司的待遇是不错，可是太累了！几乎没有休息日。",
        "pinyin": "xiàn zài zhè ge gōng sī de dài yù shì bú cuò ， kě shì tài lèi le ！ jī hū méi yǒu xiū xi rì 。",
        "hanviet": "Hiện Tại Giá Cá Công Ty Đích Đãi Ngộ Thị Bất Thác ， Khả Thị Thái Luy Liễu ！ Cơ Hồ Một Hữu Hưu Tức Nhật 。",
        "meaning": "Hiện tại chế độ đãi ngộ của công ty này thì tốt thật, nhưng mệt mỏi quá! Hầu như không có ngày nghỉ ngơi.",
        "tokens": [
            { "text": "待遇", "type": "core", "role": "Đãi ngộ, lương bổng" },
            { "text": "不错", "type": "normal", "role": "Khá tốt" },
            { "text": "可是", "type": "grammar", "role": "Liên từ chuyển ngoặt (nhưng)" },
            { "text": "太累了", "type": "normal", "role": "Mệt mỏi quá" },
            { "text": "几乎", "type": "grammar", "role": "Phó từ mức độ xấp xỉ tuyệt đối (hầu như, gần như)" },
            { "text": "没有", "type": "normal", "role": "Phủ định sự tồn tại" },
            { "text": "休息日", "type": "core", "role": "Ngày nghỉ định kỳ" }
        ],
        "grammar_point": {
            "name": "Phó từ chỉ mức độ xấp xỉ 几乎 (Hầu như / Gần như)",
            "pattern": "几乎 + 没 / 没有 + Danh từ / Động từ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: Cụm '几乎没有' là kết hợp cực kỳ phổ biến trong các đề thi HSK 4, biểu thị tình trạng gần như bằng 0 hoặc hiếm hoi vô cùng.",
            "explanation": "'几乎' bổ nghĩa cho '没有休息日' nhằm nhấn mạnh mức độ bận rộn và kiệt sức trong công việc."
        },
        "breakdown": [
            { "role": "Vế chuyển nhượng", "text": "待遇是不错，可是太累了", "type": "subject", "desc": "Nêu ưu điểm thu nhập nhưng quá tải sức lực" },
            { "role": "Trạng ngữ mức độ gần như tuyệt đối", "text": "几乎", "type": "modifier", "desc": "Tỷ lệ xảy ra đạt xấp xỉ 100%" },
            { "role": "Thực trạng làm việc", "text": "没有休息日", "type": "verb", "desc": "Hoàn toàn thiếu vắng ngày nghỉ ngơi" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "现在这个公司的待遇是不错，可是太累了！（  ）没有休息日。",
            "options": ["几乎", "逐渐", "害羞", "不要紧", "温度"],
            "blank_index": 0,
            "correct_answer": "几乎",
            "hint": "Đi liền trước '没有休息日' mang nghĩa 'gần như / hầu như không có'. Chọn '几乎'."
        }
    }
]
