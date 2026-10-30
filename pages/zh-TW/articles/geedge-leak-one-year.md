---
title: Geedge 外洩一年後的研究回顧
description: Geedge Networks 與 MESA 實驗室的內部檔案外洩之後，研究界第一次能用商用審查設備的原始碼對照防火長城。本文整理一年來兩篇論文與民間調查確認了什麼、還不確定什麼，以及報導與論文說法之間的落差。
date: 2026-10-30
---

近三十年來，研究者幾乎只能從牆外推測防火長城如何運作。方法是送出設計過的封包，記錄哪些被擋、用什麼方式被擋，再反推背後的設備。Geedge Networks（積至公司）的內部檔案外洩之後，研究者第一次取得一家與防火長城關係密切的商用審查廠商的原始碼、建置套件與工單。USENIX Security 2026 論文的作者寫明，商用 DPI（深度封包檢測，逐筆分析連線內容、判斷要不要放行的技術）的原始碼是第一次外洩[^blackbox]。研究者可以先讀程式碼找出特徵，再回到真實的網路比對，不必只靠黑箱推測。

一年下來，比對出來的範圍比部分報導寫的窄，從量測結果看，外洩的程式碼或與它相近的衍生版本很可能部署在防火長城的一部分設備上。同樣量測過的其他幾台防火長城設備與它不吻合，TLS 的比對裡沒有任何一台設備與外洩的最新版完全相同，其他客戶國家多半停在「可能」或「無法確認」[^summary][^nomatch][^mm-kz-pk]。相對地，這些結論同時有原始碼與量測兩邊的證據，比過去只靠遠端推測扎實。這篇回顧寫給開發規避工具、做量測研究與關心供應鏈的讀者，技術細節只寫到機制層級，想深入的讀者請讀原論文。

<details markdown="1">
<summary>給不熟悉技術的讀者</summary>

2025 年 9 月，替中國與其他國家建置網路審查系統的 Geedge Networks 發生外洩，內部檔案與原始碼都被公開。研究者第一次可以直接讀審查設備的程式，不必只從外面推測。

研究團隊把程式實際建置起來，再到真實的網路上比對。從結果看，中國防火長城有一部分設備很可能用了這套程式或相近的版本，其他設備與它不吻合，由誰開發目前沒有公開的證據。依外洩文件，Geedge 也把系統賣到哈薩克、衣索比亞、巴基斯坦與緬甸，但在這些國家，量測多半只能做到「可能」或「無法確認」。

翻牆工具與 VPN 一直是追蹤與封鎖的對象，客戶會回報哪些工具還能連線，Geedge 再調整封鎖規則。論文沒有測試 Tor。InterSecLab 的報告裡寫到，外洩時 Geedge 似乎還沒有有效封鎖 WebTunnel（Tor 把流量偽裝成一般網頁瀏覽的連線方式）的手段，InterSecLab 也沒有找到 Geedge 發現或利用 Tor 未知漏洞的證據。

外洩資料裡實測被封鎖的網站，九成以上不在研究者常用來量測的兩份網站清單裡，所以用清單量測沒有發現封鎖，不等於沒有封鎖。

Geedge 的系統大量使用 Linux、Kafka 等開源軟體，部分程式碼的使用方式可能違反授權條款。開源授權不限制用途，審查系統與 Tor 這類規避工具都建立在開源軟體上。

台灣的凌華科技在 2019 到 2020 年初出貨一批硬體給 Geedge，Geedge 至今不在我們比對的美國與歐盟制裁名單上。

想先了解背景，可以讀文件站的[網路自由為什麼重要](https://anoni.net/docs/basics/internet-freedom/)、[監控現在做得到什麼](https://anoni.net/docs/basics/surveillance-capability/)、[什麼是 Tor](https://anoni.net/docs/tools/what-is-tor/) 與 [VPN 的風險與選擇](https://anoni.net/docs/tools/vpn-guide/)。

</details>

## 一年來的研究

外洩一年來，聯合調查的團隊讀文件、整理 Geedge 的客戶與部署，學界讀原始碼、做遠端量測，兩邊取得的證據性質不同。
{: .sec-lead }

外洩的檔案來自 Geedge 與 MESA 實驗室兩邊。MESA 實驗室（Massive and Effective Stream Analysis）隸屬中國科學院信息工程研究所，GFW Report 形容兩者是防火長城研發能力的重要分支。依 GFW Report 的整理，Geedge 在 2018 年於海南成立，被稱為「防火長城之父」的方濱興擔任首席科學家。FOCI 論文統計外洩的總量是 572 GiB，包含原始碼庫、專案管理紀錄、客戶的部署設定與營運資料，其中八成以上是一個 RPM 套件庫（Linux 的軟體安裝套件）的封存[^gfwr-geedge]。

![外洩文件記錄的 Geedge 部署地點地圖，標出哈薩克、衣索比亞、巴基斯坦、緬甸，以及中國的新疆、福建、江蘇](https://assets.anoni.net/www/articles/geedge-leak-one-year-map-e2b327c5.svg){: .map-img width="720" height="426" loading="lazy" }

外洩文件記錄的 Geedge 部署地點。客戶國家用主色標示：① 哈薩克（`K18`、`K24`）、② 衣索比亞（`E21`）、③ 巴基斯坦（`P19`）、④ 緬甸（`M22`）。中國用另一種色調標示，圓點是省級防火牆專案：⑤ 新疆（`J24`）、⑥ 福建、⑦ 江蘇。身分不明的 `A24` 沒有標在圖上[^map]。
{: .fig-note }

<ol class="tl" aria-label="外洩之後一年的報導、調查與論文">
  <li><span class="tl-when">2025-09-08</span><span class="tl-b"><span class="tl-t">The Globe and Mail 的報導</span><span class="tl-d">聯合調查的成果開始見報，比檔案公開早三天</span></span></li>
  <li><span class="tl-when">2025-09-09</span><span class="tl-b"><span class="tl-t">InterSecLab〈The Internet Coup〉</span><span class="tl-d">國際特赦組織的《Shadows of Control》與 Justice For Myanmar 的《Silk Road of Surveillance》也在同一個月發表。社群有〈<a href="https://anoni.net/docs/reports/interseclab-network-coup/">網路政變</a>〉的中譯</span></span></li>
  <li class="tl-origin"><span class="tl-when">2025-09-11</span><span class="tl-b"><span class="tl-t">檔案公開</span><span class="tl-d">Enlace Hacktivista 公開全部檔案，DDoSecrets 也提供下載</span></span></li>
  <li><span class="tl-when">2025-09-12</span><span class="tl-b"><span class="tl-t">GFW Report 的分析文章</span><span class="tl-d">最後一次更新是 12 月 29 日，文中寫明原始碼的部分還沒有人仔細分析</span></span></li>
  <li class="tl-year"><span>2026</span></li>
  <li><span class="tl-when">2026-02-19</span><span class="tl-b"><span class="tl-t">FOCI 2026〈Geedge Cases〉</span><span class="tl-d">麻州大學阿默斯特分校與 GFW Report 的研究者比對外洩檔案裡的網域與兩份常用的網域清單</span></span></li>
  <li><span class="tl-when">2026-04-24</span><span class="tl-b"><span class="tl-t">InterSecLab〈MADLink〉</span><span class="tl-d">供應鏈系列的第一篇，主題是 Geedge 使用的伺服器與網路硬體，其中包括台灣的凌華科技。社群有〈<a href="https://anoni.net/docs/reports/interseclab-madlink/">MADLink</a>〉的中譯</span></span></li>
  <li><span class="tl-when">2026-08-05</span><span class="tl-b"><span class="tl-t">geedge.report 的說明文章</span><span class="tl-d">USENIX 論文的作者群在專案網站發表</span></span></li>
  <li><span class="tl-when">2026-08-12</span><span class="tl-b"><span class="tl-t">USENIX Security 2026 論文</span><span class="tl-d">〈Technical Analysis of the Geedge Networks Firewall Source Code Leak〉在 8 月 12 日到 14 日的研討會發表，作者來自密西根大學、帕德博恩大學、麻州大學阿默斯特分校、科羅拉多大學波德分校與 GFW Report</span></span></li>
  <li><span class="tl-when">2026-08-21</span><span class="tl-b"><span class="tl-t">Risky Bulletin 的報導</span><span class="tl-d">報導論文的結果，措辭比論文肯定（見後面的報導與論文的措辭差距一節）</span></span></li>
</ol>

報導比檔案公開早了三天。USENIX 論文的引言寫到，幾家提前取得檔案的新聞機構與記者過去一年合作分析這批文件，角度偏向非技術面[^early]。依[〈The Internet Coup〉譯文](https://anoni.net/docs/reports/interseclab-network-coup/)的致謝，Tor Project 也是這次聯合調查的合作夥伴[^coup-ack]。聯合調查讀的是文件與工單，整理出 Geedge 的客戶、部署的國家與產品功能。在 USENIX 論文之前，原始碼本身大致還沒有人分析[^early][^gfwr-src]。學界的研究是另一條線，讀原始碼、把系統建置起來，再做遠端量測。

從文件可以知道 Geedge 賣給誰、客戶要求什麼，量測則用來判斷某一台設備的行為是否與程式碼一致。部分報導把前者的結論套到後者（例子見後面的報導與論文的措辭差距一節）。

這篇回顧主要依據五份論文與報告，研究範圍與方法差異很大，讀原文前可以先對照下表（出處與連結見文末的參考資料）。

| 論文或報告 | 研究範圍 | 方法 | 適合的讀者 |
|---|---|---|---|
| 〈Technical Analysis of the Geedge Networks Firewall Source Code Leak〉，USENIX Security 2026 | TSG 的架構與第三方程式碼，TSG 與防火長城、河南、哈薩克、緬甸、巴基斯坦、伊朗審查設備的行為比對，以及工單裡規避工具簽章的調整紀錄 | 讀原始碼、建置最新的標記版本並在隔離環境測試，再從各地的量測點遠端比對 DNS、IP 分片、TCP、TLS 與 QUIC 的指紋[^build][^method] | 研究 DPI 指紋、審查量測與規避工具的研究者 |
| 〈Geedge Cases〉，FOCI 2026 | 外洩檔案裡出現的網域，與 Tranco、Citizen Lab 檢測清單的涵蓋差異 | 從外洩檔案擷取候選網域、解析過濾，在中國、巴基斯坦、緬甸與阿爾及利亞的量測點測 DNS 注入與 TLS SNI 封鎖，每個網域測 25 次[^foci-meas] | 維護檢測清單、決定量測目標的研究者 |
| 〈The Internet Coup〉，InterSecLab，2025 年 9 月 | Geedge 的產品、客戶國家與部署方式，與 MESA 實驗室的關係，對規避工具的處理 | 讀外洩的文件與工單，與媒體和民間組織的聯合調查分工[^coup-ack] | 想了解客戶、部署與人權影響的讀者，社群有中譯 |
| 〈MADLink〉，InterSecLab，2026 年 4 月 | TSG 三代硬體的來源與供應商，凌華科技的出貨 | 比對外洩文件裡的硬體紀錄與 MAC 位址的廠商前綴，向廠商與經濟部詢問[^madlink-hw] | 研究出口管制與供應鏈的讀者，社群有中譯 |
| 〈Geedge & MESA Leak〉，GFW Report，2025 年 9 月 | 外洩檔案的組成、Geedge 與 MESA 實驗室的背景，已發表調查的整理 | 整理檔案結構與既有的報導，附上安全處理檔案的建議[^gfwr-geedge] | 第一次接觸這批資料的研究者 |

## 原始碼裡的 TSG

研究團隊把外洩的原始碼建置成可以執行的 TSG，看出它由幾個各自開發的元件組成，三套辨識系統裡有兩套建立在第三方程式碼上。
{: .sec-lead }

### 建置與測試

USENIX 論文分析的是 Geedge 的旗艦產品天狗安全閘道（Tiangou Secure Gateway，TSG），作者形容它是可以完整整合進國家電信管制的審查平台。外洩的內部文件超過 10 萬份，光是 Git 儲存庫就有 500 多個，涵蓋五年以上的 commit 歷史，最新的檔案到 2024 年 11 月。分析的難處在於 TSG 的邏輯分散在許多儲存庫裡，同一個元件有多個分支與版本，論文還找到至少兩套各自獨立的 IP、UDP、TCP 協定堆疊（程式裡實作 IP、TCP 等基礎協定的部分）。

研究團隊依 DPI 的四個階段讀程式碼，也就是接收流量、重組與解析、比對規則、干擾連線。建置時，研究團隊從最新的標記版本著手，對應多個儲存庫與套件庫，並繞過了授權檢查。

建置完成之後，研究團隊在隔離的測試環境裡測試了 DNS、HTTP、TLS 與 QUIC（一種在 UDP 上傳輸的協定，HTTP/3 使用它）的處理，成功觸發偽造回應的注入、丟包與延後封鎖，也用規則引擎定義了一個自訂的封鎖對象[^build]。三套應用程式辨識系統（見下方第三方程式碼一節）是否都在這份建置裡運作，論文沒有交代，所以本文只寫到研究團隊建置並執行了 TSG 最新的標記版本，在本機測試了幾種協定的封鎖行為。論文刻意不公開完整的建置做法，理由見後面的研究倫理一節。

### 核心元件

TSG 由幾個分開開發、各有版本的元件組成。SAPP 是最底層的封包處理平台，MESA 實驗室從 2005 年開始開發，經過四次大改版，以 C 撰寫。SAPP 把封包整理成 TCP、UDP 串流再交給外掛，本身不做封鎖決定，只提供封鎖需要的功能。外掛分成三類，平台外掛提供共用功能，協定外掛從 DNS 查詢、TLS 與 QUIC 的交握取出網域等欄位，業務外掛用這些欄位實作封鎖之類的應用邏輯。

Stellar 是 Geedge 另外開發、以 C++ 撰寫的平台，追蹤連線狀態的能力比 SAPP 完整，外掛之間的溝通方式也更多樣。Stellar-on-SAPP 是 SAPP 的平台外掛，把 SAPP 的串流轉成 Stellar 的連線階段（session）交給 Stellar 的外掛處理，README 寫明它是兩個平台之間的過渡方案。在外洩的版本裡，Stellar 的外掛就是經由 Stellar-on-SAPP 在 SAPP 上執行。獨立的 stellar 儲存庫當時還在開發中，沒有出現在任何建置儲存庫裡，也沒有接進 TSG。

Maat 是規則引擎，封鎖規則存在 Maat 裡，外掛用取出的欄位比對規則，取得處置方式。規則可以比對的欄位很廣，包括傳輸與應用層協定、通道封裝的內外層位址、來源與目的 IP、連接埠、網域與 SNI（TLS 連線開頭以明文送出的網站名稱）、ASN（自治系統編號）與國家。Firewall 外掛同時掛在 SAPP 與 Stellar 上，彙整各路取出的欄位，查詢 Maat 之後執行封鎖。封鎖手段除了丟包與 RST（TCP 的重設封包，送出後連線就會中斷），還有限速、HTTP 與 DNS 的轉向、郵件與 SIP 的封鎖、竄改內容與延後封鎖。

從硬體到處置，TSG 的元件可以整理成六層[^madlink-gen][^thirdparty]：

<figure class="st-fig">
<svg class="st" viewBox="0 0 360 494" role="img" aria-labelledby="st-t">
<title id="st-t">TSG 的技術棧，依外洩的版本整理</title>
<defs><marker id="st-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path class="st-ah" d="M0 0L10 5L0 10z"/></marker></defs>
<rect class="st-band" x="0" y="0" width="360" height="64" rx="6"/>
<text class="st-l" x="10" y="16">處置</text>
<rect class="st-box" x="8.0" y="24" width="344.0" height="30" rx="5"/>
<text class="st-t" x="180.0" y="40.0">放行、丟包、RST、限速、轉向、竄改、延後封鎖</text>
<rect class="st-band" x="0" y="70" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="86">規則比對</text>
<rect class="st-box" x="8.0" y="94" width="163.0" height="40" rx="5"/>
<text class="st-t" x="89.5" y="108">Firewall 外掛</text>
<text class="st-s" x="89.5" y="124">彙整各路欄位</text>
<line class="st-ar" x1="173.0" y1="114.0" x2="185.0" y2="114.0" marker-end="url(#st-a)"/>
<rect class="st-box" x="189.0" y="94" width="163.0" height="40" rx="5"/>
<text class="st-t" x="270.5" y="108">Maat</text>
<text class="st-s" x="270.5" y="124">規則引擎</text>
<rect class="st-band" x="0" y="150" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="166">應用程式辨識</text>
<rect class="st-box" x="8.0" y="174" width="110.7" height="40" rx="5"/>
<text class="st-t" x="63.3" y="188">CBD</text>
<text class="st-s" x="63.3" y="204">Geedge 自有</text>
<rect class="st-box st-3p" x="124.7" y="174" width="110.7" height="40" rx="5"/>
<text class="st-t" x="180.0" y="188">Glimpse</text>
<text class="st-s" x="180.0" y="204">libprotoident、nDPI</text>
<rect class="st-box st-3p" x="241.3" y="174" width="110.7" height="40" rx="5"/>
<text class="st-t" x="296.7" y="188">QDPI</text>
<text class="st-s" x="296.7" y="204">Qosmos ixEngine</text>
<rect class="st-band" x="0" y="230" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="246">外掛</text>
<rect class="st-box" x="8.0" y="254" width="110.7" height="40" rx="5"/>
<text class="st-t" x="63.3" y="268">平台外掛</text>
<text class="st-s" x="63.3" y="284">共用功能</text>
<rect class="st-box" x="124.7" y="254" width="110.7" height="40" rx="5"/>
<text class="st-t" x="180.0" y="268">協定外掛</text>
<text class="st-s" x="180.0" y="284">DNS、SSL、QUIC</text>
<rect class="st-box" x="241.3" y="254" width="110.7" height="40" rx="5"/>
<text class="st-t" x="296.7" y="268">業務外掛</text>
<text class="st-s" x="296.7" y="284">Firewall 等</text>
<rect class="st-band" x="0" y="310" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="326">封包處理平台</text>
<rect class="st-box" x="8.0" y="334" width="169.0" height="40" rx="5"/>
<text class="st-t" x="92.5" y="348">SAPP</text>
<text class="st-s" x="92.5" y="364">C，MESA 實驗室</text>
<rect class="st-box" x="183.0" y="334" width="169.0" height="40" rx="5"/>
<text class="st-t" x="267.5" y="348">Stellar</text>
<text class="st-s" x="267.5" y="364">C++，經由 Stellar-on-SAPP</text>
<rect class="st-band" x="0" y="390" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="406">硬體（另有分配流量的 EtherFabric）</text>
<rect class="st-box" x="8.0" y="414" width="110.7" height="40" rx="5"/>
<text class="st-t" x="63.3" y="428">TSG-ADC</text>
<text class="st-s" x="63.3" y="444">CSA-7400</text>
<rect class="st-box" x="124.7" y="414" width="110.7" height="40" rx="5"/>
<text class="st-t" x="180.0" y="428">TSG-9140</text>
<text class="st-s" x="180.0" y="444">ATCA 電信設備</text>
<rect class="st-box" x="241.3" y="414" width="110.7" height="40" rx="5"/>
<text class="st-t" x="296.7" y="428">TSG-X</text>
<text class="st-s" x="296.7" y="444">x86 伺服器</text>
<rect class="st-box st-3p" x="8" y="476" width="16" height="12" rx="3"/>
<text class="st-s st-lg" x="30" y="486">建立在第三方程式碼上</text>
</svg>
<figcaption>本文依 USENIX 論文第 3 節與 MADLink 整理的簡化分層。CBD 是整合進 Firewall 外掛的函式庫，Glimpse 與 QDPI 是 Stellar 的外掛，Firewall 外掛同時掛在 SAPP 與 Stellar 上，實際的呼叫關係比分層複雜。</figcaption>
</figure>

一條連線經過 TSG 的處理可以簡化成下面這條路徑，實際上多條處理路徑同時進行，最後在 Firewall 外掛彙整[^modular]。

<ol class="flow" aria-label="TSG 處理一條連線的簡化流程">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>封包接收與重組（SAPP）</b><span class="d">接收流量，把封包整理成 TCP、UDP 串流，交給外掛</span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>欄位擷取（協定外掛）</b><span class="d">從 DNS 查詢、TLS 與 QUIC 的交握取出網域、SNI 等欄位</span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>應用程式辨識</b><span class="d">三套系統判斷流量屬於哪個 App</span><span class="out"><span>CBD：Geedge 自有</span><span>Glimpse：libprotoident、nDPI</span><span>QDPI：Qosmos ixEngine</span></span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>規則比對（Firewall 外掛與 Maat）</b><span class="d">彙整各路取出的欄位與辨識結果，比對 Maat 裡的封鎖規則</span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>處置</b><span class="d">放行，或丟包、送出 RST、限速、轉向、竄改內容、延後封鎖</span></span></li>
</ol>

作者從架構歸納出兩點，後面的比對都受它們影響。元件各自開發、各有版本，從遠端測出某一個外掛的指紋（能用來辨認某個系統或版本的特徵），不代表同一個部署也有另一個外掛，也無法推論另一個外掛的版本。封鎖決定在多條處理路徑彙整之後才做出，一條連線可能因為其中任何一條路徑的結果而被擋[^modular]。

### 第三方程式碼

TSG 有三套應用程式辨識系統，用來判斷一條流量屬於哪個 App 或協定，其中兩套建立在第三方程式碼上。CBD（Context-Based Detector，前身是 AppSketch）是 TSG 自己的系統，依 Maat 載入的簽章判斷。Glimpse 的協定分類核心是懷卡托大學 Libtrace 團隊的自由軟體 libprotoident，分類函式需要的程式碼都帶著 libprotoident 的著作權聲明。Glimpse 偵測 OpenVPN 的程式碼，依論文的描述看來是 2022 年某一版 nDPI（以 LGPL 授權的 DPI 函式庫，論文寫成 GPL）[^ndpi-license]的修改複本，主要函式改了名稱，邏輯幾乎相同。第三套 QDPI 建立在 Qosmos ixEngine 上，那是商用的閉源 DPI 函式庫，作者的依據是程式碼呼叫了 ixEngine 的函式並引用它的標頭檔[^thirdparty]。

論文對 libprotoident 與 nDPI 的用詞是複製後改寫，對 Qosmos 只寫建立在它之上，沒有判斷 Geedge 是否取得授權。研究團隊把 Geedge 使用這些程式碼的情形通報 libprotoident 團隊與 Qosmos 的母公司 Enea，論文發表時雙方都已回覆，也排定了會議，回應的內容沒有公開。nDPI 不在論文列出的通報對象裡。作者認為這顯示即使是資源充足、與國家有關係的廠商，從零建立完整的協定分類也很昂貴（原文用 suggests）[^disclose]。這類發現需要讀原始碼才能取得，遠端量測很難判斷辨識系統用了誰的程式碼[^beyond]。

## 與防火長城的比對

論文裡寫成高度吻合的只有防火長城的三台設備（Injector 2、GFW II 與 GFW III），其他設備與各客戶國家多半不吻合或無法判斷。
{: .sec-lead }

### 比對的方法

USENIX 論文寫到，防火長城過去被認為高度集中，近年卻有越來越多證據指向多台獨立運作、分工不同的 DPI 設備，過去的量測研究也替其中幾種設備命名[^gfw-multi]。DNS 注入（審查設備搶在真正的伺服器之前送回偽造的 DNS 回應）的設備分成 Injector 1、2、3，名稱來自 FOCI 2020 的〈Triplet Censors〉。送出 RST 中斷 TCP 連線的設備分成 GFW I、II、III，河南省另有一套區域性的審查，名稱來自 IEEE S&P 2025 的〈A Wall Behind A Wall〉。

研究團隊從原始碼找出可以從遠端量測的特徵，例如解析協定時的特殊處理方式，以及設定封包欄位用的自製亂數產生器。接著在兩台自己擁有的主機之間送出測試封包，比較各地審查設備的反應是否與 TSG 相同。量測涵蓋中國的防火長城、河南、哈薩克、緬甸與巴基斯坦，伊朗只測了 DNS，協定包括 DNS、IP 分片重組、TCP、TLS 與 QUIC。

比對分成四個步驟，最後判定結果，每一項比對都同時有原始碼與量測兩邊的依據[^method]：

<ol class="flow" aria-label="比對的步驟">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>原始碼分析</b><span class="d">找出可以從遠端觀察的行為，例如偽造封包的欄位、解析協定時的特殊處理</span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>本機驗證</b><span class="d">在隔離的測試環境執行 TSG，確認這些行為確實會出現</span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>遠端量測</b><span class="d">從各地的量測點，對研究團隊自己的主機送出測試封包，記錄審查設備的反應</span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>行為對照</b><span class="d">把實測的反應與 TSG 的行為逐項比較</span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>判定</b><span class="d">每一項比對歸入比對矩陣圖例裡的一種結果</span><span class="out"><span>吻合、與較舊的版本相同、部分相符</span><span>不吻合、無法判斷</span></span></span></li>
</ol>

審查設備接上網路的方式有兩種，量測能看出多少，跟設備用哪一種方式部署有關[^modes]：

<figure class="pd-fig">
<svg class="pd" viewBox="0 0 360 352" role="img" aria-labelledby="pd-t">
<title id="pd-t">鏡像模式與內聯模式的審查設備</title>
<defs><marker id="pd-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="pd-ah" d="M0 0L10 5L0 10z"/></marker>
<marker id="pd-ai" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="pd-ahi" d="M0 0L10 5L0 10z"/></marker></defs>
<text class="pd-h" x="0" y="16">鏡像模式：在線路旁邊複製流量</text>
<text class="pd-s" x="180" y="48" text-anchor="middle">原本的封包照常送達網站</text>
<line class="pd-wire" x1="74" y1="76" x2="284" y2="76" marker-end="url(#pd-a)"/>
<rect class="pd-box" x="2" y="59" width="72" height="34" rx="6"/><text class="pd-t" x="38" y="76">使用者</text>
<rect class="pd-box" x="286" y="59" width="72" height="34" rx="6"/><text class="pd-t" x="322" y="76">網站</text>
<line class="pd-tap" x1="200" y1="76" x2="200" y2="118"/><text class="pd-s" x="208" y="102">複製一份</text>
<rect class="pd-cen" x="145" y="118" width="110" height="34" rx="6"/><text class="pd-ct" x="200" y="135">審查設備</text>
<path class="pd-inj" d="M145 135 Q60 135 40 96" marker-end="url(#pd-ai)"/>
<text class="pd-s" x="2" y="174">搶在真正的回應之前，送回偽造的 DNS 回應或 RST</text>
<text class="pd-h" x="0" y="214">內聯模式：流量必須先通過審查設備</text>
<rect class="pd-box" x="2" y="243" width="72" height="34" rx="6"/><text class="pd-t" x="38" y="260">使用者</text>
<line class="pd-wire" x1="74" y1="260" x2="143" y2="260" marker-end="url(#pd-a)"/>
<rect class="pd-cen" x="145" y="243" width="90" height="34" rx="6"/><text class="pd-ct" x="190" y="260">審查設備</text>
<line class="pd-wire pd-cut" x1="235" y1="260" x2="284" y2="260"/>
<path class="pd-x" d="M252 251L268 269M268 251L252 269"/>
<rect class="pd-box" x="286" y="243" width="72" height="34" rx="6"/><text class="pd-t" x="322" y="260">網站</text>
<text class="pd-s" x="2" y="304">可以直接把封包丟掉，也可以送出 RST</text>
<text class="pd-s" x="2" y="324">從外面無法分辨丟包來自哪一台設備</text>
</svg>
<figcaption>鏡像模式的設備只取得流量的複本，無法擋下原本的封包，只能搶先送出偽造的封包。內聯模式的設備串在線路上，可以直接丟包，但從外面無法分辨丟包來自哪一台設備，所以表格裡哈薩克與巴基斯坦丟包設備的 TLS 標成「無法判斷」。</figcaption>
</figure>

論文在 TLS 一節寫到，路徑上可能不只一台審查設備。TSG 放行的測試封包仍可能被其他設備擋下，TSG 會擋的封包則只要經過 TSG 就一定被擋。我們的推論是，無法從封鎖行為判斷來源時，實測的「被擋」可能來自路徑上任何一台設備，無法單獨證明 TSG 存在。相對地，TSG 應該擋下、實測卻放行的結果，可以排除路徑上有行為相同的 TSG 元件[^asym]。元件又是模組化的，同一個部署可能用同一版 SAPP、不同版的 SSL 外掛，所以每一項比對只能說明一個元件。

Geedge 在外洩文件裡以代號稱呼各地的客戶：哈薩克是 `K18` 與 `K24`、衣索比亞是 `E21`、巴基斯坦是 `P19`、緬甸是 `M22`、新疆是 `J24`，另有一個身分不明的 `A24`[^codes]。下表整理五種協定的比對結果，地區附上外洩文件裡對應的客戶代號。這些代號對應文件記錄的客戶，不代表量測到的設備就屬於該專案。防火長城的設備依過去研究的命名分列，QUIC 的比對沒有區分防火長城的設備，另列一列[^matrix]。

<div class="match-wrap">
<table class="match" aria-label="TSG 與各地審查設備的比對結果">
<thead><tr><th scope="col">設備或地區</th><th scope="col">DNS</th><th scope="col">IP 分片</th><th scope="col">TCP RST</th><th scope="col">TLS</th><th scope="col">QUIC</th></tr></thead>
<tbody>
<tr class="grp"><th colspan="6" scope="rowgroup"><span>中國的防火長城</span></th></tr>
<tr><th scope="row">Injector 1<small>DNS 注入</small></th><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">Injector 2<small>DNS 注入</small></th><td class="m-yes">吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">Injector 3<small>DNS 注入</small></th><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">GFW I</th><td class="m-na"></td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-na"></td></tr>
<tr><th scope="row">GFW II</th><td class="m-na"></td><td class="m-part">部分</td><td class="m-yes">吻合</td><td class="m-old">舊版</td><td class="m-na"></td></tr>
<tr><th scope="row">GFW III</th><td class="m-na"></td><td class="m-unk">無法判斷</td><td class="m-yes">吻合</td><td class="m-no">不吻合</td><td class="m-na"></td></tr>
<tr><th scope="row">防火長城<small>未區分設備</small></th><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-part">部分</td></tr>
<tr class="grp"><th colspan="6" scope="rowgroup"><span>其他地區</span></th></tr>
<tr><th scope="row">河南</th><td class="m-na"></td><td class="m-unk">無法判斷</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-na"></td></tr>
<tr><th scope="row">哈薩克<small>K18、K24</small></th><td class="m-na"></td><td class="m-unk">無法判斷</td><td class="m-na"></td><td class="m-unk">無法判斷</td><td class="m-old">舊版</td></tr>
<tr><th scope="row">緬甸<small>M22</small></th><td class="m-na"></td><td class="m-no">不吻合</td><td class="m-unk">無法判斷</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td></tr>
<tr><th scope="row">巴基斯坦<small>P19，送出 RST 的設備</small></th><td class="m-na"></td><td class="m-unk">無法判斷</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-na" rowspan="2">未下結論</td></tr>
<tr><th scope="row">巴基斯坦<small>P19，丟包的設備</small></th><td class="m-na"></td><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-unk">無法判斷</td></tr>
<tr><th scope="row">伊朗</th><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
</tbody>
</table>
</div>

<ul class="match-key" aria-label="圖例">
  <li><span class="sw m-yes"></span>吻合</li>
  <li><span class="sw m-old"></span>與 TSG 較舊的版本相同</li>
  <li><span class="sw m-part"></span>部分相符</li>
  <li><span class="sw m-unk"></span>無法判斷</li>
  <li><span class="sw m-no"></span>不吻合</li>
  <li><span class="sw m-na"></span>沒有量測，或論文沒有下結論</li>
</ul>

<dl class="match-terms" aria-label="欄位說明">
  <dt>DNS</dt><dd>審查設備搶先送回的偽造 DNS 回應，比對回應裡的旗標、是否使用壓縮指標，以及解析查詢時處理壓縮指標的上限</dd>
  <dt>IP 分片</dt><dd>一個 IP 封包被切成多片送出時，審查設備是否先重組再檢查、最多重組幾片</dd>
  <dt>TCP RST</dt><dd>審查設備為了中斷連線而偽造的 RST 封包，比對標頭欄位的設定、一次送出幾個，以及能否從欄位反推出固定的種子值</dd>
  <dt>TLS</dt><dd>竄改 TLS 連線第一個封包（ClientHello）裡的各個長度欄位，看審查設備是否仍然解析出網域並封鎖</dd>
  <dt>QUIC</dt><dd>審查設備支援哪些 QUIC 版本，以及分片重組、最小封包大小與長度欄位的解析方式</dd>
</dl>

### 吻合的部分

中國的 Injector 2 是唯一同時符合 DNS 三項特徵的注入器，包括偽造回應裡的旗標值、回應裡使用壓縮指標（DNS 封包裡重複引用網域名稱的寫法），以及解析查詢時處理壓縮指標的上限。作者認為這些結果強烈暗示（strongly suggest）TSG 提供了 Injector 2 的 DNS 注入實作[^dns-inj2]。

TSG 偽造 RST 封包時，用一個自製的亂數產生器填入標頭的幾個欄位。從 GFW II 與 GFW III 送出的封包，可以反推出固定的種子值（亂數產生器的起始值），而且就是 TSG 的預設值。作者估計固定的種子值碰巧出現的機率約為 10 的負 44 次方，再加上數值與 TSG 的預設值相同，論文用 strongly indicating（強烈表示）形容兩者用了 TSG 的程式碼[^seed]。

同一節也列出兩者與 TSG 的偏差，GFW II 與 GFW III 送出的 RST 都使用固定的 TTL（封包還能經過幾個路由器的計數），TSG 的 TTL 則隨內部狀態變化。2023 年 12 月的量測裡，GFW II 的 TTL 還與 TSG 一致，作者據此推測 GFW II 之後稍微改了實作。過去的研究記錄到 GFW II 每次連送的幾個 RST 完全相同，研究團隊把 TSG 設成同樣一次連送幾個 RST 時，封包之間的 IPID（IP 封包的識別欄位）會變動[^rst-dev]。

IP 分片重組有部分相符的項目，GFW II 一次重組的分片上限與 TSG 非常接近。作者在這一項的說法較保守，只寫兩者可能共用相近的程式碼（potentially share similar code）[^frag]。

TLS 的測試會竄改 ClientHello 裡的各個長度欄位，看設備是否仍然解析出網域並封鎖。沒有任何設備與外洩的最新版行為完全相同，GFW II 的行為等同 TSG 較舊版本的 SSL 模組，作者推測 GFW II 解析 TLS 時用的就是這個舊版。QUIC 的結果是防火長城與哈薩克擋下的測試封包與 TSG 相同，但兩地支援的 QUIC 版本與 TSG 不同，無法完全吻合。哈薩克的解析指紋則完全符合 TSG 較舊版本的 QUIC 解析程式碼[^tls-quic]。

論文第 6 節把這些結果總結成一句：*"Notably, we find high levels of correspondence with GFW DNS Injector 2 and TCP GFW II and GFW III, suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall."*

譯成中文是「我們發現與 DNS Injector 2，以及 TCP 的 GFW II、GFW III 高度吻合，暗示外洩的 TSG 程式碼（或與它相近的衍生版本）確實部署在中國國家防火牆的一部分」，引導這句的 suggesting 是推論的語氣，indeed（確實）是原文的強調。GFW II 的 TLS 與哈薩克的 QUIC 對上的是 TSG 較舊的版本，GFW II 與 GFW III 的 RST 也與 TSG 有偏差，geedge.report 的文章同樣寫到吻合的情況會隨時間改變，部署中的程式碼已經與外洩的版本有差異[^summary]。

### 不吻合或無法判斷的部分

Injector 1 與 Injector 3 不吻合，其中 Injector 3 在這次量測裡的旗標不同，也不再使用壓縮指標，與 2020 年最初的觀察不一樣。GFW I、河南、緬甸，以及巴基斯坦送出 RST 的那一套設備，都無法反推出固定的種子值。IP 分片的比對裡，有幾台設備的重組行為與 TSG 的預設不同，論文註明重組與否可以在 TSG 的設定檔調整，所以本文歸為無法判斷[^nomatch]。

緬甸的 RST 行為可以用 TSG 的設定重現，支援的 QUIC 版本也與 TSG 完全相同。但解析指紋不符，論文因此寫 cannot confirm its use（無法確認使用）。哈薩克與巴基斯坦的部分設備以丟包封鎖，測試封包是否繞過無法判定，兩地的結果在論文裡寫成 support potential TSG deployments（與可能有 TSG 部署的推論相容）。哈薩克的審查設備不送 RST，所以沒有做 RST 的比對。哈薩克雖然有 QUIC 解析與舊版完全相符的結果，論文仍然沒有把它寫成確認部署[^mm-kz-pk]。伊朗的 DNS 旗標與 TSG 不同，衣索比亞只出現在外洩文件裡，沒有量測。

Geedge 在這些國家有客戶的證據來自文件。論文的背景一節引用民間調查，列出哈薩克、衣索比亞、巴基斯坦與緬甸的部署，研究團隊在 Jira 搜尋 vpn 得到的紀錄也以緬甸與衣索比亞的現場為主[^civil]。USENIX 論文的量測裡，寫成高度吻合（high levels of correspondence）的只有中國的部分設備[^summary]。

### 報導與論文的措辭差距

Risky Bulletin 的報導寫 TSG 是防火長城「三種已知流量過濾能力之一」（one of the Great Firewall's three known traffic filtering capabilities）[^risky]，論文全文沒有這種說法[^no-three]。「三種」可能來自過去研究對防火長城設備的分類。DNS 注入器分成三個，論文的結果是吻合一個。送出 RST 的注入器也分成 GFW I、II、III，吻合兩個。同一篇報導引用的研究者貼文也寫到 Geedge 只是參與防火長城的廠商之一[^risky]。geedge.report 首頁的粗體標題寫「China's Great Firewall is running parts of TSG」，語氣比論文肯定，同一條的說明則改用 appears to be[^geedge-home]。

論文支持的說法是防火長城的一部分設備用了 TSG 或與它相近的版本，其他量測過的設備與 TSG 不吻合，由誰提供目前沒有公開的證據。論文也沒有寫 Geedge 開發了防火長城，用的詞是 ties、affiliated，以及與 MESA 實驗室的 close collaborative relationship[^ties]。比起把 Geedge 等同於防火長城的說法，論文支持的範圍窄很多，但同時有原始碼裡的預設值與遠端量測兩邊的證據，過去只靠遠端推測的研究無法做到。

## 規避工具的簽章與封鎖

TSG 對規避工具的簽章會依客戶的回報反覆調整，Psiphon 這類沒有明顯流量特徵的工具，則改用伺服器 IP 封鎖。
{: .sec-lead }

USENIX 論文寫到，外洩檔案裡有依客戶需求反覆封鎖特定規避工具的紀錄，對象包括 Psiphon、Tor 與 ExpressVPN、NordVPN 等常見的 VPN，手法從封鎖 IP 到比對位元組樣式都有。簽章（描述某個 App 流量特徵的規則）結合了伺服器 IP、網域名稱、TLS 指紋、憑證欄位、封包長度與位元組樣式。論文分析的一份 Confluence 文件記錄了 2024 年 3 月到 11 月間一個簽章包的多次更新，裡面的簽章風險等級在 3 到 5 之間，多數是 5，另一份以中國 App 為主的測試紀錄則全部是 1[^circ]。具體的簽章條件寫在論文的表格裡，本文不轉述。

| 工具 | 外洩資料與研究裡的處理方式 |
|---|---|
| 商用 VPN（ExpressVPN、NordVPN 等） | 簽章結合伺服器 IP、網域、TLS 指紋、憑證欄位與位元組樣式，依客戶的回報反覆調整[^circ]。外洩檔案裡也有 NordVPN 的完整伺服器清單[^foci-vpn] |
| Psiphon | 依內部文件，沒有明顯的流量特徵，所以改用伺服器 IP 封鎖，再加上白名單避免誤擋[^psiphon]。外洩檔案裡有 Psiphon 的 CDN 網域[^foci-vpn] |
| OpenVPN | 偵測的程式碼看來取自開源的 nDPI[^thirdparty] |
| Tor | 列在簽章的風險等級表裡，USENIX 論文沒有描述簽章的內容，也沒有測試 Tor 的連線[^tor] |
| WebTunnel | Tor 的一種可插拔傳輸，把流量偽裝成一般的 HTTPS 網頁連線。外洩時 Geedge 看來還沒有有效的封鎖手段，MESA 實驗室的學生做過封鎖方法的初步研究[^webtunnel] |
| Signal | 一則工單記錄 Signal 開啟反審查選項之後，封鎖就失效了[^circ] |

研究團隊在 Jira 裡搜尋 vpn，找到 182 個議題底下的 700 則紀錄，內容包括回報抽出的伺服器 IP、排定封鎖的優先順序、簽章失效之後反覆修改，以及誤擋其他服務。作者的歸納是，規避工具的簽章由客戶參與調整，客戶可以回報失效、排定優先順序、標出誤擋的情況[^circ]。

在 Psiphon 的紀錄裡，偵測的成本因為混淆（讓流量看起來不像任何已知協定的技術）而提高。一份分析封鎖 Psiphon 附帶損害的內部文件寫到，Psiphon 的流量沒有明顯的特徵，所以改用伺服器 IP 辨識，再加上一套白名單保護機制避免誤判。一則工單也討論了用 IP 與 SNI 封鎖時誤擋的風險。作者在結論裡也寫到相反的一面，TSG 能以相對低的成本辨識規避工具，常常在連線一開始就比對出來[^psiphon]。

論文裡與 TSG 封鎖 Tor 有關的內容，只有引言的對象清單與簽章的風險等級表，表裡有一項 Tor Browser[^tor]。論文沒有描述 Tor Browser 簽章的內容，也沒有測試 Tor 的連線，所以無法從論文得知 TSG 如何辨識 Tor，更無法推論它能封鎖 Tor。InterSecLab 的〈The Internet Coup〉以文件為依據，報告裡寫到在外洩的時間點，Geedge 似乎還沒有有效對付 WebTunnel 的手段，MESA 實驗室的學生做過封鎖方法的初步研究。InterSecLab 也寫明沒有找到 Geedge 發現或利用 Tor 未知漏洞的證據，並與 Tor Project 協調了揭露的方式[^webtunnel]。

FOCI 論文從網域的角度提供了另一組資料。外洩檔案裡有多個檔案專門針對 VPN 與規避工具，包括 NordVPN 的完整伺服器清單與 Psiphon 的 CDN 網域[^foci-vpn]。對規避工具的開發者來說，伺服器的 IP 與網域本身就是蒐集與封鎖的對象，流量特徵只是其中一種手段。

論文的結論寫 TSG 的複雜與彈性是兩面刃，增加了規避的難度，也損害了程式碼的可維護性與正確性。核心元件 SAPP 與協定外掛以缺乏記憶體安全保障的 C 撰寫，系統仍然依賴 Stellar-on-SAPP 這類過渡方案，程式碼也從多個第三方複製而來。工單裡有一則升級 AppSketch 資料庫之後 SAPP 重新啟動的紀錄，作者形容這是拼湊式（patchwork）的開發過程，也寫到適合後續用模糊測試（fuzzing，大量送入異常輸入、找出程式錯誤的方法）與符號執行（以符號代替實際輸入、推算程式各條執行路徑的分析方法）深入研究。論文沒有提出任何 CVE 編號或可以利用的具體漏洞[^no-cve]。

## 網域清單的涵蓋範圍

外洩檔案裡實測被封鎖的網域，九成以上不在研究者常用的兩份清單裡，只用常用清單量測，只能看到審查範圍的一部分。
{: .sec-lead }

審查量測要先決定測哪些網域，常用的清單有兩份。Tranco 是依流量排名的熱門網站清單，Citizen Lab 的檢測清單由研究者與社群人工維護，依內容類型整理可能被封鎖的網站。FOCI 論文從外洩檔案擷取了 14,365,453 個候選網域，解析過濾之後剩下 6,915,266 個。廣州與南京的量測點測 DNS 注入，可靠度較高。巴基斯坦、緬甸與阿爾及利亞的量測點測 TLS 交握是否因 SNI 被中斷，可靠度較低。每個網域測 25 次，把間歇性的封鎖也納入。哈薩克與衣索比亞雖然是已知的客戶，研究團隊無法取得合適的量測點[^foci-meas]。

結果是外洩檔案裡實測被封鎖的網域中，298,955 個（93.7%）同時不在 Tranco 與 Citizen Lab 的清單裡。相對地，外洩檔案只涵蓋被封鎖的 Tranco 網域的 37.1% 到 61.6%。三份清單各有分工。依 FOCI 的說法，Tranco 用來看哪些全球熱門網站被封鎖，Citizen Lab 的清單用來長期追蹤各類敏感內容，外洩檔案則反映商用審查廠商認為值得關注的網域[^foci-937]。

FOCI 寫明不把出現在外洩檔案裡的網域當成被封鎖的網域。明確的封鎖清單屬於客戶的敏感資料，在外洩檔案裡很少見，網域多半出自內部討論客戶環境的文件，代表 Geedge 或客戶「感興趣」（of interest）的內容。數量最多的來源是 MESA 實驗室的 SNI 資料集，作者判斷看來是從網路分接（network tap，在線路上複製流量的設備）蒐集的。外洩檔案裡也有 Alexa 與 SecRank 等排名清單的複本，供 MESA 的研究使用[^of-interest]。所以 93.7% 反映的是常用清單的缺口，哪些網域真的被封鎖仍要靠量測確認，與 USENIX 論文先讀程式碼、再回到網路比對的做法相同。

社群維護的 Citizen Lab 檢測清單台灣部分（`anoni-net/citizenlab-test-lists` 的 `tw.csv`）同樣是人工整理的清單，反映的是維護者認為重要的內容。從 FOCI 的結果來看，用清單量測沒有測到封鎖時，結論只涵蓋清單裡的網站，清單以外的網域本來就不在觀測範圍內。單次測量如何判讀見[OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)，各網路有多少測量見[OONI 觀測涵蓋率](/projects/asn-coverage/)。

## 供應鏈與政策

InterSecLab 從外洩文件追查到 Geedge 有一部分硬體來自台灣的凌華科技，但在我們比對的美國與歐盟制裁名單裡，至今沒有 Geedge。
{: .sec-lead }

InterSecLab 在〈MADLink〉裡從外洩文件追查硬體供應鏈。台灣的凌華科技在 2019 到 2020 年初經由凌華的北京分公司，向 Geedge 出貨 1,708 台 CSA-7400（廠商行銷定位用於防火牆與 DPI 的高密度網路平台），依報告是第一代 TSG 平台的硬體基礎，外洩文件裡這套配置只部署在哈薩克。Geedge 自製的 EtherFabric（在多個 TSG 節點之間分配流量的網路封包經紀設備）部署在緬甸。外洩文件裡它的管理介面 MAC 位址的廠商前綴登記在凌華名下，InterSecLab 據此判斷裡面有凌華的元件，最可能是管理用的運算主板[^madlink-hw]。

外洩文件裡，Geedge 的 TSG 用過三代硬體，另有一項自製的 EtherFabric[^madlink-gen]：

| 產品 | 硬體 | 供應商 | 部署地點 |
|---|---|---|---|
| 第一代 TSG-ADC | CSA-7400 高密度網路平台 | 凌華科技（台灣） | 哈薩克 |
| 第二代 TSG-9140 | ATCA 規格的電信設備，看來以 VELA ATCA 平台為基礎 | 北京恒光信息技術 | 衣索比亞（`E21`） |
| 現行 TSG-X | 通用的 x86 運算伺服器與儲存伺服器 | Nettrix（中科曙光的子公司）、浪潮 | 衣索比亞（`E21`）、巴基斯坦（`P19`）、緬甸（`M22`） |
| EtherFabric | 看來沿用 TSG-9140 的 VELA ATCA 硬體，部分網路元件可能來自凌華 | 北京恒光信息技術、凌華科技 | 緬甸（`M22`），`A24` 的概念驗證 |

凌華科技向 InterSecLab 證實了出貨的數量，表示出貨前做了出口管制名單篩查、Geedge 不在受限名單上，並將啟動內部稽核。凌華也表示公司只提供通用的硬體平台，沒有參與和最終用途相關的軟體整合或系統設計。InterSecLab 的反駁是，外洩文件裡有 TSG-ADC 的負載平衡仰賴凌華 PacketManager 軟體的紀錄，CSA-7400 的行銷定位也是 DPI 與防火牆設備[^adlink]。經濟部說明台灣的出口管制框架參照國際防擴散機制與制裁清單，以法律限制為由不評論個案。

報告的論點是，Geedge 現行的伺服器多是通用的 x86 硬體，正規採購受阻時仍可能從次級市場取得，CSA-7400 這類專為 DPI 與防火牆設計的設備才是出口管制能實際著力的地方[^adlink]。社群翻譯了[報告全文](https://anoni.net/docs/reports/interseclab-madlink/)，也記錄了[台灣公共領域對 MADLink 報告的反應](/updates/2026/05/madlink-editorial-2026-05/)。

MADLink 的依據是文件與廠商的回覆，可以對照 USENIX 論文在哈薩克的三項量測：QUIC 解析符合舊版、TLS 因為丟包無法判定、RST 無法比對。兩者之間有時間差，CSA-7400 是 2019 到 2020 年初出貨的第一代硬體，與論文的量測相隔數年。量測到的設備是否仍是那一批硬體，目前無法判斷[^gap]。

MADLink 也提到，Geedge 現行硬體裡的伺服器來自 Nettrix，它的母公司中科曙光已經遭到美國制裁[^adlink]。Justice For Myanmar 在 2024 年 6 月 19 日的新聞稿呼籲各國政府制裁 Geedge Networks 等公司[^jfm]。截至 2026 年 10 月 30 日，我們比對美國財政部 OFAC 與歐盟的制裁名單、美國聯邦公報的實體清單公告，都沒有查到 Geedge 被列入[^sanction]。

## 審查系統裡的開源軟體

Geedge 的系統從作業系統到協定辨識都用了開源軟體，部分程式碼的納入方式可能違反授權條款，研究這套系統的人同樣仰賴開源工具。
{: .sec-lead }

依 MADLink，Geedge 的整套軟體建立在開源基礎上。外洩文件也記錄 Geedge 曾考慮改用華為的 EulerOS，因為授權費用過高而放棄[^oss-stack]。兩份報告與 USENIX 論文提到的開源專案有七個[^oss-coup][^thirdparty]：

| 開源專案 | 在 Geedge 系統裡的用途 | 出處 |
|---|---|---|
| Rocky Linux（更早是 CentOS） | 作業系統 TSG-OS 的基礎 | MADLink |
| DPDK | 封包處理，以及轉送平面 MARSIO，讓網路堆疊不受限於特定的硬體廠商 | MADLink、〈The Internet Coup〉 |
| Apache Kafka | 監控資料倉儲 TSG Galaxy 的基礎 | 〈The Internet Coup〉 |
| tcpdump | 改成 tcpdump_mesa，用來擷取應用程式的指紋 | 〈The Internet Coup〉 |
| Grafana | 管理監控方案 Network Zodiac 看來以它為範本 | 〈The Internet Coup〉 |
| libprotoident | Glimpse 的協定分類核心，程式碼帶著它的著作權聲明 | USENIX 論文 |
| nDPI | Glimpse 偵測 OpenVPN 的程式碼，看來是修改過的複本 | USENIX 論文 |

MADLink 的論點是，Geedge 的軟體是開源的，現行的伺服器又是通用的 x86 硬體，正規採購受阻時仍可以從次級市場取得，所以出口管制能實際著力的只有 CSA-7400 這類專用硬體[^oss-export]。

〈The Internet Coup〉寫到 Geedge 以可能違反授權條款的方式納入開源程式碼，推測是為了更快推出與領先對手相當的產品，同時增強承受制裁的能力[^oss-license]。libprotoident 與 nDPI 目前都以 LGPL-3.0 授權[^ndpi-license]，商業產品可以使用這些函式庫，散布時則要履行條款，例如提供修改後的函式庫原始碼。Geedge 把系統交給客戶時是否履行了這些條款，報告與論文都沒有下定論。

開源授權的共同原則是不限制使用的領域，開放原始碼促進會的開源定義第 6 條規定授權不得限制任何人把程式用在特定領域，自由軟體基金會定義的第 0 條自由是為任何目的執行程式[^oss-principle]。授權約束的是散布與修改時的義務，用途不在約束範圍內，建置審查與監控系統的廠商也能取用同一批程式碼。〈The Internet Coup〉描述被封鎖的 Tor 與 Psiphon 時，也都寫成免費、開放原始碼的工具[^oss-tools]。**我們的看法是，同一個開源生態系同時供應了審查的一方與規避的一方，這是開放的代價之一。**社群能做的是持續揭露這類使用，並讓規避工具與量測工具保持開放、容易取得。

USENIX 論文寫到，過去外界對 DPI 內部邏輯的了解，除了量測，主要來自 Snort、Suricata、Zeek 與 nDPI 這些開源系統。研究團隊的 TLS 測試封包也是擴充開源工具 Censor-Scanner 產生的，InterSecLab 的聯合調查則用開源的 Datashare 與 Apache Tika 整理外洩文件[^oss-research]。USENIX 論文依開放科學的政策公開量測結果與腳本，但不公開外洩的原始碼與研究團隊的建置，理由是審查者因此受益的風險大於對社群的好處（見下一節）[^open-science]。

## 研究倫理與資料處理

兩篇論文都不公開外洩的原始資料，USENIX 論文也不公開建置 TSG 的完整做法，外界能重現的主要是遠端量測。
{: .sec-lead }

USENIX 論文的倫理考量一節列出五類利害關係人，包括 Geedge 的員工與股東、程式碼被整合進 TSG 的第三方公司、部署 TSG 的國家、在這些國家受審查的使用者，以及反審查社群。外洩的 Git 儲存庫裡有開發者的姓名與 email，論文的處理方式是聚焦在系統與架構，不報導個人，公開的儲存庫裡也不放外洩的原始資料[^local]。

在本機運作一份 TSG 本身也有風險，可能讓部署國改進系統，或讓其他審查者更容易部署。論文因此選擇不公開架設這套防火牆的方式，公開的資料只放對辨識部署有用的內容。研究團隊也考慮過完全不在本機運作。他們的結論是，有了一份可運作的副本，反審查社群才能辨識各地的部署，對著真實的系統開發與測試規避策略，再把策略推廣到其他國家的防火牆[^local]。

量測只在研究團隊自己擁有的兩台主機之間進行，不以任何第三方伺服器為目標，租用量測點時也確認對方不在歐盟的制裁名單上。外洩的原始碼與研究團隊的建置都不公開，作者承諾依請求把建置分享給可信任的網路安全研究者，公開在 Zenodo 的是量測結果、匿名化的封包紀錄與量測用的腳本。結果是其他研究者可以用公開的腳本重現遠端量測，原始碼端的對照則只有取得分享的研究者能重現[^share]。

FOCI 論文的立場是，外洩資料已經由 Enlace Hacktivista 與 DDoSecrets 公開，廣泛的公共利益優先於可能的智慧財產權疑慮。GFW Report 的分析文章則建議只在隔離、不連網的（虛擬）機器上分析這些檔案[^foci-ethics]。

Lantern 的 geedge.lantern.io 是從外洩資料擷取發現的索引，處理方式又不一樣。頁面上寫它是 corpus.lantern.io 的姊妹專案，目的是讓規避工具的開發者清楚知道自己面對什麼，但沒有寫明背後的團隊，與 Lantern 規避工具的關係也無法從頁面確認[^lantern-site]。索引不轉載外洩的原始內容，每一則發現都附上出處的資訊。

索引裡的發現由 LLM 自動擷取，頁面寫明擷取工作由 Sonnet 等級的代理程式（agent）讀取批次文字完成，我們讀取時首頁列出 880 則發現。我們抽讀了五則，都標成最高的信心等級。其中三則只憑資料表的欄位名稱就推論系統會記錄每一條連線，出處多是測試用的設定檔，也沒有 commit hash[^lantern]。Lantern 的索引可以當成找線索的起點，引用前要自行回到原始資料核對，不能直接當成證據。

在 net4people 的討論串裡，2025 年 10 月之後有出處的後續研究只有 FOCI 論文，其他多是留言者的比對與推測[^n4p]，部分留言附上外洩內部系統的鏡像連結，本文不引用。

本文也守同樣的界線，不轉載外洩檔案的內容、網域清單與檔案路徑，不寫可以用來規避偵測或改進封鎖的參數、特徵值與簽章條件（論文本身公開了一部分，想深入的讀者請讀原文），也不提外洩資料裡的人員。

## 還沒有答案的問題

A24 的身分、防火長城其他設備的來源，以及各客戶國家的部署能否用量測確認，都還沒有公開的答案。
{: .sec-lead }

Injector 1、Injector 3 與 GFW I 都與 TSG 不吻合，論文的結果只指向防火長城的一部分設備用了 TSG 或相近的程式碼，其餘設備由誰開發，目前沒有公開的證據。

InterSecLab 在 2025 年 9 月寫到，`A24` 的相關資料沒有能辨識客戶的地點或 ISP，唯一的線索是首字母 A 與年份 2024，而代號的數字也不一定代表年份。外洩時雙方的關係還在初期，Geedge 為它做過鏡像與內聯兩種模式的概念驗證。2026 年 4 月的〈MADLink〉裡仍稱它為只以代號識別的未知客戶，並補充 Geedge 的 EtherFabric 也曾在 `A24` 做概念驗證。兩篇論文、GFW Report 與 net4people 的討論串裡，也都沒有出現新的線索[^a24]。

哈薩克、巴基斯坦、緬甸與衣索比亞的客戶關係都有文件證據，量測卻停在可能或無法確認。FOCI 的研究團隊無法取得哈薩克與衣索比亞的量測點，USENIX 論文在哈薩克有量測點但部分項目無法判定，衣索比亞兩篇論文都沒有量測。部署端也一直在改版，外洩檔案停在 2024 年 11 月，GFW II 的 TTL 從 2023 年 12 月到論文量測時已經改變[^rst-dev]，之後的量測要把版本的差異納入考量。

研究團隊的建置只載入了 DNS、SSL 與 QUIC 三個 SAPP 協定外掛，AppSketch 資料庫的封存都經過加密。簽章格式如何轉換成 Maat 的規則，作者沒有找到對應的程式碼，只從格式的相似度推論，論文也沒有涵蓋原始碼的其餘部分。作者的期待是讓這篇論文成為後續研究的指引。FOCI 列出的後續工作包括搜尋外洩檔案裡的 IP 位址、分析 PDF 等文件、改進文字辨識（OCR），以及比對 Common Crawl 與 ICANN 的網域資料[^future]。

規避工具這一端，我們在 net4people 追蹤外洩的討論串（2025 年 10 月以後的留言）裡，沒有看到 Tor、Psiphon 或 VPN 業者公開說明因應外洩做了哪些調整[^n4p]。Tor Project 也審閱過〈The Internet Coup〉的 Tor 一節，Psiphon 團隊審閱了 Psiphon 一節[^coup-ack]。有了外洩的原始碼，研究界已經能對照真實的審查設備，下一步要看量測點是否能擴展到更多客戶國家，以及工具開發者如何運用這些結果。歡迎到社群的 [Matrix](/contact/) 一起討論。

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

[^blackbox]: USENIX 論文 §1：「Traditionally, the study of DPI-based censorship systems has relied almost exclusively on black-box analysis」、「This is the first time that the source code of a commercial DPI has been leaked」。
[^summary]: USENIX 論文 §6：「Notably, we find high levels of correspondence with GFW DNS Injector 2 [9] and TCP GFW II and GFW III [47], suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall」。§6.4：「While no middlebox exhibited exactly the same behavior as the latest leaked TSG」。geedge.report〈Geedge firewall source code analysis〉：「The match is not frozen in time」、「the deployed code has drifted from the leaked version」。
[^nomatch]: USENIX 論文 Table 5 的說明：「Injector 3 has different flags and no longer uses compression pointers, different from the initial observation」。Injector 1 不吻合的依據是 §6.1 的同一句，只有 Injector 2 同時具備三項特徵。§6.3：「In contrast, the other injectors exhibit markedly different behaviors and header values」、「While we did not observe the seed key correspondence in other regions」，前一句涵蓋 GFW I，後一句涵蓋其他地區。Table 7 的說明：「"no" also includes cases where TCP window values remain identical all the time rendering k undefined」。§6.2：「This is configurable」，指 TSG 設定檔裡的重組選項。哪些設備的重組行為不同寫在論文的 Table 6，本文不轉述。
[^mm-kz-pk]: USENIX 論文 §6.3：「TSG can be configured to match the behavior in Myanmar」、「We did not test in Kazakhstan because its censors do not generate TCP RST packets」。§6.5：「We also find the supported QUIC versions in Myanmar align exactly with those supported by TSG's QUIC, though the parsing fingerprint mismatch means we cannot confirm its use」。§6.4：「both Kazakhstan and Pakistan (DROP) support potential TSG deployments, as their generic censorship mechanism of packet drops makes bypass failures inconclusive」。正文寫論文沒有把哈薩克寫成確認部署，這是本文的查證，在論文全文搜尋 confirm（不分大小寫）共 4 筆，分別在 §2.1、Figure 2 的工單、§6.3 與 §6.5，沒有一筆確認哈薩克的部署，§6 提到 Kazakhstan 的句子也沒有這樣的說法。伊朗的部分見 Table 5，伊朗那一列的旗標、壓縮指標與上限三項都與 TSG 不同。衣索比亞不在 Table 10 列出的量測點裡，Table 10 只有河南、北京、阿拉木圖、仰光、喀拉蚩與伊斯蘭馬巴德。
[^gfwr-geedge]: GFW Report〈Geedge & MESA Leak〉：「This leak originates from an important branch of the GFW's R&D capacity」、「Geedge (Hainan) Information Technology Co., Ltd. (Geedge Networks Ltd.) was founded in the same year. Fang served as chief scientist」。同一段的 same year 指 2018 年。FOCI 論文 §2.1：「572 GiB of internal documents from Geedge Networks and the related MESA lab including source code repositories, project management records, client deployment configurations, and operational data」。八成以上是本文依 USENIX 論文 Table 1 的計算，RPM 套件庫的封存占 463.0 GiB，約為總量的 81%。
[^map]: 網路政變社群譯文第 6 章〈Geedge 的營運與客戶〉：「目前辨識出的客戶代號有哈薩克（`K18` 與 `K24`）、巴基斯坦（`P19`）、衣索比亞（`E21`）、緬甸（`M22`）與新疆（`J24`）」。第 2 章〈主要發現〉：「InterSecLab 已經確認新疆、福建與江蘇的省級防火牆專案」。原報告第 6 章另有一張 Geedge 營運地區的地圖（圖 14）。本文的地圖依這些文字重畫，圓點位置標在各省省會附近，只表示省分，不代表實際的部署地點。國界資料來自 Natural Earth 1:50m（公有領域）。
[^early]: USENIX 論文 §1：「Several news organizations and journalists who were granted early access have worked together for the past year to analyze the documents from a non-technical perspective」、「The current reporting is mostly geared to non-technical audiences」、「leaving the source code itself largely unexplored」。
[^coup-ack]: 網路政變社群譯文第 8 章〈結論、反思與下一步〉的致謝：「與國際特赦組織、Justice For Myanmar、Paper Trail Media、《環球郵報》（The Globe and Mail）、Tor Project、奧地利《標準報》（DER STANDARD）與 Follow The Money 等夥伴共同合作」。同一段也寫到「也感謝 Tor Project 團隊審閱 Tor 一節，以及 Psiphon 團隊提供寶貴資訊並審閱 Psiphon 一節」。
[^gfwr-src]: GFW Report〈Geedge & MESA Leak〉：「The source-code portion of the leaked files has not yet been carefully analyzed」。
[^build]: USENIX 論文 §1：「we successfully build and run TSG's latest tagged release version」。§5.2：「We were able to successfully test the DNS, HTTP, TLS, and QUIC protocols and trigger injection responses, packet drops, and deferred blocking actions」。
[^method]: USENIX 論文 §5.2：「We developed a testbed to evaluate TSG's blocking behaviors in a controlled environment」。Ethical Considerations：「We performed all of our scans between two vantage points that we own, not including any other third-party server as the target of our scan」。從原始碼找出指紋再量測的做法見 §1：「we extract several fingerprints from TSG, including custom random number generators and parsing idiosyncrasies」。
[^foci-meas]: FOCI 論文 §3.2：「we produce a list of 14,365,453 potential domains」、「we produce a final list of 6,915,266 domains」。§3.4：「we perform measurements across vantage points in China (Guangzhou and Nanjing), Myanmar, Pakistan, and Algeria」、「While Kazakhstan and Ethiopia are known customers of Geedge Networks [12], we were unable to obtain access to appropriate vantage points in these countries」、「DNS censorship is highly reliable」、「which are inherently less reliable indicators」、「we perform 25 tests per domain to ensure intermittently blocked domains are included」。
[^madlink-hw]: MADLink 社群譯文第 1 章〈摘要與主要發現〉：「這批設備構成 Geedge 第一代防火牆平台的基礎」。第 2 章〈Geedge 供應鏈深入解析（三代 TSG 硬體）〉：「外洩文件顯示這套配置只部署在哈薩克」、「2019 至 2020 年初之間出貨給 Geedge 的 CSA-7400 共有 1,708 台」。第 3 章〈EtherFabric 與 ADLINK 的角色和回應〉：「EtherFabric 部署在緬甸」、「登記在 ADLINK Technology, Inc. 名下」、「至少包含一個凌華科技的元件，最有可能是運行管理軟體的運算主板」、「凌華科技證實，凌華科技（中國）有限公司北京分公司向 Geedge Networks 供應了標準的 CSA-7400 網路安全平台」。
[^madlink-gen]: MADLink 社群譯文第 2 章：「Geedge 為其 TSG 防火牆設備陸續供應了三代伺服器硬體」、「第一代 TSG 平台 TSG-ADC 建立在 CSA-7400 之上」、「第二代平台 TSG-9140 採用 AdvancedTCA（ATCA）規格」、「它應該是基於中國公司北京恒光信息技術的 VELA ATCA 平台」、「外洩文件顯示 TSG-9140 只部署在衣索比亞（代號 E21）客戶站點」、「現行版本 TSG-X 的主要 TSG 運算節點採用 Nettrix 伺服器，儲存 Cyber Narrator 所使用監控資料的儲存伺服器則來自浪潮（Inspur）」。第 1 章：「Geedge 目前這一代的 TSG 硬體部署在衣索比亞、巴基斯坦和緬甸」。第 3 章：「EtherFabric 看起來重用了與 TSG-9140 相同的、來自北京恒光信息技術的 VELA ATCA 硬體，但角色不同」、「部分網路元件可能由凌華科技提供」、「也作為概念驗證部署給一個只以代號 A24 識別的未知客戶」。
[^thirdparty]: USENIX 論文 §1：「including two of the three core application detection systems」。§4.2.1：「a free software project from the Libtrace team at the University of Waikato」、「All code required for this function contains the libprotoident copyright」、「appears to be a modified copy of openvpn.c from a 2022 version of nDPI」、「the logic remains nearly identical」。§4.2.2：「QDPI is built off of Qosmos ixEngine, a proprietary, enterprise DPI library」、「This is most clearly indicated by the Stellar session callback subscriber function eventually calling」，後面接的是 ixEngine 的函式名稱。
[^modular]: USENIX 論文 §3.2 與 §3.5 的 Takeaway：「fingerprinting one plugin does not necessarily imply the presence or version of another in the same deployment」、「The firewall aggregates attributes from multiple parallel processing paths」。
[^ndpi-license]: nDPI 與 libprotoident 在 GitHub 的儲存庫，2026 年 10 月 30 日讀取，兩者的 COPYING 都是 GNU Lesser General Public License v3.0（LGPL-3.0）。USENIX 論文 §4.2.1 對 nDPI 的寫法是「a GPL-licensed DPI library」。
[^disclose]: USENIX 論文 §4.2：「we find instances of third-party libraries intentionally copied and adapted into the Geedge Networks code base」。Ethical Considerations：「We disclosed the usage of code by Geedge Networks to both the Libprotoident team and Enea, the parent company of Qosmos. Both have responded to our initial disclosures, and we have scheduled meetings to engage in further discussion」。§4.2 的 Takeaway：「suggests that comprehensive protocol classification is costly to build from scratch, even for a well-resourced, state-linked vendor」。
[^beyond]: 本文的觀點。依據是 USENIX 論文 §1：「For the first time, we can move beyond remote inference」。
[^gfw-multi]: USENIX 論文 §2.1：「there has been increasing evidence pointing to the deployment of multiple, independently operating deep packet inspection (DPI) devices with distinct enforcement roles」。
[^modes]: 網路政變社群譯文第 6 章〈Geedge 的營運與客戶〉：「在鏡像模式下，客戶無法擋下特定流量，只能靠注入封包（送出偽造的封包）來阻斷連線」、「內聯模式在文件中也稱為『主動』（active）模式，流量必須先通過 Geedge 設備，才能繼續前往目的地」、「內聯模式的優點是可以完全擋下特定的流量，讓它根本無法通過網路」。USENIX 論文 §5.2：「It also supports both in- and on-path deployment」。§3.1：「Both require TSG to be deployed in-path to stop packets」。§6.4：「their generic censorship mechanism of packet drops makes bypass failures inconclusive」。
[^asym]: 本文的推論。依據是 USENIX 論文 §6.4：「Note, we can highlight comparisons with test vectors that are successfully blocked by TSG in cases of non-fingerprintable censorship decisions」、「if a test vector evades TSG, it could still get blocked by another middlebox, but if it is blocked by TSG, it is guaranteed to be blocked」。論文用這個邏輯挑選 TLS 的比較項目，本文延伸到其他協定，並推出放行的結果可以排除 TSG。
[^codes]: 網路政變社群譯文第 6 章〈Geedge 的營運與客戶〉：「目前辨識出的客戶代號有哈薩克（`K18` 與 `K24`）、巴基斯坦（`P19`）、衣索比亞（`E21`）、緬甸（`M22`）與新疆（`J24`）」、「資料裡還提到一個身分不明的客戶，代號 `A24`」、「代號的最後兩位數字可能代表 Geedge Networks 在當地開始專案的年份，但並非每個代號都符合」。
[^matrix]: 本文依 USENIX 論文 Table 5 到 Table 9 與 §6.1 到 §6.5 的正文整理，分類是本文的判斷。吻合：§6.1 的 Injector 2，§6.3 的 GFW II 與 GFW III（固定的種子值等於 TSG 的預設值）。舊版：§6.4「GFW II shows behavior equivalent to an older version of TSG's SSL module」，§6.5「the parsing fingerprint exhibited in Kazakhstan fully matches an older version of TSG's QUIC parsing code」。部分：§6.2 的 GFW II（「The observed boundary of […] fragments for GFW II is very close to TSG's」，本文歸為部分相符，因為上限只是接近），§6.5「both Kazakhstan and the GFW block the same test vectors as TSG's QUIC plugin, though we cannot match them fully due to a difference in supported QUIC versions」。無法判斷：§6.2 重組行為與 TSG 預設不同的設備（論文註明這是 TSG 可以調整的設定），§6.4「both Kazakhstan and Pakistan (DROP) support potential TSG deployments」，§6.3「TSG can be configured to match the behavior in Myanmar」。不吻合：§6.1 Table 5 的其他注入器與伊朗，§6.2 重組到測試上限仍成功的設備，§6.3「the other injectors exhibit markedly different behaviors and header values」，§6.4「no middlebox exhibited exactly the same behavior as the latest leaked TSG」之下，除了 GFW II 與兩台以丟包封鎖的設備以外的設備，§6.5「the parsing fingerprint mismatch means we cannot confirm its use」（緬甸）。巴基斯坦列在 Table 9，正文沒有討論它的 QUIC 結果。哈薩克的設備不送 RST，論文沒有做 TCP 的比對。河南與巴基斯坦送出 RST 的設備，TLS 在 Table 12 的差異都是 TSG 放行、設備擋下，這兩套設備以 RST 封鎖，可以從 RST 辨認封鎖的來源，所以本文歸為不吻合，論文正文沒有對這兩格下結論。
[^dns-inj2]: USENIX 論文 §6.1：「Our results in Table 5 strongly suggest that TSG provides the GFW Injector 2's DNS injection implementation」、「only China's Injector 2 exhibits the combination of the flag value」。旗標的數值本文省略。
[^seed]: USENIX 論文 §6.3：「corresponding to TSG's default seed_key, strongly indicating usage of TSG code」、「of exhibiting a constant seed key by random chance is approximately」，這句寫的機率估計值是 10 的負 44 次方。種子值本身本文省略。
[^rst-dev]: USENIX 論文 §6.3：「both GFW II and GFW III exhibit deviations from TSG」、「Both fix TTL values at […], but TSG generates TTL values dependent on an internal state variable」、「GFW II did exhibit TTL values consistent with TSG, suggesting that it slightly changed its implementation since then」、「GFW II is known to send […] identical RST+ACK packets [47], while our build of TSG, when configured to also send […] RST+ACK packets per injection, decreases the IPID」。[…] 是本文省略的數值。
[^frag]: USENIX 論文 §6.2：「The observed boundary of […] fragments for GFW II is very close to TSG's, suggesting the two potentially share similar code」。[…] 是本文省略的分片上限。
[^tls-quic]: USENIX 論文 §6.4：「While no middlebox exhibited exactly the same behavior as the latest leaked TSG, GFW II shows behavior equivalent to an older version of TSG's SSL module, which suggests usage of this older version in GFW II's SSL parsing」。§6.5：「both Kazakhstan and the GFW block the same test vectors as TSG's QUIC plugin, though we cannot match them fully due to a difference in supported QUIC versions」、「the parsing fingerprint exhibited in Kazakhstan fully matches an older version of TSG's QUIC parsing code」。
[^civil]: USENIX 論文 §2.2：「Civil society investigations have highlighted evidence of deployments of Geedge Networks' products across multiple countries, including Kazakhstan」、「Ethiopia」、「Pakistan」、「and Myanmar」，各國之後的站點代號本文省略。§4.1.2：「we conducted a case-insensitive search for "vpn"」、「We found major threads of site correspondence with Myanmar (440 tickets) and Ethiopia (53 tickets)」。
[^risky]: Risky Bulletin，2026-08-21：「as one of the Great Firewall's three known traffic filtering capabilities」。同一篇報導引用的研究者貼文：「Geedge is only one of the vendors involved in the GFW」、「the authors found only 1 out of the 3 of the characterized DNS injectors that comprise the GFW matched」。
[^no-three]: 本文的查證。在 USENIX 論文全文（含附錄與參考文獻）搜尋 three known 與 filtering capabilit，都是 0 筆。filtering 只出現 1 次，在一篇參考文獻的標題裡。三種可能出自過去研究的分類，這是本文的推論，依據是 §2.1：「DNS manipulation is managed by three independent on-path injectors」、§6.3：「We evaluated three TCP RST injectors」，以及 Risky Bulletin 所引研究者貼文的「1 out of the 3 of the characterized DNS injectors」。
[^geedge-home]: geedge.report 首頁：「China's Great Firewall is running parts of TSG」。同一條的說明：「The same code, or a close relative, appears to be part of China's national censorship system」。
[^ties]: USENIX 論文 Abstract：「a Chinese DPI company with ties to the Great Firewall of China」。§1：「affiliated with the Great Firewall of China」。§2.2：「maintains a close collaborative relationship with the Massive and Effective Stream Analysis (MESA) Lab」。
[^circ]: USENIX 論文 §1：「we identify client-driven, iterative efforts to block specific circumvention tools, including Psiphon, Tor, and many popular VPN providers」、「ranging from IP-based blocking to matching byte patterns」。§4.1.1：「including server IP addresses, domain names, JA3/JA4 hashes, SSL certificate fields (e.g., issuer name), payload length, and byte patterns」、「records a log of updates to a signature ZIP from March through November 2024」、「carry risk levels between three and five」、「the majority (21/29) are ranked five」、「which target predominantly Chinese applications and all have a risk score of one」。§4.1.2：「finding 700 tickets across 182 issues」、「ineffective blocking of Signal when the "censorship circumvention" option is enabled」、「customers can report failures, set priorities, and flag collateral damage」。
[^foci-vpn]: FOCI 論文 §4.2：「Multiple files specifically target VPN and circumvention tools, including comprehensive NordVPN server lists and Psiphon CDN domains」。
[^psiphon]: USENIX 論文 §4.1.2：「based on server IP addresses due to the lack of obvious signatures and integration of a "whitelist protection mechanism" to avoid misidentification」。Figure 3 的說明：「concerns of collateral damage from blocking Psiphon by IP addresses and SNI」。§7：「we also find evidence of obfuscation raising the cost of detection」、「TSG is capable of identifying circumvention tools at a relatively low cost」、「often very early in the connection」。
[^tor]: 本文的查證。在 USENIX 論文全文搜尋完整單字 Tor（區分大小寫），共 5 處：§1 引言的封鎖對象清單、§2.1 回顧過去對防火長城封鎖 Tor 的研究、Table 3 風險等級表的 Tor Browser，以及兩篇參考文獻的標題。第 6 節的量測沒有出現 Tor。
[^webtunnel]: 網路政變社群譯文第 7 章〈封鎖網路隱私與規避工具〉：「在資料外洩的時間點，Geedge Networks 似乎還沒有任何有效對付 WebTunnel 的手段」、「中國科學院 Mesalab 實驗室（Massive and Effective Stream Analysis）的學生做過初步研究，探討封鎖 WebTunnel 的可能方法」、「我們已與 Tor Project 協調，以負責任揭露」、「目前沒有找到任何證據，顯示 Geedge Networks 發現或正在利用 Tor 軟體或 Tor 設計上任何先前未知的漏洞」。
[^no-cve]: 本文的查證。在 USENIX 論文全文搜尋 CVE、vulnerab、exploit（不分大小寫），都是 0 筆。memory-unsafe 與 fuzzing 各 1 筆，都在 §7 結論。§7：「while they pose a significant obstacle to circumvention, they also undermine code maintainability and correctness」、「core components such as SAPP and its protocol plugins are written in memory-unsafe C」、「The Jira tickets corroborate this patchwork development process; we detail an example of an upgrade to the AppSketch database causing SAPP to restart」、「these reinforce the potential for future work in fuzzing or symbolic execution」。
[^foci-937]: FOCI 論文 Abstract：「298,955 censored GNL domains (93.7% of all censored GNL domains) are not included in either Tranco or the CitizenLab lists」。§5：「the GNL captures between 37.1% and 61.6% of censored Tranco domains」、「Tranco informs which globally popular sites are censored, CitizenLab monitors types of sensitive content over time, and the GNL reveals which domains commercial vendors consider of interest」。GNL 是 FOCI 對外洩資料的簡稱。
[^of-interest]: FOCI 論文 §4.1：「we do not assume domains are censored simply because they appear in the GNL」、「explicit blocklists are rare in the leak, as they constitute sensitive customer data」、「domains in the GNL represent content "of interest"」。§4.2：「The largest number of domains comes from MESA lab's specialized SNI datasets」、「appear to be gathered from network taps」，資料集的檔名本文省略。§5：「The GNL contains copies of popularity lists (Alexa, SecRank) that appear to be used for MESA lab research projects rather than deployed Geedge products」。
[^adlink]: MADLink 社群譯文第 3 章：「已完成出口管制名單篩查，確認 Geedge 不在任何受限名單上」、「該公司也表示將啟動內部稽核」、「凌華科技表示，公司僅提供通用硬體平台，未參與任何與該產品最終用途相關的軟體整合、系統設計或運營活動。然而，這項說法與外洩文件互相矛盾」、「Geedge 的 TSG-ADC 配置在負載平衡功能上仰賴凌華科技的 PacketManager 軟體」。凌華把 CSA-7400 描述為通用平台的部分，報告的回應是「但該說法與產品本身的行銷定位互相矛盾」。第 1 章：「台灣經濟部回應 InterSecLab 的詢問時，說明了這套框架，但以法律限制為由，未對個案表達看法」。第 4 章〈結論〉：「現行版本的伺服器是通用 x86 硬體，即便正規採購受阻，這些元件仍能從次級市場取得」。第 2 章：「Nettrix 是中科曙光（Sugon）的子公司，曙光是已遭美國政府制裁的中國超級電腦製造商」。
[^gap]: 本文的推論。依據是 MADLink 社群譯文第 3 章：「凌華科技確認出貨持續到 2020 年初」，以及 USENIX 論文 §6.3：「looking at previous measurements collected in December 2023」。論文以 2023 年 12 月的舊量測對照，自己的量測晚於那個時間，但沒有寫明日期。出貨在 2020 年初結束，量測晚於 2023 年 12 月，兩者至少相隔三年多。
[^jfm]: Justice For Myanmar 新聞稿，2024-06-19：「Justice For Myanmar calls on governments to urgently impose sanctions against Geedge Networks, CEIEC and Mascots Group, its directors and related companies」。
[^sanction]: 本文的查證，不是任何來源的說法。2026 年 10 月 30 日下載美國財政部 OFAC 的 SDN 名單與 Consolidated 名單、歐盟的金融制裁整合名單，搜尋 Geedge 與 Jizhi 都沒有符合的條目。作為對照，曙光（Dawning Information Industry）出現在 OFAC 的 Consolidated 名單。實體清單的新增都在聯邦公報公告，在美國聯邦公報搜尋 Geedge 是 0 筆，Jizhi 唯一的一筆是另一家公司 Changguang Jizhi Optical Technology 被列入實體清單。英國的制裁名單與美國商務部的整合篩查名單這次沒有下載成功，不在查證範圍內。
[^oss-stack]: MADLink 社群譯文第 2 章〈Geedge 供應鏈深入解析（三代 TSG 硬體）〉：「Geedge 的整套軟體堆疊建立在開源基礎上」、「其作業系統 TSG-OS 以 Rocky Linux 為基礎（更早期版本是 CentOS），網路封包處理則仰賴 Intel 開源的 DPDK 工具包」、「Geedge 曾考慮改用華為 EulerOS，但因授權費用過高而放棄」。
[^oss-coup]: 網路政變社群譯文第 5 章〈產品與服務〉：「TSG Galaxy 建立在開源的 Apache Kafka 串流處理平台上」、「使用開源的 DPDK，讓 Geedge 的網路堆疊不受限於特定的硬體廠商」、「Network Zodiac 似乎以 Grafana 為範本」。同一章的註腳：「Geedge 與 Mesalab 的學生用自行修改的開源工具 tcpdump 擷取這些指紋，修改版稱為 tcpdump_mesa」。
[^oss-export]: MADLink 社群譯文第 4 章〈結論〉：「Geedge 的軟體是開源的，現行版本的伺服器是通用 x86 硬體，即便正規採購受阻，這些元件仍能從次級市場取得」、「這讓它們成為出口管制可以實際著力的對象」。
[^oss-license]: 網路政變社群譯文第 2 章〈主要發現〉：「他們也用可能違反授權條款的方式納入開源程式碼」、「Geedge 似乎靠這些手法取得競爭優勢，更快推出能力與領先對手相當的整套產品，同時增強承受制裁的能力」。
[^oss-principle]: 開放原始碼促進會（OSI）〈The Open Source Definition〉第 6 條〈No Discrimination Against Fields of Endeavor〉：「The license must not restrict anyone from making use of the program in a specific field of endeavor」。自由軟體基金會〈What is Free Software?〉：「The freedom to run the program as you wish, for any purpose (freedom 0)」。兩頁都在 2026 年 10 月 30 日讀取。
[^oss-tools]: 網路政變社群譯文第 7 章〈封鎖網路隱私與規避工具〉：「Tor 網路是免費、開放原始碼的系統」、「是免費、開放原始碼的網路規避工具」，後一句寫的是 Psiphon。
[^oss-research]: USENIX 論文 §2.2：「has been inferred from measurements」、「or learned from open-source systems such as Snort」，同一句接著列出 Suricata、Zeek 與 nDPI。§6.4：「We created our test vectors by extending the open-source tool Censor-Scanner」。網路政變社群譯文第 4 章〈研究方法〉：「把文件索引進開源的文件探索平台 Datashare」、「我們用開源的文字擷取函式庫 Apache Tika」。
[^open-science]: USENIX 論文 Open Science：「In the context of the open science policy, we made all of our artifacts available in the following Zenodo link」、「We consider the risk of censors benefiting from such a publication greater than the potential benefit to the community」、「we do not provide the artifact openly」。
[^local]: USENIX 論文 Ethical Considerations：「the git repositories contain commits and directories that list emails and names of individual developers」、「we emphasize that our focus is on the systems and architecture, and not on individual persons」、「do not include source material in our repository」、「our efforts to run a local operational copy of TSG could harm users experiencing censorship by enabling deploying countries to refine their systems」、「we choose not to publicly document or provide additional details on how to set up this firewall」、「We also considered whether it would be better to not deploy the firewall ourselves at all」、「develop and test circumvention strategies against a working instance」。
[^share]: USENIX 論文 Ethical Considerations：「We performed all of our scans between two vantage points that we own」、「we made sure that no entity is present on the current EU sanctions list」。Open Science：「We decided against the publication of the leaked source code and our deployment of the Firewall due to ethical concerns」。§1：「We will make our build available to trusted network security researchers upon request」。geedge.report 資源頁：「All of our result files, anonymized PCAPs, and the scripts and tools used to conduct our scans are archived on Zenodo」。段落最後一句是本文的推論。
[^foci-ethics]: FOCI 論文 Ethical Considerations：「we believe the broad public interest of this information overrides potential intellectual property concerns」。GFW Report〈Geedge & MESA Leak〉：「analyzing these files only in an isolated (virtual) machine without internet access」。
[^lantern-site]: geedge.lantern.io 首頁，2026 年 10 月 30 日讀取：「Lantern research · sibling to」，後面接的是 corpus.lantern.io 的連結，頁尾另有「Sibling project」。目的寫在首頁：「extracted for one purpose: telling a circumvention-tool builder exactly what they're up against」。about 頁：「Raw leak content is never rehosted」。
[^lantern]: geedge.lantern.io 的 about 頁：「Finding extraction runs as Sonnet-tier agents reading batches of extracted text」、「`high` requires an unambiguous, explicit source」。首頁頁尾，2026 年 10 月 30 日讀取：「880 findings indexed from the September 2025 Geedge/MESA leak」。抽讀是本文的查證，同一天從首頁的 Recent findings 列表挑出五則，五則都標成 high。前三則發現從資料表的欄位推論系統逐連線記錄，原句分別是「This confirms, at the OLAP schema level」、「not just connection metadata」、「tags every session」。後兩則分別依據程式碼與 changelog。測試用的判斷依據是出處的路徑顯示是測試環境的設定集合，五則裡有四則如此。五則的出處欄都只有封存與路徑，沒有 commit hash。
[^n4p]: 本文的查證，2026 年 10 月 30 日讀取 net4people/bbs 的 #519 討論串，範圍是 2025 年 10 月以後的留言。有出處指留言附上論文或正式報告的連結。
[^a24]: 網路政變社群譯文第 6 章〈Geedge 的營運與客戶〉：「`A24` 的相關資料沒有任何可以辨識客戶的線索」、「關於 `A24` 客戶的身分，唯一的線索是首字母 A 與年份 2024」、「外洩發生時 `A24` 與 Geedge 的關係似乎還在初期階段」。MADLink 社群譯文第 3 章：「也作為概念驗證部署給一個只以代號 A24 識別的未知客戶」。「沒有看到公開的指認」是本文的查證，讀取日期 2026-10-30：USENIX 論文與 FOCI 論文全文搜尋 A24 都是 0 筆。GFW Report 分析文章的中文版寫到「除一个代号（A24）外，其余均已对应到具体国家」，其餘段落轉述 InterSecLab 的說法。net4people 討論串的 98 則留言裡有 2 則提到 `A24`（2025-09-10、2025-09-11），也都是引用 InterSecLab 的報告。
[^future]: USENIX 論文 §5.1：「which we use to load SAPP's DNS, SSL, and QUIC plugins」。§4.2.2：「While all available archives」、「of the database in the leak are encrypted」，同一句在 PDF 裡跨頁排版。§4.1.1：「Although we found no code explicitly converting ASW or TSG2402 formats into Maat signature definitions」。§7：「We hope this work will serve as a guide for future research on the leak」。FOCI 論文 Future Work：「areas for future work include searching for IP addresses in the GNL, deeper analysis of documents such as PDFs, and improved OCR」、「the Tranco and Citizen Lab lists are limited compared to larger censorship measurement lists such as Common Crawl or ICANN CZDS」。
