---
title: MADLink：台灣在 Geedge 供應鏈中的遺留
description: InterSecLab 報告 MADLink 的正體中文譯文。台灣的凌華科技在 2019 至 2020 年出貨 1,708 台 CSA-7400 網路設備給 Geedge Networks，最終部署在哈薩克的國家級網路審查系統。
lead: InterSecLab 報告 MADLink 的正體中文全文譯本，共五章。
date: 2026-05-16
source: InterSecLab
chapters: [chapter-1, chapter-2, chapter-3, chapter-4, chapter-5]
---

<figure markdown="span">
  ![MADLink 報告封面](https://assets.anoni.net/www/library/interseclab-madlink/madlink-cover.jpg){ .shot }
  <figcaption markdown="span">圖片來源：[MADLink: A Taiwanese Vestige in the Geedge Supply Chain | InterSecLab](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)</figcaption>
</figure>

MADLink 是 InterSecLab 在 2025 年 9 月發布〈[The Internet Coup](/library/interseclab-network-coup/)〉之後，供應鏈延伸調查系列的第一篇。InterSecLab 的調查發現，台灣上市公司凌華科技（ADLINK Technologies，股票代號 `6166`）在 2019 至 2020 年間，向中國的 Geedge Networks（積至公司）出貨 1,708 台 CSA-7400 高密度網路平台設備。這批硬體最後部署在哈薩克，執行 Geedge 的旗艦產品天狗安全閘道（Tiangou Secure Gateway，TSG），功能與中國防火長城相近。緬甸部署的 EtherFabric 網路封包經紀設備裡也有 ADLINK 的元件，ADLINK 與 Geedge 產品線的關聯不只 CSA-7400 這一筆交易。

報告收錄凌華科技的回應、經濟部國際貿易署的書面說明，以及立法委員沈伯洋對台灣出口管制框架的批評，焦點在台灣現行制度能否防止監控與審查技術流向威權政府。社群把報告譯成正體中文（臺灣用語），讓台灣、香港、澳門與其他華語環境的讀者都能讀到全文。

本篇收錄在[報告與指引中譯](/library/)，翻譯自 InterSecLab 的〈[MADLink: A Taiwanese Vestige in the Geedge Supply Chain](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)〉。原報告是一篇沒有章節編號的網頁文章，為了方便閱讀與在 Matrix 上分章討論，譯文依主題分成五章：

* [第 1/5 章：摘要與主要發現](/library/interseclab-madlink/chapter-1/)
* [第 2/5 章：Geedge 供應鏈深入解析（三代 TSG 硬體）](/library/interseclab-madlink/chapter-2/)
* [第 3/5 章：EtherFabric 與 ADLINK 的角色和回應](/library/interseclab-madlink/chapter-3/)
* [第 4/5 章：結論](/library/interseclab-madlink/chapter-4/)
* [第 5/5 章：附錄（凌華科技與經濟部完整聲明）](/library/interseclab-madlink/chapter-5/)

!!! tip "編輯觀察"

    MADLink 報告點名了一家台灣上市公司，到 2026 年 5 月為止，台灣的中文公共領域卻少有討論。社群把當時的觀察整理成社群動態〈[台灣對 MADLink 報告的反應，2026 年 5 月的觀察紀錄](/updates/2026/05/madlink-editorial-2026-05/)〉，記錄國內外媒體報導的對比、討論冷淡的可能原因，以及可以持續追蹤的指標。

## 編輯立場聲明

本譯文忠實翻譯 InterSecLab 的報告原文，引述包含立法委員、政府機關、廠商等多方說法。所載資訊與主張都是原報告的觀點，不代表匿名網路社群 anoni.net 的立場。對於 ADLINK 的指控段落，附錄章節收錄 ADLINK 回應的全文，請讀者自行比對雙方說法。

## 參與討論

MADLink 與 InterSecLab 的 The Internet Coup 屬於同一系列調查，社群討論沿用同一個 Matrix 頻道，加入需要 <i data-icon="simple-matrix"></i> [Element/Matrix](https://element.io/) 帳號。點下方的連結會開啟社群自架的 Element，請用 `im.anoni.net` 的帳號登入。已有 `matrix.org` 或其他伺服器帳號的話，改[從 matrix.to 加入](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net)。

* <i data-icon="chat-processing-outline"></i> [#interseclab-the-internet-coup:im.anoni.net](https://matrix.anoni.net/#/room/%23interseclab-the-internet-coup:im.anoni.net)

## 更新紀錄

* **2026/05/16：**正體中文（臺灣用語）翻譯初稿釋出，同時新增編輯觀察，整理報告發布後本地媒體、政府、立委的反應。
* **2026/05/20：**編輯觀察新增「外部交叉驗證」與「後續可追蹤指標」兩段。
* **2026/10/13：**編輯觀察從報告翻譯拆出，改成社群首頁的[社群動態](/updates/2026/05/madlink-editorial-2026-05/)，以 2026-05-20 的快照保存，報告的章節只留原報告的譯文。
* **2026/11/23：**譯文從文件站搬到社群首頁的報告與指引中譯，舊網址轉到新網址。報告封面與 EtherFabric 的照片改放在 anoni.net 的圖片主機，開啟頁面時不會對其他網站發出請求。

發現譯文需要修正的地方，歡迎到 [GitHub 的 anoni-net/www](https://github.com/anoni-net/www/issues) 開 issue，或在上方的 Matrix 頻道提出。

## 關於 InterSecLab

[InterSecLab](https://interseclab.org/about/) 是專注於數位安全的實驗室，具備數位鑑識與威脅情報能力。團隊用技術分析與研究協助各機構辨識數位威脅，也監看、分析更大範圍的趨勢，以及控制與滲透的手法。團隊的專長包括網路鑑識、惡意軟體分析、資安事件應變、公開來源情報（OSINT）、系統安全與資料科學。

InterSecLab 的使命與團隊組成，見〈網路政變〉導讀頁的[關於 InterSecLab](/library/interseclab-network-coup/#關於-InterSecLab)。

!!! tip "原始程式碼探究"

    InterSecLab 沒有全面審查外洩資料裡的原始程式碼。對程式碼研究有興趣的人，可以直接聯絡 [InterSecLab](https://interseclab.org/about/)，參與後續的合作。

## 相關閱讀

* [網路政變](/library/interseclab-network-coup/)：本系列的第一份報告，分析 Geedge Networks 如何把中國防火長城輸出到威權政府
* [Geedge 外洩一年後的研究回顧](/articles/geedge-leak-one-year/)：兩篇論文與民間調查一年來確認了什麼、還不確定什麼
