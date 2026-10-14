---
title: 去中心化网站发布
description: 自建、CDN、IPFS 与 onion 服务的设计取舍，内容寻址与连接匿名的差异，以及 anoni.net 文档站同时发布三份的部署方式。
date: 2026-05-01
---

网站的发布方式除了自建服务器加 DNS，还有 CDN 把内容缓存到各地的边缘节点、IPFS 用内容寻址让文件在多个节点之间流通，以及 Tor onion 服务让网站直接在 Tor 网络里以 .onion 地址运行。后两者常被放在一起讨论，但 IPFS 针对内容被删除与下架，onion 服务针对连接匿名与 IP 封锁。把 IPFS 当成匿名工具或期待 onion 服务抵抗下架，都会落空。anoni.net 文档站同时发布标准网站、onion 与 IPFS 三份，部署时的取舍可以当成实例。

## 网站发布的选项

从中心化、性能优先到去中心化、抗审查，常见的选项有五种：

- **自建服务器**：自行管理 IP 与 DNS，完全可控，也完全集中。IP 被封锁或服务器被没收，网站就无法访问。
- **CDN**（Cloudflare、Fastly、CloudFront）：由边缘节点代理流量，性能与抵抗 DDoS 的能力强，但高度依赖 CDN 服务商与 DNS。
- **静态网站托管**（GitHub Pages、Cloudflare Pages、Netlify）：部署简便，服务商可以单方面下架。
- **IPFS**：内容按 hash 寻址，任何节点都可以提供同一份内容，没有单一可下架的位置，内容能否存续取决于有没有节点 pin。
- **Onion 服务**：网站直接在 Tor 网络里运行，不需要公开 IP 与 DNS。连接匿名、不受 IP 封锁影响，代价是性能较差，能访问的客户端也有限。

实际部署多半混搭，主站走 CDN 求性能，IPFS 镜像抵抗删除，onion 镜像抵抗封锁。

## IPFS 的设计

IPFS（InterPlanetary File System）以内容寻址（content addressing）为核心：

- **CID**（Content Identifier，内容标识符）：按文件内容算出的 hash，同时也是内容的地址。内容相同，在任何节点上的 CID 都相同。
- **DHT**（Distributed Hash Table，分布式哈希表）：节点之间互相查询谁持有某个 CID，以 Kademlia 算法定位，不需要中央服务器登记。
- **IPNS**（InterPlanetary Name System）：把固定的名称指向当前的 CID。内容更新时 CID 会改变，IPNS 记录随之更新。

内容寻址对网站发布带来三个特性：

1. **没有单一可下架的位置**：只要还有节点 pin 住这个 CID，内容就能取得。
2. **篡改可以检测**：CID 是内容的 hash，内容被改动，CID 就不同，读者可以自行验证。
3. **跨节点共用**：同一个文件不论被多少网站引用，CID 都只有一个，缓存可以共用。

设计上的限制：

- **内容存续依赖 pin**：没有节点 pin 的内容会在垃圾回收时消失，放上 IPFS 不等于永久保存。
- **DHT 查询延迟**：第一次取得内容比 HTTP 慢。
- **依赖网关**：多数读者通过公共网关读取，网关被封锁就读不到。公共网关的数量也在减少。Cloudflare 的 cloudflare-ipfs.com 与 cf-ipfs.com 在 2024 年 8 月退役，流量转往 ipfs.io 与 dweb.link，后两者在 2026 年 9 月 30 日随 Interplanetary Shipyard 结束 IPFS 工作一起停止运营（对 pin 节点的影响见[文档站 IPFS 镜像的 pin 节点](/join/pin-ipfs-mirror/#ipfs-maintenance-2026)）。
- **动态内容受限**：IPFS 适合静态内容，动态功能需要另外一层。

## Onion 服务的设计

Tor onion 服务第 3 版（v3）让网站直接在 Tor 网络里运行（架设步骤见[.onion 服务架设指南](/join/setup-onion-service/)）：

- **自我验证的地址**：v3 的 .onion 地址长 56 个字符，由服务的 ed25519 公钥编码而成，不需要 DNS 与证书颁发机构，也少了一个域名解析被拦截或篡改的环节[^1]。
- **描述符发布**（descriptor publishing）：服务把含有引入点（introduction point）的描述符发布到 Hidden Service Directory（HSDir）。
- **会合协议**（rendezvous protocol）：用户与服务在 Tor 网络里的会合点建立加密连接，双方都不知道对方的 IP。

对网站发布的意义：

1. **双向的连接匿名**：网站看不到访客的 IP，访客也看不到网站的 IP。
2. **不依赖 DNS**：.onion 地址可以自我验证，没有 CA 信任链的问题。
3. **不受 IP 封锁影响**：流量都在 Tor 网络里，封锁网站的 IP 没有作用。
4. **不需要公网 IPv4 地址**：在 NAT 后面或动态 IP 上都能启动。

设计上的限制：

- **性能**：客户端三跳加上服务端三跳，共六个中继组成一条线路，再加上会合的过程，延迟比直连高。
- **依赖 Tor 网络**：Tor 中继被大量封锁时，整个 .onion 生态都受影响。
- **不适合大量静态资源**：图片与视频经由 Tor 传输的成本高。
- **访客门槛**：访客需要 Tor Browser 或支持 onion 的客户端。

## IPFS 与 onion 的对照


| 项目 | IPFS | Onion |
|---|---|---|
| 主要解决的问题 | 抗删除、避免集中失效 | 连接匿名、抗 IP 封锁 |
| 访客匿名 | ❌ 没有内置 | ✅ 默认提供 |
| 服务匿名 | ❌ 节点 IP 可见 | ✅ 默认提供 |
| 篡改检测 | ✅（CID 即 hash） | 需另外依靠 TLS 或签名 |
| 抗下架 | ✅（多个节点 pin） | 部分（运营者可以关闭单一服务） |
| 大文件的性能 | 中等 | 差 |
| 动态内容 | 困难 | 与一般网站相近 |
| 访客门槛 | 低（浏览器经由网关） | 高（需要 Tor Browser） |

需要抗删除选 IPFS，需要连接匿名选 onion，两者都需要时，同一个网站同时发布两份镜像。

## 已知限制与风险

挑选组合之前，需要先考虑两种技术各自做不到的部分：

- **IPFS 没有连接匿名**：PeerID 长期不变，DHT 查询在公开网络上进行，第三方看得到哪个 IP 在找哪个 CID（完整的暴露面见[常被误认为匿名的网络](docs:basics/mistaken-for-anonymity/)）。
- **IPFS 的内容存续依赖主动 pin**：Pinata 这类中心化的 pin 服务，或 Filecoin 这类以代币激励运作的去中心化存储协议，都让永久保存重新依赖第三方。
- **Onion 服务依赖 Tor 网络**：Tor 中继被大量封锁，或 Tor Project 停止运维，.onion 生态都会受影响。
- **入口多半仍是中心化服务**：读者通过公共网关或 Tor Browser 访问，这些入口本身就是潜在的攻击面。公共网关也会整批停止运营，网址写死在单一网关上的网站，网关停止运营时对外链接会一起失效。
- **法律上的灰色地带**：架设 Tor 出口节点、提供 IPFS pin 服务，在不同的司法管辖下风险不同。

## 常见组合

### Onion 与 IPFS 双镜像

主站照常发布在一般网络上，另外提供两份镜像：

- IPFS 镜像：每次发布的内容对应一个 CID，社区志愿者可以协助 pin（做法见[文档站 IPFS 镜像的 pin 节点](/join/pin-ipfs-mirror/)）。
- Onion 镜像：内容与主站相同，提供匿名访问。

EFF[^2]、Proton、BBC 与美国中央情报局（CIA）都架设过官方的 onion 镜像，纽约时报从 2017 年起提供的 onion 版在 2025 年 3 月关闭[^3]。Cloudflare 另外提供 Onion Routing，网站在 Cloudflare 启用之后，响应会带上 `alt-svc` 头，Tor Browser 的访客改由 Cloudflare 的 .onion 端点接入，不经过出口节点[^4]。

### IPFS 与 ENS

ENS（Ethereum Name Service，以太坊域名服务）可以给 IPFS 内容取一个好记的名称（例如 `example.eth`），由 ENS 上的记录指向当前的 CID，每次更新内容就更新一次记录。ENS 本身依赖以太坊区块链，名称也需要付费，去中心化的程度有前提。

## anoni.net 文档站的部署

anoni.net 文档站同时发布标准网站、onion 与 IPFS 三份，内容相同，三套构建流程各自处理网址与路径的差异。


1. **源文件**：MkDocs Material 格式的 Markdown，放在 GitHub 的 `anoni-net/docs`。
2. **标准网站与 onion**：推送 `docs` 分支时，GitHub Actions 的 `build_docs.yml` 同时构建两份三语种的静态网站，以 `aws s3 sync --delete` 上传到同一个 S3 bucket 的不同 prefix（`docs/` 与 `docs-onion/`），标准网站经由 Cloudflare 对外提供。onion 那份在构建前先执行 `replace_sitename_anoni_onion.sh`，把站内网址改写成 `docs.<onion 地址>`，并去掉统计脚本与 service worker。`build_docs_anoni.sh` 与 `build_docs_anoni_onion.sh` 是同样步骤的本地版本。
3. **IPFS**：`build_docs_anoni_ipfs.sh` 不在 workflow 里，需要另外执行。脚本先把网址改写成 IPFS 网关的地址，构建三语种，确认产物里没有残留主站网址，再由 `upload_to_ipfs.sh` 上传并更新 IPNS 名称。社区自建的网关是 `ipfs.anoni.net`，`_dnslink.anoni.net` 也指向同一个 IPNS 名称。

读者如何用 onion 或 IPFS 阅读文档站、访问过程中谁看得到什么，见[你正在用哪一种方式阅读](docs:about/how-you-are-reading/)。

### 运维上的取舍

- **pin 与内容存续**：社区成员可以协助 pin，提高内容的存续机会（[操作指南](/join/pin-ipfs-mirror/)），没有正式的保证。
- **Onion 的延迟**：经由 Tor 访问时，SPA 或大型 JavaScript 包的使用体验较差，文档站因此维持一页一个 HTML 的静态网站。
- **三个网址的定位**：标准网站是主要入口，IPFS 与 onion 是备援与抗封锁的渠道。

### 实际运行的限制

- IPFS 公共网关有时不稳定，影响第一次加载。网关也可能停止运营，所以镜像的站内链接采用网站根目录的相对路径，更换网关不需要重建整份镜像。
- IPFS 镜像需要另外构建与上传，更新时间可能晚于标准网站与 onion。
- 三语种的资源让 IPFS 上的 CID 数量增加，pin 列表随之变长。

## 相关阅读

- [你正在用哪一种方式阅读](docs:about/how-you-are-reading/)：标准网站、onion 与 IPFS 镜像在读者端的差异
- [常被误认为匿名的网络](docs:basics/mistaken-for-anonymity/)：IPFS 等网络对外暴露的信息
- [什么是 Tor](docs:tools/what-is-tor/)：Tor 网络的设计与威胁
- [网络政变报告](https://anoni.net/docs/reports/interseclab-network-coup/)（正体中文）：InterSecLab 依据外泄文件分析中国防火长城技术输出到其他国家，呈现集中化的审查基础设施如何运作
- [后量子密码概观](/articles/post-quantum/)：量子计算机对现行公钥密码的威胁与迁移时程

## 可参与的项目

- [文档站 IPFS 镜像的 pin 节点](/join/pin-ipfs-mirror/)：用常驻的 IPFS 节点为文档站的 IPFS 镜像多保存一份
- [.onion 服务架设指南](/join/setup-onion-service/)：架设 v3 onion 服务、接上 nginx，以及上线之后的运维
- [Tor Relay 架设指南](/join/setup-tor-relay/)：中继、桥接与出口节点的架设与运维
- [Tor Relay 校园建立研究专题](/join/relay-on-campus/)：在学校架设中继节点的提案与沟通
- [中文化与文件翻译](docs:community/i18n/)：文档站与 Tor 文档的翻译流程

[^1]: [V3 onion services usage](https://blog.torproject.org/v3-onion-services-usage/) - The Tor Project
[^2]: [EFF Now Has Tor Onions](https://www.eff.org/deeplinks/2023/04/eff-now-has-tor-onions) - Electronic Frontier Foundation
[^3]: [\[Onion services\] Remove NYTimes logo](https://gitlab.torproject.org/tpo/web/community/-/issues/374) - Tor Project GitLab
[^4]: [Onion Routing](https://developers.cloudflare.com/network/onion-routing/) - Cloudflare Docs
