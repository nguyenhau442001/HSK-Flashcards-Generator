"""
tools/story_data/hsk7_data.py
10 stories data for HSK 7
"""

HSK7_STORIES = [
    (1, "宏观调控与经济高质量发展", "Điều tiết vĩ mô và phát triển kinh tế chất lượng cao", "macroeconomics", "Kinh tế học vĩ mô", "📊", 6,
     "Phân tích các chính sách tài khóa và tiền tệ nhằm tối ưu hóa cơ cấu kinh tế và phát triển bền vững.",
     [
         ("面对错综复杂的国际经济环境，科学合理的宏观调控是维持国民经济平稳运行的定海神针。", "Miànduì cuòzōng-fùzá de guójì jīngjì huánjìng, kēxué hélǐ de hóngguān tiáokòng shì wéichí guómín jīngjì píngwěn yùnxíng de dìnghǎi-shénzhēn.", "Đối diện môi trường kinh tế quốc tế đan xen phức tạp, điều tiết vĩ mô khoa học và hợp lý là chiếc kim chỉ nam duy trì vận hành ổn định của nền kinh tế quốc dân."),
         ("积极的财政政策与稳健的货币政策相互协同，精准支持实体经济和科技创新企业的研发投入。", "Jījí de cáizhèng zhèngcè yǔ wěnjiàn de huòbì zhèngcè xiānghù xiétóng, jīngzhǔn zhīchí shítǐ jīngjì hé kējì chuàngxīn qǐyè de yánfā tóurù.", "Chính sách tài khóa tích cực cùng chính sách tiền tệ thận trọng phối hợp nhịp nhàng, hỗ trợ chuẩn xác cho kinh tế thực thể và đầu tư nghiên cứu của doanh nghiệp đổi mới công nghệ."),
         ("深化供给侧结构性改革，旨在淘汰落后产能并培育具有核心竞争力的战略性新兴产业。", "Shēnhuà gōngjǐcè jiégòuxìng gǎigé, zhǐzài táotài luòhòu chǎnnéng bìng péiyù jùyǒu héxīn jìngzhēnglì de zhànlüèxìng xīnxīng chǎnyè.", "Làm sâu sắc cải cách cơ cấu phía cung nhằm loại bỏ năng lực sản xuất lạc hậu và ươm mầm các ngành công nghiệp mới nổi có tính chiến lược và sức cạnh tranh cốt lõi."),
         ("激发民营经济活力与优化营商环境，是推动经济高质量增长与扩大就业容量的重要引擎。", "Jīfā mínyíng jīngjì huólì yǔ yōuhuà yíngshāng huánjìng, shì tuīdòng jīngjì gāozhìliàng zēngzhǎng yǔ kuòdà jiùyè róngliàng de zhòngyào yǐnqíng.", "Khơi dậy sức sống kinh tế tư nhân và tối ưu hóa môi trường kinh doanh là động cơ trọng yếu thúc đẩy tăng trưởng chất lượng cao và mở rộng giải quyết việc làm."),
         ("统筹发展与安全两件大事，才能确保国家经济在风浪考验中始终保持充足的韧性与后劲。", "Tǒngchóu fāzhǎn yǔ ānquán liǎng jiàn dàshì, cái néng quèbǎo guójiā jīngjì zài fēnglàng kǎoyàn zhōng shǐzhōng bǎochí chōngzú de rènxìng yǔ hòujìn.", "Quy hoạch đồng bộ hai việc lớn là phát triển và an ninh mới có thể bảo đảm nền kinh tế quốc gia giữ vững sự dẻo dai và đà tiến trước mọi sóng gió.")
     ],
     [
         ("Vai trò của việc kết hợp chính sách tài khóa và tiền tệ là gì?", ["Chỉ tập trung vào đầu cơ bất động sản", "Hỗ trợ chuẩn xác kinh tế thực thể và nghiên cứu công nghệ", "In thêm thật nhiều tiền"], 1, "Trong bài có câu: 精准支持实体经济和科技创新企业的研发投入."),
         ("Mục tiêu chính của cải cách cơ cấu phía cung là gì?", ["Giữ nguyên các nhà máy ô nhiễm", "Loại bỏ năng lực lạc hậu, bồi dưỡng ngành mới nổi chiến lược", "Giảm tiền lương người lao động"], 1, "Trong câu có viết: 淘汰落后产能并培育具有核心竞争力的战略性新兴产业."),
         ("Yếu tố then chốt giúp nền kinh tế giữ vững sự dẻo dai trước thử thách là gì?", ["Chỉ chú trọng tăng trưởng nóng", "Quy hoạch thống nhất giữa phát triển và an ninh", "Đóng cửa biên giới"], 1, "Trong câu cuối có viết: 统筹发展与安全两件大事，才能确保经济保持充足的韧性与后劲.")
     ]),
    (2, "中华古籍的数字化活化", "Số hóa và hồi sinh cổ tịch văn hiến", "ancient_texts", "Di sản văn hiến", "📜", 7,
     "Ứng dụng công nghệ quét quang học siêu nét và AI để phục dựng và lưu trữ kho tàng văn tự cổ ngàn năm.",
     [
         ("浩瀚的中华古代文献典籍，是中华民族数千年灿烂文明与哲学思辨的历史见证。", "Hàohàn de zhōnghuá gǔdài wénxiàn diǎnjí, shì zhōnghuá mínzú shù qiān nián cànlàn wénmíng yǔ zhéxué sībiàn de lìshǐ jiànzhèng.", "Kho tàng thư tịch văn hiến cổ đại mênh mông là minh chứng lịch sử cho nền văn minh rực rỡ và tư duy triết học ngàn năm của dân tộc."),
         ("然而，古籍善本普遍面临纸张老化脆化、虫蛀霉变等自然损坏的严重威胁。", "Rán'ér, gǔjí shànběn pǔbiàn miànlín zhǐzhāng lǎohuà cuìhuà, chóngzhù méibiàn děng zìrán sǔnhuài de yánzhòng wēixié.", "Dẫu vậy, các bản sách cổ quý hiếm thường đối mặt với nguy cơ hư hại tự nhiên nghiêm trọng như giòn rách ố vàng, mối mọt nấm mốc."),
         ("高精度扫描与数字图像修复技术的应用，使得残破残卷在计算机虚拟世界中重现原本风貌。", "Gāo jīngdù sǎomiáo yǔ shùzì túxiàng xiūfù jìshù de yìngyòng, shǐde cánpò cánjuàn zài jìsuànjī xūnǐ shìjiè zhōng chóngxiàn yuánběn fēngmào.", "Ứng dụng quét quang học độ phân giải cao và phục chế hình ảnh kỹ thuật số giúp những trang sách rách nát tái hiện diện mạo nguyên bản trong thế giới ảo."),
         ("借助自然语言处理与知识图谱，学者们可以跨越语料障碍，高效检索与深度挖掘古典智慧。", "Jièzhù zìrán yǔyán chǔlǐ yǔ zhīshi túpǔ, xuézhě men kěyǐ kuàyuè yǔliào zhàng'ài, gāoxiào jiǎnsuǒ yǔ shēndù wājué gǔdiǎn zhìhuì.", "Nhờ xử lý ngôn ngữ tự nhiên và đồ thị tri thức, các học giả có thể vượt qua rào cản ngữ liệu để tra cứu thần tốc và đào sâu trí tuệ cổ điển."),
         ("数字技术的赋能不仅让沉睡的古籍焕发新生，更为全人类共享经典文明开启了宽广的大门。", "Shùzì jìshù de fùnéng bùjǐn ràng chénshuì de gǔjí huànfā xīnshēng, gèng wèi quán rénlèi gòngxiǎng jīngdiǎn wénmíng kāiqǐ le kuānguǎng de dàmén.", "Sự trao quyền của công nghệ số không chỉ giúp cổ tịch ngủ yên hồi sinh mà còn mở rộng cánh cửa chia sẻ văn minh kinh điển cho toàn nhân loại.")
     ],
     [
         ("Sách cổ quý hiếm thường gặp phải nguy cơ tự nhiên nào?", ["Lão hóa giòn rách, mối mọt và nấm mốc", "Bị đánh cắp hết trong một ngày", "Không ai muốn in lại"], 0, "Trong bài có câu: 普遍面临纸张老化脆化、虫蛀霉变等自然损坏的严重威胁."),
         ("Công nghệ nào giúp học giả tra cứu và khai phá trí tuệ cổ điển hiệu quả?", ["Xử lý ngôn ngữ tự nhiên và đồ thị tri thức", "Chép tay thủ công", "Dùng kính lúp soi từng chữ"], 0, "Trong câu có viết: 借助自然语言处理与知识图谱，高效检索与深度挖掘古典智慧."),
         ("Ý nghĩa lớn lao của việc số hóa cổ tịch là gì?", ["Để cất giấu không cho ai xem", "Hồi sinh cổ tịch và mở rộng chia sẻ văn minh cho nhân loại", "Để bán đấu giá lấy tiền"], 1, "Trong câu cuối có viết: 不仅让沉睡的古籍焕发新生，更为全人类共享经典文明开启了大门.")
     ]),
    (3, "量子信息与计算新时代", "Thông tin lượng tử và kỷ nguyên tính toán mới", "quantum_frontier", "Khoa học tiên phong", "🔬", 7,
     "Khám phá nguyên lý chồng chập và vướng víu lượng tử: Bước nhảy vọt về sức mạnh tính toán và mã hóa an toàn.",
     [
         ("量子力学作为现代物理学的核心基石之一，正在掀起第二次信息科技革命的汹涌浪潮。", "Liàngzǐ lìxué zuòwéi xiàndài wùlǐxué de héxīn jīshí zhī yī, zhèngzài xiānqǐ dì-èr cì xìnxī kējì gégmìng de xiōngyǒng làngcháo.", "Cơ học lượng tử với tư cách là một trong những nền tảng của vật lý hiện đại đang dấy lên làn sóng cuộn trào của cuộc cách mạng công nghệ thông tin lần thứ hai."),
         ("利用量子叠加与纠缠等微观物理特性，量子计算机能够展现出超越传统超级计算机的指数级算力。", "Lìyòng liàngzǐ diéjiā yǔ jiūchán děng wēiguān wùlǐ tèxìng, liàngzǐ jìsuànjī nénggòu zhǎnxiàn chū chāoyuè chuántǒng chāojí jìsuànjī de zhǐshùjí suànlì.", "Tận dụng các đặc tính vi mô như chồng chập và vướng víu lượng tử, máy tính lượng tử có thể thể hiện năng lực tính toán theo hàm mũ vượt xa siêu máy tính truyền thống."),
         ("在药物分子模拟、材料科学研发以及复杂气象预测等前沿领域，量子算力展现了无可估量的应用前景。", "Zài yàowù fēnzǐ mónǐ, cáiliào kēxué yánfā yǐjí fùzá qìxiàng yùcè děng qiányán lǐngyù, liàngzǐ suànlì zhǎnxiàn le wúkě-gūliàng de yìngyòng qiánjǐng.", "Trong các lĩnh vực tiền phong như mô phỏng phân tử thuốc, nghiên cứu vật liệu và dự báo khí tượng phức tạp, năng lực tính toán lượng tử bộc lộ triển vọng vô giá."),
         ("与此同时，基于量子密钥分发的保密通信网络，能够为国防和金融数据构筑无法破译的坚固盾牌。", "Yǔcǐ-tóngshí, jīyú liàngzǐ mìyào fēnfā de bǎomì tōngxìn wǎngluò, nénggòu wèi guófáng hé jīnróng shùjù gòuzhù wúfǎ pòyì de jiāngù dùnpái.", "Đồng thời, mạng lưới truyền thông bảo mật dựa trên phân phối khóa lượng tử có thể tạo nên lá chắn kiên cố không thể giải mã cho quốc phòng và tài chính."),
         ("攀登量子科技的科研高峰，将为人类探索未知宇宙和拓展认知边界提供强有力的底层支撑。", "Pāndēng liàngzǐ kējì de kēyán gāofēng, jiāng wèi rénlèi tànsuǒ wèizhī yǔzhòu hé tuòzhǎn rènzhī biānjiè tígōng qiángyǒulì de dǐcéng zhīchēng.", "Chinh phục đỉnh cao khoa học lượng tử sẽ đem lại bệ đỡ vững chắc cho nhân loại khám phá vũ trụ bao la và nới rộng biên giới tri thức.")
     ],
     [
         ("Đặc tính vật lý vi mô nào giúp máy tính lượng tử có sức mạnh tính toán vượt trội?", ["Hiện tượng bay hơi của nước", "Chồng chập và vướng víu lượng tử", "Ma sát bề mặt"], 1, "Trong bài có câu: 利用量子叠加与纠缠等微观物理特性."),
         ("Lĩnh vực nào ứng dụng mạng truyền thông khóa lượng tử để tăng độ an toàn tuyệt đối?", ["Quốc phòng và bảo mật dữ liệu tài chính", "Bán hàng tạp hóa lẻ", "Xem phim giải trí"], 0, "Trong câu có viết: 为国防和金融数据构筑无法破译的坚固盾牌."),
         ("Tầm quan trọng của việc nghiên cứu công nghệ lượng tử là gì?", ["Không mang lại lợi ích thực tế nào", "Cung cấp nền tảng vững chắc để khám phá vũ trụ và mở rộng nhận thức nhân loại", "Làm tốn kém ngân sách"], 1, "Trong câu cuối có viết: 为人类探索未知宇宙和拓展认知边界提供强有力的底层支撑.")
     ]),
    (4, "流域生态治理与绿色协同", "Quản trị sinh thái lưu vực và hiệp đồng xanh", "river_basin", "Sinh thái lưu vực", "🏞️", 7,
     "Chiến lược quy hoạch và bảo tồn toàn diện hệ sinh thái sông lớn, hài hòa giữa kinh tế và bảo vệ nguồn nước.",
     [
         ("大江大河作为孕育人类文明的母亲河，其流域生态系统的健康直接关乎亿万人民的福祉与未来。", "Dàjiāng-dàhé zuòwéi yùnyù rénlèi wénmíng de mǔqīn-hé, qí liùyù shēngtài xìtǒng de jiànkāng zhíjiē guānhū yìwàn rénmín de fúzhǐ yǔ wèilái.", "Những dòng sông lớn tựa như dòng sông mẹ nuôi dưỡng nền văn minh, sức khỏe hệ sinh thái lưu vực của chúng liên quan trực tiếp đến phúc lợi và tương lai hàng trăm triệu người."),
         ("长期的过度开发和工业污水排放，曾一度导致沿江水质恶化与鱼类生物多样性严重锐减。", "Chángqī de guòdù kāifā hé gōngyè wūshuǐ páifàng, céng yídù dǎozhì yánjiāng shuǐzhì èhuà yǔ yúlèi shēngwù duōyàngxìng yánzhòng ruìjiǎn.", "Khai thác quá độ và xả nước thải công nghiệp kéo dài từng có thời khiến chất lượng nước suy thoái và đa dạng sinh học loài cá sụt giảm nghiêm trọng."),
         ("推行全流域联合执法与十年禁渔政策，彰显了从过度索取转向休养生息的坚定决心。", "Tuīxíng quán liùyù liánhé zhífǎ yǔ shí nián jìnyú zhèngcè, zhāngxiǎn le cóng guòdù suǒqǔ zhuǎnxiàng xiūyǎng shēngxī de jiāndìng juéxīn.", "Triển khai thực thi pháp luật liên hợp toàn lưu vực và chính sách cấm đánh bắt mười năm thể hiện quyết tâm sắt đá chuyển từ khai thác cạn kiệt sang bồi bổ phục hồi."),
         ("沿岸重点高耗能企业的转型升级与湿地生态廊道的修复，逐步再现了一江清水碧波荡漾的生动图景。", "Yán'àn zhòngdiǎn gāohàonéng qǐyè de zhuǎnxíng shēngjí yǔ shīdì shēngtài lángdào de xiūfù, zhúbù zàixiàn le yì jiāng qīngshuǐ bìbō dàngyàng de shēngdòng tújǐng.", "Chuyển đổi các doanh nghiệp tiêu hao nhiều năng lượng và khôi phục hành lang sinh thái đất ngập nước đã dần tái hiện bức tranh dòng sông biếc sóng dập dờn sống động."),
         ("将生态优先、绿色发展的理念贯穿于流域规划全局，方能走出一条人水和谐的永续之路。", "Jiāng shēngtài yōuxiān, lǜsè fāzhǎn de lǐniàn guànchuān yú liùyù guīhuà quánjú, fāng néng zǒu chū yì tiáo rén shuǐ héxié de yǒngxù zhī lù.", "Quán triệt triết lý ưu tiên sinh thái, phát triển xanh vào quy hoạch lưu vực mới có thể mở ra con đường hòa hợp bền vững giữa con người và nguồn nước.")
     ],
     [
         ("Nguyên nhân từng khiến chất lượng nước sông lớn bị suy giảm là gì?", ["Khai thác quá độ và xả thải nước công nghiệp lâu ngày", "Do mưa quá nhiều", "Do các loài chim di cư"], 0, "Trong bài có câu: 长期的过度开发和工业污水排放，曾导致沿江水质恶化."),
         ("Chính sách quyết liệt nào được áp dụng để phục hồi nguồn lợi thủy sản?", ["Khuyến khích đánh bắt lưới lớn", "Liên hợp thực thi pháp luật và cấm đánh bắt mười năm", "Xây dựng thêm nhà máy ven bờ"], 1, "Trong câu có viết: 推行全流域联合执法与十年禁渔政策."),
         ("Mô hình phát triển bền vững cho các lưu vực sông là gì?", ["Ưu tiên sinh thái và phát triển xanh làm kim chỉ nam", "Xả thải thoải mái miễn là có lợi nhuận", "Ngăn đập không cho nước chảy"], 0, "Trong câu cuối có viết: 将生态优先、绿色发展的理念贯穿于规划全局.")
     ]),
    (5, "法治社会与契约精神", "Xã hội pháp quyền và tinh thần khế ước", "rule_of_law", "Pháp luật & Xã hội", "⚖️", 7,
     "Tôn trọng luật pháp và giữ gìn chữ tín trong giao kết: Nền tảng vững chắc của xã hội văn minh hiện đại.",
     [
         ("法治不仅是一套严谨完整的法律规范体系，更是现代文明国家治理现代化的基本方式。", "Fǎzhì bùjǐn shì yí tào yánjǐn wánzhěng de fǎlǜ guīfàn tǐxì, gèng shì xiàndài wénmíng guójiā zhìlǐ xiàndàihuà de jīběn fāngshì.", "Pháp quyền không chỉ là một hệ thống quy phạm pháp luật hoàn chỉnh chặt chẽ, mà còn là phương thức cơ bản của hiện đại hóa quản trị quốc gia văn minh."),
         ("在崇尚法治的社会环境中，法律面前人人平等成为不可动摇的最高准则与信仰。", "Zài chóngshàng fǎzhì de shèhuì huánjìng zhōng, fǎlǜ miànqián rénrén píngděng chéngwéi bùkě dòngyáo de zuìgāo zhǔnzé yǔ xìnyǎng.", "Trong môi trường xã hội thượng tôn pháp luật, mọi người bình đẳng trước pháp luật trở thành chuẩn tắc và niềm tin tối thượng không thể lay chuyển."),
         ("商业契约的严格遵守与对产权的坚决保护，是市场经济繁荣与社会信任积累的基石。", "Shāngyè qìyuē de yángé zūnshǒu yǔ duì chǎnquán de jiānjué bǎohù, shì shìchǎng jīngjì fánróng yǔ shèhuì xìnrèn jīlěi de jīshí.", "Nghiêm túc tuân thủ khế ước thương mại và kiên quyết bảo vệ quyền sở hữu tài sản là nền móng cho kinh tế thị trường thịnh vượng và tích lũy niềm tin xã hội."),
         ("司法机关秉持公正、程序正义与公开透明，才能让广大民众在每一个具体案件中感受到公平正义。", "Sīfǎ jīguān bǐngchí gōngzhèng, chéngxù zhèngyì yǔ gōngkāi tòumíng, cái néng ràng guǎngdà mínzhòng zài měi yí gè jùtǐ ànjiàn zhōng gǎnshòu dào gōngpíng zhèngyì.", "Cơ quan tư pháp giữ vững sự vô tư, công lý thủ tục và công khai minh bạch mới có thể giúp người dân cảm nhận được công bằng chính trực trong từng vụ án."),
         ("当守法成为一种自发的行为习惯和公民自觉，社会治理的运行成本便能显著降低。", "Dāng shǒufǎ chéngwéi yì zhǒng zìfā de xíngwéi xíguàn hé gōngmín zìjué, shèhuì zhìlǐ de yùnxíng chéngběn biàn néng xiǎnzhù jiàngdī.", "Khi tuân thủ pháp luật trở thành thói quen tự giác và ý thức công dân, chi phí vận hành quản trị xã hội sẽ giảm đi rõ rệt.")
     ],
     [
         ("Nguyên tắc tối cao không thể lay chuyển trong xã hội pháp quyền là gì?", ["Ưu tiên người có địa vị", "Mọi người bình đẳng trước pháp luật", "Luật pháp có thể thay đổi tùy ý cá nhân"], 1, "Trong bài có câu: 法律面前人人平等成为不可动摇的最高准则与信仰."),
         ("Điều gì là nền tảng cho sự thịnh vượng của kinh tế thị trường và niềm tin xã hội?", ["Tuân thủ nghiêm khế ước thương mại và bảo vệ quyền sở hữu", "Lừa dối đối tác kinh doanh", "Bỏ qua các cam kết hợp đồng"], 0, "Trong câu có viết: 商业契约的严格遵守与对产权的坚决保护."),
         ("Lợi ích xã hội khi người dân tự giác tuân thủ pháp luật là gì?", ["Gia tăng số lượng nhà tù", "Hạ giảm đáng kể chi phí vận hành quản trị xã hội", "Không cần đến tòa án nữa"], 1, "Trong câu cuối có viết: 社会治理的运行成本便能显著降低.")
     ]),
    (6, "中医药的现代化与国际化", "Hiện đại hóa và quốc tế hóa y học cổ truyền", "tcm_modernization", "Y học & Di sản", "🌿", 7,
     "Kết hợp y lý biện chứng ngàn đời với dược lý phân tử hiện đại: Đóng góp tinh hoa cho y học thế giới.",
     [
         ("中医药学是中国古代科学的瑰宝，凝聚着中华民族几千年来同疾病作斗争的博大智慧。", "Zhōngyī-yàoxué shì Zhōngguó gǔdài kēxué de guībǎo, níngjù zhe zhōnghuá mínzú jǐ qiān nián lái tóng jíbìng zuò dòuzhēng de bódà zhìhuì.", "Y dược học cổ truyền là viên ngọc quý của khoa học cổ đại Trung Hoa, ngưng tụ trí tuệ uyên bác hàng ngàn năm trong cuộc chiến đấu chống bệnh tật."),
         ("整体观念与辨证论治是中医的核心精髓，强调因人而异、因时制宜的个性化调理方案。", "Zhěngtǐ guānniàn yǔ biànzhèng-lùnzhì shì zhōngyī de héxīn jīngsuǐ, qiángdiào yīn rén ér yì, yīn shí zhìyí de gèxìnghuà tiáolǐ fāng'àn.", "Quan niệm chỉnh thể và biện chứng luận trị là tinh túy cốt lõi của Trung y, nhấn mạnh phác đồ điều dưỡng cá thể hóa tùy người tùy thời."),
         ("借助现代分子生物学和药物提取技术，科研人员成功阐明了诸多天然草药的活性成分与作用机理。", "Jièzhù xiàndài fēnzǐ shēngwùxué hé yàowù tíqǔ jìshù, kēyán rényuán chénggōng chǎnmíng le zhūduō tiānrán cǎoyào de huóxìng chéngfèn yǔ zuòyòng jīlǐ.", "Nhờ sinh học phân tử hiện đại và kỹ thuật chiết xuất dược liệu, các nhà khoa học đã làm sáng tỏ hoạt chất và cơ chế tác dụng của nhiều loại thảo dược thiên nhiên."),
         ("青蒿素等重大科研成果在抗击全球传染病中的卓越贡献，赢得了国际医学界的广泛赞誉与认可。", "Qīnghāosù děng zhòngdà kēyán chéngguǒ zài kàngjī quánqiú chuánrǎnbìng zhōng de zhuóyuè gòngxiàn, yíngdé le guójì yīxuéjiè de guǎngfàn zànyù yǔ rènkě.", "Những thành quả nghiên cứu lớn như Artemisinin trong việc chống bệnh truyền nhiễm toàn cầu đã nhận được sự tán dương và công nhận rộng rãi của y giới quốc tế."),
         ("推动中医药与现代医学的优势互补与深度融合，将为维护全人类的健康福祉贡献独特的东方方案。", "Tuīdòng zhōngyīyào yǔ xiàndài yīxué de yōushì hùbǔ yǔ shēndù rónghé, jiāng wèi wéihù quán rénlèi de jiànkāng fúzhǐ gòngxiàn dútè de dōngfāng fāng'àn.", "Thúc đẩy y dược cổ truyền bổ sung ưu thế và dung hòa sâu sắc với y học hiện đại sẽ đóng góp giải pháp phương Đông độc đáo cho sức khỏe toàn nhân loại.")
     ],
     [
         ("Đặc trưng cốt lõi trong phương pháp luận của Đông y là gì?", ["Chỉ chữa triệu chứng bên ngoài", "Quan niệm chỉnh thể và biện chứng luận trị cá thể hóa", "Áp dụng một bài thuốc cho mọi người"], 1, "Trong bài có câu: 整体观念与辨证论治是中医的核心精髓，强调因人而异."),
         ("Thành tựu tiêu biểu nào từ thảo dược cổ truyền đã cứu sống hàng triệu người trên thế giới?", ["Artemisinin (Thanh hao tố) trong điều trị bệnh sốt rét", "Kháng sinh tổng hợp", "Vitamin C nhân tạo"], 0, "Trong câu có viết: 青蒿素等重大科研成果在抗击全球传染病中的卓越贡献."),
         ("Định hướng kết hợp y học trong tương lai là gì?", ["Xóa bỏ hoàn toàn Đông y", "Bổ sung ưu thế và kết hợp sâu sắc giữa y học cổ truyền và y học hiện đại", "Không dùng thuốc tây nữa"], 1, "Trong câu cuối có viết: 推动中医药与现代医学的优势互补与深度融合.")
     ]),
    (7, "全球气候治理的多边机制", "Cơ chế đa phương trong quản trị khí hậu toàn cầu", "climate_governance", "Địa chính trị & Môi trường", "🌍", 7,
     "Hiệp định Paris và trách nhiệm chung nhưng có phân biệt giữa các quốc gia trong cuộc chiến chống biến đổi khí hậu.",
     [
         ("全球气候变化已经不再是遥远的科学预警，而是直接威胁人类生存发展的紧迫现实危机。", "Quánqiú qìhòu biànhuà yǐjīng bú zài shì yáoyuǎn de kēxué yùjǐng, ér shì zhíjiē wēixié rénlèi shēngcún fāzhǎn de jǐnpò xiànshí wēijī.", "Biến đổi khí hậu toàn cầu không còn là cảnh báo khoa học xa xôi, mà đã là cuộc khủng hoảng hiện thực cấp bách trực tiếp đe dọa sự sinh tồn của loài người."),
         ("极端高温、剧烈干旱与特大洪涝等灾害的频发，暴露出全球应对气候风险方面的系统性脆弱。", "Jíduān gāowēn, jùliè gānhàn yǔ tèdà hónglào děng zāihài de pínfā, bàolù chū quánqiú yìngduì qìhòu fēngxiǎn fāngmiàn de xìtǒngxìng cuìruò.", "Nắng nóng cực đoan, hạn hán khốc liệt và lũ lụt lớn xảy ra thường xuyên đã bộc lộ sự mong manh mang tính hệ thống khi ứng phó rủi ro khí hậu toàn cầu."),
         ("《巴黎协定》确立的共同但有区别的责任原则，为发达国家与发展中国家携手合作提供了制度框架。", "《Bālí Xiédìng》 quèlì de gòngtóng dàn yǒu qūbié de zérèn yuánzé, wèi fādá guójiā yǔ fāzhǎnzhōng guójiā xiéshǒu hézuò tígōng le zhìdù kuàngjià.", "Nguyên tắc 'trách nhiệm chung nhưng có phân biệt' xác lập trong Thỏa thuận Paris cung cấp khung thể chế cho các nước phát triển và đang phát triển cùng chung tay."),
         ("绿色低碳技术的跨国转移与专项气候资金的切实到位，是发展中国家实现能源转型的先决条件。", "Lǜsè dītàn jìshù de kuàguó zhuǎnyí yǔ zhuānxiàng qìhòu zījīn de qièshí dàowèi, shì fāzhǎnzhōng guójiā shíxiàn néngyuán zhuǎnxíng de xiānjué tiáojiàn.", "Chuyển giao công nghệ xanh xuyên biên giới và nguồn tài chính khí hậu thực chất là điều kiện tiên quyết để các nước đang phát triển chuyển đổi năng lượng."),
         ("唯有摒弃单边主义和零和博弈思维，全球社会才能共同构建人与自然生命共同体的宏伟蓝图。", "Wéiyǒu bìngqì dānbiān zhǔyì hé línghé bóyì sīwéi, quánqiú shèhuì cái néng gòngtóng gòujiàn rén yǔ zìrán shēngmìng gòngtóngtǐ de hóngwěi lántú.", "Chỉ khi từ bỏ chủ nghĩa đơn phương và tư duy đối đầu, cộng đồng quốc tế mới có thể cùng kiến tạo bức tranh cộng đồng cùng chia sẻ sinh mệnh giữa người và tự nhiên.")
     ],
     [
         ("Nguyên tắc cốt lõi của Thỏa thuận Paris là gì?", ["Tất cả các nước chịu chi phí ngang nhau không phân biệt giàu nghèo", "Trách nhiệm chung nhưng có sự phân biệt", "Chỉ các nước nghèo phải cắt giảm khí thải"], 1, "Trong bài có câu: 确立的共同但有区别的责任原则."),
         ("Điều kiện tiên quyết giúp các nước đang phát triển chuyển đổi năng lượng là gì?", ["Chuyển giao công nghệ sạch và nguồn tài chính khí hậu được bảo đảm", "Tự xoay xở mà không nhận hỗ trợ", "Đóng cửa tất cả các cơ sở sản xuất"], 0, "Trong câu có viết: 绿色低碳技术的跨国转移与专项气候资金的切实到位是先决条件."),
         ("Tinh thần hợp tác cần có để đối phó khủng hoảng khí hậu là gì?", ["Theo đuổi chủ nghĩa bảo hộ đơn phương", "Từ bỏ tư duy đối đầu, hợp tác đa phương cùng hành động", "Trì hoãn hành động thêm 50 năm"], 1, "Trong câu cuối có viết: 唯有摒弃单边主义和零和博弈思维，全球社会才能共同构建生命共同体.")
     ]),
    (8, "深空探测与月球科学实验", "Thám hiểm không gian sâu và khoa học mặt trăng", "deep_space", "Hàng không vũ trụ", "🚀", 7,
     "Những nỗ lực đưa tàu thám hiểm lấy mẫu đất đá mặt trăng và chuẩn bị cho trạm nghiên cứu liên hành tinh.",
     [
         ("探索浩瀚宇宙、和平利用外层空间，是人类数千年来不懈追求的伟大科学梦想。", "Tànsuǒ hàohàn yǔzhòu, hépíng lìyòng wàicéng kōngjiān, shì rénlèi shù qiān nián lái búxiè zhuīqiú de wěidà kēxué mèngxiǎng.", "Khám phá vũ trụ mênh mông và sử dụng hòa bình không gian vũ trụ là giấc mơ khoa học vĩ đại mà nhân loại không ngừng theo đuổi suốt ngàn năm."),
         ("月球作为距离地球最近的天然天体，成为人类开展深空探测和建立地外科研基地的首要前哨。", "Yuèqiú zuòwéi jùlí dìqiú zuì jìn de tiānrán tiāntǐ, chéngwéi rénlèi kāizhǎn shēnkōng tàncè hé jiànlì dìwài kēyán jīdì de shǒuyào qiánshào.", "Mặt trăng với tư cách là thiên thể tự nhiên gần trái đất nhất đã trở thành tiền đồn đầu tiên để tiến hành thám hiểm vũ trụ sâu và xây dựng căn cứ khoa học ngoài không gian."),
         ("无人探测器在月球背面着陆并成功取样返回，填补了人类对月球古老地质演化历史的研究空白。", "Wúrén tàncèqì zài yuèqiú bèimiàn zhuólù bìng chénggōng qǔyàng fǎnhuí, tiánbǔ le rénlèi duì yuèqiú gǔlǎo dìzhì yǎnhuà lìshǐ de yánjiū kòngbái.", "Tàu thám hiểm không người lái đáp xuống nửa tối mặt trăng và lấy mẫu trở về thành công đã lấp đầy khoảng trống nghiên cứu lịch sử tiến hóa địa chất cổ xưa."),
         ("月壤中蕴含的丰富同位素与水冰沉积线索，为未来月球科研站的能源供给提供了无限遐想。", "Yuèrǎng zhōng yùnhán de fēngfù tóngwèisù yǔ shuǐbīng chénjī xiànsuǒ, wèi wèilái yuèqiú kēyánzhàn de néngyuán gōngjǐ tígōng le wúxiàn xiáxiǎng.", "Các đồng vị dồi dào và dấu vết lắng đọng băng nước trong đất mặt trăng đem lại triển vọng vô hạn cho việc cung cấp năng lượng cho trạm khoa học tương lai."),
         ("人类航天技术的每一次飞跃，都在持续拓展着文明的认知边界，激励着下一代勇敢奔赴星辰大海。", "Rénlèi hángtiān jìshù de měi yí cì fēiyuè, dōu zài chíxù tuòzhǎn zhe wénmíng de rènzhī biānjiè, jīlì zhe xià yí dài yǒnggǎn bēnfù xīngchén dàhǎi.", "Mỗi bước nhảy vọt của kỹ thuật hàng không vũ trụ đều đang không ngừng mở rộng ranh giới nhận thức văn minh, cổ vũ thế hệ tương lai dũng cảm hướng về biển sao rực rỡ.")
     ],
     [
         ("Tại sao mặt trăng là tiền đồn đầu tiên trong thám hiểm không gian?", ["Vì là thiên thể tự nhiên gần trái đất nhất", "Vì có đầy đủ không khí để thở ngay", "Vì thời tiết ở đó rất ấm áp"], 0, "Trong bài có câu: 月球作为距离地球最近的天然天体，成为首要前哨."),
         ("Việc lấy mẫu đất đá từ mặt trăng về trái đất có ý nghĩa khoa học gì?", ["Làm đồ trang sức", "Lấp đầy khoảng trống nghiên cứu lịch sử tiến hóa địa chất cổ xưa của mặt trăng", "Bán đấu giá"], 1, "Trong câu có viết: 填补了人类对月球古老地质演化历史的研究空白."),
         ("Ý nghĩa lâu dài của các bước tiến hàng không vũ trụ là gì?", ["Chỉ tốn kém tài chính vô ích", "Mở rộng ranh giới nhận thức và truyền cảm hứng khám phá cho các thế hệ tương lai", "Đưa tất cả mọi người lên mặt trăng sống ngay"], 1, "Trong câu cuối có viết: 拓展着文明的认知边界，激励着下一代勇敢奔赴星辰大海.")
     ]),
    (9, "乡村振兴与现代产业融合", "Hồi sinh nông thôn và tích hợp công nghiệp hiện đại", "rural_revitalization", "Phát triển nông thôn", "🌾", 7,
     "Thương mại điện tử nông sản, du lịch sinh thái và công nghệ nông nghiệp thông minh đổi mới vùng quê.",
     [
         ("全面推进乡村振兴，是消除区域发展不平衡、实现全体人民共同富裕的战略之举。", "Quánmiàn tuījìn xiāngcūn zhènxīng, shì xiāochú qūyù fāzhǎn bù pínghéng, shíxiàn quántǐ rénmín gòngtóng fùyù de zhànlüè zhī jǔ.", "Thúc đẩy toàn diện phục hưng nông thôn là bước đi chiến lược xóa bỏ mất cân bằng vùng miền, hiện thực hóa thịnh vượng chung cho toàn thể nhân dân."),
         ("数字技术与现代农业的深度融合，催生了智慧灌溉、无人机巡田等一批现代化生产新模式。", "Shùzì jìshù de shēndù rónghé, cuīshēng le zhìhuì guàngài, wúrénjī xúntián děng yí pī xiàndàihuà shēngchǎn xīn móshì.", "Sự giao hòa sâu sắc giữa công nghệ số và nông nghiệp hiện đại đã sinh ra hàng loạt mô hình sản xuất mới như tưới tiêu thông minh, máy bay không người lái tuần ruộng."),
         ("电子商务进村入户打通了农产品出山的物流堵点，让绿色无污染的田间美味直达城市餐桌。", "Diànzǐ shāngwù jìn cūn rù hù dǎtōng le nóngchǎnpǐn chūshān de wùliú dǔdiǎn, ràng lǜsè wúwūrǎn de tiánjiān měiwèi zhídá chéngshì cānzhuō.", "Thương mại điện tử về tận làng bản đã khai thông điểm nghẽn hậu cần nông sản, đưa hương vị đồng quê xanh sạch tới thẳng bàn ăn thành thị."),
         ("依托优美的自然风光和深厚的乡土民俗，乡村生态文旅产业展现出强劲的吸纳就业能力。", "Yītuō yōuměi de zìrán fēngguāng hé shēnhòu de xiāngtǔ mínsú, xiāngcūn shēngtài wénlǚ chǎnyè zhǎnxiàn chū qiángjìn de xīnà jiùyè nénglì.", "Dựa vào phong cảnh tự nhiên tươi đẹp và phong tục tập quán đậm đà, ngành văn hóa du lịch sinh thái nông thôn thể hiện sức hút lao động việc làm mạnh mẽ."),
         ("产业兴旺、生态宜居与乡风文明相得益彰，绘制出一幅生机勃勃的现代化美丽乡村新画卷。", "Chǎnyè xīngwàng, shēngtài yíjū yǔ xiāngfēng wénmíng xiāngdé-yìzhāng, huìzhì chū yì fú shēngjī-bóbó de xiàndàihuà měilì xiāngcūn xīn huàjuàn.", "Công nghiệp hưng thịnh, sinh thái đáng sống và nếp sống văn minh hòa quyện tạo nên bức tranh làng quê tươi đẹp hiện đại căng tràn sức sống.")
     ],
     [
         ("Mô hình nào minh chứng cho sự tích hợp giữa công nghệ số và nông nghiệp?", ["Tưới tiêu thông minh và dùng máy bay không người lái quản lý đồng ruộng", "Dùng sức trâu cày hoàn toàn", "Bỏ hoang đất canh tác"], 0, "Trong bài có câu: 催生了智慧灌溉、无人机巡田等一批现代化生产新模式."),
         ("Thương mại điện tử nông thôn mang lại thay đổi thiết thực nào?", ["Khơi thông dòng chảy logistics giúp nông sản tươi sạch tiếp cận người tiêu dùng thành phố", "Làm mất việc làm của nông dân", "Tăng chi phí trung gian gấp nhiều lần"], 0, "Trong câu có viết: 打通了农产品出山的物流堵点，让田间美味直达城市餐桌."),
         ("Mục tiêu toàn diện của công cuộc xây dựng nông thôn mới là gì?", ["Chỉ làm công nghiệp nặng", "Sản xuất hưng thịnh, môi trường đáng sống và đời sống văn minh hài hòa", "Biến nông thôn thành các khu chung cư dày đặc"], 1, "Trong câu cuối có viết: 产业兴旺、生态宜居与乡风文明相得益彰.")
     ]),
    (10, "城市微更新与历史文脉留存", "Cải tạo vi mô và lưu giữ văn mạch đô thị", "urban_renewal", "Quy hoạch & Kiến trúc", "🏙️", 7,
     "Từ đập phá ồ ạt chuyển sang chỉnh trang tỉ mỉ: Bảo tồn ký ức cộng đồng và hồn cốt phố xưa.",
     [
         ("在经历了大拆大建的快速扩张阶段后，当代城市发展正逐步转向精细化的有机微更新时代。", "Zài jīnglì le dà chāi dà jiàn de kuàisù kuòzhāng jiēduàn hòu, dāngdài chéngshì fāzhǎn zhèng zhúbù zhuǎnxiàng jīngxìhuà de yǒujī wēigèngxīn shídài.", "Sau khi trải qua giai đoạn mở rộng nhanh chóng với phá dỡ hàng loạt, phát triển đô thị đương đại đang từng bước chuyển sang thời kỳ chỉnh trang vi mô hữu cơ tinh tế."),
         ("保留老街区的原有肌理和邻里温情，让历史建筑在修旧如旧的前提下融入现代生活功能。", "Bǎoliú lǎo jiēqū de yuányǒu jīlǐ hé línlǐ wēnqíng, ràng lìshǐ jiànzhù zài xiū jiù rú jiù de qiántí xià róngrù xiàndài shēnghuó gōngnéng.", "Lưu giữ cấu trúc nguyên bản của phố cổ và tình làng nghĩa xóm, để các công trình lịch sử trên nguyên tắc 'tu sửa như xưa' hòa nhập công năng hiện đại."),
         ("口袋公园、社区微图书馆和文化街巷的改造，在极小尺度内极大地提升了居民的生活幸福指数。", "Kǒudài gōngyuán, shèqū wēi túshūguǎn hé wénhuà jiēxiàng de gǎizào, zài jí xiǎo chǐdù nèi jídà de tíshēng le jūmín de shēnghuó xìngfú zhǐshù.", "Cải tạo công viên bỏ túi, thư viện nhỏ cộng đồng và ngõ phố văn hóa đã nâng cao đáng kể chỉ số hạnh phúc cư dân trong quy mô nhỏ bé."),
         ("盲目追求高楼大厦千城一面的同质化开发，往往会彻底割裂城市的历史文脉与情感认同。", "Mángmù zhuīqiú gāolóu dàshà qiān chéng yí miàn de tóngzhìhuà kāifā, wǎngwǎng huì chèdǐ gēliè chéngshì de lìshǐ wénmài yǔ qínggǎn rèntóng.", "Mù quáng theo đuổi các tòa nhà chọc trời rập khuôn 'nghìn thành phố một vẻ' thường làm đứt gãy hoàn toàn mạch nguồn lịch sử và bản sắc cảm xúc đô thị."),
         ("兼顾历史记忆与现代宜居，才能打造出有温度、有灵魂、有辨识度的真正现代化都市空间。", "Jiāngù lìshǐ jìyì yǔ xiàndài yíjū, cái néng dǎzào chū yǒu wēndù, yǒu línghún, yǒu biànshídù de zhēnzhèng xiàndàihuà dūshì kōngjiān.", "Cân bằng giữa ký ức lịch sử và sự đáng sống hiện đại mới có thể kiến tạo nên không gian đô thị hiện đại thực thụ ấm áp, có linh hồn và giàu bản sắc.")
     ],
     [
         ("Chiến lược phát triển đô thị đương đại đang có sự chuyển hướng như thế nào?", ["Tiếp tục đập phá toàn bộ phố cũ để xây nhà chọc trời", "Chuyển sang chỉnh trang vi mô hữu cơ tinh tế và bảo tồn di sản", "Ngừng bảo trì tất cả các công trình"], 1, "Trong câu đầu có viết: 逐步转向精细化的有机微更新时代."),
         ("Hệ lụy của việc phát triển đô thị rập khuôn 'nghìn thành phố một mẫu' là gì?", ["Làm mất đi ký ức lịch sử và sự gắn kết bản sắc văn hóa", "Khiến thành phố trở nên độc đáo hơn", "Không gây ảnh hưởng gì"], 0, "Trong bài có câu: 彻底割裂城市的历史文脉与情感认同."),
         ("Mục tiêu của việc cải tạo không gian sống đô thị hiện đại là gì?", ["Kiến tạo không gian đô thị ấm áp, có linh hồn và giàu bản sắc riêng", "Bán đất với giá cao nhất có thể", "Xóa bỏ toàn bộ cây xanh"], 0, "Trong câu cuối có viết: 打造出有温度、有灵魂、有辨识度的真正现代化都市空间.")
     ])
]
