---
title: 个人隐私指引研究专题
description: 匿名网络社区 2026 年三大主题之一，按日常、敏感工作、高风险三种情境整理隐私工具与步骤，包含研究目标、文档站的相关文章、目前进度与参与方式。
---

个人隐私指引是匿名网络社区 anoni.net 2026 年的三大主题之一，与[Tor Relay 校园建立](/join/relay-on-campus/)、[匿名支付](/join/payments-research/)并列。社区按日常使用、敏感工作、高风险三种情境，把隐私工具与操作步骤整理成可以照着做的指引，内容写在文档站，按概念、工具、场景、进阶分层。欢迎有教学、写作、翻译、设计或信息安全背景的人一起参与（见[参与方式](#参与方式)），年度规划与各季进度见 [2026 年度路线图](/join/roadmap-2026/)。

## 独立成一个主题的原因

社区推广 Tor、Tails、OONI 多年，最常被问到的是「下一步该做什么，才能让自己更安全」。要回答这个问题，需要一套按情境分级、可以实际操作的隐私指引。

现有的中文资源多半停留在介绍单一工具或列举技巧，概念、工具、场景三层之间没有串接。读者读完工具页，常常不知道它对应哪一种风险，读完概念或场景页，也不知道该从哪一步开始。社区想把这三层接起来，让读者从知道工具的名称，一路走到在自己的情境下实际采用。

## 2026 研究目标

- **三级威胁模型框架**：把日常使用、敏感工作、高风险三种情境对应的工具与步骤整理成参考表
- **从概念到实践的判断流程**：在威胁模型与工具操作之间补上判断的依据，例如何时该提高防护等级、何时不必过度防护
- **常见误区**：拆解 VPN ≠ 匿名、HTTPS ≠ 安全、无痕模式 ≠ 隐私、去中心化 ≠ 匿名这类常见的误解。VPN 与去中心化两项已有专篇（[VPN 的风险与选择](docs:tools/vpn-guide/)、[常被误认为匿名的网络](docs:advanced/mistaken-for-anonymity/)），HTTPS 与无痕模式还没有
- **场景指引**：为记者、社运参与者、家暴受害者、LGBTQ+ 等角色整理实际操作的流程
- **跨主题串接**：把连接层、个人信息与身份、资金流三个面向（见[网络自由为什么重要](docs:basics/internet-freedom/)）整合进个人的隐私规划
- **教材**：把研究成果整理成工作坊与小型聚会可用的教材

## 相关文章

文章按文档站[指南](docs:guides/)的分层，分散在概念、工具、场景、进阶与本地法规各区：

- 概念：[匿名、隐私、假名、机密性的差别](docs:basics/anonymity-vs-privacy/)、[威胁模型如何建立](docs:basics/threat-model/)、[Metadata 是什么，为什么重要](docs:basics/metadata/)、[社交平台怎么收集你的数据](docs:basics/platform-tracking/)、[监控现在做得到什么](docs:basics/surveillance-capability/)、[怎么维持多个网络身分](docs:basics/multiple-identities/)、[浏览器指纹是什么，为什么很难摆脱](docs:basics/browser-fingerprinting/)
- 工具：[什么是匿名网络？](docs:tools/what-is-anonymity-network/)、[什么是 Tor](docs:tools/what-is-tor/)、[什么是 Tails](docs:tools/what-is-tails/)、[Tor Browser 进阶设定](docs:tools/tor-browser-advanced/)、[Tor Snowflake](docs:tools/tor-snowflake/)、[Tails、Whonix、Qubes 的差别](docs:tools/tails-vs-whonix-vs-qubes/)、[GrapheneOS：高度隐私的行动作业系统](docs:tools/grapheneos/)、[匿名通讯工具比较](docs:tools/messaging-comparison/)、[OnionShare](docs:tools/onionshare/)、[什么是 CryptPad](docs:tools/what-is-cryptpad/)、[密码管理器入门](docs:tools/password-manager/)、[邮件别名怎么用，以及它把信任交给谁](docs:tools/email-alias/)、[Asian Diceware，带亚洲味的英文密语字典](docs:tools/asian-diceware/)、[VPN 的风险与选择](docs:tools/vpn-guide/)、[加密 DNS 怎么选、怎么确认真的生效](docs:tools/encrypted-dns/)、[用 AI 工作时怎么避免数据外泄](docs:tools/ai-privacy/)、[手机隐私设置逐步指引](docs:tools/phone-privacy-settings/)
- 小工具：[威胁模型清单](docs:utils/threat-model/)
- 场景：[一般人平常该做到什么](docs:scenarios/everyday-baseline/)、[记者保护消息来源](docs:scenarios/journalist/)、[社运行动者的数字准备](docs:scenarios/activist/)、[家暴受害者的数字准备](docs:scenarios/domestic-violence/)、[LGBTQ+ 与性少数的匿名社交](docs:scenarios/lgbtq/)、[选举观察员的自保](docs:scenarios/election-observer/)、[在中国大陆的公开平台传播信息](docs:scenarios/mainland-speech/)、[出差与研讨会的数字准备（东亚与东南亚）](docs:scenarios/asia-travel/)、[出国的手机号与网络连接](docs:scenarios/travel-connectivity/)、[出国前数字安全：用 AI 自助生成目的地概况](docs:scenarios/travel-ai-briefing/)
- 进阶：[端对端加密如何运作](docs:advanced/e2ee/)、[常被误认为匿名的网络](docs:advanced/mistaken-for-anonymity/)、[后量子密码概观](docs:advanced/post-quantum/)、[去中心化网站发布](docs:advanced/dweb-ipfs-onion/)
- 本地法规：[台湾个资法 2025 修法](docs:taiwan/pdpa-2025/)、[揭弊者保护法的技术观察](docs:taiwan/whistleblower-law/)

各篇初稿大多已上线，之后按季度节奏校订与补充。

## 已完成的工作

- **概念层九篇**：[网络自由为什么重要](docs:basics/internet-freedom/)、[匿名、隐私、假名、机密性的差别](docs:basics/anonymity-vs-privacy/)、[威胁模型如何建立](docs:basics/threat-model/)、[Metadata 是什么，为什么重要](docs:basics/metadata/)、[为什么匿名支付重要](docs:basics/payments-anonymity/)、[社交平台怎么收集你的数据](docs:basics/platform-tracking/)、[监控现在做得到什么](docs:basics/surveillance-capability/)、[怎么维持多个网络身分](docs:basics/multiple-identities/)、[浏览器指纹是什么，为什么很难摆脱](docs:basics/browser-fingerprinting/)
- **三个面向的框架**：在[网络自由为什么重要](docs:basics/internet-freedom/)一文确立连接层、个人信息与身份、资金流三个面向，作为个人隐私指引的整体架构
- **本地法规参考**：[台湾个资法 2025 修法](docs:taiwan/pdpa-2025/)、[揭弊者保护法的技术观察](docs:taiwan/whistleblower-law/)两篇已完成
- **写作规范与分类**：制定[写作风格规范](/join/writing-style/)，文档站整理成七大分类并建立[指南](docs:guides/)入口页，读者可以按层次找到对应的文章

## 进行中的工作

- **各层文章的校订**：工具、场景、进阶各层的初稿已上线，按读者反馈持续校订与补充
- **常见误区的补完**：HTTPS ≠ 安全、无痕模式 ≠ 隐私两项还没有专篇
- **三级隐私指引合集**：本主题的核心交付物，原定 2026 年第三季整合上述各层的内容
- **工作坊教材**：把研究成果转成工作坊与小型聚会用的讲义
- **外部资源的翻译**：候选清单见下一节

## 翻译候选与延伸阅读

社区标记了几份候选的外部资源，欢迎志愿者协助翻译或摘录重点：

- [EFF Surveillance Self-Defense](https://ssd.eff.org/)：EFF 的个人数字安全指南，有完整的威胁模型分级与工具教学
- [Privacy Guides](https://www.privacyguides.org/)：开源社区维护的隐私工具推荐清单
- [The Citizen Lab](https://citizenlab.ca/)：监控软件与跨国威胁的实证研究
- [Security in a Box](https://securityinabox.org/)：给 NGO 与行动者的数字安全工具箱
- [Tor Project 的用户支持文档](https://support.torproject.org/zh-CN/)

## 参与方式

社区在 Matrix 讨论（主服务器 `im.anoni.net`），个人隐私指引的讨论集中在社区 Public Space 里的相关 room。协作文档用 CryptPad，定期的视频会议用 Jitsi，账号申请与各项服务的入口见[服务](/services/)。

特别欢迎具备以下背景的人加入：

- **教学推广或工作坊带领经验**：把技术概念转成一般人能理解的内容
- **写作或翻译经验**：整理篇幅较长的技术资源
- **UX 或设计背景**：把指引可视化，例如流程图、分级对照表
- **一线实务经验**（记者、NGO 工作者、社运参与者）：知道指引最常缺少哪些内容
- **信息安全背景**：审稿，确认技术描述正确

不需要信息安全背景也欢迎参与，想学就足以成为加入的理由。

2026 年 9 月 6 日，社区在葡萄牙 Estoril 的 [Global Gathering 2026](/events/gg2026/) 设摊，想在现场收集的反馈之一，是哪些隐私指引没有考虑到区域的实际处境。

## 议题守则

社区的所有讨论以合法用途为前提。个人隐私指引以教育与理解风险为目的，不协助逃避法律责任、骚扰、跟踪或其他违法行为。涉及具体个案的法律问题请咨询专业人士，社区成员的观察不能取代法律意见。
