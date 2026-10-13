---
title: 個人隱私指引研究專題
description: 匿名網路社群 2026 年三大主題之一，依日常、敏感工作、高風險三種情境整理隱私工具與步驟，包含研究目標、文件站的相關文章、目前進度與參與方式。
---

個人隱私指引是匿名網路社群 anoni.net 2026 年的三大主題之一，與[Tor Relay 校園建立](/join/relay-on-campus/)、[匿名支付](/join/payments-research/)並列。社群依日常使用、敏感工作、高風險三種情境，把隱私工具與操作步驟整理成可以照著做的指引，內容寫在文件站，依概念、工具、場景、進階分層。歡迎有教學、寫作、翻譯、設計或資安背景的人一起參與（見[參與方式](#參與方式)），年度規劃與各季進度見 [2026 年度路線圖](/join/roadmap-2026/)。

## 獨立成一個主題的原因

社群推廣 Tor、Tails、OONI 多年，最常被問到的是「下一步該做什麼，才能讓自己更安全」。要回答這個問題，需要一套依情境分級、可以實際操作的隱私指引。

現有的中文資源多半停留在介紹單一工具或列舉技巧，概念、工具、場景三層之間沒有串接。讀者讀完工具頁，常常不知道它對應哪一種風險，讀完概念或場景頁，也不知道該從哪一步開始。社群想把這三層接起來，讓讀者從知道工具的名稱，一路走到在自己的情境下實際採用。

## 2026 研究目標

- **三級威脅模型框架**：把日常使用、敏感工作、高風險三種情境對應的工具與步驟整理成參考表
- **從概念到實作的判斷流程**：在威脅模型與工具操作之間補上判斷的依據，例如何時該提高防護等級、何時不必過度防護
- **常見誤區**：拆解 VPN ≠ 匿名、HTTPS ≠ 安全、私密模式 ≠ 隱私、去中心化 ≠ 匿名這類常見的誤解。VPN 與去中心化兩項已有專篇（[VPN 的風險與選擇](docs:tools/vpn-guide/)、[常被誤認為匿名的網路](docs:advanced/mistaken-for-anonymity/)），HTTPS 與私密模式還沒有
- **場景指引**：為記者、社運參與者、家暴受害者、LGBTQ+ 等角色整理實際操作的流程
- **跨主題串接**：把連線層、個資與身分、金流三個面向（見[網路自由為什麼重要](docs:basics/internet-freedom/)）整合進個人的隱私規劃
- **教材**：把研究成果整理成工作坊與小聚可用的教材

## 相關文章

文章依文件站[指南](docs:guides/)的分層，分散在概念、工具、場景、進階與在地法規各區：

- 概念：[匿名、隱私、假名、機密性的差別](docs:basics/anonymity-vs-privacy/)、[威脅模型如何建立](docs:basics/threat-model/)、[Metadata 是什麼，為什麼重要](docs:basics/metadata/)、[社群平台怎麼收集你的資料](docs:basics/platform-tracking/)、[監控現在做得到什麼](docs:basics/surveillance-capability/)、[怎麼維持多個網路身分](docs:basics/multiple-identities/)、[瀏覽器指紋是什麼，為什麼很難擺脫](docs:basics/browser-fingerprinting/)
- 工具：[什麼是匿名網路？](docs:tools/what-is-anonymity-network/)、[什麼是 Tor](docs:tools/what-is-tor/)、[什麼是 Tails](docs:tools/what-is-tails/)、[Tor Browser 進階設定](docs:tools/tor-browser-advanced/)、[Tor Snowflake](docs:tools/tor-snowflake/)、[Tails、Whonix、Qubes 的差別](docs:tools/tails-vs-whonix-vs-qubes/)、[GrapheneOS：高度隱私的行動作業系統](docs:tools/grapheneos/)、[匿名通訊工具比較](docs:tools/messaging-comparison/)、[OnionShare](docs:tools/onionshare/)、[什麼是 CryptPad](docs:tools/what-is-cryptpad/)、[密碼管理器入門](docs:tools/password-manager/)、[郵件別名怎麼用，以及它把信任交給誰](docs:tools/email-alias/)、[Asian Diceware，帶亞洲味的英文密語字典](docs:tools/asian-diceware/)、[VPN 的風險與選擇](docs:tools/vpn-guide/)、[加密 DNS 怎麼選、怎麼確認真的生效](docs:tools/encrypted-dns/)、[用 AI 工作時怎麼避免資料外洩](docs:tools/ai-privacy/)、[手機隱私設定逐步指引](docs:tools/phone-privacy-settings/)
- 小工具：[威脅模型清單](docs:utils/threat-model/)
- 場景：[一般人平常該做到什麼](docs:scenarios/everyday-baseline/)、[記者保護消息來源](docs:scenarios/journalist/)、[社運行動者的數位準備](docs:scenarios/activist/)、[家暴受害者的數位準備](docs:scenarios/domestic-violence/)、[LGBTQ+ 與性少數的匿名社交](docs:scenarios/lgbtq/)、[選舉觀察員的自保](docs:scenarios/election-observer/)、[在中國大陸的公開平台傳播資訊](docs:scenarios/mainland-speech/)、[出差與研討會的數位準備（東亞與東南亞）](docs:scenarios/asia-travel/)、[出國的門號與網路連線](docs:scenarios/travel-connectivity/)、[出國前數位安全：用 AI 自助產生目的地概況](docs:scenarios/travel-ai-briefing/)
- 進階：[端對端加密如何運作](docs:advanced/e2ee/)、[常被誤認為匿名的網路](docs:advanced/mistaken-for-anonymity/)、[後量子密碼概觀](docs:advanced/post-quantum/)、[去中心化網站發布](docs:advanced/dweb-ipfs-onion/)
- 在地：[台灣個資法 2025 修法](docs:taiwan/pdpa-2025/)、[揭弊者保護法的技術觀察](docs:taiwan/whistleblower-law/)

各篇初稿大多已上線，之後依季度節奏校訂與補充。

## 已完成的工作

- **概念層九篇**：[網路自由為什麼重要](docs:basics/internet-freedom/)、[匿名、隱私、假名、機密性的差別](docs:basics/anonymity-vs-privacy/)、[威脅模型如何建立](docs:basics/threat-model/)、[Metadata 是什麼，為什麼重要](docs:basics/metadata/)、[為什麼匿名支付重要](docs:basics/payments-anonymity/)、[社群平台怎麼收集你的資料](docs:basics/platform-tracking/)、[監控現在做得到什麼](docs:basics/surveillance-capability/)、[怎麼維持多個網路身分](docs:basics/multiple-identities/)、[瀏覽器指紋是什麼，為什麼很難擺脫](docs:basics/browser-fingerprinting/)
- **三個面向的框架**：在[網路自由為什麼重要](docs:basics/internet-freedom/)一文確立連線層、個資與身分、金流三個面向，作為個人隱私指引的整體架構
- **在地法規參考**：[台灣個資法 2025 修法](docs:taiwan/pdpa-2025/)、[揭弊者保護法的技術觀察](docs:taiwan/whistleblower-law/)兩篇已完成
- **寫作規範與分類**：訂定[寫作風格規範](/join/writing-style/)，文件站整理成七大分類並建立[指南](docs:guides/)入口頁，讀者可以依層次找到對應的文章

## 進行中的工作

- **各層文章的校訂**：工具、場景、進階各層的初稿已上線，依讀者回饋持續校訂與補充
- **常見誤區的補完**：HTTPS ≠ 安全、私密模式 ≠ 隱私兩項還沒有專篇
- **三級隱私指引合集**：本主題的核心交付物，原訂 2026 年第三季整合上述各層的內容
- **工作坊教材**：把研究成果轉成工作坊與小聚用的講義
- **外部資源的翻譯**：候選清單見下一節

## 翻譯候選與延伸閱讀

社群標記了幾份候選的外部資源，歡迎志工協助翻譯或摘錄重點：

- [EFF Surveillance Self-Defense](https://ssd.eff.org/)：EFF 的個人數位安全指南，有完整的威脅模型分級與工具教學
- [Privacy Guides](https://www.privacyguides.org/)：開源社群維護的隱私工具推薦清單
- [The Citizen Lab](https://citizenlab.ca/)：監控軟體與跨國威脅的實證研究
- [Security in a Box](https://securityinabox.org/)：給 NGO 與行動者的數位安全工具箱
- [Tor Project 的使用者支援文件](https://support.torproject.org/zh-TW/)

## 參與方式

社群在 Matrix 討論（家伺服器 `im.anoni.net`），個人隱私指引的討論集中在社群 Public Space 裡的相關 room。共筆用 CryptPad，定期的視訊會議用 Jitsi，帳號申請與各項服務的入口見[服務](/services/)。

特別歡迎具備以下背景的人加入：

- **教學推廣或工作坊帶領經驗**：把技術概念轉成一般人能理解的內容
- **寫作或翻譯經驗**：整理篇幅較長的技術資源
- **UX 或設計背景**：把指引視覺化，例如流程圖、分級對照表
- **第一線實務經驗**（記者、NGO 工作者、社運參與者）：知道指引最常缺少哪些內容
- **資安背景**：審稿，確認技術描述正確

不需要資安背景也歡迎參與，想學就足以成為加入的理由。

2026 年 9 月 6 日，社群在葡萄牙 Estoril 的 [Global Gathering 2026](/events/gg2026/) 擺攤，想在現場收集的回饋之一，是哪些隱私指引沒有考慮到區域的實際處境。

## 議題守則

社群的所有討論以合法用途為前提。個人隱私指引以教育與理解風險為目的，不協助逃避法律責任、騷擾、跟蹤或其他違法行為。涉及具體個案的法律問題請諮詢專業人士，社群成員的觀察不能取代法律意見。
