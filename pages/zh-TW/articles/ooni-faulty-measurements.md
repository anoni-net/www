---
title: OONI 錯誤量測的辨識方法與匿名憑證
description: OONI 一篇工程文章的導讀，整理四類啟發式檢查的發現、新的偵測構想、錯誤量測的處置原則，以及匿名憑證系統如何在不儲存個資的前提下評估量測的可信度。
date: 2026-07-17
---

很多人靠 OONI 的公開資料集判斷某個網站在某個國家能否連線，anoni.net 的 [OONI 觀測涵蓋率](/projects/asn-coverage/)也建立在同一份資料上。資料集開放任何人投稿，有人送入假資料，或裝置設定錯誤產生誤導性的紀錄，整份資料的可信度都會被稀釋。OONI 在一篇工程文章[^1]裡說明他們如何找出錯誤的量測，以及正在導入正式環境的匿名憑證（anonymous credentials）系統如何在不儲存個資的前提下擋下濫用。不留個資也能評估量測可信度的做法，本身就是值得參考的隱私工程範例，後面的[匿名憑證系統的運作方式](#credentials)一節會回頭談。

!!! info ""

    本文是 anoni.net 對 OONI 工程文章 [From Heuristics to Anonymous Credentials: Assessing OONI's Approach to Bad Measurements](https://ooni.org/post/2026-faulty-measurements/)（2026-07-06）的導讀與摘要，依原文的章節整理重點，並非逐字翻譯。原文另有約 20 張統計圖與多份完整資料表，數據細節請直接讀原文。

OONI（Open Observatory of Network Interference，開放網路干擾觀測站）是全球性的網路審查觀測專案，OONI Probe 依一份網站清單逐一連線，回報每個網站在當地能否連線，結果一律進入公開資料集。任何人都能下載資料做分析，同樣地，任何人也都能送資料進來。原文要回答的問題，就是在開放投稿的前提下，如何辨認並過濾品質有問題的量測。

## 原文的架構

OONI 先用手上既有的資料建立一套辨認錯誤量測的基準，再評估新的匿名憑證系統能把基準往上推多少。啟發式（heuristic）是一組簡單、成本低的判斷規則，不追求百分之百準確，先用幾條經驗法則把可疑的量測篩出來。全文分成三塊，先用簡單規則檢查既有資料能找出多少問題（既有啟發式與四類發現），再提出更進階的規則（新啟發式），最後處理找到錯誤資料之後的因應機制（緩解策略與匿名憑證）。

## 既有指標與四個檢查角度

原文的 Existing metrics and heuristics 一節不動用任何新技術，只檢查 OONI 現在就收得到的資料能否認出錯誤的量測。OONI 挑了四個不需要犧牲使用者隱私的檢查角度，分別是 IP 地理位置的錯配、量測數量的暴增、時間戳記的不一致，以及作業系統與版本資訊的矛盾。每個角度都附了但書（caveat），說明該訊號在哪些情況下會誤判。例如 probe 內建的 GeoIP 資料庫可能過期，`probe_cc`（probe 回報的國碼）本來就可能跟真實 IP 對不上，分析時要先濾掉正常的誤差。四個角度與各自的但書，構成後面所有發現的方法論基礎。

## 四類異常的實際發現

### IP 地理位置的錯配

OONI 在 2025 年 3 月 19 到 21 日，於 probe 呼叫 `/api/v1/check-in` 端點時記錄 log，比對 probe 自己回報的國碼、ASN（自治系統編號）與收集端看到的真實出口 IP。16,139 筆樣本裡有 1,196 筆對不上，約 7.41%。原文列出最常見的 10 組國碼錯配：

| 回報國碼 | 真實 IP 國碼 | 筆數 |
|---|---|---|
| US 美國 | CA 加拿大 | 89 |
| CA 加拿大 | RU 俄羅斯 | 49 |
| CZ 捷克 | US 美國 | 43 |
| BS 巴哈馬 | US 美國 | 36 |
| CA 加拿大 | US 美國 | 30 |
| CA 加拿大 | SG 新加坡 | 30 |
| CZ 捷克 | GB 英國 | 25 |
| CA 加拿大 | KH 柬埔寨 | 18 |
| AU 澳洲 | KH 柬埔寨 | 18 |
| US 美國 | DE 德國 | 16 |

錯配的來源絕大多數是 VPN，出現最多的網路是 Datacamp、Cloudflare、M247 這些已知的 VPN 機房。回報加拿大、真實 IP 在俄羅斯的 49 筆全部來自 Cloudflare，對應的是使用 WARP 這類 VPN 的使用者。表格裡多數組合都屬於同一種情況，probe 回報自己在 A 國，流量卻從 B 國的 VPN 出口送出。原文沒有找到明顯可歸因於惡意竄改或 probe 設定錯誤的錯配。

### 量測數量的暴增

OONI 統計每個 probe 在 1 分鐘內產出的量測筆數，平均是 8 筆，99 百分位是 54 筆。篩出每分鐘超過 200 筆的極端案例後，找到一個名為 `ooniprobe-react-os`、並非 OONI 官方發行版本的用戶端。它只送 `probe_cc = CN`（中國）的資料，以每分鐘 200 筆（相當於每秒 3 筆）的速度送出 `web_connectivity` 量測，速率遠超正常範圍。更反常的是，`ooniprobe-react-os` 送出量測的速度比同地區其他 probe 還快，量這麼大卻沒有出現對應的網路瓶頸。另一個案例是緬甸在 2025 年 1 月 6 日出現的陣發性暴增。

### 時間戳記的不一致

OONI 比對量測開始時間 `measurement_start_time` 與 `measurement_uid` 內含的時間戳，找出上傳太晚或時間落在未來的紀錄。2025 年 3 月 2 日到 4 月 1 日的 3,440 多萬筆量測裡，只有 0.82% 有時間異常，多數落在過去，集中在 Linux。原文依平台拆解如下，Linux 的異常率 2.16% 明顯高於其他平台：

| 平台 | 過去異常（>1h） | 未來異常（>1h） | 異常合計 | 該平台總量 | 異常率 |
|---|---|---|---|---|---|
| ios | 2,375 | 0 | 2,375 | 240,843 | 0.99% |
| windows | 34,192 | 24,938 | 59,130 | 10,503,040 | 0.56% |
| android | 21,132 | 5,509 | 26,641 | 10,389,320 | 0.26% |
| macos | 906 | 0 | 906 | 3,103,961 | 0.03% |
| linux | 185,322 | 7,908 | 193,230 | 8,947,716 | 2.16% |

大量異常來自委內瑞拉的同一個 ASN，OONI 聯絡當地夥伴之後，確認是那批裝置的時區設錯了。排除委內瑞拉之後，Linux 的異常數字大幅下降，其他平台幾乎不變。設定錯誤就足以產生誤導性的紀錄，不一定出於惡意。

### 作業系統與版本資訊的矛盾

OONI 檢查軟體名稱與平台是否相符，例如 `software_name = ooniprobe-android` 卻標成 iOS。這類 Android 軟體出現在非 Android 平台的量測共有 718 筆，一部分追查到 OONI 團隊成員自己的開發機器，另一部分又是前面那個送中國資料的 `ooniprobe-react-os`。原文也列出幾個陌生的軟體名稱（Vladhog、murakami-ooniprobe、MySorgenia、Dismantle 等），逐一查證來源。許多看起來可疑的資料，多半來自開發過程或第三方 fork，與攻擊無關。

### 對資料使用者的意義

OONI 目前沒有在資料裡找到大量惡意污染，絕大多數異常來自 VPN、設定錯誤、開發機器或非官方分支。防禦機制仍然要做，但目前的威脅不是迫在眉睫的大規模攻擊。

anoni.net 的 OONI 觀測涵蓋率分析建立在同一份公開資料上，源頭沒有被大量污染，分析的基礎就比較穩。四類發現也提醒我們，`probe_cc` 不等於當地實際的連線狀況（ground truth）。VPN 造成的地理錯配、時區設錯這類雜訊本來就存在，做分析時要先濾掉。

## 新的啟發式構想

在既有規則之外，OONI 想再加上幾種更進階的偵測。定位一直是最大的難題，因為 GeoIP 資料庫由 probe 自己查詢，又會過期。考慮中的補強包括向手機作業系統取得行動網路的國碼與電信商代碼（MCC/MNC）、詢問作業系統的定位服務，或改在伺服器端做 IP 與地點的對照。每種做法原文都附了限制，例如伺服器端的對照會被翻牆工具擋在中間、看不到真實 IP，詢問定位權限則可能引起使用者疑慮。另外也想加上網路層與協定層的異常偵測，例如從 TLS 交握的指紋認出中間人設備（像是改寫流量的防毒軟體）。

## 錯誤量測的處置原則

偵測之後是處置，OONI 定了兩條原則。第一，一筆量測最終是否判定為錯誤資料，要經過人工審查，避免自動化規則誤刪正確的資料。第二，除非牽涉使用者隱私，否則絕不回頭修改已經送進來的資料。因為要經過人工把關，處置只能在錯誤資料進入資料管線之後進行。

可用的手段包括封鎖行為異常的假名（pseudonym）、對投稿限流、動態調整某地區某時段可接受的投稿量，或輪換簽發金鑰。假名是匿名憑證系統給一台 probe 的識別，在同一個網路內固定不變，跨網路無法串連，也對應不到任何人的真實身分（原理見下一節）。原文也點出其中的兩難，例如規定只有存在半年以上的 probe 才能投稿，可以擋下 sybil 攻擊（用大量假身分送入資料），也會連帶擋掉正常的新 probe。

## 匿名憑證系統的運作方式 {#credentials}

### 固定 ID 做法的問題

直覺的做法是給每個 probe 一個 ID，再由伺服器端維護白名單。就算 ID 是隨機產生的，只要固定不變就足以辨識出單一 probe，對隱私是災難，而且 probe 換一個新 ID 就能繞過封鎖。匿名憑證系統要解決的核心矛盾，是在不長期儲存個資的前提下，同時做到存取控制與信任評分。

### 區間揭露的憑證

憑證的概念接近酒吧門口的年齡查驗，店員看到一張證明已成年的證件就放行，不需要知道持有人的姓名、住址與生日。OONI 的憑證證明的是 probe 的資歷夠久、投稿數量夠多。

憑證由伺服器簽發，只存在 probe 本地，伺服器不保存，也不會再外傳。憑證用密碼學把 probe 的資歷（age）與投稿數（`msm_count`）編碼進去，而且只證明數值落在某個區間，例如投稿超過 1000 筆、存在超過一週，不透露精確值。用區間取代精確數字是刻意的設計，精確的投稿數幾乎是獨一無二的指紋，會讓 probe 被認出來，粗略的區間才不會洩漏身分。

### 投稿時的零知識證明

投稿時，probe 用憑證產生一段零知識證明（只證明某件事為真、不透露細節的密碼學方法）。伺服器只看到證明本身，看不到底下的真實數值，就能判斷該筆量測是否符合存取規則，例如某個國家、某個 ASN 的 probe 要投稿滿 1000 筆才收。信任分數還會鎖定在特定的國碼與 ASN 組合，一台 probe 在某個網路累積的信譽無法帶到另一個網路使用，用意是防止有人先在門檻低的網路累積憑證，再拿去攻擊別的網路。

一台全新的 probe 一開始資歷淺、投稿數低，許多嚴格的規則都還達不到，只能先持續執行量測。每投一筆，伺服器驗證通過之後回傳一張更新過的憑證，把投稿數加一。時間與量累積夠了，這台 probe 跨過滿一週、滿 1000 筆的門檻，之後送出的量測就能標成 verified。整個過程中，OONI 始終沒有取得它的固定 ID，也沒有存下任何個資。

### 複製憑證與 sybil 攻擊

憑證只存在 probe 本地，複製一百份能否假裝成一百台各有信譽的 probe？關鍵在前面提到的網路內固定。在同一個網路裡，同一份憑證推導出來的假名都相同，複製再多份，仍然被視為同一台 probe，不會變成一百個各自獨立的可信身分。OONI 也坦白承認，光靠憑證無法完全解決 sybil 攻擊，完整的防禦要靠應用層的手段，例如限制新帳號的註冊速率、對每個區域的投稿量設上限。憑證的作用是提高攻擊成本，對手需要先培養一批資歷夠久、送過夠多量測的 probe。

### 三種驗證狀態與長期指標

每筆量測最後標成 verified、unverified 或 failed 三種狀態，資料使用者可以自行決定要採信到什麼程度。部分效果需要長期觀察，OONI 會持續追蹤三類量測的比例變化，用來診斷某次用戶端更新是否讓協定實作出錯，或有舊版 probe 沒有更新。他們也會統計各協定版本的 probe 數量，以及伺服器端驗證一筆量測的耗時，及早發現效能退化。

### 隱私設計的參考價值

如何在不儲存個資的前提下做存取控制與信任評分，是很多系統都會遇到的難題。OONI 用區間揭露、憑證只存本地，並放棄精準封鎖單一 probe 來換取匿名性，這套取捨對關心隱私設計的人是很好的教材，也呼應社群[個人隱私指引研究專題](/join/privacy-guide/)的主題。

## 資料可信度的結論

OONI 的公開資料目前沒有被大量惡意污染，看到的異常多半來自 VPN、時區設錯、開發機器這類無心之過，可以繼續用來理解台灣與各地的封鎖狀況。想深入了解匿名憑證背後的密碼學，OONI 另有兩篇相關文章，一篇整理這套系統的[設計需求](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/)[^2]，一篇[宣布系統的設計與實作](https://ooni.org/post/2025-announcing-ooni-new-anonymous-credential-system/)[^3]，後者的正體中文翻譯見[OONI Probe 匿名憑證系統的設計與實作](/articles/ooni-anonymous-credentials/)。

## 原文十個大節對照

| 原文大節 | 重點 | 關鍵數字或結論 |
|---|---|---|
| Existing metrics and heuristics、Approach | 用既有資料建立偵測基準 | 四個不犧牲隱私的檢查角度 |
| IP geolocation mismatches | probe 回報位置對照真實 IP | 7.41% 對不上，多數是 VPN |
| Measurement volume anomalies | 單一 probe 投稿速率暴增 | 中國 `ooniprobe-react-os` 每秒 3 筆 |
| Timestamp inconsistencies | 量測時間戳前後不一致 | 0.82% 異常，委內瑞拉時區設錯 |
| Probe OS, version metadata | 軟體名稱與平台互相矛盾 | 718 筆，含團隊開發機 |
| New heuristics | 更進階的偵測構想 | MCC/MNC、伺服器端 GeoIP、TLS 指紋 |
| Mitigation strategies | 找到錯誤資料之後的處置 | 人工把關、不回改、限流、防 sybil |
| Naive solution | 固定 ID 做法的問題 | 固定 ID 足以去匿名，換 ID 又能繞過 |
| Anonymous credentials solution | 憑證式信任評分 | 區間揭露、只存本地、沒有固定 ID |
| Future validation | 長期驗證指標 | 追蹤 verified、unverified、failed 的比例 |

## 名詞對照

| 名詞 | 說明 |
|---|---|
| 啟發式（heuristic） | 一組簡單、成本低的判斷規則，不追求完美，先把可疑的量測篩出來 |
| OONI Probe | OONI 的手機與桌面 App，依網站清單逐一連線，回報每個網站在當地能否連線 |
| probe | 執行量測的裝置或程式 |
| `probe_cc` | probe 回報的國碼（country code） |
| `probe_asn` | probe 回報的 ASN |
| ASN | 自治系統編號（Autonomous System Number），一段 IP 位址的管理單位，通常對應一家 ISP 或機構 |
| `msm_count` | 該 probe 累積投稿的量測數（measurement count） |
| check-in 端點 | probe 開始量測前呼叫的 API，會回報自己的國碼與 ASN |
| `web_connectivity` | 網路連線測試，OONI 最常見的測試項目，檢查某個網站在當地能否連線 |
| ground truth | 當地實際的連線狀況，用來對照 probe 回報的資料 |
| sybil 攻擊 | 用大量假身分送入資料、扭曲觀測結果的攻擊 |
| pseudonym（假名） | 匿名憑證下一台 probe 的識別，在同一個地區與 IP 內固定，跨網路無法串連，不是個人身分 ID |
| verified、unverified、failed | 匿名憑證系統給每筆量測的三種信任標記 |

## 相關閱讀

- [OONI Probe 匿名憑證系統的設計與實作](/articles/ooni-anonymous-credentials/)
- [OONI Run v2 使用樣態普查，336 條檢測連結的檢測量分佈](/articles/ooni-run-v2-usage-patterns/)
- [OONI 觀測涵蓋率](/projects/asn-coverage/)
- [OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)
- [什麼是 OONI](docs:tools/what-is-ooni/)
- [台灣 OONI ASN 涵蓋觀測](docs:taiwan/ooni-asn-coverage/)

[^1]: [From Heuristics to Anonymous Credentials: Assessing OONI's Approach to Bad Measurements, OONI 2026-07-06](https://ooni.org/post/2026-faulty-measurements/)
[^2]: [Requirements for OONI's anonymous credentials, OONI](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/)
[^3]: [Announcing OONI's new anonymous credential system, OONI 2026-01-30](https://ooni.org/post/2025-announcing-ooni-new-anonymous-credential-system/)
