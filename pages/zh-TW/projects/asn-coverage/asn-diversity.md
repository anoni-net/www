---
title: ASN 多樣性與台灣的觀測缺口
description: 台灣 OONI 測量來源集中在少數 ASN 的現況與數字、補足覆蓋的參與方式，以及單筆測量資料的解讀。
---

OONI Probe 在台灣的測量數量不少，但如果絕大多數來自同一兩家電信商，整體觀測只能反映那幾家的網路狀況，無法代表台灣完整的連線環境。某個網站若只在特定一家電信商被封鎖，而那家剛好沒有人在測，這次封鎖就不會留下紀錄。測量來源的 ASN（自治系統編號）多樣性不足，是台灣 OONI 觀測資料目前最明確的問題之一。測哪些網站由檢測清單決定（見[OONI 網站檢測清單的維護](/join/ooni-test-list/)），本頁整理測量來自哪些網路。

## 以 ASN 為單位的觀測

網際網路由許多自治系統（Autonomous System，AS）相互連結而成。電信商、學術機構、企業與 CDN 業者各自管理的網路群組都是一個 AS，有獨立的路由策略，彼此透過 BGP 交換路由。每個 AS 有一個獨一無二的編號，也就是 ASN。AS 與 BGP 的基本概念見 Cloudflare Learning 的 [What is an autonomous system?](https://www.cloudflare.com/zh-tw/learning/network-layer/what-is-an-autonomous-system/) 與 [What is BGP?](https://www.cloudflare.com/zh-tw/learning/security/glossary/what-is-bgp/)。

對 OONI 觀測來說，ASN 是「在哪一家網路上看到審查」的最小單位。同一個網站可能在中華電信無法連線、在台灣大哥大正常，要以 ASN 為單位才能區分這種差異。OONI 的分析因此常看一個地區的測量來自多少個不同的 ASN，比例越高，越能反映該地區整體的連線環境。

查詢自己目前連線的 ASN 可以用 [ip.me](https://ip.me/)。[Cloudflare Radar](https://radar.cloudflare.com/zh-tw/as3462) 的 AS 頁面列出單一 ASN 的流量趨勢與歷程（例 AS3462），[Is BGP safe yet?](https://isbgpsafeyet.com/) 可以檢查目前的 ISP 是否做了 RPKI 路由驗證。

## 台灣測量來源的集中程度

[OONI](https://ooni.org/) 的全球志工用 [OONI Probe](https://ooni.org/install/) 檢測網路審查，所有測量結果上傳到專案的[公開資料庫](https://registry.opendata.aws/ooni/)。社群在 2023-11 到 2024-03 用 [ASN Coverage](https://github.com/anoni-net/asn-coverage) 分析 OONI 公開資料，2023-12 的結果如下：

- 台灣的測量數量在 OONI Explorer 排名前十
- 78.94% 的測量集中在 [AS3462（中華電信）](https://radar.cloudflare.com/zh-tw/as3462)與 [AS18041（Taiwan Digital Streaming）](https://radar.cloudflare.com/zh-tw/as18041)
- 台灣約有 437 組 ASN，測量資料裡不重複的 ASN 只占 7.32%

測量數量充足，來源卻集中在兩個 ASN，無法反映台灣完整的網路樣態。三大電信業者、有線電視寬頻、固網與第二類電信（租用電信基礎設施提供服務的業者，例如虛擬行動網路、網路電話轉售）都有覆蓋不足的問題。

2023 年之後的變化見專案首頁的 [OONI 觀測涵蓋率](/projects/asn-coverage/)。頁面每小時依 OONI 最近 60 天的測量重新產生，對照 APNIC 估計的各網路使用者人數，列出使用者多、測量少的網路。2026-10 的資料裡，測量最多的仍是中華電信 HiNet（AS3462），中華電信行動網路（AS17421）有約 16% 的使用者，測量占比卻不到 0.1%。

### 補足覆蓋的參與方式

要補上覆蓋，最直接的做法是讓一台裝置在還沒有人測過的 ASN 上持續執行檢測。社群維運的 OONI Run 連結 `10328` 是現成的入口，行動裝置安裝 [OONI Probe](https://ooni.org/install/mobile) 之後點一次連結即可完成設定，接著讓 OONI Probe 留在背景執行。安裝前需衡量的風險與清單內容見 [OONI Run v2 操作說明](docs:tools/ooni-run-v2/)。

現有測量幾乎都落在少數固網 ASN 上，行動業者與第二類電信的資料最缺乏，使用行動網路的協助者特別有幫助。目前還沒有測量的網路列在 OONI 觀測涵蓋率頁的「還沒有測量的網路」。

## 單筆測量資料的解讀

最快的入門方式是自己用 OONI Probe 產生一筆測量資料：

1. 下載 [OONI Probe](https://ooni.org/install/)（行動裝置或桌面版本）
2. 開啟 OONI Probe，選擇「網站」項目並執行檢測
3. 完成後到「測試結果」找到剛才的網站檢測，檢視是否有「！」或「？」項目
4. 點擊任一「！」或「？」查看可能的檢測問題，其中有「數據」、「在 OONI Explorer 中顯示」連結
5. 點擊連結即可查看原始測量資料

以這筆測量為例：[`20241024185921.623617_TW_webconnectivity_578b6d3845fed2e2`](https://explorer.ooni.org/zh-Hant/m/20241024185921.623617_TW_webconnectivity_578b6d3845fed2e2)

結果是「在 AS3462 上執行檢測失敗」，失敗訊息為 `unknown_failure: dial tcp [scrubbed]: connect: host is down`，表示檢測當時主機沒有回應。「DNS 查詢」段落記錄了 `www.asap.com.tw` 的 DNS `A` 紀錄指向 `60.250.151.72`（AS3462，Chunghwa Telecom Co., Ltd.），查詢結果來自 Cloudflare DNS 的 `162.158.242.36`。

結果頁面沒有完整顯示的細節，可以在「原始測量資料」找到所有檢測項目的原始內容，當作進一步分析的素材。

![OONI Explorer 原始測量資料的畫面](https://assets.anoni.net/www/ooni-raw-data-b3b80fe2.webp)

!!! note "連線端與 DNS 解析端的 ASN"

    OONI Probe 會記錄整個檢測過程。上面的範例透過中華電信的網路連線，DNS 查詢卻由 Cloudflare 回應，原始資料裡的 `probe_asn` 與 `resolver_asn` 因此分屬兩個不同的 ASN。網站受到阻擋而無法連線時，問題出在連線所在的 AS 還是 DNS 解析，需要從這兩個欄位分開判斷。

各欄位的含義見[OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)，判定結果的算法見[OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)，各測項的量測對象見[OONI 測項速查表](/projects/asn-coverage/ooni-nettests-map/)。

## 覆蓋率的自行計算

要自行擷取 OONI 公開資料、計算特定區域的 ASN 覆蓋率，工具的設定與指令見 [ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)，開發環境的準備見[參與開發的環境準備](/join/dev-setup/)。

[<i data-icon="database-search"></i> ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/){ .btn .solid }

## 後續方向

社群接下來計畫依網路類型（行動網路、家用寬頻）分開計算覆蓋率。所需的欄位只在原始測量裡，OONI 的彙總 API 沒有提供，目前只能用 [ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)的工具手動整理。另一個方向是搭配[OONI 網站檢測清單的維護](/join/ooni-test-list/)，同時改善檢測的網站與測量來源的多樣性。

## 相關閱讀

- [OONI 網站檢測清單的維護](/join/ooni-test-list/)：OONI Probe 在台灣使用的網站清單與參與維護的方式
- [OONI 觀測涵蓋率](/projects/asn-coverage/)：每小時更新的各網路使用者數與測量數對照
- [ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)：擷取 OONI 公開資料、計算覆蓋率的命令列工具
- [8/13 北部行動網路降速演練的 OONI 量測號召](/updates/2026/08/ooni-mobile-throttle-drill/)：2026-07 到 08 的測量分布，HiNet 一個網路占 39.3%
- [Tor 中繼節點觀測](/projects/pulse/)：社群的另一個觀測專案
- [網路自由為什麼重要](docs:basics/internet-freedom/)：文件站的入門說明
