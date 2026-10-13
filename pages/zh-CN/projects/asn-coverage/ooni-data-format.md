---
title: OONI 测量数据的结构
description: 一笔 OONI 测量数据的外壳、判定、证据三层结构，与各层常用字段的解读方式。以两笔台湾的真实测量对照，各字段附上游 ooni/spec 的规范文档。
---

一笔 OONI 测量有二十多个顶层字段，`test_keys` 底下还有二十几个。提取公开数据的方法写在[ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)，本页接着说明提取之后如何解读字段。

范例是两笔台湾的真实测量，测项是网络连接测试（`web_connectivity`），各字段都标出对应上游 [ooni/spec](https://github.com/ooni/spec) 的哪一份规范。

!!! info "范例数据来源"

    两笔都是台湾的 OONI Probe 在 2026-08-04 产生的公开数据，原始内容可以在 [OONI Explorer](https://explorer.ooni.org/) 查到。

    | | 正常通过 | 判定异常 |
    |---|---|---|
    | 测量对象 | `http://presidentlee.tw/` | `https://ntc.party/` |
    | `measurement_uid` | `20260804085935.603513_TW_webconnectivity_4a5fd27dec0b32f6` | `20260804084548.416537_TW_webconnectivity_f4e7b0ab3d0251bf` |

## 一笔测量的三层结构

一笔测量可以拆成三层：

1. **外壳**：记录谁在哪里、用什么软件、在什么时候测量。所有测项共用同一套字段，规范是 [df-000-base](https://github.com/ooni/spec/blob/master/data-formats/df-000-base.md)。
2. **判定**：测量得出的结论，字段随测项而异，全部收在 `test_keys` 底下。`web_connectivity` 的定义在 [ts-017](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md)。
3. **证据**：支撑结论的原始记录，包含每一次 DNS 查询、TCP 连接、TLS 握手与 HTTP 请求，以及对照组的同类记录。证据同样放在 `test_keys` 底下，各自对应一份 `df-` 开头的规范。

## 单笔测量的获取方式

通过公开 API 可以直接获取单笔测量，不需要事先搭建环境。先列出符合条件的测量：

```bash title="列出台湾最近的网络连接测试"
curl -s "https://api.ooni.org/api/v1/measurements?probe_cc=TW&test_name=web_connectivity&limit=5" \
  | python3 -m json.tool | head -40
```

再用响应里的 `measurement_uid` 获取完整内容：

```bash title="获取单条完整测量数据"
curl -s "https://api.ooni.org/api/v1/raw_measurement?measurement_uid=<measurement_uid>" \
  | python3 -m json.tool | head -60
```

原始响应是未换行的长字符串，所以上面两段命令都接上 `python3 -m json.tool` 排版，方便阅读。查询参数加上 `anomaly=true` 可以筛出判定异常的测量，适合用来寻找对照范例。改写 `probe_cc` 与 `probe_asn`，即可查询指定地区与网络的观测记录。

批量处理大量数据时，AWS S3 公开数据集的效率较高（做法见[ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)）。

## 外壳层的字段

外壳层的字段在所有测项中都相同，常用的字段如下：

| 字段 | 正常通过那笔 | 判定异常那笔 | 说明 |
|---|---|---|---|
| `probe_cc` | `TW` | `TW` | 测量发生的国家代码 |
| `probe_asn` | `AS3462` | `AS3462` | 执行测量的网络所属 ASN |
| `probe_network_name` | `Chunghwa Telecom Co., Ltd.` | `Chunghwa Telecom Co., Ltd.` | 该 ASN 的组织名称 |
| `resolver_asn` | `AS3462` | `AS13335` | 测量时实际使用的 DNS 解析器所属 ASN |
| `resolver_network_name` | `Chunghwa Telecom Co., Ltd.` | `Cloudflare Inc` | 解析器的组织名称 |
| `input` | `http://presidentlee.tw/` | `https://ntc.party/` | 测量对象的网址 |
| `test_name` | `web_connectivity` | `web_connectivity` | 测项名称 |
| `software_name` | `ooniprobe-cli` | `ooniprobe-desktop-unattended` | 产生数据的 Probe 种类 |
| `software_version` | `3.29.1` | `3.26.0` | Probe 版本 |
| `measurement_start_time` | `2026-08-04 08:59:30` | `2026-08-04 08:45:45` | 测量开始时间（UTC）|
| `report_id` | `20260804T062033Z_webconnectivity_TW_3462_n4_uEH5rGoD07cN2oYQ` | `20260804T084446Z_webconnectivity_TW_3462_n4_dFfWCDrwouM0TsT2` | 同一次执行产生的多笔测量共用此值 |

`probe_asn` 与 `resolver_asn` 可能分属不同网络，上表就有一个例子。两笔测量都在中华电信的网络上执行，其中一笔的使用者把 DNS 指向 Cloudflare。ASN 分析需要把两者分开计算，混在一起会让特定电信运营商网络上的观测结果失准。

!!! note "固定为 `127.0.0.1` 的 `probe_ip`"

    OONI 刻意不收集测量者的真实 IP，`probe_ip` 字段一律填入本机地址。回溯测量来源只能依靠 `probe_asn` 与时间（同一条隐私边界的提醒另见[OONI Run v2 操作说明](docs:tools/ooni-run-v2/)）。

## 判定层的字段

判定字段全部收在 `test_keys` 底下，由双边对照计算而来。Probe 测完之后，OONI 部署在外部网络的测量服务器（test helper）会对同一个网址再测一次，判定的依据就是两边结果的差异。test helper 一侧的记录收在 `test_keys.control`，下表的「对照组」就是指这一侧的记录。

判定结果与内容比对共八个字段，两笔并排如下：

| 字段 | 正常通过 | 判定异常 | 说明 |
|---|---|---|---|
| `blocking` | `false` | `"dns"` | 判定的干预类型，可能值为 `dns`、`tcp_ip`、`http-failure`、`http-diff`，未观测到干预时为布尔值 `false` |
| `accessible` | `true` | `false` | 是否取得了合理的响应 |
| `dns_consistency` | `"consistent"` | `"inconsistent"` | Probe 的 DNS 结果与对照组是否一致 |
| `title_match` | `true` | `null` | 网页标题是否与对照组相符 |
| `headers_match` | `true` | `null` | 响应头是否相符 |
| `status_code_match` | `true` | `null` | HTTP 状态码是否相符 |
| `body_length_match` | `true` | `null` | 响应内容长度是否相近 |
| `body_proportion` | `1` | `0` | 内容长度与对照组的比值 |

各阶段的失败原因记录在另外三个字段，解读时要与上表一起看：

| 字段 | 记录什么 |
|---|---|
| `dns_experiment_failure` | DNS 阶段的失败原因，判定异常那笔为 `"dns_nxdomain_error"` |
| `http_experiment_failure` | HTTP 阶段的失败原因，例如 `"generic_timeout_error"` |
| `control_failure` | 对照组本身是否失败。有值时双边比对的前提不成立，判定结果不可信 |

`blocking` 的四种值分别对应不同阶段的异常（四种干预手法的概念说明见[什么是 OONI](docs:tools/what-is-ooni/)）：`dns` 是解析结果与对照组不一致、`tcp_ip` 是数据包送不到目标地址、`http-failure` 是连接建立后 HTTP 阶段失败、`http-diff` 是取得的内容与对照组不同（常见于封锁告示页）。

!!! tip "容易误判的两个类型问题"

    `blocking` 未观测到干预时是布尔值 `false`，有干预时是字符串。统计前要先统一类型，否则 `false` 与 `"dns"` 会被归为两类。

    四种值的命名并不一致，`tcp_ip` 用下划线，`http-failure` 与 `http-diff` 用连字符。上游的定义就是如此，引用时照原样写，不要自行统一。

四个 `*_match` 字段在判定异常那笔全是 `null`，因为 DNS 阶段就已失败、连接没有建立，后续没有可以比对的内容。遇到整排 `null` 时，回头找测量流程中第一个有值的 failure 字段，问题就发生在那个阶段。

!!! warning "异常与封锁的差别"

    `blocking` 有值只代表该笔测量的结果与对照组不一致，要确认是否存在网络干预还需要更多佐证。以判定异常那笔为例，Probe 对 `ntc.party` 的 A 与 AAAA 查询结果都是 `dns_nxdomain_error`（域名不存在）。但我们撰稿时用多个公开 DNS 解析器查询，该域名可以解析到 IPv6 地址。仅凭单笔测量，无法区分网络干预、解析器的暂时状态与域名自身的设置变动。

    认定封锁需要跨时间、跨 ASN、跨解析器的多笔测量交叉比对。判定机制的完整拆解与常见的误判来源见[OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)，数据集层级的质量控制见[OONI 错误测量的识别方法与匿名凭证](/articles/ooni-faulty-measurements/)。

## 证据层的原始记录

`test_keys` 底下另有数个字段，记录测量过程中的每一次网络操作，各自对应一份规范：

| 字段 | 内容 | 规范 |
|---|---|---|
| `queries` | 每一次 DNS 查询的问题、响应与失败原因 | [df-002-dnst](https://github.com/ooni/spec/blob/master/data-formats/df-002-dnst.md) |
| `tcp_connect` | 每一次 TCP 连接尝试的目标与结果 | [df-005-tcpconnect](https://github.com/ooni/spec/blob/master/data-formats/df-005-tcpconnect.md) |
| `tls_handshakes` | 每一次 TLS 握手的参数、证书与结果 | [df-006-tlshandshake](https://github.com/ooni/spec/blob/master/data-formats/df-006-tlshandshake.md) |
| `requests` | 每一次 HTTP 请求与响应的完整内容 | [df-001-httpt](https://github.com/ooni/spec/blob/master/data-formats/df-001-httpt.md) |
| `network_events` | 连接过程的时序事件，用于分析延迟与中断点 | [df-008-netevents](https://github.com/ooni/spec/blob/master/data-formats/df-008-netevents.md) |
| `control` | 对照组的同类记录，结构与 Probe 侧对应，判定字段全部由它与 Probe 端的差异算出 | [ts-017](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md) |
| 各字段的 `failure` 字符串 | 所有失败原因的统一命名，例如 `dns_nxdomain_error`、`generic_timeout_error`、`ssl_unknown_authority` | [df-007-errors](https://github.com/ooni/spec/blob/master/data-formats/df-007-errors.md) |

两笔的 `queries` 对照如下：

```json title="正常通过：查到地址"
{
  "hostname": "presidentlee.tw",
  "query_type": "A",
  "failure": null,
  "answers": [{"answer_type": "A", "ipv4": "43.254.17.201"}]
}
```

```json title="判定异常：查询落空"
{
  "hostname": "ntc.party",
  "query_type": "A",
  "failure": "dns_nxdomain_error",
  "answers": []
}
```

判定层的 `dns_consistency` 是结论，依据是 `queries` 与 `control`。要确认判定是否合理，回头查验证据层即可。

## 版本与兼容性

对照 spec 之前，需要先确认版本：

- **`data_format_version`**：目前是 `0.2.0`，外壳层的字段定义稳定，可以直接对照 [df-000-base](https://github.com/ooni/spec/blob/master/data-formats/df-000-base.md)。
- **`web_connectivity` 的 `test_version`**：实际流通的是 `0.4.3`。[ts-017](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md) 的内容已经改成描述 v0.5 算法，但生产环境仍以 v0.4 为主。spec 里明确规定新版算法必须使用不同的 `test_keys` 字段，v0.4 的字段定义保持兼容，所以上表的字段读法对两个版本都适用。
- **`x_` 开头的字段**：不在 spec 内，实际数据中会出现 `x_dns_runtime`、`x_status`、`x_th_runtime` 等字段。它们属于实现端的实验性扩展，会随版本增减，分析程序不应依赖。

上游 spec 的 master 分支自 2025-06 起没有新的合并，但 issue 与 PR 的讨论持续进行（进行中的提案包含 ICMP 数据格式与 DPI 分片测项）。现阶段可以把 spec 当作稳定的参考，引用时链接回上游原文，避免复制规范内容之后因上游更新而失准。

上游规范的完整目录在 [ooni/spec](https://github.com/ooni/spec)，其中 [data-formats](https://github.com/ooni/spec/tree/master/data-formats) 收录数据格式、[nettests](https://github.com/ooni/spec/tree/master/nettests) 收录各测项的算法定义。

## 相关阅读

- [OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)：判定字段的计算方式，以及 `blocking` 有值为何不等于封锁
- [OONI 测项速查表](/projects/asn-coverage/ooni-nettests-map/)：ooni/spec 收录的各个测项与对应的上游规范
- [什么是 OONI](docs:tools/what-is-ooni/)：OONI 的工具与数据集，以及四种干预手法的概念说明
- [ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)：从公开 API 与 AWS S3 公开数据集批量提取测量数据的做法
- [ASN 自治网络观测数据分析](docs:taiwan/ooni-asn-coverage/)：台湾各 ASN 的 OONI 观测覆盖率分析
- [OONI 网站检测清单](docs:taiwan/ooni-checklist/)：OONI Probe 在台湾使用的网站检测清单与维护方式
