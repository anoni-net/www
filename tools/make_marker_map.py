"""產生文章與電子報用的標記地圖：任選經緯度範圍，把幾個國家塗成主色或另一種色調，再放上編號圓點。

每張地圖一個設定檔，放在 tools/maps/<名稱>.toml，寫範圍、要上色的國家（ISO 3166 兩碼小寫）與
編號的位置。地圖只放編號，地名與說明寫在文章的圖說，一張圖三個語系共用。

國界資料與 tools/make_region_map.py 相同，用 Natural Earth 1:50m（公有領域），投影、裁切與簡化
的做法也一樣。SVG 的顏色寫在檔內的 <style>，用 prefers-color-scheme 切換深色模式，文章直接用
<img> 引用。電子報不能用 SVG，加 --png 另外截成淺色與深色兩張 PNG（兩倍解析度）。

圖不進版控。檔名帶內容的雜湊，重新產生之後網址跟著換，不會讀到 Cloudflare 上的舊圖。目的地只放在
環境變數，不寫進公開的 repo：

    uv run tools/make_marker_map.py tools/maps/geedge-leak-one-year.toml
    uv run --with playwright tools/make_marker_map.py tools/maps/geedge-leak-one-year.toml --png
    WWW_MAP_RSYNC=<主機>:<目錄> uv run --with playwright tools/make_marker_map.py <設定檔> --png

沒有設 WWW_MAP_RSYNC 時只產生到 --out（預設是暫存目錄）、印出路徑，不上傳。下載 Natural Earth
很慢，重複執行時可以用 --geojson 指到先前下載的檔案。
"""

import argparse
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_region_map import SOURCE, TOLERANCE, simplify  # noqa: E402

# 淺色與深色的配色，照 static/css/site.css 的品牌色
CSS = """
.land{fill:#e3e9ec;stroke:#fff;stroke-width:.8}.cli{fill:#0089bf;stroke:#fff;stroke-width:.8}.dom{fill:#b3e3ff;stroke:#fff;stroke-width:.8}
.mk{fill:#13232a;stroke:#fff;stroke-width:2}.mt{fill:#fff;font:700 17px system-ui,-apple-system,"Segoe UI",sans-serif;text-anchor:middle;dominant-baseline:central}
@media (prefers-color-scheme:dark){.land{fill:#133847;stroke:#00202d}.cli{fill:#26b3ff;stroke:#00202d}.dom{fill:#003e57;stroke:#00202d}.mk{fill:#d8eef7;stroke:#00202d}.mt{fill:#00202d}}
"""
BG = {"light": "#ffffff", "dark": "#00202d"}


class Canvas:
    """等距圓柱投影，經度乘上中緯度的 cos 修正變形，跟 make_region_map.py 一致。"""

    def __init__(self, lon: list[float], lat: list[float], width: int):
        self.lon0, self.lon1 = lon
        self.lat0, self.lat1 = lat
        self.width = width
        self.kx = math.cos(math.radians((self.lat0 + self.lat1) / 2))
        self.scale = width / ((self.lon1 - self.lon0) * self.kx)
        self.height = round((self.lat1 - self.lat0) * self.scale)

    def project(self, lon: float, lat: float) -> tuple[float, float]:
        return (lon - self.lon0) * self.kx * self.scale, (self.lat1 - lat) * self.scale

    def clip(self, ring: list, pad: float = 4) -> list:
        lo_x, lo_y, hi_x, hi_y = -pad, -pad, self.width + pad, self.height + pad
        edges = [
            (lambda p: p[0] >= lo_x, lambda a, b: (lo_x, a[1] + (b[1] - a[1]) * (lo_x - a[0]) / (b[0] - a[0]))),
            (lambda p: p[0] <= hi_x, lambda a, b: (hi_x, a[1] + (b[1] - a[1]) * (hi_x - a[0]) / (b[0] - a[0]))),
            (lambda p: p[1] >= lo_y, lambda a, b: (a[0] + (b[0] - a[0]) * (lo_y - a[1]) / (b[1] - a[1]), lo_y)),
            (lambda p: p[1] <= hi_y, lambda a, b: (a[0] + (b[0] - a[0]) * (hi_y - a[1]) / (b[1] - a[1]), hi_y)),
        ]
        out = ring
        for inside, cross in edges:
            if not out:
                break
            src, out = out, []
            prev = src[-1]
            for cur in src:
                if inside(cur):
                    if not inside(prev):
                        out.append(cross(prev, cur))
                    out.append(cur)
                elif inside(prev):
                    out.append(cross(prev, cur))
                prev = cur
        return out

    def path(self, polygons: list) -> str:
        parts = []
        for poly in polygons:
            for ring in poly:
                pts = simplify(self.clip([self.project(lon, lat) for lon, lat in ring]), TOLERANCE)
                if len(pts) < 3:
                    continue
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                if max(xs) - min(xs) < 2 and max(ys) - min(ys) < 2:
                    continue  # 縮到不到一個像素的小島
                coords = []
                for x, y in pts:
                    c = f"{round(x)},{round(y)}"
                    if not coords or coords[-1] != c:
                        coords.append(c)
                if len(coords) >= 3:
                    parts.append("M" + "L".join(coords) + "Z")
        return "".join(parts)


def load_geojson(path: str | None) -> dict:
    if path:
        return json.loads(Path(path).read_text())
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "anoni.net-www-build"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.load(resp)


def color_overrides(conf: dict) -> str:
    """設定檔的 [colors] 可以改兩組的填色，各寫 [淺色, 深色]。沒寫就用 CSS 的預設（主色較深、另一種色調較淺）。
    寫在預設之後，同樣的選擇器後面的規則會蓋過前面。"""
    colors = conf.get("colors", {})
    pairs = [(key, cls) for key, cls in (("primary", "cli"), ("secondary", "dom")) if key in colors]
    light = "".join(f".{cls}{{fill:{colors[key][0]}}}" for key, cls in pairs)
    dark = "".join(f".{cls}{{fill:{colors[key][1]}}}" for key, cls in pairs)
    return f"{light}@media (prefers-color-scheme:dark){{{dark}}}" if pairs else ""


def class_styles(conf: dict) -> tuple[str, dict[str, str]]:
    """設定檔的 [[classes]] 是有順序的分級（例如評分的高低），每一級寫 codes、light、dark，
    依序對應 CSS class c1、c2……。回傳樣式與「國碼 → class」的對照。"""
    light, dark, by_code = [], [], {}
    for i, c in enumerate(conf.get("classes", []), 1):
        light.append(f".c{i}{{fill:{c['light']};stroke:#fff;stroke-width:.8}}")
        dark.append(f".c{i}{{fill:{c['dark']};stroke:#00202d}}")
        for code in c["codes"]:
            by_code[code] = f"c{i}"
    if not light:
        return "", by_code
    return "".join(light) + f"@media (prefers-color-scheme:dark){{{''.join(dark)}}}", by_code


def _wrap(polygons: list) -> list:
    """以太平洋為中心的地圖：整個環都在西半球（經度全部小於 0）才加 360。Natural Earth 的多邊形
    已在換日線切開，跨過本初子午線的環（例如英國、法國）維持原樣，才不會被拉成橫跨全圖的長條。"""
    return [[[(lon + 360, lat) for lon, lat in ring] if max(lon for lon, _ in ring) < 0 else ring
             for ring in poly] for poly in polygons]


def render_svg(conf: dict, data: dict) -> str:
    cv = Canvas(conf["lon"], conf["lat"], conf.get("width", 720))
    groups = conf.get("groups", {})
    primary, secondary = set(groups.get("primary", [])), set(groups.get("secondary", []))
    class_css, by_code = class_styles(conf)
    wrap = conf.get("wrap", False)
    paths = {}
    for feature in data["features"]:
        props = feature["properties"]
        code = (props.get("ISO_A2_EH") or props.get("ISO_A2") or "").lower()
        if len(code) != 2 or not code.isalpha():
            continue
        geom = feature["geometry"]
        polygons = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        d = cv.path(_wrap(polygons) if wrap else polygons)
        if d:
            paths[code] = d
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cv.width} {cv.height}" role="img">'
             f'<title>{escape(conf["title"])}</title><style>{CSS.strip()}{color_overrides(conf)}{class_css}</style>']
    colored = primary | secondary | set(by_code)
    # 上色的國家最後畫，國界才不會被鄰國的白邊蓋掉
    for code, d in sorted(paths.items(), key=lambda kv: kv[0] in colored):
        cls = "cli" if code in primary else "dom" if code in secondary else by_code.get(code, "land")
        parts.append(f'<path class="{cls}" d="{d}"/>')
    # 小到看不見的島國用圓點，顏色跟所屬的分級一樣：[經度, 緯度, 國碼]
    for lon, lat, code in conf.get("dots", []):
        x, y = cv.project(lon + 360 if wrap and lon < 0 else lon, lat)
        parts.append(f'<circle class="{by_code.get(code, "land")}" cx="{x:.1f}" cy="{y:.1f}" r="5.5"/>')
    for n, lon, lat in conf.get("markers", []):
        x, y = cv.project(lon + 360 if wrap and lon < 0 else lon, lat)
        parts.append(f'<circle class="mk" cx="{x:.1f}" cy="{y:.1f}" r="14"/>'
                     f'<text class="mt" x="{x:.1f}" y="{y:.1f}">{n}</text>')
    parts.append("</svg>")
    return "".join(parts)


def render_png(svg_file: Path, width: int, height: int) -> list[Path]:
    """淺色與深色各截一張，兩倍解析度，底色跟網站一致。"""
    from playwright.sync_api import sync_playwright
    out = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for scheme, bg in BG.items():
            page = browser.new_page(viewport={"width": width, "height": height},
                                    color_scheme=scheme, device_scale_factor=2)
            html = svg_file.with_name(f"{svg_file.stem}-{scheme}.html")
            html.write_text(f'<body style="margin:0;background:{bg}">'
                            f'<img src="{svg_file.name}" width="{width}" height="{height}" style="display:block"></body>')
            page.goto(html.as_uri())
            page.wait_for_timeout(300)
            png = svg_file.with_name(f"{svg_file.stem}-{scheme}.png")
            page.screenshot(path=str(png))
            html.unlink()
            page.close()
            out.append(png)
        browser.close()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("config", help="tools/maps/ 底下的設定檔")
    ap.add_argument("--out", help="輸出目錄，預設是暫存目錄")
    ap.add_argument("--geojson", help="先前下載的 Natural Earth GeoJSON，省掉重新下載")
    ap.add_argument("--png", action="store_true", help="另外截成淺色與深色兩張 PNG，需要 playwright")
    args = ap.parse_args()

    conf = tomllib.loads(Path(args.config).read_text())
    svg = render_svg(conf, load_geojson(args.geojson))
    digest = hashlib.sha256(svg.encode()).hexdigest()[:8]
    out = Path(args.out) if args.out else Path(tempfile.mkdtemp(prefix="marker-map-"))
    out.mkdir(parents=True, exist_ok=True)
    svg_file = out / f"{conf['name']}-{digest}.svg"
    svg_file.write_text(svg)
    files = [svg_file]
    if args.png:
        cv = Canvas(conf["lon"], conf["lat"], conf.get("width", 720))
        files += render_png(svg_file, cv.width, cv.height)
    for f in files:
        print(f)

    dest = os.environ.get("WWW_MAP_RSYNC")
    if not dest:
        print("沒有設 WWW_MAP_RSYNC，只產生到輸出目錄，沒有上傳")
        return 0
    subprocess.run(["rsync", "-av", *map(str, files), dest.rstrip("/") + "/"], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
