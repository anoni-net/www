---
title: AI 助理的 Tor 節點查詢
description: 社群開發並自架的 Tor 中繼節點查詢服務。在雲端 AI 助理加上一個網址，不必寫程式就能用中文查詢各地的 Tor 節點數、頻寬與所在的電信網路。
lead: 在雲端 AI 助理貼上一個網址，就能用中文查詢各地的 Tor 中繼節點。
---

台灣現在有幾個運作中的 Tor 節點、半年來增加還是減少、節點分布在哪幾家電信業者，答案都在 Tor Project 的公開資料裡，過去需要自行寫程式抓取、計算。在 AI 助理（例如 claude.ai）接上 onionoo MCP 之後，輸入一句「台灣現在有幾個能用的 Tor 節點？」，AI 助理會查詢資料、計算，整理成一份可讀的報告。

前半頁寫給需要查資料、但不寫程式的讀者，例如記者、公民團體與事實查核者，照著步驟即可上手。後半的[程式呼叫與自架](#程式呼叫與自架)寫給要用程式呼叫服務，或想自行架設一份的工程師。

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-tw-summary-result.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-tw-summary-result.png"
            alt="Claude Desktop 針對「整理台灣 Tor 中繼節點現況」提問產生的彙整報告，顯示 13 個 running relay、總頻寬約 39.2 MiB/s（約 329 Mbps）、consensus weight 8,570，並列出前 5 大 ASN 表格（AS3462 中華電信 10 個、AS1659 TANet、AS9416 和信超媒體、AS18041 Taiwan Digital Streaming 各 1 個）"
            title="AI 助理整理的台灣 Tor 中繼節點現況報告"
            class="shot">
    </a>
    <figcaption>用一句中文提問，AI 助理回傳整理好的報告，包含運作中節點數、總頻寬與前五大電信網路。數值來自 Tor Project 的官方資料，是查詢當下的快照，會隨時間變動。</figcaption>
</figure>

## 可以回答的問題

- **事實查核**：遇到「台灣的 Tor 量能很低」這類說法時，可以當場查詢運作中的節點數、總頻寬，以及與過去某個時間點相比的變化，取得能對照、能引用的數字。
- **新聞報導**：報導某個國家的網路封鎖或翻牆基礎建設時，可以盤點當地有多少 Tor 中繼節點、出口節點（流量離開 Tor、連回一般網站的最後一個節點）集中在哪些網路供應商，再做跨國比較。
- **公民團體與倡議**：盤點某個地區的節點分散在幾家電信業者（越分散越不容易被一次切斷），當作數位韌性的觀察指標。

## 雲端 AI 助理的接法

不寫程式的話，把服務接到平常使用的雲端 AI 助理最簡便，不需要安裝軟體或編輯設定檔。在助理的設定裡新增一個自訂連接器（custom connector），貼上以下網址：

`https://onionoo.anoni.net/mcp`

亞太地區常見的三家雲端 AI 服務，目前的接法與門檻各不相同：

<div class="tbl-names" markdown>

| 雲端 AI | App 內貼網址 | 接法 |
|---|---|---|
| **Claude（claude.ai）** | 可以，免費方案也適用（限 1 個連接器） | 設定 → Connectors（連接器）→ Add custom connector，貼上網址 |
| **ChatGPT** | 可以，需付費方案（Plus 以上，免費版不支援） | 設定 → Apps → 進階設定 → 開啟「Developer Mode（開發者模式）」→ 新增自訂 connector，貼上網址 |
| **Google Gemini** | 消費版聊天 App 目前不支援 | 需透過 Gemini CLI（需編寫設定檔）或 Gemini Enterprise（需 Google Cloud 管理權限），屬於工程或企業的用法，見[程式呼叫與自架](#程式呼叫與自架) |

</div>

各家的方案門檻與設定位置可能變動，以官方說明為準（Claude[^connector]、ChatGPT[^chatgpt]、Gemini[^gemini]）。

以門檻最低的 Claude 為例，完整步驟如下：

1. 開啟 [claude.ai](https://claude.ai)（網頁版或桌面版皆可）並登入。
2. 進入設定，找到「Connectors（連接器）」，點選「Add custom connector（新增自訂連接器）」。
3. 名稱填 `onionoo`，網址貼上 `https://onionoo.anoni.net/mcp`，按下「Add」。
4. 回到 AI 助理開啟新對話，直接用中文提問（例句見下一節）。

使用公司或團隊帳號時，通常只有帳號管理者（Owner）能新增連接器，需請管理者代為新增。

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-claude-desktop.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-claude-desktop.png"
            alt="Claude Desktop 的 Connectors 設定頁，onionoo 顯示為 CUSTOM connector、連到 https://onionoo.anoni.net/mcp，工具清單列出 aggregate_as、aggregate_countries、aggregate_flags、get_bandwidth、get_clients、get_details、get_summary、get_uptime、get_weights 等工具"
            title="貼上網址後的 Connectors 設定頁"
            class="shot">
    </a>
    <figcaption>新增完成後，Connectors 頁會列出 <code>onionoo</code> 自訂連接器與它提供的查詢工具。使用時不必指定工具，用中文提問，AI 助理會自行選用。</figcaption>
</figure>

## 可以直接複製的問句

以下三句可以直接複製，再依需要換成想查的國家或地區。

**可引用的數字（事實查核）**

> 台灣現在有幾個運作中的 Tor 中繼節點？總頻寬大約多少？幫我整理成一句我能直接引用的話。

**跨國比較（新聞報導）**

> 幫我比較台灣、香港、日本目前運作中的 Tor 中繼節點數量與總頻寬，做成一個表格。

**節點的分散程度（公民團體）**

> 台灣的 Tor 中繼節點分別由哪些電信業者（ASN）承載？前五大是哪些、各有幾個？

得到答案後，可以追問「這些數字是什麼時候的？」、「資料來源是哪裡？」，請 AI 助理交代出處。

??? info "名詞說明"

    第一次看到這些詞時，知道大概的意思即可，需要時也可以請 AI 助理解釋。

    - **中繼節點（relay）**：Tor 網路裡負責轉送流量的伺服器，由志工架設，全球近萬個。連上 Tor 時，流量會依序經過好幾個中繼節點。
    - **橋接（bridge）**：沒有公開列出的中繼節點，供無法連上一般 Tor 節點（例如遭到封鎖）的使用者繞道連線。
    - **出口節點（exit）**：流量離開 Tor 網路、連回一般網站時經過的最後一個節點。
    - **ASN（自治系統編號）**：電信業者或網路供應商在網際網路上的編號。節點所在的 ASN 代表承載它的業者。
    - **consensus weight（共識權重）**：Tor 分配流量時給每個節點的分量，大致反映節點能承擔的流量，數字越大，分到的流量越多。

## 數字的可靠度與引用方式

查到的數字可以引用，底層資料來自 Tor Project 官方維護的 [Onionoo](https://metrics.torproject.org/onionoo.html)（Tor 中繼節點的公開資料服務）。onionoo.anoni.net 只把資料轉成較易讀的格式，不另外儲存或加工數值。

- **交叉核對**：同樣的節點可以在 Tor Project 官方的 [Relay Search](https://metrics.torproject.org/rs.html) 查到，兩邊的數字應該一致。
- **時效**：為了減輕上游負擔，服務會把回應快取約 5 分鐘。Onionoo 本身也是定期更新，取得的數字是某個時間點的快照，不是即時值，引用時要一併記下查詢時間。
- **引用寫法**：可以寫成「資料來源：Tor Project Onionoo（經 anoni.net onionoo 服務查詢，查詢時間 2026-06-09）」。

---

## 程式呼叫與自架

`onionoo-fastapi` 把 Onionoo API 包裝成兩種介面，讓工具與 AI 代理（agent）更容易使用：

- **語義化 HTTP API**（附 OpenAPI / Swagger）：把 Onionoo 的短欄位（`n`、`f`、`a`、`r` 等）轉成可讀的 `nickname`、`fingerprint`、`addresses`、`running`，並補上一份完整的 OpenAPI 規格。
- **[Model Context Protocol（MCP）](https://modelcontextprotocol.io/) 伺服器**：讓 Claude Desktop、Cursor、Claude Code 等支援 MCP 的客戶端以工具呼叫（tool call）查詢 Tor 中繼節點，不需要撰寫 HTTP 請求的程式碼。

服務本身**不儲存**任何 Onionoo 資料，只負責轉發與重新包裝回應，上游資料來自 Tor Project 的 [Onionoo 服務](https://onionoo.torproject.org)。

- **服務網址**：<https://onionoo.anoni.net>
- **Swagger UI**：<https://onionoo.anoni.net/docs>
- **MCP 端點**：`https://onionoo.anoni.net/mcp`（Streamable HTTP）
- **原始碼**：<https://github.com/anoni-net/onionoo-fastapi>（MIT 授權，目前版本 v1.2.0）

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-swagger.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-swagger.png"
            alt="onionoo.anoni.net 的 Swagger UI，顯示 Onionoo FastAPI Proxy v1.0.0，列出 /healthz、/metrics 與 /v1/summary、/v1/details、/v1/bandwidth、/v1/weights、/v1/clients 等端點"
            title="onionoo.anoni.net 的 Swagger UI"
            class="shot">
    </a>
    <figcaption><code>onionoo.anoni.net/docs</code> 的 Swagger UI，每個 <code>/v1/*</code> 端點都附完整 schema，可以用「Try it out」即時測試。</figcaption>
</figure>

### 服務的緣起

Onionoo 的規格完整，但**沒有 OpenAPI 描述**，欄位名稱也為了傳輸效率縮成短碼。工程師讀文件、自行撰寫 client 時不成問題，AI 代理與第三方工具使用起來就比較困難：

- 沒有 OpenAPI，Swagger UI、Postman 與 code generator 就無法自動讀取規格。
- 短欄位名稱容易讓語言模型誤判，例如分不清 `r` 是 `relay` 還是 `running`。
- 一個問題往往要組合好幾個端點（`/details` 加 `/uptime` 加 `/bandwidth`），AI 代理每次重新拼湊，容易出錯。

`onionoo-fastapi` 補上 OpenAPI 規格、改用語義化欄位，並把常見任務包成單一的 MCP 工具呼叫，例如查詢某個中繼節點目前的健康狀況，一個工具就能完成。

### API 與 MCP 的差別

**API（Application Programming Interface，應用程式介面）** 讓程式之間可以互相查詢資料。Onionoo 就是一個 API，送出一個 HTTP 請求（例如查詢台灣所有 running 的 relay），會收到一份 JSON。規格寫給工程師閱讀，回傳的是原始資料，適合已經知道要問什麼的情境。

**MCP（Model Context Protocol，模型上下文協定）** 是 Anthropic 在 2024 年提出的開放協定，定義 AI 模型呼叫外部工具的標準格式。現有的 API 包裝成 MCP server 之後，支援 MCP 的 AI 代理與客戶端都能直接接上，由模型讀取工具清單，自行決定何時呼叫哪個工具。每出現一個新的客戶端，也不必重做一次整合。

資料探勘的初期透過 MCP 提問，不必先學會這份資料的 schema，由 AI 助理做初步查詢與整理，讀完報告再決定下一步。需要重複執行的查詢，或要進入正式分析時，再改用 API 撰寫腳本，兩種方式可以並用。

### MCP 伺服器的設定檔

客戶端以設定檔連接時（不經過前半頁的 Connectors 介面），在 `mcpServers` 區塊加上：

```json
{
  "mcpServers": {
    "onionoo": {
      "type": "http",
      "url": "https://onionoo.anoni.net/mcp"
    }
  }
}
```

存檔並重新啟動客戶端後，工具清單會出現 `onionoo` 這組工具。

要在本機執行、不依賴遠端服務時，改用 stdio transport：

```json
{
  "mcpServers": {
    "onionoo": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/anoni-net/onionoo-fastapi", "onionoo-mcp"]
    }
  }
}
```

需先安裝 [`uv`](https://docs.astral.sh/uv/)（macOS 可用 `brew install uv`，Linux 見官方文件）。

Gemini CLI 同樣讀取 `mcpServers` 設定（位於它的 settings.json），格式與上面相近，填入同一個遠端網址即可。消費版的 Gemini 聊天 App 目前沒有貼上網址連接遠端 MCP 的入口，需等官方支援。

### HTTP API 的呼叫方式

每個端點都回傳語義化的 JSON，並以 `_meta` 標示快取狀態：

```bash
# 查詢 moria1 的詳細資訊，只回傳 nickname 與 fingerprint
curl -s 'https://onionoo.anoni.net/v1/details?search=moria&fields=nickname,fingerprint' | jq .

# 列出台灣的 relay，依 consensus weight 排序
curl -s 'https://onionoo.anoni.net/v1/details?country=tw&running=true&order=-consensus_weight&limit=5' | jq .

# 依國家彙整目前 running 的 relay 數量
curl -s 'https://onionoo.anoni.net/v1/aggregate/countries?running=true' | jq .
```

完整的端點、查詢參數與回應欄位見 [Swagger UI](https://onionoo.anoni.net/docs)，查詢參數沿用 Onionoo 的[官方規格](https://metrics.torproject.org/onionoo.html)。

### Docker 自架

要自行架設一份（例如架在 .onion 服務、內網或實驗環境）時：

```bash
git clone https://github.com/anoni-net/onionoo-fastapi
cd onionoo-fastapi
docker compose up -d --build
```

預設監聽 `8000` 埠，OpenAPI 文件在 `http://localhost:8000/docs`，MCP 端點在 `http://localhost:8000/mcp`。

常用設定（環境變數）：

| 變數 | 用途 | 預設 |
|---|---|---|
| `ONIONOO_BASE_URL` | 上游 Onionoo 位址 | `https://onionoo.torproject.org` |
| `CACHE_MAXSIZE` / `CACHE_DEFAULT_TTL_SECONDS` | 記憶體快取大小 / TTL | `128` / `300` 秒 |
| `RATE_LIMIT_ENABLED` / `RATE_LIMIT_PER_MINUTE` | 是否啟用 IP 限流 | `false` / `120` |
| `CORS_ALLOW_ORIGINS` | 允許跨來源請求的網域清單，逗號分隔，設成空字串即關閉（1.0.0 的舊名 `CORS_ALLOWED_ORIGINS` 仍可使用） | `https://anoni.net`、文件站的 onion 鏡像與本機預覽 |
| `LOG_FORMAT` | `json` 或 `console` | `json` |
| `METRICS_ENABLED` | 是否啟用 `/metrics`（Prometheus 格式） | `true` |

完整設定清單見 [README](https://github.com/anoni-net/onionoo-fastapi#configuration)。

### MCP 工具一覽

任務導向的工具由 stdio transport 提供，建議代理使用：

| 工具 | 用途 |
|---|---|
| `find_relay(query)` | 自由文字查詢，自動判斷輸入是 40 碼指紋、AS 號、IP，或暱稱子字串 |
| `get_relay_health(fingerprint)` | 合併 details、uptime、bandwidth 三個端點，產生一份健康度快照 |
| `top_relays_by_bandwidth(country?, flag?, limit)` | 依 consensus weight 取前 N 名，可選國家或旗標過濾 |
| `compare_relays(fingerprints)` | 平行取得多個 fingerprint 的 details 並排比較 |
| `country_summary(country)` | 單一國家的 running 數量、總頻寬、旗標分布 |
| `aggregate_relays(group_by, running, top)` | 在伺服器端依 country、AS 或 flag 做 group-by |

對應 Onionoo 原生端點的低階透傳工具，兩種 transport 都有提供，名稱與參數不同。Streamable HTTP 端是 `get_summary`、`get_details`、`get_bandwidth`、`get_weights`、`get_clients`、`get_uptime`，查詢參數逐一列為工具參數，回傳語義化的 JSON。stdio 端是 `onionoo_summary`、`onionoo_details` 等同樣六個工具，接受一個 `params` dict，回傳 Onionoo 的原始回應。

> Streamable HTTP 的 `/mcp` 提供六個低階工具加上三個 aggregate（countries、as、flags），任務導向工具與整合的 `aggregate_relays` 則由 stdio 端提供。兩種 transport 可以同時使用。

### 台灣 Tor 中繼節點的盤點範例

onionoo MCP 接上 Claude Desktop 或 Claude Code 之後，可以直接提問：

> 「幫我整理一份台灣 Tor 中繼節點現況：總共多少個 running、總頻寬、前五大 ASN，順便挑出 consensus weight 最高的三個 relay，告訴我它們的 nickname 與所在 AS。」

代理會把問題拆成幾個 MCP 工具呼叫，再把結果彙整成一份報告（HTTP transport 通常用 `aggregate_countries` 加 `get_details`，stdio transport 另有 `country_summary`、`aggregate_relays`、`top_relays_by_bandwidth` 等任務導向工具）。以往這類查詢需要手動組合 Onionoo 參數、合併 JSON，現在一句話即可完成。

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-tool-use-detail.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-tool-use-detail.png"
            alt="Claude Opus 4.7 思考過程的截圖：先說「我要找臺灣的 relay 資訊」、列出可能工具、然後決定先呼叫 aggregate_countries 找台灣那一列、再用 get_details 抓 country=tw 的 AS 資訊、最後依 consensus weight 拉前三名。可以看到 aggregate_countries 這個工具呼叫已展開、回傳 Result"
            title="Claude Opus 4.7 的工具呼叫展開過程"
            class="shot">
    </a>
    <figcaption>展開模型的推理過程，可以逐步看到代理打算查詢的內容、選用的工具，以及結果回傳後的下一步。推理文字之間穿插實際的 <code>aggregate_countries</code>、<code>get_details</code> 工具呼叫，方便除錯或調整 prompt。</figcaption>
</figure>

### 觀測指標與運維

- `/healthz`：靜態存活檢查，不連線上游。
- `/healthz/ready`：嘗試連線 Onionoo（結果會快取），回傳 200 表示上游可以連線，503 表示無法連線。
- `/metrics`：Prometheus 格式，含快取命中率（`onionoo_cache_hits_total` 與 `_misses_total`）、上游延遲（`onionoo_upstream_seconds`）與錯誤率。
- 每個請求都帶有 `X-Request-ID`，可以對照 log 與回應 header，方便除錯。

## 參與與貢獻

- **回報問題與建議**：[onionoo-fastapi 的 GitHub issues](https://github.com/anoni-net/onionoo-fastapi/issues)
- **架設 Tor relay**：見[Tor Relay 架設指南](/join/setup-tor-relay/)，區域內中繼節點的觀測數字見[Tor 中繼節點觀測](/projects/pulse/)。
- **出國前評估**：[出國前數位安全：用 AI 自助產生目的地概況](docs:scenarios/travel-ai-briefing/)，記者與公民團體出國前查詢目的地的 Tor 中繼節點狀況時，接上 onionoo MCP 可以取得能引用的 Onionoo 數字。
- **延伸閱讀**：[什麼是 Tor](docs:tools/what-is-tor/)、[ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)。

服務目前的版本是 v1.2.0，以 MIT 授權釋出。歡迎提出 issue、PR，也歡迎在 Matrix 一起討論接下來要補上哪些任務導向工具。

[^connector]: [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) - Claude Help Center（自訂連接器在免費、Pro、Max、Team、Enterprise 方案皆可使用，免費方案限一個）。

[^chatgpt]: [Developer mode — apps and full MCP connectors in ChatGPT (beta)](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta) - OpenAI Help Center（自訂 MCP connector 需在 Plus、Pro、Business、Enterprise、Edu 方案開啟 Developer Mode，免費版不支援）。

[^gemini]: [Set up your custom MCP server data store](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server) - Gemini Enterprise（Google Cloud）。消費版 Gemini 聊天 App 尚未提供在介面內貼網址接遠端 MCP 的功能，開發端可用 [Gemini CLI](https://geminicli.com/docs/tools/mcp-server/) 的 `mcpServers` 設定。
