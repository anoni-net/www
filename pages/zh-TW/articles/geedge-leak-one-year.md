---
title: Geedge 外洩一年後的研究回顧
description: Geedge Networks 與 MESA 實驗室的內部檔案外洩之後，研究界第一次能用商用審查設備的原始碼對照防火長城。本文整理一年來兩篇論文與民間調查確認了什麼、還不確定什麼，以及報導與論文說法之間的落差。
date: 2026-10-30
---

近三十年來，研究者幾乎只能從牆外推測防火長城如何運作，方法是送出設計過的封包，記錄哪些被擋、用什麼方式被擋，再反推背後的設備。Geedge Networks（積至公司）的內部檔案外洩之後，研究者第一次取得一家與防火長城關係密切的商用審查廠商的原始碼、建置套件與工單。USENIX Security 2026 論文的作者寫明，商用 DPI（深度封包檢測，逐筆分析連線內容、判斷要不要放行的技術）的原始碼是第一次外洩。研究者可以先讀程式碼找出特徵，再回到真實的網路比對，不必只靠黑箱推測。

一年下來，比對出來的範圍比部分報導寫的窄，量測結果顯示外洩的程式碼或與它相近的衍生版本很可能部署在防火長城的一部分設備上。同樣量測過的其他幾台防火長城設備與它不吻合，沒有任何一台設備與外洩的最新版完全相同，其他客戶國家多半停在「可能」或「無法確認」。相對地，這些結論同時有原始碼與量測兩邊的證據，比過去只靠遠端推測扎實。本文整理這一年誰做了什麼研究、確定了什麼、還不確定什麼，寫給開發規避工具、做量測研究與關心供應鏈的讀者。技術細節只寫到機制層級，想深入的讀者請讀原論文。

## 一年來的研究

外洩的檔案來自 Geedge 與 MESA 實驗室兩邊。MESA 實驗室（Massive and Effective Stream Analysis）隸屬中國科學院信息工程研究所，GFW Report 形容兩者是防火長城研發能力的重要分支。依 GFW Report 的整理，Geedge 在 2018 年於海南成立，被稱為「防火長城之父」的方濱興擔任首席科學家。FOCI 論文統計外洩的總量是 572 GiB，包含原始碼庫、專案管理紀錄、客戶的部署設定與營運資料，其中八成以上是一個 RPM 套件庫（Linux 的軟體安裝套件）的封存。

- **2025 年 9 月 8 日起**：The Globe and Mail 刊出報導，InterSecLab 在 9 月 9 日發表報告〈The Internet Coup〉，國際特赦組織的《Shadows of Control》與 Justice For Myanmar 的《Silk Road of Surveillance》也在同一個月發表。
- **2025 年 9 月 11 日**：Enlace Hacktivista 公開全部檔案，DDoSecrets 也提供下載。
- **2025 年 9 月 12 日**：GFW Report 發表外洩的分析文章，最後一次更新是 12 月 29 日。文中寫明原始碼的部分還沒有人仔細分析。
- **2026 年 2 月 19 日**：麻州大學阿默斯特分校與 GFW Report 的研究者發表 FOCI 2026 論文〈Geedge Cases〉，比對外洩檔案裡的網域與兩份常用的網域清單。
- **2026 年 4 月 24 日**：InterSecLab 發表〈MADLink〉，供應鏈系列的第一篇，主題是 Geedge 使用的伺服器與網路硬體，其中包括台灣的凌華科技。
- **2026 年 8 月**：作者群 8 月 5 日在專案網站 geedge.report 發表說明文章。論文〈Technical Analysis of the Geedge Networks Firewall Source Code Leak〉在 8 月 12 日到 14 日的 USENIX Security 2026 發表，作者來自密西根大學、帕德博恩大學、麻州大學阿默斯特分校、科羅拉多大學波德分校與 GFW Report。Risky Bulletin 在 8 月 21 日報導。

報導比檔案公開早了三天。USENIX 論文的引言寫到，幾家提前取得檔案的新聞機構與記者過去一年合作分析這批文件，角度偏向非技術面。依[〈The Internet Coup〉譯文](https://anoni.net/docs/reports/interseclab-network-coup/)的致謝，Tor Project 也是這次聯合調查的合作夥伴。聯合調查讀的是文件與工單，整理出 Geedge 的客戶、部署的國家與產品功能。在 USENIX 論文之前，原始碼本身大致還沒有人分析。學界的研究是另一條線，讀原始碼、把系統建置起來，再做遠端量測。

兩條線的證據性質不同，從文件可以知道 Geedge 賣給誰、客戶要求什麼，量測則用來判斷某一台設備的行為是否與程式碼一致。部分報導把前者的結論套到後者（例子見後面的報導與論文的措辭差距一節）。

## 原始碼裡的 TSG

### 建置與測試

USENIX 論文分析的是 Geedge 的旗艦產品天狗安全閘道（Tiangou Secure Gateway，TSG），作者形容它是可以完整整合進國家電信管制的審查平台。外洩的內部文件超過 10 萬份，光是 Git 儲存庫就有 500 多個，涵蓋五年以上的 commit 歷史，最新的檔案到 2024 年 11 月。分析的難處在於 TSG 的邏輯分散在許多儲存庫裡，同一個元件有多個分支與版本，論文還找到至少兩套各自獨立的 IP、UDP、TCP 協定堆疊（程式裡實作 IP、TCP 等基礎協定的部分）。

研究團隊依 DPI 的四個階段讀程式碼，也就是接收流量、重組與解析、比對規則、干擾連線。建置時，研究團隊從最新的標記版本著手，對應多個儲存庫與套件庫，並繞過了授權檢查。

建置完成之後，研究團隊在隔離的測試環境裡測試了 DNS、HTTP、TLS 與 QUIC（一種在 UDP 上傳輸的協定，HTTP/3 使用它）的處理，成功觸發偽造回應的注入、丟包與延後封鎖，也用規則引擎定義了一個自訂的封鎖對象。三套應用程式辨識系統（見下方第三方程式碼一節）是否都在這份建置裡運作，論文沒有交代，所以本文只寫到研究團隊建置並執行了 TSG 最新的標記版本，在本機測試了幾種協定的封鎖行為。論文刻意不公開完整的建置做法，理由見後面的研究倫理一節。

### 核心元件

TSG 由幾個分開開發、各有版本的元件組成。SAPP 是最底層的封包處理平台，MESA 實驗室從 2005 年開始開發，經過四次大改版，以 C 撰寫。SAPP 把封包整理成 TCP、UDP 串流再交給外掛，本身不做封鎖決定，只提供封鎖需要的功能。外掛分成三類，平台外掛提供共用功能，協定外掛從 DNS 查詢、TLS 與 QUIC 的交握取出網域等欄位，業務外掛用這些欄位實作封鎖之類的應用邏輯。

Stellar 是 Geedge 另外開發、以 C++ 撰寫的平台，追蹤連線狀態的能力比 SAPP 完整，外掛之間的溝通方式也更多樣。Stellar-on-SAPP 是 SAPP 的平台外掛，把 SAPP 的串流轉成 Stellar 的連線階段（session）交給 Stellar 的外掛處理，README 寫明它是兩個平台之間的過渡方案。在外洩的版本裡，Stellar 的外掛就是經由 Stellar-on-SAPP 在 SAPP 上執行。獨立的 stellar 儲存庫當時還在開發中，沒有出現在任何建置儲存庫裡，也沒有接進 TSG。

Maat 是規則引擎，封鎖規則存在 Maat 裡，外掛用取出的欄位比對規則，取得處置方式。規則可以比對的欄位很廣，包括傳輸與應用層協定、通道封裝的內外層位址、來源與目的 IP、連接埠、網域與 SNI（TLS 連線開頭以明文送出的網站名稱）、ASN（自治系統編號）與國家。Firewall 外掛同時掛在 SAPP 與 Stellar 上，彙整各路取出的欄位，查詢 Maat 之後執行封鎖。封鎖手段除了丟包與 RST（TCP 的重設封包，送出後連線就會中斷），還有限速、HTTP 與 DNS 的轉向、郵件與 SIP 的封鎖、竄改內容與延後封鎖。

作者從架構歸納出兩點，後面的比對都受它們影響。元件各自開發、各有版本，從遠端測出某一個外掛的指紋（能用來辨認某個系統或版本的特徵），不代表同一個部署也有另一個外掛，也無法推論另一個外掛的版本。封鎖決定在多條處理路徑彙整之後才做出，一條連線可能因為其中任何一條路徑的結果而被擋。

### 第三方程式碼

TSG 有三套應用程式辨識系統，用來判斷一條流量屬於哪個 App 或協定，其中兩套建立在第三方程式碼上。CBD（Context-Based Detector，前身是 AppSketch）是 TSG 自己的系統，依 Maat 載入的簽章判斷。Glimpse 的協定分類核心是懷卡托大學 Libtrace 團隊的自由軟體 libprotoident，相關的程式碼都帶著 libprotoident 的著作權聲明。Glimpse 偵測 OpenVPN 的程式碼，依論文的描述看來是 2022 年某一版 nDPI（以 GPL 授權的 DPI 函式庫）的修改複本，主要函式改了名稱，邏輯幾乎相同。第三套 QDPI 建立在 Qosmos ixEngine 上，那是商用的閉源 DPI 函式庫，作者的依據是程式碼呼叫了 ixEngine 的函式並引用它的標頭檔。

論文對 libprotoident 與 nDPI 的用詞是複製後改寫，對 Qosmos 只寫建立在它之上，沒有判斷 Geedge 是否取得授權。研究團隊把 Geedge 使用這些程式碼的情形通報 libprotoident 團隊與 Qosmos 的母公司 Enea，論文發表時雙方都已回覆，也排定了會議，回應的內容沒有公開。nDPI 不在論文列出的通報對象裡。作者認為這顯示即使是資源充足、與國家有關係的廠商，從零建立完整的協定分類也很昂貴（原文用 suggests）。這類發現需要讀原始碼才能取得，遠端量測很難判斷辨識系統用了誰的程式碼。

## 與防火長城的比對

### 比對的方法

USENIX 論文寫到，防火長城過去被認為高度集中，近年卻有越來越多證據指向多台獨立運作、分工不同的 DPI 設備，過去的量測研究也替其中幾種設備命名。DNS 注入（審查設備搶在真正的伺服器之前送回偽造的 DNS 回應）的設備分成 Injector 1、2、3，名稱來自 FOCI 2020 的〈Triplet Censors〉。送出 RST 中斷 TCP 連線的設備分成 GFW I、II、III，河南省另有一套區域性的審查，名稱來自 IEEE S&P 2025 的〈A Wall Behind A Wall〉。

研究團隊從原始碼找出可以從遠端量測的特徵，例如解析協定時的特殊處理方式，以及設定封包欄位用的自製亂數產生器。接著在兩台自己擁有的主機之間送出測試封包，比較各地審查設備的反應是否與 TSG 相同。量測涵蓋中國的防火長城、河南、哈薩克、緬甸與巴基斯坦，伊朗只測了 DNS，協定包括 DNS、IP 分片重組、TCP、TLS 與 QUIC。

論文在 TLS 一節寫到，路徑上可能不只一台審查設備。TSG 放行的測試封包仍可能被其他設備擋下，TSG 會擋的封包則只要經過 TSG 就一定被擋。我們的推論是，無法從封鎖行為判斷來源時，實測的「被擋」可能來自路徑上任何一台設備，無法單獨證明 TSG 存在。相對地，TSG 應該擋下、實測卻放行的結果，可以排除路徑上有行為相同的 TSG 元件。模組化讓情況更複雜，同一個部署可能用同一版 SAPP、不同版的 SSL 外掛，所以每一項比對只能說明一個元件。

### 吻合的部分

中國的 Injector 2 是唯一同時符合 DNS 三項特徵的注入器，包括偽造回應裡的旗標值、回應裡使用壓縮指標（DNS 封包裡重複引用網域名稱的寫法），以及解析查詢時處理壓縮指標的上限。作者認為這些結果強烈暗示（strongly suggest）TSG 提供了 Injector 2 的 DNS 注入實作。

TSG 偽造 RST 封包時，用一個自製的亂數產生器填入標頭的幾個欄位。從 GFW II 與 GFW III 送出的封包，可以反推出固定的種子值（亂數產生器的起始值），而且就是 TSG 的預設值。作者估計固定的種子值碰巧出現的機率約為 10 的負 44 次方，再加上數值與 TSG 的預設值相同，論文用 strongly indicating（強烈表示）形容兩者用了 TSG 的程式碼。

同一節也列出兩者與 TSG 的偏差，GFW II 與 GFW III 送出的 RST 都使用固定的 TTL（封包還能經過幾個路由器的計數），TSG 的 TTL 則隨內部狀態變化。2023 年 12 月的量測裡，GFW II 的 TTL 還與 TSG 一致，作者據此推測 GFW II 之後稍微改了實作。過去的研究記錄到 GFW II 每次連送的幾個 RST 完全相同，研究團隊把 TSG 設成同樣一次連送幾個 RST 時，封包之間的 IPID（IP 封包的識別欄位）會變動。

IP 分片重組也有吻合的項目，GFW II 一次重組的分片上限與 TSG 非常接近。作者在這一項的說法較保守，只寫兩者可能共用相近的程式碼（potentially share similar code）。

TLS 的測試竄改 ClientHello（TLS 連線的第一個封包）裡的各個長度欄位，看設備是否仍然解析出網域並封鎖。沒有任何設備與外洩的最新版行為完全相同，GFW II 的行為等同 TSG 較舊版本的 SSL 模組，作者推測 GFW II 解析 TLS 時用的就是這個舊版。QUIC 的結果是防火長城與哈薩克擋下的測試封包與 TSG 相同，但兩地支援的 QUIC 版本與 TSG 不同，無法完全吻合。哈薩克的解析指紋則完全符合 TSG 較舊版本的 QUIC 解析程式碼。

論文第 6 節把這些結果總結成一句：Injector 2、GFW II 與 GFW III 高度吻合，suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall。中文可以譯成「顯示外洩的 TSG 程式碼（或與它相近的衍生版本）很可能部署在中國國家防火牆的一部分」，引導這句的 suggesting 是推論的語氣，indeed（確實）是原文的強調。吻合的多半是舊版模組，geedge.report 的文章同樣寫到吻合的情況會隨時間改變，部署中的程式碼已經與外洩的版本有差異。

### 不吻合或無法判斷的部分

Injector 1 與 Injector 3 不吻合。Injector 3 在這次量測裡的旗標不同，也不再使用壓縮指標，與 2020 年最初的觀察不一樣。GFW I、河南、緬甸，以及巴基斯坦送出 RST 的那一套設備，都沒有固定的種子值。GFW III、河南、哈薩克，以及巴基斯坦送出 RST 的那一套設備，都不重組 IP 分片，直接轉送。論文註明是否重組是 TSG 設定檔可以調整的選項。

緬甸的 RST 行為可以用 TSG 的設定重現，支援的 QUIC 版本也與 TSG 完全相同，但解析指紋不符，論文的結論是 cannot confirm its use，無法確認緬甸使用 TSG。哈薩克與巴基斯坦的部分設備以丟包封鎖，測試封包是否繞過無法判定，兩地的結果在論文裡寫成 support potential TSG deployments（與可能有 TSG 部署的推論相容）。哈薩克的審查設備不送 RST，所以沒有做 RST 的比對。哈薩克雖然有 QUIC 解析與舊版完全相符的結果，論文仍然沒有把它寫成確認部署。伊朗的 DNS 旗標與 TSG 不同，衣索比亞只出現在外洩的工單裡，沒有量測。

Geedge 在這些國家有客戶的證據來自文件，論文的背景一節引用民間調查，列出哈薩克、衣索比亞、巴基斯坦與緬甸的部署，外洩的 Jira 工單也以緬甸與衣索比亞的現場為主。就 USENIX 論文的量測而言，到目前為止能與 TSG 程式碼高度吻合的，只有中國的部分設備。

### 報導與論文的措辭差距

Risky Bulletin 的報導寫 TSG 是防火長城「三種已知流量過濾能力之一」（one of the Great Firewall's three known traffic filtering capabilities），論文全文沒有這種說法。「三種」可能來自過去研究對防火長城設備的分類。DNS 注入器分成三個，論文的結果是吻合一個。送出 RST 的注入器也分成 GFW I、II、III，吻合兩個。同一篇報導引用的研究者貼文也寫到 Geedge 只是參與防火長城的廠商之一。geedge.report 首頁寫的是「China's Great Firewall is running parts of TSG」，語氣同樣比論文的推論肯定。

論文支持的說法是防火長城的一部分設備用了 TSG 或與它相近的版本，其他量測過的設備與 TSG 不吻合，由誰提供目前沒有公開的證據。論文也沒有寫 Geedge 開發了防火長城，用的詞是 ties、affiliated，以及與 MESA 實驗室的 close collaborative relationship。這個範圍比把 Geedge 等同於防火長城的說法窄很多，但它同時有原始碼裡的預設值與遠端量測兩邊的證據，過去只靠遠端推測的研究無法做到。

## 規避工具的簽章與封鎖

USENIX 論文寫到，外洩檔案裡有依客戶需求反覆封鎖特定規避工具的紀錄，對象包括 Psiphon、Tor 與 ExpressVPN、NordVPN 等常見的 VPN，手法從封鎖 IP 到比對位元組樣式都有。簽章（描述某個 App 流量特徵的規則）結合了伺服器 IP、網域名稱、TLS 指紋、憑證欄位、封包長度與位元組樣式。論文分析的一份 Confluence 文件記錄了 2024 年 3 月到 11 月間一個簽章包的多次更新，裡面的簽章風險等級在三到五之間，多數是五，另一份以中國 App 為主的測試紀錄則全部是一。具體的簽章條件寫在論文的表格裡，本文不轉述。

研究團隊在 Jira 裡搜尋 vpn，找到 182 個議題底下的 700 則紀錄，內容包括回報抽出的伺服器 IP、排定封鎖的優先順序、簽章失效之後反覆修改，以及誤擋其他服務。其中一則工單記錄 Signal 開啟反審查選項之後封鎖失效。作者的歸納是，規避工具的簽章由客戶參與調整，客戶可以回報失效、排定優先順序、標出誤擋的情況。

在 Psiphon 的紀錄裡，偵測的成本因為混淆（讓流量看起來不像任何已知協定的技術）而提高。一份分析封鎖 Psiphon 附帶損害的內部文件寫到，Psiphon 的流量沒有明顯的特徵，所以改用伺服器 IP 辨識，再加上一套白名單保護機制避免誤判。一則工單也討論了用 IP 與 SNI 封鎖時誤擋的風險。作者在結論把這件事與 TSG 的另一面並列：TSG 能以相對低的成本辨識規避工具，常常在連線一開始就比對出來。

論文裡與 TSG 封鎖 Tor 有關的內容，只有引言的對象清單與簽章的風險等級表，表裡有一項 Tor Browser。論文沒有描述 Tor Browser 簽章的內容，也沒有測試 Tor 的連線，所以無法從論文得知 TSG 如何辨識 Tor，更無法推論它能封鎖 Tor。InterSecLab 的〈The Internet Coup〉讀的是文件，報告寫到在外洩的時間點，Geedge 似乎還沒有有效對付 WebTunnel（Tor 的一種可插拔傳輸，把流量偽裝成一般的 HTTPS 網頁連線）的手段，MESA 實驗室的學生做過封鎖方法的初步研究。報告也寫明沒有找到 Geedge 發現或利用 Tor 未知漏洞的證據，並與 Tor Project 協調了揭露的方式。

FOCI 論文從網域的角度補上一塊，外洩檔案裡有多個檔案專門針對 VPN 與規避工具，包括商用 VPN 的完整伺服器清單與 Psiphon 的 CDN 網域。對規避工具的開發者來說，伺服器的 IP 與網域本身就是蒐集與封鎖的對象，流量特徵只是其中一種手段。

至於程式碼的品質，論文的結論寫 TSG 的複雜與彈性是兩面刃，增加了規避的難度，也損害了程式碼的可維護性與正確性。核心元件 SAPP 與協定外掛以缺乏記憶體安全保障的 C 撰寫，系統仍然依賴 Stellar-on-SAPP 這類過渡方案，程式碼也從多個第三方複製而來。工單裡有一則升級 AppSketch 資料庫之後 SAPP 重新啟動的紀錄，作者形容這是東拼西湊（patchwork）的開發過程，也寫到適合後續用模糊測試（fuzzing，大量送入異常輸入、找出程式錯誤的方法）與符號執行（以符號代替實際輸入、推算程式各條執行路徑的分析方法）深入研究。論文沒有提出任何 CVE 編號或可以利用的具體漏洞。

## 網域清單的涵蓋範圍

審查量測要先決定測哪些網域，常用的清單有兩份。Tranco 是依流量排名的熱門網站清單，Citizen Lab 的檢測清單由研究者與社群人工維護，依內容類型整理可能被封鎖的網站。FOCI 論文從外洩檔案擷取了 1,436 萬多個候選網域，解析過濾之後剩下 6,915,266 個。廣州與南京的量測點測 DNS 注入，可靠度較高。巴基斯坦、緬甸與阿爾及利亞的量測點測 TLS 交握是否因 SNI 被中斷，可靠度較低。每個網域測 25 次，把間歇性的封鎖也算進去。哈薩克與衣索比亞雖然是已知的客戶，研究團隊無法取得合適的量測點。

結果是外洩檔案裡實測被封鎖的網域中，298,955 個（93.7%）同時不在 Tranco 與 Citizen Lab 的清單裡。相對地，外洩檔案只涵蓋被封鎖的 Tranco 網域的 37.1% 到 61.6%。三份清單各有分工，FOCI 的說法是 Tranco 回答哪些全球熱門網站被封鎖，Citizen Lab 長期追蹤各類敏感內容，外洩檔案則呈現商用審查廠商認為值得關注的網域。

解讀這些數字之前要先理解網域的來源，FOCI 寫明不把出現在外洩檔案裡的網域當成被封鎖的網域。明確的封鎖清單屬於客戶的敏感資料，在外洩檔案裡很少見，網域多半出自內部討論客戶環境的文件，代表 Geedge 或客戶「感興趣」（of interest）的內容。數量最多的來源是 MESA 實驗室的 SNI 資料集，作者判斷看來是從網路分接（network tap，在線路上複製流量的設備）蒐集的。外洩檔案裡也有 Alexa 與 SecRank 等排名清單的複本，供 MESA 的研究使用。所以 93.7% 說明的是常用清單的缺口。外洩檔案提供了廠商端的視角，哪些網域真的被封鎖仍要靠量測確認，與 USENIX 論文先讀程式碼、再回到網路比對的做法相同。

社群維護的 Citizen Lab 檢測清單台灣部分（`anoni-net/citizenlab-test-lists` 的 `tw.csv`）同樣是人工整理的清單，反映的是維護者認為重要的內容。從 FOCI 的結果來看，用清單量測沒有測到封鎖時，結論只涵蓋清單裡的網站，清單以外的網域本來就不在觀測範圍內。單次測量如何判讀見[OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)，各網路有多少測量見[OONI 觀測涵蓋率](/projects/asn-coverage/)。

## 供應鏈與政策

InterSecLab 的〈MADLink〉從外洩文件追到硬體供應鏈。台灣上市公司凌華科技在 2019 到 2020 年初向 Geedge 出貨 1,708 台 CSA-7400（廠商行銷定位用於防火牆與 DPI 的高密度網路平台），依報告是第一代 TSG 平台的硬體基礎，外洩文件裡這套配置只部署在哈薩克。Geedge 自製的 EtherFabric（在多個 TSG 節點之間分配流量的網路封包經紀設備）部署在緬甸，外洩文件裡它的管理介面 MAC 位址的廠商前綴登記在凌華名下，InterSecLab 據此判斷裡面有凌華的元件，最可能是管理用的運算主板。

凌華科技向 InterSecLab 證實了出貨的數量，表示出貨前做了出口管制名單篩查、Geedge 不在受限名單上，並將啟動內部稽核。凌華也表示公司只提供通用的硬體平台，沒有參與與最終用途相關的軟體整合或系統設計。InterSecLab 的反駁是，外洩文件裡有 TSG-ADC 的負載平衡仰賴凌華 PacketManager 軟體的紀錄，CSA-7400 的行銷定位也是 DPI 與防火牆設備。經濟部說明台灣的出口管制框架參照國際防擴散機制與制裁清單，以法律限制為由不評論個案。

報告的論點是，Geedge 現行的伺服器多是通用的 x86 硬體，正規採購受阻時仍能從次級市場取得，CSA-7400 這類專為 DPI 與防火牆設計的設備才是出口管制能實際著力的地方。社群翻譯了[報告全文](https://anoni.net/docs/reports/interseclab-madlink/)，也記錄了[台灣公共領域對 MADLink 報告的反應](/updates/2026/05/madlink-editorial-2026-05/)。

MADLink 讀的是文件與廠商的回覆，可以對照 USENIX 論文在哈薩克的三項量測：QUIC 解析符合舊版、TLS 因為丟包無法判定、RST 無法比對。兩者之間有時間差，CSA-7400 是 2019 到 2020 年初出貨的第一代硬體，與論文的量測相隔數年，量測到的設備是否仍是那一批硬體，目前無法判斷。

MADLink 也提到，Geedge 現行硬體裡的伺服器來自 Nettrix，它的母公司中科曙光已經遭到美國制裁。Justice For Myanmar 在 2024 年 6 月 19 日的新聞稿呼籲各國政府制裁 Geedge Networks 等公司。截至 2026 年 10 月，我們在 OFAC 的公告、OpenSanctions 與公開報導裡，都沒有查到 Geedge 被列入制裁名單。

## 研究倫理與資料處理

USENIX 論文的倫理考量一節列出五類利害關係人，包括 Geedge 的員工與股東、程式碼被整合進 TSG 的第三方公司、部署 TSG 的國家、在這些國家受審查的使用者，以及反審查社群。外洩的 Git 儲存庫裡有開發者的姓名與 email，論文的處理方式是聚焦在系統與架構，不報導個人，公開的儲存庫裡也不放外洩的原始資料。

在本機運作一份 TSG 本身也有風險，可能讓部署國改進系統，或讓其他審查者更容易部署。論文因此選擇不公開架設這套防火牆的方式，公開的資料只放對辨識部署有用的內容。研究團隊也考慮過完全不在本機運作。他們的結論是，有了一份可運作的副本，反審查社群才能辨識各地的部署，對著真實的系統開發與測試規避策略，再把策略推廣到其他國家的防火牆。

量測只在研究團隊自己擁有的兩台主機之間進行，不以任何第三方伺服器為目標，租用量測點時也確認對方不在歐盟的制裁名單上。外洩的原始碼與研究團隊的建置都不公開，作者承諾依請求把建置分享給可信任的網路安全研究者，公開在 Zenodo 的是量測結果、匿名化的封包紀錄與量測用的腳本。這些取捨的結果是，其他研究者可以用公開的腳本重做遠端量測，原始碼端的對照則只有取得分享的研究者能重做。

FOCI 論文的立場是，外洩資料已經由 Enlace Hacktivista 與 DDoSecrets 公開，廣泛的公共利益優先於可能的智慧財產權疑慮。GFW Report 的分析文章則建議只在隔離、不連網的（虛擬）機器上分析這些檔案。

Lantern 的 geedge.lantern.io 採取另一種處理方式，頁面上寫它是 corpus.lantern.io 的姊妹專案，目的是讓規避工具的開發者清楚知道自己面對什麼，但頁面沒有寫明背後的團隊，與 Lantern 規避工具的關係也無法從頁面確認。索引不轉載外洩的原始內容，每一則發現都附上出處的指標。

索引裡的發現由 LLM 自動擷取，頁面寫明擷取工作由 Sonnet 等級的代理讀取批次文字完成，我們讀取時首頁列出 880 則發現。我們抽讀了五則，都標成最高的信心等級。其中三則只憑設定檔的欄位名稱就推論系統會記錄每一條連線，出處多是測試用的設定檔，也沒有 commit hash。Lantern 的索引可以當成找線索的起點，引用前要自行回到原始資料核對，不能直接當成證據。

在 net4people 的討論串裡，2025 年 10 月之後有出處的後續研究只有 FOCI 論文，其他多是留言者的比對與推測，部分留言附上外洩內部系統的鏡像連結，本文不引用。

本文也守同樣的界線，不轉載外洩檔案的內容、網域清單與檔案路徑，不寫可以用來規避偵測或改進封鎖的參數、特徵值與簽章條件（論文本身公開了一部分，想深入的讀者請讀原文），也不提外洩資料裡的人員。

## 還沒有答案的問題

Injector 1、Injector 3 與 GFW I 都與 TSG 不吻合，論文的結果只指向防火長城的一部分設備用了 TSG 或相近的程式碼，其餘設備由誰開發，目前沒有公開的證據。

哈薩克、巴基斯坦、緬甸與衣索比亞的客戶關係都有文件證據，量測卻停在可能或無法確認。FOCI 的研究團隊無法取得哈薩克與衣索比亞的量測點，USENIX 論文在哈薩克有量測點但部分項目無法判定，衣索比亞兩篇論文都沒有量測。部署端也一直在改版，外洩檔案停在 2024 年 11 月，GFW II 的 TTL 從 2023 年 12 月到論文量測時已經改變，之後的量測要把版本的差異算進去。

研究團隊的建置只載入了 DNS、SSL 與 QUIC 三個 SAPP 協定外掛，AppSketch 資料庫的封存都經過加密。簽章格式如何轉換成 Maat 的規則，論文沒有找到對應的程式碼，只從格式的相似度推論，原始碼還有許多部分沒有人審查。作者的期待是讓這篇論文成為後續研究的指引。FOCI 也列出外洩檔案裡的 IP 位址、PDF 與更好的文字辨識，以及比對 Common Crawl 與 ICANN 的網域資料，作為之後的工作。

規避工具這一端，我們在 net4people 追蹤外洩的討論串（2025 年 10 月以後的留言）裡，沒有看到 Tor、Psiphon 或 VPN 業者公開說明因應外洩做了哪些調整。Tor Project 也審閱過〈The Internet Coup〉的 Tor 一節，Psiphon 團隊審閱了 Psiphon 一節。外洩已經讓研究界能用原始碼對照真實的審查設備，下一步要看量測點是否能擴展到更多客戶國家，以及工具開發者如何運用這些結果。歡迎到社群的 [Matrix](/contact/) 一起討論。

## 參考資料

- [Technical Analysis of the Geedge Networks Firewall Source Code Leak](https://www.usenix.org/conference/usenixsecurity26/presentation/ablove)：USENIX Security 2026，密西根大學、帕德博恩大學、麻州大學阿默斯特分校、科羅拉多大學波德分校與 GFW Report
- [Geedge Cases: Censorship Measurement Insights from the Geedge Networks Leak](https://gfw.report/publications/foci26b/en/)：FOCI 2026，麻州大學阿默斯特分校與 GFW Report，2026-02-19
- [geedge.report](https://geedge.report/)：USENIX 論文作者群的專案網站，摘要文章 [Geedge firewall source code analysis](https://geedge.report/posts/2026/08/geedge-firewall-source-code-analysis/) 發表於 2026-08-05
- [Geedge & MESA Leak: Analyzing the Great Firewall's Largest Document Leak](https://gfw.report/blog/geedge_and_mesa_leak/en/)：GFW Report，2025-09-12，2025-12-29 更新
- [The Internet Coup](https://interseclab.org/research/the-internet-coup/)：InterSecLab，2025-09-09
- [MADLink: A Taiwanese Vestige in the Geedge Supply Chain](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)：InterSecLab，2026-04-24
- [Pakistan: Shadows of Control](https://www.amnesty.org/en/documents/asa33/0206/2025/en/)：國際特赦組織，2025-09
- [Silk Road of Surveillance](https://www.justiceformyanmar.org/stories/silk-road-of-surveillance)：Justice For Myanmar，2025-09
- [JFM calls for action against Chinese and Myanmar companies involved in junta digital surveillance and censorship](https://www.justiceformyanmar.org/press-releases/jfm-calls-for-action-against-chinese-and-myanmar-companies-involved-in-junta-digital-surveillance-and-censorship)：Justice For Myanmar 的新聞稿，2024-06-19
- [Leaked files show a Chinese company is exporting the Great Firewall's censorship technology](https://www.theglobeandmail.com/world/article-leaked-files-show-a-chinese-company-is-exporting-the-great-firewalls/)：The Globe and Mail，2025-09-08
- [Academics find source code overlaps between Geedge and China's Great Firewall](https://news.risky.biz/risky-bulletin-academics-find-source-code-overlaps-between-geedge-and-chinas-great-firewall/)：Risky Bulletin，2026-08-21
- [geedge.lantern.io](https://geedge.lantern.io/)：Lantern 的外洩索引，內容由 LLM 自動擷取，只能當線索

## 相關閱讀

- [網路政變](https://anoni.net/docs/reports/interseclab-network-coup/)：InterSecLab〈The Internet Coup〉的社群中譯
- [MADLink：台灣在 Geedge 供應鏈中的遺留](https://anoni.net/docs/reports/interseclab-madlink/)：InterSecLab〈MADLink〉的社群中譯
- [OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)：單次測量的判定與確認封鎖之間的差距
- [OONI 觀測涵蓋率](/projects/asn-coverage/)：台灣與鄰近地區的測量來自哪些網路
