---
title: 2026 年度路线图
description: 匿名网络社区 anoni.net 2026 年的三大主题、文档站的季度规划、活动、对外协作、技术项目与参与方式。
---

匿名网络社区 anoni.net 2026 年延续 Tor、Tails、OONI 的在地推广，另外推进三个新主题：个人隐私指引、Tor Relay 校园建立、匿名支付探索。每一季结束时检视交付状况，再调整下一季的安排。

2025 年的回顾与 2026 年规划的背景见[延续 2025，走向 2026](/updates/2026/01/2025to2026/)。

## 三大主题

### 个人隐私指引

2025 年推广 Tor、Tails、OONI 时，社区最常被问到「下一步该怎么做才能更安全」，回答这个问题需要一套可以照着操作、依情境分级的隐私指引。个人隐私指引依日常使用、敏感工作、高风险情境三种等级整理工具与步骤，写成文档站的[概念层](docs:basics/)、[工具层](docs:tools/)、[场景层](docs:scenarios/)三层文档。

文章索引与目前进度见[个人隐私指引研究专题](/join/privacy-guide/)。

### Tor Relay 校园建立

主题源自 EFF 与 Tor Project 合作推动的 [Tor University Challenge](https://toruniversity.eff.org/zh-tw/)，目标是在大专院校架设稳定运行的中继节点。国立台湾师范大学资讯工程学系的资讯中心已经在运行一个 Tor 中继节点，由社区伙伴向教授与教职员提案、协调后架设完成（经过见[在台师大架设 Tor Relay](/updates/2025/12/ntnu-nz/)）。

社区在 2025 年完成 Tor University Challenge 网站的正体中文翻译，2026 年到校园推动架设。台师大的经验在 2026 年 5 月整理成提案范本、架设 SOP、校方 FAQ 三份范本，其他学校可以依自己的状况改写后沿用。

范本、案例与参与方式见[Tor Relay 校园建立研究专题](/join/relay-on-campus/)，架设的技术步骤见[Tor Relay 架设指南](/join/setup-tor-relay/)。

### 匿名支付探索

现金是最成熟的匿名支付方式，用在跨境、线上与组织收受捐款时有明显的限制。社区在合法的前提下研究链上工具的可行性，包含加密货币、稳定币、零知识身份验证与多重签名的实现。中文资源里还没有完整、有系统的整理，社区从研究起步，逐步写成实现指引。

文章索引与目前进度见[匿名支付研究专题](/join/payments-research/)。

## 文档站的季度规划

文档站的指南分成概念、工具、场景、进阶、报告五个子群组，2026 年依这个架构逐季补齐内容。各季的范围与目前的状态：

- **Q1（已完成）**：优先补齐[概念层](docs:basics/)，加上在地法规（[台湾个资法 2025 修法](docs:taiwan/pdpa-2025/)、[台湾 VASP 法 2026](docs:taiwan/vasp-2026/)）、[紧急求救](docs:help/)页、社区治理与路线图
- **Q2（初稿已上线）**：工具层的 Tor Browser 进阶设置、匿名操作系统比较、通讯工具比较、密码管理器、加密货币的隐私光谱，以及进阶层的端到端加密，各篇持续校订
- **Q3（初稿已上线）**：场景层的记者、社运行动者、家暴受害者、LGBTQ+、选举观察员等情境，进阶层的后量子密码与去中心化网站发布，以及揭弊者保护法的技术观察
- **Q4（进行中）**：[治理章程](/about/governance/)草案与[贡献者百科](docs:community/contributor-handbook/)已上线，年度回顾在年底整理

实际进度视撰稿志愿者的人力而定。

## 活动

### COSCUP 2026

社区延续 2025 年参与 COSCUP 的经验，2026 年 8 月 8 日、9 日在国立台湾科技大学再度开设社区议程轨，并与 [ETHTaipei](https://ethtaipei.org/) 合办匿名支付主题场次，安排在 8 月 8 日下午的 `TR-511`。完整议程见[COSCUP 2026 匿名网络社区议程轨](/events/coscup-2026/)，议程开放投稿时的说明见[COSCUP 2026 公开征稿](/events/coscup-2026-cfp/)。

### 工作坊与小聚

延续 2025 年 8 月在台科大举办[匿名网络工作坊 2025/08](/events/workshop-2025/)的经验，2026 年视议题进度与伙伴的需求安排定点工作坊与线上小聚。对象包含新闻媒体、独立记者、公民团体、技术社区与一般关注者。

## 对外协作

### 研究与报告翻译

社区在 2025 年下半年翻译并分享了 InterSecLab 研究中国审查技术输出的报告[网络政变 / The Internet Coup](https://anoni.net/docs/reports/interseclab-network-coup/)（中译只有正体中文版）。2026 年持续挑选对在地有参考价值的国际报告，翻译并加上注释，收在文档站的[严选报告](docs:reports/)。

### 外部活动参与

社区成员常参加在地开源、公民团体与隐私相关的活动，例如黑客松、年会、议题小聚与讲座。多半以个人或社区代表的身份交流、了解议题的脉络，属于非正式的往来。议程联合征稿、报告翻译协作、活动共同筹办这类正式合作，确定之后会在[活动参与](/events/)公告。

## 技术项目

社区也开发并运维几个与 Tor、OONI、密码安全相关的技术项目：

- **[Tor 中继节点观测](/projects/pulse/)（Pulse）**：收集 Tor 中继节点的数据并提供 API，使用 FastAPI 与 PostgreSQL
- **[OONI 观测覆盖率](/projects/asn-coverage/)（ASN Coverage）**：批次分析 OONI 的公开数据，相关文章见文档站的[ASNs 自治网络观测数据分析](docs:taiwan/ooni-asn-coverage/)
- **Asian Diceware**：与 EFF 兼容的 7776 字密语词表，混入有字典背书的亚洲外来语。社区之后想自建类似 Tor Project [AnonTicket](https://anonticket.torproject.org/) 的匿名服务平台，词表也是生成账号代码的字源，介绍见[Asian Diceware，带亚洲味的英文密语字典](docs:tools/asian-diceware/)

三个项目的源代码与议题追踪分别在 GitHub 的 [anoni-net/pulse](https://github.com/anoni-net/pulse)、[anoni-net/asn-coverage](https://github.com/anoni-net/asn-coverage)、[anoni-net/asian-diceware](https://github.com/anoni-net/asian-diceware)。两个观测工具与 Tor 上游 network-health 团队工作的关联，见[参与 Tor Project](/join/tor-project/)。

## 参与方式

参与不需要技术背景，可以依兴趣选一个入口：

- 了解议题、关注社区动态：订阅电子报（见[持续关注](/contact/)）、加入 Matrix
- 参与翻译与写作：见[中文化与文件翻译](docs:community/i18n/)、[参与](/join/)
- 评估自己的技术涉入程度：见[自我技能评估表](docs:community/skill-level/)
- 了解沟通与协作工具：见社区的[服务](/services/)

社区的讨论主要在 Matrix（家服务器 `im.anoni.net`），共笔用 CryptPad，在线会议用 Jitsi，账号申请与各服务的入口也整理在[服务](/services/)页。

## 路线图更新

路线图每季结束时检视并调整，重大调整依社区的提案流程讨论，并在 Matrix 公布（提案流程见[治理章程](/about/governance/)）。

**最后更新**：2026-10（Q4 进行中）。
