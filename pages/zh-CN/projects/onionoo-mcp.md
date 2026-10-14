---
title: AI 助手的 Tor 节点查询
description: 社区开发并自架的 Tor 中继节点查询服务。在云端 AI 助手加上一个网址，不必写代码就能用中文查询各地的 Tor 节点数、带宽与所在的电信网络。
lead: 在云端 AI 助手贴上一个网址，就能用中文查询各地的 Tor 中继节点。
---

台湾现在有几个运行中的 Tor 节点、半年来增加还是减少、节点分布在哪几家电信运营商，答案都在 Tor Project 的公开数据里，过去需要自行写代码抓取、计算。在 AI 助手（例如 claude.ai）接上 onionoo MCP 之后，输入一句「台湾现在有几个能用的 Tor 节点？」，AI 助手会查询数据、计算，整理成一份可读的报告。

前半页写给需要查数据、但不写代码的读者，例如记者、公民团体与事实核查者，照着步骤即可上手。后半的[代码调用与自架](#代码调用与自架)写给要用代码调用服务，或想自行架设一份的工程师。

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-tw-summary-result.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-tw-summary-result.png"
            alt="Claude Desktop 针对「整理台湾 Tor 中继节点现况」提问生成的汇总报告，显示 13 个 running relay、总带宽约 39.2 MiB/s（约 329 Mbps）、consensus weight 8,570，并列出前 5 大 ASN 表格（AS3462 中华电信 10 个、AS1659 TANet、AS9416 和信超媒体、AS18041 Taiwan Digital Streaming 各 1 个）"
            title="AI 助手整理的台湾 Tor 中继节点现况报告"
            class="shot">
    </a>
    <figcaption>用一句中文提问，AI 助手返回整理好的报告，包含运行中节点数、总带宽与前五大电信网络。数值来自 Tor Project 的官方数据，是查询当下的快照，会随时间变动。</figcaption>
</figure>

## 可以回答的问题

- **事实核查**：遇到「台湾的 Tor 量能很低」这类说法时，可以当场查询运行中的节点数、总带宽，以及与过去某个时间点相比的变化，取得能对照、能引用的数字。
- **新闻报道**：报道某个国家的网络封锁或翻墙基础建设时，可以盘点当地有多少 Tor 中继节点、出口节点（流量离开 Tor、连回普通网站的最后一个节点）集中在哪些网络运营商，再做跨国比较。
- **公民团体与倡议**：盘点某个地区的节点分散在几家电信运营商（越分散越不容易被一次切断），当作数字韧性的观察指标。

## 云端 AI 助手的接法

不写代码的话，把服务接到平常使用的云端 AI 助手最简便，不需要安装软件或编辑配置文件。在助手的设置里新增一个自定义连接器（custom connector），贴上以下网址：

`https://onionoo.anoni.net/mcp`

亚太地区常见的三家云端 AI 服务，目前的接法与门槛各不相同：

<div class="tbl-names" markdown>

| 云端 AI | App 内贴网址 | 接法 |
|---|---|---|
| **Claude（claude.ai）** | 可以，免费方案也适用（限 1 个连接器） | 设置 → Connectors（连接器）→ Add custom connector，贴上网址 |
| **ChatGPT** | 可以，需付费方案（Plus 以上，免费版不支持） | 设置 → Apps → 高级设置 → 开启「Developer Mode（开发者模式）」→ 新增自定义 connector，贴上网址 |
| **Google Gemini** | 消费版聊天 App 目前不支持 | 需通过 Gemini CLI（需编写配置文件）或 Gemini Enterprise（需 Google Cloud 管理权限），属于工程或企业的用法，见[代码调用与自架](#代码调用与自架) |

</div>

各家的方案门槛与设置位置可能变动，以官方说明为准（Claude[^connector]、ChatGPT[^chatgpt]、Gemini[^gemini]）。

以门槛最低的 Claude 为例，完整步骤如下：

1. 打开 [claude.ai](https://claude.ai)（网页版或桌面版皆可）并登录。
2. 进入设置，找到「Connectors（连接器）」，点击「Add custom connector（新增自定义连接器）」。
3. 名称填 `onionoo`，网址贴上 `https://onionoo.anoni.net/mcp`，按下「Add」。
4. 回到 AI 助手开启新对话，直接用中文提问（例句见下一节）。

使用公司或团队账号时，通常只有账号管理员（Owner）能新增连接器，需请管理员代为新增。

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-claude-desktop.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-claude-desktop.png"
            alt="Claude Desktop 的 Connectors 设置页，onionoo 显示为 CUSTOM connector、连到 https://onionoo.anoni.net/mcp，工具清单列出 aggregate_as、aggregate_countries、aggregate_flags、get_bandwidth、get_clients、get_details、get_summary、get_uptime、get_weights 等工具"
            title="贴上网址后的 Connectors 设置页"
            class="shot">
    </a>
    <figcaption>新增完成后，Connectors 页会列出 <code>onionoo</code> 自定义连接器与它提供的查询工具。使用时不必指定工具，用中文提问，AI 助手会自行选用。</figcaption>
</figure>

## 可以直接复制的问句

以下三句可以直接复制，再依需要换成想查的国家或地区。

**可引用的数字（事实核查）**

> 台湾现在有几个运行中的 Tor 中继节点？总带宽大约多少？帮我整理成一句我能直接引用的话。

**跨国比较（新闻报道）**

> 帮我比较台湾、香港、日本目前运行中的 Tor 中继节点数量与总带宽，做成一个表格。

**节点的分散程度（公民团体）**

> 台湾的 Tor 中继节点分别由哪些电信运营商（ASN）承载？前五大是哪些、各有几个？

得到答案后，可以追问「这些数字是什么时候的？」、「数据来源是哪里？」，请 AI 助手交代出处。

??? info "名词说明"

    第一次看到这些词时，知道大概的意思即可，需要时也可以请 AI 助手解释。

    - **中继节点（relay）**：Tor 网络里负责转发流量的服务器，由志愿者架设，全球近万个。连上 Tor 时，流量会依次经过好几个中继节点。
    - **网桥（bridge）**：没有公开列出的中继节点，供无法连上普通 Tor 节点（例如遭到封锁）的用户绕道连接。
    - **出口节点（exit）**：流量离开 Tor 网络、连回普通网站时经过的最后一个节点。
    - **ASN（自治系统编号）**：电信运营商或网络供应商在互联网上的编号。节点所在的 ASN 代表承载它的运营商。
    - **consensus weight（共识权重）**：Tor 分配流量时给每个节点的分量，大致反映节点能承担的流量，数字越大，分到的流量越多。

## 数字的可靠度与引用方式

查到的数字可以引用，底层数据来自 Tor Project 官方维护的 [Onionoo](https://metrics.torproject.org/onionoo.html)（Tor 中继节点的公开数据服务）。onionoo.anoni.net 只把数据转成较易读的格式，不另外存储或加工数值。

- **交叉核对**：同样的节点可以在 Tor Project 官方的 [Relay Search](https://metrics.torproject.org/rs.html) 查到，两边的数字应该一致。
- **时效**：为了减轻上游负担，服务会把响应缓存约 5 分钟。Onionoo 本身也是定期更新，取得的数字是某个时间点的快照，不是实时值，引用时要一并记下查询时间。
- **引用写法**：可以写成「数据来源：Tor Project Onionoo（经 anoni.net onionoo 服务查询，查询时间 2026-06-09）」。

---

## 代码调用与自架

`onionoo-fastapi` 把 Onionoo API 包装成两种接口，让工具与 AI 代理（agent）更容易使用：

- **语义化 HTTP API**（附 OpenAPI / Swagger）：把 Onionoo 的短字段（`n`、`f`、`a`、`r` 等）转成可读的 `nickname`、`fingerprint`、`addresses`、`running`，并补上一份完整的 OpenAPI 规范。
- **[Model Context Protocol（MCP）](https://modelcontextprotocol.io/) 服务器**：让 Claude Desktop、Cursor、Claude Code 等支持 MCP 的客户端以工具调用（tool call）查询 Tor 中继节点，不需要编写 HTTP 请求的代码。

服务本身**不存储**任何 Onionoo 数据，只负责转发与重新包装响应，上游数据来自 Tor Project 的 [Onionoo 服务](https://onionoo.torproject.org)。

- **服务站点**：<https://onionoo.anoni.net>
- **Swagger UI**：<https://onionoo.anoni.net/docs>
- **MCP 端点**：`https://onionoo.anoni.net/mcp`（Streamable HTTP）
- **源码**：<https://github.com/anoni-net/onionoo-fastapi>（MIT 许可证，当前版本 v1.2.0）

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-swagger.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-swagger.png"
            alt="onionoo.anoni.net 的 Swagger UI，显示 Onionoo FastAPI Proxy v1.0.0，列出 /healthz、/metrics 与 /v1/summary、/v1/details、/v1/bandwidth、/v1/weights、/v1/clients 等端点"
            title="onionoo.anoni.net 的 Swagger UI"
            class="shot">
    </a>
    <figcaption><code>onionoo.anoni.net/docs</code> 的 Swagger UI，每个 <code>/v1/*</code> 端点都附完整 schema，可以用「Try it out」即时测试。</figcaption>
</figure>

### 服务的缘起

Onionoo 的规范完整，但**没有 OpenAPI 描述**，字段名称也为了传输效率缩成短码。工程师读文档、自行编写 client 时不成问题，AI 代理与第三方工具使用起来就比较困难：

- 没有 OpenAPI，Swagger UI、Postman 与 code generator 就无法自动读取规范。
- 短字段名称容易让语言模型误判，例如分不清 `r` 是 `relay` 还是 `running`。
- 一个问题往往要组合好几个端点（`/details` 加 `/uptime` 加 `/bandwidth`），AI 代理每次重新拼凑，容易出错。

`onionoo-fastapi` 补上 OpenAPI 规范、改用语义化字段，并把常见任务包成单一的 MCP 工具调用，例如查询某个中继节点目前的健康状况，一个工具就能完成。

### API 与 MCP 的差别

**API（Application Programming Interface，应用程序接口）** 让程序之间可以互相查询数据。Onionoo 就是一个 API，发送一个 HTTP 请求（例如查询台湾所有 running 的 relay），会收到一份 JSON。规范写给工程师阅读，返回的是原始数据，适合已经知道要问什么的情境。

**MCP（Model Context Protocol，模型上下文协议）** 是 Anthropic 在 2024 年提出的开放协议，定义 AI 模型调用外部工具的标准格式。现有的 API 包装成 MCP server 之后，支持 MCP 的 AI 代理与客户端都能直接接上，由模型读取工具清单，自行决定何时调用哪个工具。每出现一个新的客户端，也不必重做一次集成。

数据挖掘的初期通过 MCP 提问，不必先学会这份数据的 schema，由 AI 助手做初步查询与整理，读完报告再决定下一步。需要重复执行的查询，或要进入正式分析时，再改用 API 编写脚本，两种方式可以并用。

### MCP 服务器的配置文件

客户端以配置文件连接时（不经过前半页的 Connectors 界面），在 `mcpServers` 区块加上：

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

保存并重新启动客户端后，工具清单会出现 `onionoo` 这组工具。

要在本机执行、不依赖远端服务时，改用 stdio transport：

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

需先安装 [`uv`](https://docs.astral.sh/uv/)（macOS 可用 `brew install uv`，Linux 见官方文档）。

Gemini CLI 同样读取 `mcpServers` 配置（位于它的 settings.json），格式与上面相近，填入同一个远端网址即可。消费版的 Gemini 聊天 App 目前没有贴上网址连接远端 MCP 的入口，需等官方支持。

### HTTP API 的调用方式

每个端点都返回语义化的 JSON，并以 `_meta` 标示缓存状态：

```bash
# 查询 moria1 的详细信息，只返回 nickname 与 fingerprint
curl -s 'https://onionoo.anoni.net/v1/details?search=moria&fields=nickname,fingerprint' | jq .

# 列出台湾的 relay，依 consensus weight 排序
curl -s 'https://onionoo.anoni.net/v1/details?country=tw&running=true&order=-consensus_weight&limit=5' | jq .

# 依国家汇总目前 running 的 relay 数量
curl -s 'https://onionoo.anoni.net/v1/aggregate/countries?running=true' | jq .
```

完整的端点、查询参数与响应字段见 [Swagger UI](https://onionoo.anoni.net/docs)，查询参数沿用 Onionoo 的[官方规范](https://metrics.torproject.org/onionoo.html)。

### Docker 自架

要自行架设一份（例如架在 .onion 服务、内网或实验环境）时：

```bash
git clone https://github.com/anoni-net/onionoo-fastapi
cd onionoo-fastapi
docker compose up -d --build
```

默认监听 `8000` 端口，OpenAPI 文档在 `http://localhost:8000/docs`，MCP 端点在 `http://localhost:8000/mcp`。

常用配置（环境变量）：

| 变量 | 用途 | 默认 |
|---|---|---|
| `ONIONOO_BASE_URL` | 上游 Onionoo 地址 | `https://onionoo.torproject.org` |
| `CACHE_MAXSIZE` / `CACHE_DEFAULT_TTL_SECONDS` | 内存缓存大小 / TTL | `128` / `300` 秒 |
| `RATE_LIMIT_ENABLED` / `RATE_LIMIT_PER_MINUTE` | 是否启用 IP 限流 | `false` / `120` |
| `CORS_ALLOW_ORIGINS` | 允许跨来源请求的域名列表，逗号分隔，设为空字符串即关闭（1.0.0 的旧名 `CORS_ALLOWED_ORIGINS` 仍可使用） | `https://anoni.net`、文档站的 onion 镜像与本机预览 |
| `LOG_FORMAT` | `json` 或 `console` | `json` |
| `METRICS_ENABLED` | 是否启用 `/metrics`（Prometheus 格式） | `true` |

完整配置清单见 [README](https://github.com/anoni-net/onionoo-fastapi#configuration)。

### MCP 工具一览

任务导向的工具由 stdio transport 提供，建议代理使用：

| 工具 | 用途 |
|---|---|
| `find_relay(query)` | 自由文字查询，自动判断输入是 40 位指纹、AS 号、IP，或昵称子字符串 |
| `get_relay_health(fingerprint)` | 合并 details、uptime、bandwidth 三个端点，生成一份健康度快照 |
| `top_relays_by_bandwidth(country?, flag?, limit)` | 依 consensus weight 取前 N 名，可选国家或旗标过滤 |
| `compare_relays(fingerprints)` | 并行获取多个 fingerprint 的 details 并排比较 |
| `country_summary(country)` | 单一国家的 running 数量、总带宽、旗标分布 |
| `aggregate_relays(group_by, running, top)` | 在服务器端依 country、AS 或 flag 做 group-by |

对应 Onionoo 原生端点的低阶透传工具，两种 transport 都有提供，名称与参数不同。Streamable HTTP 端是 `get_summary`、`get_details`、`get_bandwidth`、`get_weights`、`get_clients`、`get_uptime`，查询参数逐一列为工具参数，返回语义化的 JSON。stdio 端是 `onionoo_summary`、`onionoo_details` 等同样六个工具，接受一个 `params` dict，返回 Onionoo 的原始响应。

> Streamable HTTP 的 `/mcp` 提供六个低阶工具加上三个 aggregate（countries、as、flags），任务导向工具与整合的 `aggregate_relays` 则由 stdio 端提供。两种 transport 可以同时使用。

### 台湾 Tor 中继节点的盘点示例

onionoo MCP 接上 Claude Desktop 或 Claude Code 之后，可以直接提问：

> 「帮我整理一份台湾 Tor 中继节点现况：总共多少个 running、总带宽、前五大 ASN，顺便挑出 consensus weight 最高的三个 relay，告诉我它们的 nickname 与所在 AS。」

代理会把问题拆成几个 MCP 工具调用，再把结果汇总成一份报告（HTTP transport 通常用 `aggregate_countries` 加 `get_details`，stdio transport 另有 `country_summary`、`aggregate_relays`、`top_relays_by_bandwidth` 等任务导向工具）。以往这类查询需要手动组合 Onionoo 参数、合并 JSON，现在一句话即可完成。

<figure markdown="span">
    <a href="https://assets.anoni.net/docs/onionoo-mcp-tool-use-detail.png" target="_blank">
        <img src="https://assets.anoni.net/docs/onionoo-mcp-tool-use-detail.png"
            alt="Claude Opus 4.7 思考过程的截图：先说「我要找台湾的 relay 信息」、列出可能工具、然后决定先调用 aggregate_countries 找台湾那一列、再用 get_details 抓 country=tw 的 AS 信息、最后依 consensus weight 拉前三名。可以看到 aggregate_countries 这个工具调用已展开、返回 Result"
            title="Claude Opus 4.7 的工具调用展开过程"
            class="shot">
    </a>
    <figcaption>展开模型的推理过程，可以逐步看到代理打算查询的内容、选用的工具，以及结果返回后的下一步。推理文字之间穿插实际的 <code>aggregate_countries</code>、<code>get_details</code> 工具调用，方便调试或调整 prompt。</figcaption>
</figure>

### 观测指标与运维

- `/healthz`：静态存活检查，不连接上游。
- `/healthz/ready`：尝试连接 Onionoo（结果会缓存），返回 200 表示上游可以连接，503 表示无法连接。
- `/metrics`：Prometheus 格式，含缓存命中率（`onionoo_cache_hits_total` 与 `_misses_total`）、上游延迟（`onionoo_upstream_seconds`）与错误率。
- 每个请求都带有 `X-Request-ID`，可以对照 log 与响应 header，方便调试。

## 参与与贡献

- **回报问题与建议**：[onionoo-fastapi 的 GitHub issues](https://github.com/anoni-net/onionoo-fastapi/issues)
- **架设 Tor relay**：见[Tor Relay 架设指南](/join/setup-tor-relay/)，区域内中继节点的观测数字见[Tor 中继节点观测](/projects/pulse/)。
- **出国前评估**：[出国前数字安全：用 AI 自助生成目的地概况](docs:scenarios/travel-ai-briefing/)，记者与公民团体出国前查询目的地的 Tor 中继节点状况时，接上 onionoo MCP 可以取得能引用的 Onionoo 数字。
- **延伸阅读**：[什么是 Tor](docs:tools/what-is-tor/)、[ASNs 自治网络观测数据分析](docs:taiwan/ooni-asn-coverage/)。

服务目前的版本是 v1.2.0，以 MIT 许可证发布。欢迎提出 issue、PR，也欢迎在 Matrix 一起讨论接下来要补上哪些任务导向工具。

[^connector]: [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) - Claude Help Center（自定义连接器在免费、Pro、Max、Team、Enterprise 方案皆可使用，免费方案限一个）。

[^chatgpt]: [Developer mode — apps and full MCP connectors in ChatGPT (beta)](https://help.openai.com/en/articles/12584461-developer-mode-apps-and-full-mcp-connectors-in-chatgpt-beta) - OpenAI Help Center（自定义 MCP connector 需在 Plus、Pro、Business、Enterprise、Edu 方案开启 Developer Mode，免费版不支持）。

[^gemini]: [Set up your custom MCP server data store](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server) - Gemini Enterprise（Google Cloud）。消费版 Gemini 聊天 App 尚未提供在界面内贴网址接远端 MCP 的功能，开发端可用 [Gemini CLI](https://geminicli.com/docs/tools/mcp-server/) 的 `mcpServers` 配置。
