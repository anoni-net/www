---
title: Tor 系統管理團隊的 ADR 決策紀錄
description: Tor 系統管理團隊（TPA）從 RFC 改用 ADR 的全文翻譯，附上其他開源專案的提案與決策流程對照，以及台灣專案與社群的決策紀錄現況。
date: 2026-03-19
---

!!! info ""

    本文翻譯自 Tor Project 部落格的 [Keeping track of decisions using the ADR model](https://blog.torproject.org/tpa-adr/)（2026-02-16），文中的「我們」是 Tor Project 的系統管理團隊 TPA。文末的「社群補充」一節由 anoni.net 撰寫，對照其他開源專案的做法與台灣的現況。

在 Tor Project 的系統管理團隊（俗稱 TPA）裡，我們最近改變了做決策的方式。之後不論是即將進行的變更，或是針對某項提案的具體問題，你從我們這邊收到的溝通都會更清楚。

新流程只影響 TPA 團隊，Tor 內部每個團隊都有自己協調與決策的方式。我們鼓勵 Tor 內外的其他團隊評估看看，能否改善你們的流程與文件。

## 新流程

我們過去一直使用 RFC（Request For Comments，請求意見）流程，最近改為 ADR（Architecture Decision Record，架構決策紀錄）。

對我們來說，ADR 流程相當簡單，包含三件事：

1. 更精簡的模板
2. 更精簡的流程
3. 與決策紀錄分開的溝通準則

### 模板

作為團隊負責人，我做的第一件事是提出新模板（見 [ADR-100](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/0100-adr-template)），它是 [Nygard 模板](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md)的變體。[TPA 版本的模板](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/template)同樣簡潔，只有 5 個標題，值得完整引用：

- **Context（脈絡）**：我們看到什麼問題，促使我們做這項決策或變更？
- **Decision（決策）**：我們提議或正在進行的變更是什麼？
- **Consequences（後果）**：變更之後，哪些事變得更容易或更困難？
- **More Information（更多資訊，選填）**：還有什麼我們該知道的？較大的專案可以考慮納入時程、成本估計，以及對受影響使用者的衝擊（或許包含既有的 Personas）。一般會在這裡簡短評估考慮過的替代方案。
- **Metadata（詮釋資料）**：狀態、決策日期、決策者、被諮詢者、需被告知的使用者，以及討論區的連結。

[先前的 RFC 模板](https://gitlab.torproject.org/tpo/tpa/wiki-replica/-/blob/d52de1828d3ee406996345704d12663dd30f5513/policy/template.md)有 **17** 個標題，容易寫成很長的文件。現在的決策紀錄一眼就能讀完。

改用新模板之後，我更常把比較與腦力激盪放進 GitLab 的 issue。定價、替代方案的深入比較這類細節，改記在討論用的 issue 裡，文件本身維持精簡。

### 流程

整個流程簡單到也值得完整引用：

> 重大決策在會議中向利害關係人說明，較小的決策則用電子郵件。採納之前保留一段時間，讓大家提出最後的意見。

細節都寫在 [ADR-101](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/0101-adr-process)，重點是保持簡單。

提案的關鍵之一，是 Jacob Kaplan-Moss 稱為 [one weird trick](https://jacobian.org/2023/dec/5/how-to-decide/) 的「先決定誰做決定」。我們過去的流程對誰來做決策交代得很模糊，新的模板與流程在每項決策上都寫明決策者。

相對地，被諮詢的利害關係人太多時，有些決策會變成在瑣碎議題上沒完沒了的討論，也就是[瑣碎法則](https://en.wikipedia.org/wiki/Bike_shedding)（Law of triviality），又稱自行車棚效應（Bike Shed syndrome）。

新流程把利害關係人分得更清楚：

- **需被告知者**（informed）：以前叫「受影響使用者」
- **被諮詢者**（consulted）：以前沒有定義
- **決策者**（decision maker）：取代含糊的「核准」

要挑出這些利害關係人仍然不容易，但定義更明確了，也與經典的 [RACI 矩陣](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix)（Responsible, Accountable, Consulted, Informed）一致。

### 溝通準則

流程中很重要的一環（[ADR-102](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/0102-adr-communications)），是把做決策、記錄決策與對外溝通決策拆開。兩者要解決的問題截然不同，我們發現一份文件無法同時兼顧。

ADR 可能影響的範圍很廣，所以我們沒有替溝通訂固定的模板，只建議用[五何法](https://en.wikipedia.org/wiki/Five_Ws)（Five Ws，誰、什麼、何時、哪裡、為什麼），一樣保持簡單。

## 改變的緣由

[ADR 流程](https://adr.github.io/)不是我發明的，我最早是在 [Thunderbird Android 專案](https://github.com/thunderbird/thunderbird-android/blob/be2af5c6a0bce08385fc3f654c1185ccf9db3859/docs/architecture/adr/README.md)看到它。同一段時間，我正在檢討 RFC 流程（見[討論 issue](https://gitlab.torproject.org/tpo/tpa/team/-/issues/41428)），也讀了 Jacob Kaplan-Moss 對 [RFC 流程的批評](https://jacobian.org/2023/dec/1/against-rfcs/)。他的論點大致是：

1. RFC 流程「沒有包含任何決策框架」
2. 「RFC 流程容易導致無止境的討論」
3. 流程「獎勵能寫到讓人精疲力竭的人」
4. 「這些流程對專業不敏感」，對「權力動態與權力結構」也不敏感

上述問題我很多都犯過。我寫東西很囉唆，寫過[極長的提案](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/tpa-rfc-33-monitoring)，我懷疑從來沒有人從頭讀完。有些提案是大家累到放棄才通過的，有些則因為沒找對利害關係人而被忽略。

我們的 RFC 流程有哪些問題，[討論 issue](https://gitlab.torproject.org/tpo/tpa/team/-/issues/41428) 裡有更多細節。公平地說，舊流程在當時還是有用的，有總比沒有好，6 年間也記錄了數量可觀的變更與決策（[95 份 RFC](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy)）。

## 後續的實驗

如何溝通決策，我們仍在實驗，本文或許就是一例。溝通是獨立的一步，所以容易被遺忘或拖延，本文就晚了好幾個月才發出。

以前我們直接把 RFC 副本寄給大家，又快又簡單，但多數人讀不懂。現在需要另外寫一份溝通稿，工作量變多，希望換來的結果更容易消化。

歡迎在原文底下或[討論 issue](https://gitlab.torproject.org/tpo/tpa/team/-/issues/41428) 告訴我們你對新流程的想法，以及它在你那邊的效果。我們特別想聽已經在用類似流程的人，或讀完本文之後打算採用的人的經驗。

!!! note "重點整理"

    TPA 過去用 RFC 記錄決策，6 年累積了 95 份。RFC 流程缺乏決策框架，討論容易拖長，也獎勵寫得多的人，對專業與權力結構不敏感，結果文件難讀，誰有權拍板也不清楚。

    改用 ADR 之後有三項變化。模板從 17 個標題縮成 5 個，比較與估價移到 GitLab issue。每項決策寫明決策者、被諮詢者、需被告知者，對齊 RACI，避免沒人拍板，也避免太多人捲入瑣事。ADR 只負責記錄決策，對外公告另寫一份。

## 社群補充

以下兩節由 anoni.net 撰寫，不屬於原文。

### 其他開源專案的提案與決策流程

各專案提出提案、記錄決策的方式不盡相同，幾個常見的做法如下：

- **GOV.UK Design System**：用 RFC 討論提案、用 ADR 記錄最終決策，兩者並行。提案放在公開的儲存庫，第一份就是 [001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions](https://github.com/alphagov/govuk-design-system-architecture/blob/main/proposals/001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions.md)。
- **Bitwarden**：在貢獻者文件裡維護 [ADR 索引](https://contributing.bitwarden.com/architecture/adr/)，以 ADR 為主要的架構決策紀錄。
- **GitLab**：Delivery 團隊在公開的 handbook 維護 ADR，收在 [Delivery Decisions](https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/gitlab-delivery/decisions/)（2026-10 查核）。
- **ADR 社群與 MADR**：[adr.github.io](https://adr.github.io/) 提供 MADR（Markdown Architectural Decision Records）模板與工具，通用且輕量，許多專案採用。
- **Rust**：語言與標準庫的變更走 [rust-lang/rfcs](https://github.com/rust-lang/rfcs) 的 RFC 流程，提案編號、公開討論，決策結果留在同一個儲存庫。
- **Python**：語言與標準庫的變更以 [PEP](https://peps.python.org/)（Python Enhancement Proposal）作為正式的提案與編號制度。
- **Kubernetes**：功能與架構變更以 [KEP](https://github.com/kubernetes/enhancements)（Kubernetes Enhancement Proposal）提案與討論。

GOV.UK 讓 RFC 討論與 ADR 紀錄並行，Bitwarden 與 TPA 以 ADR 為主，大型生態系則多半用編號提案（RFC、PEP、KEP）。TPA 的做法有兩點與眾不同，一是明確「先決定誰做決定」，二是把決策紀錄與對外溝通分開處理。

### 台灣專案與社群的現況

台灣多數的專案與社群已經有提案、討論、取得共識的流程，只是不一定用 ADR 這個名稱，也較少把決策文件放在 `adr/` 目錄或用 MADR 模板公開。

- **公民科技社群（例如 g0v）**：常見做法是提案文件、[HackMD 共筆](https://g0v.hackmd.io/@jothon/intro)、黑客松或線上會議討論（見 [g0v 開源協作手冊](https://g0v.hackmd.io/@jothon/g0v-cowork-guideline/)）。架構層級的關鍵決策分散在共筆、issue、PR、簡報與大松提案裡，過一段時間就不容易追溯當初的理由。
- **政府與公部門的合作案**：多半有規格書、系統設計文件或專案報告，形式接近在里程碑一次寫完的大文件，不會隨時間累積成 ADR log，通常不完全公開，外部貢獻者看不到背後的取捨。
- **企業的開源專案**：有些團隊在公司內部用決策紀錄或設計文件管理架構變更，但只留在內部的維運知識庫，公開的只有程式碼，看不到決策歷史。

上述專案缺少的是穩定、容易追溯、外部的人也讀得懂的決策紀錄。ADR 讓每個重要決定各自寫成一份小檔案，記下當時的理由，不必硬寫一大本規格書，也比只留在 issue 裡容易長期維護。新加入的人讀過 ADR，就知道系統為什麼長成現在的樣子，不必重複同樣的討論。

anoni.net 的[治理章程](/about/governance/)（草案）在「決策方式」一節用一張表，依影響範圍列出提案管道與決策方式，例如結構性變動先在 Matrix 討論再提交 PR，保留 3 天緩衝，自架服務的政策變更由核心成員以共識決定。章程的表格回答了「誰做決定」，但沒有規定決定之後要留下什麼樣的紀錄，ADR 的單檔模板可以補上紀錄的部分。
