"""專案卡片上的「最新內容」：文件站與新聞導讀最近發布的幾篇。

建置時讀兩個網站各語系的 RSS，只留標題、網址與日期，寫進 .cache/latest/<網站>-<語系>.json。
新聞導讀每天都有新稿，一小時內的建置直接用快取（m6 每小時重建一次）。讀取失敗時退回舊的快取，
連快取都沒有就不列最新內容，卡片照樣顯示，建置照樣成功。設了 WWW_OFFLINE 時只用快取。

網址一律是 clearnet 的 https://anoni.net/...，onion 版在寫檔前由 site.toml 的對照表改寫。
"""

import html
import json
import os
import re
import time
import urllib.request
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path

MAX_AGE = 3600
# 各網站 RSS 的位置，{prefix} 是語系前綴（正體是空字串，其他是 /zh-cn、/en）
FEEDS = {
    "docs": "https://anoni.net/docs{prefix}/feed_rss_created.xml",
    "news": "https://anoni.net/news{prefix}/feed.xml",
}
ITEM = re.compile(r"<item>(.*?)</item>", re.S)


def _field(item: str, tag: str) -> str:
    m = re.search(rf"<{tag}>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</{tag}>", item, re.S)
    return html.unescape(m[1].strip()) if m else ""


def parse(xml: str, limit: int = 20) -> list[dict]:
    items = []
    for raw in ITEM.findall(xml)[:limit]:
        try:
            day = parsedate_to_datetime(_field(raw, "pubDate")).date().isoformat()
        except (TypeError, ValueError):
            continue
        items.append({"title": _field(raw, "title"), "link": _field(raw, "link"), "date": day})
    # RSS 不保證照時間排，新的在前
    return sorted(items, key=lambda i: i["date"], reverse=True)


def load(product: str, prefix: str, cache_dir: Path, count: int = 3) -> list[dict]:
    """回傳最新的 count 篇，每篇有 title、link 與 date（datetime.date）。讀不到就是空的清單。"""
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{product}-{prefix.strip('/') or 'zh-tw'}.json"
    items = None
    fresh = path.exists() and time.time() - path.stat().st_mtime < MAX_AGE
    if fresh or os.environ.get("WWW_OFFLINE"):
        items = json.loads(path.read_text()) if path.exists() else []
    else:
        url = FEEDS[product].format(prefix=prefix)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "anoni.net-www-build"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                items = parse(resp.read().decode("utf-8"))
            path.write_text(json.dumps(items, ensure_ascii=False))
        except Exception as err:  # 連不上、逾時、格式不對都退回快取
            print(f"latest：{url} 讀取失敗（{err}），改用快取", flush=True)
            items = json.loads(path.read_text()) if path.exists() else []
    return [{**i, "date": datetime.fromisoformat(i["date"]).date()} for i in items[:count]]
