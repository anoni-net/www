---
title: 社群 VPN 服務發布 Vessel
description: 匿名網路社群 anoni.net 為身邊的人架設的 VPN，在學校、旅館與國外這些 VPN 常無法連線的地方也能使用。介紹台北、東京與新加坡的節點、中繼路線、網域過濾，以及取得邀請碼的方式。
date: 2026-11-07
kind: new
og_image: https://assets.anoni.net/vessel/og-zh-tw-d6c00920.png
---

<figure markdown="span">
    <a href="https://vessel.anoni.net/" target="_blank">
        <img src="https://assets.anoni.net/newsletter/newsletter-vessel-overview-zh-tw-orig-59490d4a.png"
            alt="等角投影的藍圖樣式示意圖。你和身邊的人的裝置避開流量檢查，直接或經台北入口連到台北、東京與新加坡的節點，再經過列有詐騙網站的過濾名單，連到網際網路" class="shot">
    </a>
</figure>

在學校、旅館或國外，常用的 VPN 不一定能連上，遇到問題也不容易找到人詢問。[Vessel](https://vessel.anoni.net/){target="_blank"} 是匿名網路社群 anoni.net 為身邊的人架設的 VPN，連線經過偽裝，在 VPN 連線受到封鎖的網路裡也比較容易連上。不需要 email，也不用付費，有問題有人回應。

!!! tip "取得邀請碼"

    Vessel 目前以邀請碼分批開放，邀請碼透過電子報寄給訂閱者，歡迎[訂閱電子報](https://form.anoni.net/s/cmc9ceju1000dlj017fiathzq){target="_blank"}。也可以寄信到 whisper@anoni.net，或寫在[意見回覆](https://vessel.anoni.net/feedback/){target="_blank"}並留下聯絡方式，跟我們說明你的需要。

10 月 28 日寄出第一波邀請碼之後，我們依照大家的使用狀況調整服務。目前新增了台北節點與經台北入口的中繼路線，直接連線不穩時多一條路可以選擇，網域過濾也補上台灣的詐騙網站名單。

## 產品標準的設計與營運

Vessel 是一項會長期維運的服務，我們用產品的標準來設計、調整與營運，也會持續開發下去。做每項決定時，我們先看使用者連線時遇到的實際狀況，包含能否連上、步驟是否簡單、出問題時有沒有人處理。

節點分散在台北、東京與新加坡，分屬不同的主機商，某個城市的網路受阻或某家主機商出狀況時，還有其他路線可選。直接連線不穩時可以改走中繼路線，之後也會依使用狀況與意見回覆增加城市。

VPN 之外，我們也持續開發使用者的加值功能，不另外收費。第一項是網域過濾的阻擋保護名單，我們比對各份公開名單的涵蓋範圍，補上不足的部分，再依新的資料來源與使用者的回報調整。

日常營運同樣照這個標準，新增功能時要讓不懂技術的人也能照著步驟完成，改動之後在桌機與手機實際檢查並執行自動測試。服務狀況公開在[服務狀態](https://vessel.anoni.net/status/){target="_blank"}頁，我們也持續檢查偽裝的方式與節點被探測的跡象，意見回覆有人閱讀、會處理。

## 台北、東京與新加坡的節點

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-map-orig-5f1fb0f8.png"
        alt="方格組成的東亞與東南亞地圖，台北、東京與新加坡各有一座燈塔，三座燈塔之間以虛線相連" class="shot">
</figure>

節點是你的連線連到網際網路之前經過的主機。建立裝置時選擇城市，想換城市就新增一台裝置。台北節點的主機在 Greenhost 的台北機房，從中華電信（台灣）連線的延遲約 2 毫秒，連到東京或新加坡則要 35 到 67 毫秒。台北節點的頻寬比較小，適合日常瀏覽，大量下載建議選東京或新加坡。

我們找了一段時間都沒有合適的台灣主機，社群營運的服務也不容易獲得主機商支持。Greenhost 收到來信後同意讓我們試行，協助開通了台北機房。謝謝 Greenhost。

## 經台北入口的中繼路線

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-fig04-zh-orig-b3065627.png"
        alt="等角投影的示意圖。裝置先連到台北入口，由入口轉送、不解開加密內容。連線再通往東京、台北或新加坡節點，出口是你選的城市" class="shot">
</figure>

中繼路線的連線分成兩段，架構跟 Apple 的 iCloud Private Relay 相近。連線先到台北的入口，再原封不動轉送到你選的節點。入口收到的資料有你的 IP 與加密過的封包，從中無法得知你連往哪裡，也只統計經過的流量。節點連上網站時取得的資料有連線目的地，來源則是入口的 IP，不含你的 IP。Vessel 與 iCloud Private Relay 的差別是，Apple 的兩段分屬不同公司，Vessel 的入口與節點都由社群營運。

網路業者只能看到你連到入口，無法得知你實際使用哪個節點。直接連到節點不穩或無法連線時，也可以改走中繼路線。

新增裝置時，在城市下方選擇「台北入口 → 東京」、「台北入口 → 新加坡」或「台北入口 → 台北」，出口是節點所在的城市。想改用中繼路線的話，新增一台裝置即可。

## 網域過濾與台灣的詐騙網站名單

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-fig02-zh-orig-faca315a.png"
        alt="等角投影的示意圖。裝置連往網站之前，依序經過惡意程式、釣魚網站與詐騙網站三道名單，名單上的網域被擋下" class="shot">
</figure>

新增裝置時可以選擇網域過濾，裝置連往網站之前會先向節點上的 DNS 解析器（把網域名稱查成 IP 的服務）查詢，名單上的惡意網站會直接被擋下。我們組合多份公開的名單，各自涵蓋不同的類別：

- **惡意程式與釣魚網站**：HaGeZi 的 Threat Intelligence Feeds，每 8 小時更新
- **台灣的詐騙網站**：台灣警政署 165（反詐騙諮詢專線）停止解析的涉詐網站，以及台灣數位產業署停止解析的詐騙購物網站
- **廣告與追蹤**：選擇擋廣告時再加上 HaGeZi Multi PRO，每天更新

HaGeZi 的名單來源以歐美為主，10 月 31 日比對台灣 165 列管的 8.6 萬個涉詐網域，只有 0.2% 在 HaGeZi 的名單上，因此我們先補上 165 的名單。之後再盤點其他公開的來源，台灣數位產業署的 1,734 個詐騙購物網域裡，約 15% 不在現有名單上而且還在運作，所以也一起加入。接下來會繼續評估其他華語地區公開的警示資料。

從 9 月的網域抽出 149 個查詢，中華電信（台灣）的 DNS 全部回應封鎖頁，Cloudflare 的 1.1.1.1 卻有 103 個解析到真正的網站。不論你從哪裡連上 Vessel，查詢都會改走節點的解析器，當地電信業者的 DNS 封鎖也就不再生效。

要更換已建立裝置的過濾設定，需刪除裝置再重新建立。在[網域過濾](https://vessel.anoni.net/dns/){target="_blank"}頁可以查詢某個網站是否在名單上。

## 從設計開始的隱私與資安

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-exploded-zh-orig-7e046afc.png"
        alt="四層疊起的分解圖，由上而下是你的裝置（私鑰只在這裡）、入口網站（不需要 email、帳號號碼只存雜湊、不留誰邀請了誰）、節點（防火牆紀錄關閉、換頁不寫入硬碟）與公開的圖紙（程式碼與主機設定都在 GitHub）" class="shot shot-narrow">
</figure>

連線用的私鑰（只留在裝置上的金鑰）在你的瀏覽器產生，帳號不需要 email，帳號號碼只存雜湊（無法還原回號碼的單向運算結果），都是一開始就放進設計裡的做法（privacy and security by design）。邀請碼兌換之後也不留下誰邀請了誰。上線之後我們持續調整，例如關掉節點防火牆的紀錄、停止把記憶體的換頁寫入硬碟，減少節點硬碟上可能留下的連線資訊。

Vessel 網站的程式碼與節點的主機設定，都完整公開在 [GitHub](https://github.com/anoni-net/vessel){target="_blank"}。歡迎大家一起檢視、查核，發現問題或有更好的修正與功能，都可以開 issue 或送 pull request。

## 藍圖樣式的網站

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-design-sheet-zh-orig-e336b47d.png"
        alt="藍圖樣式的設計稿，並排 Vessel 首頁的桌機與手機版面，旁邊標出方塊字標題、等角示意圖、方格紙底色與細線方框，下方列出色票與字型" class="shot">
</figure>

[Vessel 的網站](https://vessel.anoni.net/){target="_blank"}是工程藍圖的樣式，鈷藍色的線條、方格紙的底色，標題是一格格方塊疊成的 Vessel。

Vessel 有船的意思，造船之前要先畫圖紙。每個零件的位置與尺寸都標在圖紙上，檢查時也看同一份。VPN 服務的網站上常見盾牌與鎖頭的圖案，使用者仍然無法得知內部如何運作。我們希望大家信任的是實際的做法，所以把網站畫成一張攤開的圖紙，連線經過哪些節點、名單如何比對、金鑰在哪裡產生，都畫在首頁。

Vessel 也有容器的意思，你的連線會先裝進加密的通道再出發，沿路的網路業者看到的是外層偽裝過的封包，無法取得裡面的內容。到了節點，封包才取出來送往網站，連線的目的地與時間不會寫進紀錄。

社群的主機與頻寬跟容器一樣有固定的容量，所以每個帳號每月有 50 GB 的額度，邀請碼也依使用狀況分批發送。我們希望先維持好容量內的服務，有問題時有人回應，再逐步增加節點與名額。

首頁的方塊標題也依照這個意思設計，像素小人扛著鈷藍色的封包跳過字母，壓進最後的 l，整個字由下往上慢慢裝滿。

## 使用前要知道的事

Vessel 不提供匿名，你連往的網域與 IP 會經過節點，需要匿名時請使用 Tor Browser。服務由志工維運，不保證服務不中斷。偽裝能降低被封鎖的機會，但不保證每個網路都能連上（規則見[使用條款](https://vessel.anoni.net/terms/){target="_blank"}）。

有些地方限制或禁止未經核准的 VPN，在當地使用 Vessel 也可能受罰，當地的網路業者仍然可以看到裝置連到境外的 IP。處境敏感時，請先讀常見問題的[所在地限制 VPN 時，使用 Vessel 安全嗎？](https://vessel.anoni.net/faq/#q-risky){target="_blank"}與文件站的[出差與研討會的數位準備](docs:scenarios/asia-travel/)，再決定是否使用。

## 分享給朋友的邀請碼與意見回覆

如果你認識我們的社群，也認同社群維運、程式碼公開的做法，歡迎把 Vessel 分享給身邊需要的人。帳號建立滿 14 天、而且有裝置連線過之後，可以在[帳號](https://vessel.anoni.net/account/){target="_blank"}頁的「邀請朋友」產生一組邀請碼。邀請碼請給認識、信任的人使用，不要公開張貼。邀請碼 7 天內有效，只能用來建立一個帳號。

使用上遇到問題、連線品質不穩，或希望加開其他城市的節點，請寫在[意見回覆](https://vessel.anoni.net/feedback/){target="_blank"}，也可以透過以下管道聯絡：

- **即時討論**：Matrix 公開聊天室（家伺服器 `im.anoni.net`，連結見[社群服務頁](/services/)）
- **匿名線索**：whisper@anoni.net（[GPG 公鑰](/contact/)）

## 相關閱讀

- [Vessel 的常見問題](https://vessel.anoni.net/faq/){target="_blank"}
- [VPN 的風險與選擇](docs:tools/vpn-guide/)
- [出差與研討會的數位準備](docs:scenarios/asia-travel/)
