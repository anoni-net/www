---
title: Tor 中继节点观测
description: 社群维护的 Pulse 每小时收集台湾与邻近地区的 Tor 中继节点数据，画出中继数量、带宽、所在的自治网络、Tor 版本与角色的变化。
lead: 台湾与邻近地区有多少 Tor 中继，分散在哪些网络。
---

Tor 中继节点是志愿者架设、替全球 Tor 用户转送加密流量的服务器。一个地区运作中的中继越多、带宽越大，本地能提供的转送能量越强。中继分散在越多自治网络（ASN）也越好，全部集中在单一电信商的话，那家网络出问题或被施压时，整批节点会一起受影响。

页面的数据来自社群维护的 [Pulse](https://github.com/anoni-net/pulse)，每小时从 Tor Metrics 的 Onionoo 收集一次，页面也每小时重新生成。默认显示台湾，其他地区当作参照，从下方的地区列表切换。每一季的变化整理在[观测季报](/projects/reports/)。

<!-- pulse -->

## 数据的计算方式

- 每一天取当天最后一次快照，不是整天出现过的所有中继
- 带宽是运作中中继的观测带宽（observed bandwidth）加总
- 中继占全网络的权重是运作中中继的共识权重比例（consensus weight fraction）加总，2026 年 10 月开始收集
- 用户估计来自 [Tor Metrics](https://metrics.torproject.org/userstats-relay-country.html)，每天更新、晚两三天，推算方法与限制见[台湾有多少人在用 Tor](docs:taiwan/tor-users/)
- 中继的角色依 Onionoo 给的概率判断，guard、middle、exit 的概率大于 0 就算在该角色
- 收集中断的日子在图上留下缺口，不补值
- 原始数据可以从 [Pulse 的 API](https://anoni.net/api/readme) 读取，这一页用的是 `/api/summary`

## 架设 Tor 中继节点

- [如何搭建 Tor Relay](docs:community/setup-tor-relay/)
- [Tor Relay 校园建设](/join/relay-on-campus/)：社群 2026 年的三大主题之一
- [用一句中文查 Tor 节点现况](docs:community/onionoo-mcp/)
- [台湾有多少人在用 Tor](docs:taiwan/tor-users/)
