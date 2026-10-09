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
| `/srv/anoni-net-www/releases/<commit>` | One build per commit; the five most recent are kept |
| `/srv/anoni-net-www/current` | A symlink to the live build |
| `/home/ubuntu/www-deploy.log` | A record of every release and failure |

The script runs `--check` first, builds into a new directory if it passes, and only then switches `current`, so a failed build leaves the live site on the previous version. nginx serves both `anoni.net` and the root onion address from `current`, configured in `/etc/nginx/conf.d/anoninet.conf` on m6, with `error_page 404` pointing to `404.html` at the root.

Pages moved over from the docs site are recorded in [`tools/docs_moved.toml`](./tools/docs_moved.toml), which both the import and the redirect table for old URLs are generated from:

```bash
uv run tools/import_from_docs.py --import about/governance  # convert a docs source file into a page under pages/
uv run tools/import_from_docs.py --nginx                    # regenerate tools/nginx-docs-moved.conf
```

The converter reads `origin/main` of a docs clone and rewrites internal links by destination: moved pages become URLs on this site, everything else becomes the `docs:` shorthand, and blog post URLs are built from their front matter. Afterwards it checks every `docs:` link against the docs site's URL contract and prints a warning for any link that is missing or only redirects. Layout components specific to the docs site, such as card grids, have to be rewritten by hand.

Old URLs are redirected with a 301 by nginx on m6, with one `map` for clearnet and one for onion. Copy the generated table to `/etc/nginx/conf.d/anoni-docs-moved.conf` and reload. The order is: the new pages go live first, then the redirects are applied, and finally the source files are deleted from the docs site and its `redirect_maps` are updated.

To roll back, first create `/srv/anoni-net-www/hold` to pause automatic releases, then point `current` at an older build under `releases/`. Once the problem is fixed, delete `hold` and the next run releases the latest `main`.

## Categories

Content on the site falls into three categories, projects, services and topics, decided by who develops it.

| Category | Definition | Examples | Page | Data |
|---|---|---|---|---|
| Project | Content or code written by the community, with its own roadmap and contributors | docs, news, onionoo-mcp, Pulse, ASN Coverage | `/projects/` | `data/projects.toml` |
| Service | Software developed by other open-source projects, set up and run by the community | Matrix, CryptPad, Etherpad, SearXNG, Send, Formbricks | `/services/` | `data/services.toml` |
| Topic | A direction for the year's work that readers can take up and join, rather than a finished product | Personal privacy guides for 2026, building Tor relays on campuses, anonymous payments | `/join/` | `data/topics.toml` |

When something could fit two categories, decide by who develops it. onionoo-mcp is code written by the community that also runs as a public service, so it is a project. Open-source software we set up in future is a service, and new tools the community writes are projects.

This site carries only a card and a one-line description for each project, linking to the project's own about page, and the full description lives in the project's repository. Keeping the same description in two places makes it easy to update one and miss the other.

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
