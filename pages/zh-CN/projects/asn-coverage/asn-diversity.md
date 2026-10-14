---
title: ASN 多样性与台湾的观测缺口
description: 台湾 OONI 测量来源集中在少数 ASN 的现状与数字、补足覆盖的参与方式，以及单笔测量数据的解读。
---

OONI Probe 在台湾的测量数量不少，但如果绝大多数来自同一两家电信运营商，整体观测只能反映那几家的网络状况，无法代表台湾完整的连接环境。某个网站若只在特定一家运营商被封锁，而那家刚好没有人在测，这次封锁就不会留下记录。测量来源的 ASN（自治系统编号）多样性不足，是台湾 OONI 观测数据目前最明确的问题之一。测哪些网站由检测清单决定（见[OONI 网站检测清单的维护](/join/ooni-test-list/)），本页整理测量来自哪些网络。

## 以 ASN 为单位的观测

互联网由许多自治系统（Autonomous System，AS）相互连接而成。电信运营商、学术机构、企业与 CDN 服务商各自管理的网络群组都是一个 AS，有独立的路由策略，彼此通过 BGP 交换路由。每个 AS 有一个独一无二的编号，也就是 ASN。AS 与 BGP 的基本概念见 Cloudflare Learning 的 [What is an autonomous system?](https://www.cloudflare.com/zh-cn/learning/network-layer/what-is-an-autonomous-system/) 与 [What is BGP?](https://www.cloudflare.com/zh-cn/learning/security/glossary/what-is-bgp/)。

对 OONI 观测来说，ASN 是「在哪一家网络上看到审查」的最小单位。同一个网站可能在中华电信无法连接、在台湾大哥大正常，要以 ASN 为单位才能区分这种差异。OONI 的分析因此常看一个地区的测量来自多少个不同的 ASN，比例越高，越能反映该地区整体的连接环境。

查询自己当前连接的 ASN 可以用 [ip.me](https://ip.me/)。[Cloudflare Radar](https://radar.cloudflare.com/zh-cn/as3462) 的 AS 页面列出单一 ASN 的流量趋势与历史记录（例 AS3462），[Is BGP safe yet?](https://isbgpsafeyet.com/) 可以检查当前的 ISP 是否做了 RPKI 路由验证。

## 台湾测量来源的集中程度

[OONI](https://ooni.org/) 的全球志愿者用 [OONI Probe](https://ooni.org/install/) 检测网络审查，所有测量结果上传到项目的[公开数据库](https://registry.opendata.aws/ooni/)。社区在 2023-11 到 2024-03 用 [ASN Coverage](https://github.com/anoni-net/asn-coverage) 分析 OONI 公开数据，2023-12 的结果如下：

- 台湾的测量数量在 OONI Explorer 排名前十
- 78.94% 的测量集中在 [AS3462（中华电信）](https://radar.cloudflare.com/zh-cn/as3462)与 [AS18041（Taiwan Digital Streaming）](https://radar.cloudflare.com/zh-cn/as18041)
- 台湾约有 437 组 ASN，测量数据里不重复的 ASN 只占 7.32%

测量数量充足，来源却集中在两个 ASN，无法反映台湾完整的网络样态。三大电信运营商、有线电视宽带、固网与第二类电信（租用电信基础设施提供服务的业者，例如虚拟移动网络、网络电话转售）都有覆盖不足的问题。

2023 年之后的变化见项目首页的 [OONI 观测覆盖率](/projects/asn-coverage/)。页面每小时依 OONI 最近 60 天的测量重新生成，对照 APNIC 估计的各网络用户人数，列出用户多、测量少的网络。2026-10 的数据里，测量最多的仍是中华电信 HiNet（AS3462），中华电信移动网络（AS17421）有约 16% 的用户，测量占比却不到 0.1%。

### 补足覆盖的参与方式

要补上覆盖，最直接的做法是让一台设备在还没有人测过的 ASN 上持续执行检测。社区维护的 OONI Run 链接 `10328` 是现成的入口，移动设备安装 [OONI Probe](https://ooni.org/install/mobile) 之后点一次链接即可完成设置，接着让 OONI Probe 留在后台运行。安装前需衡量的风险与清单内容见 [OONI Run v2 操作说明](docs:tools/ooni-run-v2/)。

现有测量几乎都落在少数固网 ASN 上，移动运营商与第二类电信的数据最缺乏，使用移动网络的协助者特别有帮助。目前还没有测量的网络列在 OONI 观测覆盖率页的「还没有测量的网络」。

## 单笔测量数据的解读

最快的入门方式是自己用 OONI Probe 产生一笔测量数据：

1. 下载 [OONI Probe](https://ooni.org/install/)（移动设备或桌面版本）
2. 打开 OONI Probe，选择「网站」项目并执行检测
3. 完成后到「测试结果」找到刚才的网站检测，查看是否有「！」或「？」项目
4. 点击任一「！」或「？」查看可能的检测问题，其中有「数据」、「在 OONI Explorer 中显示」链接
5. 点击链接即可查看原始测量数据

以这笔测量为例：[`20241024185921.623617_TW_webconnectivity_578b6d3845fed2e2`](https://explorer.ooni.org/zh-cn/m/20241024185921.623617_TW_webconnectivity_578b6d3845fed2e2)

结果是「在 AS3462 上执行检测失败」，失败信息为 `unknown_failure: dial tcp [scrubbed]: connect: host is down`，表示检测当时主机没有响应。「DNS 查询」段落记录了 `www.asap.com.tw` 的 DNS `A` 记录指向 `60.250.151.72`（AS3462，Chunghwa Telecom Co., Ltd.），查询结果来自 Cloudflare DNS 的 `162.158.242.36`。

结果页面没有完整显示的细节，可以在「原始测量数据」找到所有检测项目的原始内容，作为进一步分析的素材。

![OONI Explorer 原始测量数据的界面](https://assets.anoni.net/www/ooni-raw-data-b3b80fe2.webp)

!!! note "连接端与 DNS 解析端的 ASN"

    OONI Probe 会记录整个检测过程。上面的示例通过中华电信的网络连接，DNS 查询却由 Cloudflare 响应，原始数据里的 `probe_asn` 与 `resolver_asn` 因此分属两个不同的 ASN。网站受到阻挡而无法连接时，问题出在连接所在的 AS 还是 DNS 解析，需要从这两个字段分开判断。

各字段的含义见[OONI 测量数据的结构](/projects/asn-coverage/ooni-data-format/)，判定结果的算法见[OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)，各测项的测量对象见[OONI 测项速查表](/projects/asn-coverage/ooni-nettests-map/)。

## 覆盖率的自行计算

要自行提取 OONI 公开数据、计算特定区域的 ASN 覆盖率，工具的设置与指令见 [ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)，开发环境的准备见[参与开发的环境准备](/join/dev-setup/)。

[<i data-icon="database-search"></i> ASN 观测数据的提取与分析](/projects/asn-coverage/howto/){ .btn .solid }

## 后续方向

社区接下来计划依网络类型（移动网络、家用宽带）分开计算覆盖率。所需的字段只在原始测量里，OONI 的汇总 API 没有提供，目前只能用 [ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)的工具手动整理。另一个方向是搭配[OONI 网站检测清单的维护](/join/ooni-test-list/)，同时改善检测的网站与测量来源的多样性。

## 相关阅读

- [OONI 网站检测清单的维护](/join/ooni-test-list/)：OONI Probe 在台湾使用的网站清单与参与维护的方式
- [OONI 观测覆盖率](/projects/asn-coverage/)：每小时更新的各网络用户数与测量数对照
- [ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)：提取 OONI 公开数据、计算覆盖率的命令行工具
- [8/13 台湾北部移动网络降速演练的 OONI 测量号召](/updates/2026/08/ooni-mobile-throttle-drill/)：2026-07 到 08 的测量分布，HiNet 一个网络占 39.3%
- [Tor 中继节点观测](/projects/pulse/)：社区的另一个观测项目
- [网络自由为什么重要](docs:basics/internet-freedom/)：文档站的入门说明
