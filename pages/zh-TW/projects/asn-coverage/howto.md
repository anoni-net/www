---
title: ASN 觀測資料的擷取與分析
description: OONI 觀測涵蓋率（ASN Coverage）命令列工具的設定與用法，包含 OONI 三種資料入口的取捨、S3 公開資料集的路徑結構、輸出的 CSV 欄位，以及 ASN 覆蓋率的計算方式。
---

[OONI 觀測涵蓋率](/projects/asn-coverage/)（ASN Coverage）提供命令列工具（[`anoni-net/asn-coverage`](https://github.com/anoni-net/asn-coverage)），用來擷取 OONI 的公開資料，計算特定區域內 ASN（自治系統編號）的觀測覆蓋率。為什麼要看 ASN 的覆蓋率，寫在[ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)，工具的設定與用法則整理在本頁。

開始前建議先照[參與開發的環境準備](/join/dev-setup/)建置開發環境。

!!! tip "執行位置"

    以下指令都在 [`anoni-net/asn-coverage`](https://github.com/anoni-net/asn-coverage) 的目錄下執行。第一次使用時先 clone repo 並 `cd` 進目錄，執行 `uv sync` 安裝相依套件，再照下方範例以 `uv run python ooni.py ...` 執行。

## 三種取用路徑

OONI 的觀測資料有三個入口，各自適合的用途差異很大，著手前需先選定：

| 入口 | 適合的情境 | 限制 |
|---|---|---|
| [AWS S3 公開資料集](https://registry.opendata.aws/ooni/) | 批次分析、全量統計、跨時間比對 | 需自行解析，下載量以 GB 計 |
| [OONI API](https://api.ooni.org/api/v1/measurements) | 依條件篩選、取單筆完整測量 | 單次回傳筆數有上限 |
| [OONI Explorer](https://explorer.ooni.org/zh-Hant) | 人工查閱、確認個別測量 | 不適合程式化取用 |

ASN Coverage 用來統計覆蓋率，用不到單筆查詢，所以採用 S3 路徑。單筆查詢與小量篩選的 API 用法見[OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)。

## 程式的統計範圍

`ooni.py` 現階段統計覆蓋率與判定結果的分布，資料的取用範圍有三個限制：

- **只讀 `webconnectivity` 目錄**，同一小時底下其他十幾個測項都沒有納入，`tor`、`telegram`、`signal` 等測項的觀測不會出現在統計中。各測項的量測對象見[OONI 測項速查表](/projects/asn-coverage/ooni-nettests-map/)。
- **每筆測量只取三個欄位**，`probe_asn`、`annotations.network_type` 與 `test_keys.blocking`。證據層的 `queries`、`tcp_connect`、`requests` 都沒有讀取，所以從輸出可以看出哪些 ASN 有人在測、測了幾次、判定結果如何分布，看不到單筆測量的證據內容。
- **只取 `.jsonl.gz`**，跳過同目錄的 `.tar.gz`。

`blocking` 在未觀測到干預時是布林值 `false`，有干預時是字串。程式在計數前把兩種值統一成同一組鍵，沒有判定結果的測量記為 `none`，所以每個 ASN 的判定分布加總一定等於測量筆數。判讀前提見[OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)。

要再往下分析證據層，需要取出那一層的欄位逐筆比對。單純的計數統計無法容納這些資料，儲存方式需要另行設計。

## S3 資料集的目錄結構

Bucket 名稱是 `ooni-data-eu-fra`，位於 `eu-central-1`，公開讀取不需認證憑證。路徑依日期、小時、國碼、測項分成四層：

```text title="路徑結構"
raw/{YYYYMMDD}/{HH}/{國碼}/{測項}/{YYYYMMDDHH}_{國碼}_{測項}.n{編號}.{序號}.jsonl.gz
```

!!! warning "以 UTC 表示的日期與小時"

    路徑中的 `{YYYYMMDD}` 與 `{HH}`，以及後續 CSV 輸出的 `date` 與 `hour` 欄位，全部使用 UTC。程式內部一律以 `arrow.Arrow.utcnow()` 取得時間。分析台灣某個時段的觀測分布時，需要加 8 小時換算，否則圖表會整體偏移。

檔名尾端的 `.n{編號}.{序號}` 是 OONI 內部的批次編號，解析時可忽略。

不必安裝任何工具也能確認目錄內容：

```bash title="台灣單一小時的測項清單"
curl -s "https://ooni-data-eu-fra.s3.eu-central-1.amazonaws.com/?list-type=2&prefix=raw/20260804/00/TW/&delimiter=/" \
  | grep -oE '<Prefix>raw/[^<]+</Prefix>'
```

回應是未斷行的 XML，上例接上 `grep` 只取出目錄名稱。台灣在單一小時內通常有十幾個測項目錄，`webconnectivity` 只是其中之一，同層還有 `tor`、`telegram`、`signal`、`whatsapp`、`dnscheck`、`echcheck`、`openvpn`、`psiphon`、`ndt`、`dash` 等。

每個測項目錄底下，同一批資料有 `.jsonl.gz` 與 `.tar.gz` 兩種封裝。`.jsonl.gz` 解開後一行一筆測量，適合逐行解析，程式讀取的就是 `.jsonl.gz`。以 2026-08-04 台灣的 `webconnectivity` 為例，單一檔案約 10 MB。換算成全國整個月的資料量相當可觀，執行前應先估算頻寬與執行時間。程式以串流處理，原始檔不會寫入磁碟，最後只輸出 CSV。

各欄位的判讀方式見[OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)，判定欄位的含義見[OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)。

## 擷取與分析指令

### 近期資料的回溯

```bash title="最近 36 小時的資料"
uv run python ooni.py lookback --units=36 --loc=TW --frame=hours
```

三個參數都可以省略，預設值與上例相同。`--frame` 設定回溯總長度的單位，可填 `hours`、`days`、`weeks` 等。不論單位為何，資料一律按小時切分。輸出檔名的格式：

- `lookback_{loc}_{YYYYMMDD}_{units}_{frame}.csv`

檔名中的 `{YYYYMMDD}` 是執行當天的 UTC 日期，並非資料涵蓋的區間，實際範圍要看檔案內容。檔案寫入目前的工作目錄。

### 指定區間的資料

```bash title="指定區間的資料"
uv run python ooni.py span --start=2026/08/01 --end=2026/08/03 --loc=TW --chunk=40
```

帶入開始時間（`start`）與結束時間（`end`），可以取得該期間每個小時的資料。`--chunk` 控制同時處理的小時數，預設 `40`，網路或記憶體不足時應調小。輸出檔名的格式：

- `span_{loc}_{開始YYYYMMDD}_{結束YYYYMMDD}.csv`

### 試算表格式的轉換

```bash title="試算表格式的展開"
uv run python ooni.py sheetrow --path=./span_TW_20260801_20260803.csv
```

`sheetrow` 把已擷取的資料展開，方便在試算表中計算。輸出檔名是在原檔名前加上 `rows_`，上例的輸出即 `rows_span_TW_20260801_20260803.csv`。

## 輸出的 CSV 欄位格式

`lookback` 與 `span` 產出的檔案有四個欄位，一列代表一個小時：

| 欄位 | 內容 |
|---|---|
| `loc` | 國碼，例如 `TW` |
| `date` | 日期，格式 `YYYY/MM/DD`，UTC |
| `hour` | 小時，格式 `HH`，UTC |
| `statistics` | 該小時的統計結果，內容是一段 JSON |

`statistics` 內含三份計數：`counts` 依 ASN 統計測量筆數、`network_type` 依連線類型統計、`blocking` 依 ASN 統計判定結果的分布。以 2026-08-04 台灣 `00` 時的實際資料為例，該小時共 551 筆測量：

```json title="statistics 欄位展開"
{"counts": {"AS3462": 300, "AS17716": 100, "AS18419": 100, "AS24158": 51},
 "network_type": {"mobile": 44, "no_internet": 7},
 "blocking": {"AS3462": {"false": 294, "dns": 1, "tcp_ip": 1, "none": 4},
              "AS17716": {"false": 94, "none": 6},
              "AS18419": {"false": 99, "none": 1},
              "AS24158": {"false": 51}}}
```

`counts` 與 `blocking` 的加總逐 ASN 相等，`network_type` 的加總則不會相符。`network_type` 由 Probe 自行標記，行動版 App 通常會寫入，CLI 與桌面版多半不會。上例 551 筆中只有 51 筆帶標記，程式會跳過未標記的測量。其中 `no_internet` 代表 Probe 在測量當下偵測到自身沒有連線。標記涵蓋率不到一成，適合觀察趨勢，不適合作為行動與固網的比例依據。

`blocking` 中的 `none` 代表該筆沒有判定結果，缺少 `test_keys` 或 `blocking` 為 `null` 的測量都歸入此類。上例 551 筆中有 11 筆屬於 `none`，佔比不高，但每個 ASN 都有。計算異常率前，要先決定這些測量是否納入分母。

巢狀 JSON 不易在試算表中計算，`sheetrow` 把它攤平成一列一個 ASN：

| `loc` | `date` | `hour` | `asn` | `count` | `anomaly` | `blocking_false` | `blocking_dns` | `blocking_tcp_ip` |
|---|---|---|---|---|---|---|---|---|
| `TW` | `2026/08/04` | `00` | `AS3462` | `300` | `2` | `294` | `1` | `1` |
| `TW` | `2026/08/04` | `00` | `AS17716` | `100` | `0` | `94` | `0` | `0` |

上表受限於版面只列出前幾欄，完整欄位還有 `blocking_http_failure`、`blocking_http_diff`、`blocking_none` 與 `blocking_other`。`anomaly` 是四種干預類型的加總，可直接在試算表中作為分子。`blocking_other` 收錄 `ts-017` 尚未定義的值，正常情況下應為 `0`，出現非零值代表上游新增了判定類型。

實際分析輸出的試算表範例（2023-09 至 2023-12）：

[<i data-icon="google-spreadsheet"></i> 20230901-20231204-TW](https://docs.google.com/spreadsheets/d/1lMDsqX8Oa3GKW68y8TuFeKQW2nKM7X0u4z-RopfJIaA/){ .btn .solid }

## ASN 覆蓋率的計算

計算覆蓋率需要兩個數字：觀測資料中出現過的不重複 ASN 數，以及該區域登記在案的 ASN 總數。前者用樞紐分析從上一節攤平後的 CSV 取得，後者用 `ripe.py` 向 RIPE NCC 查詢：

```bash title="區域內的全量 ASN 清單"
uv run python ripe.py save --loc=TW
```

輸出檔名為 `asns_{YYYYMMDDTHH}.csv`，六個欄位分別是 `no`、`location`、`org_id`、`registrar`、`reserved`、`name`。

!!! warning "兩份資料的 ASN 格式差異"

    `ripe.py` 輸出的 `no` 欄位是純數字（`3462`），OONI 資料的 `probe_asn` 帶 `AS` 前綴（`AS3462`）。直接用 VLOOKUP 比對會全部落空，比對前要先在其中一邊補上或去除 `AS`，統一兩邊的格式。

兩個數字備齊後即可計算：

```text title="覆蓋率算式"
覆蓋率 = 觀測資料中出現的不重複 ASN 數 ÷ 該區域登記的 ASN 總數
```

以社群 2023-12 的分析為例（見[ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)），台灣當時約有 437 組 ASN，觀測資料涵蓋的不重複 ASN 佔 7.32%。同一算式也可以套用在近期的區間，對照覆蓋率是否改善。

## miniooni 與 OONI Run v2 清單 {#miniooni}

OONI Probe 的命令列版本 [miniooni](https://github.com/ooni/probe-cli) 可以在伺服器、研究腳本或排程裡執行 OONI Run v2 清單。`-i` 參數要給 API 的 descriptor 網址，給 `run.ooni.org` 的網頁網址會失敗：

```bash
# 錯誤：取得的是 HTML，JSON 解析失敗
miniooni oonirun -i https://run.ooni.org/v2/10328

# 正確：指向 API 的 descriptor JSON
miniooni oonirun -i https://api.ooni.org/api/v2/oonirun/links/10328
```

miniooni 會把 `-i` 的網址當成 descriptor 端點直接 GET，`run.ooni.org/v2/<ID>` 是給瀏覽器的網頁，回應是 HTML。descriptor 的網址格式是 `https://api.ooni.org/api/v2/oonirun/links/<LINK_ID>`，`<LINK_ID>` 取自網頁網址的最後一段，社群維運的清單是 `10328`。桌面版與行動 App 由作業系統把網頁網址交給 OONI Probe 處理，不受影響。上游的程式裡已有 [TODO 註記](https://github.com/ooni/probe-cli/blob/master/internal/oonirun/link.go)，之後可能會改成自動轉換。

## 相關閱讀

- [OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)：一筆測量的各個欄位與判讀方式
- [OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)：`blocking` 等判定欄位的含義
- [OONI 測項速查表](/projects/asn-coverage/ooni-nettests-map/)：各測項的量測對象
- [ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)：台灣各 ASN 的觀測覆蓋率分析，覆蓋率算式的範例數字取自該頁 2023-12 的分析
- [參與開發的環境準備](/join/dev-setup/)：參與專案開發前的環境設定
- [如何參與與認領主題](/join/)：加入社群、認領年度主題的方式
