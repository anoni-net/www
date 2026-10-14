"""觀測頁共用的圖表，畫成內嵌的 SVG。

/projects/pulse/ 與 /projects/asn-coverage/ 都用這裡的函式，頁面不需要 JavaScript，
onion 版也不會連到 clearnet。顏色一律用 CSS class（`.pc-s1` 到 `.pc-s5`），深色模式跟著
網站的樣式走。每個長條與資料點都有 <title>，滑鼠停在上面會顯示數值。
"""

import math
from datetime import date, timedelta
from html import escape

from markupsafe import Markup

# 圖表的畫布，SVG 用 viewBox 縮放，寬度跟著外框走
W, H = 640, 220
LEFT, RIGHT, TOP, BOTTOM = 54, 10, 14, 30


# 日期

def calendar(daily: list[dict]) -> tuple[list[date], dict[date, dict]]:
    """從第一天到最後一天的每一天，沒有資料的日子對應不到值，畫出來是缺口。"""
    by_day = {date.fromisoformat(d["date"]): d for d in daily}
    if not by_day:
        return [], {}
    first, last = min(by_day), max(by_day)
    return [first + timedelta(days=i) for i in range((last - first).days + 1)], by_day


def align(series: dict[str, dict]) -> dict[str, list]:
    """多個 {日期: 數值} 對齊到同一段日期，從最早到最晚的每一天，沒有資料的日子是 None。"""
    every = [d for values in series.values() for d in values]
    if not every:
        return {k: [] for k in series}
    first, last = min(every), max(every)
    days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
    return {k: [values.get(d) for d in days] for k, values in series.items()}


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
    parts.append('<g class="pc-marks pc-bars">')
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
    parts.append("</g></svg>")
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
    parts.append('<g class="pc-marks pc-trace">')
    for run in runs:
        pts = " ".join(f"{x(i) + half:.1f},{y(v):.1f}" for i, _, v in run)
        if len(run) > 1:
            parts.append(f'<polygon fill="url(#{gid})" points="{x(run[0][0]) + half:.1f},{y(0):.1f} {pts} '
                         f'{x(run[-1][0]) + half:.1f},{y(0):.1f}"/>')
            parts.append(f'<polyline class="pc-line" points="{pts}"/>')
        for i, d, v in run:
            parts.append(f'<circle class="pc-dot" cx="{x(i) + half:.1f}" cy="{y(v):.1f}" r="2.6">'
                         f'<title>{d:%Y/%m/%d} {escape(name)} {num(v)}</title></circle>')
    parts.append("</g></svg>")
    return Markup("".join(parts))


def lines(days: list[date], series: list[tuple[str, dict, str]], label: str) -> Markup:
    top = nice_max(max((v for s in series for v in s[1].values() if v is not None), default=0))
    parts, x, y = _frame(days, top, label)
    half = _step(days) / 2
    parts.append('<g class="pc-marks pc-trace">')
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
    parts.append("</g></svg>")
    return Markup("".join(parts))


def timeline(points: list[tuple[date, float]], cap: float, label: str, bands=(), markers=(),
             peak: str | None = None, height: int = 240) -> Markup:
    """幾年長的每日曲線，不畫資料點，橫軸標年份。

    cap 是縱軸上限，超過的部分壓在上緣，用 peak 標出實際的最高值，讓短期的異常不會把長期的
    小幅變化壓扁。bands 是 (開始, 結束, 文字) 的底色區間，markers 是 (日期, 文字) 的垂直虛線。
    """
    if len(points) < 2:
        return Markup("")
    first, last = points[0][0], points[-1][0]
    span = (last - first).days or 1
    plot_w, plot_h = W - LEFT - RIGHT, height - TOP - BOTTOM

    def x(d: date) -> float:
        return LEFT + plot_w * (d - first).days / span

    def y(v: float) -> float:
        return TOP + plot_h - (min(v, cap) / cap) * plot_h

    parts = [f'<svg class="pc pc-timeline" viewBox="0 0 {W} {height}" role="img" aria-label="{escape(label)}">']
    for start, end, text in bands:
        x0, x1 = x(max(start, first)), x(min(end, last))
        parts.append(f'<rect class="pc-band" x="{x0:.1f}" y="{TOP}" width="{x1 - x0:.1f}" height="{plot_h}"/>')
        parts.append(f'<text class="pc-note" x="{x0 + 4:.1f}" y="{TOP + plot_h - 8}">{escape(text)}</text>')
    for frac in (0, 0.5, 1):
        gy = y(cap * frac)
        parts.append(f'<line class="pc-grid" x1="{LEFT}" x2="{W - RIGHT}" y1="{gy:.1f}" y2="{gy:.1f}"/>')
        parts.append(f'<text class="pc-tick" x="{LEFT - 6}" y="{gy + 4:.1f}" text-anchor="end">{tick(cap * frac)}</text>')
    # 每年一月一日畫一條直線，年份標在該年落在圖內那一段的中間
    for year in range(first.year, last.year + 1):
        jan, dec = date(year, 1, 1), date(year, 12, 31)
        if jan > first:
            parts.append(f'<line class="pc-grid" x1="{x(jan):.1f}" x2="{x(jan):.1f}" y1="{TOP}" y2="{TOP + plot_h}"/>')
        mid = (x(max(jan, first)) + x(min(dec, last))) / 2
        parts.append(f'<text class="pc-tick" x="{mid:.1f}" y="{height - 6}" text-anchor="middle">{year}</text>')
    for d, text in markers:
        mx = x(d)
        parts.append(f'<line class="pc-mark" x1="{mx:.1f}" x2="{mx:.1f}" y1="{TOP}" y2="{TOP + plot_h}"/>')
        parts.append(f'<text class="pc-note" x="{mx + 4:.1f}" y="{TOP + 56}">{escape(text)}</text>')
    pts = " ".join(f"{x(d):.1f},{y(v):.1f}" for d, v in points)
    parts.append(f'<g class="pc-marks pc-trace"><polyline class="pc-line pc-thin" points="{pts}"/></g>')
    if peak:
        # 放在第一段底色的左邊，曲線在那裡還在縱軸中段，上方是空的，手機上也不會跟事件的註記疊在一起
        px = x(max(bands[0][0], first)) - 6 if bands else W - RIGHT
        parts.append(f'<text class="pc-note pc-peak" x="{px:.1f}" y="{TOP + 24}" text-anchor="end">{escape(peak)}</text>')
    parts.append("</svg>")
    return Markup("".join(parts))


def share_bars(days: list[date], series: list[tuple[str, dict, str]], label: str) -> Markup:
    """每天的長條疊滿 100%，看各系列的占比變化。"""
    parts, x, y = _frame(days, 100, label)
    bar = _step(days) * 0.72
    parts.append('<g class="pc-marks pc-bars">')
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
    parts.append("</g></svg>")
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


def multiple(values: list, lo: float, hi: float, base: float | None = None,
             width: int = 120, height: int = 44) -> Markup:
    """小倍數圖：每個地區一張，全部用同一個刻度 lo 到 hi，起伏與高低可以直接比較。

    values 要對齊同一段日期，沒有資料的日子是 None，畫出來是缺口，晚加入觀測的地區從中間開始。
    超出刻度的值貼在邊上。base 畫一條虛線當參考，例如指數化之後的 100。"""
    span = (hi - lo) or 1
    step = width / max(len(values) - 1, 1)

    def y(v: float) -> float:
        return height - 2 - (min(max(v, lo), hi) - lo) / span * (height - 4)

    runs, run = [], []
    for i, v in enumerate(values + [None]):
        if v is None:
            if run:
                runs.append(run)
            run = []
        else:
            run.append((i * step, y(v)))
    if not runs:
        return Markup("")
    parts = [f'<svg class="pc-multi" viewBox="0 0 {width} {height}" preserveAspectRatio="none" aria-hidden="true">']
    if base is not None:
        parts.append(f'<line class="pc-base" x1="0" x2="{width}" y1="{y(base):.1f}" y2="{y(base):.1f}"/>')
    parts.append('<g class="pc-marks">')
    for run in runs:
        pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in run)
        if len(run) > 1:
            parts.append(f'<polygon points="{run[0][0]:.1f},{height} {pts} {run[-1][0]:.1f},{height}"/>'
                         f'<polyline points="{pts}"/>')
    parts.append("</g></svg>")
    return Markup("".join(parts))


def domain(series: list[list], base: float | None = None, floor: float | None = None,
           ceil: float | None = None) -> tuple[float, float]:
    """多張小倍數圖共用的刻度：涵蓋所有值，留一點邊，再用 floor、ceil 限制範圍。"""
    vals = [v for s in series for v in s if v is not None] + ([base] if base is not None else [])
    if not vals:
        return 0, 1
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.08 or 1
    lo, hi = lo - pad, hi + pad
    # 刻度取整到 10，圖下方寫得出簡單的範圍
    lo, hi = math.floor(lo / 10) * 10, math.ceil(hi / 10) * 10
    if floor is not None:
        lo = max(lo, floor)
    if ceil is not None:
        hi = min(hi, ceil)
    return lo, hi


SHADES = ["pc-s1", "pc-s2", "pc-s3", "pc-s4", "pc-s5"]
