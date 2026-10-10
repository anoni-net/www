"""產生 anoni.net 首頁與社群頁面的 clearnet 與 onion 兩份靜態產物。

    uv run build.py          # 產生 public/clearnet 與 public/onion
    uv run build.py --out DIR  # 產生到 DIR/clearnet 與 DIR/onion，m6 部署時用
    uv run build.py --check  # 產生到暫存目錄，再執行下方 check() 的檢查

頁面寫在 pages/<語系>/，社群動態寫在 updates/<語系>/，資料寫在 data/，兩個目標與三個語系的
差異寫在 site.toml，介面文字寫在 strings.toml。
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
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path

import markdown
from pymdownx.slugs import slugify
from pymdownx.emoji import to_alt, twemoji
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

import pulse

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
DATA = ROOT / "data"
ICONS = ROOT / "icons"
STATIC = ROOT / "static"
EXTRA = ROOT / "extra"
UPDATES = ROOT / "updates"
TEMPLATES = ROOT / "templates"
CACHE = ROOT / ".cache"

# 寫在 Markdown 裡的連結簡寫，建置時依語系展開：
#   /join/                → 本站的頁面，加上語系前綴
#   docs:tools/what-is-tor/ → 文件站同語系的頁面
#   news:about/           → 新聞導讀同語系的頁面
HREF = re.compile(r'(href|src)="([^"]*)"')
PLACEHOLDER = re.compile(r"<!--\s*(\w[\w-]*)\s*-->")
# 寫在 Markdown 原始 HTML 裡的圖示，例如 <span class="ic">ICON:upload-outline</span>
ICON_REF = re.compile(r"ICON:([a-z0-9-]+)")
# 從文件站搬過來的頁面，圖示寫成 <i data-icon="名稱"></i>（見 tools/import_from_docs.py）
PULSE_SLUG = "projects/pulse"
ICON_TAG = re.compile(r'<i data-icon="([a-z0-9-]+)"></i>')


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


_slug = slugify()


def doc_slug(text: str, sep: str) -> str:
    """跟文件站一樣的錨點。文件站的 emoji 是 SVG 標籤，產生錨點前就被剝掉，這裡的 emoji 是
    Unicode 字元，去掉之後會在開頭留下一個分隔符號（「📚 參加」變成「-參加」），修掉它。"""
    return _slug(text, sep).strip(sep)


def render_markdown(body: str) -> str:
    # 擴充與參數照文件站的 mkdocs.yml，從文件站搬過來的頁面才會有相同的結果。圖示不用
    # pymdownx.emoji，轉換工具把 :material-*: 改成 ICON:名稱，由 icon() 內嵌。
    md = markdown.Markdown(
        extensions=["abbr", "attr_list", "md_in_html", "admonition", "tables", "toc", "footnotes",
                    "pymdownx.details", "pymdownx.superfences", "pymdownx.tabbed", "pymdownx.tasklist",
                    "pymdownx.emoji"],
        extension_configs={
            # 錨點的寫法跟文件站一致（保留中文與大小寫）。從文件站搬過來的頁面，舊網址轉過來時
            # 瀏覽器會帶著 # 後面那段，兩邊一致才跳得到同一段。
            "toc": {"permalink": False, "slugify": doc_slug},
            "pymdownx.tabbed": {"alternate_style": True},
            "pymdownx.tasklist": {"custom_checkbox": True},
            # :books: 這類短碼換成 Unicode 字元，不載入 twemoji 的圖片
            "pymdownx.emoji": {"emoji_index": twemoji, "emoji_generator": to_alt},
        },
    )
    return md.convert(body)


@dataclass
class Post:
    """一篇社群動態。網址是 <語系前綴>/updates/YYYY/MM/<slug>/，跟文件站部落格的格式一樣。"""
    lang: str
    slug: str
    date: date
    meta: dict
    body: str
    path: str


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
        self.posts = {lang.code: self.load_posts(lang) for lang in self.langs}
        # Tor 中繼節點觀測：第一個國家是主頁，其他國家各一頁，路徑是 projects/pulse/<code>
        self.pulse_codes = [c["code"] for c in self.data.get("pulse", {}).get("countries", [])]
        self.pulse_slugs = [f"{PULSE_SLUG}/{c}" for c in self.pulse_codes[1:]] if PULSE_SLUG in self.slugs else []
        self._pulse = None

    def load_posts(self, lang: Lang) -> list[Post]:
        """社群動態不要求三個語系都有，只有正體中文的公告不會出現在其他語系的列表。"""
        posts = []
        for src in sorted((UPDATES / lang.code).glob("*.md")):
            where = src.relative_to(ROOT).as_posix()
            meta, body = split_front_matter(src.read_text(encoding="utf-8"), where)
            day = meta.get("date")
            if not isinstance(day, date):
                raise SystemExit(f"{where}：front matter 的 date 要寫成 YYYY-MM-DD")
            slug = meta.get("slug") or src.stem
            posts.append(Post(lang.code, slug, day, meta, body,
                              f"{lang.prefix}/updates/{day:%Y/%m}/{slug}/"))
        return sorted(posts, key=lambda p: p.date, reverse=True)

    def updates_for(self, lang: Lang) -> list[dict]:
        """動態列表：本站的新文章加上文件站舊的社群文章，由新到舊。"""
        items = [{"date": p.date, "title": p.meta["title"], "summary": p.meta["description"],
                  "href": p.path, "source": "www"} for p in self.posts[lang.code]]
        for old in self.data.get("docs_updates", {}).get("posts", []):
            if lang.code in old:
                items.append({"date": old["date"], "title": old[lang.code]["title"],
                              "summary": old[lang.code]["summary"],
                              "href": self.product_url("docs", lang, old[lang.code]["url"]),
                              "source": "docs"})
        return sorted(items, key=lambda i: i["date"], reverse=True)

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
        # pulse 每個國家各畫一次，在 build_pulse 裡另外處理
        names = [p.name.removeprefix("_block-").removesuffix(".html.j2")
                 for p in TEMPLATES.glob("_block-*.html.j2") if p.name != "_block-pulse.html.j2"]
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
            "updates": self.updates_for(lang),
            "feed_url": f"{lang.prefix}/updates/feed.xml",
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
                target=target, langs=self.langs, slugs=self.slugs + self.pulse_slugs, page_path=self.page_path,
                posts=[p for lang in self.langs for p in self.posts[lang.code]]), target)
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
            if slug == PULSE_SLUG:
                self.build_pulse(lang, target, out, meta, body, blocks, where)
                continue
            body_html = self.fill_blocks(render_markdown(body), blocks, where)
            body_html = ICON_REF.sub(lambda m: icon(m[1]), body_html)
            body_html = ICON_TAG.sub(lambda m: icon(m[1]), body_html)
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
        self.build_posts(lang, target, out)

    def pulse_data(self) -> dict:
        """各國的摘要，同一次建置只讀一次（clearnet 與 onion 共用）。"""
        if self._pulse is None:
            self._pulse = pulse.load(self.pulse_codes, self.data["pulse"]["days"], CACHE / "pulse")
        return self._pulse

    def build_pulse(self, lang: Lang, target: dict, out: Path, meta: dict, body: str,
                    blocks: dict, where: str) -> None:
        """Tor 中繼節點觀測：同一份 Markdown，每個國家各產生一頁，圖表各自畫。"""
        conf = self.data["pulse"]
        labels = conf["labels"]
        pick = lambda value: value[lang.code] if isinstance(value, dict) else value  # noqa: E731
        L = {k: pick(v).replace("{days}", str(conf["days"])).replace("{back}", str(conf["compare_days"]))
             for k, v in labels.items()}
        loaded = self.pulse_data()
        views = {c: pulse.view(loaded[c]["data"], labels, pick, conf["compare_days"]) if loaded[c]["data"] else None
                 for c in self.pulse_codes}

        def path(other: Lang, code: str) -> str:
            return self.page_path(other, PULSE_SLUG if code == self.pulse_codes[0] else f"{PULSE_SLUG}/{code}")

        countries = [{"code": c["code"], "name": pick(c["name"]), "href": path(lang, c["code"]),
                      "title_name": c.get("title_name", {}).get(lang.code, pick(c["name"])),
                      "running": views[c["code"]]["latest"]["running"] if views[c["code"]] and views[c["code"]]["latest"] else None,
                      "spark": pulse.sparkline(views[c["code"]]["running_series"]) if views[c["code"]] else ""}
                     for c in conf["countries"]]
        for country in countries:
            code = country["code"]
            block = self.env.get_template("_block-pulse.html.j2").render(
                **self.context(lang, target), L=L, v=views[code], stale=loaded[code]["stale"],
                country=country, countries=[{**c, "current": c["code"] == code} for c in countries])
            body_html = self.fill_blocks(render_markdown(body), {**blocks, "pulse": block}, where)
            body_html = ICON_REF.sub(lambda m: icon(m[1]), body_html)
            body_html = ICON_TAG.sub(lambda m: icon(m[1]), body_html)
            body_html = self.localize(body_html, lang)
            first = code == self.pulse_codes[0]
            # 導言寫的是整頁的主題，只放在主頁，各國子頁的標題已經寫明是哪個地區
            page = {
                **{k: v for k, v in meta.items() if first or k != "lead"},
                "title": meta["title"] if first else L["title_country"].replace("{name}", country["title_name"]),
                "slug": PULSE_SLUG,
                "section": "projects",
                "parent": "projects",
                "path": path(lang, code),
                "alternates": [(other, path(other, code)) for other in self.langs],
            }
            text = self.env.get_template(f"{meta.get('template', 'page')}.html.j2").render(
                **self.context(lang, target), page=page, body=Markup(body_html))
            self.write(out / page["path"].lstrip("/") / "index.html", text, target)

    def build_posts(self, lang: Lang, target: dict, out: Path) -> None:
        for post in self.posts[lang.code]:
            where = f"updates/{lang.code}/{post.slug}"
            body_html = ICON_TAG.sub(lambda m: icon(m[1]), render_markdown(post.body))
            body_html = self.localize(body_html, lang)
            # 其他語系有同一篇（slug 相同）就連過去，沒有就回到那個語系的動態列表
            alternates = []
            for other in self.langs:
                twin = next((p for p in self.posts[other.code] if p.slug == post.slug), None)
                alternates.append((other, twin.path if twin else self.page_path(other, "updates")))
            page = {
                **post.meta,
                "slug": f"updates/{post.slug}",
                "section": "updates",
                "parent": "updates",
                "path": post.path,
                "date": post.date,
                "alternates": alternates,
            }
            text = self.env.get_template("post.html.j2").render(
                **self.context(lang, target), page=page, body=Markup(body_html))
            self.write(out / post.path.lstrip("/") / "index.html", text, target)
        # RSS，本站的文章與文件站的舊文章一起列，最多 30 則
        items = []
        for item in self.updates_for(lang)[:30]:
            href = item["href"] if "://" in item["href"] else f"{target['base']}{item['href']}"
            pub = datetime(item["date"].year, item["date"].month, item["date"].day, tzinfo=timezone.utc)
            items.append({**item, "link": href, "pub": format_datetime(pub)})
        feed = self.env.get_template("feed.xml.j2").render(
            t=self.strings[lang.code], lang=lang, target=target, items=items,
            home=f"{target['base']}{self.page_path(lang, 'updates')}",
            self_url=f"{target['base']}{lang.prefix}/updates/feed.xml")
        self.write(out / lang.prefix.lstrip("/") / "updates" / "feed.xml", feed, target)

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
    import xml.etree.ElementTree as ET
    problems = []
    for out in outs:
        for feed in out.rglob("feed.xml"):
            try:
                ET.parse(feed)
            except ET.ParseError as err:
                problems.append(f"{out.name}/{feed.relative_to(out)}：RSS 不是合法的 XML（{err}）")
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
    posts = sum(len(p) for p in site.posts.values())
    print(f"檢查通過：{len(site.langs)} 個語系、{len(site.slugs)} 頁、{posts} 篇動態、clearnet 與 onion 兩份")
    return 0


if __name__ == "__main__":
    sys.exit(main())
