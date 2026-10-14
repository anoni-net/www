---
title: COSCUP 2026 匿名網路社群議程軌
description: 匿名網路社群 anoni.net 2026 年 8 月 8、9 日在 COSCUP 2026（國立臺灣科技大學）的兩日議程與工作坊紀錄，主題涵蓋 Tor、Tails、OONI、瀏覽器追蹤、校園 Tor 節點、個資權利、隱私指南與匿名支付。
---

![COSCUP 2026 匿名網路社群議程軌主視覺](https://assets.anoni.net/event/anoni-net-eth-taipei.webp){ .shot }

記者需要保護消息來源，公民團體需要保護成員與捐款人，開發者想確認手上的工具能抵擋監控。也有一般人被詐騙簡訊與廣告追蹤困擾，想多掌握自己的資料。四種需求牽涉同一組風險，包括通訊遭攔截、身分被追蹤，以及從一筆轉帳的時間與金額反推出整張關係網。組織的成員名單與金流，也可能在當事人不知情時曝光。

匿名網路社群 anoni.net 在 COSCUP 2026 開設兩天的社群議程軌，內容來自社群這一年在 [Tor](docs:tools/what-is-tor/)、[Tails](docs:tools/what-is-tails/)、[OONI](docs:tools/what-is-ooni/)、個人隱私與匿名支付的實作經驗。議程從網路與審查的運作原理開始，涵蓋開源隱私工具的實際運用、校園 Tor 節點、瀏覽器追蹤、健保資料庫的個資權利，以及與 ETHTaipei 合辦的匿名支付場。前三場導論由社群成員主講，其餘為邀請、合辦與錄取議程。

!!! info "活動資訊"

    - 日期：2026/08/08（六）、2026/08/09（日）
    - 地點：國立臺灣科技大學（NTUST），社群議程軌在 `TR-510`，8/08 下午與 ETHTaipei 合辦場在 `TR-511`
    - 形式：社群議程、實作工作坊，以及與 ETHTaipei 合辦的匿名支付場
    - 入場：COSCUP 免費入場，社群議程軌不需另外報名（實際時間以 [COSCUP 官方議程](https://pretalx.coscup.org/coscup-2026/) 為準）
    - 狀態：活動已經結束，本頁保留議程、各場介紹與講者簡報作為紀錄
    - 簡報：講者提供的簡報與錄影附在[議程總覽](#議程總覽)各場的說明下方，著作權屬於各講者，轉載或改作前請先取得講者同意（另外標示授權的依標示）

[前往 COSCUP 2026 議程](#議程總覽){ .btn .solid }

!!! tip "免費入場、免報名的匿名參加方式"

    COSCUP 免費入場，社群議程軌也不需事先報名，聽眾當天走進教室即可參與。對推廣匿名的社群來說，參加方式本身也能匿名，聽議程不必留下任何個人資訊。

!!! tip "依聽眾身分的建議場次"

    - **新聞媒體、獨立記者**：8/08 上午的「現實世界的開源隱私工具」整理記者實際使用的安全收件管道、去識別化與隔離工具，可搭配「威脅模型與 Metadata 入門」。8/09 下午有「瀏覽器追蹤技術、反追蹤策略」，談瀏覽器如何洩漏使用者聯繫過誰，「健保資料庫案之後」與「隱私指南 2026」再延伸到個資權利與法律調取資料的因應（延伸閱讀：[記者保護消息來源](docs:scenarios/journalist/)）。
    - **公民團體、NGO**：8/08 上午的四場導論最貼近組織處境，其中「現實世界的開源隱私工具」整理公民團體與 NGO 使用的加密通訊、內部協作與檢舉投遞工具。「毒品非毒、洗錢非洗錢」探討受助者或檢舉者如何證明自己符合條件，又不留下身分資料，8/09 的「隱私指南 2026」涵蓋組織遭法律調取資料時的事前準備。評估匿名捐款管道時，8/08 下午合辦場的「我不洗錢，為何要理解匿名支付？」是白話入門，不需要加密貨幣背景。
    - **開源、科技社群**：8/09 的技術含量最高，OpenWRT、臺師大 Tor 節點與瀏覽器指紋研究都有實作內容。8/08 下午的零知識證明（ZK）自然人憑證、隱私保護的 KYC（金融機構確認客戶身分的程序）與隱匿地址，是協議層最扎實的內容。想參與貢獻見[參與](/join/)。

## <i data-icon="calendar-text"></i> 議程總覽 { #議程總覽 }

社群議程軌的時間與題目如下，實際時間以 [COSCUP 官方議程](https://pretalx.coscup.org/coscup-2026/) 為準。場次之間有換場休息，8/08 上午每場間隔 10 分鐘，8/09 議程較滿，間隔 5 分鐘。各場摘要見[議程介紹](#議程介紹)。

### Day 1：2026/08/08（六）

8/08 上午是四場開源匿名網路導論，前三場由 anoni.net 社群成員主講，第四場為邀請議程。四場都從入門角度切入，以開源工具為主軸，適合公民團體、新聞媒體與獨立記者。下午 13:00 起是與 ETHTaipei 合辦的「匿名支付」場，協議層的技術內容較多。

**上午 09:30-12:00　開源匿名網路導論（教室 `TR-510`）**

| 時間 | 議程 | 講者 |
|------|------|------|
| 09:30-10:00<br>30 分鐘 | <span class="tag tag--basic">通用</span> <i data-icon="account-group"></i> **匿名網路社群 anoni.net 介紹：開源匿名工具、社群實踐與 2026 三大主題**<br><i data-icon="arrow-right-bottom"></i> 社群在台灣將 Tor、Tails、OONI 等隱私工具中文化並推廣，場次介紹社群的組成與工作，以及高風險工作為何需要能檢驗原始碼的開源工具<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/anoni-net-intro.pdf) | anoni.net 社群 |
| 10:10-10:40<br>30 分鐘 | <span class="tag tag--basic">通用</span> <i data-icon="target-account"></i> **威脅模型與 Metadata 入門：認識你的對手，以及為什麼匿名工具要開源才可信**<br><i data-icon="arrow-right-bottom"></i> 就算通話內容沒有被監聽，誰在什麼時間聯繫了誰，往往就足以讓消息來源曝光。內容包括如何判斷要防範誰、防到什麼程度<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/anoni-net-threat-model.pdf) | anoni.net 社群 |
| 10:50-11:20<br>30 分鐘 | <span class="tag tag--basic">通用</span> <i data-icon="toolbox-outline"></i> **現實世界的開源隱私工具：公民團體、獨立記者與個人隱私防護的實際運用**<br><i data-icon="arrow-right-bottom"></i> 整理記者、NGO 與在意隱私的一般人實際使用的免費開源工具，原始碼公開、可供檢驗，聽眾可以從中挑一兩個先用<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/anoni-net-realworld-tools.pdf) | anoni.net 社群 |
| 11:30-12:00<br>30 分鐘 | <span class="tag tag--basic">通用</span> <i data-icon="scale-balance"></i> **毒品非毒、洗錢非洗錢—淺談匿名的資格驗證**<br><i data-icon="arrow-right-bottom"></i> 同一件事換一套規則就被歸成兩種性質，誰有權定義合法與非法？講者在實名與匿名之外尋找第三條路，聽眾不需要密碼學背景 | Denken Chen | <!-- docs-style-lint: disable-line -->

**下午 13:00-16:30　ETHTaipei 合辦「匿名支付」場（教室 `TR-511`，議程由 ETHTaipei 安排）**

| 時間 | 議程 | 講者 |
|------|------|------|
| 13:00-13:30<br>30 分鐘 | <span class="tag tag--payments">匿名支付</span> <i data-icon="card-account-details-outline"></i> **零知識證明與自然人憑證身份驗證**<br><i data-icon="arrow-right-bottom"></i> 不必交出任何個資，就能用自然人憑證向網站證明自己是台灣公民 | Ya-wen Jeng |
| 13:40-14:10<br>30 分鐘 | <span class="tag tag--payments">匿名支付</span> <i data-icon="account-check-outline"></i> **The Privacy-preserving Identity Pipeline in KYC**<br><i data-icon="arrow-right-bottom"></i> 以一組密碼學原語組合出可通過 KYC、伺服器卻看不到身分資料的流程 | ryanycw（Ryan Wang） |
| 14:20-14:50<br>30 分鐘 | <span class="tag tag--payments">匿名支付</span> <i data-icon="link-off"></i> **從不可連結性出發：隱匿地址如何解決鏈上金融隱私（以 Fluidkey 為例）**<br><i data-icon="arrow-right-bottom"></i> 隱匿地址讓同一人每次收款都落在互不相關的地址，外部無法串連成同一身分 | Jennifer HSU |
| 15:00-15:30<br>30 分鐘 | <span class="tag tag--payments">匿名支付</span> <i data-icon="bitcoin"></i> **我不洗錢，為何要理解匿名支付？從零開始介紹隱私加密金流交易**<br><i data-icon="arrow-right-bottom"></i> 倡議組織與捐款人為何需要了解加密貨幣金流的隱私風險，並以白話介紹幾套解法<br><i data-icon="presentation"></i> [簡報（網頁）](https://mashbean.net/decks/coscup-2026-privacy-money/) | 黃豆泥 mashbean |
| 15:40-16:30<br>50 分鐘 | <span class="tag tag--payments">匿名支付</span> <i data-icon="hammer-wrench"></i> **隱私支付實作工作坊：從龍捲風現金到隱私池**<br><i data-icon="arrow-right-bottom"></i> 以道具與實機示範 Tornado Cash 與 Privacy Pool 的用法，現場備有模擬網路，聽眾可自備電腦操作<br><i data-icon="presentation"></i> [簡報（網頁）](https://chihchengliang.github.io/notes/2026-07-27_privacy_pools/slides.html) | Liangcc |

### Day 2：2026/08/09（日）

8/09 全天是七場錄取議程，題材從網路與審查的基礎、家用網路與校園 Tor 節點，到健保資料庫的個資權利與個人隱私防護。技術場次與貼近日常的場次交錯安排，開發者、記者與公民團體各有適合的場次。

**上午 10:00-12:00（教室 `TR-510`）**

| 時間 | 議程 | 講者 |
|------|------|------|
| 10:00-10:50<br>50 分鐘 | <span class="tag tag--basic">通用</span> <i data-icon="web"></i> **The Workings of the Internet：網路如何運作、審查如何擋住你（英文進行）**<br><i data-icon="arrow-right-bottom"></i> 以寄明信片比喻連線過程，說明從裝置到網站的路上有哪些角色能偷看或竄改內容，英文不熟的聽眾也能掌握大意<br><i data-icon="presentation"></i> [簡報（PDF）](https://saxrag.com/bucket/random/workings_of_the_internet.pdf)（CC BY 4.0） | Raghu |
| 10:55-11:25<br>30 分鐘 | <span class="tag tag--basic">通用</span> <i data-icon="router-network"></i> **以 OpenWRT 等開源軟體建立家用網路環境**<br><i data-icon="arrow-right-bottom"></i> 在家用路由器上完成一般機種沒有的進階設定，包含 VLAN 隔離、多 WAN、site-to-site VPN 與 Tor 上游<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/pellaeon-openwrt-home-network.pdf)（講者保留所有權利，僅供閱覽） | Pellaeon |
| 11:30-12:00<br>30 分鐘 | <span class="tag tag--payments">匿名支付</span> <i data-icon="fingerprint"></i> **區塊鏈網路上基於開放標準的實體身份識別方法**<br><i data-icon="arrow-right-bottom"></i> 虛擬資產服務法通過後，哪些開放標準會被用來在區塊鏈上定位台灣使用者的身分 | Yusef Schultz |

（12:00-13:00 午休）

**下午 13:00-16:00（教室 `TR-510`）**

| 時間 | 議程 | 講者 |
|------|------|------|
| 13:00-13:30<br>30 分鐘 | <span class="tag tag--relay">Tor Relay</span> <i data-icon="simple-torproject"></i> **在學校種洋蔥？臺師大 Tor 節點建立實務與 EFF Tor University Challenge 經驗談**<br><i data-icon="arrow-right-bottom"></i> 在臺師大架設學術 Tor 節點的完整歷程，從技術配置到校內政策協調<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/nz-tor-relay-on-campus.pdf) <i data-icon="video-outline"></i> [錄影（Google Drive）](https://drive.google.com/file/d/1bAzgU6rSNg9hXSrDhDIXYd4PM-P8Dxte/view?usp=sharing) | NZ |
| 13:35-14:25<br>50 分鐘 | <span class="tag tag--privacy">個人隱私</span> <i data-icon="eye-off-outline"></i> **瀏覽器追蹤技術、反追蹤策略和使用者自主**<br><i data-icon="arrow-right-bottom"></i> 日常使用的瀏覽器如何被指紋追蹤、如何洩漏聯繫對象，以及反追蹤的做法<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/pellaeon-browser-tracking-and-user-autonomy.pdf)（講者保留所有權利，僅供閱覽） | Pellaeon |
| 14:30-15:00<br>30 分鐘 | <span class="tag tag--privacy">個人隱私</span> <i data-icon="database-lock"></i> **健保資料庫案之後：停止利用權如何實踐？以及其他大型資料庫**<br><i data-icon="arrow-right-bottom"></i> 健保資料庫從退出權訴訟到修法的經過，以及停止利用權的申請方式<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/kuan-nhi-database-right-to-opt-out.pdf) | Kuan-Ju Chou |
| 15:05-15:55<br>50 分鐘 | <span class="tag tag--privacy">個人隱私</span> <i data-icon="shield-account-outline"></i> **隱私指南 2026**<br><i data-icon="arrow-right-bottom"></i> 從個人隱私風險矩陣、NGO 與媒體面對法律調取資料的準備，到門檻簽章、MPC 等組織級進階工具<br><i data-icon="presentation"></i> [簡報（PDF）](https://assets.anoni.net/event/coscup-2026/justyn-privacy-guides-2026.pdf) | Justyn |

## <i data-icon="text-box-multiple-outline"></i> 議程介紹 { #議程介紹 }

### 8/08 上午的開源匿名網路導論

前三場導論由 anoni.net 社群成員主講，內容取材自文件站與 2025 年工作坊，第四場為邀請議程。導論介紹的工具（Tor、Tails、OONI、Signal、SecureDrop、OnionShare、CryptPad、mat2 等）都是自由開源軟體，社群也透過翻譯、架設中繼節點與回報問題參與這些國際開源專案。

??? abstract "匿名網路社群 anoni.net 介紹：開源匿名工具、社群實踐與 2026 三大主題"

    匿名網路社群 anoni.net 是台灣的開源社群，近一年持續推廣 Tor、Tails、OONI 等自由開源的匿名網路工具。開場介紹社群的緣起與運作方式，以及社群如何以開源協作參與國際專案，例如把 Tor、Tails、OONI 與 Tor University Challenge 的介面翻成正體中文、回報問題、協助在校園架設中繼節點。

    接著說明記者、公民團體、人權倡議者這類高風險工作，為何特別倚賴原始碼公開的開源工具，封閉的黑箱軟體無從驗證是否遭到竄改。最後介紹社群 2026 年的三個主題：依情境分級的個人隱私指引、校園 Tor Relay 中繼節點建立，以及在合法前提下探索匿名支付的開源工具。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/8CZ7ER/)

??? abstract "威脅模型與 Metadata 入門：認識你的對手，以及為什麼匿名工具要開源才可信"

    挑選工具之前，要先回答三個問題：要保護什麼、要防範的對手是誰、願意付出多少成本。講者用[威脅模型](docs:basics/threat-model/)把三個問題組成判斷框架，並說明 [metadata](docs:basics/metadata/)（連線、時間、聯絡對象這類沒有加密的紀錄）的風險。就算通話內容沒有被監聽，對手仍可能從通聯紀錄得知誰在什麼時間聯繫了誰、聯繫多久。對記者與公民團體來說，這類紀錄往往足以反推出消息來源與整個行動的關係網。

    有了判斷框架，遇到新工具、新威脅時就能自行對照。對手有能力檢查裝置與通訊時，工具能否被獨立稽核就攸關安全，Tor Browser、Tails 採用開放原始碼與可重現建置（reproducible build，任何人都能從原始碼編出位元相同的程式，驗證沒有被動過手腳）也是出於這個原因。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/GFKLC8/)

??? abstract "現實世界的開源隱私工具：公民團體、獨立記者與個人隱私防護的實際運用"

    講者整理公民團體、獨立記者與注重隱私的個人實際採用的開源隱私工具，分三個場景介紹，每一項都交代使用者與適用情境。高風險場景特別倚賴原始碼可供公開稽核的開源工具，封閉軟體無從驗證是否遭到竄改，與前一場[威脅模型](docs:basics/threat-model/)的判斷框架相互呼應。介紹以最容易上手的幾樣工具為主，聽眾不必記住整份清單，可以先挑一兩個開始使用。

    公民團體與 NGO 對外用 Signal、Matrix 加密通訊，內部協作用 CryptPad、Etherpad。檢舉與敏感資料的投遞用 SecureDrop、[OnionShare](docs:tools/onionshare/)，網路審查的觀測則用 OONI。獨立記者的部分有安全收件管道、用 mat2 與 Metadata Cleaner 清除檔案內嵌的作者與 GPS metadata，以及用 Tails、Qubes OS 隔離高風險作業。個人隱私防護則有 Tor Browser 與 Brave 抵禦網頁追蹤、GrapheneOS 與 LineageOS 取回手機的控制權、KeePassXC 與 Bitwarden 管理密碼。完整的場景與工具對照見[記者保護消息來源](docs:scenarios/journalist/)與[匿名通訊工具比較](docs:tools/messaging-comparison/)。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/QPDZEC/)

<!-- docs-style-lint: disable -->
??? abstract "毒品非毒、洗錢非洗錢—淺談匿名的資格驗證（Denken Chen，30 分鐘）"

    講者從《我們與惡的距離》談起，提問看完那部戲之後，我們為何仍對善惡的邊界這麼有把握。同一件事物換一套規則就被歸成兩種性質，也就是標題「毒品非毒、洗錢非洗錢」的由來。接著講者提出核心問題，在全面實名監控與無須許可的匿名服務之間，是否還有第三條路。

    技術上，這個提問對應到資格驗證，也就是證明一個人符合某項條件，而不必一併揭露身分。W3C 的可驗證憑證（Verifiable Credentials，VC）等開放標準搭配選擇性揭露（selective disclosure），持有者可以只出示「已成年」這一項，其餘資料驗證方看不到。開放標準讓驗證規則不由單一廠商定義，任何人都能自行實作錢包或驗證端。使用者手上那一端是否開源、可供稽核，決定了使用者能否確認它沒有多送出資料。講者也區分了證明資格與證明身分，作為檢視各種實名制方案的依據。

    OONI 採用同一類思路的匿名憑證（anonymous credentials），讓量測資料可信，又不追蹤回報者，設計與取捨見 [OONI Probe 匿名憑證系統的設計與實作](/articles/ooni-anonymous-credentials/)。講者在 8/09 的 Open Source Policy 議程軌另與黃豆泥 mashbean 合講[年齡驗證、數位監控、隱私權，討論這些以前，不妨先開源吧](https://pretalx.coscup.org/coscup-2026/talk/JSMGDZ/)，分析歐盟以開源方式開發的年齡驗證 App。適合關心數位身分、實名制爭議與匿名服務治理的聽眾，不需要密碼學背景。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/WYGFAZ/)
<!-- docs-style-lint: enable -->

### 8/08 下午的 ETHTaipei 合辦「匿名支付」場

13:00-16:30 是與 [ETHTaipei](https://ethtaipei.org/)（台北以太坊社群）合辦的「匿名支付」主題場，在 `TR-511` 教室進行，共五場，議程由 ETHTaipei 安排。上午的導論從公民與倡議的角度談隱私工具與匿名的資格驗證，以白話為主，不深入密碼學細節。下午前兩場把資格驗證接到金流上，一場用零知識證明搭配自然人憑證向服務證明「我是台灣公民」，另一場用 zkKYC 證明「已成年、與上個月註冊的是同一人」。兩場都是上午「證明符合條件而不揭露身分」的協議層實作，後三場再從鏈上的隱匿地址談到隱私加密金流，最後是實作工作坊。兩個社群切入匿名支付的角度不同，分工與背景見[跨社群合作](#跨社群合作)。

??? abstract "零知識證明與自然人憑證身份驗證（Ya-wen Jeng，30 分鐘）"

    如何在不洩漏任何個人資訊的前提下，向服務提供者證明「我是台灣公民」？講者把零知識證明（zero-knowledge proof，不透露內容就能證明某件事為真的密碼學方法）與自然人憑證結合，建立一套保護隱私的身分驗證系統。自然人憑證內建 RSA 非對稱金鑰，可以對任意訊息做數位簽章。系統以 OpenAC 電路框架設計一套 ZKP proving scheme，解析並驗證憑證產生的 RSA 簽章，同時在電路層面隱藏所有可識別個人的欄位。

    整套流程在使用者的裝置上完成，應用程式請求自然人憑證對特定 challenge 簽章後在本機生成零知識證明，最後只把 proof 提交給驗證方。驗證方能確認對方持有合法的自然人憑證、是台灣公民，卻無從得知姓名、身分證字號等個資。講者也介紹已釋出的 SDK 與範例應用，內容包括 RSA 簽章電路設計、on-device proof 生成的效能優化與整合示範，適合對隱私強化技術（PET）、去中心化身分（DID）以及密碼學在公民科技上的應用有興趣的聽眾。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/997SN8/)

??? abstract "The Privacy-preserving Identity Pipeline in KYC（ryanycw / Ryan Wang，30 分鐘）"

    KYC（金融機構確認客戶身分的程序）有一個內在矛盾，主管機關要求嚴格的身分證明，但服務每多儲存一筆身分資料，就多一個永久的外洩破口。傳統做法把證件收齊、查核、歸檔，每個 KYC 服務商因此成為高價值的攻擊目標，使用者則承擔永久的揭露風險。講者介紹 zkKYC 領域已在運作的另一套流程，用一組精選的密碼學原語組合成一個系統，能證明使用者的宣稱（護照有效、已成年、與上個月註冊的是同一人），伺服器卻看不到身分資料。

    講者整理出一套評估隱私保護身分系統的語彙，說明裝置綁定金鑰、加密的身分儲存、政府簽署的證件鏈、生物特徵承諾、零知識證明與經過認證的宣稱遞送如何組合在一起。內容以系統設計與架構圖為主，每個密碼學原語只做高層次說明，不深入數學，適合工程師與產品人員。講者也盤點了尚未解決的問題，例如生物特徵的撤銷、後量子 SNARK，以及不犧牲不可連結性的去重。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/BBQDPR/)

??? abstract "從不可連結性出發：隱匿地址如何解決鏈上金融隱私（以 Fluidkey 為例）（Jennifer HSU，30 分鐘）"

    區塊鏈上任何人都能查到一個地址的完整交易歷史與餘額，永久公開的財務紀錄不符合日常支付、薪資發放或商業往來對隱私的基本需求。講者從 ECDH 金鑰交換出發，拆解隱匿地址（Stealth Address）在 ERC-5564 的推導流程。收款方公開一組 stealth meta-address，每次收款都推導出一個全新的一次性地址，同一人收到上百筆款項，也會落在上百個彼此無關的鏈上地址。外部觀察者無法把這些地址連到同一個身分，只有持有對應 viewing key 的收款人能掃出哪些地址屬於自己。

    隱匿地址提供不可連結性（unlinkability），但不保證不可追溯性（untraceability），每筆交易的金額與流向在鏈上依然可見、可以審計。被切斷的只有地址與身分之間、同一人不同地址之間的關聯，因此在稅務、審計這類需要選擇性揭露的場景，比全匿名方案更實用。最後以 Fluidkey 為例，說明它把 ephemeral key 改為從 viewing key 依 BIP-32 階層式路徑推導，使用者能完全獨立地重新推導出歷史地址、恢復資金，不必依賴任何中心化服務。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/WK8EEE/)

??? abstract "我不洗錢，為何要理解匿名支付？從零開始介紹隱私加密金流交易（黃豆泥 mashbean，30 分鐘）"

    很多人以為加密貨幣是匿名的，實際上只要知道一個錢包地址，就能在公開鏈上看到對方完整的金流、社會關係與行動軌跡。對倡議組織、跨境協作的公民團體，以及需要保護身分的捐款人與受助者來說，這項風險經常被低估。講者用白話走過鏈上隱私金流的設計邏輯，對照近年區塊鏈社群發展出的三套方案。Tornado Cash 是曾遭美國制裁、開發者被起訴的混幣器，Privacy Pool 走白名單路線，在同一個架構裡協商合規與隱私。Railgun 以黑名單搭配冷卻期與集體偵測，2025 年擋下 zkLend 駭客約 950 萬美元的洗錢，另外也介紹把隱私設為所有錢包預設值的 Kohaku。

    講者最後提出一個比技術更難的問題，隱私從技術問題延伸成治理問題時，由誰來定義好人與壞人？適合關心數位人權與公民安全的工作者、想了解加密貨幣合規邊界的法遵與會計人員，以及對「我又沒做壞事，為什麼要在乎隱私」這句話感到不對勁的人。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/QGUGMK/)

??? abstract "隱私支付實作工作坊：從龍捲風現金到隱私池（Liangcc，50 分鐘）"

    工作坊從使用者的角度出發，介紹龍捲風現金（Tornado Cash）的設計哲學，以及隱私池（Privacy Pool）在它之上的改進。

    現場以道具與實機示範兩項工具的操作，並備有模擬網路，聽眾可以自備電腦實際操作。時間允許時，也談這些工具的沿革與在現實世界造成的衝擊。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/3WHJYA/)

### 8/09 的七場錄取議程

七場議程從網路與審查的運作原理開始，接著是家用網路與校園 Tor 節點的實地部署。之後的場次談區塊鏈身分、瀏覽器追蹤、健保資料庫的個資權利與個人隱私指南，屬於制度與個人層面的實踐，技術深淺不一。

??? abstract "The Workings of the Internet：網路如何運作、審查如何擋住你（Raghu，50 分鐘，英文進行）"

    在瀏覽器輸入 `google.com`、按下 Enter 之後，封包到底經過哪些人的手？講者用寄明信片比喻，說明從裝置到目標網站之間有哪些角色經手（多半是合法的），以及它們能看到、能改動什麼。議程以英文進行，但從生活比喻切入、不預設技術背景，英文不熟的聽眾也能掌握大意。

    理解這套機制，就能看懂審查、監控與資料外洩如何發生，也能分辨那些勸人購買「某某 VPN」的廣告話術問題在哪裡。內容也提到預設情況下網路的隱私有多不足，以及看待掠奪式 VPN 行銷時該有的警覺。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/UY8UQN/)

??? abstract "以 OpenWRT 等開源軟體建立家用網路環境（Pellaeon，30 分鐘）"

    OpenWRT 是一套開源的路由器作業系統，講者跳過基本網路設定，直接示範一般家用路由器不提供、透過 OpenWRT 設定即可達成的便利、安全與隱私功能。

    內容包括挑選支援 OpenWRT 硬體的要點、用 VLAN 隔離訪客網路與危險設備、透過多 WAN 運用電信商配發的多個 IP、設定策略路由與 site-to-site VPN、阻擋危險 IP 與網域，以及把 VPN 供應商與 Tor 設成特殊的上游網路。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/CNNASG/)

??? abstract "區塊鏈網路上基於開放標準的實體身份識別方法（Yusef Schultz，30 分鐘）"

    各國政府陸續參考並引入區塊鏈防制洗錢的法案，以防範國際犯罪，共同點在於定位使用者本身。台灣的對應法案是虛擬資產服務法，2026 年 4 月 2 日通過。台灣使用者的身分在鏈上如何被定位，因此逐漸成為虛擬資產持有者關注的議題。

    講者盤點目前用於鏈上身分定位的幾種開放標準，說明使用者的身分在區塊鏈上如何被認定，以及密碼學研究為這個領域帶來的正面影響。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/ZV88PP/)

??? abstract "在學校種洋蔥？臺師大 Tor 節點建立實務與 EFF Tor University Challenge 經驗談（NZ，30 分鐘）"

    學術網路頻寬穩定、IP 聲譽良好，一直是全球 Tor 網路最重要的支柱之一，在校園部署 Tor 節點卻要同時處理技術配置與校內政策。講者分享在國立臺灣師範大學（NTNU）建立學術 Tor 節點的完整歷程。

    內容從 EFF 發起 Tor University Challenge 的緣起與意義，談到 Linux 環境下的節點配置與防火牆規則、如何與學校資訊單位溝通並運用 EFF 提供的法律指南，以及節點上線後的流量觀察。其他學校可以參考這套實務經驗，講者也希望藉此邀請更多台灣學研單位參與全球隱私基礎設施的建設。社群整理的校園架設脈絡見 [Tor Relay 校園建立研究專題](/join/relay-on-campus/)。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/7AP8HY/)

??? abstract "瀏覽器追蹤技術、反追蹤策略和使用者自主（Pellaeon，50 分鐘）"

    現代瀏覽器提供許多看似不屬於網頁的 API：WebGL 讓網頁使用圖形加速、WebAudio 讓網頁執行複雜的音訊合成、WebAssembly 讓網頁直接執行低階指令碼。與硬體緊密結合的 API 讓網頁能做的事變多，網頁也因此能蒐集更多使用者資料，更精準地追蹤與識別使用者。網頁要求時，API 就自動啟用，不會徵詢使用者同意。

    Pellaeon 分享他在瀏覽器指紋（browser fingerprint）與反追蹤方面的研究，說明瀏覽器可能如何洩漏使用者的行蹤，以及 Tor Browser、Brave、VPN 等軟體各自的反追蹤策略、潛在解法與實際使用心得。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/KSWEDB/)

??? abstract "健保資料庫案之後：停止利用權如何實踐？以及其他大型資料庫（Kuan-Ju Chou，30 分鐘）"

    台灣的就醫資料多年來未經病人同意，就提供產業與學界使用。台灣人權促進會、台灣女人連線、健保監督聯盟三個民間團體發動退出權訴訟之後，健保資料庫的目的外利用陸續停止販售光碟，並限縮為僅供研究使用。2022 年的憲法訴訟確認政府必須讓人民實踐停止利用權，也就是不同意將個資提供其他目的使用。之後台灣完成修法，民眾開始可以行使這項權利，但立法過程增加不少例外，適用範圍縮小許多。

    講者說明停止利用權的申請方式與目前的限制，並介紹台灣其他規範不明、對個資當事人權利保障尚不清楚的大型資料庫，同樣需要公民社會一起監督。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/GEKJRV/)

??? abstract "隱私指南 2026（Justyn，50 分鐘）"

    工作坊與座談從個人談到組織，第一部分建立個人隱私風險矩陣，把廣告追蹤與資料仲介、詐騙與盜帳號、親密關係加害者、跨境盤查、針對性監控等威脅來源分級。威脅來源對應到數位身分、行動裝置、SaaS 與雲端、金流四個暴露面，矩陣的每一格都給出以開源工具與裝置內建設定為主的預設配置建議。

    第二部分是自我檢核的方法學，包括如何檢查 App 內嵌的追蹤器、如何觀察裝置實際連線的對象、如何讀懂 iOS App Privacy Report。自評的基準則對照 NIST Privacy Framework 與 OWASP MASVS，只做最小範圍的檢核。

    第三部分談組織層面的多人協作隱私，對象是 NGO、獨立媒體與小型公司，內容涵蓋共享密碼管理、端對端加密協作、組織遭遇法律調取資料的事前準備，以及 Shamir Secret Sharing、門檻簽章（FROST、TSS）、MPC（多方計算）、Private Set Intersection（隱私集合交集）、OpenMLS 等較進階的工具。門檻簽章、MPC、PSI 是給有密碼學背景的組織管理者的重點，非技術背景的聽眾略過這串工具名稱，也不影響前兩部分。

    個人、NGO 與小型團隊都能從中取得對照自身情境的預設配置與自我檢核方法，遇到新工具、新威脅、新法規時可以自行判斷，不必仰賴固定的推薦清單。密碼學細節則點到為止。

    <i data-icon="open-in-new"></i> [COSCUP 官方議程頁](https://pretalx.coscup.org/coscup-2026/talk/K8BYBU/)

## <i data-icon="handshake"></i> 匿名網路社群與 ETHTaipei 的跨社群合作 { #跨社群合作 }

2026 年社群與 [ETHTaipei](https://ethtaipei.org/)（台北以太坊社群）合作安排議程，8/08 下午的「匿名支付」合辦場同時面向關心數位人權的社群與區塊鏈開發者。NGO 與記者在這裡了解捐款與金流的隱私風險，開發者則聽到協議層的零知識證明與隱匿地址實作。徵稿時，應用導向與科普類的稿件安排在匿名網路社群議程軌，技術與協議層的稿件可能調整到 ETHTaipei 的區塊鏈議程軌（見 [COSCUP 2026 公開徵稿](/events/coscup-2026-cfp/#anoni-netxETHTaipei)的跨社群合作一節），聽眾也可以在兩個議程軌之間跨場。

## <i data-icon="account-voice"></i> 講者簡介 { #講者簡介 }

8/08 上午的前三場導論由 anoni.net 社群成員主講，他們實際維運 Tor 中繼節點，也參與 Tails 與 OONI 的正體中文化與問題回報（社群背景見[關於我們](/about/)）。邀請、合辦與錄取議程的講者依議程順序列在下方，點選名字可以前往 COSCUP pretalx 上講者本人提供的完整簡介，Raghu 與 Pellaeon 依講者意願改連到個人網站與部落格。

**8/08 上午 邀請議程**

- **[Denken Chen](https://pretalx.coscup.org/coscup-2026/speaker/FW9HYA/)**：從事軟體開發與寫作十餘年，投入 W3C 的去中心化識別碼與可驗證憑證標準，參與 Credentials Community Group 與台灣數位憑證皮夾的工作，也是 Ptt-iOS、Taiwan E-Book Search 等開源專案的發起人。主講「毒品非毒、洗錢非洗錢—淺談匿名的資格驗證」，並在 8/09 的 Open Source Policy 議程軌與黃豆泥 mashbean 合講「年齡驗證、數位監控、隱私權，討論這些以前，不妨先開源吧」。 <!-- docs-style-lint: disable-line -->

**8/08 下午 ETHTaipei 合辦「匿名支付」場**

- **[Ya-wen Jeng（Vivian Jeng）](https://pretalx.coscup.org/coscup-2026/speaker/KBPWBX/)**：任職 Ethereum Foundation 的 Privacy Stewards of Ethereum 團隊，專注零知識證明與隱私技術推廣，主導 Mopro、Unirep 等開源工具開發。主講「零知識證明與自然人憑證身份驗證」。
- **[ryanycw（Ryan Wang）](https://pretalx.coscup.org/coscup-2026/speaker/8WM9UR/)**：DeFi 開發者，ETHTaipei 共同主辦，關注隱私、技術與以太坊。主講「The Privacy-preserving Identity Pipeline in KYC」。
- **[Jennifer HSU](https://pretalx.coscup.org/coscup-2026/speaker/ZJ98MX/)**：任職自託管隱私錢包 Fluidkey，台灣開發者社群 XueDAO 創辦人，推廣區塊鏈技術。主講「從不可連結性出發：隱匿地址如何解決鏈上金融隱私」。
- **[黃豆泥 mashbean](https://pretalx.coscup.org/coscup-2026/speaker/ZMHFCQ/)**：專注分散式科技與數位自主權，Matters 總經理，曾任數位發展部資安制度工程師（推動數位憑證皮夾與開放網路標準、參與 W3C），活動當時為哈佛大學政策訪問研究員與以太坊基金會 Silviculture 成員。主講「我不洗錢，為何要理解匿名支付？」。
- **[Liangcc（CC）](https://pretalx.coscup.org/coscup-2026/speaker/UYKEPE/)**：在以太坊生態開發零知識應用，關注人文、經濟與密碼學證明。帶領「隱私支付實作工作坊：從龍捲風現金到隱私池」。

**8/09 Day 2 議程**

- **[Raghu](https://saxrag.com/)**：後端工程師，投入 IP、TCP、封包分析與資安研究。主講「The Workings of the Internet」（英文進行）。
- **[Pellaeon](https://nyllep.wordpress.com/)**：數位安全研究員與講師，關注數位人權與自由軟體。主講「以 OpenWRT 等開源軟體建立家用網路環境」與「瀏覽器追蹤技術、反追蹤策略和使用者自主」兩場。
- **[Yusef Schultz](https://pretalx.coscup.org/coscup-2026/speaker/FAGUY7/)**：主講「區塊鏈網路上基於開放標準的實體身份識別方法」，完整簡介見 pretalx 講者頁。
- **[NZ（蘇恩立）](https://pretalx.coscup.org/coscup-2026/speaker/WCJNBL/)**：臺師大資工系學生，維運臺灣學術網路（TANet）首個 Tor 節點，關注資安與網路治理。主講「在學校種洋蔥？臺師大 Tor 節點建立實務與 EFF Tor University Challenge 經驗談」。
- **[Kuan-Ju Chou](https://pretalx.coscup.org/coscup-2026/speaker/UAREZS/)**：在台灣人權促進會服務，負責數位人權。主講「健保資料庫案之後：停止利用權如何實踐？」。
- **[Justyn](https://pretalx.coscup.org/coscup-2026/speaker/WZGMJG/)**：主講「隱私指南 2026」，pretalx 講者頁未附簡介。

## <i data-icon="link-variant"></i> 相關連結

- [COSCUP 2026 公開徵稿](/events/coscup-2026-cfp/)：徵稿主題、跨社群合作與投稿說明
- [匿名網路工作坊 2025/08](/events/workshop-2025/)：2025 年兩日工作坊與圓桌會議的紀錄
- [延續 2025，走向 2026：個人隱私指引、Tor Relay 校園建立競賽、匿名支付探索](/updates/2026/01/2025to2026/)
- [關於我們](/about/)
- [參與](/join/)：參與 Tor、OONI、翻譯或架設節點的入口
- [參與 Tor Project](/join/tor-project/)：參與 Tor 上游專案的管道與方式

!!! info "官方議程與活動通知"

    各場的正式時間與題目以 [COSCUP 官方議程](https://pretalx.coscup.org/coscup-2026/) 為準。想收到社群之後的活動通知，見[持續關注](/contact/)。
