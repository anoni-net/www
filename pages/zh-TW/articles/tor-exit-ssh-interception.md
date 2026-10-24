---
title: 2026 年 10 月 Tor 出口中繼遭入侵事件與營運者的安全檢查
description: 2026 年 10 月初，數百個 Tor 出口中繼的出口政策遭竄改，用來攔截 SSH 登入。本文整理事件經過、各項數字的計算方式與尚未釐清的問題，以及中繼營運者檢查、處置與預防入侵的做法。
date: 2026-10-24
---

2026 年 10 月初，數百個 Tor 出口中繼的出口政策遭竄改。經由這些中繼用密碼登入 SSH 的人，密碼可能已經外洩。目前查得最清楚的入侵途徑來自受害最多的一個中繼家族，攻擊者用一組重複使用的密碼，登入一台開放 SSH 密碼登入的管理伺服器。在台灣與其他地方營運中繼的人，最先能做的是關閉 SSH 的密碼登入，並讓登入、sudo 與備份各用不同的密碼。

## 事件經過

文中的時間除了另外註明以外都是 UTC，資料查證到 2026 年 10 月 24 日。第一手資料有四份：Tor Network Health 團隊（Tor Project 負責監看中繼網路異常的團隊）在 tor-relays 郵件列表的公告、Quetzalcoatl 中繼家族營運者的事後檢討、一位中繼營運者的目錄資料分析，以及最早公開異狀的使用者（以下稱發現者）的文章。目錄資料分析用的是 CollecTor（Tor Metrics 保存歷次目錄文件的封存服務）的公開資料，在 AI 工具輔助下完成。腳本與 CSV 公開在 GitHub，可以自行重現，但不是 Tor Project 的官方統計。

- **8 月 28 日**：攻擊者用營運者帳號的密碼登入 Quetzalcoatl 家族的管理伺服器，第一次嘗試就成功。5 分鐘內取得 root 權限後裝上 Ebury（一種 OpenSSH 後門），一個多小時後再登入另一台運作出口中繼的伺服器，同樣裝上 Ebury。
- **10 月 1 日 15:33 起**：Quetzalcoatl 以外 21 位營運者的 40 個中繼，在約 5 分鐘內改用同一份出口政策，其中多數是重新載入設定。
- **10 月 2 日 09:27 起**：Quetzalcoatl 家族的 277 個中繼全部改成另一份出口政策。發現者同一天早上（未註明時區）經由 Tor 以 SSH 連線時看到主機金鑰變更的警告，用 exitmap（逐一經由每個出口連線、比對回應的掃描工具）掃描全部出口，當晚通報 Network Health 團隊。
- **10 月 4 日**：01:00 的共識裡，使用攻擊者政策的出口占可用出口權重的 7.46%，是最高點。13:56 前後，Quetzalcoatl 家族接到 Network Health 團隊的聯絡，停止一台主機上的 Tor。18:00 起，目錄授權（directory authority，投票決定中繼清單的幾台伺服器）陸續對受影響的中繼投下 BadExit（客戶端不再把它當成出口）與 MiddleOnly（只能擔任中間節點）。21:00 的共識（consensus，目錄授權每小時發布、列出可用中繼與旗標的清單）開始帶有這兩個旗標。
- **10 月 5 日**：17:00 起，共識裡已經沒有使用攻擊者政策的中繼。17:50 Network Health 團隊在 tor-relays 發布公告。
- **10 月 7 日到 22 日**：Quetzalcoatl 家族的事後檢討（10 月 7 日）、目錄資料分析（10 月 9 日）與發現者的文章（10 月 20 日）陸續發布，The Hacker News 與 SecureWorld 在 10 月 21 日、22 日報導。

從發現者通報到旗標生效約兩天，受影響的中繼完全離開共識又花了將近一天。這段期間經由 Tor 用密碼登入 SSH、又接受了新的主機金鑰的人，密碼可能已被取走。

## 攻擊者更動的設定

目錄資料分析把攻擊者用的出口政策分成兩份。A 政策拒絕連接埠 25、110、143、445、3389 等，其餘全部放行。B 政策是 Tor 的預設政策再多拒絕 465、587、993、995。兩份政策都放行 22（SSH），也都關閉加密的收信連接埠 993 與 995。B 政策另外放行明文的 110 與 143，經過 B 政策出口的收信只剩明文可用。從公開資料無法判斷攻擊者為何關閉加密的連接埠。

Tor 的 `ExitRelay` 預設為 `auto`，torrc（Tor 的設定檔）只要設定了 `ExitPolicy`（或 `ReducedExitPolicy`、`IPv6Exit`），中繼就會依出口政策擔任出口。Network Health 團隊的公告提到，攻擊者取得 Linux 主機的權限之後，會把非出口中繼的 torrc 改成出口。目錄資料分析裡有 24 個中繼原本不是出口，改完之後全部取得 Exit 旗標，不過多數受影響的中繼本來就是出口。

只改出口政策無法攔截，連線還要被轉向攔截伺服器。Network Health 團隊的公告請營運者檢查有沒有 NAT（網路位址轉換）規則把連接埠 22 的連線轉向別處。依發現者的文章，經由受影響的出口以 SSH 連線時，連線會被導到 12 台攔截伺服器的其中一台。使用者略過警告、繼續登入之後，攻擊者取得密碼。攻擊者再把連線轉給真正的伺服器，並記錄使用者輸入的每個指令。攻擊者另外開一條連線，替那台伺服器裝上 Ebury。

發現者用蜜罐（刻意讓攻擊者登入、用來觀察手法的主機）觀察到，攔截端取得帳號密碼之後會先確認帳號能否使用 sudo，再執行一段 base64 編碼的 Perl 安裝程式。依資安公司 ESET 2024 年的報告，Ebury 是一個 OpenSSH 後門，從 2009 年起約有 40 萬台伺服器被它入侵。Quetzalcoatl 家族在主機上找到的是 1.8.3 版，形式是一個不屬於任何套件、帶 setuid 權限的 `libkeyutils` 函式庫，`libkeyutils.so.1` 的符號連結改指向它。套件內的原始檔未被修改，所以用 `dpkg -V` 與 `debsums` 都無法比對出異常。Ebury 會記下 sshd 收到的每一次密碼輸入，失敗的嘗試也算在內，後門自己的登入則不留下登入紀錄與 shell 歷史。

## 數字的來源與差異

333、377、7.46% 與 Exit 旗標數來自四種不同的算法，不能互相換算。

| 數字 | 來源 | 計算方式 |
|---|---|---|
| 333 | 發現者的文章 | 10 月 2 日用 exitmap 掃描約 3,000 個出口，十多個出口本身出示假的主機金鑰，其餘三百多個把連線轉到 12 台攔截伺服器。名單與原始資料沒有公開 |
| 377 個中繼、59 位營運者 | 目錄資料分析 | 10 月 1 日到 4 日之間發布過 A 或 B 政策的中繼，其中 277 個屬於 Quetzalcoatl 家族。分析者註明這只代表政策吻合，不能證明主機被入侵 |
| 7.46% | 目錄資料分析 | 10 月 4 日 01:00 的共識裡，351 個受影響的可用出口占所有可用出口的共識權重 |
| 3,084 → 2,715 | Tor Metrics | 帶 Exit 旗標的中繼數，10 月 3 日到 5 日少了 369 個，10 月 21 日是 2,688 個。事件之前就有下降的趨勢，9 月 2 日是 3,235 個，10 月 1 日是 3,068 個 |

The Hacker News 把「342 個原本擋掉 SSH 的中繼」與「24 個原本不是出口的中繼」寫成兩批，依目錄資料分析的算法，342 已經包含那 24 個。

## 已知的入侵途徑

Quetzalcoatl 家族的營運者在事後檢討裡承認問題出在自己（原文是「The root cause was ours」）。SSH 登入、sudo 與備份加密用的是同一組密碼，以明文寫在兩台伺服器的腳本裡，對外的管理伺服器又開放 SSH 密碼登入。營運者以為離線保管的中繼主身分金鑰（設定 `OfflineMasterKey` 時不放在中繼主機上的長期金鑰），副本放在管理伺服器上的工作站備份裡，加密用的正是攻擊者已經取得的那組密碼。

攻擊者在 8 月 28 日之前從哪裡取得這組密碼，目前仍不清楚。ESET 那份 Ebury 報告的作者（以下稱 ESET 研究人員）在郵件列表上猜測，密碼是營運者從一台已經被 Ebury 入侵的主機登入時被記下的。另一台出口主機為什麼接受了一把營運者找不到對應 `authorized_keys` 項目的金鑰，也還沒有答案。

另外 58 位營運者的中繼為什麼出現同樣的政策、主機是否被入侵，目前都沒有答案。依目錄資料分析，受影響的主機集中在託管商 FranTech（品牌名 BuyVM，`AS53667`）。10 月 1 日的共識裡，其他營運者放在 FranTech 的 101 個中繼有 71 個受影響，放在其他網路的 9,054 個只有 13 個受影響。同時在 FranTech 與其他網路都有中繼的 12 位營運者，其他網路上的 50 個中繼沒有一個受影響。

託管商本身被入侵是一種解釋，ESET 研究人員在郵件列表上把它列為可能之一。ESET 2024 年的報告裡有攻擊者經由託管商的基礎設施、替整批租用的伺服器裝上 Ebury 的案例。ESET 向其中一家被入侵的託管商租了一台虛擬主機，七天內就被裝上 Ebury。分析者在 GitHub 儲存庫的[託管商備忘錄](https://github.com/1aeo/TorExitPolicyManipulation/blob/main/collector-exit-policy-analysis/PROVIDER_MEMO.md)裡，把帳號密碼或連線階段被竊取、受害者集中在 FranTech 客戶的假設列為最符合公開資料的一項，理由是只發生在 FranTech 的機制無法解釋跨託管商的受害者。Quetzalcoatl 家族被入侵的管理伺服器也在另一家託管商。也有 BuyVM 的客戶在郵件列表上表示自己的虛擬主機沒有異狀，不認為是託管商層級的問題。

## 亞洲的受影響中繼

我們用 Tor 套件附的 GeoIP 資料庫（IPFire Location）對照目錄資料分析公開的 377 個中繼 IP。美國 171 個、盧森堡 97 個、德國 56 個、新加坡 24 個，其餘分散在克羅埃西亞、摩爾多瓦、荷蘭、瑞士、塞席爾與印度，台灣、日本、南韓、香港沒有受影響的中繼。新加坡的 24 個全部屬於 Quetzalcoatl 家族，位在同一家託管商的亞洲機房，印度的 1 個屬於另一位營運者。以上是我們自行比對的結果（IP 的地理位置資料庫可能有誤差），Tor Project 沒有公布這類資料。

[Tor 中繼節點觀測](/projects/pulse/)的每日數字（每天最後一次快照，UTC）也記錄到同樣的變化。[新加坡](/projects/pulse/sg/)帶 Exit 旗標的中繼在 10 月 3 日有 34 個，10 月 4 日剩 9 個，到 10 月 23 日是 8 個。我們推測減少的主要是上一段提到的新加坡 24 個中繼。台灣的出口在同一段時間都維持在 2 到 4 個之間。

## 中繼的自我檢查

依 Network Health 團隊的公告，Linux 上的營運者要檢查：

- 在 [Relay Search](https://metrics.torproject.org/rs.html) 查詢自己的中繼，確認是否出現未經設定的 Exit 旗標或出口政策
- 檢查 torrc 與 `%include` 引入的所有檔案，`ExitRelay`、`ExitPolicy`、`ContactInfo`、`MyFamily`、`Nickname` 是否被改過
- 用 `nft list ruleset` 或 `iptables -t nat -S` 找把連接埠 22 轉向別處的 NAT 規則
- 用 `ss -tnp` 找來源不明的對外連線，監聽中的程序另外用 `ss -tlnp` 列出。公告的回覆串裡有人提醒，其他中繼把 ORPort（中繼之間互連用的連接埠）設在 22 是正常的，連往它們的連線不代表有問題
- 用 `debsums tor` 或 `rpm -V tor` 比對 tor 執行檔與發行版的套件
- 找新增的使用者、`authorized_keys` 項目、cron 工作與 systemd 單元，公告裡提到的一種常駐手法（讓惡意程式重開機後仍會執行），是偽裝成大寫 `CRON` 的 root 程序
- 留意未經授權載入的核心模組、通道介面與無法解釋的記憶體用量

清單上的項目全部正常也不代表主機沒有被入侵，Quetzalcoatl 家族的兩台伺服器就沒有出現公告所列的 NAT 轉向、新使用者與金鑰、cron 工作與 systemd 單元，tor 執行檔也沒被改過。營運者的建議是開機進救援系統或掛載離線的磁碟映像再檢查。需要登入可疑的主機時只用金鑰，絕不輸入密碼，因為 Ebury 會記下來。

事後檢討列出幾項 Ebury 的痕跡（全文還列了攻擊者的來源位址與三把 SSH 金鑰的指紋）：

- 帶 setuid 的 `libkeyutils` 檔案，或 `libkeyutils.so.1` 的符號連結指向不屬於任何套件的檔案（`find / -xdev -name 'libkeyutils*' -perm -4000`、`dpkg -S "$(readlink -f /usr/lib/x86_64-linux-gnu/libkeyutils.so.1)"`，RPM 系統用 `rpm -qf`）
- `/proc/net/unix` 裡有 `@event-` 開頭的抽象 Unix socket（不對應檔案系統路徑的 socket）
- `ssh.service` 的 cgroup 裡有不是 sshd 的程序（`systemctl status ssh`，Ubuntu 24.04 也要看 `init.scope`）
- 日誌裡沒有 `Requested-By:` 的 apt 交易（unattended-upgrades 本來就沒有這一行）、由 uid 0 開啟的 su 工作階段，以及 sudo 執行 `base64 -d | perl` 的紀錄

在運作中的系統上檢查時，使用者層的 rootkit 會把這些檔案藏起來。ESET 公開的 [detect_ebury.sh](https://github.com/eset/malware-research/tree/master/ebury) 內建了因應的步驟，它會嘗試連線 Ebury 各版本使用的抽象 Unix socket，可以連上時列出對應的版本與程序。1.8.3 版的 socket 位址在 10 月 9 日才加進 ESET 的腳本，事後檢討發布時（10 月 7 日）的腳本還無法偵測這個版本。腳本的結尾也寫明，沒有找到 socket 不代表系統沒有 Ebury，仍要對照完整的入侵指標。

Quetzalcoatl 家族也建議定期從外部比對，把 Onionoo（Tor Metrics 查詢中繼現況的 API）或 CollecTor 公布的出口政策、家族與 `ContactInfo`，跟自己部署的設定對照。主機被入侵時本機的檔案可能被改寫，已經發布的描述檔（descriptor）則不會被改。

## 入侵後的處置

Network Health 團隊的公告列出的處置順序如下：

1. 讓中繼下線
2. 清除前先保留磁碟與日誌
3. 重新安裝系統，不在原系統上清理
4. 產生新的中繼身分，舊的金鑰視為已被竊取
5. 更換主機上出現過的每一組帳號密碼

Quetzalcoatl 家族補充，要更換的憑證包括每一把 SSH 金鑰、每一組密碼與 WireGuard 金鑰。重新開機或清除前也要先傾印記憶體內容，他們主機上的隱藏程序就是在重新開機之後消失的。ESET 研究人員建議先傾印網路設定（`iptables-save`、`nft list ruleset`、`ip rule show`）。Ebury 會擴散到其他主機，要依被入侵主機 `~/.ssh/known_hosts` 裡的紀錄，逐一檢查那台主機連過的機器。

確認或懷疑被入侵時，寫信到 `bad-relays@lists.torproject.org`。IP 被目錄授權封鎖的營運者，清理完之後也要寫信到同一個地址，才會從封鎖清單移除。

用 `FamilyId` 宣告家族的營運者，要照 [FamilyId 說明頁](https://community.torproject.org/relay/setup/post-install/family-ids/)的程序換掉家族金鑰，否則攻擊者的中繼可以冒稱是該營運者的家族成員。說明頁寫的程序是產生新金鑰、複製到每一個中繼、新舊兩個 `FamilyId` 同時設定幾天，再移除舊的。Quetzalcoatl 家族另外建議，曾經存放離線主金鑰的機器只要被入侵，用那把金鑰的所有中繼身分都要退役。

在 Debian 上用多個執行個體（instance）運作的中繼，每個執行個體都有各自可以啟用的 systemd 單元。Quetzalcoatl 家族的主機上，攻擊者另外在開機目標裡加了符號連結，所以 `systemctl disable tor` 無法阻止這些執行個體啟動。家族的做法是用 `systemctl mask` 停用 `tor@` 單元，又因為運作中的後門可以解除 mask，主機也要下線。

## 預防入侵的做法

Tor Project 的營運者文件沒有 SSH 設定的指引，下列做法整理自 Quetzalcoatl 家族的事後檢討、ESET 研究人員與 tor-relays 的討論，屬於營運者與研究人員的建議。

最優先的是關閉 SSH 的密碼登入，`PasswordAuthentication` 與 `KbdInteractiveAuthentication` 都設成 `no`。後者的預設值是 `yes`，搭配 PAM（Linux 的可插拔驗證模組）時仍可能出現密碼提示。跳板主機（只用來轉進其他伺服器的管理入口）與管理伺服器只接受 VPN 或白名單 IP 連入。改完設定用 `sshd -T` 確認實際生效的值。sshd 採用第一個讀到的設定，VPS 映像檔預先寫在前面的 `PermitRootLogin yes` 會蓋過後面加上的 `no`。

登入、sudo 與備份加密各用不同的帳號密碼，密碼不寫進腳本。自動化改用只能以金鑰登入的帳號，加上範圍很窄的 `NOPASSWD` sudo。討論中也有人建議 SSH 加上多因素驗證，OpenSSH 從 8.2 版起支援 FIDO/U2F 的硬體金鑰。有密碼保護的私鑰不算第二個因素。

管理用的伺服器上不放對外的網頁服務，也不放金鑰備份。Quetzalcoatl 家族的管理伺服器上有一套曾經暴露在網路上的 WireGuard 管理介面，版本有未驗證即可讀取檔案的漏洞（`CVE-2026-44343`）。營運者後來排除這個漏洞是入侵入口的可能，仍把它列為要避免的做法。

離線主金鑰要真的離線，不能留在任何連網機器的備份裡。日誌轉送到另一台主機保存，sshd 的 `LogLevel` 被調到 INFO 以下時發出警報。用 AIDE（檔案完整性檢查工具）這類工具，監看函式庫目錄裡不屬於任何套件或帶 setuid 的檔案。

社群的[校園中繼 SOP](/join/relay-on-campus/sop/)（標準作業程序）裡已經規定只允許金鑰登入、SSH 只開放校內 VPN 網段，也建議金鑰備份兩份以上，其中一份放在指導教授的實驗室。對照這次的經驗，那一份應該放在離線的媒體上。SOP 的事故處置一節已依 Network Health 團隊的公告修訂。無法排除入侵時，舊的身分金鑰一律視為已外洩，要產生新的中繼身分。

## 經由 Tor 使用 SSH 的人

主機金鑰改變時，OpenSSH 會警告並停用密碼驗證，`StrictHostKeyChecking` 維持預設的 `ask` 時會直接拒絕連線。使用者自行刪掉 `known_hosts` 裡的舊紀錄之後，ssh 沒有舊紀錄可以比對，才會走到輸入密碼這一步。第一次連線的伺服器沒有舊紀錄可以比對，使用者只看到一般的確認提示。第一次連線時要用其他管道核對指紋，例如請管理者提供。用 SSHFP 紀錄（在 DNS 公布主機金鑰指紋的紀錄）比對時，要設定 `VerifyHostKeyDNS`，而且只有通過 DNSSEC（替 DNS 回應加上簽章的機制）驗證的紀錄才會被自動信任。

發現者公開了其中一台攔截伺服器的 ED25519 指紋 `SHA256:6baCZCPsl+AfQuujUS81fMEE/C7UeJ+AwjrImqmDB3E`，接受過陌生金鑰的人可以用 `ssh-keygen -lf ~/.ssh/known_hosts` 列出已儲存的指紋比對。其他攔截伺服器可能用不同的金鑰，沒有相同的指紋也不代表沒有受影響。

依 The Hacker News 根據 `RFC 4252`（SSH 驗證協定的規格）所做的推論，只有用密碼登入的人會被取走帳號密碼。公開金鑰驗證的簽章包含這一次連線的識別碼，攔截者無法用它登入真正的伺服器。密碼則會在加密通道裡以明文送給對方，而對方就是攔截者。報導也提到，攔截者仍可以接受金鑰登入、顯示假的 shell，我們推論在假 shell 裡輸入的 sudo 密碼一樣可能外洩。

The Hacker News 列出的可能受害者，是 10 月 1 日到 5 日之間經由 Tor 用密碼登入、而且接受了陌生或已變更主機金鑰的人（報導裡沒有註明時區），四份第一手資料裡都沒有這個範圍。起點只能當參考，Quetzalcoatl 家族的伺服器在 9 月 30 日就出現用途不明的隱藏程序。Tor 論壇在 8 月 31 日也有一則經由 Tor 以 SSH 連線時看到主機金鑰警告的回報，沒有指出是哪個出口，我們查到的資料也沒有把它與這起事件連起來。

10 月初前後經由 Tor 用密碼登入 SSH、而且接受過新的或已變更的主機金鑰的人，要把密碼視為已經外洩。被登入的伺服器可能已經被裝上 Ebury，確認之前不要在上面輸入任何密碼，換新密碼也一樣。先用金鑰登入或從救援系統檢查，再換掉所有用過那組密碼的地方。

要經由 Tor 管理伺服器時，可以把 SSH 設成洋蔥服務（onion service，網址以 .onion 結尾、只能經由 Tor 連上的服務）。連線在 Tor 網路內就到達伺服器，不經過出口中繼。設定方式見[.onion 服務架設指南](/join/setup-onion-service/)，客戶端再用 `torsocks` 或 ssh 的 `ProxyCommand` 經由 Tor 連線。

## 還沒有答案的問題

Quetzalcoatl 以外 58 位營運者的中繼如何被竄改，到 10 月 24 日仍沒有公開資料。Network Health 團隊的公告提到的 NAT 轉向與假 `CRON` 程序，跟 Quetzalcoatl 家族主機上的 Ebury 是否出自同一批人，也還不清楚。被偷走的帳號密碼送到哪裡、10 月 9 日之後是否還有中繼被改，目前都沒有資料。ESET 研究人員在郵件列表上提醒，很可能還有其他被入侵的 Tor 中繼沒被發現。發現者依攻擊者大量收集未加密資料的做法，推測是以金錢為目的的犯罪集團，也寫明那只是推測。

發現自己的中繼有異狀時，寫信到 `bad-relays@lists.torproject.org`，也歡迎到社群的 [Matrix](/contact/) 一起討論。

## 參考資料

- [Security incident affecting some relay operators](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/WOHPLKCSHYXFTBRZXDENDKJZMBMPLMG5/)：Tor Network Health 團隊的公告，2026-10-05
- [Ebury 1.8.3 on two Quetzalcoatl relay servers: timeline, lessons, open questions](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/QHRD6YOX6RZRDR7NCHNDO7GLCEA6VFM6/)：Quetzalcoatl 家族的事後檢討，2026-10-07
- [ESET 研究人員的回覆](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/RXWGWYYYKBDEBNXC2C3NYIQ2HHHWXL7O/)：tor-relays，2026-10-08
- [目錄資料分析](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/message/Z2B6XYKJZBBQADU77MSNL6FJP7MHZHIV/)：tor-relays，2026-10-09，腳本與資料在 [1aeo/TorExitPolicyManipulation](https://github.com/1aeo/TorExitPolicyManipulation)
- [How I got over 300 Tor exit nodes removed](https://kaba.cx/posts/20261020_Tor/)：發現者的文章，2026-10-20
- [Attackers Hijacked Over 300 Tor Exit Relays to Intercept SSH Connections](https://thehackernews.com/2026/10/attackers-hijacked-over-300-tor-exit.html)：The Hacker News，2026-10-21
- [Tor Exit Relay Hijack: 'The Root Cause Was Ours'](https://secureworld.io/industry-news/tor-exit-relay-hijack-root-cause)：SecureWorld，2026-10-22
- [Ebury is alive but unseen](https://www.welivesecurity.com/en/eset-research/ebury-alive-unseen-400k-linux-servers-compromised-cryptotheft-financial-gain/)：ESET，2024-05-14
- [Bad relays](https://community.torproject.org/relay/community-resources/bad-relays/)：Tor Project 的壞中繼通報說明

## 相關閱讀

- [Tor Relay 架設指南](/join/setup-tor-relay/)：中間節點的安裝、torrc 設定與多個 instance 的管理
- [校園 Tor Relay 架設 SOP](/join/relay-on-campus/sop/)：SSH、防火牆與交接的設定範本
- [無狀態 Tor Relay 的部署路線與開放問題](/articles/stateless-relays/)：讓中繼主機不保留狀態、身分金鑰交給 TPM 的做法
- [Tor 中繼節點觀測](/projects/pulse/)：台灣與鄰近地區中繼的數量、頻寬與旗標變化
