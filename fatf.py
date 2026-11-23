"""匿名支付主題 FATF 系列（/join/payments-research/fatf/）的圖表，畫成內嵌的 SVG。

Markdown 寫 <!-- fatf-grey -->、<!-- fatf-share -->、<!-- fatf-ratings -->、<!-- fatf-groups -->、
<!-- fatf-imf -->，由 build.py 的 fatf_blocks() 換成這裡畫的圖，文字在 data/fatf.toml。
資料的整理方法與來源見工作區的 research/fatf-grey-list/（toomore/anoni-net-ws#512）。

外觀沿用 charts.py 的畫布與 .pulse 的圖表樣式。所得分組是有順序的類別，用同一個色相由深到淺
（.fi-1 到 .fi-4，色值在 site.css 的 .fatf），深色模式另選四階。時間軸的兩張圖在手機上另畫一張
較高的版本，用 CSS 依寬度切換，文字不會被拉長。頁面不需要 JavaScript，每個長條都有 <title>。
"""

import csv
import statistics
from datetime import date
from html import escape
from pathlib import Path

from charts import BOTTOM, LEFT, RIGHT, TOP, W, tick

GROUPS = ("high", "upper_middle", "lower_middle", "low", "unclassified")  # 由下往上疊
SHADE = {"high": "fi-1", "upper_middle": "fi-2", "lower_middle": "fi-3", "low": "fi-4", "unclassified": "fi-na"}
GAP = 2  # 堆疊分段之間留的底色間隙
WIDE, NARROW = 240, 420  # 桌機與手機的畫布高度

# 斜線材質放在獨立、不隱藏的 SVG 裡，桌機與手機兩張圖共用。放在被 display:none 的那張裡，Chrome 不會畫
HATCH = ('<svg class="fi-defs" width="0" height="0" aria-hidden="true"><defs><pattern id="fi-hatch" width="6" '
         'height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect class="fi-na-bg" width="6" '
         'height="6"/><line class="fi-na-line" x1="0" y1="0" x2="0" y2="6"/></pattern></defs></svg>')


def load(data_dir: Path) -> tuple[list[dict], list[dict]]:
    grey = list(csv.DictReader((data_dir / "income-groups.csv").open(encoding="utf-8")))
    ratings = list(csv.DictReader((data_dir / "ratings.csv").open(encoding="utf-8")))
    return grey, ratings


def pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def signed(value: float) -> str:
    return f"{value:.2f}".replace("-", "−")


def _bar_path(x: float, y_top: float, w: float, h: float, r: float = 3) -> str:
    """上緣兩角圓弧、下緣貼齊基線的長條。"""
    r = min(r, h, w / 2)
    return (f"M{x:.1f},{y_top + h:.1f} V{y_top + r:.1f} Q{x:.1f},{y_top:.1f} {x + r:.1f},{y_top:.1f} "
            f"H{x + w - r:.1f} Q{x + w:.1f},{y_top:.1f} {x + w:.1f},{y_top + r:.1f} V{y_top + h:.1f} Z")


def _time_frame(rows: list[dict], height: int, ticks: tuple, top: float, label: str, cls: str, fmt=tick):
    """以每次大會為一格的時間軸：橫軸在每年第一次大會標年份，縱軸用給定的刻度。"""
    plot_w, plot_h = W - LEFT - RIGHT, height - TOP - BOTTOM
    step = plot_w / len(rows)

    def y(v: float) -> float:
        return TOP + plot_h - v / top * plot_h

    p = [f'<svg class="pc {cls}" viewBox="0 0 {W} {height}" role="img" aria-label="{escape(label)}">']
    for v in ticks:
        p.append(f'<line class="pc-grid" x1="{LEFT}" x2="{W - RIGHT}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
        p.append(f'<text class="pc-tick" x="{LEFT - 6}" y="{y(v) + 4:.1f}" text-anchor="end">{fmt(v)}</text>')
    seen = set()
    for i, r in enumerate(rows):
        year = r["plenary_date"][:4]
        if year not in seen:
            seen.add(year)
            p.append(f'<text class="pc-tick" x="{LEFT + step * i + step / 2:.1f}" y="{height - 6}" '
                     f'text-anchor="middle">{year}</text>')
    return p, step, plot_h, y


def _pause(p: list, rows: list[dict], pause: str, step: float, plot_h: float, note: str) -> None:
    for i, r in enumerate(rows):
        if r["plenary_date"] == pause:
            p.append(f'<rect class="fi-pause" x="{LEFT + step * i:.1f}" y="{TOP}" width="{step:.1f}" '
                     f'height="{plot_h:.1f}"><title>{escape(note)}</title></rect>')


def _month(r: dict) -> str:
    return date.fromisoformat(r["plenary_date"]).strftime("%Y/%m")


def grey_bars(rows: list[dict], L: dict, pause: str, height: int, cls: str) -> str:
    """每次大會一條堆疊長條，長條總高是灰名單的國家數，分段是所得分組。"""
    top = 30  # 最多是 2023/06 的 26 國
    p, step, plot_h, y = _time_frame(rows, height, (0, 10, 20, 30), top, L["grey"], cls)
    _pause(p, rows, pause, step, plot_h, L["pause"])
    bw = step * 0.7
    peak = max(range(len(rows)), key=lambda i: int(rows[i]["grey_count"]))
    p.append('<g class="pc-marks">')
    for i, r in enumerate(rows):
        x = LEFT + step * i + (step - bw) / 2
        segs = [(g, int(r[g])) for g in GROUPS if int(r[g])]
        base = 0
        for j, (g, v) in enumerate(segs):
            y0, y1 = y(base), y(base + v)
            tip = f"<title>{_month(r)} {escape(L[g])} {escape(L['count'].format(n=v))}</title>"
            if j == len(segs) - 1:
                p.append(f'<path class="{SHADE[g]}" d="{_bar_path(x, y1, bw, y0 - y1)}">{tip}</path>')
            else:
                p.append(f'<rect class="{SHADE[g]}" x="{x:.1f}" y="{y1 + GAP:.1f}" width="{bw:.1f}" '
                         f'height="{max(y0 - y1 - GAP, 0):.1f}">{tip}</rect>')
            base += v
        total = int(r["grey_count"])
        if i in (peak, len(rows) - 1):
            p.append(f'<text class="pc-note fi-total" x="{LEFT + step * i + step / 2:.1f}" y="{y(total) - 5:.1f}" '
                     f'text-anchor="middle">{total}</text>')
    p.append("</g></svg>")
    return "".join(p)


def share_lines(rows: list[dict], L: dict, pause: str, height: int, cls: str) -> str:
    """灰名單裡非高所得的比例，對照同一年度全世界的比例。兩條線用同一個百分比刻度。"""
    p, step, plot_h, y = _time_frame(rows, height, (0, 0.25, 0.5, 0.75, 1), 1, L["share"], cls,
                                     fmt=lambda v: f"{v * 100:.0f}%")
    _pause(p, rows, pause, step, plot_h, L["pause"])
    p.append('<g class="pc-marks pc-trace">')
    for key, name, shade in (("world_not_high_share", L["share_world"], "fi-world"),
                             ("not_high_share", L["share_grey"], "fi-2")):
        pts = []
        for i, r in enumerate(rows):
            cx, cy = LEFT + step * i + step / 2, y(float(r[key]))
            pts.append(f"{cx:.1f},{cy:.1f}")
            p.append(f'<circle class="pc-dot {shade}" cx="{cx:.1f}" cy="{cy:.1f}" r="3">'
                     f'<title>{_month(r)} {escape(name)} {pct(float(r[key]))}</title></circle>')
        p.append(f'<polyline class="pc-line {shade}" points="{" ".join(pts)}"/>')
    p.append("</g></svg>")
    return "".join(p)


def ratings_hist(ratings: list[dict], L: dict, height: int, cls: str) -> str:
    """每個司法管轄區達到實質或高度有效的項數（0 到 11），每一格是幾個司法管轄區，標出台灣那一格。"""
    counts = [0] * 12
    for r in ratings:
        counts[int(r["high_or_substantial"])] += 1
    taiwan = int(next(r for r in ratings if r["jurisdiction"] == "Chinese Taipei")["high_or_substantial"])
    top = 90  # 最多是 0 項的 83 個
    plot_w, plot_h = W - LEFT - RIGHT, height - TOP - BOTTOM
    step = plot_w / 12

    def y(v: float) -> float:
        return TOP + plot_h - v / top * plot_h

    p = [f'<svg class="pc {cls}" viewBox="0 0 {W} {height}" role="img" aria-label="{escape(L["ratings"])}">']
    for v in (0, 30, 60, 90):
        p.append(f'<line class="pc-grid" x1="{LEFT}" x2="{W - RIGHT}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
        p.append(f'<text class="pc-tick" x="{LEFT - 6}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    bw = step * 0.7
    p.append('<g class="pc-marks">')
    for k, n in enumerate(counts):
        cx = LEFT + step * k + step / 2
        p.append(f'<text class="pc-tick" x="{cx:.1f}" y="{height - 6}" text-anchor="middle">{k}</text>')
        if not n:
            continue
        shade = "fi-1" if k == taiwan else "fi-3"
        p.append(f'<path class="{shade}" d="{_bar_path(cx - bw / 2, y(n), bw, y(0) - y(n))}">'
                 f'<title>{escape(L["ratings_bin"].format(k=k, n=n))}</title></path>')
        # 0 項那一格標數量，台灣那一格只標「台灣」，數量放在 <title>，免得被讀成台灣的分數
        if k == 0:
            p.append(f'<text class="pc-note fi-total" x="{cx:.1f}" y="{y(n) - 5:.1f}" text-anchor="middle">{n}</text>')
        if k == taiwan:
            p.append(f'<text class="pc-note fi-total" x="{cx:.1f}" y="{y(n) - 5:.1f}" text-anchor="middle">'
                     f'{escape(L["taiwan"])}</text>')
    p.append("</g></svg>")
    return "".join(p)


def group_means(ratings: list[dict]) -> list[tuple[str, float]]:
    def mean(items):
        return round(statistics.mean(int(r["high_or_substantial"]) for r in items), 2)

    member = [r for r in ratings if r["fatf_member"] == "True"]
    other = [r for r in ratings if r["fatf_member"] != "True"]
    high = [r for r in ratings if r["income_group"] == "high"]
    rows = [("member", mean(member)), ("not_member", mean(other))]
    rows += [(g, mean([r for r in ratings if r["income_group"] == g])) for g in GROUPS[:4]]
    rows += [("high_member", mean([r for r in high if r["fatf_member"] == "True"])),
             ("high_not_member", mean([r for r in high if r["fatf_member"] != "True"]))]
    return rows


def groups_bars(ratings: list[dict], L: dict) -> str:
    items = []
    for key, v in group_means(ratings):
        items.append(f'<li><span class="l">{escape(L[key])}</span><span class="bar"><span style="width:'
                     f'{v / 11 * 100:.2f}%"></span></span><span class="n">{v:.1f}</span></li>')
    return f'<ul class="pulse-bars fi-groups" aria-label="{escape(L["groups"])}">{"".join(items)}</ul>'


def imf_bars(imf: dict, L: dict, narrow: bool = False) -> str:
    """IMF 估計的資本流入變化，四個項目各一條往左的長條，橫線是 95% 信賴區間。
    手機版把項目名稱放到長條上方，長條用滿整個寬度，列高與長條也加粗。"""
    rows = [("total", "imf_total"), ("fdi", "imf_fdi"), ("portfolio", "imf_portfolio"), ("other", "imf_other")]
    if narrow:
        label_w, right, row_h, top_pad, bh = 24, 24, 92, 40, 26
    else:
        label_w, right, row_h, top_pad, bh = 150, 24, 44, 26, 14
    height = top_pad + row_h * len(rows) + 8
    lo = -12
    plot_w = W - label_w - right

    def x(v: float) -> float:
        return label_w + (v - lo) / (0 - lo) * plot_w

    cls = "fi-narrow" if narrow else "fi-wide"
    p = [f'<svg class="pc fi-imf {cls}" viewBox="0 0 {W} {height}" role="img" aria-label="{escape(L["imf"])}">']
    for v in (-12, -9, -6, -3, 0):
        p.append(f'<line class="pc-grid" x1="{x(v):.1f}" x2="{x(v):.1f}" y1="{top_pad - 6}" y2="{height - 6}"/>')
        p.append(f'<text class="pc-tick" x="{x(v):.1f}" y="{top_pad - 12}" text-anchor="middle">'
                 f'{signed(v).rstrip("0").rstrip(".")}</text>')
    p.append('<g class="pc-marks">')
    for i, (key, name) in enumerate(rows):
        v, ci_lo, ci_hi = imf[key]
        cy = top_pad + row_h * i + (row_h / 2 + 14 if narrow else row_h / 2)
        tip = f"<title>{escape(L[name])} {escape(L['imf_ci'].format(v=signed(v), lo=signed(ci_lo), hi=signed(ci_hi)))}</title>"
        if narrow:
            p.append(f'<text class="fi-label" x="{label_w}" y="{cy - bh / 2 - 12:.1f}">{escape(L[name])}</text>')
        else:
            p.append(f'<text class="fi-label" x="{label_w - 10}" y="{cy + 5:.1f}" text-anchor="end">{escape(L[name])}</text>')
        shade = "fi-1" if key == "total" else "fi-3"
        p.append(f'<rect class="{shade}" x="{x(v):.1f}" y="{cy - bh / 2:.1f}" width="{x(0) - x(v):.1f}" '
                 f'height="{bh}" rx="4">{tip}</rect>')
        # 信賴區間的線先畫一圈底色，壓在深色長條上也看得到
        for halo in ("fi-ci-halo", "fi-ci"):
            p.append(f'<line class="{halo}" x1="{x(ci_lo):.1f}" x2="{x(ci_hi):.1f}" y1="{cy:.1f}" y2="{cy:.1f}"/>')
            for end in (ci_lo, ci_hi):
                p.append(f'<line class="{halo}" x1="{x(end):.1f}" x2="{x(end):.1f}" y1="{cy - bh / 2 + 2:.1f}" '
                         f'y2="{cy + bh / 2 - 2:.1f}"/>')
        if narrow:
            p.append(f'<text class="pc-note fi-total" x="{x(0):.1f}" y="{cy - bh / 2 - 12:.1f}" text-anchor="end">'
                     f'{signed(v)}</text>')
        else:
            p.append(f'<text class="pc-note fi-total" x="{x(ci_lo) - 6:.1f}" y="{cy + 4:.1f}" text-anchor="end">'
                     f'{signed(v)}</text>')
    p.append("</g></svg>")
    return "".join(p)


def legend(L: dict, keys: list[tuple[str, str]]) -> str:
    return "".join(f'<i class="sw {shade}"></i>{escape(L[key])}' for key, shade in keys)


def figure(title: str, body: str, lg: str = "", note: str = "", table: str = "") -> str:
    head = f'<figcaption>{escape(title)}<span class="lg">{lg}</span></figcaption>' if lg else f"<figcaption>{escape(title)}</figcaption>"
    foot = f'<p class="fi-note">{escape(note)}</p>' if note else ""
    return f'<div class="pulse fatf"><figure class="pulse-chart">{head}{body}{foot}{table}</figure></div>'


def grey_table(rows: list[dict], L: dict) -> str:
    head = f"<tr><th>{escape(L['plenary'])}</th>" + "".join(f"<th>{escape(L[g])}</th>" for g in GROUPS)
    head += f"<th>{escape(L['share_grey'])}</th><th>{escape(L['share_world'])}</th></tr>"
    body = "".join(
        f"<tr><td>{_month(r)}</td>" + "".join(f"<td>{r[g]}</td>" for g in GROUPS)
        + f"<td>{r['grey_count']}（{pct(float(r['not_high_share']))}）</td><td>{pct(float(r['world_not_high_share']))}</td></tr>"
        for r in rows)
    return f'<details><summary>{escape(L["table"])}</summary><div class="fi-table"><table>{head}{body}</table></div></details>'


def blocks(data_dir: Path, conf: dict, pick) -> dict[str, str]:
    L = {k: pick(v) for k, v in conf["labels"].items()}
    grey, ratings = load(data_dir)
    pause = conf["pause"]
    both = lambda fn, *args: fn(*args, WIDE, "fi-wide") + fn(*args, NARROW, "fi-narrow")  # noqa: E731
    income_lg = legend(L, [(g, SHADE[g]) for g in GROUPS])
    return {
        "fatf-grey": figure(L["grey"], HATCH + both(grey_bars, grey, L, pause), income_lg, L["grey_note"],
                            grey_table(grey, L)),
        "fatf-share": figure(L["share"], both(share_lines, grey, L, pause),
                             legend(L, [("share_grey", "fi-2"), ("share_world", "fi-world")]), L["share_note"]),
        "fatf-ratings": figure(L["ratings"], both(ratings_hist, ratings, L), note=L["ratings_note"]),
        "fatf-groups": figure(L["groups"], groups_bars(ratings, L)),
        "fatf-imf": figure(L["imf"], imf_bars(conf["imf"], L) + imf_bars(conf["imf"], L, narrow=True),
                           note=L["imf_note"]),
    }


def check(data_dir: Path) -> list[str]:
    """build.py --check 用：資料檔的基本一致性。"""
    problems = []
    grey, ratings = load(data_dir)
    for r in grey:
        if sum(int(r[g]) for g in GROUPS) != int(r["grey_count"]):
            problems.append(f"data/fatf/income-groups.csv：{r['plenary_date']} 各分組加總不等於 grey_count")
    if not any(r["jurisdiction"] == "Chinese Taipei" for r in ratings):
        problems.append("data/fatf/ratings.csv：沒有 Chinese Taipei")
    return problems

