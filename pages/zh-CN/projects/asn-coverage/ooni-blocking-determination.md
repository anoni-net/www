---
title: OONI 的封锁判定方式
description: 网络连接测试（Web Connectivity）的 blocking 字段如何计算、四种判定各自对应的证据，以及 blocking 有值与确认封锁之间的差距，附五笔实际测量的判读与常见的误判来源。
---

`blocking` 记录的是单次测量与对照组不一致，离确认封锁还有一段距离，因此在多数情况下，单凭 `blocking: "dns"` 不足以断定某个网站在台湾被封锁。

各字段在测量数据里的位置见[OONI 测量数据的结构](/projects/asn-coverage/ooni-data-format/)。

## 双边对照的判定机制

只靠 Probe 单方面测一个网站，无法区分「网站遭到干预」与「网站本身无法连接」。网络连接测试（`web_connectivity`）因此把同一个网址测两次，分别从 Probe 所在的网络与 OONI 的 test helper 所在的外部网络发出，再比对两边的结果。

test helper 是 OONI 架设在外部网络的测量服务器，观测结果放在 `test_keys.control` 下面，包含 DNS 解析结果、TCP 连接状态与 HTTP 响应。判定字段的值全部取决于两边的差异出现在哪个阶段。比对依下列顺序逐阶段进行，停在第一个出现差异的阶段：

<ol class="flow" aria-label="网络连接测试的四个判定阶段">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>DNS 解析</b><span class="d">比对两边对同一个域名的 A 与 AAAA 查询结果</span><span class="out"><span class="if">解析结果不一致</span><code>blocking: "dns"</code></span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>TCP 连接</b><span class="d">两边能否连上目标 IP 的端口</span><span class="out"><span class="if">只有 Probe 无法连接</span><code>blocking: "tcp_ip"</code></span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>HTTP 请求</b><span class="d">连接建立之后，能否取得 HTTP 响应</span><span class="out"><span class="if">HTTP 阶段失败</span><code>blocking: "http-failure"</code></span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>响应内容</b><span class="d">比对状态码、标题、标头与内容长度</span><span class="out"><span class="if">内容与 test helper 不同</span><code>blocking: "http-diff"</code></span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>四个阶段都一致</b><span class="out"><code>blocking: false</code><code>accessible: true</code></span></span></li>
</ol>

比对在更早的阶段就已中止，所以前三种判定的四个 `*_match` 字段全为 `null`。下一节的四笔实际测量各自对应一个阶段。

!!! tip "`control` 与 `blocking` 的判读顺序"

    `blocking` 是双边比对的结果，并非 Probe 单方面的观测。判读异常测量时，先确认 `test_keys.control` 里 test helper 的观测内容，再回头读 `blocking`。下一节的 `tcp_ip` 示例，就是忽略 `control` 而把网站自身的问题误判成封锁的情况。

判定算法的完整定义在上游的 [ts-017-web-connectivity](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md)，失败字符串的统一命名在 [df-007-errors](https://github.com/ooni/spec/blob/master/data-formats/df-007-errors.md)。

## 四种判定对应的证据

后续章节引用的五笔测量都是 2026-08-04 的公开数据，原始内容可以在 [OONI Explorer](https://explorer.ooni.org/) 查到。

### `dns`，解析结果的差异

台湾对 `https://ntc.party/` 的测量里，Probe 对 A 与 AAAA 的查询都得到 `dns_nxdomain_error`（域名不存在）。test helper 端可以查到，因此 `dns_consistency` 标为 `inconsistent`。

```json title="test_keys.queries"
{"query_type": "A", "failure": "dns_nxdomain_error", "answers": []}
{"query_type": "AAAA", "failure": "dns_nxdomain_error", "answers": []}
```

判读 DNS 判定时要留意解析器属于哪个网络，该笔的解析器 ASN（自治系统编号，`resolver_asn`）是 `AS13335`（Cloudflare），Probe 所在的 ASN（`probe_asn`）则是 `AS3462`（中华电信）。测量者把 DNS 指向境外服务时，DNS 阶段的异常未必反映本地运营商的行为。

### `tcp_ip`，目标地址的连接失败

台湾对 `http://www.tkec.com.tw/` 的测量判定为 `tcp_ip`，DNS 正常解析到 `210.64.193.1`，Probe 连接 `80` 端口时超时。

单看 Probe 端容易误读成封锁，对照 `control` 的结果则会得出不同的结论：

```json title="test_keys.control.tcp_connect"
{"210.64.193.1:443": {"status": true,  "failure": null},
 "210.64.193.1:80":  {"status": false, "failure": "generic_timeout_error"}}
```

test helper 从外部连接 `80` 端口同样超时，可见该网站的 `80` 端口从外部也无法连接，与台湾的网络环境无关。同一个 IP 的 `443` 端口在两侧都可以连接，进一步确认问题出在该端口，与连接路径无关。

### `http-failure`，连接建立后的内容获取失败

台湾对 `https://bit.ly/` 的测量判定为 `http-failure`。DNS 正常，两个目标 IP 的 `443` 端口都可以连接，`control` 记录的 test helper 端结果也相同。差异出现在 HTTP 阶段，错误是 `generic_timeout_error`。

连接层正常而应用层失败，常见于服务器端的速率限制、对特定来源的拒绝服务，以及 TLS 层的中断。要区分成因，需查看 `tls_handshakes` 与 `network_events` 的时序。

### `http-diff`，获取内容的差异

台湾的数据里也有 `http-diff`，但形态与封锁告示页不同（见文末的台湾现况），因此以下改用印尼的测量说明典型的告示页。

四种类型中只有 `http-diff` 会用到四个 `*_match` 字段，印尼 `http://www.sportsinteraction.com/` 的测量是典型的例子：

| 观测方 | 状态码 | 标题 | 内容长度 |
|---|---|---|---|
| Probe | `200` | `Trustpositif` | 7,044 |
| test helper | `403` | `Maintenance` | 7,067 |

Probe 的请求被重定向到 `http://lamanlabuh.aduankonten.id/`，属于印尼官方的内容申诉域名，页面标题 `Trustpositif` 是当地网络内容过滤系统的名称。ISP 在连接途中把用户导向告示页，是 `http-diff` 最典型的成因。

从同一笔测量也可以看出，单一字段不足以作为判断标准：

```text title="四个 *_match 字段与 body_proportion"
title_match: false        status_code_match: false
headers_match: true       body_length_match: true
body_proportion: 0.9967
```

`body_length_match` 为 `true`、`body_proportion` 接近 `1`，只是因为封锁告示页与对照组页面的长度相近。单看长度会得到错误的结论，四个字段要一并判读，其中 `title_match` 与 `status_code_match` 的区分度通常最高。

## 误判的来源

`blocking` 有值、实际上却没有网络干预，在数据集里是常态，前述 `tkec.com.tw` 的 `80` 端口无法连接就是一例。

埃及 `http://www.newipnow.com/` 的测量是更隐蔽的例子，判定为 `http-diff`。四个 `*_match` 有三个不符，`body_proportion` 只有 `0.02`，表面上像是被插入了封锁页。实际内容如下：

| 观测方 | 状态码 | 标题 |
|---|---|---|
| Probe | `520` | `newipnow.com \| 520: Web server is returning an unknown error` |
| test helper | `200` | `Buy Private Proxies: $0.88 per Dedicated Premium IP - NewIPNow` |

`520` 是目标网站前方的 Cloudflare 在源服务器异常时返回的错误页，表示该网站当时发生异常，与埃及的网络管制无关。该笔的 `probe_asn` 是 `AS13335`（Cloudflare），测量端本身也位于 Cloudflare 的网络上，属于下列第二类的测量环境因素。

常见的误判来源可分为以下几类：

- **来源网站自身状态**：服务器错误、维护页、CDN 错误页、地理限制。
- **测量环境**：Probe 启用 VPN 或 Tor 时，测得的是出口所在地的网络。
- **网站的动态内容**：轮播广告、个性化内容与 A/B 测试，会让两侧的内容本来就不相同。
- **对照组本身失败**：`control_failure` 有值时，双边比对的前提不成立。

OONI 在数据集层级也处理同一类问题，过滤异常提交所用的启发式规则整理在[OONI 错误测量的识别方法与匿名凭证](/articles/ooni-faulty-measurements/)。

## 单笔测量之外的补强

要从观测推进到「某个网站在某地被封锁」的结论，单笔数据并不足够，实践中还需补上以下几个维度：

1. **跨时间**：同一个网址在数天到数周内反复出现同样的判定，才能排除偶发故障。
2. **跨 ASN**：多家运营商测得相同的结果，指向网络层的普遍行为。只在单一 ASN 出现的结果，比较可能是该运营商的个别设置。
3. **跨解析器**：更换 DNS 解析器后仍然异常，才能排除解析器本身的问题。
4. **`confirmed` 字段**：OONI 后端以已知的封锁告示页指纹比对测量，命中时把 `confirmed` 标为 `true`。该字段出现在 [measurements API](https://api.ooni.org/api/v1/measurements) 的响应里，属于后端的分析结果，不在 Probe 产生的原始数据内。

跨时间与跨 ASN 比对所需的批量获取做法，见[ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)。

!!! warning "`confirmed` 与 `http-diff` 的区别"

    `confirmed` 标记的依据是封锁指纹比对，容易与 `http-diff` 混淆。DNS 被导向已知的封锁用 IP 时同样会标为 `confirmed`，判定类型仍是 `dns`。撰稿时抽查伊朗、俄罗斯、土耳其、中国各 5 笔 `confirmed` 测量，样本全部落在 `blocking: "dns"`。样本数少，只能看出两者并非同一件事，不足以推论一般规律。

## 台湾现况

以下数字取自 2026-08-05 往前 24 小时的台湾 `web_connectivity` 全量数据，共 22,105 笔测量。统计时把该区间在 S3 上的每一笔逐行解析，再把 `test_keys.blocking` 按 ASN 累计：

| 判定 | 笔数 | 占比 |
|---|---|---|
| `false`（未观测到干预） | 21,029 | 95.13% |
| `none`（没有判定结果） | 512 | 2.32% |
| `tcp_ip` | 312 | 1.41% |
| `dns` | 150 | 0.68% |
| `http-failure` | 67 | 0.30% |
| `http-diff` | 35 | 0.16% |

四种干预类型合计 564 笔，占全部测量的 2.55%。`none` 是缺少 `test_keys` 或 `blocking` 为 `null` 的测量，计算异常率前要先决定是否纳入分母。

另外抽查 100 笔异常测量，`confirmed` 为 `true` 的有 0 笔，与[ASN 多样性与台湾的观测缺口](/projects/asn-coverage/asn-diversity/)长期以来的描述一致。

!!! warning "小样本的分布偏差"

    本页初稿曾以 measurements API 异常清单的 40 笔抽样估计判定分布，得到 `dns` 最多、`http-diff` 为零的结论。改用全量统计之后两个结论都不成立，`tcp_ip` 是 `dns` 的两倍以上，`http-diff` 也确实存在。API 的异常清单有自己的排序逻辑，直接当成随机样本会失准。判定分布应以全量统计取得，做法见[ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)。

抽查 4 小时区间内台湾的 15 笔 `http-diff`，`body_proportion` 全部落在 `0.004` 到 `0.21`，Probe 取得的内容远短于对照组。前述印尼的封锁告示页接近 `1`，台湾的 `http-diff` 是相反的形态，属于不同的现象。内容极短通常代表错误页或空响应，成因要逐笔查验证据层才能判断，我们不在本页下结论。

重新执行上述统计的命令：

```bash title="取得判定分布"
uv run python ooni.py lookback --units=24 --loc=TW --frame=hours
```

命令会输出 `blocking` 的合计，并把逐 ASN 的分布写入 CSV。单笔查验仍使用 API：

```bash title="列出台湾的异常测量"
curl -s "https://api.ooni.org/api/v1/measurements?probe_cc=TW&test_name=web_connectivity&anomaly=true&limit=100" \
  | python3 -m json.tool | head -40
```

以上数字是单一 24 小时区间的快照，反映的是当日的形态，不足以作为长期趋势的结论。趋势分析需要涵盖更长的时间，台湾的观测本身也有 ASN 集中度过高的限制（细节见前述的[ASN 多样性与台湾的观测缺口](/projects/asn-coverage/asn-diversity/)）。

## 相关阅读

- [ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)：跨时间、跨 ASN 比对的起点，含公开数据集的批量获取与覆盖率计算
- [OONI 测量数据的结构](/projects/asn-coverage/ooni-data-format/)：一笔测量数据由哪些字段组成，以及各字段的读法
- [OONI 测项速查表](/projects/asn-coverage/ooni-nettests-map/)：ooni/spec 收录的各个测项的测量内容与台湾的观测情况
- [ASN 多样性与台湾的观测缺口](/projects/asn-coverage/asn-diversity/)：台湾各 ASN 的 OONI 观测覆盖率与集中度
- [OONI 网站检测清单的维护](/join/ooni-test-list/)：OONI Probe 在台湾使用的网站清单如何维护
