---
title: 去中心化網站發布
description: 自架、CDN、IPFS 與 onion 服務的設計取捨，內容定址與連線匿名的差異，以及 anoni.net 文件站同時發布三份的部署方式。
date: 2026-05-01
---

網站的發布方式除了自架伺服器加 DNS，還有 CDN 把內容快取到各地的邊緣節點、IPFS 用內容定址讓檔案在多個節點之間流通，以及 Tor onion 服務讓網站直接在 Tor 網路裡以 .onion 位址運作。後兩者常被放在一起討論，但 IPFS 針對內容被刪除與下架，onion 服務針對連線匿名與 IP 封鎖。把 IPFS 當成匿名工具或期待 onion 服務抵抗下架，都會落空。anoni.net 文件站同時發布標準網站、onion 與 IPFS 三份，部署時的取捨可以當成實例。

## 網站發布的選項

從中心化、效能優先到去中心化、抗審查，常見的選項有五種：

- **自架伺服器**：自行管理 IP 與 DNS，完全可控，也完全集中。IP 被封鎖或伺服器被沒收，網站就無法連線。
- **CDN**（Cloudflare、Fastly、CloudFront）：由邊緣節點代理流量，效能與抵抗 DDoS 的能力強，但高度依賴 CDN 業者與 DNS。
- **靜態網站託管**（GitHub Pages、Cloudflare Pages、Netlify）：部署簡便，業者可以單方面下架。
- **IPFS**：內容依 hash 定址，任何節點都可以提供同一份內容，沒有單一可下架的位置，內容能否存續取決於有沒有節點 pin。
- **Onion 服務**：網站直接在 Tor 網路裡運作，不需要公開 IP 與 DNS。連線匿名、不受 IP 封鎖影響，代價是效能較差，能連上的用戶端也有限。

實際部署多半混搭，主站走 CDN 求效能，IPFS 鏡像抵抗刪除，onion 鏡像抵抗封鎖。

## IPFS 的設計

IPFS（InterPlanetary File System）以內容定址（content addressing）為核心：

- **CID**（Content Identifier，內容識別碼）：依檔案內容算出的 hash，同時也是內容的位址。內容相同，在任何節點上的 CID 都相同。
- **DHT**（Distributed Hash Table，分散式雜湊表）：節點之間互相查詢誰持有某個 CID，以 Kademlia 演算法定位，不需要中央伺服器登記。
- **IPNS**（InterPlanetary Name System）：把固定的名稱指向目前的 CID。內容更新時 CID 會改變，IPNS 紀錄隨之更新。

內容定址對網站發布帶來三個特性：

1. **沒有單一可下架的位置**：只要還有節點 pin 住這個 CID，內容就能取得。
2. **竄改可以偵測**：CID 是內容的 hash，內容被改動，CID 就不同，讀者可以自行驗證。
3. **跨節點共用**：同一個檔案不論被多少網站引用，CID 都只有一個，快取可以共用。

設計上的限制：

- **內容存續仰賴 pin**：沒有節點 pin 的內容會在垃圾回收時消失，放上 IPFS 不等於永久保存。
- **DHT 查詢延遲**：第一次取得內容比 HTTP 慢。
- **依賴閘道**：多數讀者透過公開閘道讀取，閘道被封鎖就讀不到。公開閘道的數量也在減少。Cloudflare 的 cloudflare-ipfs.com 與 cf-ipfs.com 在 2024 年 8 月除役，流量轉往 ipfs.io 與 dweb.link，後兩者在 2026 年 9 月 30 日隨 Interplanetary Shipyard 結束 IPFS 工作一起停止營運（對 pin 節點的影響見[文件站 IPFS 鏡像的 pin 節點](/join/pin-ipfs-mirror/#ipfs-maintenance-2026)）。
- **動態內容受限**：IPFS 適合靜態內容，動態功能需要另外一層。

## Onion 服務的設計

Tor onion 服務第 3 版（v3）讓網站直接在 Tor 網路裡運作（架設步驟見[.onion 服務架設指南](/join/setup-onion-service/)）：

- **自我驗證的位址**：v3 的 .onion 位址長 56 個字元，由服務的 ed25519 公鑰編碼而成，不需要 DNS 與憑證機構，也少了一個網域解析被攔截或竄改的環節[^1]。
- **描述檔發布**（descriptor publishing）：服務把含有引介點（introduction point）的描述檔發布到 Hidden Service Directory（HSDir）。
- **會合協定**（rendezvous protocol）：使用者與服務在 Tor 網路裡的會合點建立加密連線，雙方都不知道對方的 IP。

對網站發布的意義：

1. **雙向的連線匿名**：網站看不到訪客的 IP，訪客也看不到網站的 IP。
2. **不依賴 DNS**：.onion 位址可以自我驗證，沒有 CA 信任鏈的問題。
3. **不受 IP 封鎖影響**：流量都在 Tor 網路裡，封鎖網站的 IP 沒有作用。
4. **不需要公開的 IPv4 位址**：在 NAT 後方或浮動 IP 上都能啟動。

設計上的限制：

- **效能**：用戶端三跳加上服務端三跳，共六個中繼組成一條電路，再加上會合的過程，延遲比直連高。
- **依賴 Tor 網路**：Tor 中繼被大量封鎖時，整個 .onion 生態系都受影響。
- **不適合大量靜態資源**：圖片與影片經由 Tor 傳送的成本高。
- **訪客門檻**：訪客需要 Tor Browser 或支援 onion 的用戶端。

## IPFS 與 onion 的對照


| 項目 | IPFS | Onion |
|---|---|---|
| 主要解決的問題 | 抗刪除、避免集中失效 | 連線匿名、抗 IP 封鎖 |
| 訪客匿名 | ❌ 沒有內建 | ✅ 預設提供 |
| 服務匿名 | ❌ 節點 IP 可見 | ✅ 預設提供 |
| 竄改偵測 | ✅（CID 即 hash） | 需另外靠 TLS 或簽章 |
| 抗下架 | ✅（多個節點 pin） | 部分（營運者可以關閉單一服務） |
| 大型檔案的效能 | 中等 | 差 |
| 動態內容 | 困難 | 與一般網站相近 |
| 訪客門檻 | 低（瀏覽器經由閘道） | 高（需要 Tor Browser） |

需要抗刪除選 IPFS，需要連線匿名選 onion，兩者都需要時，同一個網站同時發布兩份鏡像。

## 已知限制與風險

挑選組合之前，需要先考量兩種技術各自做不到的部分：

- **IPFS 沒有連線匿名**：PeerID 長期不變，DHT 查詢在公開網路上進行，第三方看得到哪個 IP 在找哪個 CID（完整的暴露面見[常被誤認為匿名的網路](docs:basics/mistaken-for-anonymity/)）。
- **IPFS 的內容存續仰賴主動 pin**：Pinata 這類中心化的 pin 服務，或 Filecoin 這類以代幣獎勵運作的去中心化儲存協定，都讓永久保存重新依賴第三方。
- **Onion 服務依賴 Tor 網路**：Tor 中繼被大量封鎖，或 Tor Project 停止維運，.onion 生態系都會受影響。
- **入口多半仍是中心化服務**：讀者透過公開閘道或 Tor Browser 連線，這些入口本身就是潛在的攻擊面。公開閘道也會整批停止營運，網址寫死在單一閘道上的網站，閘道停止營運時對外連結會一起失效。
- **法律上的灰色地帶**：架設 Tor 出口節點、提供 IPFS pin 服務，在不同的司法管轄下風險不同。

## 常見組合

### Onion 與 IPFS 雙鏡像

主站照常發布在一般網路上，另外提供兩份鏡像：

- IPFS 鏡像：每次發布的內容對應一個 CID，社群志工可以協助 pin（做法見[文件站 IPFS 鏡像的 pin 節點](/join/pin-ipfs-mirror/)）。
- Onion 鏡像：內容與主站相同，提供匿名連線。

EFF[^2]、Proton、BBC 與美國中央情報局（CIA）都架設過官方的 onion 鏡像，紐約時報從 2017 年起提供的 onion 版在 2025 年 3 月關閉[^3]。Cloudflare 另外提供 Onion Routing，網站在 Cloudflare 啟用之後，回應會帶上 `alt-svc` 標頭，Tor Browser 的訪客改由 Cloudflare 的 .onion 端點連入，不經過出口節點[^4]。

### IPFS 與 ENS

ENS（Ethereum Name Service，以太坊名稱服務）可以替 IPFS 內容取一個好記的名稱（例如 `example.eth`），由 ENS 上的紀錄指向目前的 CID，每次更新內容就更新一次紀錄。ENS 本身依賴以太坊區塊鏈，名稱也需要付費，去中心化的程度有前提。

## anoni.net 文件站的部署

anoni.net 文件站同時發布標準網站、onion 與 IPFS 三份，內容相同，三套建置流程各自處理網址與路徑的差異。


1. **原始檔**：MkDocs Material 格式的 Markdown，放在 GitHub 的 `anoni-net/docs`。
2. **標準網站與 onion**：推送 `docs` 分支時，GitHub Actions 的 `build_docs.yml` 同時建置兩份三語系的靜態網站，以 `aws s3 sync --delete` 上傳到同一個 S3 bucket 的不同 prefix（`docs/` 與 `docs-onion/`），標準網站經由 Cloudflare 對外提供。onion 那份在建置前先執行 `replace_sitename_anoni_onion.sh`，把站內網址改寫成 `docs.<onion 位址>`，並拿掉分析腳本與 service worker。`build_docs_anoni.sh` 與 `build_docs_anoni_onion.sh` 是同樣步驟的本機版本。
3. **IPFS**：`build_docs_anoni_ipfs.sh` 不在 workflow 裡，需要另外執行。腳本先把網址改寫成 IPFS 閘道的位址，建置三語系，確認產物裡沒有殘留主站網址，再由 `upload_to_ipfs.sh` 上傳並更新 IPNS 名稱。社群自架的閘道是 `ipfs.anoni.net`，`_dnslink.anoni.net` 也指向同一個 IPNS 名稱。

讀者如何用 onion 或 IPFS 讀文件站、連線過程中誰看得到什麼，見[你正在用哪一種方式閱讀](docs:about/how-you-are-reading/)。

### 維運上的取捨

- **pin 與內容存續**：社群成員可以協助 pin，提高內容的存續機會（[操作指南](/join/pin-ipfs-mirror/)），沒有正式的保證。
- **Onion 的延遲**：經由 Tor 連線時，SPA 或大型 JavaScript 套件的使用體驗較差，文件站因此維持一頁一個 HTML 的靜態網站。
- **三個網址的定位**：標準網站是主要入口，IPFS 與 onion 是備援與抗封鎖的管道。

### 實際運作的限制

- IPFS 公開閘道有時不穩定，影響第一次載入。閘道也可能停止營運，所以鏡像的站內連結採用網站根目錄的相對路徑，更換閘道不需要重建整份鏡像。
- IPFS 鏡像需要另外建置與上傳，更新時間可能晚於標準網站與 onion。
- 三語系的資源讓 IPFS 上的 CID 數量增加，pin 清單隨之變長。

## 相關閱讀

- [你正在用哪一種方式閱讀](docs:about/how-you-are-reading/)：標準網站、onion 與 IPFS 鏡像在讀者端的差異
- [常被誤認為匿名的網路](docs:basics/mistaken-for-anonymity/)：IPFS 等網路對外暴露的資訊
- [什麼是 Tor](docs:tools/what-is-tor/)：Tor 網路的設計與威脅
- [網路政變報告](docs:reports/interseclab-network-coup/)：InterSecLab 依外洩資料分析中國防火長城技術輸出到其他國家，呈現集中化的審查基礎建設如何運作
- [後量子密碼概觀](/articles/post-quantum/)：量子電腦對現行公鑰密碼的威脅與遷移時程

## 可參與的專案

- [文件站 IPFS 鏡像的 pin 節點](/join/pin-ipfs-mirror/)：用常駐的 IPFS 節點替文件站的 IPFS 鏡像多保存一份
- [.onion 服務架設指南](/join/setup-onion-service/)：架設 v3 onion 服務、接上 nginx，以及上線之後的維運
- [Tor Relay 架設指南](/join/setup-tor-relay/)：中繼、橋接與出口節點的架設與維運
- [Tor Relay 校園建立研究專題](/join/relay-on-campus/)：在學校架設中繼節點的提案與溝通
- [中文化與文件翻譯](docs:community/i18n/)：文件站與 Tor 文件的翻譯流程

[^1]: [V3 onion services usage](https://blog.torproject.org/v3-onion-services-usage/) - The Tor Project
[^2]: [EFF Now Has Tor Onions](https://www.eff.org/deeplinks/2023/04/eff-now-has-tor-onions) - Electronic Frontier Foundation
[^3]: [\[Onion services\] Remove NYTimes logo](https://gitlab.torproject.org/tpo/web/community/-/issues/374) - Tor Project GitLab
[^4]: [Onion Routing](https://developers.cloudflare.com/network/onion-routing/) - Cloudflare Docs
