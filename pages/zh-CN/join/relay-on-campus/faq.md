---
title: 给校方与法务的校园 Tor Relay FAQ
description: 校方信息中心、法务与网管对校园 Tor Relay 最常提出的十个疑虑与回应建议，附给网管与给行政法务的两份一页摘要。
---

在校园架设 Tor Relay，信息中心、法务与网管最常提出的疑虑大致是同样十个。本页从[校园 Tor Relay 提案范本](/join/relay-on-campus/proposal/)衍生，每题补上台湾背景，可以附在提案文件后面，或在面谈前先发给对方参考。

[Tor Relay 架设指南](/join/setup-tor-relay/)末尾的 FAQ 写给个人运营者，本页的读者则是学校行政、法务与网管，重点放在学校的风险评估，以及被问到时如何回答。

各题的「台湾背景补充」以台湾的首例与法规为准，一般性的回答在其他地区同样适用。在台湾以外提案时，请把这些段落换成当地的对应内容。

## 使用方式

- **提案时**：附在计划书后面作为附录一
- **面谈前**：发给信息中心、网管、法务先读一遍
- **被问到时**：展开对应的问题，复制内容引用
- **页尾的两份一页摘要**：30 秒可以读完，适合放在邮件开头，或在会议上作为发给对方的书面材料

## 常见疑虑

??? question "为什么大学适合架设 Tor Relay？"

    学术网络的带宽稳定，计算机、信息安全与信息中心本来就有架设与运维的人力。架设可以从风险最低的 Non-Exit Relay 开始，不经手出口流量，也不需要处理对外连接引起的投诉。节点随时可以停止，是可逆的决定。架设与运维的过程本身就是匿名网络、信息安全与开源治理的教学案例。重视学术自由与信息获取的学校，也能借此把理念落实到基础设施。

    **台湾背景补充**

    国立台湾师范大学资讯工程学系已完成台湾首例（2025 年 11 月上线），过程见 [Tor Project 博客的客座文章](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)与[社群访谈](/updates/2025/12/ntnu-nz/)。台湾的高等教育体系本来就承担计算机、信息安全与网络治理的教学，校园 Tor Relay 可以作为实际的教学案例。

??? question "我们不想架设 Exit Relay，这样可以吗？"

    可以，Tor 网络需要各种类型的 Relay 才能保持健康。默认情况下，架设的 Relay 会担任 Entry 或 Middle Relay，只在 Tor 节点之间转发加密流量。Entry 与 Middle Relay 是维护成本最低的形式，也不会收到出口流量引起的投诉。

    另外也可以选择同时运营 Bridge 或 [Tor Snowflake](docs:tools/tor-snowflake/) 代理，协助身处网络审查地区的用户连上 Tor。

    **台湾背景补充**

    台湾的校园案例（台师大）就是 Non-Exit Relay。建议台湾所有校园 Relay 计划都从 Non-Exit 开始，不要尝试 Exit Relay，Exit Relay 的法律与行政成本远超出个人或学生社团能负担的范围。

??? question "愿意运营 Relay，但不想处理滥用问题，该如何处理？"

    Exit Policy（出口策略）就是为此设计的，每个 Tor Relay 都有一份，指定允许或拒绝哪些对外连接。Exit Policy 通过目录服务发布给 Tor 客户端，客户端会自动避开拒绝该连接的 Exit Relay。每个 Relay 可以依滥用风险与自身情况，决定允许的服务、主机与网络。

    默认的 Exit Policy 允许许多常见服务（例如网页浏览），但会限制滥用风险高的服务（例如邮件），以及 Tor 网络无法负荷的服务（例如文件共享的默认端口）。

    允许部分出口连接时，请务必确认 DNS 解析正常运作。

    **台湾背景补充**

    校园计划最简单的做法是配置 `ExitPolicy reject *:*`，关闭所有对外连接。流量不会从这个 Relay 出去，所以几乎不会收到滥用投诉（仍建议备好 EFF 的 abuse 回应模板）。配置细节见[校园 Tor Relay 架设 SOP](/join/relay-on-campus/sop/#torrc-参考配置)。

??? question "Tor 不是会让犯罪分子做坏事吗？"

    Tor 的使命是促进人权，以自由、开源的技术协助用户抵抗大规模监控与网络审查。Tor 社群一向谴责把工具用于不法用途的行为。

    犯罪的意图在于人，不在工具，加密、电话、现金都可能被恶意使用，Tor 也一样。移除 Tor 之后，有恶意的人会改用其他工具，并不会因此停手。

    Tor 与其他隐私工具同时保护真正需要的人，可以防范身份盗用、实体跟踪等犯罪，也能协助执法部门调查案件、支持受害者。

    **台湾背景补充**

    台湾刑法第三十六章妨害电脑使用罪（第 358 条至第 363 条）规范的是具体行为，例如无故输入他人账号密码而入侵他人电脑（第 358 条），以及无故取得、删除或变更他人电脑的电磁记录（第 359 条）。Middle Relay 不接触内容、不解析用户数据、不知道用户身份，性质与网络传输基础设施相近，与前述条文的犯罪构成要件无关。

    台湾个人资料保护法第 2 条把个人资料定义为「得以直接或间接方式识别该个人之资料」。Middle Relay 处理的是 Tor 网络的加密 cell，没有可识别个人的数据，因此不涉及个人资料的处理。节点被选为入口节点（Guard）时，会看到连入客户端的 IP 地址，但不知道对方要连到哪里，Tor 默认的日志配置（`SafeLogging 1`）也会把地址遮掉。IP 地址是否构成个人资料，要看能否与其他数据比对、识别出特定个人，这一点建议一并咨询法律专业人员。

    以上是社群整理的法律观点，并非正式的法律意见。个案的法律疑虑，建议咨询法律专业人员。

??? question "分布式拒绝服务攻击（DDoS）的风险呢？"

    DDoS 攻击通常依赖成千上万台电脑同时发送 UDP 数据包，占满受害者的带宽。

    Tor 只传输完整的 TCP 连接，不传输任意的 IP 数据包，所以无法发送 UDP 数据包，也无法发动 SYN Flood 这类攻击。常见的 DDoS 攻击手法无法通过 Tor 进行。

    Tor 也不允许带宽放大攻击，送进 Tor 多少数据，Tor 就只送出多少数据。攻击者若真的拥有足以发动 DDoS 的带宽，也不需要经过 Tor。

    **台湾背景补充**

    目前没有台湾 ISP 针对 Middle Relay 发出 DDoS 投诉的记录。台师大的节点自 2025 年 11 月上线以来，也没有收到 DDoS 相关的通报。

??? question "垃圾邮件（Spam）的风险呢？"

    Tor 默认的 Exit Policy 拒绝所有 SMTP（25 端口）流量，无法直接通过 Tor 发送垃圾邮件。

    少数 Relay 可能开放 SMTP，风险与架设一台开放式邮件服务器相同，并非 Tor 带来的特有风险。垃圾邮件发送者也可能通过 Tor 连到开放的 HTTP Proxy、利用有漏洞的 CGI 脚本发信，或控制僵尸网络，在没有 Tor 的情况下同样可以做到。

    许多垃圾邮件手法（例如伪造的 UDP 数据包）无法通过 Tor 进行，因为 Tor 只支持 TCP。

    **台湾背景补充**

    校园 Relay 配置 `ExitPolicy reject *:*` 之后，SMTP 流量也不会发出，校园 Non-Exit Relay 没有垃圾邮件的问题。

??? question "Tor 常被滥用吗？"

    Tor 用 Exit Policy 降低滥用风险，每个 Relay 都能决定允许或拒绝哪些服务，并公告给客户端。Tor Project 也有专门的 Network Health 团队，负责调查恶意 Relay 并将它们移出网络。

    Tor 的设计刻意让 Tor Project 与 Relay 运营者都无法监控用户的行为，因此能为人权工作者、记者、家暴幸存者、吹哨人与执法部门提供可靠的隐私与匿名保护。

    **台湾背景补充**

    对校园 Non-Exit Relay 而言，滥用的概念基本上不适用，因为节点不会接触用户最终要访问的内容。经过节点的流量都是 Tor 节点之间的加密转发，与外部网站之间至少还隔着一个 Relay。

??? question "架设 Exit Relay 会遇到哪些情况？"

    允许出口连接的 Relay，迟早会收到滥用投诉，例如：

    - 有人通过 Tor 连到 Hotmail 发出勒索信，FBI 等执法部门联系你，说明之后通常会被接受
    - 有人通过 Tor 在 Google Groups 发送垃圾消息，你的 ISP 收到投诉信
    - 有人通过 Tor 在 IRC 捣乱，你的服务器可能遭到 DDoS
    - 有人通过 Tor 下载盗版电影，你的 ISP 可能收到 DMCA 侵权通知，依 EFF 建议的模板回复，通常不会有法律责任

    各家网络服务提供商对 Tor Exit Relay 的接受程度不同，有些愿意配合，有些则较严格。部分网站也会封锁 Exit Relay 的 IP，这是常见的情况。要运营 Exit Relay，最好使用不影响其他业务的专用 IP。

    **台湾背景补充**

    强烈不建议在台湾的校园架设 Exit Relay，台湾学术网络（TANet）的对外连接需经教育部审核，Exit Relay 的流量无法预期，与审核框架不相容。此外，目前没有先例可以引用，沟通成本会增加。学生或社团负责人通常也无法承担可能的法律或行政后果。

    对 Exit Relay 有兴趣，建议在海外对 Tor 友好的云服务商租用个人 VPS 试运行，不要把校园资源牵扯进来。

??? question "如何回应 ISP 的投诉？"

    Tor 社群已经整理出完整的回复范例，Relay 运营者可以照着模板回复 ISP，见 [EFF Tor Legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/) 与 [Tor abuse-templates](https://community.torproject.org/relay/community-resources/tor-abuse-templates/)。

    **台湾背景补充**

    校园 Non-Exit Relay 不会与外部网站直接通信，理论上不会收到 ISP 投诉。如果真的收到投诉信（例如对方误以为这是 Exit Relay），可以这样回应：

    1. 确认投诉事件的时间，以及目的 IP 或网址
    2. 出示 `ContactInfo` 与 `ExitPolicy reject *:*` 的配置截图
    3. 引用 [Tor Project 对各类 Relay 的说明](https://community.torproject.org/relay/types-of-relays/)，Non-Exit Relay 只在 Tor 网络内转发加密流量，不会与最终目的地建立连接
    4. 必要时请指导教授或学校法务协助

??? question "Tor 如何处理技术被滥用的问题？"

    Tor Project 谴责任何把技术用于犯罪的行为，并在能力范围内处理恶意行为，例如封锁恶意 Relay。

    Tor 的设计让它无法监控或禁止用户的行为，虽然可能被恶意利用，但更多时候保护了真正需要的人，包括人权工作者、记者、家暴幸存者、吹哨人、执法人员，以及其他需要隐私保护的群体。

    **台湾背景补充**

    台湾社会近年对揭弊者保护、家暴与跟踪骚扰防治、新闻自由的关注持续增加。Tor 在这些情境对台湾用户的价值与其他国家相同，架设校园 Relay，是让这套基础设施在台湾可用的具体贡献。

    延伸阅读：[揭弊者保护法的技术观察](docs:taiwan/whistleblower-law/)、[家暴受害者的数字准备](docs:scenarios/domestic-violence/)。

## 给网管的一页摘要

!!! info "网管与信息中心技术人员的 30 秒摘要"

    **节点类型**

    - Tor Relay（中继节点），不是 Exit Node
    - 只在 Tor 网络内转发加密流量，不与外部网站直接通信

    **部署需求**

    - 一个固定 IPv4 地址
    - 对外只开放 1 个 TCP 端口（ORPort 9001 或 443）
    - 可选用 80 或 443 端口提供状态页
    - 其余端口全部关闭

    **不会发生的事**

    - 不解析、不记录用户流量
    - 不会收到滥用投诉（Non-Exit）
    - 不会增加校园边界防火墙的负荷
    - 不会影响校园的 DNS 或内容过滤策略

    **可逆性**

    - 停止 systemd 服务，10 分钟内即可下线
    - 随时可以移除，不影响校园网络环境

    **参考案例**

    - 全球多所大学都有运营，包括 MIT、Stanford、Cambridge、CMU
    - 台湾首例：[国立台湾师范大学资讯工程学系（2025 年 11 月上线）](/updates/2025/12/ntnu-nz/)
    - 国际计划：[EFF Tor University Challenge](https://toruniversity.eff.org/)

## 给校方行政与法务的一页摘要

!!! info "校方行政与法务的 30 秒摘要"

    **计划背景**

    在校园架设 Tor Relay，是参与 EFF（Electronic Frontier Foundation）推动的 Tor University Challenge 国际计划。全球已有多所大学参与，包括 MIT、Stanford、Cambridge、CMU。

    **法律定位**

    - 架设的是 Non-Exit Relay，法律上的性质与网络传输基础设施相近
    - 不接触用户内容，不识别个人资料
    - 与台湾刑法妨害电脑使用罪章、个人资料保护法的构成要件无关（社群整理的观点，并非正式法律意见）
    - EFF 提供法律与技术资源

    **对学校的意义**

    - 以实际的基础设施表明学校重视信息自由与隐私保护
    - 列入 Tor University Challenge 的国际大学名单
    - 教学：计算机、信息安全与网络治理的教学案例
    - 研究：网络研究与课程的素材

    **运营影响**

    - 随时可以下线（10 分钟内）
    - 由学生与指导教授共同运维，学校的行政负担很低
    - 不需要修改现有的校园防火墙或内容过滤策略

    **参考案例**

    - 台湾：[国立台湾师范大学资讯工程学系（2025 年 11 月上线）](/updates/2025/12/ntnu-nz/)
    - 国际：[Tor Project 博客的 Setting Up a Tor University Relay in Taiwan](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)

!!! tip "下一步"

    依目前的进度选择：

    - **还没写提案**：回到[校园 Tor Relay 提案范本](/join/relay-on-campus/proposal/)，改写成自己学校的版本，并把本页附在后面
    - **提案已通过**：依[校园 Tor Relay 架设 SOP](/join/relay-on-campus/sop/) 进行技术上线
    - **只是被问到 Tor Relay**：把[给网管的一页摘要](#给网管的一页摘要)或[给校方行政与法务的一页摘要](#给校方行政与法务的一页摘要)直接转给对方

## 相关阅读

- [Tor Relay 校园建立研究专题](/join/relay-on-campus/)：三份范本的入口与专题的进度
- [校园 Tor Relay 提案范本](/join/relay-on-campus/proposal/)：供各校改写成自己版本的提案文件
- [校园 Tor Relay 架设 SOP](/join/relay-on-campus/sop/)：torrc、UFW、监控与事件处置的技术细节
- [在台师大架设 Tor Relay](/updates/2025/12/ntnu-nz/)：台湾首例的完整过程
- [EFF Tor Legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)：以美国法为基础的完整法律 FAQ（英文）

## 资料来源与致谢

本页十题的主体由社群伙伴**苏恩立（NZ）**提供，整理自他在台湾师范大学的计划书原始版本，台湾背景补充由匿名网络社群 anoni.net 整理。原始材料经 NZ 同意，以 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) 授权发布。
