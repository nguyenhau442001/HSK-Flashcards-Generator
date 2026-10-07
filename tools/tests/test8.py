# -*- coding: utf-8 -*-
"""
Authentic items curated from HSK 4 模拟试卷 8 (Mock Test 8).
Source: Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
"""

TEST8_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building 86-95)
    # =========================================================================
    {
        "id": "hsk4_test8_q86",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第86题)",
        "zh": "请把钢笔递给我。",
        "pinyin": "qǐng bǎ gāng bǐ dì gěi wǒ 。",
        "hanviet": "Thỉnh Bả Cương Bút Đệ Cấp Ngã 。",
        "meaning": "Xin hãy chuyền/đưa cây bút mực cho tôi.",
        "tokens": [
            { "text": "请", "type": "normal", "role": "Từ lịch sự" },
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "钢笔", "type": "core", "role": "Tân ngữ chịu tác động (bút mực)" },
            { "text": "递", "type": "core", "role": "Động từ chính (chuyền, chuyển giao bằng tay)" },
            { "text": "给", "type": "grammar", "role": "Bổ ngữ chỉ đối tượng tiếp nhận" },
            { "text": "我", "type": "normal", "role": "Người tiếp nhận" }
        ],
        "grammar_point": {
            "name": "Câu chữ 把 với động từ chuyển giao tiếp xúc: 把 + Vật + 递 / 借 / 送 + 给 + Người",
            "pattern": "请 / Chủ ngữ + 把 + Vật cụ thể + 递给 + Người nhận",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: Động từ '递' (chuyền qua tay) thường đi liền mạch với '给' thành cụm '递给'. Người nhận '我' phải đứng ngay sau '给'.",
            "explanation": "Câu chữ 把 nhấn mạnh sự dịch chuyển cự ly gần của cây bút từ tay đối phương sang tay người nói."
        },
        "breakdown": [
            { "role": "Lời thỉnh cầu", "text": "请", "type": "subject", "desc": "Lời nhờ vả nhã nhặn" },
            { "role": "Giới từ 把 + Vật tác động", "text": "把钢笔", "type": "object", "desc": "Đưa đối tượng bút máy lên trước" },
            { "role": "Vị ngữ + Người nhận", "text": "递给我", "type": "verb", "desc": "Thao tác chuyền tay đưa sang cho '我'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["递给我", "钢笔", "把", "请"],
            "target_chunks": ["请", "把", "钢笔", "递给我"],
            "hint": "Cấu trúc: 请 + 把 + [钢笔] + 递给我."
        }
    },
    {
        "id": "hsk4_test8_q87",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第87题)",
        "zh": "杯子让我摔坏了。",
        "pinyin": "bēi zi ràng wǒ shuāi huài le 。",
        "hanviet": "Bôi Tử Nhượng Ngã Suất Hoại Liễu 。",
        "meaning": "Cái ly đã bị tôi làm rơi vỡ mất rồi.",
        "tokens": [
            { "text": "杯子", "type": "core", "role": "Chủ ngữ chịu tổn hại (cốc/ly)" },
            { "text": "让", "type": "grammar", "role": "Giới từ bị động khẩu ngữ (bị/do)" },
            { "text": "我", "type": "normal", "role": "Tác nhân gây ra sự cố" },
            { "text": "摔", "type": "core", "role": "Động từ chính (rơi, va đập)" },
            { "text": "坏", "type": "grammar", "role": "Bổ ngữ kết quả (hư hại, vỡ nát)" },
            { "text": "了", "type": "normal", "role": "Trợ từ hoàn thành" }
        ],
        "grammar_point": {
            "name": "Câu bị động khẩu ngữ với giới từ 让 / 叫 (thay cho 被)",
            "pattern": "Vật chịu tác động + 让 / 叫 + Tác nhân gây hại + Động từ + Bổ ngữ kết quả + 了",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Trong khẩu ngữ tiếng Trung, '让' và '叫' hoàn toàn có thể làm GIỚI TỪ BỊ ĐỘNG tương đương như '被' ('杯子让我摔坏了' = '杯子被我摔坏了'). Khác với '被', sau '让' và '叫' bắt buộc PHẢI có tác nhân ('我'), không được lược bỏ.",
            "explanation": "Câu diễn tả tai nạn bất cẩn ngoài ý muốn khiến đồ vật bị hư hỏng, mang sắc thái nhận lỗi."
        },
        "breakdown": [
            { "role": "Chủ ngữ chịu hư hại", "text": "杯子", "type": "subject", "desc": "Chiếc cốc thủy tinh hoặc gốm" },
            { "role": "Giới từ bị động + Tác nhân", "text": "让我", "type": "modifier", "desc": "Bị bản thân tôi sơ ý tác động" },
            { "role": "Vị ngữ + Bổ ngữ kết quả", "text": "摔坏了", "type": "verb", "desc": "Động từ '摔' làm vỡ hỏng vật thể" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["摔坏了", "杯子", "让我"],
            "target_chunks": ["杯子", "让我", "摔坏了"],
            "hint": "Cấu trúc bị động khẩu ngữ: Đồ vật (杯子) + 让我 + 摔坏了."
        }
    },
    {
        "id": "hsk4_test8_q88",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第88题)",
        "zh": "我们还是坐火车去吧。",
        "pinyin": "wǒ men hái shì zuò huǒ chē qù ba 。",
        "hanviet": "Ngã Môn Hoàn Thị Tọa Hỏa Xa Khứ Ba 。",
        "meaning": "Chúng ta hay là đi bằng tàu hỏa đi.",
        "tokens": [
            { "text": "我们", "type": "normal", "role": "Chủ ngữ" },
            { "text": "还是", "type": "grammar", "role": "Phó từ đưa ra kiến nghị tối ưu" },
            { "text": "坐", "type": "normal", "role": "Động từ cách thức di chuyển" },
            { "text": "火车", "type": "normal", "role": "Phương tiện" },
            { "text": "去", "type": "normal", "role": "Động từ xu hướng hướng ra xa" },
            { "text": "吧", "type": "grammar", "role": "Trợ từ ngữ khí đề xuất" }
        ],
        "grammar_point": {
            "name": "Phó từ 还是 biểu thị quyết định sau khi cân nhắc và Phương thức di chuyển 坐 + Phương tiện + 去",
            "pattern": "Chủ ngữ + 还是 + 坐 / 乘 + Phương tiện giao thông + 去 / 来 + 吧",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: '还是' đứng trước cụm vị ngữ '坐火车去' để thể hiện giải pháp hợp lý nhất. Trợ từ ngữ khí '吧' ở cuối câu tạo sự đồng thuận.",
            "explanation": "Có thể giữa các phương án máy bay, ô tô hoặc tàu hỏa, người nói kiến nghị chọn đi tàu hỏa vì an toàn hoặc tiết kiệm."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "我们", "type": "subject", "desc": "Nhóm người cùng đi" },
            { "role": "Ý kiến lựa chọn", "text": "还是", "type": "grammar", "desc": "Chọn phương án có lợi hơn" },
            { "role": "Phương thức di chuyển", "text": "坐火车", "type": "modifier", "desc": "Sử dụng tàu hỏa làm phương tiện" },
            { "role": "Vị ngữ + Ngữ khí", "text": "去吧", "type": "verb", "desc": "Di chuyển tới đích đến kèm lời rủ rê" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["去吧", "坐火车", "我们", "还是"],
            "target_chunks": ["我们", "还是", "坐火车", "去吧"],
            "hint": "Chủ ngữ (我们) + 还是 + Phương thức (坐火车) + 去吧."
        }
    },
    {
        "id": "hsk4_test8_q89",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第89题)",
        "zh": "你买的空调怎么样？",
        "pinyin": "nǐ mǎi de kōng tiáo zěn me yàng ？",
        "hanviet": "Nhĩ Mãi Đích Không Điều Chẩm Ma Dạng ？",
        "meaning": "Chiếc máy điều hòa bạn mua dùng thế nào?",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Đại từ" },
            { "text": "买", "type": "normal", "role": "Động từ làm định ngữ" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "空调", "type": "core", "role": "Chủ ngữ trung tâm (máy điều hòa)" },
            { "text": "怎么样", "type": "core", "role": "Đại từ nghi vấn hỏi về tính chất, trải nghiệm" }
        ],
        "grammar_point": {
            "name": "Câu hỏi đánh giá phẩm chất: Cụm định-trung (V+的+N) + 怎么样？",
            "pattern": "Chủ ngữ (Định ngữ + 的 + Danh từ) + 怎么样？",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY CẤU TRÚC: '你买的' là cụm định ngữ bổ nghĩa cho '空调'. '怎么样' trực tiếp làm vị ngữ để hỏi chất lượng hoặc cảm nhận sau khi sử dụng.",
            "explanation": "Câu giao tiếp hỏi thăm trải nghiệm mua sắm vật dụng gia đình thường thấy."
        },
        "breakdown": [
            { "role": "Định ngữ mệnh đề", "text": "你买的", "type": "modifier", "desc": "Hành vi mua sắm của bạn" },
            { "role": "Chủ ngữ danh từ", "text": "空调", "type": "subject", "desc": "Thiết bị làm mát không khí" },
            { "role": "Vị ngữ nghi vấn", "text": "怎么样", "type": "verb", "desc": "Dò hỏi mức độ hài lòng, công năng sử dụng" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["空调", "怎么样", "你买的"],
            "target_chunks": ["你买的", "空调", "怎么样"],
            "hint": "Cấu trúc: [你买的] + 空调 + 怎么样？"
        }
    },
    {
        "id": "hsk4_test8_q90",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第90题)",
        "zh": "海南岛一年四季都很美。",
        "pinyin": "hǎi nán dǎo yì nián sì jì dōu hěn měi 。",
        "hanviet": "Hải Nam Đảo Nhất Niên Tứ Quý Đô Hẩn Mỹ 。",
        "meaning": "Đảo Hải Nam suốt bốn mùa quanh năm đều rất đẹp.",
        "tokens": [
            { "text": "海南岛", "type": "core", "role": "Chủ ngữ (đảo Hải Nam)" },
            { "text": "一年四季", "type": "core", "role": "Thành ngữ thời gian (bốn mùa quanh năm)" },
            { "text": "都", "type": "grammar", "role": "Phó từ khái quát toàn bộ" },
            { "text": "很", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "美", "type": "normal", "role": "Tính từ vị ngữ (đẹp)" }
        ],
        "grammar_point": {
            "name": "Cụm thời gian chỉ sự liên tục kết hợp Phó từ 都",
            "pattern": "Địa điểm + 一年四季 / 天天 / 处处 + 都 + (很) + Tính từ",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY TỪ HƯ: Sau cụm từ mang ý nghĩa bao quát toàn bộ thời gian như '一年四季' (quanh năm suốt tháng), bắt buộc phải có phó từ '都' đứng trước vị ngữ miêu tả.",
            "explanation": "Câu ca ngợi cảnh sắc thiên nhiên nhiệt đới trù phú, tươi đẹp quanh năm của hòn đảo Hải Nam."
        },
        "breakdown": [
            { "role": "Chủ ngữ địa danh", "text": "海南岛", "type": "subject", "desc": "Hòn đảo du lịch phía nam Trung Quốc" },
            { "role": "Trạng ngữ thời gian liên tục", "text": "一年四季", "type": "modifier", "desc": "Bốn mùa xuân hạ thu đông" },
            { "role": "Vị ngữ khẳng định toàn thể", "text": "都很美", "type": "verb", "desc": "Phó từ '都' kết hợp tính từ '美'" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["一年四季", "海南岛", "都很美"],
            "target_chunks": ["海南岛", "一年四季", "都很美"],
            "hint": "Chủ ngữ (海南岛) + Thời gian (一年四季) + Vị ngữ (都很美)."
        }
    },
    {
        "id": "hsk4_test8_q91",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第91题)",
        "zh": "他一上课就想睡觉。",
        "pinyin": "tā yí shàng kè jiù xiǎng shuì jiào 。",
        "hanviet": "Tha Nhất Thượng Khóa Tựu Tưởng Thụy Giác 。",
        "meaning": "Cậu ấy hễ cứ vào học là lại muốn đi ngủ.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "一", "type": "grammar", "role": "Cặp liên từ điều kiện liên tiếp (hễ/vừa)" },
            { "text": "上课", "type": "core", "role": "Hành động điều kiện 1 (vào giờ học)" },
            { "text": "就", "type": "grammar", "role": "Phó từ liên kết hệ quả tức thì (là/thì)" },
            { "text": "想", "type": "normal", "role": "Nguyện vọng" },
            { "text": "睡觉", "type": "core", "role": "Hành vi buồn ngủ diễn ra ngay sau đó" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ phản ứng tức thì: 一...就... (Hễ... là... / Vừa... liền...)",
            "pattern": "Chủ ngữ + 一 + Hành động 1 + 就 + (想) + Hành động 2",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY CẤU TRÚC: Cặp cấu trúc '一...就...' dùng để chỉ sự việc thứ hai diễn ra ngay tức khắc sau sự việc thứ nhất theo quy luật bất di bất dịch. '一' đứng ngay trước động từ 1 (上课), '就' đứng ngay trước động từ 2 (想睡觉).",
            "explanation": "Câu nói hóm hỉnh miêu tả thói quen lười học hoặc mệt mỏi của học sinh khi bước vào tiết giảng."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Cậu học trò" },
            { "role": "Điều kiện kích hoạt", "text": "一上课", "type": "modifier", "desc": "Vừa mới bước vào giờ học" },
            { "role": "Phản ứng tất yếu", "text": "就想睡觉", "type": "verb", "desc": "Lập tức xuất hiện cảm giác buồn ngủ" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["想睡觉", "一上课", "就", "他"],
            "target_chunks": ["他", "一上课", "就", "想睡觉"],
            "hint": "Cấu trúc: 主语 (他) + 一上课 + 就 + 想睡觉."
        }
    },
    {
        "id": "hsk4_test8_q92",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第92题)",
        "zh": "医院里看病的人非常多。",
        "pinyin": "yī yuàn lǐ kàn bìng de rén fēi cháng duō 。",
        "hanviet": "Y Viện Lý Khán Bệnh Đích Nhân Phi Thường Đa 。",
        "meaning": "Người đến khám bệnh trong bệnh viện rất đông.",
        "tokens": [
            { "text": "医院里", "type": "core", "role": "Định ngữ nơi chốn" },
            { "text": "看病", "type": "core", "role": "Hành vi làm định ngữ (khám chữa bệnh)" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "人", "type": "normal", "role": "Chủ ngữ trung tâm (người)" },
            { "text": "非常", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "多", "type": "normal", "role": "Tính từ vị ngữ (đông, nhiều)" }
        ],
        "grammar_point": {
            "name": "Cụm định-trung phức hợp nhiều tầng làm chủ ngữ: Nơi chốn + Hành vi + 的 + Danh từ",
            "pattern": "Nơi chốn + Động từ + 的 + Danh từ người + (非常/很) + 多",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Cụm '医院里看病的人' là toàn bộ chủ ngữ dài (người khám bệnh ở bệnh viện). '非常多' là cụm tính từ làm vị ngữ.",
            "explanation": "Câu miêu tả thực trạng đông đúc, quá tải của các cơ sở y tế."
        },
        "breakdown": [
            { "role": "Chủ ngữ phức hợp", "text": "医院里看病的人", "type": "subject", "desc": "Bệnh nhân và người nhà tới bệnh viện" },
            { "role": "Vị ngữ mức độ số lượng", "text": "非常多", "type": "verb", "desc": "Số lượng vô cùng đông đảo" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["非常多", "医院里", "看病的人"],
            "target_chunks": ["医院里", "看病的人", "非常多"],
            "hint": "Địa điểm + đối tượng (医院里看病的人) + Vị ngữ (非常多)."
        }
    },
    {
        "id": "hsk4_test8_q93",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第93题)",
        "zh": "你做的计划非常合理。",
        "pinyin": "nǐ zuò de jì huà fēi cháng hé lǐ 。",
        "hanviet": "Nhĩ Tác Đích Kế Hoạch Phi Thường Hợp Lý 。",
        "meaning": "Bản kế hoạch do bạn lập ra vô cùng hợp lý.",
        "tokens": [
            { "text": "你做的", "type": "normal", "role": "Định ngữ mệnh đề" },
            { "text": "计划", "type": "core", "role": "Chủ ngữ danh từ (kế hoạch)" },
            { "text": "非常", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "合理", "type": "core", "role": "Tính từ vị ngữ (hợp lý, khoa học)" }
        ],
        "grammar_point": {
            "name": "Cụm V+的+N làm chủ ngữ và Tính từ vị ngữ 合理",
            "pattern": "Người + 做 / 写 / 提 + 的 + Kế hoạch / Đề án + 非常 + 合理",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY TỪ VỰNG: '合理' (hợp lý) là tính từ khen ngợi tính logic, khả thi của một phương án hoặc kế hoạch.",
            "explanation": "Lời đánh giá cao từ cấp trên hoặc đồng nghiệp đối với sự chuẩn bị chu đáo của bạn."
        },
        "breakdown": [
            { "role": "Chủ ngữ định-trung", "text": "你做的计划", "type": "subject", "desc": "Bản phương án do bạn xây dựng" },
            { "role": "Vị ngữ đánh giá tích cực", "text": "非常合理", "type": "verb", "desc": "Tính khả thi và khoa học ở mức cao" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["非常合理", "计划", "你做的"],
            "target_chunks": ["你做的", "计划", "非常合理"],
            "hint": "Chủ ngữ (你做的计划) + Vị ngữ (非常合理)."
        }
    },
    {
        "id": "hsk4_test8_q94",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第94题)",
        "zh": "你们不是已经准备好了吗？",
        "pinyin": "nǐ men bú shì yǐ jīng zhǔn bèi hǎo le ma ？",
        "hanviet": "Nhĩ Môn Bất Thị Dĩ Kinh Chuẩn Bị Hảo Liễu Ma ？",
        "meaning": "Các bạn chẳng phải đã chuẩn bị xong xuôi rồi sao?",
        "tokens": [
            { "text": "你们", "type": "normal", "role": "Chủ ngữ" },
            { "text": "不是", "type": "grammar", "role": "Phó từ phản vấn tu từ" },
            { "text": "已经", "type": "normal", "role": "Phó từ hoàn thành" },
            { "text": "准备", "type": "core", "role": "Động từ chính (chuẩn bị)" },
            { "text": "好", "type": "grammar", "role": "Bổ ngữ kết quả (chu tất/hoàn tất)" },
            { "text": "了", "type": "normal", "role": "Trợ từ biến hóa" },
            { "text": "吗", "type": "grammar", "role": "Trợ từ nghi vấn" }
        ],
        "grammar_point": {
            "name": "Câu hỏi phản vấn với 不是...吗 và Bổ ngữ kết quả 好",
            "pattern": "Chủ ngữ + 不是 + 已经 + Động từ + 好 + 了吗？",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY NGỮ PHÁP: '准备好' có '好' là bổ ngữ kết quả chỉ sự việc đã sẵn sàng trọn vẹn. Cấu trúc '不是...了吗' nhấn mạnh việc người nói đinh ninh đối phương đã hoàn tất việc đó.",
            "explanation": "Câu hỏi bày tỏ sự ngạc nhiên khi thấy mọi người dường như vẫn còn đang bối rối hoặc chưa sẵn sàng xuất phát."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你们", "type": "subject", "desc": "Các bạn" },
            { "role": "Khung câu phản vấn", "text": "不是...吗", "type": "grammar", "desc": "Khẳng định điều hiển nhiên" },
            { "role": "Hành động đã sẵn sàng", "text": "已经准备好了", "type": "verb", "desc": "Đã thu xếp tươm tất mọi thứ" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["准备好了吗", "已经", "你们", "不是"],
            "target_chunks": ["你们", "不是", "已经", "准备好了吗"],
            "hint": "Cấu trúc phản vấn: 你们 + 不是 + 已经 + 准备好了吗？"
        }
    },
    {
        "id": "hsk4_test8_q95",
        "category": "sentence_building",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 书写 第一部分 (第95题)",
        "zh": "学校给我们提供了很好的条件。",
        "pinyin": "xué xiào gěi wǒ men tí gōng le hěn hǎo de tiáo jiàn 。",
        "hanviet": "Học Hiệu Cấp Ngã Môn Đề Cung Liễu Hẩn Hảo Đích Điều Kiện 。",
        "meaning": "Nhà trường đã tạo điều kiện rất tốt cho chúng tôi.",
        "tokens": [
            { "text": "学校", "type": "core", "role": "Chủ ngữ (nhà trường)" },
            { "text": "给", "type": "grammar", "role": "Giới từ chỉ đối tượng thụ hưởng (cho)" },
            { "text": "我们", "type": "normal", "role": "Tân ngữ giới từ" },
            { "text": "提供", "type": "core", "role": "Động từ chính (cung cấp, tạo ra)" },
            { "text": "了", "type": "normal", "role": "Trợ từ động thái hoàn thành" },
            { "text": "很好的", "type": "normal", "role": "Định ngữ" },
            { "text": "条件", "type": "core", "role": "Tân ngữ trực tiếp (điều kiện, cơ sở vật chất)" }
        ],
        "grammar_point": {
            "name": "Cụm giới từ 给 chỉ đối tượng hưởng lợi: 给 + Người + 提供 + Điều kiện / Cơ hội",
            "pattern": "Chủ ngữ + 给 + Đối tượng + 提供 + (了) + Tân ngữ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Cụm giới từ '给 + Chúng tôi' bắt buộc phải đứng TRƯỚC động từ '提供'. Không được nói '提供给我们' khi phía sau còn tân ngữ dài.",
            "explanation": "Cặp từ phối hợp vàng trong HSK 4: 提供条件 (tạo điều kiện), 提供帮助 (cung cấp sự giúp đỡ), 提供机会 (mang lại cơ hội)."
        },
        "breakdown": [
            { "role": "Chủ thể mang lại phúc lợi", "text": "学校", "type": "subject", "desc": "Cơ sở giáo dục" },
            { "role": "Trạng ngữ hướng đối tượng", "text": "给我们", "type": "modifier", "desc": "Giới từ '给' hướng về sinh viên" },
            { "role": "Vị ngữ động từ", "text": "提供了", "type": "verb", "desc": "Hành vi đáp ứng, hỗ trợ" },
            { "role": "Tân ngữ trực tiếp", "text": "很好的条件", "type": "object", "desc": "Môi trường học tập và sinh hoạt chất lượng cao" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["很好的条件", "学校", "提供了", "给我们"],
            "target_chunks": ["学校", "给我们", "提供了", "很好的条件"],
            "hint": "Cấu trúc: 学校 + 给我们 + 提供了 + 很好的条件."
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Logic 56-65)
    # =========================================================================
    {
        "id": "hsk4_test8_q56",
        "category": "sentence_logic",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 阅读 第二部分 (第56题)",
        "zh": "她从小就想成为一名歌手，经过不断的努力，最后她终于考上了音乐学院。",
        "pinyin": "tā cóng xiǎo jiù xiǎng chéng wéi yì míng gē shǒu ， jīng guò bú duàn de nǔ lì ， zuì hòu tā zhōng yú kǎo shàng le yīn yuè xué yuàn 。",
        "hanviet": "Tha Tùng Tiểu Tựu Tưởng Thành Vi Nhất Danh Ca Thủ ， Kinh Quá Bất Đoán Đích Nỗ Lực ， Tối Hậu Tha Chung Vu Khảo Thượng Liễu Âm Nhạc Học Viện 。",
        "meaning": "Từ nhỏ cô ấy đã ước ao trở thành một ca sĩ, trải qua những nỗ lực không ngừng nghỉ, cuối cùng cô ấy cũng đã thi đỗ vào học viện âm nhạc.",
        "tokens": [
            { "text": "她从小就想成为一名歌手", "type": "core", "role": "Ước mơ thời thơ ấu (A)" },
            { "text": "经过不断的努力", "type": "core", "role": "Quá trình kiên trì phấn đấu (C)" },
            { "text": "最后", "type": "grammar", "role": "Thời điểm kết cuộc" },
            { "text": "她终于考上了音乐学院", "type": "core", "role": "Hiện thực hóa giấc mơ với 终于 (B)" }
        ],
        "grammar_point": {
            "name": "Mạch thời gian tự sự: Ước mơ thuở nhỏ (A) -> Quá trình nỗ lực (C) -> Kết quả đạt được (B)",
            "pattern": "Chủ đề thời thơ ấu (从小) + Quá trình (经过...努力) + Kết quả (最后...终于...)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: '从小' (từ nhỏ) giới thiệu xuất phát điểm mơ ước nên câu A luôn đứng đầu. Cụm '经过不断的努力' (C) là bước đệm cần thiết trước khi dẫn tới thành quả '最后她终于考上了音乐学院' (B).",
            "explanation": "Trình tự nhân quả theo trục thời gian hoàn hảo: Khát vọng -> Rèn luyện nỗ lực -> Đạt được mục tiêu."
        },
        "breakdown": [
            { "role": "Khởi đầu ước mơ (A)", "text": "她从小就想成为一名歌手", "type": "subject", "desc": "Giới thiệu nhân vật và lý tưởng ban đầu" },
            { "role": "Giai đoạn phấn đấu (C)", "text": "经过不断的努力", "type": "verb", "desc": "Hành trình nỗ lực bền bỉ theo thời gian" },
            { "role": "Gặt hái thành công (B)", "text": "最后她终于考上了音乐学院", "type": "object", "desc": "Dùng '最后' và '终于' chốt lại thắng lợi" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "她从小就想成为一名歌手" },
                { "id": "B", "text": "最后她终于考上了音乐学院" },
                { "id": "C", "text": "经过不断的努力" }
            ],
            "correct_order": "ACB",
            "hint": "Ước mơ ban đầu '从小' (A) -> Nỗ lực '经过' (C) -> Thành quả '最后终于' (B)."
        }
    },
    {
        "id": "hsk4_test8_q60",
        "category": "sentence_logic",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 阅读 第二部分 (第60题)",
        "zh": "她学习成绩特别好，而且尊敬老师，爱护同学，所以连续三年被评为优秀学生。",
        "pinyin": "tā xué xí chéng jì tè bié hǎo ， ér qiě zūn jìng lǎo shī ， ài hù tóng xué ， suǒ yǐ lián xù sān nián bèi píng wéi yōu xiù xué sheng 。",
        "hanviet": "Tha Học Tập Thành Tích Đặc Biệt Hảo ， Nhi Thả Tôn Kính Lão Sư ， Ái Hộ Đồng Học ， Sở Dĩ Liên Tục Tam Niên Bị Bình Vi Ưu Tú Học Sanh 。",
        "meaning": "Thành tích học tập của cô ấy đặc biệt xuất sắc, hơn nữa lại kính trọng thầy cô, yêu quý bạn bè, vì vậy liên tục ba năm liền được bầu chọn là học sinh ưu tú.",
        "tokens": [
            { "text": "她学习成绩特别好", "type": "core", "role": "Ưu điểm cốt lõi thứ nhất (B)" },
            { "text": "而且", "type": "grammar", "role": "Liên từ tăng tiến phẩm chất (hơn nữa)" },
            { "text": "尊敬老师，爱护同学", "type": "core", "role": "Phẩm chất đạo đức thứ hai (C)" },
            { "text": "所以", "type": "grammar", "role": "Liên từ kết quả" },
            { "text": "连续三年被评为优秀学生", "type": "core", "role": "Danh hiệu vinh danh đạt được (A)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc tăng tiến và kết quả: Ưu điểm 1 (B) + 而且 + Phẩm chất 2 (C) + 所以 + Hệ quả (A)",
            "pattern": "Đặc điểm tốt 1 + 而且 + Đặc điểm tốt 2 + 所以 + Vinh danh đạt được",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: '而且' (hơn nữa) bắt buộc phải đứng sau một ưu điểm đã nêu. '所以' (vì vậy) luôn đứng ở mệnh đề kết luận cuối cùng.",
            "explanation": "Câu B nêu học lực giỏi. Câu C tăng tiến về đạo đức tư cách. Câu A đưa ra danh hiệu thi đua xứng đáng bằng liên từ '所以'."
        },
        "breakdown": [
            { "role": "Năng lực học tập (B)", "text": "她学习成绩特别好", "type": "subject", "desc": "Giới thiệu nhân vật và kết quả học tập" },
            { "role": "Đạo đức lối sống (C)", "text": "而且尊敬老师，爱护同学", "type": "verb", "desc": "Dùng '而且' tăng tiến về thái độ với thầy cô, bạn bè" },
            { "role": "Phần thưởng danh dự (A)", "text": "所以连续三年被评为优秀学生", "type": "object", "desc": "Dùng '所以' chốt lại danh hiệu học sinh giỏi toàn diện" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "所以连续三年被评为优秀学生" },
                { "id": "B", "text": "她学习成绩特别好" },
                { "id": "C", "text": "而且尊敬老师，爱护同学" }
            ],
            "correct_order": "BCA",
            "hint": "Điểm tốt 1 (B) -> Tăng tiến '而且' (C) -> Kết luận '所以' (A)."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test 46-55)
    # =========================================================================
    {
        "id": "hsk4_test8_q51",
        "category": "cloze",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 阅读 第一部分 (第51题)",
        "zh": "对女人来说，是事业重要还是家庭重要呢？",
        "pinyin": "duì nǚ rén lái shuō ， shì shì yè zhòng yào hái shì jiā tíng zhòng yào ne ？",
        "hanviet": "Đối Nữ Nhân Lai Thuyết ， Thị Sự Nghiệp Trọng Yếu Hoàn Thị Gia Đình Trọng Yếu Nê ？",
        "meaning": "Đối với phụ nữ mà nói, là sự nghiệp quan trọng hay là gia đình quan trọng hơn?",
        "tokens": [
            { "text": "对", "type": "grammar", "role": "Giới từ chỉ góc nhìn quan điểm (đối với)" },
            { "text": "女人", "type": "normal", "role": "Đối tượng" },
            { "text": "来说", "type": "grammar", "role": "Từ kết hợp chỉ góc độ nhìn nhận (mà nói)" },
            { "text": "是", "type": "grammar", "role": "Liên từ câu hỏi lựa chọn" },
            { "text": "事业重要", "type": "core", "role": "Lựa chọn 1 (sự nghiệp)" },
            { "text": "还是", "type": "grammar", "role": "Liên từ nghi vấn (hay là)" },
            { "text": "家庭重要", "type": "core", "role": "Lựa chọn 2 (gia đình)" },
            { "text": "呢", "type": "grammar", "role": "Trợ từ ngữ khí" }
        ],
        "grammar_point": {
            "name": "Cấu trúc cố định nêu góc nhìn: 对...来说 (Đối với ai đó mà nói)",
            "pattern": "对 + Đối tượng + 来说 / 而言 ， Mệnh đề nhận định / câu hỏi",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ HƯ: Cụm cố định '对...来说' luôn đi chung với nhau ở đầu câu để định vị góc nhìn. Không được nhầm với '给...来说' hay '在...来说'.",
            "explanation": "Câu hỏi mở về sự cân bằng giữa sự nghiệp và tổ ấm gia đình của người phụ nữ thời hiện đại."
        },
        "breakdown": [
            { "role": "Góc nhìn đối tượng", "text": "对女人来说", "type": "modifier", "desc": "Cụm '对...来说' đứng đầu câu xác lập chủ đề" },
            { "role": "Câu hỏi lựa chọn hai vế", "text": "是事业重要还是家庭重要呢", "type": "verb", "desc": "Cấu trúc lựa chọn '是 A 还是 B'" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "（  ）女人来说，是事业重要还是家庭重要呢？",
            "options": ["对", "绝对", "目标", "单调", "幅"],
            "blank_index": 0,
            "correct_answer": "对",
            "hint": "Cấu trúc cố định đầu câu '（  ）...来说' (đối với... mà nói). Chọn '对'."
        }
    },
    {
        "id": "hsk4_test8_q52",
        "category": "cloze",
        "test_id": 8,
        "source": "HSK 4 模拟试卷 8 阅读 第一部分 (第52题)",
        "zh": "放心吧，绝对没问题。",
        "pinyin": "fàng xīn ba ， jué duì méi wèn tí 。",
        "hanviet": "Phóng Tâm Ba ， Tuyệt Đối Một Vấn Đề 。",
        "meaning": "Yên tâm đi, tuyệt đối không có vấn đề gì đâu.",
        "tokens": [
            { "text": "放心吧", "type": "normal", "role": "Lời trấn an" },
            { "text": "绝对", "type": "core", "role": "Phó từ khẳng định tuyệt đối (nhất định/chắc chắn 100%)" },
            { "text": "没问题", "type": "core", "role": "Không có vấn đề, hoàn toàn ổn" }
        ],
        "grammar_point": {
            "name": "Phó từ khẳng định chắc chắn 绝对 (Tuyệt đối / Chắc chắn 100%)",
            "pattern": "放心吧 / 主语 + 绝对 + (没问题 / 不会 / 能)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '绝对' đứng trước '没问题' là cụm khẩu ngữ cực kỳ thông dụng thể hiện sự đảm bảo tuyệt đối về chất lượng hoặc độ tin cậy.",
            "explanation": "Người nói dùng '绝对没问题' để xóa tan mọi nghi ngờ của người bạn về nhãn hiệu điện thoại mới."
        },
        "breakdown": [
            { "role": "Lời an ủi", "text": "放心吧", "type": "subject", "desc": "Xoa dịu sự lo lắng" },
            { "role": "Khẳng định tuyệt đối", "text": "绝对没问题", "type": "verb", "desc": "Phó từ '绝对' củng cố mức độ an toàn tối đa" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "放心吧，（  ）没问题。",
            "options": ["绝对", "对", "目标", "单调", "幅"],
            "blank_index": 0,
            "correct_answer": "绝对",
            "hint": "Cần một phó từ đứng trước '没问题' mang nghĩa 'tuyệt đối / chắc chắn 100%'. Chọn '绝对'."
        }
    }
]
