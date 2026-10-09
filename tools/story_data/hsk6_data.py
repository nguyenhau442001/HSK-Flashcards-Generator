"""
tools/story_data/hsk6_data.py
10 stories data for HSK 6
"""

HSK6_STORIES = [
    (1, "深海探测与未知世界", "Thám hiểm biển sâu và thế giới bí ẩn", "ocean_exploration", "Khoa học đại dương", "🌊", 6,
     "Những bước đột phá của tàu lặn thám hiểm rãnh đại dương và khám phá hệ sinh thái kỳ vĩ.",
     [
         ("深海是地球上最具神秘色彩的未知领域之一，蕴藏着极其丰富的生物资源与矿产宝藏。", "Shēnhǎi shì dìqiú shàng zuì jù shénmì sècǎi de wèizhī lǐngyù zhī yī, yùncáng zhe jíqí fēngfù de shēngwù zīyuán yǔ kuàngchǎn bǎozàng.", "Biển sâu là một trong những lãnh hạt bí ẩn nhất trên trái đất, ẩn chứa nguồn tài nguyên sinh vật và khoáng sản vô cùng phong phú."),
         ("随着深海潜水器技术的不断突破，科学家们得以深入万米海底观察极端环境下的生命奇迹。", "Suízhe shēnhǎi qiánshuǐqì jìshù de búduàn tūpò, kēxuéjiā men déyǐ shēnrù wàn mǐ hǎidǐ guānchá jiéduān huánjìng xià de shēngmìng qíjì.", "Cùng với sự đột phá liên tục của công nghệ tàu lặn sâu, các nhà khoa học đã có thể lặn xuống đáy biển vạn mét để quan sát kỳ tích sự sống trong môi trường khắc nghiệt."),
         ("在完全缺乏阳光与承受巨大水压的海沟深处，许多奇特生物依靠地热能量繁衍生息。", "Zài wánquán quēfá yángguāng yǔ chéngshòu jùdà shuǐyā de hǎigōu shēnchù, xǔduō qítè shēngwù yīkào dìrè néngliàng fányǎn shēngxī.", "Tại đáy rãnh biển sâu hoàn toàn thiếu ánh sáng mặt trời và chịu áp lực nước khổng lồ, nhiều sinh vật kỳ lạ dựa vào năng lượng địa nhiệt để sinh sôi nảy nở."),
         ("这些珍贵发现彻底颠覆了人类传统上对生命存在极限的固有认知。", "Zhèxiē zhēnguì fāxiàn chèdǐ diānfù le rénlèi chuántǒng shàng duì shēngmìng cúnzài jíxiàn de gùyǒu rènzhī.", "Những phát hiện quý báu này đã lật đổ hoàn toàn nhận thức cố hữu truyền thống của nhân loại về giới hạn tồn tại của sự sống."),
         ("保护深海脆弱的生态环境，是全人类在探索蓝色星球进程中不可推卸的崇高使命。", "Bǎohù shēnhǎi cuìruò de shēngtài huánjìng, shì quán rénlèi zài tànsuǒ lánsè xīngqiú jìnchéng zhōng bùkě tuīxiè de chónggāo shǐmìng.", "Bảo vệ môi trường sinh thái mong manh của biển sâu là sứ mệnh cao cả không thể thoái thác của toàn nhân loại trong hành trình khám phá hành tinh xanh.")
     ],
     [
         ("Sinh vật ở rãnh biển sâu sinh tồn dựa vào nguồn năng lượng nào?", ["Ánh sáng mặt trời", "Năng lượng địa nhiệt", "Thức ăn do con người cung cấp"], 1, "Trong bài có câu: 许多奇特生物依靠地热能量繁衍生息."),
         ("Phát hiện sinh vật biển sâu mang lại ý nghĩa gì cho giới khoa học?", ["Lật đổ nhận thức cũ về giới hạn tồn tại của sự sống", "Chứng minh không có sự sống ở đáy biển", "Cho thấy biển sâu rất ô nhiễm"], 0, "Trong câu có viết: 彻底颠覆了人类传统上对生命存在极限的固有认知."),
         ("Sứ mệnh của nhân loại đối với biển sâu là gì?", ["Khai thác cạn kiệt tài nguyên", "Bảo vệ môi trường sinh thái mong manh của biển sâu", "Bỏ qua không quan tâm"], 1, "Trong câu cuối có viết: 保护深海脆弱的生态环境，是全人类不可推卸的崇高使命.")
     ]),
    (2, "古典诗词的审美意境", "Ý cảnh thẩm mỹ trong thi từ cổ điển", "classical_poetry", "Văn học & Thi ca", "📜", 6,
     "Nghệ thuật 'tá cảnh sinh tình' và vẻ đẹp ngôn từ cô đọng trong kho tàng thi ca cổ điển.",
     [
         ("中国古典诗词以其精炼凝重的语言和悠远深邃的意境，成为东方文学殿堂中的璀璨明珠。", "Zhōngguó gǔdiǎn shīcí yǐ qí jīngliàn níngzhòng de yǔyán hé yōuyuǎn shēnsuì de yìjìng, chéngwéi dōngfāng wénxué diàntáng zhōng de cuǐcàn míngzhū.", "Thơ từ cổ điển Trung Hoa với ngôn từ hàm súc cô đọng và ý cảnh xa xăm sâu lắng đã trở thành viên ngọc rực rỡ trong lâu đài văn học phương Đông."),
         ("古代文人擅长借景抒情，将微妙复杂的人生感悟寄托于一草一木与烟雨山川之间。", "Gǔdài wénrén shàncháng jièjǐng shūqíng, jiāng wēimiào fùzá de rénshēng gǎnwù jìtuō yú yì cǎo yí mù yǔ yānyǔ shānchuān zhījiān.", "Các văn nhân cổ đại tinh thông thủ pháp mượn cảnh tả tình, gửi gắm những cảm ngộ nhân sinh vi tế phức tạp vào từng nhành cây ngọn cỏ hay non nước mịt mờ khói sóng."),
         ("读者在吟诵名篇佳作时，仿佛能穿越千百年时光与古人产生强烈的精神共鸣。", "Dúzhe zài yínsòng míngpiān jiāzuò shí, fǎngfú néng chuānyuè qiān bǎi nián shíguāng yǔ gǔrén chǎnshēng qiángliè de jīngshén gòngmíng.", "Người đọc khi ngâm nga những áng thơ trác tuyệt dường như có thể vượt qua ngàn trăm năm thời gian để giao cảm tâm hồn mãnh liệt cùng người xưa."),
         ("诗词中所蕴含的豁达胸襟与忧国忧民情怀，至今依然能够洗涤现代人的浮躁心灵。", "Shīcí zhōng suǒ yùnhán de huòdá xiōngjīn yǔ yōuguó yōumín qínghuái, zhìjīn yīrán nénggòu xǐdí xiàndàirén de fúzào xīnlíng.", "Tấm lòng khoáng đạt và nỗi niềm ưu quốc ưu dân chứa chan trong thi từ đến nay vẫn đủ sức gột rửa tâm hồn xốc nổi của người hiện đại."),
         ("传承诗词文化不仅是温习历史，更是在快节奏的生活中寻找精神家园的温润滋养。", "Chuánchéng shīcí wénhuà bùjǐn shì wēnxí lìshǐ, gèng shì zài kuài jiézòu de shēnghuó zhōng xúnzhǎo jīngshén jiāyuán de wēnrùn zīyǎng.", "Kế thừa văn hóa thi từ không chỉ là ôn lại lịch sử, mà còn là tìm kiếm sự nuôi dưỡng ấm áp cho chốn nương tựa tâm hồn giữa dòng đời hối hả.")
     ],
     [
         ("Thủ pháp nghệ thuật đặc trưng của văn nhân xưa trong thơ từ là gì?", ["Miêu tả trực diện không dùng hình ảnh", "Mượn cảnh tả tình gửi gắm cảm ngộ nhân sinh", "Chỉ ghi chép sự kiện lịch sử"], 1, "Trong bài có câu: 借景抒情，将微妙复杂的人生感悟寄托于一草一木."),
         ("Giá trị tinh thần của thi từ đối với con người hiện đại là gì?", ["Gột rửa tâm hồn xốc nổi nhờ sự khoáng đạt và sâu lắng", "Giúp tăng tốc độ làm việc", "Không còn phù hợp với hiện tại"], 0, "Trong câu có viết: 豁达胸襟与忧国忧民情怀，至今依然能够洗涤现代人的浮躁心灵."),
         ("Kế thừa thi từ mang lại ý nghĩa sâu xa nào?", ["Tìm kiếm sự nuôi dưỡng ấm áp cho bến đỗ tinh thần", "Chỉ để học thuộc lòng thi cử", "Làm tốn thời gian học tập"], 0, "Trong câu cuối có viết: 在快节奏的生活中寻找精神家园的温润滋养.")
     ]),
    (3, "生物多样性与自然共生", "Đa dạng sinh học và cộng sinh cùng tự nhiên", "biodiversity", "Môi trường & Sinh thái", "🐼", 6,
     "Bảo vệ các loài quý hiếm và khôi phục hệ sinh thái cân bằng cho tương lai bền vững.",
     [
         ("生物多样性是地球生命支持系统的基石，维持着自然界脆弱而精妙的动态平衡。", "Shēngwù duōyàngxìng shì dìqiú shēngmìng zhīchí xìtǒng de jīshí, wéichí zhe zìránjiè cuìruò ér jīngmiào de dòngtài pínghéng.", "Đa dạng sinh học là tảng đá nền móng của hệ thống nâng đỡ sự sống trên trái đất, duy trì sự cân bằng động tinh vi mong manh của giới tự nhiên."),
         ("森林砍伐、气候变暖和环境污染正在以前所未有的速度导致物种栖息地破碎化。", "Sēnlín kǎnfá, qìhòu biànnuǎn hé huánjìng wūrǎn zhèngzài yǐ qiánsuǒwèiyǒu de sùdù dǎozhì wùzhǒng qīxīdì pòsuìhuà.", "Nạn phá rừng, nóng lên toàn cầu và ô nhiễm môi trường đang khiến môi trường sống của các loài bị chia cắt với tốc độ chưa từng có."),
         ("建立国家公园与自然保护区，为濒危野生动植物提供了休养生息的庇护港湾。", "Jiànlì guójiā gōngyuán yǔ zìrán bǎohùqū, wèi bīnwēi yèshēng dòngzhíwù tígōng le xiūyǎng shēngxī de bìhù gǎngwān.", "Xây dựng các vườn quốc gia và khu bảo tồn thiên nhiên đã mang lại bến đỗ bình yên để các loài động thực vật hoang dã nguy cấp sinh sôi hồi phục."),
         ("保护野生动物不仅是出于慈悲之心，更是为了维护人类自身生存所依赖的生态安全。", "Bǎohù yèshēng dòngwù bùjǐn shì chūyú cíbēi zhī xīn, gèng shì wèile wéihù rénlèi zìshēn shēngcún suǒ yīlài de shēngtài ānquán.", "Bảo vệ động vật hoang dã không chỉ xuất phát từ lòng từ bi, mà còn nhằm bảo vệ an ninh sinh thái mà sự sinh tồn của con người dựa vào."),
         ("只有当全社会形成尊重自然、顺应自然的共识，我们才能迎来繁荣美好的明天。", "Zhǐyǒu dāng quán shèhuì xíngchéng zūnzhòng zìrán, shùnyìng zìrán de gòngshí, wǒmen cái néng yínglái fánróng měihǎo de míngtiān.", "Chỉ khi toàn xã hội hình thành nhận thức chung về tôn trọng tự nhiên và thuận theo tự nhiên, chúng ta mới có thể đón nhận ngày mai phồn vinh tốt đẹp.")
     ],
     [
         ("Nguyên nhân nào khiến nơi cư trú của các sinh vật bị chia cắt?", ["Phá rừng, biến đổi khí hậu và ô nhiễm môi trường", "Sự bảo tồn quá mức", "Do động vật di cư tự nhiên"], 0, "Trong bài có câu: 森林砍伐、气候变暖和环境污染正在导致物种栖息地破碎化."),
         ("Vai trò của các khu bảo tồn thiên nhiên là gì?", ["Khai thác du lịch thương mại", "Cung cấp bến đỗ bảo bọc để các loài quý hiếm hồi phục sinh sôi", "Bắt nhốt động vật"], 1, "Trong câu có viết: 为濒危野生动植物提供了休养生息的庇护港湾."),
         ("Mục đích cốt lõi của việc bảo vệ động vật hoang dã là gì?", ["Duy trì an ninh sinh thái cho chính sự tồn vong của loài người", "Tạo thú vui tiêu khiển", "Để lấy giống chăn nuôi"], 0, "Trong câu có viết: 为了维护人类自身生存所依赖的生态安全.")
     ]),
    (4, "数字经济与金融普惠", "Kinh tế số và tài chính toàn diện", "fintech", "Kinh tế & Công nghệ", "💳", 6,
     "Công nghệ tài chính số hóa giúp thu hẹp khoảng cách tiếp cận dịch vụ và thúc đẩy phát triển công bằng.",
     [
         ("数字技术的迅猛迭代，正在重构全球金融行业的底层架构与服务模式。", "Shùzì jìshù de xùnměng diédài, zhèngzài chónggòu quánqiú jīnróng hángyè de dǐcéng jiàgòu yǔ fúwù móshì.", "Sự nâng cấp vũ bão của công nghệ số đang định hình lại cấu trúc nền tảng và phương thức dịch vụ của ngành tài chính toàn cầu."),
         ("移动支付与普惠金融的结合，使得偏远地区的农户也能便捷地获得小额贷款与保险支持。", "Yídòng zhīfù yǔ pǔhuì jīnróng de jiéhé, shǐde piānyuǎn dìqū de nónghù yě néng biànjié de huòdé xiǎoxé dàikuǎn yǔ bǎoxiǎn zhīchí.", "Sự kết hợp giữa thanh toán di động và tài chính toàn diện giúp nông dân ở vùng sâu vùng xa cũng dễ dàng tiếp cận vay vốn nhỏ và bảo hiểm."),
         ("大数据和人工智能算法能够有效评估信用风险，显著降低了传统金融服务的门槛。", "Dà shùjù hé réngōng zhìnéng suànfǎ nénggòu yǒuxiào pínggū xìnyòng fēngxiǎn, xiǎnzhù jiàngdī le chuántǒng jīnróng fúwù de ménkǎn.", "Dữ liệu lớn và thuật toán AI có thể đánh giá rủi ro tín dụng hiệu quả, hạ thấp đáng kể ngưỡng cửa dịch vụ tài chính truyền thống."),
         ("然而，数字化在带来高效便捷的同时，也对用户隐私保护和网络安全提出了严峻考验。", "Rán'ér, shùzìhuà zài dàilái gāoxiào biànjié de tóngshí, yě duì yònghù yǐnsī bǎohù hé wǎngluò ānquán tíchū le yánjùn kǎoyàn.", "Tuy nhiên, bên cạnh việc đem lại hiệu quả tiện lợi, chuyển đổi số cũng đặt ra thử thách gay gắt đối với bảo vệ quyền riêng tư và an ninh mạng."),
         ("构建安全可靠、普惠共享的数字金融生态，是促进经济包容性增长的关键所在。", "Gòujiàn ānquán kěkào, pǔhuì gòngxiǎng de shùzì jīnróng shēngtài, shì cùjìn jīngjì bāoróngxìng zēngzhǎng de guānjiàn suǒzài.", "Xây dựng hệ sinh thái tài chính số an toàn tin cậy và cùng chia sẻ là chìa khóa then chốt thúc đẩy tăng trưởng kinh tế bao trùm.")
     ],
     [
         ("Tài chính toàn diện mang lại lợi ích thiết thực gì cho người dân vùng xa?", ["Tiếp cận dễ dàng các khoản vay nhỏ và bảo hiểm hỗ trợ", "Được cấp tiền miễn phí vô điều kiện", "Mua điện thoại giá rẻ"], 0, "Trong bài có câu: 使得偏远地区的农户也能便捷地获得小额贷款与保险支持."),
         ("Công nghệ nào giúp hạ thấp ngưỡng đánh giá tín dụng?", ["Dữ liệu lớn và thuật toán trí tuệ nhân tạo", "Ghi chép sổ sách thủ công", "Giấy giới thiệu"], 0, "Trong câu có viết: 大数据和人工智能算法能够有效评估信用风险."),
         ("Thách thức lớn nhất đi kèm với sự phát triển của tài chính số là gì?", ["Bảo vệ quyền riêng tư người dùng và an ninh mạng", "Không ai sử dụng điện thoại", "Ngân hàng bị đóng cửa hoàn toàn"], 0, "Trong bài có viết: 对用户隐私保护和网络安全提出了严峻考验.")
     ]),
    (5, "认知重构与情绪智慧", "Tái cấu trúc nhận thức và trí tuệ cảm xúc", "psychology", "Tâm lý học", "🧠", 6,
     "Khám phá cơ chế điều hòa tâm lý, chuyển hóa cảm xúc tiêu cực thành nguồn năng lượng tích cực.",
     [
         ("现代心理学研究表明，决定我们情绪体验的往往不是事件本身，而是我们对事件的解释。", "Xiàndài xīnlǐxué yánjiū biǎomíng, juédìng wǒmen qíngxù tǐyàn de wǎngwǎng bú shì shìjiàn běnshēn, ér shì wǒmen duì shìjiàn de jiěshì.", "Nghiên cứu tâm lý học hiện đại chỉ ra rằng điều quyết định trải nghiệm cảm xúc thường không phải là bản thân sự việc mà là cách ta diễn giải sự việc đó."),
         ("当我们陷入挫败感或过度自责时，认知偏差常常会放大客观困难并削弱自信心。", "Dāng wǒmen xiànrù cuòbàigǎn huò guòdù zìzé shí, rènzhī piānchà chángcháng huì fàngdà kèguān kùnnan bìng xuēruò zìxìnxīn.", "Khi ta rơi vào cảm giác thất bại hay tự trách quá mức, sai lệch nhận thức thường phóng đại khó khăn và làm suy yếu lòng tự tin."),
         ("通过有意识的认知重构训练，我们可以学会识别消极思维并用客观理性的态度审视现状。", "Tōngguò yǒuyìshí de rènzhī chónggòu xùnliàn, wǒmen kěyǐ xuéhuì shíbié xiāojí sīwéi bìng yòng kèguān lǐxìng de tàidù shěnshì xiànzhuàng.", "Thông qua rèn luyện tái cấu trúc nhận thức có ý thức, ta có thể học cách nhận diện suy nghĩ tiêu cực và xem xét hiện trạng một cách lý tính khách quan."),
         ("接纳不完美的自我并不意味着妥协，而是放下执念、重新出发的心灵契机。", "Jiēnà bù wánměi de zìwǒ bìng bù yìwèizhe tuǒxié, ér shì fàngxià zhíniàn, chóngxīn chūfā de xīnlíng qìjī.", "Chấp nhận bản thân không hoàn hảo không đồng nghĩa với thỏa hiệp, mà là buông bỏ chấp niệm, mở ra cơ hội để tâm hồn tái khởi hành."),
         ("拥有高度的情绪智慧，能让我们在风浪中稳住舵盘，成为内心平静而坚定的人。", "Yōngyǒu gāodù de qíngxù zhìhuì, néng ràng wǒmen zài fēnglàng zhōng wěn zhù duòpán, chéngwéi nèixīn píngjìng ér jiāndìng de rén.", "Sở hữu trí tuệ cảm xúc cao giúp ta giữ vững bánh lái giữa giông bão, trở thành người có nội tâm an định và kiên định.")
     ],
     [
         ("Theo tâm lý học, điều gì quyết định trạng thái cảm xúc của một người?", ["Bản thân sự việc bên ngoài", "Cách người đó nhìn nhận và diễn giải sự việc", "Sự may rủi"], 1, "Trong câu đầu có viết: 决定我们情绪体验的往往不是事件本身，而是我们对事件的解释."),
         ("Tác dụng của phương pháp tái cấu trúc nhận thức là gì?", ["Nhận diện suy nghĩ tiêu cực và đánh giá hiện thực khách quan lý tính", "Trốn tránh khó khăn", "Tự lừa dối bản thân"], 0, "Trong bài có câu: 学会识别消极思维并用客观理性的态度审视现状."),
         ("Chấp nhận bản thân không hoàn hảo mang lại ý nghĩa gì?", ["Từ bỏ mọi cố gắng phấn đấu", "Buông bỏ chấp niệm để bắt đầu lại với tinh thần mới", "Làm mất đi nguyên tắc sống"], 1, "Trong câu có viết: 放下执念、重新出发的心灵契机.")
     ]),
    (6, "工业遗产的艺术新生", "Sức sống nghệ thuật mới của di sản công nghiệp", "architecture_heritage", "Kiến trúc & Di sản", "🏛️", 6,
     "Hành trình biến đổi những nhà máy cũ hoang tàn thành trung tâm triển lãm và không gian sáng tạo sôi động.",
     [
         ("废弃的旧厂房与生锈的机械管道，常常被视作城市化进程中留下的工业伤痕。", "Fèiqì de jiù chǎngfáng yǔ shēngxiù de jīxiè guǎndào, chángcháng bèi shì zuò chéngshìhuà jìnchéng zhōng liúxià de gōngyè shānghén.", "Những khu nhà xưởng bỏ hoang và đường ống máy móc rỉ sét thường bị xem là những vết thương công nghiệp sót lại trong quá trình đô thị hóa."),
         ("然而在富有远见的建筑师与艺术家眼中，这些粗犷的空间恰恰蕴藏着无限的创意潜能。", "Rán'ér zài fùyǒu yuǎnjiàn de jiànzhùshī yǔ yìshùjiā yǎnzhōng, zhèxiē cūguǎng de kōngjiān qiàqià yùncáng zhe wúxiàn de chuàngyì qiánnéng.", "Thế nhưng trong mắt các kiến trúc sư và nghệ sĩ có tầm nhìn, những không gian thô mộc này lại ẩn chứa tiềm năng sáng tạo vô hạn."),
         ("经过巧妙的结构加固与功能改造，老旧车间华丽转身为充满现代气息的艺术画廊与文化园区。", "Jīngguò qiǎomiào de jiégòu jiāgù yǔ gōngnéng gǎizào, lǎojiù chējiān huálì zhuǎnshēn wéi chōngmǎn xiàndài qìxī de yìshù huàláng yǔ wénhuà yuánqū.", "Qua bàn tay gia cố kết cấu và cải tạo công năng khéo léo, phân xưởng cũ đã lột xác thành phòng tranh nghệ thuật và công viên văn hóa đậm hơi thở hiện đại."),
         ("红砖墙与当代雕塑的视觉碰撞，让游客在重温历史记忆的同时感受到蓬勃的先锋活力。", "Hóngzhuān qiáng yǔ dāngdài diāosù de shìjué pèngzhuàng, ràng yóukè zài chóngwēn lìshǐ jìyì de tóngshí gǎnshòu dào péngbó de xiānfēng huólì.", "Sự va chạm thị giác giữa tường gạch đỏ và điêu khắc đương đại giúp du khách vừa ôn lại ký ức lịch sử vừa cảm nhận sức sống tiên phong tràn trề."),
         ("工业遗产的保护性再利用，不仅留住了城市的历史文脉，更为社区注入了持久的文化生机。", "Gōngyè yíchǎn de bǎohùxìng zàilìyòng, bùjǐn liú zhù le chéngshì de lìshǐ wénmài, gèng wèi shèqū zhùrù le chíjiǔ de wénhuà shēngjī.", "Tái sử dụng có bảo tồn di sản công nghiệp không chỉ lưu giữ mạch nguồn lịch sử đô thị mà còn truyền sinh khí văn hóa lâu dài vào cộng đồng.")
     ],
     [
         ("Các xưởng máy cũ được nhìn nhận như thế nào bởi các nghệ sĩ sáng tạo?", ["Là đống phế liệu vô giá trị cần phá bỏ", "Chứa đựng tiềm năng sáng tạo nghệ thuật vô hạn", "Là nơi nguy hiểm cấm vào"], 1, "Trong bài có câu: 这些粗犷的空间恰恰蕴藏着无限的创意潜能."),
         ("Sự kết hợp giữa tường gạch đỏ và điêu khắc hiện đại tạo nên hiệu ứng gì?", ["Làm không gian thêm cũ kỹ", "Vừa gợi nhắc ký ức lịch sử vừa toát lên sức sống tiên phong", "Gây rối mắt cho người xem"], 1, "Trong câu có viết: 让游客在重温历史记忆的同时感受到蓬勃的先锋活力."),
         ("Lợi ích lâu dài của việc bảo tồn và tái sử dụng di sản công nghiệp là gì?", ["Giữ gìn mạch nguồn văn hóa lịch sử và thổi sức sống cho cộng đồng", "Thu hồi phế liệu bán lấy tiền", "Tăng mật độ nhà ở"], 0, "Trong câu cuối có viết: 不仅留住了城市的历史文脉，更为社区注入了持久的文化生机.")
     ]),
    (7, "基因编辑与生命伦理", "Chỉnh sửa gen và đạo đức sinh học", "bioethics", "Y học & Đạo đức", "⚕️", 6,
     "Trước ngưỡng cửa đột phá công nghệ gen, ranh giới đạo đức và trách nhiệm nhân loại cần được định vị.",
     [
         ("基因编辑技术的迅猛发展，为攻克遗传性罕见疾病带来了前所未有的曙光。", "Jīyīn biānjí jìshù de xùnměng fāzhǎn, wèi gōngkè yíchuánxìng hǎnjiàn jíbìng dàilái le qiánsuǒwèiyǒu de shǔguāng.", "Sự phát triển vượt bậc của công nghệ chỉnh sửa gen đã đem lại tia hy vọng chưa từng có trong việc chinh phục các căn bệnh di truyền hiếm gặp."),
         ("科学家们可以通过精确修改特定的碱基序列，从根源上阻断致病突变的传递。", "Kēxuéjiā men kěyǐ tōngguò jīngquè xiūgǎi tèdìng de jiǎnjī xùliè, cóng gēnyuán shàng zǔduàn zhìbìng tūbiàn de chuándì.", "Các nhà khoa học có thể thông qua chỉnh sửa chuẩn xác trình tự base đặc thù để chặn đứng sự lây truyền đột biến gây bệnh từ gốc rễ."),
         ("然而，当这项技术触及人类生殖细胞以及非医疗目的的基因增强时，引发了广泛的伦理争议。", "Rán'ér, dāng zhè xiàng jìshù chùjí rénlèi shēngzhí xìbāo yǐjí fēi yīliáo mùdì de jīyīn zēngqiáng shí, yǐnfā le guǎngfàn de lúnlǐ zhēngyì.", "Dẫu vậy, khi công nghệ này chạm đến tế bào sinh sản cũng như nâng cấp gen phi mục đích y tế, nó đã dấy lên tranh cãi đạo đức sâu rộng."),
         ("科技的进步一旦脱离道德约束与法律监管，可能会加剧社会不公甚至动摇人类物种的定义。", "Kējì de jìnbù yídàn tuōlí dàodé yuēshù yǔ fǎlǜ jiānguǎn, kěnéng huì jiājù shèhuì bùgōng shènzhì dòngyáo rénlèi wùzhǒng de dìngyì.", "Tiến bộ công nghệ một khi thoát ly khỏi sự ràng buộc đạo đức và giám sát pháp luật có thể khoét sâu bất công xã hội và lung lay định nghĩa loài người."),
         ("保持对生命的崇高敬畏，在探索科学真理与坚守伦理底线之间维持理性平衡，是文明延续的保障。", "Bǎochí duì shēngmìng de chónggāo jìngwèi, zài tànsuǒ kēxué zhēnlǐ yǔ jiānshǒu lúnlǐ dǐxiàn zhījiān wéichí lǐxìng pínghéng, shì wénmíng yánxù de bǎozhàng.", "Giữ vững lòng kính sợ cao quý với sự sống, duy trì cân bằng lý tính giữa tìm tòi chân lý khoa học và giữ vững lằn ranh đạo đức là bảo đảm duy trì văn minh.")
     ],
     [
         ("Công nghệ chỉnh sửa gen đem lại triển vọng lớn trong lĩnh vực nào?", ["Chữa trị các bệnh di truyền hiếm gặp từ gốc rễ", "Thay đổi màu mắt động vật", "Thay thế hoàn toàn thuốc men"], 0, "Trong bài có câu: 为攻克遗传性罕见疾病带来了前所未有的曙光."),
         ("Mối lo ngại đạo đức nảy sinh khi công nghệ can thiệp vào điều gì?", ["Tế bào sinh sản và tăng cường gen phi mục đích y tế", "Sản xuất kháng sinh thông thường", "Khám bệnh từ xa"], 0, "Trong câu có viết: 当这项技术触及人类生殖细胞以及非医疗目的的基因增强时，引发了广泛争议."),
         ("Điều kiện tiên quyết để khoa học phát triển lành mạnh vì nhân loại là gì?", ["Không cần bất kỳ sự kiểm soát nào", "Kính sợ sự sống và giữ vững cân bằng giữa khoa học và lằn ranh đạo đức", "Dừng mọi nghiên cứu sinh học"], 1, "Trong câu cuối có viết: 在探索科学真理与坚守伦理底线之间维持理性平衡.")
     ]),
    (8, "丝绸之路的历史回响", "Dư âm lịch sử của Con đường Tơ Lụa", "silk_road", "Lịch sử & Thương mại", "🐫", 6,
     "Hành trình giao thương ngàn dặm nối liền Đông Tây, gieo mầm cho sự thấu hiểu và hòa bình giữa các nền văn minh.",
     [
         ("在漫长的历史长河中，古老的丝绸之路宛如一条金色的纽带，将欧亚大陆紧密连接在一起。", "Zài màncháng de lìshǐ chánghé zhōng, gǔlǎo de sīchóuzhīlù wǎnrú yì tiáo jīnsè de niǔdài, jiāng Ōu-Yà dàlù jǐnmì liánjiē zài yìqǐ.", "Trong dòng chảy lịch sử đằng đẵng, Con đường Tơ Lụa cổ xưa tựa như một dải lụa vàng kết nối chặt chẽ lục địa Á - Âu."),
         ("清脆的骆驼铃声回荡在广袤无垠的沙漠绿洲之间，见证了东西方商旅的艰辛跋涉与繁荣贸易。", "Qīngcuì de luòtuo língshēng huídàng zài guǎngmào wúyín de shāmò lǜzhōu zhījiān, jiànzhèng le dōng-xīfāng shānglǚ de jiānxīn báshè yǔ fánróng màoyì.", "Tiếng chuông lạc đà trong trẻo ngân vang giữa những ốc đảo sa mạc mênh mông, chứng kiến bước chân bươn chải nhọc nhằn và giao thương phồn thịnh giữa Đông và Tây."),
         ("丝绸之路不仅仅是商品交易的物流通道，更是文化思想、天文医药与造纸印刷技术传播的巨大动脉。", "Sīchóuzhīlù bù jǐnjǐn shì shāngpǐn jiāoyì de wùliú tōngdào, gèng shì wénhuà sīxiǎng, tiānwén yīyào yǔ zàozhǐ yìnshuā jìshù chuánbō de jùdà dòngmài.", "Con đường Tơ Lụa không chỉ là tuyến đường vận tải hàng hóa mà còn là đại động mạch lan tỏa tư tưởng văn hóa, thiên văn y dược cùng kỹ thuật làm giấy in ấn."),
         ("不同宗教、信仰与习俗在这里和平交汇、相互汲取营养，造就了灿烂辉煌的多元文明体系。", "Bùtóng zōngjiào, xìnyǎng yǔ xísú zài zhèlǐ hépíng jiāohuì, xiānghù jíqǔ yíngyǎng, zàojiù le cànlàn huīhuáng de duōyuán wénmíng tǐxì.", "Các tôn giáo, tín ngưỡng và tập tục khác biệt đã giao thoa hòa bình, tiếp thu dinh dưỡng lẫn nhau, tạo nên hệ thống văn minh đa nguyên rực rỡ."),
         ("回顾丝路历史给予我们最宝贵的启迪，便是开放带来进步，包容方能共赢。", "Huígù sīlù lìshǐ jǐyǔ wǒmen zuì bǎoguì de qǐdí, biàn shì kāifàng dàilái jìnbù, bāoróng fāng néng gòngyíng.", "Nhìn lại lịch sử con đường tơ lụa cho ta bài học quý giá nhất: Cởi mở đem lại tiến bộ, bao dung mới có thể cùng thắng.")
     ],
     [
         ("Hình ảnh âm thanh nào tượng trưng cho các đoàn thương buôn trên con đường tơ lụa cổ xưa?", ["Tiếng còi tàu hỏa", "Tiếng chuông lạc đà ngân vang giữa sa mạc", "Tiếng động cơ máy bay"], 1, "Trong bài có câu: 清脆的骆驼铃声回荡在广袤无垠的沙漠绿洲之间."),
         ("Ngoài hàng hóa buôn bán, Con đường Tơ Lụa còn truyền bá những gì?", ["Văn hóa, tư tưởng, thiên văn y dược và kỹ thuật làm giấy", "Vũ khí hủy diệt", "Chỉ truyền đi tin đồn"], 0, "Trong câu có viết: 更是文化思想、天文医药与造纸印刷技术传播的巨大动脉."),
         ("Bài học quý giá nhất mà lịch sử con đường tơ lụa để lại là gì?", ["Bế quan tỏa cảng để an toàn", "Cởi mở đem lại tiến bộ, bao dung mới có thể cùng thắng", "Tranh giành lãnh thổ"], 1, "Trong câu cuối có viết: 开放带来进步，包容方能共赢.")
     ]),
    (9, "清洁能源与低碳转型", "Năng lượng sạch và chuyển đổi carbon thấp", "green_energy", "Năng lượng & Bền vững", "⚡", 6,
     "Công nghệ quang điện, điện gió và nỗ lực đạt mục tiêu trung hòa khí thải toàn cầu.",
     [
         ("应对全球气候变化的严峻挑战，加速推动能源结构的绿色低碳转型已成为世界各国的普遍共识。", "Yìngduì quánqiú qìhòu biànhuà de yánjùn tiǎozhàn, jiāsù tuīdòng néngyuán jiégòu de lǜsè dītàn zhuǎnxíng yǐ chéngwéi shìjiè gèguó de pǔbiàn gòngshí.", "Ứng phó với thử thách gay gắt của biến đổi khí hậu toàn cầu, đẩy nhanh chuyển đổi cơ cấu năng lượng xanh carbon thấp đã trở thành đồng thuận chung."),
         ("风能与太阳能发电技术的突飞猛进，使得可再生清洁电力的成本大幅下降，具备了极强的经济竞争力。", "Fēngnéng yǔ tàiyángnéng fādiàn jìshù de tūfēi-měngjìn, shǐde kězàishēng qīngjié diànlì de chéngběn dàfú xiàjiàng, jùbèi le jí qiáng de jīngjì jìngzhēnglì.", "Sự đột phá vượt bậc của kỹ thuật phát điện gió và năng lượng mặt trời giúp chi phí điện sạch tái tạo giảm sâu, có sức cạnh tranh kinh tế mạnh mẽ."),
         ("先进的储能设备与智能电网系统，为解决清洁能源不稳定、波动大的技术瓶颈提供了关键支撑。", "Xiānjìn de chǔnéng shèbèi yǔ zhìnéng diànwǎng xìtǒng, wèi jiějué qīngjié néngyuán bù wěndìng, bōdòng dà de jìshù píngjǐng tígōng le guānjiàn zhīchēng.", "Thiết bị lưu trữ năng lượng tiên tiến cùng lưới điện thông minh cung cấp trụ cột then chốt giải quyết nút thắt dao động bất ổn của năng lượng sạch."),
         ("逐步替代传统化石能源不仅有助于减少温室气体排放，还能有效改善日益严峻的空气质量状况。", "Zhúbù tìdài chuántǒng huàshí néngyuán bùjǐn yǒuzhù yú jiǎnshǎo wēnshì qìtǐ páifàng, hái néng yǒuxiào gǎishàn rìyì yánjùn de kōngqì zhìliàng zhuàngkuàng.", "Từng bước thay thế nhiên liệu hóa thạch truyền thống không chỉ giảm phát thải khí nhà kính mà còn cải thiện hiệu quả chất lượng không khí."),
         ("实现碳中和的宏伟目标需要持之以恒的科技创新与全社会的协同努力，共同守护地球家园。", "Shíxiàn tànzhōnghé de hóngwěi mùbiāo xūyào chízhīyǐhéng de kējì chuàngxīn yǔ quán shèhuì de xiétóng nǔlì, gòngtóng shǒuhù dìqiú jiāyuán.", "Hiện thực hóa mục tiêu trung hòa carbon đòi hỏi sự đổi mới công nghệ bền bỉ và nỗ lực hiệp đồng của toàn xã hội để cùng che chở mái nhà trái đất.")
     ],
     [
         ("Điều gì giúp năng lượng tái tạo gió và mặt trời nâng cao sức cạnh tranh kinh tế?", ["Được nhà nước bao cấp mãi mãi", "Chi phí sản xuất giảm mạnh nhờ công nghệ tiến bộ", "Không cần xây dựng nhà máy"], 1, "Trong bài có câu: 技术的突飞猛进，使得清洁电力的成本大幅下降，具备了极强的经济竞争力."),
         ("Hệ thống nào giải quyết điểm nghẽn dao động không ổn định của điện mặt trời và gió?", ["Thiết bị lưu trữ năng lượng và lưới điện thông minh", "Máy nổ chạy dầu", "Đốt thêm than đá"], 0, "Trong câu có viết: 先进的储能设备与智能电网系统，为解决波动大的技术瓶颈提供了关键支撑."),
         ("Mục tiêu tối hậu của việc chuyển đổi năng lượng xanh là gì?", ["Giảm khí nhà kính, cải thiện không khí và hướng tới trung hòa carbon", "Chỉ để làm đẹp cảnh quan", "Để tăng giá điện"], 0, "Trong câu có viết: 减少温室气体排放，还能改善空气质量，实现碳中和的宏伟目标.")
     ]),
    (10, "艺术创作与智能算法", "Sáng tạo nghệ thuật và thuật toán thông minh", "ai_art", "Nghệ thuật & Tương lai", "🎨", 6,
     "Khi trí tuệ nhân tạo vẽ tranh và sáng tác nhạc: Câu hỏi về bản sắc và cảm xúc của nghệ thuật.",
     [
         ("当深度学习算法能够在一瞬间生成华丽细腻的画作与悦耳动听的交响乐时，整个艺术界为之震动。", "Dāng shēndù xuéxí suànfǎ nénggòu zài yí shùnjiān shēngchéng huálì xìnì de huàzuò yǔ yuè'ěr dòngtīng de jiāoxiǎngyuè shí, zhěnggè yìshùjiè wéi zhī zhèndòng.", "Khi thuật toán học sâu có thể chớp mắt tạo ra những bức họa hoa lệ tinh xảo và bản giao hưởng êm tai, cả giới nghệ thuật đã chấn động."),
         ("许多人开始认真思考，冷冰冰的代码与海量数据是否真的能够具备人类独有的灵感与创造力。", "Xǔduō rén kāishǐ rènzhēn sīkǎo, lěngbīngbīng de dàimǎ yǔ hǎiliàng shùjù shìfǒu zhēnde nénggòu jùbèi rénlèi dúyǒu de línggǎn yǔ chuàngzàolì.", "Nhiều người bắt đầu suy ngẫm liệu dòng code lạnh lẽo và khối dữ liệu khổng lồ có thực sự sở hữu cảm hứng và sức sáng tạo độc nhất của con người."),
         ("不可否认，人工智能是极其高效的创作工具，能够极大拓宽艺术家的表现手法与构思空间。", "Bùkě fǒurèn, réngōng zhìnéng shì jíqí gāoxiào de chuàngzuò gōngjù, nénggòu jídà tuòkuān yìshùjiā de biǎoxiàn shǒufǎ yǔ gòusī kōngjiān.", "Không thể phủ nhận AI là công cụ sáng tạo vô cùng hiệu quả, có thể mở rộng đáng kể thủ pháp biểu đạt và không gian ý tưởng của nghệ sĩ."),
         ("然而，真正触动人类灵魂深处的伟大艺术，始终源于艺术家对痛苦、欢乐与生命的切身体验。", "Rán'ér, zhēnzhèng chùdòng rénlèi línghún shēnchù de wěidà yìshù, shǐzhōng yuányú yìshùjiā duì tòngkǔ, huānlè yǔ shēngmìng de qièshēn tǐyàn.", "Tuy vậy, nghệ thuật vĩ đại thực sự lay động tận đáy tâm hồn con người luôn bắt nguồn từ trải nghiệm sâu sắc về nỗi đau, niềm vui và sự sống của người nghệ sĩ."),
         ("科技与艺术的交融并非零和博弈，而是携手探索人类审美可能性的全新起点。", "Kējì yǔ yìshù de jiāoróng bìng fēi línghé bóyì, ér shì xiéshǒu tànsuǒ rénlèi shěnměi kěnéngxìng de quánxīn qǐdiǎn.", "Sự giao hòa giữa công nghệ và nghệ thuật không phải trò chơi có tổng bằng không, mà là khởi điểm mới để cùng nhau khai phá các tiềm năng thẩm mỹ nhân loại.")
     ],
     [
         ("Ưu thế nổi bật của AI trong sáng tạo nghệ thuật là gì?", ["Là công cụ hiệu quả giúp mở rộng thủ pháp thể hiện và không gian ý tưởng", "Biết đau đớn như con người", "Tự có cảm xúc độc lập"], 0, "Trong bài có câu: 是极其高效的创作工具，能够极大拓宽艺术家的表现手法与构思空间."),
         ("Cội nguồn của các tác phẩm nghệ thuật vĩ đại lay động lòng người đến từ đâu?", ["Từ việc ghép nối dữ liệu ngẫu nhiên", "Từ trải nghiệm sâu sắc của người nghệ sĩ về buồn vui và cuộc sống", "Từ tốc độ tính toán nhanh của máy"], 1, "Trong câu có viết: 始终源于艺术家对痛苦、欢乐与生命的切身体验."),
         ("Mối quan hệ giữa nghệ thuật và công nghệ được tác giả nhìn nhận như thế nào?", ["Một bên sẽ tiêu diệt bên kia", "Là khởi điểm mới cùng khám phá tiềm năng thẩm mỹ của nhân loại", "Hoàn toàn đối lập không thể dung hòa"], 1, "Trong câu cuối có viết: 携手探索人类审美可能性的全新起点.")
     ])
]
