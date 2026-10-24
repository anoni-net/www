---
title: 校園 Tor Relay 架設 SOP
description: 在台灣校園網路架設 Tor Relay 的技術步驟，包含 torrc 範例、UFW 防火牆規則、狀態網頁的兩種方案、監控與事件處置 runbook、驗收測試、IPv6 與交接。
---

本頁補充[Tor Relay 架設指南](/join/setup-tor-relay/)沒有涵蓋的校園網路情境，內容整理自社群夥伴 NZ 在台灣師範大學的實作經驗，搭配[校園 Tor Relay 提案範本](/join/relay-on-campus/proposal/)與[給校方與法務的校園 Tor Relay FAQ](/join/relay-on-campus/faq/)使用。

本頁假設你已經取得學校的上線許可。還在評估是否要做、如何說服學校時，先從[校園 Tor Relay 提案範本](/join/relay-on-campus/proposal/)開始。

## 校園與個人架設的差異

校園網路跟家用網路、個人 VPS 有幾個結構上的差異，會直接影響技術選擇：

- **IP 由學校配發**：通常是一組固定的 IPv4 位址，需走資訊中心的申請流程
- **IPv6 另外申請**：多數學校預設不開放 IPv6，雙堆疊需要額外提出申請
- **對外服務需申請例外開放**：TANet 校園網路預設不開放對外服務，每一項都要走例外開放的申請
- **SSH 限校內 VPN 網段**：管理連線只開放校內 VPN 網段連入，不直接暴露在網際網路上
- **每項設定都要能向校方說明**：每個對外開放的 port、每一段流量都要能對應到計畫書裡的描述
- **長期維運需考慮畢業交接**：ContactInfo 不使用個人的主要 email

## 專案範疇與範疇外事項

跟資訊中心溝通時，先說明不做哪些事，比說明要做什麼更重要。

### 範疇內

- 只建置非出口節點（Non-Exit Relay），也就是入口節點（Entry Guard）與中間節點（Middle Relay）
- 對外公開的只有節點狀態頁，不含使用者資料

### 範疇外

- 不提供 VPN、代理上網與 Tor 客戶端服務（SocksPort、DNSPort）
- 不提供 Onion Services（.onion 服務）
- 不變更校園邊界防火牆、DNS 解析與內容過濾的政策
- 不執行深度封包檢測（DPI）

### 可逆性

任何時間都可以在 10 分鐘內下線，做法是停止 systemd 服務並關閉 ORPort。

## 服務與連線一覽

### 對外公開的連接埠（Inbound）

| 服務 | Port 與協定 | 來源 | 說明 |
|---|---|---|---|
| Tor ORPort | 9001/tcp | Internet | Relay 之間的 TLS 連線，唯一必要的對外連接埠 |
| HTTP（ACME） | 80/tcp | Internet | Let's Encrypt 憑證簽發與 301 轉址 |
| HTTPS（狀態頁） | 443/tcp | Internet | 對外的狀態網頁 |
| SSH | 22/tcp | 校內 VPN 網段 | 管理用，限校內網段 |
| DirPort | 不開放 | – | 不開 DirPort，減少攻擊面 |

Tor 相關的 TCP 連接埠只對外開放 ORPort 一個。443 沒有被狀態網頁或其他服務使用時，也可以把 ORPort 改成 443，審查嚴格地區的使用者比較容易連上。

### 對外主動連線（Outbound）

| 用途 | Port 與協定 | 去向 |
|---|---|---|
| 取得目錄共識、連線到其他 Relay | TCP 443、9001 等（動態） | Tor 目錄權威（directory authority）與各 Relay |
| 系統更新 | TCP 80、443 | 套件鏡像站 |
| 時間同步 | UDP 123 | 指定的 NTP 伺服器 |

### 明確封鎖的項目

- 所有 UDP（指定的 NTP 伺服器除外）
- 郵件連接埠 SMTP 25、465、587
- IRC 6667、6697 與 P2P 常用的連接埠
- SocksPort、DNSPort、HTTPTunnelPort 一律不啟用

## 作業系統與安全基準

作業系統建議使用 Ubuntu Server 24.04 LTS 的最小安裝（minimal install），再完成以下設定：

1. **最小化安裝**：只安裝 `tor`、`nginx`、`certbot`、`fail2ban`、`unattended-upgrades`、`rsyslog`、`auditd`、`chrony`，視需要加上 `prometheus-node-exporter`
2. **SSH 設定**
    - 只允許金鑰登入：`PasswordAuthentication no`
    - 停用 root 直接登入：`PermitRootLogin no`
    - 限定使用者：`AllowUsers <你的帳號>`
    - 連線逾時：`ClientAliveInterval 300`
3. **自動安全更新**：啟用 `unattended-upgrades`
4. **時間同步**：使用 `chrony`，事件調查的時間一律以 UTC 記錄
5. **系統強化**：啟用 AppArmor，設定 `fs.protected_*` 參數
6. **日誌持久化**：`journald` 設為 `Storage=persistent`，可以再透過 `rsyslog` 轉送到校內的 SIEM
7. **檔案完整性（選用）**：部署 AIDE，定期比對檔案基準
8. **磁碟加密（選用）**：硬體允許時以 LUKS 加密整顆磁碟，至少保護 `/var/lib/tor`
9. **備份**：離線或異地備份 `/etc/tor/torrc` 與 `/var/lib/tor/keys/`，**身分金鑰需嚴格保密**

## Tor 的安裝

- **套件來源**：優先使用 [Tor Project 官方套件庫](https://support.torproject.org/apt/tor-deb-repo/)，發行版內建的版本通常落後一兩版
- **服務帳號**：以套件預設的 `debian-tor` 帳號執行，**不要用 root**
- **只營運非出口節點**：以 `ExitRelay 0` 與 `ExitPolicy reject *:*` 明確宣告，避免成為 Exit Relay

## torrc 參考設定

設定檔位置：`/etc/tor/torrc`

```bash
# 基本身分
Nickname    <YourSchoolRelayName>
ContactInfo <project-email@example.edu> - Non-exit relay at <Dept/School>; Abuse: <noc@example.edu>

# 只做 Guard 與 Middle（非出口）
ExitRelay   0
ExitPolicy  reject *:*

# ORPort：對外服務唯一必要的入口
ORPort      0.0.0.0:9001

# 不需要目錄鏡像時關閉 DirPort
DirPort     0

# 不提供本機 Socks 代理
SocksPort   0
SocksPolicy reject *

# 控制埠（僅限本機，供 nyx 與維運使用）
ControlPort           127.0.0.1:9051
CookieAuthentication  1
CookieAuthFileGroupReadable 1
DataDirectoryGroupReadable  1

# 頻寬與突發流量（依學校政策調整）
# 例：持續 80 MB/s，突發 120 MB/s
RelayBandwidthRate    80 MB
RelayBandwidthBurst   120 MB

# 日誌（notice 等級即可，避免記錄敏感細節）
Log notice file /var/log/tor/notices.log

# MetricsPort（選用）：只給本機或內網監控，絕不對外
# MetricsPort       127.0.0.1:9035
# MetricsPortPolicy accept 127.0.0.1
```

### ContactInfo 的寫法

- 不使用個人的主要 email，改用專案 email 或社團的共用信箱
- 留下 abuse 聯絡信箱，Tor 的 Network Health 團隊才能聯絡到維運者
- 欄位內容會公開顯示在 Relay Search，**寫入前就當成公開資訊處理**

### MetricsPort 的安全考量

`MetricsPort` 讓 Prometheus 可以擷取 relay 的統計指標。依 [Tor 官方的說明](https://support.torproject.org/relay-operators/relay-bridge-overloaded/)，公開 MetricsPort 會危及 Tor 網路的使用者。需要遠端擷取時，以防火牆與 `MetricsPortPolicy` 嚴格限制來源，並經過 TLS Proxy。

## UFW 防火牆規則

預設策略：

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw logging on
```

SSH 只開放校內 VPN 網段（把 `<學校 IP 段>` 換成學校的 CIDR）：

```bash
sudo ufw allow from <學校 IP 段> to any port 22 proto tcp comment 'SSH from campus VPN'
sudo ufw limit 22/tcp comment 'Rate-limit SSH'
```

狀態網頁的 Web 服務：

```bash
sudo ufw allow 80/tcp  comment 'HTTP for ACME/redirect'
sudo ufw allow 443/tcp comment 'HTTPS status site'
```

Tor ORPort（Guard 與 Middle 唯一需要開放的連接埠）：

```bash
sudo ufw allow 9001/tcp comment 'Tor ORPort'
```

MetricsPort 預設不開放，有內網監控主機 `<監控主機 IP>` 時才加上：

```bash
sudo ufw allow from <監控主機 IP> to any port 9035 proto tcp comment 'Prometheus -> Tor MetricsPort'
```

啟用並確認規則：

```bash
sudo ufw enable
sudo ufw status numbered
```

## 對外狀態網頁

校方與外部人士可以從公開網頁確認 relay 正在運作，有助於建立信任。以下兩種架構擇一即可。

### 方案 A，Nginx 與 Onionoo

- 以 Nginx 提供 HTTPS 狀態頁
- 頁面向 [Tor Onionoo API](https://metrics.torproject.org/onionoo.html) 取得自身 fingerprint 的公開資料（流量、旗標、上線狀態）
- 只顯示公開資訊，不暴露任何內部 endpoint

推薦採用方案 A，架構簡單，資料全部由前端向公開 API 取得，不涉及內部服務。缺點是圖表的彈性較低。

### 方案 B，MetricsPort、Prometheus 與 Grafana

需要完整的可觀測性時採用方案 B：

- 本機啟用 `MetricsPort 127.0.0.1:9035`，**不對外開放**
- 在本機或內網架設 Prometheus 擷取 `/metrics`
- 以 Grafana 製作圖表
- 對外只能公開 Grafana，並且**必須**符合以下條件：
    1. 唯讀帳號，搭配強密碼或 SSO
    2. HTTPS
    3. 只放公開、不含敏感資訊的圖表
    4. Prometheus **不直接對外**
    5. MetricsPort **絕不對外**

### Nginx 與 TLS 設定

- 以 `certbot --nginx` 自動簽發與續期憑證
- 只啟用 TLS 1.2 與 1.3，關閉弱加密套件（cipher）
- 啟用 HSTS、`X-Content-Type-Options: nosniff`、`Content-Security-Policy`
- 加上 `X-Robots-Tag: noindex, nofollow`，避免被搜尋引擎索引
- `/.well-known/acme-challenge/` 走 80/TCP，其餘 80 埠的請求全部以 301 轉址到 443

## 監控、日誌與事件處置

### 日誌

- `journald` 持久化，視需要以 `rsyslog` 轉送
- Nginx 與 Tor 的日誌各自寫入獨立檔案，以 `logrotate` 輪替
- Tor 建議使用 `Log notice` 等級，避免記錄敏感細節
- 事件發生時可以暫時調高等級，處理完再恢復

### 主機層的可觀測性

- `node_exporter` 綁定 `127.0.0.1:9100`
- 由本機的 Prometheus 擷取、Grafana 顯示，**對外公開時限唯讀**

### 異動稽核

- `auditd` 記錄關鍵檔案的異動：`/etc/tor/torrc`、`/var/lib/tor/keys/`
- AIDE 定期比對，結果寄到維運信箱

### 備份與金鑰保全

- 離線或異地備份 `torrc` 與 `/var/lib/tor/keys/`
- 身分金鑰遺失時，relay 只能以新的身分重新加入網路，先前累積的穩定度紀錄無法延續

### 事件處置 Runbook

收到異常告警時依序處理：

1. **初步判斷（Triage）**：
    ```bash
    sudo ss -tnlp | egrep ':22|:80|:443|:9001|:9035'
    sudo journalctl -u tor@default -n 200
    sudo ufw status numbered
    ```
2. **停止服務**：
    ```bash
    sudo systemctl stop tor@default
    ```
    並保留 `/var/log` 與 `/var/lib/tor/` 的完整快照
3. **內部通報**：30 分鐘內提出初步事故報告，內容包含影響範圍、起因、處置與預計回復時間
4. **疑似遭入侵**：依序封存證據、隔離主機、重建系統。無法排除入侵時，舊的身分金鑰一律視為已外洩，產生新的中繼身分，不用備份的金鑰復原，並通報 `bad-relays@lists.torproject.org`（檢查與處置的細節見 [2026 年 10 月 Tor 出口中繼遭入侵事件與營運者的安全檢查](/articles/tor-exit-ssh-interception/)）

**下線條件**：影響校務網路、發生資安異常，或主管、指導教授要求下線。

## 驗收與連線測試

1. **本機設定檢查**：
    ```bash
    sudo -u debian-tor tor --verify-config
    ```
2. **ORPort 可達性**：
    ```bash
    # 從校外的另一台主機執行
    nmap -p 9001 <你的公網 IP>
    # 或
    telnet <你的公網 IP> 9001
    ```
    Tor 日誌出現 ORPort 無法確認可達（reachability）的警告時，通常是防火牆或例外開放的申請還沒生效
3. **Relay 上線確認**：啟動約 3 小時後，到 [Tor Metrics Relay Search](https://metrics.torproject.org/rs.html) 以 fingerprint 查詢狀態

## IPv6 設定（選用）

要支援 IPv6 時，先向資訊中心申請 IPv6 位址，再於 `torrc` 加入：

```bash
ORPort [<你的 IPv6>]:9001
```

UFW 也要放行對應的 IPv6 流量。IPv6 雖然是選用項目，對 Tor 網路的多元性有明顯幫助，建議向學校爭取。

## 交接與畢業後的維運

維運者會畢業是校園 Relay 與個人 Relay 最大的差別，從上線第一天就要準備交接：

- **共用的 ContactInfo 信箱**：使用社團 email、專案 email 或共用信箱，不使用個人的主要 email
- **兩份以上的金鑰備份**：一份在維運者手上，一份放在指導教授的實驗室
- **交接清單**：torrc、UFW 規則、SSH 金鑰、CDN 與監控帳號、ContactInfo 信箱的密碼
- **提早尋找接手者**：畢業前一學期就要確定接手的人
- **交接手冊**：記錄主機的沿革、遇過的問題與約定的維運頻率

!!! tip "上線之後"

    - **回報案例**：透過[服務](/services/)頁面的管道聯繫匿名網路社群 anoni.net，我們會把你的案例加進[Tor Relay 校園建立研究專題](/join/relay-on-campus/)的「已完成的工作」，讓之後加入的學校有更多參考
    - **長期維運**：[Tor Relay 架設指南](/join/setup-tor-relay/)有 nyx 監控的設定，常見問題一節補充了軟體更新與入口節點的選定方式
    - **其他貢獻方式**：另外執行 [Tor Snowflake](docs:tools/tor-snowflake/) 的代理，協助受審查地區的使用者連上 Tor

## 相關閱讀

- [Tor Relay 架設指南](/join/setup-tor-relay/)：個人與家用環境的基礎安裝
- [校園 Tor Relay 提案範本](/join/relay-on-campus/proposal/)：跟學校溝通用的提案文件
- [給校方與法務的校園 Tor Relay FAQ](/join/relay-on-campus/faq/)：校方常見的疑慮與回答
- [Tor Relay 校園建立研究專題](/join/relay-on-campus/)：社群推動校園 Relay 的入口
- [Tor Project Relay Operator Guides](https://community.torproject.org/relay/)：官方的營運指南
- [Tor Relay Post-install and good practices](https://community.torproject.org/relay/setup/post-install/)：上線後的注意事項

## 資料來源與致謝

本頁的原始設計文件與實作經驗由社群夥伴 **蘇恩立（NZ）** 提供，整理自他在台灣師範大學的部署過程。NZ 同意原始材料以 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hant) 授權釋出。

照著本頁操作時，若發現步驟不適用於你的學校環境，或有可以補強的細節，歡迎透過[服務](/services/)頁面列出的管道回報，我們會持續更新本頁的內容。
