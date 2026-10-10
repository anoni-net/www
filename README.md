<a id="zh-tw"></a>

# anoni.net

**正體中文** | [English](#en)

`anoni.net` 首頁與社群頁面的原始碼，包含社群介紹、參與方式、專案與自架服務的目錄、活動與社群動態。由[匿名網路社群 anoni.net](https://anoni.net/) 維護。

## 跟其他 repo 的分工

社群自己寫的內容與程式稱為專案，各自一個 repo，掛在 `anoni.net` 底下的路徑。社群架設、由其他開源專案開發的軟體稱為服務，各自一個子網域。這個 repo 只放社群本身的頁面，專案與服務的詳細介紹寫在各自的 repo。

| 網址 | repo |
|---|---|
| `anoni.net/` | 本 repo |
| `anoni.net/docs/` | [`anoni-net/docs`](https://github.com/anoni-net/docs) |
| `anoni.net/news/` | [`anoni-net/news`](https://github.com/anoni-net/news) |

## 狀態

社群頁面在 2026-10 從文件站搬完，導覽列六項都是本站的頁面。文件站部落格裡 2026-10 以前的社群文章留在原址，社群動態的列表直接連過去，名單在 `tools/docs_updates.toml`。

## 建置

```bash
uv sync
uv run build.py          # 產生 public/clearnet 與 public/onion
uv run build.py --check  # 產生到暫存目錄並檢查，CI 跑同一個指令
```

不採用現成的靜態網站產生器，`build.py` 讀 Markdown 頁面與資料檔，用 Jinja 模板輸出純 HTML 與一份 CSS，不載入任何框架或外部字型。

| 位置 | 內容 |
|---|---|
| `pages/<語系>/` | 每一頁一個 Markdown 檔，三個語系的檔名要一致 |
| `updates/<語系>/` | 社群動態，一篇一個 Markdown 檔，見下方「社群動態」 |
| `data/` | 主題、專案、服務的資料，三個語系寫在同一筆 |
| `site.toml` | 語系、導覽列、兩個輸出目標與 onion 的網址改寫 |
| `strings.toml` | 模板裡的介面文字 |
| `templates/` | 頁面模板，`_block-*.html.j2` 是可以插進 Markdown 的區塊 |
| `static/` | CSS、logo、PGP 公鑰等原樣複製的檔案 |
| `extra/` | 只有部分目標需要的檔案，例如 clearnet 的 `llms.txt`，在 `site.toml` 指定 |
| `icons/` | 內嵌的 SVG 圖示，來源與授權見該目錄的 README |

Markdown 裡的連結有三種寫法，建置時依語系展開：

- `/join/`：本站的頁面，加上語系前綴，例如英文版變成 `/en/join/`
- `docs:tools/what-is-tor/`：文件站同語系的頁面
- `news:about/`：新聞導讀同語系的頁面

在 Markdown 裡單獨一行寫 `<!-- topics -->`，建置時換成 `templates/_block-topics.html.j2` 的內容，主題、專案卡片、服務卡片都用這個方式放進頁面。

onion 版本在寫檔前把 `https://anoni.net/docs` 這類 clearnet 網址改寫成 onion 位址，對照表在 `site.toml` 的 `[targets.onion.rewrite]`。`--check` 會檢查三個語系的頁面是否一致、站內連結是否找得到檔案，以及 onion 版本有沒有漏改的網址。

## 社群動態

社群公告寫在 `updates/<語系>/`，一篇一個 Markdown 檔，front matter 要有 `title`、`description` 與 `date`（`YYYY-MM-DD`），網址是 `/updates/YYYY/MM/<檔名>/`，跟文件站部落格的格式一樣。三個語系不強制都有，檔名相同的會互相連成語言切換，沒有對應版本的語系切過去會回到動態列表。

`/updates/` 的列表、首頁的「最新動態」與每個語系的 RSS（`/updates/feed.xml`），除了本站的文章，也列出文件站部落格裡舊的社群文章，點下去連到文件站原本的網址。那份名單寫在 `tools/docs_updates.toml`，執行 `uv run tools/import_from_docs.py --updates` 產生 `data/docs_updates.toml`。

翻譯、技術分析、觀測報告與文件站自己的更新回顧，照樣發在文件站的部落格。

## 部署

在 m6 上建置，不經過 GitHub Actions。m6 的 crontab 每 5 分鐘執行一次 [`tools/deploy-m6.sh`](./tools/deploy-m6.sh)（複製到 `/home/ubuntu/www-deploy.sh`），合併進 `main` 之後幾分鐘內上線。

| m6 上的位置 | 內容 |
|---|---|
| `/srv/anoni-net-www/repo` | 本 repo 的 clone，只拉 `main` |
| `/srv/anoni-net-www/releases/<commit>-<小時>` | 每個 commit 每小時建置一份，保留最近六份 |
| `/srv/anoni-net-www/current` | symlink，指向線上的那一份 |
| `/home/ubuntu/www-deploy.log` | 每次發布與失敗的紀錄 |

同一個 commit 每小時也重建一次，給 Tor 中繼節點觀測頁更新資料，見下方「Tor 中繼節點觀測」。腳本先執行 `--check`，通過之後建置到新的目錄，最後才切換 `current`，建置失敗時線上維持原本的版本。nginx 的 `anoni.net` 與根 onion 位址都讀 `current`，設定在 m6 的 `/etc/nginx/conf.d/anoninet.conf`，`error_page 404` 指到根目錄的 `404.html`。

從文件站搬過來的頁面記在 [`tools/docs_moved.toml`](./tools/docs_moved.toml)，搬內容、產生舊網址的轉址對照表都讀這一份：

```bash
uv run tools/import_from_docs.py --import about/governance  # 把文件站的原始檔轉成 pages/ 底下的頁面
uv run tools/import_from_docs.py --nginx                    # 重新產生 tools/nginx-docs-moved.conf
```

轉換工具讀的是文件站 clone 的 `origin/main`，站內連結依目標改寫：搬過來的頁面改成本站網址，其他的改成 `docs:` 簡寫，部落格文章從 front matter 組出網址。轉完會拿每個 `docs:` 連結比對文件站的網址合約，找不到或只是轉址都會印警告。卡片格線這類文件站特有的版面元件要手動改寫。

舊網址在 m6 的 nginx 用 301 轉過來，clearnet 與 onion 各一份 `map`，把產生的對照表複製到 `/etc/nginx/conf.d/anoni-docs-moved.conf` 再 reload。順序是新頁面先上線，再套轉址，最後在文件站刪原始檔、補 `redirect_maps`。

要退回上一版，先建立 `/srv/anoni-net-www/hold` 暫停自動發布，再把 `current` 改指到 `releases/` 底下較舊的那一份。修好之後刪掉 `hold`，下一輪就會發布 `main` 的最新版。

## 預覽卡片

分享到社群平台時的預覽圖（og:image），每一頁三個語系各一張，寫著區塊、頁面標題、導言與網址。兩個觀測頁與各地區的子頁加上觀測地區地圖，標出那一頁的地區。地圖只畫亞洲，德國、荷蘭、美國的子頁不放地圖。

卡片不進版控。[`tools/make_og_cards.py`](./tools/make_og_cards.py) 用 `templates/og-card.html.j2` 截圖，上傳到 assets.anoni.net 的 `www/og/`，網址寫進 `og_cards.toml`。建置時每一頁從卡片上的文字、模板與 logo 算出檔名的雜湊（規則在 [`og_cards.py`](./og_cards.py) 開頭），跟登記表一致才用，還沒產生或內容改過時用根目錄的 `og.png`，所以 m6 建置不需要瀏覽器。front matter 寫了 `og_image` 的頁面用指定的圖。

新增頁面、改了標題或導言之後，在合併前執行一次，把更新過的 `og_cards.toml` 跟內容放在同一個 PR：

```bash
uv run --with playwright tools/make_og_cards.py --dry-run  # 只產圖，.cache/og-cards/preview.html 排在一起看
WWW_OG_RSYNC=<主機>:<目錄> uv run --with playwright tools/make_og_cards.py
```

上傳目的地只放在環境變數，不寫進公開的 repo。`build.py --check` 會提示有幾頁的卡片缺少或過期，但不算失敗，GitHub 上的 CI 不能上傳圖片。改了模板，所有卡片的雜湊都會換，要整批重新產生，再到圖片主機刪掉登記表裡已經沒有的舊檔。

## Tor 中繼節點觀測

`/projects/pulse/` 是 [Pulse](https://github.com/anoni-net/pulse) 的觀測頁，原本是文件站的「Tor Relays 觀測點」。頁面的文字在 `pages/<語系>/projects/pulse.md`，`<!-- pulse -->` 的位置放儀表板，國家清單與圖表上的文字在 `data/pulse.toml`。第一個國家是主頁，其他國家各一頁 `/projects/pulse/<代碼>/`，由同一份 Markdown 產生。

建置時 [`pulse.py`](./pulse.py) 從 Pulse 的 `/api/summary` 讀每個國家的資料，圖表畫成內嵌的 SVG，頁面不需要 JavaScript，onion 版也不會連到 clearnet。每個長條與資料點都帶 `<title>`，滑鼠停在上面會顯示數值。顏色只用 cyan 的五個深淺，CSS 在 `site.css` 的 `.pulse` 一段。

| 環境變數 | 用途 |
|---|---|
| `PULSE_API` | API 的位址，預設 `https://anoni.net/api`。m6 的部署腳本設成本機的 `http://127.0.0.1:8899/api` |

讀到的資料寫進 `.cache/pulse/`，十分鐘內的建置直接用快取，部署腳本先 `--check` 再建置，同一輪只讀一次 API。API 沒有回應時退回舊的快取，頁面標示資料是快取。連快取都沒有時頁面顯示提示，建置照樣成功，所以 GitHub 上的 CI 不受 API 影響。

在本機預覽時讀的是公開的 API，回應經過 Cloudflare 的快取，Pulse 剛改過端點時可能讀到舊的回應，清掉 `/api/summary?country=<代碼>&days=60` 的快取即可。

「使用與貢獻」一段另外讀 [Tor Metrics](https://metrics.torproject.org/) 的使用者估計（[`tor_users.py`](./tor_users.py)），每個國家兩份 CSV（直接連線、透過橋接），加上全球兩份當分母，寫進 `.cache/tor-users/`。Tor Metrics 每天更新一次、晚兩三天，所以快取 12 小時，十五國重讀一輪約 30 秒。讀不到時退回快取，連快取都沒有就不畫那一段。中繼占全網路的權重來自 `/api/summary` 的 `weight`，Pulse 2026-10 起才收集，更早的日子是空的。

國家清單要跟 Pulse 的 `backend/countries.py` 一致。新增國家時先部署 Pulse，再改 `data/pulse.toml`，順序反過來的話 `/api/summary` 對新國家回 422，那幾頁會顯示資料暫時無法取得。

共用的圖表函式在 [`charts.py`](./charts.py)，下一節的 OONI 觀測涵蓋率頁也用同一套。

兩個觀測頁的頁首與社群動態文章裡的 `<!-- region-map -->` 放一張觀測地區地圖（[`region_map.py`](./region_map.py)），觀測地區用主色、參照地區用淺色，點下去開那個地區的頁面。國界資料在 `data/region-map.json`，由 `tools/make_region_map.py` 從 [Natural Earth](https://www.naturalearthdata.com/) 的 1:50m 國界（公有領域）產生，只留亞洲那一塊、簡化到一個像素，約 25 KB。國界很少變動，資料改了才需要重新執行，產出的 JSON 進版控，建置時不連網路。香港、澳門、新加坡小到看不見，畫成圓點。

季報開頭也放一張，只上色那一期數字檔的 `countries`（季報比較的地區），之後新增的地區不會回頭改舊的季報。每一期季報另有一組分享圖與電子報 banner，由 `tools/make_report_images.py <季度>` 產生並上傳到 assets.anoni.net 的 `reports/`（圖不進版控，用法寫在工具開頭），季報頁與那一期的社群動態在 front matter 用 `og_image` 寫完整網址，其他頁面用下方「預覽卡片」自動產生的卡片。

## OONI 觀測涵蓋率

`/projects/asn-coverage/` 對照 OONI 的測量數與各 ASN 的使用者人數，看測量涵蓋多少使用者、集中在哪些網路、哪些網路還沒有測量，原本只有文件站一篇 2023 年的分析（ASN 自治網路觀測資料分析）。頁面的文字在 `pages/<語系>/projects/asn-coverage.md`，`<!-- asn-coverage -->` 的位置放儀表板，地區清單與圖表上的文字在 `data/asn-coverage.toml`，分頁方式跟 Tor 中繼節點觀測相同。

建置時 [`asn_coverage.py`](./asn_coverage.py) 讀三個公開來源，寫進 `.cache/asn-coverage/`：

| 來源 | 內容 | 快取 |
|---|---|---|
| [OONI 彙總 API](https://api.ooni.io/) | 各 ASN 每天的測量數，分成正常、異常、確認封鎖、測量失敗 | 6 小時 |
| [APNIC 的 ASN 使用者估計](https://stats.labs.apnic.net/aspop/) | 各 ASN 的使用者人數與名稱，APNIC 每週更新 | 7 天 |
| [RIPE NCC 的 ASN 名稱表](https://ftp.ripe.net/ripe/asnames/asn.txt) | 不在 APNIC 估計裡的網路名稱，例如學術網路 | 7 天 |
| OONI 彙總 API，`axis_x=probe_cc` | Signal、WhatsApp、Telegram 測試在各國最近 30 天的結果，一個 App 一次查完所有國家 | 6 小時 |

部署在 m6 時每小時重建一次，OONI 每六小時才真的重讀，十二個地區約 25 秒（本機實測），APNIC 與 RIPE 每週重讀一次。讀取失敗的處理跟 Pulse 相同，退回快取並標示。APNIC 的資料允許註明出處後再利用，頁面的「資料的計算方式」寫了來源。

穩定涵蓋率只算最近 30 天裡至少 15 天有測量的網路，跟「有一筆就算」的涵蓋率並排，看使用者有多少在只有零星測量的網路上，門檻是 `asn_coverage.py` 的 `STABLE_DAYS`。通訊 App 的比較表除了有頁面的地區，另外列 `data/asn-coverage.toml` 的 `[[apps.regions]]`，那些地區有封鎖紀錄，可以拿來對照。Messenger 的測試在沒有封鎖紀錄的地區也常有一成以上的異常，所以不列。

需要網路類型（行動、寬頻）或封鎖方式的細節時，用 [ASN Coverage](https://github.com/anoni-net/asn-coverage) 下載原始測量分析，彙總 API 沒有這兩項。

## 觀測季報

`/projects/reports/` 每季整理一次 Tor 中繼節點與 OONI 觀測涵蓋率，兩個觀測頁顯示最近 60 天，季報把當季的數字定格下來，加上社群的解讀。每一期的本文在 `reports/<語系>/<季度>.md`（例如 `reports/zh-TW/2026-q3.md`），三個語系都要有，缺一個 `build.py --check` 就不會通過。列表頁是 `pages/<語系>/projects/reports.md`。

圖表與表格用 `<!-- rq-名稱 -->` 放進本文，名稱對應 `templates/_report.html.j2` 的 macro，整理數字的程式在 [`reports.py`](./reports.py)，圖表上的文字在 `data/reports.toml`。數字來自 `data/reports/<季度>.json`，進版控之後就是那一季定格的數字，之後重建網站也不會變。

每季產生一次數字檔，步驟寫在 [`tools/quarterly_report.py`](./tools/quarterly_report.py) 的開頭：

1. 在 m6 上對 Pulse 的資料庫執行 `tools/quarterly_pulse.sql`（唯讀），比對季初與季末的中繼名單與 ASN 分布。Pulse 的 API 目前沒有這兩項
2. 執行 `tools/quarterly_report.py <季度> --pulse-extra <上一步的輸出>`，抓 Pulse 的每日總數與版本、OONI 的彙總、APNIC 的使用者估計與 RIPE 的 ASN 名稱，合併成數字檔

APNIC 只提供最近 60 天的估計，查不到過去的值，所以每一期用的是產生數字檔當時的那一份，檔案裡記著日期。網路類型（行動、固網與有線寬頻、學術）的人工標記在 `data/reports/asn-types.toml`。

電子報的版本用 [`tools/report_email.py`](./tools/report_email.py) 產生，從同一份數字檔輸出幾張圖表的 HTML 與純文字，貼進 mail-mass 的信件模板。信件程式大多不顯示 SVG，遠端圖片又會回傳開信紀錄，所以信裡的圖表用表格與底色畫（`templates/_report_email.html.j2`），純文字版用 `█` 字元畫長條。

## 分類

站上的內容分成專案、服務、主題三類，判斷的依據是誰開發的。

| 分類 | 定義 | 例子 | 頁面 | 資料 |
|---|---|---|---|---|
| 專案 | 社群自己寫的內容或程式，有自己的路線圖與貢獻者 | docs、news、onionoo-mcp、Pulse、ASN Coverage | `/projects/` | `data/projects.toml` |
| 服務 | 其他開源專案開發的軟體，社群負責架設與維運 | Matrix、CryptPad、Etherpad、SearXNG、Send、Formbricks | `/services/` | `data/services.toml` |
| 主題 | 年度的工作方向，讀者可以認領、加入，不是成品 | 2026 年的個人隱私指引、Tor Relay 校園建立、匿名支付 | `/join/` | `data/topics.toml` |

兩類都說得通時，照開發者判斷。onionoo-mcp 是社群寫的程式，也架設成公開服務，歸在專案。之後新架設的開源軟體歸服務，社群新寫的工具歸專案。

本站只放專案的卡片與一句介紹，連到專案自己的關於頁，詳細介紹寫在專案的 repo。同一份介紹放兩處，改的時候容易漏掉一邊。

### 名稱與代號

三個觀測工具對讀者用正式名稱，跟頁面標題、專案列表一致。代號是 repo、API 與程式裡的名字，只在提到程式本身時使用，第一次出現寫成「正式名稱（代號）」。文件站、本站、各 repo 的 README 與 GitHub 說明都照這張表。

| 代號 | repo | 正體 | 簡體 | 英文 | 頁面 |
|---|---|---|---|---|---|
| Pulse | `anoni-net/pulse` | Tor 中繼節點觀測 | Tor 中继节点观测 | Tor Relay Watch | `/projects/pulse/` |
| ASN Coverage | `anoni-net/asn-coverage` | OONI 觀測涵蓋率 | OONI 观测覆盖率 | OONI Coverage | `/projects/asn-coverage/` |
| onionoo MCP | `anoni-net/onionoo-fastapi` | AI 助理的 Tor 節點查詢 | AI 助手的 Tor 节点查询 | Tor relay lookup for AI assistants | `/projects/onionoo-mcp/` |

舊的名稱「Tor Relays 觀測點」、「Tor relay watcher」、「ASN 涵蓋分析工具」不再使用。部落格文章的標題與內文保留發布當時的寫法，只有指到觀測頁的連結文字改成正式名稱。

## 寫作規則

[寫作風格規範](https://anoni.net/join/writing-style/)是本站的一頁，原始檔在 `pages/<語系>/join/writing-style.md`。社群首頁、文件站、新聞導讀與各 repo 的說明文件共用這一份。可以機器判斷的規則寫在 `anoni-net/docs` 的 `tools/docs_style_lint.py`，改規則時兩邊一起改。

## 授權

程式碼與頁面內容分開授權：

| 授權 | 涵蓋 |
|---|---|
| [MIT](./LICENSE-code) | `build.py`、`site.toml`、`pyproject.toml`、`templates/`、`static/css/`、`tools/`、`.github/` |
| 各圖示套件的授權 | `icons/`，來源與授權見 [`icons/README.md`](./icons/README.md) |
| [CC-BY 4.0](./LICENSE) | 其餘檔案，包含 `pages/`、`updates/`、`data/`、`strings.toml` 這些頁面上讀得到的文字，以及 `static/` 底下的 logo、favicon 與預覽圖 |

logo、wordmark 與色票的使用方式寫在本站的[品牌素材](https://anoni.net/brand/)（`pages/<語系>/brand.md`），下載用的 SVG 放在 `static/brand/`。文件站的 header 與 favicon 用的是同一批檔案，要換 logo 時兩邊一起換。

---

<a id="en"></a>

# anoni.net

[正體中文](#zh-tw) | **English**

Source for the `anoni.net` home page and community pages: who we are, how to take part, the directory of projects and self-hosted services, events and community updates. It is maintained by [anoni.net](https://anoni.net/), a community based in Taiwan.

## Division of work with the other repositories

Content and code written by the community are called projects. Each has its own repository and is served from a path under `anoni.net`. Software developed by other open-source projects and run by the community is called a service, and each service has its own subdomain. This repository holds only the community's own pages; projects and services are described in detail in their own repositories.

| URL | Repository |
|---|---|
| `anoni.net/` | This repository |
| `anoni.net/docs/` | [`anoni-net/docs`](https://github.com/anoni-net/docs) |
| `anoni.net/news/` | [`anoni-net/news`](https://github.com/anoni-net/news) |

## Status

The community pages finished moving over from the docs site in 2026-10, and all six items in the navigation bar now point to pages on this site. Community posts published on the docs site's blog before 2026-10 stay at their original addresses, and the community updates list links straight to them; the list of those posts is in `tools/docs_updates.toml`.

## Building

```bash
uv sync
uv run build.py          # writes public/clearnet and public/onion
uv run build.py --check  # builds into a temporary directory and checks it; CI runs the same command
```

We do not use an off-the-shelf static site generator. `build.py` reads the Markdown pages and data files and renders plain HTML and a single CSS file through Jinja templates, without loading any framework or external fonts.

| Location | Contents |
|---|---|
| `pages/<locale>/` | One Markdown file per page; file names must match across the three locales |
| `updates/<locale>/` | Community updates, one Markdown file per post (see "Community updates" below) |
| `data/` | Topics, projects and services, with all three locales in the same entry |
| `site.toml` | Locales, the navigation bar, the two output targets and the onion URL rewrites |
| `strings.toml` | Interface text used in the templates |
| `templates/` | Page templates; `_block-*.html.j2` are blocks that can be placed inside Markdown |
| `static/` | Files copied as they are, such as the CSS, the logo and the PGP public key |
| `extra/` | Files only some targets need, such as `llms.txt` for clearnet, listed in `site.toml` |
| `icons/` | Inline SVG icons; their sources and licenses are in that directory's README |

Links in Markdown come in three forms, expanded for each locale at build time:

- `/join/`: a page on this site, given the locale prefix, so the English version becomes `/en/join/`
- `docs:tools/what-is-tor/`: a page on the docs site in the same locale
- `news:about/`: a page on News in the same locale

A line in Markdown containing only `<!-- topics -->` is replaced at build time with the contents of `templates/_block-topics.html.j2`. Topics, project cards and service cards are all placed on pages this way.

Before writing files, the onion build rewrites clearnet URLs such as `https://anoni.net/docs` to their onion addresses, using the table in `[targets.onion.rewrite]` in `site.toml`. `--check` verifies that the three locales have matching pages, that internal links resolve to files, and that no clearnet URL was missed in the onion build.

## Community updates

Community announcements go in `updates/<locale>/`, one Markdown file per post. The front matter needs `title`, `description` and `date` (`YYYY-MM-DD`), and the URL is `/updates/YYYY/MM/<file name>/`, the same format as the docs site's blog. A post does not need all three locales. Files with the same name are linked to each other by the language switcher, and switching to a locale without that post leads back to the updates list.

The `/updates/` list, the "latest updates" section on the home page and each locale's RSS feed (`/updates/feed.xml`) include older community posts from the docs site's blog alongside this site's own, linking to their original addresses on the docs site. That list is kept in `tools/docs_updates.toml`; run `uv run tools/import_from_docs.py --updates` to generate `data/docs_updates.toml` from it.

Translations, technical analyses, measurement reports and the docs site's own update reviews are still published on the docs site's blog.

## Deployment

The site is built on m6, not through GitHub Actions. m6's crontab runs [`tools/deploy-m6.sh`](./tools/deploy-m6.sh) (copied to `/home/ubuntu/www-deploy.sh`) every 5 minutes, so a merge into `main` goes live within a few minutes.

| Location on m6 | Contents |
|---|---|
| `/srv/anoni-net-www/repo` | A clone of this repository that only pulls `main` |
| `/srv/anoni-net-www/releases/<commit>-<hour>` | One build per commit per hour; the six most recent are kept |
| `/srv/anoni-net-www/current` | A symlink to the live build |
| `/home/ubuntu/www-deploy.log` | A record of every release and failure |

The same commit is also rebuilt every hour so the Tor Relay Watch pages get fresh data (see "Tor Relay Watch" below). The script runs `--check` first, builds into a new directory if it passes, and only then switches `current`, so a failed build leaves the live site on the previous version. nginx serves both `anoni.net` and the root onion address from `current`, configured in `/etc/nginx/conf.d/anoninet.conf` on m6, with `error_page 404` pointing to `404.html` at the root.

Pages moved over from the docs site are recorded in [`tools/docs_moved.toml`](./tools/docs_moved.toml), which both the import and the redirect table for old URLs are generated from:

```bash
uv run tools/import_from_docs.py --import about/governance  # convert a docs source file into a page under pages/
uv run tools/import_from_docs.py --nginx                    # regenerate tools/nginx-docs-moved.conf
```

The converter reads `origin/main` of a docs clone and rewrites internal links by destination: moved pages become URLs on this site, everything else becomes the `docs:` shorthand, and blog post URLs are built from their front matter. Afterwards it checks every `docs:` link against the docs site's URL contract and prints a warning for any link that is missing or only redirects. Layout components specific to the docs site, such as card grids, have to be rewritten by hand.

Old URLs are redirected with a 301 by nginx on m6, with one `map` for clearnet and one for onion. Copy the generated table to `/etc/nginx/conf.d/anoni-docs-moved.conf` and reload. The order is: the new pages go live first, then the redirects are applied, and finally the source files are deleted from the docs site and its `redirect_maps` are updated.

To roll back, first create `/srv/anoni-net-www/hold` to pause automatic releases, then point `current` at an older build under `releases/`. Once the problem is fixed, delete `hold` and the next run releases the latest `main`.

## Preview cards

The preview image shown when a page is shared on social media (og:image) is one card per page per locale, carrying the section, the page title, its lead and the URL. The two dashboards and their regional subpages add the map of observed regions with that page's region highlighted. The map covers Asia only, so the subpages for Germany, the Netherlands and the United States leave it out.

The cards are not committed. [`tools/make_og_cards.py`](./tools/make_og_cards.py) screenshots `templates/og-card.html.j2`, uploads the cards to `www/og/` on assets.anoni.net and records their URLs in `og_cards.toml`. At build time each page computes the hash in its card's file name from the text on the card, the template and the logo (the rules are at the top of [`og_cards.py`](./og_cards.py)), and uses the card only when the registry matches. Pages whose card is missing or out of date use `og.png` at the root, so building on m6 needs no browser. Pages that set `og_image` in their front matter use that image.

After adding a page or changing a title or lead, run the tool before merging and include the updated `og_cards.toml` in the same PR:

```bash
uv run --with playwright tools/make_og_cards.py --dry-run  # images only; .cache/og-cards/preview.html shows them side by side
WWW_OG_RSYNC=<host>:<directory> uv run --with playwright tools/make_og_cards.py
```

The upload destination lives only in the environment variable and is never written into the public repository. `build.py --check` reports how many pages have a missing or outdated card without failing, since CI on GitHub cannot upload images. Changing the template changes every card's hash, so regenerate them all, then delete the old files on the image host that the registry no longer lists.

## Tor Relay Watch

`/projects/pulse/` is the dashboard for [Pulse](https://github.com/anoni-net/pulse), which used to be the docs site's "Tor Relays 觀測點". The page text is in `pages/<locale>/projects/pulse.md`, the dashboard goes where `<!-- pulse -->` is, and the country list and chart labels are in `data/pulse.toml`. The first country is the main page, and every other country gets its own page, `/projects/pulse/<code>/`, generated from the same Markdown.

At build time [`pulse.py`](./pulse.py) reads each country's data from Pulse's `/api/summary` and draws the charts as inline SVG, so the page needs no JavaScript and the onion build never reaches out to clearnet. Every bar and data point carries a `<title>`, so hovering shows its value. The colours are limited to five shades of cyan, and the CSS is the `.pulse` section of `site.css`.

| Environment variable | Purpose |
|---|---|
| `PULSE_API` | The API address, `https://anoni.net/api` by default. The deploy script on m6 sets it to the local `http://127.0.0.1:8899/api` |

Responses are written to `.cache/pulse/`, and builds within ten minutes reuse the cache. The deploy script runs `--check` before building, so each run reads the API only once. When the API does not respond, the build falls back to the old cache and the page says the data is cached. With no cache at all the page shows a notice and the build still succeeds, so CI on GitHub does not depend on the API.

A local preview reads the public API, whose responses go through Cloudflare's cache, so right after Pulse changes an endpoint you may get a stale response. Purging the cache for `/api/summary?country=<code>&days=60` fixes it.

The "Use and contribution" section also reads the user estimates from [Tor Metrics](https://metrics.torproject.org/) ([`tor_users.py`](./tor_users.py)): two CSVs per country (direct connections and via bridges), plus the two global ones as the denominator, written to `.cache/tor-users/`. Tor Metrics updates once a day and runs two or three days behind, so the cache lasts 12 hours, and rereading all fifteen countries takes about 30 seconds. If the data cannot be read the build falls back to the cache, and with no cache that section is left out. Relays' share of the network's weight comes from `weight` in `/api/summary`. Pulse started collecting it in 2026-10, so earlier days are empty.

The country list must match Pulse's `backend/countries.py`. To add a country, deploy Pulse first and then edit `data/pulse.toml`. In the other order `/api/summary` returns 422 for the new country, and those pages say the data is temporarily unavailable.

The shared chart functions are in [`charts.py`](./charts.py), which the OONI Coverage pages in the next section use as well.

The header of both dashboards, and `<!-- region-map -->` in a community update, show a map of the regions we observe ([`region_map.py`](./region_map.py)). Observed regions use the main colour and reference regions a lighter one, and clicking a region opens its page. The borders are in `data/region-map.json`, generated by `tools/make_region_map.py` from the 1:50m country borders of [Natural Earth](https://www.naturalearthdata.com/) (public domain), cropped to Asia and simplified to one pixel, about 25 KB. Borders rarely change, so the tool only needs rerunning when the source data does. The generated JSON is committed, and the build does not go online for it. Hong Kong, Macao and Singapore are too small to see, so they are drawn as dots.

Each quarterly report opens with the same map, colouring only the `countries` in that quarter's numbers file (the regions the report compares), so regions added later do not change old reports. Each quarter also has a set of preview images and an email banner, generated by `tools/make_report_images.py <quarter>` and uploaded to `reports/` on assets.anoni.net (the images are not committed; usage is at the top of the tool). The report pages and that quarter's community update set `og_image` to the full URL in their front matter, and every other page uses the generated card described in "Preview cards" below.

## OONI Coverage

`/projects/asn-coverage/` compares OONI's measurement counts with the number of users on each ASN, to show how many users the measurements cover, which networks they concentrate on and which networks have none. Before it, the docs site only had one analysis from 2023 (ASN 自治網路觀測資料分析). The page text is in `pages/<locale>/projects/asn-coverage.md`, the dashboard goes where `<!-- asn-coverage -->` is, and the region list and chart labels are in `data/asn-coverage.toml`. Pages are split per region the same way as Tor Relay Watch.

At build time [`asn_coverage.py`](./asn_coverage.py) reads three public sources and writes them to `.cache/asn-coverage/`:

| Source | Contents | Cache |
|---|---|---|
| [OONI aggregation API](https://api.ooni.io/) | Daily measurement counts per ASN, split into OK, anomaly, confirmed blocking and failure | 6 hours |
| [APNIC's ASN user estimates](https://stats.labs.apnic.net/aspop/) | User counts and names per ASN, updated weekly by APNIC | 7 days |
| [RIPE NCC's ASN name list](https://ftp.ripe.net/ripe/asnames/asn.txt) | Names of networks missing from APNIC's estimates, such as academic networks | 7 days |
| OONI aggregation API, `axis_x=probe_cc` | Results of the Signal, WhatsApp and Telegram tests in each country over the last 30 days, one query per app for all countries | 6 hours |

Deployed on m6, the site rebuilds every hour, but OONI is only reread every six hours, about 25 seconds for twelve regions (measured locally), and APNIC and RIPE once a week. Read failures are handled the same way as Pulse: fall back to the cache and say so on the page. APNIC's data may be reused with attribution, and the "How the numbers are calculated" section of the page names the sources.

Steady coverage counts only networks measured on at least 15 of the last 30 days, shown next to the coverage that counts a network after a single measurement, to show how many users sit on networks with only scattered measurements. The threshold is `STABLE_DAYS` in `asn_coverage.py`. Besides the regions with pages, the messaging app table lists the `[[apps.regions]]` in `data/asn-coverage.toml`, regions with a record of blocking, for comparison. Messenger's test often shows more than one in ten anomalies even in regions with no record of blocking, so it is left out.

For network types (mobile, broadband) or details of how blocking works, download the raw measurement analysis with [ASN Coverage](https://github.com/anoni-net/asn-coverage). The aggregation API has neither.

## Quarterly reports

`/projects/reports/` looks at Tor relays and OONI coverage once a quarter. The two dashboards show the last 60 days, and a report fixes that quarter's numbers and adds the community's reading of them. Each report's text is in `reports/<locale>/<quarter>.md` (for example `reports/zh-TW/2026-q3.md`). All three locales are required, and `build.py --check` fails if one is missing. The list page is `pages/<locale>/projects/reports.md`.

Charts and tables go into the text with `<!-- rq-name -->`, where the name matches a macro in `templates/_report.html.j2`. The code that prepares the numbers is in [`reports.py`](./reports.py), and the chart labels are in `data/reports.toml`. The numbers come from `data/reports/<quarter>.json`. Once committed, that file holds the quarter's fixed numbers, and rebuilding the site later does not change them.

The numbers file is generated once a quarter, with the steps at the top of [`tools/quarterly_report.py`](./tools/quarterly_report.py):

1. On m6, run `tools/quarterly_pulse.sql` (read-only) against Pulse's database to compare the relay list and ASN distribution at the start and end of the quarter. Pulse's API does not offer either yet
2. Run `tools/quarterly_report.py <quarter> --pulse-extra <output of the previous step>` to fetch Pulse's daily totals and versions, OONI's aggregates, APNIC's user estimates and RIPE's ASN names, and merge them into the numbers file

APNIC only provides estimates for the last 60 days and past values cannot be looked up, so each report uses the estimates available when its numbers file was generated, with the date recorded in the file. Network types (mobile, fixed and cable broadband, academic) are labelled by hand in `data/reports/asn-types.toml`.

The email version is generated by [`tools/report_email.py`](./tools/report_email.py), which turns the same numbers file into HTML and plain text for a few of the charts, to paste into a mail-mass template. Most email clients do not display SVG, and remote images report back when a message is opened, so the charts in the email are drawn with tables and background colours (`templates/_report_email.html.j2`), and the plain-text version draws bars with `█` characters.

## Categories

Content on the site falls into three categories, projects, services and topics, decided by who develops it.

| Category | Definition | Examples | Page | Data |
|---|---|---|---|---|
| Project | Content or code written by the community, with its own roadmap and contributors | docs, news, onionoo-mcp, Pulse, ASN Coverage | `/projects/` | `data/projects.toml` |
| Service | Software developed by other open-source projects, set up and run by the community | Matrix, CryptPad, Etherpad, SearXNG, Send, Formbricks | `/services/` | `data/services.toml` |
| Topic | A direction for the year's work that readers can take up and join, rather than a finished product | Personal privacy guides for 2026, building Tor relays on campuses, anonymous payments | `/join/` | `data/topics.toml` |

When something could fit two categories, decide by who develops it. onionoo-mcp is code written by the community that also runs as a public service, so it is a project. Open-source software we set up in future is a service, and new tools the community writes are projects.

This site carries only a card and a one-line description for each project, linking to the project's own about page, and the full description lives in the project's repository. Keeping the same description in two places makes it easy to update one and miss the other.

### Names and code names

Readers see the three measurement tools under their official names, which match the page titles and the project list. Code names are the names used in repositories, APIs and code, and are only used when talking about the code itself. The first mention reads "official name (code name)". The docs site, this site, each repository's README and the GitHub descriptions all follow this table.

| Code name | Repository | Traditional Chinese | Simplified Chinese | English | Page |
|---|---|---|---|---|---|
| Pulse | `anoni-net/pulse` | Tor 中繼節點觀測 | Tor 中继节点观测 | Tor Relay Watch | `/projects/pulse/` |
| ASN Coverage | `anoni-net/asn-coverage` | OONI 觀測涵蓋率 | OONI 观测覆盖率 | OONI Coverage | `/projects/asn-coverage/` |
| onionoo MCP | `anoni-net/onionoo-fastapi` | AI 助理的 Tor 節點查詢 | AI 助手的 Tor 节点查询 | Tor relay lookup for AI assistants | `/projects/onionoo-mcp/` |

The old names "Tor Relays 觀測點", "Tor relay watcher" and "ASN 涵蓋分析工具" are no longer used. Blog post titles and text keep the wording from when they were published; only the text of links pointing to the dashboards changes to the official names.

## Writing style

The [writing style guide](https://anoni.net/en/join/writing-style/) is a page on this site, with its source in `pages/<locale>/join/writing-style.md`. The community site, the docs site, News and every repository's documentation share it. The rules that can be checked mechanically live in `tools/docs_style_lint.py` in `anoni-net/docs`; when a rule changes, update both.

## License

Code and page content are licensed separately:

| License | Covers |
|---|---|
| [MIT](./LICENSE-code) | `build.py`, `site.toml`, `pyproject.toml`, `templates/`, `static/css/`, `tools/`, `.github/` |
| The license of each icon set | `icons/`; sources and licenses are in [`icons/README.md`](./icons/README.md) |
| [CC-BY 4.0](./LICENSE) | Everything else, including the text readers see on the pages (`pages/`, `updates/`, `data/`, `strings.toml`) and the logo, favicon and preview images under `static/` |

How to use the logo, wordmark and colour palette is described on the site's [brand assets](https://anoni.net/en/brand/) page (`pages/<locale>/brand.md`), and the SVGs for download are in `static/brand/`. The docs site's header and favicon use the same files, so a logo change has to be made in both places.
