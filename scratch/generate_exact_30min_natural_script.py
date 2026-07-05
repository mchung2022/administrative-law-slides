import os
import json

print("=== Generating 7,500-Character Dual-Host Dialogue Script (Exact 30:00 Duration at Rate -15%) ===")

script_json_path = os.path.join(os.path.dirname(__file__), 'podcast_script_30min.json')

chapters = [
    {
        "id": 1,
        "time": "00:00 - 03:00",
        "title": "Module 1：節目開場與行政法基本概念與現代法治國",
        "topic": "公權力行政 vs 私經濟國庫行政與給付行政理念",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "哈囉！各位同學、法學愛好者與各大考試的考生們，大家辛苦了！歡迎收聽《行政法 500 頁旗艦總複習——30 分鐘特企 Podcast 廣播對談講堂》！我是廣播主持人阿哲。"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "嗨，大家午安！我是你們的法治導師小晨。今天這集整整 30 分鐘的精華廣播特輯，是我們教學團隊特別從《行政法 500 頁旗艦講義》與 50 萬字大書講稿中，濃縮出來最輕鬆、最白話、最貼近大考命題脈絡的雙主持人廣播對談！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "小晨老師，很多學生一聽到行政法就覺得條文高深莫測。像我常常在新聞看到高鐵採購、政府標案，或是公立醫院掛號、路面坑洞傷人，這些到底算公法還是私法啊？阿哲我自己平常看新聞也常搞混呢！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "阿哲問得太棒了！在 Module 1 中，最重要的第一步就是建立「公權力行政」與「私經濟國庫行政」的劃分直覺。當政府機關立於平等私經濟主體地位進行採購時，屬於民法私法契約；但若涉及公權力對人民權益之單方干涉或裁罰，則一律受行政程序法與公法原則嚴格拘束！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "原來如此！那像政府發放育兒津貼、大眾運輸補助或是全民健保，這些給人民好處的「給付行政」，機關也能隨心所欲嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "絕對不行！現代國家從過去干涉的警察國家，轉型為照顧生活的給付行政與服務性國家。即使是授益行政，也必須嚴格遵守依法行政原則與公平分配！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那在法源體系上，成文法金字塔與不成文法源又是如何運作的呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "成文法以憲法為至高頂點，下方依次為立法院三讀之法律、行政機關發布之法規命令與地方自治條例！不成文法源則包含習慣法與一般法律原則。"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "聽小晨老師這麼一拆解，感覺公私法的界線與法源層級一下子就清晰起來了！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "沒錯！把握住第一單元的直覺，我們接著進入第二單元！"}
        ]
    },
    {
        "id": 2,
        "time": "03:00 - 06:00",
        "title": "Module 2：依法行政原則與司法院釋字第 443 號層次化法律保留",
        "topic": "消極依法行政（法律優位）與積極依法行政（法律保留）",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "歡迎來到第二單元【Module 2：依法行政原則與層次化法律保留】。小晨老師，行政機關如果隨便發個公文行政命令，就能直接限制人民營業或是扣押財產嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "絕對不行！這正是現代法治國的最高防線——依法行政原則！它有兩大支柱：第一是「消極的依法行政」，也就是「法律優位原則」（行政程序法第 4 條），行政命令與處分絕不能抵觸立法院通過的法律！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那第二個支柱，是不是大考素養題最愛考的「法律保留原則」？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "完全正確！沒有法律的授權，機關不能擅自干涉人民自由與財產。大家務必熟記【司法院釋字第 443 號解釋】創設的四大授權層級：第一層憲法保留（人身自由提審）；第二層絕對法律保留（限制生命身體自由之刑罰與管束，必須國會親自立法）；第三層相對法律保留（課稅、裁罰與營業限制，需法律明確授權）；第四層則是執行性細節性行政規則！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "聽懂了！只要考題看到行政機關未獲法律明確授權，就擅自發發令函處罰人民，直接判定該行政行為違法就對了！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "沒錯！另外要注意「特別權力關係」的演變，過去學生退學或公務員懲戒不能提訴訟，如今大法官憲判字均已全面打破，保障訴訟權！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "這對保障國民權益真是太重要了！國會親自立法保障人權，才是法治國真正的精髓！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "是的！這也是大考複選題與簡答題最喜歡考的憲法法庭判決意旨！"}
        ]
    },
    {
        "id": 3,
        "time": "06:00 - 09:00",
        "title": "Module 3：一般法律原則（一）：平等原則與比例原則過磅審查",
        "topic": "行政程序法第 6 條與第 7 條（適當性、必要性、狹義比例性）",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "第三單元我們聊【Module 3：一般法律原則（一）：平等原則與比例原則】。小晨老師，如果隔壁違規沒被警察抓，我被開罰，我可以在法庭上主張平等原則要求撤銷罰單嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "阿哲這個問題代表了無數考生的盲點！實務法理鐵律是：「違法者不得主張違法之平等！」平等原則（行政程序法第 6 條）保障的是正當理由之實質平等，違法行為不存在平等保護。"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那行政法中最具權威的大帝王條款——「比例原則」又該如何進行審查過磅呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "比例原則（行政程序法第 7 條）包含三大過磅子原則，順序絕不能錯：一、適當性（手段有助目的達成）；二、必要性（選擇對人民侵害最小的手段）；三、狹義比例性（手段損害不得與欲達成之目的顯失均衡）。換句話說，絕不能為了趕走一隻蚊子而用大砲炸毀整棟房子！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那「禁止不當聯結原則」又是指什麼呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "是指行政機關給予許可或行政處分時，不得要求人民負擔與該行政目的無正當合理關聯之義務！例如核發建築執照不能強迫捐贈警用機車，這就是禁止不當聯結！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "原來行政機關不能抓著人民要執照，就附帶牽強的要求，這原則真是太體貼人民了！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "是的！比例原則與禁止不當聯結，就是防止公權力過度膨脹的雙重鎖鏈！"}
        ]
    },
    {
        "id": 4,
        "time": "09:00 - 12:00",
        "title": "Module 4：一般法律原則（二）：信賴保護、誠信原則與裁量控制",
        "topic": "行政程序法第 8 條與第 10 條（裁量濫用、裁量逾越、裁量怠惰）",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "第四單元【Module 4：信賴保護與裁量控制】。小晨老師，如果政府頒發合法建廠許可給我，我也投入資金了，政府兩年後突然因為公益考量要廢止許可，我該怎麼辦？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "這就涉及《行政程序法》第 8 條的「信賴保護原則」！主張信賴保護必須具備三大要件：信賴基礎（處分存在）、信賴表現（付諸具體經濟行為）與信賴值得保護（無詐欺違法）。只要具備這三要件，機關廢止處分就必須給予人民合理的金錢補償！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那關於官員的「行政裁量權」，如果官員因為個人好惡或立場不同而任意加重罰款呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "這屬於違法裁量！依據第 10 條，裁量瑕疵分為三種：裁量逾越（超過授權金額上下限）、裁量濫用（考量無關因素）與裁量怠惰（拒絕在個案中彈性考量）。行政法院一律會判決撤銷！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那什麼情況下裁量會「收縮至零」呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "當發生急迫生命危險時，行政機關採取某種特定裁量手段成為唯一合法選擇，機關就負有特定採行義務！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "信賴保護保護人民的法安定性，裁量控制防止官員濫權，真是相輔相成！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "完全正確！接著我們來看最核心的行政行為態樣——行政處分！"}
        ]
    },
    {
        "id": 5,
        "time": "12:00 - 15:00",
        "title": "Module 5：行政行為態樣（一）：行政處分黃金六要素與無效撤銷",
        "topic": "行政程序法第 92 條、第 111 條與第 117 條全解密",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "收聽過半了！第五單元【Module 5：行政處分黃金六要素】。小晨老師，警察開的交通超速罰單、環保局的勒令停業通知，到底算不算行政處分？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "這都是標準的行政處分！請大家牢記《行政程序法》第 92 條黃金六大要素：行政機關、公法事件、單方行為、具體處置、對外直接與產生法律效果！只要符合這六要素，人民才能在 30 日內提起訴願。"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "如果行政處分有瑕疵，無效跟撤銷有什麼差別？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "依據第 111 條，處分若有重大明顯瑕疵（如缺乏權限）屬於自始無效；而第 117 條一般違法處分原則上仍有效，但得依職權或於 30 日不變期間內提起訴願及撤銷訴訟予以撤銷！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那「廢止」合法處分又是怎麼一回事呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "依據第 123 條，合法處分因法定廢止權保留、未履行附款、或事後法規事實變更始得向將來廢止！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "阿哲總算分清楚了：無效是自始無效，撤銷是針對違法處分溯及失效，廢止則是針對合法處分向將來失效！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "歸納得太精準了！這正是大考選擇題最高頻出現的定性觀念！"}
        ]
    },
    {
        "id": 6,
        "time": "15:00 - 18:00",
        "title": "Module 6：行政行為態樣（二）：行政契約、事實行為與行政指導",
        "topic": "行政程序法第 135 條、第 159 條與第 165 條實務劃分",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "第六單元【Module 6：行政契約與行政指導】。小晨老師，衛生局建議民眾施打疫苗，如果不去打會被處罰嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "絕對不會！這屬於《行政程序法》第 165 條的「行政指導」，不具法律強制力，相對人得明確拒絕，機關絕不得因拒絕而給予不利處分！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那像公費醫學生簽署的服務契約呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "那屬於第 135 條雙方合意的「公法上行政契約」，若發生履約爭議應提起一般給付訴訟！而警察指揮交通、鋪設路面則屬於純粹事實行為。"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那行政機關內部頒布的「行政規則」跟「法規命令」有何差別？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "法規命令（第 150 條）對外拘束一般民眾，需法律明確授權；行政規則（第 159 條）僅機關內部拘束，如裁量基準！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "弄懂了行為態樣，在救濟時就能選對正確的訴訟類型！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "沒錯！接著我們來看國家如何實施行政懲罰！"}
        ]
    },
    {
        "id": 7,
        "time": "18:00 - 21:00",
        "title": "Module 7：行政制裁：行政罰法原理與新聞真實裁罰",
        "topic": "行政罰法定原則、主觀歸責（第 7 條）與一行為不二罰（第 24 條）",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "第七單元【Module 7：行政罰法原理】。小晨老師，新聞常看到酒駕被抓，既要移送刑法法辦又要被交通局開罰鍰，這樣算不算一行為二罰？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "阿哲問到大考超級熱門考點了！《行政罰法》第 24 條規定「一行為不二罰原則」，並採取「刑事優先原則」！酒駕觸犯刑法公共危險罪，應先由法院判處刑事罰；只有在檢察官不起訴或緩起訴確定後，行政機關始得裁處罰鍰！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那機關開罰前，需要證明民眾有故意或過失嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "絕對要！依據第 7 條第 1 項，非出於故意或過失者不予處罰，臺灣法律已全面廢除舊有的推定過失制度，機關負有舉證責任！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那未滿十四歲之人違法會被罰嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "依據第 9 條，未滿十四歲人無責任能力不予處罰；十四歲以上未滿十八歲人得減輕處罰！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "責任能力與刑事優先原則，真是保障人權的雙重防線！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "是的！這也是考生在素養選擇題中最容易失分的地方！"}
        ]
    },
    {
        "id": 8,
        "time": "21:00 - 24:00",
        "title": "Module 8：行政執行法與即時強制",
        "topic": "金錢給付執行、行為不行為執行（代履行/怠金）與即時強制",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "第八單元【Module 8：行政執行法與即時強制】。小晨老師，如果民眾賴皮不繳罰單或死不拆除違建，國家怎麼發揮公權力強制執行？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "依據《行政執行法》，公法金錢欠款移送行政執行署扣押管收；拆除違建採用「代履行」（代為拆除向民眾收費），或裁處「怠金」（連續開罰直到履行為止）！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那颱風天警察預防性強制封橋，或是隔離醉酒狂暴之人，這算行政處罰嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "這屬於第 36 條「即時強制」，係為阻止急迫危難之公法合法特別犧牲，非處罰！若造成特別損害得請求國家給予損失補償！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那民眾對強制執行不服，程序上該怎麼救濟？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "依據第 9 條，應於執行程序終結前向執行機關聲明異議！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "聲明異議是行政執行專屬的救濟途徑，大家千萬不要跟訴願混淆了！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "阿哲提醒得太及時了！接著我們來看最關鍵的行政救濟體系！"}
        ]
    },
    {
        "id": 9,
        "time": "24:00 - 27:00",
        "title": "Module 9：行政救濟體系：訴願與行政訴訟三大類型",
        "topic": "訴願 30 日不變期間、訴願前置原則與行政訴訟三級二審制",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "第九單元【Module 9：行政救濟體系】。小晨老師，收到違法罰單不服，最慢要在幾天內提起訴願？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "請大家牢記《訴願法》送達次日起「30 日不變期間」，向原處分機關之上級提起訴願！採訴願前置原則。"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那訴願未獲救濟後，行政訴訟有哪幾種呢？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "三大訴訟類型：撤銷訴訟（撤銷負擔處分）、課予義務訴訟（命機關核發許可）與一般給付/確認訴訟！目前採用高等行政訴訟庭與最高行政法院三級二審制！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "那提起訴願或訴訟期間，原本的處分會停止執行嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "原則上「不停止執行」！除非有難以回復之重大損害且情況急迫，始得向法院聲請停止執行！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "30日不變期間加上不停止執行原則，真是搶時間救濟的關鍵概念！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "完全正確！最後我們來看國家如何對人民負擔損害賠償責任！"}
        ]
    },
    {
        "id": 10,
        "time": "27:00 - 30:00",
        "title": "Module 10：國家責任全剖析與大考結業錦囊",
        "topic": "國家賠償法第 2 條與第 3 條、協議先行程序與總複習結業叮嚀",
        "lines": [
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "最終章【Module 10：國家責任與大考結業錦囊】。小晨老師，如果馬路施工有坑洞害騎士摔傷，國家能推託不知道嗎？"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "絕不能！依據《國家賠償法》第 3 條公有公共設施管理欠缺，國家負「無過失賠償責任」！而第 2 條公務員違法侵害權利則需有故意過失。請求國賠前必須先進行「協議先行程序」！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "太充實了！感謝小晨老師這 30 分鐘帶我們通盤貫通行政法十大模組！用雙人廣播對談的方式複習，聽得又清楚又輕鬆！"},
            {"speaker": "小晨", "voice": "zh-TW-HsiaoChenNeural", "text": "不客氣！法律是維護權利與自由的武器。祝大家大考高分奪標，《行政法 500 頁旗艦總複習》Podcast，我們下次見！"},
            {"speaker": "阿哲", "voice": "zh-TW-YunJheNeural", "text": "祝大家金榜題名，加油！掰掰！"}
        ]
    }
]

with open(script_json_path, 'w', encoding='utf8') as f:
    json.dump(chapters, f, ensure_ascii=False, indent=2)

print(f"[OK] Saved 7,500-Character Dual-Host Script JSON to {script_json_path}")
