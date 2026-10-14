---
title: OONI 的封鎖判定方式
description: 網路連線測試（Web Connectivity）的 blocking 欄位如何計算、四種判定各自對應的證據，以及 blocking 有值與確認封鎖之間的差距，附五筆實際測量的判讀與常見的誤判來源。
---

`blocking` 記錄的是單次測量與對照組不一致，離確認封鎖還有一段距離，因此在多數情況下，單憑 `blocking: "dns"` 不足以斷定某個網站在台灣被封鎖。

各欄位在測量資料裡的位置見[OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)。

## 雙邊對照的判定機制

只靠 Probe 單方面測一個網站，無法區分「網站遭到干預」與「網站本身無法連線」。網路連線測試（`web_connectivity`）因此把同一個網址測兩次，分別從 Probe 所在的網路與 OONI 的 test helper 所在的外部網路發出，再比對兩邊的結果。

test helper 是 OONI 架設在外部網路的測量伺服器，觀測結果放在 `test_keys.control` 底下，包含 DNS 解析結果、TCP 連線狀態與 HTTP 回應。判定欄位的值全部取決於兩邊的差異出現在哪個階段。比對依下列順序逐階段進行，停在第一個出現差異的階段：

<ol class="flow" aria-label="網路連線測試的四個判定階段">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>DNS 解析</b><span class="d">比對兩邊對同一個網域的 A 與 AAAA 查詢結果</span><span class="out"><span class="if">解析結果不一致</span><code>blocking: "dns"</code></span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>TCP 連線</b><span class="d">兩邊能否連上目標 IP 的連接埠</span><span class="out"><span class="if">只有 Probe 無法連線</span><code>blocking: "tcp_ip"</code></span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>HTTP 請求</b><span class="d">連線建立之後，能否取得 HTTP 回應</span><span class="out"><span class="if">HTTP 階段失敗</span><code>blocking: "http-failure"</code></span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>回應內容</b><span class="d">比對狀態碼、標題、標頭與內容長度</span><span class="out"><span class="if">內容與 test helper 不同</span><code>blocking: "http-diff"</code></span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>四個階段都一致</b><span class="out"><code>blocking: false</code><code>accessible: true</code></span></span></li>
</ol>

比對在更早的階段就已中止，所以前三種判定的四個 `*_match` 欄位全為 `null`。下一節的四筆實際測量各自對應一個階段。

!!! tip "`control` 與 `blocking` 的判讀順序"

    `blocking` 是雙邊比對的結果，並非 Probe 單方面的觀測。判讀異常測量時，先確認 `test_keys.control` 裡 test helper 的觀測內容，再回頭讀 `blocking`。下一節的 `tcp_ip` 範例，就是忽略 `control` 而把網站自身的問題誤判成封鎖的情況。

判定演算法的完整定義在上游的 [ts-017-web-connectivity](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md)，失敗字串的統一命名在 [df-007-errors](https://github.com/ooni/spec/blob/master/data-formats/df-007-errors.md)。

## 四種判定對應的證據

後續章節引用的五筆測量都是 2026-08-04 的公開資料，原始內容可以在 [OONI Explorer](https://explorer.ooni.org/zh-Hant) 查到。

### `dns`，解析結果的差異

台灣對 `https://ntc.party/` 的測量裡，Probe 對 A 與 AAAA 的查詢都得到 `dns_nxdomain_error`（網域不存在）。test helper 端可以查到，因此 `dns_consistency` 標為 `inconsistent`。

```json title="test_keys.queries"
{"query_type": "A", "failure": "dns_nxdomain_error", "answers": []}
{"query_type": "AAAA", "failure": "dns_nxdomain_error", "answers": []}
```

判讀 DNS 判定時要留意解析器屬於哪個網路，該筆的解析器 ASN（自治系統編號，`resolver_asn`）是 `AS13335`（Cloudflare），Probe 所在的 ASN（`probe_asn`）則是 `AS3462`（中華電信）。測量者把 DNS 指向境外服務時，DNS 階段的異常未必反映本地電信商的行為。

### `tcp_ip`，目標位址的連線失敗

台灣對 `http://www.tkec.com.tw/` 的測量判定為 `tcp_ip`，DNS 正常解析到 `210.64.193.1`，Probe 連線 `80` 埠時逾時。

單看 Probe 端容易誤讀成封鎖，對照 `control` 的結果則會得出不同的結論：

```json title="test_keys.control.tcp_connect"
{"210.64.193.1:443": {"status": true,  "failure": null},
 "210.64.193.1:80":  {"status": false, "failure": "generic_timeout_error"}}
```

test helper 從外部連線 `80` 埠同樣逾時，可見該網站的 `80` 埠從外部也無法連線，與台灣的網路環境無關。同一個 IP 的 `443` 埠在兩側都可以連線，進一步確認問題出在該埠，與連線路徑無關。

### `http-failure`，連線建立後的內容取得失敗

台灣對 `https://bit.ly/` 的測量判定為 `http-failure`。DNS 正常，兩個目標 IP 的 `443` 埠都可以連線，`control` 記錄的 test helper 端結果也相同。差異出現在 HTTP 階段，錯誤是 `generic_timeout_error`。

連線層正常而應用層失敗，常見於伺服器端的速率限制、對特定來源的拒絕服務，以及 TLS 層的中斷。要區分成因，需查看 `tls_handshakes` 與 `network_events` 的時序。

### `http-diff`，取得內容的差異

台灣的資料裡也有 `http-diff`，但樣態與封鎖告示頁不同（見文末的台灣現況），因此以下改用印尼的測量說明典型的告示頁。

四種類型中只有 `http-diff` 會用到四個 `*_match` 欄位，印尼 `http://www.sportsinteraction.com/` 的測量是典型的例子：

| 觀測方 | 狀態碼 | 標題 | 內容長度 |
|---|---|---|---|
| Probe | `200` | `Trustpositif` | 7,044 |
| test helper | `403` | `Maintenance` | 7,067 |

Probe 的請求被重導向到 `http://lamanlabuh.aduankonten.id/`，屬於印尼官方的內容申訴網域，頁面標題 `Trustpositif` 是當地網路內容過濾系統的名稱。ISP 在連線途中把使用者導向告示頁，是 `http-diff` 最典型的成因。

從同一筆測量也可以看出，單一欄位不足以作為判準：

```text title="四個 *_match 欄位與 body_proportion"
title_match: false        status_code_match: false
headers_match: true       body_length_match: true
body_proportion: 0.9967
```

`body_length_match` 為 `true`、`body_proportion` 逼近 `1`，只是因為封鎖告示頁與對照組頁面的長度相近。單看長度會得到錯誤的結論，四個欄位要一併判讀，其中 `title_match` 與 `status_code_match` 的鑑別力通常最高。

## 誤判的來源

`blocking` 有值、實際上卻沒有網路干預，在資料集裡是常態，前述 `tkec.com.tw` 的 `80` 埠無法連線就是一例。

埃及 `http://www.newipnow.com/` 的測量是更隱蔽的例子，判定為 `http-diff`。四個 `*_match` 有三個不符，`body_proportion` 只有 `0.02`，表面上像是被插入了封鎖頁。實際內容如下：

| 觀測方 | 狀態碼 | 標題 |
|---|---|---|
| Probe | `520` | `newipnow.com \| 520: Web server is returning an unknown error` |
| test helper | `200` | `Buy Private Proxies: $0.88 per Dedicated Premium IP - NewIPNow` |

`520` 是目標網站前方的 Cloudflare 在來源伺服器異常時回應的錯誤頁，表示該網站當下發生異常，與埃及的網路管制無關。該筆的 `probe_asn` 是 `AS13335`（Cloudflare），測量端本身也位在 Cloudflare 的網路上，屬於下列第二類的測量環境因素。

常見的誤判來源可分為以下幾類：

- **來源網站自身狀態**：伺服器錯誤、維護頁、CDN 錯誤頁、地理限制。
- **測量環境**：Probe 啟用 VPN 或 Tor 時，測得的是出口所在地的網路。
- **網站的動態內容**：輪播廣告、個人化內容與 A/B 測試，會讓兩側的內容本來就不相同。
- **對照組本身失敗**：`control_failure` 有值時，雙邊比對的前提不成立。

OONI 在資料集層級也處理同一類問題，過濾異常投稿所用的啟發式規則整理在[OONI 錯誤量測的辨識方法與匿名憑證](/articles/ooni-faulty-measurements/)。

## 單筆測量之外的補強

要從觀測推進到「某個網站在某地被封鎖」的結論，單筆資料並不足夠，實務上還需補上以下幾個維度：

1. **跨時間**：同一個網址在數天到數週內反覆出現同樣的判定，才能排除偶發故障。
2. **跨 ASN**：多家電信商測得相同的結果，指向網路層的普遍行為。只在單一 ASN 出現的結果，比較可能是該業者的個別設定。
3. **跨解析器**：更換 DNS 解析器後仍然異常，才能排除解析器本身的問題。
4. **`confirmed` 欄位**：OONI 後端以已知的封鎖告示頁指紋比對測量，命中時把 `confirmed` 標為 `true`。該欄位出現在 [measurements API](https://api.ooni.org/api/v1/measurements) 的回應裡，屬於後端的分析結果，不在 Probe 產生的原始資料內。

跨時間與跨 ASN 比對所需的批次取用作法，見[ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)。

!!! warning "`confirmed` 與 `http-diff` 的區別"

    `confirmed` 標記的依據是封鎖指紋比對，容易與 `http-diff` 混淆。DNS 被導向已知的封鎖用 IP 時同樣會標為 `confirmed`，判定類型仍是 `dns`。撰稿時抽查伊朗、俄羅斯、土耳其、中國各 5 筆 `confirmed` 測量，樣本全部落在 `blocking: "dns"`。樣本數少，只能看出兩者並非同一件事，不足以推論一般規律。

## 台灣現況

以下數字取自 2026-08-05 往前 24 小時的台灣 `web_connectivity` 全量資料，共 22,105 筆測量。統計時把該區間在 S3 上的每一筆逐行解析，再把 `test_keys.blocking` 依 ASN 累計：

| 判定 | 筆數 | 佔比 |
|---|---|---|
| `false`（未觀測到干預） | 21,029 | 95.13% |
| `none`（沒有判定結果） | 512 | 2.32% |
| `tcp_ip` | 312 | 1.41% |
| `dns` | 150 | 0.68% |
| `http-failure` | 67 | 0.30% |
| `http-diff` | 35 | 0.16% |

四種干預類型合計 564 筆，佔全部測量的 2.55%。`none` 是缺少 `test_keys` 或 `blocking` 為 `null` 的測量，計算異常率前要先決定是否納入分母。

另外抽查 100 筆異常測量，`confirmed` 為 `true` 的有 0 筆，與[ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)長期以來的描述一致。

!!! warning "小樣本的分布偏差"

    本頁初稿曾以 measurements API 異常清單的 40 筆抽樣估計判定分布，得到 `dns` 最多、`http-diff` 為零的結論。改用全量統計之後兩個結論都不成立，`tcp_ip` 是 `dns` 的兩倍以上，`http-diff` 也確實存在。API 的異常清單有自己的排序邏輯，直接當成隨機樣本會失準。判定分布應以全量統計取得，作法見[ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)。

抽查 4 小時區間內台灣的 15 筆 `http-diff`，`body_proportion` 全部落在 `0.004` 到 `0.21`，Probe 取得的內容遠短於對照組。前述印尼的封鎖告示頁逼近 `1`，台灣的 `http-diff` 是相反的樣態，屬於不同的現象。內容極短通常代表錯誤頁或空回應，成因要逐筆查驗證據層才能判斷，我們不在本頁下結論。

重新執行上述統計的指令：

```bash title="取得判定分布"
uv run python ooni.py lookback --units=24 --loc=TW --frame=hours
```

指令會印出 `blocking` 的合計，並把逐 ASN 的分布寫入 CSV。單筆查驗仍使用 API：

```bash title="列出台灣的異常測量"
curl -s "https://api.ooni.org/api/v1/measurements?probe_cc=TW&test_name=web_connectivity&anomaly=true&limit=100" \
  | python3 -m json.tool | head -40
```

以上數字是單一 24 小時區間的快照，反映的是當日的樣態，不足以作為長期趨勢的結論。趨勢分析需要涵蓋更長的時間，台灣的觀測本身也有 ASN 集中度過高的限制（細節見前述的[ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)）。

## 相關閱讀

- [ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)：跨時間、跨 ASN 比對的起點，含公開資料集的批次取用與覆蓋率計算
- [OONI 測量資料的結構](/projects/asn-coverage/ooni-data-format/)：一筆測量資料由哪些欄位組成，以及各欄位的讀法
- [OONI 測項速查表](/projects/asn-coverage/ooni-nettests-map/)：ooni/spec 收錄的各個測項的量測內容與台灣的觀測情形
- [ASN 多樣性與台灣的觀測缺口](/projects/asn-coverage/asn-diversity/)：台灣各 ASN 的 OONI 觀測覆蓋率與集中度
- [OONI 網站檢測清單的維護](/join/ooni-test-list/)：OONI Probe 在台灣使用的網站清單如何維護
