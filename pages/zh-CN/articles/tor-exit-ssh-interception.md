---
title: 2026 年 10 月 Tor 出口中继遭入侵事件与运营者的安全检查
description: 2026 年 10 月初，数百个 Tor 出口中继的出口政策遭窜改，用来拦截 SSH 登录。本文整理事件经过、各项数字的计算方式与尚未厘清的问题，以及中继运营者检查、处置与预防入侵的做法。
date: 2026-10-24
---

2026 年 10 月初，数百个 Tor 出口中继的出口政策遭窜改。经由这些中继用密码登录 SSH 的人，密码可能已经外泄。目前查得最清楚的入侵途径来自受害最多的一个中继家族，攻击者用一组重复使用的密码，登录一台开放 SSH 密码登录的管理服务器。在台湾与其他地方运营中继的人，最先能做的是关闭 SSH 的密码登录，并让登录、sudo 与备份各用不同的密码。

## 事件经过

文中的时间除了另外注明以外都是 UTC，数据查证到 2026 年 10 月 24 日。第一手资料有四份：Tor Network Health 团队（Tor Project 负责监控中继网络异常的团队）在 tor-relays 邮件列表的公告、Quetzalcoatl 中继家族运营者的事后复盘、一位中继运营者的目录数据分析，以及最早公开异状的用户（以下称发现者）的文章。目录数据分析用的是 CollecTor（Tor Metrics 保存历次目录文档的存档服务）的公开数据，在 AI 工具辅助下完成。脚本与 CSV 公开在 GitHub，可以自行重现，但不是 Tor Project 的官方统计。

- **8 月 28 日**：攻击者用运营者账号的密码登录 Quetzalcoatl 家族的管理服务器，第一次尝试就成功。5 分钟内取得 root 权限后装上 Ebury（一种 OpenSSH 后门），一个多小时后再登录另一台运行出口中继的服务器，同样装上 Ebury。
- **10 月 1 日 15:33 起**：Quetzalcoatl 以外 21 位运营者的 40 个中继，在约 5 分钟内改用同一份出口政策，其中多数是重新加载配置。
- **10 月 2 日 09:27 起**：Quetzalcoatl 家族的 277 个中继全部改成另一份出口政策。发现者同一天早上（未注明时区）经由 Tor 以 SSH 连接时看到主机密钥变更的警告，用 exitmap（逐一经由每个出口连接、比对回应的扫描工具）扫描全部出口，当晚报告 Network Health 团队。
- **10 月 4 日**：01:00 的共识里，使用攻击者政策的出口占可用出口权重的 7.46%，是最高点。13:56 前后，Quetzalcoatl 家族接到 Network Health 团队的联系，停止一台主机上的 Tor。18:00 起，目录权威（directory authority，投票决定中继清单的几台服务器）陆续对受影响的中继投下 BadExit（客户端不再把它当成出口）与 MiddleOnly（只能担任中间节点）。21:00 的共识（consensus，目录权威每小时发布、列出可用中继与标记的清单）开始带有这两个标记。
- **10 月 5 日**：17:00 起，共识里已经没有使用攻击者政策的中继。17:50 Network Health 团队在 tor-relays 发布公告。
- **10 月 7 日到 22 日**：Quetzalcoatl 家族的事后复盘（10 月 7 日）、目录数据分析（10 月 9 日）与发现者的文章（10 月 20 日）陆续发布，The Hacker News 与 SecureWorld 在 10 月 21 日、22 日报道。

从发现者报告到标记生效约两天，受影响的中继完全离开共识又花了将近一天。这段期间经由 Tor 用密码登录 SSH、又接受了新的主机密钥的人，密码可能已被取走。

## 攻击者更动的设置

目录数据分析把攻击者用的出口政策分成两份。A 政策拒绝端口 25、110、143、445、3389 等，其余全部放行。B 政策是 Tor 的默认政策再多拒绝 465、587、993、995。两份政策都放行 22（SSH），也都关闭加密的收信端口 993 与 995。B 政策另外放行明文的 110 与 143，经过 B 政策出口的收信只剩明文可用。从公开数据无法判断攻击者为何关闭加密的端口。

Tor 的 `ExitRelay` 默认为 `auto`，torrc（Tor 的配置文件）只要设置了 `ExitPolicy`（或 `ReducedExitPolicy`、`IPv6Exit`），中继就会依出口政策担任出口。Network Health 团队的公告提到，攻击者取得 Linux 主机的权限之后，会把非出口中继的 torrc 改成出口。目录数据分析里有 24 个中继原本不是出口，改完之后全部取得 Exit 标记，不过多数受影响的中继本来就是出口。

只改出口政策无法拦截，连接还要被转向拦截服务器。Network Health 团队的公告请运营者检查有没有 NAT（网络地址转换）规则把端口 22 的连接转向别处。依发现者的文章，经由受影响的出口以 SSH 连接时，连接会被导到 12 台拦截服务器的其中一台。用户略过警告、继续登录之后，攻击者取得密码。攻击者再把连接转给真正的服务器，并记录用户输入的每个指令。攻击者另外开一条连接，替那台服务器装上 Ebury。

发现者用蜜罐（刻意让攻击者登录、用来观察手法的主机）观察到，拦截端取得账号密码之后会先确认账号能否使用 sudo，再运行一段 base64 编码的 Perl 安装程序。依安全公司 ESET 2024 年的报告，Ebury 是一个 OpenSSH 后门，从 2009 年起约有 40 万台服务器被它入侵。Quetzalcoatl 家族在主机上找到的是 1.8.3 版，形式是一个不属于任何软件包、带 setuid 权限的 `libkeyutils` 函数库，`libkeyutils.so.1` 的符号链接改指向它。软件包内的源文件未被修改，所以用 `dpkg -V` 与 `debsums` 都无法比对出异常。Ebury 会记下 sshd 收到的每一次密码输入，失败的尝试也算在内，后门自己的登录则不留下登录记录与 shell 历史。

## 数字的来源与差异

333、377、7.46% 与 Exit 标记数来自四种不同的算法，不能互相换算。

| 数字 | 来源 | 计算方式 |
|---|---|---|
| 333 | 发现者的文章 | 10 月 2 日用 exitmap 扫描约 3,000 个出口，十多个出口本身出示假的主机密钥，其余三百多个把连接转到 12 台拦截服务器。名单与原始数据没有公开 |
| 377 个中继、59 位运营者 | 目录数据分析 | 10 月 1 日到 4 日之间发布过 A 或 B 政策的中继，其中 277 个属于 Quetzalcoatl 家族。分析者注明这只代表政策吻合，不能证明主机被入侵 |
| 7.46% | 目录数据分析 | 10 月 4 日 01:00 的共识里，351 个受影响的可用出口占所有可用出口的共识权重 |
| 3,084 → 2,715 | Tor Metrics | 带 Exit 标记的中继数，10 月 3 日到 5 日少了 369 个，10 月 21 日是 2,688 个。事件之前就有下降的趋势，9 月 2 日是 3,235 个，10 月 1 日是 3,068 个 |

The Hacker News 把「342 个原本挡掉 SSH 的中继」与「24 个原本不是出口的中继」写成两批，依目录数据分析的算法，342 已经包含那 24 个。

## 已知的入侵途径

Quetzalcoatl 家族的运营者在事后复盘里承认问题出在自己（原文是「The root cause was ours」）。SSH 登录、sudo 与备份加密用的是同一组密码，以明文写在两台服务器的脚本里，对外的管理服务器又开放 SSH 密码登录。运营者以为脱机保管的中继主身份密钥（设置 `OfflineMasterKey` 时不放在中继主机上的长期密钥），副本放在管理服务器上的工作站备份里，加密用的正是攻击者已经取得的那组密码。

攻击者在 8 月 28 日之前从哪里取得这组密码，目前仍不清楚。ESET 那份 Ebury 报告的作者（以下称 ESET 研究人员）在邮件列表上猜测，密码是运营者从一台已经被 Ebury 入侵的主机登录时被记下的。另一台出口主机为什么接受了一把运营者找不到对应 `authorized_keys` 项目的密钥，也还没有答案。

另外 58 位运营者的中继为什么出现同样的政策、主机是否被入侵，目前都没有答案。依目录数据分析，受影响的主机集中在托管商 FranTech（品牌名 BuyVM，`AS53667`）。10 月 1 日的共识里，其他运营者放在 FranTech 的 101 个中继有 71 个受影响，放在其他网络的 9,054 个只有 13 个受影响。同时在 FranTech 与其他网络都有中继的 12 位运营者，其他网络上的 50 个中继没有一个受影响。

托管商本身被入侵是一种解释，ESET 研究人员在邮件列表上把它列为可能之一。ESET 2024 年的报告里有攻击者经由托管商的基础设施、替整批租用的服务器装上 Ebury 的案例。ESET 向其中一家被入侵的托管商租了一台虚拟主机，七天内就被装上 Ebury。分析者在 GitHub 保存库的[托管商备忘录](https://github.com/1aeo/TorExitPolicyManipulation/blob/main/collector-exit-policy-analysis/PROVIDER_MEMO.md)里，把账号密码或连接阶段被窃取、受害者集中在 FranTech 客户的假设列为最符合公开数据的一项，理由是只发生在 FranTech 的机制无法解释跨托管商的受害者。Quetzalcoatl 家族被入侵的管理服务器也在另一家托管商。也有 BuyVM 的客户在邮件列表上表示自己的虚拟主机没有异状，不认为是托管商层级的问题。

## 亚洲的受影响中继

我们用 Tor 软件包附的 GeoIP 数据库（IPFire Location）对照目录数据分析公开的 377 个中继 IP。美国 171 个、卢森堡 97 个、德国 56 个、新加坡 24 个，其余分散在克罗地亚、摩尔多瓦、荷兰、瑞士、塞舌尔与印度，台湾、日本、韩国、香港没有受影响的中继。新加坡的 24 个全部属于 Quetzalcoatl 家族，位在同一家托管商的亚洲机房，印度的 1 个属于另一位运营者。以上是我们自行比对的结果（IP 的地理位置数据库可能有误差），Tor Project 没有公布这类数据。

[Tor 中继节点观测](/projects/pulse/)的每日数字（每天最后一次快照，UTC）也记录到同样的变化。[新加坡](/projects/pulse/sg/)带 Exit 标记的中继在 10 月 3 日有 34 个，10 月 4 日剩 9 个，到 10 月 23 日是 8 个。我们推测减少的主要是上一段提到的新加坡 24 个中继。台湾的出口在同一段时间都维持在 2 到 4 个之间。

## 中继的自我检查

依 Network Health 团队的公告，Linux 上的运营者要检查：

- 在 [Relay Search](https://metrics.torproject.org/rs.html) 查找自己的中继，确认是否出现未经设置的 Exit 标记或出口政策
- 检查 torrc 与 `%include` 引入的所有文件，`ExitRelay`、`ExitPolicy`、`ContactInfo`、`MyFamily`、`Nickname` 是否被改过
- 用 `nft list ruleset` 或 `iptables -t nat -S` 找把端口 22 转向别处的 NAT 规则
- 用 `ss -tnp` 找来源不明的对外连接，监听中的进程另外用 `ss -tlnp` 列出。公告的回复帖里有人提醒，其他中继把 ORPort（中继之间互连用的端口）设在 22 是正常的，连往它们的连接不代表有问题
- 用 `debsums tor` 或 `rpm -V tor` 比对 tor 可执行文件与发行版的软件包
- 找添加的用户、`authorized_keys` 项目、cron 工作与 systemd 单元，公告里提到的一种驻留手法（让恶意程序重开机后仍会运行），是伪装成大写 `CRON` 的 root 进程
- 留意未经授权加载的内核模块、隧道接口与无法解释的内存用量

清单上的项目全部正常也不代表主机没有被入侵，Quetzalcoatl 家族的两台服务器就没有出现公告所列的 NAT 转向、新用户与密钥、cron 工作与 systemd 单元，tor 可执行文件也没被改过。运营者的建议是开机进救援系统或挂载脱机的磁盘镜像再检查。需要登录可疑的主机时只用密钥，绝不输入密码，因为 Ebury 会记下来。

事后复盘列出几项 Ebury 的痕迹（全文还列了攻击者的来源地址与三把 SSH 密钥的指纹）：

- 带 setuid 的 `libkeyutils` 文件，或 `libkeyutils.so.1` 的符号链接指向不属于任何软件包的文件（`find / -xdev -name 'libkeyutils*' -perm -4000`、`dpkg -S "$(readlink -f /usr/lib/x86_64-linux-gnu/libkeyutils.so.1)"`，RPM 系统用 `rpm -qf`）
- `/proc/net/unix` 里有 `@event-` 开头的抽象 Unix socket（不对应文件系统路径的 socket）
- `ssh.service` 的 cgroup 里有不是 sshd 的进程（`systemctl status ssh`，Ubuntu 24.04 也要看 `init.scope`）
- 日志里没有 `Requested-By:` 的 apt 交易（unattended-upgrades 本来就没有这一行）、由 uid 0 打开的 su 会话，以及 sudo 运行 `base64 -d | perl` 的记录

在运行中的系统上检查时，用户层的 rootkit 会把这些文件藏起来。ESET 公开的 [detect_ebury.sh](https://github.com/eset/malware-research/tree/master/ebury) 内置了对应的步骤，它会尝试连接 Ebury 各版本使用的抽象 Unix socket，可以连上时列出对应的版本与进程。1.8.3 版的 socket 地址在 10 月 9 日才加进 ESET 的脚本，事后复盘发布时（10 月 7 日）的脚本还无法检测这个版本。脚本的结尾也写明，没有找到 socket 不代表系统没有 Ebury，仍要对照完整的入侵指标。

Quetzalcoatl 家族也建议定期从外部比对，把 Onionoo（Tor Metrics 查找中继现况的 API）或 CollecTor 公布的出口政策、家族与 `ContactInfo`，跟自己部署的设置对照。主机被入侵时本机的文件可能被改写，已经发布的描述符（descriptor）则不会被改。

## 入侵后的处置

Network Health 团队的公告列出的处置顺序如下：

1. 让中继下线
2. 清除前先保留磁盘与日志
3. 重新安装系统，不在原系统上清理
4. 生成新的中继身份，旧的密钥视为已被窃取
5. 更换主机上出现过的每一组账号密码

Quetzalcoatl 家族补充，要更换的凭证包括每一把 SSH 密钥、每一组密码与 WireGuard 密钥。重新开机或清除前也要先倾印内存内容，他们主机上的隐藏进程就是在重新开机之后消失的。ESET 研究人员建议先倾印网络设置（`iptables-save`、`nft list ruleset`、`ip rule show`）。Ebury 会扩散到其他主机，要依被入侵主机 `~/.ssh/known_hosts` 里的记录，逐一检查那台主机连过的机器。

确认或怀疑被入侵时，发邮件到 `bad-relays@lists.torproject.org`。IP 被目录权威封锁的运营者，清理完之后也要发邮件到同一个地址，才会从封锁清单移除。

用 `FamilyId` 声明家族的运营者，要照 [FamilyId 说明页](https://community.torproject.org/relay/setup/post-install/family-ids/)的流程换掉家族密钥，否则攻击者的中继可以冒称是该运营者的家族成员。说明页写的流程是生成新密钥、拷贝到每一个中继、新旧两个 `FamilyId` 同时设置几天，再移除旧的。Quetzalcoatl 家族另外建议，曾经存放脱机主密钥的机器只要被入侵，用那把密钥的所有中继身份都要退役。

在 Debian 上用多个实例（instance）运行的中继，每个实例都有各自可以激活的 systemd 单元。Quetzalcoatl 家族的主机上，攻击者另外在开机目标里加了符号链接，所以 `systemctl disable tor` 无法阻止这些实例启动。家族的做法是用 `systemctl mask` 停用 `tor@` 单元，又因为运行中的后门可以解除 mask，主机也要下线。

## 预防入侵的做法

Tor Project 的运营者文档没有 SSH 设置的指引，下列做法整理自 Quetzalcoatl 家族的事后复盘、ESET 研究人员与 tor-relays 的讨论，属于运营者与研究人员的建议。

最优先的是关闭 SSH 的密码登录，`PasswordAuthentication` 与 `KbdInteractiveAuthentication` 都设成 `no`。后者的默认值是 `yes`，搭配 PAM（Linux 的可插拔验证模块）时仍可能出现密码提示。跳板主机（只用来转进其他服务器的管理入口）与管理服务器只接受 VPN 或白名单 IP 连入。改完设置用 `sshd -T` 确认实际生效的值。sshd 采用第一个读到的设置，VPS 镜像预先写在前面的 `PermitRootLogin yes` 会盖过后面加上的 `no`。

登录、sudo 与备份加密各用不同的账号密码，密码不写进脚本。自动化改用只能以密钥登录的账号，加上范围很窄的 `NOPASSWD` sudo。讨论中也有人建议 SSH 加上多因素验证，OpenSSH 从 8.2 版起支持 FIDO/U2F 的硬件密钥。有密码保护的私钥不算第二个因素。

管理用的服务器上不放对外的网页服务，也不放密钥备份。Quetzalcoatl 家族的管理服务器上有一套曾经暴露在网络上的 WireGuard 管理接口，版本有未验证即可读取文件的漏洞（`CVE-2026-44343`）。运营者后来排除这个漏洞是入侵入口的可能，仍把它列为要避免的做法。

脱机主密钥要真的脱机，不能留在任何连网机器的备份里。日志转送到另一台主机保存，sshd 的 `LogLevel` 被调到 INFO 以下时发出警报。用 AIDE（文件完整性检查工具）这类工具，监控函数库目录里不属于任何软件包或带 setuid 的文件。

社区的[校园中继 SOP](/join/relay-on-campus/sop/)（标准作业程序）里已经规定只允许密钥登录、SSH 只开放校内 VPN 网段，也建议密钥备份两份以上，其中一份放在指导教授的实验室。对照这次的经验，那一份应该放在脱机的媒体上。SOP 的事故处置一节已依 Network Health 团队的公告修订。无法排除入侵时，旧的身份密钥一律视为已外泄，要生成新的中继身份。

## 经由 Tor 使用 SSH 的人

主机密钥改变时，OpenSSH 会警告并停用密码验证，`StrictHostKeyChecking` 维持默认的 `ask` 时会直接拒绝连接。用户自行删掉 `known_hosts` 里的旧记录之后，ssh 没有旧记录可以比对，才会走到输入密码这一步。第一次连接的服务器没有旧记录可以比对，用户只看到一般的确认提示。第一次连接时要用其他渠道核对指纹，例如请管理员提供。用 SSHFP 记录（在 DNS 公布主机密钥指纹的记录）比对时，要设置 `VerifyHostKeyDNS`，而且只有通过 DNSSEC（替 DNS 回应加上签名的机制）验证的记录才会被自动信任。

发现者公开了其中一台拦截服务器的 ED25519 指纹 `SHA256:6baCZCPsl+AfQuujUS81fMEE/C7UeJ+AwjrImqmDB3E`，接受过陌生密钥的人可以用 `ssh-keygen -lf ~/.ssh/known_hosts` 列出已保存的指纹比对。其他拦截服务器可能用不同的密钥，没有相同的指纹也不代表没有受影响。

依 The Hacker News 根据 `RFC 4252`（SSH 验证协议的规格）所做的推论，只有用密码登录的人会被取走账号密码。公开密钥验证的签名包含这一次连接的识别码，拦截者无法用它登录真正的服务器。密码则会在加密通道里以明文送给对方，而对方就是拦截者。报道也提到，拦截者仍可以接受密钥登录、显示假的 shell，我们推论在假 shell 里输入的 sudo 密码一样可能外泄。

The Hacker News 列出的可能受害者，是 10 月 1 日到 5 日之间经由 Tor 用密码登录、而且接受了陌生或已变更主机密钥的人（报道里没有注明时区），四份第一手资料里都没有这个范围。起点只能当参考，Quetzalcoatl 家族的服务器在 9 月 30 日就出现用途不明的隐藏进程。Tor 论坛在 8 月 31 日也有一则经由 Tor 以 SSH 连接时看到主机密钥警告的反馈，没有指出是哪个出口，我们查到的数据也没有把它与这起事件连起来。

10 月初前后经由 Tor 用密码登录 SSH、而且接受过新的或已变更的主机密钥的人，要把密码视为已经外泄。被登录的服务器可能已经被装上 Ebury，确认之前不要在上面输入任何密码，换新密码也一样。先用密钥登录或从救援系统检查，再换掉所有用过那组密码的地方。

要经由 Tor 管理服务器时，可以把 SSH 设成 onion 服务（onion service，网址以 .onion 结尾、只能经由 Tor 连上的服务）。连接在 Tor 网络内就到达服务器，不经过出口中继。设置方式见[.onion 服务架设指南](/join/setup-onion-service/)，客户端再用 `torsocks` 或 ssh 的 `ProxyCommand` 经由 Tor 连接。

## 还没有答案的问题

Quetzalcoatl 以外 58 位运营者的中继如何被窜改，到 10 月 24 日仍没有公开数据。Network Health 团队的公告提到的 NAT 转向与假 `CRON` 进程，跟 Quetzalcoatl 家族主机上的 Ebury 是否出自同一批人，也还不清楚。被偷走的账号密码送到哪里、10 月 9 日之后是否还有中继被改，目前都没有数据。ESET 研究人员在邮件列表上提醒，很可能还有其他被入侵的 Tor 中继没被发现。发现者依攻击者大量收集未加密数据的做法，推测是以金钱为目的的犯罪集团，也写明那只是推测。

发现自己的中继有异状时，发邮件到 `bad-relays@lists.torproject.org`，也欢迎到社区的 [Matrix](/contact/) 一起讨论。

## 参考资料

- [Security incident affecting some relay operators](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/WOHPLKCSHYXFTBRZXDENDKJZMBMPLMG5/)：Tor Network Health 团队的公告，2026-10-05
- [Ebury 1.8.3 on two Quetzalcoatl relay servers: timeline, lessons, open questions](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/QHRD6YOX6RZRDR7NCHNDO7GLCEA6VFM6/)：Quetzalcoatl 家族的事后复盘，2026-10-07
- [ESET 研究人员的回复](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/RXWGWYYYKBDEBNXC2C3NYIQ2HHHWXL7O/)：tor-relays，2026-10-08
- [目录数据分析](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/message/Z2B6XYKJZBBQADU77MSNL6FJP7MHZHIV/)：tor-relays，2026-10-09，脚本与数据在 [1aeo/TorExitPolicyManipulation](https://github.com/1aeo/TorExitPolicyManipulation)
- [How I got over 300 Tor exit nodes removed](https://kaba.cx/posts/20261020_Tor/)：发现者的文章，2026-10-20
- [Attackers Hijacked Over 300 Tor Exit Relays to Intercept SSH Connections](https://thehackernews.com/2026/10/attackers-hijacked-over-300-tor-exit.html)：The Hacker News，2026-10-21
- [Tor Exit Relay Hijack: 'The Root Cause Was Ours'](https://secureworld.io/industry-news/tor-exit-relay-hijack-root-cause)：SecureWorld，2026-10-22
- [Ebury is alive but unseen](https://www.welivesecurity.com/en/eset-research/ebury-alive-unseen-400k-linux-servers-compromised-cryptotheft-financial-gain/)：ESET，2024-05-14
- [Bad relays](https://community.torproject.org/relay/community-resources/bad-relays/)：Tor Project 的坏中继报告说明

## 相关阅读

- [Tor Relay 架设指南](/join/setup-tor-relay/)：中间节点的安装、torrc 设置与多个 instance 的管理
- [校园 Tor Relay 架设 SOP](/join/relay-on-campus/sop/)：SSH、防火墙与交接的设置范本
- [无状态 Tor Relay 的部署路线与开放问题](/articles/stateless-relays/)：让中继主机不保留状态、身份密钥交给 TPM 的做法
- [Tor 中继节点观测](/projects/pulse/)：台湾与邻近地区中继的数量、带宽与标记变化
