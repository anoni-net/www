---
title: 2026 年 10 月 Tor 出口中繼遭入侵事件與營運者的安全檢查
description: 2026 年 10 月初，數百個 Tor 出口中繼的出口政策遭竄改，用來攔截 SSH 登入。本文整理事件經過、各項數字的計算方式與尚未釐清的問題，以及中繼營運者檢查、處置與預防入侵的做法。
date: 2026-10-24
---

2026 年 10 月初，有數百個 Tor 出口中繼的出口政策被人改掉，經過它們的 SSH 連線被導到攔截伺服器。使用者略過主機金鑰的警告或接受陌生的金鑰、輸入密碼之後，密碼就被取走。依發現者的觀察，攻擊者接著用同一組密碼登入目標伺服器，試圖裝上名為 Ebury 的 OpenSSH 後門。經由攔截而被裝上 Ebury 的伺服器，目前沒有人公開確認過。

確認有 Ebury 的是受害最多的中繼家族 Quetzalcoatl 的兩台伺服器，一台是管理伺服器，另一台運作出口中繼。兩台都是在 8 月經由管理伺服器的密碼被入侵的，其他受影響主機的狀況還沒有人查證。入侵途徑比較清楚的也只有這個家族，管理伺服器開著密碼登入，密碼又重複使用。

本文寫給在台灣與其他地方營運中繼的人。文中的時間除了另外註明的以外都是 UTC，資料查證到 2026 年 10 月 24 日。

## 事件經過

第一手資料有四份：Tor Network Health 團隊在 tor-relays 郵件列表的公告、受害最多的中繼家族（Quetzalcoatl）營運者寫的事後檢討、一位中繼營運者用公開目錄資料做的分析，以及發現者 kaba 的文章。時間線依這四份資料排出，後面的小節再說明每一段。

- **8 月 28 日**：攻擊者用營運者帳號的密碼登入 Quetzalcoatl 家族的管理伺服器，第一次就成功，5 分鐘內取得 root，接著裝上 Ebury。一個多小時後，攻擊者登入另一台運作出口中繼的伺服器，同樣裝上 Ebury。
- **10 月 1 日 15:33 起**：Quetzalcoatl 以外 21 位營運者的 40 個中繼在 5 分多鐘內改用同一份出口政策，多數是重新載入設定。
- **10 月 2 日 09:27 起**：Quetzalcoatl 家族的 277 個中繼全部改成另一份出口政策。kaba 同一天早上（未註明時區）經由 Tor 連 SSH 時看到主機金鑰變更的警告，用 exitmap 掃描全部出口，當晚通報 Tor Network Health 團隊。
- **10 月 4 日**：01:00 時，使用攻擊者政策的出口占可用出口權重 7.46%，是最高點。13:56 前後，Quetzalcoatl 家族接到 Network Health 團隊的聯絡，停掉一台主機上的 Tor。18:00 起目錄授權（directory authority）陸續對受影響的中繼投下 BadExit 與 MiddleOnly，21:00 的共識開始帶有這兩個旗標。
- **10 月 5 日**：17:00 起，共識裡已經沒有使用攻擊者政策的中繼。17:50 Network Health 團隊在 tor-relays 發布公告。
- **10 月 7 日到 22 日**：Quetzalcoatl 家族的事後檢討（10/7）、目錄資料分析（10/9）、kaba 的文章（10/20），以及 The Hacker News 與 SecureWorld 的報導（10/21、10/22）。

BadExit 讓客戶端不再把該中繼當成出口，MiddleOnly 只允許它擔任中間節點。kaba 通報之後約兩天，共識開始帶上旗標，受影響的中繼完全離開共識又花了將近一天。

## 攻擊者更動的設定

分析者把攻擊者用的出口政策分成兩份。A 政策拒絕 25、110、143、445、3389 等連接埠，其餘全部放行。B 政策是 Tor 的預設政策再多拒絕 465、587、993、995。兩份政策都放行 22（SSH），也都關掉加密的收信連接埠 993 與 995。B 政策另外放行明文的 110 與 143，經過 B 政策出口的收信只剩明文可用。攻擊者為什麼關掉加密的連接埠，公開資料看不出來。

Tor 的 `ExitRelay` 預設是 `auto`。在這個設定下，torrc 只要設定了 `ExitPolicy`（或 `ReducedExitPolicy`、`IPv6Exit`），中繼就會依出口政策當出口。Tor 的公告裡寫，攻擊者取得 Linux 主機的權限之後，會把非出口中繼的 torrc 改成出口。分析者的資料裡有 24 個中繼原本不是出口，改完之後全部取得 Exit 旗標，不過多數受影響的中繼本來就是出口。

只改出口政策還不足以攔截，連線要被導走才行，Tor 的公告請營運者檢查有沒有把 port 22 轉走的 NAT 規則。使用者端的經過寫在 kaba 的文章裡。經由受影響的出口連 SSH 時，連線被導到 12 台攔截伺服器其中一台。使用者略過警告、繼續登入之後，攻擊者取得密碼。攻擊者把連線轉給真正的伺服器，記錄使用者輸入的每個指令，再另外開一條連線替那台伺服器裝上 Ebury。kaba 用蜜罐觀察到，攔截端取得帳密之後會先檢查 sudo，再執行一段 base64 編碼的 Perl 安裝程式。

Ebury 是一個 OpenSSH 後門，依 ESET 2024 年的報告，從 2009 年起約有 40 萬台伺服器被它入侵。Quetzalcoatl 家族在自己的主機上找到的是 1.8.3 版，形式是一個沒有套件擁有、帶 setuid 的 `libkeyutils` 函式庫，`libkeyutils.so.1` 的符號連結改指向它。套件的原始檔沒有被動過，所以 `dpkg -V` 與 `debsums` 檢查不出來。Ebury 在 sshd 裡記下每一次輸入的密碼，失敗的嘗試也算在內，後門登入則不留下登入紀錄與 shell 歷史。

## 數字的來源與差異

報導裡的數字來自不同的方法，引用時要寫出是哪一種：

| 數字 | 來源 | 計算方式 |
|---|---|---|
| 333 | kaba 的文章 | 10 月 2 日用 exitmap 掃描約 3,000 個出口，約十來個出口本身出示假的主機金鑰，其餘三百多個把連線轉到 12 台攔截伺服器。名單與原始資料沒有公開 |
| 377 個中繼、59 位營運者 | 目錄資料分析 | 10 月 1 日到 4 日之間發布過 A 或 B 政策的中繼，其中 277 個屬於 Quetzalcoatl 家族。分析者註明這只代表政策吻合，不能證明主機被入侵 |
| 7.46% | 目錄資料分析 | 10 月 4 日 01:00 的共識裡，351 個受影響的可用出口占所有可用出口的共識權重 |
| 3,084 → 2,715 | Tor Metrics | 帶 Exit 旗標的中繼數，10 月 3 日到 5 日少了 369 個，10 月 21 日是 2,688 個。事件之前就有下降的趨勢，9 月 2 日是 3,235 個，10 月 1 日是 3,068 個 |

The Hacker News 把「342 個原本擋掉 SSH 的中繼」與「24 個原本不是出口的中繼」寫成兩批，但依目錄資料分析的算法，342 已經包含那 24 個。目錄資料分析是一位中繼營運者用公開的 CollecTor 資料、在 AI 工具輔助下完成的。腳本與 CSV 都公開在 GitHub，可以自行重現，但它不是 Tor Project 的官方統計。

## 已知的入侵途徑

入侵途徑比較清楚的只有 Quetzalcoatl 家族。營運者在事後檢討裡寫的原因是「The root cause was ours」：SSH 登入、sudo 與備份的加密密碼是同一組，而且以明文寫在兩台伺服器的腳本裡，對外的管理伺服器又開著 SSH 密碼登入。營運者以為離線保管的中繼主金鑰，副本放在管理伺服器的工作站備份裡，加密用的正是攻擊者已經取得的那組密碼。

攻擊者在 8 月 28 日之前從哪裡取得這組密碼，到現在還不知道。ESET 的 Ebury 報告作者在郵件列表上的猜測，是營運者從一台已經被 Ebury 入侵的主機登入時，密碼被記了下來。另一台出口主機為什麼接受了一把不在任何 `authorized_keys` 裡的金鑰，也還沒有答案。

另外 58 位營運者的中繼為什麼出現同樣的政策、主機是否被入侵，到現在還是最大的疑問，目錄資料分析發現受影響的主機集中在 FranTech（BuyVM，AS53667）。10 月 1 日的共識裡，其他營運者放在 FranTech 的 101 個中繼有 71 個受影響，放在其他網路的 9,054 個只有 13 個受影響。同時在 FranTech 與其他網路都有中繼的 12 位營運者，其他網路上的 50 個中繼沒有一個受影響。

託管商本身被入侵是一種解釋，ESET 的 Ebury 報告作者在郵件列表上把它列為可能之一。ESET 2024 年的報告記錄過攻擊者經由託管商的基礎設施，替整批租用的伺服器裝上 Ebury。研究人員向其中一家租了一台虛擬主機，七天內就被裝上。分析者在 repo 的[託管商備忘錄](https://github.com/1aeo/TorExitPolicyManipulation/blob/main/collector-exit-policy-analysis/PROVIDER_MEMO.md)裡，把「帳密或連線階段被竊取，受害者集中在 FranTech 的客戶」排在較可能的位置。理由是只發生在 FranTech 的機制解釋不了跨託管商的受害者。另外，Quetzalcoatl 家族自己的入口也在另一家託管商上。也有 BuyVM 的客戶在郵件列表上表示自己的虛擬主機沒有異狀，不認為是託管商層級的問題。到 10 月 24 日為止，沒有任何一方給出確認的答案。

## 亞洲的受影響中繼

我們用 Tor 套件附的 GeoIP 資料庫（IPFire Location）對照目錄資料分析公開的 377 個中繼 IP。美國 171 個、盧森堡 97 個、德國 56 個、新加坡 24 個，其餘分散在克羅埃西亞、摩爾多瓦、荷蘭、瑞士、塞席爾與印度，台灣、日本、南韓、香港沒有受影響的中繼。新加坡的 24 個全部屬於 Quetzalcoatl 家族，位在同一家託管商的亞洲機房，印度的 1 個屬於另一位營運者。IP 的地理位置資料庫可能有誤差，以上是我們自行比對的結果，Tor Project 沒有公布這類資料。

[Tor 中繼節點觀測](/projects/pulse/)的每日數字（每天最後一次快照，UTC）也可以看到同樣的變化。[新加坡](/projects/pulse/sg/)帶 Exit 旗標的中繼在 10 月 3 日有 34 個，10 月 4 日剩 9 個，到 10 月 23 日是 8 個。我們推測減少的主要就是這 24 個。台灣的出口在同一段時間都維持在 2 到 4 個之間。

## 中繼的自我檢查

Tor Network Health 團隊的公告請 Linux 上的營運者逐項檢查：

- 在 [Relay Search](https://metrics.torproject.org/rs.html) 查自己的中繼，有沒有出現自己沒設定的 Exit 旗標或出口政策
- 檢查 torrc 與 `%include` 引入的所有檔案，`ExitRelay`、`ExitPolicy`、`ContactInfo`、`MyFamily`、`Nickname` 有沒有被改過
- 用 `nft list ruleset` 或 `iptables -t nat -S` 找把 port 22 轉走的 NAT 規則
- 用 `ss -tnp` 找不明的對外連線，監聽中的程序另外用 `ss -tlnp` 列出。公告的回覆串裡有人提醒，其他中繼把 ORPort 設在 22 是正常的，連往它們的連線不代表有問題
- 用 `debsums tor` 或 `rpm -V tor` 比對 tor 執行檔與發行版的套件
- 找新增的使用者、`authorized_keys` 項目、cron 工作與 systemd 單元，公告裡寫有一種持久化方式是偽裝成大寫 `CRON` 的 root 程序
- 留意未經授權載入的核心模組、通道介面與無法解釋的記憶體用量

清單上的項目全部正常也不代表主機沒有被入侵，Quetzalcoatl 家族的兩台伺服器就沒有出現公告列的任何一項痕跡，NAT 規則、新使用者、新金鑰、cron、systemd 單元與 tor 執行檔都正常。營運者的建議是開機進救援系統或掛上離線的磁碟映像再檢查。需要登入可疑的主機時只用金鑰，絕不輸入密碼，因為 Ebury 會記下來。

事後檢討列出的 Ebury 痕跡，可以補在公告的清單之後：

- 帶 setuid 的 `libkeyutils` 檔案，或 `libkeyutils.so.1` 的符號連結指向沒有套件擁有的檔案（`find / -xdev -name 'libkeyutils*' -perm -4000`、`dpkg -S "$(readlink -f /usr/lib/x86_64-linux-gnu/libkeyutils.so.1)"`，RPM 系統用 `rpm -qf`）
- `/proc/net/unix` 裡有 `@event-` 開頭的抽象 Unix socket
- `ssh.service` 的 cgroup 裡有不是 sshd 的程序（`systemctl status ssh`，Ubuntu 24.04 也要看 `init.scope`）
- 日誌裡沒有 `Requested-By:` 的 apt 交易（unattended-upgrades 本來就沒有這一行）、由 uid 0 開啟的 su 工作階段，以及 sudo 執行 `base64 -d | perl` 的紀錄

在運作中的系統上檢查時，使用者層的 rootkit 會把這些檔案藏起來。ESET 公開的 [detect_ebury.sh](https://github.com/eset/malware-research/tree/master/ebury) 內建了因應的步驟，它會嘗試連線 Ebury 各版本使用的抽象 Unix socket，可以連上時列出對應的版本與程序。1.8.3 的 socket 位址在 10 月 9 日合併進 ESET 的版本，事後檢討發布時（10 月 7 日）的 ESET 版本還偵測不到。腳本自己的結尾也寫明，找不到 socket 不代表系統沒有 Ebury，仍要對照完整的入侵指標。事後檢討的全文另外列了攻擊者的來源位址與三把 SSH 金鑰的指紋。

Quetzalcoatl 家族也建議從外部檢查：定期把 Onionoo 或 CollecTor 公布的出口政策、家族與 `ContactInfo` 跟自己部署的設定比對。主機被入侵時本機的檔案可能被改寫，已經發布的描述檔則不受影響。

## 入侵後的處置

Tor 的公告列出的處置順序如下：

1. 讓中繼下線
2. 清除前先保留磁碟與日誌
3. 重新安裝系統，不在原系統上清理
4. 產生新的中繼身分，舊的金鑰視為已被竊取
5. 更換主機上出現過的每一組帳密

Quetzalcoatl 家族補充，要更換的帳密包括每一把 SSH 金鑰、每一組密碼與 WireGuard 金鑰。重新開機或清除前也要先保存記憶體，他們主機上的隱藏程序就是在重新開機之後消失的。ESET 的 Ebury 報告作者建議先傾印網路設定（`iptables-save`、`nft list ruleset`、`ip rule show`），並提醒 Ebury 會擴散，要依被入侵主機的 `~/.ssh/known_hosts` 檢查它連過的其他主機。

確認或懷疑被入侵時，寫信到 `bad-relays@lists.torproject.org`。IP 被目錄授權封鎖的營運者，清理完之後也要寫信到同一個地址，才會從封鎖清單移除。

用 `FamilyId` 宣告家族的營運者，要照 [FamilyId 說明頁](https://community.torproject.org/relay/setup/post-install/family-ids/)的程序換掉家族金鑰，否則攻擊者的中繼可以冒稱是你的家族成員。說明頁寫的程序是產生新金鑰、複製到每一個中繼、新舊兩個 `FamilyId` 同時設定幾天，再移除舊的。Quetzalcoatl 家族另外建議，曾經存放離線主金鑰（`OfflineMasterKey`）的機器只要被入侵，那些身分就要全部退役。家族金鑰與 `FamilyId` 也要重新產生。

Debian 上用多個 instance 執行的中繼，每個 instance 的單元可以各自啟用。Quetzalcoatl 家族的主機上，攻擊者還另外加了開機連結，所以 `systemctl disable tor` 擋不住它們。家族的做法是把 `tor@` 單元 mask 掉，又因為運作中的後門可以把 mask 復原，主機也要下線。

## 預防入侵的做法

Tor Project 的營運者文件裡找不到 SSH 設定的指引。下面的做法來自 Quetzalcoatl 家族的事後檢討、ESET 的 Ebury 報告作者與 tor-relays 的討論，屬於營運者與研究人員的建議。

SSH 只允許金鑰登入，`PasswordAuthentication` 與 `KbdInteractiveAuthentication` 都設成 `no`。後者的預設值是 `yes`，搭配 PAM 時仍可能出現密碼提示。跳板與管理伺服器只接受 VPN 或白名單 IP 連入。改完設定用 `sshd -T` 確認實際生效的值，sshd 採用第一個讀到的設定，VPS 映像檔預先寫在前面的 `PermitRootLogin yes` 會蓋過後面加上的 `no`。

登入、sudo 與備份加密各用不同的帳密，密碼不寫進腳本。自動化改用只能以金鑰登入的帳號，加上範圍很窄的 `NOPASSWD` sudo。討論中也有人建議 SSH 加上多因素驗證，OpenSSH 從 8.2 版起支援 FIDO/U2F 的硬體金鑰，有密碼保護的私鑰不算第二個因素。

管理用的伺服器上不放對外的網頁服務，也不放金鑰備份。Quetzalcoatl 家族的管理伺服器上有一套曾經暴露在網路上的 WireGuard 管理介面，版本有未驗證即可讀取檔案的漏洞（`CVE-2026-44343`）。營運者後來把它排除在入口之外，仍列為要避免的做法。離線主金鑰要真的離線，不能留在任何連網機器的備份裡。日誌送出主機，sshd 的 `LogLevel` 被調到 INFO 以下時發出警報，用 AIDE 這類工具監看函式庫目錄裡沒有套件擁有或帶 setuid 的檔案。

社群的[校園中繼 SOP](/join/relay-on-campus/sop/) 已經要求只允許金鑰登入、SSH 只開放校內 VPN 網段。SOP 也建議金鑰備份兩份以上，其中一份放在指導教授的實驗室。對照這次的經驗，那一份應該放在離線的媒體上。SOP 的事故處置也依 Tor 的公告修改。無法排除入侵時，舊的身分金鑰一律視為已外洩，要產生新的中繼身分。

## 經由 Tor 使用 SSH 的人

主機金鑰改變時，OpenSSH 會警告並停用密碼驗證。`StrictHostKeyChecking` 維持預設的 `ask` 時，ssh 會拒絕連線。使用者要自行刪掉 `known_hosts` 的舊紀錄或改掉設定，才會繼續登入。第一次連線的伺服器沒有舊紀錄可以比對，使用者只看到一般的確認提示。這時要用其他管道核對指紋，例如請管理者提供。用 DNS 的 SSHFP 紀錄比對時，要設定 `VerifyHostKeyDNS`，而且只有通過 DNSSEC 驗證的紀錄才會被自動信任。

kaba 公開了其中一台攔截伺服器的 ED25519 指紋 `SHA256:6baCZCPsl+AfQuujUS81fMEE/C7UeJ+AwjrImqmDB3E`，接受過陌生金鑰的人可以用 `ssh-keygen -lf ~/.ssh/known_hosts` 列出已儲存的指紋比對。其他攔截伺服器可能用不同的金鑰，比對不到不代表沒事。

The Hacker News 依 RFC 4252 推論，只有用密碼登入的人會被取走帳密。公開金鑰驗證的簽章包含這一次連線的識別碼，攔截者無法拿去登入真正的伺服器，密碼則會在加密通道裡以原文送到對方手上。同一篇報導也寫，攔截者仍可以接受金鑰登入、顯示假的 shell。我們的推論是，在那個畫面輸入的 sudo 密碼一樣可能外洩。

報導據此寫出的範圍，是 10 月 1 日到 5 日之間經由 Tor 用密碼登入、而且接受了陌生或改變過的主機金鑰的人，報導沒有標時區。Tor 的公告、Quetzalcoatl 家族、目錄資料分析與 kaba 的文章都沒有這樣界定。起點只能當參考，Quetzalcoatl 家族的伺服器在 9 月 30 日就出現用途不明的隱藏程序。Tor 論壇在 8 月 31 日也有一則經由 Tor 連 SSH 時看到主機金鑰警告的回報，沒有指出是哪個出口，也沒有人把它跟這起事件連起來。

在那段時間前後這樣登入過的人，要把密碼當成已經外洩。被登入的那台伺服器可能已經被裝上 Ebury，確認之前不要在上面輸入任何密碼，換新密碼也一樣。先用金鑰登入或從救援系統檢查，再換掉所有用過那組密碼的地方。

要經由 Tor 管理伺服器時，把 SSH 設成洋蔥服務可以完全不經過出口中繼。連線在 Tor 網路內就會到達伺服器，出口中繼的攔截也就無從發生。洋蔥服務的設定方式見[.onion 服務架設指南](/join/setup-onion-service/)，客戶端再用 `torsocks` 或 ssh 的 `ProxyCommand` 經由 Tor 連線。

## 還沒有答案的問題

到 10 月 24 日為止，Quetzalcoatl 以外的 58 位營運者的中繼如何被改，仍然沒有公開的答案。Tor 公告裡寫的 NAT 轉向與假 `CRON` 程序，跟 Quetzalcoatl 家族主機上的 Ebury 是否出自同一批人，也還不清楚。被偷走的帳密送到哪裡、10 月 9 日之後是否還有中繼被改，目前都沒有資料。ESET 的 Ebury 報告作者在郵件列表上寫，很可能還有其他被入侵的 Tor 中繼沒被發現。kaba 依攻擊者大量收集未加密資料的做法，推測是以金錢為目的的犯罪集團，也寫明那只是推測。

發現自己的中繼有異狀時，寫信到 `bad-relays@lists.torproject.org`，也歡迎到社群的 [Matrix](/contact/) 一起討論。

## 參考資料

- [Security incident affecting some relay operators](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/WOHPLKCSHYXFTBRZXDENDKJZMBMPLMG5/)：Tor Network Health 團隊的公告，2026-10-05
- [Ebury 1.8.3 on two Quetzalcoatl relay servers: timeline, lessons, open questions](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/QHRD6YOX6RZRDR7NCHNDO7GLCEA6VFM6/)：Quetzalcoatl 家族的事後檢討，2026-10-07
- [ESET 的 Ebury 報告作者的回覆](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/RXWGWYYYKBDEBNXC2C3NYIQ2HHHWXL7O/)：tor-relays，2026-10-08
- [目錄資料分析](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/message/Z2B6XYKJZBBQADU77MSNL6FJP7MHZHIV/)：tor-relays，2026-10-09，腳本與資料在 [1aeo/TorExitPolicyManipulation](https://github.com/1aeo/TorExitPolicyManipulation)
- [How I got over 300 Tor exit nodes removed](https://kaba.cx/posts/20261020_Tor/)：kaba，2026-10-20
- [Attackers Hijacked Over 300 Tor Exit Relays to Intercept SSH Connections](https://thehackernews.com/2026/10/attackers-hijacked-over-300-tor-exit.html)：The Hacker News，2026-10-21
- [Tor Exit Relay Hijack: 'The Root Cause Was Ours'](https://secureworld.io/industry-news/tor-exit-relay-hijack-root-cause)：SecureWorld，2026-10-22
- [Ebury is alive but unseen](https://www.welivesecurity.com/en/eset-research/ebury-alive-unseen-400k-linux-servers-compromised-cryptotheft-financial-gain/)：ESET，2024-05-14
- [Bad relays](https://community.torproject.org/relay/community-resources/bad-relays/)：Tor Project 的壞中繼通報說明

## 相關閱讀

- [Tor Relay 架設指南](/join/setup-tor-relay/)：中間節點的安裝、torrc 設定與多個 instance 的管理
- [校園 Tor Relay 架設 SOP](/join/relay-on-campus/sop/)：SSH、防火牆與交接的設定範本
- [無狀態 Tor Relay 的部署路線與開放問題](/articles/stateless-relays/)：讓中繼主機不保留狀態、身分金鑰交給 TPM 的做法
- [Tor 中繼節點觀測](/projects/pulse/)：台灣與鄰近地區中繼的數量、頻寬與旗標變化
