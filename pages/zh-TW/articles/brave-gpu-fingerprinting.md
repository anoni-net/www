---
title: Brave 抹平 GPU 指紋的兩種相反手法
description: Brave 1.93 預設啟用的三項 GPU 指紋防護、一致化與隨機化在 WebGL 與 WebGPU 之間的分工，以及與 Tor Browser、Firefox 做法的對照。
date: 2026-08-19
---

網頁上的 JavaScript 可以取得顯示卡型號、驅動資訊，以及硬體支援哪些功能。回傳的值在同一台電腦上幾乎不變，追蹤公司把它們與其他裝置特徵組合起來，就成了一組不需要 cookie、不需要使用者同意、跨網站跟著使用者的識別碼。

顯示卡是瀏覽器指紋的來源之一，字型清單、螢幕尺寸、時區、音訊運算結果同樣算在裡面，本文只處理顯示卡（整套機制與各家瀏覽器的預設狀態見文件站的[瀏覽器指紋說明](docs:basics/browser-fingerprinting/)）。

Brave 從 1.93 版起處理這組訊號，桌面版與 Android 版預設開啟、分批推送[^brave]。三項防護分別是把 WebGL 的廠商與繪圖器字串換成所有 Brave 使用者一致的通用字串、清空 WebGPU 的硬體描述欄位，以及在 WebGL 支援的擴充清單注入雜訊。

前兩項讓所有使用者看起來一樣，第三項讓同一個使用者在每個網站看起來都不一樣。兩種方向相反的手法在同一次更新裡各自負責不同的 API，分工的界線也是 Brave 與 Tor Browser 在指紋抗性上分歧的起點。

## 顯示卡資訊的識別力

WebGL 與 WebGPU 讓網站使用硬體加速繪圖，地圖、遊戲、資料視覺化都仰賴它們。為了讓網站能針對硬體調整繪圖方式，兩組 API 也把底層的硬體細節開放給 JavaScript 查詢。

網站能取得的資訊有三類[^brave]：

- **廠商與繪圖器字串**：透過 `WEBGL_debug_renderer_info` 擴充提供的 `UNMASKED_VENDOR_WEBGL` 與 `UNMASKED_RENDERER_WEBGL` 兩個參數[^mdn]，網站會取得類似 `ANGLE (Apple, ANGLE Metal Renderer: Apple M5 Max)` 的字串，精確到晶片型號。除錯用的擴充最早是 Chrome 為了 Google Maps 開放，後來所有網站都能呼叫。
- **支援的擴充清單**：同一個 WebGL context 會回報它支援的完整擴充清單，內容隨 GPU 與驅動而異，追蹤者把整份清單雜湊成一組精簡的識別碼。
- **WebGPU 的硬體描述**：較新的 WebGPU API 會回傳 adapter 的 `vendor`、`architecture` 與 `device` 欄位，例如 `{vendor: 'apple', architecture: 'metal-3'}`。

顯示卡不會天天更換，所以這些值長期穩定，比 cookie 更難清除。使用者換帳號、開無痕視窗、清空瀏覽紀錄，API 回報的硬體特徵仍是同一組。

Brave 做了一次小規模的網路爬取，分析排行前段的網站呼叫這些 API 之前的呼叫堆疊（stack trace）。公告裡的結論是多數網站呼叫它們的唯一用途是瀏覽器指紋識別[^brave]，爬取規模與比例沒有公開。

## 一致化與隨機化的分工

| 訊號 | Brave 的處理 | 手法性質 |
|------|--------------|----------|
| WebGL 廠商與繪圖器字串 | 換成單一通用字串，所有 Brave 使用者取得相同的值 | 一致化 |
| WebGPU 的 adapter 描述 | 清空 `vendor`、`architecture`、`device` | 一致化 |
| WebGL 擴充清單 | 注入雜訊，每個 session、每個網站（eTLD+1）、每個儲存區取得的值都不同 | 隨機化 |

第三項沿用 Brave 既有的 farbling 機制，Brave 在 2020 年的隱私更新裡把它定義為「對半識別性的瀏覽器功能輸出做輕微隨機化，讓網站難以偵測，又不破壞良性、以使用者為本的網站」[^farbling]。

## farbling 的種子機制

瀏覽器啟動時產生一組隨機的 session token，再與每個造訪的第一方頂層框架網域經 HMAC256 混合，得出每個網域一組、壽命與 session 相同的 token[^farbling]。同一個網站在同一個 session 內重複量測會取得完全相同的值，換一個網站取得不同的值，下一個 session 再全部換過。第三方 frame 與 script 沿用頂層 eTLD+1 的種子[^farbling]，所以無法靠嵌入第三方內容繞過。

指紋器會把大量半識別特徵雜湊成單一識別碼，只要其中一項被隨機化，整組雜湊值就被汙染。技術源頭是 PriVaricator（WWW 2015）與 FPRandom（ESSoS 2017）兩項研究[^farbling]。

## 擴充清單改走隨機化的原因

公告裡沒有寫擴充清單改走隨機化的原因，從 API 的用途推測，改動兩種資料對網站功能的衝擊差距很大。

廠商與繪圖器字串主要用於效能調校與硬體黑名單。網站取得的字串不在既有清單裡時，最壞的結果是改走一般繪圖路徑。把值收斂成一個常數，該欄位對指紋的貢獻直接歸零，代價有限。

擴充清單用於功能協商，網站依清單裡是否有某個擴充，決定啟用哪條繪圖路徑或改走哪一種後備方案。給一份與硬體實況不符的統一清單，網站可能選到硬體無法支援的路徑，也可能放棄本來可用的加速。剩下的做法是在保留可用性的前提下加入雜訊，讓雜湊值不穩定。

一致化降低熵（entropy），讓某一項特徵失去區辨力，理想狀態是全世界的 Brave 使用者在該欄位完全相同。注入雜訊則破壞可連結性（linkability），值仍然帶有資訊，但每個網站、每次取得的都不一樣，追蹤者無法把兩個網站上的同一位使用者串在一起。

## Tor Browser 與 Firefox 的做法

Tor Project 部落格 2019 年的指紋介紹文章，開頭就寫著「所有 Tor 使用者應該有完全相同的指紋」。當時的具體做法包含在所有平台回報同一組作業系統資訊、統一時區與螢幕解析度，以及 letterboxing。letterboxing 在內容周圍加上灰邊，把可視區域對齊到固定尺寸，避免最大化的視窗洩漏螢幕大小[^tor]。

隨機化的風險也寫在同一篇文章裡，文中引用 Eckersley 提出的「可指紋化的隱私增強技術悖論」（Paradox of Fingerprintable Privacy Enhancing Technologies）。文中的例子是某個擴充套件改掉一批數值，卻漏改 `navigator.platform`，造出一組現實中不存在的特徵組合，使用者反而更容易被辨認[^tor]。要讓隨機化有效，覆蓋範圍必須夠完整，Brave 持續擴充 farbling 的端點清單也是同一個原因。

Firefox 系的瀏覽器在 `privacy.resistFingerprinting` 開啟時直接停用 `WEBGL_debug_renderer_info`，網站呼叫不到這個擴充[^mdn]。該開關預設關閉，需要使用者自行到 `about:config` 開啟。停用之後網站取不到值、需要自行處理空值。回傳通用值時，網站收到的資料與真實硬體無異，可以照常運作。Brave 選擇回傳通用值，與它一貫壓低功能損壞風險的取向一致。公告裡的另一項主張是防護要預設開啟，不藏在特殊模式或旗標後面[^brave]。

Brave 在 2020 年說明 farbling 的更新裡建議，需要對抗定向攻擊的使用者改用 Tor Browser[^farbling]。隨機化擋得住大規模部署的商業追蹤，但不提供匿名集（anonymity set）。

## 實務上的界線

Brave 這次更新最實際的價值是預設生效，多數人不會為了隱私去改 `about:config`、切換特殊模式或安裝擴充套件，公告裡也寫了擴充套件本身帶有安全與隱私問題[^brave]。要確認更新是否生效，可以用 EFF 的 [Cover Your Tracks](https://coveryourtracks.eff.org/) 檢查瀏覽器回報的 WebGL 廠商與繪圖器字串，更新完整推送之後兩個欄位會變成通用值[^brave]。

需要匿名時仍要用 Tor Browser，因為 Brave 的隨機化只處理跨站串接。IP 位址照樣直接送到網站，網路路徑上的觀察者也看得到連線的目的地。Tor 在中國大陸受到重度封鎖，需要橋接或其他接入方式，在台灣、香港、澳門、新加坡、馬來西亞一般可以直連（逐地的可達性與法規見文件站的[東亞與東南亞出差準備](docs:scenarios/asia-travel/)）。

Tor Browser 的一致化路線靠所有使用者維持相同的樣貌，安裝擴充套件、最大化視窗、改動字型設定，都會讓使用者從人群裡凸顯出來（細節見文件站的 [Tor Browser 進階設定](docs:tools/tor-browser-advanced/)）。同一個動作在 Brave 上影響有限，在 Tor Browser 上會直接破壞防護的前提。寫給一般讀者的完整說明見文件站的[瀏覽器指紋說明](docs:basics/browser-fingerprinting/)。

## 尚未涵蓋的範圍

公告發布時（2026-08），WebGPU 支援的擴充清單還沒納入隨機化，公告裡寫了之後會補上[^brave]。圖形 API 仍是指紋研究的活躍領域，新的洩漏管道會持續出現。

網站功能受損的情況仍在觀察中，Brave 保留了逐站調整防護的能力。遇到確實無法正常運作的網站，使用者可以單站關閉圖形防護、關閉指紋防護，或整個關掉 Shields[^brave]。保留這些開關代表取捨仍在，一致化與注入雜訊都無法保證所有網站維持原本的行為。

顯示卡之外，字型清單、canvas 繪圖結果、音訊運算特徵仍然可以用來識別瀏覽器。能安全收斂成常數的訊號就收斂，牽涉功能協商的訊號就注入雜訊，檢視其他標榜指紋抗性的工具時也可以用同一條分工線對照。

## 相關閱讀

- [瀏覽器指紋是什麼，為什麼很難擺脫](docs:basics/browser-fingerprinting/)：指紋由哪些特徵組成、結構上難以規避的原因，以及各家瀏覽器的預設狀態
- [社群平台怎麼收集你的資料](docs:basics/platform-tracking/)：裝置指紋在整套追蹤機制裡的位置
- [Tor Browser 進階設定](docs:tools/tor-browser-advanced/)：指紋抗性與視窗大小的實際操作
- [威脅模型如何建立](docs:basics/threat-model/)：先確認要防範誰，再選工具

[^brave]: [Brave improves protections against GPU fingerprinting](https://brave.com/privacy-updates/38-webgl-webgpu-fingerprinting-protections/) - Brave 隱私更新第 38 篇。本文引用的三項防護、爬取觀察、相容性處理與後續規劃皆出自此文。查證日 2026-08-14。
[^farbling]: [Fingerprinting defenses 2.0](https://brave.com/privacy-updates/4-fingerprinting-defenses-2.0/) - Brave 隱私更新第 4 篇，2020 年。farbling 的定義、HMAC256 種子機制與研究出處出自此文，第三方 frame 沿用頂層種子的說明另見 Brave 的 [Fingerprinting Protections wiki](https://github.com/brave/brave-browser/wiki/Fingerprinting-Protections)。wiki 頁面會被持續編輯，查證日 2026-08-18。
[^tor]: [Browser Fingerprinting: An Introduction and the Challenges Ahead](https://blog.torproject.org/browser-fingerprinting-introduction-and-challenges-ahead/) - Pierre Laperdrix，The Tor Project 部落格，2019 年 9 月 4 日。一致化路線、letterboxing 與可指紋化隱私增強技術悖論的說明出自此文，文中的具體做法對應撰文當時的 Tor Browser 版本，該悖論一詞出自 Eckersley 的 PETS 2010 論文，由本文引用。查證日 2026-08-18。
[^mdn]: [WEBGL_debug_renderer_info](https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_debug_renderer_info) - MDN Web Docs。兩個常數的定義，以及 Firefox 在 `privacy.resistFingerprinting` 為 true 時停用此擴充的說明。查證日 2026-08-18。
