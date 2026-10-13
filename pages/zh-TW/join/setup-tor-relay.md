---
title: Tor Relay 架設指南
description: 在 Debian 或 Ubuntu 架設 Tor 中間節點的步驟，包含 torrc 設定、nyx 監控、同一台主機執行多個 instance，以及法律風險、家用網路與頻寬需求的常見問題。
---

Tor 網路的頻寬與穩定性來自各地志工營運的中繼節點（relay），每多一個中繼，就有更多人能安全、匿名地上網。中間節點（Middle Relay）只在 Tor 網路內轉送流量，不直接連到最終目的地，營運者承擔的法律風險比出口節點低得多（各類節點的角色見[什麼是 Tor](docs:tools/what-is-tor/)）。本頁的步驟以中間節點為例。

## 架設前的評估

![Tor 中繼節點的運作流程](https://assets.anoni.net/www/tor-diagram-fac3c33d.webp)

架設前需先決定下列事項，打算架設出口節點的話，還要另外評估自己能承擔的風險：

- 節點類型：出口節點，或橋接、中間節點這類非出口節點。
- 出口政策：架設出口節點時要開放哪些連接埠。開放的連接埠越多，通常會收到越多濫用或違法投訴。
- `ORPort`：接受 Tor 連線的對外 TCP 連接埠。伺服器上沒有其他服務佔用 443 時，建議設成 `ORPort 443`。公共 Wi-Fi 通常只開放少數幾個連接埠，443 多半在其中。9001 也是常用的 `ORPort`。
- `ContactInfo`：節點的聯絡信箱，會公開顯示。
- 頻寬與流量：願意分給 Tor 的頻寬與每月流量。
- IPv6：伺服器是否有 IPv6 位址。

## 中間節點的架設

建議使用 Debian 或 Ubuntu，以下範例以這兩個發行版操作。其他作業系統與更詳細的安裝說明見官方文件 [Tor Project | Middle/Guard relay](https://community.torproject.org/relay/setup/guard/)。

### 套件安裝

```bash
apt update
apt install tor
```

!!! info "最新版與測試版"

    各 Linux 發行版收錄的 tor 不一定是最新版本，需要最新版或測試版時，照官方說明改用 Tor Project 的套件庫：[Why and how I can enable Tor Package Repository in Debian?](https://support.torproject.org/apt/tor-deb-repo/)

### torrc 設定

編輯設定檔 `/etc/tor/torrc`：

```bash
Nickname    myNiceRelay # 把 "myNiceRelay" 改成要公開顯示的名稱
ContactInfo your@e-mail # 聯絡方式，會公開顯示
                        # 不想公開可設成 none
ORPort      9001        # 預設的連接埠為 9001
                        # 改用 443 這類常見的 HTTPS 連接埠
                        # 審查嚴格地區的使用者更容易連上
                        # 記得在防火牆與路由器開放對應的連接埠
ExitRelay   0           # 不成為出口節點
SocksPort   0
Log notice file /var/log/tor/notices.log # 開啟 log 紀錄
```

重新啟動 tor，預設的 instance 是 `tor@default`：

```bash
systemctl restart tor@default
```

接著檢查 `/var/log/tor/notices.log` 或系統日誌 `/var/log/syslog`，出現 `Self-testing indicates your ORPort` 與 `reachable` 字樣，代表外部可以連到 ORPort。約三個小時後，可以在 [Relay Search](https://metrics.torproject.org/rs.html) 搜尋到節點的資訊。

!!! info "安裝後的維運事項"

    安裝完成後的注意事項見官方文件 [Tor Project | Relay Post-install and good practices](https://community.torproject.org/relay/setup/post-install/)。

## nyx 監控

nyx 是 Tor 的終端機監控工具，可以即時查看節點的狀態與效能，安裝後執行 `nyx` 即可開啟。

```bash
apt install nyx
```

## 同一台主機的多個 instance

Debian 與 Ubuntu 的 tor 套件附帶 `tor-instance-create` 腳本，可以在同一台伺服器建立多個獨立的 Tor instance，各自的設定與日誌分開管理。

### instance 的建立

`tor-instance-create` 的參數是 instance 名稱，只能使用英文字母與數字，對應的 systemd 服務是 `tor@<instance 名稱>`。

```bash
tor-instance-create {instance-name}
tor-instance-create mytor2
```

上例建立名為 `mytor2` 的 instance，設定檔在 `/etc/tor/instances/mytor2/torrc`，資料目錄是 `/var/lib/tor-instances/mytor2`。

### instance 的設定

在 `/etc/tor/instances/mytor2/torrc` 設定這個 instance 的參數，例如：

```bash
ORPort 9002  # 設定新的 ORPort，每個 instance 使用不同的連接埠
DataDirectory /var/lib/tor-instances/mytor2/data
Log notice file /var/lib/tor-instances/mytor2/notice.log
```

### instance 的啟動

啟動或重新啟動新建立的 instance：

```bash
# systemctl start tor@{instance-name}
systemctl start tor@mytor2
```

### 個別 instance 的 nyx 監控

nyx 用 `-s` 指定該 instance 的 control socket：

```bash
nyx -s /run/tor-instances/{instance-name}/control
```

## 常見問題

### 法律風險

入口節點（Guard Relay）與中間節點只在 Tor 網路內轉送流量，不直接連到最終目的地，執法單位因此找上營運者的機會很低。出口節點（Exit Relay）的法律風險較高，架設前需審慎評估。

在台灣架設 Tor 中繼目前是合法的，法律狀況仍可能變動，建議持續關注網路自由相關的議題與法規。台灣以外的地區可以先讀 EFF 的 [Legal FAQ for Tor Relay Operators](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)。

### 家用網路

用家用網路（例如中華電信光世代、有線電視寬頻）架設時，可能需要調整電信業者提供的路由器，有一定的技術門檻。家用路由器預設會阻擋所有連入的連線，需要在防火牆允許連入 ORPort 的連線，並在路由器設定連接埠轉發。

### 頻寬與網路條件

Tor Project 建議中繼的上傳與下載頻寬各至少 10 Mbit/s（約 1.25 MB/s，見 [Relay requirements](https://community.torproject.org/relay/relays-requirements/)）。頻寬不足 10 Mbit/s 但仍有 1 Mbit/s 以上時，官方建議改架設 obfs4 橋接。中繼另外需要固定的 IP 位址，也要確認 ISP 允許這類流量，防火牆與路由器能設定所需的連接埠轉發。

中繼只會用到設定的頻寬上限，不會佔滿所有網路資源。高負載時仍可能感覺到網速稍慢，可以視需要調整設定裡的頻寬限制。

### 營運者的隱私

中繼本身不會存取或追蹤使用者的流量。設定時留意會公開的識別資訊，`ContactInfo` 不要用可識別個人身分的信箱。

### 軟體更新

Tor 軟體需保持更新，才能取得安全修補與新功能。多數 Linux 系統透過套件管理器更新，Windows 與 macOS 需定期到 Tor 官網確認新版本。

### 入口節點的選定

入口節點的身分是自動指派的，營運者無法手動設定。節點穩定運作且頻寬足夠時，就有機會被選為入口節點。

## 相關閱讀

- [Tor WebTunnel 橋接架設指南](/join/setup-tor-webtunnel/)：把橋接流量偽裝成一般 HTTPS，適合一般中繼無法連上的受審查網路
- [Tor 中繼節點觀測](/projects/pulse/)：台灣與鄰近地區中繼節點的數量、頻寬與角色變化
- [Tor Relay 校園建立研究專題](/join/relay-on-campus/)：在校園網路架設中繼的計畫與案例
- [參與 Tor Project](/join/tor-project/)：參與 Tor 上游的方式與官方溝通管道
