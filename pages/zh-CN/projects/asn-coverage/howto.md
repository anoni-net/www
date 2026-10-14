---
title: ASN 观测数据的提取与分析
description: OONI 观测覆盖率（ASN Coverage）命令行工具的设置与用法，包含 OONI 三种数据入口的取舍、S3 公开数据集的路径结构、输出的 CSV 字段，以及 ASN 覆盖率的计算方式。
---

[OONI 观测覆盖率](/projects/asn-coverage/)（ASN Coverage）提供命令行工具（[`anoni-net/asn-coverage`](https://github.com/anoni-net/asn-coverage)），用来提取 OONI 的公开数据，计算特定区域内 ASN（自治系统编号）的观测覆盖率。为什么要看 ASN 的覆盖率，写在[ASN 多样性与台湾的观测缺口](/projects/asn-coverage/asn-diversity/)，工具的设置与用法则整理在本页。

开始前建议先按[参与开发的环境准备](/join/dev-setup/)搭建开发环境。

!!! tip "执行位置"

    以下指令都在 [`anoni-net/asn-coverage`](https://github.com/anoni-net/asn-coverage) 的目录下执行。第一次使用时先 clone repo 并 `cd` 进目录，执行 `uv sync` 安装依赖，再按下方范例以 `uv run python ooni.py ...` 执行。

## 三种取用路径

OONI 的观测数据有三个入口，各自适合的用途差异很大，着手前需先选定：

| 入口 | 适合的情境 | 限制 |
|---|---|---|
| [AWS S3 公开数据集](https://registry.opendata.aws/ooni/) | 批次分析、全量统计、跨时间比对 | 需自行解析，下载量以 GB 计 |
| [OONI API](https://api.ooni.org/api/v1/measurements) | 依条件筛选、取单笔完整测量 | 单次返回笔数有上限 |
| [OONI Explorer](https://explorer.ooni.org/) | 人工查阅、确认个别测量 | 不适合程序化取用 |

ASN Coverage 用来统计覆盖率，用不到单笔查询，所以采用 S3 路径。单笔查询与小量筛选的 API 用法见[OONI 测量数据的结构](/projects/asn-coverage/ooni-data-format/)。

## 程序的统计范围

`ooni.py` 现阶段统计覆盖率与判定结果的分布，数据的取用范围有三个限制：

- **只读 `webconnectivity` 目录**，同一小时底下其他十几个测项都没有纳入，`tor`、`telegram`、`signal` 等测项的观测不会出现在统计中。各测项的测量对象见[OONI 测项速查表](/projects/asn-coverage/ooni-nettests-map/)。
- **每笔测量只取三个字段**，`probe_asn`、`annotations.network_type` 与 `test_keys.blocking`。证据层的 `queries`、`tcp_connect`、`requests` 都没有读取，所以从输出可以看出哪些 ASN 有人在测、测了几次、判定结果如何分布，看不到单笔测量的证据内容。
- **只取 `.jsonl.gz`**，跳过同目录的 `.tar.gz`。

`blocking` 在未观测到干预时是布尔值 `false`，有干预时是字符串。程序在计数前把两种值统一成同一组键，没有判定结果的测量记为 `none`，所以每个 ASN 的判定分布加总一定等于测量笔数。判读前提见[OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)。

要再往下分析证据层，需要取出那一层的字段逐笔比对。单纯的计数统计无法容纳这些数据，存储方式需要另行设计。

## S3 数据集的目录结构

Bucket 名称是 `ooni-data-eu-fra`，位于 `eu-central-1`，公开读取不需认证凭证。路径依日期、小时、国家代码、测项分成四层：

```text title="路径结构"
raw/{YYYYMMDD}/{HH}/{国码}/{测项}/{YYYYMMDDHH}_{国码}_{测项}.n{编号}.{序号}.jsonl.gz
```

!!! warning "以 UTC 表示的日期与小时"

    路径中的 `{YYYYMMDD}` 与 `{HH}`，以及后续 CSV 输出的 `date` 与 `hour` 字段，全部使用 UTC。程序内部一律以 `arrow.Arrow.utcnow()` 取得时间。分析台湾某个时段的观测分布时，需要加 8 小时换算，否则图表会整体偏移。

文件名尾端的 `.n{编号}.{序号}` 是 OONI 内部的批次编号，解析时可忽略。

不必安装任何工具也能确认目录内容：

```bash title="台湾单一小时的测项清单"
curl -s "https://ooni-data-eu-fra.s3.eu-central-1.amazonaws.com/?list-type=2&prefix=raw/20260804/00/TW/&delimiter=/" \
  | grep -oE '<Prefix>raw/[^<]+</Prefix>'
```

响应是未换行的 XML，上例接上 `grep` 只取出目录名称。台湾在单一小时内通常有十几个测项目录，`webconnectivity` 只是其中之一，同层还有 `tor`、`telegram`、`signal`、`whatsapp`、`dnscheck`、`echcheck`、`openvpn`、`psiphon`、`ndt`、`dash` 等。

每个测项目录底下，同一批数据有 `.jsonl.gz` 与 `.tar.gz` 两种封装。`.jsonl.gz` 解开后一行一笔测量，适合逐行解析，程序读取的就是 `.jsonl.gz`。以 2026-08-04 台湾的 `webconnectivity` 为例，单一文件约 10 MB。换算成全国整个月的数据量相当可观，执行前应先估算带宽与执行时间。程序以流式处理，原始文件不会写入磁盘，最后只输出 CSV。

各字段的判读方式见[OONI 测量数据的结构](/projects/asn-coverage/ooni-data-format/)，判定字段的含义见[OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)。

## 提取与分析指令

### 近期数据的回溯

```bash title="最近 36 小时的数据"
uv run python ooni.py lookback --units=36 --loc=TW --frame=hours
```

三个参数都可以省略，默认值与上例相同。`--frame` 设置回溯总长度的单位，可填 `hours`、`days`、`weeks` 等。不论单位为何，数据一律按小时切分。输出文件名的格式：

- `lookback_{loc}_{YYYYMMDD}_{units}_{frame}.csv`

文件名中的 `{YYYYMMDD}` 是执行当天的 UTC 日期，并非数据涵盖的区间，实际范围要看文件内容。文件写入当前的工作目录。

### 指定区间的数据

```bash title="指定区间的数据"
uv run python ooni.py span --start=2026/08/01 --end=2026/08/03 --loc=TW --chunk=40
```

带入开始时间（`start`）与结束时间（`end`），可以取得该期间每个小时的数据。`--chunk` 控制同时处理的小时数，默认 `40`，网络或内存不足时应调小。输出文件名的格式：

- `span_{loc}_{开始YYYYMMDD}_{结束YYYYMMDD}.csv`

### 电子表格格式的转换

```bash title="电子表格格式的展开"
uv run python ooni.py sheetrow --path=./span_TW_20260801_20260803.csv
```

`sheetrow` 把已提取的数据展开，方便在电子表格中计算。输出文件名是在原文件名前加上 `rows_`，上例的输出即 `rows_span_TW_20260801_20260803.csv`。

## 输出的 CSV 字段格式

`lookback` 与 `span` 产出的文件有四个字段，一行代表一个小时：

| 字段 | 内容 |
|---|---|
| `loc` | 国码，例如 `TW` |
| `date` | 日期，格式 `YYYY/MM/DD`，UTC |
| `hour` | 小时，格式 `HH`，UTC |
| `statistics` | 该小时的统计结果，内容是一段 JSON |

`statistics` 内含三份计数：`counts` 依 ASN 统计测量笔数、`network_type` 依连接类型统计、`blocking` 依 ASN 统计判定结果的分布。以 2026-08-04 台湾 `00` 时的实际数据为例，该小时共 551 笔测量：

```json title="statistics 字段展开"
{"counts": {"AS3462": 300, "AS17716": 100, "AS18419": 100, "AS24158": 51},
 "network_type": {"mobile": 44, "no_internet": 7},
 "blocking": {"AS3462": {"false": 294, "dns": 1, "tcp_ip": 1, "none": 4},
              "AS17716": {"false": 94, "none": 6},
              "AS18419": {"false": 99, "none": 1},
              "AS24158": {"false": 51}}}
```

`counts` 与 `blocking` 的加总逐 ASN 相等，`network_type` 的加总则不会相符。`network_type` 由 Probe 自行标记，移动版 App 通常会写入，CLI 与桌面版多半不会。上例 551 笔中只有 51 笔带标记，程序会跳过未标记的测量。其中 `no_internet` 代表 Probe 在测量当下检测到自身没有连接。标记覆盖率不到一成，适合观察趋势，不适合作为移动网络与固网的比例依据。

`blocking` 中的 `none` 代表该笔没有判定结果，缺少 `test_keys` 或 `blocking` 为 `null` 的测量都归入此类。上例 551 笔中有 11 笔属于 `none`，占比不高，但每个 ASN 都有。计算异常率前，要先决定这些测量是否纳入分母。

嵌套的 JSON 不易在电子表格中计算，`sheetrow` 把它摊平成一行一个 ASN：

| `loc` | `date` | `hour` | `asn` | `count` | `anomaly` | `blocking_false` | `blocking_dns` | `blocking_tcp_ip` |
|---|---|---|---|---|---|---|---|---|
| `TW` | `2026/08/04` | `00` | `AS3462` | `300` | `2` | `294` | `1` | `1` |
| `TW` | `2026/08/04` | `00` | `AS17716` | `100` | `0` | `94` | `0` | `0` |

上表受限于版面只列出前几列，完整字段还有 `blocking_http_failure`、`blocking_http_diff`、`blocking_none` 与 `blocking_other`。`anomaly` 是四种干预类型的加总，可直接在电子表格中作为分子。`blocking_other` 收录 `ts-017` 尚未定义的值，正常情况下应为 `0`，出现非零值代表上游新增了判定类型。

实际分析输出的电子表格范例（2023-09 至 2023-12）：

[<i data-icon="google-spreadsheet"></i> 20230901-20231204-TW](https://docs.google.com/spreadsheets/d/1lMDsqX8Oa3GKW68y8TuFeKQW2nKM7X0u4z-RopfJIaA/){ .btn .solid }

## ASN 覆盖率的计算

计算覆盖率需要两个数字：观测数据中出现过的不重复 ASN 数，以及该区域登记在案的 ASN 总数。前者用数据透视表从上一节摊平后的 CSV 取得，后者用 `ripe.py` 向 RIPE NCC 查询：

```bash title="区域内的全量 ASN 清单"
uv run python ripe.py save --loc=TW
```

输出文件名为 `asns_{YYYYMMDDTHH}.csv`，六个字段分别是 `no`、`location`、`org_id`、`registrar`、`reserved`、`name`。

!!! warning "两份数据的 ASN 格式差异"

    `ripe.py` 输出的 `no` 字段是纯数字（`3462`），OONI 数据的 `probe_asn` 带 `AS` 前缀（`AS3462`）。直接用 VLOOKUP 比对会全部落空，比对前要先在其中一边补上或去除 `AS`，统一两边的格式。

两个数字备齐后即可计算：

```text title="覆盖率算式"
覆盖率 = 观测数据中出现的不重复 ASN 数 ÷ 该区域登记的 ASN 总数
```

以社区 2023-12 的分析为例（见[ASN 多样性与台湾的观测缺口](/projects/asn-coverage/asn-diversity/)），台湾当时约有 437 组 ASN，观测数据涵盖的不重复 ASN 占 7.32%。同一算式也可以套用在近期的区间，对照覆盖率是否改善。

## 相关阅读

- [OONI 测量数据的结构](/projects/asn-coverage/ooni-data-format/)：一笔测量的各个字段与判读方式
- [OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)：`blocking` 等判定字段的含义
- [OONI 测项速查表](/projects/asn-coverage/ooni-nettests-map/)：各测项的测量对象
- [ASN 多样性与台湾的观测缺口](/projects/asn-coverage/asn-diversity/)：台湾各 ASN 的观测覆盖率分析，覆盖率算式的范例数字取自该页 2023-12 的分析
- [参与开发的环境准备](/join/dev-setup/)：参与项目开发前的环境设置
- [如何参与与认领主题](/join/)：加入社区、认领年度主题的方式
