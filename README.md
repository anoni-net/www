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

第一批頁面是首頁、關於、聯絡、參與、專案、服務，活動與社群動態還在文件站，導覽列暫時連過去。

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
| `/srv/anoni-net-www/releases/<commit>` | 每個 commit 建置一份，保留最近五份 |
| `/srv/anoni-net-www/current` | symlink，指向線上的那一份 |
| `/home/ubuntu/www-deploy.log` | 每次發布與失敗的紀錄 |

腳本先執行 `--check`，通過之後建置到新的目錄，最後才切換 `current`，建置失敗時線上維持原本的版本。nginx 的 `anoni.net` 與根 onion 位址都讀 `current`，設定在 m6 的 `/etc/nginx/conf.d/anoninet.conf`，`error_page 404` 指到根目錄的 `404.html`。

從文件站搬過來的頁面記在 [`tools/docs_moved.toml`](./tools/docs_moved.toml)，搬內容、產生舊網址的轉址對照表都讀這一份：

```bash
uv run tools/import_from_docs.py --import about/governance  # 把文件站的原始檔轉成 pages/ 底下的頁面
uv run tools/import_from_docs.py --nginx                    # 重新產生 tools/nginx-docs-moved.conf
```

轉換工具讀的是文件站 clone 的 `origin/main`，站內連結依目標改寫：搬過來的頁面改成本站網址，其他的改成 `docs:` 簡寫，部落格文章從 front matter 組出網址。轉完會拿每個 `docs:` 連結比對文件站的網址合約，找不到或只是轉址都會印警告。卡片格線這類文件站特有的版面元件要手動改寫。

舊網址在 m6 的 nginx 用 301 轉過來，clearnet 與 onion 各一份 `map`，把產生的對照表複製到 `/etc/nginx/conf.d/anoni-docs-moved.conf` 再 reload。順序是新頁面先上線，再套轉址，最後在文件站刪原始檔、補 `redirect_maps`。

要退回上一版，先建立 `/srv/anoni-net-www/hold` 暫停自動發布，再把 `current` 改指到 `releases/` 底下較舊的那一份。修好之後刪掉 `hold`，下一輪就會發布 `main` 的最新版。

## 分類

- **專案**：社群自己寫的內容或程式，有自己的路線圖與貢獻者，例如 docs、news、onionoo-mcp、Pulse、ASN Coverage
- **服務**：其他開源專案開發的軟體，社群負責架設與維運，例如 Matrix、CryptPad、Etherpad、SearXNG、Send、Formbricks
- **主題**：年度的工作方向，讀者可以認領、加入，放在「參與」底下

## 寫作規則

照[貢獻者百科](https://anoni.net/docs/community/contributor-handbook/)的寫作風格規範，本 repo 不另外寫一份。

## 授權

程式碼與頁面內容分開授權：

| 授權 | 涵蓋 |
|---|---|
| [MIT](./LICENSE-code) | `build.py`、`site.toml`、`pyproject.toml`、`templates/`、`static/css/`、`tools/`、`.github/` |
| 各圖示套件的授權 | `icons/`，來源與授權見 [`icons/README.md`](./icons/README.md) |
| [CC-BY 4.0](./LICENSE) | 其餘檔案，包含 `pages/`、`updates/`、`data/`、`strings.toml` 這些頁面上讀得到的文字，以及 `static/` 底下的 logo、favicon 與預覽圖 |

logo 與色票跟文件站的[品牌素材](https://anoni.net/docs/community/brand-assets/)是同一套。
