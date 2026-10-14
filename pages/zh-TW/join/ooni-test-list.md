---
title: OONI 網站檢測清單的維護
description: OONI Probe 檢測網站時依據的 Citizen Lab 清單，包含收錄分類、OONI 依分類排定檢測頻率的方式、台灣 tw.csv 的現況與參與維護的方式。
---

OONI Probe 執行網站連線測試時，照著一份事前列好的網址清單逐一檢查。清單收錄哪些網站、分類是否正確、多久更新一次，決定了後續的觀測能看到什麼，[ASN 多樣性](/projects/asn-coverage/asn-diversity/)這類分析也受同樣的限制。清單過時的國家看起來像沒有審查，原因可能只是會被封鎖的網站沒有人測。台灣的清單需要重新整理，維護工作不必寫程式。

清單由 [Citizen Lab](https://citizenlab.ca/) 的 [test-lists](https://github.com/citizenlab/test-lists) 專案管理，分成全球（global）與各國（local）兩種。全球清單以英文網站為主。各國清單由當地社群協助蒐集，收錄當地語言的網站與當地關注的主題，有網路審查的國家也會收錄已知被封鎖的網站，方便持續觀測。

收錄標準粗分為四大主題（CSV 裡實際用約 30 個細項分類標記）：

1. **政治**：與現任政府立場不同的網站，也包含人權、言論自由、少數族群權利、宗教運動等延伸主題。
2. **社會**：性別、賭博、非法藥物、酒精，以及其他在當地被視為敏感的議題。
3. **衝突與安全**：武裝衝突、邊界爭議、分裂運動、激進團體相關的內容。
4. **網際網路工具**：電子郵件、雲端空間、搜尋、翻譯、網路電話（VoIP）、規避審查工具等服務。

## 分類與檢測頻率

四大分類除了整理用途，也決定每個網址被測到的頻率。OONI Probe 取得的清單是 OONI API 排序過的結果，並非直接讀取 CSV。排序邏輯寫在 [`prio.py`](https://github.com/ooni/backend/blob/master/api/ooniapi/prio.py)，分兩段計算。

第一段算出每個網址的優先權（priority）。OONI 維護一組規則，每條規則有四個比對欄位：分類、網域、完整網址、國家代碼，`*` 代表不限。命中的規則全部相加，不互相取代。全域預設規則 `*/*/*/*` 給 50，分類規則再疊加上去。歸在新聞媒體（`NEWS`）的網址優先權因此是 `50 + 100 = 150`，歸在電子商務（`COMM`）的是 `50 + 20 = 70`。

目前的分類加權（實際優先權是加上基底 50 之後的值）：

| 加權 | 分類 | 實際優先權 |
|---:|---|---:|
| +120 | `GRP` 社群網路 | 170 |
| +100 | `ANON` 匿名與規避工具、`HUMR` 人權、`LGBT`、`NEWS` 新聞媒體、`POLR` 政治批評 | 150 |
| +80 | `COMT` 通訊工具、`MMED` 媒體分享、`PUBH` 公共衛生、`SRCH` 搜尋引擎 | 130 |
| +60 | `ENV` 環境、`HOST` 主機與部落格、`REL` 宗教、`XED` 性教育 | 110 |
| +40 | `CULTR` 文化、`FILE` 檔案分享、`GOVT` 政府、`IGO` 國際組織 | 90 |
| +30 | `ALDR` 酒精與藥物、`DATE` 交友、`GMB` 賭博、`HATE` 仇恨言論、`MILX` 武裝團體、`PORN`、`PROV` 暴露服飾 | 80 |
| +20 | `COMM` 電子商務、`CTRL` 內容管制、`ECON` 經濟、`GAME` 遊戲、`HACK` 駭客工具、`MISC` 未分類 | 70 |

社群平台與言論類的加權最高，商業與娛樂最低，兩端相差 2.4 倍，有落差但不到一個數量級。

第二段把優先權除以近期的測量次數，得到實際的排序鍵：

```
weight = priority / max(msmt_cnt, 0.1)
```

`msmt_cnt` 是該網址在本週與上週被測量的次數，範圍限定在同一個國家，probe 有回報 ASN 時則限定在同一個 ASN。測得越多，權重下降得越快，網址往後排，其他網址隨之往前。

排序會隨測量次數變動，優先權決定一個網址能分到多少檢測，測量次數決定已經用掉多少。加權高的分類換來的是測過之後較快排回前面，並非永遠佔住前排。

## 突發事件的專屬規則

規則表除了分類加權，還有兩種用法。第一種是把單一目標推到清單最前面，截至 2026-09 的設定如下：

| 目標 | 範圍 | 優先權 |
|---|---|---:|
| `www.aljazeera.net` | 以色列 | `9999999` |
| `orda.kz` | 哈薩克 | `99999` |
| `eltoque.com` | 古巴 | `6969` |
| Twitter、Facebook、Instagram、YouTube 四個網址 | 全球 | `69999` |

優先權遠高於分類加權的量級，目標因此在清單裡幾乎固定排在第一位，通常對應正在發生或剛發生的封鎖事件。

第二種是把優先權設成負值來排除網址，程式遇到優先權小於等於零的項目直接跳過，不發給 probe。目前唯一的一組負值規則在阿富汗，把酒精與藥物、交友、賭博、仇恨言論、`LGBT`、武裝團體、`PORN`、性教育八個分類設為 `-9999`，用意是保護執行測量的人，避免網路紀錄裡出現在當地可能帶來危險的內容。

同一份規則表裡沒有台灣的國家層級規則，`tw.csv` 每一則的優先權都只有「50 加上分類加權」，分類因此是唯一能影響檢測頻率的欄位。歸錯分類不會出現任何錯誤訊息，只會讓網址被測得比應有的頻率少或多。提交清單修正時，分類判斷的價值跟找到一個值得收錄的網站一樣大。

完整規則表可以從 OONI API 的 [`url-priorities/list`](https://api.ooni.io/api/_/url-priorities/list) 端點查詢，設計背景見 OONI 的 [Building a smart URL list system](https://ooni.org/post/ooni-smart-url-list-system/)。

## tw.csv 的現況

台灣的清單 [`tw.csv`](https://github.com/citizenlab/test-lists/blob/master/lists/tw.csv) 共有 466 則，其中 361 則在 2017 年加入，之後多年缺乏維護。不少網站已停止營運或換了網址，也有 245 則仍以 `http://` 開頭（2026-10 查核）。

!!! note "http:// 與 https://"

    有些網站不會用 [`301 Moved Permanently`](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Status/301) 或 [`308 Permanent Redirect`](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Status/308) 把 `http://` 轉址到 `https://`，造成 OONI 檢測誤判。TLS 憑證現在容易取得，加密傳輸也是網站的基本配備，清單上的網址應該預設使用 `https://`。

## 既有項目的檢查

第一步是逐一檢查 [`tw.csv`](https://github.com/citizenlab/test-lists/blob/master/lists/tw.csv) 上的網站，標記「需更新」或「可棄用」，再提交 pull request 到 [citizenlab/test-lists](https://github.com/citizenlab/test-lists)。同樣的檢查方式也適用於其他國家的 `lists/<國碼>.csv`。

!!! info "PR #1444 與之後的做法"

    社群在 2023-09-28 提交過一份[檢測名單修正](https://github.com/citizenlab/test-lists/pull/1444)，一次改動約 100 個國家的清單檔，難以審查。PR #1444 在 2026-09 關閉，沒有合併。之後的 PR 只改 `lists/tw.csv`，每次的範圍縮小到可以單獨審查，逐則確認失效網址與 `http://` 網址。網站換了網域的，優先修改網址，不直接刪除。

## 新增網站

2017 年之後規模最大的一次新增在 2026-09，[PR #2267](https://github.com/citizenlab/test-lists/pull/2267) 補上 74 個台灣的網站並已合併，其中政治批評（`POLR`）的 20 則最多。新增的候選依前面的四大分類篩選，篩選標準社群還在持續討論。

## 參與方式

清單維護適合新貢獻者入門，不需要寫程式，需要的是：

- **網路使用者的觀察力**：哪些網站在台灣被討論、哪些近期關閉、哪些是新出現值得納入的對象
- **判斷分類的能力**：對照四大分類與細項分類歸類
- **基本的 GitHub 操作**：fork、修改 CSV、提交 PR

依想參與的部分，從下列頁面開始：

- 清單維護：到 Matrix 的 anoni-net 公開空間表達意願，會有夥伴協助分配要檢查的範圍（加入方式見[參與](/join/)）
- 觀測資料的分析：[ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)、[ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)
- 測量資料的判讀：[OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)、[OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)
- 清單以外的測項：[OONI 測項速查表](/projects/asn-coverage/ooni-nettests-map/)

## 相關閱讀

- [參與開發的環境準備](/join/dev-setup/)：執行社群的分析工具前需要的開發環境
- [Tor 中繼節點觀測](/projects/pulse/)：社群的另一個觀測專案，每小時收集台灣與鄰近地區的 Tor 中繼節點資料
- [什麼是 OONI](docs:tools/what-is-ooni/)：OONI 的運作方式，以及適合與不適合的用途
- [網路自由為什麼重要](docs:basics/internet-freedom/)：網路審查與網路自由的背景
