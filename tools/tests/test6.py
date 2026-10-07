# -*- coding: utf-8 -*-
"""
Authentic items curated from HSK 4 模拟试卷 6 (Mock Test 6).
Source: Tiengtrungthuonghai.vn_Mô phỏng đề thi HSK4 mới.pdf
"""

TEST6_ENTRIES = [
    # =========================================================================
    # PART A: 书写 第一部分 - 组句 (Sentence Building 86-95)
    # =========================================================================
    {
        "id": "hsk4_test6_q86",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第86题)",
        "zh": "他好不容易才赶上火车。",
        "pinyin": "tā hǎo bù róng yì cái gǎn shàng huǒ chē 。",
        "hanviet": "Tha Hảo Bất Dung Dịch Tài Cản Thượng Hỏa Xa 。",
        "meaning": "Khó khăn lắm anh ấy mới kịp chuyến tàu hỏa.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "好不容易", "type": "core", "role": "Cụm phó từ (khó khăn lắm mới...)" },
            { "text": "才", "type": "grammar", "role": "Phó từ nhấn mạnh sự việc diễn ra chật vật, muộn màng" },
            { "text": "赶上", "type": "core", "role": "Động từ mang bổ ngữ kết quả (đuổi kịp/bắt kịp)" },
            { "text": "火车", "type": "normal", "role": "Tân ngữ trực tiếp" }
        ],
        "grammar_point": {
            "name": "Cấu trúc phó từ nhấn mạnh: 好不容易 + 才 + Động từ",
            "pattern": "Chủ ngữ + 好不容易 + 才 + Động từ + Tân ngữ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: '好不容易' mang nghĩa khẳng định 'vô cùng khó khăn mới đạt được' (đồng nghĩa với '好容易'). Đi kèm với phó từ '才' đứng trước động từ để biểu thị sự trắc trở.",
            "explanation": "'赶上' có bổ ngữ kết quả '上' biểu thị tiếp cận kịp lúc phương tiện giao thông '火车'."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Hành khách đi tàu" },
            { "role": "Trạng ngữ mức độ khó khăn", "text": "好不容易才", "type": "modifier", "desc": "Nhấn mạnh quá trình vô cùng gian nan vất vả" },
            { "role": "Vị ngữ + Bổ ngữ", "text": "赶上", "type": "verb", "desc": "Kịp giờ bước lên toa" },
            { "role": "Tân ngữ", "text": "火车", "type": "object", "desc": "Phương tiện đường sắt" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["火车", "赶上", "才", "好不容易", "他"],
            "target_chunks": ["他", "好不容易", "才", "赶上", "火车"],
            "hint": "Cấu trúc: Chủ ngữ (他) + 好不容易 + 才 + Động từ (赶上) + 火车."
        }
    },
    {
        "id": "hsk4_test6_q87",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第87题)",
        "zh": "你是怎么来北京的？",
        "pinyin": "nǐ shì zěn me lái běi jīng de ？",
        "hanviet": "Nhĩ Thị Chẩm Ma Lai Bắc Kinh Đích ？",
        "meaning": "Bạn đến Bắc Kinh bằng cách nào thế?",
        "tokens": [
            { "text": "你", "type": "normal", "role": "Chủ ngữ" },
            { "text": "是", "type": "grammar", "role": "Thành phần mở đầu cấu trúc nhấn mạnh" },
            { "text": "怎么", "type": "core", "role": "Đại từ nghi vấn hỏi phương thức cách thức" },
            { "text": "来", "type": "normal", "role": "Động từ hành vi đã diễn ra" },
            { "text": "北京", "type": "normal", "role": "Địa điểm nơi chốn" },
            { "text": "的", "type": "grammar", "role": "Trợ từ kết thúc cấu trúc nhấn mạnh" }
        ],
        "grammar_point": {
            "name": "Cấu trúc nhấn mạnh phương thức/cách thức: 是...的",
            "pattern": "Chủ ngữ + 是 + 怎么 + Động từ + Tân ngữ + 的？",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: Cấu trúc '是...的' dùng cho sự việc ĐÃ XẢY RA trong quá khứ để nhấn mạnh chi tiết phương thức (bằng cách nào/phương tiện gì). '的' phải đứng ở cuối câu hoặc sau động từ.",
            "explanation": "Người nói và người nghe đều biết việc 'đến Bắc Kinh' đã hoàn thành, câu hỏi nhắm vào phương tiện hoặc lộ trình di chuyển."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "你", "type": "subject", "desc": "Người được hỏi" },
            { "role": "Cấu trúc nhấn mạnh", "text": "是...的", "type": "grammar", "desc": "Bao bọc thông tin trọng tâm cần làm rõ" },
            { "role": "Trọng tâm nghi vấn cách thức", "text": "怎么", "type": "modifier", "desc": "Hỏi phương tiện hoặc hình thức" },
            { "role": "Hành vi và địa điểm", "text": "来北京", "type": "verb", "desc": "Hành động di chuyển đến thủ đô" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["来", "的", "是怎么", "北京", "你"],
            "target_chunks": ["你", "是", "怎么", "来", "北京", "的"],
            "hint": "Cấu trúc nhấn mạnh: 你 + 是 + 怎么 + 来 + 北京 + 的？"
        }
    },
    {
        "id": "hsk4_test6_q88",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第88题)",
        "zh": "我这儿不能办理留学手续。",
        "pinyin": "wǒ zhèr bù néng bàn lǐ liú xué shǒu xù 。",
        "hanviet": "Ngã Giá Nhi Bất Năng Biện Lý Lưu Học Thủ Tục 。",
        "meaning": "Chỗ tôi không thể làm thủ tục du học được.",
        "tokens": [
            { "text": "我这儿", "type": "normal", "role": "Chủ ngữ nơi chốn (chỗ tôi/quầy của tôi)" },
            { "text": "不能", "type": "grammar", "role": "Phủ định năng nguyện (không thể)" },
            { "text": "办理", "type": "core", "role": "Động từ chính (giải quyết/làm thủ tục)" },
            { "text": "留学", "type": "core", "role": "Định ngữ danh từ (du học)" },
            { "text": "手续", "type": "core", "role": "Tân ngữ trực tiếp (thủ tục, giấy tờ)" }
        ],
        "grammar_point": {
            "name": "Cụm danh từ nơi chốn làm chủ ngữ và Cụm động tân 办理手续",
            "pattern": "Đại từ + 这儿/那儿 + 不能 / 可以 + 办理 + Tân ngữ thủ tục",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ PHỐI HỢP: '办理' là động từ chuyên dùng đi với '手续' (办理手续 = làm thủ tục). '我这儿' làm chủ ngữ chỉ địa điểm văn phòng/bộ phận.",
            "explanation": "'留学手续' là cụm danh từ định-trung. '不能' đứng trước động từ để biểu thị giới hạn chức năng thẩm quyền."
        },
        "breakdown": [
            { "role": "Chủ ngữ địa điểm", "text": "我这儿", "type": "subject", "desc": "Vị trí quầy tiếp nhận" },
            { "role": "Phủ định năng nguyện", "text": "不能", "type": "grammar", "desc": "Không có chức năng thẩm quyền" },
            { "role": "Vị ngữ động từ", "text": "办理", "type": "verb", "desc": "Tiến hành giải quyết giấy tờ" },
            { "role": "Tân ngữ chuyên biệt", "text": "留学手续", "type": "object", "desc": "Các giấy tờ liên quan việc du học" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["办理", "我这儿", "留学手续", "不能"],
            "target_chunks": ["我这儿", "不能", "办理", "留学手续"],
            "hint": "Chủ ngữ địa điểm (我这儿) + 不能 + Động từ (办理) + Tân ngữ (留学手续)."
        }
    },
    {
        "id": "hsk4_test6_q89",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第89题)",
        "zh": "服务员对我们很热情。",
        "pinyin": "fú wù yuán duì wǒ men hěn rè qíng 。",
        "hanviet": "Phục Vụ Viên Đối Ngã Môn Hẩn Nhiệt Tình 。",
        "meaning": "Nhân viên phục vụ rất nhiệt tình với chúng tôi.",
        "tokens": [
            { "text": "服务员", "type": "core", "role": "Chủ ngữ" },
            { "text": "对", "type": "grammar", "role": "Giới từ chỉ đối tượng hướng tới" },
            { "text": "我们", "type": "normal", "role": "Tân ngữ của giới từ 对" },
            { "text": "很", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "热情", "type": "core", "role": "Tính từ vị ngữ (nhiệt tình, niềm nở)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc giới từ chỉ thái độ: 对 + Đối tượng + 很 + Tính từ",
            "pattern": "Chủ ngữ + 对 + Đối tượng + (很/非常) + 热情 / 友好 / 严格",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: Trong tiếng Trung, thái độ đối với ai luôn đặt cụm giới từ '对 + Đối tượng' TRƯỚC tính từ biểu thị thái độ. Không được nói '很热情对我们'.",
            "explanation": "'服务员' là người phát ra thái độ, '我们' là đối tượng tiếp nhận sự hiếu khách chu đáo đó."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "服务员", "type": "subject", "desc": "Nhân viên chăm sóc khách hàng" },
            { "role": "Trạng ngữ hướng đối tượng", "text": "对我们", "type": "modifier", "desc": "Giới từ '对' dẫn dắt người thụ hưởng thái độ" },
            { "role": "Vị ngữ tính từ", "text": "很热情", "type": "verb", "desc": "Thái độ niềm nở, chu đáo" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["很热情", "服务员", "对我们"],
            "target_chunks": ["服务员", "对我们", "很热情"],
            "hint": "Cấu trúc: Chủ ngữ (服务员) + 对 [我们] + 很热情."
        }
    },
    {
        "id": "hsk4_test6_q90",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第90题)",
        "zh": "为什么不去英国留学呢？",
        "pinyin": "wèi shén me bú qù yīng guó liú xué ne ？",
        "hanviet": "Vi Thập Ma Bất Khứ Anh Quốc Lưu Học Nê ？",
        "meaning": "Tại sao lại không đi Anh du học nhỉ?",
        "tokens": [
            { "text": "为什么", "type": "core", "role": "Đại từ nghi vấn hỏi lý do" },
            { "text": "不", "type": "grammar", "role": "Phó từ phủ định" },
            { "text": "去", "type": "normal", "role": "Động từ liên động 1" },
            { "text": "英国", "type": "normal", "role": "Địa danh quốc gia" },
            { "text": "留学", "type": "core", "role": "Động từ liên động 2 (mục đích)" },
            { "text": "呢", "type": "grammar", "role": "Trợ từ ngữ khí nghi vấn nhẹ nhàng" }
        ],
        "grammar_point": {
            "name": "Cấu trúc gợi ý, thắc mắc: 为什么不...呢？",
            "pattern": "为什么 + 不 + Động từ + (Tân ngữ) + 呢？",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY NGỮ DỤNG: Cấu trúc '为什么不...呢？' thường dùng như một lời khuyên hoặc gợi mở một khả năng tốt đẹp, chứ không đơn thuần chỉ là câu cật vấn lý do.",
            "explanation": "'为什么' đứng đầu câu làm trạng ngữ nghi vấn, '呢' đặt ở cuối câu tạo âm hưởng êm ái, gợi ý chân thành."
        },
        "breakdown": [
            { "role": "Trạng ngữ nghi vấn", "text": "为什么", "type": "modifier", "desc": "Hỏi căn nguyên hoặc khơi gợi đề xuất" },
            { "role": "Phủ định liên động", "text": "不去英国留学", "type": "verb", "desc": "Không đến nước Anh để học tập" },
            { "role": "Trợ từ ngữ khí", "text": "呢", "type": "grammar", "desc": "Giúp câu nói mang sắc thái thảo luận mềm mỏng" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["英国留学", "为什么", "不去", "呢"],
            "target_chunks": ["为什么", "不去", "英国留学", "呢"],
            "hint": "Cấu trúc gợi ý: 为什么 + 不去 + 英国留学 + 呢？"
        }
    },
    {
        "id": "hsk4_test6_q91",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第91题)",
        "zh": "请把通知写在黑板上。",
        "pinyin": "qǐng bǎ tōng zhī xiě zài hēi bǎn shang 。",
        "hanviet": "Thỉnh Bả Thông Tri Tả Tại Hắc Bản Thượng 。",
        "meaning": "Xin hãy viết bản thông báo lên trên bảng đen.",
        "tokens": [
            { "text": "请", "type": "normal", "role": "Từ lịch sự đề nghị" },
            { "text": "把", "type": "grammar", "role": "Giới từ câu chữ 把" },
            { "text": "通知", "type": "core", "role": "Tân ngữ chịu tác động (thông báo)" },
            { "text": "写", "type": "normal", "role": "Động từ chính (viết)" },
            { "text": "在", "type": "grammar", "role": "Bổ ngữ kết quả định vị nơi chốn" },
            { "text": "黑板上", "type": "core", "role": "Tân ngữ nơi chốn (trên bảng đen)" }
        ],
        "grammar_point": {
            "name": "Câu chữ 把 kết hợp Động từ có bổ ngữ kết quả 在: 把 + Vật + V + 在 + Nơi chốn",
            "pattern": "请 / Chủ ngữ + 把 + Đối tượng + 写 / 贴 / 挂 + 在 + Vị trí",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Động từ tạo ra văn bản hoặc dấu vết '写' kết hợp với '在' tạo thành cụm '写在', vị trí xuất hiện kết quả ('黑板上') bắt buộc đứng sau '在'.",
            "explanation": "Câu chữ 把 nhấn mạnh vị trí hiển thị mới của bản thông báo sau khi được viết ra là ở trên mặt bảng đen."
        },
        "breakdown": [
            { "role": "Lời thỉnh cầu", "text": "请", "type": "subject", "desc": "Lời nhờ vả trang trọng" },
            { "role": "Giới từ 把 + Đối tượng", "text": "把通知", "type": "object", "desc": "Nội dung văn bản thông tri" },
            { "role": "Vị ngữ + Giới từ định vị", "text": "写在", "type": "verb", "desc": "Hành vi viết lưu lại" },
            { "role": "Vị trí không gian", "text": "黑板上", "type": "object", "desc": "Bề mặt tấm bảng đen trong lớp học" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["写在", "黑板上", "请", "把通知"],
            "target_chunks": ["请", "把通知", "写在", "黑板上"],
            "hint": "Cấu trúc: 请 + 把通知 + 写在 + 黑板上."
        }
    },
    {
        "id": "hsk4_test6_q92",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第92题)",
        "zh": "他的态度很值得怀疑。",
        "pinyin": "tā de tài du hěn zhí de huái yí 。",
        "hanviet": "Tha Đích Thái Độ Hẩn Trị Đắc Hoài Nghi 。",
        "meaning": "Thái độ của anh ấy rất đáng nghi ngờ.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Đại từ nhân xưng" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "态度", "type": "core", "role": "Chủ ngữ danh từ (thái độ)" },
            { "text": "很", "type": "normal", "role": "Phó từ mức độ" },
            { "text": "值得", "type": "core", "role": "Động từ mang tính đánh giá (xứng đáng/đáng để)" },
            { "text": "怀疑", "type": "core", "role": "Động từ làm tân ngữ của 值得 (hoài nghi/nghi ngờ)" }
        ],
        "grammar_point": {
            "name": "Động từ 值得 (Đáng để / Bõ công) mang tân ngữ là động từ",
            "pattern": "Chủ ngữ + (很 / 不) + 值得 + Động từ (怀疑 / 学习 / 考虑 / 同情)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ LOẠI: '值得' là động từ năng lượng đặc biệt, phía sau nó có thể trực tiếp tiếp nhận một động từ khác ('怀疑', '学习') làm tân ngữ.",
            "explanation": "Câu biểu thị sự đánh giá về thái độ kỳ lạ của một người, cho rằng thái độ đó rất có vấn đề, đáng để đặt câu hỏi nghi vấn."
        },
        "breakdown": [
            { "role": "Chủ ngữ định-trung", "text": "他的态度", "type": "subject", "desc": "Cung cách biểu hiện của đối phương" },
            { "role": "Phó từ mức độ", "text": "很", "type": "modifier", "desc": "Mức độ đáng kể" },
            { "role": "Vị ngữ động từ", "text": "值得", "type": "verb", "desc": "Đáng giá, đáng để" },
            { "role": "Tân ngữ hành động", "text": "怀疑", "type": "object", "desc": "Nảy sinh mối ngờ vực" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["很", "值得怀疑", "他的", "态度"],
            "target_chunks": ["他的", "态度", "很", "值得怀疑"],
            "hint": "Chủ ngữ (他的态度) + Mức độ (很) + Động từ (值得怀疑)."
        }
    },
    {
        "id": "hsk4_test6_q93",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第93题)",
        "zh": "他正在写作业。",
        "pinyin": "tā zhèng zài xiě zuò yè 。",
        "hanviet": "Tha Chính Tại Tả Tác Nghiệp 。",
        "meaning": "Cậu ấy đang làm bài tập về nhà.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "正在", "type": "grammar", "role": "Phó từ tiếp diễn (đang)" },
            { "text": "写", "type": "normal", "role": "Động từ chính" },
            { "text": "作业", "type": "core", "role": "Tân ngữ (bài tập)" }
        ],
        "grammar_point": {
            "name": "Phó từ thời thái 正在 biểu thị hành động đang tiến hành",
            "pattern": "Chủ ngữ + 正在 / 正 / 在 + Động từ + (Tân ngữ) + (呢)",
            "level": "HSK 4 Căn bản",
            "trap_note": "BẪY THI: '正在' đứng ngay trước động từ vị ngữ để nhấn mạnh hành động diễn ra tại đúng thời điểm nói.",
            "explanation": "Cụm '写作业' là kết hợp động tân cố định diễn tả việc làm bài tập của học sinh."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Người đang học bài" },
            { "role": "Trạng ngữ tiếp diễn", "text": "正在", "type": "modifier", "desc": "Hành vi đang xảy ra tại chỗ" },
            { "role": "Vị ngữ động tân", "text": "写作业", "type": "verb", "desc": "Viết và hoàn thành bài tập" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["作业", "正在", "他", "写"],
            "target_chunks": ["他", "正在", "写", "作业"],
            "hint": "Chủ ngữ (他) + Phó từ tiếp diễn (正在) + Động từ (写) + Tân ngữ (作业)."
        }
    },
    {
        "id": "hsk4_test6_q94",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第94题)",
        "zh": "李经理的包被小偷拿走了。",
        "pinyin": "lǐ jīng lǐ de bāo bèi xiǎo tōu ná zǒu le 。",
        "hanviet": "Lý Kinh Lý Đích Bao Bị Tiểu Thâu Nã Tẩu Liễu 。",
        "meaning": "Túi xách của giám đốc Lý đã bị tên trộm lấy mất rồi.",
        "tokens": [
            { "text": "李经理", "type": "core", "role": "Định ngữ danh xưng" },
            { "text": "的", "type": "normal", "role": "Trợ từ kết cấu" },
            { "text": "包", "type": "core", "role": "Chủ ngữ chịu tác động (túi xách)" },
            { "text": "被", "type": "grammar", "role": "Giới từ câu bị động" },
            { "text": "小偷", "type": "core", "role": "Tác nhân gây ra hành động (kẻ trộm)" },
            { "text": "拿走", "type": "core", "role": "Động từ + bổ ngữ xu hướng (cầm đi, lấy mất)" },
            { "text": "了", "type": "normal", "role": "Trợ từ hoàn thành" }
        ],
        "grammar_point": {
            "name": "Câu bị động với giới từ 被: Đối tượng chịu tác động + 被 + Tác nhân + Động từ + Thành phần khác",
            "pattern": "Vật/Người chịu tác động + 被 + Kẻ thực hiện + Động từ + Bổ ngữ kết quả/xu hướng + 了",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Vật bị mất mát '李经理的包' phải đứng làm chủ ngữ ở đầu câu, sau đó đến '被 + Tác nhân (小偷)'. Động từ trong câu bị động bắt buộc phải có thành phần khác đi kèm (ở đây là bổ ngữ xu hướng '走' và trợ từ '了').",
            "explanation": "Câu bị động chữ 被 dùng để nhấn mạnh sự việc không may, tổn thất xảy ra đối với chiếc túi của giám đốc Lý."
        },
        "breakdown": [
            { "role": "Đối tượng chịu tác động (Chủ ngữ)", "text": "李经理的包", "type": "subject", "desc": "Tài sản bị kẻ xấu nhắm đến" },
            { "role": "Giới từ bị động + Tác nhân", "text": "被小偷", "type": "modifier", "desc": "Bị tên trộm ra tay" },
            { "role": "Vị ngữ + Bổ ngữ xu hướng", "text": "拿走了", "type": "verb", "desc": "Động từ '拿' đi kèm kết quả mang đi mất" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["被小偷", "李经理的包", "拿走了"],
            "target_chunks": ["李经理的包", "被小偷", "拿走了"],
            "hint": "Cấu trúc bị động: Đối tượng bị hại (李经理的包) + 被小偷 + 拿走了."
        }
    },
    {
        "id": "hsk4_test6_q95",
        "category": "sentence_building",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 书写 第一部分 (第95题)",
        "zh": "他从来没去过上海。",
        "pinyin": "tā cóng lái méi qù guo shàng hǎi 。",
        "hanviet": "Tha Tùng Lai Một Khứ Quá Thượng Hải 。",
        "meaning": "Từ trước đến nay anh ấy chưa từng đến Thượng Hải.",
        "tokens": [
            { "text": "他", "type": "normal", "role": "Chủ ngữ" },
            { "text": "从来", "type": "core", "role": "Phó từ thời gian (từ trước tới nay)" },
            { "text": "没", "type": "grammar", "role": "Phó từ phủ định kinh nghiệm" },
            { "text": "去", "type": "normal", "role": "Động từ" },
            { "text": "过", "type": "grammar", "role": "Trợ từ động thái chỉ kinh nghiệm trong quá khứ" },
            { "text": "上海", "type": "normal", "role": "Tân ngữ nơi chốn" }
        ],
        "grammar_point": {
            "name": "Cấu trúc phủ định kinh nghiệm: 从来 + 没 + Động từ + 过",
            "pattern": "Chủ ngữ + 从来 + 没 / 没有 + Động từ + 过 + Tân ngữ",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY THI: Khi phủ định sự từng trải nghiệm trong quá khứ, '从来' bắt buộc phải kết hợp với '没/没有...过', tuyệt đối KHÔNG được dùng '从来不...过'.",
            "explanation": "'从来没去过' nhấn mạnh suốt từ điểm khởi đầu trong quá khứ cho tới thời điểm hiện tại chưa từng có tiền lệ đặt chân tới Thượng Hải."
        },
        "breakdown": [
            { "role": "Chủ ngữ", "text": "他", "type": "subject", "desc": "Đối tượng chưa có trải nghiệm" },
            { "role": "Trạng ngữ phủ định kinh nghiệm", "text": "从来没", "type": "modifier", "desc": "Phó từ '从来' kết hợp phủ định '没'" },
            { "role": "Vị ngữ động từ + Trợ từ kinh nghiệm", "text": "去过", "type": "verb", "desc": "Hành vi đi và trải nghiệm" },
            { "role": "Tân ngữ nơi chốn", "text": "上海", "type": "object", "desc": "Thành phố chưa từng ghé thăm" }
        ],
        "practice": {
            "type": "sentence_building",
            "scrambled_chunks": ["上海", "没去过", "他", "从来"],
            "target_chunks": ["他", "从来", "没去过", "上海"],
            "hint": "Cấu trúc kinh nghiệm phủ định: Chủ ngữ (他) + 从来 + 没去过 + 上海."
        }
    },

    # =========================================================================
    # PART B: 阅读 第二部分 - 排列顺序 (Sentence Logic 56-65)
    # =========================================================================
    {
        "id": "hsk4_test6_q56",
        "category": "sentence_logic",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 阅读 第二部分 (第56题)",
        "zh": "为了身体健康，我天天坚持跑步，所以我现在觉得很精神。",
        "pinyin": "wèi le shēn tǐ jiàn kāng ， wǒ tiān tiān jiān chí pǎo bù ， suǒ yǐ wǒ xiàn zài jué de hěn jīng shen 。",
        "hanviet": "Vị Liễu Thân Thể Kiện Khang ， Ngã Thiên Thiên Kiên Trì Bào Bộ ， Sở Dĩ Ngã Hiện Tại Giác Đắc Hẩn Tinh Thần 。",
        "meaning": "Vì sức khỏe của bản thân, ngày nào tôi cũng kiên trì chạy bộ, cho nên hiện tại tôi cảm thấy rất sảng khoái và tràn đầy năng lượng.",
        "tokens": [
            { "text": "为了身体健康", "type": "core", "role": "Trạng ngữ mục đích (B)" },
            { "text": "我天天坚持跑步", "type": "core", "role": "Hành động thực hiện đều đặn (C)" },
            { "text": "所以", "type": "grammar", "role": "Liên từ kết quả" },
            { "text": "我现在觉得很精神", "type": "normal", "role": "Hệ quả tích cực thể chất và tinh thần (A)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc mục đích - hành động - hệ quả: 为了... + Hành động + 所以...",
            "pattern": "为了 + Mục đích (B) + Chủ ngữ + Hành động kiên trì (C) + 所以 + Kết quả đạt được (A)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Cụm chỉ mục đích '为了...' luôn đứng ở vị trí mở đầu câu. '所以' dẫn dắt kết quả đạt được từ hành động đó đứng ở cuối.",
            "explanation": "B đặt mục tiêu vì thể chất. C miêu tả thói quen tập luyện hàng ngày. A chốt lại cảm giác tỉnh táo, khỏe khoắn với liên từ '所以'."
        },
        "breakdown": [
            { "role": "Mục đích mở đầu (B)", "text": "为了身体健康", "type": "modifier", "desc": "Xác định mục tiêu hướng đến sức khỏe" },
            { "role": "Hành động rèn luyện (C)", "text": "我天天坚持跑步", "type": "verb", "desc": "Kiên trì chạy bộ mỗi ngày" },
            { "role": "Kết quả chuyển biến (A)", "text": "所以我现在觉得很精神", "type": "object", "desc": "Thể trạng và tinh thần dồi dào sức sống" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "所以我现在觉得很精神" },
                { "id": "B", "text": "为了身体健康" },
                { "id": "C", "text": "我天天坚持跑步" }
            ],
            "correct_order": "BCA",
            "hint": "Mục đích '为了' (B) -> Hành động chạy bộ (C) -> Kết quả '所以' (A)."
        }
    },
    {
        "id": "hsk4_test6_q58",
        "category": "sentence_logic",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 阅读 第二部分 (第58题)",
        "zh": "无论是国家领导，还是普通老百姓，都应该按照规章办事。",
        "pinyin": "wú lùn shì guó jiā lǐng dǎo ， hái shì pǔ tōng lǎo bǎi xìng ， dōu yīng gāi àn zhào guī zhāng bàn shì 。",
        "hanviet": "Vô Luận Thị Quốc Gia Lãnh Đạo ， Hoàn Thị Phổ Thông Lão Bách Tính ， Đô Ưng Cai Án Chiếu Quy Chương Biện Sự 。",
        "meaning": "Bất kể là lãnh đạo đất nước, hay là người dân bách tính bình thường, đều nên làm việc theo đúng quy định kỷ cương.",
        "tokens": [
            { "text": "无论是", "type": "grammar", "role": "Cặp liên từ biểu thị điều kiện vô điều kiện (bất kể là)" },
            { "text": "国家领导", "type": "core", "role": "Đối tượng 1 cấp cao (A)" },
            { "text": "还是", "type": "grammar", "role": "Liên từ liệt kê lựa chọn (hay là)" },
            { "text": "普通老百姓", "type": "core", "role": "Đối tượng 2 bình dân (C)" },
            { "text": "都应该", "type": "grammar", "role": "Phó từ khái quát toàn thể (đều nên)" },
            { "text": "按照规章办事", "type": "core", "role": "Quy tắc áp dụng chung (B)" }
        ],
        "grammar_point": {
            "name": "Cấu trúc liên từ đẳng lập: 无论...还是...都...",
            "pattern": "无论(是) + A + 还是 + B + 都 + Vị ngữ hành động",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LOGIC: Cặp liên từ '无论...还是...都...' có trật tự cố định không thể đảo ngược: 无论是 [A] (câu A) -> 还是 [B] (câu C) -> 都 [V] (câu B).",
            "explanation": "Câu diễn tả tính bình đẳng trước pháp luật kỷ cương. Dù ở địa vị cao như lãnh đạo hay thường dân thì đều phải tuân thủ quy tắc."
        },
        "breakdown": [
            { "role": "Phạm vi thứ nhất (A)", "text": "无论是国家领导", "type": "subject", "desc": "Mở đầu cấu trúc với '无论是' và đối tượng thứ nhất" },
            { "role": "Phạm vi thứ hai (C)", "text": "还是普通老百姓", "type": "modifier", "desc": "Liên từ '还是' nối tiếp đối tượng đối trọng" },
            { "role": "Nguyên tắc chung quy về một mối (B)", "text": "都应该按照规章办事", "type": "verb", "desc": "Phó từ '都' chốt lại chuẩn mực hành xử chung" }
        ],
        "practice": {
            "type": "sentence_logic",
            "options": [
                { "id": "A", "text": "无论是国家领导" },
                { "id": "B", "text": "都应该按照规章办事" },
                { "id": "C", "text": "还是普通老百姓" }
            ],
            "correct_order": "ACB",
            "hint": "Cặp liên từ: 无论(是) A (A) -> 还是 B (C) -> 都... (B)."
        }
    },

    # =========================================================================
    # PART C: 阅读 第一部分 - 选词填空 (Cloze Test 46-55)
    # =========================================================================
    {
        "id": "hsk4_test6_q51",
        "category": "cloze",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 阅读 第一部分 (第51题)",
        "zh": "除非打折，否则我不会考虑的。",
        "pinyin": "chú fēi dǎ zhé ， fǒu zé wǒ bú huì kǎo lǜ de 。",
        "hanviet": "Trừ Phi Đả Chiết ， Phủ Tắc Ngã Bất Hội Khảo Lự Đích 。",
        "meaning": "Trừ phi giảm giá, nếu không tôi sẽ không cân nhắc mua đâu.",
        "tokens": [
            { "text": "除非", "type": "grammar", "role": "Liên từ điều kiện duy nhất (trừ phi)" },
            { "text": "打折", "type": "core", "role": "Giảm giá, chiết khấu" },
            { "text": "否则", "type": "grammar", "role": "Liên từ hệ quả nghịch đảo (nếu không thì)" },
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "不会", "type": "normal", "role": "Sẽ không" },
            { "text": "考虑", "type": "core", "role": "Động từ (cân nhắc)" },
            { "text": "的", "type": "normal", "role": "Trợ từ ngữ khí" }
        ],
        "grammar_point": {
            "name": "Cặp liên từ điều kiện duy nhất: 除非...否则...",
            "pattern": "除非 + Điều kiện độc nhất + 否则 / 不然 + Hệ quả ngược lại",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY LIÊN TỪ: '除非' chỉ điều kiện bắt buộc duy nhất phải thỏa mãn. Đi cặp với nó ở phân câu sau là '否则' (nếu không thì).",
            "explanation": "Người nói kiên quyết chỉ mua bộ ấm chén nếu có chương trình hạ giá, bất kỳ tình huống nào khác cũng sẽ từ chối."
        },
        "breakdown": [
            { "role": "Điều kiện cần thiết duy nhất", "text": "除非打折", "type": "modifier", "desc": "Giới hạn mua sắm ở mức có giảm giá" },
            { "role": "Liên từ loại trừ", "text": "否则", "type": "grammar", "desc": "Biểu thị tình huống trái với điều kiện trên" },
            { "role": "Thái độ quyết định", "text": "我不会考虑的", "type": "verb", "desc": "Từ chối thẳng thừng" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "（  ）打折，否则我不会考虑的。",
            "options": ["除非", "任何", "吵架", "安排", "忍不住"],
            "blank_index": 0,
            "correct_answer": "除非",
            "hint": "Cặp liên từ đi với '否则' ở vế sau là '除非...否则...' (trừ phi... nếu không)."
        }
    },
    {
        "id": "hsk4_test6_q52",
        "category": "cloze",
        "test_id": 6,
        "source": "HSK 4 模拟试卷 6 阅读 第一部分 (第52题)",
        "zh": "我们同学聚会，大家玩儿得高兴，我忍不住多喝了几杯。",
        "pinyin": "wǒ men tóng xué jù huì ， dà jiā wánr de gāo xìng ， wǒ rěn bu zhù duō hē le jǐ bēi 。",
        "hanviet": "Ngã Môn Đồng Học Tụ Hội ， Đại Gia Ngoạn Nhi Đắc Cao Hứng ， Ngã Nhẫn Bất Trụ Đa Hát Liễu Kỷ Bôi 。",
        "meaning": "Lớp chúng tôi họp lớp, mọi người chơi vui quá nên tôi không kìm được đã uống thêm vài ly.",
        "tokens": [
            { "text": "同学聚会", "type": "core", "role": "Họp mặt bạn bè cùng lớp" },
            { "text": "大家", "type": "normal", "role": "Mọi người" },
            { "text": "玩儿得高兴", "type": "normal", "role": "Vui chơi hào hứng" },
            { "text": "我", "type": "normal", "role": "Chủ ngữ" },
            { "text": "忍不住", "type": "grammar", "role": "Động từ mang bổ ngữ khả năng phủ định (không kìm được, không nén nổi)" },
            { "text": "多喝了", "type": "core", "role": "Uống nhiều thêm" },
            { "text": "几杯", "type": "normal", "role": "Vài ly rượu" }
        ],
        "grammar_point": {
            "name": "Bổ ngữ khả năng cố định 忍不住 (Không kìm nén nổi / Không nhịn được)",
            "pattern": "Chủ ngữ + 忍不住 + (想 / Động từ hành vi bộc phát)",
            "level": "HSK 4 Trọng điểm",
            "trap_note": "BẪY TỪ VỰNG: '忍不住' biểu thị cảm xúc hoặc hành động trào dâng mà ý chí không thể kiểm soát được (như 忍不住笑了, 忍不住哭了, 忍不住多喝了几杯). Trái nghĩa là '忍得住'.",
            "explanation": "Trong không khí sôi động của buổi họp lớp, người nói vì quá cao hứng nên không thể tự chủ được tửu lượng."
        },
        "breakdown": [
            { "role": "Bối cảnh họp lớp", "text": "我们同学聚会，大家玩儿得高兴", "type": "subject", "desc": "Không khí tụ tập bạn bè phấn chấn" },
            { "role": "Trạng thái mất kiểm soát cảm xúc", "text": "我忍不住", "type": "grammar", "desc": "Không thể ngăn lại được thôi thúc" },
            { "role": "Hành vi bộc phát quá đà", "text": "多喝了几杯", "type": "verb", "desc": "Uống vượt quá mức bình thường" }
        ],
        "practice": {
            "type": "cloze",
            "cloze_text": "我们同学聚会，大家玩儿得高兴，我（  ）多喝了几杯。",
            "options": ["忍不住", "除非", "任何", "吵架", "安排"],
            "blank_index": 0,
            "correct_answer": "忍不住",
            "hint": "Cần một từ diễn tả việc 'không kìm chế được' dẫn tới uống nhiều rượu. Chọn '忍不住'."
        }
    }
]
