---
title: Gears 檔案工作台與本機處理的設計
description: 社群從文件站的小工具延伸出 Gears 檔案工作台的原因，以及它如何用 CSP、套件審查與統計白名單，讓檔案不離開裝置成為讀者能檢查的事。
date: 2026-10-24
---

手機拍的照片裡，通常記著拍攝地點的經緯度、手機型號與精確到秒的時間。聊天截圖上有對方的名字與頭像，Word 檔記著作者、公司名稱，有時還有電腦上的資料夾路徑。這些資訊平常無害，檔案一旦交給記者、貼到網路上，或寄給不完全信任的人，就可能讓提供檔案的人被認出來。

清除這些資訊的線上服務不少，幾乎都要先上傳檔案。為了保護一張照片，先把它交給一台不認識的伺服器，順序是反的。[Gears 檔案工作台](https://anoni.net/gears/)把清除中繼資料、遮蔽個資、加密這些處理放進讀者的瀏覽器，檔案預設不離開裝置。

## 另外做一個產品的原因

Gears 的前身是文件站的[小工具區](docs:utils/)。扣掉機器流量之後，小工具區是文件站首頁以外最多人使用的一區，用得最多的是清除中繼資料、遮蔽、密語產生器、QR code 與網址清理。使用的人多半是一般的正體中文使用者，需求跟 Tor 沒有直接關係。

文件站的小工具守著三條規則：離線可用、頁面不連網、沒有建置流程。規則讓文件站在斷網的地方照樣能用，也讓工具長不大。找人臉只能用 240 KB 的輕量偵測器，合照裡的小臉常常漏掉，清除中繼資料也讀不了 iPhone 預設的 HEIC 照片。從搜尋引擎進來的讀者又幾乎不會逛到小工具區，工具做好了，需要的人卻找不到。

2026-10-14 我們決定把小工具延伸成獨立的產品，文件站的小工具維持原樣。Gears 可以用 npm 套件、打包工具與幾百 MB 的模型，換來文件站做不到的功能：HEIC 照片的清除、PDF 的遮蔽、錄音轉逐字稿、查證收到的檔案。桌面依讀者的目的分成交出去之前、安全地傳送、檢查收到的三組，所有工具共用一個只存在記憶體裡的暫存區，關掉分頁就清空。兩天後第一版上線，逐字稿與查證已經在裡面，遠端傳送接著在 10-20 加入。

![Gears 的桌面，左側是暫存區與選擇檔案的按鈕，右側的工具分成交出去之前、安全地傳送、檢查收到的三組](https://assets.anoni.net/www/articles/gears-local-first-1.zh-TW-0a4cfd98.webp)

## 拿掉「頁面不連網」之後

文件站的小工具有「頁面不連網」這條規則撐著，讀者不必相信我們，也知道檔案不會被送走。Gears 拿掉了這條規則。npm 套件裡有幾萬行不是我們寫的程式，逐字稿的大模型要從 Hugging Face 下載，遠端傳送要經過社群的伺服器。每多一項，檔案會不會被送走就多一分只能聽我們說。

Gears 把頁面能連到哪裡寫死在讀者可以自行檢查的地方，需要連網的功能逐一說明送出了什麼、誰看得到，還做不到的部分照實寫出來，用這種方式守住同一個承諾。下面是做法，以及開發這兩週出過的三個錯。

## 頁面的 CSP

CSP（Content Security Policy，內容安全政策）是網站交給瀏覽器的一份規則，列出頁面可以從哪裡載入程式、可以連線到哪裡，規則以外的請求由瀏覽器直接擋下。Gears 的每個頁面在 `<head>` 裡放一個 meta 標籤，clearnet 版的內容如下（兩個送出網址換成說明）：

```
default-src 'none'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self';
img-src 'self' blob: data:; media-src blob:;
connect-src 'self' <使用統計的送出網址> <建議與回饋的送出網址>;
worker-src 'self' blob:; font-src 'self'; manifest-src 'self';
base-uri 'none'; form-action 'none'
```

重點在 `connect-src`。即使某個相依套件被植入惡意程式，`fetch`、`XMLHttpRequest` 與 WebSocket 也只能連到自己的網域與兩個送出網址，讀者的檔案送不出去。規則就在頁面原始碼裡，在瀏覽器選「檢視原始碼」就看得到，不必相信我們的說法。`wasm-unsafe-eval` 給 HEIC 解碼器與辨識模型用的 WebAssembly，它只允許編譯 WebAssembly，JavaScript 的 `eval` 仍然不能用。

規則產生在 [`vite.config.ts`](https://github.com/anoni-net/gears/blob/main/vite.config.ts) 的 `policy()`。新增任何對外連線都要改那裡，畫面上也要標示，程式審查時一眼就看得出來。

## 逐字稿 Worker 的對外請求

第一個錯出在逐字稿。辨識在 Web Worker 裡執行，避免轉錄時畫面停住。Worker 從網址載入時，套用的是 Worker 腳本自己回應標頭裡的 CSP，頁面 meta 標籤的規則管不到它。

2026-10-15 加入逐字稿時，Transformers.js 帶著自己的一份 onnxruntime-web，預設從 jsDelivr 的 CDN 下載 WebAssembly。當時只有 meta 標籤的 CSP，Worker 不受限制，請求真的送出去了。改法是用 Vite 的 `?url` 匯入那一份 WebAssembly，從自己的網域載入，nginx 也改成用標頭送一份 CSP，Worker 從此受到同一組規則約束。頁面同時有標頭與 meta 標籤時，請求要兩邊都符合才放行，頁面本身仍然只能連到 meta 標籤列出的對象。

同樣的錯誤現在由瀏覽器測試把關。[`tests/e2e/guard.ts`](https://github.com/anoni-net/gears/blob/main/tests/e2e/guard.ts) 在每個測試記下頁面發出的請求與主控台錯誤，連到測試伺服器以外的請求，以及被 CSP 擋下時留在主控台的錯誤，都會讓測試失敗。

逐字稿的 large-v3-turbo 約 760 MB，從社群的主機送出流量太重，改由讀者選擇之後從 Hugging Face 下載。按鈕寫成「從 Hugging Face 下載並開始」，按下之前畫面先說明 Hugging Face 看得到 IP 位址、瀏覽器與下載了哪個模型。標頭的 CSP 只開那幾個模型、鎖定 commit 的下載路徑，每個檔案讀完比對 SHA-256，對不上就不存，請求也不帶 cookie 與 Referer。

![逐字稿選擇模型的畫面，選了 large-v3-turbo 之後，下方說明模型從 Hugging Face 下載、Hugging Face 會看到 IP 位址、瀏覽器與下載的模型，錄音不會送出](https://assets.anoni.net/www/articles/gears-local-first-2.zh-TW-0593ec2a.webp)

## 套件新增的對外連線

CSP 是最後一道防線，平常要靠升級套件時先在套件裡搜尋對外的網址。2026-10-15 Gears 第一次加入找人臉時用的是 MediaPipe。選版本時在套件裡搜尋，發現 `@mediapipe/tasks-vision` 從 1.0.0 起多了送往 `odml.pa.googleapis.com` 的網址，所以停在還沒有這段程式的 0.10.35。CSP 擋得下這種請求，但擋下之後主控台會留下錯誤，也很難確定套件在請求失敗之後走了哪一條路，套件新增的對外連線要在升級時就發現。同一天找人臉因為準確度換成 OpenCV 的 YuNet，MediaPipe 也就從 Gears 拿掉了。

也有只能靠 CSP 的情況。查證工具用 c2pa-web 驗證內容憑證（相機與編輯軟體附在檔案上的來源紀錄），遇到其中的身分聲明時，底下的 c2pa-rs 會連線取得簽發者的金鑰，沒有設定可以關掉（[c2pa-rs issue #1645](https://github.com/contentauth/c2pa-rs/issues/1645)）。這個請求由 CSP 擋下，是 Gears 唯一預期會出現的 CSP 錯誤，測試只放過這一個路徑。

## 網址檢查不送出網址

收到可疑的簡訊連結時，讀者可以貼進 Gears 的網址檢查，比對 165 反詐騙諮詢專線公開的「遭停止解析涉詐網站」清單。最直接的做法是把網址送到伺服器查詢，但查詢紀錄會累積成一份「誰收到了哪些詐騙連結」的資料。

2026-10-14 查證時，清單有 86,173 個不重複的網域，整理成純文字約 1.5 MB。壓縮後約 400 KB，整份放進瀏覽器比對也不算大。Gears 在部署時下載清單，跟網站一起送到讀者的瀏覽器，網址完全不必送出。比對用完整的主機名稱，清單裡有共用平台的子網域，不能把整個平台標成詐騙。清單只收已經停止解析的網域，畫面上也寫明不在清單裡不代表安全。

短網址的展開評估過之後決定不做。由伺服器代為連線的話，任何人都能用自己的短網址取得主機的真實 IP，也可能被當成探測內部網路的跳板。詐騙簡訊又常給每個收件人不同的短網址，代為展開，在對方那邊就記成一次點擊，等於替讀者確認收到了訊息。遇到短網址時，Gears 提醒讀者請對方提供完整的網址。

## Cloudflare 的注入與壓縮

第二個錯跟 Cloudflare 有關。anoni.net 前面是 Cloudflare，它會在整個 zone 的 HTML 回應裡注入 Web Analytics 與 JS Detections 的 script。Gears 的 CSP 會擋下這些 script，但讀者取得的頁面應該跟建置出來的一樣，所以回應帶上 `Cache-Control: no-transform`，要求 Cloudflare 不改動內容。

2026-10-17 第一次部署時，`no-transform` 加在所有檔案上。帶了它的回應，Cloudflare 完全不壓縮，連 nginx 送出的 gzip 也會解開，上線後實測 1.5 MB 的 165 清單與 14 MB 的 onnxruntime WebAssembly 都以原始大小送到讀者手上。注入只發生在 HTML，所以改成只有頁面與圖片帶 `no-transform`（圖片是為了避開 Polish 重新壓縮）。其他檔案交給 Cloudflare 壓縮，WebAssembly 壓縮後約小四分之三。

Cloudflare 在邊緣解開 TLS，經過它的檔案對它來說是明文，所以 Gears 的原則寫明，上傳檔案的端點不經過 Cloudflare。遠端傳送是例外，clearnet 的入口經過 Cloudflare，因為內容在兩端之間另外加密。分享連結的 `#` 後面帶著一把金鑰，瀏覽器不會把 `#` 之後的內容送到伺服器。兩端用它導出金鑰之後，每則訊息再用 AES-256-GCM 加密，轉送服務與 Cloudflare 只經手密文。

Cloudflare 仍然看得到兩端的 IP 與連線時間，產生連結之前畫面上會寫明，經過哪些伺服器、記下什麼另外寫在[遠端傳送的伺服器說明](https://anoni.net/gears/remote-server/)。打開分享連結之後也要按「加入」才會連線。通訊軟體產生連結預覽時，可能在它的伺服器上先打開這個網址，自動加入的話，一次性的房間會被預覽用掉。

![遠端傳送產生連結之前的說明，路線是你、Cloudflare、中繼伺服器、對方，表格列出中繼伺服器與 Cloudflare 可得知 IP 位址與連線時間，無法得知檔名、內容與文字訊息](https://assets.anoni.net/www/articles/gears-local-first-3.zh-TW-1decb3b8.webp)

## 使用統計

維護者需要知道讀者打開哪些工具、有沒有處理完、在哪裡失敗。Gears 不載入 Umami 的 script，由程式直接把事件送到社群自架的 Umami，CSP 只開那一個網址。

每個事件只能帶白名單裡的欄位，值也要在清單裡，對不上就整筆不送。檔名、檔案大小、檔案內容、讀者輸入的文字、檢查的網址、信件的寄件人、雜湊值與查證的結果都不送，螢幕尺寸只取到百位數。瀏覽器開了 Do Not Track 或 Global Privacy Control 時一律不送，頁尾也可以選擇不要記錄。onion 版在建置時把整段程式拿掉，產物裡沒有送出統計的程式。

## Tor Browser 讀到的亂數

第三個錯出現在 2026-10-17 做 onion 版的時候。Tor Browser 15.0 在一般安全等級下，讀者允許之前，canvas 的 `getImageData` 與 `toBlob` 一律回傳亂數，不會報錯。HEIC 轉 JPEG、PDF 轉成圖片這類要從 canvas 讀回像素的工具，因此輸出一張看起來正常、內容卻是雜訊的圖。

現在 `src/ui/canvas-access.ts` 在讀取之前先畫四個點、讀回來比對，對不上就停下來，請讀者在網址列的 canvas 圖示允許之後再按一次，同一個分頁之後就正常。

onion 版放在 `gears.<onion>`，建置之後由 `scripts/check-site.mjs --onion` 確認產物裡沒有連到 clearnet 的 anoni.net。Tor Browser 沒有 service worker，不能離線使用。沒有 cross-origin isolation，逐字稿只能用 1 個 CPU 核心。WebRTC 也整個關掉，面對面傳送不能用。這些限制都寫在畫面上，面對面傳送的位置建議改用遠端傳送，或完全不經過伺服器的 OnionShare。

## 目前的對外連線

整理成一張表，打開瀏覽器開發者工具的網路分頁就能對照：

| 連到哪裡 | 什麼時候 | 送出什麼、誰看得到 |
|---|---|---|
| anoni.net 自己的網域 | 開啟頁面、第一次用到某個工具時 | 頁面、程式與模型檔的請求，不含讀者的檔案 |
| 社群自架的 Umami | 使用工具時，開了 Do Not Track、Global Privacy Control 或選擇不記錄時不送 | 工具代號、事件與失敗原因的代碼 |
| 社群自架的 Formbricks | 讀者在「建議與回饋」按下送出 | 讀者填寫的內容、從哪個工具過來、介面語系與版本 |
| assets.anoni.net | 讀者選了社群轉檔的逐字稿模型 | 模型檔的請求 |
| Hugging Face | 讀者選擇逐字稿的 large-v3-turbo，並按下下載 | 模型檔的請求，Hugging Face 看得到 IP、瀏覽器與下載的模型 |
| 遠端傳送的轉送服務 | 讀者產生或加入遠端傳送的連結 | 兩端之間加密過的內容，經手的 Cloudflare 看得到 IP 與時間 |
| Cloudflare Realtime 的 TURN | 遠端傳送的視訊通話 | 加密過的影音，TURN 看得到兩端的 IP |

onion 版沒有使用統計，社群轉檔的模型也改由同一個 onion 網站提供。

## 還沒做到的部分

在 clearnet 選擇從 Hugging Face 下載大模型時，Hugging Face 看得到讀者的 IP。遠端傳送的視訊通話經過 Cloudflare Realtime 的 TURN，社群自架的 coturn 已經設定好、驗證過，還在等一台 VPS。

CSP 防的是被植入的相依套件，防不了被入侵的伺服器，伺服器被入侵時，送出的頁面連同 CSP 都可以被換掉。要確認網站上執行的就是 repo 裡的原始碼，需要兩段比對。第一段是網站與 `build` 分支：網站在 GitHub Actions 公開建置，產物推到 repo 公開的 `build` 分支，讀者現在就可以拿網站上的檔案跟它比對。

第二段是 `build` 分支與原始碼，也就是可重現建置，任何人從同一個 commit 建置，都要得到逐位元組相同的檔案。這一段還沒做到，也還沒驗證過。已知的障礙是 165 清單在建置時下載，每週一自動重建一次，同一個 commit 在不同週建置出來的清單不同，service worker 的版本號也跟著不同。

Gears 還在 Beta，文中的版本、數字與檔案位置都是發文時的狀態。對實作的意見歡迎到 [anoni-net/gears](https://github.com/anoni-net/gears) 開 issue，也可以在 Gears 的「建議與回饋」留言。

## 相關閱讀

- [文件站離線閱讀與本機加密的技術設計](/articles/offline-first-docs/)：Gears 的離線使用與 age 加密沿用同一套思路
- [遠端傳送的伺服器說明](https://anoni.net/gears/remote-server/)：轉送服務經過哪些伺服器、看得到與保存什麼
- [Gears 的設計文件](https://github.com/anoni-net/gears/blob/main/AGENTS.md)：本文提到的每一項設計，在這裡有完整的規格與測試方式
