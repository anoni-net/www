"""產生 anoni.net 首頁與社群頁面的 clearnet 與 onion 兩份靜態產物。

    uv run build.py          # 產生 public/clearnet 與 public/onion
    uv run build.py --out DIR  # 產生到 DIR/clearnet 與 DIR/onion，m6 部署時用
    uv run build.py --check  # 產生到暫存目錄，再執行下方 check() 的檢查

頁面寫在 pages/<語系>/，資料寫在 data/，兩個目標與三個語系的差異寫在 site.toml，
介面文字寫在 strings.toml。
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from pathlib import Path

import markdown
from pymdownx.slugs import slugify
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
DATA = ROOT / "data"
ICONS = ROOT / "icons"
STATIC = ROOT / "static"
EXTRA = ROOT / "extra"
TEMPLATES = ROOT / "templates"

# 寫在 Markdown 裡的連結簡寫，建置時依語系展開：
#   /join/                → 本站的頁面，加上語系前綴
#   docs:tools/what-is-tor/ → 文件站同語系的頁面
#   news:about/           → 新聞導讀同語系的頁面
HREF = re.compile(r'(href|src)="([^"]*)"')
PLACEHOLDER = re.compile(r"<!--\s*(\w[\w-]*)\s*-->")
# 寫在 Markdown 原始 HTML 裡的圖示，例如 <span class="ic">ICON:upload-outline</span>
ICON_REF = re.compile(r"ICON:([a-z0-9-]+)")


@dataclass(frozen=True)
class Lang:
    code: str      # 目錄名稱與 strings.toml 的鍵，例如 zh-TW
    html: str      # <html lang>
    prefix: str    # 網址前綴，正體中文是空字串，例如 /en
    label: str     # 語言切換上顯示的名稱


def load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def split_front_matter(text: str, where: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise SystemExit(f"{where}：缺少 front matter")
    _, head, body = text.split("---\n", 2)
    meta = yaml.safe_load(head) or {}
    for key in ("title", "description"):
        if not meta.get(key):
            raise SystemExit(f"{where}：front matter 缺少 {key}")
    return meta, body


def page_slugs(root: Path) -> list[str]:
    """一個語系目錄底下的頁面。pages/zh-TW/about/governance.md 是 about/governance，
    輸出到 /about/governance/。"""
    return sorted(p.relative_to(root).with_suffix("").as_posix() for p in root.rglob("*.md"))


def icon(name: str, cls: str = "i") -> Markup:
    svg = (ICONS / f"{name}.svg").read_text(encoding="utf-8").strip()
    return Markup(svg.replace("<svg ", f'<svg class="{cls}" aria-hidden="true" ', 1))


def logo(cls: str = "logo") -> Markup:
    svg = (STATIC / "logo-tonal.svg").read_text(encoding="utf-8").strip()
    return Markup(svg.replace("<svg ", f'<svg class="{cls}" aria-hidden="true" ', 1))


def render_markdown(body: str) -> str:
    md = markdown.Markdown(
        extensions=["attr_list", "tables", "fenced_code", "admonition", "md_in_html", "toc"],
        # 錨點的寫法跟文件站一致（保留中文與大小寫）。從文件站搬過來的頁面，舊網址轉過來時
        # 瀏覽器會帶著 # 後面那段，兩邊一致才跳得到同一段。
        extension_configs={"toc": {"permalink": False, "slugify": slugify()}},
    )
    return md.convert(body)


class Site:
    def __init__(self) -> None:
        self.config = load_toml(ROOT / "site.toml")
        self.strings = load_toml(ROOT / "strings.toml")
        self.langs = [Lang(**lang) for lang in self.config["languages"]]
        self.data = {p.stem: load_toml(p) for p in sorted(DATA.glob("*.toml"))}
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )
        self.env.globals["icon"] = icon
        self.env.globals["logo"] = logo
        self.slugs = page_slugs(PAGES / self.langs[0].code)

    # 網址

    def section_of(self, slug: str) -> str:
        """頁面所屬的區塊，給導覽列標示目前位置。about/governance 屬於 about。"""
        return slug.split("/", 1)[0]

    def page_path(self, lang: Lang, slug: str) -> str:
        """本站頁面的路徑，首頁是語系的根目錄。"""
        tail = "" if slug == "index" else f"{slug}/"
        return f"{lang.prefix}/{tail}"

    def product_url(self, product: str, lang: Lang, path: str = "") -> str:
        """文件站與新聞導讀的完整網址，一律寫 clearnet，onion 版本在最後一步改寫。"""
        return f"https://anoni.net/{product}{lang.prefix}/{path}"

    def localize_href(self, href: str, lang: Lang) -> str:
        for product in ("docs", "news"):
            if href.startswith(f"{product}:"):
                return self.product_url(product, lang, href[len(product) + 1:])
        # 本站頁面加上語系前綴。帶副檔名的是根目錄的檔案（例如 PGP 公鑰），已經帶語系前綴的
        # （模板用 page_url 產生的、語言切換指向其他語系的）也不加。
        if href.startswith("/") and not href.startswith("//"):
            path, _, frag = href.partition("#")
            prefixed = any(lg.prefix and path.startswith(f"{lg.prefix}/") for lg in self.langs)
            if not prefixed and "." not in path.rsplit("/", 1)[-1]:
                return f"{lang.prefix}{path}" + (f"#{frag}" if frag else "")
        return href

    def localize(self, text: str, lang: Lang) -> str:
        return HREF.sub(lambda m: f'{m[1]}="{self.localize_href(html.unescape(m[2]), lang)}"', text)

    # 頁面裡的區塊，Markdown 用 <!-- 名稱 --> 標出位置

    def blocks(self, lang: Lang, target: dict) -> dict[str, str]:
        ctx = self.context(lang, target)
        names = [p.name.removeprefix("_block-").removesuffix(".html.j2")
                 for p in TEMPLATES.glob("_block-*.html.j2")]
        return {n: self.env.get_template(f"_block-{n}.html.j2").render(**ctx) for n in names}

    def fill_blocks(self, body_html: str, blocks: dict[str, str], where: str) -> str:
        def repl(m: re.Match) -> str:
            name = m[1]
            if name not in blocks:
                raise SystemExit(f"{where}：沒有名為 {name} 的區塊（templates/_block-{name}.html.j2）")
            return blocks[name]
        return PLACEHOLDER.sub(repl, body_html)

    def context(self, lang: Lang, target: dict) -> dict:
        return {
            "lang": lang,
            "langs": self.langs,
            "t": self.strings[lang.code],
            "target": target,
            "onion_host": self.config["onion_host"],
            "data": self.data,
            "nav": self.config["nav"],
            "docs_url": lambda path="": self.product_url("docs", lang, path),
            "news_url": lambda path="": self.product_url("news", lang, path),
            "page_url": lambda slug: self.page_path(lang, slug),
            "pick": lambda value: value[lang.code] if isinstance(value, dict) else value,
            "service_url": lambda svc: self.service_url(svc, target),
            "pgp_key": (STATIC / "B7DF84305C7911D90D59A66061F66CF36EE386D4.asc").read_text(encoding="utf-8").strip(),
        }

    def service_url(self, svc: dict, target: dict) -> str:
        if target["name"] == "onion" and svc.get("onion"):
            return f"http://{svc['host'].split('.')[0]}.{self.config['onion_host']}/"
        return f"https://{svc['host']}/"

    # 輸出

    def build(self, out_root: Path) -> list[Path]:
        outs = []
        for name, target in self.config["targets"].items():
            target = {**target, "name": name}
            out = out_root / name
            if out.exists():
                shutil.rmtree(out)
            shutil.copytree(STATIC, out)
            for lang in self.langs:
                self.build_lang(lang, target, out)
            self.build_404(target, out)
            # 只有部分目標需要的檔案，例如 clearnet 的 llms.txt
            for name in target.get("extra", []):
                self.write(out / name, (EXTRA / name).read_text(encoding="utf-8"), target)
            self.write(out / "robots.txt", self.env.get_template("robots.txt.j2").render(
                target=target, langs=self.langs, slugs=self.slugs, page_path=self.page_path), target)
            self.write(out / "sitemap.xml", self.env.get_template("sitemap.xml.j2").render(
                target=target, langs=self.langs, slugs=self.slugs, page_path=self.page_path), target)
            outs.append(out)
        return outs

    def build_lang(self, lang: Lang, target: dict, out: Path) -> None:
        blocks = self.blocks(lang, target)
        for slug in self.slugs:
            src = PAGES / lang.code / f"{slug}.md"
            where = src.relative_to(ROOT).as_posix()
            if not src.exists():
                raise SystemExit(f"{where}：缺少這個語系的頁面")
            meta, body = split_front_matter(src.read_text(encoding="utf-8"), where)
            body_html = self.fill_blocks(render_markdown(body), blocks, where)
            body_html = ICON_REF.sub(lambda m: icon(m[1]), body_html)
            # 只有 Markdown 內文用連結簡寫，模板產生的連結（導覽列、語言切換）已經是完整路徑，
            # 整頁套用會把正體中文沒有前綴的 /about/ 誤加成目前語系的 /en/about/。
            body_html = self.localize(body_html, lang)
            template = meta.get("template", "page")
            page = {
                **meta,
                "slug": slug,
                "section": self.section_of(slug),
                "parent": self.section_of(slug) if "/" in slug else None,
                "path": self.page_path(lang, slug),
                "alternates": [(other, self.page_path(other, slug)) for other in self.langs],
            }
            text = self.env.get_template(f"{template}.html.j2").render(
                **self.context(lang, target), page=page, body=Markup(body_html))
            self.write(out / page["path"].lstrip("/") / "index.html", text, target)

    def build_404(self, target: dict, out: Path) -> None:
        """一份 404 頁放在根目錄，三種語言寫在同一頁，nginx 的 error_page 指到它。"""
        lang = self.langs[0]
        page = {
            "title": self.strings[lang.code]["not_found_title"],
            "description": self.strings[lang.code]["not_found_title"],
            "slug": "404",
            "section": "404",
            "parent": None,
            "path": "/404.html",
            "alternates": [(other, self.page_path(other, "index")) for other in self.langs],
        }
        messages = [(other, self.strings[other.code]) for other in self.langs]
        text = self.env.get_template("404.html.j2").render(
            **self.context(lang, target), page=page, messages=messages,
            home=lambda other: self.page_path(other, "index"))
        self.write(out / "404.html", text, target)

    def write(self, dest: Path, text: str, target: dict) -> None:
        for old, new in target.get("rewrite", {}).items():
            text = text.replace(old, new.replace("{onion}", self.config["onion_host"]))
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")


def check(site: Site, outs: list[Path]) -> list[str]:
    problems = []
    for lang in site.langs[1:]:
        have = page_slugs(PAGES / lang.code)
        if have != site.slugs:
            problems.append(f"pages/{lang.code} 的頁面跟 {site.langs[0].code} 不一致：{have}")
    for out in outs:
        files = {p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file()}
        for page in sorted(out.rglob("*.html")):
            rel = page.relative_to(out).as_posix()
            text = page.read_text(encoding="utf-8")
            for leftover in ("docs:", "news:", "<!--"):
                if f'"{leftover}' in text or (leftover == "<!--" and PLACEHOLDER.search(text)):
                    problems.append(f"{out.name}/{rel}：沒有展開的 {leftover}")
            for href in re.findall(r'(?:href|src)="(/[^"#?]*)', text):
                if href.startswith("//"):
                    continue
                want = href.lstrip("/")
                if not (want in files or f"{want}index.html" in files or (want == "" and "index.html" in files)):
                    problems.append(f"{out.name}/{rel}：站內連結找不到 {href}")
            # 語言切換的每個連結都要指到該語系的同一頁
            for href, want in re.findall(r'<a href="([^"]*)" hreflang="([^"]*)"', text):
                dest = out / href.lstrip("/") / "index.html"
                got = re.search(r'<html lang="([^"]*)"', dest.read_text(encoding="utf-8"))[1] if dest.exists() else None
                if got != want:
                    problems.append(f"{out.name}/{rel}：語言切換 {want} 指到 {href}，那一頁是 {got}")
            if out.name == "onion":
                for host in site.config["targets"]["onion"].get("rewrite", {}):
                    if host in text:
                        problems.append(f"{out.name}/{rel}：onion 版本還有 {host}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="產生到暫存目錄並檢查，不寫入 public/")
    parser.add_argument("--out", type=Path, default=ROOT / "public", help="輸出目錄，預設是 public/")
    args = parser.parse_args()
    site = Site()
    if not args.check:
        for out in site.build(args.out.resolve()):
            print(f"產生 {out}/")
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        problems = check(site, site.build(Path(tmp)))
    if problems:
        print("\n".join(problems))
        return 1
    print(f"檢查通過：{len(site.langs)} 個語系、{len(site.slugs)} 頁、clearnet 與 onion 兩份")
    return 0


if __name__ == "__main__":
    sys.exit(main())
