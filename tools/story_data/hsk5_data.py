"""
tools/story_data/hsk5_data.py
10 stories data for HSK 5
"""

HSK5_STORIES = [
    (1, "传统手工艺的现代传承", "Nghệ thuật thủ công truyền thống và sự kế thừa hiện đại", "art_heritage", "Di sản nghệ thuật", "🏺", 5,
     "Sự kết hợp hài hòa giữa kỹ nghệ gốm sứ truyền thống và thiết kế sáng tạo đương đại.",
     [
         ("在现代工业快速发展的今天，传统手工艺依然散发着独特的魅力。", "Zài xiàndài gōngyè kuàisù fāzhǎn de jīntiān, chuántǒng shǒugōngyì yīrán sànfā zhe dútè de mèilì.", "Trong thời đại công nghiệp hiện đại phát triển nhanh chóng, nghề thủ công truyền thống vẫn tỏa ra sức hấp dẫn độc đáo."),
         ("许多年轻的设计师将现代审美观念巧妙地融入古典陶瓷制作中。", "Xǔduō niánqīng de shèjìshī jiāng xiàndài shěnměi guānniàn qiǎomiào de róngrù gǔdiǎn táocí zhìzuò zhōng.", "Nhiều nhà thiết kế trẻ đã khéo léo lồng ghép quan niệm thẩm mỹ hiện đại vào chế tác gốm sứ cổ điển."),
         ("这种创新不仅保留了传统技艺的精髓，而且赋予了古老器物新的生命力。", "Zhè zhǒng chuàngxīn bùjǐn bǎoliú le chuántǒng jìyì de jīngsuǐ, érqiě fùyǔ le gǔlǎo qìwù xīn de shēngmìnglì.", "Sự đổi mới này không chỉ lưu giữ tinh hoa kỹ nghệ truyền thống mà còn thổi sức sống mới vào những đồ vật cổ xưa."),
         ("越来越多的消费者愿意为具有文化内涵的手工制品买单。", "Yuè lái yuè duō de xiāofèizhě yuànyì wèi jùyǒu wénhuà nèihán de shǒugōng zhìpǐn mǎidān.", "Ngày càng nhiều người tiêu dùng sẵn sàng chi trả cho các sản phẩm thủ công chứa đựng chiều sâu văn hóa."),
         ("文化的传承需要我们在尊重历史的同时，勇敢地开辟未来。", "Wénhuà de chuánchéng xūyào wǒmen zài zūnzhòng lìshǐ de tóngshí, yǒnggǎn de kāipì wèilái.", "Sự kế thừa văn hóa đòi hỏi chúng ta vừa tôn trọng lịch sử, vừa dũng cảm mở lối tương lai.")
     ],
     [
         ("Các nhà thiết kế trẻ đã làm gì để bảo tồn nghề gốm sứ?", ["Kết hợp thẩm mỹ hiện đại vào chế tác truyền thống", "Dừng sản xuất thủ công", "Chuyển sang làm máy móc hoàn toàn"], 0, "Trong bài có câu: 将现代审美观念巧妙地融入古典陶瓷制作中."),
         ("Phản ứng của người tiêu dùng đối với sản phẩm thủ công ra sao?", ["Không quan tâm", "Sẵn lòng chi trả cho sản phẩm có chiều sâu văn hóa", "Cho rằng giá quá đắt"], 1, "Trong câu có viết: 愿意为具有文化内涵的手工制品买单."),
         ("Thông điệp cốt lõi về kế thừa văn hóa là gì?", ["Vừa tôn trọng lịch sử vừa dũng cảm đổi mới cho tương lai", "Chỉ giữ nguyên bản không thay đổi", "Lãng quên quá khứ"], 0, "Trong câu cuối có viết: 在尊重历史的同时，勇敢地开辟未来.")
     ]),
    (2, "人工智能与未来生活", "Trí tuệ nhân tạo và cuộc sống tương lai", "technology_ai", "Công nghệ & AI", "🤖", 5,
     "Những bước tiến vượt bậc của trí tuệ nhân tạo và sự thích nghi của con người trong kỷ nguyên số.",
     [
         ("人工智能技术的飞速突破，正在深刻地改变着人类社会的方方面面。", "Réngōng zhìnéng jìshù de fēisù tūpò, zhèngzài shēnkè de gǎibiàn zhe rénlèi shèhuì de fāngfāng-miànmiàn.", "Sự đột phá thần tốc của trí tuệ nhân tạo đang làm thay đổi sâu sắc mọi mặt đời sống nhân loại."),
         ("从自动驾驶汽车到智能医疗诊断，科技让我们的日常生活更加高效便捷。", "Cóng zìdòng jiàshǐ qìchē dào zhìnéng yīliáo zhěnduàn, kējì ràng wǒmen de rìcháng shēnghuó gèngjiā gāoxiào biànjié.", "Từ xe tự lái đến chẩn đoán y tế thông minh, công nghệ giúp sinh hoạt thường nhật thêm hiệu quả và tiện lợi."),
         ("然而，机器的高速运算并不能完全代替人类的情感关怀与创造性思维。", "Rán'ér, jīqì de gāosù yùnsuàn bìng bù néng wánquán dàitì rénlèi de qínggǎn guānhuái yǔ chuàngzàoxìng sīwéi.", "Thế nhưng, tốc độ tính toán siêu việt của máy móc không thể thay thế hoàn toàn tình cảm và tư duy sáng tạo của con người."),
         ("面对未来的挑战，我们需要学会与人工智能合作，提升自身的核心价值。", "Miànduì wèilái de tiǎozhàn, wǒmen xūyào xuéhuì yǔ réngōng zhìnéng hézuò, tíshēng zìshēn de héxīn jiàzhí.", "Đối diện thử thách tương lai, chúng ta cần học cách cộng tác cùng AI và nâng cao giá trị cốt lõi của bản thân."),
         ("科技的终极目标，应当是促进人类社会的公平、温暖与繁荣。", "Kējì de zhōngjí mùbiāo, yīngdāng shì cùjìn rénlèi shèhuì de gōngpíng, wēnnuǎn yǔ fánróng.", "Mục tiêu tối thượng của công nghệ phải là thúc đẩy một xã hội công bằng, ấm áp và thịnh vượng.")
     ],
     [
         ("AI đã ứng dụng vào những lĩnh vực nào được nêu trong bài?", ["Xe tự lái và chẩn đoán y tế thông minh", "Nấu ăn trong gia đình", "Du lịch vũ trụ"], 0, "Trong bài có câu: 从自动驾驶汽车到智能医疗诊断."),
         ("Điều gì máy móc không thể thay thế con người?", ["Tốc độ tính toán", "Tình cảm và tư duy sáng tạo", "Lưu trữ dữ liệu"], 1, "Trong câu có viết: 并不能完全代替人类的情感关怀与创造性思维."),
         ("Mục tiêu tối hậu của công nghệ là gì?", ["Thay thế con người", "Thúc đẩy xã hội công bằng, ấm áp và thịnh vượng", "Kiếm lợi nhuận cao nhất"], 1, "Trong câu cuối có viết: 促进人类社会的公平、温暖与繁荣.")
     ]),
    (3, "青年创业的机遇与挑战", "Cơ hội và thách thức khi khởi nghiệp của giới trẻ", "business_startup", "Kinh doanh & Khởi nghiệp", "🚀", 5,
     "Hành trình khởi nghiệp đầy đam mê, đối mặt rủi ro tài chính và bài học lãnh đạo bản lĩnh.",
     [
         ("近年来，越来越多的年轻大学毕业生选择踏上自主创业的道路。", "Jìnnián lái, yuè lái yuè duō de niánqīng dàxué bìyèshēng xuǎnzé tà shàng zìzhǔ chuàngyè de dàolù.", "Những năm gần đây, ngày càng nhiều cử nhân đại học trẻ tuổi lựa chọn bước vào con đường tự thân lập nghiệp."),
         ("创业不仅需要充满激情的梦想，更需要周密的市场调研和资金预算。", "Chuàngyè bùjǐn xūyào chōngmǎn jīqíng de mèngxiǎng, gèng xūyào zhōumì de shìchǎng diàoyán hé zījīn yùsuàn.", "Khởi nghiệp không chỉ cần ước mơ tràn đầy nhiệt huyết, mà còn đòi hỏi nghiên cứu thị trường và dự toán vốn chu toàn."),
         ("面对激烈的市场竞争，创业团队往往要经历许多预料之外的挫折。", "Miànduì jīliè de shìchǎng jìngzhēng, chuàngyè tuánduì wǎngwǎng yào jīnglì xǔduō yùliào zhī wài de cuòzhé.", "Đối mặt cạnh tranh khốc liệt, đội ngũ khởi nghiệp thường phải trải qua nhiều va vấp ngoài dự liệu."),
         ("唯有具备敏锐的商业眼光和坚持到底的韧劲，才能在逆境中生存下来。", "Wéiyǒu jùbèi mǐnruì de shāngyè yǎnguāng hé jiānchí dàodǐ de rènjìn, cái néng zài nìjìng zhōng shēngcún xiàlái.", "Chỉ có sở hữu tầm nhìn kinh doanh nhạy bén cùng sự kiên cường tới cùng mới có thể tồn tại trong nghịch cảnh."),
         ("无论最终成功与否，创业过程本身就是人生中一笔极其宝贵的财富。", "Wúlùn zuìzhōng chénggōng yǔ fǒu, chuàngyè guòchéng běnshēn jiù shì rénshēng zhōng yì bǐ jíqí bǎoguì de cáifù.", "Dù thành công hay không, quá trình khởi nghiệp tự nó đã là một tài sản vô giá trong đời.")
     ],
     [
         ("Khởi nghiệp cần những yếu tố thiết thực nào ngoài ước mơ?", ["Chỉ cần vốn lớn", "Nghiên cứu thị trường chu đáo và dự toán tài chính kỹ lưỡng", "Sự may mắn"], 1, "Trong câu có viết: 更需要周密的市场调研和资金预算."),
         ("Yếu tố nào giúp các đội ngũ khởi nghiệp vượt qua nghịch cảnh?", ["Tầm nhìn nhạy bén và ý chí kiên định", "Hạ giá sản phẩm bất chấp", "Trông chờ trợ cấp"], 0, "Trong bài có câu: 具备敏锐的商业眼光和坚持到底的韧劲."),
         ("Tác giả nhìn nhận quá trình khởi nghiệp như thế nào?", ["Là sự lãng phí thời gian", "Là tài sản trải nghiệm cực kỳ quý giá trong đời", "Chỉ có ý nghĩa khi kiếm được nhiều tiền"], 1, "Trong câu cuối có viết: 创业过程本身就是人生中一笔极其宝贵的财富.")
     ]),
    (4, "读书的力量与终身学习", "Sức mạnh của đọc sách và học tập suốt đời", "education_growth", "Giáo dục & Phát triển", "📖", 5,
     "Thói quen đọc sách mở rộng tầm mắt, làm phong phú tâm hồn và nuôi dưỡng tư duy phản biện.",
     [
         ("阅读一本优秀的著作，就如同在与一位高尚的智者进行深入的灵魂对话。", "Yuèdú yì běn yōuxiù de zhùzuò, jiù rútóng zài yǔ yí wèi gāoshàng de zhìzhě jìnxíng shēnrù de línghún duìhuà.", "Đọc một cuốn sách ưu tú tựa như đang đối thoại sâu sắc về tâm hồn với một bậc hiền triết cao thượng."),
         ("书籍不仅能帮助我们开阔眼界，还能在迷茫时提供前行的智慧与力量。", "Shūjí bùjǐn néng bāngzhù wǒmen kāikuò yǎnjiè, hái néng zài mímáng shí tígōng qiánxíng de zhìhuì yǔ lìliàng.", "Sách vở không chỉ giúp ta mở rộng tầm mắt mà còn đem lại trí tuệ và sức mạnh vững bước khi hoang mang."),
         ("在信息爆炸的今天，碎片化阅读往往使人浮躁，深度阅读显得尤为珍贵。", "Zài xìnxī bàozhà de jīntiān, suìpiànhuà yuèdú wǎngwǎng shǐ rén fúzào, shēndù yuèdú xiǎnde yóuwèi zhēnguì.", "Trong thời đại bùng nổ thông tin, đọc phân mảnh dễ khiến con người nông nổi, đọc sâu càng trở nên đáng quý."),
         ("每天抽出一段安静的时间专心读书，是保持独立思考能力的最佳途径。", "Měitiān chōuchū yí duàn ānjìng de shíjiān zhuānxīn dúshū, shì bǎochí dúlì sīkǎo nénglì de zuì jiā tújìng.", "Mỗi ngày dành chút thời gian tĩnh lặng chuyên tâm đọc sách là cách tốt nhất để duy trì tư duy độc lập."),
         ("让学习成为一种终身习惯，生命便会因此而变得格外丰盈和精彩。", "Ràng xuéxí chéngwéi yì zhǒng zhōngshēn xíguàn, shēngmìng biàn huì yīncǐ ér biàn de géwài fēngyíng hé jīngcǎi.", "Biến học tập thành thói quen trọn đời, cuộc sống sẽ trở nên phong phú và rạng rỡ bội phần.")
     ],
     [
         ("Đọc sách hay được ví như điều gì?", ["Xem một bộ phim", "Đối thoại sâu sắc với một bậc hiền triết", "Đi dạo công viên"], 1, "Trong câu đầu có viết: 如同在与一位高尚的智者进行深入的灵魂对话."),
         ("Đọc sâu có giá trị gì trong thời đại thông tin bùng nổ?", ["Giúp duy trì năng lực tư duy độc lập và tĩnh tâm", "Gây mất thời gian", "Làm giảm trí nhớ"], 0, "Trong bài có câu: 是保持独立思考能力的最佳途径."),
         ("Lợi ích của việc coi học tập là thói quen trọn đời là gì?", ["Giúp cuộc sống trở nên phong phú và rạng rỡ", "Để có nhiều bằng cấp", "Không có lợi ích rõ ràng"], 0, "Trong câu cuối có viết: 生命便会因此而变得格外丰盈和精彩.")
     ]),
    (5, "城市绿色发展与生态保护", "Phát triển xanh và bảo vệ sinh thái đô thị", "urban_ecology", "Đô thị & Sinh thái", "🌳", 5,
     "Kiến tạo không gian sống trong lành thông qua công viên cây xanh và quy hoạch đô thị bền vững.",
     [
         ("现代城市的繁荣不应当以牺牲优美的自然生态环境为代价。", "Xiàndài chéngshì de fánróng bù yīngdāng yǐ xīshēng yōuměi de zìrán shēngtài huánjìng wéi dàijià.", "Sự phồn hoa của đô thị hiện đại không nên đánh đổi bằng sự hy sinh môi trường sinh thái tự nhiên."),
         ("越来越多的城市开始重视湿地公园建设和绿色公共空间的拓展。", "Yuè lái yuè duō de chéngshì kāishǐ zhòngshì shīdì gōngyuán jiànshè hé lǜsè gōnggòng kōngjiān de tuòzhǎn.", "Ngày càng nhiều đô thị coi trọng việc xây dựng công viên ngập nước và mở rộng không gian công cộng xanh."),
         ("大面积的绿化带不仅能够吸收粉尘，还能有效降低城市的温室效应。", "Dà miànjī de lǜhuàdài bùjǐn nénggòu xīshōu fěnchén, hái néng yǒuxiào jiàngdī chéngshì de wēnshì xiàoyìng.", "Những dải cây xanh diện tích lớn không chỉ hấp thụ khói bụi mà còn hạ giảm hiệu ứng nhà kính hiệu quả."),
         ("推行公共交通和自行车出行，有助于显著改善城市上空的空气质量。", "Tuīxíng gōnggòng jiāotōng hé zìxíngchē chūxíng, yǒuzhù yú xiǎnzhù gǎishàn chéngshì shàngkōng de kōngqì zhìliàng.", "Khuyến khích giao thông công cộng và xe đạp giúp cải thiện rõ rệt chất lượng không khí."),
         ("人与自然的和谐共生，才是现代文明最为理想与持久的发展模式。", "Rén yǔ zìrán de héxié gòngshēng, cái shì xiàndài wénmíng zuìwéi lǐxiǎng yǔ chíjiǔ de fāzhǎn móshì.", "Con người hòa hợp cộng sinh cùng tự nhiên mới là mô hình phát triển lý tưởng và bền vững nhất.")
     ],
     [
         ("Dải cây xanh đô thị mang lại lợi ích gì?", ["Hấp thụ khói bụi và giảm hiệu ứng nhà kính", "Gây cản trở giao thông", "Tăng chi phí bảo trì mà không có tác dụng"], 0, "Trong bài có câu: 吸收粉尘，还能有效降低城市的温室效应."),
         ("Hành động giao thông nào giúp cải thiện không khí thành phố?", ["Đi xe hơi cá nhân", "Sử dụng giao thông công cộng và xe đạp", "Hạn chế ra đường"], 1, "Trong câu có viết: 推行公共交通和自行车出行，有助于显著改善空气质量."),
         ("Mô hình phát triển lý tưởng nhất của văn minh hiện đại là gì?", ["Khai thác cạn kiệt tài nguyên", "Con người hòa hợp cùng sinh tồn với tự nhiên", "Xây dựng toàn bê tông"], 1, "Trong câu cuối có viết: 人与自然的和谐共生，才是最为理想与持久的发展模式.")
     ]),
    (6, "跨文化交流中的包容与对话", "Bao dung và đối thoại trong giao lưu đa văn hóa", "culture_dialogue", "Giao lưu văn hóa", "🌐", 5,
     "Vượt qua định kiến và rào cản ngôn ngữ để thấu hiểu sự phong phú của các nền văn minh thế giới.",
     [
         ("全球化使世界各国的距离大大缩短，跨文化交流变得前所未有地频繁。", "Quánqiúhuà shǐ shìjiè gèguó de jùlí dàdà suōduǎn, kuàwénhuà jiāoliú biàn de qiánsuǒwèiyǒu de pínfán.", "Toàn cầu hóa thu hẹp khoảng cách giữa các quốc gia, khiến giao lưu đa văn hóa diễn ra sôi nổi chưa từng có."),
         ("面对不同的风俗习惯和价值观念，相互尊重与坦诚沟通是理解的基础。", "Miànduì bùtóng de fēngsú xíguàn hé jiàzhí guānniàn, xiānghù zūnzhòng hé tǎncéng gōutōng shì lǐjiě de jīchǔ.", "Đối diện các phong tục và hệ giá trị khác nhau, sự tôn trọng và trao đổi chân thành là nền tảng thấu hiểu."),
         ("简单地用自己的文化标准去衡量他人的行为，往往容易产生不必要的偏见。", "Jiǎndān de yòng zìjǐ de wénhuà biāozhǔn qù héngliáng tārén de xíngwéi, wǎngwǎng róngyì chǎnshēng bú bìyào de piānjiàn.", "Nếu chỉ đơn thuần lấy chuẩn mực của mình để phán xét người khác sẽ dễ nảy sinh định kiến không đáng có."),
         ("学会倾听与换位思考，能让我们发现多元文化背后共同的人性美好。", "Xuéhuì qīngtīng yǔ huànwèi sīkǎo, néng ràng wǒmen fāxiàn duōyuán wénhuà bèihòu gòngtóng de rénxìng měihǎo.", "Học cách lắng nghe và đặt mình vào vị trí đối phương sẽ giúp ta nhận ra nét đẹp nhân tính chung."),
         ("开放包容的心态，能够架起不同文明之间友谊与合作的坚固桥梁。", "Kāifàng bāoróng de xīntài, nénggòu jià qǐ bùtóng wénmíng zhījiān yǒuyì yǔ hézuò de jiāngù qiáoliáng.", "Tâm thế cởi mở bao dung sẽ dựng nên nhịp cầu hữu nghị và hợp tác bền vững giữa các nền văn minh.")
     ],
     [
         ("Nền tảng của sự thấu hiểu trong giao lưu đa văn hóa là gì?", ["Tôn trọng lẫn nhau và trao đổi chân thành", "Áp đặt quan điểm riêng", "Giữ im lặng"], 0, "Trong bài có câu: 相互尊重与坦诚沟通是理解的基础."),
         ("Hành vi nào dễ dẫn đến định kiến văn hóa?", ["Lấy chuẩn mực văn hóa của mình để phán xét người khác", "Học thêm ngôn ngữ mới", "Đi du lịch tìm hiểu"], 0, "Trong câu có viết: 用自己的文化标准去衡量他人的行为，往往容易产生不必要的偏见."),
         ("Thái độ cởi mở bao dung mang lại tác dụng gì?", ["Tạo khoảng cách lớn hơn", "Dựng nên nhịp cầu hữu nghị và hợp tác bền vững", "Làm mất đi bản sắc cá nhân"], 1, "Trong câu cuối có viết: 架起不同文明之间友谊与合作的坚固桥梁.")
     ]),
    (7, "心理韧性与压力管理", "Sức bền tâm lý và quản lý áp lực cuộc sống", "psychology_resilience", "Tâm lý & Bản lĩnh", "🧘", 5,
     "Rèn luyện tâm lý vững vàng, biến áp lực thành động lực tích cực để trưởng thành hơn mỗi ngày.",
     [
         ("在竞争激烈的现代社会，每个人都会不可避免地承受各种心理压力。", "Zài jìngzhēng jīliè de xiàndài shèhuì, měi gè rén dōu huì bùkě-bìmiǎn de chéngshòu gèzhǒng xīnlǐ yālì.", "Trong xã hội hiện đại cạnh tranh gay gắt, ai cũng khó tránh khỏi việc chịu đựng các áp lực tâm lý."),
         ("适度的压力能够激发我们的潜能，但过度的焦虑则会损害身心健康。", "Shìdù de yālì nénggòu jīfā wǒmen de qiánnéng, dàn guòdù de jiāolǜ zé huì sǔnhài shēnxīn jiànkāng.", "Áp lực vừa phải có thể khơi dậy tiềm năng, nhưng lo âu quá mức sẽ gây tổn hại sức khỏe thân tâm."),
         ("培养强大的心理韧性，意味着我们在面对挫折时能够迅速调整心态。", "Péiyǎng qiángdà de xīnlǐ rènxìng, yìwèizhe wǒmen zài miànduì cuòzhé shí nénggòu xùnsù tiáozhěng xīntài.", "Rèn luyện sức bền tâm lý vững vàng nghĩa là ta có thể nhanh chóng điều chỉnh tâm trạng trước nghịch cảnh."),
         ("学会倾诉、规律运动以及保持充足睡眠，是有效缓解压力的科学良方。", "Xuéhuì qīngsù, guīlǜ yùndòng yǐjí bǎochí chōngzú shuìmián, shì yǒuxiào huǎnjiě yālì de kēxué liángfāng.", "Biết chia sẻ, vận động điều độ và ngủ đủ giấc là những phương thuốc khoa học xua tan áp lực."),
         ("从容面对生活的起伏，才能在风雨过后迎接属于自己的明媚阳光。", "Cóngróng miànduì shēnghuó de qǐfú, cái néng zài fēngyǔ guòhòu yíngjiē shǔyú zìjǐ de míngmèi yángguāng.", "Bình thản đón nhận những thăng trầm cuộc đời, ta mới có thể đón ánh nắng rực rỡ sau cơn mưa.")
     ],
     [
         ("Tác động của áp lực đối với con người được phân tích như thế nào?", ["Hoàn toàn có hại", "Áp lực vừa phải kích thích tiềm năng, lo âu quá độ gây hại sức khỏe", "Không có ảnh hưởng gì"], 1, "Trong bài có câu: 适度的压力能够激发我们的潜能，但过度的焦虑则会损害身心健康."),
         ("Biện pháp khoa học nào giúp giải tỏa căng thẳng hiệu quả?", ["Tâm sự, vận động điều độ và ngủ đủ giấc", "Làm việc liên tục không nghỉ", "Tự cô lập bản thân"], 0, "Trong câu có viết: 学会倾诉、规律运动以及保持充足睡眠，是有效缓解压力的科学良方."),
         ("Ý nghĩa của sức bền tâm lý là gì?", ["Không bao giờ gặp khó khăn", "Có thể nhanh chóng điều chỉnh tâm thái khi đối mặt thất bại", "Luôn vui vẻ giả tạo"], 1, "Trong câu có viết: 在面对挫折时能够迅速调整心态.")
     ]),
    (8, "中国古典园林的美学智慧", "Trí tuệ thẩm mỹ của hoa viên cổ điển Trung Hoa", "oriental_aesthetics", "Thẩm mỹ phương Đông", "🏞️", 5,
     "Nghệ thuật 'dời non dời sông' tài tình trong kiến trúc hoa viên Tô Châu: Thiên nhiên thu nhỏ trong tấc gang.",
     [
         ("苏州古典园林是中国古代建筑艺术的杰出代表，被誉为凝固的优美诗篇。", "Sūzhōu gǔdiǎn yuánlín shì zhōngguó gǔdài jiànzhù yìshù de jiéchū dàibiǎo, bèi yù wéi nínggù de yōuměi shīpiān.", "Hoa viên cổ điển Tô Châu là đại diện kiệt xuất của nghệ thuật kiến trúc cổ đại Trung Hoa, được ví như bài thơ ngưng đọng."),
         ("造园名家巧妙利用假山、池水、花木和亭台，在有限空间内创造无限意境。", "Zàoyuán míngjiā qiǎomiào lìyòng jiǎshān, chíshuǐ, huāmù hé tíngtái, zài yǒuxiàn kōngjiān nèi chuàngzào wúxiàn yìjìng.", "Các bậc thầy làm vườn khéo léo dùng hòn non bộ, hồ nước, hoa cỏ và lầu đình để tạo ý cảnh vô tận trong không gian hữu hạn."),
         ("漫步在曲折的回廊之中，游人一步一景，处处感受到自然的生机与静谧。", "Mànbù zài qūzhé de huíláng zhī zhōng, yóurén yí bù yì jǐng, chùchù gǎnshòu dào zìrán de shēngjī yǔ jìngmì.", "Tản bộ giữa những dãy hành lang uốn lượn, du khách bước một bước đổi một cảnh, cảm nhận sinh khí và tĩnh mịch."),
         ("这种虽由人作、宛自天开的艺术追求，深刻体现了天人合一的哲学思想。", "Zhè zhǒng suī yóu rén zuò, wǎn zì tiān kāi de yìshù zhuīqiú, shēnkè tǐxiàn le tiānrén-héyī de zhéxué sīxiǎng.", "Sự theo đuổi nghệ thuật 'tuy do người làm mà như trời tạo' thể hiện sâu sắc tư tưởng triết học thiên nhân hợp nhất."),
         ("古典园林不仅是游览胜地，更是滋养心灵、体悟东方文化的静心之所。", "Gǔdiǎn yuánlín bùjǐn shì yóulǎn shèngdì, gèng shì zīyǎng xīnlíng, tǐwù dōngfāng wénhuà de jìngxīn zhī suǒ.", "Hoa viên cổ điển không chỉ là thắng cảnh du ngoạn mà còn là nơi nuôi dưỡng tâm hồn và chiêm nghiệm văn hóa phương Đông.")
     ],
     [
         ("Các bậc thầy hoa viên Tô Châu đã sử dụng thủ pháp gì?", ["Dùng bê tông cốt thép hiện đại", "Kết hợp non bộ, hồ nước, cây cỏ tạo ý cảnh vô hạn trong không gian nhỏ", "Chặt hết cây cối"], 1, "Trong câu có viết: 利用假山、池水、花木和亭台，在有限空间内创造无限意境."),
         ("Tư tưởng triết học cốt lõi nào được thể hiện qua hoa viên cổ điển?", ["Thiên nhân hợp nhất (con người hòa hợp với tự nhiên)", "Chinh phục tự nhiên bằng vũ lực", "Chủ nghĩa tiêu dùng"], 0, "Trong bài có câu: 深刻体现了天人合一的哲学思想."),
         ("Trải nghiệm đặc sắc của du khách khi dạo bước trong hoa viên là gì?", ["Nhìn cảnh vật đơn điệu", "Mỗi bước đi là một cảnh trí mới lạ đầy sức sống", "Cảm thấy ngột ngạt"], 1, "Trong câu có viết: 游人一步一景，处处感受到自然的生机与静谧.")
     ]),
    (9, "数字化时代的社交变迁", "Biến chuyển trong giao tiếp xã hội thời đại số", "digital_society", "Xã hội số & Giao tiếp", "📱", 5,
     "Mạng xã hội kéo gần khoảng cách địa lý nhưng cũng đặt ra câu hỏi về chiều sâu của các mối quan hệ thực tế.",
     [
         ("智能手机与社交媒体的普及，彻底重塑了人们日常交流沟通的方式。", "Zhìnéng shǒujī yǔ shèjiāo méitǐ de pǔjí, chèdǐ chóngsù le rénmen rìcháng jiāoliú gōutōng de fāngshì.", "Sự phổ cập của điện thoại thông minh và mạng xã hội đã định hình lại hoàn toàn phương thức giao tiếp thường nhật."),
         ("无论身处世界的哪一个角落，我们都可以瞬间通过屏幕分享文字与视频。", "Wúlùn shēn chǔ shìjiè de nǎ yí gè jiǎoluò, wǒmen dōu kěyǐ shùnjiān tōngguò píngmù fēnxiǎng wénzì yǔ shìpín.", "Bất kể ở góc nào trên thế giới, ta đều có thể lập tức chia sẻ câu chữ và video qua màn hình."),
         ("然而，虚拟世界中热闹的点赞与互动，有时却掩盖了现实中的孤独感。", "Rán'ér, xūnǐ shìjiè zhōng rènao de diǎnzàn yǔ hùdòng, yǒushí què yǎngài le xiànshí zhōng de gūdúgǎn.", "Dẫu vậy, những lượt thích và tương tác náo nhiệt trên mạng ảo đôi khi lại che giấu sự cô đơn ngoài đời thực."),
         ("面对面的眼神接触、温暖的拥抱和真实的陪伴，是任何算法都无法替代的。", "Miànduìmiàn de yǎnshén jiēchù, wēnnuǎn de yōngbào hé zhēnshí de péibàn, shì rènhé suànfǎ dōu wúfǎ tìdài de.", "Ánh mắt chạm nhau trực tiếp, cái ôm ấm áp và sự đồng hành chân thực là điều không thuật toán nào thay thế nổi."),
         ("合理掌控使用屏幕的时间，多回归现实生活，才能建立真正深厚的友谊。", "Hélǐ zhǎngkòng shǐyòng píngmù de shíjiān, duō huíguī xiànshí shēnghuó, cái néng jiànlì zhēnzhèng shēnhòu de yǒuyì.", "Kiểm soát hợp lý thời gian nhìn màn hình, trở về với đời sống thực tế mới có thể xây dựng tình bạn sâu sắc bền lâu.")
     ],
     [
         ("Mạng xã hội đã mang lại sự tiện lợi gì cho giao lưu con người?", ["Cho phép chia sẻ hình ảnh và tin nhắn tức thì từ mọi nơi", "Loại bỏ hoàn toàn công việc văn phòng", "Tạo ra lương thực miễn phí"], 0, "Trong bài có câu: 无论身处世界的哪一个角落，我们都可以瞬间通过屏幕分享文字与视频."),
         ("Thực trạng tâm lý đáng chú ý trong thế giới ảo là gì?", ["Không ai còn cảm thấy buồn", "Sự tương tác náo nhiệt trên mạng đôi khi che giấu nỗi cô đơn thực tế", "Mọi người đều trở nên xa cách tuyệt đối"], 1, "Trong câu có viết: 虚拟世界中热闹的点赞与互动，有时却掩盖了现实中的孤独感."),
         ("Tác giả khuyên điều gì để có tình bạn sâu sắc đích thực?", ["Tăng thời gian lướt mạng gấp đôi", "Kiểm soát thời gian dùng màn hình và quay về với đời sống thực tế", "Ngừng giao tiếp với người ngoài"], 1, "Trong câu cuối có viết: 合理掌控使用屏幕的时间，多回归现实生活.")
     ]),
    (10, "饮食文化与慢生活哲学", "Văn hóa ẩm thực và triết lý sống chậm", "slow_living", "Ẩm thực & Triết lý", "🍲", 5,
     "Tận hưởng niềm vui nấu nướng và trân trọng từng hương vị tự nhiên trong nhịp sống hối hả ngày nay.",
     [
         ("在习惯了快餐与外卖的忙碌节奏中，我们常常忽略了食物本身的纯正滋味。", "Zài xíguàn le kuàicān yǔ wàimài de mánglù jiézòu zhōng, wǒmen chángcháng hūlüè le shíwù běnshēn de chúnzhèng zīwèi.", "Trong nhịp sống bận rộn quen thuộc với đồ ăn nhanh, ta thường lơ là hương vị thuần khiết của món ăn."),
         ("慢食运动倡导人们放慢匆忙的脚步，亲自挑选新鲜食材并用心烹饪。", "Mànshí yùndòng chàngdǎo rénmen fàngmàn cōngmáng de jiǎobù, qīnzì tiāoxuǎn xīnxian shícái bìng yòngxīn pēngrèn.", "Phong trào sống chậm cổ vũ mọi người bước chậm lại, tự tay lựa chọn nguyên liệu tươi và tận tâm nấu nướng."),
         ("与家人朋友围坐在一起，细细品味热腾腾的饭菜，是最朴素的幸福时光。", "Yǔ jiārén péngyou wéizuò zài yìqǐ, xìxì pǐnwèi rètēngtēng de fàncài, shì zuì pǔsù de xìngfú shíguāng.", "Quây quần bên người thân bạn bè, chậm rãi thưởng thức bữa cơm nóng hổi là khoảnh khắc hạnh phúc mộc mạc nhất."),
         ("厨房里升腾的温暖烟火气，最能治愈一天奔波劳累所带来的疲惫。", "Chúfáng lǐ shēngténg de wēnnuǎn yānhuǒqì, zuì néng zhìyù yì tiān bēnbō láolèi suǒ dàilái de píbèi.", "Hơi ấm nghi ngút từ gian bếp là liều thuốc xoa dịu tốt nhất cho những mỏi mệt sau một ngày bươn chải."),
         ("懂得享受生活的细节与温度，平淡的每一天也能过得充满诗意。", "Dǒngde xiǎngshòu shēnghuó de xìjié yǔ wēndù, píngdàn de měi yì tiān yě néng guò de chōngmǎn shīyì.", "Biết nâng niu từng chi tiết và độ ấm của đời sống, mỗi ngày bình dị cũng ngập tràn thi vị.")
     ],
     [
         ("Phong trào 'Ăn chậm' (Slow food) khuyến khích điều gì?", ["Ăn đồ đóng hộp", "Bước chậm lại, tự chọn nguyên liệu tươi và nấu ăn bằng cả tấm lòng", "Nhịn ăn"], 1, "Trong bài có câu: 放慢匆忙的脚步，亲自挑选新鲜食材并用心烹饪."),
         ("Khoảnh khắc hạnh phúc mộc mạc nhất được miêu tả là gì?", ["Mua sắm đồ hiệu đắt tiền", "Quây quần cùng người thân thưởng thức bữa cơm nóng ấm", "Đi du lịch một mình"], 1, "Trong câu có viết: 与家人朋友围坐在一起，细细品味热腾腾的饭菜，是最朴素的幸福时光."),
         ("Hơi ấm bếp lửa gia đình mang lại giá trị tinh thần nào?", ["Gây tốn điện nước", "Xoa dịu sự mệt mỏi sau ngày dài lao động vất vả", "Làm căn nhà bừa bộn"], 1, "Trong câu có viết: 温暖烟火气，最能治愈一天奔波劳累所带来的疲惫.")
     ])
]
