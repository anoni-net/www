---
title: Geedge 外泄一年后的研究回顾
description: Geedge Networks 与 MESA 实验室的内部文件外泄之后，研究界第一次能用商用审查设备的源代码对照防火长城。本文整理一年来两篇论文与民间调查确认了什么、还不确定什么，以及报道与论文说法之间的落差。
date: 2026-10-30
---

近三十年来，研究者几乎只能从墙外推测防火长城如何运作。方法是发出设计过的数据包，记录哪些被拦、用什么方式被拦，再反推背后的设备。Geedge Networks（积至公司）的内部文件外泄之后，研究者第一次取得一家与防火长城关系密切的商用审查厂商的源代码、构建软件包与工单。USENIX Security 2026 论文的作者写明，商用 DPI（深度包检测，逐条分析连接内容、判断要不要放行的技术）的源代码是第一次外泄[^blackbox]。研究者可以先读代码找出特征，再回到真实的网络比对，不必只靠黑箱推测。

一年下来，比对出来的范围比部分报道写的窄，从测量结果看，外泄的代码或与它相近的衍生版本很可能部署在防火长城的一部分设备上。同样测量过的其他几台防火长城设备与它不吻合，TLS 的比对里没有任何一台设备与外泄的最新版完全相同，其他客户国家多半停在「可能」或「无法确认」[^summary][^nomatch][^mm-kz-pk]。相对地，这些结论同时有源代码与测量两边的证据，比过去只靠远程推测扎实。这篇回顾写给开发规避工具、做测量研究与关心供应链的读者，技术细节只写到机制层级，想深入的读者请读原论文。

<details markdown="1">
<summary>给不熟悉技术的读者</summary>

2025 年 9 月，为中国与其他国家构建网络审查系统的 Geedge Networks 发生外泄，内部文件与源代码都被公开。研究者第一次可以直接读审查设备的程序，不必只从外面推测。

研究团队把程序实际构建起来，再到真实的网络上比对。从结果看，中国防火长城有一部分设备很可能用了这套程序或相近的版本，其他设备与它不吻合，由谁开发目前没有公开的证据。依外泄文件，Geedge 也把系统卖到哈萨克斯坦、埃塞俄比亚、巴基斯坦与缅甸，但在这些国家，测量多半只能做到「可能」或「无法确认」。

翻墙工具与 VPN 一直是追踪与封锁的对象，客户会上报哪些工具还能连接，Geedge 再调整封锁规则。论文没有测试 Tor。InterSecLab 的报告里写到，外泄时 Geedge 似乎还没有有效封锁 WebTunnel（Tor 把流量伪装成普通网页浏览的连接方式）的手段，InterSecLab 也没有找到 Geedge 发现或利用 Tor 未知漏洞的证据。

外泄数据里实测被封锁的网站，九成以上不在研究者常用来测量的两份网站清单里，所以用清单测量没有发现封锁，不等于没有封锁。

台湾的凌华科技在 2019 到 2020 年初出货一批硬件给 Geedge，Geedge 至今不在我们比对的美国与欧盟制裁名单上。

想先了解背景，可以读文件站的[网络自由为什么重要](https://anoni.net/docs/zh-cn/basics/internet-freedom/)、[监控现在做得到什么](https://anoni.net/docs/zh-cn/basics/surveillance-capability/)、[什么是 Tor](https://anoni.net/docs/zh-cn/tools/what-is-tor/) 与 [VPN 的风险与选择](https://anoni.net/docs/zh-cn/tools/vpn-guide/)。

</details>

## 一年来的研究

外泄一年来，联合调查的团队读文件、整理 Geedge 的客户与部署，学界读源代码、做远程测量，两边取得的证据性质不同。
{: .sec-lead }

外泄的文件来自 Geedge 与 MESA 实验室两边。MESA 实验室（Massive and Effective Stream Analysis）隶属中国科学院信息工程研究所，GFW Report 形容两者是防火长城研发能力的重要分支。依 GFW Report 的整理，Geedge 在 2018 年于海南成立，被称为「防火长城之父」的方滨兴担任首席科学家。FOCI 论文统计外泄的总量是 572 GiB，包含源代码库、项目管理记录、客户的部署配置与运营数据，其中八成以上是一个 RPM 软件包仓库（Linux 的软件安装包）的存档[^gfwr-geedge]。

![外泄文件记录的 Geedge 部署地点地图，标出哈萨克斯坦、埃塞俄比亚、巴基斯坦、缅甸，以及中国的新疆、福建、江苏](https://assets.anoni.net/www/articles/geedge-leak-one-year-map-e2b327c5.svg){: .map-img width="720" height="426" loading="lazy" }

外泄文件记录的 Geedge 部署地点。客户国家用主色标示：① 哈萨克斯坦（`K18`、`K24`）、② 埃塞俄比亚（`E21`）、③ 巴基斯坦（`P19`）、④ 缅甸（`M22`）。中国用另一种色调标示，圆点是省级防火墙项目：⑤ 新疆（`J24`）、⑥ 福建、⑦ 江苏。身份不明的 `A24` 没有标在图上[^map]。
{: .fig-note }

- **2025 年 9 月 8 日起**：The Globe and Mail 刊出报道，InterSecLab 在 9 月 9 日发表报告〈The Internet Coup〉，国际特赦组织的《Shadows of Control》与 Justice For Myanmar 的《Silk Road of Surveillance》也在同一个月发表。
- **2025 年 9 月 11 日**：Enlace Hacktivista 公开全部文件，DDoSecrets 也提供下载。
- **2025 年 9 月 12 日**：GFW Report 发表外泄的分析文章，最后一次更新是 12 月 29 日。文中写明源代码的部分还没有人仔细分析[^gfwr-src]。
- **2026 年 2 月 19 日**：马萨诸塞大学阿默斯特分校与 GFW Report 的研究者发表 FOCI 2026 论文〈Geedge Cases〉，比对外泄文件里的域名与两份常用的域名清单。
- **2026 年 4 月 24 日**：InterSecLab 发表〈MADLink〉，供应链系列的第一篇，主题是 Geedge 使用的服务器与网络硬件，其中包括台湾的凌华科技。
- **2026 年 8 月**：作者群 8 月 5 日在项目网站 geedge.report 发表说明文章。论文〈Technical Analysis of the Geedge Networks Firewall Source Code Leak〉在 8 月 12 日到 14 日的 USENIX Security 2026 发表，作者来自密歇根大学、帕德博恩大学、马萨诸塞大学阿默斯特分校、科罗拉多大学博尔德分校与 GFW Report。Risky Bulletin 在 8 月 21 日报道。

报道比文件公开早了三天。USENIX 论文的引言写到，几家提前取得文件的新闻机构与记者过去一年合作分析这批文件，角度偏向非技术面[^early]。依[〈The Internet Coup〉译文](https://anoni.net/docs/reports/interseclab-network-coup/)的致谢，Tor Project 也是这次联合调查的合作伙伴[^coup-ack]。联合调查读的是文件与工单，整理出 Geedge 的客户、部署的国家与产品功能。在 USENIX 论文之前，源代码本身大致还没有人分析[^early]。学界的研究是另一条线，读源代码、把系统构建起来，再做远程测量。

从文件可以知道 Geedge 卖给谁、客户要求什么，测量则用来判断某一台设备的行为是否与代码一致。部分报道把前者的结论套到后者（例子见后面的报道与论文的措辞差距一节）。

这篇回顾主要依据五份论文与报告，研究范围与方法差异很大，读原文前可以先对照下表（出处与链接见文末的参考资料）。

| 论文或报告 | 研究范围 | 方法 | 适合的读者 |
|---|---|---|---|
| 〈Technical Analysis of the Geedge Networks Firewall Source Code Leak〉，USENIX Security 2026 | TSG 的架构与第三方代码，TSG 与防火长城、河南、哈萨克斯坦、缅甸、巴基斯坦、伊朗审查设备的行为比对，以及工单里规避工具签名的调整记录 | 读源代码、构建最新的标记版本并在隔离环境测试，再从各地的测量点远程比对 DNS、IP 分片、TCP、TLS 与 QUIC 的指纹[^build][^method] | 研究 DPI 指纹、审查测量与规避工具的研究者 |
| 〈Geedge Cases〉，FOCI 2026 | 外泄文件里出现的域名，与 Tranco、Citizen Lab 检测清单的覆盖差异 | 从外泄文件提取候选域名、解析过滤，在中国、巴基斯坦、缅甸与阿尔及利亚的测量点测 DNS 注入与 TLS SNI 封锁，每个域名测 25 次[^foci-meas] | 维护检测清单、决定测量目标的研究者 |
| 〈The Internet Coup〉，InterSecLab，2025 年 9 月 | Geedge 的产品、客户国家与部署方式，与 MESA 实验室的关系，对规避工具的处理 | 读外泄的文件与工单，与媒体和民间组织的联合调查分工[^coup-ack] | 想了解客户、部署与人权影响的读者，社区有中译 |
| 〈MADLink〉，InterSecLab，2026 年 4 月 | TSG 三代硬件的来源与供应商，凌华科技的出货 | 比对外泄文件里的硬件记录与 MAC 地址的厂商前缀，向厂商与经济部询问[^madlink-hw] | 研究出口管制与供应链的读者，社区有中译 |
| 〈Geedge & MESA Leak〉，GFW Report，2025 年 9 月 | 外泄文件的组成、Geedge 与 MESA 实验室的背景，已发表调查的整理 | 整理文件结构与既有的报道，附上安全处理文件的建议[^gfwr-geedge] | 第一次接触这批数据的研究者 |

## 源代码里的 TSG

研究团队把外泄的源代码构建成可以运行的 TSG，看出它由几个各自开发的组件组成，三套识别系统里有两套建立在第三方代码上。
{: .sec-lead }

### 构建与测试

USENIX 论文分析的是 Geedge 的旗舰产品天狗安全网关（Tiangou Secure Gateway，TSG），作者形容它是可以完整集成进国家电信管制的审查平台。外泄的内部文件超过 10 万份，光是 Git 仓库就有 500 多个，涵盖五年以上的 commit 历史，最新的文件到 2024 年 11 月。分析的难处在于 TSG 的逻辑分散在许多仓库里，同一个组件有多个分支与版本，论文还找到至少两套各自独立的 IP、UDP、TCP 协议栈（程序里实现 IP、TCP 等基础协议的部分）。

研究团队依 DPI 的四个阶段读代码，也就是接收流量、重组与解析、比对规则、干扰连接。构建时，研究团队从最新的标签版本着手，对应多个仓库与软件包仓库，并绕过了授权检查。

构建完成之后，研究团队在隔离的测试环境里测试了 DNS、HTTP、TLS 与 QUIC（一种在 UDP 上传输的协议，HTTP/3 使用它）的处理，成功触发伪造响应的注入、丢包与延迟封锁，也用规则引擎定义了一个自定义的封锁对象[^build]。三套应用识别系统（见下方第三方代码一节）是否都在这份构建里运行，论文没有交代，所以本文只写到研究团队构建并运行了 TSG 最新的标签版本，在本机测试了几种协议的封锁行为。论文刻意不公开完整的构建做法，理由见后面的研究伦理一节。

### 核心组件

TSG 由几个分开开发、各有版本的组件组成。SAPP 是最底层的数据包处理平台，MESA 实验室从 2005 年开始开发，经过四次大改版，用 C 编写。SAPP 把数据包整理成 TCP、UDP 流再交给插件，本身不做封锁决定，只提供封锁需要的功能。插件分成三类，平台插件提供共用功能，协议插件从 DNS 查询、TLS 与 QUIC 的握手取出域名等字段，业务插件用这些字段实现封锁之类的应用逻辑。

Stellar 是 Geedge 另外开发、用 C++ 编写的平台，跟踪连接状态的能力比 SAPP 完整，插件之间的通信方式也更多样。Stellar-on-SAPP 是 SAPP 的平台插件，把 SAPP 的流转成 Stellar 的会话（session）交给 Stellar 的插件处理，README 写明它是两个平台之间的过渡方案。在外泄的版本里，Stellar 的插件就是经由 Stellar-on-SAPP 在 SAPP 上运行。独立的 stellar 仓库当时还在开发中，没有出现在任何构建仓库里，也没有接入 TSG。

Maat 是规则引擎，封锁规则存在 Maat 里，插件用取出的字段比对规则，取得处置方式。规则可以比对的字段很广，包括传输层与应用层协议、隧道封装的内外层地址、来源与目的 IP、端口、域名与 SNI（TLS 连接开头以明文发送的网站名称）、ASN（自治系统编号）与国家。Firewall 插件同时挂在 SAPP 与 Stellar 上，汇总各路取出的字段，查询 Maat 之后执行封锁。封锁手段除了丢包与 RST（TCP 的重置数据包，发出后连接就会中断），还有限速、HTTP 与 DNS 的重定向、邮件与 SIP 的封锁、篡改内容与延迟封锁。

一条连接经过 TSG 的处理可以简化成下面这条路径，实际上多条处理路径同时进行，最后在 Firewall 插件汇总[^modular]。

<ol class="flow" aria-label="TSG 处理一条连接的简化流程">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>数据包接收与重组（SAPP）</b><span class="d">接收流量，把数据包整理成 TCP、UDP 流，交给插件</span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>字段提取（协议插件）</b><span class="d">从 DNS 查询、TLS 与 QUIC 的握手提取域名、SNI 等字段</span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>应用程序识别</b><span class="d">三套系统判断流量属于哪个 App</span><span class="out"><span>CBD：Geedge 自有</span><span>Glimpse：libprotoident、nDPI</span><span>QDPI：Qosmos ixEngine</span></span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>规则比对（Firewall 插件与 Maat）</b><span class="d">汇总各路提取的字段与识别结果，比对 Maat 里的封锁规则</span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>处置</b><span class="d">放行，或丢包、发送 RST、限速、重定向、篡改内容、延迟封锁</span></span></li>
</ol>

作者从架构归纳出两点，后面的比对都受它们影响。组件各自开发、各有版本，从远程测出某一个插件的指纹（能用来辨认某个系统或版本的特征），不代表同一个部署也有另一个插件，也无法推论另一个插件的版本。封锁决定在多条处理路径汇总之后才做出，一条连接可能因为其中任何一条路径的结果而被拦[^modular]。

### 第三方代码

TSG 有三套应用识别系统，用来判断一条流量属于哪个 App 或协议，其中两套建立在第三方代码上。CBD（Context-Based Detector，前身是 AppSketch）是 TSG 自己的系统，依 Maat 加载的签名判断。Glimpse 的协议分类核心是怀卡托大学 Libtrace 团队的自由软件 libprotoident，分类函数需要的代码都带着 libprotoident 的版权声明。Glimpse 检测 OpenVPN 的代码，依论文的描述看来是 2022 年某一版 nDPI（以 GPL 授权的 DPI 函数库）的修改副本，主要函数改了名称，逻辑几乎相同。第三套 QDPI 建立在 Qosmos ixEngine 上，那是商用的闭源 DPI 函数库，作者的依据是代码调用了 ixEngine 的函数并引用它的头文件[^thirdparty]。

论文对 libprotoident 与 nDPI 的用词是复制后改写，对 Qosmos 只写建立在它之上，没有判断 Geedge 是否取得授权。研究团队把 Geedge 使用这些代码的情形通报 libprotoident 团队与 Qosmos 的母公司 Enea，论文发表时双方都已回复，也排定了会议，回应的内容没有公开。nDPI 不在论文列出的通报对象里。作者认为这显示即使是资源充足、与国家有关系的厂商，从零建立完整的协议分类也很昂贵（原文用 suggests）[^disclose]。这类发现需要读源代码才能取得，远程测量很难判断识别系统用了谁的代码[^beyond]。

## 与防火长城的比对

论文里写成高度吻合的只有防火长城的三台设备（Injector 2、GFW II 与 GFW III），其他设备与各客户国家多半不吻合或无法判断。
{: .sec-lead }

### 比对的方法

USENIX 论文写到，防火长城过去被认为高度集中，近年却有越来越多证据指向多台独立运作、分工不同的 DPI 设备，过去的测量研究也替其中几种设备命名[^gfw-multi]。DNS 注入（审查设备抢在真正的服务器之前发回伪造的 DNS 响应）的设备分成 Injector 1、2、3，名称来自 FOCI 2020 的〈Triplet Censors〉。发出 RST 中断 TCP 连接的设备分成 GFW I、II、III，河南省另有一套区域性的审查，名称来自 IEEE S&P 2025 的〈A Wall Behind A Wall〉。

研究团队从源代码找出可以从远程测量的特征，例如解析协议时的特殊处理方式，以及设置数据包字段用的自制随机数生成器。接着在两台自己拥有的主机之间发出测试数据包，比较各地审查设备的反应是否与 TSG 相同。测量涵盖中国的防火长城、河南、哈萨克斯坦、缅甸与巴基斯坦，伊朗只测了 DNS，协议包括 DNS、IP 分片重组、TCP、TLS 与 QUIC。

比对分成四个步骤，最后判定结果，每一项比对都同时有源代码与测量两边的依据[^method]：

<ol class="flow" aria-label="比对的步骤">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>源代码分析</b><span class="d">找出可以从远程观察的行为，例如伪造数据包的字段、解析协议时的特殊处理</span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>本机验证</b><span class="d">在隔离的测试环境运行 TSG，确认这些行为确实会出现</span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>远程测量</b><span class="d">从各地的测量点，对研究团队自己的主机发出测试数据包，记录审查设备的反应</span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>行为对照</b><span class="d">把实测的反应与 TSG 的行为逐项比较</span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>判定</b><span class="d">每一项比对归入比对矩阵图例里的一种结果</span><span class="out"><span>吻合、与较旧的版本相同、部分相符</span><span>不吻合、无法判断</span></span></span></li>
</ol>

审查设备接入网络的方式有两种，测量能看出多少，跟设备用哪一种方式部署有关[^modes]：

<figure class="pd-fig">
<svg class="pd" viewBox="0 0 360 352" role="img" aria-labelledby="pd-t">
<title id="pd-t">镜像模式与内联模式的审查设备</title>
<defs><marker id="pd-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="pd-ah" d="M0 0L10 5L0 10z"/></marker>
<marker id="pd-ai" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="pd-ahi" d="M0 0L10 5L0 10z"/></marker></defs>
<text class="pd-h" x="0" y="16">镜像模式：在线路旁边复制流量</text>
<text class="pd-s" x="180" y="48" text-anchor="middle">原本的数据包照常送达网站</text>
<line class="pd-wire" x1="74" y1="76" x2="284" y2="76" marker-end="url(#pd-a)"/>
<rect class="pd-box" x="2" y="59" width="72" height="34" rx="6"/><text class="pd-t" x="38" y="76">用户</text>
<rect class="pd-box" x="286" y="59" width="72" height="34" rx="6"/><text class="pd-t" x="322" y="76">网站</text>
<line class="pd-tap" x1="200" y1="76" x2="200" y2="118"/><text class="pd-s" x="208" y="102">复制一份</text>
<rect class="pd-cen" x="145" y="118" width="110" height="34" rx="6"/><text class="pd-ct" x="200" y="135">审查设备</text>
<path class="pd-inj" d="M145 135 Q60 135 40 96" marker-end="url(#pd-ai)"/>
<text class="pd-s" x="2" y="174">抢在真正的响应之前，发回伪造的 DNS 响应或 RST</text>
<text class="pd-h" x="0" y="214">内联模式：流量必须先通过审查设备</text>
<rect class="pd-box" x="2" y="243" width="72" height="34" rx="6"/><text class="pd-t" x="38" y="260">用户</text>
<line class="pd-wire" x1="74" y1="260" x2="143" y2="260" marker-end="url(#pd-a)"/>
<rect class="pd-cen" x="145" y="243" width="90" height="34" rx="6"/><text class="pd-ct" x="190" y="260">审查设备</text>
<line class="pd-wire pd-cut" x1="235" y1="260" x2="284" y2="260"/>
<path class="pd-x" d="M252 251L268 269M268 251L252 269"/>
<rect class="pd-box" x="286" y="243" width="72" height="34" rx="6"/><text class="pd-t" x="322" y="260">网站</text>
<text class="pd-s" x="2" y="304">可以直接把数据包丢掉，也可以发出 RST</text>
<text class="pd-s" x="2" y="324">从外面无法分辨丢包来自哪一台设备</text>
</svg>
<figcaption>镜像模式的设备只取得流量的副本，无法拦下原本的数据包，只能抢先发出伪造的数据包。内联模式的设备串在线路上，可以直接丢包，但从外面无法分辨丢包来自哪一台设备，所以表格里哈萨克斯坦与巴基斯坦丢包设备的 TLS 标成「无法判断」。</figcaption>
</figure>

论文在 TLS 一节写到，路径上可能不只一台审查设备。TSG 放行的测试数据包仍可能被其他设备拦下，TSG 会拦的数据包则只要经过 TSG 就一定被拦。我们的推论是，无法从封锁行为判断来源时，实测的「被拦」可能来自路径上任何一台设备，无法单独证明 TSG 存在。相对地，TSG 应该拦下、实测却放行的结果，可以排除路径上有行为相同的 TSG 组件[^asym]。组件又是模块化的，同一个部署可能用同一版 SAPP、不同版的 SSL 插件，所以每一项比对只能说明一个组件。

Geedge 在外泄文件里以代号称呼各地的客户：哈萨克斯坦是 `K18` 与 `K24`、埃塞俄比亚是 `E21`、巴基斯坦是 `P19`、缅甸是 `M22`、新疆是 `J24`，另有一个身份不明的 `A24`[^codes]。下表整理五种协议的比对结果，地区附上外泄文件里对应的客户代号。这些代号对应文件记录的客户，不代表测量到的设备就属于该项目。防火长城的设备依过去研究的命名分列，QUIC 的比对没有区分防火长城的设备，另列一行[^matrix]。

<div class="match-wrap">
<table class="match" aria-label="TSG 与各地审查设备的比对结果">
<thead><tr><th scope="col">设备或地区</th><th scope="col">DNS</th><th scope="col">IP 分片</th><th scope="col">TCP RST</th><th scope="col">TLS</th><th scope="col">QUIC</th></tr></thead>
<tbody>
<tr class="grp"><th colspan="6" scope="rowgroup"><span>中国的防火长城</span></th></tr>
<tr><th scope="row">Injector 1<small>DNS 注入</small></th><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">Injector 2<small>DNS 注入</small></th><td class="m-yes">吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">Injector 3<small>DNS 注入</small></th><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">GFW I</th><td class="m-na"></td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-na"></td></tr>
<tr><th scope="row">GFW II</th><td class="m-na"></td><td class="m-part">部分</td><td class="m-yes">吻合</td><td class="m-old">旧版</td><td class="m-na"></td></tr>
<tr><th scope="row">GFW III</th><td class="m-na"></td><td class="m-unk">无法判断</td><td class="m-yes">吻合</td><td class="m-no">不吻合</td><td class="m-na"></td></tr>
<tr><th scope="row">防火长城<small>未区分设备</small></th><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-part">部分</td></tr>
<tr class="grp"><th colspan="6" scope="rowgroup"><span>其他地区</span></th></tr>
<tr><th scope="row">河南</th><td class="m-na"></td><td class="m-unk">无法判断</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-na"></td></tr>
<tr><th scope="row">哈萨克斯坦<small>K18、K24</small></th><td class="m-na"></td><td class="m-unk">无法判断</td><td class="m-na"></td><td class="m-unk">无法判断</td><td class="m-old">旧版</td></tr>
<tr><th scope="row">缅甸<small>M22</small></th><td class="m-na"></td><td class="m-no">不吻合</td><td class="m-unk">无法判断</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td></tr>
<tr><th scope="row">巴基斯坦<small>P19，发送 RST 的设备</small></th><td class="m-na"></td><td class="m-unk">无法判断</td><td class="m-no">不吻合</td><td class="m-no">不吻合</td><td class="m-na" rowspan="2">未下结论</td></tr>
<tr><th scope="row">巴基斯坦<small>P19，丢包的设备</small></th><td class="m-na"></td><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-unk">无法判断</td></tr>
<tr><th scope="row">伊朗</th><td class="m-no">不吻合</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
</tbody>
</table>
</div>

<ul class="match-key" aria-label="图例">
  <li><span class="sw m-yes"></span>吻合</li>
  <li><span class="sw m-old"></span>与 TSG 较旧的版本相同</li>
  <li><span class="sw m-part"></span>部分相符</li>
  <li><span class="sw m-unk"></span>无法判断</li>
  <li><span class="sw m-no"></span>不吻合</li>
  <li><span class="sw m-na"></span>没有测量，或论文没有下结论</li>
</ul>

<dl class="match-terms" aria-label="各列说明">
  <dt>DNS</dt><dd>审查设备抢先发回的伪造 DNS 响应，比对响应里的标志值、是否使用压缩指针，以及解析查询时处理压缩指针的上限</dd>
  <dt>IP 分片</dt><dd>一个 IP 数据包被切成多片发送时，审查设备是否先重组再检查、最多重组几片</dd>
  <dt>TCP RST</dt><dd>审查设备为了中断连接而伪造的 RST 数据包，比对头部字段的设置、一次发送几个，以及能否从字段反推出固定的种子值</dd>
  <dt>TLS</dt><dd>篡改 TLS 连接第一个数据包（ClientHello）里的各个长度字段，看审查设备是否仍然解析出域名并封锁</dd>
  <dt>QUIC</dt><dd>审查设备支持哪些 QUIC 版本，以及分片重组、最小数据包大小与长度字段的解析方式</dd>
</dl>

### 吻合的部分

中国的 Injector 2 是唯一同时符合 DNS 三项特征的注入器，包括伪造响应里的标志值、响应里使用压缩指针（DNS 数据包里重复引用域名的写法），以及解析查询时处理压缩指针的上限。作者认为这些结果强烈暗示（strongly suggest）TSG 提供了 Injector 2 的 DNS 注入实现[^dns-inj2]。

TSG 伪造 RST 数据包时，用一个自制的随机数生成器填入头部的几个字段。从 GFW II 与 GFW III 发出的数据包，可以反推出固定的种子值（随机数生成器的起始值），而且就是 TSG 的默认值。作者估计固定的种子值碰巧出现的概率约为 10 的负 44 次方，再加上数值与 TSG 的默认值相同，论文用 strongly indicating（强烈表示）形容两者用了 TSG 的代码[^seed]。

同一节也列出两者与 TSG 的偏差，GFW II 与 GFW III 发出的 RST 都使用固定的 TTL（数据包还能经过几个路由器的计数），TSG 的 TTL 则随内部状态变化。2023 年 12 月的测量里，GFW II 的 TTL 还与 TSG 一致，作者据此推测 GFW II 之后稍微改了实现。过去的研究记录到 GFW II 每次连发的几个 RST 完全相同，研究团队把 TSG 设成同样一次连发几个 RST 时，数据包之间的 IPID（IP 数据包的标识字段）会变动[^rst-dev]。

IP 分片重组有部分相符的项目，GFW II 一次重组的分片上限与 TSG 非常接近。作者在这一项的说法较保守，只写两者可能共用相近的代码（potentially share similar code）[^frag]。

TLS 的测试会篡改 ClientHello 里的各个长度字段，看设备是否仍然解析出域名并封锁。没有任何设备与外泄的最新版行为完全相同，GFW II 的行为等同 TSG 较旧版本的 SSL 模块，作者推测 GFW II 解析 TLS 时用的就是这个旧版。QUIC 的结果是防火长城与哈萨克斯坦拦下的测试数据包与 TSG 相同，但两地支持的 QUIC 版本与 TSG 不同，无法完全吻合。哈萨克斯坦的解析指纹则完全符合 TSG 较旧版本的 QUIC 解析代码[^tls-quic]。

论文第 6 节把这些结果总结成一句：*"Notably, we find high levels of correspondence with GFW DNS Injector 2 and TCP GFW II and GFW III, suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall."*

译成中文是「我们发现与 DNS Injector 2，以及 TCP 的 GFW II、GFW III 高度吻合，暗示外泄的 TSG 代码（或与它相近的衍生版本）确实部署在中国国家防火墙的一部分」，引导这句的 suggesting 是推论的语气，indeed（确实）是原文的强调。GFW II 的 TLS 与哈萨克斯坦的 QUIC 对上的是 TSG 较旧的版本，GFW II 与 GFW III 的 RST 也与 TSG 有偏差，geedge.report 的文章同样写到吻合的情况会随时间改变，部署中的代码已经与外泄的版本有差异[^summary]。

### 不吻合或无法判断的部分

Injector 1 与 Injector 3 不吻合，其中 Injector 3 在这次测量里的标志不同，也不再使用压缩指针，与 2020 年最初的观察不一样。GFW I、河南、缅甸，以及巴基斯坦发出 RST 的那一套设备，都无法反推出固定的种子值。IP 分片的比对里，有几台设备的重组行为与 TSG 的默认不同，论文注明重组与否可以在 TSG 的配置文件调整，所以本文归为无法判断[^nomatch]。

缅甸的 RST 行为可以用 TSG 的配置重现，支持的 QUIC 版本也与 TSG 完全相同。但解析指纹不符，论文因此写 cannot confirm its use（无法确认使用）。哈萨克斯坦与巴基斯坦的部分设备以丢包封锁，测试数据包是否绕过无法判定，两地的结果在论文里写成 support potential TSG deployments（与可能有 TSG 部署的推论相容）。哈萨克斯坦的审查设备不发 RST，所以没有做 RST 的比对。哈萨克斯坦虽然有 QUIC 解析与旧版完全相符的结果，论文仍然没有把它写成确认部署[^mm-kz-pk]。伊朗的 DNS 标志与 TSG 不同，埃塞俄比亚只出现在外泄文件里，没有测量。

Geedge 在这些国家有客户的证据来自文件。论文的背景一节引用民间调查，列出哈萨克斯坦、埃塞俄比亚、巴基斯坦与缅甸的部署，研究团队在 Jira 搜索 vpn 得到的记录也以缅甸与埃塞俄比亚的现场为主[^civil]。USENIX 论文的测量里，写成高度吻合（high levels of correspondence）的只有中国的部分设备[^summary]。

### 报道与论文的措辞差距

Risky Bulletin 的报道写 TSG 是防火长城「三种已知流量过滤能力之一」（one of the Great Firewall's three known traffic filtering capabilities）[^risky]，论文全文没有这种说法[^no-three]。「三种」可能来自过去研究对防火长城设备的分类。DNS 注入器分成三个，论文的结果是吻合一个。发出 RST 的注入器也分成 GFW I、II、III，吻合两个。同一篇报道引用的研究者帖子也写到 Geedge 只是参与防火长城的厂商之一[^risky]。geedge.report 首页的粗体标题写「China's Great Firewall is running parts of TSG」，语气比论文肯定，同一条的说明则改用 appears to be[^geedge-home]。

论文支持的说法是防火长城的一部分设备用了 TSG 或与它相近的版本，其他测量过的设备与 TSG 不吻合，由谁提供目前没有公开的证据。论文也没有写 Geedge 开发了防火长城，用的词是 ties、affiliated，以及与 MESA 实验室的 close collaborative relationship[^ties]。比起把 Geedge 等同于防火长城的说法，论文支持的范围窄很多，但同时有源代码里的默认值与远程测量两边的证据，过去只靠远程推测的研究无法做到。

## 规避工具的签名与封锁

TSG 对规避工具的签名会依客户的反馈反复调整，Psiphon 这类没有明显流量特征的工具，则改用服务器 IP 封锁。
{: .sec-lead }

USENIX 论文写到，外泄文件里有依客户需求反复封锁特定规避工具的记录，对象包括 Psiphon、Tor 与 ExpressVPN、NordVPN 等常见的 VPN，手法从封锁 IP 到比对字节模式都有。签名（描述某个 App 流量特征的规则）结合了服务器 IP、域名、TLS 指纹、证书字段、数据包长度与字节模式。论文分析的一份 Confluence 文档记录了 2024 年 3 月到 11 月间一个签名包的多次更新，里面的签名风险等级在 3 到 5 之间，多数是 5，另一份以中国 App 为主的测试记录则全部是 1[^circ]。具体的签名条件写在论文的表格里，本文不转述。

| 工具 | 外泄数据与研究里的处理方式 |
|---|---|
| 商业 VPN（ExpressVPN、NordVPN 等） | 签名结合服务器 IP、域名、TLS 指纹、证书字段与字节模式，依客户的反馈反复调整[^circ]。外泄文件里也有 NordVPN 的完整服务器清单[^foci-vpn] |
| Psiphon | 依内部文件，没有明显的流量特征，所以改用服务器 IP 封锁，再加上白名单避免误封[^psiphon]。外泄文件里有 Psiphon 的 CDN 域名[^foci-vpn] |
| OpenVPN | 检测的代码看来取自开源的 nDPI[^thirdparty] |
| Tor | 列在签名的风险等级表里，USENIX 论文没有描述签名的内容，也没有测试 Tor 的连接[^tor] |
| WebTunnel | Tor 的一种可插拔传输，把流量伪装成普通的 HTTPS 网页连接。外泄时 Geedge 看来还没有有效的封锁手段，MESA 实验室的学生做过封锁方法的初步研究[^webtunnel] |
| Signal | 一条工单记录 Signal 开启反审查选项之后，封锁就失效了[^circ] |

研究团队在 Jira 里搜索 vpn，找到 182 个议题下的 700 条记录，内容包括上报提取出的服务器 IP、排定封锁的优先级、签名失效之后反复修改，以及误封其他服务。作者的归纳是，规避工具的签名由客户参与调整，客户可以上报失效、排定优先级、标出误封的情况[^circ]。

在 Psiphon 的记录里，检测的成本因为混淆（让流量看起来不像任何已知协议的技术）而提高。一份分析封锁 Psiphon 附带损害的内部文件写到，Psiphon 的流量没有明显的特征，所以改用服务器 IP 识别，再加上一套白名单保护机制避免误判。一条工单也讨论了用 IP 与 SNI 封锁时误封的风险。作者在结论里也写到相反的一面，TSG 能以相对低的成本识别规避工具，常常在连接一开始就比对出来[^psiphon]。

论文里与 TSG 封锁 Tor 有关的内容，只有引言的对象清单与签名的风险等级表，表里有一项 Tor Browser[^tor]。论文没有描述 Tor Browser 签名的内容，也没有测试 Tor 的连接，所以无法从论文得知 TSG 如何识别 Tor，更无法推论它能封锁 Tor。InterSecLab 的〈The Internet Coup〉以文件为依据，报告里写到在外泄的时间点，Geedge 似乎还没有有效对付 WebTunnel 的手段，MESA 实验室的学生做过封锁方法的初步研究。InterSecLab 也写明没有找到 Geedge 发现或利用 Tor 未知漏洞的证据，并与 Tor Project 协调了披露的方式[^webtunnel]。

FOCI 论文从域名的角度提供了另一组数据。外泄文件里有多个文件专门针对 VPN 与规避工具，包括 NordVPN 的完整服务器清单与 Psiphon 的 CDN 域名[^foci-vpn]。对规避工具的开发者来说，服务器的 IP 与域名本身就是收集与封锁的对象，流量特征只是其中一种手段。

论文的结论写 TSG 的复杂性与灵活性是双刃剑，增加了规避的难度，也损害了代码的可维护性与正确性。核心组件 SAPP 与协议插件以缺乏内存安全保障的 C 编写，系统仍然依赖 Stellar-on-SAPP 这类过渡方案，代码也从多个第三方复制而来。工单里有一条升级 AppSketch 数据库之后 SAPP 重新启动的记录，作者形容这是拼凑式（patchwork）的开发过程，也写到适合后续用模糊测试（fuzzing，大量输入异常数据、找出程序错误的方法）与符号执行（以符号代替实际输入、推算程序各条执行路径的分析方法）深入研究。论文没有提出任何 CVE 编号或可以利用的具体漏洞[^no-cve]。

## 域名清单的覆盖范围

外泄文件里实测被封锁的域名，九成以上不在研究者常用的两份清单里，只用常用清单测量，只能看到审查范围的一部分。
{: .sec-lead }

审查测量要先决定测哪些域名，常用的清单有两份。Tranco 是按流量排名的热门网站清单，Citizen Lab 的检测清单由研究者与社区人工维护，按内容类型整理可能被封锁的网站。FOCI 论文从外泄文件提取了 14,365,453 个候选域名，解析过滤之后剩下 6,915,266 个。广州与南京的测量点测 DNS 注入，可靠性较高。巴基斯坦、缅甸与阿尔及利亚的测量点测 TLS 握手是否因 SNI 被中断，可靠性较低。每个域名测 25 次，把间歇性的封锁也纳入。哈萨克斯坦与埃塞俄比亚虽然是已知的客户，研究团队无法取得合适的测量点[^foci-meas]。

结果是外泄文件里实测被封锁的域名中，298,955 个（93.7%）同时不在 Tranco 与 Citizen Lab 的清单里。相对地，外泄文件只覆盖被封锁的 Tranco 域名的 37.1% 到 61.6%。三份清单各有分工。依 FOCI 的说法，Tranco 用来看哪些全球热门网站被封锁，Citizen Lab 的清单用来长期跟踪各类敏感内容，外泄文件则反映商用审查厂商认为值得关注的域名[^foci-937]。

FOCI 写明不把出现在外泄文件里的域名当成被封锁的域名。明确的封锁清单属于客户的敏感数据，在外泄文件里很少见，域名多半出自内部讨论客户环境的文件，代表 Geedge 或客户「感兴趣」（of interest）的内容。数量最多的来源是 MESA 实验室的 SNI 数据集，作者判断看来是从网络分流器（network tap，在线路上复制流量的设备）收集的。外泄文件里也有 Alexa 与 SecRank 等排名清单的副本，供 MESA 的研究使用[^of-interest]。所以 93.7% 反映的是常用清单的缺口，哪些域名真的被封锁仍要靠测量确认，与 USENIX 论文先读代码、再回到网络比对的做法相同。

社区维护的 Citizen Lab 检测清单台湾部分（`anoni-net/citizenlab-test-lists` 的 `tw.csv`）同样是人工整理的清单，反映的是维护者认为重要的内容。从 FOCI 的结果来看，用清单测量没有测到封锁时，结论只涵盖清单里的网站，清单以外的域名本来就不在观测范围内。单次测量如何判读见[OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)，各网络有多少测量见[OONI 观测覆盖率](/projects/asn-coverage/)。

## 供应链与政策

InterSecLab 从外泄文件追查到 Geedge 有一部分硬件来自台湾的凌华科技，但在我们比对的美国与欧盟制裁名单里，至今没有 Geedge。
{: .sec-lead }

InterSecLab 在〈MADLink〉里从外泄文件追查硬件供应链。台湾的凌华科技在 2019 到 2020 年初经由凌华的北京分公司，向 Geedge 出货 1,708 台 CSA-7400（厂商营销定位用于防火墙与 DPI 的高密度网络平台），依报告是第一代 TSG 平台的硬件基础，外泄文件里这套配置只部署在哈萨克斯坦。Geedge 自制的 EtherFabric（在多个 TSG 节点之间分配流量的网络数据包代理设备）部署在缅甸。外泄文件里它的管理接口 MAC 地址的厂商前缀登记在凌华名下，InterSecLab 据此判断里面有凌华的组件，最可能是管理用的计算主板[^madlink-hw]。

外泄文件里，Geedge 的 TSG 用过三代硬件，另有一项自制的 EtherFabric[^madlink-gen]：

| 产品 | 硬件 | 供应商 | 部署地点 |
|---|---|---|---|
| 第一代 TSG-ADC | CSA-7400 高密度网络平台 | 凌华科技（台湾） | 哈萨克斯坦 |
| 第二代 TSG-9140 | ATCA 规格的电信设备，看来以 VELA ATCA 平台为基础 | 北京恒光信息技术 | 埃塞俄比亚（`E21`） |
| 现行 TSG-X | 通用的 x86 计算服务器与存储服务器 | Nettrix（中科曙光的子公司）、浪潮 | 埃塞俄比亚（`E21`）、巴基斯坦（`P19`）、缅甸（`M22`） |
| EtherFabric | 看来沿用 TSG-9140 的 VELA ATCA 硬件，部分网络组件可能来自凌华 | 北京恒光信息技术、凌华科技 | 缅甸（`M22`），`A24` 的概念验证 |

凌华科技向 InterSecLab 证实了出货的数量，表示出货前做了出口管制名单筛查、Geedge 不在受限名单上，并将启动内部审计。凌华也表示公司只提供通用的硬件平台，没有参与和最终用途相关的软件集成或系统设计。InterSecLab 的反驳是，外泄文件里有 TSG-ADC 的负载均衡依赖凌华 PacketManager 软件的记录，CSA-7400 的营销定位也是 DPI 与防火墙设备[^adlink]。经济部说明台湾的出口管制框架参照国际防扩散机制与制裁清单，以法律限制为由不评论个案。

报告的论点是，Geedge 现行的服务器多是通用的 x86 硬件，正规采购受阻时仍可能从次级市场取得，CSA-7400 这类专为 DPI 与防火墙设计的设备才是出口管制能实际着力的地方[^adlink]。社区翻译了[报告全文](https://anoni.net/docs/reports/interseclab-madlink/)，也记录了[台湾公共领域对 MADLink 报告的反应](/updates/2026/05/madlink-editorial-2026-05/)。

MADLink 的依据是文件与厂商的回复，可以对照 USENIX 论文在哈萨克斯坦的三项测量：QUIC 解析符合旧版、TLS 因为丢包无法判定、RST 无法比对。两者之间有时间差，CSA-7400 是 2019 到 2020 年初出货的第一代硬件，与论文的测量相隔数年。测量到的设备是否仍是那一批硬件，目前无法判断[^gap]。

MADLink 也提到，Geedge 现行硬件里的服务器来自 Nettrix，它的母公司中科曙光已经遭到美国制裁[^adlink]。Justice For Myanmar 在 2024 年 6 月 19 日的新闻稿呼吁各国政府制裁 Geedge Networks 等公司[^jfm]。截至 2026 年 10 月 30 日，我们比对美国财政部 OFAC 与欧盟的制裁名单、美国联邦公报的实体清单公告，都没有查到 Geedge 被列入[^sanction]。

## 研究伦理与数据处理

两篇论文都不公开外泄的原始数据，USENIX 论文也不公开构建 TSG 的完整做法，外界能重现的主要是远程测量。
{: .sec-lead }

USENIX 论文的伦理考量一节列出五类利益相关方，包括 Geedge 的员工与股东、代码被集成进 TSG 的第三方公司、部署 TSG 的国家、在这些国家受审查的用户，以及反审查社区。外泄的 Git 仓库里有开发者的姓名与 email，论文的处理方式是聚焦在系统与架构，不报道个人，公开的仓库里也不放外泄的原始数据[^local]。

在本机运行一份 TSG 本身也有风险，可能让部署国改进系统，或让其他审查者更容易部署。论文因此选择不公开架设这套防火墙的方式，公开的数据只放对识别部署有用的内容。研究团队也考虑过完全不在本机运行。他们的结论是，有了一份可运行的副本，反审查社区才能识别各地的部署，对着真实的系统开发与测试规避策略，再把策略推广到其他国家的防火墙[^local]。

测量只在研究团队自己拥有的两台主机之间进行，不以任何第三方服务器为目标，租用测量点时也确认对方不在欧盟的制裁名单上。外泄的源代码与研究团队的构建都不公开，作者承诺依请求把构建分享给可信任的网络安全研究者，公开在 Zenodo 的是测量结果、匿名化的数据包记录与测量用的脚本。结果是其他研究者可以用公开的脚本重现远程测量，源代码端的对照则只有取得分享的研究者能重现[^share]。

FOCI 论文的立场是，外泄数据已经由 Enlace Hacktivista 与 DDoSecrets 公开，广泛的公共利益优先于可能的知识产权疑虑。GFW Report 的分析文章则建议只在隔离、不联网的（虚拟）机器上分析这些文件[^foci-ethics]。

Lantern 的 geedge.lantern.io 是从外泄数据提取发现的索引，处理方式又不一样。页面上写它是 corpus.lantern.io 的姊妹项目，目的是让规避工具的开发者清楚知道自己面对什么，但没有写明背后的团队，与 Lantern 规避工具的关系也无法从页面确认[^lantern-site]。索引不转载外泄的原始内容，每一条发现都附上出处的信息。

索引里的发现由 LLM 自动提取，页面写明提取工作由 Sonnet 等级的智能体（agent）读取批量文本完成，我们读取时首页列出 880 条发现。我们抽查了五条，都标成最高的置信等级。其中三条只凭数据表的字段名称就推论系统会记录每一条连接，出处多是测试用的配置文件，也没有 commit hash[^lantern]。Lantern 的索引可以当成找线索的起点，引用前要自行回到原始数据核对，不能直接当成证据。

在 net4people 的讨论帖里，2025 年 10 月之后有出处的后续研究只有 FOCI 论文，其他多是留言者的比对与推测[^n4p]，部分留言附上外泄内部系统的镜像链接，本文不引用。

本文也守同样的界线，不转载外泄文件的内容、域名清单与文件路径，不写可以用来规避检测或改进封锁的参数、特征值与签名条件（论文本身公开了一部分，想深入的读者请读原文），也不提外泄数据里的人员。

## 还没有答案的问题

A24 的身份、防火长城其他设备的来源，以及各客户国家的部署能否用测量确认，都还没有公开的答案。
{: .sec-lead }

Injector 1、Injector 3 与 GFW I 都与 TSG 不吻合，论文的结果只指向防火长城的一部分设备用了 TSG 或相近的代码，其余设备由谁开发，目前没有公开的证据。

InterSecLab 在 2025 年 9 月写到，`A24` 的相关数据没有能识别客户的地点或 ISP，唯一的线索是首字母 A 与年份 2024，而代号的数字也不一定代表年份。外泄时双方的关系还在初期，Geedge 为它做过镜像与内联两种模式的概念验证。2026 年 4 月的〈MADLink〉里仍称它为只以代号识别的未知客户，并补充 Geedge 的 EtherFabric 也曾在 `A24` 做概念验证。两篇论文、GFW Report 与 net4people 的讨论帖里，也都没有出现新的线索[^a24]。

哈萨克斯坦、巴基斯坦、缅甸与埃塞俄比亚的客户关系都有文件证据，测量却停在可能或无法确认。FOCI 的研究团队无法取得哈萨克斯坦与埃塞俄比亚的测量点，USENIX 论文在哈萨克斯坦有测量点但部分项目无法判定，埃塞俄比亚两篇论文都没有测量。部署端也一直在改版，外泄文件停在 2024 年 11 月，GFW II 的 TTL 从 2023 年 12 月到论文测量时已经改变[^rst-dev]，之后的测量要把版本的差异纳入考虑。

研究团队的构建只加载了 DNS、SSL 与 QUIC 三个 SAPP 协议插件，AppSketch 数据库的存档都经过加密。签名格式如何转换成 Maat 的规则，作者没有找到对应的代码，只从格式的相似度推论，论文也没有涵盖源代码的其余部分。作者的期待是让这篇论文成为后续研究的指引。FOCI 列出的后续工作包括搜索外泄文件里的 IP 地址、分析 PDF 等文件、改进文字识别（OCR），以及比对 Common Crawl 与 ICANN 的域名数据[^future]。

规避工具这一端，我们在 net4people 跟踪外泄的讨论帖（2025 年 10 月以后的留言）里，没有看到 Tor、Psiphon 或 VPN 厂商公开说明为应对外泄做了哪些调整[^n4p]。Tor Project 也审阅过〈The Internet Coup〉的 Tor 一节，Psiphon 团队审阅了 Psiphon 一节[^coup-ack]。有了外泄的源代码，研究界已经能对照真实的审查设备，下一步要看测量点是否能扩展到更多客户国家，以及工具开发者如何运用这些结果。欢迎到社区的 [Matrix](/contact/) 一起讨论。

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

[^blackbox]: USENIX 论文 §1：「Traditionally, the study of DPI-based censorship systems has relied almost exclusively on black-box analysis」、「This is the first time that the source code of a commercial DPI has been leaked」。
[^summary]: USENIX 论文 §6：「Notably, we find high levels of correspondence with GFW DNS Injector 2 [9] and TCP GFW II and GFW III [47], suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall」。§6.4：「While no middlebox exhibited exactly the same behavior as the latest leaked TSG」。geedge.report〈Geedge firewall source code analysis〉：「The match is not frozen in time」、「the deployed code has drifted from the leaked version」。
[^nomatch]: USENIX 论文 Table 5 的说明：「Injector 3 has different flags and no longer uses compression pointers, different from the initial observation」。Injector 1 不吻合的依据是 §6.1 的同一句，只有 Injector 2 同时具备三项特征。§6.3：「In contrast, the other injectors exhibit markedly different behaviors and header values」、「While we did not observe the seed key correspondence in other regions」，前一句涵盖 GFW I，后一句涵盖其他地区。Table 7 的说明：「"no" also includes cases where TCP window values remain identical all the time rendering k undefined」。§6.2：「This is configurable」，指 TSG 配置文件里的重组选项。哪些设备的重组行为不同写在论文的 Table 6，本文不转述。
[^mm-kz-pk]: USENIX 论文 §6.3：「TSG can be configured to match the behavior in Myanmar」、「We did not test in Kazakhstan because its censors do not generate TCP RST packets」。§6.5：「We also find the supported QUIC versions in Myanmar align exactly with those supported by TSG's QUIC, though the parsing fingerprint mismatch means we cannot confirm its use」。§6.4：「both Kazakhstan and Pakistan (DROP) support potential TSG deployments, as their generic censorship mechanism of packet drops makes bypass failures inconclusive」。正文写论文没有把哈萨克斯坦写成确认部署，这是本文的查证，在论文全文搜索 confirm（不分大小写）共 4 处，分别在 §2.1、Figure 2 的工单、§6.3 与 §6.5，没有一处确认哈萨克斯坦的部署，§6 提到 Kazakhstan 的句子也没有这样的说法。伊朗的部分见 Table 5，伊朗那一行的标志、压缩指针与上限三项都与 TSG 不同。埃塞俄比亚不在 Table 10 列出的测量点里，Table 10 只有河南、北京、阿拉木图、仰光、卡拉奇与伊斯兰堡。
[^gfwr-geedge]: GFW Report〈Geedge & MESA Leak〉：「This leak originates from an important branch of the GFW's R&D capacity」、「Geedge (Hainan) Information Technology Co., Ltd. (Geedge Networks Ltd.) was founded in the same year. Fang served as chief scientist」。同一段的 same year 指 2018 年。FOCI 论文 §2.1：「572 GiB of internal documents from Geedge Networks and the related MESA lab including source code repositories, project management records, client deployment configurations, and operational data」。八成以上是本文依 USENIX 论文 Table 1 的计算，RPM 软件包仓库的存档占 463.0 GiB，约为总量的 81%。
[^map]: 网络政变社区译文第 6 章〈Geedge 的營運與客戶〉：「目前辨識出的客戶代號有哈薩克（`K18` 與 `K24`）、巴基斯坦（`P19`）、衣索比亞（`E21`）、緬甸（`M22`）與新疆（`J24`）」。第 2 章〈主要發現〉：「InterSecLab 已經確認新疆、福建與江蘇的省級防火牆專案」。原报告第 6 章另有一张 Geedge 运营地区的地图（图 14）。本文的地图依这些文字重画，圆点位置标在各省省会附近，只表示省份，不代表实际的部署地点。国界数据来自 Natural Earth 1:50m（公有领域）。
[^gfwr-src]: GFW Report〈Geedge & MESA Leak〉：「The source-code portion of the leaked files has not yet been carefully analyzed」。
[^early]: USENIX 论文 §1：「Several news organizations and journalists who were granted early access have worked together for the past year to analyze the documents from a non-technical perspective」、「The current reporting is mostly geared to non-technical audiences」、「leaving the source code itself largely unexplored」。
[^coup-ack]: 网络政变社区译文第 8 章〈結論、反思與下一步〉的致谢：「與國際特赦組織、Justice For Myanmar、Paper Trail Media、《環球郵報》（The Globe and Mail）、Tor Project、奧地利《標準報》（DER STANDARD）與 Follow The Money 等夥伴共同合作」。同一段也写到「也感謝 Tor Project 團隊審閱 Tor 一節，以及 Psiphon 團隊提供寶貴資訊並審閱 Psiphon 一節」。
[^build]: USENIX 论文 §1：「we successfully build and run TSG's latest tagged release version」。§5.2：「We were able to successfully test the DNS, HTTP, TLS, and QUIC protocols and trigger injection responses, packet drops, and deferred blocking actions」。
[^method]: USENIX 论文 §5.2：「We developed a testbed to evaluate TSG's blocking behaviors in a controlled environment」。Ethical Considerations：「We performed all of our scans between two vantage points that we own, not including any other third-party server as the target of our scan」。从源代码找出指纹再测量的做法见 §1：「we extract several fingerprints from TSG, including custom random number generators and parsing idiosyncrasies」。
[^foci-meas]: FOCI 论文 §3.2：「we produce a list of 14,365,453 potential domains」、「we produce a final list of 6,915,266 domains」。§3.4：「we perform measurements across vantage points in China (Guangzhou and Nanjing), Myanmar, Pakistan, and Algeria」、「While Kazakhstan and Ethiopia are known customers of Geedge Networks [12], we were unable to obtain access to appropriate vantage points in these countries」、「DNS censorship is highly reliable」、「which are inherently less reliable indicators」、「we perform 25 tests per domain to ensure intermittently blocked domains are included」。
[^madlink-hw]: MADLink 社区译文第 1 章〈摘要與主要發現〉：「這批設備構成 Geedge 第一代防火牆平台的基礎」。第 2 章〈Geedge 供應鏈深入解析（三代 TSG 硬體）〉：「外洩文件顯示這套配置只部署在哈薩克」、「2019 至 2020 年初之間出貨給 Geedge 的 CSA-7400 共有 1,708 台」。第 3 章〈EtherFabric 與 ADLINK 的角色和回應〉：「EtherFabric 部署在緬甸」、「登記在 ADLINK Technology, Inc. 名下」、「至少包含一個凌華科技的元件，最有可能是運行管理軟體的運算主板」、「凌華科技證實，凌華科技（中國）有限公司北京分公司向 Geedge Networks 供應了標準的 CSA-7400 網路安全平台」。
[^modular]: USENIX 论文 §3.2 与 §3.5 的 Takeaway：「fingerprinting one plugin does not necessarily imply the presence or version of another in the same deployment」、「The firewall aggregates attributes from multiple parallel processing paths」。
[^thirdparty]: USENIX 论文 §1：「including two of the three core application detection systems」。§4.2.1：「a free software project from the Libtrace team at the University of Waikato」、「All code required for this function contains the libprotoident copyright」、「appears to be a modified copy of openvpn.c from a 2022 version of nDPI」、「the logic remains nearly identical」。§4.2.2：「QDPI is built off of Qosmos ixEngine, a proprietary, enterprise DPI library」、「This is most clearly indicated by the Stellar session callback subscriber function eventually calling」，后面接的是 ixEngine 的函数名称。
[^disclose]: USENIX 论文 §4.2：「we find instances of third-party libraries intentionally copied and adapted into the Geedge Networks code base」。Ethical Considerations：「We disclosed the usage of code by Geedge Networks to both the Libprotoident team and Enea, the parent company of Qosmos. Both have responded to our initial disclosures, and we have scheduled meetings to engage in further discussion」。§4.2 的 Takeaway：「suggests that comprehensive protocol classification is costly to build from scratch, even for a well-resourced, state-linked vendor」。
[^beyond]: 本文的观点。依据是 USENIX 论文 §1：「For the first time, we can move beyond remote inference」。
[^gfw-multi]: USENIX 论文 §2.1：「there has been increasing evidence pointing to the deployment of multiple, independently operating deep packet inspection (DPI) devices with distinct enforcement roles」。
[^modes]: 网络政变社区译文第 6 章〈Geedge 的營運與客戶〉：「在鏡像模式下，客戶無法擋下特定流量，只能靠注入封包（送出偽造的封包）來阻斷連線」、「內聯模式在文件中也稱為『主動』（active）模式，流量必須先通過 Geedge 設備，才能繼續前往目的地」、「內聯模式的優點是可以完全擋下特定的流量，讓它根本無法通過網路」。USENIX 论文 §5.2：「It also supports both in- and on-path deployment」。§3.1：「Both require TSG to be deployed in-path to stop packets」。§6.4：「their generic censorship mechanism of packet drops makes bypass failures inconclusive」。
[^asym]: 本文的推论。依据是 USENIX 论文 §6.4：「Note, we can highlight comparisons with test vectors that are successfully blocked by TSG in cases of non-fingerprintable censorship decisions」、「if a test vector evades TSG, it could still get blocked by another middlebox, but if it is blocked by TSG, it is guaranteed to be blocked」。论文用这个逻辑挑选 TLS 的比较项目，本文延伸到其他协议，并推出放行的结果可以排除 TSG。
[^codes]: 网络政变社区译文第 6 章〈Geedge 的營運與客戶〉：「目前辨識出的客戶代號有哈薩克（`K18` 與 `K24`）、巴基斯坦（`P19`）、衣索比亞（`E21`）、緬甸（`M22`）與新疆（`J24`）」、「資料裡還提到一個身分不明的客戶，代號 `A24`」、「代號的最後兩位數字可能代表 Geedge Networks 在當地開始專案的年份，但並非每個代號都符合」。
[^matrix]: 本文依 USENIX 论文 Table 5 到 Table 9 与 §6.1 到 §6.5 的正文整理，分类是本文的判断。吻合：§6.1 的 Injector 2，§6.3 的 GFW II 与 GFW III（固定的种子值等于 TSG 的默认值）。旧版：§6.4「GFW II shows behavior equivalent to an older version of TSG's SSL module」，§6.5「the parsing fingerprint exhibited in Kazakhstan fully matches an older version of TSG's QUIC parsing code」。部分：§6.2 的 GFW II（「The observed boundary of […] fragments for GFW II is very close to TSG's」，本文归为部分相符，因为上限只是接近），§6.5「both Kazakhstan and the GFW block the same test vectors as TSG's QUIC plugin, though we cannot match them fully due to a difference in supported QUIC versions」。无法判断：§6.2 重组行为与 TSG 默认不同的设备（论文注明这是 TSG 可以调整的设置），§6.4「both Kazakhstan and Pakistan (DROP) support potential TSG deployments」，§6.3「TSG can be configured to match the behavior in Myanmar」。不吻合：§6.1 Table 5 的其他注入器与伊朗，§6.2 重组到测试上限仍成功的设备，§6.3「the other injectors exhibit markedly different behaviors and header values」，§6.4「no middlebox exhibited exactly the same behavior as the latest leaked TSG」之下，除了 GFW II 与两台以丢包封锁的设备以外的设备，§6.5「the parsing fingerprint mismatch means we cannot confirm its use」（缅甸）。巴基斯坦列在 Table 9，正文没有讨论它的 QUIC 结果。哈萨克斯坦的设备不发送 RST，论文没有做 TCP 的比对。河南与巴基斯坦发出 RST 的设备，TLS 在 Table 12 的差异都是 TSG 放行、设备拦下，这两套设备以 RST 封锁，可以从 RST 辨认封锁的来源，所以本文归为不吻合，论文正文没有对这两格下结论。
[^dns-inj2]: USENIX 论文 §6.1：「Our results in Table 5 strongly suggest that TSG provides the GFW Injector 2's DNS injection implementation」、「only China's Injector 2 exhibits the combination of the flag value」。标志的数值本文省略。
[^seed]: USENIX 论文 §6.3：「corresponding to TSG's default seed_key, strongly indicating usage of TSG code」、「of exhibiting a constant seed key by random chance is approximately」，这句写的概率估计值是 10 的负 44 次方。种子值本身本文省略。
[^rst-dev]: USENIX 论文 §6.3：「both GFW II and GFW III exhibit deviations from TSG」、「Both fix TTL values at […], but TSG generates TTL values dependent on an internal state variable」、「GFW II did exhibit TTL values consistent with TSG, suggesting that it slightly changed its implementation since then」、「GFW II is known to send […] identical RST+ACK packets [47], while our build of TSG, when configured to also send […] RST+ACK packets per injection, decreases the IPID」。[…] 是本文省略的数值。
[^frag]: USENIX 论文 §6.2：「The observed boundary of […] fragments for GFW II is very close to TSG's, suggesting the two potentially share similar code」。[…] 是本文省略的分片上限。
[^tls-quic]: USENIX 论文 §6.4：「While no middlebox exhibited exactly the same behavior as the latest leaked TSG, GFW II shows behavior equivalent to an older version of TSG's SSL module, which suggests usage of this older version in GFW II's SSL parsing」。§6.5：「both Kazakhstan and the GFW block the same test vectors as TSG's QUIC plugin, though we cannot match them fully due to a difference in supported QUIC versions」、「the parsing fingerprint exhibited in Kazakhstan fully matches an older version of TSG's QUIC parsing code」。
[^civil]: USENIX 论文 §2.2：「Civil society investigations have highlighted evidence of deployments of Geedge Networks' products across multiple countries, including Kazakhstan」、「Ethiopia」、「Pakistan」、「and Myanmar」，各国之后的站点代号本文省略。§4.1.2：「we conducted a case-insensitive search for "vpn"」、「We found major threads of site correspondence with Myanmar (440 tickets) and Ethiopia (53 tickets)」。
[^risky]: Risky Bulletin，2026-08-21：「as one of the Great Firewall's three known traffic filtering capabilities」。同一篇报道引用的研究者帖子：「Geedge is only one of the vendors involved in the GFW」、「the authors found only 1 out of the 3 of the characterized DNS injectors that comprise the GFW matched」。
[^no-three]: 本文的查证。在 USENIX 论文全文（含附录与参考文献）搜索 three known 与 filtering capabilit，都是 0 处。filtering 只出现 1 次，在一篇参考文献的标题里。三种可能出自过去研究的分类，这是本文的推论，依据是 §2.1：「DNS manipulation is managed by three independent on-path injectors」、§6.3：「We evaluated three TCP RST injectors」，以及 Risky Bulletin 所引研究者帖子的「1 out of the 3 of the characterized DNS injectors」。
[^geedge-home]: geedge.report 首页：「China's Great Firewall is running parts of TSG」。同一条的说明：「The same code, or a close relative, appears to be part of China's national censorship system」。
[^ties]: USENIX 论文 Abstract：「a Chinese DPI company with ties to the Great Firewall of China」。§1：「affiliated with the Great Firewall of China」。§2.2：「maintains a close collaborative relationship with the Massive and Effective Stream Analysis (MESA) Lab」。
[^circ]: USENIX 论文 §1：「we identify client-driven, iterative efforts to block specific circumvention tools, including Psiphon, Tor, and many popular VPN providers」、「ranging from IP-based blocking to matching byte patterns」。§4.1.1：「including server IP addresses, domain names, JA3/JA4 hashes, SSL certificate fields (e.g., issuer name), payload length, and byte patterns」、「records a log of updates to a signature ZIP from March through November 2024」、「carry risk levels between three and five」、「the majority (21/29) are ranked five」、「which target predominantly Chinese applications and all have a risk score of one」。§4.1.2：「finding 700 tickets across 182 issues」、「ineffective blocking of Signal when the "censorship circumvention" option is enabled」、「customers can report failures, set priorities, and flag collateral damage」。
[^foci-vpn]: FOCI 论文 §4.2：「Multiple files specifically target VPN and circumvention tools, including comprehensive NordVPN server lists and Psiphon CDN domains」。
[^psiphon]: USENIX 论文 §4.1.2：「based on server IP addresses due to the lack of obvious signatures and integration of a "whitelist protection mechanism" to avoid misidentification」。Figure 3 的说明：「concerns of collateral damage from blocking Psiphon by IP addresses and SNI」。§7：「we also find evidence of obfuscation raising the cost of detection」、「TSG is capable of identifying circumvention tools at a relatively low cost」、「often very early in the connection」。
[^tor]: 本文的查证。在 USENIX 论文全文搜索完整单词 Tor（区分大小写），共 5 处：§1 引言的封锁对象清单、§2.1 回顾过去对防火长城封锁 Tor 的研究、Table 3 风险等级表的 Tor Browser，以及两篇参考文献的标题。第 6 节的测量没有出现 Tor。
[^webtunnel]: 网络政变社区译文第 7 章〈封鎖網路隱私與規避工具〉：「在資料外洩的時間點，Geedge Networks 似乎還沒有任何有效對付 WebTunnel 的手段」、「中國科學院 Mesalab 實驗室（Massive and Effective Stream Analysis）的學生做過初步研究，探討封鎖 WebTunnel 的可能方法」、「我們已與 Tor Project 協調，以負責任揭露」、「目前沒有找到任何證據，顯示 Geedge Networks 發現或正在利用 Tor 軟體或 Tor 設計上任何先前未知的漏洞」。
[^no-cve]: 本文的查证。在 USENIX 论文全文搜索 CVE、vulnerab、exploit（不分大小写），都是 0 处。memory-unsafe 与 fuzzing 各 1 处，都在 §7 结论。§7：「while they pose a significant obstacle to circumvention, they also undermine code maintainability and correctness」、「core components such as SAPP and its protocol plugins are written in memory-unsafe C」、「The Jira tickets corroborate this patchwork development process; we detail an example of an upgrade to the AppSketch database causing SAPP to restart」、「these reinforce the potential for future work in fuzzing or symbolic execution」。
[^foci-937]: FOCI 论文 Abstract：「298,955 censored GNL domains (93.7% of all censored GNL domains) are not included in either Tranco or the CitizenLab lists」。§5：「the GNL captures between 37.1% and 61.6% of censored Tranco domains」、「Tranco informs which globally popular sites are censored, CitizenLab monitors types of sensitive content over time, and the GNL reveals which domains commercial vendors consider of interest」。GNL 是 FOCI 对外泄数据的简称。
[^of-interest]: FOCI 论文 §4.1：「we do not assume domains are censored simply because they appear in the GNL」、「explicit blocklists are rare in the leak, as they constitute sensitive customer data」、「domains in the GNL represent content "of interest"」。§4.2：「The largest number of domains comes from MESA lab's specialized SNI datasets」、「appear to be gathered from network taps」，数据集的文件名本文省略。§5：「The GNL contains copies of popularity lists (Alexa, SecRank) that appear to be used for MESA lab research projects rather than deployed Geedge products」。
[^madlink-gen]: MADLink 社区译文第 2 章：「Geedge 為其 TSG 防火牆設備陸續供應了三代伺服器硬體」、「第一代 TSG 平台 TSG-ADC 建立在 CSA-7400 之上」、「第二代平台 TSG-9140 採用 AdvancedTCA（ATCA）規格」、「它應該是基於中國公司北京恒光信息技術的 VELA ATCA 平台」、「外洩文件顯示 TSG-9140 只部署在衣索比亞（代號 E21）客戶站點」、「現行版本 TSG-X 的主要 TSG 運算節點採用 Nettrix 伺服器，儲存 Cyber Narrator 所使用監控資料的儲存伺服器則來自浪潮（Inspur）」。第 1 章：「Geedge 目前這一代的 TSG 硬體部署在衣索比亞、巴基斯坦和緬甸」。第 3 章：「EtherFabric 看起來重用了與 TSG-9140 相同的、來自北京恒光信息技術的 VELA ATCA 硬體，但角色不同」、「部分網路元件可能由凌華科技提供」、「也作為概念驗證部署給一個只以代號 A24 識別的未知客戶」。
[^adlink]: MADLink 社区译文第 3 章：「已完成出口管制名單篩查，確認 Geedge 不在任何受限名單上」、「該公司也表示將啟動內部稽核」、「凌華科技表示，公司僅提供通用硬體平台，未參與任何與該產品最終用途相關的軟體整合、系統設計或運營活動。然而，這項說法與外洩文件互相矛盾」、「Geedge 的 TSG-ADC 配置在負載平衡功能上仰賴凌華科技的 PacketManager 軟體」。凌华把 CSA-7400 描述为通用平台的部分，报告的回应是「但該說法與產品本身的行銷定位互相矛盾」。第 1 章：「台灣經濟部回應 InterSecLab 的詢問時，說明了這套框架，但以法律限制為由，未對個案表達看法」。第 4 章〈結論〉：「現行版本的伺服器是通用 x86 硬體，即便正規採購受阻，這些元件仍能從次級市場取得」。第 2 章：「Nettrix 是中科曙光（Sugon）的子公司，曙光是已遭美國政府制裁的中國超級電腦製造商」。
[^gap]: 本文的推论。依据是 MADLink 社区译文第 3 章：「凌華科技確認出貨持續到 2020 年初」，以及 USENIX 论文 §6.3：「looking at previous measurements collected in December 2023」。论文以 2023 年 12 月的旧测量对照，自己的测量晚于那个时间，但没有写明日期。出货在 2020 年初结束，测量晚于 2023 年 12 月，两者至少相隔三年多。
[^jfm]: Justice For Myanmar 新闻稿，2024-06-19：「Justice For Myanmar calls on governments to urgently impose sanctions against Geedge Networks, CEIEC and Mascots Group, its directors and related companies」。
[^sanction]: 本文的查证，不是任何来源的说法。2026 年 10 月 30 日下载美国财政部 OFAC 的 SDN 名单与 Consolidated 名单、欧盟的金融制裁整合名单，搜索 Geedge 与 Jizhi 都没有符合的条目。作为对照，曙光（Dawning Information Industry）出现在 OFAC 的 Consolidated 名单。实体清单的新增都在联邦公报公告，在美国联邦公报搜索 Geedge 是 0 条，Jizhi 唯一的一条是另一家公司 Changguang Jizhi Optical Technology 被列入实体清单。英国的制裁名单与美国商务部的整合筛查名单这次没有下载成功，不在查证范围内。
[^local]: USENIX 论文 Ethical Considerations：「the git repositories contain commits and directories that list emails and names of individual developers」、「we emphasize that our focus is on the systems and architecture, and not on individual persons」、「do not include source material in our repository」、「our efforts to run a local operational copy of TSG could harm users experiencing censorship by enabling deploying countries to refine their systems」、「we choose not to publicly document or provide additional details on how to set up this firewall」、「We also considered whether it would be better to not deploy the firewall ourselves at all」、「develop and test circumvention strategies against a working instance」。
[^share]: USENIX 论文 Ethical Considerations：「We performed all of our scans between two vantage points that we own」、「we made sure that no entity is present on the current EU sanctions list」。Open Science：「We decided against the publication of the leaked source code and our deployment of the Firewall due to ethical concerns」。§1：「We will make our build available to trusted network security researchers upon request」。geedge.report 资源页：「All of our result files, anonymized PCAPs, and the scripts and tools used to conduct our scans are archived on Zenodo」。段落最后一句是本文的推论。
[^foci-ethics]: FOCI 论文 Ethical Considerations：「we believe the broad public interest of this information overrides potential intellectual property concerns」。GFW Report〈Geedge & MESA Leak〉：「analyzing these files only in an isolated (virtual) machine without internet access」。
[^lantern-site]: geedge.lantern.io 首页，2026 年 10 月 30 日读取：「Lantern research · sibling to」，后面接的是 corpus.lantern.io 的链接，页脚另有「Sibling project」。目的写在首页：「extracted for one purpose: telling a circumvention-tool builder exactly what they're up against」。about 页：「Raw leak content is never rehosted」。
[^lantern]: geedge.lantern.io 的 about 页：「Finding extraction runs as Sonnet-tier agents reading batches of extracted text」、「`high` requires an unambiguous, explicit source」。首页页脚，2026 年 10 月 30 日读取：「880 findings indexed from the September 2025 Geedge/MESA leak」。抽查是本文的查证，同一天从首页的 Recent findings 列表挑出五条，五条都标成 high。前三条发现从数据表的字段推论系统逐连接记录，原句分别是「This confirms, at the OLAP schema level」、「not just connection metadata」、「tags every session」。后两条分别依据代码与 changelog。测试用的判断依据是出处的路径显示是测试环境的配置集合，五条里有四条如此。五条的出处栏都只有存档与路径，没有 commit hash。
[^n4p]: 本文的查证，2026 年 10 月 30 日读取 net4people/bbs 的 #519 讨论帖，范围是 2025 年 10 月以后的留言。有出处指留言附上论文或正式报告的链接。
[^a24]: 网络政变社区译文第 6 章〈Geedge 的營運與客戶〉：「`A24` 的相關資料沒有任何可以辨識客戶的線索」、「關於 `A24` 客戶的身分，唯一的線索是首字母 A 與年份 2024」、「外洩發生時 `A24` 與 Geedge 的關係似乎還在初期階段」。MADLink 社区译文第 3 章：「也作為概念驗證部署給一個只以代號 A24 識別的未知客戶」。「没有看到公开的指认」是本文的查证，读取日期 2026-10-30：USENIX 论文与 FOCI 论文全文搜索 A24 都是 0 处。GFW Report 分析文章的中文版写到「除一个代号（A24）外，其余均已对应到具体国家」，其余段落转述 InterSecLab 的说法。net4people 讨论帖的 98 条留言里有 2 条提到 `A24`（2025-09-10、2025-09-11），也都是引用 InterSecLab 的报告。
[^future]: USENIX 论文 §5.1：「which we use to load SAPP's DNS, SSL, and QUIC plugins」。§4.2.2：「While all available archives」、「of the database in the leak are encrypted」，同一句在 PDF 里跨页排版。§4.1.1：「Although we found no code explicitly converting ASW or TSG2402 formats into Maat signature definitions」。§7：「We hope this work will serve as a guide for future research on the leak」。FOCI 论文 Future Work：「areas for future work include searching for IP addresses in the GNL, deeper analysis of documents such as PDFs, and improved OCR」、「the Tranco and Citizen Lab lists are limited compared to larger censorship measurement lists such as Common Crawl or ICANN CZDS」。
