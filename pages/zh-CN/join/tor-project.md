---
title: 参与 Tor Project
description: Tor Project 的规划与活跃项目、官方沟通渠道、中文社区可以开始的参与方式，以及匿名网络社区的工作与 Tor 的关联。
---

Tor Project 是公开治理的非营利组织，沟通渠道、源代码与规划文档大多对外开放，个人不必代表任何组织，就能从翻译、运营中继或举办 meetup 开始参与。匿名网络社区 anoni.net 推广 Tor、Tails、OONI 的这一年，最常被问到的就是如何直接参与 Tor 上游的开发与社区。

在地的观测数据可以交给 Tor 维护网络健康的团队，亚太每多一个中继，Tor 网络的地址就更分散。Tor 的正体中文翻译也需要有人跟着每次更新维护。各项参与方式在文档站有操作教程的，都附上链接。

!!! tip "门槛最低的两项参与方式"

    一项是到 Weblate 校对 Tor 支持文档的正体中文翻译，`zh_Hant` 已大致译完，目前的工作是跟上原文的更新（[Tor new-support-portal](https://hosted.weblate.org/projects/tor/new-support-portal/)，流程见[中文化与文件翻译](docs:community/i18n/)）。另一项是到 Tor 官方论坛与 Matrix 的 `#tor-project:matrix.org` 频道自我介绍。两项都不需要等待批准，以个人身份参与即可，之后的正式合作也从这些贡献记录开始。

## Tor 规划的公开位置

Tor Project 的规划分两层公开，给一般关注者的策略写在官方博客，给贡献者的细部规划放在自建的 GitLab wiki。

Tor Project 每年在[官方博客](https://blog.torproject.org/)发布年度方向，列出当年的优先项目。2026 年的重点是把规避审查的功能整合进更多 Tor 软件（例如 Tails 与 Tor VPN），并持续关注俄罗斯、中国这类各自封闭网络的做法[^1]。年度回顾里的长期重点有四项：性能与安全、网络健康、抗审查、与第三方整合的兼容性[^2]。财报可以看出资助结构的变化，美国政府资助的占比从 FY2021-22 的 53.5% 降到 FY2023-24 的 35.08%，目标是降低对单一资助来源的依赖[^3]。线上大会 State of the Onion 通常在年底举行，2025 年分成 11 月的团队更新与 12 月的社区更新两场，可以一次看完年度方向[^4]。

细部规划在 [Tor 的 GitLab](https://gitlab.torproject.org/tpo)，公开项目不需要登录就能阅读。各团队的 `team` meta 项目在 wiki 放 roadmap 与会议记录，整个组织的资助案整理在 `tpo/team` 的 Sponsors 总览页[^5]。系统管理团队（TPA）的年度 roadmap 写得最具体[^6]，Arti 的里程碑标在群组里带 Roadmap 标签的 issue 上[^7]。milestones 端点需要登录，计划的期程也无法通过公开 API 取得，要从各 wiki 内嵌的链接查。

## 重点方向与活跃项目

本节内容在 2026 年 6 月核对，Tor 的项目与资助变动快，以官方最新的公告为准。参与 Tor 不需要先了解这些技术细节，想直接看能做什么，可以跳到[参与方式](#参与方式)。

### 项目的活跃度

Tor 的 GitLab 上有两百多个项目，活跃程度差异很大。2026 年 6 月用公开 API 扫描时，未归档的项目约 252 个，其中约 103 个在 30 天内有活动，最活跃的是 network-health，web、core、tpa、applications 也有不少项目在持续更新[^8]。数字会随时间变动，实时的状态可以在 GitLab 按 `last_activity_at` 排序查看。

### 技术主线

- 抗审查的三种连接方式。WebTunnel 把桥接流量伪装成普通的 HTTPS，2025 年在俄罗斯是重要的规避工具。Snowflake 用志愿者浏览器的 WebRTC（浏览器之间建立实时连接的技术）当临时代理，目前稳定运作，介绍见 [Tor Snowflake 桥接点](docs:tools/tor-snowflake/)。Conjure 利用 ISP 没有使用的地址空间，对抗审查者逐一列出已知代理 IP 再封锁的手法，官方规划从 2026 年起逐步推出[^9]。
- Arti，用 Rust 重写的 Tor。客户端核心、circuit 与 Onion Service 已经稳定，relay 与 directory authority（维护中继名册的核心服务器）还在开发，官方没有承诺与旧版 C 实现功能一致的时程。
- Counter Galois Onion（CGO），新的对称加密方式，修补旧加密可以被篡改、被用来追踪连接的弱点。目前在 Arti 里标为实验功能，测试完成后才会默认启用。
- Android 版的 Tor VPN，底层使用 Arti，2025 年 9 月推出 beta 版，官方标明仍属实验、不适合高风险的情境。iOS 上仍然使用 Orbot。
- Onion Service 的易用性与防止滥用，以及 Tails（见[什么是 Tails](docs:tools/what-is-tails/)）并入 Tor Project 之后的整合。

### 资助案与延续的方向

资助案最能看出哪些方向会延续下去。下表是 Sponsors 总览页列出的部分资助案[^5]，编号以 `S` 开头。

| 资助案 | 方向 | 与匿名网络社区的关联 |
|---|---|---|
| `S96` | 中国、香港、西藏的审查规避，包含新的 pluggable transport、更难封锁的桥接、改善桥接的分发 | 社区关注的审查规避 |
| `S112` | 对抗恶意中继、改善网络健康，包含监控工具、中继运营者的行为准则、抵御中继攻击 | 社区的观测工作 |
| `S119` | Arti，用 Rust 重写的 Tor | 下一代的技术基础 |
| `S150` | 淘汰 BridgeDB，全面改用 RDSys 分发桥接 | 桥接的分发方式 |
| `S101` | Android 版的 Tor VPN | 给一般用户的产品 |
| `S131` | Mullvad Browser 与 Tor Browser 的重构 | 浏览器 |

`S96` 与 `S112` 跟社区的工作最相关，前者处理中文用户面对的审查，后者对应社区在做的网络可达性观测。

## 官方沟通渠道

Tor 的 IRC（OFTC 网络）与 Matrix 双向桥接，用 Element 加入 Matrix 或用 IRC，都会进到同一个频道[^10]。Tor 官方的频道在 `matrix.org`，与匿名网络社区自建的 `im.anoni.net` 分开。

| 频道 | 用途 |
|---|---|
| `#tor` | 用户支持，询问 Tor 的操作问题 |
| `#tor-dev` | 开发、协议与程序的技术讨论 |
| `#tor-project` | 组织与社区事务、meetup、outreach |
| `#tor-relays` | 中继运营者的社区 |
| `#tor-l10n` | 翻译与本地化 |
| `#tor-meeting` | 旁听或参加有公开记录的团队会议 |

文字讨论与公告在 [Tor Forum](https://forum.torproject.org/)（Discourse 论坛，分成用户支持、本地化、活动等类别），邮件列表在 [lists.torproject.org](https://lists.torproject.org/) 订阅。组织层级的事务用 email 联系：非营利事务、商标与合作协调寄 <frontdesk@torproject.org>，邀请讲者寄 <speaking@torproject.org>，安全问题寄 <security@torproject.org>。

加入频道与论坛之前，先阅读 Tor 的[社区政策与行为准则](https://community.torproject.org/policies/)。

## 参与方式

依中文在地社区的可行性排序，文档站有操作教程的都附上链接。

1. 本地化翻译。门槛最低，不需要审核账号，也不需要技术背景。个人就能在 Weblate 开始，同时改善正体中文的质量，也是累积社区贡献记录最快的方式。流程与 Weblate 的链接见[中文化与文件翻译](docs:community/i18n/)的「Tor 文件翻译」一节，第一次参与先读[成为 Tor 翻译者](https://community.torproject.org/localization/becoming-tor-translator/)。
2. 在 `#tor-project` 与论坛自我介绍。meetup、outreach 与社区事务都在这里讨论，之后的正式合作也从这里开始。
3. 举办在地 meetup。Tor 的 [Outreach](https://community.torproject.org/outreach/) 提供 Street Team Kit、幻灯片与举办 Tor meetup 的素材，官方鼓励自主举办，不需要审核，需要讲者时写信到 <speaking@torproject.org>。
4. 运营中继或桥接。有机器与带宽的成员可以架设中继，增加亚太的节点，步骤见[Tor Relay 架设指南](/join/setup-tor-relay/)。伪装成 HTTPS 的桥接见[Tor WebTunnel 桥接架设指南](/join/setup-tor-webtunnel/)，遇到问题可以到 `#tor-relays` 与 tor-relays 邮件列表询问。
5. 开发与报告问题。到 [anonticket.torproject.org](https://anonticket.torproject.org/) 可以匿名申请 GitLab 账号或报告问题，取得账号之后到对应的 repo 开 issue。新手可以从标了 first-contributors 的 issue 开始，技术讨论在 `#tor-dev`。
6. 成为 Training Partner。Tor 的 [training partners](https://community.torproject.org/training/partners/) 是组织与 Tor 之间最正式的合作形式，通常要先在前几项累积贡献记录，适合当作中长期的目标。

## 匿名网络社区的工作与 Tor 的关联

- 正体中文的翻译与用语。社区已经在做 `zh_Hant` 的翻译与用语规范，可以直接延伸到 Weblate 上的 Tor 翻译。
- 网络可达性观测。社区维护的 [Tor 中继节点观测](/projects/pulse/)（Pulse）与 [OONI 观测覆盖率](/projects/asn-coverage/)（ASN Coverage）对应 network-health 团队与 `S112` 的工作，观测成果可以在该团队的社区场合分享。
- 校园中继。[Tor Relay 校园建立研究专题](/join/relay-on-campus/)源自 EFF 与 Tor Project 合作的 Tor University Challenge，台师大已经有运作中的节点（见[台师大 NZ 访谈](/updates/2025/12/ntnu-nz/)）。

社区年度计划里的安排见 [2026 年度路线图](/join/roadmap-2026/)。State of the Onion 的社区场会公开征求各地社区的更新，社区可以在那里向国际报告这些成果。

## 相关阅读

- [中文化与文件翻译](docs:community/i18n/)：Tor 文档的翻译流程与 Weblate 的使用方式
- [Tor Relay 架设指南](/join/setup-tor-relay/)：架设中继的步骤
- [Tor WebTunnel 桥接架设指南](/join/setup-tor-webtunnel/)：把桥接流量伪装成普通 HTTPS 的架设方式
- [如何参与与认领主题](/join/)：加入匿名网络社区、认领年度主题的方式

[^1]: [Advancing digital rights in 2026](https://blog.torproject.org/advancing-digital-rights-in-2026/) - The Tor Project Blog
[^2]: [The Tor Project's 2024 Year in Review](https://blog.torproject.org/2024-year-in-review/) - The Tor Project Blog
[^3]: [The Tor Project Financial Reports for July 2023 to June 2024](https://blog.torproject.org/financials-blog-post-2023-2024/) - The Tor Project Blog
[^4]: [State of the Onion 2025](https://blog.torproject.org/state-of-the-onion-2025/) - The Tor Project Blog
[^5]: [tpo/team wiki：Sponsors 总览](https://gitlab.torproject.org/tpo/team/-/wikis/Projects/Sponsors-2023) - Tor Project GitLab
[^6]: [tpo/tpa/team wiki：roadmap/2025](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/roadmap/2025) - Tor Project GitLab
[^7]: [tpo 群组 Roadmap 标签 issues](https://gitlab.torproject.org/groups/tpo/-/issues/?label_name[]=Roadmap&state=opened) - Tor Project GitLab
[^8]: [Tor Project GitLab 公开 API](https://gitlab.torproject.org/api/v4/groups/tpo/projects?include_subgroups=true) - 2026 年 6 月扫描的非归档项目活跃度快照
[^9]: [Staying ahead of the censors in 2025](https://blog.torproject.org/staying-ahead-of-censors-2025/) - The Tor Project Blog
[^10]: [Chat with the Tor community](https://support.torproject.org/get-in-touch/chat-with-us/) - Tor Project Support
