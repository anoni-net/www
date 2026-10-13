---
title: .onion 服務架設指南
description: 用 Tor 官方的方式架設 v3 onion 服務，含 nginx 導流、子網域、權限、日誌、除錯與上線後的維運，以及 vanity 位址的產生方式與限制。
---

Onion 服務讓別人透過 Tor 直接連到你的伺服器，過程中不需要公開伺服器的 IP，也不需要向任何憑證機構註冊網域。連線兩端都在 Tor 網路內完成，加密由 Tor 本身處理。

!!! info "與中繼、橋接的差別"

    營運 [Tor 中繼節點](/join/setup-tor-relay/)、[WebTunnel 橋接](/join/setup-tor-webtunnel/)與 [Snowflake](docs:tools/tor-snowflake/)，是**把頻寬貢獻給 Tor 網路**、替別人轉送流量。

    Onion 服務則是**用 Tor 架設自己的網站**，只提供自己的內容、不轉送他人的流量，也不增加 Tor 網路的容量。兩者的風險、法律處境與維運負擔都不同。

onion 服務的設計原理、與 IPFS 的取捨，以及 anoni.net 文件站三軌部署的架構，見[去中心化網站發布](/articles/dweb-ipfs-onion/)。只想臨時分享檔案或架設用完即丟的網站時，[OnionShare](docs:tools/onionshare/) 的成本比自行架設服務低。

## 事前準備

- 可以自行管理的伺服器，以 Linux 為主
- 已安裝的 `tor`，用 `tor --version` 確認，發行版套件庫的版本通常都支援 v3
- 可以從 `127.0.0.1` 連線的網頁服務

### 網頁服務的監聽位址

```bash
sudo ss -ltnp | grep -E 'nginx|apache|caddy'
```

輸出的 `Local Address` 欄位是 `127.0.0.1:80` 時，只有本機可以連線。`0.0.0.0:80` 或 `*:80` 則代表對整個網際網路開放。

兩種情況都可以接上 onion 服務，要同時保留 clearnet 版本就維持對外監聽，Tor 一樣可以連到 `127.0.0.1`。目的是讓伺服器完全不在 clearnet 上露出時，才需要把服務改成只綁定 `127.0.0.1`，並關閉對外的埠。

### 出站連線

Tor 需要主動向外連線才能加入 Tor 網路。防火牆**不需要**為 onion 服務開放任何入站埠。機器位在限制出站連線的企業內網時，Tor 無法連上 Tor 網路，後續每一步都不會成功。出站受限通常是內網環境最先遇到的問題。

## 一、Tor 官方的設定方式

設定檔是 `/etc/tor/torrc`，加上兩行即可，以下是 [Tor 官方文件](https://community.torproject.org/onion-services/setup/)的範例：

```
HiddenServiceDir /var/lib/tor/my_website/
HiddenServicePort 80 127.0.0.1:80
```

`HiddenServiceDir` 是 Tor 存放服務身分的目錄。`HiddenServicePort` 的第一個數字是 onion 位址對外的埠，後面接後端服務實際監聽的位址與埠。

同一個 `torrc` 可以設定多組，每組各有獨立的 onion 位址：

```
HiddenServiceDir /var/lib/tor/site-a/
HiddenServicePort 80 127.0.0.1:8080

HiddenServiceDir /var/lib/tor/site-b/
HiddenServicePort 80 127.0.0.1:8081
```

每一行 `HiddenServicePort` 都歸屬於它上方最近的 `HiddenServiceDir`。

### 目錄權限

官方文件對權限只寫了目錄要「readable/writeable by the user that will be running Tor」，沒有具體的權限數值。實務上目錄權限必須是 `0700`，權限較寬時 Tor 會拒絕使用這個目錄。

套件安裝的 `tor` 通常以 `debian-tor` 或 `tor` 使用者執行，確認執行身分：

```bash
systemctl cat tor@default.service | grep -E 'User=|debian-tor'
ps -o user= -C tor
```

權限設定與確認：

```bash
sudo chown -R debian-tor:debian-tor /var/lib/tor/my_website
sudo chmod 0700 /var/lib/tor/my_website
sudo ls -ld /var/lib/tor/my_website
```

目錄由 Tor 自行建立時（`torrc` 寫好後重啟即可），權限本來就正確，`chown` 與 `chmod` 只在手動建立目錄時需要。

其他程式需要讀取 `hostname` 時，可以在 `torrc` 設定 `HiddenServiceDirGroupReadable 1`，開放同群組讀取目錄與 `hostname` 檔（預設是 `0`）。金鑰檔不會因此變成群組可讀。

### 套用設定

```bash
sudo tor --verify-config          # 先檢查語法，不影響執行中的服務
sudo systemctl restart tor@default
sudo systemctl status tor@default
```

!!! warning "Debian 與 Ubuntu 的兩個 tor unit"

    套件同時提供 `tor.service` 與 `tor@default.service`。實際運作的是 `tor@default.service`，`tor.service` 只是不做任何事的外殼。只重啟 `tor.service` 不會套用新設定，畫面上也看不出差別。

    不確定時用 `systemctl list-units 'tor*'` 查看哪一個處於 `running`。

### 日誌的位置

Tor 出問題時，原因幾乎都能從日誌找到。透過 systemd 執行時：

```bash
sudo journalctl -u tor@default -n 50 --no-pager
sudo journalctl -u tor@default -f          # 持續輸出新的日誌
```

也可以在 `torrc` 另外指定日誌檔，這一行預設是註解掉的：

```
Log notice file /var/log/tor/notices.log
```

首先確認 Tor 是否已連上 Tor 網路，日誌裡要有這一行：

```
Bootstrapped 100% (done): Done
```

沒有這一行代表 Tor 還沒連上網路，原因多半是出站連線被擋。此時無論 `HiddenServiceDir` 是否設定正確，都不會產生 onion 位址。

### onion 位址與金鑰

Tor 正常啟動後，`HiddenServiceDir` 底下會有下列檔案：

| 檔案 | 內容 |
|---|---|
| `hostname` | 56 字元的 v3 位址加上 `.onion` |
| `hs_ed25519_public_key` | 公鑰 |
| `hs_ed25519_secret_key` | **私鑰，外洩即無法挽回** |
| `authorized_clients/` | 存取控制用的目錄，預設是空的 |

目錄是 `0700`、檔案是 `0600`，都由 Tor 自行建立。只有 Tor 的執行身分可以讀取，查看位址要用 `sudo`：

```bash
sudo cat /var/lib/tor/my_website/hostname
```

其餘檔案是服務的金鑰，官方文件的警告如下：

> The other files are your Onion Service keys, so it is imperative that these are kept private. If your keys leak, other people can impersonate your Onion Service, deeming it compromised, useless, and dangerous to visit.

onion 位址就是公鑰的編碼，既沒有撤銷機制、也沒有機構可以代為註銷，金鑰外洩後無從補救。唯一的處理是產生新位址並通知所有讀者，而在抗審查的情境下，通知本身往往無法做到。

!!! tip "權限與備份的檢查"

    `sudo ls -la /var/lib/tor/my_website` 的輸出中，目錄是 `drwx------`、檔案是 `-rw-------`、擁有者是 Tor 的執行身分，就是正常狀態。Tor 自行建立的目錄本來就是如此，不需要額外處理。

    備份整個 `HiddenServiceDir` 目錄，存放位置要以等同或高於伺服器的標準保護。具體做法是加密（例如放進已加密的密碼管理器，或用 `gpg -c` 加密後再存），不要放進一般的雲端硬碟或程式碼倉庫。

## 二、nginx 導流

Onion 服務只負責把連線轉到指定的位址與埠，之後的導流由 nginx 的設定決定。

Debian 與 Ubuntu 的慣例是把設定放進 `/etc/nginx/sites-available/`，再連結到 `sites-enabled/`：

```bash
sudo nano /etc/nginx/sites-available/onion
sudo ln -s /etc/nginx/sites-available/onion /etc/nginx/sites-enabled/
sudo nginx -t                     # 語法檢查，一定要先執行
sudo systemctl reload nginx
```

設定內容：

```nginx
server {
    listen 127.0.0.1:80;
    server_name <你的位址>.onion;

    root /var/www/site;
    index index.html;
}
```

`server_name` 填入實際的 onion 位址。同一個 `listen` 上只有一個 server block 時，填錯也不影響。多個 server block 共用同一個 `listen` 時（例如第三節的子網域），沒有對上的請求會落到 nginx 的 default server，回應錯誤的內容或預設頁。

### Unix socket 連線

`torrc` 的 `HiddenServicePort` 指向 `unix:` 路徑時，nginx 要改成監聽同一個 socket，後端就完全不經過 TCP。

!!! danger "`/run/tor/` 的權限限制"

    `/run/tor/` 是 Tor 的 runtime 目錄，由 systemd 在啟動時以 `debian-tor` 身分建立（unit 的 `ExecStartPre` 寫著 `-o debian-tor -g debian-tor -d /run/tor`）。nginx 以 `www-data` 執行，無法在該目錄建立 socket。

另外建立一個兩邊都能存取的目錄：

```bash
sudo mkdir -p /run/onion
sudo chown www-data:debian-tor /run/onion
sudo chmod 0770 /run/onion
```

`/run` 是 tmpfs，重開機會清空，要讓目錄在重開機後重建，需加一條 tmpfiles 規則：

```bash
echo 'd /run/onion 0770 www-data debian-tor -' | sudo tee /etc/tmpfiles.d/onion.conf
sudo systemd-tmpfiles --create
```

`torrc` 與 nginx 指向同一個路徑：

```
HiddenServicePort 80 unix:/run/onion/site.sock
```

```nginx
server {
    listen unix:/run/onion/site.sock;
    server_name <你的位址>.onion;

    root /var/www/site;
    index index.html;
}
```

socket 由 nginx 建立，Tor 是連線的一方，所以 Tor 的執行身分需要有寫入權限。nginx 的 `listen` 指令沒有設定 socket 擁有者、群組或權限的參數，權限只能在目錄這一層控制。

reload 之後實際檢查一次，不要假設預設值可用：

```bash
ls -l /run/onion/site.sock
```

權限太嚴時 Tor 無法連線，太寬則本機任何使用者都可以連到後端，兩個方向都要檢查。

`torrc` 的 `GroupWritable` 與 `WorldWritable` 旗標只作用在 Tor 自行建立的 socket（例如 `ControlSocket` 與 `SocksPort`），對 nginx 建立的 socket 沒有作用。

### HTTPS 的取捨

連到 onion 服務的連線本身已經端到端加密並經過驗證，位址就是公鑰。再包一層 TLS 在密碼學上不會增加保護，預設建議維持 HTTP，由 Tor 處理加密。

稽核規定要求「一律要有 TLS」時，可以改用公開 CA 核發的 onion 憑證。CA/Browser Forum 在 2021 年通過修正案，允許為 v3 `.onion` 核發 DV 憑證，目前有商業 CA 提供付費服務。Tor Browser 曾把純 HTTP 的 `.onion` 標示為不安全，這個問題在 2017 年已經修正（[`#21321`](https://gitlab.torproject.org/tpo/applications/tor-browser/-/issues/21321)），不必為了網址列的提示加上 TLS。

### 常見的設定錯誤

- **回應裡寫死的 clearnet 網址**：頁面上的連結、表單 action、重新導向指向原本的網域時，訪客點一下就離開 Tor，匿名性隨即失效
- **外部資源**：圖片、字型、分析腳本從 clearnet 載入時，訪客的瀏覽器同樣會對外連線
- **Referrer 外洩**：頁面上連到 clearnet 網站的連結，瀏覽器預設會帶上 `Referer`，你的 `.onion` 位址就會出現在對方的日誌裡。可以加上 `add_header Referrer-Policy no-referrer;`，或在連結加上 `rel="noreferrer"`
- **`Host` 標頭檢查**：有些應用程式框架會拒絕不在允許清單內的 `Host`，onion 位址要另外加進去
- **access log 裡的 `127.0.0.1`**：所有連線都經過本機的 Tor 轉發，日誌記錄的一律是本機位址，屬於正常現象，日誌設定沒有問題

## 三、子網域的運作方式

Onion 位址可以帶子網域，不需要另外申請或設定 DNS。Tor 把完整的 `Host` 原樣傳給後端，由 nginx 決定如何分流。

anoni.net 文件站的 onion 位址就是這種結構：

```
docs.anoninetru5tflukgfaehun7q6khowgmymcff3gtk5oyesqazhmfxtyd.onion
└┬─┘ └──────────────────── 56 字元的 v3 位址 ────────────────────┘
 └── 子網域，由 nginx 的 server_name 分流
```

同一個 onion 位址可以承載多個子網域，nginx 的設定如下：

```nginx
server {
    listen 127.0.0.1:80;
    server_name docs.<你的位址>.onion;
    root /var/www/docs;
}

server {
    listen 127.0.0.1:80;
    server_name <你的位址>.onion;
    root /var/www/main;
}
```

`torrc` 不需要為子網域另外設定，一組 `HiddenServiceDir` 與 `HiddenServicePort` 即可。

## 四、存取控制

服務不打算對所有人開放時，可以用 v3 onion 內建的存取控制（client authorization）。未經授權的連線在交會階段就被拒絕，無法取得任何內容，比只靠位址保密可靠得多。

伺服器端把授權用的公鑰放進 `HiddenServiceDir/authorized_clients/`，用戶端在自己的 `torrc` 用 `ClientOnionAuthDir` 指向存放私鑰的目錄。內部工具與只提供給特定夥伴的鏡像，都適合用這種方式。

金鑰的產生方式與檔案格式見 [Tor 官方的 client authorization 說明](https://community.torproject.org/onion-services/advanced/client-auth/)。

## 五、vanity 位址（選用）

!!! info "可略過的步驟"

    Vanity 位址只讓開頭的字串比較好記，不影響服務是否可用，也不影響安全性。第一次架設建議先跳過，等服務運作正常再回來設定。

預設產生的位址是完全隨機的 56 個字元。想讓開頭是可辨識的字串（例如 anoni.net 的 `anoninet`），需要反覆產生金鑰，直到開頭符合為止。

[mkp224o](https://github.com/cathugger/mkp224o) 是常用的工具，[Tor 官方的 vanity 位址說明](https://community.torproject.org/onion-services/advanced/vanity-addresses/)也以它為主。

依 mkp224o 說明文件所列，先安裝編譯需要的套件：

```bash
sudo apt install gcc libc6-dev libsodium-dev make autoconf
```

編譯與執行：

```bash
./autogen.sh
./configure
make
./mkp224o -d nekokeys neko
```

AMD64 平台可以在 `configure` 加上 `--enable-amd64-51-30k` 提升效能，BSD 系統把 `make` 換成 `gmake`。產生的金鑰目錄結構與 `HiddenServiceDir` 相同，搬過去之後照「目錄權限」一節設定擁有者與權限。

### 運算成本

依 mkp224o 說明文件的估計，6 個字元的前綴「shouldn't take more than few tens of minutes」，前提是 `if using batch mode`（細節在 `OPTIMISATION.txt`）。7 個字元則是「can take hours to days」。同一份文件也寫明結果「depends on pure luck」，所需時間無法保證。

每多一個字元，搜尋空間乘以 32。anoni.net 使用的 `anoninet` 有 8 個字元，難度是「hours to days」那一級 7 個字元的 32 倍。

### 字元集的限制

onion 位址用 base32 編碼，字元集是 `a` 到 `z` 與 `2` 到 `7`，不含數字 `0`、`1`、`8`、`9`，帶這些數字的前綴不可能產生。mkp224o 會在開始前檢查並提早報錯。

### vanity 位址與身分驗證

Vanity 位址最容易被誤解的地方在身分，Tor 官方文件的說明如下：

> An attacker wishing to impersonate an existing onionsite by creating a fake version of it might use vanity addresses as an additional way to convince users that their address is the right one.

任何人都可以用一般的運算資源，產生另一組以 `anoninet` 開頭的位址。前綴相同不代表是同一個服務，前綴只提升可讀性，沒有驗證作用。

對外公布位址時要給完整的 56 個字元，讀者驗證時也要比對完整位址，不能只看開頭。

前綴以外的部分仍然隨機產生，所以安全性不受影響，vanity 位址不會比一般位址容易被破解。

## 六、上線前的檢查

以下六項依序確認。

### 1. Tor 網路的連線狀態

```bash
sudo journalctl -u tor@default | grep -i bootstrapped | tail -1
```

輸出要有 `Bootstrapped 100% (done)`。

### 2. onion 位址

```bash
sudo cat /var/lib/tor/my_website/hostname
```

輸出應為 56 個字元加上 `.onion`。

### 3. 後端的本機回應

```bash
curl -sI http://127.0.0.1:80/ -H 'Host: <你的位址>.onion' | head -1
```

輸出應為 `HTTP/1.1 200 OK`。帶上 `Host` 標頭可以模擬 Tor 實際轉來的請求，同時驗證 `server_name` 是否對上。

### 4. 經由 Tor 的連線

用 Tor Browser 開啟該 `.onion` 位址，沒有圖形介面時改用 `torsocks`：

```bash
sudo apt install torsocks
torsocks curl -sI http://<你的位址>.onion/ | head -1
```

!!! warning "描述子發布前的空窗"

    服務的描述子（descriptor）要先發布到 Tor 網路，剛設定完的前幾分鐘無法連線屬於正常現象。等幾分鐘再試一次，先不要回頭改設定。

    重啟 Tor 之後也有同樣的空窗。

### 5. 對外連線

檢視頁面原始碼，確認圖片、字型、腳本都沒有從 clearnet 載入，再點過站上主要的連結，確認不會離開 Tor。

### 6. 金鑰備份

做法見第一節的「權限與備份的檢查」。

### Onion-Location 標頭

clearnet 網站加上 `Onion-Location` 標頭後，用 Tor Browser 造訪的訪客會看到切換到 onion 版本的提示：

```nginx
add_header Onion-Location http://<你的位址>.onion$request_uri;
```

依官方說明，這個標頭要加在**走 HTTPS 的 clearnet 網站**上，加在 onion 網站本身沒有作用。

## 七、常見的連線問題

??? question "Tor 啟動失敗"

    先查看日誌：`sudo journalctl -u tor@default -n 50`。

    出現 `Permissions on directory ... are too permissive` 是目錄權限過寬，對該目錄執行 `sudo chmod 0700` 即可。

    出現 `Failed to parse/validate config` 表示 `torrc` 語法有誤，用 `sudo tor --verify-config` 可以找出是哪一行。

??? question "修改 torrc 後未生效"

    多半是重啟了 `tor.service`，實際運作的 `tor@default.service` 沒有重啟。用 `systemctl list-units 'tor*'` 確認哪一個正在運作。

??? question "日誌正常但無法連線"

    依序排除：

    1. 日誌是否有 `Bootstrapped 100%`，沒有的話是 Tor 無法連上 Tor 網路，檢查出站防火牆
    2. `hostname` 檔是否存在，不存在表示 `HiddenServiceDir` 那段設定沒有生效
    3. 剛設定完或剛重啟時，描述子發布需要時間，等幾分鐘再試
    4. 本機直接連後端是否正常（見第六節第 3 項），不正常的話問題在 nginx，與 Tor 無關

??? question "權限正確但 Tor 無法存取"

    使用非預設的路徑時，可能是 AppArmor 或 SELinux 擋下了存取。這類失敗不會顯示成權限錯誤，`ls -l` 的結果也一切正常。

    ```bash
    sudo journalctl -k | grep -i 'apparmor.*DENIED'
    sudo dmesg | grep -i denied
    ```

    有符合的紀錄時，把路徑改回 `/var/lib/tor/` 底下是最快的解法。systemd unit 本身的沙盒設定（`ProtectSystem`、`ReadWritePaths`）也可能擋下非預設路徑，要一併確認。

??? question "nginx 端的排查"

    ```bash
    sudo nginx -t
    sudo tail -50 /var/log/nginx/error.log
    ```

    使用 Unix socket 時，用 `ls -l /run/onion/site.sock` 確認 socket 檔存在，且 Tor 的執行身分有寫入權限。

??? question "重開機後的連線失敗"

    socket 所在的目錄放在 `/run` 底下時，重開機會被清空（`/run` 是 tmpfs），需要 `/etc/tmpfiles.d/` 的規則才會重建（見第二節）。

    另外確認 nginx 與 tor 的啟動順序，nginx 先建立 socket，Tor 才能連上。

## 八、上線後的維運

### 故障偵測

Tor 的行程仍在執行，不代表描述子還正常發布在網路上。最直接的檢查是定期從外部實際連線，例如用 `torsocks curl` 排一個定時工作。

### 重啟後的空窗

每次重啟 Tor 都要重新發布描述子，服務會有幾分鐘無法連線，不屬於故障。

### 連線延遲

連線要經過數個中繼，往返延遲通常是幾百毫秒到超過一秒。互動式的應用（後台管理介面、即時協作）在 onion 上的體感明顯比 clearnet 差，靜態內容影響較小，決定是否把某個服務放上 onion 前要先納入考量。

### 主機搬移

位址綁在金鑰上，把整個 `HiddenServiceDir` 搬到新主機並設定正確權限，位址就不會改變。也因此，這個目錄的備份要當成機密資料保管。

### 服務下線

移除 `torrc` 裡對應的兩行並重啟即可。位址停用後，onion 這一側無法告知訪客發生了什麼事，有讀者依賴這個位址時，先在 clearnet 那一側公告。

### 多台主機的負載分攤

需要多台機器分攤同一個 onion 位址的流量時，可以考慮 Tor Project 底下的 [OnionBalance](https://gitlab.torproject.org/tpo/onion-services/onionbalance)。專案在 2021 到 2025 年之間停滯過一段時間，2025 年 4 月恢復發布，最新版本是 `0.2.4`（2026-10 查核）。評估前先確認專案的近況。

## 九、Caddy 的設定方式

環境裡已經使用 Caddy 的話，可以照著 [Onion mirror with Caddy](https://flower.codes/2025/10/23/onion-mirror.html) 的說明設定。

Caddy 預設會自動申請 TLS 憑證，用在 onion 服務上要關閉（理由見第二節的「HTTPS 的取捨」）。整體流程與本文相同，差別只在導流的設定語法。

## 相關閱讀

- [去中心化網站發布](/articles/dweb-ipfs-onion/)：onion 服務的設計原理、與 IPFS 的取捨，以及 anoni.net 三軌部署的架構
- [文件站 IPFS 鏡像的 pin 節點](/join/pin-ipfs-mirror/)：另一種抗封鎖鏡像，歡迎協助 pin
- [Tor Relay 架設指南](/join/setup-tor-relay/)：把頻寬貢獻給 Tor 網路，與本文是不同性質的工作
- [OnionShare](docs:tools/onionshare/)：臨時分享檔案與架站，不需要自行維運服務
