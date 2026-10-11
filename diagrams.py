"""頁面裡的示意圖，建置時畫成內嵌的 SVG 或 HTML，頁面不需要 JavaScript，onion 版也一樣。

圖上的文字在 data/diagrams.toml，三個語系各一份。顏色一律用 CSS class，深色模式跟著網站的
樣式走，CSS 在 site.css 的「示意圖」一段。

SVG 的畫布照手機的寬度設計（360 左右），桌機上用 max-width 放大，字才不會在手機上縮到看不清楚。
SVG 的文字不會自動換行，所以用 wrap() 依字數估算寬度、自己斷行。
"""

import re
from html import escape
from pathlib import Path

from markupsafe import Markup

import region_map


# 文字

def text_width(text: str, size: float) -> float:
    """估算文字的寬度。中日韓文字約一個字寬，英數約半個多字寬，夠用來斷行。"""
    return sum(size if ord(c) > 0x2E80 else size * 0.56 for c in text)


def wrap(text: str, size: float, width: float) -> list[str]:
    """依寬度斷行。英文在空白處斷，中文每個字都可以斷，標點不放在行首。"""
    tokens = re.findall(r"[A-Za-z0-9.,'&/()\-]+\s*|\s+|.", text)
    lines, line = [], ""
    for tok in tokens:
        if line and text_width((line + tok).rstrip(), size) > width and tok not in "，、。）":
            lines.append(line.rstrip())
            line = tok.lstrip()
        else:
            line += tok
    if line.strip():
        lines.append(line.rstrip())
    return lines


def balanced(text: str, size: float, width: float) -> list[str]:
    """跟 wrap() 一樣斷行，但各行的長度盡量平均，最後一行不會只剩一兩個字。"""
    lines = wrap(text, size, width)
    if len(lines) < 2:
        return lines
    target = text_width(text, size) / len(lines)
    while target < width:
        trial = wrap(text, size, target)
        if len(trial) == len(lines):
            return trial
        target += size / 2
    return lines


def _nested(svg: str, x: float, y: float, size: float, cls: str) -> str:
    """把圖示或 logo 的 SVG 放進另一張 SVG 裡的指定位置。"""
    return svg.replace("<svg ", f'<svg class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" '
                       'aria-hidden="true" ', 1)


# 社群在做的事

W = 360
NAME, ITEM = 16, 13.5        # 字級，手機上整張圖縮到八成多，小字約 11px
NAME_LH, ITEM_LH = 20, 18    # 行高
TEXT_W = 166                 # 每一格文字的寬度
R = 20                       # 圓的半徑


def community(conf: dict, topics: list[dict], pick, page_url, icon_svg, logo_svg: str) -> Markup:
    """中間是 anoni.net，四個項目排在四個角落，上排的文字在圓的上方，下排的在下方，
    連線只走中間，不會穿過文字。同一排的名稱對齊在同一條線上。"""
    by_cat = {t["cat"]: t for t in topics}
    nodes = []
    for n in conf["nodes"]:
        t = by_cat.get(n.get("topic"), {})
        nodes.append({
            "cat": n.get("topic") or n["cat"],
            "icon": n.get("icon") or t["icon"],
            "href": page_url(n.get("page") or t["page"]),
            # 名稱是粗體，估寬時多算一成
            "name": balanced(pick(n.get("name") or t["name"]), NAME * 1.1, TEXT_W),
            "items": [line for item in pick(n["items"]) for line in balanced(item, ITEM, TEXT_W)],
        })

    def block_h(n: dict) -> float:
        return len(n["name"]) * NAME_LH + 6 + len(n["items"]) * ITEM_LH

    top_h = max(block_h(n) for n in nodes[:2])
    bottom_h = max(block_h(n) for n in nodes[2:])
    y1 = 14 + top_h + 12 + R          # 上排圓心
    cy = y1 + 62                      # 中心
    y2 = cy + 62                      # 下排圓心
    height = y2 + R + 16 + bottom_h + 6
    xs = (88, W - 88)
    spots = [(xs[0], y1, "up"), (xs[1], y1, "up"), (xs[0], y2, "down"), (xs[1], y2, "down")]

    parts = [f'<svg class="dg dg-community" viewBox="0 0 {W} {height:.0f}" aria-labelledby="dg-community-t">',
             f'<title id="dg-community-t">{escape(pick(conf["label"]))}</title>']
    for n, (x, y, _) in zip(nodes, spots):
        parts.append(f'<line class="dg-link topic-{n["cat"]}" x1="{W / 2}" y1="{cy}" x2="{x}" y2="{y}"/>')
    parts.append(f'<circle class="dg-hub" cx="{W / 2}" cy="{cy}" r="34"/>')
    # logo 的六角形在 24×24 的畫布裡實際占 x 3–22.25、y 2–22，照實際範圍的中心對齊圓心
    scale = 44 / 24
    parts.append(_nested(logo_svg, W / 2 - 12.625 * scale, cy - 12 * scale, 44, "dg-logo"))
    parts.append(f'<text class="dg-hub-t" x="{W / 2}" y="{cy + 54}" text-anchor="middle">anoni.net</text>')
    for n, (x, y, side) in zip(nodes, spots):
        lines = [("dg-name", NAME_LH, s) for s in n["name"]] + [("dg-item", ITEM_LH, s) for s in n["items"]]
        if side == "up":
            ty = 14 + NAME_LH - 4
        else:
            ty = y + R + 16 + NAME_LH - 4
        text = []
        for i, (cls, lh, s) in enumerate(lines):
            if i and cls == "dg-item" and lines[i - 1][0] == "dg-name":
                ty += 6
            text.append(f'<text class="{cls}" x="{x}" y="{ty:.1f}" text-anchor="middle">{escape(s)}</text>')
            ty += lh
        parts.append(f'<a class="dg-node topic-{n["cat"]}" href="{escape(n["href"])}">'
                     f'<circle class="dg-dot" cx="{x}" cy="{y}" r="{R}"/>'
                     + _nested(icon_svg(n["icon"]), x - 11, y - 11, 22, "dg-ic") + "".join(text) + "</a>")
    parts.append("</svg>")
    return Markup(f'<figure class="dg-fig dg-fig-community">{"".join(parts)}'
                  f'<figcaption>{escape(pick(conf["note"]))}</figcaption></figure>')


# 關注地區

# 地區名稱的位置：(相對於地區中心的位移, 對齊)。香港與澳門的圓點靠得很近，名稱分在左右兩邊
LABEL_AT = {
    "tw": ((12, 6), "start"),
    "hk": ((2, -12), "middle"),
    "mo": ((-10, 14), "end"),
    "sg": ((-10, 16), "end"),
    "cn": ((0, 6), "middle"),
    "my": ((0, 6), "middle"),
}


def _bbox(path: str) -> tuple[float, float, float, float]:
    nums = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", path)]
    xs, ys = nums[0::2], nums[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def regions(root: Path, conf: dict, pick) -> Markup:
    """亞洲地圖裁到關注的地區，臺灣用實色，其他地區用淺色，地區名稱直接寫在圖上。"""
    d = region_map.data(root)
    codes = conf["first"] + conf["others"]
    boxes, anchor = [], {}
    for code in codes:
        if code in d["points"]:
            dx, dy = region_map.NUDGE.get(code, (0, 0))
            x, y = d["points"][code][0] + dx, d["points"][code][1] + dy
            boxes.append((x - 10, y - 10, x + 10, y + 10))
            anchor[code] = (x, y)
        else:
            b = _bbox(d["countries"][code])
            boxes.append(b)
            anchor[code] = ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
    pad = 16
    x0 = min(b[0] for b in boxes) - pad
    y0 = min(b[1] for b in boxes) - pad
    x1 = max(b[2] for b in boxes) + pad + 60   # 右邊留給臺灣的名稱
    y1 = max(b[3] for b in boxes) + pad
    w, h = x1 - x0, y1 - y0

    parts = [f'<svg class="rmap dg-regions" viewBox="{x0:.0f} {y0:.0f} {w:.0f} {h:.0f}" role="img" '
             f'aria-label="{escape(pick(conf["label"]))}">']
    for code, path in d["countries"].items():
        if code not in codes:
            parts.append(f'<path class="rm-land" d="{path}"/>')
    for code in conf["others"] + conf["first"]:
        cls = "rm-first" if code in conf["first"] else "rm-second"
        name = escape(pick(conf["names"][code]))
        if code in d["points"]:
            x, y = anchor[code]
            parts.append(f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="6"><title>{name}</title></circle>')
        else:
            parts.append(f'<path class="{cls}" d="{d["countries"][code]}"><title>{name}</title></path>')
    for code in codes:
        (dx, dy), align = LABEL_AT.get(code, ((0, 4), "middle"))
        x, y = anchor[code]
        cls = "dg-label dg-label-first" if code in conf["first"] else "dg-label"
        parts.append(f'<text class="{cls}" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{align}">'
                     f'{escape(pick(conf["names"][code]))}</text>')
    parts.append("</svg>")
    legend = (f'<span class="lg"><span><i class="sw rm-sw-first"></i>{escape(pick(conf["legend_first"]))}</span>'
              f'<span><i class="sw rm-sw-second"></i>{escape(pick(conf["legend_others"]))}</span></span>')
    return Markup(f'<figure class="rmap-fig dg-fig dg-fig-regions">{"".join(parts)}'
                  f'<figcaption>{legend}{escape(pick(conf["note"]))}</figcaption></figure>')


# 社群的起點

def history(conf: dict, pick, link) -> Markup:
    """時間軸用 HTML 的有序清單，左邊一條線、每一筆一個圓點，文字照常換行，讀屏軟體也讀得到順序。
    link(item) 回傳那一筆的網址。"""
    rows = []
    for item in conf["items"]:
        rows.append(f'<li class="tl-{item["kind"]}"><span class="tl-when">{escape(item["when"])}</span>'
                    f'<span class="tl-b"><a class="tl-t" href="{escape(link(item))}">{escape(pick(item["title"]))}</a>'
                    f'<span class="tl-d">{escape(pick(item["desc"]))}</span></span></li>')
    return Markup(f'<ol class="tl" aria-label="{escape(pick(conf["label"]))}">{"".join(rows)}</ol>')
