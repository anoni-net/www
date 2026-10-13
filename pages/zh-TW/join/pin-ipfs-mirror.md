---
title: 文件站 IPFS 鏡像的 pin 節點
description: 用常駐的 IPFS 節點與排程腳本 pin anoni.net 文件站的 IPFS 鏡像，包含 Windows、Linux、macOS 與 Docker 的安裝、排程、驗證與 peering 設定。
---

anoni.net 文件站在主站之外另有一份 IPFS 鏡像，主站被封鎖或下架時仍可以讀取文件。IPFS 上的內容需要有節點 pin 住才會留存。2026 年 8 月查詢網路上的提供者，只有社群自己的一台節點，整份鏡像目前是單點。每多一個節點協助 pin，網路上就多一份完整複本，社群那台機器被停權或故障時文件仍然留存。

協助的方式是架設一個常駐的 IPFS 節點，再用排程腳本定期 pin 最新版本。Windows、Linux、macOS 都適用，用不用 Docker 皆可。

!!! tip "所需條件"

    - 一台幾乎整天開機、能連上網路的電腦（桌機、家用伺服器或小主機）
    - 安裝好的 IPFS（安裝方式見下方）
    - 一支每隔幾小時自動 pin 最新版本的排程腳本

    第一次要下載的整份鏡像約 240 MB，來源目前只有社群那一台，建議一開始就設定[與社群節點的固定連線](#peering)，下載會順利許多。無法常駐節點的話，文末有改用 pinning service 代 pin 的做法。

## CID、IPNS 與 pin 的關係

需要排程的原因在於 CID 會隨內容改變。IPFS 的完整設計見[去中心化網站發布](/articles/dweb-ipfs-onion/)，以下只整理 pin 會用到的概念。

- IPFS 依檔案內容算出一段 hash，稱為 CID（Content Identifier），也就是內容在 IPFS 上的位址。內容相同則 CID 相同。
- 內容一改，CID 就跟著改變。文件站每次更新、重新發布，都會產生新的 CID。
- IPNS（InterPlanetary Name System）是固定的名稱，指向目前最新的 CID，文件站的 IPNS 名稱是下方那串 `k51…`。
- pin 代表保留某個 CID 的內容。pin 綁在 CID 上，不會跟著 IPNS 更新。文件站發布新版之後，上次 pin 的仍是舊 CID。

pin 腳本先把 IPNS 解析成當前的 CID 並 pin 住，再放掉舊版。CID 每次發布都會變，所以要用排程定期重新執行。

### 三種相似的識別碼

IPFS 有三種外觀相近、用途不同的識別碼，貼錯欄位時工具會直接回報錯誤。

| 識別碼 | 開頭 | 是否改變 | 用途 |
|---|---|---|---|
| CID | `bafybei…` | 每次發布都變 | 指定某一版內容 |
| IPNS 名稱 | `k51qzi…` | 固定 | 取得最新版，本頁的 pin 用這個 |
| Peer ID | `12D3KooW…` | 固定 | 指定要連到哪一個節點 |

pin 文件站只需要 IPNS 名稱，Peer ID 在設定[與社群節點的固定連線](#peering)時才會用到。

## 排程 pin 的運作方式

IPNS 是各節點共用的同步點，文件站發布新版時只更新 IPNS，社群不需要另外通知。節點這端每隔幾小時解析一次 IPNS，發現 CID 改變就 pin 新版，全程不需要人工協調。

!!! info "文件站的 IPFS 座標"

    以下都是公開值，可以直接使用。

    - IPNS 名稱：`k51qzi5uqu5dlfm2jj0f70ex3r3babmwy8qh071inwknttr7wqa3uhdwvlmrmw`
    - 節點 Peer ID：`12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9`（設定 peering 時才會用到）
    - DNSLink：`_dnslink.anoni.net` 指向同一個 IPNS 名稱，透過任何支援 DNSLink 的閘道都能讀取同一份內容
    - 瀏覽器：社群自架的 [IPFS 閘道](https://ipfs.anoni.net/)（`ipfs.anoni.net`）。舊網址 `anoni-net.ipns.dweb.link` 在 2026 年 9 月 30 日停止營運，見[2026 年 9 月之後的 IPFS 維護變化](#ipfs-maintenance-2026)

腳本每次執行時依序解析 IPNS 取得當前 CID、pin 新 CID、unpin 上一版，最後回收空間。新版 pin 成功之後才會放掉舊版，解析失敗或下載不到內容時，節點上現有的複本維持原狀。

## 常駐的 IPFS 節點

pin 需要本機有持續運作的 IPFS daemon 才能取得完整內容，依環境擇一安裝。

=== "Linux / macOS"

    安裝 IPFS 官方的命令列實作 [kubo](https://docs.ipfs.tech/install/command-line/)，macOS 可以用 Homebrew：

    ```bash
    brew install kubo
    ```

    Homebrew 的套件名稱已從 `ipfs` 改為 `kubo`，舊名稱仍可安裝，但後面設定服務時需使用 `kubo`。Intel 與 Apple Silicon 都支援。

    Linux 依[官方說明](https://docs.ipfs.tech/install/command-line/)下載對應架構的 kubo，安裝後初始化並啟動 daemon：

    ```bash
    ipfs init          # 只有第一次需要
    ipfs daemon
    ```

    要讓 daemon 長時間常駐，Linux 建議設成 systemd user service。macOS 用 Homebrew 安裝時，套件附有服務定義，執行下列指令即可常駐，並在登入時自動啟動：

    ```bash
    brew services start kubo
    ```

    臨時測試時，直接在背景執行 `ipfs daemon` 即可。

=== "Windows"

    最簡便的做法是安裝內含 kubo 的 [IPFS Desktop](https://docs.ipfs.tech/install/ipfs-desktop/)，登入後常駐在系統匣，daemon 持續運作。IPFS Desktop 從 2026 年 9 月 30 日起沒有專職維護者（見[2026 年 9 月之後的 IPFS 維護變化](#ipfs-maintenance-2026)），想減少這項不確定性，Windows 也可以安裝獨立版 kubo 或使用 Docker。

    安裝後確認命令列可以呼叫 `ipfs`。獨立版 kubo 需自行把 `ipfs.exe` 加進系統 PATH。使用 IPFS Desktop 而 PATH 找不到 `ipfs` 時，在腳本裡改用完整路徑即可。

=== "Docker"

    用 `docker-compose.yml` 執行 kubo，容器名稱設為 `ipfs_host`：

    ```yaml
    services:
      ipfs_host:
        image: ipfs/kubo:latest
        restart: always
        volumes:
          - ./ipfs-data:/data/ipfs
        ports:
          - "4001:4001"   # swarm，對外開放有助於連上其他節點
    ```

    啟動：

    ```bash
    docker compose up -d
    ```

    之後的 IPFS 指令都透過容器執行。設定下列環境變數，pin 腳本會自動套用：

    ```bash
    export IPFS_CMD="docker exec ipfs_host ipfs"
    ```

## pin 腳本

pin 腳本負責解析 IPNS、pin 新版與 unpin 舊版，IPNS 名稱已寫在腳本裡，不需要修改。Docker 使用者需先設定上一步的 `IPFS_CMD`。腳本會在你的機器上定期執行，建議先在 GitHub 讀過原始碼再執行。

### `anoni-pin.sh`（Linux、macOS、Docker）

[<i data-icon="download"></i> 下載 anoni-pin.sh](https://raw.githubusercontent.com/anoni-net/docs/main/docs/_scripts/anoni-pin.sh){ .btn } [<i data-icon="octicons-mark-github-24"></i> 在 GitHub 檢視原始碼](https://github.com/anoni-net/docs/blob/main/docs/_scripts/anoni-pin.sh){ .btn }

存檔後加上執行權限，先手動執行一次確認運作正常：

```bash
chmod +x anoni-pin.sh
./anoni-pin.sh          # 先手動執行一次確認正常
```

### `anoni-pin.ps1`（Windows）

[<i data-icon="download"></i> 下載 anoni-pin.ps1](https://raw.githubusercontent.com/anoni-net/docs/main/docs/_scripts/anoni-pin.ps1){ .btn } [<i data-icon="octicons-mark-github-24"></i> 在 GitHub 檢視原始碼](https://github.com/anoni-net/docs/blob/main/docs/_scripts/anoni-pin.ps1){ .btn }

先手動執行一次確認運作正常。PowerShell 預設會阻擋腳本，`-ExecutionPolicy Bypass` 只對這一次執行放行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\anoni-pin.ps1
```

## 排程設定

文件站更新不頻繁，每 6 小時執行一次已足夠，想更快跟上新版可以縮短間隔。

=== "Linux / macOS"

    使用 cron，編輯排程表：

    ```bash
    crontab -e
    ```

    加入下列一行，每 6 小時執行一次並把輸出寫進 log：

    ```bash
    0 */6 * * * /path/to/anoni-pin.sh >> $HOME/.anoni-pin/log 2>&1
    ```

    需要在開機後補執行錯過的排程時，可以改用 systemd timer 並設定 `Persistent=true`。

=== "Windows"

    使用「工作排程器」，從命令列建立最快。以下設定每 6 小時執行一次：

    ```powershell
    schtasks /Create /TN "anoni-ipfs-pin" `
      /TR "powershell -NoProfile -ExecutionPolicy Bypass -File C:\Tools\anoni-pin.ps1" `
      /SC HOURLY /MO 6 /RL LIMITED
    ```

    把 `C:\Tools\anoni-pin.ps1` 換成實際存放的路徑。也可以用工作排程器的圖形介面建立，「程式或指令碼」填 `powershell`，「新增引數」填 `-NoProfile -ExecutionPolicy Bypass -File 你的路徑`。

=== "Docker"

    排程依主機的作業系統設定（Linux、macOS 用 cron，Windows 用工作排程器，見前兩個分頁），差別在執行腳本前需先設定 `IPFS_CMD`，例如包一層 wrapper：

    ```bash
    #!/usr/bin/env bash
    export IPFS_CMD="docker exec ipfs_host ipfs"
    exec /path/to/anoni-pin.sh
    ```

    cron 改為執行這支 wrapper 即可。

## pin 結果的驗證

先解析出當前的 CID，再確認它在 pin 清單裡：

```bash
CID=$(ipfs name resolve --nocache /ipns/k51qzi5uqu5dlfm2jj0f70ex3r3babmwy8qh071inwknttr7wqa3uhdwvlmrmw)
ipfs pin ls --type=recursive | grep "${CID#/ipfs/}"
```

也可以從本機閘道開啟 `http://127.0.0.1:8080${CID}/`，內容正常顯示即代表 pin 成功。Docker 使用者把上面的 `ipfs` 換成 `docker exec ipfs_host ipfs`，上方的 compose 範例沒有對外開放 8080，用指令確認即可。

## 與社群節點的固定連線 { #peering }

pin 只需要 IPNS 名稱，內容透過 DHT 查找。第一次下載整份鏡像時，DHT 查詢緩慢或查不到來源都會拖長時間。設定 kubo 的 peering，可以讓節點與來源節點維持固定連線。

編輯 `~/.ipfs/config`，在最外層加入 `Peering` 區塊：

```json
"Peering": {
  "Peers": [
    { "ID": "12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9" }
  ]
}
```

`Addrs` 可以省略，kubo 會自動向 DHT 查詢位址。修改後重新啟動 daemon 即生效。Docker 使用者改的是 `./ipfs-data/config`，改完執行 `docker compose restart`。

確認是否已連上：

```bash
ipfs swarm peers | grep 12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9
```

peering 是單向設定，社群節點沒有對應的條目，維持連線由你的節點負責。[kubo 的設定文件](https://github.com/ipfs/kubo/blob/master/docs/config.md#peering)裡寫到，單向 peering 會佔用對方節點的連線資源，鏡像數量增加之後負擔會集中在同一台機器。目前提供者只有一台，第一次的 240 MB 都要從它下載，所以建議一開始就設定 peering。協助 pin 的節點變多、來源不再集中在同一台之後，再移除設定即可。

## 2026 年 9 月之後的 IPFS 維護變化 { #ipfs-maintenance-2026 }

Interplanetary Shipyard 是過去幾年維護 IPFS 主要軟體的團隊，Protocol Labs 停止資助之後，Shipyard 在 [2026 年 9 月 30 日結束 IPFS 的工作](https://ipshipyard.com/blog/2026-the-end-of-ipfs-at-shipyard/)。本頁的做法仍然可行，以下三項有所改變。

- **軟體維護**：kubo、Helia、Boxo、IPFS Desktop、IPFS Companion 都已沒有專職維護者，IPFS Foundation 改成對個別維護者發放 grant。程式繼續運作，安全性更新的節奏會變慢，安裝前先確認版本的發布日期。
- **公開閘道與 bootstrap 節點**：ipfs.io、dweb.link 與 IPFS 的 bootstrap 節點在同一天停止營運。kubo 0.38 之後 `Bootstrap` 的預設值是 `auto`，展開後的清單就包含這些節點。
- **本頁的瀏覽網址**：舊的 `anoni-net.ipns.dweb.link` 屬於 dweb.link，已換成社群自架的 [IPFS 閘道](https://ipfs.anoni.net/)（`ipfs.anoni.net`）。兩者讀取同一個 IPNS 名稱，透過 DNSLink 記錄對應。pin 腳本使用 IPNS 名稱，不受閘道影響。

下列指令可以查看節點目前取得的 bootstrap 節點，以及已連上的 peer 數量：

```bash
ipfs config Bootstrap --expand-auto
ipfs swarm peers | wc -l
```

`auto` 展開的節點停止營運之後，新安裝的節點可能無法加入 DHT。最直接的做法是把社群節點設為固定連線對象（見[與社群節點的固定連線](#peering)），`Peering` 只需要填 Peer ID。

## 維護與注意事項

- **版本更新**：文件站換了 CID 之後，下一次排程就會 pin 新版、放掉舊版，不需要人工處理。
- **差異下載**：pin 新版時舊版的區塊仍在節點上，IPFS 只下載實際不同的區塊。第一次要下載整份，之後一般的內容更新通常只有幾 MB。改動導覽列或版型時例外，全站 HTML 會一起重寫，差異接近鏡像大小的一半。
- **磁碟用量**：腳本 unpin 舊版後會執行一次垃圾回收，只保留最新版本。一份完整鏡像約 240 MB（2026 年 8 月實測）。
- **停止協助**：unpin 目前的版本並移除排程即可，不影響其他節點。
- **隱私與風險**：pin 的是公開文件，沒有隱私上的顧慮。提供 IPFS pin 的風險依司法管轄而不同，相關限制見[去中心化網站發布](/articles/dweb-ipfs-onion/)的「已知限制與風險」。

## pinning service 的替代做法

不想維護 daemon 與排程時，可以改用 [Pinata](https://www.pinata.cloud/)、[Storacha](https://storacha.network/) 這類 pinning service。手動 pin 時在服務的介面貼上當前的 CID，自動化則用服務的 API 寫成排程，流程與本頁的腳本相同（解析 IPNS 取得 CID，再交給服務 pin）。

代價是鏡像的存續改為依賴第三方服務商，可以當作備援。要真正去中心化，自架節點仍是最直接的做法。

## 相關閱讀

- [去中心化網站發布](/articles/dweb-ipfs-onion/)：IPFS 與 Onion 服務的設計核心，以及文件站的實際部署
- [.onion 服務架設指南](/join/setup-onion-service/)：另一種抗封鎖鏡像的做法
- [Tor Relay 架設指南](/join/setup-tor-relay/)：用自己的機器與頻寬增加 Tor 網路的中繼節點
