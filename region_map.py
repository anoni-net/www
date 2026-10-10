"""觀測地區地圖：亞洲的國界畫成內嵌的 SVG，觀測地區與參照地區上色。

國界資料在 data/region-map.json，由 tools/make_region_map.py 從 Natural Earth 產生，路徑已經是
畫布座標。這裡只負責上色與連結，頁面不需要 JavaScript，onion 版也不會連到外部的地圖服務。

香港、澳門、新加坡在這個比例尺小到看不見，另外畫成圓點。顏色一律用 CSS class，深色模式
跟著網站的樣式走。
"""

import json
from html import escape
from pathlib import Path

from markupsafe import Markup

_DATA = None
# 香港與澳門的中心只差 5 個像素，圓點會疊在一起，各往外推一點。圓點比實際面積大很多，
# 手機上地圖縮到一半以下，太小就點不到
NUDGE = {"hk": (7, -5), "mo": (-7, 5)}


def data(root: Path) -> dict:
    global _DATA
    if _DATA is None:
        _DATA = json.loads((root / "data" / "region-map.json").read_text())
    return _DATA


def svg(root: Path, observed: dict[str, tuple[str, str]], refs: dict[str, str],
        current: str | None, label: str) -> Markup:
    """observed 是 {代碼: (名稱, 連結)}，refs 是 {代碼: 名稱}，current 是目前這一頁的地區。"""
    d = data(root)
    w, h = d["width"], d["height"]
    parts = [f'<svg class="rmap" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">']
    # 底圖先畫，上色的地區後畫，邊界才不會被灰色蓋住
    for code, path in d["countries"].items():
        if code not in observed and code not in refs:
            parts.append(f'<path class="rm-land" d="{path}"/>')
    for code, name in refs.items():
        if code in d["countries"]:
            parts.append(f'<path class="rm-ref" d="{d["countries"][code]}"><title>{escape(name)}</title></path>')
    for code, (name, href) in observed.items():
        cls = "rm-obs rm-cur" if code == current else "rm-obs"
        if code in d["points"]:
            dx, dy = NUDGE.get(code, (0, 0))
            x, y = d["points"][code][0] + dx, d["points"][code][1] + dy
        shape = (f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="7"/>'
                 if code in d["points"] else
                 f'<path class="{cls}" d="{d["countries"][code]}"/>' if code in d["countries"] else "")
        if shape:
            parts.append(f'<a href="{escape(href)}"><title>{escape(name)}</title>{shape}</a>')
    parts.append("</svg>")
    return Markup("".join(parts))


def drawable(root: Path, code: str) -> bool:
    d = data(root)
    return code in d["countries"] or code in d["points"]


def plain_svg(root: Path, observed: list[str], current: str | None, height: int,
              colors: dict[str, str]) -> Markup:
    """給預覽卡片截圖用，顏色直接寫在圖上，不帶連結。colors 要有 land、edge、obs、cur。"""
    d = data(root)
    parts = [f'<svg viewBox="0 0 {d["width"]} {d["height"]}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    for code, path in d["countries"].items():
        if code not in observed:
            parts.append(f'<path d="{path}" fill="{colors["land"]}" stroke="{colors["edge"]}" stroke-width="0.8"/>')
    # 目前這一頁的地區最後畫，邊界才不會被旁邊的地區蓋住
    for code in sorted(observed, key=lambda c: c == current):
        fill = colors["cur"] if code == current else colors["obs"]
        if code in d["points"]:
            dx, dy = NUDGE.get(code, (0, 0))
            x, y = d["points"][code][0] + dx, d["points"][code][1] + dy
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{fill}" stroke="{colors["edge"]}" stroke-width="1.5"/>')
        elif code in d["countries"]:
            parts.append(f'<path d="{d["countries"][code]}" fill="{fill}" stroke="{colors["edge"]}" stroke-width="0.8"/>')
    parts.append("</svg>")
    return Markup("".join(parts))
