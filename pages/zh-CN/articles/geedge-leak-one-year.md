---
title: Geedge 外泄一年后的研究回顾
description: Geedge Networks 与 MESA 实验室的内部文件外泄之后，研究界第一次能用商用审查设备的源代码对照防火长城。本文整理一年来两篇论文与民间调查确认了什么、还不确定什么，以及报道与论文说法之间的落差。
date: 2026-10-30
---

近三十年来，研究者几乎只能从墙外推测防火长城如何运作，方法是发出设计过的数据包，记录哪些被拦、用什么方式被拦，再反推背后的设备。Geedge Networks（积至公司）的内部文件外泄之后，研究者第一次取得一家与防火长城关系密切的商用审查厂商的源代码、构建软件包与工单。USENIX Security 2026 论文的作者写明，商用 DPI（深度包检测，逐条分析连接内容、判断要不要放行的技术）的源代码是第一次外泄。研究者可以先读代码找出特征，再回到真实的网络比对，不必只靠黑箱推测。

一年下来，比对出来的范围比部分报道写的窄，测量结果显示外泄的代码或与它相近的衍生版本很可能部署在防火长城的一部分设备上。同样测量过的其他几台防火长城设备与它不吻合，没有任何一台设备与外泄的最新版完全相同，其他客户国家多半停在「可能」或「无法确认」。相对地，这些结论同时有源代码与测量两边的证据，比过去只靠远程推测扎实。本文整理这一年谁做了什么研究、确定了什么、还不确定什么，写给开发规避工具、做测量研究与关心供应链的读者。技术细节只写到机制层级，想深入的读者请读原论文。

## 一年来的研究

外泄的文件来自 Geedge 与 MESA 实验室两边。MESA 实验室（Massive and Effective Stream Analysis）隶属中国科学院信息工程研究所，GFW Report 形容两者是防火长城研发能力的重要分支。依 GFW Report 的整理，Geedge 在 2018 年于海南成立，被称为「防火长城之父」的方滨兴担任首席科学家。FOCI 论文统计外泄的总量是 572 GiB，包含源代码库、项目管理记录、客户的部署配置与运营数据，其中八成以上是一个 RPM 软件包仓库（Linux 的软件安装包）的存档。

- **2025 年 9 月 8 日起**：The Globe and Mail 刊出报道，InterSecLab 在 9 月 9 日发表报告〈The Internet Coup〉，国际特赦组织的《Shadows of Control》与 Justice For Myanmar 的《Silk Road of Surveillance》也在同一个月发表。
- **2025 年 9 月 11 日**：Enlace Hacktivista 公开全部文件，DDoSecrets 也提供下载。
- **2025 年 9 月 12 日**：GFW Report 发表外泄的分析文章，最后一次更新是 12 月 29 日。文中写明源代码的部分还没有人仔细分析。
- **2026 年 2 月 19 日**：马萨诸塞大学阿默斯特分校与 GFW Report 的研究者发表 FOCI 2026 论文〈Geedge Cases〉，比对外泄文件里的域名与两份常用的域名清单。
- **2026 年 4 月 24 日**：InterSecLab 发表〈MADLink〉，供应链系列的第一篇，主题是 Geedge 使用的服务器与网络硬件，其中包括台湾的凌华科技。
- **2026 年 8 月**：作者群 8 月 5 日在项目网站 geedge.report 发表说明文章。论文〈Technical Analysis of the Geedge Networks Firewall Source Code Leak〉在 8 月 12 日到 14 日的 USENIX Security 2026 发表，作者来自密歇根大学、帕德博恩大学、马萨诸塞大学阿默斯特分校、科罗拉多大学博尔德分校与 GFW Report。Risky Bulletin 在 8 月 21 日报道。

报道比文件公开早了三天。USENIX 论文的引言写到，几家提前取得文件的新闻机构与记者过去一年合作分析这批文件，角度偏向非技术面。依[〈The Internet Coup〉译文](https://anoni.net/docs/reports/interseclab-network-coup/)的致谢，Tor Project 也是这次联合调查的合作伙伴。联合调查读的是文件与工单，整理出 Geedge 的客户、部署的国家与产品功能。在 USENIX 论文之前，源代码本身大致还没有人分析。学界的研究是另一条线，读源代码、把系统构建起来，再做远程测量。

两条线的证据性质不同，从文件可以知道 Geedge 卖给谁、客户要求什么，测量则用来判断某一台设备的行为是否与代码一致。部分报道把前者的结论套到后者（例子见后面的报道与论文的措辞差距一节）。

## 源代码里的 TSG

### 构建与测试

USENIX 论文分析的是 Geedge 的旗舰产品天狗安全网关（Tiangou Secure Gateway，TSG），作者形容它是可以完整集成进国家电信管制的审查平台。外泄的内部文件超过 10 万份，光是 Git 仓库就有 500 多个，涵盖五年以上的 commit 历史，最新的文件到 2024 年 11 月。分析的难处在于 TSG 的逻辑分散在许多仓库里，同一个组件有多个分支与版本，论文还找到至少两套各自独立的 IP、UDP、TCP 协议栈（程序里实现 IP、TCP 等基础协议的部分）。

研究团队依 DPI 的四个阶段读代码，也就是接收流量、重组与解析、比对规则、干扰连接。构建时，研究团队从最新的标签版本着手，对应多个仓库与软件包仓库，并绕过了授权检查。

构建完成之后，研究团队在隔离的测试环境里测试了 DNS、HTTP、TLS 与 QUIC（一种在 UDP 上传输的协议，HTTP/3 使用它）的处理，成功触发伪造回应的注入、丢包与延迟封锁，也用规则引擎定义了一个自定义的封锁对象。三套应用识别系统（见下方第三方代码一节）是否都在这份构建里运行，论文没有交代，所以本文只写到研究团队构建并运行了 TSG 最新的标签版本，在本机测试了几种协议的封锁行为。论文刻意不公开完整的构建做法，理由见后面的研究伦理一节。

### 核心组件

TSG 由几个分开开发、各有版本的组件组成。SAPP 是最底层的数据包处理平台，MESA 实验室从 2005 年开始开发，经过四次大改版，用 C 编写。SAPP 把数据包整理成 TCP、UDP 流再交给插件，本身不做封锁决定，只提供封锁需要的功能。插件分成三类，平台插件提供共用功能，协议插件从 DNS 查询、TLS 与 QUIC 的握手取出域名等字段，业务插件用这些字段实现封锁之类的应用逻辑。

Stellar 是 Geedge 另外开发、用 C++ 编写的平台，跟踪连接状态的能力比 SAPP 完整，插件之间的通信方式也更多样。Stellar-on-SAPP 是 SAPP 的平台插件，把 SAPP 的流转成 Stellar 的会话（session）交给 Stellar 的插件处理，README 写明它是两个平台之间的过渡方案。在外泄的版本里，Stellar 的插件就是经由 Stellar-on-SAPP 在 SAPP 上运行。独立的 stellar 仓库当时还在开发中，没有出现在任何构建仓库里，也没有接入 TSG。

Maat 是规则引擎，封锁规则存在 Maat 里，插件用取出的字段比对规则，取得处置方式。规则可以比对的字段很广，包括传输层与应用层协议、隧道封装的内外层地址、来源与目的 IP、端口、域名与 SNI（TLS 连接开头以明文发送的网站名称）、ASN（自治系统编号）与国家。Firewall 插件同时挂在 SAPP 与 Stellar 上，汇总各路取出的字段，查询 Maat 之后执行封锁。封锁手段除了丢包与 RST（TCP 的重置数据包，发出后连接就会中断），还有限速、HTTP 与 DNS 的重定向、邮件与 SIP 的封锁、篡改内容与延迟封锁。

作者从架构归纳出两点，后面的比对都受它们影响。组件各自开发、各有版本，从远程测出某一个插件的指纹（能用来辨认某个系统或版本的特征），不代表同一个部署也有另一个插件，也无法推论另一个插件的版本。封锁决定在多条处理路径汇总之后才做出，一条连接可能因为其中任何一条路径的结果而被拦。

### 第三方代码

TSG 有三套应用识别系统，用来判断一条流量属于哪个 App 或协议，其中两套建立在第三方代码上。CBD（Context-Based Detector，前身是 AppSketch）是 TSG 自己的系统，依 Maat 加载的签名判断。Glimpse 的协议分类核心是怀卡托大学 Libtrace 团队的自由软件 libprotoident，相关的代码都带着 libprotoident 的版权声明。Glimpse 检测 OpenVPN 的代码，依论文的描述看来是 2022 年某一版 nDPI（以 GPL 授权的 DPI 函数库）的修改副本，主要函数改了名称，逻辑几乎相同。第三套 QDPI 建立在 Qosmos ixEngine 上，那是商用的闭源 DPI 函数库，作者的依据是代码调用了 ixEngine 的函数并引用它的头文件。

论文对 libprotoident 与 nDPI 的用词是复制后改写，对 Qosmos 只写建立在它之上，没有判断 Geedge 是否取得授权。研究团队把 Geedge 使用这些代码的情形通报 libprotoident 团队与 Qosmos 的母公司 Enea，论文发表时双方都已回复，也排定了会议，回应的内容没有公开。nDPI 不在论文列出的通报对象里。作者认为这显示即使是资源充足、与国家有关系的厂商，从零建立完整的协议分类也很昂贵（原文用 suggests）。这类发现需要读源代码才能取得，远程测量很难判断识别系统用了谁的代码。

## 与防火长城的比对

### 比对的方法

USENIX 论文写到，防火长城过去被认为高度集中，近年却有越来越多证据指向多台独立运作、分工不同的 DPI 设备，过去的测量研究也替其中几种设备命名。DNS 注入（审查设备抢在真正的服务器之前发回伪造的 DNS 回应）的设备分成 Injector 1、2、3，名称来自 FOCI 2020 的〈Triplet Censors〉。发出 RST 中断 TCP 连接的设备分成 GFW I、II、III，河南省另有一套区域性的审查，名称来自 IEEE S&P 2025 的〈A Wall Behind A Wall〉。

研究团队从源代码找出可以从远程测量的特征，例如解析协议时的特殊处理方式，以及设置数据包字段用的自制随机数生成器。接着在两台自己拥有的主机之间发出测试数据包，比较各地审查设备的反应是否与 TSG 相同。测量涵盖中国的防火长城、河南、哈萨克斯坦、缅甸与巴基斯坦，伊朗只测了 DNS，协议包括 DNS、IP 分片重组、TCP、TLS 与 QUIC。

论文在 TLS 一节写到，路径上可能不只一台审查设备。TSG 放行的测试数据包仍可能被其他设备拦下，TSG 会拦的数据包则只要经过 TSG 就一定被拦。我们的推论是，无法从封锁行为判断来源时，实测的「被拦」可能来自路径上任何一台设备，无法单独证明 TSG 存在。相对地，TSG 应该拦下、实测却放行的结果，可以排除路径上有行为相同的 TSG 组件。模块化让情况更复杂，同一个部署可能用同一版 SAPP、不同版的 SSL 插件，所以每一项比对只能说明一个组件。

### 吻合的部分

中国的 Injector 2 是唯一同时符合 DNS 三项特征的注入器，包括伪造回应里的标志值、回应里使用压缩指针（DNS 数据包里重复引用域名的写法），以及解析查询时处理压缩指针的上限。作者认为这些结果强烈暗示（strongly suggest）TSG 提供了 Injector 2 的 DNS 注入实现。

TSG 伪造 RST 数据包时，用一个自制的随机数生成器填入头部的几个字段。从 GFW II 与 GFW III 发出的数据包，可以反推出固定的种子值（随机数生成器的起始值），而且就是 TSG 的默认值。作者估计固定的种子值碰巧出现的概率约为 10 的负 44 次方，再加上数值与 TSG 的默认值相同，论文用 strongly indicating（强烈表示）形容两者用了 TSG 的代码。

同一节也列出两者与 TSG 的偏差，GFW II 与 GFW III 发出的 RST 都使用固定的 TTL（数据包还能经过几个路由器的计数），TSG 的 TTL 则随内部状态变化。2023 年 12 月的测量里，GFW II 的 TTL 还与 TSG 一致，作者据此推测 GFW II 之后稍微改了实现。过去的研究记录到 GFW II 每次连发的几个 RST 完全相同，研究团队把 TSG 设成同样一次连发几个 RST 时，数据包之间的 IPID（IP 数据包的标识字段）会变动。

IP 分片重组也有吻合的项目，GFW II 一次重组的分片上限与 TSG 非常接近。作者在这一项的说法较保守，只写两者可能共用相近的代码（potentially share similar code）。

TLS 的测试篡改 ClientHello（TLS 连接的第一个数据包）里的各个长度字段，看设备是否仍然解析出域名并封锁。没有任何设备与外泄的最新版行为完全相同，GFW II 的行为等同 TSG 较旧版本的 SSL 模块，作者推测 GFW II 解析 TLS 时用的就是这个旧版。QUIC 的结果是防火长城与哈萨克斯坦拦下的测试数据包与 TSG 相同，但两地支持的 QUIC 版本与 TSG 不同，无法完全吻合。哈萨克斯坦的解析指纹则完全符合 TSG 较旧版本的 QUIC 解析代码。

论文第 6 节把这些结果总结成一句：Injector 2、GFW II 与 GFW III 高度吻合，suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall。中文可以译成「显示外泄的 TSG 代码（或与它相近的衍生版本）很可能部署在中国国家防火墙的一部分」，引导这句的 suggesting 是推论的语气，indeed（确实）是原文的强调。吻合的多半是旧版模块，geedge.report 的文章同样写到吻合的情况会随时间改变，部署中的代码已经与外泄的版本有差异。

### 不吻合或无法判断的部分

Injector 1 与 Injector 3 不吻合。Injector 3 在这次测量里的标志不同，也不再使用压缩指针，与 2020 年最初的观察不一样。GFW I、河南、缅甸，以及巴基斯坦发出 RST 的那一套设备，都没有固定的种子值。GFW III、河南、哈萨克斯坦，以及巴基斯坦发出 RST 的那一套设备，都不重组 IP 分片，直接转发。论文注明是否重组是 TSG 配置文件可以调整的选项。

缅甸的 RST 行为可以用 TSG 的配置重现，支持的 QUIC 版本也与 TSG 完全相同，但解析指纹不符，论文的结论是 cannot confirm its use，无法确认缅甸使用 TSG。哈萨克斯坦与巴基斯坦的部分设备以丢包封锁，测试数据包是否绕过无法判定，两地的结果在论文里写成 support potential TSG deployments（与可能有 TSG 部署的推论相容）。哈萨克斯坦的审查设备不发 RST，所以没有做 RST 的比对。哈萨克斯坦虽然有 QUIC 解析与旧版完全相符的结果，论文仍然没有把它写成确认部署。伊朗的 DNS 标志与 TSG 不同，埃塞俄比亚只出现在外泄的工单里，没有测量。

Geedge 在这些国家有客户的证据来自文件，论文的背景一节引用民间调查，列出哈萨克斯坦、埃塞俄比亚、巴基斯坦与缅甸的部署，外泄的 Jira 工单也以缅甸与埃塞俄比亚的现场为主。就 USENIX 论文的测量而言，到目前为止能与 TSG 代码高度吻合的，只有中国的部分设备。

### 报道与论文的措辞差距

Risky Bulletin 的报道写 TSG 是防火长城「三种已知流量过滤能力之一」（one of the Great Firewall's three known traffic filtering capabilities），论文全文没有这种说法。「三种」可能来自过去研究对防火长城设备的分类。DNS 注入器分成三个，论文的结果是吻合一个。发出 RST 的注入器也分成 GFW I、II、III，吻合两个。同一篇报道引用的研究者帖子也写到 Geedge 只是参与防火长城的厂商之一。geedge.report 首页写的是「China's Great Firewall is running parts of TSG」，语气同样比论文的推论肯定。

论文支持的说法是防火长城的一部分设备用了 TSG 或与它相近的版本，其他测量过的设备与 TSG 不吻合，由谁提供目前没有公开的证据。论文也没有写 Geedge 开发了防火长城，用的词是 ties、affiliated，以及与 MESA 实验室的 close collaborative relationship。这个范围比把 Geedge 等同于防火长城的说法窄很多，但它同时有源代码里的默认值与远程测量两边的证据，过去只靠远程推测的研究无法做到。

## 规避工具的签名与封锁

USENIX 论文写到，外泄文件里有依客户需求反复封锁特定规避工具的记录，对象包括 Psiphon、Tor 与 ExpressVPN、NordVPN 等常见的 VPN，手法从封锁 IP 到比对字节模式都有。签名（描述某个 App 流量特征的规则）结合了服务器 IP、域名、TLS 指纹、证书字段、数据包长度与字节模式。论文分析的一份 Confluence 文档记录了 2024 年 3 月到 11 月间一个签名包的多次更新，里面的签名风险等级在三到五之间，多数是五，另一份以中国 App 为主的测试记录则全部是一。具体的签名条件写在论文的表格里，本文不转述。

研究团队在 Jira 里搜索 vpn，找到 182 个议题下的 700 条记录，内容包括上报提取出的服务器 IP、排定封锁的优先级、签名失效之后反复修改，以及误封其他服务。其中一条工单记录 Signal 开启反审查选项之后封锁失效。作者的归纳是，规避工具的签名由客户参与调整，客户可以上报失效、排定优先级、标出误封的情况。

在 Psiphon 的记录里，检测的成本因为混淆（让流量看起来不像任何已知协议的技术）而提高。一份分析封锁 Psiphon 附带损害的内部文件写到，Psiphon 的流量没有明显的特征，所以改用服务器 IP 识别，再加上一套白名单保护机制避免误判。一条工单也讨论了用 IP 与 SNI 封锁时误封的风险。作者在结论把这件事与 TSG 的另一面并列：TSG 能以相对低的成本识别规避工具，常常在连接一开始就比对出来。

论文里与 TSG 封锁 Tor 有关的内容，只有引言的对象清单与签名的风险等级表，表里有一项 Tor Browser。论文没有描述 Tor Browser 签名的内容，也没有测试 Tor 的连接，所以无法从论文得知 TSG 如何识别 Tor，更无法推论它能封锁 Tor。InterSecLab 的〈The Internet Coup〉读的是文件，报告写到在外泄的时间点，Geedge 似乎还没有有效对付 WebTunnel（Tor 的一种可插拔传输，把流量伪装成普通的 HTTPS 网页连接）的手段，MESA 实验室的学生做过封锁方法的初步研究。报告也写明没有找到 Geedge 发现或利用 Tor 未知漏洞的证据，并与 Tor Project 协调了披露的方式。

FOCI 论文从域名的角度补上一块，外泄文件里有多个文件专门针对 VPN 与规避工具，包括商用 VPN 的完整服务器清单与 Psiphon 的 CDN 域名。对规避工具的开发者来说，服务器的 IP 与域名本身就是收集与封锁的对象，流量特征只是其中一种手段。

至于代码的质量，论文的结论写 TSG 的复杂性与灵活性是双刃剑，增加了规避的难度，也损害了代码的可维护性与正确性。核心组件 SAPP 与协议插件以缺乏内存安全保障的 C 编写，系统仍然依赖 Stellar-on-SAPP 这类过渡方案，代码也从多个第三方复制而来。工单里有一条升级 AppSketch 数据库之后 SAPP 重新启动的记录，作者形容这是东拼西凑（patchwork）的开发过程，也写到适合后续用模糊测试（fuzzing，大量输入异常数据、找出程序错误的方法）与符号执行（以符号代替实际输入、推算程序各条执行路径的分析方法）深入研究。论文没有提出任何 CVE 编号或可以利用的具体漏洞。

## 域名清单的覆盖范围

审查测量要先决定测哪些域名，常用的清单有两份。Tranco 是按流量排名的热门网站清单，Citizen Lab 的检测清单由研究者与社区人工维护，按内容类型整理可能被封锁的网站。FOCI 论文从外泄文件提取了 1,436 万多个候选域名，解析过滤之后剩下 6,915,266 个。广州与南京的测量点测 DNS 注入，可靠性较高。巴基斯坦、缅甸与阿尔及利亚的测量点测 TLS 握手是否因 SNI 被中断，可靠性较低。每个域名测 25 次，把间歇性的封锁也算进去。哈萨克斯坦与埃塞俄比亚虽然是已知的客户，研究团队无法取得合适的测量点。

结果是外泄文件里实测被封锁的域名中，298,955 个（93.7%）同时不在 Tranco 与 Citizen Lab 的清单里。相对地，外泄文件只覆盖被封锁的 Tranco 域名的 37.1% 到 61.6%。三份清单各有分工，FOCI 的说法是 Tranco 回答哪些全球热门网站被封锁，Citizen Lab 长期跟踪各类敏感内容，外泄文件则呈现商用审查厂商认为值得关注的域名。

解读这些数字之前要先理解域名的来源，FOCI 写明不把出现在外泄文件里的域名当成被封锁的域名。明确的封锁清单属于客户的敏感数据，在外泄文件里很少见，域名多半出自内部讨论客户环境的文件，代表 Geedge 或客户「感兴趣」（of interest）的内容。数量最多的来源是 MESA 实验室的 SNI 数据集，作者判断看来是从网络分流器（network tap，在线路上复制流量的设备）收集的。外泄文件里也有 Alexa 与 SecRank 等排名清单的副本，供 MESA 的研究使用。所以 93.7% 说明的是常用清单的缺口。外泄文件提供了厂商端的视角，哪些域名真的被封锁仍要靠测量确认，与 USENIX 论文先读代码、再回到网络比对的做法相同。

社区维护的 Citizen Lab 检测清单台湾部分（`anoni-net/citizenlab-test-lists` 的 `tw.csv`）同样是人工整理的清单，反映的是维护者认为重要的内容。从 FOCI 的结果来看，用清单测量没有测到封锁时，结论只涵盖清单里的网站，清单以外的域名本来就不在观测范围内。单次测量如何判读见[OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)，各网络有多少测量见[OONI 观测覆盖率](/projects/asn-coverage/)。

## 供应链与政策

InterSecLab 的〈MADLink〉从外泄文件追到硬件供应链。台湾上市公司凌华科技在 2019 到 2020 年初向 Geedge 出货 1,708 台 CSA-7400（厂商营销定位用于防火墙与 DPI 的高密度网络平台），依报告是第一代 TSG 平台的硬件基础，外泄文件里这套配置只部署在哈萨克斯坦。Geedge 自制的 EtherFabric（在多个 TSG 节点之间分配流量的网络数据包代理设备）部署在缅甸，外泄文件里它的管理接口 MAC 地址的厂商前缀登记在凌华名下，InterSecLab 据此判断里面有凌华的组件，最可能是管理用的计算主板。

凌华科技向 InterSecLab 证实了出货的数量，表示出货前做了出口管制名单筛查、Geedge 不在受限名单上，并将启动内部审计。凌华也表示公司只提供通用的硬件平台，没有参与与最终用途相关的软件集成或系统设计。InterSecLab 的反驳是，外泄文件里有 TSG-ADC 的负载均衡依赖凌华 PacketManager 软件的记录，CSA-7400 的营销定位也是 DPI 与防火墙设备。经济部说明台湾的出口管制框架参照国际防扩散机制与制裁清单，以法律限制为由不评论个案。

报告的论点是，Geedge 现行的服务器多是通用的 x86 硬件，正规采购受阻时仍能从二手市场取得，CSA-7400 这类专为 DPI 与防火墙设计的设备才是出口管制能实际着力的地方。社区翻译了[报告全文](https://anoni.net/docs/reports/interseclab-madlink/)，也记录了[台湾公共领域对 MADLink 报告的反应](/updates/2026/05/madlink-editorial-2026-05/)。

MADLink 读的是文件与厂商的回复，可以对照 USENIX 论文在哈萨克斯坦的三项测量：QUIC 解析符合旧版、TLS 因为丢包无法判定、RST 无法比对。两者之间有时间差，CSA-7400 是 2019 到 2020 年初出货的第一代硬件，与论文的测量相隔数年，测量到的设备是否仍是那一批硬件，目前无法判断。

MADLink 也提到，Geedge 现行硬件里的服务器来自 Nettrix，它的母公司中科曙光已经遭到美国制裁。Justice For Myanmar 在 2024 年 6 月 19 日的新闻稿呼吁各国政府制裁 Geedge Networks 等公司。截至 2026 年 10 月，我们在 OFAC 的公告、OpenSanctions 与公开报道里，都没有查到 Geedge 被列入制裁名单。

## 研究伦理与数据处理

USENIX 论文的伦理考量一节列出五类利益相关方，包括 Geedge 的员工与股东、代码被集成进 TSG 的第三方公司、部署 TSG 的国家、在这些国家受审查的用户，以及反审查社区。外泄的 Git 仓库里有开发者的姓名与 email，论文的处理方式是聚焦在系统与架构，不报道个人，公开的仓库里也不放外泄的原始数据。

在本机运行一份 TSG 本身也有风险，可能让部署国改进系统，或让其他审查者更容易部署。论文因此选择不公开架设这套防火墙的方式，公开的数据只放对识别部署有用的内容。研究团队也考虑过完全不在本机运行。他们的结论是，有了一份可运行的副本，反审查社区才能识别各地的部署，对着真实的系统开发与测试规避策略，再把策略推广到其他国家的防火墙。

测量只在研究团队自己拥有的两台主机之间进行，不以任何第三方服务器为目标，租用测量点时也确认对方不在欧盟的制裁名单上。外泄的源代码与研究团队的构建都不公开，作者承诺依请求把构建分享给可信任的网络安全研究者，公开在 Zenodo 的是测量结果、匿名化的数据包记录与测量用的脚本。这些取舍的结果是，其他研究者可以用公开的脚本重做远程测量，源代码端的对照则只有取得分享的研究者能重做。

FOCI 论文的立场是，外泄数据已经由 Enlace Hacktivista 与 DDoSecrets 公开，广泛的公共利益优先于可能的知识产权疑虑。GFW Report 的分析文章则建议只在隔离、不联网的（虚拟）机器上分析这些文件。

Lantern 的 geedge.lantern.io 采取另一种处理方式，页面上写它是 corpus.lantern.io 的姊妹项目，目的是让规避工具的开发者清楚知道自己面对什么，但页面没有写明背后的团队，与 Lantern 规避工具的关系也无法从页面确认。索引不转载外泄的原始内容，每一条发现都附上指向出处的指针。

索引里的发现由 LLM 自动提取，页面写明提取工作由 Sonnet 等级的代理读取批量文本完成，我们读取时首页列出 880 条发现。我们抽查了五条，都标成最高的置信等级。其中三条只凭配置文件的字段名称就推论系统会记录每一条连接，出处多是测试用的配置文件，也没有 commit hash。Lantern 的索引可以当成找线索的起点，引用前要自行回到原始数据核对，不能直接当成证据。

在 net4people 的讨论帖里，2025 年 10 月之后有出处的后续研究只有 FOCI 论文，其他多是留言者的比对与推测，部分留言附上外泄内部系统的镜像链接，本文不引用。

本文也守同样的界线，不转载外泄文件的内容、域名清单与文件路径，不写可以用来规避检测或改进封锁的参数、特征值与签名条件（论文本身公开了一部分，想深入的读者请读原文），也不提外泄数据里的人员。

## 还没有答案的问题

Injector 1、Injector 3 与 GFW I 都与 TSG 不吻合，论文的结果只指向防火长城的一部分设备用了 TSG 或相近的代码，其余设备由谁开发，目前没有公开的证据。

哈萨克斯坦、巴基斯坦、缅甸与埃塞俄比亚的客户关系都有文件证据，测量却停在可能或无法确认。FOCI 的研究团队无法取得哈萨克斯坦与埃塞俄比亚的测量点，USENIX 论文在哈萨克斯坦有测量点但部分项目无法判定，埃塞俄比亚两篇论文都没有测量。部署端也一直在改版，外泄文件停在 2024 年 11 月，GFW II 的 TTL 从 2023 年 12 月到论文测量时已经改变，之后的测量要把版本的差异算进去。

研究团队的构建只加载了 DNS、SSL 与 QUIC 三个 SAPP 协议插件，AppSketch 数据库的存档都经过加密。签名格式如何转换成 Maat 的规则，论文没有找到对应的代码，只从格式的相似度推论，源代码还有许多部分没有人审查。作者的期待是让这篇论文成为后续研究的指引。FOCI 也列出外泄文件里的 IP 地址、PDF 与更好的文字识别，以及比对 Common Crawl 与 ICANN 的域名数据，作为之后的工作。

规避工具这一端，我们在 net4people 跟踪外泄的讨论帖（2025 年 10 月以后的留言）里，没有看到 Tor、Psiphon 或 VPN 厂商公开说明为应对外泄做了哪些调整。Tor Project 也审阅过〈The Internet Coup〉的 Tor 一节，Psiphon 团队审阅了 Psiphon 一节。外泄已经让研究界能用源代码对照真实的审查设备，下一步要看测量点是否能扩展到更多客户国家，以及工具开发者如何运用这些结果。欢迎到社区的 [Matrix](/contact/) 一起讨论。

## 参考资料

- [Technical Analysis of the Geedge Networks Firewall Source Code Leak](https://www.usenix.org/conference/usenixsecurity26/presentation/ablove)：USENIX Security 2026，密歇根大学、帕德博恩大学、马萨诸塞大学阿默斯特分校、科罗拉多大学博尔德分校与 GFW Report
- [Geedge Cases: Censorship Measurement Insights from the Geedge Networks Leak](https://gfw.report/publications/foci26b/en/)：FOCI 2026，马萨诸塞大学阿默斯特分校与 GFW Report，2026-02-19
- [geedge.report](https://geedge.report/)：USENIX 论文作者群的项目网站，摘要文章 [Geedge firewall source code analysis](https://geedge.report/posts/2026/08/geedge-firewall-source-code-analysis/) 发表于 2026-08-05
- [Geedge & MESA Leak: Analyzing the Great Firewall's Largest Document Leak](https://gfw.report/blog/geedge_and_mesa_leak/en/)：GFW Report，2025-09-12，2025-12-29 更新
- [The Internet Coup](https://interseclab.org/research/the-internet-coup/)：InterSecLab，2025-09-09
- [MADLink: A Taiwanese Vestige in the Geedge Supply Chain](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/)：InterSecLab，2026-04-24
- [Pakistan: Shadows of Control](https://www.amnesty.org/en/documents/asa33/0206/2025/en/)：国际特赦组织，2025-09
- [Silk Road of Surveillance](https://www.justiceformyanmar.org/stories/silk-road-of-surveillance)：Justice For Myanmar，2025-09
- [JFM calls for action against Chinese and Myanmar companies involved in junta digital surveillance and censorship](https://www.justiceformyanmar.org/press-releases/jfm-calls-for-action-against-chinese-and-myanmar-companies-involved-in-junta-digital-surveillance-and-censorship)：Justice For Myanmar 的新闻稿，2024-06-19
- [Leaked files show a Chinese company is exporting the Great Firewall's censorship technology](https://www.theglobeandmail.com/world/article-leaked-files-show-a-chinese-company-is-exporting-the-great-firewalls/)：The Globe and Mail，2025-09-08
- [Academics find source code overlaps between Geedge and China's Great Firewall](https://news.risky.biz/risky-bulletin-academics-find-source-code-overlaps-between-geedge-and-chinas-great-firewall/)：Risky Bulletin，2026-08-21
- [geedge.lantern.io](https://geedge.lantern.io/)：Lantern 的外泄索引，内容由 LLM 自动提取，只能当线索

## 相关阅读

- [网络政变](https://anoni.net/docs/reports/interseclab-network-coup/)：InterSecLab〈The Internet Coup〉的社区中译（正体中文）
- [MADLink：台湾在 Geedge 供应链中的遗留](https://anoni.net/docs/reports/interseclab-madlink/)：InterSecLab〈MADLink〉的社区中译（正体中文）
- [OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)：单次测量的判定与确认封锁之间的差距
- [OONI 观测覆盖率](/projects/asn-coverage/)：台湾与邻近地区的测量来自哪些网络
