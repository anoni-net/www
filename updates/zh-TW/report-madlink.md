---
title: InterSecLab MADLink 報告的正體中文翻譯
description: InterSecLab 的 MADLink 報告指出，凌華科技在 2019 至 2020 年出貨的 1,708 台 CSA-7400 成了 Geedge 第一代防火牆平台的硬體基底。社群的正體中文翻譯放在文件站，另附報告發布後台灣反應的觀察紀錄。
date: 2026-05-23
kind: new
---

![MADLink 報告封面](https://interseclab.org/wp-content/uploads/2026/04/MADLink-A-Taiwanese-Vestige-in-the-Geedge-Suply-Chain.jpg){ .shot }

一家台灣上市公司出貨的網路設備，最後在哈薩克成了國家級網路審查與監控系統的核心。InterSecLab 的 MADLink 報告追查了這條供應鏈，匿名網路社群 anoni.net 已完成正體中文翻譯，收在文件站的[研究報告中譯](docs:reports/)。

設備來自凌華科技（ADLINK Technologies，股票代號 6166），客戶是中國公司 Geedge Networks（積至公司），旗艦產品「天狗安全閘道（Tiangou Secure Gateway，TSG）」的能力可與中國防火長城相比。報告〈[MADLink: A Taiwanese Vestige in the Geedge Supply Chain](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)〉在 2026 年 4 月發布，是 InterSecLab 繼 2025 年 9 月的《[The Internet Coup](docs:reports/interseclab-network-coup/)》之後，對 Geedge 供應鏈的第一篇延伸調查。


## 報告的主要發現

凌華在 2019 至 2020 年間出貨給 Geedge 的 1,708 台 CSA-7400，構成 Geedge 第一代防火牆平台的硬體基底，部署在哈薩克，用於國家層級的網路審查與監控。CSA-7400 是高密度 4U 設備，凌華自家的行銷定位就是深度封包檢測（DPI）與防火牆。

凌華的硬體也出現在 Geedge 部署於緬甸的 EtherFabric 裡。EtherFabric 是客製化的網路封包經紀設備（network packet broker，NPB），用來在多個 TSG 節點之間分散流量。外洩文件中的一組 MAC 位址可以追溯到凌華，顯示凌華在 Geedge 產品線中的角色不只單筆 CSA-7400 交易。

Geedge 現行世代的 TSG 部署在衣索比亞、巴基斯坦和緬甸，伺服器來自中科曙光（Sugon，已遭美國制裁）旗下的 Nettrix，儲存設備來自浪潮（Inspur）。這些標準 x86 元件即使直接採購受限，仍可從次級市場取得。報告的結論是，為監控用途設計的專用硬體（CSA-7400、EtherFabric 裡的凌華元件）才是出口管制最能發揮效果的對象。

## 中譯的章節

完整中譯在文件站的 [MADLink 報告中譯](docs:reports/interseclab-madlink/)。原報告是單頁長文，翻譯團隊依主題切成 5 章，方便在 Matrix 上分章節討論：

- [第 1/5 章：摘要與主要發現](docs:reports/interseclab-madlink/index_1/)
- [第 2/5 章：Geedge 供應鏈深入解析（三代 TSG 硬體）](docs:reports/interseclab-madlink/index_2/)
- [第 3/5 章：EtherFabric 與 ADLINK 的角色和回應](docs:reports/interseclab-madlink/index_3/)
- [第 4/5 章：結論](docs:reports/interseclab-madlink/index_4/)
- [第 5/5 章：附錄（凌華科技與經濟部完整聲明）](docs:reports/interseclab-madlink/index_5/)

凌華與經濟部國際貿易署的回應全文都收在附錄，讀者可以自行比對雙方的說法。

## 台灣反應的觀察紀錄

MADLink 點名了一家台灣上市公司，照理會引來本地媒體追問、立委質詢與主管機關回應，截至 2026-05-20，台灣中文公共領域的反應卻明顯偏少。我們把查證過程、媒體的報導與主管機關的回應整理成另一篇[觀察紀錄](/updates/2026/05/madlink-editorial-2026-05/)，以當天的快照發布。

## 致謝與討論頻道

感謝 InterSecLab 持續推動這個系列調查，也感謝投入翻譯與觀察整理的社群成員。

《The Internet Coup》與《MADLink》兩份報告的討論都在同一個 [Matrix 討論頻道](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net)，發現相關的新報導、政府文件或公開發言，歡迎到頻道分享。

## 相關閱讀

- [MADLink 報告中譯](docs:reports/interseclab-madlink/)
- [台灣對 MADLink 報告的反應，2026 年 5 月的觀察紀錄](/updates/2026/05/madlink-editorial-2026-05/)
- [The Internet Coup 報告中譯](docs:reports/interseclab-network-coup/)
- [InterSecLab 網路政變報告的正體中文翻譯](/updates/2025/10/report-the-internet-coup/)
