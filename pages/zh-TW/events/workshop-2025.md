---
title: 匿名網路工作坊 2025/08
description: 2025 年 8 月 9 日到 10 日在國立臺灣科技大學舉辦的兩天工作坊，匿名網路社群 anoni.net 帶參與者實際操作 Tor、Tails 與 OONI，另有五場圓桌討論，談開源工具的信任、社群節點與在地化的工具包。
---

![匿名網路工作坊招募工作人員與培訓小幫手](docs:assets/images/event-workshop-2025.png){ .shot }

新聞記者、公民團體與人權倡議者在工作上面對通訊遭攔截、身分遭追蹤的風險，受訪者的安全也可能因此受到威脅。匿名網路工作坊為他們安排了兩天的實作與討論，用開源的匿名網路工具把通訊的掌控權取回自己手上，減少對單一平台的依賴。

- 日期：2025/08/09（六）、2025/08/10（日）
- 地點：國立臺灣科技大學 研揚教學大樓 TR-510 教室
- 形式：工作坊、圓桌討論

!!! info "活動紀錄"

    工作坊已經結束，頁面保留當時公布的議程。各場次的共筆可以從議程表的「共筆」連結閱讀，活動之後的整理見[2025/08 專案進度更新](/updates/2025/09/updates-202508/)。

匿名網路社群 anoni.net 負責技術支援與實作引導，介紹 [Tor](docs:tools/what-is-tor/)、[Tails](docs:tools/what-is-tails/)、[OONI](docs:tools/what-is-ooni/) 等開源匿名網路工具，帶參與者準備第二台安全裝置、以匿名方式連線，並實際測量網路審查。

## 工作坊的學習內容

### 數位安全與匿名技術

- 用 Tor 網路匿名瀏覽
- 以 Tails 與 USB 隨身碟建立**第二工作環境**，不在使用的電腦上留下紀錄
- 基礎的威脅模型評估，包含認識對手、評估風險與對應的行動
- 在網路受到審查的國家或環境，用橋接（bridge）與 [Snowflake](docs:tools/tor-snowflake/) 連上 Tor

### 實作與工具

- 用 Tails 製作**可攜式匿名作業系統**，在公用或不受信任的裝置上安全工作
- [OONI Probe](https://ooni.org/install/) 測量網路審查與服務封鎖的方式，以及把結果回報到全球公開的資料庫
- 用 [Tor Browser](https://www.torproject.org/zh-TW/download/) 與 [OnionShare](docs:tools/onionshare/) 安全地分享檔案與協作

### 社群支援與持續學習

- 台灣在地的匿名網路社群（見[關於我們](/about/)）
- 參與國際開源專案（例如 Tor、Tails、OONI）的貢獻方式
- 活動後的技術諮詢與進階學習資源

### 適用情境

- 採訪敏感議題、聯繫**揭弊者**與**吹哨者**（見[公益揭弊者保護法的總統府公報](https://www.president.gov.tw/Page/294/49717)）、跨境協作查核資料
- NGO 跨國合作，或在網路受到限制的國家與地區倡議時，建立匿名的通訊與行動管道
- 組織內部數位安全訓練與 SOP 制定的參考基礎

## 圓桌討論的主題

### 在地參與與基礎建設

- **開源與匿名網路**：Tor、Tails、OONI 背後的開源理念，以及保護隱私、抵抗審查為何需要自由軟體。
- **在地參與**：台灣的使用者如何成為 Tor 與 OONI 的在地貢獻者，讓匿名網路工具更貼近在地的語言與文化。
- **社群節點的建立與維運**：協助架設 Tor relay、OONI 測試點等基礎節點，參與網路自由的基礎建設，同時認識其中的風險與貢獻方式。

### 去中心化的推廣與協作

- **台灣在地的開源匿名工具包**：把這些工具整合成 NGO、新聞媒體與獨立記者容易上手的匿名工具包。
- **去中心化推廣的策略與挑戰**：去中心、開源協作的推廣計畫如何在台灣落地，以及教育、技術與社群三方面的人力如何分配。
- **與印太地區匿名網路社群的連結**：區域合作的潛力與現況，以及與印太地區其他倡議者交流、協作的方式。

---

## 各場次內容

### 場地

活動分成工作坊與圓桌討論兩種形式，在兩天內進行，場地約可容納 30 到 45 人。

- 日期：2025/08/09（六）、2025/08/10（日）
- 地點：國立臺灣科技大學 研揚教學大樓 TR-510 教室
    - 教學大樓位在基隆路三段 155 巷、台大癌醫中心那一側，從臺科大正門進入要走一段距離
    - 位置見[學校地圖](https://www.ntust.edu.tw/p/412-1000-102.php?Lang=zh-tw)上標記 `15` 的建築

### OONI 網路審核干預資料分析

- 時間：`2025/08/09 12:30 - 13:30 UTC+8`{style="color: green; font-weight: bold;"}
- 內容：
    - OONI 計畫簡介
    - OONI Probe 的運作方式
        - 行動裝置版的安裝與使用，以及台灣觀測名單未更新的問題
    - 用 OONI Explorer 介面解讀觀測資料
        - 時間區間的資料、國家與類別的比較、觀測結果的判定
    - 用 OONI Run v2 建立觀測網站名單
        - 建立自己的觀測名單，並在 OONI Explorer 查閱自己的觀測結果
    - 其他與 OONI 類似的觀測計畫
        - Cloudflare Radar、IODA、Sinar Project

### Tor/Tails 匿名網路工作坊

- 時間：`2025/08/09 13:30 - 15:30 UTC+8`{style="color: green; font-weight: bold;"}
- 內容：
    - 第二台裝置的概念與使用情境
        - 把工作與個人活動分開，保護線上身分與資料
    - Tails 匿名作業系統
        - Tails 與 Tor 洋蔥網路的整合，以及如何用來匿名瀏覽與通訊
    - Tor 的運作原理
        - 連上 .onion 網站的方式
    - 實際安裝 Tails
        - 在 USB 隨身碟上安裝並設定 Tails，用於線上與離線的安全作業

兩場工作坊都需要用到筆記型電腦，參與者自備設備，現場另外架設了臨時網路供教學使用。

### 工作坊講座

講座是兩天活動中唯一的一場，內容回顧 Roger 在 RightsCon 2025 台北的演講，包括 Tor 在世界各地的現況、大眾把 Tor 洋蔥路由網路等同於暗網的誤解，以及如何保護個人隱私、推動網路自由相關的政策。

| 形式/日期/時間 | 討論議程 |
| --- | --- |
| <span class="tag tag--solid">講座</span><br>2025/08/09<br>10:30-11:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1030)</span> | <span class="tag-text"><i data-icon="simple-torproject"></i> Tor 在網路監控的世界中捍衛個人線上隱私權</span><br><i data-icon="arrow-right-bottom"></i>回顧 Tor Project 創辦人分享的網路自由現況，以及 Tor 在保護使用者隱私上的工作。<br><i data-icon="arrow-right-bottom"></i>技術遭到濫用或誤解，讓大眾對暗網產生刻板印象，以及改善的方式。<br><i data-icon="arrow-right-bottom"></i>教育使用者保護個人隱私，支持或參與政策倡議，推動合理的網路自由政策。 |

### 圓桌討論

工作坊之外另有五場圓桌討論，主題是新聞媒體、獨立記者、公民團體與開源技術社群共同參與的可能，也邀請參與者談對匿名網路社群未來的想像，以及社群能在技術與資源上提供哪些協助。

| 形式/日期/時間 | 討論議程 |
| --- | --- |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/09<br>11:30-12:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1130)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「自由軟體與數位人權：為何開源是匿名工具的關鍵？」</span><br><i data-icon="arrow-right-bottom"></i>對記者與公民團體來說，開源為何重要？如何建立對工具的信任？<br><i data-icon="arrow-right-bottom"></i>可驗證性（verifiability）、抵禦審查與社群治理等核心價值。<br><i data-icon="arrow-right-bottom"></i>開源與封閉的商業資安工具，如何選擇？ |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/09<br>15:30-16:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1530)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「推動一個去中心、開源協作的匿名網路推廣計畫」</span><br><i data-icon="arrow-right-bottom"></i>以公民科技社群與開源社群的協作模式推廣，可以如何分工？<br><i data-icon="arrow-right-bottom"></i>能否成立「開源維運小組」（工作小組模式），維護 Tor 與 OONI 的伺服器，並定期測試 ISP 的封鎖狀況？<br><i data-icon="arrow-right-bottom"></i>哪些非技術角色（設計、翻譯、講師、寫手）可以參與？ |

| 形式/日期/時間 | 討論議程 |
| --- | --- |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/10<br>11:00-12:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d2-1100)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「從使用者到貢獻者：台灣如何建立 Tor/OONI 的社群節點與回饋模式」</span><br><i data-icon="arrow-right-bottom"></i>台灣是否已有 Tor relay、OONI Probe 等基礎節點？運作情況如何？<br><i data-icon="arrow-right-bottom"></i>實際會遇到哪些技術、行政與法律上的挑戰？（例如主機費用、遭到封鎖、法律疑慮）<br><i data-icon="arrow-right-bottom"></i>能否以社群的方式協助運作，並培訓新手？ |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/10<br>13:00-14:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d2-1300)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「Tor/Tails/OONI 的開源基礎與在地參與可能」</span><br><i data-icon="arrow-right-bottom"></i>這些工具如何運作？採用哪些自由軟體與開源授權？<br><i data-icon="arrow-right-bottom"></i>台灣的開發者或資安研究者可以參與哪些部分？（例如翻譯、bug 回報、撰寫教學）<br><i data-icon="arrow-right-bottom"></i>如何降低技術上的距離感，讓更多人願意貢獻？ |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/10<br>14:00-15:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d2-1400)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「如何在地化一套開源匿名工具包？」</span><br><i data-icon="arrow-right-bottom"></i>從日常瀏覽（Tor）、作業系統（Tails）到網路監測（OONI），還有哪些開源工具可以納入？<br><i data-icon="arrow-right-bottom"></i>工具包該包含哪些內容？（例如 Live USB 映像檔、在地語系包、手冊）<br><i data-icon="arrow-right-bottom"></i>適合 NGO、記者與新手的「台灣版本」簡化套件。 |

## 完整時程表

- 日期：2025/08/09（六）、2025/08/10（日）
- 地點：國立臺灣科技大學 研揚教學大樓 TR-510 教室

<figure markdown="span">
  ![活動時程表](docs:assets/images/event_workshop_2025_schedule.svg)
  <figcaption>兩天活動的預定時程。</figcaption>
</figure>

### 8 月 9 日（六）

| 形式/日期/時間 | 討論議程 |
| --- | --- |
| <span class="tag tag--solid">講座</span><br>2025/08/09<br>10:30-11:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1030)</span> | <span class="tag-text"><i data-icon="simple-torproject"></i> Tor 在網路監控的世界中捍衛個人線上隱私權</span><br><i data-icon="arrow-right-bottom"></i>回顧 Tor Project 創辦人分享的網路自由現況，以及 Tor 在保護使用者隱私上的工作。<br><i data-icon="arrow-right-bottom"></i>技術遭到濫用或誤解，讓大眾對暗網產生刻板印象，以及改善的方式。<br><i data-icon="arrow-right-bottom"></i>教育使用者保護個人隱私，支持或參與政策倡議，推動合理的網路自由政策。 |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/09<br>11:30-12:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1130)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「自由軟體與數位人權：為何開源是匿名工具的關鍵？」</span><br><i data-icon="arrow-right-bottom"></i>對記者與公民團體來說，開源為何重要？如何建立對工具的信任？<br><i data-icon="arrow-right-bottom"></i>可驗證性（verifiability）、抵禦審查與社群治理等核心價值。<br><i data-icon="arrow-right-bottom"></i>開源與封閉的商業資安工具，如何選擇？ |
| <span class="tag tag--solid">工作坊</span><br>2025/08/09<br>12:30-13:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1230)</span> | <span class="tag-text"><i data-icon="tools"></i> OONI 網路審核干預資料分析</span><br><i data-icon="arrow-right-bottom"></i>OONI 計畫簡介<br><i data-icon="arrow-right-bottom"></i>OONI Probe 的運作方式<br><i data-icon="arrow-right-bottom"></i>用 OONI Explorer 介面解讀觀測資料<br><i data-icon="arrow-right-bottom"></i>用 OONI Run v2 建立觀測網站名單<br><i data-icon="arrow-right-bottom"></i>其他與 OONI 類似的觀測計畫 |
| <span class="tag tag--solid">工作坊</span><br>2025/08/09<br>13:30-15:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1330)</span> | <span class="tag-text"><i data-icon="tools"></i> Tor/Tails 匿名網路工作坊</span><br><i data-icon="arrow-right-bottom"></i>第二台裝置的概念與使用情境<br><i data-icon="arrow-right-bottom"></i>Tails 匿名作業系統<br><i data-icon="arrow-right-bottom"></i>Tor 的運作原理<br><i data-icon="arrow-right-bottom"></i>實際安裝 Tails |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/09<br>15:30-16:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d1-1530)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「推動一個去中心、開源協作的匿名網路推廣計畫」</span><br><i data-icon="arrow-right-bottom"></i>以公民科技社群與開源社群的協作模式推廣，可以如何分工？<br><i data-icon="arrow-right-bottom"></i>能否成立「開源維運小組」（工作小組模式），維護 Tor 與 OONI 的伺服器，並定期測試 ISP 的封鎖狀況？<br><i data-icon="arrow-right-bottom"></i>哪些非技術角色（設計、翻譯、講師、寫手）可以參與？ |

### 8 月 10 日（日）

| 形式/日期/時間 | 討論議程 |
| --- | --- |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/10<br>11:00-12:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d2-1100)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「從使用者到貢獻者：台灣如何建立 Tor/OONI 的社群節點與回饋模式」</span><br><i data-icon="arrow-right-bottom"></i>台灣是否已有 Tor relay、OONI Probe 等基礎節點？運作情況如何？<br><i data-icon="arrow-right-bottom"></i>實際會遇到哪些技術、行政與法律上的挑戰？（例如主機費用、遭到封鎖、法律疑慮）<br><i data-icon="arrow-right-bottom"></i>能否以社群的方式協助運作，並培訓新手？ |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/10<br>13:00-14:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d2-1300)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「Tor/Tails/OONI 的開源基礎與在地參與可能」</span><br><i data-icon="arrow-right-bottom"></i>這些工具如何運作？採用哪些自由軟體與開源授權？<br><i data-icon="arrow-right-bottom"></i>台灣的開發者或資安研究者可以參與哪些部分？（例如翻譯、bug 回報、撰寫教學）<br><i data-icon="arrow-right-bottom"></i>如何降低技術上的距離感，讓更多人願意貢獻？ |
| <span class="tag tag--solid">圓桌討論</span><br>2025/08/10<br>14:00-15:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> 共筆](https://pad.anoni.net/p/ws-note-d2-1400)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i>「如何在地化一套開源匿名工具包？」</span><br><i data-icon="arrow-right-bottom"></i>從日常瀏覽（Tor）、作業系統（Tails）到網路監測（OONI），還有哪些開源工具可以納入？<br><i data-icon="arrow-right-bottom"></i>工具包該包含哪些內容？（例如 Live USB 映像檔、在地語系包、手冊）<br><i data-icon="arrow-right-bottom"></i>適合 NGO、記者與新手的「台灣版本」簡化套件。 |

## 相關頁面

- [籌備：匿名網路工作坊 2025/08](/events/workshop-2025-prepare/)：活動前的工作人員與培訓小幫手招募
- [2025/08 專案進度更新](/updates/2025/09/updates-202508/)：活動後的整理，以及在研討會會場放置的匿名網路手冊
- [延續 2025，走向 2026：個人隱私指引、Tor Relay 校園建立競賽、匿名支付探索](/updates/2026/01/2025to2026/)：2025 年的活動回顧與 2026 年的三個主題
- [COSCUP 2026 匿名網路社群議程軌](/events/coscup-2026/)：2026 年 8 月在同一間教室舉辦的兩天社群議程
