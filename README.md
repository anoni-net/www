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

籌備中，目前的首頁仍由舊的 repo 產生。第一批頁面是首頁、關於、聯絡、參與、專案、服務，活動與社群動態還在文件站，導覽列暫時連過去。

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
| `data/` | 主題、專案、服務的資料，三個語系寫在同一筆 |
| `site.toml` | 語系、導覽列、兩個輸出目標與 onion 的網址改寫 |
| `strings.toml` | 模板裡的介面文字 |
| `templates/` | 頁面模板，`_block-*.html.j2` 是可以插進 Markdown 的區塊 |
| `static/` | CSS、logo、PGP 公鑰等原樣複製的檔案 |
| `icons/` | 內嵌的 SVG 圖示，來源與授權見該目錄的 README |

Markdown 裡的連結有三種寫法，建置時依語系展開：

- `/join/`：本站的頁面，加上語系前綴，例如英文版變成 `/en/join/`
- `docs:tools/what-is-tor/`：文件站同語系的頁面
- `news:about/`：新聞導讀同語系的頁面

在 Markdown 裡單獨一行寫 `<!-- topics -->`，建置時換成 `templates/_block-topics.html.j2` 的內容，主題、專案卡片、服務卡片都用這個方式放進頁面。

onion 版本在寫檔前把 `https://anoni.net/docs` 這類 clearnet 網址改寫成 onion 位址，對照表在 `site.toml` 的 `[targets.onion.rewrite]`。`--check` 會檢查三個語系的頁面是否一致、站內連結是否找得到檔案，以及 onion 版本有沒有漏改的網址。

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
| [MIT](./LICENSE-code) | `build.py`、`site.toml`、`pyproject.toml`、`templates/`、`static/css/`、`.github/` |
| [Pictogrammers Free License](./icons/LICENSE) | `icons/`，來源見 [`icons/README.md`](./icons/README.md) |
| [CC-BY 4.0](./LICENSE) | 其餘檔案，包含 `pages/`、`data/`、`strings.toml` 這些頁面上讀得到的文字，以及 `static/` 底下的 logo、favicon 與預覽圖 |

logo 與色票跟文件站的[品牌素材](https://anoni.net/docs/community/brand-assets/)是同一套。
