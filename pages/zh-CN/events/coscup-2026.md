---
title: COSCUP 2026 匿名网络社区议程轨
description: 匿名网络社区 anoni.net 2026 年 8 月 8、9 日在 COSCUP 2026（国立台湾科技大学）的两日议程与工作坊记录，主题涵盖 Tor、Tails、OONI、浏览器追踪、校园 Tor 节点、个人信息权利、隐私指南与匿名支付。
---

![COSCUP 2026 匿名网络社区议程轨主视觉](https://assets.anoni.net/event/anoni-net-eth-taipei.webp){ .shot }

记者需要保护消息来源，公民团体需要保护成员与捐款人，开发者想确认手上的工具能抵挡监控。也有一般人被诈骗短信与广告追踪困扰，想多掌握自己的数据。四种需求牵涉同一组风险，包括通信遭拦截、身份被追踪，以及从一笔转账的时间与金额反推出整张关系网。组织的成员名单与金流，也可能在当事人不知情时曝光。

匿名网络社区 anoni.net 在 COSCUP 2026 开设两天的社区议程轨，内容来自社区这一年在 [Tor](docs:tools/what-is-tor/)、[Tails](docs:tools/what-is-tails/)、[OONI](docs:tools/what-is-ooni/)、个人隐私与匿名支付的实践经验。议程从网络与审查的运作原理开始，涵盖开源隐私工具的实际运用、校园 Tor 节点、浏览器追踪、健保数据库的个人信息权利，以及与 ETHTaipei 合办的匿名支付场。前三场导论由社区成员主讲，其余为邀请、合办与录取议程。

!!! info "活动信息"

    - 日期：2026/08/08（六）、2026/08/09（日）
    - 地点：国立台湾科技大学（NTUST），社区议程轨在 `TR-510`，8/08 下午与 ETHTaipei 合办场在 `TR-511`
    - 形式：社区议程、实操工作坊，以及与 ETHTaipei 合办的匿名支付场
    - 入场：COSCUP 免费入场，社区议程轨不需另外报名（实际时间以 [COSCUP 官方议程](https://pretalx.coscup.org/coscup-2026/) 为准）
    - 状态：活动已经结束，本页保留议程、各场介绍与讲者幻灯片作为记录
    - 幻灯片：讲者提供的幻灯片与录影附在[议程总览](#议程总览)各场的说明下方，著作权属于各讲者，转载或改作前请先取得讲者同意（另外标示授权的依标示）

[前往 COSCUP 2026 议程](#议程总览){ .btn .solid }

!!! tip "免费入场、免报名的匿名参加方式"

    COSCUP 免费入场，社区议程轨也不需事先报名，听众当天走进教室即可参与。对推广匿名的社区来说，参加方式本身也能匿名，听议程不必留下任何个人信息。

!!! tip "依听众身份的建议场次"

    - **新闻媒体、独立记者**：8/08 上午的「现实世界的开源隐私工具」整理记者实际使用的安全收件渠道、去标识化与隔离工具，可搭配「威胁模型与 Metadata 入门」。8/09 下午有「浏览器追踪技术、反追踪策略」，谈浏览器如何泄漏用户联系过谁，「健保数据库案之后」与「隐私指南 2026」再延伸到个人信息权利与法律调取数据的因应（延伸阅读：[记者保护消息来源](docs:scenarios/journalist/)）。
    - **公民团体、NGO**：8/08 上午的四场导论最贴近组织处境，其中「现实世界的开源隐私工具」整理公民团体与 NGO 使用的加密通信、内部协作与举报投递工具。「毒品非毒、洗钱非洗钱」探讨受助者或举报者如何证明自己符合条件，又不留下身份数据，8/09 的「隐私指南 2026」涵盖组织遭法律调取数据时的事前准备。评估匿名捐款渠道时，8/08 下午合办场的「我不洗钱，为何要理解匿名支付？」是白话入门，不需要加密货币背景。
    - **开源、科技社区**：8/09 的技术含量最高，OpenWRT、台师大 Tor 节点与浏览器指纹研究都有实操内容。8/08 下午的零知识证明（ZK）自然人凭证、隐私保护的 KYC（金融机构确认客户身份的程序）与隐匿地址，是协议层最扎实的内容。想参与贡献见[参与](/join/)。

## <i data-icon="calendar-text"></i> 议程总览 { #议程总览 }

社区议程轨的时间与题目如下，实际时间以 [COSCUP 官方议程](https://pretalx.coscup.org/coscup-2026/) 为准。场次之间有换场休息，8/08 上午每场间隔 10 分钟，8/09 议程较满，间隔 5 分钟。各场摘要见[议程介绍](#议程介绍)。

### Day 1：2026/08/08（六）

8/08 上午是四场开源匿名网络导论，前三场由 anoni.net 社区成员主讲，第四场为邀请议程。四场都从入门角度切入，以开源工具为主轴，适合公民团体、新闻媒体与独立记者。下午 13:00 起是与 ETHTaipei 合办的「匿名支付」场，协议层的技术内容较多。

**上午 09:30-12:00　开源匿名网络导论（教室 `TR-510`）**

| 时间 | 议程 | 讲者 |
|------|------|------|
| 09:30-10:00<br>30 分钟 | <span class="tag tag--basic">通用</span> <i data-icon="account-group"></i> **匿名网络社区 anoni.net 介绍：开源匿名工具、社区实践与 2026 三大主题**<br><i data-icon="arrow-right-bottom"></i> 社区在台湾将 Tor、Tails、OONI 等隐私工具中文化并推广，场次介绍社区的组成与工作，以及高风险工作为何需要能检验源代码的开源工具<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/anoni-net-intro.pdf) | anoni.net 社区 |
| 10:10-10:40<br>30 分钟 | <span class="tag tag--basic">通用</span> <i data-icon="target-account"></i> **威胁模型与 Metadata 入门：认识你的对手，以及为什么匿名工具要开源才可信**<br><i data-icon="arrow-right-bottom"></i> 就算通话内容没有被监听，谁在什么时间联系了谁，往往就足以让消息来源曝光。内容包括如何判断要防范谁、防到什么程度<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/anoni-net-threat-model.pdf) | anoni.net 社区 |
| 10:50-11:20<br>30 分钟 | <span class="tag tag--basic">通用</span> <i data-icon="toolbox-outline"></i> **现实世界的开源隐私工具：公民团体、独立记者与个人隐私防护的实际运用**<br><i data-icon="arrow-right-bottom"></i> 整理记者、NGO 与在意隐私的一般人实际使用的免费开源工具，源代码公开、可供检验，听众可以从中挑一两个先用<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/anoni-net-realworld-tools.pdf) | anoni.net 社区 |
| 11:30-12:00<br>30 分钟 | <span class="tag tag--basic">通用</span> <i data-icon="scale-balance"></i> **毒品非毒、洗钱非洗钱—浅谈匿名的资格验证**<br><i data-icon="arrow-right-bottom"></i> 同一件事换一套规则就被归成两种性质，谁有权定义合法与非法？讲者在实名与匿名之外寻找第三条路，听众不需要密码学背景 | Denken Chen | <!-- docs-style-lint: disable-line -->

**下午 13:00-16:30　ETHTaipei 合办「匿名支付」场（教室 `TR-511`，议程由 ETHTaipei 安排）**

| 时间 | 议程 | 讲者 |
|------|------|------|
| 13:00-13:30<br>30 分钟 | <span class="tag tag--payments">匿名支付</span> <i data-icon="card-account-details-outline"></i> **零知识证明与自然人凭证身份验证**<br><i data-icon="arrow-right-bottom"></i> 不必交出任何个人信息，就能用自然人凭证向网站证明自己是台湾公民 | Ya-wen Jeng |
| 13:40-14:10<br>30 分钟 | <span class="tag tag--payments">匿名支付</span> <i data-icon="account-check-outline"></i> **The Privacy-preserving Identity Pipeline in KYC**<br><i data-icon="arrow-right-bottom"></i> 以一组密码学原语组合出可通过 KYC、服务器却看不到身份数据的流程 | ryanycw（Ryan Wang） |
| 14:20-14:50<br>30 分钟 | <span class="tag tag--payments">匿名支付</span> <i data-icon="link-off"></i> **从不可链接性出发：隐匿地址如何解决链上金融隐私（以 Fluidkey 为例）**<br><i data-icon="arrow-right-bottom"></i> 隐匿地址让同一人每次收款都落在互不相关的地址，外部无法串连成同一身份 | Jennifer HSU |
| 15:00-15:30<br>30 分钟 | <span class="tag tag--payments">匿名支付</span> <i data-icon="bitcoin"></i> **我不洗钱，为何要理解匿名支付？从零开始介绍隐私加密金流交易**<br><i data-icon="arrow-right-bottom"></i> 倡议组织与捐款人为何需要了解加密货币金流的隐私风险，并以白话介绍几套解法<br><i data-icon="presentation"></i> [幻灯片（网页）](https://mashbean.net/decks/coscup-2026-privacy-money/) | 黄豆泥 mashbean |
| 15:40-16:30<br>50 分钟 | <span class="tag tag--payments">匿名支付</span> <i data-icon="hammer-wrench"></i> **隐私支付实作工作坊：从龙卷风现金到隐私池**<br><i data-icon="arrow-right-bottom"></i> 以道具与实机示范 Tornado Cash 与 Privacy Pool 的用法，现场备有模拟网络，听众可自备电脑操作<br><i data-icon="presentation"></i> [幻灯片（网页）](https://chihchengliang.github.io/notes/2026-07-27_privacy_pools/slides.html) | Liangcc |

### Day 2：2026/08/09（日）

8/09 全天是七场录取议程，题材从网络与审查的基础、家用网络与校园 Tor 节点，到健保数据库的个人信息权利与个人隐私防护。技术场次与贴近日常的场次交错安排，开发者、记者与公民团体各有适合的场次。

**上午 10:00-12:00（教室 `TR-510`）**

| 时间 | 议程 | 讲者 |
|------|------|------|
| 10:00-10:50<br>50 分钟 | <span class="tag tag--basic">通用</span> <i data-icon="web"></i> **The Workings of the Internet：网络如何运作、审查如何挡住你（英文进行）**<br><i data-icon="arrow-right-bottom"></i> 以寄明信片比喻连接过程，说明从设备到网站的路上有哪些角色能偷看或窜改内容，英文不熟的听众也能掌握大意<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://saxrag.com/bucket/random/workings_of_the_internet.pdf)（CC BY 4.0） | Raghu |
| 10:55-11:25<br>30 分钟 | <span class="tag tag--basic">通用</span> <i data-icon="router-network"></i> **以 OpenWRT 等开源软件建立家用网络环境**<br><i data-icon="arrow-right-bottom"></i> 在家用路由器上完成一般机种没有的高级设置，包含 VLAN 隔离、多 WAN、site-to-site VPN 与 Tor 上游<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/pellaeon-openwrt-home-network.pdf)（讲者保留所有权利，仅供阅览） | Pellaeon |
| 11:30-12:00<br>30 分钟 | <span class="tag tag--payments">匿名支付</span> <i data-icon="fingerprint"></i> **区块链网络上基于开放标准的实体身份识别方法**<br><i data-icon="arrow-right-bottom"></i> 虚拟资产服务法通过后，哪些开放标准会被用来在区块链上定位台湾用户的身份 | Yusef Schultz |

（12:00-13:00 午休）

**下午 13:00-16:00（教室 `TR-510`）**

| 时间 | 议程 | 讲者 |
|------|------|------|
| 13:00-13:30<br>30 分钟 | <span class="tag tag--relay">Tor Relay</span> <i data-icon="simple-torproject"></i> **在学校种洋葱？台师大 Tor 节点建立实务与 EFF Tor University Challenge 经验谈**<br><i data-icon="arrow-right-bottom"></i> 在台师大架设学术 Tor 节点的完整历程，从技术配置到校内政策协调<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/nz-tor-relay-on-campus.pdf) <i data-icon="video-outline"></i> [录影（Google Drive）](https://drive.google.com/file/d/1bAzgU6rSNg9hXSrDhDIXYd4PM-P8Dxte/view?usp=sharing) | NZ |
| 13:35-14:25<br>50 分钟 | <span class="tag tag--privacy">个人隐私</span> <i data-icon="eye-off-outline"></i> **浏览器追踪技术、反追踪策略和用户自主**<br><i data-icon="arrow-right-bottom"></i> 日常使用的浏览器如何被指纹追踪、如何泄漏联系对象，以及反追踪的做法<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/pellaeon-browser-tracking-and-user-autonomy.pdf)（讲者保留所有权利，仅供阅览） | Pellaeon |
| 14:30-15:00<br>30 分钟 | <span class="tag tag--privacy">个人隐私</span> <i data-icon="database-lock"></i> **健保数据库案之后：停止利用权如何实践？以及其他大型数据库**<br><i data-icon="arrow-right-bottom"></i> 健保数据库从退出权诉讼到修法的经过，以及停止利用权的申请方式<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/kuan-nhi-database-right-to-opt-out.pdf) | Kuan-Ju Chou |
| 15:05-15:55<br>50 分钟 | <span class="tag tag--privacy">个人隐私</span> <i data-icon="shield-account-outline"></i> **隐私指南 2026**<br><i data-icon="arrow-right-bottom"></i> 从个人隐私风险矩阵、NGO 与媒体面对法律调取数据的准备，到门限签名、MPC 等组织级高级工具<br><i data-icon="presentation"></i> [幻灯片（PDF）](https://assets.anoni.net/event/coscup-2026/justyn-privacy-guides-2026.pdf) | Justyn |

## <i data-icon="text-box-multiple-outline"></i> 议程介绍 { #议程介绍 }

### 8/08 上午的开源匿名网络导论

前三场导论由 anoni.net 社区成员主讲，内容取材自文档站与 2025 年工作坊，第四场为邀请议程。导论介绍的工具（Tor、Tails、OONI、Signal、SecureDrop、OnionShare、CryptPad、mat2 等）都是自由开源软件，社区也通过翻译、架设中继节点与回报问题参与这些国际开源项目。

??? abstract "匿名网络社区 anoni.net 介绍：开源匿名工具、社区实践与 2026 三大主题"

    匿名网络社区 anoni.net 是台湾的开源社区，近一年持续推广 Tor、Tails、OONI 等自由开源的匿名网络工具。开场介绍社区的缘起与运作方式，以及社区如何以开源协作参与国际项目，例如把 Tor、Tails、OONI 与 Tor University Challenge 的界面翻成正体中文、回报问题、协助在校园架设中继节点。

    接着说明记者、公民团体、人权倡议者这类高风险工作，为何特别倚赖源代码公开的开源工具，封闭的黑箱软件无从验证是否遭到窜改。最后介绍社区 2026 年的三个主题：依情境分级的个人隐私指引、校园 Tor Relay 中继节点建立，以及在合法前提下探索匿名支付的开源工具。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/8CZ7ER/)

??? abstract "威胁模型与 Metadata 入门：认识你的对手，以及为什么匿名工具要开源才可信"

    挑选工具之前，要先回答三个问题：要保护什么、要防范的对手是谁、愿意付出多少成本。讲者用[威胁模型](docs:basics/threat-model/)把三个问题组成判断框架，并说明 [metadata](docs:basics/metadata/)（连接、时间、联系对象这类没有加密的记录）的风险。就算通话内容没有被监听，对手仍可能从通信记录得知谁在什么时间联系了谁、联系多久。对记者与公民团体来说，这类记录往往足以反推出消息来源与整个行动的关系网。

    有了判断框架，遇到新工具、新威胁时就能自行对照。对手有能力检查设备与通信时，工具能否被独立审计就攸关安全，Tor Browser、Tails 采用开放源代码与可重现构建（reproducible build，任何人都能从源代码编出比特相同的程序，验证没有被动过手脚）也是出于这个原因。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/GFKLC8/)

??? abstract "现实世界的开源隐私工具：公民团体、独立记者与个人隐私防护的实际运用"

    讲者整理公民团体、独立记者与注重隐私的个人实际采用的开源隐私工具，分三个场景介绍，每一项都交代用户与适用情境。高风险场景特别倚赖源代码可供公开审计的开源工具，封闭软件无从验证是否遭到窜改，与前一场[威胁模型](docs:basics/threat-model/)的判断框架相互呼应。介绍以最容易上手的几样工具为主，听众不必记住整份清单，可以先挑一两个开始使用。

    公民团体与 NGO 对外用 Signal、Matrix 加密通信，内部协作用 CryptPad、Etherpad。举报与敏感数据的投递用 SecureDrop、[OnionShare](docs:tools/onionshare/)，网络审查的观测则用 OONI。独立记者的部分有安全收件渠道、用 mat2 与 Metadata Cleaner 清除文件内嵌的作者与 GPS metadata，以及用 Tails、Qubes OS 隔离高风险作业。个人隐私防护则有 Tor Browser 与 Brave 抵御网页追踪、GrapheneOS 与 LineageOS 取回手机的控制权、KeePassXC 与 Bitwarden 管理密码。完整的场景与工具对照见[记者保护消息来源](docs:scenarios/journalist/)与[匿名通讯工具比较](docs:tools/messaging-comparison/)。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/QPDZEC/)

<!-- docs-style-lint: disable -->
??? abstract "毒品非毒、洗钱非洗钱—浅谈匿名的资格验证（Denken Chen，30 分钟）"

    讲者从《我们与恶的距离》谈起，提问看完那部戏之后，我们为何仍对善恶的边界这么有把握。同一件事物换一套规则就被归成两种性质，也就是标题「毒品非毒、洗钱非洗钱」的由来。接着讲者提出核心问题，在全面实名监控与无须许可的匿名服务之间，是否还有第三条路。

    技术上，这个提问对应到资格验证，也就是证明一个人符合某项条件，而不必一并披露身份。W3C 的可验证凭证（Verifiable Credentials，VC）等开放标准搭配选择性披露（selective disclosure），持有者可以只出示「已成年」这一项，其余数据验证方看不到。开放标准让验证规则不由单一厂商定义，任何人都能自行实现钱包或验证端。用户手上那一端是否开源、可供审计，决定了用户能否确认它没有多送出数据。讲者也区分了证明资格与证明身份，作为审视各种实名制方案的依据。

    OONI 采用同一类思路的匿名凭证（anonymous credentials），让测量数据可信，又不追踪回报者，设计与取舍见 [OONI Probe 匿名凭证系统的设计与实现](/articles/ooni-anonymous-credentials/)。讲者在 8/09 的 Open Source Policy 议程轨另与黄豆泥 mashbean 合讲[年龄验证、数字监控、隐私权，讨论这些以前，不妨先开源吧](https://pretalx.coscup.org/coscup-2026/talk/JSMGDZ/)，分析欧盟以开源方式开发的年龄验证 App。适合关心数字身份、实名制争议与匿名服务治理的听众，不需要密码学背景。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/WYGFAZ/)
<!-- docs-style-lint: enable -->

### 8/08 下午的 ETHTaipei 合办「匿名支付」场

13:00-16:30 是与 [ETHTaipei](https://ethtaipei.org/)（台北以太坊社区）合办的「匿名支付」主题场，在 `TR-511` 教室进行，共五场，议程由 ETHTaipei 安排。上午的导论从公民与倡议的角度谈隐私工具与匿名的资格验证，以白话为主，不深入密码学细节。下午前两场把资格验证接到金流上，一场用零知识证明搭配自然人凭证向服务证明「我是台湾公民」，另一场用 zkKYC 证明「已成年、与上个月注册的是同一人」。两场都是上午「证明符合条件而不披露身份」的协议层实现，后三场再从链上的隐匿地址谈到隐私加密金流，最后是实操工作坊。两个社区切入匿名支付的角度不同，分工与背景见[跨社区合作](#跨社区合作)。

??? abstract "零知识证明与自然人凭证身份验证（Ya-wen Jeng，30 分钟）"

    如何在不泄漏任何个人信息的前提下，向服务提供者证明「我是台湾公民」？讲者把零知识证明（zero-knowledge proof，不透露内容就能证明某件事为真的密码学方法）与自然人凭证结合，建立一套保护隐私的身份验证系统。自然人凭证内置 RSA 非对称密钥，可以对任意消息做数字签名。系统以 OpenAC 电路框架设计一套 ZKP proving scheme，解析并验证凭证产生的 RSA 签名，同时在电路层面隐藏所有可识别个人的字段。

    整套流程在用户的设备上完成，应用程序请求自然人凭证对特定 challenge 签名后在本地生成零知识证明，最后只把 proof 提交给验证方。验证方能确认对方持有合法的自然人凭证、是台湾公民，却无从得知姓名、身份证号等个人信息。讲者也介绍已发布的 SDK 与范例应用，内容包括 RSA 签名电路设计、on-device proof 生成的性能优化与集成示范，适合对隐私强化技术（PET）、去中心化身份（DID）以及密码学在公民科技上的应用有兴趣的听众。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/997SN8/)

??? abstract "The Privacy-preserving Identity Pipeline in KYC（ryanycw / Ryan Wang，30 分钟）"

    KYC（金融机构确认客户身份的程序）有一个内在矛盾，主管机关要求严格的身份证明，但服务每多保存一笔身份数据，就多一个永久的外泄破口。传统做法把证件收齐、查核、归档，每个 KYC 服务商因此成为高价值的攻击目标，用户则承担永久的披露风险。讲者介绍 zkKYC 领域已在运作的另一套流程，用一组精选的密码学原语组合成一个系统，能证明用户的宣称（护照有效、已成年、与上个月注册的是同一人），服务器却看不到身份数据。

    讲者整理出一套评估隐私保护身份系统的语汇，说明设备绑定密钥、加密的身份保存、政府签署的证件链、生物特征承诺、零知识证明与经过认证的宣称递送如何组合在一起。内容以系统设计与架构图为主，每个密码学原语只做高层次说明，不深入数学，适合工程师与产品人员。讲者也盘点了尚未解决的问题，例如生物特征的撤销、后量子 SNARK，以及不牺牲不可链接性的去重。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/BBQDPR/)

??? abstract "从不可链接性出发：隐匿地址如何解决链上金融隐私（以 Fluidkey 为例）（Jennifer HSU，30 分钟）"

    区块链上任何人都能查到一个地址的完整交易历史与余额，永久公开的财务记录不符合日常支付、薪资发放或商业往来对隐私的基本需求。讲者从 ECDH 密钥交换出发，拆解隐匿地址（Stealth Address）在 ERC-5564 的推导流程。收款方公开一组 stealth meta-address，每次收款都推导出一个全新的一次性地址，同一人收到上百笔款项，也会落在上百个彼此无关的链上地址。外部观察者无法把这些地址连到同一个身份，只有持有对应 viewing key 的收款人能扫出哪些地址属于自己。

    隐匿地址提供不可链接性（unlinkability），但不保证不可追溯性（untraceability），每笔交易的金额与流向在链上依然可见、可以审计。被切断的只有地址与身份之间、同一人不同地址之间的关联，因此在税务、审计这类需要选择性披露的场景，比全匿名方案更实用。最后以 Fluidkey 为例，说明它把 ephemeral key 改为从 viewing key 依 BIP-32 阶层式路径推导，用户能完全独立地重新推导出历史地址、恢复资金，不必依赖任何中心化服务。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/WK8EEE/)

??? abstract "我不洗钱，为何要理解匿名支付？从零开始介绍隐私加密金流交易（黄豆泥 mashbean，30 分钟）"

    很多人以为加密货币是匿名的，实际上只要知道一个钱包地址，就能在公开链上看到对方完整的金流、社会关系与行动轨迹。对倡议组织、跨境协作的公民团体，以及需要保护身份的捐款人与受助者来说，这项风险经常被低估。讲者用白话走过链上隐私金流的设计逻辑，对照近年区块链社区发展出的三套方案。Tornado Cash 是曾遭美国制裁、开发者被起诉的混币器，Privacy Pool 走白名单路线，在同一个架构里协商合规与隐私。Railgun 以黑名单搭配冷却期与集体检测，2025 年挡下 zkLend 黑客约 950 万美元的洗钱，另外也介绍把隐私设为所有钱包默认值的 Kohaku。

    讲者最后提出一个比技术更难的问题，隐私从技术问题延伸成治理问题时，由谁来定义好人与坏人？适合关心数字人权与公民安全的工作者、想了解加密货币合规边界的合规与会计人员，以及对「我又没做坏事，为什么要在乎隐私」这句话感到不对劲的人。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/QGUGMK/)

??? abstract "隐私支付实作工作坊：从龙卷风现金到隐私池（Liangcc，50 分钟）"

    工作坊从用户的角度出发，介绍龙卷风现金（Tornado Cash）的设计哲学，以及隐私池（Privacy Pool）在它之上的改进。

    现场以道具与实机示范两项工具的操作，并备有模拟网络，听众可以自备电脑实际操作。时间允许时，也谈这些工具的沿革与在现实世界造成的冲击。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/3WHJYA/)

### 8/09 的七场录取议程

七场议程从网络与审查的运作原理开始，接着是家用网络与校园 Tor 节点的实地部署。之后的场次谈区块链身份、浏览器追踪、健保数据库的个人信息权利与个人隐私指南，属于制度与个人层面的实践，技术深浅不一。

??? abstract "The Workings of the Internet：网络如何运作、审查如何挡住你（Raghu，50 分钟，英文进行）"

    在浏览器输入 `google.com`、按下 Enter 之后，数据包到底经过哪些人的手？讲者用寄明信片比喻，说明从设备到目标网站之间有哪些角色经手（多半是合法的），以及它们能看到、能改动什么。议程以英文进行，但从生活比喻切入、不预设技术背景，英文不熟的听众也能掌握大意。

    理解这套机制，就能看懂审查、监控与数据外泄如何发生，也能分辨那些劝人购买「某某 VPN」的广告话术问题在哪里。内容也提到默认情况下网络的隐私有多不足，以及看待掠夺式 VPN 营销时该有的警觉。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/UY8UQN/)

??? abstract "以 OpenWRT 等开源软件建立家用网络环境（Pellaeon，30 分钟）"

    OpenWRT 是一套开源的路由器操作系统，讲者跳过基本网络设置，直接示范一般家用路由器不提供、通过 OpenWRT 设置即可达成的便利、安全与隐私功能。

    内容包括挑选支持 OpenWRT 硬件的要点、用 VLAN 隔离访客网络与危险设备、通过多 WAN 运用电信商配发的多个 IP、设置策略路由与 site-to-site VPN、阻挡危险 IP 与域名，以及把 VPN 供应商与 Tor 设成特殊的上游网络。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/CNNASG/)

??? abstract "区块链网络上基于开放标准的实体身份识别方法（Yusef Schultz，30 分钟）"

    各国政府陆续参考并引入区块链防制洗钱的法案，以防范国际犯罪，共同点在于定位用户本身。台湾的对应法案是虚拟资产服务法，2026 年 4 月 2 日通过。台湾用户的身份在链上如何被定位，因此逐渐成为虚拟资产持有者关注的议题。

    讲者盘点目前用于链上身份定位的几种开放标准，说明用户的身份在区块链上如何被认定，以及密码学研究为这个领域带来的正面影响。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/ZV88PP/)

??? abstract "在学校种洋葱？台师大 Tor 节点建立实务与 EFF Tor University Challenge 经验谈（NZ，30 分钟）"

    学术网络带宽稳定、IP 声誉良好，一直是全球 Tor 网络最重要的支柱之一，在校园部署 Tor 节点却要同时处理技术配置与校内政策。讲者分享在国立台湾师范大学（NTNU）建立学术 Tor 节点的完整历程。

    内容从 EFF 发起 Tor University Challenge 的缘起与意义，谈到 Linux 环境下的节点配置与防火墙规则、如何与学校信息部门沟通并运用 EFF 提供的法律指南，以及节点上线后的流量观察。其他学校可以参考这套实践经验，讲者也希望借此邀请更多台湾学术研究机构参与全球隐私基础设施的建设。社区整理的校园架设脉络见 [Tor Relay 校园建立研究专题](/join/relay-on-campus/)。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/7AP8HY/)

??? abstract "浏览器追踪技术、反追踪策略和用户自主（Pellaeon，50 分钟）"

    现代浏览器提供许多看似不属于网页的 API：WebGL 让网页使用图形加速、WebAudio 让网页运行复杂的音频合成、WebAssembly 让网页直接运行底层指令。与硬件紧密结合的 API 让网页能做的事变多，网页也因此能搜集更多用户数据，更精准地追踪与识别用户。网页要求时，API 就自动启用，不会征询用户同意。

    Pellaeon 分享他在浏览器指纹（browser fingerprint）与反追踪方面的研究，说明浏览器可能如何泄漏用户的行踪，以及 Tor Browser、Brave、VPN 等软件各自的反追踪策略、潜在解法与实际使用心得。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/KSWEDB/)

??? abstract "健保数据库案之后：停止利用权如何实践？以及其他大型数据库（Kuan-Ju Chou，30 分钟）"

    台湾的就医数据多年来未经病人同意，就提供产业与学界使用。台湾人权促进会、台湾女人连线、健保监督联盟三个民间团体发动退出权诉讼之后，健保数据库的目的外利用陆续停止贩售光盘，并限制为仅供研究使用。2022 年的宪法诉讼确认政府必须让人民实践停止利用权，也就是不同意将个人信息提供其他目的使用。之后台湾完成修法，民众开始可以行使这项权利，但立法过程增加不少例外，适用范围缩小许多。

    讲者说明停止利用权的申请方式与目前的限制，并介绍台湾其他规范不明、对个人信息主体权利保障尚不清楚的大型数据库，同样需要公民社会一起监督。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/GEKJRV/)

??? abstract "隐私指南 2026（Justyn，50 分钟）"

    工作坊与座谈从个人谈到组织，第一部分建立个人隐私风险矩阵，把广告追踪与数据中介、诈骗与盗账号、亲密关系加害者、跨境盘查、针对性监控等威胁来源分级。威胁来源对应到数字身份、移动设备、SaaS 与云端、金流四个暴露面，矩阵的每一格都给出以开源工具与设备内置设置为主的默认配置建议。

    第二部分是自我检查的方法学，包括如何检查 App 内嵌的追踪器、如何观察设备实际连接的对象、如何读懂 iOS App Privacy Report。自评的基准则对照 NIST Privacy Framework 与 OWASP MASVS，只做最小范围的检查。

    第三部分谈组织层面的多人协作隐私，对象是 NGO、独立媒体与小型公司，内容涵盖共享密码管理、端对端加密协作、组织遭遇法律调取数据的事前准备，以及 Shamir Secret Sharing、门限签名（FROST、TSS）、MPC（多方计算）、Private Set Intersection（隐私集合交集）、OpenMLS 等较高级的工具。门限签名、MPC、PSI 是给有密码学背景的组织管理者的重点，非技术背景的听众略过这串工具名称，也不影响前两部分。

    个人、NGO 与小型团队都能从中取得对照自身情境的默认配置与自我检查方法，遇到新工具、新威胁、新法规时可以自行判断，不必仰赖固定的推荐清单。密码学细节则点到为止。

    <i data-icon="open-in-new"></i> [COSCUP 官方议程页](https://pretalx.coscup.org/coscup-2026/talk/K8BYBU/)

## <i data-icon="handshake"></i> 匿名网络社区与 ETHTaipei 的跨社区合作 { #跨社区合作 }

2026 年社区与 [ETHTaipei](https://ethtaipei.org/)（台北以太坊社区）合作安排议程，8/08 下午的「匿名支付」合办场同时面向关心数字人权的社区与区块链开发者。NGO 与记者在这里了解捐款与金流的隐私风险，开发者则听到协议层的零知识证明与隐匿地址实现。征稿时，应用导向与科普类的稿件安排在匿名网络社区议程轨，技术与协议层的稿件可能调整到 ETHTaipei 的区块链议程轨（见 [COSCUP 2026 公开征稿](/events/coscup-2026-cfp/#anoni-netxETHTaipei)的跨社区合作一节），听众也可以在两个议程轨之间跨场。

## <i data-icon="account-voice"></i> 讲者简介 { #讲者简介 }

8/08 上午的前三场导论由 anoni.net 社区成员主讲，他们实际运维 Tor 中继节点，也参与 Tails 与 OONI 的正体中文化与问题回报（社区背景见[关于我们](/about/)）。邀请、合办与录取议程的讲者依议程顺序列在下方，点击名字可以前往 COSCUP pretalx 上讲者本人提供的完整简介，Raghu 与 Pellaeon 依讲者意愿改连到个人网站与博客。

**8/08 上午 邀请议程**

- **[Denken Chen](https://pretalx.coscup.org/coscup-2026/speaker/FW9HYA/)**：从事软件开发与写作十余年，投入 W3C 的去中心化识别码与可验证凭证标准，参与 Credentials Community Group 与台湾数字凭证皮夹的工作，也是 Ptt-iOS、Taiwan E-Book Search 等开源项目的发起人。主讲「毒品非毒、洗钱非洗钱—浅谈匿名的资格验证」，并在 8/09 的 Open Source Policy 议程轨与黄豆泥 mashbean 合讲「年龄验证、数字监控、隐私权，讨论这些以前，不妨先开源吧」。 <!-- docs-style-lint: disable-line -->

**8/08 下午 ETHTaipei 合办「匿名支付」场**

- **[Ya-wen Jeng（Vivian Jeng）](https://pretalx.coscup.org/coscup-2026/speaker/KBPWBX/)**：任职 Ethereum Foundation 的 Privacy Stewards of Ethereum 团队，专注零知识证明与隐私技术推广，主导 Mopro、Unirep 等开源工具开发。主讲「零知识证明与自然人凭证身份验证」。
- **[ryanycw（Ryan Wang）](https://pretalx.coscup.org/coscup-2026/speaker/8WM9UR/)**：DeFi 开发者，ETHTaipei 共同主办，关注隐私、技术与以太坊。主讲「The Privacy-preserving Identity Pipeline in KYC」。
- **[Jennifer HSU](https://pretalx.coscup.org/coscup-2026/speaker/ZJ98MX/)**：任职自托管隐私钱包 Fluidkey，台湾开发者社区 XueDAO 创办人，推广区块链技术。主讲「从不可链接性出发：隐匿地址如何解决链上金融隐私」。
- **[黄豆泥 mashbean](https://pretalx.coscup.org/coscup-2026/speaker/ZMHFCQ/)**：专注分布式科技与数字自主权，Matters 总经理，曾任数位发展部资安制度工程师（推动数字凭证皮夹与开放网络标准、参与 W3C），活动当时为哈佛大学政策访问研究员与以太坊基金会 Silviculture 成员。主讲「我不洗钱，为何要理解匿名支付？」。
- **[Liangcc（CC）](https://pretalx.coscup.org/coscup-2026/speaker/UYKEPE/)**：在以太坊生态开发零知识应用，关注人文、经济与密码学证明。带领「隐私支付实作工作坊：从龙卷风现金到隐私池」。

**8/09 Day 2 议程**

- **[Raghu](https://saxrag.com/)**：后端工程师，投入 IP、TCP、数据包分析与安全研究。主讲「The Workings of the Internet」（英文进行）。
- **[Pellaeon](https://nyllep.wordpress.com/)**：数字安全研究员与讲师，关注数字人权与自由软件。主讲「以 OpenWRT 等开源软件建立家用网络环境」与「浏览器追踪技术、反追踪策略和用户自主」两场。
- **[Yusef Schultz](https://pretalx.coscup.org/coscup-2026/speaker/FAGUY7/)**：主讲「区块链网络上基于开放标准的实体身份识别方法」，完整简介见 pretalx 讲者页。
- **[NZ（苏恩立）](https://pretalx.coscup.org/coscup-2026/speaker/WCJNBL/)**：台师大资工系学生，运维台湾学术网络（TANet）首个 Tor 节点，关注网络安全与网络治理。主讲「在学校种洋葱？台师大 Tor 节点建立实务与 EFF Tor University Challenge 经验谈」。
- **[Kuan-Ju Chou](https://pretalx.coscup.org/coscup-2026/speaker/UAREZS/)**：在台湾人权促进会服务，负责数字人权。主讲「健保数据库案之后：停止利用权如何实践？」。
- **[Justyn](https://pretalx.coscup.org/coscup-2026/speaker/WZGMJG/)**：主讲「隐私指南 2026」，pretalx 讲者页未附简介。

## <i data-icon="link-variant"></i> 相关链接

- [COSCUP 2026 公开征稿](/events/coscup-2026-cfp/)：征稿主题、跨社区合作与投稿说明
- [匿名网络工作坊 2025/08](/events/workshop-2025/)：2025 年两日工作坊与圆桌会议的记录
- [延续 2025，走向 2026：个人隐私指引、Tor Relay 校园建设竞赛、匿名支付探索](/updates/2026/01/2025to2026/)
- [关于我们](/about/)
- [参与](/join/)：参与 Tor、OONI、翻译或架设节点的入口
- [参与 Tor Project](/join/tor-project/)：参与 Tor 上游项目的渠道与方式

!!! info "官方议程与活动通知"

    各场的正式时间与题目以 [COSCUP 官方议程](https://pretalx.coscup.org/coscup-2026/) 为准。想收到社区之后的活动通知，见[持续关注](/contact/)。
