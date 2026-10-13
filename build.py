"""產生 anoni.net 首頁與社群頁面的 clearnet 與 onion 兩份靜態產物。

    uv run build.py          # 產生 public/clearnet 與 public/onion
    uv run build.py --out DIR  # 產生到 DIR/clearnet 與 DIR/onion，m6 部署時用
    uv run build.py --check  # 產生到暫存目錄，再執行下方 check() 的檢查

頁面寫在 pages/<語系>/，社群動態寫在 updates/<語系>/，資料寫在 data/，兩個目標與三個語系的
差異寫在 site.toml，介面文字寫在 strings.toml。
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
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

import asn_coverage
import charts
import diagrams
import latest
import og_cards
import pulse
import region_map
import tor_users
import reports

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
DATA = ROOT / "data"
ICONS = ROOT / "icons"
STATIC = ROOT / "static"
EXTRA = ROOT / "extra"
UPDATES = ROOT / "updates"
REPORTS = ROOT / "reports"
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
ICON_TAG = re.compile(r'<i data-icon="([a-z0-9-]+)"></i>')
# 每個地區各一頁的觀測頁：Markdown 只有一份，資料與地區清單在 data/<名稱>.toml
PULSE_SLUG = "projects/pulse"
ASN_SLUG = "projects/asn-coverage"
REPORTS_SLUG = "projects/reports"
# 社群動態的標籤：新增（專案或服務上線）、活動、更新（工作進度）。觀點、立場與經驗不加標籤。
# 顏色照品牌素材頁的「公告 tag」
UPDATE_KINDS = ("new", "event", "update")
# 季報各期的圖表，名稱對應 templates/_report.html.j2 的 macro，Markdown 裡寫成 <!-- rq-relays-chart -->
REPORT_BLOCKS = ("relays_stats", "relays_chart", "churn", "upgrade", "asn", "density", "ooni_stats",
                 "types", "networks", "gaps", "changes", "ooni_daily", "run", "glossary")


@dataclass(frozen=True)
class Lang:
    code: str      # 目錄名稱與 strings.toml 的鍵，例如 zh-TW
    html: str      # <html lang>
    prefix: str    # 網址前綴，正體中文是空字串，例如 /en
    label: str     # 語言切換上顯示的名稱
    og: str        # og:locale，例如 zh_TW


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


def asset(rel: str) -> str:
    """static/ 底下檔案的網址，後面接內容的雜湊當版本號，跟新聞導讀的 static_version 同一個做法。
    內容改了網址就跟著變，瀏覽器與 Cloudflare 會當成新檔案去抓，部署後不必為了樣式清快取。"""
    return f"/{rel}?v={hashlib.sha256((STATIC / rel).read_bytes()).hexdigest()[:10]}"


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
    return stack_tables(md.convert(body))


TABLE = re.compile(r"<table>.*?</table>", re.S)
TH = re.compile(r"<th[^>]*>(.*?)</th>", re.S)
TR = re.compile(r"<tr>.*?</tr>", re.S)
TD = re.compile(r"<td([^>]*)>(.*?)</td>", re.S)
TAG = re.compile(r"<[^>]+>")
# 寫作風格規範的對照表，欄名只有一個打叉或打勾的圖示，卡片上改用符號標出
ICON_NAME = re.compile(r'data-icon="([^"]+)"')
ICON_LABEL = {"close": "✗", "check": "✓"}
# 欄名的寬度（中日韓文字算 1，其他字元算 0.6）都小於這個值時，手機上把欄名放在內容左邊；
# 否則不顯示欄名，第三欄以後改成灰色小字。「提案管道」是 4，「Proposal channel」是 9.6，
# 「與匿名網路社群的關聯」是 10
LABEL_MAX = 10


def label_width(text: str) -> float:
    return sum(1 if ord(c) > 0x2E80 else 0.6 for c in text)


def stack_tables(body: str) -> str:
    """三欄以上的表格在手機上擠到一欄只剩三、四個字，改成一列一塊，桌機維持表格。

    欄名短的（stack--label）把欄名放在每一格左邊，像「提案管道　GitHub PR」；欄名長的
    （stack--plain）不顯示欄名，第一格當標題、第二格是內文、之後的格子用灰色小字。
    每一格帶上欄名（data-label），內容包一層 span，CSS 的 grid 才不會把文字與連結拆成兩格。"""
    def one(m: re.Match) -> str:
        table = m[0]
        labels = [html.unescape(TAG.sub("", h)).strip() or ICON_LABEL.get(next(iter(ICON_NAME.findall(h)), ""), "")
                  for h in TH.findall(table)]
        if len(labels) < 3:
            return table
        width = max(label_width(t) for t in labels[1:])
        attrs = (f'class="stack stack--label" style="--lw: {max(width, 1.5):.1f}"' if width < LABEL_MAX
                 else 'class="stack stack--plain"')

        def row(r: re.Match) -> str:
            cells = iter(labels)

            def cell(c: re.Match) -> str:
                label = html.escape(next(cells, ""), quote=True)
                inner = c[2] if not c[2].strip() else f'<span class="v">{c[2]}</span>'
                return f'<td{c[1]} data-label="{label}">{inner}</td>'

            return TD.sub(cell, r[0])

        head, sep, rest = table.partition("</thead>")
        return (head + sep + TR.sub(row, rest)).replace("<table>", f"<table {attrs}>", 1)

    return TABLE.sub(one, body)


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
        self.env.globals["asset"] = asset
        self.slugs = page_slugs(PAGES / self.langs[0].code)
        self.posts = {lang.code: self.load_posts(lang) for lang in self.langs}
        # Tor 中繼節點觀測：第一個國家是主頁，其他國家各一頁，路徑是 projects/pulse/<code>
        self.pulse_codes = [c["code"] for c in self.data.get("pulse", {}).get("countries", [])]
        self.pulse_slugs = [f"{PULSE_SLUG}/{c}" for c in self.pulse_codes[1:]] if PULSE_SLUG in self.slugs else []
        self._pulse = None
        self._tor_users = None
        # OONI 觀測涵蓋率：同樣第一個地區是主頁，路徑是 projects/asn-coverage/<code>
        self.asn_codes = [c["code"] for c in self.data.get("asn-coverage", {}).get("countries", [])]
        self.asn_slugs = [f"{ASN_SLUG}/{c}" for c in self.asn_codes[1:]] if ASN_SLUG in self.slugs else []
        self._asn = None
        self._apps = None
        self.reports = {lang.code: self.load_reports(lang) for lang in self.langs}
        self._report_views = {}
        # 每一頁的預覽卡片，見 og_cards.py。cards 收集這次建置每一頁該有的卡片，給 tools/make_og_cards.py 用
        self.og_registry = og_cards.load()
        self.cards: dict[str, tuple[str, str, dict]] = {}

    def load_posts(self, lang: Lang) -> list[Post]:
        """社群動態不要求三個語系都有，只有正體中文的公告不會出現在其他語系的列表。"""
        posts = []
        for src in sorted((UPDATES / lang.code).glob("*.md")):
            where = src.relative_to(ROOT).as_posix()
            meta, body = split_front_matter(src.read_text(encoding="utf-8"), where)
            day = meta.get("date")
            if not isinstance(day, date):
                raise SystemExit(f"{where}：front matter 的 date 要寫成 YYYY-MM-DD")
            if meta.get("kind") not in (None, *UPDATE_KINDS):
                raise SystemExit(f"{where}：kind 只能是 {'、'.join(UPDATE_KINDS)}，觀點與經驗類的文章不寫")
            slug = meta.get("slug") or src.stem
            posts.append(Post(lang.code, slug, day, meta, body,
                              f"{lang.prefix}/updates/{day:%Y/%m}/{slug}/"))
        return sorted(posts, key=lambda p: p.date, reverse=True)

    def load_reports(self, lang: Lang) -> list[Post]:
        """觀測季報，檔名是季度，例如 2026-q3.md。每一期都要三個語系，check() 會擋缺的。"""
        items = []
        for src in sorted((REPORTS / lang.code).glob("*.md")):
            where = src.relative_to(ROOT).as_posix()
            meta, body = split_front_matter(src.read_text(encoding="utf-8"), where)
            if not isinstance(meta.get("date"), date):
                raise SystemExit(f"{where}：front matter 的 date 要寫成 YYYY-MM-DD")
            items.append(Post(lang.code, src.stem, meta["date"], meta, body,
                              f"{lang.prefix}/{REPORTS_SLUG}/{src.stem}/"))
        return sorted(items, key=lambda r: r.slug, reverse=True)

    def report_items(self, lang: Lang, target: dict) -> list[dict]:
        """季報列表。這個語系還沒有的季報，列出正體中文版並標明語言。正體中文的網址沒有語系
        前綴，寫成站內路徑會被 localize 加上這個語系的前綴，所以寫完整網址（onion 版在最後一步改寫）。"""
        labels = self.data.get("reports", {}).get("labels", {})
        mine = {r.slug for r in self.reports[lang.code]}
        items = [{"title": r.meta["title"], "summary": r.meta["description"], "href": r.path, "date": r.date,
                  "note": ""} for r in self.reports[lang.code]]
        for r in self.reports[self.langs[0].code]:
            if r.slug not in mine:
                items.append({"title": r.meta["title"], "summary": r.meta["description"],
                              "href": f"{target['base']}{r.path}",
                              "date": r.date, "note": labels.get("only_zh_tw", {}).get(lang.code, "")})
        return sorted(items, key=lambda i: i["href"].rstrip("/").rsplit("/", 1)[-1], reverse=True)

    def updates_for(self, lang: Lang) -> list[dict]:
        """動態列表，由新到舊。文件站部落格的舊社群文章 2026-10 全部搬到 updates/（#42）。"""
        items = [{"date": p.date, "title": p.meta["title"], "summary": p.meta["description"],
                  "href": p.path, "kind": p.meta.get("kind")} for p in self.posts[lang.code]]
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
        # 觀測頁的區塊每個地區各畫一次，在 build_regions 裡另外處理
        regional = {"_block-pulse.html.j2", "_block-asn-coverage.html.j2"}
        names = [p.name.removeprefix("_block-").removesuffix(".html.j2")
                 for p in TEMPLATES.glob("_block-*.html.j2") if p.name not in regional]
        blocks = {n: self.env.get_template(f"_block-{n}.html.j2").render(**ctx) for n in names}
        return {**blocks, **self.diagram_blocks(lang, ctx)}

    def diagram_blocks(self, lang: Lang, ctx: dict) -> dict[str, str]:
        """關於頁的示意圖，Markdown 寫 <!-- diagram-community --> 這類標記，內容在 data/diagrams.toml。"""
        conf, pick = self.data["diagrams"], ctx["pick"]

        def link(item: dict) -> str:
            if "page" in item:
                return self.page_path(lang, item["page"])
            if "docs" in item:
                return self.product_url("docs", lang, item["docs"])
            # 社群動態要三個語系都有，連結會加上語系前綴，連不到其他語系的版本
            post = next((p for p in self.posts[lang.code] if p.slug == item["post"]), None)
            if not post:
                raise SystemExit(f"data/diagrams.toml：{lang.code} 沒有社群動態 {item['post']}，改連三個語系都有的頁面")
            return post.path

        return {
            "diagram-community": diagrams.community(
                conf["community"], self.data["topics"]["topics"], pick, ctx["page_url"],
                lambda name: (ICONS / f"{name}.svg").read_text(encoding="utf-8").strip(),
                (STATIC / "logo-tonal.svg").read_text(encoding="utf-8").strip()),
            "diagram-regions": diagrams.regions(ROOT, conf["regions"], pick),
            "diagram-history": diagrams.history(conf["history"], pick, link),
        }

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
            "product_url": lambda product, other, path="": self.product_url(product, other, path),
            "latest": lambda product, count: latest.load(product, lang.prefix, CACHE / "latest", count),
            "page_url": lambda slug: self.page_path(lang, slug),
            "pick": lambda value: value[lang.code] if isinstance(value, dict) else value,
            "service_url": lambda svc: self.service_url(svc, target),
            "updates": self.updates_for(lang),
            "report_items": self.report_items(lang, target),
            "feed_url": f"{lang.prefix}/updates/feed.xml",
            "jsonld": lambda page: self.jsonld(lang, target, page),
            "pgp_key": (STATIC / "B7DF84305C7911D90D59A66061F66CF36EE386D4.asc").read_text(encoding="utf-8").strip(),
        }

    def jsonld(self, lang: Lang, target: dict, page: dict) -> Markup:
        """結構化資料（schema.org），每頁都有 WebSite 與 Organization，子頁加麵包屑，
        社群動態與季報加文章，兩個觀測頁的主頁加 Dataset。"""
        base = target["base"]
        t = self.strings[lang.code]
        url = f"{base}{page['path']}"
        org = {"@type": "Organization", "@id": f"{base}/#org", "name": t["site_name"],
               "alternateName": "anoni.net", "url": f"{base}/", "email": "whisper@anoni.net",
               "logo": f"{base}/og.png",
               "sameAs": ["https://github.com/anoni-net", self.product_url("docs", lang), self.product_url("news", lang)]}
        graph = [{"@type": "WebSite", "@id": f"{base}/#website", "name": t["site_name"], "alternateName": "anoni.net",
                  "url": f"{base}{self.page_path(lang, 'index')}", "inLanguage": lang.html, "publisher": {"@id": org["@id"]}},
                 org]
        if page["slug"] != "index":
            crumbs = [(t["site_name"], self.page_path(lang, "index"))]
            if page.get("parent"):
                crumbs.append((t[f"nav_{page['parent']}"], self.page_path(lang, page["parent"])))
            crumbs += [c for c in page.get("trail", []) if c[1] != crumbs[-1][1]]
            crumbs.append((page["title"], page["path"]))
            graph.append({"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": i, "name": name, "item": f"{base}{path}"}
                for i, (name, path) in enumerate(crumbs, 1)]})
        image = page.get("og_image") or "/og.png"
        image = image if "://" in image else f"{base}{image}"
        if page.get("date"):
            graph.append({"@type": "BlogPosting" if page["section"] == "updates" else "Article",
                          "headline": page["title"], "description": page["description"], "image": image,
                          "datePublished": page["date"].isoformat(), "inLanguage": lang.html, "url": url,
                          "mainEntityOfPage": url, "author": {"@id": org["@id"]}, "publisher": {"@id": org["@id"]}})
        if page.get("dataset"):
            d = page["dataset"]
            # Google 要求 Dataset 的 description 至少 50 個字元，中文的 description 不夠長時接上導言
            desc = page["description"]
            if len(desc) < 50 and page.get("lead"):
                desc += (" " if lang.code == "en" else "") + page["lead"]
            item = {"@type": "Dataset", "name": page["title"], "description": desc, "url": url,
                    "inLanguage": lang.html, "isAccessibleForFree": True, "creator": {"@id": org["@id"]},
                    "spatialCoverage": [{"@type": "Place", "name": n} for n in d["regions"]],
                    "isBasedOn": d["sources"]}
            if d.get("download"):
                item["distribution"] = [{"@type": "DataDownload", "encodingFormat": "application/json",
                                         "contentUrl": d["download"]}]
            graph.append(item)
        text = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
        # JSON 放在 <script> 裡，</ 要跳脫，內容才不會提早結束標籤
        return Markup(text.replace("</", "<\\/"))

    def service_url(self, svc: dict, target: dict) -> str:
        if target["name"] == "onion" and svc.get("onion"):
            return f"http://{svc['host'].split('.')[0]}.{self.config['onion_host']}/"
        return f"https://{svc['host']}/"

    def with_card(self, lang: Lang, page: dict, label: list[str], sub: str | None = None,
                  rmap: dict | None = None) -> dict:
        """沒有指定 og_image 的頁面換成這一頁的預覽卡片，登記過而且內容相符的才用，否則維持 og.png。"""
        if page.get("og_image"):
            return page
        font = {"zh-TW": "Noto Sans CJK TC", "zh-CN": "Noto Sans CJK SC"}.get(lang.code, "Noto Sans")
        data = {"html_lang": lang.html, "font": font, "label": label, "title": page["title"],
                "sub": page.get("tagline") or page.get("lead") or page.get("description", "") if sub is None else sub,
                "site_url": "anoni.net" + page["path"].rstrip("/"), "map": rmap}
        entry = og_cards.card(lang.code, page["path"], data)
        self.cards[entry[0]] = entry
        found = og_cards.url(entry, self.og_registry)
        return {**page, "og_image": found} if found else page

    def section_label(self, lang: Lang, section: str) -> list[str]:
        label = self.strings[lang.code].get(f"nav_{section}")
        return [label] if label else []

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
                target=target, langs=self.langs, slugs=self.slugs + self.pulse_slugs + self.asn_slugs, page_path=self.page_path,
                posts=[p for lang in self.langs for p in self.posts[lang.code] + self.reports[lang.code]]), target)
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
            if slug == ASN_SLUG:
                self.build_asn(lang, target, out, meta, body, blocks, where)
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
            # 三大主題的頁面，頁首放一個主題色的標籤
            topic = next((tp for tp in self.data.get("topics", {}).get("topics", []) if tp["page"] == slug), None)
            if topic:
                page["topic"] = topic
            page = self.with_card(lang, page, self.section_label(lang, page["section"]))
            text = self.env.get_template(f"{template}.html.j2").render(
                **self.context(lang, target), page=page, body=Markup(body_html))
            self.write(out / page["path"].lstrip("/") / "index.html", text, target)
        self.build_posts(lang, target, out)
        self.build_reports(lang, target, out, blocks)

    def pulse_data(self) -> dict:
        """各國的摘要，同一次建置只讀一次（clearnet 與 onion 共用）。"""
        if self._pulse is None:
            self._pulse = pulse.load(self.pulse_codes, self.data["pulse"]["days"], CACHE / "pulse")
        return self._pulse

    def region_labels(self, conf: dict, lang: Lang) -> tuple[dict, callable]:
        pick = lambda value: value[lang.code] if isinstance(value, dict) else value  # noqa: E731
        L = {k: pick(v).replace("{days}", str(conf["days"])).replace("{back}", str(conf["compare_days"]))
             for k, v in conf["labels"].items()}
        return L, pick

    def build_regions(self, lang: Lang, target: dict, out: Path, meta: dict, body: str, blocks: dict,
                      where: str, slug: str, name: str, countries: list[dict], render,
                      dataset: dict | None = None) -> None:
        """同一份 Markdown，每個地區各產生一頁。countries 每一項至少要有 code、title_name，
        render(country, countries) 回傳那個地區的區塊 HTML，放進 <!-- name --> 的位置。"""
        L, _ = self.region_labels(self.data[name], lang)
        first_code = countries[0]["code"]

        def path(other: Lang, code: str) -> str:
            return self.page_path(other, slug if code == first_code else f"{slug}/{code}")

        countries = [{**c, "href": path(lang, c["code"])} for c in countries]
        for country in countries:
            code = country["code"]
            block = render(country, [{**c, "current": c["code"] == code} for c in countries])
            body_html = self.fill_blocks(render_markdown(body), {**blocks, name: block}, where)
            body_html = ICON_REF.sub(lambda m: icon(m[1]), body_html)
            body_html = ICON_TAG.sub(lambda m: icon(m[1]), body_html)
            body_html = self.localize(body_html, lang)
            first = code == first_code
            # 導言寫的是整頁的主題，只放在主頁，各地區子頁的標題已經寫明是哪個地區
            page = {
                **{k: v for k, v in meta.items() if first or k != "lead"},
                "title": meta["title"] if first else L["title_country"].replace("{name}", country["title_name"]),
                # 各地區子頁的 description 寫出地區，搜尋結果才分得出是哪一頁
                "description": meta["description"] if first else L["desc_country"].replace("{name}", country["title_name"]),
                "trail": [] if first else [(meta["title"], path(lang, first_code))],
                "dataset": dataset if first else None,
                "slug": slug,
                "section": "projects",
                "parent": "projects",
                "path": path(lang, code),
                "alternates": [(other, path(other, code)) for other in self.langs],
            }
            # 卡片的地圖跟頁首的一樣，目前這一頁的地區另外標出來
            # 地圖只有亞洲，德國、荷蘭、美國這些畫不出來的地區不放地圖
            page = self.with_card(lang, page, self.section_label(lang, "projects") + [meta["title"]],
                                  None if first else meta.get("description", ""),
                                  {"observed": [c["code"] for c in countries], "current": code}
                                  if region_map.drawable(ROOT, code) else None)
            text = self.env.get_template(f"{meta.get('template', 'page')}.html.j2").render(
                **self.context(lang, target), page=page, body=Markup(body_html))
            self.write(out / page["path"].lstrip("/") / "index.html", text, target)

    def pulse_data(self) -> dict:
        """各國的摘要，同一次建置只讀一次（clearnet 與 onion 共用）。"""
        if self._pulse is None:
            self._pulse = pulse.load(self.pulse_codes, self.data["pulse"]["days"], CACHE / "pulse")
        return self._pulse

    def tor_users_data(self) -> dict:
        """Tor Metrics 的使用者估計，同一次建置只讀一次。"""
        if self._tor_users is None:
            refs = [r["code"] for r in self.data["pulse"].get("use_refs", [])]
            self._tor_users = tor_users.load(self.pulse_codes + refs, self.data["pulse"]["days"], CACHE / "tor-users")
        return self._tor_users

    def build_pulse(self, lang: Lang, target: dict, out: Path, meta: dict, body: str,
                    blocks: dict, where: str) -> None:
        """Tor 中繼節點觀測：每個國家各一頁，圖表各自畫。"""
        conf = self.data["pulse"]
        L, pick = self.region_labels(conf, lang)
        loaded = self.pulse_data()
        views = {c: pulse.view(loaded[c]["data"], conf["labels"], pick, conf["compare_days"]) if loaded[c]["data"] else None
                 for c in self.pulse_codes}
        users_raw = self.tor_users_data()
        world = users_raw["all"]["data"]
        users = {c: tor_users.view(users_raw[c]["data"], world, conf["labels"], pick, conf["compare_days"])
                 if users_raw[c]["data"] else None for c in self.pulse_codes}
        # 各地區比較的小倍數圖：對齊同一段日期，以各地區第一天的數量為 100，全部用同一個刻度
        aligned = charts.align({c: v["running_by_day"] for c, v in views.items() if v})
        indexed = {}
        for code, vals in aligned.items():
            first = next((x for x in vals if x), None)
            indexed[code] = [x / first * 100 if x is not None and first else None for x in vals]
        lo, hi = charts.domain(list(indexed.values()), base=100, floor=0, ceil=200)
        multi_scale = L["multi_scale"].replace("{lo}", f"{lo:g}").replace("{hi}", f"{hi:g}")

        def change(code: str) -> str:
            """第一天到最後一天的變化。資料不到一週的地區（剛加入觀測）不寫，兩三天的變化沒有意義。"""
            vals = [x for x in indexed.get(code, []) if x is not None]
            if len(vals) < 7:
                return ""
            last = vals[-1]
            d = round(last - 100)
            return f"{'+' if d > 0 else ''}{d}%"

        countries = []
        for c in conf["countries"]:
            v, u = views[c["code"]], users[c["code"]]
            countries.append({
                "code": c["code"], "name": pick(c["name"]),
                "title_name": c.get("title_name", {}).get(lang.code, pick(c["name"])),
                "running": v["latest"]["running"] if v and v["latest"] else None,
                "multi": charts.multiple(indexed[c["code"]], lo, hi, 100) if c["code"] in indexed else "",
                "change": change(c["code"]),
                "weight": tor_users.pct(v["weight"]) if v and v["weight"] is not None else "–",
                "users": u["users_text"] if u else "–",
                "bridge": tor_users.pct(u["bridge_pct"]) if u else "–",
            })

        # 比較表最後的參照地區，只有使用者估計
        use_refs = []
        for r in conf.get("use_refs", []):
            u = tor_users.view(users_raw[r["code"]]["data"], world, conf["labels"], pick, conf["compare_days"]) \
                if users_raw[r["code"]]["data"] else None
            use_refs.append({"name": pick(r["name"]), "users": u["users_text"] if u else "–",
                             "bridge": tor_users.pct(u["bridge_pct"]) if u else "–"})

        refs = {r["code"]: pick(r["name"]) for r in conf.get("use_refs", [])}

        steps = conf["map_steps"]
        levels = {c["code"]: (region_map.level(c["running"], steps),
                              f'{L["map_scale"]} {c["running"]:,}' if c["running"] is not None else L["map_na"])
                  for c in countries}

        def render(country: dict, countries: list[dict]) -> str:
            code = country["code"]
            rmap = region_map.svg(ROOT, {c["code"]: (c["name"], c["href"]) for c in countries}, refs, code,
                                  L["map_label"], levels=levels)
            return self.env.get_template("_block-pulse.html.j2").render(rmap=rmap,
                scale=region_map.scale(steps), map_na=any(lv == 0 for lv, _ in levels.values()),
                multi_scale=multi_scale,
                **self.context(lang, target), L=L, v=views[code], stale=loaded[code]["stale"],
                u=users[code], u_stale=users_raw[code]["stale"] or users_raw["all"]["stale"],
                pct=tor_users.pct, country=country, countries=countries, use_refs=use_refs,
                flag_desc={k: pick(v) for k, v in conf.get("flag_desc", {}).items()})

        # 主頁標成 Dataset，資料可以從 Pulse 的 API 下載
        dataset = {"regions": [c["name"] for c in countries],
                   "sources": ["https://metrics.torproject.org/onionoo.html", "https://metrics.torproject.org/"],
                   "download": f"{self.config['targets']['clearnet']['base']}/api/summary?country={self.pulse_codes[0]}&days={conf['days']}"}
        self.build_regions(lang, target, out, meta, body, blocks, where, PULSE_SLUG, "pulse", countries, render, dataset)

    def asn_data(self) -> dict:
        if self._asn is None:
            self._asn = asn_coverage.load(self.asn_codes, self.data["asn-coverage"]["days"], CACHE / "asn-coverage")
        return self._asn

    def apps_data(self) -> dict:
        """通訊 App 的測試，一個 App 一次查完所有國家，同一次建置只讀一次。"""
        if self._apps is None:
            conf = self.data["asn-coverage"]["apps"]
            # 跟卡片與表格同一段時間（compare_days），頁面上的 {back} 才對得上
            self._apps = asn_coverage.load_apps([t["test"] for t in conf["tests"]],
                                                self.data["asn-coverage"]["compare_days"], CACHE / "asn-coverage")
        return self._apps

    def build_asn(self, lang: Lang, target: dict, out: Path, meta: dict, body: str,
                  blocks: dict, where: str) -> None:
        """OONI 觀測涵蓋率：每個地區各一頁。"""
        conf = self.data["asn-coverage"]
        L, pick = self.region_labels(conf, lang)
        loaded = self.asn_data()
        views = {}
        for c in self.asn_codes:
            data = loaded["countries"][c]["data"]
            views[c] = asn_coverage.view(c, data, loaded["names"], conf["labels"], pick,
                                         conf["compare_days"]) if data else None
        apps = self.apps_data()
        tests = conf["apps"]["tests"]
        # 各地區比較的小倍數圖：對齊同一段日期，全部用同一個刻度
        aligned = charts.align({c: v["coverage_by_day"] for c, v in views.items() if v and v["latest"]})
        lo, hi = charts.domain(list(aligned.values()), floor=0, ceil=100)
        multi_scale = L["multi_scale"].replace("{lo}", f"{lo:g}").replace("{hi}", f"{hi:g}")
        countries = []
        for c in conf["countries"]:
            v = views[c["code"]]
            ok = v and v["latest"]
            countries.append({
                "code": c["code"], "name": pick(c["name"]),
                "title_name": c.get("title_name", {}).get(lang.code, pick(c["name"])),
                "coverage": v["coverage"] if ok else None,
                "stable": v["stable"] if ok else None,
                "multi": charts.multiple(aligned[c["code"]], lo, hi) if ok else "",
                "apps": asn_coverage.apps_view(c["code"], apps, tests, pick),
            })
        # App 比較表另外放幾個沒有自己頁面的參照地區
        app_refs = [{"name": pick(r["name"]), "apps": asn_coverage.apps_view(r["code"], apps, tests, pick)}
                    for r in conf["apps"].get("regions", [])]

        map_refs = {r["code"]: pick(r["name"]) for r in conf["apps"].get("regions", [])}

        steps = conf["map_steps"]
        levels = {c["code"]: (region_map.level(c["coverage"], steps),
                              f'{L["map_scale"]} {c["coverage"]:.1f}%' if c["coverage"] is not None else L["map_na"])
                  for c in countries}

        def render(country: dict, countries: list[dict]) -> str:
            rmap = region_map.svg(ROOT, {c["code"]: (c["name"], c["href"]) for c in countries}, map_refs,
                                  country["code"], L["map_label"], levels=levels)
            return self.env.get_template("_block-asn-coverage.html.j2").render(rmap=rmap,
                scale=region_map.scale(steps, "%"), map_na=any(lv == 0 for lv, _ in levels.values()),
                multi_scale=multi_scale,
                **self.context(lang, target), L=L, v=views[country["code"]],
                stale=loaded["countries"][country["code"]]["stale"], country=country, countries=countries,
                tests=tests, app_refs=app_refs, apps_stale=apps["stale"], app_min=asn_coverage.APP_MIN)

        dataset = {"regions": [c["name"] for c in countries],
                   "sources": ["https://api.ooni.io/", "https://stats.labs.apnic.net/aspop/"], "download": None}
        self.build_regions(lang, target, out, meta, body, blocks, where, ASN_SLUG, "asn-coverage", countries, render, dataset)

    def region_map_figure(self, lang: Lang, codes: list[str] | None = None, note: str | None = None) -> str:
        """文章與季報裡的 <!-- region-map -->，點下去開那個地區的觀測頁。

        codes 沒給時是兩個觀測頁目前的地區加上參照地區（社群動態用）。給了的時候（季報）那幾個地區
        用主色，是那一期比較的地區，跟當時的數字一致。目前觀測、但那一期還沒比較的地區用淺色，
        讀者才看得到社群關注的完整範圍，也分得出這一期的數字涵蓋哪些地區。"""
        pick = lambda value: value[lang.code] if isinstance(value, dict) else value  # noqa: E731
        pulse_conf, asn_conf = self.data["pulse"], self.data["asn-coverage"]
        L = {k: pick(v) for k, v in pulse_conf["labels"].items()}
        first = pulse_conf["countries"][0]["code"]
        observed = {c["code"]: (pick(c["name"]), self.page_path(lang, PULSE_SLUG if c["code"] == first
                                                                 else f"{PULSE_SLUG}/{c['code']}"))
                    for c in pulse_conf["countries"]}
        for c in asn_conf["countries"]:
            observed.setdefault(c["code"], (pick(c["name"]), self.page_path(lang, f"{ASN_SLUG}/{c['code']}")))
        refs = {r["code"]: pick(r["name"]) for r in pulse_conf.get("use_refs", []) + asn_conf["apps"].get("regions", [])}
        later = {}
        legend_obs = L["map_obs"]
        if codes is not None:
            later = {c: v for c, v in observed.items() if c not in codes}
            observed = {c: observed[c] for c in codes if c in observed}
            refs = {}
            R = {k: pick(v) for k, v in self.data["reports"]["labels"].items()}
            legend_obs = R["map_cmp"]
        svg = region_map.svg(ROOT, observed, refs, None, L["map_label"], later)
        legend = f'<span><i class="sw rm-sw-obs"></i>{legend_obs}</span>'
        if later:
            legend += f'<span><i class="sw rm-sw-later"></i>{R["map_later"]}</span>'
        if refs:
            legend += f'<span><i class="sw rm-sw-ref"></i>{L["map_ref_post"]}</span>'
        return (f'<figure class="rmap-fig">{svg}<figcaption><span class="lg">{legend}</span>'
                f'{note or L["map_note_post"]}</figcaption></figure>')

    def build_posts(self, lang: Lang, target: dict, out: Path) -> None:
        for post in self.posts[lang.code]:
            where = f"updates/{lang.code}/{post.slug}"
            body_html = ICON_TAG.sub(lambda m: icon(m[1]), render_markdown(post.body))
            if "<!-- region-map -->" in body_html:
                body_html = body_html.replace("<!-- region-map -->", self.region_map_figure(lang))
            body_html = self.localize(body_html, lang)
            # 其他語系有同一篇（slug 相同）就連過去，沒有就回到那個語系的動態列表
            alternates, hreflang = [], []
            for other in self.langs:
                twin = next((p for p in self.posts[other.code] if p.slug == post.slug), None)
                alternates.append((other, twin.path if twin else self.page_path(other, "updates")))
                if twin:
                    hreflang.append((other, twin.path))
            page = {
                **post.meta,
                "slug": f"updates/{post.slug}",
                "section": "updates",
                "parent": "updates",
                "path": post.path,
                "date": post.date,
                "alternates": alternates,
                # 語言切換在沒有翻譯時回到動態列表，hreflang 只列真的有翻譯的版本
                "hreflang": hreflang,
            }
            page = self.with_card(lang, page, self.section_label(lang, "updates") + [post.date.isoformat()],
                                  post.meta.get("description", ""))
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

    def build_reports(self, lang: Lang, target: dict, out: Path, blocks: dict) -> None:
        """每一期季報一頁，圖表從 data/reports/<季度>.json 畫，同一期的數字三個語系共用。"""
        conf = self.data.get("reports", {})
        labels = conf.get("labels", {})
        pick = lambda value: value[lang.code] if isinstance(value, dict) else value  # noqa: E731
        L = {k: pick(v) for k, v in labels.items()}
        cname = {c["code"]: pick(c["name"]) for c in self.data["pulse"]["countries"]}
        # 名詞說明的反引號排成 code，其餘照字面輸出
        glossary = [{"term": pick(g["term"]),
                     "desc": Markup(re.sub(r"`([^`]+)`", r"<code>\1</code>", str(html.escape(pick(g["desc"])))))}
                    for g in conf.get("glossary", [])]
        for rep in self.reports[lang.code]:
            where = f"reports/{lang.code}/{rep.slug}.md"
            data = reports.load(ROOT, rep.slug)
            v = reports.view(ROOT, data, labels, pick, data["names"])
            module = self.env.get_template("_report.html.j2").make_module(
                {**self.context(lang, target), "v": v, "L": L, "cname": cname, "cc": data["ooni"]["cc"],
                 "G": glossary})
            parts = {f"rq-{n.replace('_', '-')}": str(getattr(module, n)()) for n in REPORT_BLOCKS}
            # 季報的地圖只上色那一期比較的地區，之後新增的地區不算進去
            parts["region-map"] = self.region_map_figure(lang, data["countries"], L.get("map_note"))
            body_html = self.fill_blocks(render_markdown(rep.body), {**blocks, **parts}, where)
            body_html = ICON_REF.sub(lambda m: icon(m[1]), body_html)
            body_html = self.localize(body_html, lang)
            alternates, hreflang = [], []
            for other in self.langs:
                twin = next((r for r in self.reports[other.code] if r.slug == rep.slug), None)
                alternates.append((other, twin.path if twin else self.page_path(other, REPORTS_SLUG)))
                if twin:
                    hreflang.append((other, twin.path))
            page = {
                **rep.meta,
                "slug": f"{REPORTS_SLUG}/{rep.slug}",
                "section": "projects",
                "parent": "projects",
                "path": rep.path,
                "date": rep.date,
                "since": v["since"],
                "until": v["until"],
                "alternates": alternates,
                "hreflang": hreflang,
                "crumb": L.get("nav", ""),
                "trail": [(L.get("nav", ""), self.page_path(lang, REPORTS_SLUG))],
            }
            text = self.env.get_template("report.html.j2").render(
                **self.context(lang, target), page=page, body=Markup(body_html))
            self.write(out / rep.path.lstrip("/") / "index.html", text, target)

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
    # 觀測季報每一期都要三個語系（社群動態可以只有正體中文，季報不行）
    for rep in site.reports[site.langs[0].code]:
        for lang in site.langs[1:]:
            if not any(r.slug == rep.slug for r in site.reports[lang.code]):
                problems.append(f"reports/{lang.code}/{rep.slug}.md：季報要三個語系都有，這個語系還沒有")
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
    # 卡片要上傳到圖片主機，CI 做不到，所以缺卡片只提示、不算失敗，那幾頁先用 og.png
    missing = [key for key, entry in site.cards.items() if og_cards.url(entry, site.og_registry) is None]
    if missing:
        print(f"預覽卡片：{len(missing)} 頁還沒有或已經過期，用 og.png，"
              f"執行 tools/make_og_cards.py 補上（例如 {missing[0]}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
