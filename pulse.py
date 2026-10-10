"""Tor 中繼節點觀測頁（/projects/pulse/）的資料與圖表。

建置時從 Pulse 的 /api/summary 讀每個國家的資料，圖表畫成內嵌的 SVG，頁面不需要
JavaScript，onion 版也不會連到 clearnet。顏色一律用 CSS class，深色模式跟著網站的
樣式走。每個長條與資料點都有 <title>，滑鼠停在上面會顯示數值。

API 的位址由環境變數 PULSE_API 指定，m6 上是本機的 http://127.0.0.1:8899/api。
讀到的資料寫進 .cache/pulse/，十分鐘內的建置直接用快取（部署腳本會先 --check 再建置，
同一輪不必打兩次 API）。API 沒有回應時退回舊的快取並標示，連快取都沒有就顯示提示。
"""

import json
import math
import os
import time
import urllib.request
from datetime import date, timedelta
from html import escape
from pathlib import Path

from markupsafe import Markup

DEFAULT_API = "https://anoni.net/api"
MAX_AGE = 600

# 圖表的畫布，SVG 用 viewBox 縮放，寬度跟著外框走
W, H = 640, 220
LEFT, RIGHT, TOP, BOTTOM = 54, 10, 14, 30


# 資料

def fetch(code: str, days: int, api: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(
        f"{api.rstrip('/')}/summary?country={code}&days={days}",
        headers={"User-Agent": "anoni.net-www-build"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.load(resp)


def load(codes: list[str], days: int, cache_dir: Path) -> dict[str, dict]:
    """每個國家回傳 {"data": 摘要或 None, "stale": 是否是舊的快取}。"""
    api = os.environ.get("PULSE_API", DEFAULT_API)
    cache_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    for code in codes:
        path = cache_dir / f"{code}.json"
        if path.exists() and time.time() - path.stat().st_mtime < MAX_AGE:
            result[code] = {"data": json.loads(path.read_text()), "stale": False}
            continue
        try:
            data = fetch(code, days, api)
            path.write_text(json.dumps(data))
            result[code] = {"data": data, "stale": False}
        except Exception as err:  # 連不上、逾時、回應不是 JSON 都退回快取
            print(f"pulse：{code} 讀取失敗（{err}），改用快取", flush=True)
            data = json.loads(path.read_text()) if path.exists() else None
            result[code] = {"data": data, "stale": data is not None}
    return result


def calendar(daily: list[dict]) -> tuple[list[date], dict[date, dict]]:
    """從第一天到最後一天的每一天，沒有資料的日子對應不到值，畫出來是缺口。"""
    by_day = {date.fromisoformat(d["date"]): d for d in daily}
    if not by_day:
        return [], {}
    first, last = min(by_day), max(by_day)
    return [first + timedelta(days=i) for i in range((last - first).days + 1)], by_day


# 數字

def nice_max(value: float) -> float:
    if value <= 0:
        return 1
    exp = 10 ** math.floor(math.log10(value))
    for step in (1, 2, 2.5, 5, 10):
        if value <= step * exp:
            return step * exp
    return 10 * exp


def num(value: float) -> str:
    return f"{value:,.0f}" if value >= 100 or value == int(value) else f"{value:,.1f}"


def tick(value: float) -> str:
    """刻度用精簡的寫法，手機上的刻度字放大之後才放得下。"""
    if value >= 1_000_000:
        return f"{value / 1_000_000:g}M"
    if value >= 1000:
        return f"{value / 1000:g}k"
    return f"{value:g}"


def mbps(byte_rate: float) -> float:
    return byte_rate / 1_000_000


def bandwidth_parts(byte_rate: float) -> tuple[str, str]:
    mb = mbps(byte_rate)
    return (f"{mb / 1000:,.1f}", "GB/s") if abs(mb) >= 1000 else (f"{mb:,.1f}", "MB/s")


def bandwidth_text(byte_rate: float) -> str:
    return " ".join(bandwidth_parts(byte_rate))


# SVG 的共用部分

def _frame(days: list[date], top: float, label: str, height: int = H) -> tuple[list[str], callable, callable]:
    plot_w, plot_h = W - LEFT - RIGHT, height - TOP - BOTTOM
    step = plot_w / max(len(days), 1)

    def x(i: int) -> float:
        return LEFT + step * i

    def y(v: float) -> float:
        return TOP + plot_h - (v / top) * plot_h

    parts = [f'<svg class="pc" viewBox="0 0 {W} {height}" role="img" aria-label="{escape(label)}">']
    for frac in (0, 0.5, 1):
        gy = y(top * frac)
        parts.append(f'<line class="pc-grid" x1="{LEFT}" x2="{W - RIGHT}" y1="{gy:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'<text class="pc-tick" x="{LEFT - 6}" y="{gy + 4:.1f}" text-anchor="end">{tick(top * frac)}</text>')
    if days:
        for i in sorted({0, len(days) // 2, len(days) - 1}):
            anchor = "start" if i == 0 else "end" if i == len(days) - 1 else "middle"
            tx = x(i) if i == 0 else x(i + 1) if i == len(days) - 1 else x(i) + step / 2
            parts.append(f'<text class="pc-tick" x="{tx:.1f}" y="{height - 6}" text-anchor="{anchor}">{days[i]:%m/%d}</text>')
    return parts, x, y


def _step(days: list[date]) -> float:
    return (W - LEFT - RIGHT) / max(len(days), 1)


def stacked_bars(days: list[date], series: list[tuple[str, dict, str]], label: str) -> Markup:
    """series 是 (名稱, {日期: 數值}, CSS class)，由下往上疊。"""
    totals = [sum(s[1].get(d, 0) or 0 for s in series) for d in days]
    top = nice_max(max(totals, default=0))
    parts, x, y = _frame(days, top, label)
    bar = _step(days) * 0.72
    for i, d in enumerate(days):
        base = 0
        for name, values, cls in series:
            v = values.get(d)
            if v is None:
                continue
            y0, y1 = y(base), y(base + v)
            parts.append(f'<rect class="{cls}" x="{x(i) + (_step(days) - bar) / 2:.1f}" y="{y1:.1f}" '
                         f'width="{bar:.1f}" height="{max(y0 - y1, 0):.1f}"><title>{d:%Y/%m/%d} {escape(name)} {num(v)}</title></rect>')
            base += v
    parts.append("</svg>")
    return Markup("".join(parts))


def area(days: list[date], values: dict, label: str, name: str, gid: str) -> Markup:
    top = nice_max(max((v for v in values.values() if v is not None), default=0))
    parts, x, y = _frame(days, top, label)
    half = _step(days) / 2
    parts.append(f'<defs><linearGradient id="{gid}" x1="0" x2="0" y1="0" y2="1">'
                 '<stop offset="0" class="pc-grad-top"/><stop offset="1" class="pc-grad-bottom"/></linearGradient></defs>')
    # 有缺口的日子把線段切開，每一段各自畫一塊面積
    runs, run = [], []
    for i, d in enumerate(days):
        if values.get(d) is None:
            if run:
                runs.append(run)
            run = []
        else:
            run.append((i, d, values[d]))
    if run:
        runs.append(run)
    for run in runs:
        pts = " ".join(f"{x(i) + half:.1f},{y(v):.1f}" for i, _, v in run)
        if len(run) > 1:
            parts.append(f'<polygon fill="url(#{gid})" points="{x(run[0][0]) + half:.1f},{y(0):.1f} {pts} '
                         f'{x(run[-1][0]) + half:.1f},{y(0):.1f}"/>')
            parts.append(f'<polyline class="pc-line" points="{pts}"/>')
        for i, d, v in run:
            parts.append(f'<circle class="pc-dot" cx="{x(i) + half:.1f}" cy="{y(v):.1f}" r="2.6">'
                         f'<title>{d:%Y/%m/%d} {escape(name)} {num(v)}</title></circle>')
    parts.append("</svg>")
    return Markup("".join(parts))


def lines(days: list[date], series: list[tuple[str, dict, str]], label: str) -> Markup:
    top = nice_max(max((v for s in series for v in s[1].values() if v is not None), default=0))
    parts, x, y = _frame(days, top, label)
    half = _step(days) / 2
    for name, values, cls in series:
        segment = []
        for i, d in enumerate(days + [None]):
            v = values.get(d) if d else None
            if v is None:
                if len(segment) > 1:
                    parts.append(f'<polyline class="pc-line {cls}" points="{" ".join(segment)}"/>')
                segment = []
                continue
            segment.append(f"{x(i) + half:.1f},{y(v):.1f}")
            parts.append(f'<circle class="pc-dot {cls}" cx="{x(i) + half:.1f}" cy="{y(v):.1f}" r="2.2">'
                         f'<title>{d:%Y/%m/%d} {escape(name)} {num(v)}</title></circle>')
    parts.append("</svg>")
    return Markup("".join(parts))


def share_bars(days: list[date], series: list[tuple[str, dict, str]], label: str) -> Markup:
    """每天的長條疊滿 100%，看各系列的占比變化。"""
    parts, x, y = _frame(days, 100, label)
    bar = _step(days) * 0.72
    for i, d in enumerate(days):
        total = sum(s[1].get(d, 0) or 0 for s in series)
        if not total:
            continue
        base = 0
        for name, values, cls in series:
            v = values.get(d) or 0
            if not v:
                continue
            pct = v / total * 100
            y0, y1 = y(base), y(base + pct)
            parts.append(f'<rect class="{cls}" x="{x(i) + (_step(days) - bar) / 2:.1f}" y="{y1:.1f}" '
                         f'width="{bar:.1f}" height="{max(y0 - y1, 0):.1f}"><title>{d:%Y/%m/%d} {escape(name)} {num(v)}（{pct:.0f}%）</title></rect>')
            base += pct
    parts.append("</svg>")
    return Markup("".join(parts))


def sparkline(values: list, width: int = 120, height: int = 32) -> Markup:
    pts = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(pts) < 2:
        return Markup("")
    lo = min(v for _, v in pts)
    hi = max(v for _, v in pts)
    span = (hi - lo) or 1
    step = width / max(len(values) - 1, 1)
    coords = " ".join(f"{i * step:.1f},{height - 3 - (v - lo) / span * (height - 6):.1f}" for i, v in pts)
    last_x, last_y = coords.split()[-1].split(",")
    return Markup(f'<svg class="pc-spark" viewBox="0 0 {width} {height}" aria-hidden="true">'
                  f'<polyline points="{coords}"/><circle cx="{last_x}" cy="{last_y}" r="2.5"/></svg>')


# 頁面要的整理過的資料

SHADES = ["pc-s1", "pc-s2", "pc-s3", "pc-s4", "pc-s5"]


def view(summary: dict, labels: dict, pick, days_back: int = 30) -> dict:
    """把 API 的摘要整理成模板直接用的形狀，圖表都在這裡畫好。"""
    daily = summary["daily"]
    days, by_day = calendar(daily)

    def col(key, f=lambda v: v):
        return {d: f(by_day[d][key]) for d in days if d in by_day}

    latest = daily[-1] if daily else None
    # 跟 days_back 天前（或最接近、更早的那一天）比
    then = None
    if latest:
        target = date.fromisoformat(latest["date"]) - timedelta(days=days_back)
        earlier = [d for d in daily if date.fromisoformat(d["date"]) <= target]
        then = earlier[-1] if earlier else daily[0]

    def delta(key):
        if not latest or not then or then is latest:
            return None
        return latest[key] - then[key]

    stats = []
    for key, label in (("running", "relays"), ("bandwidth", "bandwidth"), ("asns", "asns"), ("exit", "exits")):
        d = delta(key)
        value, unit = bandwidth_parts(latest[key]) if latest and key == "bandwidth" else (num(latest[key]) if latest else "–", "")
        stats.append({
            "label": pick(labels[label]),
            "value": value,
            "unit": unit,
            "delta": None if d is None else (("+" if d > 0 else "") + (bandwidth_text(d) if key == "bandwidth" else num(d))),
            "trend": "up" if d and d > 0 else "down" if d and d < 0 else "flat",
            "spark": sparkline([by_day[x][key] if x in by_day else None for x in days]),
        })

    running_name, stopped_name = pick(labels["running"]), pick(labels["stopped"])
    charts = {
        "relays": stacked_bars(days, [(running_name, col("running"), "pc-s1"),
                                      (stopped_name, col("stopped"), "pc-s4")], pick(labels["chart_relays"])),
        "bandwidth": area(days, col("bandwidth", mbps), pick(labels["chart_bandwidth"]),
                          pick(labels["bandwidth"]), f"g-bw-{summary['country']}"),
        "asns": lines(days, [(pick(labels["asn_trend"]), col("asns"), "pc-s1")], pick(labels["asn_trend"])),
        "roles": lines(days, [("Guard", col("guard"), "pc-s1"), ("Middle", col("middle"), "pc-s3"),
                              ("Exit", col("exit"), "pc-s2 pc-dash")], pick(labels["roles"])),
    }

    # Tor 版本：最近一天最多的四個，其他的合併。舊的快取沒有 versions，退回按系列分
    series_by = {}
    by_version = summary.get("versions")
    for s in by_version if by_version is not None else summary["series"]:
        key = s["version"] if by_version is not None else s["series"]
        series_by.setdefault(key, {})[date.fromisoformat(s["date"])] = s["count"]
    last_day = days[-1] if days else None
    ranked = sorted(series_by, key=lambda k: (series_by[k].get(last_day, 0), k), reverse=True)
    keep = ranked[:4]
    other = {}
    for k in ranked[4:]:
        for d, v in series_by[k].items():
            other[d] = other.get(d, 0) + v
    version_series = [(k, series_by[k], SHADES[i]) for i, k in enumerate(keep)]
    if other:
        version_series.append((pick(labels["other"]), other, "pc-s5"))
    charts["versions"] = share_bars(days, version_series, pick(labels["versions"]))

    asns = summary["latest"]["asns"]
    total_relays = sum(a["count"] for a in asns) or 1
    top_asns = asns[:8]
    rest = asns[8:]
    share = [{"asn": a["asn"], "name": a["as_name"], "count": a["count"],
              "pct": a["count"] / total_relays * 100, "shade": SHADES[min(i, 4)]} for i, a in enumerate(asns[:5])]
    if len(asns) > 5:
        n = sum(a["count"] for a in asns[5:])
        share.append({"asn": "", "name": "", "count": n, "pct": n / total_relays * 100, "shade": "pc-s5 pc-rest"})

    running = latest["running"] if latest else 0
    flags = [{"flag": f["flag"], "count": f["count"], "pct": f["count"] / (running or 1) * 100}
             for f in summary["latest"]["flags"] if f["flag"] not in ("Running", "Valid")]
    versions = summary["latest"]["versions"]
    vtotal = sum(v["count"] for v in versions) or 1

    return {
        "latest": latest,
        "snapshot": summary["latest"]["snapshot"],
        "stats": stats,
        "charts": charts,
        "legend_versions": [(k, cls) for k, _, cls in version_series],
        "asn_share": share,
        "asn_top": [{**a, "pct": a["count"] / total_relays * 100} for a in top_asns],
        "asn_rest": len(rest),
        "flags": flags,
        "versions": [{**v, "pct": v["count"] / vtotal * 100} for v in versions[:8]],
        "running_series": [by_day[x]["running"] if x in by_day else None for x in days],
    }
