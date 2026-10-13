---
title: 文件站互動區與 Tor 中繼地球儀的開放資料授權
description: 文件站互動區的三件 Tor 作品，以及製作中繼地球儀時查過的二十幾份公開資料，哪些授權允許再散布、哪些受阻在條款。
date: 2026-07-28
kind: new
og_image: https://assets.anoni.net/games/tor-network.png
---

![Tor 中繼地球儀](https://assets.anoni.net/games/tor-network.png){ .shot }

文件站新增了[互動與呈現](docs:games/)區，目前收錄三件以 Tor 為題的作品。資料量最大的是 [Tor 中繼地球儀](docs:games/tor-network/)，把全球近萬台運作中的中繼標在球面上，其中超過六成集中在美國、德國、荷蘭。

製作地球儀時，我們查了二十幾份公開資料，最後可用的只有六份。多數 API 都能正常回應，資料格式也乾淨，受阻的原因幾乎都在條款不允許再散布。


## 用畫面呈現的理由

匿名網路的基礎建設很難用文字說清楚，難處在順序與規模。

Tor 的順序最具代表性。封包在三個中繼之間依序前進，每經過一跳剝除一層加密，到出口才還原成原本的請求。哪一層在哪一跳剝掉、每一站看得到什麼，都由這個順序決定。文字寫得再仔細，讀者仍需在腦中自行補上封包移動的過程，每個人補出來的版本未必相同。

規模更難傳達。「近萬台中繼，高度集中在少數國家」是一句讀過即忘的敘述，把每一台實際標到地球上，北美與西歐連成一片光帶，其餘地區只有零星幾點。同一份數字換成畫面，讀者不必仰賴我們的形容詞，可以自行判斷。

## 地球儀用到的六份資料

| 資料 | 來源 | 授權 |
|------|------|------|
| 中繼分布 | [Onionoo](https://metrics.torproject.org/onionoo.html) | CC0 1.0 |
| 使用者與橋接人數 | [Tor Metrics](https://metrics.torproject.org/) | CC0 1.0 |
| 連線受阻的觀測 | [OONI](https://ooni.org/) | CC BY-NC-SA 4.0 |
| 斷網事件 | [Access Now KeepItOn](https://www.accessnow.org/keepiton-data-dashboard/) | CC BY 4.0 |
| 海底電纜 | [OpenStreetMap](https://www.openstreetmap.org/copyright) 貢獻者 | ODbL 1.0 |
| 國界與海岸線 | [Natural Earth](https://www.naturalearthdata.com/) | public domain |

Onionoo 的中繼快照經過蒸餾，只保留國家層級的聚合，不含 fingerprint、nickname、IP 或聯絡資訊。ASN 的登記名稱另外過濾過，因為個人申請的 AS 在 RIR 登記的是持有人本名。對在審查嚴格地區營運中繼的人來說，公開這個名稱，等於把中繼的歸屬與身分證上的名字一起公開。

陸地亮度可以切換四種指標。中繼台數最直觀。共識權重（consensus weight）反映該國實際承擔的流量比重，常與台數有明顯落差。單一業者集中度是最大一家托管商在該國的占比，數字愈高，該國的匿名流量愈依賴同一個機房持續運作與配合。使用者估計是需求端的數字，跟前三個供給端指標並列時，兩端的落差本身就是資訊。

!!! info "2026-07-31 補上的三份資料"

    發表後地球儀又加入三份資料，授權檢查的標準相同。

    | 資料 | 來源 | 授權 |
    |------|------|------|
    | 上網人口比例 | [World Bank](https://data.worldbank.org/indicator/IT.NET.USER.ZS) | CC BY 4.0 |
    | 台灣的上網人口比例 | [數位發展部 國家數位近用調查](https://moda.gov.tw/digital-affairs/digital-service/operations/208) | 政府資料開放授權條款-第1版 |
    | 海底地形 | [Natural Earth](https://www.naturalearthdata.com/) | public domain |

    上網人口比例當作分母使用。畫面原本只呈現各國使用 Tor 的人數，這個數字很大一部分反映的是人口多寡。知道該國有多少比例的人上網，才能判斷兩國的落差是否只因為其中一國上網的人本來就少。

    World Bank 那份涵蓋的 217 個經濟體裡沒有台灣，對本站來說是個尷尬的缺口。台灣的數字改取自數位發展部的調查，兩份的方法論不同，一份是 ITU 彙整各國通報，一份是對 12 歲以上人口的電話抽樣，畫面上註明不宜直接比較。缺口來自資料政治，跟前面的授權限制不同類，結果同樣由下游的使用者承擔。

    海底地形跟國界同源，沒有新的授權要處理。地球儀取 200、1000、3000、5000 公尺四層等深線，最淺那一層就是大陸棚。加上海底地形之後，海纜那一層才有解釋力。海纜幾乎都沿著陸棚鋪設、避開深海盆，兩層對照可以看出纜線走那些路徑的原因。

    順著海纜又查了登陸點，登陸點是整條纜線最脆弱的位置，台灣的幾處尤其受到關注。OpenStreetMap 本身沒有收錄這份資料，用 taginfo 查全球數量，`man_made=cable_landing_point`、`seamark:type=landing_point` 等五個候選標籤都是 `0` 筆。登陸點座標跟纜線幾何一樣是 TeleGeography 商品的一部分，受阻在同一道條款（2026-10 補註：之後地球儀以數位發展部公開的海纜清單為骨幹，逐點交叉查證座標，自建了台灣 14 處登陸點的資料集，細節見 [Tor 中繼地球儀](docs:games/tor-network/)的說明頁）。

## 刻意克制的呈現

OONI 的資料最能說明我們的取捨。OONI 提供各國 Tor 測試的異常率（anomaly rate），數字看起來足以畫一張全球審查地圖，中段卻是量測雜訊。實測瑞士 `22.2%`、加拿大 `21.2%`、紐西蘭 `41.1%`，這些國家都沒有審查疑慮。把中段畫成色階，等於用雜訊指控特定國家。

畫面最後只標示異常率達 `85%` 以上且樣本足夠的少數國家，中段數值一律不上色，措辭也停在「沒有照預期完成」。`85%` 這個門檻沒有推導公式，是看過分布之後訂的。雜訊最高落在四成上下，拉到 `85%` 才留出足夠的距離，我們寧可漏掉幾個真的受阻的國家，也不要把沒問題的國家標紅。

Access Now 的斷網事件則相反，每一筆都經過人工查證、成因清楚，可以明確標示此處發生過人為斷網。武裝衝突與族群衝突造成的中斷未必出自政府決策，可能是戰事破壞了基礎設施，畫面上與資訊管制類分開說明。

基於同樣的理由，我們放棄了 V-Dem 的數位社會指標。V-Dem 的授權在技術上可用，但資料是每個國家每年由約五位專家評分，再經統計模型轉成連續量表。把專家評分畫成地圖色塊，等於用我們的畫面替某個機構的政治判斷背書。

## 無法使用的資料

### 海底電纜

一開始想用領域內最權威的 [TeleGeography](https://www.submarinecablemap.com/) Submarine Cable Map，查下去才發現座標資料已經是 TeleGeography 販售的正式商品。[License TeleGeography's Map Data](https://www2.telegeography.com/license-geocoded-map-data) 採年費授權，GeoJSON 經 Amazon S3 或 API 交付、每次更新自動推送，GeoJSON 就是商品本體。

台灣的[海纜動態地圖](https://smc.peering.tw/)在授權不明朗時採取了務實的做法。程式碼以 MIT 授權開源，幾何資料放在另一個對外回應 404 的 repo，主 repo 的 README 直接寫「You can leave the folder empty」。

地球儀上的海纜最後取自 OpenStreetMap 貢獻者標註的路徑，共 `228` 段，以歐洲、地中海與大西洋較完整，太平洋中段幾乎是空的。OSM 社群 [2011 年的討論串](https://lists.openstreetmap.org/pipermail/talk/2011-October/060415.html)裡，有人提議把 TeleGeography 的資料併進 OSM。社群成員判斷那份授權禁止商業使用與改作，跟 ODbL 不相容，提議之後沒有下文。十五年後，太平洋中段仍然是空的。

### 網路基礎建設

網路基礎建設這一類查了一輪，幾乎全部受阻，理由也相近。

[RIPE Atlas](https://atlas.ripe.net/) 部署在各地的量測節點（probe）資料品質很好，`2026` 年 7 月查詢時全球有近六萬個節點，含經緯度與 ASN，API 可以直接取得。服務條款則寫明商業使用需另外取得 RIPE NCC 許可，也沒有開放授權宣告。PeeringDB 的 API 同樣可以存取，可接受使用政策則寫明不可整批轉散布給第三方。Packet Clearing House 的 IXP 目錄是 CC BY-NC-SA 3.0，Cloudflare Radar 是 CC BY-NC 4.0，兩者的非商業條款都會延伸到我們的內容上。

[IODA](https://ioda.inetintel.cc.gatech.edu/) 是其中最可惜的一份。IODA 以 BGP 路由撤除、主動探測與 darknet 流量異常偵測各國的網路中斷，屬於實際量測，主題跟本站高度吻合。API 有回傳資料，回應裡卻附上一行 `Copyright (c) 2021-2025 Georgia Tech Research Corporation. All Rights Reserved.`。

完全沒有條款的資料是另一類。各 RIR 的 delegated stats 檔案可以下載，開頭只有免責聲明，沒有一個字提到授權。root-servers.org 的節點清單有 JSON 端點，整站找不到授權宣告。沒有聲明不能解讀成允許，又比明文禁止更難處理，因為連判斷的依據都沒有。

### 指數類資料

Freedom House 的 Freedom on the Net 與無國界記者（RSF）的新聞自由指數最常被引用，兩份都無法使用。RSF 的授權是 CC BY-**ND**，禁止改作，轉成 JSON 重新呈現就違反條款。Freedom House 的官方頁面查不到授權聲明，取得資料需要寫信申請。

## 沒有個別詢問授權的原因

依開放資料圈的常規做法，讀完條款之後會再去信詢問一次，通常有機會取得非營利或研究用途的例外。上面這幾個機構，我們刻意沒有這麼做。

製作地球儀想了解的，正是一個下游再利用者實際會遇到什麼。如果每一份受阻的資料都靠個別協商解決，得到的會是幾封友善的回信，無法回答開放資料圈對想接手的人有多友善。條款寫成什麼樣子，就是絕大多數人實際遇到的樣子。沒有人脈、沒有機構背景、只是想做點東西的人，看到的就是那一頁條款，所以本文只記錄條款本身。

## 開放 API 與開放資料的落差

我們原本以為困難會在技術面，結果多數端點都能存取、資料格式也乾淨，受阻的全在條款，開放 API 不等於開放資料。RIR、CAIDA、RIPE NCC、PeeringDB 這些機構的預設立場是可以看、可以研究，但不能整批搬走，跟 Tor Metrics、OONI、Natural Earth 的文化完全不同。完全沒寫授權的資料也算在內，實務上等同不可用。業界確實有很多工具在用這類檔案，風險由使用者各自承擔，公開發布的文件站不能比照辦理。

文件站的架構也不容許「應該沒問題」的僥倖。文件站是靜態網站，資料檔會直接發布出去，還會推上 IPFS。內容定址的資料發出去就收不回來，鏡像可能長期存在。

相對地，地球儀能夠完成，很大程度是因為 Tor Project 把 Onionoo 與 Tor Metrics 都以 CC0 釋出，Natural Earth 則屬公有領域。當年可能只是一行設定，十幾年後一個不相干的社群就能直接取用，不必寫信談授權，也不必擔心哪天被要求下架。

OONI 的資料採 CC BY-NC-SA 4.0，其中的相同方式分享（ShareAlike）跟網站的 CC BY 4.0 互不相容。處理方式是讓 `ooni.json` 保持獨立的一份，內容不併進其他資料檔，畫面上也只跟其他來源並列，讓整體屬於 CC 定義的「集合」，相同方式分享的範圍停在那一份檔案。`NOTICE` 已經寫明這個前提，避免日後有人把 OONI 的欄位併進中繼快照，讓整份衍生物落入相同方式分享的範圍。

## 另外兩件作品

[Tor 路由解謎](docs:games/onion-routing/)讓讀者自行挑選三個中繼，組成 guard、middle、exit 路徑，過程中要避開被監聽的節點、把三跳分散到不同 ASN，遇到封鎖則改走橋接。看著電路因為三跳擠在同一個 ASN 而失敗，比讀十次「要分散」更容易記住。

[Tor 連線流量](docs:games/onion-rendezvous/)用發光粒子呈現兩種路徑的差異。連線 .onion 服務時，雙方各建一條三跳電路，在隨機選出的會合點相遇。連線明網網站時，則是走三跳到出口後原路往返。

三件作品都以 three.js 在瀏覽器中執行，免安裝，支援正體中文、簡體中文與英文。原始碼在 [anoni-net/docs](https://github.com/anoni-net/docs) 的 `docs/zh-TW/games/` 底下，沒有建置流程，修改後存檔、重新整理即可看到結果。

有想法的話，歡迎到[社群](/join/)找我們一起參與製作。
