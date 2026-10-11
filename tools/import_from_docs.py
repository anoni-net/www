"""把文件站（anoni-net/docs）的頁面搬到本站，以及產生舊網址的 nginx 對照表。

    uv run tools/import_from_docs.py --import about/governance join/roadmap-2026
    uv run tools/import_from_docs.py --import-all     # docs_moved.toml 裡 import = true 的全部
    uv run tools/import_from_docs.py --nginx          # 重新產生 tools/nginx-docs-moved.conf
    uv run tools/import_from_docs.py --updates        # 從 tools/docs_updates.toml 產生 data/docs_updates.toml
    WWW_UPDATES_RSYNC=<主機>:<目錄> uv run tools/import_from_docs.py --import-post move-to-anoni-net.md

讀的是文件站的 git（預設 ../anoni-net-docs 的 origin/main），不是工作目錄，所以本機
有沒有切到別的分支都不影響。搬遷對照寫在 tools/docs_moved.toml。

轉換只處理機械性的部分：front matter 只留 title 與 description，拿掉第一個 # 標題
（本站的模板用 title 產生），拿掉 {target="_blank"}，站內連結依目標改寫。

Material 的圖示（:material-*:、:octicons-*: 等）改成 <i data-icon="名稱"></i>，建置時
內嵌 SVG，用到的 SVG 從文件站的 mkdocs-material 套件複製到 icons/。用空標籤而不是文字
佔位，是因為標題裡的佔位文字會被算進錨點。admonition 與折疊區塊的標題是純文字，
那裡的圖示直接拿掉。.md-button 改成本站的 .btn，議程表的彩色標籤改成單色的 .tag。
轉完要人工看一次，遇到這支不處理的寫法會印出警告。

--import-post 把文件站部落格的社群文章搬成 updates/<語系>/<slug>.md（名單與分組在
tools/docs_updates.toml，搬過的列在 moved）。標題取 H1，日期只取發布日，依組別帶上 kind，
拿掉 <!-- more -->。文件站 repo 裡的圖片上傳到 assets.anoni.net 的 updates/，檔名帶內容雜湊，
內文改成新網址，圖不進本站的版控。上傳目的地只放在環境變數 WWW_UPDATES_RSYNC，沒有設時
只產生到 .cache/updates-images/，頁面上的圖會是 404。分享圖不搬，由 tools/make_og_cards.py
重新產生，原本就在 assets.anoni.net 的照用。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
import tomllib
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MOVED = ROOT / "tools" / "docs_moved.toml"
NGINX = ROOT / "tools" / "nginx-docs-moved.conf"
# 文件站的 clone。主 clone 旁邊就是 anoni-net-docs，在 .claude/worktrees/ 底下的 worktree 則要回到
# 工作區根目錄找，兩種都找不到時用 --docs 指定。
DEFAULT_DOCS = next((p for p in (ROOT.parent / "anoni-net-docs",
                                 *(a / "anoni-net-docs" for a in ROOT.parents if a.name == ".claude" for a in [a.parent]))
                     if (p / ".git").exists()), ROOT.parent / "anoni-net-docs")
ONION = "anoninetru5tflukgfaehun7q6khowgmymcff3gtk5oyesqazhmfxtyd.onion"

# 文件站的語系目錄與網址前綴，跟本站的 site.toml 一致
LANGS = {"zh-TW": "", "zh-CN": "/zh-cn", "en": "/en"}

LINK = re.compile(r"(\]\()([^)\s]+)(\))")
ICON = re.compile(r":((?:material|octicons|simple|fontawesome)-[a-z0-9-]+):(\{[^}]*\})?")
TITLE_LINE = re.compile(r'^(\s*(?:!!!|\?\?\?\+?)\s+[a-z-]+\s+")(.*)("\s*)$', re.M)
UNSUPPORTED = re.compile(r'--8<--|```vegalite|\sstyle="[^"]*"', re.M)
UPDATES_LIST = ROOT / "tools" / "docs_updates.toml"
IMAGE_CACHE = ROOT / ".cache" / "updates-images"
ASSETS_UPDATES = "https://assets.anoni.net/updates/"
IMAGE = re.compile(r'(!\[[^\]]*\]\(|<img\b[^>]*\bsrc="|<a\b[^>]*\bhref=")([^)"\s]+)')
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
ICON_DIR = ROOT / "icons"
# 文件站的 mkdocs-material 隨附的圖示，跟文件站用同一套
MATERIAL_ICONS: list[Path] = []

# 議程表的彩色標籤。頂層網站只用 cyan 一個色相，類型用實心、場地用線框、強調文字用粗體
STYLE_SPANS = [
    (re.compile(r'<span style="background-color:\s*(?:green|purple|dodgerblue|#[0-9a-f]{3,6});\s*color:\s*#fff(?:fff)?;[^"]*">', re.I), '<span class="tag tag--solid">'),
    (re.compile(r'<span style="background-color:\s*#fefefe;[^"]*">', re.I), '<span class="tag">'),
    (re.compile(r'<span style="color:\s*(?:green|purple|dodgerblue|#[0-9a-f]{3,6});\s*font-weight:\s*bold;?">', re.I), '<span class="tag-text">'),
    (re.compile(r'<span class="sess-tag sess-tag--[a-z]+">'), '<span class="tag">'),
    # 籌備頁待辦清單的狀態標籤（公告、報名等）寫成帶顏色的 code，顏色拿掉
    (re.compile(r'<code style="[^"]*">'), '<code>'),
]


def icon_file(name: str) -> tuple[str, Path | None]:
    """:material-x: 對應的本站圖示名稱與文件站裡的原始 SVG。material 沿用原名，其他套件加前綴。"""
    base = MATERIAL_ICONS[0] if MATERIAL_ICONS else None
    if name.startswith("material-"):
        stem, rel = name[len("material-"):], f"material/{name[len('material-'):]}.svg"
    elif name.startswith("fontawesome-"):
        _, style, rest = name.split("-", 2)
        stem, rel = name, f"fontawesome/{style}/{rest}.svg"
    else:
        kind, rest = name.split("-", 1)
        stem, rel = name, f"{kind}/{rest}.svg"
    return stem, (base / rel) if base else None


def use_icon(name: str) -> str:
    stem, src = icon_file(name)
    dest = ICON_DIR / f"{stem}.svg"
    if not dest.exists():
        if not src or not src.exists():
            print(f"  ! 找不到圖示 {name}", file=sys.stderr)
            return ""
        dest.write_bytes(src.read_bytes())
        print(f"  + 複製圖示 {dest.relative_to(ROOT)}")
    return stem


def load_moved() -> list[dict]:
    with open(MOVED, "rb") as f:
        return tomllib.load(f)["moved"]


def docs_url_path(src: str) -> str:
    """文件站原始檔對應的網址路徑（不含 /docs 與語系前綴）。community/index.md 是 community/。"""
    if src == "index.md":
        return ""
    if src.endswith("/index.md"):
        return src[: -len("index.md")]
    return src[: -len(".md")] + "/"


def git_show(docs: Path, ref: str, path: str) -> str | None:
    result = subprocess.run(["git", "-C", str(docs), "show", f"{ref}:{path}"],
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def convert(text: str, src: str, lang: str, moved: list[dict], where: str, blog_url=None,
            posts: dict[str, str] | None = None) -> str:
    """posts 是已經搬到本站的部落格文章：文件站的原始檔路徑（blog/posts/x.md）或網址路徑
    （blog/YYYY/MM/slug/）對到本站的 /updates/YYYY/MM/slug/，連過去的連結改成本站。"""
    posts = posts or {}
    _, head, body = text.split("---\n", 2)
    meta = yaml.safe_load(head) or {}
    front = {k: meta[k] for k in ("title", "description") if k in meta}

    # 本站的模板用 title 產生 <h1>，原稿的第一個 # 標題拿掉
    body = re.sub(r"\A\s*# [^\n]*\n", "", body, count=1)
    # admonition 與折疊區塊的標題是純文字，圖示拿掉
    body = TITLE_LINE.sub(lambda m: m[1] + ICON.sub("", m[2]).strip() + m[3], body)
    body = ICON.sub(lambda m: f'<i data-icon="{use_icon(m[1])}"></i>', body)
    body = re.sub(r"\{[^}]*\.md-button[^}]*\}",
                  lambda m: "{ .btn .solid }" if "md-button--primary" in m[0] else "{ .btn }", body)
    for pattern, repl_tag in STYLE_SPANS:
        body = pattern.sub(repl_tag, body)
    body = body.replace('{target="_blank"}', "").replace("{ target=\"_blank\" }", "")
    # 文件站截圖的框線寫在 style 裡，本站改用 class
    body = re.sub(r'(!\[[^\]]*\]\([^)]+\))\{\s*style="[^"]*"\s*\}', r"\1{ .shot }", body)
    # 屬性清單裡夾在其他屬性中間的圓角（例如 { align=left width="30%" style="border-radius: 5px;" }）
    body = re.sub(r'\{([^{}\n]*?)\s*style="border-radius:\s*[\d.]+(?:px|rem)?;?\s*"([^{}\n]*)\}',
                  lambda m: "{ " + " ".join(x for x in (m[1].strip(), ".shot", m[2].strip()) if x) + " }", body)
    # HTML 寫的 <img> 只帶圓角時，同樣改成 .shot
    body = re.sub(r'(<img\b[^>]*?)\s+style="border-radius:\s*[\d.]+(?:px|rem)?;?\s*"', r'\1 class="shot"', body)

    by_docs = {m["docs"]: m for m in moved if lang in m["langs"]}
    site_pages = {p.relative_to(ROOT / "pages" / lang).with_suffix("").as_posix()
                  for p in (ROOT / "pages" / lang).rglob("*.md")} | {m["page"] for m in moved}
    prefix = LANGS[lang]
    src_dir = posixpath.dirname(src)

    def rewrite(m: re.Match) -> str:
        target = m[2]
        path, _, anchor = target.partition("#")
        anchor = f"#{anchor}" if anchor else ""
        if path.startswith(("mailto:", "#")):
            return m[0]
        if path == "/docs" or path.startswith("/docs/"):
            # 文件站的站內絕對路徑，例如 /docs/en/，寫成完整網址，onion 版建置時會改寫
            path = f"https://anoni.net{path}"
        if "://" in path:
            # 文件站裡指向已搬走頁面的完整網址，改成本站的路徑
            docs_base = f"https://anoni.net/docs{prefix}/"
            if path.startswith(docs_base):
                rest = path[len(docs_base):]
                if rest in posts:
                    return f"{m[1]}{posts[rest]}{anchor}{m[3]}"
                for d, item in by_docs.items():
                    if rest == docs_url_path(d):
                        return f"{m[1]}/{item['page']}/{anchor}{m[3]}"
            # 本站同語系頁面的完整網址改成站內路徑，建置時再加語系前綴
            own = f"https://anoni.net{prefix}/"
            if path.startswith(own) and path[len(own):].strip("/") in site_pages:
                return f"{m[1]}/{path[len(own):]}{anchor}{m[3]}"
            # 已經搬到本站的動態，文件站那一側先改成了完整網址，搬回本站時改成站內路徑
            if path.startswith(f"{own}updates/"):
                return f"{m[1]}/{path[len(own):]}{anchor}{m[3]}"
            return f"{m[1]}{path}{anchor}{m[3]}"
        if not path:
            return m[0]
        resolved = posixpath.normpath(posixpath.join(src_dir, path))
        if resolved in by_docs:
            return f"{m[1]}/{by_docs[resolved]['page']}/{anchor}{m[3]}"
        if resolved in posts:
            return f"{m[1]}{posts[resolved]}{anchor}{m[3]}"
        if resolved.startswith("blog/posts/") and resolved.endswith(".md") and blog_url:
            return f"{m[1]}docs:{blog_url(lang, resolved)}{anchor}{m[3]}"
        if resolved.endswith(".md"):
            return f"{m[1]}docs:{docs_url_path(resolved)}{anchor}{m[3]}"
        return f"{m[1]}docs:{resolved}{anchor}{m[3]}"

    body = LINK.sub(rewrite, body)
    for found in UNSUPPORTED.findall(body):
        print(f"  ! {where}：有本站不支援的語法 {found!r}，要手動改寫", file=sys.stderr)
    head = yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=1000)
    return f"---\n{head}---\n\n{body.lstrip()}"


def blog_resolver(docs: Path, ref: str):
    """部落格文章的網址是 blog/YYYY/MM/<slug>/，從文章的 front matter 讀日期與 slug。"""
    def resolve(lang: str, path: str) -> str:
        text = git_show(docs, ref, f"docs/{lang}/{path}")
        if text is None:
            raise SystemExit(f"找不到 docs/{lang}/{path}")
        meta = yaml.safe_load(text.split("---\n", 2)[1]) or {}
        date = meta.get("date")
        if isinstance(date, dict):
            date = date.get("created")
        slug = meta.get("slug") or posixpath.basename(path)[:-3]
        return f"blog/{date:%Y/%m}/{slug}/" if hasattr(date, "year") else f"blog/{str(date)[:4]}/{str(date)[5:7]}/{slug}/"
    return resolve


# ---------------------------------------------------------------- 部落格文章

def load_update_groups() -> tuple[dict[str, list[str]], list[str]]:
    """tools/docs_updates.toml：依類型分組的文章名單，以及已經搬到本站的 moved。"""
    with open(UPDATES_LIST, "rb") as f:
        data = tomllib.load(f)
    moved = data.pop("moved", [])
    return data, moved


def post_info(docs: Path, ref: str, lang: str, name: str) -> dict | None:
    """文件站一篇文章在某個語系的 front matter 與網址。"""
    path = f"docs/{lang}/blog/posts/{name}"
    text = git_show(docs, ref, path)
    if text is None:
        # 已經從文件站刪掉的文章（搬過來的批次），讀刪除前的版本，轉址表與連結改寫才不會漏
        deleted = subprocess.run(["git", "-C", str(docs), "log", "-1", "--format=%H", "--diff-filter=D", ref, "--", path],
                                 capture_output=True, text=True).stdout.strip()
        text = git_show(docs, f"{deleted}^", path) if deleted else None
    if text is None:
        return None
    meta = yaml.safe_load(text.split("---\n", 2)[1]) or {}
    date = meta.get("date")
    if isinstance(date, dict):
        date = date.get("created")
    slug = meta.get("slug") or name[:-3]
    return {"text": text, "meta": meta, "date": date, "slug": slug,
            "url": f"blog/{date:%Y/%m}/{slug}/"}


def www_slug(infos: dict[str, dict], name: str) -> str:
    """本站三個語系要同一個檔名才連得成語言切換。文件站的 slug 有一篇三語各不同，
    優先用 ASCII 的那個，都不是時用檔名。"""
    for lang in ("zh-TW", "en", "zh-CN"):
        slug = infos.get(lang, {}).get("slug", "")
        if slug and slug.isascii():
            return slug
    return name[:-3]


def moved_posts_index(docs: Path, ref: str, names: list[str]) -> dict[str, dict[str, str]]:
    """每個語系：文件站的原始檔路徑與網址路徑，對到本站動態的路徑（不含語系前綴）。"""
    index = {lang: {} for lang in LANGS}
    for name in names:
        infos = {lang: i for lang in LANGS if (i := post_info(docs, ref, lang, name))}
        if not infos:
            raise SystemExit(f"{name}：文件站的歷史裡找不到這篇")
        slug = www_slug(infos, name)
        for lang, info in infos.items():
            dest = f"/updates/{info['date']:%Y/%m}/{slug}/"
            index[lang][f"blog/posts/{name}"] = dest
            index[lang][info["url"]] = dest
    return index


def git_blob(docs: Path, ref: str, path: str) -> bytes | None:
    result = subprocess.run(["git", "-C", str(docs), "show", f"{ref}:{path}"], capture_output=True)
    return result.stdout if result.returncode == 0 else None


def stage_images(text: str, lang: str, docs: Path, ref: str, where: str, staged: dict[str, Path]) -> str:
    """文件站 repo 裡的圖片複製到 .cache/updates-images/，檔名加上內容雜湊，內文改成 assets.anoni.net 的網址。"""
    def repl(m: re.Match) -> str:
        path = m[2]
        if "://" in path or path.startswith(("data:", "#", "mailto:")):
            return m[0]
        # <a href> 只處理指到圖片的（點圖放大），其他連結交給 convert()
        if m[1].startswith("<a") and not path.lower().endswith(IMAGE_EXT):
            return m[0]
        rel = posixpath.normpath(posixpath.join("blog/posts", path))
        # 文件站有些圖用網址的層級寫相對路徑（文章網址是 blog/YYYY/MM/slug/，往上四層），
        # 照原始檔的位置算會跑出 docs/ 之外，這種從文件站的根目錄找
        if rel.startswith(".."):
            rel = re.sub(r"^(\.\./)+", "", rel)
        rel = rel.removeprefix("/").removeprefix("docs/")
        blob = git_blob(docs, ref, f"docs/{lang}/{rel}") or git_blob(docs, ref, f"docs/zh-TW/{rel}")
        if blob is None:
            print(f"  ! {where}：找不到圖片 {path}", file=sys.stderr)
            return m[0]
        stem, ext = posixpath.splitext(posixpath.basename(rel))
        name = f"{stem}-{hashlib.sha256(blob).hexdigest()[:8]}{ext.lower()}"
        dest = IMAGE_CACHE / name
        if name not in staged:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(blob)
            staged[name] = dest
        return f"{m[1]}{ASSETS_UPDATES}{name}"
    return IMAGE.sub(repl, text)


def import_posts(names: list[str], docs: Path, ref: str) -> int:
    groups, moved_names = load_update_groups()
    kind_of = {n: kind for kind, items in groups.items() for n in items}
    unknown = [n for n in names if n not in kind_of]
    if unknown:
        raise SystemExit(f"這幾篇不在 tools/docs_updates.toml 的名單裡：{unknown}")
    moved = load_moved()
    blog_url = blog_resolver(docs, ref)
    # 連結改寫時，這一次要搬的文章也算已經搬過
    index = moved_posts_index(docs, ref, sorted(set(moved_names) | set(names)))
    staged: dict[str, Path] = {}
    count = 0
    for name in names:
        infos = {lang: i for lang in LANGS if (i := post_info(docs, ref, lang, name))}
        slug = www_slug(infos, name)
        for lang, info in infos.items():
            where = f"docs/{lang}/blog/posts/{name}"
            meta, text = info["meta"], info["text"]
            body = text.split("---\n", 2)[2]
            h1 = re.search(r"^# (.+)$", body, re.M)
            title = ICON.sub("", h1[1] if h1 else meta.get("title", "")).strip()
            desc = str(meta.get("description") or meta.get("summary") or "").strip()
            desc = re.sub(r"\*\*|`", "", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", desc))
            text = text.replace("<!-- more -->\n", "").replace("<!-- more -->", "")
            # images.anoni.net 是同一台圖片主機的舊網域，onion 版只改寫 assets.anoni.net
            text = text.replace("https://images.anoni.net/", "https://assets.anoni.net/")
            text = stage_images(text, lang, docs, ref, where, staged)
            out = convert(text, f"blog/posts/{name}", lang, moved, where, blog_url, index[lang])
            check_docs_links(out, lang, docs, ref, where)
            front = {"title": title, "description": desc, "date": info["date"]}
            if kind_of[name] in UPDATE_KINDS:
                front["kind"] = kind_of[name]
            image = str(meta.get("image") or "")
            if image.startswith(ASSETS_UPDATES.rsplit("/", 2)[0]):
                front["og_image"] = image
            head = yaml.safe_dump(front, allow_unicode=True, sort_keys=False, width=1000)
            dest = ROOT / "updates" / lang / f"{slug}.md"
            converted = out.split("---\n", 2)[2].lstrip()
            dest.write_text(f"---\n{head}---\n\n{converted}", encoding="utf-8")
            print(f"  {where} → {dest.relative_to(ROOT)}")
            count += 1
    upload_images(staged)
    return count


def upload_images(staged: dict[str, Path]) -> None:
    if not staged:
        return
    target = os.environ.get("WWW_UPDATES_RSYNC")
    if not target:
        print(f"  ! 沒有設 WWW_UPDATES_RSYNC，{len(staged)} 張圖只放在 {IMAGE_CACHE.relative_to(ROOT)}，"
              "頁面上的圖在上傳之前會是 404", file=sys.stderr)
        return
    subprocess.run(["rsync", "-a", "--chmod=F644", "--mkpath", *map(str, staged.values()), target.rstrip("/") + "/"],
                   check=True)
    for name in staged:
        req = urllib.request.Request(ASSETS_UPDATES + name, method="HEAD", headers={"User-Agent": "anoni-www-import"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status != 200:
                raise SystemExit(f"{ASSETS_UPDATES}{name} 回 {resp.status}")
    print(f"  上傳 {len(staged)} 張圖到 {ASSETS_UPDATES}")


def check_docs_links(text: str, lang: str, docs: Path, ref: str, where: str) -> None:
    """轉完的 docs: 連結拿去比對文件站的網址合約，對不上就印警告。"""
    contract = git_show(docs, ref, "tools/data/url_contract.txt") or ""
    lines = [line for line in contract.splitlines() if line.startswith("/")]
    pages = {line for line in lines if " -> " not in line}
    redirects = {line.split(" -> ")[0] for line in lines if " -> " in line}
    prefix = LANGS[lang]
    for target in re.findall(r"\]\(docs:([^)#\s]*)", text):
        url = f"{prefix}/{target}"
        if url in redirects:
            print(f"  ! {where}：{url} 在文件站只是轉址，改連它的目的地或其他語系", file=sys.stderr)
        elif url not in pages and not target.startswith(("assets/", "feed")):
            print(f"  ! {where}：文件站沒有 {url}", file=sys.stderr)


def import_pages(pages: list[str], docs: Path, ref: str) -> int:
    moved = load_moved()
    blog_url = blog_resolver(docs, ref)
    by_page = {m["page"]: m for m in moved if m.get("import")}
    count = 0
    for page in pages:
        item = by_page.get(page)
        if not item:
            raise SystemExit(f"{page} 不在 docs_moved.toml 裡，或 import 不是 true")
        for lang in item["langs"]:
            src = f"docs/{lang}/{item['docs']}"
            text = git_show(docs, ref, src)
            if text is None:
                print(f"  - {src} 不存在，略過")
                continue
            dest = ROOT / "pages" / lang / f"{page}.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            out = convert(text, item["docs"], lang, moved, src, blog_url)
            check_docs_links(out, lang, docs, ref, src)
            dest.write_text(out, encoding="utf-8")
            print(f"  {src} → {dest.relative_to(ROOT)}")
            count += 1
    return count


# 社群動態的標籤，跟 build.py 的 UPDATE_KINDS 一致
UPDATE_KINDS = ("new", "event", "update")


def updates_index(docs: Path, ref: str) -> str:
    """文件站舊的社群文章：每篇每個語系的標題、日期、摘要與網址，給動態列表用。"""
    groups, moved_names = load_update_groups()
    # 依組別帶上類型，community（觀點、立場、經驗）不加標籤。已經搬到本站的不列，本站有自己的那一篇
    names = [(name, kind) for kind, items in groups.items() for name in items if name not in moved_names]
    blog_url = blog_resolver(docs, ref)
    contract = git_show(docs, ref, "tools/data/url_contract.txt") or ""
    published = {line.split(" ")[0] for line in contract.splitlines()
                 if line.startswith("/") and " -> " not in line}
    out = ["# 由 tools/import_from_docs.py --updates 從 tools/docs_updates.toml 產生，不要手改。",
           "# 文件站舊的社群文章，本站的動態列表連過去。url 是文件站同語系底下的路徑。", ""]
    for name, kind in names:
        out.append("[[posts]]")
        if kind in UPDATE_KINDS:
            out.append(f'kind = "{kind}"')
        for lang in LANGS:
            path = f"docs/{lang}/blog/posts/{name}"
            text = git_show(docs, ref, path)
            if text is None:
                continue
            meta = yaml.safe_load(text.split("---\n", 2)[1]) or {}
            h1 = re.search(r"^# (.+)$", text.split("---\n", 2)[2], re.M)
            title = ICON.sub("", h1[1] if h1 else meta.get("title", "")).strip()
            summary = (meta.get("summary") or meta.get("description") or "").strip()
            # 列表與 RSS 用純文字，拿掉 Markdown 的行內程式碼與連結
            summary = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", summary).replace("`", "")
            date = meta.get("date")
            if isinstance(date, dict):
                date = date.get("created")
            url = blog_url(lang, f"blog/posts/{name}")
            if f"{LANGS[lang]}/{url}" not in published:
                # 例如 redirect_maps 剛好佔用了文章的網址，文章本身沒有發布出去
                print(f"  ! {path}：{LANGS[lang]}/{url} 在文件站不是正式頁面，這個語系不列", file=sys.stderr)
                continue
            if lang == "zh-TW":
                out.append(f"date = {str(date)[:10]}")
            out.append(f"[posts.{lang}]")
            out.append(f"title = {json.dumps(title, ensure_ascii=False)}")
            out.append(f"summary = {json.dumps(summary, ensure_ascii=False)}")
            out.append(f"url = {json.dumps(url)}")
        out.append("")
    return "\n".join(out)


def nginx_conf(docs: Path, ref: str) -> str:
    moved = load_moved()
    _, moved_names = load_update_groups()
    posts = []
    for name in moved_names:
        infos = {lang: i for lang in LANGS if (i := post_info(docs, ref, lang, name))}
        if not infos:
            # 漏掉的話舊網址會少一條 301，寧可中止
            raise SystemExit(f"{name}：文件站的歷史裡找不到這篇，轉址表沒有寫入")
        slug = www_slug(infos, name)
        posts += [(lang, info["url"].rstrip("/"), f"updates/{info['date']:%Y/%m}/{slug}") for lang, info in infos.items()]
    lines = [
        "# 文件站搬到官網的頁面，clearnet 與 onion 兩邊的 301 對照表。",
        "#",
        "# 由 tools/import_from_docs.py --nginx 從 tools/docs_moved.toml 產生，不要手改。",
        "# 複製到 m6 的 /etc/nginx/conf.d/anoni-docs-moved.conf，nginx -t 通過再 reload。",
        "# conf.d 底下的檔案由 nginx.conf 在 http 區塊引入，map 只能寫在那一層。",
        "#",
        "# anoninet.conf 的 anoni.net 與 docs.<onion> 兩個 server 開頭各有一行 if 讀這裡的變數：",
        "#   if ($anoni_docs_moved)       { return 301 $anoni_docs_moved; }",
        "#   if ($anoni_docs_moved_onion) { return 301 $anoni_docs_moved_onion; }",
        "#",
        "# 每一條比對三種寫法：不帶尾斜線、帶尾斜線、帶 index.html。query string 不帶過去。",
        "",
    ]
    for var, docs_root, site in (("anoni_docs_moved", "/docs", "https://anoni.net"),
                                 ("anoni_docs_moved_onion", "", f"http://{ONION}")):
        label = "clearnet：anoni.net/docs/..." if docs_root else "onion：docs.<onion>/...，路徑不帶 /docs"
        lines += [f"# {label}", f"map $uri ${var} {{", '    default "";']
        for item in moved:
            lines.append("")
            for lang in LANGS:
                if lang not in item["langs"]:
                    continue
                prefix = LANGS[lang]
                path = docs_url_path(item["docs"]).rstrip("/")
                key = re.escape(f"{docs_root}{prefix}/{path}").replace("\\/", "/").replace("\\-", "-")
                lines.append(f"    ~^{key}(/|/index\\.html)?$  {site}{prefix}/{item['page']}/;")
        if posts:
            lines += ["", "    # 部落格的社群文章，搬到 /updates/（tools/docs_updates.toml 的 moved）"]
        for lang, src, dest in posts:
            prefix = LANGS[lang]
            key = re.escape(f"{docs_root}{prefix}/{src}").replace("\\/", "/").replace("\\-", "-")
            lines.append(f"    ~^{key}(/|/index\\.html)?$  {site}{prefix}/{dest}/;")
        lines += ["}", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--import", dest="pages", nargs="+", metavar="PAGE", help="要搬的頁面")
    parser.add_argument("--import-all", action="store_true", help="搬 import = true 的全部頁面")
    parser.add_argument("--nginx", action="store_true", help="重新產生 nginx 對照表")
    parser.add_argument("--updates", action="store_true", help="重新產生文件站舊社群文章的清單")
    parser.add_argument("--import-post", dest="posts", nargs="+", metavar="FILE",
                        help="把部落格文章搬到 updates/，檔名照 tools/docs_updates.toml，例如 move-to-anoni-net.md")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS, help="文件站的 clone")
    parser.add_argument("--ref", default="origin/main", help="文件站要讀的 ref")
    args = parser.parse_args()
    MATERIAL_ICONS[:] = sorted(args.docs.glob("docs/.venv/lib/python*/site-packages/material/templates/.icons"))
    if args.import_all:
        args.pages = [m["page"] for m in load_moved() if m.get("import")]
    if args.pages:
        print(f"搬了 {import_pages(args.pages, args.docs, args.ref)} 個檔案")
    if args.posts:
        print(f"搬了 {import_posts(args.posts, args.docs, args.ref)} 個檔案")
    if args.nginx:
        NGINX.write_text(nginx_conf(args.docs, args.ref), encoding="utf-8")
        print(f"寫入 {NGINX.relative_to(ROOT)}")
    if args.updates:
        (ROOT / "data" / "docs_updates.toml").write_text(updates_index(args.docs, args.ref), encoding="utf-8")
        print("寫入 data/docs_updates.toml")
    if not (args.pages or args.posts or args.nginx or args.updates):
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
