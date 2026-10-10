"""產生觀測季報的數字檔 data/reports/<季度>.json。

季報的圖表在建置時從這份檔案畫，檔案進版控之後就是那一季定格的數字，之後重建網站
也不會變。每季跑一次：

    # 1. 在 m6 上對 Pulse 的資料庫跑季初與季末的比對（唯讀查詢）
    ssh m6_tailscale "cd /home/ubuntu/app/pulse && docker compose exec -T db sh -c \\
      'psql -U \\$POSTGRES_USER -d \\${POSTGRES_DB:-\\$POSTGRES_USER} -At -v ON_ERROR_STOP=1 \\
       -v since=2026-07-01 -v until=2026-10-01'" < tools/quarterly_pulse.sql > /tmp/pulse-extra.json

    # 2. 抓其餘的公開資料，合併成數字檔
    uv run tools/quarterly_report.py 2026-q3 --pulse-extra /tmp/pulse-extra.json

來源：Pulse 的 /api/summary（每日總數與版本）、OONI 的彙總 API、APNIC 的 ASN 使用者
估計、RIPE NCC 的 ASN 名稱表。APNIC 只提供最近 60 天的估計，查不到過去的值，所以
季報用的是產生當下的那一份，檔案裡記著它的日期。
"""

import argparse
import json
import sys
import tomllib
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from asn_coverage import parse_names, pop_date  # noqa: E402

PULSE_API = "https://anoni.net/api"
OONI_API = "https://api.ooni.io/api/v1/aggregation"
APNIC_API = "https://stats.labs.apnic.net/aspop/"
RIPE_NAMES = "https://ftp.ripe.net/ripe/asnames/asn.txt"
# 社群維運的 OONI Run 連結
RUN_LINK = 10328
REPORT_CC = "tw"


def get(url: str, timeout: int = 120) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "anoni.net-www-quarterly"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def get_json(url: str):
    return json.loads(get(url))


def quarter_range(qid: str) -> tuple[date, date]:
    year, q = qid.lower().split("-q")
    start = date(int(year), (int(q) - 1) * 3 + 1, 1)
    end = date(start.year + (start.month + 2) // 12, (start.month + 2) % 12 + 1, 1)
    return start, end


def ooni(params: str) -> list | dict:
    return get_json(f"{OONI_API}?{params}")["result"]


def stable_version(v: str) -> bool:
    return "-" not in v


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("quarter", help="例如 2026-q3")
    ap.add_argument("--pulse-extra", type=Path, required=True, help="tools/quarterly_pulse.sql 的輸出")
    args = ap.parse_args()

    since, until = quarter_range(args.quarter)
    prev_since, _ = quarter_range(f"{since.year if since.month > 3 else since.year - 1}-q{(since.month - 1) // 3 or 4}")
    pulse_conf = tomllib.loads((ROOT / "data/pulse.toml").read_text(encoding="utf-8"))
    codes = [c["code"] for c in pulse_conf["countries"]]
    extra = json.loads(args.pulse_extra.read_text(encoding="utf-8"))
    if extra["since"] != since.isoformat() or extra["until"] != until.isoformat():
        sys.exit(f"--pulse-extra 的期間是 {extra['since']} 到 {extra['until']}，跟 {args.quarter} 不符")

    today = datetime.now(timezone.utc).date()
    days = (today - prev_since).days + 1

    # Pulse：兩季的每日總數、季末的版本分布、這一季第一次出現的版本
    pulse = {"daily": {}, "versions_end": {}, "first_seen": {}}
    first_any: dict[str, str] = {}
    for cc in codes:
        s = get_json(f"{PULSE_API}/summary?country={cc}&days={min(days, 365)}")
        pulse["daily"][cc] = [
            {k: d[k] for k in ("date", "running", "stopped", "bandwidth", "exit", "asns")}
            for d in s["daily"] if prev_since.isoformat() <= d["date"] < until.isoformat()]
        in_q = [v for v in s["versions"] if since.isoformat() <= v["date"] < until.isoformat()]
        last = max((v["date"] for v in in_q), default=None)
        pulse["versions_end"][cc] = sorted(
            ({"version": v["version"], "count": v["count"]} for v in in_q if v["date"] == last),
            key=lambda v: -v["count"])
        seen = {}
        for v in s["versions"]:
            if v["date"] < until.isoformat():
                seen[v["version"]] = min(seen.get(v["version"], v["date"]), v["date"])
        pulse["first_seen"][cc] = seen
        for ver, d in seen.items():
            first_any[ver] = min(first_any.get(ver, d), d)
        print(f"pulse {cc}: {len(pulse['daily'][cc])} 天", flush=True)
    pulse["releases"] = sorted(
        ({"version": v, "first_seen": d} for v, d in first_any.items()
         if stable_version(v) and since.isoformat() <= d < until.isoformat()),
        key=lambda r: r["first_seen"])
    # 每個地區只留這一季新版本第一次出現的日期，其他版本用不到
    new = {r["version"] for r in pulse["releases"]}
    pulse["first_seen"] = {cc: {v: d for v, d in seen.items() if v in new} for cc, seen in pulse["first_seen"].items()}
    pulse["churn"] = {c["country"]: c for c in extra["churn"]}
    # 季末各 ASN 的中繼數：臺灣全部留下，其他地區只要前五名（算集中度用前兩名，總數在 churn）
    pulse["asn_end"] = defaultdict(list)
    for a in extra["asn_end"]:
        if a["country"] == REPORT_CC or len(pulse["asn_end"][a["country"]]) < 5:
            pulse["asn_end"][a["country"]].append({"asn": a["asn"], "as_name": a["as_name"], "n": a["n"]})
    pulse["asn_start"] = [{"asn": a["asn"], "n": a["n"]} for a in extra["asn_start"] if a["country"] == REPORT_CC]

    # APNIC：各地區的網路使用者總數，臺灣另外留各 ASN 的占比
    apnic = {"users": {}, "asns": []}
    for cc in codes:
        d = get_json(f"{APNIC_API}?c={cc.upper()}&f=j")
        apnic["users"][cc] = sum(p["Users"] for p in d["Data"])
        apnic["date"] = pop_date(d.get("Date", ""))
        if cc == REPORT_CC:
            total = apnic["users"][cc] or 1
            apnic["asns"] = [{"asn": p["AS"], "name": p["Description"], "pct": p["Users"] / total * 100}
                             for p in d["Data"]]
        print(f"apnic {cc}", flush=True)

    # OONI：本季每天各 ASN 的測量、上一季各 ASN 的測量、社群 OONI Run 連結、網站測試的確認封鎖
    cc = REPORT_CC.upper()
    q = f"probe_cc={cc}&since={since}&until={until}"
    p = f"probe_cc={cc}&since={prev_since}&until={since}"
    rows = ooni(f"{q}&axis_x=measurement_start_day&axis_y=probe_asn")
    per_asn = defaultdict(lambda: {"count": 0, "days": 0, "anomaly": 0, "confirmed": 0, "failure": 0})
    daily = defaultdict(lambda: {"total": 0, "ok": 0, "anomaly": 0, "confirmed": 0, "failure": 0, "asns": 0})
    for r in rows:
        if not r.get("probe_asn"):
            continue
        a = per_asn[r["probe_asn"]]
        a["count"] += r["measurement_count"]
        a["days"] += 1
        for k in ("anomaly", "confirmed", "failure"):
            a[k] += r[f"{k}_count"]
        d = daily[r["measurement_start_day"]]
        d["total"] += r["measurement_count"]
        d["asns"] += 1
        for k in ("ok", "anomaly", "confirmed", "failure"):
            d[k] += r[f"{k}_count"]
    prev = {r["probe_asn"]: r["measurement_count"] for r in ooni(f"{p}&axis_x=probe_asn") if r.get("probe_asn")}
    run_q = {r["probe_asn"]: r["measurement_count"] for r in ooni(f"{q}&axis_x=probe_asn&ooni_run_link_id={RUN_LINK}")
             if r.get("probe_asn")}
    run_prev = ooni(f"{p}&ooni_run_link_id={RUN_LINK}")["measurement_count"]
    web = ooni(f"{q}&test_name=web_connectivity&axis_x=domain&axis_y=probe_asn")
    confirmed = [r for r in web if r["confirmed_count"]]
    by_domain = defaultdict(int)
    for r in confirmed:
        by_domain[r["domain"]] += r["confirmed_count"]
    print(f"ooni: {len(per_asn)} 個 ASN", flush=True)

    names = parse_names(get(RIPE_NAMES).decode("utf-8", "replace"))
    known = {a["asn"] for a in apnic["asns"]}
    wanted = (set(per_asn) | set(prev) | set(run_q)) - known

    data = {
        "quarter": args.quarter.lower(),
        "since": since.isoformat(),
        "until": until.isoformat(),
        "prev_since": prev_since.isoformat(),
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "countries": codes,
        "pulse": pulse,
        "apnic": apnic,
        "ooni": {
            "cc": REPORT_CC,
            "per_asn": {str(k): v for k, v in sorted(per_asn.items())},
            "daily": [{"date": k, **v} for k, v in sorted(daily.items())],
            "prev_per_asn": {str(k): v for k, v in sorted(prev.items())},
            "run_link": RUN_LINK,
            "run_per_asn": {str(k): v for k, v in sorted(run_q.items())},
            "run_prev_total": run_prev,
            # 網站測試裡確認封鎖的測量。網域名稱不放進來，季報只寫數量與分布
            "web_total": sum(r["measurement_count"] for r in web),
            "web_confirmed": sum(r["confirmed_count"] for r in web),
            "web_confirmed_domains": len(by_domain),
            "web_confirmed_max_per_domain": max(by_domain.values(), default=0),
            "web_confirmed_asns": len({r["probe_asn"] for r in confirmed}),
        },
        "names": {str(a): names.get(a, "") for a in sorted(wanted)},
    }
    out = ROOT / "data" / "reports" / f"{args.quarter.lower()}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"寫入 {out.relative_to(ROOT)}（{out.stat().st_size // 1024} KB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
