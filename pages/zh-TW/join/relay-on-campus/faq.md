---
title: 給校方與法務的校園 Tor Relay FAQ
description: 校方資訊中心、法務與網管對校園 Tor Relay 最常提出的十個疑慮與回應建議，附給網管與給行政法務的兩份一頁摘要。
---

在校園架設 Tor Relay，資訊中心、法務與網管最常提出的疑慮大致是同樣十個。本頁從[校園 Tor Relay 提案範本](/join/relay-on-campus/proposal/)衍生，每題補上台灣脈絡，可以附在提案文件後面，或在面談前先寄給對方參考。

[Tor Relay 架設指南](/join/setup-tor-relay/)末尾的 FAQ 寫給個人營運者，本頁的讀者則是學校行政、法務與網管，重點放在學校的風險評估，以及被問到時如何回答。

各題的「台灣脈絡補充」以台灣的首例與法規為準，一般性的回答在其他地區同樣適用。在台灣以外提案時，請把這些段落換成當地的對應內容。

## 使用方式

- **提案時**：附在計畫書後面當作附錄一
- **面談前**：寄給資訊中心、網管、法務先讀一遍
- **被問到時**：展開對應的問題，複製內容引用
- **頁尾的兩份一頁摘要**：30 秒可以讀完，適合放在 email 開頭，或在會議上當作發給對方的書面資料

## 常見疑慮

??? question "為什麼大學適合架設 Tor Relay？"

    學術網路的頻寬穩定，資工、資安與資訊中心本來就有架設與維運的人力。架設可以從風險最低的 Non-Exit Relay 開始，不經手出口流量，也不需要處理對外連線引起的投訴。節點隨時可以停止，是可以撤回的決定。架設與維運的過程本身就是匿名網路、資安與開源治理的教學案例。重視學術自由與資訊近用的學校，也能藉此把理念落實到基礎建設。

    **台灣脈絡補充**

    國立臺灣師範大學資訊工程學系已完成台灣首例（2025 年 11 月上線），過程見 [Tor Project 部落格的客座文章](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)與[社群訪談](/updates/2025/12/ntnu-nz/)。台灣的高教體系本來就承擔資訊工程、資訊安全與網路治理的教學，校園 Tor Relay 可以當作實際的教學案例。

??? question "我們不想架設 Exit Relay，這樣可以嗎？"

    可以，Tor 網路需要各種類型的 Relay 才能維持健康。預設情況下，架設的 Relay 會擔任 Entry 或 Middle Relay，只在 Tor 節點之間轉送加密流量。Entry 與 Middle Relay 是維護成本最低的形式，也不會收到出口流量引起的投訴。

    另外也可以選擇同時營運 Bridge 或 [Tor Snowflake](docs:tools/tor-snowflake/) 代理，協助身處網路審查地區的使用者連上 Tor。

    **台灣脈絡補充**

    台灣的校園案例（台師大）就是 Non-Exit Relay。建議台灣所有校園 Relay 計畫都從 Non-Exit 開始，不要嘗試 Exit Relay，Exit Relay 的法律與行政成本遠超出個人或學生社團能負擔的範圍。

??? question "願意營運 Relay，但不想處理濫用問題，該如何處理？"

    Exit Policy（出口政策）就是為此設計的，每個 Tor Relay 都有一份，指定允許或拒絕哪些對外連線。Exit Policy 透過目錄服務發布給 Tor 用戶端，用戶端會自動避開拒絕該連線的 Exit Relay。每個 Relay 可以依濫用風險與自身情況，決定允許的服務、主機與網路。

    預設的 Exit Policy 允許許多常見服務（例如網頁瀏覽），但會限制濫用風險高的服務（例如郵件），以及 Tor 網路無法負荷的服務（例如檔案分享的預設連接埠）。

    允許部分出口連線時，請務必確認 DNS 解析正常運作。

    **台灣脈絡補充**

    校園計畫最簡單的做法是設定 `ExitPolicy reject *:*`，關閉所有對外連線。流量不會從這個 Relay 出去，所以幾乎不會收到濫用投訴（仍建議備妥 EFF 的 abuse 回應範本）。設定細節見[校園 Tor Relay 架設 SOP](/join/relay-on-campus/sop/#torrc-參考設定)。

??? question "Tor 不是會讓犯罪分子做壞事嗎？"

    Tor 的使命是促進人權，以自由、開源的技術協助使用者抵抗大規模監控與網路審查。Tor 社群一向譴責把工具用於不法用途的行為。

    犯罪的意圖在於人，不在工具，加密、電話、現金都可能被惡意使用，Tor 也一樣。移除 Tor 之後，有惡意的人會改用其他工具，並不會因此停手。

    Tor 與其他隱私工具同時保護真正需要的人，可以防範身分盜用、實體跟蹤等犯罪，也能協助執法單位調查案件、支援受害者。

    **台灣脈絡補充**

    刑法第三十六章妨害電腦使用罪（第 358 條至第 363 條）規範的是具體行為，例如無故輸入他人帳號密碼而入侵他人電腦（第 358 條），以及無故取得、刪除或變更他人電腦的電磁紀錄（第 359 條）。Middle Relay 不接觸內容、不解析使用者資料、不知道使用者身分，性質與網路傳輸基礎設施相近，與前述條文的犯罪構成要件無關。

    個人資料保護法第 2 條把個人資料定義為「得以直接或間接方式識別該個人之資料」。Middle Relay 處理的是 Tor 網路的加密 cell，沒有可識別個人的資料，因此不涉及個資的處理。節點被選為入口節點（Guard）時，會看到連入用戶端的 IP 位址，但不知道對方要連到哪裡，Tor 預設的日誌設定（`SafeLogging 1`）也會把位址遮掉。IP 位址是否構成個人資料，要看能否與其他資料比對、識別出特定個人，這一點建議一併諮詢法律專業人員。

    以上是社群整理的法律觀點，並非正式的法律意見。個案的法律疑慮，建議諮詢法律專業人員。

??? question "分散式阻斷服務攻擊（DDoS）的風險呢？"

    DDoS 攻擊通常仰賴成千上萬台電腦同時發送 UDP 封包，塞滿受害者的頻寬。

    Tor 只傳輸完整的 TCP 連線，不傳輸任意的 IP 封包，所以無法傳送 UDP 封包，也無法發動 SYN Flood 這類攻擊。常見的 DDoS 攻擊手法無法透過 Tor 進行。

    Tor 也不允許頻寬放大攻擊，送進 Tor 多少資料，Tor 就只送出多少資料。攻擊者若真的擁有足以發動 DDoS 的頻寬，也不需要經過 Tor。

    **台灣脈絡補充**

    目前沒有台灣 ISP 針對 Middle Relay 發出 DDoS 投訴的紀錄。台師大的節點自 2025 年 11 月上線以來，也沒有收到 DDoS 相關的通報。

??? question "垃圾郵件（Spam）的風險呢？"

    Tor 預設的 Exit Policy 拒絕所有 SMTP（25 連接埠）流量，無法直接透過 Tor 傳送垃圾郵件。

    少數 Relay 可能開放 SMTP，風險與架設一台開放式郵件伺服器相同，並非 Tor 帶來的特有風險。垃圾郵件發送者也可能透過 Tor 連到開放的 HTTP Proxy、利用有漏洞的 CGI 腳本寄信，或控制殭屍網路，在沒有 Tor 的情況下同樣可以做到。

    許多垃圾郵件手法（例如偽造的 UDP 封包）無法透過 Tor 進行，因為 Tor 只支援 TCP。

    **台灣脈絡補充**

    校園 Relay 設定 `ExitPolicy reject *:*` 之後，SMTP 流量也不會送出，校園 Non-Exit Relay 沒有垃圾郵件的問題。

??? question "Tor 常被濫用嗎？"

    Tor 用 Exit Policy 降低濫用風險，每個 Relay 都能決定允許或拒絕哪些服務，並公告給用戶端。Tor Project 也有專責的 Network Health 團隊，負責調查惡意 Relay 並將它們移出網路。

    Tor 的設計刻意讓 Tor Project 與 Relay 營運者都無法監控使用者的行為，因此能為人權工作者、記者、家暴倖存者、吹哨者與執法單位提供可靠的隱私與匿名保護。

    **台灣脈絡補充**

    對校園 Non-Exit Relay 而言，濫用的概念基本上不適用，因為節點不會接觸使用者最終要存取的內容。經過節點的流量都是 Tor 節點之間的加密轉送，與外部網站之間至少還隔著一個 Relay。

??? question "架設 Exit Relay 會遇到哪些情況？"

    允許出口連線的 Relay，遲早會收到濫用投訴，例如：

    - 有人透過 Tor 連到 Hotmail 寄出勒索信，FBI 等執法單位聯絡你，說明之後通常會被接受
    - 有人透過 Tor 在 Google Groups 發送垃圾訊息，你的 ISP 收到投訴信
    - 有人透過 Tor 在 IRC 搗亂，你的伺服器可能遭到 DDoS
    - 有人透過 Tor 下載盜版電影，你的 ISP 可能收到 DMCA 侵權通知，依 EFF 建議的範本回覆，通常不會有法律責任

    各家網路服務供應商對 Tor Exit Relay 的接受程度不同，有些願意配合，有些則較嚴格。部分網站也會封鎖 Exit Relay 的 IP，這是常見的情況。要營運 Exit Relay，最好使用不影響其他業務的專用 IP。

    **台灣脈絡補充**

    強烈不建議在台灣的校園架設 Exit Relay，台灣學術網路（TANet）的對外連線需經教育部審核，Exit Relay 的流量無法預期，與審核框架不相容。此外，目前沒有先例可以引用，溝通成本會增加。學生或社團負責人通常也無法承擔可能的法律或行政後果。

    對 Exit Relay 有興趣，建議在海外對 Tor 友善的雲端供應商租用個人 VPS 試行，不要把校園資源牽扯進來。

??? question "如何回應 ISP 的投訴？"

    Tor 社群已經整理出完整的回覆範例，Relay 營運者可以照著範本回覆 ISP，見 [EFF Tor Legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/) 與 [Tor abuse-templates](https://community.torproject.org/relay/community-resources/tor-abuse-templates/)。

    **台灣脈絡補充**

    校園 Non-Exit Relay 不會與外部網站直接通訊，理論上不會收到 ISP 投訴。如果真的收到投訴信（例如對方誤以為這是 Exit Relay），可以這樣回應：

    1. 確認投訴事件的時間，以及目的 IP 或網址
    2. 出示 `ContactInfo` 與 `ExitPolicy reject *:*` 的設定截圖
    3. 引用 [Tor Project 對各類 Relay 的說明](https://community.torproject.org/relay/types-of-relays/)，Non-Exit Relay 只在 Tor 網路內轉送加密流量，不會與最終目的地建立連線
    4. 必要時請指導教授或學校法務協助

??? question "Tor 如何處理技術被濫用的問題？"

    Tor Project 譴責任何把技術用於犯罪的行為，並在能力範圍內處理惡意行為，例如封鎖惡意 Relay。

    Tor 的設計讓它無法監控或禁止使用者的行為，雖然可能被惡意利用，但更多時候保護了真正需要的人，包括人權工作者、記者、家暴倖存者、吹哨者、執法人員，以及其他需要隱私保護的群體。

    **台灣脈絡補充**

    台灣社會近年對揭弊者保護、家暴與跟蹤騷擾防制、新聞自由的關注持續增加。Tor 在這些情境對台灣使用者的價值與其他國家相同，架設校園 Relay，是讓這套基礎設施在台灣可用的具體貢獻。

    延伸閱讀：[揭弊者保護法的技術觀察](docs:taiwan/whistleblower-law/)、[家暴受害者的數位準備](docs:scenarios/domestic-violence/)。

## 給網管的一頁摘要

!!! info "網管與資訊中心技術人員的 30 秒摘要"

    **節點類型**

    - Tor Relay（中繼節點），不是 Exit Node
    - 只在 Tor 網路內轉送加密流量，不與外部網站直接通訊

    **部署需求**

    - 一組固定 IPv4
    - 對外只開放 1 個 TCP 連接埠（ORPort 9001 或 443）
    - 選用 80 或 443 連接埠提供狀態頁
    - 其餘連接埠全部關閉

    **不會發生的事**

    - 不解析、不記錄使用者流量
    - 不會收到濫用投訴（Non-Exit）
    - 不會增加校園邊界防火牆的負荷
    - 不會影響校園的 DNS 或內容過濾政策

    **可撤回性**

    - 停止 systemd 服務，10 分鐘內即可下線
    - 隨時可以移除，不影響校園網路環境

    **參考案例**

    - 全球多所大學都有營運，包括 MIT、Stanford、Cambridge、CMU
    - 台灣首例：[國立臺灣師範大學資訊工程學系（2025 年 11 月上線）](/updates/2025/12/ntnu-nz/)
    - 國際計畫：[EFF Tor University Challenge](https://toruniversity.eff.org/zh-tw/)

## 給校方行政與法務的一頁摘要

!!! info "校方行政與法務的 30 秒摘要"

    **計畫背景**

    在校園架設 Tor Relay，是參與 EFF（Electronic Frontier Foundation）推動的 Tor University Challenge 國際計畫。全球已有多所大學參與，包括 MIT、Stanford、Cambridge、CMU。

    **法律定位**

    - 架設的是 Non-Exit Relay，法律上的性質與網路傳輸基礎設施相近
    - 不接觸使用者內容，不識別個人資料
    - 與刑法妨害電腦使用罪章、個資法的構成要件無關（社群整理的觀點，並非正式法律意見）
    - EFF 提供法律與技術資源

    **對學校的意義**

    - 以實際的基礎建設表明學校重視資訊自由與隱私保護
    - 列名 Tor University Challenge 的國際大學名單
    - 教學：資訊工程、資訊安全與網路治理的教學案例
    - 研究：網路研究與課程的素材

    **營運影響**

    - 隨時可以下線（10 分鐘內）
    - 由學生與指導教授共同維運，學校的行政負擔很低
    - 不需要修改現有的校園防火牆或內容過濾政策

    **參考案例**

    - 台灣：[國立臺灣師範大學資訊工程學系（2025 年 11 月上線）](/updates/2025/12/ntnu-nz/)
    - 國際：[Tor Project 部落格的 Setting Up a Tor University Relay in Taiwan](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)

!!! tip "下一步"

    依目前的進度選擇：

    - **還沒寫提案**：回到[校園 Tor Relay 提案範本](/join/relay-on-campus/proposal/)，改寫成自己學校的版本，並把本頁附在後面
    - **提案已通過**：依[校園 Tor Relay 架設 SOP](/join/relay-on-campus/sop/) 進行技術上線
    - **只是被問到 Tor Relay**：把[給網管的一頁摘要](#給網管的一頁摘要)或[給校方行政與法務的一頁摘要](#給校方行政與法務的一頁摘要)直接轉給對方

## 相關閱讀

- [Tor Relay 校園建立研究專題](/join/relay-on-campus/)：三份範本的入口與專題的進度
- [校園 Tor Relay 提案範本](/join/relay-on-campus/proposal/)：供各校改寫成自己版本的提案文件
- [校園 Tor Relay 架設 SOP](/join/relay-on-campus/sop/)：torrc、UFW、監控與事件處置的技術細節
- [在台師大架設 Tor Relay](/updates/2025/12/ntnu-nz/)：台灣首例的完整過程
- [EFF Tor Legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)：以美國法為基礎的完整法律 FAQ（英文）

## 資料來源與致謝

本頁十題的主體由社群夥伴**蘇恩立（NZ）**提供，整理自他在台灣師範大學的計畫書原始版本，台灣脈絡補充由匿名網路社群 anoni.net 整理。原始材料經 NZ 同意，以 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hant) 授權釋出。
