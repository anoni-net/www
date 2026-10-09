"""把文件站（anoni-net/docs）的頁面搬到本站，以及產生舊網址的 nginx 對照表。

    uv run tools/import_from_docs.py --import about/governance join/roadmap-2026
    uv run tools/import_from_docs.py --import-all     # docs_moved.toml 裡 import = true 的全部
    uv run tools/import_from_docs.py --nginx          # 重新產生 tools/nginx-docs-moved.conf
    uv run tools/import_from_docs.py --updates        # 從 tools/docs_updates.toml 產生 data/docs_updates.toml

讀的是文件站的 git（預設 ../anoni-net-docs 的 origin/main），不是工作目錄，所以本機
有沒有切到別的分支都不影響。搬遷對照寫在 tools/docs_moved.toml。

轉換只處理機械性的部分：front matter 只留 title 與 description，拿掉第一個 # 標題
（本站的模板用 title 產生），拿掉 {target="_blank"}，站內連結依目標改寫。

Material 的圖示（:material-*:、:octicons-*: 等）改成 <i data-icon="名稱"></i>，建置時
內嵌 SVG，用到的 SVG 從文件站的 mkdocs-material 套件複製到 icons/。用空標籤而不是文字
佔位，是因為標題裡的佔位文字會被算進錨點。admonition 與折疊區塊的標題是純文字，
那裡的圖示直接拿掉。.md-button 改成本站的 .btn，議程表的彩色標籤改成單色的 .tag。
轉完要人工看一次，遇到這支不處理的寫法會印出警告。
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import subprocess
import sys
import tomllib
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


def convert(text: str, src: str, lang: str, moved: list[dict], where: str, blog_url=None) -> str:
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
        if "://" in path:
            # 文件站裡指向已搬走頁面的完整網址，改成本站的路徑
            docs_base = f"https://anoni.net/docs{prefix}/"
            if path.startswith(docs_base):
                rest = path[len(docs_base):]
                for d, item in by_docs.items():
                    if rest == docs_url_path(d):
                        return f"{m[1]}/{item['page']}/{anchor}{m[3]}"
            # 本站同語系頁面的完整網址改成站內路徑，建置時再加語系前綴
            own = f"https://anoni.net{prefix}/"
            if path.startswith(own) and path[len(own):].strip("/") in site_pages:
                return f"{m[1]}/{path[len(own):]}{anchor}{m[3]}"
            return m[0]
        if not path:
            return m[0]
        resolved = posixpath.normpath(posixpath.join(src_dir, path))
        if resolved in by_docs:
            return f"{m[1]}/{by_docs[resolved]['page']}/{anchor}{m[3]}"
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


def updates_index(docs: Path, ref: str) -> str:
    """文件站舊的社群文章：每篇每個語系的標題、日期、摘要與網址，給動態列表用。"""
    with open(ROOT / "tools" / "docs_updates.toml", "rb") as f:
        names = tomllib.load(f)["posts"]
    blog_url = blog_resolver(docs, ref)
    contract = git_show(docs, ref, "tools/data/url_contract.txt") or ""
    published = {line.split(" ")[0] for line in contract.splitlines()
                 if line.startswith("/") and " -> " not in line}
    out = ["# 由 tools/import_from_docs.py --updates 從 tools/docs_updates.toml 產生，不要手改。",
           "# 文件站舊的社群文章，本站的動態列表連過去。url 是文件站同語系底下的路徑。", ""]
    for name in names:
        out.append("[[posts]]")
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


def nginx_conf() -> str:
    moved = load_moved()
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
        lines += ["}", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--import", dest="pages", nargs="+", metavar="PAGE", help="要搬的頁面")
    parser.add_argument("--import-all", action="store_true", help="搬 import = true 的全部頁面")
    parser.add_argument("--nginx", action="store_true", help="重新產生 nginx 對照表")
    parser.add_argument("--updates", action="store_true", help="重新產生文件站舊社群文章的清單")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS, help="文件站的 clone")
    parser.add_argument("--ref", default="origin/main", help="文件站要讀的 ref")
    args = parser.parse_args()
    MATERIAL_ICONS[:] = sorted(args.docs.glob("docs/.venv/lib/python*/site-packages/material/templates/.icons"))
    if args.import_all:
        args.pages = [m["page"] for m in load_moved() if m.get("import")]
    if args.pages:
        print(f"搬了 {import_pages(args.pages, args.docs, args.ref)} 個檔案")
    if args.nginx:
        NGINX.write_text(nginx_conf(), encoding="utf-8")
        print(f"寫入 {NGINX.relative_to(ROOT)}")
    if args.updates:
        (ROOT / "data" / "docs_updates.toml").write_text(updates_index(args.docs, args.ref), encoding="utf-8")
        print("寫入 data/docs_updates.toml")
    if not (args.pages or args.nginx or args.updates):
        parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
