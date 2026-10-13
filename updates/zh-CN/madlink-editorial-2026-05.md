---
title: 台湾对 MADLink 报告的反应，2026 年 5 月的观察记录
description: MADLink 报告点名台湾上市公司凌华科技之后，台湾媒体、立法院与主管机关的反应，以 2026-05-20 的快照记录，附上查证过程与可跟踪的公开入口。
date: 2026-05-20
---

InterSecLab 的 MADLink 报告点名了一家台湾上市公司，指出它出货的网络设备成了中国公司 Geedge Networks 在哈萨克斯坦部署审查系统的硬件基底。报告追问台湾的出口管制能否阻止本地公司供应监控与审查设备给威权政府，这个问题需要本地的报道、质询与主管机关回应接手。报告发布后将近一个月，台湾中文公共领域的反应明显偏少。

我们把查证过程与当时的观察记录下来，让之后查询这份报告的人可以看到它在台湾的接收背景，也让想持续跟踪的人有一个起点。

!!! note "2026-05-20 的观察快照"

    本文是 anoni.net 编辑团队在 2026-05-20 的观察整理（2026-05-16 初版，05-20 补上外部交叉验证），不属于 InterSecLab 原报告的内容。发布之后没有持续更新，文中提到的状态都以快照日为准。报告翻译本体在文档站的 [MADLink 报告中译](https://anoni.net/docs/reports/interseclab-madlink/)（中译只有正体中文版）。


## 外部交叉验证

报告点名一家上市公司，并引述一连串技术细节。记录台湾的反应之前，我们先对报告的关键事证做了一轮独立查证，读者也可以照着重现。

### EtherFabric 的 MAC 地址前缀

IEEE OUI `00:30:64` 登记在 ADLINK Technology, Inc. 名下，这个硬件指纹是报告把 EtherFabric 与凌华连在一起的依据，也是整份报告最容易自行验证的线索。通过 macvendors.com（[`api.macvendors.com/00:30:64`](https://api.macvendors.com/00:30:64)）与 macvendorlookup.com（[`api.macvendorlookup.com/api/v2/003064`](https://www.macvendorlookup.com/api/v2/003064)）查询，两个独立来源都返回「ADLINK TECHNOLOGY, INC.」，登记地址是凌华在新北市中和区的旧址。查询结果从硬件层级证实了 EtherFabric 管理接口的 MAC 地址来自凌华设备。

### CSA-7400 的产品定位

凌华主张 CSA-7400 是通用平台，报告反驳的依据是这款产品本身的市场定位。在凌华中英文官网的[产品页](https://www.adlinktech.com/Products/Network_Security_Appliance/4UNetworkAppliance/CSA-7400?lang=en)上，CSA-7400 归在「Network Security Appliance」底下，营销为 DPI、IDS/IPS、DDoS、NGFW 用途的 carrier-grade 设备。manualzz 上的 [Quick Start Manual](https://manualzz.com/doc/55701658/adlink-technology-csa-7400-quick-start-manual) 也载明出货时预装 CentOS 7，与报告描述 TSG-OS 早期以 CentOS 为基础的细节一致。

### Geedge 的创立背景

积至（海南）信息技术有限公司在 2018 年于海南创立。维基百科的[积至信息](https://zh.wikipedia.org/wiki/%E7%A7%AF%E8%87%B3%E4%BF%A1%E6%81%AF)条目、[大纪元 2025-09-13 的报道](https://www.epochtimes.com/b5/25/9/13/n14593857.htm)与[新唐人的报道](https://www.ntdtv.com/b5/2025/09/13/a104019706.html)，可以互相印证公司的基本信息、创办人背景，以及与中国科学院信息工程研究所 MESA 实验室的同源关系。

### New Bloom Magazine 的报道

我们引用的 New Bloom Magazine 报道确实存在，标题是「[Taiwanese Company Implicated in Great Firewall Supply Chain By Report](https://newbloommag.net/2026/04/29/tw-adlink-geedge/)」，发布时间为 2026-04-29 07:41 UTC。

## 媒体的报道

### 国际与英文媒体

- InterSecLab 的[原报告](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)（2026-04）接续 2025-09 的〈[The Internet Coup](https://interseclab.org/research/the-internet-coup/)〉，是这个系列调查的第一手研究。
- [New Bloom Magazine](https://newbloommag.net/2026/04/29/tw-adlink-geedge/)（破土，以台湾议题为主的英文媒体，2026-04-29）是快照日前唯一明确聚焦凌华与 Geedge 关联的台湾相关独立媒体报道。文中也提到 Geedge 是中国公司，台湾政府对涉及中国的案子通常会有反应，这次却意外安静。
- cybernews、osnews、Daily Security Review 等国际科技与信息安全媒体，多数延续 2025-09 Geedge 500GB 泄露事件的报道框架，没有特别着墨凌华这个台湾供应链节点。

### 台湾中文媒体

用「凌華 Geedge」、「MADLink 凌華」、「凌華 哈薩克」等正体关键字跨媒体搜索，联合、自由、中央社、TVBS、TechNews、iThome 等台湾主流媒体，截至 2026-05-20 都没有直接报道 MADLink，或凌华、Geedge、哈萨克斯坦这条线。[TechNews 科技新报](https://infosecu.technews.tw/2025/09/14/china-geedge-mesa-leak-analyzing-the-great-firewall-largest-document-leak/)在 2025-09 写过防火长城 500GB 泄露事件本身，没有后续跟踪凌华的供应链。同一段时间，凌华的中文新闻集中在边缘 AI 接单、Taiwan Excellence 奖项与 CYBERSEC 2026 参展等业务话题。

## 主管机关、立法院与凌华的回应

经济部国际贸易署回复 InterSecLab 时，说明台湾的战略性高科技货品出口管制以防止大规模毁灭性武器扩散为目的。管制货品清单参照四大国际出口管制机制，实体清单参照联合国安理会与伙伴国家的制裁清单。对于个案，国贸署以法律限制为由，不揭露涉及个别公司的信息（全文见报告翻译的[附录](https://anoni.net/docs/reports/interseclab-madlink/index_5/)）。

原报告引述了一位立委的主张，认为台湾应建立自己的实体清单，不只依赖美国与欧盟的清单，并订出更清楚的标准，厘清组件制造商在什么情况下需要对最终用途负责。在立法院议事系统、社交平台与媒体采访记录里，截至快照日都找不到这位立委就此议题进一步发言的记录。

凌华在 2025 年 11 月 14 日回复 InterSecLab 的声明里写了将启动内部审计，全文同样收在报告翻译的附录。在[公开资讯观测站](https://mopsov.twse.com.tw/)以代号 6166 查询，截至 2026-05-20，没有针对 Geedge、CSA-7400 出货案或内部审计的重大讯息公告。

## 台湾反应偏少的可能原因

以下是编辑团队整理的可能因素，属于观察，不是定论，欢迎补充与反驳。

- **技术门槛**：一般财经与政治记者要把 CSA-7400、深度数据包检测、Geedge TSG 与出口管制串成一条线并不容易，缺少本地的技术背景材料与翻译，写出符合台湾读者语境的报道成本很高。
- **信息安全媒体的报道重心**：iThome、资安人这类媒体以企业信息安全采购与技术趋势为主，「台湾零部件用于威权监控」的题目不在报道习惯里。
- **新闻热度**：MADLink 在 2026-04 才具体点名凌华，Geedge 泄露事件的新闻热度在 2025 年底已经消退，台湾媒体没有把这条线当成持续跟踪的题材。
- **公民团体的关注重心**：关注信息与数字人权的台湾公民团体，近年主要投入中国对台信息战、假消息治理与数字平台责任，较少把监控科技出口的人权审查当成主要议题。anoni.net 翻译 MADLink 报告，也是想补上这个位置。

## 制度面的缺口

报告的结论是，台湾的出口管制框架以防扩散为主轴，没有涵盖把具监控能力的科技出口给供应威权政府的厂商。缺少报道、质询与公民团体倡议的情况下，主管机关没有修补框架的压力，凌华也没有对外揭露内部审计进度的压力。

## 可跟踪的公开入口

### 政府与制度

**经济部国际贸易署**

- 入口：[战略性高科技货品出口实体管制清单](https://publicinfo.trade.gov.tw/icp/exportList.html)、[国贸署新闻稿](https://www.trade.gov.tw/Pages/List.aspx?nodeID=40)
- 观察重点：是否把监控与审查设备的供应商纳入实体清单、是否引入针对最终用途的审查机制、跨部会审查会议是否就此案公开结论

**立法院**

- 入口：[立法院 IVOD](https://ivod.ly.gov.tw/)、[立法院议事暨公报资讯网](https://lci.ly.gov.tw/)、[立法院议事整合资讯网](https://ppg.ly.gov.tw/ppg/)
- 观察重点：原报告引述的立委或其他立委（特别是经济、外交及国防、司法及法制委员会）是否就此议题提出书面质询、口头质询、提案或新闻稿，委员会是否邀请主管机关列席报告

**金管会与证交所（凌华为上市公司）**

- 入口：[公开资讯观测站](https://mopsov.twse.com.tw/)代号 6166（重大讯息、年报、ESG 报告）
- 观察重点：凌华是否公告与 Geedge 出货案相关的重大讯息、是否在 2026 年年报或可持续发展报告揭露此案与内部审计结果、业绩说明会上是否被分析师问到

**监察院**

- 入口：[监察院](https://www.cy.gov.tw/)的纠正案公告
- 观察重点：是否就主管机关在出口合规审查中未辨识最终用途一事，提出纠正或纠举

### 媒体与公民团体

- 中文媒体：过去报道过防火长城、中国信息安全或出口管制议题的科技媒体与调查报道媒体，是否有后续跟踪
- 公民团体：关注数字人权、开放政府与经贸政策的公民团体，是否就此议题发起联署、座谈或政策倡议

### 跟踪方式与成本

| 方式 | 一次性成本 | 持续成本 | 做法 |
|---|---|---|---|
| Google Alerts | 10 分钟 | 0 | 设置「凌華 Geedge」、「ADLINK Geedge」、「戰略性高科技貨品 監控」等正体关键字，命中时收到 email 通知 |
| 手动巡查 | 0 | 每月约 30 分钟 | 社区轮值，依上面的入口逐一检查，结果回报到 Matrix 频道 |
| RSS 或 HTML diff bot | 1–2 小时设置 | 0 | 把国贸署新闻稿、公开资讯观测站 6166 的公告转进社区的 Matrix 频道 |
| 自动化爬虫 | 4–6 小时设置 | 0 | 定期抓取实体清单与重大讯息页面，内容有变动时自动开 GitHub Issue |

四种方式可以混用，成本最低的组合是 Google Alerts 加上手动巡查。出现具体信号之后（例如国贸署更新框架、立委公开质询、凌华发布重大讯息），再考虑加上自动化监测。

## 补充材料

本文以 2026-05-20 的快照发布，之后不再更新。如果你发现本文没有收录的报道、政府文件或公开发言，欢迎到 [Matrix 讨论频道](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net)分享。

## 相关阅读

- [MADLink 报告中译](https://anoni.net/docs/reports/interseclab-madlink/)
- [InterSecLab MADLink 报告的正体中文翻译](/updates/2026/05/report-madlink/)
- [The Internet Coup 报告中译](https://anoni.net/docs/reports/interseclab-network-coup/)

*[ADLINK]: 凌华科技股份有限公司（ADLINK Technology, Inc.），台湾上市公司，股票代号 6166。
*[Geedge Networks]: 积至公司，中国的网络公司，研发、部署并对外出口互联网审查与监控技术。
*[Geedge]: 积至公司。
*[CSA-7400]: 凌华科技的高密度 4U 网络平台设备，厂商营销定位用于防火墙与深度数据包检测。
*[TSG]: 天狗安全网关（Tiangou Secure Gateway），Geedge Networks 的旗舰审查与监控产品。
