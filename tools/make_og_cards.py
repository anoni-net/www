"""產生每一頁的社群預覽卡片（og:image），上傳到 assets.anoni.net，寫進 og_cards.toml。

    uv run --with playwright tools/make_og_cards.py --dry-run
    WWW_OG_RSYNC=<主機>:<目錄> uv run --with playwright tools/make_og_cards.py [頁面路徑 ...]

先完整建置一次，收集每一頁該有的卡片（規則在 og_cards.py 開頭），沒給頁面路徑時只處理還沒有卡片、
或內容改過讓卡片過期的頁面，給了路徑（例如 /en/projects/pulse/）就重做那幾頁。卡片用
templates/og-card.html.j2 截成 1200x630 的 PNG，中文字型用系統的 Noto Sans CJK，再用 pngquant
壓一次（有安裝的話）。

--dry-run 只產圖，放在 .cache/og-cards/，另外產生 .cache/og-cards/preview.html 把卡片排在一起看。
拿掉 --dry-run 之後用 rsync 傳到 $WWW_OG_RSYNC（assets.anoni.net 的 www/og/ 背後的目錄），確認網址
回 200，才寫進 og_cards.toml。目的地只放在環境變數，不寫進公開的 repo。卡片不進版控，repo 裡只有登記表。
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

from markupsafe import Markup

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build  # noqa: E402
import og_cards  # noqa: E402
import region_map  # noqa: E402

CACHE = ROOT / ".cache" / "og-cards"
CHROME = os.environ.get("CHROME", "/usr/bin/google-chrome")
MAX_BYTES = 150_000
# 照 static/css/site.css 的 --brand-cyan-*，跟季報的分享圖同一組
COLORS = {"land": "#0d5675", "edge": "#003e57", "obs": "#00aeff", "cur": "#ffffff"}


def logo(size: int) -> Markup:
    svg = (ROOT / "static" / "logo-tonal.svg").read_text()
    return Markup(svg.replace("<svg", f'<svg width="{size}" height="{size}"', 1))


def card_html(site: "build.Site", data: dict) -> str:
    rmap = data.get("map")
    svg = region_map.plain_svg(ROOT, rmap["observed"], rmap["current"], 510, COLORS) if rmap else None
    return site.env.get_template("og-card.html.j2").render(c=data, map=svg, logo=logo(52), mark=logo(560))


def shoot(page, html: str, out: Path) -> None:
    page.set_content(html, wait_until="load")
    out.parent.mkdir(parents=True, exist_ok=True)
    page.locator(".card").screenshot(path=str(out))
    if shutil.which("pngquant"):
        subprocess.run(["pngquant", "--force", "--skip-if-larger", "--quality", "80-95",
                        "--output", str(out), str(out)], check=False)
    if out.stat().st_size > MAX_BYTES:
        raise SystemExit(f"{out.name}：{out.stat().st_size:,} bytes，超過 {MAX_BYTES:,}")


def preview(made: list[tuple[str, Path]]) -> Path:
    rows = "\n".join(f'<figure><img src="{path.relative_to(CACHE)}" width="600" height="315" alt="">'
                     f"<figcaption>{key}</figcaption></figure>" for key, path in made)
    page = CACHE / "preview.html"
    page.write_text(f"""<!DOCTYPE html><meta charset="utf-8"><title>預覽卡片</title>
<style>body{{font-family:sans-serif;display:flex;flex-wrap:wrap;gap:24px;padding:24px;background:#eee}}
figure{{margin:0}}img{{display:block;box-shadow:0 1px 4px #0004}}figcaption{{font-size:13px;margin-top:6px}}</style>
{rows}
""", encoding="utf-8")
    return page


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", help="只重做這幾頁（頁面路徑，例如 /en/projects/），沒給就處理缺的與過期的")
    ap.add_argument("--dry-run", action="store_true", help="只產圖與預覽頁，不上傳也不改登記表")
    args = ap.parse_args()

    site = build.Site()
    with tempfile.TemporaryDirectory() as tmp:
        site.build(Path(tmp))
    registry = og_cards.load()
    unknown = [p for p in args.paths if p not in site.cards]
    if unknown:
        raise SystemExit(f"找不到這幾頁：{unknown}")
    todo = [site.cards[p] for p in args.paths] if args.paths else \
        [e for e in site.cards.values() if og_cards.url(e, registry) is None]
    if not todo:
        print(f"{len(site.cards)} 頁都有最新的卡片")
        return 0

    from playwright.sync_api import sync_playwright

    made = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME, args=["--password-store=basic"])
        page = browser.new_page(device_scale_factor=1, viewport={"width": 1200, "height": 630})
        for key, rel, data in todo:
            out = CACHE / rel
            shoot(page, card_html(site, data), out)
            made.append((key, out))
            print(f"{key} → {rel}（{out.stat().st_size // 1024} KB）")
        browser.close()
    print(f"預覽：{preview(made)}")
    if args.dry_run:
        return 0

    dest = os.environ.get("WWW_OG_RSYNC")
    if not dest:
        print("沒有設定 WWW_OG_RSYNC，卡片沒有上傳，登記表沒有改動")
        return 1
    subprocess.run(["rsync", "-a", "--chmod=F644", "--mkpath", *(str(out) for _, out in made),
                    dest.rstrip("/") + "/"], check=True)
    for key, rel, _ in todo:
        url = og_cards.ASSETS + rel
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "anoni-www-og-cards"})
        with urllib.request.urlopen(request, timeout=30) as response:
            if response.status != 200:
                raise SystemExit(f"{url} 回 {response.status}，登記表沒有改動")
        registry[key] = rel
    og_cards.write(registry)
    print(f"已上傳 {len(made)} 張，寫進 {og_cards.REGISTRY.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
