---
title: 參與 Tor Project
description: Tor Project 的規劃與活躍專案、官方溝通管道、正體中文社群可以開始的參與方式，以及匿名網路社群的工作與 Tor 的關聯。
---

Tor Project 是公開治理的非營利組織，溝通管道、原始碼與規劃文件大多對外開放，個人不必代表任何組織，就能從翻譯、營運中繼或舉辦 meetup 開始參與。匿名網路社群 anoni.net 推廣 Tor、Tails、OONI 的這一年，最常被問到的就是如何直接參與 Tor 上游的開發與社群。

在地的觀測資料可以交給 Tor 維護網路健康的團隊，亞太每多一個中繼，Tor 網路的位址就更分散。Tor 的正體中文翻譯也需要有人跟著每次更新維護。各項參與方式在文件站有操作教學的，都附上連結。

!!! tip "門檻最低的兩項參與方式"

    一項是到 Weblate 校對 Tor 支援文件的正體中文翻譯，`zh_Hant` 已大致譯完，目前的工作是跟上原文的更新（[Tor new-support-portal](https://hosted.weblate.org/projects/tor/new-support-portal/)，流程見[中文化與文件翻譯](docs:community/i18n/)）。另一項是到 Tor 官方論壇與 Matrix 的 `#tor-project:matrix.org` 頻道自我介紹。兩項都不需要等待核准，以個人身分參與即可，之後的正式合作也從這些貢獻紀錄開始。

## Tor 規劃的公開位置

Tor Project 的規劃分兩層公開，給一般關注者的策略寫在官方部落格，給貢獻者的細部規劃放在自架的 GitLab wiki。

Tor Project 每年在[官方部落格](https://blog.torproject.org/)發布年度方向，列出當年的優先項目。2026 年的重點是把規避審查的功能整合進更多 Tor 軟體（例如 Tails 與 Tor VPN），並持續關注俄羅斯、中國這類各自封閉網路的做法[^1]。年度回顧裡的長期重點有四項：效能與安全、網路健康、抗審查、與第三方整合的相容性[^2]。財報可以看出資助結構的變化，美國政府資助的占比從 FY2021-22 的 53.5% 降到 FY2023-24 的 35.08%，目標是降低對單一資助來源的依賴[^3]。線上大會 State of the Onion 通常在年底舉行，2025 年分成 11 月的團隊更新與 12 月的社群更新兩場，可以一次看完年度方向[^4]。

細部規劃在 [Tor 的 GitLab](https://gitlab.torproject.org/tpo)，公開專案不需要登入就能閱讀。各團隊的 `team` meta 專案在 wiki 放 roadmap 與會議記錄，整個組織的資助案整理在 `tpo/team` 的 Sponsors 總覽頁[^5]。系統管理團隊（TPA）的年度 roadmap 寫得最具體[^6]，Arti 的里程碑標在群組裡帶 Roadmap 標籤的 issue 上[^7]。milestones 端點需要登入，計畫的期程也無法透過公開 API 取得，要從各 wiki 內嵌的連結查。

## 重點方向與活躍專案

本節內容在 2026 年 6 月查核，Tor 的專案與資助變動快，以官方最新的公告為準。參與 Tor 不需要先了解這些技術細節，想直接看能做什麼，可以跳到[參與方式](#參與方式)。

### 專案的活躍度

Tor 的 GitLab 上有兩百多個專案，活躍程度差異很大。2026 年 6 月用公開 API 掃描時，未封存的專案約 252 個，其中約 103 個在 30 天內有活動，最活躍的是 network-health，web、core、tpa、applications 也有不少專案在持續更新[^8]。數字會隨時間變動，即時的狀態可以在 GitLab 依 `last_activity_at` 排序查看。

### 技術主線

- 抗審查的三種連線方式。WebTunnel 把橋接流量偽裝成一般的 HTTPS，2025 年在俄羅斯是重要的規避工具。Snowflake 用志工瀏覽器的 WebRTC（瀏覽器之間建立即時連線的技術）當臨時代理，目前穩定運作，介紹見 [Tor Snowflake 橋接點](docs:tools/tor-snowflake/)。Conjure 利用 ISP 沒有使用的位址空間，對抗審查者逐一列出已知代理 IP 再封鎖的手法，官方規劃從 2026 年起逐步推出[^9]。
- Arti，用 Rust 重寫的 Tor。客戶端核心、circuit 與 Onion Service 已經穩定，relay 與 directory authority（維護中繼名冊的核心伺服器）還在開發，官方沒有承諾與舊版 C 實作功能一致的時程。
- Counter Galois Onion（CGO），新的對稱加密方式，修補舊加密可以被竄改、被用來追蹤連線的弱點。目前在 Arti 裡標為實驗功能，測試完成後才會預設啟用。
- Android 版的 Tor VPN，底層使用 Arti，2025 年 9 月推出 beta 版，官方標明仍屬實驗、不適合高風險的情境。iOS 上仍然使用 Orbot。
- Onion Service 的易用性與防止濫用，以及 Tails（見[什麼是 Tails](docs:tools/what-is-tails/)）併入 Tor Project 之後的整合。

### 資助案與延續的方向

資助案最能看出哪些方向會延續下去。下表是 Sponsors 總覽頁列出的部分資助案[^5]，編號以 `S` 開頭。

| 資助案 | 方向 | 與匿名網路社群的關聯 |
|---|---|---|
| `S96` | 中國、香港、西藏的審查規避，包含新的 pluggable transport、更難封鎖的橋接、改善橋接的派發 | 社群關注的審查規避 |
| `S112` | 對抗惡意中繼、改善網路健康，包含監控工具、中繼營運者的行為準則、抵禦中繼攻擊 | 社群的觀測工作 |
| `S119` | Arti，用 Rust 重寫的 Tor | 下一代的技術基礎 |
| `S150` | 淘汰 BridgeDB，全面改用 RDSys 派發橋接 | 橋接的派發方式 |
| `S101` | Android 版的 Tor VPN | 給一般使用者的產品 |
| `S131` | Mullvad Browser 與 Tor Browser 的重構 | 瀏覽器 |

`S96` 與 `S112` 跟社群的工作最相關，前者處理正體中文使用者面對的審查，後者對應社群在做的網路可達性觀測。

## 官方溝通管道

Tor 的 IRC（OFTC 網路）與 Matrix 雙向橋接，用 Element 加入 Matrix 或用 IRC，都會進到同一個頻道[^10]。Tor 官方的頻道在 `matrix.org`，與匿名網路社群自架的 `im.anoni.net` 分開。

| 頻道 | 用途 |
|---|---|
| `#tor` | 使用者支援，詢問 Tor 的操作問題 |
| `#tor-dev` | 開發、協定與程式的技術討論 |
| `#tor-project` | 組織與社群事務、meetup、outreach |
| `#tor-relays` | 中繼營運者的社群 |
| `#tor-l10n` | 翻譯與在地化 |
| `#tor-meeting` | 旁聽或參加有公開紀錄的團隊會議 |

文字討論與公告在 [Tor Forum](https://forum.torproject.org/)（Discourse 論壇，分成使用者支援、在地化、活動等類別），郵件列表在 [lists.torproject.org](https://lists.torproject.org/) 訂閱。組織層級的事務用 email 聯絡：非營利事務、商標與合作協調寄 <frontdesk@torproject.org>，邀請講者寄 <speaking@torproject.org>，安全問題寄 <security@torproject.org>。

加入頻道與論壇之前，先閱讀 Tor 的[社群政策與行為準則](https://community.torproject.org/policies/)。

## 參與方式

依正體中文在地社群的可行性排序，文件站有操作教學的都附上連結。

1. 在地化翻譯。門檻最低，不需要審核帳號，也不需要技術背景。個人就能在 Weblate 開始，同時改善正體中文的品質，也是累積社群貢獻紀錄最快的方式。流程與 Weblate 的連結見[中文化與文件翻譯](docs:community/i18n/)的「Tor 文件翻譯」一節，第一次參與先讀[成為 Tor 翻譯者](https://community.torproject.org/localization/becoming-tor-translator/)。
2. 在 `#tor-project` 與論壇自我介紹。meetup、outreach 與社群事務都在這裡討論，之後的正式合作也從這裡開始。
3. 舉辦在地 meetup。Tor 的 [Outreach](https://community.torproject.org/outreach/) 提供 Street Team Kit、簡報與舉辦 Tor meetup 的素材，官方鼓勵自主舉辦，不需要審核，需要講者時寫信到 <speaking@torproject.org>。
4. 營運中繼或橋接。有機器與頻寬的成員可以在台灣架設中繼，增加亞太的節點，步驟見[如何搭建 Tor Relay](docs:community/setup-tor-relay/)。偽裝成 HTTPS 的橋接見[設置 Tor WebTunnel](docs:community/setup-tor-webtunnel/)，遇到問題可以到 `#tor-relays` 與 tor-relays 郵件列表詢問。
5. 開發與回報問題。到 [anonticket.torproject.org](https://anonticket.torproject.org/) 可以匿名申請 GitLab 帳號或回報問題，取得帳號之後到對應的 repo 開 issue。新手可以從標了 first-contributors 的 issue 開始，技術討論在 `#tor-dev`。
6. 成為 Training Partner。Tor 的 [training partners](https://community.torproject.org/training/partners/) 是組織與 Tor 之間最正式的合作形式，通常要先在前幾項累積貢獻紀錄，適合當作中長期的目標。

## 匿名網路社群的工作與 Tor 的關聯

- 正體中文的翻譯與用語。社群已經在做 `zh_Hant` 的翻譯與用語規範，可以直接延伸到 Weblate 上的 Tor 翻譯。
- 網路可達性觀測。社群維運的 [Tor 中繼節點觀測](/projects/pulse/)（Pulse）與 [OONI 觀測涵蓋率](/projects/asn-coverage/)（ASN Coverage）對應 network-health 團隊與 `S112` 的工作，觀測成果可以在該團隊的社群場合分享。
- 校園中繼。[Tor Relay 校園建立研究專題](/join/relay-on-campus/)源自 EFF 與 Tor Project 合作的 Tor University Challenge，台師大已經有運作中的節點（見[台師大 NZ 訪談](/updates/2025/12/ntnu-nz/)）。

社群年度計畫裡的安排見 [2026 年度路線圖](/join/roadmap-2026/)。State of the Onion 的社群場會公開徵求各地社群的更新，社群可以在那裡向國際報告這些成果。

## 相關閱讀

- [中文化與文件翻譯](docs:community/i18n/)：Tor 文件的翻譯流程與 Weblate 的使用方式
- [如何搭建 Tor Relay](docs:community/setup-tor-relay/)：在台灣架設中繼的步驟
- [設置 Tor WebTunnel](docs:community/setup-tor-webtunnel/)：把橋接流量偽裝成一般 HTTPS 的架設方式
- [如何參與與認領主題](/join/)：加入匿名網路社群、認領年度主題的方式

[^1]: [Advancing digital rights in 2026](https://blog.torproject.org/advancing-digital-rights-in-2026/) - The Tor Project Blog
[^2]: [The Tor Project's 2024 Year in Review](https://blog.torproject.org/2024-year-in-review/) - The Tor Project Blog
[^3]: [The Tor Project Financial Reports for July 2023 to June 2024](https://blog.torproject.org/financials-blog-post-2023-2024/) - The Tor Project Blog
[^4]: [State of the Onion 2025](https://blog.torproject.org/state-of-the-onion-2025/) - The Tor Project Blog
[^5]: [tpo/team wiki：Sponsors 總覽](https://gitlab.torproject.org/tpo/team/-/wikis/Projects/Sponsors-2023) - Tor Project GitLab
[^6]: [tpo/tpa/team wiki：roadmap/2025](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/roadmap/2025) - Tor Project GitLab
[^7]: [tpo 群組 Roadmap 標籤 issues](https://gitlab.torproject.org/groups/tpo/-/issues/?label_name[]=Roadmap&state=opened) - Tor Project GitLab
[^8]: [Tor Project GitLab 公開 API](https://gitlab.torproject.org/api/v4/groups/tpo/projects?include_subgroups=true) - 2026 年 6 月掃描的非封存專案活躍度快照
[^9]: [Staying ahead of the censors in 2025](https://blog.torproject.org/staying-ahead-of-censors-2025/) - The Tor Project Blog
[^10]: [Chat with the Tor community](https://support.torproject.org/get-in-touch/chat-with-us/) - Tor Project Support
