"""把觀測季報的幾張圖表輸出成電子報可用的 HTML 與純文字。

信件程式大多不顯示 SVG，遠端圖片又會回傳開信紀錄，所以電子報版的圖表用表格與底色畫
（templates/_report_email.html.j2），純文字版用 █ 字元畫長條。數字跟網頁同一份
data/reports/<季度>.json，信件與網頁不會對不上。

    uv run tools/report_email.py 2026-q3 --lang zh-TW --out /tmp/q3-email

每張圖輸出 <名稱>.html 與 <名稱>.txt，貼進 mail-mass 的信件模板（HTML 與 Markdown 各一份）。
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402
import reports  # noqa: E402

BLOCKS = ("stats", "regions", "types")
WIDTH = 20


def bar(pct: float) -> str:
    n = max(0, min(WIDTH, round(pct / 100 * WIDTH)))
    return "█" * n + "░" * (WIDTH - n)


def text_blocks(v: dict, L: dict, cname: dict, cc: str, regions: list[str], en: bool) -> dict[str, str]:
    colon, lp, rp = (": ", " (", ")") if en else ("：", "（", "）")
    r = v["relays"]
    tw = next(d for d in v["density"] if d["code"] == cc)
    top2 = next(t for t in v["top2"] if t["code"] == cc)
    first = v["asn_share"][0]
    stats = "\n".join([
        f"- {L['em_relays']}{colon}{r['end']['running']}{lp}{L['at_start']} {r['start']['running']}{rp}",
        f"- {L['em_density']}{colon}{tw['value']:.1f}",
        f"- {L['em_top2']}{colon}{top2['pct']:.0f}%{lp}{first['asn']} · {first['n']} / {r['end']['running']}{rp}",
        f"- {L['em_upgrade']}{colon}{v['upgrade_cc']['pct']:.0f}%{lp}{v['upgrade_cc']['on_new']} / {v['upgrade_cc']['total']}{rp}",
    ])
    counts = sorted(((v["relays_end"][c], c) for c in regions), reverse=True)
    top = counts[0][0] or 1
    density = [L["em_regions"], ""]
    for n, c in counts:
        density.append(f"    {bar(n / top * 100)} {n:>4}  {cname[c]}")
    types = [L["em_types"], ""]
    for t in v["types"]:
        types.append(f"    {t['label']}")
        types.append(f"    {bar(t['users'])} {t['users']:5.1f}%  {L['col_users']}")
        types.append(f"    {bar(t['measured'])} {t['measured']:5.1f}%  {L['col_measured']}")
    return {"stats": stats, "regions": "\n".join(density), "types": "\n".join(types)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("quarter")
    ap.add_argument("--lang", default="zh-TW")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    site = build.Site()
    labels = site.data["reports"]["labels"]
    pick = lambda value: value[args.lang] if isinstance(value, dict) else value  # noqa: E731
    L = {k: pick(v) for k, v in labels.items()}
    cname = {c["code"]: pick(c["name"]) for c in site.data["pulse"]["countries"]}
    data = reports.load(ROOT, args.quarter)
    v = reports.view(ROOT, data, labels, pick, data["names"])
    cc = data["ooni"]["cc"]
    regions = site.data["reports"]["email_regions"]
    module = site.env.get_template("_report_email.html.j2").make_module(
        {"v": v, "L": L, "cname": cname, "cc": cc,
         "region_rows": sorted(((c, v["relays_end"][c]) for c in regions), key=lambda r: -r[1])})
    args.out.mkdir(parents=True, exist_ok=True)
    texts = text_blocks(v, L, cname, cc, regions, args.lang == "en")
    for name in BLOCKS:
        html = "\n".join(line for line in str(getattr(module, name)()).splitlines() if line.strip())
        (args.out / f"{name}.html").write_text(html + "\n", encoding="utf-8")
        (args.out / f"{name}.txt").write_text(texts[name] + "\n", encoding="utf-8")
        print(f"{args.out / name}.html / .txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
