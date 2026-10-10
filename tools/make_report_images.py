"""產生觀測季報的分享圖（og:image）與電子報的 banner。

每一期季報一組圖，三個語系各一張 1200x630 的分享圖，加一張中英並列、1200x400 的電子報 banner。
左邊是季別與副標，右邊是觀測地區地圖，上色的地區取自那一期數字檔的 countries（季報比較的地區），
跟季報頁上的地圖一致。

圖不進版控。產生之後用 rsync 傳到 assets.anoni.net 背後的目錄，季報頁與社群動態的 front matter
用 og_image 寫完整網址，電子報的 campaign 在 images 寫同一個網址，寄送時才下載。檔名帶內容的
雜湊，重新產生之後網址跟著換，不會讀到 Cloudflare 上的舊圖。目的地只放在環境變數，不寫進公開的 repo：

    WWW_ASSETS_RSYNC=<主機>:<目錄>/reports uv run --with playwright tools/make_report_images.py 2026-q3

沒有設 WWW_ASSETS_RSYNC 時只產生到暫存目錄、印出路徑，不上傳。用無頭的 Chrome 把一段 HTML
截成 PNG，中文字型用系統的 Noto Sans CJK，再用 pngquant 壓一次（有安裝的話），每張約 40 KB。
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/usr/bin/google-chrome"
ASSETS_URL = "https://assets.anoni.net/reports"

# 品牌色，照 static/css/site.css 的 --brand-cyan-*
BG = "#003e57"       # cyan-900
OBS = "#00aeff"      # cyan-500
LAND = "#0d5675"     # 底色往亮一點，讓國界看得出來
EDGE = "#003e57"
SOFT = "#80d1ff"     # cyan-200

TEXT = {
    "zh-TW": ("anoni.net 觀測季報", "臺灣與亞洲 {n} 個地區的 Tor 中繼節點與 OONI 觀測", "zh-Hant", "Noto Sans CJK TC"),
    "zh-CN": ("anoni.net 观测季报", "台湾与亚洲 {n} 个地区的 Tor 中继节点与 OONI 观测", "zh-Hans", "Noto Sans CJK SC"),
    "en": ("anoni.net quarterly observation report",
           "Tor relays and OONI measurements in Taiwan and {m} other Asian regions", "en", "Noto Sans"),
}


def quarter_label(slug: str) -> str:
    year, q = slug.split("-")
    return f"{year} {q.upper()}"


def map_svg(observed: set[str], height: int) -> str:
    d = json.loads((ROOT / "data" / "region-map.json").read_text())
    w, h = d["width"], d["height"]
    parts = [f'<svg viewBox="0 0 {w} {h}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    for code, path in d["countries"].items():
        if code not in observed:
            parts.append(f'<path d="{path}" fill="{LAND}" stroke="{EDGE}" stroke-width="0.8"/>')
    for code in observed:
        if code in d["points"]:
            x, y = d["points"][code]
            parts.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{OBS}" stroke="{EDGE}" stroke-width="1.5"/>')
        elif code in d["countries"]:
            parts.append(f'<path d="{d["countries"][code]}" fill="{OBS}" stroke="{EDGE}" stroke-width="0.8"/>')
    parts.append("</svg>")
    return "".join(parts)


def logo() -> str:
    svg = (ROOT / "static" / "logo-tonal.svg").read_text()
    return svg.replace("<svg", '<svg width="56" height="56"', 1)


def og_html(lang: str, quarter: str, observed: set[str]) -> str:
    label, sub, html_lang, font = TEXT[lang]
    n = len(observed)
    sub = sub.format(n=n, m=n - 1)
    return f"""<!doctype html><html lang="{html_lang}"><meta charset="utf-8"><style>
body {{ margin: 0; }}
.card {{ width: 1200px; height: 630px; background: {BG}; color: #fff; position: relative; overflow: hidden;
        font-family: "{font}", "Noto Sans CJK TC", sans-serif; }}
.map {{ position: absolute; right: 0; top: 70px; }}
.fade {{ position: absolute; inset: 0; background: linear-gradient(90deg, {BG} 38%, transparent 52%),
        linear-gradient(180deg, {BG} 9%, transparent 22%); }}
.text {{ position: absolute; left: 72px; top: 72px; width: 500px; }}
.brand {{ display: flex; align-items: center; gap: 16px; font-size: 30px; color: {SOFT}; font-weight: 500; }}
.q {{ margin-top: 70px; font-size: 128px; font-weight: 800; line-height: 1; letter-spacing: -2px; }}
.sub {{ margin-top: 36px; width: 470px; font-size: 34px; line-height: 1.45; font-weight: 500; }}
.url {{ position: absolute; left: 72px; bottom: 56px; font-size: 26px; color: {SOFT}; }}
:lang(en) .sub {{ font-size: 30px; }}
</style><div class="card">
<div class="map">{map_svg(observed, 510)}</div><div class="fade"></div>
<div class="text"><div class="brand">{logo()}<span>{escape(label)}</span></div>
<div class="q">{escape(quarter)}</div><div class="sub">{escape(sub)}</div></div>
<div class="url">anoni.net/projects/reports</div>
</div></html>"""


def banner_html(quarter: str, observed: set[str]) -> str:
    n = len(observed)
    zh = TEXT["zh-TW"][1].format(n=n)
    en = TEXT["en"][1].format(m=n - 1)
    return f"""<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><style>
body {{ margin: 0; }}
.card {{ width: 1200px; height: 400px; background: {BG}; color: #fff; position: relative; overflow: hidden;
        font-family: "Noto Sans CJK TC", sans-serif; }}
.map {{ position: absolute; right: -10px; top: 20px; }}
.fade {{ position: absolute; inset: 0; background: linear-gradient(90deg, {BG} 52%, transparent 66%),
        linear-gradient(180deg, {BG} 4%, transparent 14%); }}
.text {{ position: absolute; left: 64px; top: 52px; width: 700px; }}
.brand {{ display: flex; align-items: center; gap: 14px; font-size: 22px; color: {SOFT}; font-weight: 500; white-space: nowrap; }}
.q {{ margin-top: 28px; font-size: 96px; font-weight: 800; line-height: 1; letter-spacing: -1px; }}
.sub {{ margin-top: 22px; font-size: 27px; line-height: 1.4; font-weight: 500; }}
.en {{ margin-top: 6px; font-size: 20px; color: {SOFT}; font-family: "Noto Sans", sans-serif; }}
</style><div class="card">
<div class="map">{map_svg(observed, 380)}</div><div class="fade"></div>
<div class="text"><div class="brand">{logo()}<span>anoni.net 觀測季報 · Quarterly observation report</span></div>
<div class="q">{escape(quarter)}</div><div class="sub">{escape(zh)}</div><div class="en">{escape(en)}</div></div>
</div></html>"""


def shoot(page, html: str, out: Path, width: int, height: int) -> None:
    page.set_viewport_size({"width": width, "height": height})
    page.set_content(html, wait_until="load")
    page.locator(".card").screenshot(path=str(out))
    if shutil.which("pngquant"):
        subprocess.run(["pngquant", "--force", "--skip-if-larger", "--quality", "80-95",
                        "--output", str(out), str(out)], check=False)


def hashed(path: Path) -> Path:
    """檔名加上內容雜湊的前 8 碼，圖改了網址就換。"""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
    target = path.with_name(f"{path.stem}-{digest}{path.suffix}")
    path.rename(target)
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("quarter", help="季度，例如 2026-q3")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    data = json.loads((ROOT / "data" / "reports" / f"{args.quarter}.json").read_text())
    regions = json.loads((ROOT / "data" / "region-map.json").read_text())
    observed = {c for c in data["countries"] if c in regions["countries"] or c in regions["points"]}
    quarter = quarter_label(args.quarter)
    out_dir = Path(tempfile.mkdtemp(prefix="report-images-"))
    files = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, args=["--password-store=basic"])
        page = browser.new_page(device_scale_factor=1)
        for lang in TEXT:
            out = out_dir / f"{args.quarter}-og-{lang.lower()}.png"
            shoot(page, og_html(lang, quarter, observed), out, 1200, 630)
            files[f"og_image ({lang})"] = hashed(out)
        out = out_dir / f"{args.quarter}-banner.png"
        shoot(page, banner_html(quarter, observed), out, 1200, 400)
        files["電子報 banner"] = hashed(out)
        browser.close()

    dest = os.environ.get("WWW_ASSETS_RSYNC")
    if dest:
        subprocess.run(["rsync", "-a", "--chmod=F644", "--mkpath", *map(str, files.values()), dest.rstrip("/") + "/"],
                       check=True)
    for label, path in files.items():
        where = f"{ASSETS_URL}/{path.name}" if dest else str(path)
        print(f"{label}: {where}（{path.stat().st_size:,} bytes）")
    if not dest:
        print("沒有設 WWW_ASSETS_RSYNC，只產生到暫存目錄，沒有上傳")
    return 0


if __name__ == "__main__":
    sys.exit(main())
