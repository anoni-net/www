---
title: 網路政變
description: InterSecLab 報告 The Internet Coup 的正體中文譯文，分析 Geedge Networks 如何把中國防火長城的技術做成產品，輸出到其他國家。
lead: InterSecLab 報告 The Internet Coup 的正體中文全文譯本，共八章。
date: 2025-10-01
source: InterSecLab
chapters: [chapter-1, chapter-2, chapter-3, chapter-4, chapter-5, chapter-6, chapter-7, chapter-8]
---

![The Internet Coup 報告封面](https://assets.anoni.net/the-internet-coup/The-Internet-Coup-InterSecLab-2048x986.png){ .shot }

InterSecLab 分析外洩的約 500GB 檔案，說明 Geedge Networks（積至公司）如何把中國防火長城的技術做成整套產品，賣給哈薩克、衣索比亞、巴基斯坦、緬甸等國的政府，也在新疆等中國省分部署。審查設備成了可以採購的商品，各國政府取得大規模監控與封鎖規避工具的能力，不必再從頭開發。社群把報告譯成正體中文（臺灣用語），讓台灣、香港、澳門與其他華語環境的讀者，都能讀到完整的技術細節與各國案例，一起討論網路自由與網路治理。

本篇收錄在[報告與指引中譯](/library/)，翻譯自「[The Internet Coup: A Technical Analysis on How a Chinese Company is Exporting The Great Firewall to Autocratic Regimes | InterSecLab](https://interseclab.org/research/the-internet-coup/)」所附的「[The Internet Coup: A Technical Analysis on How a Chinese Company is Exporting The Great Firewall to Autocratic Regimes](https://interseclab.org/wp-content/uploads/2025/09/The-Internet-Coup_September2025.pdf)」報告，以正體中文、臺灣用語翻譯。

原報告共八章，另附致謝與附錄。譯文依照原報告的目錄（INDEX）分章，方便對照原文：

* [INDEX 1/8：摘要](/library/interseclab-network-coup/chapter-1/)
* [INDEX 2/8：主要發現](/library/interseclab-network-coup/chapter-2/)
* [INDEX 3/8：引言](/library/interseclab-network-coup/chapter-3/)
* [INDEX 4/8：研究方法](/library/interseclab-network-coup/chapter-4/)
* [INDEX 5/8：產品與服務](/library/interseclab-network-coup/chapter-5/)
* [INDEX 6/8：Geedge 的營運與客戶](/library/interseclab-network-coup/chapter-6/)
* [INDEX 7/8：封鎖網路隱私與規避工具](/library/interseclab-network-coup/chapter-7/)
* [INDEX 8/8：結論、反思與下一步](/library/interseclab-network-coup/chapter-8/)

## 編輯立場聲明

本譯文忠實翻譯 InterSecLab 的報告原文，所載資訊與主張都是原報告的觀點，不代表匿名網路社群 anoni.net 的立場。原報告附錄收錄的公司回覆信也一併翻譯，請讀者自行比對各方說法。

## 參與討論

社群為這份報告開了一個 Matrix 討論頻道，加入需要 <i data-icon="simple-matrix"></i> [Element/Matrix](https://element.io/) 帳號。點下方的連結會開啟社群自架的 Element，請用 `im.anoni.net` 的帳號登入。已有 `matrix.org` 或其他伺服器帳號的話，改[從 matrix.to 加入](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net)。

* <i data-icon="chat-processing-outline"></i> [#interseclab-the-internet-coup:im.anoni.net](https://matrix.anoni.net/#/room/%23interseclab-the-internet-coup:im.anoni.net)

## 更新紀錄

* **2025/10/01：**正體中文（臺灣用語）翻譯釋出，目前註腳內容尚未完全翻譯完成，持續補完中。
* **2026/10/13：**註腳全部翻譯完成。補上原報告第 17 到 75 則註腳，並依原報告修正第 5、9、13 則的誤植，第 51、55 則修正原報告網址裡的錯字（pakisan）。
* **2026/10/14：**對照原報告 PDF 核對註腳：第 34、36 則的三個 Internet Society Pulse 網址失效，換成同一筆紀錄的新網址。第 1、35、73 則照錄原報告，加上譯註說明網址現況與原報告的編排錯誤。逐則對照原報告的文字層：第 74、75 則的編號原本錯標成 75、76，已改正。第 16 則改回原報告的封存網址，第 43 則依網站修正日期。
* **2026/10/30：**八章全文從原報告重新翻譯，舊譯文的中國用語與翻譯腔較多。補上漏譯的段落（主要發現的「對資料主權的重大影響」一節、第 7 章「對 Tor 的封鎖」一節最後一段，與 Tor Project 協調揭露研究發現），以及哈薩克、衣索比亞、巴基斯坦、緬甸四節開頭以圖呈現的時間軸。附錄的公司回覆信逐句對照原信修正，第 8 章新增原報告封底的出版資訊。小標題改名之後，舊網址的錨點仍然有效。
* **2026/11/23：**譯文從文件站搬到社群首頁的報告與指引中譯，舊網址轉到新網址，錨點也維持不變。

發現譯文需要修正的地方，歡迎到 [GitHub 的 anoni-net/www](https://github.com/anoni-net/www/issues) 開 issue，或在上方的 Matrix 頻道提出。

## 關於 InterSecLab

[InterSecLab](https://interseclab.org/about/) 是專注於數位安全的實驗室，具備進階的數位鑑識與威脅情報能力。團隊用技術分析與研究協助各機構辨識數位威脅，也監看、分析更大範圍的趨勢，以及不斷演變的控制與滲透手法。團隊的專長包括網路鑑識、惡意軟體分析、資安事件應變、公開來源情報（OSINT）、系統安全與資料科學。

InterSecLab 為合作機構提供安全的研究基礎設施，開發處理與分析大型複雜資料集的方法，也和研究人員、記者與各機構一起辨識、調查與因應數位威脅。InterSecLab 的介紹頁把這些工作的目的寫成三件事：讓各方更了解全球的威脅情勢、促進數位自主，以及建立更有韌性、更安全的網路環境。

### 使命

InterSecLab 在介紹頁列出四項使命：

1. 與各方共同累積知識，讓外界更容易取得監控產業與網路安全領域的資訊，這兩個領域向來不透明。
2. 與機構及社群合作研究，擴大研究各種威脅與弱點的能力。
3. 培養全球視角，挑戰既有的權力地理觀，以多元、在地、理解脈絡的觀點面對挑戰。
4. 重視透明，與利害關係人分享研究發現，並倡議用公開的溝通解決數位安全問題。

### 團隊組成 { #專家團隊包括 }

* 資訊技術專家：調查數位威脅、因應進階網路攻擊，並追溯威脅來源以預測趨勢。他們也分析可疑的應用程式、評估 App 權限、監看不明的程序，並驗證 APK（Android 安裝檔）的真偽。
* 研究人員：結合社會與脈絡分析，補強威脅情報。
* 溝通專家：讓受影響的人了解風險、與媒體聯繫，並與合作夥伴一起擴大研究發現的影響。

InterSecLab 結合技術專業、研究與對外合作，協助第一線的防禦者提升資安能力。

!!! tip "原始程式碼探究"

    InterSecLab 這次的研究沒有全面審查外洩資料裡的原始程式碼。對程式碼研究有興趣的人，可以直接聯絡 [InterSecLab](https://interseclab.org/about/)，參與後續的合作。
