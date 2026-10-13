---
title: Tor Relay 校園建立研究專題
description: 匿名網路社群 2026 年三大主題之一，在大專院校架設 Tor 中繼節點的推動目標、台師大案例、提案與架設範本，以及參與方式。
---

Tor Relay 校園建立是匿名網路社群 anoni.net 2026 年的三大主題之一，與[個人隱私指引](/join/privacy-guide/)、[匿名支付](/join/payments-research/)並列。社群在大專院校推動架設 Tor 中繼節點，並把提案、與校方溝通、技術設定與維運的過程整理成範本，讓之後加入的學校更容易推動。歡迎在學學生、校友、教職員與有網路維運經驗的人一起參與（見[參與方式](#參與方式)）。

## 選擇校園的原因

Tor 網路的匿名性仰賴多元的中繼節點，中繼集中在少數國家或少數網路供應商時，Tor 對抗流量分析的能力就會降低。台灣在 Tor Metrics 上能看到的中繼數量有限，截至 2026-06 約有 15 個運作中的中繼，德國有上千個、美國有數千個，差距明顯（數字會隨時間變動，即時狀況見 [Tor 中繼節點觀測](/projects/pulse/)）。

大專院校適合補上台灣中繼數量的缺口：

- **頻寬穩定**：學術網路通常有充足且穩定的頻寬
- **技術人才**：資工、資管系與資訊中心的師生具備架設與維運的能力
- **制度明確**：學校有正式的提案與審核流程，比個人或小公司架設更容易說明用途、爭取支持
- **教育價值**：架設過程本身就是匿名網路、資安與開源治理的教學場景
- **國際計畫**：參與 EFF 的 [Tor University Challenge](https://toruniversity.eff.org/zh-tw/)，把台灣的校園納入全球的校園中繼網路

## 2026 推動目標

- **校園架設 SOP**：涵蓋提案、與學校溝通、技術設定、上線與後續維運的完整流程（2026-05 隨範本工具包公開）
- **應答範本與案例庫**：法律疑慮、頻寬使用、用途說明等常見問題的回應參考
- **其他學校的接洽**：以台師大為起點，擴展到其他大專院校
- **與 EFF、Tor Project 的聯繫管道**：建立穩定的國際聯繫，把台灣的案例回饋給全球計畫
- **即時觀測**：用 [Tor 中繼節點觀測](/projects/pulse/)持續追蹤校園節點的運作狀況
- **結合資安教育活動**：把 Tor Relay 架設納入校園資安宣導、迎新講座等場合

## 相關文章

- 案例：[在台師大架設 Tor Relay：一段與學校溝通、留下可能性的實作經驗](/updates/2025/12/ntnu-nz/)
- 國際：Tor Project 部落格的客座文章 [Setting Up a Tor University Relay in Taiwan](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)
- 架設指南：[Tor Relay 架設指南](/join/setup-tor-relay/)、[Tor WebTunnel 橋接架設指南](/join/setup-tor-webtunnel/)
- 觀測：[Tor 中繼節點觀測](/projects/pulse/)
- 概念：[什麼是 Tor](docs:tools/what-is-tor/)、[Tor Snowflake](docs:tools/tor-snowflake/)
- 進階：[一台會遺忘的伺服器：探索 Stateless Relays](docs:blog/2026/04/a-server-that-forgets-exploring-stateless-relays/)

## 已完成的工作

- **第一個校園節點**：國立臺灣師範大學資訊工程學系資訊中心的 Tor Relay 運作中，由社群夥伴 NZ 經教授與教職員提案、協調後完成建置
- **Tor Project 部落格客座文章**：台師大案例的英文版刊登在 [Tor Project 部落格](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)，讓其他國家的推動者也能參考
- **Tor University Challenge 中譯**：完成 [EFF Tor University Challenge 網站](https://toruniversity.eff.org/zh-tw/)的正體中文翻譯，降低台灣其他學校接觸計畫的語言門檻
- **Tor 中繼節點觀測上線**：[觀測頁](/projects/pulse/)每小時更新台灣與鄰近共十五個地區的中繼節點狀況
- **案例訪談**：台師大的架設過程整理成[深度訪談](/updates/2025/12/ntnu-nz/)，公開給後續的推動者參考
- **範本工具包**：台師大的實作經驗整理成提案文件、技術 SOP 與校方 FAQ 三份範本，其他學校可以直接套用（見[上線公告](/updates/2026/05/2026-campus-tor-relay-template-kit/)與下一節）

## 範本工具包

範本工具包整理自社群夥伴 NZ 在台師大的實作經驗，其他學校的學生不必從零開始，可以複製範本、依學校的狀況改寫，再送進自己學校的審核流程。

- [校園 Tor Relay 提案範本](/join/relay-on-campus/proposal/)：提案文件、四封溝通 email、行政時間軸
- [校園 Tor Relay 架設 SOP](/join/relay-on-campus/sop/)：torrc、UFW、狀態網頁、監控、事件處置 runbook
- [給校方與法務的校園 Tor Relay FAQ](/join/relay-on-campus/faq/)：校方常見疑慮的問答與台灣脈絡的補充

建議先讀[台師大案例訪談](/updates/2025/12/ntnu-nz/)了解全貌，再依角色選讀範本，提案者讀提案範本、技術維運者讀 SOP，與校方面談時帶上 FAQ。

## 進行中的工作

- **其他學校的接洽**：與其他大專院校初步聯繫、評估可行性
- **資安活動的合作**：與學校資安週、迎新講座、Hackathon 等活動的合作模式
- **政策溝通材料**：給教育部層級的計畫說明、跨國比較資料
- **外部資源的翻譯**：候選清單見下一節

## 翻譯候選與延伸閱讀

社群標記了幾份候選的外部資源，歡迎志工協助翻譯或摘錄重點：

- [Tor Project Relay Operator Guides](https://community.torproject.org/relay/)：Tor Project 官方的中繼營運指南
- [Tor University Challenge case studies](https://toruniversity.eff.org/case-studies/)：國際的校園案例研究
- [EFF Legal FAQ for Tor relay operators](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)：營運中繼的法律常見問題
- 各國校園 Tor Relay 的政策案例（MIT、Stanford、CMU 等）

## 參與方式

社群在 Matrix 討論（家伺服器 `im.anoni.net`），校園 Tor Relay 的討論集中在社群 Public Space 裡的相關 room，帳號申請與各項服務的入口見[社群自架服務](/services/)。

特別歡迎具備以下背景的人加入：

- **大學在學生、校友、教職員**：了解自己的學校，能評估推動的可行性
- **網路維運經驗**：參與技術設定與長期維運
- **政策溝通能力**：協助與校方、資訊中心、法務單位溝通
- **法律專業**：解讀中繼營運相關的法律疑慮（個資、刑事責任、學校規章）
- **活動籌辦經驗**：把架設工作納入資安週、迎新等校園活動

沒有架設過 Tor Relay 也歡迎參與，想學就足以成為加入的理由，社群會搭配 [Tor Relay 架設指南](/join/setup-tor-relay/)協助你實際操作。

## 議題守則

社群的所有討論以合法用途為前提，校園 Tor Relay 主題以教育、研究與參與網路基礎建設為目的，不協助任何違法行為。校園架設會使用學校的資源，需走正式的提案與審核流程，並向校方充分說明節點的用途與營運責任。
