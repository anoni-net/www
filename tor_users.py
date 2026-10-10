"""Tor 中繼節點觀測頁（/projects/pulse/）的使用者估計。

Tor Metrics 從中繼收到的目錄請求推算每個地區每天平均同時上線的 Tor 客戶端，直接連線與透過
橋接（bridge）的分開計算。這是平均同時上線的數量，不是不重複的人數，方法與限制見文件站的
「台灣有多少人在用 Tor」。橋接的比例高，通常代表直接連上 Tor 受到阻擋。

建置時讀 Tor Metrics 的公開 CSV（CC0），每個地區兩份，加上全球（all）兩份當分母，
都寫進 .cache/tor-users/。Tor Metrics 每天更新一次、晚兩三天，十二小時內的建置直接用快取。
讀取失敗時退回舊的快取並標示，連快取都沒有就不畫這一段，建置照樣成功。
"""

import time
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from charts import calendar, lines, num, sparkline

METRICS = "https://metrics.torproject.org"
KINDS = {"relay": "userstats-relay-country.csv", "bridge": "userstats-bridge-country.csv"}
MAX_AGE = 12 * 3600


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "anoni.net-www-build"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def cached(path: Path, url: str) -> tuple[bytes | None, bool]:
    """回傳 (內容, 是否是過期的快取)。"""
    if path.exists() and time.time() - path.stat().st_mtime < MAX_AGE:
        return path.read_bytes(), False
    try:
        body = fetch(url)
        path.write_bytes(body)
        return body, False
    except Exception as err:  # 連不上、逾時都退回快取
        print(f"tor-users：{url} 讀取失敗（{err}），改用快取", flush=True)
        return (path.read_bytes(), True) if path.exists() else (None, False)


def parse(text: str) -> dict[str, float]:
    """CSV 開頭是 # 註解，接著 date,country,users,…。users 空白的日子還沒算出來，略過。"""
    rows = {}
    header = None
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        cols = line.split(",")
        if header is None:
            header = cols
            continue
        row = dict(zip(header, cols))
        if row.get("users"):
            rows[row["date"]] = float(row["users"])
    return rows


def load(codes: list[str], days: int, cache_dir: Path) -> dict:
    """回傳 {code: {"data": {"relay": {日期: 人數}, "bridge": {…}} 或 None, "stale": bool}}，
    code 多一個 "all" 是全球。"""
    cache_dir.mkdir(parents=True, exist_ok=True)
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days)
    result = {}
    for code in [*codes, "all"]:
        data, stale = {}, False
        for kind, csv in KINDS.items():
            body, old = cached(cache_dir / f"{kind}-{code}.csv",
                               f"{METRICS}/{csv}?start={start}&end={end}&country={code}")
            stale = stale or old
            data[kind] = parse(body.decode("utf-8", "replace")) if body else None
        ok = data["relay"] is not None and data["bridge"] is not None
        result[code] = {"data": data if ok else None, "stale": stale}
    return result


# 頁面要的整理過的資料

def pct(value: float | None) -> str:
    """比例的寫法，小的地區只有千分之幾，多留幾位小數。"""
    if value is None:
        return "–"
    if 0 < value < 0.001:
        return "<0.001%"
    if value < 0.1:
        return f"{value:.3f}%"
    if value < 1:
        return f"{value:.2f}%"
    return f"{value:.1f}%"


def recent(series: dict[str, float], last: str, back: int) -> list[float]:
    """last（含）往前 back 天裡有值的日子。"""
    first = (date.fromisoformat(last) - timedelta(days=back - 1)).isoformat()
    return [v for d, v in series.items() if first <= d <= last]


def view(raw: dict, world: dict | None, labels: dict, pick, recent_days: int = 30) -> dict | None:
    """一個地區的使用者估計。最近 recent_days 天取平均，兩份 CSV 都有值的最後一天當結尾。"""
    relay, bridge = raw["relay"], raw["bridge"]
    both = sorted(set(relay) & set(bridge))
    if not both:
        return None
    last = both[-1]
    r, b = recent(relay, last, recent_days), recent(bridge, last, recent_days)
    users = sum(r) / len(r) + sum(b) / len(b)
    bridge_avg = sum(b) / len(b)
    share = None
    if world and world["relay"] and world["bridge"]:
        wr, wb = recent(world["relay"], last, recent_days), recent(world["bridge"], last, recent_days)
        if wr and wb:
            share = users / (sum(wr) / len(wr) + sum(wb) / len(wb)) * 100

    daily = [{"date": d, "relay": relay.get(d), "bridge": bridge.get(d)} for d in sorted(set(relay) | set(bridge))]
    days, by_day = calendar(daily)

    def col(key):
        return {d: by_day[d][key] for d in days if d in by_day and by_day[d][key] is not None}

    bridge_pct = {d: by_day[d]["bridge"] / (by_day[d]["relay"] + by_day[d]["bridge"]) * 100
                  for d in days if d in by_day and by_day[d]["relay"] and by_day[d]["bridge"] is not None}
    return {
        "last": last,
        "users": users,
        "users_text": num(users),
        "bridge_pct": bridge_avg / users * 100 if users else None,
        "share": share,
        "spark_users": sparkline([(by_day[d]["relay"] or 0) + (by_day[d]["bridge"] or 0) if d in by_day else None
                                  for d in days]),
        "spark_bridge": sparkline([bridge_pct.get(d) for d in days]),
        # 透過橋接的人數多半只有直接連線的幾十分之一，畫在同一張圖會貼在底線上，改畫比例
        "chart": lines(days, [(pick(labels["users_direct"]), col("relay"), "pc-s1")], pick(labels["chart_users"])),
        "chart_bridge": lines(days, [(pick(labels["bridge_share"]), bridge_pct, "pc-s2")],
                              pick(labels["chart_bridge"])),
    }
