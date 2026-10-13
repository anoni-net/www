---
title: 无状态 Tor Relay 的部署路线与开放问题
description: Osservatorio Nessuno 在 Tor Blog 发表的 A Server That Forgets 全文翻译，内容包括无状态 Tor Relay 的 TPM 密钥保护、三种部署路线与尚未解决的工程问题，文末补充台湾运营者的视角。
date: 2026-04-10
---

中继节点被扣押时，机器里能交出的东西越少，用户就越安全。在意大利运营出口节点的 Osservatorio Nessuno 把这个想法推进到操作系统层，让 relay 每次开机都从同一份只读镜像启动，身份密钥交给 TPM 保管。他们在 Tor Blog 的客座文章比较了三种已经有人采用的部署路线，也列出重新 sealing、自动更新与内存上限等尚未解决的问题，适合正在评估硬件与部署方式的运营者参考。

以下翻译自 Osservatorio Nessuno 在 Tor Blog「捍卫自由网络的组织」系列发表的 [A Server That Forgets: Exploring Stateless Relays](https://blog.torproject.org/exploring-stateless-relays/)（2026-04-08），文中的「我们」指 Osservatorio Nessuno。文末的台湾运营者视角由 anoni.net 社区补充。

[![A Server That Forgets](https://forum.torproject.org/uploads/default/original/2X/e/ee9375b0ec3906d4a0338bc230d97d0a659d996a.jpeg){ .shot }](https://blog.torproject.org/exploring-stateless-relays/)

运营 Tor relay 需要持续对抗试图攻击节点、借此破坏整个网络的对手，对方可能是私人势力，也可能有国家支持。一些运营者还要面对扣押、搜查，或硬件遭到直接物理接触。[奥地利](https://www.zdnet.com/article/austrian-man-raided-for-operating-tor-exit-node/)、[德国](https://forum.torproject.org/t/tor-relays-artikel-5-e-v-another-police-raid-in-germany-general-assembly-on-sep-21st-2024/14533)、[美国](https://www.npr.org/sections/alltechconsidered/2016/04/04/472992023/when-a-dark-web-volunteer-gets-raided-by-the-police)与[俄罗斯](https://torservers.net/blog/2017-04-14-freebogatov-relaymob/)都有先例，其他地方很可能也有。在这些案例里，服务器本身可能成为运营者的负担。

Tor 存在的目的，是保护网络用户免受不必要的监控。Tor 网络的设计让任何单一运营者或服务器都无法还原谁在和谁通信，记者、社会活动人士与吹哨人都依赖这个前提。relay 若在扣押后能交出内容，整个系统赖以运作的信任就会受到侵蚀，我们想解决的正是这个问题。

本文探讨无状态、无磁盘的操作系统如何从固件到用户空间提升 relay 的安全，重点放在软件完整性与抵抗物理攻击的能力。内容来自 Osservatorio Nessuno 在意大利运营出口 relay 的经验。relay 的管理方式随背景、技术能力、预算与司法管辖而有很大差异，我们希望引发讨论，文中的做法只是其中一种模式。

## 无状态系统

无状态系统在重启之间不保留任何数据，每次开机都从固定、已知的镜像启动，做法与 [Tails](https://tails.net/) 相同。把 Tor relay 完全放在 RAM 里运行并非新构想，专为这个用途制作、基于 uClibc 的微型 Linux 发行版 [Tor-ramdisk](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html)，至少在 2015 年就已经出现。

对 relay 运营者来说，无状态的设计本身就要求更好的操作习惯，安全门槛也随之提高：

- **抵抗物理攻击**：机器被扣押或克隆时，里面没有可供分析的东西。视部署方式而定，提取 relay 密钥可能变得不可行。
- **声明式配置**：系统配置纳入版本控制，每次开机都重新应用一次声明的配置，系统不会偏离它。
- **不可变的运行环境**：文件系统只读，攻击者即使取得代码执行权限，也无法让任何东西在重启后留存。
- **可复现性**：重启前后不变的系统比较容易验证，进一步也能复现与审计。

## Tor Relay 做到无状态的难处

Tor relay 的信誉随时间积累，连续运行数月的 relay 会获得带宽相关的标记，对网络更有用。信誉绑定在长期的加密身份密钥上，密钥丢失，relay 就失去身份与在网络中的信誉，只能从头开始。

所以 relay 的身份必须在重启后延续，同时又不能被提取。存在磁盘上的密钥可能被扣押与复制，放在 TPM 这类安全芯片里，攻击者要取得可能就困难得多。

除了身份密钥，relay 还会积累一份 state 文件，记录带宽历史与其他临时信息，每次重启都丢弃它会拖累性能。完全在 RAM 里运行，也意味着整个操作系统要放得进内存，而且没有 swap 可用。进程超出可用内存时，内核的 OOM killer 会直接终止它们。实践中，把 glibc 的内存分配器换成 jemalloc 或 mimalloc，可以明显[降低 Tor 的内存占用](https://1aeo.com/blog/tor-memory-optizations-what-actually-works.html)，在一台繁忙的 guard relay 上从约 5.7 GB 降到 1.2 GB 以下，主要原因是避开了目录缓存对象频繁更替造成的碎片化。

## TPM 的角色

TPM（Trusted Platform Module，可信平台模块）是主板上的专用硬件芯片，负责存储加密密钥并用它们执行运算，私钥从不暴露给操作系统。TPM 可以 seal 一份秘密，也就是把它绑定到机器的特定度量状态，只有度量到的软件栈与创建密钥时完全相同，密钥才能使用。

对无状态 relay 来说，身份密钥存在硬件里，可以跨重启保留，即使机器遭到物理接触，也无法用常规方法提取。TPM 也支持远程证明（remote attestation），芯片可以向外部系统证明机器启动时加载了哪些软件，并附上以硬件为信任根的签名。这样一来，不必信任运营者，也能验证节点实际运行的内容。

TPM 也有解决不了的地方，例如 Tor 使用的 ed25519 密钥不受 TPM 芯片支持，密钥虽然经过 TPM 加密，仍以字节串存放在非易失性存储中，技术上还是有可能导出。

sealing 还要求事先决定 TPM 要信任哪些软件状态。更新内核或 bootloader 时度量状态会跟着改变，运营者必须预测下一次开机的度量结果，重新 seal TPM。

## 现有的部署路线

不同的运营者在部署的简便程度与安全深度之间，选了不同的取舍点。

### 最小化的 RAM disk

最简单的做法是全部放在 RAM 里运行，密钥手动管理。[Tor-ramdisk](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html) 从 2015 年起就采用这种做法，身份密钥通过 SCP 导出与导入，重启前没有导出就只能从头开始。这条路线没有 TPM、远程证明与 verified boot，唯一的保证是断电后 RAM 的内容不会留存，但与传统把状态存在磁盘上的部署相比，仍是有意义的改进。

### 以 VM 运行的 RAM disk

[Emerald Onion](https://blog.emeraldonion.org/evolving-our-tor-relay-security-architecture) 在 Proxmox hypervisor 上为每个 relay 运行一份 Alpine Linux 镜像（每份 66 MB），VM 完全启动到 RAM 里，不挂载任何持久存储。身份用 Tor 的 OfflineMasterKey 功能管理，长期的 master key 在离线环境生成，从不经过 relay。更新的方式是重建镜像，回滚很容易，也不需要特殊硬件。

### 裸机与绑定 TPM 的身份

我们开发的 [Patela](https://github.com/osservatorionessuno/patela) 走偏向硬件的路线。relay 通过 [stboot](https://docs.system-transparency.org/st-1.3.0/docs/reference/stboot-system/) 启动，这个 bootloader 会先下载已签名的操作系统镜像并验证签名，再交出控制权。启动之后，节点通过 mTLS 从中央服务器获取配置。中央服务器即使被入侵，攻击者也只能让服务中断，无法把凭据推送到节点，也无法从节点提取密钥。relay 的身份密钥存在 TPM 的非易失性存储中，绑定度量过的启动状态，可以跨重启保留，即使遭到物理接触也无法提取。代价是运营更复杂，需要裸机，每次更新后也要重新 seal。

## 尚未解决的问题

有些问题只出现在我们的部署，有些是所有无状态 relay 都会遇到的。

### 更新后的重新 sealing

软件栈改变时，TPM 的度量状态也跟着改变。要自动化重新 sealing，就得预测更新后的启动度量值，目前仍是较难的未解问题之一。systemd-pcrlock 等工具正朝这个方向发展，但还无法开箱即用。

### 无状态重启与升级的冲突

我们用标准的 unattended upgrades 更新 Tor 可执行文件，但重启会回到操作系统镜像，镜像里还是前一个版本，结果变成非预期的降级。自动安全更新与无状态镜像要如何兼顾，我们还没有完全解决。

### 内存限制

没有 swap，进程超出可用内存时会在没有预警的情况下被终止，而 Tor 运行时的内存占用很难预测。前面提到的分配器替换帮助很大，但根本的限制仍在。

### 网络稳定性

持久的更新只能通过重建镜像、重新启动来应用。relay 若太频繁重启，可能失去 Stable 标记，影响网络分配给它的流量。

## 未来方向

### 远程证明

sealing 把密钥绑定在机器的状态上，attestation 则让节点向外部证明自己处于该状态。配置服务器，或将来的 Tor directory authority 这类验证方，可以发出加密挑战，只有运行预期软件栈的节点能正确响应。启动完整性因此从只能在本机确认的属性，变成可以远程验证，对运营者的信任需求也随之降低。

### 透明日志

有了度量过的启动链，就能把度量结果公开。relay 运营者提供可复现构建的做法，任何人都能重新计算预期的哈希值，比对是否与 TPM 报告的一致。只能追加写入的透明日志（transparency log）可以让这些证明接受公开审计，Tor 社区也可以运行独立的监测服务，跟踪整个 relay 群的状态。

### 机密计算

VM 路线可以再结合 AMD SEV-SNP 等技术，把 guest VM 的内存与 hypervisor 本身隔离。结合之后同样能降低对运营者的信任需求，也能缩小 VM 与裸机路线之间的安全差距。

### 更小的硬件

Walking onions 是一项提案中的 Tor 协议扩展，节点不再需要在本地保存整个网络的视图。如果 arti 与相关工具能在更小的硬件上运行，目前负担不起资源成本的设备也有机会用来运营 relay。

## 结语

对 Tor 这类应用，无状态设计同时能防范攻击与减少运营者的操作失误。再经过更多研究与工程，还有机会提高整个网络的可信度。

无状态系统有实际的运营成本，也有真正困难的未解问题，资源较多的项目与组织同样要面对。不过它可以作为改进隐私基础设施的基础，类似的概念与框架也能用在技术栈的其他部分。

这项工作从 [Tor Community Gathering 2025](https://tcg2025.4711.se/sessions/stateless_tor_relay/) 开始，目前仍在进行。如果你运营 relay、开发 Tor 相关工具，或思考过上述任何一个问题，我们很想听听你的想法。

## 参考资料

- [Stateless Tor Relay – Tor Community Gathering 2025](https://tcg2025.4711.se/sessions/stateless_tor_relay/)
- [Patela v1: A Basement Full of Amnesic Servers](https://osservatorionessuno.org/blog/2025/05/patela-a-basement-full-of-amnesic-servers/)
- [Patela v2: From Certificates to Hardware](https://osservatorionessuno.org/blog/2025/12/patela-v2-from-certificates-to-hardware/)
- [stboot System Documentation – System Transparency](https://docs.system-transparency.org/st-1.3.0/docs/reference/stboot-system/)
- [Tor-ramdisk 20150714 Release Announcement](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html)
- [Evolving Our Tor Relay Security Architecture – Emerald Onion](https://blog.emeraldonion.org/evolving-our-tor-relay-security-architecture)
- [Tor Memory Optimizations: What Actually Works – 1AEO](https://1aeo.com/blog/tor-memory-optizations-what-actually-works.html)

---

## 台湾运营者的视角

以下由 anoni.net 社区补充。台湾网络普及、商业托管成熟，同时身处区域信息冲突的压力之下，同一套技术方案常要兼顾快速上线与高压下的实际考验。

台湾现有的小型主机供应、数据中心服务与公民科技社区，可以帮助运营者比较快建立标准化的镜像、事件应对流程与可验证的运行记录。不过台湾的 relay 多由志愿者分散运维，遇到滥用投诉、设备处置要求或执法部门接触时，流程若没有事先准备好，技术设计再好也无法降低运营者个人承担的风险。放到台湾的条件来看，下面三个方向值得先着手。

### 志愿者运营与法律程序

台湾的 relay 与 exit 运营者可以先整理机房通知、执法接触与设备扣押的标准应对流程。技术上先把可提取的数据降到最低，事件发生时运营者个人承担的风险也比较小。

### 硬件获取与供应链成本

具备 TPM 的主机、小型服务器与托管服务在台湾都可以获取，但成本差距很大。社区若能整理出几组可复现的硬件与镜像组合，运维与审计的成本比较容易控制。每个团队各自组一套的话，安全主张难以互相比较，维护成本也会持续增加。

### 可验证计算的公共讨论

度量启动链、远程证明与透明日志的用途不限于 Tor 的技术圈，也与公民科技、关键基础设施透明度的讨论有关。这些证明要成为社区共享、外界能理解的证据，才能支撑社会的信任。若只有少数技术人员能读懂，外界的信任仍只能依靠口碑。

## 相关阅读

- [Tor Relay 架设指南](/join/setup-tor-relay/)：中间节点的架设步骤与运维配置
- [Tor Relay 校园建立研究专题](/join/relay-on-campus/)：在大专院校架设 relay 的评估与经验
