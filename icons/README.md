# 圖示

頁面用到的圖示，建置時由 `build.py` 的 `icon()` 內嵌進 HTML，不透過字型或 CDN 載入，onion 版本一樣可用。只放用到的圖示，從文件站搬頁面時由 `tools/import_from_docs.py` 自動複製進來。

全部取自 mkdocs-material 9.7.7 隨附的 `templates/.icons/`，跟文件站用同一套。檔名沒有前綴的是 Material Design Icons，其他套件的圖示加上套件名稱當前綴。

| 檔名 | 來源 | 授權 |
|---|---|---|
| 沒有前綴，例如 `forum-outline.svg` | [Material Design Icons](https://pictogrammers.com/library/mdi/) | Pictogrammers Free License，全文在 [`licenses/material.txt`](./licenses/material.txt) |
| `octicons-*.svg` | [Octicons](https://primer.style/octicons/)（GitHub） | MIT，全文在 [`licenses/octicons.txt`](./licenses/octicons.txt) |
| `fontawesome-*.svg` | [Font Awesome Free](https://fontawesome.com/) | 圖示 CC BY 4.0，SVG 內保留原本的授權註解，全文在 [`licenses/fontawesome.txt`](./licenses/fontawesome.txt) |
| `simple-*.svg` | [Simple Icons](https://simpleicons.org/) | CC0 1.0，全文在 [`licenses/simple-icons.md`](./licenses/simple-icons.md) |

`simple-torproject.svg` 是 Tor Project 的商標，這裡只用來標示跟 Tor 有關的連結。

導覽列不放圖示，圖示只用在需要從幾個項目裡挑一個的地方，例如三大主題、專案與服務的卡片，以及從文件站搬過來的頁面原本就有的圖示。
