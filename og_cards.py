"""每一頁的社群預覽卡片（og:image）。

卡片由 tools/make_og_cards.py 用 templates/og-card.html.j2 截圖產生，上傳到 assets.anoni.net 的 www/og/，
路徑登記在 og_cards.toml。圖不進版控，repo 裡只有登記表。

建置時每一頁算出自己的卡片路徑，檔名帶雜湊，來源是卡片上的每一個字、模板與 logo（有地圖的再加國界
資料），內容改了檔名就換。登記表裡的路徑跟算出來的一樣才用，還沒產生或內容改過時用根目錄的 og.png，
等下一次執行工具補上。front matter 寫了 og_image 的頁面（季報與那一期的社群動態）用指定的圖。
"""

import hashlib
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "og_cards.toml"
TEMPLATE = ROOT / "templates" / "og-card.html.j2"
ASSETS = "https://assets.anoni.net/www/"
DIR = "og"


def _inputs(with_map: bool) -> bytes:
    files = [TEMPLATE, ROOT / "static" / "logo-tonal.svg"]
    if with_map:
        files.append(ROOT / "data" / "region-map.json")
    return b"".join(f.read_bytes() for f in files)


def card(lang_code: str, path: str, data: dict) -> tuple[str, str, dict]:
    """(登記表的鍵, 圖片在 www/ 底下的路徑, 填進模板的資料)。鍵是頁面的路徑，三個語系各自一筆。"""
    key = path
    stem = path.strip("/")
    # 語系前綴已經在路徑裡，正體中文沒有前綴，檔名補上語系，三個語系的檔名才分得開
    if not any(stem == p or stem.startswith(f"{p}/") for p in ("en", "zh-cn")):
        stem = f"zh-tw/{stem}" if stem else "zh-tw"
    stem = stem.replace("/", "-")
    digest = hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")
                            + _inputs(bool(data.get("map")))).hexdigest()[:8]
    return key, f"{DIR}/{stem}-{digest}.png", data


def load(path: Path = REGISTRY) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("rb") as handle:
        return tomllib.load(handle).get("cards", {})


def url(entry: tuple[str, str, dict], registry: dict[str, str]) -> str | None:
    """上傳好而且跟目前內容相符的卡片網址，沒有時回傳 None。"""
    key, rel, _ = entry
    return ASSETS + rel if registry.get(key) == rel else None


def write(registry: dict[str, str], path: Path = REGISTRY) -> None:
    lines = ["# 每一頁的社群預覽卡片，由 tools/make_og_cards.py 寫入，不要手改。說明在 og_cards.py 開頭。",
             f"# 鍵是頁面的路徑，值是卡片在 {ASSETS} 底下的路徑。",
             "", "[cards]"]
    lines += [f'"{key}" = "{registry[key]}"' for key in sorted(registry)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
