#!/bin/sh
# m6 上建置並發布 anoni.net 首頁與社群頁面，由 ubuntu 的 crontab 每 5 分鐘執行一次：
#
#   */5 * * * * /home/ubuntu/www-deploy.sh
#
# 本檔是那支腳本的原始檔，改了之後要複製到 m6 的 /home/ubuntu/www-deploy.sh。
#
# 目錄結構：
#   /srv/anoni-net-www/repo            anoni-net/www 的 clone，只拉 main
#   /srv/anoni-net-www/releases/<sha>  每個 commit 建置一份，保留最近 KEEP 份
#   /srv/anoni-net-www/current         symlink，nginx 讀 current/clearnet 與 current/onion
#
# 建置完成、檢查通過之後才切換 current，切換是原子操作，建置失敗時線上維持原本的版本。
# 只接受 fast-forward，main 的歷史被改寫時停下來寫進 log，不強制覆蓋，等人處理。
# 同一個 commit 建置失敗過就不再重試，有新的 commit 才會再建置。
# 有更新時才寫 log，沒有變動就安靜結束。上一輪還沒跑完時這一輪直接略過。
# 要暫停自動發布（例如手動退回上一版時），建立 /srv/anoni-net-www/hold，刪掉就恢復。
set -eu

BASE=/srv/anoni-net-www
REPO=$BASE/repo
LOG=/home/ubuntu/www-deploy.log
UV=/home/ubuntu/.local/bin/uv
KEEP=5

exec 9>/tmp/www-deploy.lock
flock -n 9 || exit 0
[ -e "$BASE/hold" ] && exit 0

before=$(git -C "$REPO" rev-parse --short=12 HEAD)
if ! git -C "$REPO" pull --ff-only -q origin main 2>>"$LOG"; then
    echo "$(date -Iseconds) 無法 fast-forward，停在 $before，需要人工處理" >>"$LOG"
    exit 1
fi
sha=$(git -C "$REPO" rev-parse --short=12 HEAD)
current=$(readlink "$BASE/current" 2>/dev/null || true)
[ "$current" = "releases/$sha" ] && exit 0
[ "$(cat "$BASE/failed" 2>/dev/null || true)" = "$sha" ] && exit 0

dest=$BASE/releases/$sha
rm -rf "$dest.tmp"
if ! (cd "$REPO" && "$UV" run --quiet --frozen build.py --check && "$UV" run --quiet --frozen build.py --out "$dest.tmp") >/dev/null 2>>"$LOG"; then
    echo "$(date -Iseconds) $sha 建置或檢查失敗，線上維持 ${current:-（尚未發布）}" >>"$LOG"
    echo "$sha" >"$BASE/failed"
    rm -rf "$dest.tmp"
    exit 1
fi
rm -rf "$dest"
mv "$dest.tmp" "$dest"
ln -sfn "releases/$sha" "$BASE/current.tmp"
mv -T "$BASE/current.tmp" "$BASE/current"
rm -f "$BASE/failed"
echo "$(date -Iseconds) 發布 $sha $(git -C "$REPO" log -1 --format=%s)" >>"$LOG"

# 保留最近 KEEP 份，正在使用的那一份不會被刪
ls -1t "$BASE/releases" | tail -n +$((KEEP + 1)) | while read -r old; do
    [ "releases/$old" = "releases/$sha" ] || rm -rf "${BASE:?}/releases/$old"
done
