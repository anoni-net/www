---
title: InterSecLab MADLink 报告的正体中文翻译
description: InterSecLab 的 MADLink 报告指出，凌华科技在 2019 至 2020 年出货的 1,708 台 CSA-7400 成了 Geedge 第一代防火墙平台的硬件基底。社区的正体中文翻译放在文档站，另附报告发布后台湾反应的观察记录。
date: 2026-05-23
kind: new
---

![MADLink 报告封面](https://interseclab.org/wp-content/uploads/2026/04/MADLink-A-Taiwanese-Vestige-in-the-Geedge-Suply-Chain.jpg){ .shot }

一家台湾上市公司出货的网络设备，最后在哈萨克斯坦成了国家级网络审查与监控系统的核心。InterSecLab 的 MADLink 报告追查了这条供应链，匿名网络社区 anoni.net 已完成正体中文翻译，收在文档站的[研究报告中译](https://anoni.net/docs/reports/)（中译只有正体中文版）。

设备来自凌华科技（ADLINK Technologies，股票代号 6166），客户是中国公司 Geedge Networks（积至公司），旗舰产品「天狗安全网关（Tiangou Secure Gateway，TSG）」的能力可与中国防火长城相比。报告〈[MADLink: A Taiwanese Vestige in the Geedge Supply Chain](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)〉在 2026 年 4 月发布，是 InterSecLab 继 2025 年 9 月的《[The Internet Coup](https://anoni.net/docs/reports/interseclab-network-coup/)》之后，对 Geedge 供应链的第一篇延伸调查。


## 报告的主要发现

凌华在 2019 至 2020 年间出货给 Geedge 的 1,708 台 CSA-7400，构成 Geedge 第一代防火墙平台的硬件基底，部署在哈萨克斯坦，用于国家层级的网络审查与监控。CSA-7400 是高密度 4U 设备，凌华自家的营销定位就是深度数据包检测（DPI）与防火墙。

凌华的硬件也出现在 Geedge 部署于缅甸的 EtherFabric 里。EtherFabric 是定制的网络数据包代理设备（network packet broker，NPB），用来在多个 TSG 节点之间分散流量。泄露文件中的一组 MAC 地址可以追溯到凌华，显示凌华在 Geedge 产品线中的角色不只单笔 CSA-7400 交易。

Geedge 当前一代的 TSG 部署在埃塞俄比亚、巴基斯坦和缅甸，服务器来自中科曙光（Sugon，已遭美国制裁）旗下的 Nettrix，存储设备来自浪潮（Inspur）。这些标准 x86 元件即使直接采购受限，仍可从二手市场取得。报告的结论是，为监控用途设计的专用硬件（CSA-7400、EtherFabric 里的凌华元件）才是出口管制最能发挥效果的对象。

## 中译的章节

完整中译在文档站的 [MADLink 报告中译](https://anoni.net/docs/reports/interseclab-madlink/)。原报告是单页长文，翻译团队依主题切成 5 章，方便在 Matrix 上分章节讨论：

- [第 1/5 章：摘要与主要发现](https://anoni.net/docs/reports/interseclab-madlink/index_1/)
- [第 2/5 章：Geedge 供应链深入解析（三代 TSG 硬件）](https://anoni.net/docs/reports/interseclab-madlink/index_2/)
- [第 3/5 章：EtherFabric 与 ADLINK 的角色和回应](https://anoni.net/docs/reports/interseclab-madlink/index_3/)
- [第 4/5 章：结论](https://anoni.net/docs/reports/interseclab-madlink/index_4/)
- [第 5/5 章：附录（凌华科技与经济部完整声明）](https://anoni.net/docs/reports/interseclab-madlink/index_5/)

凌华与经济部国际贸易署的回应全文都收在附录，读者可以自行比对双方的说法。

## 台湾反应的观察记录

MADLink 点名了一家台湾上市公司，照理会引来本地媒体追问、立委质询与主管机关回应，截至 2026-05-20，台湾中文公共领域的反应却明显偏少。我们把查证过程、媒体的报道与主管机关的回应整理成另一篇[观察记录](/updates/2026/05/madlink-editorial-2026-05/)，以当天的快照发布。

## 致谢与讨论频道

感谢 InterSecLab 持续推动这个系列调查，也感谢投入翻译与观察整理的社区成员。

《The Internet Coup》与《MADLink》两份报告的讨论都在同一个 [Matrix 讨论频道](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net)，发现相关的新报道、政府文件或公开发言，欢迎到频道分享。

## 相关阅读

- [MADLink 报告中译](https://anoni.net/docs/reports/interseclab-madlink/)
- [台湾对 MADLink 报告的反应，2026 年 5 月的观察记录](/updates/2026/05/madlink-editorial-2026-05/)
- [The Internet Coup 报告中译](https://anoni.net/docs/reports/interseclab-network-coup/)
- [InterSecLab 网络政变报告的正体中文翻译](/updates/2025/10/report-the-internet-coup/)
