---
title: Tor 中繼節點觀測
description: 社群維運的 Pulse 每小時收集臺灣與鄰近地區的 Tor 中繼節點資料，畫出中繼數量、頻寬、所在的自治網路、Tor 版本與角色的變化。
lead: 臺灣與鄰近地區有多少 Tor 中繼，分散在哪些網路。
---

Tor 中繼節點是志工架設、替全球 Tor 使用者轉送加密流量的伺服器。一個地區運作中的中繼越多、頻寬越大，在地能提供的轉送能量越強。中繼分散在越多自治網路（ASN）也越好，全部集中在單一電信商的話，那家網路出問題或被施壓時，整批節點會一起受影響。

頁面的資料來自社群維運的 [Pulse](https://github.com/anoni-net/pulse)，每小時從 Tor Metrics 的 Onionoo 收集一次，頁面也每小時重新產生。預設顯示臺灣，其他地區當作參照，從下方的地區清單切換。每一季的變化整理在[觀測季報](/projects/reports/)。

<!-- pulse -->

## 資料的計算方式

- 每一天取當天最後一次快照，不是整天出現過的所有中繼
- 頻寬是運作中中繼的觀測頻寬（observed bandwidth）加總
- 中繼的角色依 Onionoo 給的機率判斷，guard、middle、exit 的機率大於 0 就算在該角色
- 收集中斷的日子在圖上留下缺口，不補值
- 原始資料可以從 [Pulse 的 API](https://anoni.net/api/readme) 讀取，這一頁用的是 `/api/summary`

## 架設 Tor 中繼節點

- [如何搭建 Tor Relay](docs:community/setup-tor-relay/)
- [Tor Relay 校園建立](/join/relay-on-campus/)：社群 2026 年的三大主題之一
- [用一句中文查 Tor 節點現況](docs:community/onionoo-mcp/)
- [臺灣有多少人在用 Tor](docs:taiwan/tor-users/)
