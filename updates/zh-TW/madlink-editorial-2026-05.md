---
title: 台灣對 MADLink 報告的反應，2026 年 5 月的觀察紀錄
description: MADLink 報告點名台灣上市公司凌華科技之後，台灣媒體、立法院與主管機關的反應，以 2026-05-20 的快照記錄，附上查證過程與可追蹤的公開入口。
date: 2026-05-20
---

InterSecLab 的 MADLink 報告點名了一家台灣上市公司，指出它出貨的網路設備成了中國公司 Geedge Networks 在哈薩克部署審查系統的硬體基底。報告追問台灣的出口管制能否阻止本地公司供應監控與審查設備給威權政府，這個問題需要本地的報導、質詢與主管機關回應接手。報告發布後將近一個月，台灣中文公共領域的反應明顯偏少。

我們把查證過程與當時的觀察記錄下來，讓之後查找這份報告的人可以看到它在台灣的接收脈絡，也讓想持續追蹤的人有一個起點。

!!! note "2026-05-20 的觀察快照"

    本文是 anoni.net 編輯團隊在 2026-05-20 的觀察整理（2026-05-16 初版，05-20 補上外部交叉驗證），不屬於 InterSecLab 原報告的內容。發布之後沒有持續更新，文中提到的狀態都以快照日為準。報告翻譯本體在文件站的 [MADLink 報告中譯](docs:reports/interseclab-madlink/)。


## 外部交叉驗證

報告點名一家上市公司，並引述一連串技術細節。記錄台灣的反應之前，我們先對報告的關鍵事證做了一輪獨立查證，讀者也可以照著重現。

### EtherFabric 的 MAC 位址前綴

IEEE OUI `00:30:64` 登記在 ADLINK Technology, Inc. 名下，這個硬體指紋是報告把 EtherFabric 與凌華連在一起的依據，也是整份報告最容易自行驗證的線索。透過 macvendors.com（[`api.macvendors.com/00:30:64`](https://api.macvendors.com/00:30:64)）與 macvendorlookup.com（[`api.macvendorlookup.com/api/v2/003064`](https://www.macvendorlookup.com/api/v2/003064)）查詢，兩個獨立來源都回傳「ADLINK TECHNOLOGY, INC.」，登記地址是凌華在新北市中和區的舊址。查詢結果從硬體層級證實了 EtherFabric 管理介面的 MAC 位址來自凌華設備。

### CSA-7400 的產品定位

凌華主張 CSA-7400 是通用平台，報告反駁的依據是這款產品本身的市場定位。在凌華中英文官網的[產品頁](https://www.adlinktech.com/Products/Network_Security_Appliance/4UNetworkAppliance/CSA-7400?lang=en)上，CSA-7400 歸在「Network Security Appliance」底下，行銷為 DPI、IDS/IPS、DDoS、NGFW 用途的 carrier-grade 設備。manualzz 上的 [Quick Start Manual](https://manualzz.com/doc/55701658/adlink-technology-csa-7400-quick-start-manual) 也載明出貨時預載 CentOS 7，與報告描述 TSG-OS 早期以 CentOS 為基礎的細節一致。

### Geedge 的創立背景

積至（海南）信息技術有限公司在 2018 年於海南創立。維基百科的[积至信息](https://zh.wikipedia.org/wiki/%E7%A7%AF%E8%87%B3%E4%BF%A1%E6%81%AF)條目、[大紀元 2025-09-13 的報導](https://www.epochtimes.com/b5/25/9/13/n14593857.htm)與[新唐人的報導](https://www.ntdtv.com/b5/2025/09/13/a104019706.html)，可以互相印證公司的基本資料、創辦人背景，以及與中國科學院信息工程研究所 MESA 實驗室的同源關係。

### New Bloom Magazine 的報導

我們引用的 New Bloom Magazine 報導確實存在，標題是「[Taiwanese Company Implicated in Great Firewall Supply Chain By Report](https://newbloommag.net/2026/04/29/tw-adlink-geedge/)」，發布時間為 2026-04-29 07:41 UTC。

## 媒體的報導

### 國際與英文媒體

- InterSecLab 的[原報告](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)（2026-04）接續 2025-09 的〈[The Internet Coup](https://interseclab.org/research/the-internet-coup/)〉，是這個系列調查的第一手研究。
- [New Bloom Magazine](https://newbloommag.net/2026/04/29/tw-adlink-geedge/)（破土，以台灣議題為主的英文媒體，2026-04-29）是快照日前唯一明確聚焦凌華與 Geedge 關聯的台灣相關獨立媒體報導。文中也提到 Geedge 是中國公司，台灣政府對涉及中國的案子通常會有反應，這次卻意外安靜。
- cybernews、osnews、Daily Security Review 等國際科技與資安媒體，多數延續 2025-09 Geedge 500GB 外洩事件的報導框架，沒有特別著墨凌華這個台灣供應鏈節點。

### 台灣中文媒體

用「凌華 Geedge」、「MADLink 凌華」、「凌華 哈薩克」等關鍵字跨媒體搜尋，聯合、自由、中央社、TVBS、TechNews、iThome 等台灣主流媒體，截至 2026-05-20 都沒有直接報導 MADLink，或凌華、Geedge、哈薩克這條線。[TechNews 科技新報](https://infosecu.technews.tw/2025/09/14/china-geedge-mesa-leak-analyzing-the-great-firewall-largest-document-leak/)在 2025-09 寫過防火長城 500GB 外洩事件本身，沒有後續追蹤凌華的供應鏈。同一段時間，凌華的中文新聞集中在邊緣 AI 接單、Taiwan Excellence 獎項與 CYBERSEC 2026 參展等業務話題。

## 主管機關、立法院與凌華的回應

經濟部國際貿易署回覆 InterSecLab 時，說明台灣的戰略性高科技貨品出口管制以防止大規模毀滅性武器擴散為目的。管制貨品清單參照四大國際出口管制機制，實體清單參照聯合國安理會與夥伴國家的制裁清單。對於個案，國貿署以法律限制為由，不揭露涉及個別公司的資訊（全文見報告翻譯的[附錄](docs:reports/interseclab-madlink/index_5/)）。

原報告引述了一位立委的主張，認為台灣應建立自己的實體清單，不只依賴美國與歐盟的清單，並訂出更清楚的標準，釐清元件製造商在什麼情況下需要對最終用途負責。在立法院議事系統、社群平台與媒體採訪紀錄裡，截至快照日都找不到這位立委就此議題進一步發言的紀錄。

凌華在 2025 年 11 月 14 日回覆 InterSecLab 的聲明裡寫了將啟動內部稽核，全文同樣收在報告翻譯的附錄。在[公開資訊觀測站](https://mopsov.twse.com.tw/)以代號 6166 查詢，截至 2026-05-20，沒有針對 Geedge、CSA-7400 出貨案或內部稽核的重大訊息公告。

## 台灣反應偏少的可能原因

以下是編輯團隊整理的可能因素，屬於觀察，不是定論，歡迎補充與反駁。

- **技術門檻**：一般財經與政治記者要把 CSA-7400、深度封包檢測、Geedge TSG 與出口管制串成一條線並不容易，缺少在地的技術簡報與翻譯，寫出符合台灣讀者語境的報導成本很高。
- **資安媒體的報導重心**：iThome、資安人這類媒體以企業資安採購與技術趨勢為主，「台灣零組件用於威權監控」的題目不在報導習慣裡。
- **新聞熱度**：MADLink 在 2026-04 才具體點名凌華，Geedge 外洩事件的新聞熱度在 2025 年底已經消退，台灣媒體沒有把這條線當成持續追蹤的題材。
- **公民團體的關注重心**：關注資訊與數位人權的台灣公民團體，近年主要投入中國對台資訊戰、假訊息治理與數位平台責任，較少把監控科技出口的人權審查當成主要議題。anoni.net 翻譯 MADLink 報告，也是想補上這個位置。

## 制度面的缺口

報告的結論是，台灣的出口管制框架以防擴散為主軸，沒有涵蓋把具監控能力的科技出口給供應威權政府的廠商。缺少報導、質詢與公民團體倡議的情況下，主管機關沒有修補框架的壓力，凌華也沒有對外揭露內部稽核進度的壓力。

## 可追蹤的公開入口

### 政府與制度

**經濟部國際貿易署**

- 入口：[戰略性高科技貨品出口實體管制清單](https://publicinfo.trade.gov.tw/icp/exportList.html)、[國貿署新聞稿](https://www.trade.gov.tw/Pages/List.aspx?nodeID=40)
- 觀察重點：是否把監控與審查設備的供應商納入實體清單、是否引入針對最終用途的審查機制、跨部會審查會議是否就此案公開結論

**立法院**

- 入口：[立法院 IVOD](https://ivod.ly.gov.tw/)、[立法院議事暨公報資訊網](https://lci.ly.gov.tw/)、[立法院議事整合資訊網](https://ppg.ly.gov.tw/ppg/)
- 觀察重點：原報告引述的立委或其他立委（特別是經濟、外交及國防、司法及法制委員會）是否就此議題提出書面質詢、口頭質詢、提案或新聞稿，委員會是否邀請主管機關列席報告

**金管會與證交所（凌華為上市公司）**

- 入口：[公開資訊觀測站](https://mopsov.twse.com.tw/)代號 6166（重大訊息、年報、ESG 報告）
- 觀察重點：凌華是否公告與 Geedge 出貨案相關的重大訊息、是否在 2026 年年報或永續報告書揭露此案與內部稽核結果、法說會上是否被分析師問到

**監察院**

- 入口：[監察院](https://www.cy.gov.tw/)的糾正案公告
- 觀察重點：是否就主管機關在出口合規審查中未辨識最終用途一事，提出糾正或糾舉

### 媒體與公民團體

- 中文媒體：過去報導過防火長城、中國資安或出口管制議題的科技媒體與調查報導媒體，是否有後續追蹤
- 公民團體：關注數位人權、開放政府與經貿政策的公民團體，是否就此議題發起連署、座談或政策倡議

### 追蹤方式與成本

| 方式 | 一次性成本 | 持續成本 | 做法 |
|---|---|---|---|
| Google Alerts | 10 分鐘 | 0 | 設定「凌華 Geedge」、「ADLINK Geedge」、「戰略性高科技貨品 監控」等關鍵字，命中時收到 email 通知 |
| 手動巡查 | 0 | 每月約 30 分鐘 | 社群輪值，依上面的入口逐一檢查，結果回報到 Matrix 頻道 |
| RSS 或 HTML diff bot | 1–2 小時設定 | 0 | 把國貿署新聞稿、公開資訊觀測站 6166 的公告轉進社群的 Matrix 頻道 |
| 自動化爬蟲 | 4–6 小時設定 | 0 | 定期抓取實體清單與重大訊息頁面，內容有變動時自動開 GitHub Issue |

四種方式可以混用，成本最低的組合是 Google Alerts 加上手動巡查。出現具體訊號之後（例如國貿署更新框架、立委公開質詢、凌華發布重大訊息），再考慮加上自動化監測。

## 補充資料

本文以 2026-05-20 的快照發布，之後不再更新。如果你發現本文沒有收錄的報導、政府文件或公開發言，歡迎到 [Matrix 討論頻道](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net)分享。

## 相關閱讀

- [MADLink 報告中譯](docs:reports/interseclab-madlink/)
- [InterSecLab MADLink 報告的正體中文翻譯](/updates/2026/05/report-madlink/)
- [The Internet Coup 報告中譯](docs:reports/interseclab-network-coup/)

*[ADLINK]: 凌華科技股份有限公司（ADLINK Technology, Inc.），台灣上市公司，股票代號 6166。
*[Geedge Networks]: 積至公司，中國的網路公司，研發、部署並對外出口網際網路審查與監控技術。
*[Geedge]: 積至公司。
*[CSA-7400]: 凌華科技的高密度 4U 網路平台設備，廠商行銷定位用於防火牆與深度封包檢測。
*[TSG]: 天狗安全閘道（Tiangou Secure Gateway），Geedge Networks 的旗艦審查與監控產品。
