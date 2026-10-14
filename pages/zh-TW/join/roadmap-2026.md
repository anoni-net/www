---
title: 2026 年度路線圖
description: 匿名網路社群 anoni.net 2026 年的三大主題、文件站的季度規劃、活動、對外協作、技術專案與參與方式。
---

匿名網路社群 anoni.net 2026 年延續 Tor、Tails、OONI 的在地推廣，另外推進三個新主題：個人隱私指引、Tor Relay 校園建立、匿名支付探索。每一季結束時檢視交付狀況，再調整下一季的安排。

2025 年的回顧與 2026 年規劃的背景見[延續 2025，走向 2026](/updates/2026/01/2025to2026/)。

## 三大主題

### 個人隱私指引

2025 年推廣 Tor、Tails、OONI 時，社群最常被問到「下一步該怎麼做才能更安全」，回答這個問題需要一套可以照著做、依情境分級的隱私指引。個人隱私指引依日常使用、敏感工作、高風險情境三種等級整理工具與步驟，寫成文件站的[概念層](docs:basics/)、[工具層](docs:tools/)、[場景層](docs:scenarios/)三層文件。

文章索引與目前進度見[個人隱私指引研究專題](/join/privacy-guide/)。

### Tor Relay 校園建立

主題源自 EFF 與 Tor Project 合作推動的 [Tor University Challenge](https://toruniversity.eff.org/zh-tw/)，目標是在大專院校架設穩定運作的中繼節點。國立臺灣師範大學資訊工程學系的資訊中心已經在運作一個 Tor 中繼節點，由社群夥伴向教授與教職員提案、協調後架設完成（經過見[在台師大架設 Tor Relay](/updates/2025/12/ntnu-nz/)）。

社群在 2025 年完成 Tor University Challenge 網站的正體中文翻譯，2026 年到校園推動架設。台師大的經驗在 2026 年 5 月整理成提案範本、架設 SOP、校方 FAQ 三份範本，其他學校可以依自己的狀況改寫後沿用。

範本、案例與參與方式見[Tor Relay 校園建立研究專題](/join/relay-on-campus/)，架設的技術步驟見[Tor Relay 架設指南](/join/setup-tor-relay/)。

### 匿名支付探索

現金是最成熟的匿名支付方式，用在跨境、線上與組織收受捐款時有明顯的限制。社群在合法的前提下研究鏈上工具的可行性，包含加密貨幣、穩定幣、零知識身分驗證與多重簽署的實作。中文資源裡還沒有完整、有系統的整理，社群從研究起步，逐步寫成實作指引。

文章索引與目前進度見[匿名支付研究專題](/join/payments-research/)。

## 文件站的季度規劃

文件站的指南分成概念、工具、場景、進階、報告五個子群組，2026 年依這個架構逐季補齊內容。各季的範圍與目前的狀態：

- **Q1（已完成）**：優先補齊[概念層](docs:basics/)，加上在地法規（[台灣個資法 2025 修法](docs:taiwan/pdpa-2025/)、[台灣 VASP 法 2026](docs:taiwan/vasp-2026/)）、[緊急求救](docs:help/)頁、社群治理與路線圖
- **Q2（初稿已上線）**：工具層的 Tor Browser 進階設定、匿名作業系統比較、通訊工具比較、密碼管理器、加密貨幣的隱私光譜，以及進階層的端對端加密，各篇持續校訂
- **Q3（初稿已上線）**：場景層的記者、社運行動者、家暴受害者、LGBTQ+、選舉觀察員等情境，進階層的後量子密碼與去中心化網站發布，以及揭弊者保護法的技術觀察
- **Q4（進行中）**：[治理章程](/about/governance/)草案與[貢獻者百科](docs:community/contributor-handbook/)已上線，年度回顧在年底整理

實際進度視撰稿志工的人力而定。

## 活動

### COSCUP 2026

社群延續 2025 年參與 COSCUP 的經驗，2026 年 8 月 8 日、9 日在國立臺灣科技大學再度開設社群議程軌，並與 [ETHTaipei](https://ethtaipei.org/) 合辦匿名支付主題場次，安排在 8 月 8 日下午的 `TR-511`。完整議程見[COSCUP 2026 匿名網路社群議程軌](/events/coscup-2026/)，議程開放投稿時的說明見[COSCUP 2026 公開徵稿](/events/coscup-2026-cfp/)。

### 工作坊與小聚

延續 2025 年 8 月在臺科大舉辦[匿名網路工作坊 2025/08](/events/workshop-2025/)的經驗，2026 年視議題進度與夥伴的需求安排定點工作坊與線上小聚。對象包含新聞媒體、獨立記者、公民團體、技術社群與一般關注者。

## 對外協作

### 研究與報告翻譯

社群在 2025 年下半年翻譯並分享了 InterSecLab 研究中國審查技術輸出的報告[網路政變 / The Internet Coup](docs:reports/interseclab-network-coup/)。2026 年持續挑選對在地有參考價值的國際報告，翻譯並加上註釋，收在文件站的[嚴選報告](docs:reports/)。

### 外部活動參與

社群成員常參加在地開源、公民團體與隱私相關的活動，例如黑客松、年會、議題小聚與講座。多半以個人或社群代表的身分交流、了解議題的脈絡，屬於非正式的往來。議程聯合徵稿、報告翻譯協作、活動共同籌辦這類正式合作，確定之後會在[活動參與](/events/)公告。

## 技術專案

社群也開發並維運幾個與 Tor、OONI、密碼安全相關的技術專案：

- **[Tor 中繼節點觀測](/projects/pulse/)（Pulse）**：收集 Tor 中繼節點的資料並提供 API，使用 FastAPI 與 PostgreSQL
- **[OONI 觀測涵蓋率](/projects/asn-coverage/)（ASN Coverage）**：批次分析 OONI 的公開資料，背景說明見[ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)
- **Asian Diceware**：與 EFF 相容的 7776 字密語詞表，混入有字典背書的亞洲外來語。社群之後想自建類似 Tor Project [AnonTicket](https://anonticket.torproject.org/) 的匿名服務平台，詞表也是產生帳號代碼的字源，介紹見[Asian Diceware，帶亞洲味的英文密語字典](docs:tools/asian-diceware/)

三個專案的程式碼與議題追蹤分別在 GitHub 的 [anoni-net/pulse](https://github.com/anoni-net/pulse)、[anoni-net/asn-coverage](https://github.com/anoni-net/asn-coverage)、[anoni-net/asian-diceware](https://github.com/anoni-net/asian-diceware)。兩個觀測工具與 Tor 上游 network-health 團隊工作的關聯，見[參與 Tor Project](/join/tor-project/)。

## 參與方式

參與不需要技術背景，可以依興趣選一個入口：

- 了解議題、關注社群動態：訂閱電子報（見[持續關注](/contact/)）、加入 Matrix
- 參與翻譯與寫作：見[中文化與文件翻譯](docs:community/i18n/)、[參與](/join/)
- 評估自己的技術涉入程度：見[自我技能評估表](docs:community/skill-level/)
- 了解溝通與協作工具：見社群的[服務](/services/)

社群的討論主要在 Matrix（家伺服器 `im.anoni.net`），共筆用 CryptPad，線上會議用 Jitsi，帳號申請與各服務的入口也整理在[服務](/services/)頁。

## 路線圖更新

路線圖每季結束時檢視並調整，重大調整依社群的提案流程討論，並在 Matrix 公布（提案流程見[治理章程](/about/governance/)）。

**最後更新**：2026-10（Q4 進行中）。
