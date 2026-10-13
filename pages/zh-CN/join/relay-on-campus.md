---
title: Tor Relay 校园建立研究专题
description: 匿名网络社群 2026 年三大主题之一，在大专院校架设 Tor 中继节点的推动目标、台师大案例、提案与架设范本，以及参与方式。
---

Tor Relay 校园建立是匿名网络社群 anoni.net 2026 年的三大主题之一，与[个人隐私指引](/join/privacy-guide/)、[匿名支付](/join/payments-research/)并列。社群在大专院校推动架设 Tor 中继节点，并把提案、与校方沟通、技术配置与运维的过程整理成范本，让之后加入的学校更容易推动。欢迎在校学生、校友、教职员与有网络运维经验的人一起参与（见[参与方式](#参与方式)）。

## 选择校园的原因

Tor 网络的匿名性依赖多元的中继节点，中继集中在少数国家或少数网络服务商时，Tor 对抗流量分析的能力就会降低。台湾在 Tor Metrics 上能看到的中继数量有限，截至 2026-06 约有 15 个运行中的中继，德国有上千个、美国有数千个，差距明显（数字会随时间变动，实时状况见 [Tor 中继节点观测](/projects/pulse/)）。

大专院校适合补上台湾中继数量的缺口：

- **带宽稳定**：学术网络通常有充足且稳定的带宽
- **技术人才**：计算机、信息管理相关院系与学校信息中心的师生具备架设与运维的能力
- **制度明确**：学校有正式的提案与审核流程，比个人或小公司架设更容易说明用途、争取支持
- **教育价值**：架设过程本身就是匿名网络、信息安全与开源治理的教学场景
- **国际计划**：参与 EFF 的 [Tor University Challenge](https://toruniversity.eff.org/zh-tw/)，把台湾的校园纳入全球的校园中继网络

## 2026 推动目标

- **校园架设 SOP**：涵盖提案、与学校沟通、技术配置、上线与后续运维的完整流程（2026-05 随范本工具包公开）
- **应答范本与案例库**：法律疑虑、带宽使用、用途说明等常见问题的回应参考
- **其他学校的接洽**：以台师大为起点，扩展到其他大专院校
- **与 EFF、Tor Project 的联系渠道**：建立稳定的国际联系，把台湾的案例反馈给全球计划
- **实时观测**：用 [Tor 中继节点观测](/projects/pulse/)持续追踪校园节点的运行状况
- **结合信息安全教育活动**：把 Tor Relay 架设纳入校园信息安全宣传、迎新讲座等场合

## 相关文章

- 案例：[在台师大架设 Tor Relay：一段与学校沟通、留下可能性的实现经验](/updates/2025/12/ntnu-nz/)
- 国际：Tor Project 博客的客座文章 [Setting Up a Tor University Relay in Taiwan](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)
- 架设指南：[Tor Relay 架设指南](/join/setup-tor-relay/)、[Tor WebTunnel 桥接架设指南](/join/setup-tor-webtunnel/)
- 观测：[Tor 中继节点观测](/projects/pulse/)
- 概念：[什么是 Tor](docs:tools/what-is-tor/)、[Tor Snowflake](docs:tools/tor-snowflake/)
- 进阶：[一台会遗忘的服务器：探索 Stateless Relays](docs:blog/2026/04/a-server-that-forgets-exploring-stateless-relays/)

## 已完成的工作

- **第一个校园节点**：国立台湾师范大学资讯工程学系资讯中心的 Tor Relay 运行中，由社群伙伴 NZ 经教授与教职员提案、协调后完成建置
- **Tor Project 博客客座文章**：台师大案例的英文版刊登在 [Tor Project 博客](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)，供其他国家的推动者参考
- **Tor University Challenge 中译**：完成 [EFF Tor University Challenge 网站](https://toruniversity.eff.org/zh-tw/)的正体中文翻译，降低台湾其他学校接触计划的语言门槛
- **Tor 中继节点观测上线**：[观测页](/projects/pulse/)每小时更新台湾与邻近共十五个地区的中继节点状况
- **案例访谈**：台师大的架设过程整理成[深度访谈](/updates/2025/12/ntnu-nz/)，公开给后续的推动者参考
- **范本工具包**：台师大的实践经验整理成提案文件、技术 SOP 与校方 FAQ 三份范本，其他学校可以直接套用（见下一节）

## 范本工具包

范本工具包整理自社群伙伴 NZ 在台师大的实践经验，其他学校的学生不必从零开始，可以复制范本、按学校的情况改写，再提交到自己学校的审核流程。

- [校园 Tor Relay 提案范本](/join/relay-on-campus/proposal/)：提案文件、四封沟通邮件、行政时间轴
- [校园 Tor Relay 架设 SOP](/join/relay-on-campus/sop/)：torrc、UFW、状态网页、监控、事件处置 runbook
- [给校方与法务的校园 Tor Relay FAQ](/join/relay-on-campus/faq/)：校方常见疑虑的问答与台湾背景的补充

建议先读[台师大案例访谈](/updates/2025/12/ntnu-nz/)了解全貌，再按角色选读范本，提案者读提案范本、技术运维者读 SOP，与校方面谈时带上 FAQ。

## 进行中的工作

- **其他学校的接洽**：与其他大专院校初步联系、评估可行性
- **信息安全活动的合作**：与学校信息安全周、迎新讲座、Hackathon 等活动的合作模式
- **政策沟通材料**：给教育部层级的计划说明、跨国比较资料
- **外部资源的翻译**：候选清单见下一节

## 翻译候选与延伸阅读

社群标记了几份候选的外部资源，欢迎志愿者协助翻译或摘录重点：

- [Tor Project Relay Operator Guides](https://community.torproject.org/relay/)：Tor Project 官方的中继运营指南
- [Tor University Challenge case studies](https://toruniversity.eff.org/case-studies/)：国际的校园案例研究
- [EFF Legal FAQ for Tor relay operators](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)：运营中继的法律常见问题
- 各国校园 Tor Relay 的政策案例（MIT、Stanford、CMU 等）

## 参与方式

社群在 Matrix 讨论（主服务器 `im.anoni.net`），校园 Tor Relay 的讨论集中在社群 Public Space 里的相关 room，账号申请与各项服务的入口见[社群自建服务](/services/)。

特别欢迎具备以下背景的人加入：

- **大学在校生、校友、教职员**：了解自己的学校，能评估推动的可行性
- **网络运维经验**：参与技术配置与长期运维
- **政策沟通能力**：协助与校方、信息中心、法务部门沟通
- **法律专业**：解读中继运营相关的法律疑虑（个人信息、刑事责任、学校规章）
- **活动筹办经验**：把架设工作纳入信息安全周、迎新等校园活动

没有架设过 Tor Relay 也欢迎参与，想学就足以成为加入的理由，社群会结合 [Tor Relay 架设指南](/join/setup-tor-relay/)协助你实际操作。

## 议题守则

社群的所有讨论以合法用途为前提，校园 Tor Relay 主题以教育、研究与参与网络基础设施建设为目的，不协助任何违法行为。校园架设会使用学校的资源，需走正式的提案与审核流程，并向校方充分说明节点的用途与运营责任。
