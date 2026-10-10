"""產生觀測地區地圖用的國界資料 data/region-map.json。

來源是 Natural Earth 的 1:50m 國界（公有領域），香港、澳門、新加坡在這個比例尺有獨立的邊界。
只留亞洲那一塊（東經 60 到 150 度、南緯 12 度到北緯 50 度），投影成等距圓柱（經度乘上
中緯度的 cos 修正變形），裁到畫布範圍，再用 Douglas-Peucker 簡化到一個像素左右，座標取整數。地圖只用來看出關注哪些地區，細節不需要，
每一頁都內嵌一份，檔案越小越好。
輸出的路徑已經是畫布座標，build.py 直接拼成 SVG，建置時不需要地理運算的套件。

國界變動很少，資料改了才需要重新執行一次，產出的 JSON 進版控：

    uv run tools/make_region_map.py
"""

import json
import math
import sys
import urllib.request
from pathlib import Path

SOURCE = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
          "geojson/ne_50m_admin_0_countries.geojson")
OUT = Path(__file__).resolve().parent.parent / "data" / "region-map.json"

LON0, LON1, LAT0, LAT1 = 60.0, 150.0, -12.0, 50.0
WIDTH = 720
KX = math.cos(math.radians((LAT0 + LAT1) / 2))
SCALE = WIDTH / ((LON1 - LON0) * KX)
HEIGHT = round((LAT1 - LAT0) * SCALE)
TOLERANCE = 0.9
# 面積太小、縮到畫布上看不見的地區另外記一個中心點，地圖上畫成圓點
POINTS = {"hk", "mo", "sg"}


def project(lon: float, lat: float) -> tuple[float, float]:
    return (lon - LON0) * KX * SCALE, (LAT1 - lat) * SCALE


def clip(ring: list, pad: float = 4) -> list:
    """Sutherland-Hodgman，把多邊形裁到畫布外擴一點的矩形，俄羅斯這類大國只留畫得到的部分。"""
    lo_x, lo_y, hi_x, hi_y = -pad, -pad, WIDTH + pad, HEIGHT + pad
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


def simplify(points: list, tol: float) -> list:
    if len(points) < 3:
        return points
    if points[0] == points[-1]:
        # 封閉的環頭尾是同一點，直接算會退化成零長度的線段，先從離起點最遠的點切成兩半
        x0, y0 = points[0]
        k = max(range(len(points)), key=lambda i: (points[i][0] - x0) ** 2 + (points[i][1] - y0) ** 2)
        if k == 0:
            return points[:1]
        return simplify(points[:k + 1], tol) + simplify(points[k:], tol)[1:]
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = points[a]
        bx, by = points[b]
        dx, dy = bx - ax, by - ay
        norm = math.hypot(dx, dy) or 1e-9
        far, idx = 0.0, None
        for i in range(a + 1, b):
            px, py = points[i]
            d = abs(dy * px - dx * py + bx * ay - by * ax) / norm
            if d > far:
                far, idx = d, i
        if idx is not None and far > tol:
            keep[idx] = True
            stack += [(a, idx), (idx, b)]
    return [p for p, k in zip(points, keep) if k]


def path(polygons: list) -> str:
    parts = []
    for poly in polygons:
        for ring in poly:
            pts = clip([project(lon, lat) for lon, lat in ring])
            pts = simplify(pts, TOLERANCE)
            if len(pts) < 3:
                continue
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
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


def centroid(polygons: list) -> list[float]:
    """最大那一塊的外框的平均點，夠標一個圓點就好。"""
    ring = max((poly[0] for poly in polygons), key=len)
    pts = [project(lon, lat) for lon, lat in ring]
    return [round(sum(p[0] for p in pts) / len(pts), 1), round(sum(p[1] for p in pts) / len(pts), 1)]


def main() -> int:
    req = urllib.request.Request(SOURCE, headers={"User-Agent": "anoni.net-www-build"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    countries, points = {}, {}
    for feature in data["features"]:
        props = feature["properties"]
        code = (props.get("ISO_A2_EH") or props.get("ISO_A2") or "").lower()
        if len(code) != 2 or not code.isalpha():
            continue
        geom = feature["geometry"]
        polygons = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        d = path(polygons)
        if d:
            countries[code] = d
        if code in POINTS:
            points[code] = centroid(polygons)
    OUT.write_text(json.dumps({
        "source": "Natural Earth 1:50m Admin 0 Countries (public domain)",
        "width": WIDTH, "height": HEIGHT,
        "countries": dict(sorted(countries.items())),
        "points": points,
    }, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"寫入 {OUT}：{len(countries)} 個地區，{OUT.stat().st_size:,} bytes，畫布 {WIDTH}x{HEIGHT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
