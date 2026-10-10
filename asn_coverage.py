"""OONI 觀測涵蓋率頁（/projects/asn-coverage/）的資料。

一個地區的網路審查觀測，只看得到有人執行 OONI Probe 的那些網路（ASN）。這一頁把 OONI
的測量數跟 APNIC 估計的各 ASN 使用者人數放在一起，看測量涵蓋了多少使用者、集中在哪幾個
網路，以及哪些有不少使用者的網路還沒有任何測量。圖表用 charts.py 畫成內嵌的 SVG。

建置時讀三個公開的來源，都寫進 .cache/asn-coverage/：

- OONI 的彙總 API，各 ASN 每天的測量數，六小時內的建置直接用快取
- APNIC 的 ASN 使用者估計，每週更新一次，快取七天
- RIPE 的 ASN 名稱表，補上不在 APNIC 估計裡的網路名稱，快取七天
- OONI 的彙總 API，通訊 App 測試（Signal、WhatsApp 等）各國最近 30 天的結果，
  一個 App 一次查完所有國家，快取六小時

讀取失敗時退回舊的快取並標示，連快取都沒有就顯示提示，建置照樣成功。
"""

import json
import time
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from charts import SHADES, area, calendar, lines, num, sparkline, stacked_bars

OONI_API = "https://api.ooni.io/api/v1/aggregation"
APNIC_API = "https://stats.labs.apnic.net/aspop/"
RIPE_NAMES = "https://ftp.ripe.net/ripe/asnames/asn.txt"
OONI_MAX_AGE = 6 * 3600
WEEK = 7 * 86400

# 使用者占比在這個比例以上、又沒有任何測量的網路，列進「還沒有測量的網路」
GAP_MIN_PCT = 0.1
# 穩定涵蓋率：最近 N 天裡至少這個比例的日子有測量，才算穩定涵蓋
STABLE_DAYS = 0.5
# 通訊 App 的測試，測量少於這個數字的地區不算比例
APP_MIN = 30


# 資料

def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "anoni.net-www-build"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def cached(path: Path, max_age: int, url: str) -> tuple[bytes | None, bool]:
    """回傳 (內容, 是否是過期的快取)。"""
    if path.exists() and time.time() - path.stat().st_mtime < max_age:
        return path.read_bytes(), False
    try:
        body = fetch(url)
        path.write_bytes(body)
        return body, False
    except Exception as err:  # 連不上、逾時都退回快取
        print(f"asn-coverage：{url} 讀取失敗（{err}），改用快取", flush=True)
        return (path.read_bytes(), True) if path.exists() else (None, False)


def parse_names(text: str) -> dict[int, str]:
    """asn.txt 一行一個 ASN，格式是 `3462 HINET Data Communication Business Group, TW`。"""
    names = {}
    for line in text.splitlines():
        no, _, rest = line.partition(" ")
        if no.isdigit():
            names[int(no)] = rest.rsplit(",", 1)[0].strip()
    return names


def load(codes: list[str], days: int, cache_dir: Path) -> dict:
    cache_dir.mkdir(parents=True, exist_ok=True)
    until = datetime.now(timezone.utc).date()
    since = until - timedelta(days=days)
    body, names_stale = cached(cache_dir / "asn-names.txt", WEEK, RIPE_NAMES)
    names = parse_names(body.decode("utf-8", "replace")) if body else {}
    result = {}
    for code in codes:
        cc = code.upper()
        ooni, ooni_stale = cached(
            cache_dir / f"ooni-{code}.json", OONI_MAX_AGE,
            f"{OONI_API}?probe_cc={cc}&since={since}&until={until}"
            "&axis_x=measurement_start_day&axis_y=probe_asn")
        pop, pop_stale = cached(cache_dir / f"aspop-{code}.json", WEEK, f"{APNIC_API}?c={cc}&f=j")
        try:
            data = {"ooni": json.loads(ooni)["result"], "aspop": json.loads(pop)} if ooni and pop else None
        except (ValueError, KeyError) as err:
            print(f"asn-coverage：{code} 的回應無法解析（{err}）", flush=True)
            data = None
        result[code] = {"data": data, "stale": ooni_stale or pop_stale or names_stale}
    return {"countries": result, "names": names}


def load_apps(tests: list[str], days: int, cache_dir: Path) -> dict:
    """通訊 App 的測試，回傳 {"data": {test: {國碼大寫: 彙總}}, "stale": bool}。"""
    cache_dir.mkdir(parents=True, exist_ok=True)
    until = datetime.now(timezone.utc).date()
    since = until - timedelta(days=days)
    data, stale = {}, False
    for test in tests:
        body, old = cached(cache_dir / f"app-{test}.json", OONI_MAX_AGE,
                           f"{OONI_API}?test_name={test}&since={since}&until={until}&axis_x=probe_cc")
        stale = stale or old
        try:
            data[test] = {r["probe_cc"]: r for r in json.loads(body)["result"]} if body else {}
        except (ValueError, KeyError) as err:
            print(f"asn-coverage：{test} 的回應無法解析（{err}）", flush=True)
            data[test] = {}
    return {"data": data, "stale": stale}


def apps_view(code: str, apps: dict, tests: list[dict], pick) -> list[dict]:
    """一個地區各 App 的測量數與異常比例，測量太少的比例是 None。"""
    rows = []
    for t in tests:
        r = apps["data"].get(t["test"], {}).get(code.upper())
        count = r["measurement_count"] if r else 0
        rows.append({
            "name": t["name"],
            "count": count,
            "anomaly": r["anomaly_count"] / count * 100 if r and count >= APP_MIN else None,
        })
    return rows


# 頁面要的整理過的資料

def pop_date(text: str) -> str:
    """APNIC 的日期寫成 DD/MM/YYYY，頁面上統一用 ISO 的寫法。"""
    try:
        return datetime.strptime(text, "%d/%m/%Y").date().isoformat()
    except ValueError:
        return text


RESULTS = ("ok_count", "anomaly_count", "confirmed_count", "failure_count")


def view(code: str, raw: dict, names: dict[int, str], labels: dict, pick, recent_days: int = 30) -> dict:
    rows = [r for r in raw["ooni"] if r.get("probe_asn")]
    pop = {p["AS"]: p for p in raw["aspop"]["Data"]}
    pop_total = sum(p["Users"] for p in pop.values()) or 1
    share_of = {a: p["Users"] / pop_total * 100 for a, p in pop.items()}

    def name_of(asn: int) -> str:
        if asn in pop:
            return pop[asn]["Description"]
        return names.get(asn, "")

    # 每天：四種結果的測量數、有測量的 ASN、那些 ASN 涵蓋的使用者
    per_day = defaultdict(lambda: {"asns": set(), **{k: 0 for k in RESULTS}, "total": 0})
    per_day_asn = defaultdict(lambda: defaultdict(int))
    for r in rows:
        d = per_day[r["measurement_start_day"]]
        d["asns"].add(r["probe_asn"])
        d["total"] += r["measurement_count"]
        for k in RESULTS:
            d[k] += r.get(k, 0)
        per_day_asn[r["measurement_start_day"]][r["probe_asn"]] += r["measurement_count"]

    def top2(counts: dict) -> float:
        total = sum(counts.values())
        return sum(sorted(counts.values(), reverse=True)[:2]) / total * 100 if total else 0

    daily = []
    for day, d in sorted(per_day.items()):
        daily.append({"date": day, "total": d["total"], "asns": len(d["asns"]),
                      "coverage": sum(share_of.get(a, 0) for a in d["asns"]),
                      "top2": top2(per_day_asn[day]), **{k: d[k] for k in RESULTS}})
    days, by_day = calendar(daily)
    if not days:
        return {"latest": None}

    # 卡片與表格看最近 recent_days 天，跟再往前的同樣天數比
    end = days[-1]
    recent_from = end - timedelta(days=recent_days - 1)
    prev_from = recent_from - timedelta(days=recent_days)

    def window(lo: date, hi: date) -> dict[int, dict]:
        acc = defaultdict(lambda: {"count": 0, "days": 0, "anomaly": 0})
        for r in rows:
            if lo <= date.fromisoformat(r["measurement_start_day"]) <= hi:
                a = acc[r["probe_asn"]]
                a["count"] += r["measurement_count"]
                a["days"] += 1
                a["anomaly"] += r.get("anomaly_count", 0)
        return acc

    recent = window(recent_from, end)
    prev = window(prev_from, recent_from - timedelta(days=1)) if days[0] <= prev_from else None

    def summary(acc: dict) -> dict:
        total = sum(a["count"] for a in acc.values())
        return {
            "asns": len(acc),
            "coverage": sum(share_of.get(a, 0) for a in acc),
            # 只有一兩天有測量的網路，涵蓋率會把它算進去，穩定涵蓋率不算
            "stable": sum(share_of.get(a, 0) for a, v in acc.items() if v["days"] >= recent_days * STABLE_DAYS),
            "total": total,
            "top2": top2({k: v["count"] for k, v in acc.items()}),
        }

    now, then = summary(recent), summary(prev) if prev else None

    def delta(key: str, pct: bool) -> str | None:
        if not then:
            return None
        d = now[key] - then[key]
        if pct:
            return f"{d:+.1f} pp" if round(d, 1) else "±0"
        return ("+" if d > 0 else "") + num(d) if d else "±0"

    def series(key: str) -> list:
        return [by_day[x][key] if x in by_day else None for x in days]

    stats = []
    for key, label, pct in (("asns", "stat_asns", False), ("coverage", "stat_coverage", True),
                            ("total", "stat_total", False), ("top2", "stat_top2", True)):
        d = delta(key, pct)
        stats.append({
            "label": pick(labels[label]),
            "value": f"{now[key]:.1f}" if pct else num(now[key]),
            "unit": "%" if pct else "",
            "delta": d,
            # 測量越分散越好，前兩大的占比往下才是好消息
            "trend": "flat" if not d or d == "±0" else ("up" if (d.startswith("+")) != (key == "top2") else "down"),
            "spark": sparkline(series(key)),
        })

    def col(key: str) -> dict:
        return {d: by_day[d][key] for d in days if d in by_day}

    charts = {
        "measurements": stacked_bars(days, [
            (pick(labels["ok"]), col("ok_count"), "pc-s3"),
            (pick(labels["anomaly"]), col("anomaly_count"), "pc-s1"),
            (pick(labels["confirmed"]), col("confirmed_count"), "pc-s2"),
            (pick(labels["failure"]), col("failure_count"), "pc-s5"),
        ], pick(labels["chart_measurements"])),
        "asns": lines(days, [(pick(labels["stat_asns"]), col("asns"), "pc-s1")], pick(labels["chart_asns"])),
        "coverage": area(days, col("coverage"), pick(labels["chart_coverage"]),
                         pick(labels["stat_coverage"]), f"g-cov-{code}"),
    }

    total = now["total"] or 1
    measured = sorted(recent.items(), key=lambda kv: kv[1]["count"], reverse=True)
    share = [{"asn": f"AS{a}", "name": name_of(a), "pct": v["count"] / total * 100, "shade": SHADES[min(i, 4)]}
             for i, (a, v) in enumerate(measured[:5])]
    if len(measured) > 5:
        rest = sum(v["count"] for _, v in measured[5:])
        share.append({"asn": "", "name": pick(labels["other"]), "pct": rest / total * 100, "shade": "pc-s5 pc-rest"})

    # 使用者最多的網路：使用者占比對照測量占比
    by_users = sorted(pop.values(), key=lambda p: p["Users"], reverse=True)
    networks = [{"asn": f"AS{p['AS']}", "name": p["Description"], "users": share_of[p["AS"]],
                 "measured": recent[p["AS"]]["count"] / total * 100 if p["AS"] in recent else 0,
                 "days": recent[p["AS"]]["days"] if p["AS"] in recent else 0}
                for p in by_users[:10]]

    gaps_all = [p for p in by_users if p["AS"] not in recent and share_of[p["AS"]] >= GAP_MIN_PCT]
    gaps = [{"asn": f"AS{p['AS']}", "name": p["Description"], "users": share_of[p["AS"]]} for p in gaps_all[:8]]

    # 測量裡有、APNIC 估計裡沒有的網路，多半是學術網路、機房或雲端
    outside = [a for a in recent if a not in pop]

    return {
        "latest": end.isoformat(),
        "since": days[0].isoformat(),
        "recent_from": recent_from.isoformat(),
        "stats": stats,
        "charts": charts,
        "asn_share": share,
        "networks": networks,
        # 表格裡的長條以最大的那一格為滿，小網路的長條才看得出差別
        "networks_max": max([n["users"] for n in networks] + [n["measured"] for n in networks] + [1]),
        "gaps": gaps,
        "gaps_count": len(gaps_all),
        "gaps_users": sum(share_of[p["AS"]] for p in gaps_all),
        "outside_count": len(outside),
        "outside_pct": sum(recent[a]["count"] for a in outside) / total * 100,
        "pop_asns": len(pop),
        "pop_date": pop_date(raw["aspop"].get("Date", "")),
        "coverage": now["coverage"],
        "stable": now["stable"],
        "stable_days": int(recent_days * STABLE_DAYS),
        "coverage_series": series("coverage"),
    }
