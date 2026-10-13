---
title: OONI 測項速查表
description: ooni/spec 收錄的 41 個網路測項的量測內容、資料產出狀況與台灣的觀測情形，附上游規格連結，供挑選測項或解讀資料時對照。
---

[ooni/spec](https://github.com/ooni/spec/tree/master/nettests) 的 `nettests` 目錄收錄 41 份測項規格，其中相當比例已停止使用。挑選測項或解讀既有資料時，先確認哪些測項仍在產出資料，比逐份閱讀規格更有效率。

測項輸出的共通欄位另外定義在上游的 [data-formats](https://github.com/ooni/spec/tree/master/data-formats)。

!!! info "狀態欄位的定義"

    **spec 狀態**取自各份規格開頭的 `_status_` 標記，分為 `current`、`experimental`、`obsolete` 三種，反映上游對該測項的定位。

    **資料流通**是實測結果，以撰稿當日（2026-08-04）為快照，透過 [OONI API](https://api.ooni.org/api/v1/measurements) 盤點各測項最近的公開測量。

    **台灣**欄位來自 S3 公開資料集，抽查 2026-08-03 的五個時段，列出台灣的目錄底下出現過的測項。

## 狀態標記與實際資料的落差

規格的狀態標記與實際資料不一致的情況分成兩種：

- **標為 `current` 卻查不到資料**：`tlsmiddlebox`、`portfiltering`、`captiveportal` 三個。
- **標為 `experimental` 卻每日都有資料**：`dnscheck`、`echcheck`、`openvpn`、`stunreachability`、`vanilla_tor` 等，資料量與部分 `current` 測項相當。

`experimental` 只代表規格本身的成熟度，與資料量多寡沒有必然關係。要判斷測項是否適合用於分析，直接向 API 查詢是否有資料，比狀態標記可靠。

## 測項的用途分群

依觀測目的分群如下（各測項的細節見後方表格）：

- **網站封鎖偵測**：`web_connectivity`
- **中間設備與干擾手法**：`http_header_field_manipulation`、`http_invalid_request_line`、`sni_blocking`、`echcheck`
- **通訊軟體可達性**：`telegram`、`whatsapp`、`signal`、`facebook_messenger`
- **規避工具可用性**：`tor`、`vanilla_tor`、`torsf`、`psiphon`、`riseupvpn`、`openvpn`
- **DNS 行為**：`dnscheck`、`dnsping`
- **連線效能**：`ndt`、`dash`、`stunreachability`、`quicping`

## 仍在產出資料的測項

下表的測項在撰稿當日都可以查到公開測量，也是解讀 OONI 資料時最常遇到的測項。

| 測項 | 量測內容 | spec 狀態 | 台灣 |
|---|---|---|---|
| [`web_connectivity`](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md) | 網站可達性與封鎖判定，資料量最大的測項 | current | 有 |
| [`tor`](https://github.com/ooni/spec/blob/master/nettests/ts-023-tor.md) | Tor 目錄權威節點與橋接的可達性 | current | 有 |
| [`vanilla_tor`](https://github.com/ooni/spec/blob/master/nettests/ts-016-vanilla-tor.md) | 未經偽裝的 Tor 能否順利啟動連線 | experimental | 有 |
| [`torsf`](https://github.com/ooni/spec/blob/master/nettests/ts-030-torsf.md) | 透過 Snowflake 傳輸層的 Tor 連線 | experimental | 無 |
| [`telegram`](https://github.com/ooni/spec/blob/master/nettests/ts-020-telegram.md) | Telegram 網頁版與資料中心端點可達性 | current | 有 |
| [`whatsapp`](https://github.com/ooni/spec/blob/master/nettests/ts-018-whatsapp.md) | WhatsApp 端點與註冊服務可達性 | current | 有 |
| [`signal`](https://github.com/ooni/spec/blob/master/nettests/ts-029-signal.md) | Signal 服務端點可達性 | current | 有 |
| [`facebook_messenger`](https://github.com/ooni/spec/blob/master/nettests/ts-019-facebook-messenger.md) | Facebook Messenger 端點可達性 | current | 有 |
| [`dnscheck`](https://github.com/ooni/spec/blob/master/nettests/ts-028-dnscheck.md) | 指定 DNS 解析器的行為，涵蓋加密查詢（DoH、DoT） | experimental | 有 |
| [`dnsping`](https://github.com/ooni/spec/blob/master/nettests/ts-035-dnsping.md) | DNS 查詢的延遲與回應行為 | experimental | 無 |
| [`echcheck`](https://github.com/ooni/spec/blob/master/nettests/ts-039-echcheck.md) | 加密用戶端問候（ECH）的支援與干擾狀況 | experimental | 有 |
| [`http_header_field_manipulation`](https://github.com/ooni/spec/blob/master/nettests/ts-006-header-field-manipulation.md) | 中間設備是否竄改 HTTP 標頭 | current | 有 |
| [`http_invalid_request_line`](https://github.com/ooni/spec/blob/master/nettests/ts-007-http-invalid-request-line.md) | 中間設備對異常請求行的反應，用於偵測透明代理 | current | 有 |
| [`openvpn`](https://github.com/ooni/spec/blob/master/nettests/ts-040-openvpn.md) | OpenVPN 握手能否完成 | experimental | 有 |
| [`psiphon`](https://github.com/ooni/spec/blob/master/nettests/ts-015-psiphon.md) | Psiphon 規避工具能否建立連線 | current | 有 |
| [`riseupvpn`](https://github.com/ooni/spec/blob/master/nettests/ts-026-riseupvpn.md) | RiseupVPN 服務可達性 | current | 有 |
| [`stunreachability`](https://github.com/ooni/spec/blob/master/nettests/ts-025-stun-reachability.md) | STUN 伺服器可達性，牽動 WebRTC 通話 | experimental | 有 |
| [`ndt`](https://github.com/ooni/spec/blob/master/nettests/ts-022-ndt.md) | 連線速度與效能診斷 | current | 有 |
| [`dash`](https://github.com/ooni/spec/blob/master/nettests/ts-021-dash.md) | 影音串流播放品質 | current | 有 |
| [`browser_web`](https://github.com/ooni/spec/blob/master/nettests/ts-036-browser_web.md) | 以真實瀏覽器引擎載入網頁 | experimental | 無 |

!!! note "表中出現的縮寫"

    - **DoH、DoT**：把 DNS 查詢包在 HTTPS 或 TLS 裡傳送，避免查詢內容以明文經過網路（詳見[加密 DNS](docs:tools/encrypted-dns/)）。
    - **ECH（Encrypted Client Hello）**：TLS 握手的第一個訊息原本會以明文帶出連線目標的網域名稱，ECH 把該欄位加密。
    - **SNI（Server Name Indication）**：TLS 握手時以明文送出的目標網域名稱，常被當作封鎖的判斷依據。
    - **STUN**：協助裝置找出自己對外 IP 與埠號的協定，WebRTC 通話建立連線時會用到。
    - **QUIC**：以 UDP 為基礎的傳輸協定，HTTP/3 建立在其上。

## 偶爾才有資料的測項

| 測項 | 量測內容 | spec 狀態 | 最近一筆 |
|---|---|---|---|
| [`quicping`](https://github.com/ooni/spec/blob/master/nettests/ts-031-quicping.md) | QUIC 協定的可達性 | experimental | 2026-07-30 |
| [`sni_blocking`](https://github.com/ooni/spec/blob/master/nettests/ts-024-sni-blocking.md) | 針對 TLS SNI 欄位的封鎖偵測 | experimental | 2026-07-20 |

## 查不到公開資料的測項

下表七個測項在 API 查不到公開測量，規格仍保留在上游倉庫，設計新測項或研究方法時可以參考。

| 測項 | 量測內容 | spec 狀態 |
|---|---|---|
| [`tlsmiddlebox`](https://github.com/ooni/spec/blob/master/nettests/ts-037-tlsmiddlebox.md) | TLS 連線路徑上的中間設備行為 | current |
| [`portfiltering`](https://github.com/ooni/spec/blob/master/nettests/ts-038-port-filtering.md) | 特定連接埠是否被過濾 | current |
| [`captiveportal`](https://github.com/ooni/spec/blob/master/nettests/ts-010-captive-portal.md) | 是否處於需要登入的受控網路 | current |
| [`urlgetter`](https://github.com/ooni/spec/blob/master/nettests/ts-027-urlgetter.md) | 供其他測項複用的通用抓取元件 | experimental |
| [`tcpping`](https://github.com/ooni/spec/blob/master/nettests/ts-032-tcpping.md) | TCP 層的往返延遲 | experimental |
| [`tlsping`](https://github.com/ooni/spec/blob/master/nettests/ts-033-tlsping.md) | TLS 握手的往返延遲 | experimental |
| [`simplequicping`](https://github.com/ooni/spec/blob/master/nettests/ts-034-simplequicping.md) | QUIC 的簡化延遲量測 | experimental |

## 標記為 obsolete 的歷史測項

上游標為 `obsolete` 的有 12 份，多數功能已被 `web_connectivity` 吸收，或隨測量方法演進而退場。處理歷史資料時仍可能遇到這些測項的紀錄，規劃新的觀測則不必採用。

| 測項 | 規格 |
|---|---|
| bridgeT | [ts-001](https://github.com/ooni/spec/blob/master/nettests/ts-001-bridget.md) |
| DNS Consistency | [ts-002](https://github.com/ooni/spec/blob/master/nettests/ts-002-dns-consistency.md) |
| HTTP Requests | [ts-003](https://github.com/ooni/spec/blob/master/nettests/ts-003-http-requests.md) |
| HTTP Host | [ts-004](https://github.com/ooni/spec/blob/master/nettests/ts-004-http-host.md) |
| DNS Spoof | [ts-005](https://github.com/ooni/spec/blob/master/nettests/ts-005-dns-spoof.md) |
| TCP Connect | [ts-008](https://github.com/ooni/spec/blob/master/nettests/ts-008-tcp-connect.md) |
| Multi Protocol Traceroute | [ts-009](https://github.com/ooni/spec/blob/master/nettests/ts-009-multi-protocol-traceroute.md) |
| Bridge Reachability | [ts-011](https://github.com/ooni/spec/blob/master/nettests/ts-011-bridge-reachability.md) |
| DNS Injection | [ts-012](https://github.com/ooni/spec/blob/master/nettests/ts-012-dns-injection.md) |
| Lantern | [ts-013](https://github.com/ooni/spec/blob/master/nettests/ts-013-lantern.md) |
| Meek Fronted Requests | [ts-014](https://github.com/ooni/spec/blob/master/nettests/ts-014-meek-fronted-requests.md) |
| OpenVPN Client Test（舊版） | [ts-016](https://github.com/ooni/spec/blob/master/nettests/ts-016-openvpn.md) |

!!! note "重複的 ts-016 編號與新舊 OpenVPN 規格"

    上游有兩份規格同編為 `ts-016`，分別是上表標為 `obsolete` 的 `ts-016-openvpn.md` 與標為 `experimental` 的 `ts-016-vanilla-tor.md`。現行的 OpenVPN 測項規格是 `ts-040-openvpn.md`，引用時留意不要誤用舊版。

## 台灣觀測到的測項

抽查 2026-08-03 的五個時段，台灣的目錄底下出現過 17 個測項（以下用 API 的底線寫法）：`web_connectivity`、`tor`、`vanilla_tor`、`telegram`、`whatsapp`、`signal`、`facebook_messenger`、`dnscheck`、`echcheck`、`http_header_field_manipulation`、`http_invalid_request_line`、`openvpn`、`psiphon`、`riseupvpn`、`stunreachability`、`ndt`、`dash`。

S3 上的目錄名與測項名稱欄位（`test_name`）的寫法不同，目錄名沒有底線（`webconnectivity`、`vanillator`、`facebookmessenger`）。API 查詢要用底線形式（`web_connectivity`、`vanilla_tor`、`facebook_messenger`），取用路徑的細節見[ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)。

台灣目前的觀測集中在 `web_connectivity`，其他測項的樣本量偏小。擴充在地觀測的涵蓋面時，`tor` 與 `dnscheck` 是與社群既有主題最接近的兩個方向。

要執行特定測項，可以在 [OONI Probe](https://ooni.org/install/) 桌面版或行動版的設定中挑選啟用的測項。要邀集他人共同測試固定的網址清單，則用 [OONI Run v2](docs:tools/ooni-run-v2/) 建立連結分享，社群目前維運的連結 ID 是 `10328`。

## 相關閱讀

- [OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)：一筆 OONI 測量的欄位組成與閱讀方式
- [OONI 的封鎖判定方式](/projects/asn-coverage/ooni-blocking-determination/)：OONI 如何判定一個網站遭到封鎖
- [ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)：觀測資料的取用路徑與分析方式
- [OONI Run v2 操作說明](docs:tools/ooni-run-v2/)：建立與分享測試連結的方式
- [什麼是 OONI](docs:tools/what-is-ooni/)：OONI 的入門介紹
