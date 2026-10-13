---
title: oniux，以 Linux 命名空間隔離應用程式的 Tor 工具
description: Tor Project 介紹 oniux 的翻譯，說明它如何用 Linux 命名空間讓任意程式只能經由 Tor 連線，附上 2026-10 查核的安裝方式，以及 oniux 與 onionmasq 的關係。
date: 2025-05-16
---

!!! info ""

    本文翻譯自 Tor Project 部落格的 [Introducing oniux: Kernel-level Tor isolation for any Linux app](https://blog.torproject.org/introducing-oniux-tor-isolation-using-linux-namespaces/)（2025-05-14），文中的「我們」是 Tor Project。安裝方式依 2026-10 的官方文件更新，補註、「oniux 與 onionmasq」與「社群的看法」兩節由 anoni.net 撰寫。

![oniux 的介紹圖](https://blog.torproject.org/introducing-oniux-tor-isolation-using-linux-namespaces/lead.webp){ .shot }

開發者在推出重視隱私的應用程式與服務時，希望每一個封包都確實經由 Tor 傳送。只要代理設定錯一處，或有一次系統呼叫不小心繞過了 SOCKS，資料就可能外洩。

我們因此推出 oniux，一個小型的命令列工具，利用 Linux 命名空間替第三方應用程式提供 Tor 網路隔離。oniux 建立在 Arti 與 onionmasq 之上，把任何 Linux 程式放進專屬的網路命名空間，流量全部經由 Tor 路由，排除資料外洩的可能。工作、行動或研究需要嚴格的流量隔離時，可以考慮 oniux。

## Linux 命名空間

命名空間（namespace）是 Linux 核心大約在 2000 年引入的隔離功能，可以安全地把應用程式的特定部分與系統的其餘部分隔開。命名空間有網路、掛載、行程等多種，每一種隔離一部分系統資源。

系統資源是系統上所有應用程式共用的東西，最明顯的例子是作業系統的時鐘，其他還有行程清單、檔案系統與使用者清單。

命名空間把應用程式的某一部分與作業系統的其餘部分容器化，Docker 的隔離機制就是用它實作的。

## Tor 與命名空間的結合

命名空間可以用來隔離任意應用程式的 Tor 網路存取。我們把每個應用程式放進一個網路命名空間，裡面看不到系統層級的網路介面（例如 `eth0`），只有一個自訂的網路介面 `onion0`。

以命名空間隔離仰賴作業系統核心提供的安全機制，是軟體層面隔離任意應用程式最安全的方式。SOCKS 代理則不同，開發者一時疏忽，讓某條連線沒有經過設定好的 SOCKS，資料就會意外外洩。

## oniux 與 torsocks 的比較

另一個目標相近的工具是 `torsocks`，它覆寫所有與網路相關的 libc 函式，把流量導向 Tor 提供的 SOCKS 代理。torsocks 的跨平台能力稍好，缺點是應用程式只要不經由動態連結的 libc 發出系統呼叫，不論有意或無意，資料都會外洩。純靜態的二進位檔與 Zig 生態系的應用程式因此都不適用。

| oniux                | torsocks                                           |
| -------------------- | -------------------------------------------------- |
| 獨立的應用程式       | 需要執行 Tor 常駐程式                              |
| 使用 Linux 命名空間  | 使用 ld.so 預先載入（preload）的手法               |
| 適用於所有應用程式   | 只適用於經由 libc 發出系統呼叫的應用程式           |
| 惡意應用程式無法洩漏 | 惡意應用程式可以直接用組合語言發出系統呼叫洩漏資料 |
| 只支援 Linux         | 跨平台                                             |
| 新專案，仍屬實驗性質 | 超過 15 年的實際使用紀錄                           |
| 以 Arti 為引擎       | 以 C Tor 為引擎                                    |
| 以 Rust 撰寫         | 以 C 撰寫                                          |

## 安裝與使用

原文發表時的安裝指令指定 `v0.4.0` 標籤，以下依 2026-10 查核的官方資料更新。oniux 大約每月隨 Arti 的發布推出新版，2026-10 查核時最新的標籤是 `v0.13.0`（2026-09-09），編譯需要 Rust 1.91 以上。

官方說明頁列出 Alpine Linux、Nix、Void Linux 已收錄 oniux 套件，其他發行版的收錄情形見 [Repology](https://repology.org/project/oniux/versions)。crates.io 上名為 oniux 的套件只是 0.0.0 版的佔位套件，要從 Tor Project 的 GitLab 取得原始碼安裝。

發行版沒有套件時，先用 rustup 安裝新版的 Rust 工具鏈，再用 cargo 安裝：

``` bash
$ cargo install --locked --git https://gitlab.torproject.org/tpo/core/oniux --tag v0.13.0 oniux
```

新版發布之後，把 `--tag` 換成 [oniux 的 GitLab 專案](https://gitlab.torproject.org/tpo/core/oniux/-/tags)上最新的標籤即可。oniux 需要 `tun` 核心模組，多數發行版預設就會載入，執行時出現 `File not found` 錯誤的話，先執行 `modprobe tun` 再試一次。

使用方式是在原本的指令前面加上 `oniux`：

``` bash
# 用 oniux 做一次簡單的 HTTPS 查詢
$ oniux curl https://icanhazip.com
<A TOR EXIT NODE IP ADDRESS>

# 也支援 IPv6
$ oniux curl -6 https://ipv6.icanhazip.com
<A TOR EXIT NODE IPv6 ADDRESS>

# 連線到洋蔥服務
$ oniux curl http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion/index.html

# 需要除錯時可以開啟日誌
$ RUST_LOG=debug oniux curl https://icanhazip.com

# 把整個 shell 放進 oniux，裡面的所有行程都經由 Tor 連線
$ oniux bash

# 在桌面環境裡也可以隔離圖形介面的應用程式
$ oniux hexchat
```

## 內部運作

oniux 一啟動就用 `clone(2)` 系統呼叫產生一個子行程，放在獨立的網路、掛載、PID 與使用者命名空間裡。子行程掛載自己的 `/proc`，再依父行程的 UID 與 GID 設定對應的 UID、GID 映射。

接著，子行程建立一個寫有 nameserver 項目的暫存檔，綁定掛載（bind mount）到 `/etc/resolv.conf`，命名空間裡的應用程式因此改用可以經由 Tor 解析網域名稱的解析器。

然後，子行程用 onionmasq 建立名為 `onion0` 的 TUN 介面，再透過 `rtnetlink(7)` 完成必要的設定，例如指派 IP 位址。

子行程接著用 Unix domain socket 把 TUN 介面的檔案描述子（file descriptor）傳給父行程。父行程從執行 `clone(2)` 之後就一直在等這個訊息。

完成上述步驟後，子行程放棄它身為使用者命名空間裡的 root 行程所取得的全部權限（capabilities）。

最後，oniux 用 Rust 標準函式庫提供的功能執行使用者指定的指令。

## 實驗階段的限制

oniux 還很新，使用的 Arti 與 onionmasq 也都是新的 Tor 軟體。目前功能都照預期運作，但 torsocks 這類工具已經存在超過 15 年，實際使用的經驗多得多。我們希望 oniux 也能達到同樣穩定的程度，歡迎試用。

!!! note "2026-10 補註"

    oniux 的 README 寫明，應用程式在 oniux 裡比在 torsocks 底下更難洩漏流量，但無法完全避免。應用程式透過 Unix domain socket 等行程間通訊連到 oniux 外面的行程時，連線會繞過隔離。以伺服器模式執行的 Emacs 是一個例子。伺服器行程在 oniux 外面時，連上它的用戶端不論是否經由 oniux 執行，網路連線都會外洩。網路命名空間在技術上就有這項限制，擋下行程間通訊又會犧牲可用性（見 [oniux 的 GitLab 專案](https://gitlab.torproject.org/tpo/core/oniux)）。

## oniux 與 onionmasq

oniux 裡的 `onion0` 介面由 onionmasq 提供。onionmasq 是 Tor Project 用 Rust 開發的使用者空間網路堆疊，負責處理 TCP 與 UDP 的連線狀態，讓 TUN 介面收到的流量可以轉進 Tor 網路（見 [onionmasq 的 GitLab 專案](https://gitlab.torproject.org/tpo/core/onionmasq)）。oniux 處理命名空間的隔離，封包進入 Tor 網路的部分交給 onionmasq 與 Arti。Tor Project 的 Android 版 Tor VPN 也建立在以 Arti 與 onionmasq 為核心的模組化 Tor 堆疊上（見 Tor Project 部落格的 [Tor VPN Beta](https://blog.torproject.org/tor-vpn-beta/)）。

## 社群的看法

oniux 最適合命令列工具與腳本，例如量測腳本、套件下載或臨時的 `curl` 查詢。這類程式常常不支援代理設定，或是靜態連結，逐一設定 SOCKS 容易漏掉。oniux 決定封包的去向，但不會改變應用程式自己透露的資訊。cookie、登入的帳號與瀏覽器指紋經由 Tor 一樣能辨識出使用者，瀏覽網頁仍然要用 Tor Browser。oniux 只支援 Linux，也還在實驗階段。高風險的工作比較適合整台機器隔離的系統，例如 Tails 或 Whonix（文件站的 [Tails、Whonix、Qubes 的差別](docs:tools/tails-vs-whonix-vs-qubes/)有比較）。

## 致謝與來源

Tor Project 在原文最後感謝 `smoltcp` 的開發者，oniux 大量使用這個以 Rust 實作完整 IP 協定堆疊的 crate。另一位受感謝的貢獻者，教開發團隊不靠 `capabilities(7)`、改用正確的 `user_namespaces(7)` 實作隔離。oniux 的開發經費來自支持 Tor Project 的個人與組織，想支持這項工作可以[捐款給 Tor Project](https://donate.torproject.org/)。

oniux 現在有自己的說明頁，放在 [Arti 的網站](https://arti.torproject.org/related/oniux)。2026-10 查核時說明頁的安裝指令仍寫 `v0.10.0`，最新版本以 GitLab 專案的標籤為準。
