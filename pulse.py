"""Tor 中繼節點觀測頁（/projects/pulse/）的資料。

建置時從 Pulse 的 /api/summary 讀每個國家的資料，圖表用 charts.py 畫成內嵌的 SVG。

API 的位址由環境變數 PULSE_API 指定，m6 上是本機的 http://127.0.0.1:8899/api。
讀到的資料寫進 .cache/pulse/，十分鐘內的建置直接用快取（部署腳本會先 --check 再建置，
同一輪不必打兩次 API）。API 沒有回應時退回舊的快取並標示，連快取都沒有就顯示提示。
"""

import json
import os
import time
import urllib.request
from datetime import date, timedelta
from pathlib import Path

from charts import SHADES, area, calendar, lines, num, share_bars, sparkline, stacked_bars

DEFAULT_API = "https://anoni.net/api"
MAX_AGE = 600

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


# 頻寬

def mbps(byte_rate: float) -> float:
    return byte_rate / 1_000_000


def bandwidth_parts(byte_rate: float) -> tuple[str, str]:
    mb = mbps(byte_rate)
    return (f"{mb / 1000:,.1f}", "GB/s") if abs(mb) >= 1000 else (f"{mb:,.1f}", "MB/s")


def bandwidth_text(byte_rate: float) -> str:
    return " ".join(bandwidth_parts(byte_rate))


# 頁面要的整理過的資料



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
        # 占全網路共識權重的比例，Pulse 2026-10 起才收集，舊的快照與舊的快取沒有
        "weight": latest["weight"] * 100 if latest and latest.get("weight") is not None else None,
        "spark_weight": sparkline([by_day[x].get("weight") if x in by_day else None for x in days]),
    }
