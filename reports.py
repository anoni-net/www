"""觀測季報（/projects/reports/<季度>/）的資料整理與圖表。

數字來自 data/reports/<季度>.json，由 tools/quarterly_report.py 每季產生一次之後定格。
這裡只負責把那份檔案整理成模板要的形狀，圖表用 charts.py 畫成內嵌的 SVG，跟 Tor 中繼
節點觀測頁同一套樣式。季報的文字寫在 reports/<語系>/<季度>.md，圖表與表格用
<!-- rq-名稱 --> 放進文字之間，名稱對應 templates/_report.html.j2 裡的 macro。
"""

import json
import tomllib
from datetime import date, timedelta
from pathlib import Path

from charts import SHADES, calendar, lines, num, stacked_bars

TYPES = ("mobile", "fixed", "academic", "other")


def load(root: Path, qid: str) -> dict:
    return json.loads((root / "data" / "reports" / f"{qid}.json").read_text(encoding="utf-8"))


def asn_types(root: Path, cc: str) -> dict[int, str]:
    conf = tomllib.loads((root / "data" / "reports" / "asn-types.toml").read_text(encoding="utf-8")).get(cc, {})
    return {asn: kind for kind in TYPES for asn in conf.get(kind, [])}


def gaps(days: list[date], have: set[date]) -> list[tuple[date, date]]:
    """沒有資料的連續日期區段。"""
    out, start = [], None
    for d in days:
        if d not in have and start is None:
            start = d
        if d in have and start is not None:
            out.append((start, d - timedelta(days=1)))
            start = None
    if start is not None:
        out.append((start, days[-1]))
    return out


def complete_days(daily: list[dict]) -> tuple[list[dict], list[str]]:
    """拿掉不完整的快照。收集中途出錯的那一小時只會收到少數中繼，例如 2026-04-07 臺灣只有
    3 筆、全部是已停止，畫出來像中繼全部消失。總數（運作中加已停止）不到中位數一半的日子
    當作缺資料，回傳留下的日子與被拿掉的日期。"""
    totals = sorted(d["running"] + d["stopped"] for d in daily)
    if not totals:
        return daily, []
    median = totals[len(totals) // 2]
    keep = [d for d in daily if d["running"] + d["stopped"] >= median / 2]
    return keep, [d["date"] for d in daily if d not in keep]


def pct(part: float, whole: float) -> float:
    return part / whole * 100 if whole else 0


def view(root: Path, data: dict, labels: dict, pick, names: dict) -> dict:
    cc = data["ooni"]["cc"]
    since, until = date.fromisoformat(data["since"]), date.fromisoformat(data["until"])
    q_days = [since + timedelta(days=i) for i in range((until - since).days)]
    p = data["pulse"]

    # 中繼：兩季的每日走勢，季初與季末
    daily, dropped_days = complete_days(p["daily"][cc])
    days, by_day = calendar(daily)
    in_q = [d for d in daily if since.isoformat() <= d["date"] < until.isoformat()]
    first, last = in_q[0], in_q[-1]
    q_have = {date.fromisoformat(d["date"]) for d in in_q}
    churn = p["churn"][cc]
    left, new = churn["at_start"] - churn["stayed"], churn["at_end"] - churn["stayed"]

    def col(key, f=lambda v: v):
        return {d: f(by_day[d][key]) for d in days if d in by_day}

    relays_chart = stacked_bars(days, [(pick(labels["running"]), col("running"), "pc-s1"),
                                       (pick(labels["stopped"]), col("stopped"), "pc-s4")],
                                pick(labels["chart_relays"]))

    # 升級：季末跑這一季新版本的比例，以及新版本在各地區第一次出現的日期
    new_versions = [r["version"] for r in p["releases"]]
    upgrade = []
    for c in data["countries"]:
        vs = p["versions_end"][c]
        total = sum(v["count"] for v in vs)
        on_new = sum(v["count"] for v in vs if v["version"] in new_versions)
        lag = None
        if new_versions:
            seen = p["first_seen"][c].get(new_versions[0])
            if seen:
                lag = (date.fromisoformat(seen) - date.fromisoformat(p["releases"][0]["first_seen"])).days
        upgrade.append({"code": c, "pct": pct(on_new, total), "on_new": on_new, "total": total, "lag": lag})
    upgrade.sort(key=lambda u: -u["pct"])

    # 網路分布：臺灣季末各 ASN 的中繼，各地區前兩大 ASN 的占比
    asn_end = p["asn_end"][cc]
    share = [{"asn": a["asn"], "name": a["as_name"], "n": a["n"], "pct": pct(a["n"], churn["at_end"]),
              "shade": SHADES[min(i, 4)]} for i, a in enumerate(asn_end)]
    top2 = []
    for c in data["countries"]:
        top = p["asn_end"][c][:2]
        top2.append({"code": c, "pct": pct(sum(a["n"] for a in top), p["churn"][c]["at_end"])})
    top2.sort(key=lambda t: -t["pct"])

    # 每百萬網路使用者的中繼數，使用者人數是 APNIC 的估計
    density = []
    for c in data["countries"]:
        users = data["apnic"]["users"][c]
        density.append({"code": c, "relays": p["churn"][c]["at_end"], "users": users,
                        "value": p["churn"][c]["at_end"] / (users / 1_000_000) if users else 0})
    density.sort(key=lambda d: -d["value"])
    dmax = max(d["value"] for d in density) or 1

    # OONI：本季與上一季的涵蓋率、測量集中度
    o = data["ooni"]
    users = {a["asn"]: a for a in data["apnic"]["asns"]}
    q_asn = {int(k): v for k, v in o["per_asn"].items()}
    prev_asn = {int(k): v for k, v in o["prev_per_asn"].items()}

    def coverage(asns) -> float:
        return sum(users[a]["pct"] for a in asns if a in users)

    def top2_share(counts: dict) -> float:
        vals = sorted(counts.values(), reverse=True)
        return pct(sum(vals[:2]), sum(vals))

    q_counts = {a: v["count"] for a, v in q_asn.items()}
    q_total = sum(q_counts.values())
    prev_total = sum(prev_asn.values())

    def name_of(asn: int) -> str:
        return users[asn]["name"] if asn in users else names.get(str(asn), "")

    ooni_stats = {
        "coverage": coverage(q_asn), "coverage_prev": coverage(prev_asn),
        "asns": len(q_asn), "asns_prev": len(prev_asn),
        "total": q_total, "total_prev": prev_total,
        "top2": top2_share(q_counts), "top2_prev": top2_share(prev_asn),
        "outside": len([a for a in q_asn if a not in users]),
    }
    added = sorted((a for a in q_asn if a not in prev_asn), key=lambda a: -q_counts[a])
    dropped = sorted((a for a in prev_asn if a not in q_asn), key=lambda a: -prev_asn[a])

    # 網路類型：使用者占比、測量占比、類型內的涵蓋率
    kinds = asn_types(root, cc)
    by_type = {k: {"users": 0.0, "covered": 0.0, "measured": 0} for k in TYPES}
    for a, u in users.items():
        k = kinds.get(a, "other")
        by_type[k]["users"] += u["pct"]
        if a in q_asn:
            by_type[k]["covered"] += u["pct"]
    for a, n in q_counts.items():
        by_type[kinds.get(a, "other")]["measured"] += n
    types = [{"kind": k, "label": pick(labels[f"type_{k}"]), "users": v["users"],
              "measured": pct(v["measured"], q_total), "coverage": pct(v["covered"], v["users"])}
             for k, v in by_type.items() if v["users"] or v["measured"]]

    networks = [{"asn": f"AS{a['asn']}", "name": a["name"], "users": a["pct"],
                 "measured": pct(q_counts.get(a["asn"], 0), q_total),
                 "days": q_asn[a["asn"]]["days"] if a["asn"] in q_asn else 0,
                 "kind": pick(labels[f"type_{kinds.get(a['asn'], 'other')}"])}
                for a in data["apnic"]["asns"][:10]]
    networks_max = max([n["users"] for n in networks] + [n["measured"] for n in networks] + [1])
    gap_list = [{"asn": f"AS{a['asn']}", "name": a["name"], "users": a["pct"],
                 "kind": pick(labels[f"type_{kinds.get(a['asn'], 'other')}"])}
                for a in data["apnic"]["asns"] if a["asn"] not in q_asn and a["pct"] >= 0.1]

    o_daily = o["daily"]
    od, ob = calendar(o_daily)

    def ocol(key):
        return {d: ob[d][key] for d in od if d in ob}

    measurements_chart = stacked_bars(od, [
        (pick(labels["ok"]), ocol("ok"), "pc-s3"),
        (pick(labels["anomaly"]), ocol("anomaly"), "pc-s1"),
        (pick(labels["confirmed"]), ocol("confirmed"), "pc-s2"),
        (pick(labels["failure"]), ocol("failure"), "pc-s5"),
    ], pick(labels["chart_measurements"]))
    asns_chart = lines(od, [(pick(labels["chart_asns"]), ocol("asns"), "pc-s1")], pick(labels["chart_asns"]))

    run = {int(k): v for k, v in o["run_per_asn"].items()}
    run_total = sum(run.values())
    run_list = [{"asn": f"AS{a}", "name": name_of(a), "n": n, "pct": pct(n, run_total),
                 "kind": pick(labels[f"type_{kinds.get(a, 'other')}"])}
                for a, n in sorted(run.items(), key=lambda kv: -kv[1])]

    return {
        "label": data["quarter"].upper().replace("-", " "),
        "since": since, "until": until - timedelta(days=1),
        "pulse_days": len(q_have), "q_days": len(q_days), "dropped_days": dropped_days,
        "pulse_gaps": gaps(q_days, q_have),
        "relays": {
            "start": first, "end": last, "churn": churn, "left": left, "new": new,
            "chart": relays_chart,
            "bandwidth_start": first["bandwidth"] / 1_000_000, "bandwidth_end": last["bandwidth"] / 1_000_000,
        },
        "flow_max": max(churn["at_start"], churn["at_end"]) or 1,
        "releases": p["releases"],
        "upgrade": upgrade,
        "upgrade_cc": next(u for u in upgrade if u["code"] == cc),
        "asn_share": share,
        "asn_start_count": len(p["asn_start"]),
        "top2": top2,
        "density": [{**d, "bar": d["value"] / dmax * 100} for d in density],
        "ooni": ooni_stats,
        "added": [{"asn": f"AS{a}", "name": name_of(a), "n": q_counts[a]} for a in added],
        "dropped": [{"asn": f"AS{a}", "name": name_of(a), "n": prev_asn[a]} for a in dropped],
        "types": types,
        "networks": networks,
        "networks_max": networks_max,
        "gaps": gap_list,
        "gaps_users": sum(g["users"] for g in gap_list),
        "measurements_chart": measurements_chart,
        "asns_chart": asns_chart,
        "run": {"total": run_total, "prev": o["run_prev_total"], "list": run_list,
                "share": pct(run_total, q_total), "link": o["run_link"]},
        "web": {k: o[f"web_{k}"] for k in ("total", "confirmed", "confirmed_domains",
                                             "confirmed_max_per_domain", "confirmed_asns")},
        "apnic_date": data["apnic"]["date"],
        "num": num,
    }
