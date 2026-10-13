---
title: Tor WebTunnel 橋接架設指南
description: Tor WebTunnel 橋接在 VPS 上的架設步驟與維運做法，包含網域、TLS 憑證、nginx 反向代理、Docker 部署、防火牆、偽裝頁與事件處置。
---

WebTunnel 把 Tor 流量包進一般的 HTTPS 連線，流量形態與瀏覽網頁相近，深度封包檢測（DPI）很難單獨把它挑出來。審查系統用 DPI 封鎖 obfs4 這類特徵與 HTTPS 不同的協定時，WebTunnel 通常仍能通過，是 Tor 目前抗審查能力最強的橋接方式之一。

本頁以 Tor Project 的 Docker 部署方式為準，另外補上官方文件沒有寫的 nginx 強化設定，以及上線後的監控、偽裝頁、防火牆與事件處置。

!!! info "橋接與中繼的差別"

    貢獻 Tor 網路的方式有三種，門檻與抗審查強度各不相同：

    - [Tor Snowflake](docs:tools/tor-snowflake/)：開一個瀏覽器分頁就能執行的臨時橋接，門檻最低。Snowflake 走 WebRTC，握手特徵可能被指紋辨識，中國已有封鎖紀錄。
    - WebTunnel（本頁）：需要 VPS、網域與 TLS 憑證，偽裝成 HTTPS，在重度審查的網路裡最難被封鎖。
    - [Tor 中繼節點](/join/setup-tor-relay/)：提供 Tor 網路的頻寬與節點多元性，不屬於橋接。

    橋接（bridge）跟中繼一樣不直接連向使用者要去的目的地，目的地網站收到的連線來自 Tor 出口節點。營運橋接的法律風險因此與入口、中間節點同級，遠低於出口節點。

## 增設 WebTunnel 橋接的理由

審查者會封鎖已知的橋接 IP，橋接分散在越多國家與網路供應商（ASN），受審查的使用者可用的入口就越多。台灣對外連線受審查的程度低、頻寬充足，適合當橋接的來源地。WebTunnel 也比中繼節點省資源，一台 512MB 到 1GB RAM 的 VPS 即可執行，成本與維運負擔都比較低。

2026 年伊朗在軍事行動期間多次大規模斷網，第二階段從 2 月底持續到 5 月底，將近三個月。網路重新開放後，社群架設的 WebTunnel 流量明顯增加（見[伊朗封網後的 WebTunnel 流量](/updates/2026/05/iran-blackout-webtunnel/)）。在以 DPI 嚴格過濾的網路裡，偽裝成 HTTPS 的橋接常是少數還能連上 Tor 的方式。

## 架設前的準備

- 一台 VPS，Debian 或 Ubuntu，512MB RAM 以上，建議 1GB，讓 Tor 行程有餘裕。
- 一個可以編輯 DNS 的網域或子網域。
- 對外開放的 443 連接埠，WebTunnel 走標準的 HTTPS 連接埠才像一般網站。
- 聯絡用的 email，會公開在橋接的 `ContactInfo`。

!!! tip "網域與營運隱私"

    WebTunnel 的偽裝效果取決於網域看起來是否像一般網站：

    - 選用無法一眼看出是 Tor 橋接的網域或子網域。
    - 根路徑（`/`）放一個無害的頁面，例如個人首頁、網域停放頁或簡單的部落格，讓掃描者看到的是一般網站。
    - 在台灣這類低風險的環境，用既有網域的子網域通常沒有問題。需要更高的營運隱私時，再考慮匿名註冊的獨立網域。

架設分成兩部分。先設定網域、TLS 憑證與反向代理，讓伺服器對外像一般的 HTTPS 網站，再用 Docker 執行橋接。

## 網域、TLS 與 nginx 反向代理

### DNS 紀錄

在網域的 DNS 新增一筆 A 紀錄，把網域或子網域（例如 `bridge.example.com`）指向 VPS 的對外 IP，等 DNS 生效後再進行下一步。

### TLS 憑證

WebTunnel 需要瀏覽器信任的 TLS 憑證，連線才會像連到一般的 HTTPS 網站，用 Let's Encrypt 最簡便。

```bash
apt update
apt install certbot python3-certbot-nginx
certbot --nginx -d bridge.example.com
```

certbot 套件會安裝自動續期的 systemd timer，確認方式：

```bash
systemctl status certbot.timer
```

!!! info "其他簽發憑證的方式"

    也可以用 `acme.sh` 之類的 ACME 客戶端簽發憑證，做法見 [Tor Project | WebTunnel Bridge](https://community.torproject.org/relay/setup/webtunnel/)。

### nginx 反向代理設定

WebTunnel 橋接在本機的 `127.0.0.1:15000` 監聽，nginx 負責對外的 HTTPS，再把一條秘密路徑反向代理到橋接。秘密路徑用一組隨機字串，下方範例以 `$PATH` 代表。

在既有或新建的 vhost 加上下面的 `location` 區塊，WebSocket 標頭不可省略：

```nginx
location = /$PATH {
    proxy_pass http://127.0.0.1:15000;
    proxy_http_version 1.1;
    ### WebSocket 標頭 ###
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ### Proxy 標頭 ###
    proxy_set_header Accept-Encoding "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    add_header Front-End-Https on;
    proxy_redirect off;
    access_log off;
    error_log /dev/null;
}
```

!!! tip "反向代理的兩項強化設定"

    以下兩項調整不在官方文件裡，可以讓秘密路徑更難被探測，長時間的連線也更穩定。

    **秘密路徑的探測防護**

    預設設定下，不帶 WebSocket 握手的一般請求送到秘密路徑時，nginx 也會轉發給橋接。橋接的回應可能與站上其他路徑不同，反而暴露出路徑的存在。加上一行設定，讓沒有 Upgrade 標頭的請求一律回傳 404，秘密路徑的回應就與站上任何不存在的網址相同：

    ```nginx
    location = /$PATH {
        # 只有真正的 WebTunnel 握手能通過，一般的探測一律回 404
        if ($http_upgrade = "") { return 404; }
        proxy_pass http://127.0.0.1:15000;
        # ⋯⋯其餘設定同上
    }
    ```

    WebTunnel 的連線一定帶有 Upgrade 標頭，這行設定不會擋下正常的橋接客戶端。

    **長連線的逾時設定**

    nginx 的 `proxy_read_timeout` 預設是 60 秒，連線超過 60 秒沒有資料傳輸就會被切斷，長時間維持的 Tor 迴路會因此無故斷線。在 `location` 區塊裡拉長逾時，並開啟 TCP keepalive：

    ```nginx
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        proxy_socket_keepalive on;
    ```

根路徑的 `location /` 維持回傳一般網頁，伺服器整體看起來就是普通網站，只有知道秘密路徑的 Tor 客戶端會連到橋接。改完後測試設定並重新載入：

```bash
nginx -t && systemctl reload nginx
```

## WebTunnel 橋接的 Docker 部署

### Docker 安裝

```bash
apt install curl sudo
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

### `.env` 設定檔

`URL` 換成網域加上秘密路徑（與 nginx 設定裡的 `$PATH` 相同），`OPERATOR_EMAIL` 換成聯絡用的信箱，再執行：

```bash
truncate --size 0 .env
echo "URL=https://bridge.example.com/your-secret-path" >> .env
echo "OPERATOR_EMAIL=your@email.org" >> .env
echo "BRIDGE_NICKNAME=WTBr$(cat /dev/urandom | tr -cd 'qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAQWERTUIOP0987654321'|head -c 10)" >> .env
echo "GENEDORPORT=4$(cat /dev/urandom | tr -cd '0987654321'|head -c 4)" >> .env
```

### docker-compose 設定檔

```bash
curl https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/webtunnel/-/raw/main/release/container/docker-compose.yml?inline=false > docker-compose.yml
```

compose 設定檔預設開啟自動更新，橋接會自動更新到新版。接著啟動容器：

```bash
docker compose up -d
```

### 橋接行與連線驗證

```bash
docker compose exec webtunnel-bridge get-bridge-line.sh
```

把輸出的橋接行（bridge line）貼進 Tor Browser 的橋接設定，即可測試能否連線。

!!! warning "指令失效時的替代寫法"

    較新版本的容器名稱可能是 `webtunnelBridge`，上面的指令會執行失敗，改用：

    ```bash
    docker exec webtunnelBridge get-bridge-line.sh
    ```

橋接行裡的 IP（特別是 IPv6）是隨機產生的佔位值，因為 pluggable transport 規格要求那個位置要有 IP，實際上不會使用。客戶端連線時用的是網域與秘密路徑。橋接預設會透過 [bridges.torproject.org](https://bridges.torproject.org/) 自動派發給需要的使用者。

## 進階維運

### 防火牆

WebTunnel 對外只需要開放 443（HTTPS），SSH 依管理需求保留。橋接監聽的 `15000` 綁定在 `127.0.0.1`，不要對外開放。

```bash
ufw allow 443/tcp
ufw allow OpenSSH
ufw enable
ufw status
```

### 偽裝頁設計

根路徑的頁面也是偽裝的一部分，建議放有實際內容、不會引人懷疑的靜態頁，例如個人作品集、技術筆記或網域停放頁。空白頁與 nginx 預設的歡迎頁反而顯眼。

### 監控與健康檢查

- 容器狀態與日誌：

    ```bash
    docker compose ps
    docker compose logs -f
    ```

- TLS 憑證的有效期與續期狀態：`systemctl status certbot.timer`。
- 橋接上線數小時後，可以透過 [bridges.torproject.org](https://bridges.torproject.org/) 的流程或 Tor Browser 實測橋接是否已被派發、能否連線。

### 軟體更新

橋接本體由 compose 設定自動更新。系統層的 Docker、nginx、certbot 仍需定期執行 `apt update && apt upgrade`，TLS 憑證的續期交給 certbot timer。

### 事件處置 runbook

- **橋接無法連線**：先看 `docker compose logs`，再確認 nginx 的秘密路徑與 `.env` 的 `URL` 路徑一致、TLS 憑證未過期、443 已開放。
- **憑證過期**：執行 `certbot renew` 之後 `systemctl reload nginx`。
- **濫用通報或法律詢問**：橋接的角色接近入口與中間節點，不直接連向目的地。回覆時說明 Tor 橋接的角色，並附上 [EFF 的 Tor 中繼營運者法律 FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)。
- **橋接下線**：`docker compose down` 停止橋接，再移除 nginx 的 `location` 區塊並重新載入。

## 常見問題

??? question "WebTunnel 與 Snowflake、obfs4 的差異"

    三者都是繞過審查、連上 Tor 的橋接。Snowflake 透過 WebRTC（瀏覽器用來視訊通話的即時連線技術）運作，開瀏覽器就能執行，但容易被偵測。obfs4 把流量變成隨機雜訊，DPI 仍可能辨識出它不像 HTTPS 而封鎖。WebTunnel 把流量包進真正的 HTTPS 連線，審查者要封鎖它就得連帶封掉大量正常網站，所以在 DPI 過濾嚴格的網路裡最有效。

??? question "營運橋接的法律風險"

    橋接與入口、中間節點一樣不連向最終目的地，目的地網站收到的連線來自 Tor 出口節點。台灣的網路相對自由，目前允許營運這類節點，風險遠低於出口節點。收到詢問時可以參考 [EFF 的 Tor 中繼營運者法律 FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)。

??? question "伺服器規格"

    512MB RAM 的小型 VPS 可以執行，但建議配置 1GB，Tor 行程本身可能用到接近 1GiB 的記憶體。CPU 與頻寬的需求都不高。

??? question "家用網路的架設條件"

    家用網路也能架設，條件是有固定的對外 IP、能在路由器設定 443 的連接埠轉發，而且 ISP 允許這類流量。動態 IP 會讓橋接位址不穩定，用 VPS 通常更簡便、穩定。

??? question "Docker 以外的安裝方式"

    也可以從原始碼編譯 Go 執行檔，做法見 [Tor Project | Compile and run WebTunnel from source](https://community.torproject.org/relay/setup/webtunnel/source/)。多數情況下 Docker 最簡便。

## 相關閱讀

- [網路自由為什麼重要](docs:basics/internet-freedom/)
- [什麼是 Tor](docs:tools/what-is-tor/)
- [Tor Snowflake](docs:tools/tor-snowflake/)：開瀏覽器分頁就能執行的臨時橋接

## 其他參與方式

- [Tor Relay 架設指南](/join/setup-tor-relay/)：在台灣架設中繼節點的法律、技術與行政考量
- [Tor Relay 校園建立研究專題](/join/relay-on-campus/)：在大學校園架設 Tor 中繼節點的計畫與案例
- [Tor 中繼節點觀測](/projects/pulse/)：台灣與鄰近地區中繼節點的數量、頻寬與版本變化

## 官方參考文件

- [Tor Project | WebTunnel Bridge](https://community.torproject.org/relay/setup/webtunnel/)：網域、TLS、nginx 設定的主要文件
- [Tor Project | WebTunnel Docker setup](https://community.torproject.org/relay/setup/webtunnel/docker/)：Docker 部署
- [Tor Project | Compile and run WebTunnel from source](https://community.torproject.org/relay/setup/webtunnel/source/)：從原始碼編譯
- [Introducing WebTunnel](https://blog.torproject.org/introducing-webtunnel-evading-censorship-by-hiding-in-plain-sight/)：WebTunnel 的設計理念
