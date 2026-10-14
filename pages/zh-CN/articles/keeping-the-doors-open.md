---
title: Unredacted 的抗审查基础设施与台湾的对照
description: Unredacted 在 Tor Blog 客座文章的全文翻译，介绍他们用 300 多台服务器运行的 FreeSocks、Tor 网桥与 Snowflake，以及用约 400W 运行 123 个出口节点的 GreenWare，文末对照台湾的 Tor 中继节点现况与参与方式。
date: 2026-06-01
---

审查越严格，人们需要的替代路径就越多，维持这些路径靠的是服务器、带宽与电费。Unredacted 在全球运维 300 多台服务器，为身处审查环境的用户提供绕过封锁的服务，也尝试用单板计算机降低 Tor 出口节点的耗电。以下翻译他们在 Tor Blog 的客座文章，文末是 anoni.net 社区的三节补充，对照台湾的中继节点数量、在台湾复制 GreenWare 的成本，以及读者可以参与的方式。

原文是 Unredacted 在 Tor Blog「捍卫自由网络的组织」系列发表的 [Keeping the doors open](https://blog.torproject.org/keeping-the-doors-open-unredacted/)（2026-05-15），文中的「我们」指 Unredacted。

有位中国的用户曾这样描述我们的工作：

> 「你们帮了很多很多人翻过防火长城。如果没有你们的帮助，我会被困在完全的黑暗里，被洗脑。」

使用我们服务的人很少发声，他们大多没有办法，或觉得无法安全地传出消息。每次有一条消息传过来，都提醒我们这份工作真正关系到什么。

我们是 Unredacted，注册在美国的 501(c)(3) 非营利组织（美国税法下的免税公益组织）。我们建立并运维网络基础设施，帮助大家连上开放的网络、保护自己的隐私权，做法是在全球运维一个超过 300 台服务器的网络。前门被锁住时，我们是另一条通道，公共广场不再安全时，我们是还能交谈的地方。

这份工作大多看不见，包括数据中心作业、硬件、自动化、开源软件、带宽、滥用投诉的处理、监控告警，以及为了让一切保持在线而熬过的深夜。

我们的工作分成三个方向。Censorship Evasion（绕过审查）是 Unredacted Door 所在的地方，所有用来绕过封锁的服务都归在这个名称底下。Secure Infrastructure（安全基础设施）底下有 [XMPP.is](https://xmpp.is/)、我们的 Matrix homeserver，以及其他以安全与隐私为前提的免费服务。Unredacted Education 是写作与文档的部分，提供指南与说明给想理解这些工作、想自行复制一套的人。三个方向之外，我们在 Unredacted Labs 实验还没到正式上线等级的基础设施构想，GreenWare 是其中之一，目标是用耗电不高的硬件承载实际的网络容量。

## Unredacted Door

名称就是字面上的意思，通往开放网络的入口被墙封住时，人们需要另一条进去的路。

Unredacted Door 整合了我们几项绕过审查的服务，包括 FreeSocks、Signal 与 Telegram 的消息代理、Tor 网桥与 Snowflake 代理。最近 30 天内，这些服务为数万名在自己国家绕过审查的用户承载了将近 300 TiB 的流量，大约相当于播放数万小时 4K 视频的带宽。需求没有减缓，我们需要继续扩建。每一道新的过滤规则、每一条新法律、每一次打着「为了你的安全」名义推出的措施，都让更多人去找审查者还没发现的路。

Unredacted Door 里规模最大的是 FreeSocks，提供给审查严重地区的免费代理。代理是一个中转点，你的应用程序连到中转的服务器，由它把连接带过你与外部网络之间的过滤设备，再接到被封锁的服务。

FreeSocks 的设计目标是让中转点低调、不引人注意，一般 VPN 正好缺少这个特质。VPN 的端点与握手方式都是已知的，在线路上也有明显的数据包形状，审查者很擅长封锁可以识别的东西。

Tor Browser 提供强度足够的浏览隐私与匿名性。Snowflake 在 Tor 网络本身被封锁时，帮用户连上 Tor。FreeSocks 代理则让特定流量走一条较难察觉的路径。没有单一工具能覆盖所有情境，身处审查环境的人通常需要同时准备几种，因为没有一扇门能永远开着。

所以我们投入相当多的精力开发 FreeSocks 第二版（v2）。v2 使用 Xray，一套强大且灵活的流量路由引擎，可以让代理流量更接近一般的网页流量。

!!! note "Xray"

    Xray 是源自 V2Ray 项目的流量路由与伪装工具，支持 VLESS、Trojan、Reality 等协议，把代理流量伪装成一般的 HTTPS、TLS 流量。传统 VPN 容易识别的握手与数据包特征，在 Xray 的流量里比较难找到，所以近年在审查严重的网络环境里是常见的代理工具。详见 [Xray-core 项目](https://github.com/XTLS/Xray-core)。

我们把 Xray 与自家开源的控制平面结合，审查者找到并封锁某台服务器时，系统可以自动轮换端点。用户本来就承受压力，需要自行调整的设置越少越好。

## GreenWare 与低耗电硬件

Tor 中继、网桥与代理都在数据中心的硬件上运行，硬件有实际的成本，包括财务、运营与环境。如果希望隐私基础设施能长期维持，就要问什么样的运维方式才真的能持续。

GreenWare 是我们在不减少承载量的前提下缩小成本的尝试。大多数 Tor 中继的流量，并不需要一台耗电像取暖器的服务器。中继需要的是稳定的网络、可预测的 CPU，以及足够存放状态的内存，只要机箱设计得够扎实，单板计算机就能处理这种规模的工作量。

我们从 Raspberry Pi 5 主板开始，通过 PoE（以太网供电）用一根网线同时提供电力与数据。构想本身可行，数据中心典型的服务器耗电约等于一台小型取暖器，一台 Pi 比一个灯泡还少。不过第一代有它的上限，密度不如预期，部分配套组件也无法承受我们长时间的使用。

所以我们现在同时采用两种部署。第一种是在 1U 机箱里装 20 个 ComputeBlade 模块，20 个全部部署在我们的数据中心，并把一部分 Tor 出口节点迁到上面运行。机箱满载时耗电略超过 100W，大约是一个旧式白炽灯泡。第二种是我们自行设计的 Raspberry Pi 机箱，ComputeBlade 的经验让我们更清楚现场真正需要什么。两种都已经上线，截至撰文时，我们全部 123 个 Tor 出口节点都在这套合并后的基础设施上运行，总耗电约 400W。项目更成熟之后，我们会再分享机箱设计与整体进展。

Tor 网络依赖愿意为它运维基础设施的个人与组织。出口节点是其中最难的部分，需要带宽、维护、滥用投诉处理、承担法律风险的勇气，以及资金。如果能降低提供实际出口容量所需的成本与电力，就有更多人能分担一部分工作，让网络更多元、规模更大。

更长期的目标是持续推动高效率硬件、碳排放追踪，以及最终以可再生能源供电的小型站点（micro points of presence）。我们很乐意与希望这件事扩大的组织和公司合作。

开放的网络能保持开放，靠的是许多个人与组织投入的精力与时间，包括测量审查的研究者、提供带宽的中继运维者，以及不放弃彼此的社区。Unredacted 负责的部分，是在明显的路径消失时，建立并维护人们可能需要的替代路径。

---

以下三节由 anoni.net 社区补充。

## 台湾的对照

Unredacted 引用的那段用户留言格外少见，身处审查环境的人多半没有渠道，也难以安全地对外发声。台湾的网络环境相对自由，没有防火长城，不要求 VPN 登记，ISP 也没有接到国家的审查命令。正因如此，台湾有条件为被封锁的地区架设 Tor 中继与网桥，分担一部分抗审查基础设施的工作。

anoni.net 社区通过 [Tor 中继节点观测](/projects/pulse/)追踪台湾 Tor 中继节点的数量与分布。截至 2026-05-31，Onionoo（Tor 官方的中继数据查询服务）的数据里，位于台湾、正在运行的中继节点有 12 个，其中带 Exit 标记的只有 3 个。Unredacted 一个组织就运行 123 个出口节点，30 天承载近 300 TiB 流量，台湾全境的出口节点数量还不到他们的 3%。最新的数字见 [Tor 中继节点观测](/projects/pulse/)，页面上的数据持续更新。台湾各 ASN 的 OONI 观测覆盖率另见 [ASN 自治网络观测数据分析](docs:taiwan/ooni-asn-coverage/)。

中文的抗审查资源相对稀缺，anoni.net 的工作之一就是补齐中文资源，包括[什么是 Tor](docs:tools/what-is-tor/)、[Tor Snowflake](docs:tools/tor-snowflake/)、[什么是 OONI](docs:tools/what-is-ooni/) 等基础文档，方向与 Unredacted Education 相同。

## GreenWare 在台湾的可行性

Unredacted 用 400W 运行 123 个出口节点。以台湾一般工商业电价每度约 NT$ 3.5 至 6（约人民币 0.8 至 1.4 元）估算[^1]，400W 全年运转约 3,500 度，一年电费约 NT$ 12,000 至 21,000，在学校信息中心或社区协作空间可以负担的范围内。其他地区的读者可以按当地电价换算。

规模化的关键在硬件设计，Raspberry Pi 5 对 maker 社区并不陌生，PoE+ HAT 与 PoE 交换机在常见的电子零售与网购渠道都可以买到。ComputeBlade（20 模块的 1U 机箱）的零售渠道较少，可以通过官方海外订购或社区代购取得。校园机房比家用网络更适合，有固定 IP、学术网络带宽，也有人定期巡检机器。

Tor Relay 校园建立是 anoni.net 2026 年的三大主题之一，社区正把校园架设的经验整理成 SOP（见 [Tor Relay 校园建立研究专题](/join/relay-on-campus/)与[台师大架设 Tor Relay 的经验](/updates/2025/12/ntnu-nz/)）。之后评估架设方案的学校，可以参考 Unredacted 在 GreenWare 上的工程做法，先用 PoE 供电的 Raspberry Pi 5 试做一台 middle relay，运行稳定之后再考虑出口节点与机箱密度。

个人或小团体可以从 Snowflake proxy 开始（浏览器扩展或 Docker），几乎没有电费负担，是参与抗审查基础设施门槛最低的方式（见 [Tor Snowflake](docs:tools/tor-snowflake/)）。

## 参与方式

想为审查地区的人多维持一条对外的路，可以从下面几项开始：

- **了解 Unredacted**：到 [unredacted.org](https://unredacted.org/) 查看服务与透明度信息，再决定是否通过官方渠道支持服务器、带宽与人力成本。
- **运行 Snowflake**：门槛最低的参与方式，用浏览器扩展或 Docker 即可运行（见 [Tor Snowflake](docs:tools/tor-snowflake/)）。
- **架设 Tor relay 或 bridge**：需要稳定的网络与一些运维时间，步骤见 [Tor Relay 架设指南](/join/setup-tor-relay/)与 [Tor WebTunnel 网桥架设指南](/join/setup-tor-webtunnel/)。
- **校园 Tor Relay**：在大专院校工作或就读的人，可以从 [Tor Relay 校园建立研究专题](/join/relay-on-campus/)开始评估。
- **加入社区讨论**：在 Matrix 与其他社区成员交流经验，入口见[参与](/join/)，其他联系渠道见[持续关注](/contact/)。

## 相关阅读

- [什么是 Tor](docs:tools/what-is-tor/)
- [什么是 OONI](docs:tools/what-is-ooni/)
- [伊朗断网后涌进社区 Tor WebTunnel 网桥的流量](/updates/2026/05/iran-blackout-webtunnel/)
- [台师大架设 Tor Relay 的经验](/updates/2025/12/ntnu-nz/)
- [Tor 中继节点观测](/projects/pulse/)
- 同系列：[Defending the public's right to know（OONI）](https://blog.torproject.org/Defending-the-right-to-know/)、[Preserving evidence: How OpenArchive fosters accountability and media sovereignty](https://blog.torproject.org/preserving-evidence-openarchive-fosters-accountability-media-sovereignty/)

[^1]: 台电 2026 年平均电价为每度 NT$ 3.7823（经济部 2026-03-27 电价审议会决议，4 至 9 月维持平均电价），实际每度单价依用电种类与分时电价（峰时、谷时）而有差异。数据来源：[台湾电力公司电价表](https://www.taipower.com.tw/2289/2290/46940/)。（2026-10 补注：经济部 2026-09-18 的电价费率审议会决议暂不调整，10 月起全台平均电价仍为每度 NT$ 3.7823，见[今周刊的报道](https://www.businesstoday.com.tw/article/category/183027/post/202609180046/)。）
