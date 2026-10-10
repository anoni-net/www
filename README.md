# anoni.net

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

## Tor 中繼節點觀測

`/projects/pulse/` 是 [Pulse](https://github.com/anoni-net/pulse) 的觀測頁，原本是文件站的「Tor Relays 觀測點」。頁面的文字在 `pages/<語系>/projects/pulse.md`，`<!-- pulse -->` 的位置放儀表板，國家清單與圖表上的文字在 `data/pulse.toml`。第一個國家是主頁，其他國家各一頁 `/projects/pulse/<代碼>/`，由同一份 Markdown 產生。

建置時 [`pulse.py`](./pulse.py) 從 Pulse 的 `/api/summary` 讀每個國家的資料，圖表畫成內嵌的 SVG，頁面不需要 JavaScript，onion 版也不會連到 clearnet。每個長條與資料點都帶 `<title>`，滑鼠停在上面會顯示數值。顏色只用 cyan 的五個深淺，CSS 在 `site.css` 的 `.pulse` 一段。

| 環境變數 | 用途 |
|---|---|
| `PULSE_API` | API 的位址，預設 `https://anoni.net/api`。m6 的部署腳本設成本機的 `http://127.0.0.1:8899/api` |

讀到的資料寫進 `.cache/pulse/`，十分鐘內的建置直接用快取，部署腳本先 `--check` 再建置，同一輪只讀一次 API。API 沒有回應時退回舊的快取，頁面標示資料是快取。連快取都沒有時頁面顯示提示，建置照樣成功，所以 GitHub 上的 CI 不受 API 影響。

在本機預覽時讀的是公開的 API，回應經過 Cloudflare 的快取，Pulse 剛改過端點時可能讀到舊的回應，清掉 `/api/summary?country=<代碼>&days=60` 的快取即可。

共用的圖表函式在 [`charts.py`](./charts.py)，下一節的 OONI 觀測涵蓋率頁也用同一套。

## OONI 觀測涵蓋率

`/projects/asn-coverage/` 對照 OONI 的測量數與各 ASN 的使用者人數，看測量涵蓋多少使用者、集中在哪些網路、哪些網路還沒有測量，原本只有文件站一篇 2023 年的分析（ASN 自治網路觀測資料分析）。頁面的文字在 `pages/<語系>/projects/asn-coverage.md`，`<!-- asn-coverage -->` 的位置放儀表板，地區清單與圖表上的文字在 `data/asn-coverage.toml`，分頁方式跟 Tor 中繼節點觀測相同。

建置時 [`asn_coverage.py`](./asn_coverage.py) 讀三個公開來源，寫進 `.cache/asn-coverage/`：

| 來源 | 內容 | 快取 |
|---|---|---|
| [OONI 彙總 API](https://api.ooni.io/) | 各 ASN 每天的測量數，分成正常、異常、確認封鎖、測量失敗 | 6 小時 |
| [APNIC 的 ASN 使用者估計](https://stats.labs.apnic.net/aspop/) | 各 ASN 的使用者人數與名稱，APNIC 每週更新 | 7 天 |
| [RIPE NCC 的 ASN 名稱表](https://ftp.ripe.net/ripe/asnames/asn.txt) | 不在 APNIC 估計裡的網路名稱，例如學術網路 | 7 天 |

部署在 m6 時每小時重建一次，OONI 每六小時才真的重讀，六個地區約 12 秒，連 APNIC 與 RIPE 一起重讀的那一輪約 25 秒。讀取失敗的處理跟 Pulse 相同，退回快取並標示。APNIC 的資料允許註明出處後再利用，頁面的「資料的計算方式」寫了來源。

需要網路類型（行動、寬頻）或封鎖方式的細節時，用 [ASN Coverage](https://github.com/anoni-net/asn-coverage) 下載原始測量分析，彙總 API 沒有這兩項。

## 觀測季報

`/projects/reports/` 每季整理一次 Tor 中繼節點與 OONI 觀測涵蓋率，兩個觀測頁顯示最近 60 天，季報把當季的數字定格下來，加上社群的解讀。每一期的本文在 `reports/<語系>/<季度>.md`（例如 `reports/zh-TW/2026-q3.md`），三個語系都要有，缺一個 `build.py --check` 就不會通過。列表頁是 `pages/<語系>/projects/reports.md`。

圖表與表格用 `<!-- rq-名稱 -->` 放進本文，名稱對應 `templates/_report.html.j2` 的 macro，整理數字的程式在 [`reports.py`](./reports.py)，圖表上的文字在 `data/reports.toml`。數字來自 `data/reports/<季度>.json`，進版控之後就是那一季定格的數字，之後重建網站也不會變。

每季產生一次數字檔，步驟寫在 [`tools/quarterly_report.py`](./tools/quarterly_report.py) 的開頭：

1. 在 m6 上對 Pulse 的資料庫執行 `tools/quarterly_pulse.sql`（唯讀），比對季初與季末的中繼名單與 ASN 分布。Pulse 的 API 目前沒有這兩項
2. 執行 `tools/quarterly_report.py <季度> --pulse-extra <上一步的輸出>`，抓 Pulse 的每日總數與版本、OONI 的彙總、APNIC 的使用者估計與 RIPE 的 ASN 名稱，合併成數字檔

APNIC 只提供最近 60 天的估計，查不到過去的值，所以每一期用的是產生數字檔當時的那一份，檔案裡記著日期。網路類型（行動、固網與有線寬頻、學術）的人工標記在 `data/reports/asn-types.toml`。

## 分類

站上的內容分成專案、服務、主題三類，判斷的依據是誰開發的。

| 分類 | 定義 | 例子 | 頁面 | 資料 |
|---|---|---|---|---|
| 專案 | 社群自己寫的內容或程式，有自己的路線圖與貢獻者 | docs、news、onionoo-mcp、Pulse、ASN Coverage | `/projects/` | `data/projects.toml` |
| 服務 | 其他開源專案開發的軟體，社群負責架設與維運 | Matrix、CryptPad、Etherpad、SearXNG、Send、Formbricks | `/services/` | `data/services.toml` |
| 主題 | 年度的工作方向，讀者可以認領、加入，不是成品 | 2026 年的個人隱私指引、Tor Relay 校園建立、匿名支付 | `/join/` | `data/topics.toml` |

兩類都說得通時，照開發者判斷。onionoo-mcp 是社群寫的程式，也架設成公開服務，歸在專案。之後新架設的開源軟體歸服務，社群新寫的工具歸專案。

本站只放專案的卡片與一句介紹，連到專案自己的關於頁，詳細介紹寫在專案的 repo。同一份介紹放兩處，改的時候容易漏掉一邊。

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
