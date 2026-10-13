---
title: Unredacted 的抗審查基礎設施與台灣的對照
description: Unredacted 在 Tor Blog 客座文章的全文翻譯，介紹他們用 300 多台伺服器執行的 FreeSocks、Tor 橋接與 Snowflake，以及用約 400W 執行 123 個出口節點的 GreenWare，文末對照台灣的 Tor 中繼節點現況與參與方式。
date: 2026-06-01
---

審查越嚴格，人們需要的替代路徑就越多，維持這些路徑靠的是伺服器、頻寬與電費。Unredacted 在全球維運 300 多台伺服器，替身處審查環境的使用者提供繞過封鎖的服務，也嘗試用單板電腦降低 Tor 出口節點的耗電。以下翻譯他們在 Tor Blog 的客座文章，文末是 anoni.net 社群的三節補充，對照台灣的中繼節點數量、在台灣複製 GreenWare 的成本，以及讀者可以參與的方式。

原文是 Unredacted 在 Tor Blog「捍衛自由網路的組織」系列發表的 [Keeping the doors open](https://blog.torproject.org/keeping-the-doors-open-unredacted/)（2026-05-15），文中的「我們」指 Unredacted。

有位中國的使用者曾這樣描述我們的工作：

> 「你們幫了很多很多人翻過防火長城。如果沒有你們的幫助，我會被困在完全的黑暗裡，被洗腦。」

使用我們服務的人很少發聲，他們大多沒有辦法，或覺得無法安全地傳出訊息。每次有一則訊息傳過來，都提醒我們這份工作真正關係到什麼。

我們是 Unredacted，註冊在美國的 501(c)(3) 非營利組織（美國稅法下的免稅公益組織）。我們建立並維運網路基礎設施，協助大家連上開放的網路、保護自己的隱私權，做法是在全球維運一個超過 300 台伺服器的網路。前門被鎖住時，我們是另一條通道，公共廣場不再安全時，我們是還能交談的地方。

這份工作大多看不見，包括資料中心作業、硬體、自動化、開源軟體、頻寬、濫用通報的處理、監控警報，以及為了讓一切維持上線而熬過的深夜。

我們的工作分成三個方向。Censorship Evasion（繞過審查）是 Unredacted Door 所在的地方，所有用來繞過封鎖的服務都收在這個名稱底下。Secure Infrastructure（安全基礎設施）底下有 [XMPP.is](https://xmpp.is/)、我們的 Matrix homeserver，以及其他以安全與隱私為前提的免費服務。Unredacted Education 是寫作與文件的部分，提供指南與說明給想理解這些工作、想自行複製一套的人。三個方向之外，我們在 Unredacted Labs 實驗還沒到正式上線等級的基礎設施構想，GreenWare 是其中之一，目標是用耗電不高的硬體承載實際的網路容量。

## Unredacted Door

名稱就是字面上的意思，通往開放網路的入口被牆封住時，人們需要另一條進去的路。

Unredacted Door 整合了我們幾項繞過審查的服務，包括 FreeSocks、Signal 與 Telegram 的訊息代理、Tor 橋接與 Snowflake 代理。最近 30 天內，這些服務替數萬名在自己國家繞過審查的使用者承載了將近 300 TiB 的流量，大約相當於串流數萬小時 4K 影片的頻寬。需求沒有減緩，我們需要繼續擴建。每一道新的過濾規則、每一條新法律、每一次打著「為了你的安全」名義推出的措施，都讓更多人去找審查者還沒發現的路。

Unredacted Door 裡規模最大的是 FreeSocks，提供給審查嚴重地區的免費代理。代理是一個轉接點，你的應用程式連到轉接的伺服器，由它把連線帶過你與外部網路之間的過濾設備，再接到被封鎖的服務。

FreeSocks 的設計目標是讓轉接點低調、不引人注意，一般 VPN 正好缺少這個特質。VPN 的端點與握手方式都是已知的，在線路上也有明顯的封包形狀，審查者很擅長封鎖可以辨識的東西。

Tor Browser 提供強度足夠的瀏覽隱私與匿名性。Snowflake 在 Tor 網路本身被封鎖時，幫使用者連上 Tor。FreeSocks 代理則讓特定流量走一條較難察覺的路徑。沒有單一工具能涵蓋所有情境，身處審查環境的人通常需要同時準備幾種，因為沒有一扇門能永遠開著。

所以我們投入相當多的心力開發 FreeSocks 第二版（v2）。v2 使用 Xray，一套強大且有彈性的流量路由引擎，可以讓代理流量更接近一般的網頁流量。

!!! note "Xray"

    Xray 是源自 V2Ray 專案的流量路由與偽裝工具，支援 VLESS、Trojan、Reality 等協定，把代理流量偽裝成一般的 HTTPS、TLS 流量。傳統 VPN 容易辨識的握手與封包樣態，在 Xray 的流量裡比較難找到，所以近年在審查嚴重的網路環境裡是常見的代理工具。詳見 [Xray-core 專案](https://github.com/XTLS/Xray-core)。

我們把 Xray 與自家開源的控制平面結合，審查者找到並封鎖某台伺服器時，系統可以自動輪替端點。使用者本來就承受壓力，需要自行調整的設定越少越好。

## GreenWare 與低耗電硬體

Tor 中繼、橋接與代理都在資料中心的硬體上執行，硬體有實際的成本，包括財務、營運與環境。如果希望隱私基礎設施能長期維持，就要問什麼樣的維運方式才真的能持續。

GreenWare 是我們在不減少承載量的前提下縮小成本的嘗試。大多數 Tor 中繼的流量，並不需要一台耗電像暖風機的伺服器。中繼需要的是穩定的網路、可預測的 CPU，以及足夠存放狀態的記憶體，只要外殼設計得夠扎實，單板電腦就能處理這種規模的工作量。

我們從 Raspberry Pi 5 主機板開始，透過 PoE（乙太網路供電）用一條網路線同時提供電力與資料。構想本身可行，資料中心典型的伺服器耗電約等於一台小型暖風機，一台 Pi 比一顆燈泡還少。不過第一代有它的上限，密度不如預期，部分配套元件也無法承受我們長時間的使用。

所以我們現在同時採用兩種部署。第一種是在 1U 機箱裡裝 20 個 ComputeBlade 模組，20 個全部部署在我們的資料中心，並把一部分 Tor 出口節點移到上面執行。機箱滿載時耗電略超過 100W，大約是一顆舊式白熾燈泡。第二種是我們自行設計的 Raspberry Pi 機箱，ComputeBlade 的經驗讓我們更清楚現場真正需要什麼。兩種都已經上線，截至撰文時，我們全部 123 個 Tor 出口節點都在這套合併後的基礎設施上執行，總耗電約 400W。專案更成熟之後，我們會再分享機箱設計與整體進展。

Tor 網路仰賴願意替它維運基礎設施的個人與組織。出口節點是其中最難的部分，需要頻寬、維護、濫用通報處理、承擔法律風險的勇氣，以及資金。如果能降低提供實際出口容量所需的成本與電力，就有更多人能分擔一部分工作，讓網路更多元、規模更大。

更長期的目標是持續推動高效率硬體、碳排追蹤，以及最終以再生能源供電的小型據點（micro points of presence）。我們很樂意與希望這件事擴大的組織和公司合作。

開放的網路能保持開放，靠的是許多個人與組織投入的心力與時間，包括量測審查的研究者、提供頻寬的中繼維運者，以及不放棄彼此的社群。Unredacted 負責的部分，是在明顯的路徑消失時，建立並維護人們可能需要的替代路徑。

---

以下三節由 anoni.net 社群補充。

## 台灣的對照

Unredacted 引用的那段使用者留言格外少見，身處審查環境的人多半沒有管道，也難以安全地對外發聲。台灣的網路環境相對自由，沒有防火長城，不要求 VPN 登記，ISP 也沒有接到國家的審查命令。正因如此，台灣有條件替被封鎖的地區架設 Tor 中繼與橋接，分擔一部分抗審查基礎設施的工作。

anoni.net 社群透過 [Tor 中繼節點觀測](/projects/pulse/)追蹤台灣 Tor 中繼節點的數量與分布。截至 2026-05-31，Onionoo（Tor 官方的中繼資料查詢服務）的資料裡，位在台灣、正在運作的中繼節點有 12 個，其中帶 Exit 旗標的只有 3 個。Unredacted 一個組織就執行 123 個出口節點，30 天承載近 300 TiB 流量，台灣全國的出口節點數量還不到他們的 3%。最新的數字見 [Tor 中繼節點觀測](/projects/pulse/)，頁面上的資料持續更新。台灣各 ASN 的 OONI 觀測涵蓋率另見 [ASN 自治網路觀測資料分析](docs:taiwan/ooni-asn-coverage/)。

正體中文的抗審查資源相對稀缺，anoni.net 的工作之一就是補齊中文資源，包括[什麼是 Tor](docs:tools/what-is-tor/)、[Tor Snowflake 橋接點](docs:tools/tor-snowflake/)、[什麼是 OONI](docs:tools/what-is-ooni/) 等基礎文件，方向與 Unredacted Education 相同。

## GreenWare 在台灣的可行性

Unredacted 用 400W 執行 123 個出口節點。以台灣一般工商業電價每度約 NT$ 3.5 至 6 估算[^1]，400W 全年運轉約 3,500 度，一年電費約 NT$ 12,000 至 21,000，在學校資訊中心或社群協作空間可以負擔的範圍內。

規模化的關鍵在硬體設計，台灣的 maker 社群對 Raspberry Pi 5 並不陌生，PoE+ HAT 與 PoE 交換器在常見的電子零售與網購通路都可以買到。ComputeBlade（20 模組的 1U 機箱）在台灣的零售管道較少，可以透過官方海外訂購或社群代購取得。校園機房比家用網路更適合，有固定 IP、學術網路頻寬，也有人定期巡檢機器。

Tor Relay 校園建立是 anoni.net 2026 年的三大主題之一，社群正把校園架設的經驗整理成 SOP（見 [Tor Relay 校園建立研究專題](/join/relay-on-campus/)與[台師大架設 Tor Relay 的經驗](/updates/2025/12/ntnu-nz/)）。之後評估架設方案的學校，可以參考 Unredacted 在 GreenWare 上的工程做法，先用 PoE 供電的 Raspberry Pi 5 試做一台 middle relay，運作穩定之後再考慮出口節點與機箱密度。

個人或小團體可以從 Snowflake proxy 開始（瀏覽器擴充套件或 Docker），幾乎沒有電費負擔，是參與抗審查基礎設施門檻最低的方式（見 [Tor Snowflake 橋接點](docs:tools/tor-snowflake/)）。

## 參與方式

想替審查地區的人多維持一條對外的路，可以從下面幾項開始：

- **了解 Unredacted**：到 [unredacted.org](https://unredacted.org/) 查看服務與透明度資訊，再決定是否透過官方管道支持伺服器、頻寬與人力成本。
- **執行 Snowflake**：門檻最低的參與方式，用瀏覽器擴充套件或 Docker 即可執行（見 [Tor Snowflake 橋接點](docs:tools/tor-snowflake/)）。
- **架設 Tor relay 或 bridge**：需要穩定的網路與一些維運時間，步驟見 [Tor Relay 架設指南](/join/setup-tor-relay/)與 [Tor WebTunnel 橋接架設指南](/join/setup-tor-webtunnel/)。
- **校園 Tor Relay**：在大專院校工作或就讀的人，可以從 [Tor Relay 校園建立研究專題](/join/relay-on-campus/)開始評估。
- **加入社群討論**：在 Matrix 與其他社群成員交換經驗，入口見[參與](/join/)，其他聯絡管道見[持續關注](/contact/)。

## 相關閱讀

- [什麼是 Tor](docs:tools/what-is-tor/)
- [什麼是 OONI](docs:tools/what-is-ooni/)
- [伊朗封網後湧進社群 Tor WebTunnel 橋接的流量](/updates/2026/05/iran-blackout-webtunnel/)
- [台師大架設 Tor Relay 的經驗](/updates/2025/12/ntnu-nz/)
- [Tor 中繼節點觀測](/projects/pulse/)
- 同系列：[Defending the public's right to know（OONI）](https://blog.torproject.org/Defending-the-right-to-know/)、[Preserving evidence: How OpenArchive fosters accountability and media sovereignty](https://blog.torproject.org/preserving-evidence-openarchive-fosters-accountability-media-sovereignty/)

[^1]: 台電 2026 年平均電價為每度 NT$ 3.7823（經濟部 2026-03-27 電價審議會決議，4 至 9 月維持平均電價），實際每度單價依用電種類與時間電價（尖峰、離峰）而有差異。資料來源：[台灣電力公司電價表](https://www.taipower.com.tw/2289/2290/46940/)。（2026-10 補註：經濟部 2026-09-18 的電價費率審議會決議暫不調整，10 月起全國平均電價仍為每度 NT$ 3.7823，見[今周刊的報導](https://www.businesstoday.com.tw/article/category/183027/post/202609180046/)。）
