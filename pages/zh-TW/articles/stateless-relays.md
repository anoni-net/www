---
title: 無狀態 Tor Relay 的部署路線與開放問題
description: Osservatorio Nessuno 在 Tor Blog 發表的 A Server That Forgets 全文翻譯，內容包含無狀態 Tor Relay 的 TPM 金鑰保護、三種部署路線與尚未解決的工程問題，文末補上台灣營運者的觀點。
date: 2026-04-10
---

中繼節點被扣押時，機器裡能交出的東西越少，使用者就越安全。在義大利營運出口節點的 Osservatorio Nessuno 把這個想法推到作業系統層，讓 relay 每次開機都從同一份唯讀映像啟動，身分金鑰交給 TPM 保管。他們在 Tor Blog 的客座文章比較了三種已經有人採用的部署路線，也列出重新 sealing、自動更新與記憶體上限等尚未解決的問題，適合正在評估硬體與部署方式的營運者參考。

以下翻譯自 Osservatorio Nessuno 在 Tor Blog「捍衛自由網路的組織」系列發表的 [A Server That Forgets: Exploring Stateless Relays](https://blog.torproject.org/exploring-stateless-relays/)（2026-04-08），文中的「我們」指 Osservatorio Nessuno。文末的台灣營運者觀點由 anoni.net 社群補充。

[![A Server That Forgets](https://forum.torproject.org/uploads/default/original/2X/e/ee9375b0ec3906d4a0338bc230d97d0a659d996a.jpeg){ .shot }](https://blog.torproject.org/exploring-stateless-relays/)

營運 Tor relay 需要持續對抗試圖攻擊節點、藉此破壞整個網路的敵手，對方可能是民間勢力，也可能有國家支持。有些營運者還要面對扣押、搜索，或硬體遭到直接實體接觸。[奧地利](https://www.zdnet.com/article/austrian-man-raided-for-operating-tor-exit-node/)、[德國](https://forum.torproject.org/t/tor-relays-artikel-5-e-v-another-police-raid-in-germany-general-assembly-on-sep-21st-2024/14533)、[美國](https://www.npr.org/sections/alltechconsidered/2016/04/04/472992023/when-a-dark-web-volunteer-gets-raided-by-the-police)與[俄羅斯](https://torservers.net/blog/2017-04-14-freebogatov-relaymob/)都有先例，其他地方很可能也有。在這些案例裡，伺服器本身可能成為營運者的負擔。

Tor 存在的目的，是保護網路使用者免於不必要的監控。Tor 網路的設計讓任何單一營運者或伺服器都無法重建誰在跟誰通訊，記者、社運工作者與吹哨者都仰賴這項前提。relay 若在扣押後能交出內容，整個系統賴以運作的信任就會受到侵蝕，我們想解決的正是這個問題。

本文探討無狀態、無磁碟的作業系統如何從韌體到使用者空間提升 relay 的安全，重點放在軟體完整性與抵抗實體攻擊的能力。內容來自 Osservatorio Nessuno 在義大利營運出口 relay 的經驗。relay 的管理方式隨背景、技術能力、預算與司法管轄而有很大差異，我們希望引發討論，文中的做法只是其中一種模式。

## 無狀態系統

無狀態系統在重開機之間不保留任何資料，每次開機都從固定、已知的映像啟動，做法與 [Tails](https://tails.net/) 相同。把 Tor relay 完全放在 RAM 裡執行並非新構想，專為這個用途製作、以 uClibc 為基礎的微型 Linux 發行版 [Tor-ramdisk](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html)，至少在 2015 年就已經出現。

對 relay 營運者來說，無狀態的設計本身就要求更好的操作習慣，安全門檻也隨之提高：

- **抵抗實體攻擊**：機器被扣押或複製時，裡面沒有可供分析的東西。視部署方式而定，抽取 relay 金鑰可能變得不可行。
- **宣告式設定**：系統設定納入版本控制，每次開機都重新套用一次宣告的設定，系統不會偏離它。
- **不可變的執行環境**：檔案系統唯讀，攻擊者即使取得程式執行權，也無法讓任何東西在重開機後留存。
- **可重現性**：重開機前後不變的系統比較容易驗證，進一步也能重現與稽核。

## Tor Relay 做到無狀態的難處

Tor relay 的信譽隨時間累積，連續運作數個月的 relay 會取得頻寬相關的旗標，對網路更有用。信譽綁在長期的加密身分金鑰上，金鑰遺失，relay 就失去身分與在網路中的信譽，只能從頭開始。

所以 relay 的身分必須在重開機後延續，同時又不能被抽取。存在磁碟上的金鑰可能被扣押與複製，放在 TPM 這類安全晶片裡，攻擊者要取得可能就困難得多。

除了身分金鑰，relay 還會累積一份 state 檔，記錄頻寬歷史與其他暫存資訊，每次重開機都丟掉它會拖累效能。完全在 RAM 裡執行，也代表整個作業系統要放得進記憶體，而且沒有 swap 可用。行程超出可用記憶體時，核心的 OOM killer 會直接終止它們。實務上，把 glibc 的記憶體配置器換成 jemalloc 或 mimalloc，可以明顯[降低 Tor 的記憶體用量](https://1aeo.com/blog/tor-memory-optizations-what-actually-works.html)，在一台繁忙的 guard relay 上從約 5.7 GB 降到 1.2 GB 以下，主要原因是避開了目錄快取物件頻繁汰換造成的碎片化。

## TPM 的角色

TPM（Trusted Platform Module，可信任平台模組）是主機板上的專用硬體晶片，負責儲存加密金鑰並用它們執行運算，私鑰從不暴露給作業系統。TPM 可以 seal 一份秘密，也就是把它綁定到機器的特定量測狀態，只有量測到的軟體堆疊與建立金鑰時完全相同，金鑰才能使用。

對無狀態 relay 來說，身分金鑰存在硬體裡，可以跨重開機保留，即使機器遭到實體接觸，也無法用一般方法抽取。TPM 也支援遠端證明（remote attestation），晶片可以向外部系統證明機器開機時載入了哪些軟體，並附上以硬體為信任根的簽章。如此一來，不必信任營運者，也能驗證節點實際執行的內容。

TPM 也有解決不了的地方，例如 Tor 使用的 ed25519 金鑰不受 TPM 晶片支援，金鑰雖然經過 TPM 加密，仍以位元組字串存放在非揮發性記憶體，技術上還是有可能匯出。

sealing 還要求事先決定 TPM 要信任哪些軟體狀態。更新核心或 bootloader 時量測狀態會跟著改變，營運者必須預測下一次開機的量測結果，重新 seal TPM。

## 既有的部署路線

不同的營運者在部署的簡便程度與安全深度之間，選了不同的取捨點。

### 最小化的 RAM disk

最簡單的做法是全部放在 RAM 裡執行，金鑰手動管理。[Tor-ramdisk](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html) 從 2015 年起就採用這種做法，身分金鑰透過 SCP 匯出與匯入，重開機前沒有匯出就只能從頭開始。這條路線沒有 TPM、遠端證明與 verified boot，唯一的保證是斷電後 RAM 的內容不會留存，但跟傳統把狀態存在磁碟上的部署相比，仍是有意義的改進。

### 以 VM 執行的 RAM disk

[Emerald Onion](https://blog.emeraldonion.org/evolving-our-tor-relay-security-architecture) 在 Proxmox hypervisor 上替每個 relay 執行一份 Alpine Linux 映像（每份 66 MB），VM 完全開機到 RAM 裡，不掛載任何持久儲存。身分用 Tor 的 OfflineMasterKey 功能管理，長期的 master key 在離線環境產生，從不經過 relay。更新的方式是重建映像，回滾很容易，也不需要特殊硬體。

### 裸機與綁定 TPM 的身分

我們開發的 [Patela](https://github.com/osservatorionessuno/patela) 走偏向硬體的路線。relay 透過 [stboot](https://docs.system-transparency.org/st-1.3.0/docs/reference/stboot-system/) 開機，這個 bootloader 會先下載已簽署的作業系統映像並驗證簽章，再交出控制權。開機之後，節點透過 mTLS 向中央伺服器取得設定。中央伺服器即使遭入侵，攻擊者也只能讓服務中斷，無法把憑證推送到節點，也無法從節點抽取金鑰。relay 的身分金鑰存在 TPM 的非揮發性記憶體，綁定量測過的開機狀態，可以跨重開機保留，即使遭到實體接觸也無法抽取。代價是營運更複雜，需要裸機，每次更新後也要重新 seal。

## 尚未解決的問題

有些問題只出現在我們的部署，有些是所有無狀態 relay 都會遇到的。

### 更新後的重新 sealing

軟體堆疊改變時，TPM 的量測狀態也跟著改變。要自動化重新 sealing，就得預測更新後的開機量測值，目前仍是較難的未解問題之一。systemd-pcrlock 等工具正朝這個方向發展，但還無法開箱即用。

### 無狀態重開機與升級的衝突

我們用標準的 unattended upgrades 更新 Tor 執行檔，但重開機會回到作業系統映像，映像裡還是前一個版本，結果變成非預期的降版。自動安全更新與無狀態映像要如何兼顧，我們還沒有完全解決。

### 記憶體限制

沒有 swap，行程超出可用記憶體時會在沒有預警的情況下被終止，而 Tor 執行時的記憶體用量很難預測。前面提到的配置器替換幫助很大，但根本的限制仍在。

### 網路穩定性

持久的更新只能透過重建映像、重新開機來套用。relay 若太常重新啟動，可能失去 Stable 旗標，影響網路分配給它的流量。

## 未來方向

### 遠端證明

sealing 把金鑰綁在機器的狀態上，attestation 則讓節點向外部證明自己處在該狀態。設定伺服器，或將來的 Tor directory authority 這類驗證方，可以發出加密挑戰，只有執行預期軟體堆疊的節點能正確回應。開機完整性因此從只能在本機確認的性質，變成可以遠端驗證，對營運者的信任需求也隨之降低。

### 透明日誌

有了量測過的開機鏈，就能把量測結果公開。relay 營運者提供可重現建置的做法，任何人都能重新計算預期的雜湊值，比對是否與 TPM 回報的一致。只能附加寫入的透明日誌（transparency log）可以讓這些證明接受公開稽核，Tor 社群也可以執行獨立的監測服務，追蹤整個 relay 群的狀態。

### 機密運算

VM 路線可以再結合 AMD SEV-SNP 等技術，把 guest VM 的記憶體與 hypervisor 本身隔離。結合之後同樣能降低對營運者的信任需求，也能縮小 VM 與裸機路線之間的安全差距。

### 更小的硬體

Walking onions 是一項提案中的 Tor 協定擴充，節點不再需要在本機保存整個網路的視圖。如果 arti 與相關工具能在更小的硬體上執行，目前負擔不起資源成本的裝置也有機會用來營運 relay。

## 結語

對 Tor 這類應用，無狀態設計同時能防範攻擊與減少營運者的操作失誤。再經過更多研究與工程，還有機會提高整個網路的可信度。

無狀態系統有實際的營運成本，也有真正困難的未解問題，資源較多的專案與組織同樣要面對。不過它可以作為改進隱私基礎設施的基礎，類似的概念與框架也能用在技術堆疊的其他部分。

這項工作從 [Tor Community Gathering 2025](https://tcg2025.4711.se/sessions/stateless_tor_relay/) 開始，目前仍在進行。如果你營運 relay、開發 Tor 相關工具，或思考過上述任何一個問題，我們很想聽聽你的想法。

## 參考資料

- [Stateless Tor Relay – Tor Community Gathering 2025](https://tcg2025.4711.se/sessions/stateless_tor_relay/)
- [Patela v1: A Basement Full of Amnesic Servers](https://osservatorionessuno.org/blog/2025/05/patela-a-basement-full-of-amnesic-servers/)
- [Patela v2: From Certificates to Hardware](https://osservatorionessuno.org/blog/2025/12/patela-v2-from-certificates-to-hardware/)
- [stboot System Documentation – System Transparency](https://docs.system-transparency.org/st-1.3.0/docs/reference/stboot-system/)
- [Tor-ramdisk 20150714 Release Announcement](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html)
- [Evolving Our Tor Relay Security Architecture – Emerald Onion](https://blog.emeraldonion.org/evolving-our-tor-relay-security-architecture)
- [Tor Memory Optimizations: What Actually Works – 1AEO](https://1aeo.com/blog/tor-memory-optizations-what-actually-works.html)

---

## 台灣營運者的觀點

以下由 anoni.net 社群補充。台灣網路普及、商業託管成熟，同時身處區域資訊衝突的壓力之下，同一套技術方案常要兼顧快速上線與高壓下的實際考驗。

台灣既有的小型主機供應、資料中心服務與公民科技社群，可以幫助營運者比較快建立標準化的映像、事件應變流程與可驗證的運作紀錄。不過台灣的 relay 多由志工分散維運，遇到濫用通報、設備處置要求或執法單位接觸時，流程若沒有事先準備好，技術設計再好也無法降低營運者個人承擔的風險。放到台灣的條件來看，下面三個方向值得先著手。

### 志工營運與法律程序

台灣的 relay 與 exit 營運者可以先整理機房通知、執法接觸與設備扣押的標準應變流程。技術上先把可擷取的資料降到最低，事件發生時營運者個人承擔的風險也比較小。

### 硬體取得與供應鏈成本

具備 TPM 的主機、小型伺服器與代管服務在台灣都可以取得，但成本差距很大。社群若能整理出幾組可重現的硬體與映像組合，維運與稽核的成本比較容易控制。每個團隊各自組一套的話，安全主張難以互相比較，維護成本也會持續增加。

### 可驗證運算的公共討論

量測開機鏈、遠端證明與透明日誌的用途不限於 Tor 的技術圈，也跟公民科技、關鍵基礎設施透明度的討論有關。這些證明要成為社群共享、外界能理解的證據，才能支撐社會的信任。若只有少數技術人員能讀懂，外界的信任仍只能依靠口碑。

## 相關閱讀

- [Tor Relay 架設指南](/join/setup-tor-relay/)：中間節點的架設步驟與維運設定
- [Tor Relay 校園建立研究專題](/join/relay-on-campus/)：在大專院校架設 relay 的評估與經驗
