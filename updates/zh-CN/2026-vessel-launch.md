---
title: Vessel 社区 VPN 发布公告
description: 匿名网络社区 anoni.net 为身边的人架设的 VPN，在学校、酒店与国外这些 VPN 常无法连接的地方也能使用。介绍台北、东京与新加坡的节点、中继路线、域名过滤，以及获取邀请码的方式。
date: 2026-11-07
kind: new
og_image: https://assets.anoni.net/vessel/og-zh-cn-bdeedae3.png
---

<figure markdown="span">
    <a href="https://vessel.anoni.net/zh-cn/" target="_blank">
        <img src="https://assets.anoni.net/newsletter/newsletter-vessel-overview-zh-tw-orig-59490d4a.png"
            alt="等角投影的蓝图样式示意图。你和身边的人的设备避开流量检查，直接或经台北入口连到台北、东京与新加坡的节点，再经过列有诈骗网站的过滤名单，连到互联网" class="shot">
    </a>
</figure>

在学校、酒店或国外，常用的 VPN 不一定能连上，遇到问题也不容易找到人询问。[Vessel](https://vessel.anoni.net/zh-cn/){target="_blank"} 是匿名网络社区 anoni.net 为身边的人架设的 VPN，连接经过伪装，在 VPN 连接受到封锁的网络里也比较容易连上。不需要 email，也不用付费，有问题有人回应。

!!! tip "获取邀请码"

    Vessel 目前以邀请码分批开放，邀请码通过电子报寄给订阅者，欢迎[订阅电子报](https://form.anoni.net/s/cmc9ceju1000dlj017fiathzq){target="_blank"}。也可以寄信到 whisper@anoni.net，或写在[反馈](https://vessel.anoni.net/zh-cn/feedback/){target="_blank"}页并留下联系方式，跟我们说明你的需要。

10 月 28 日寄出第一波邀请码之后，我们依照大家的使用状况调整服务。目前新增了台北节点与经台北入口的中继路线，直接连接不稳时多一条路可以选择，域名过滤也补上台湾的诈骗网站名单。

## 台北、东京与新加坡的节点

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-map-orig-5f1fb0f8.png"
        alt="方格组成的东亚与东南亚地图，台北、东京与新加坡各有一座灯塔，三座灯塔之间以虚线相连" class="shot">
</figure>

节点是你的连接连到互联网之前经过的主机。创建设备时选择城市，想换城市就新增一台设备。台北节点的主机在 Greenhost 的台北机房，从中华电信（台湾）连接的延迟约 2 毫秒，连到东京或新加坡则要 35 到 67 毫秒。台北节点的带宽比较小，适合日常浏览，大量下载建议选东京或新加坡。

我们找了一段时间都没有合适的台湾主机，社区运营的服务也不容易获得主机商支持。Greenhost 收到来信后同意让我们试行，协助开通了台北机房。谢谢 Greenhost。

## 经台北入口的中继路线

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-fig04-zh-orig-b3065627.png"
        alt="等角投影的示意图。设备先连到台北入口，由入口转发、不解开加密内容。连接再通往东京、台北或新加坡节点，出口是你选的城市" class="shot">
</figure>

中继路线的连接分成两段，架构跟 Apple 的 iCloud Private Relay 相近。连接先到台北的入口，再原封不动转发到你选的节点。入口收到的数据有你的 IP 与加密过的数据包，从中无法得知你连往哪里，也只统计经过的流量。节点连上网站时取得的数据有连接目的地，来源则是入口的 IP，不含你的 IP。Vessel 与 iCloud Private Relay 的差别是，Apple 的两段分属不同公司，Vessel 的入口与节点都由社区运营。

网络运营商只能看到你连到入口，无法得知你实际使用哪个节点。直接连到节点不稳或无法连接时，也可以改走中继路线。

新增设备时，在城市下方选择“台北入口 → 东京”、“台北入口 → 新加坡”或“台北入口 → 台北”，出口是节点所在的城市。想改用中继路线的话，新增一台设备即可。

## 域名过滤与台湾的诈骗网站名单

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-fig02-zh-orig-faca315a.png"
        alt="等角投影的示意图。设备连往网站之前，依次经过恶意程序、钓鱼网站与诈骗网站三道名单，名单上的域名被拦下" class="shot">
</figure>

新增设备时可以选择域名过滤。设备连往网站之前，会先向节点上的 DNS 解析器（把域名查成 IP 的服务）查询，名单上的恶意网站会直接被拦下。我们组合多份公开的名单，各自涵盖不同的类别：

- **恶意程序与钓鱼网站**：HaGeZi 的 Threat Intelligence Feeds，每 8 小时更新
- **台湾的诈骗网站**：台湾警政署 165（反诈骗咨询专线）停止解析的涉诈网站，以及台湾数位产业署停止解析的诈骗购物网站
- **广告与跟踪**：选择拦截广告时再加上 HaGeZi Multi PRO，每天更新

HaGeZi 的名单来源以欧美为主，10 月 31 日比对台湾 165 列管的 8.6 万个涉诈域名，只有 0.2% 在 HaGeZi 的名单上，因此我们先补上 165 的名单。之后再盘点其他公开的来源，台湾数位产业署的 1,734 个诈骗购物域名里，约 15% 不在现有名单上而且还在运作，所以也一起加入。接下来会继续评估其他华语地区公开的警示数据。

从 9 月的域名抽出 149 个查询，中华电信（台湾）的 DNS 全部回应封锁页，Cloudflare 的 1.1.1.1 却有 103 个解析到真正的网站。不论你从哪里连上 Vessel，查询都会改走节点的解析器，当地电信运营商的 DNS 封锁也就不再生效。

要更换已创建设备的过滤设置，需删除设备再重新创建。在[域名过滤](https://vessel.anoni.net/zh-cn/dns/){target="_blank"}页可以查询某个网站是否在名单上。

## 从设计开始的隐私与安全

<figure markdown="span">
    <img src="https://assets.anoni.net/newsletter/newsletter-vessel-exploded-zh-orig-7e046afc.png"
        alt="四层叠起的分解图，由上而下是你的设备（私钥只在这里）、入口网站（不需要 email、账号号码只存哈希、不留谁邀请了谁）、节点（防火墙记录关闭、交换不写入硬盘）与公开的图纸（代码与主机设置都在 GitHub）" class="shot">
</figure>

连接用的私钥（只留在设备上的密钥）在你的浏览器生成，账号不需要 email，账号号码只存哈希（无法还原回号码的单向运算结果），都是一开始就放进设计里的做法（privacy and security by design）。邀请码兑换之后也不留下谁邀请了谁。上线之后我们持续调整，例如关掉节点防火墙的记录、停止把内存的交换数据写入硬盘，减少节点硬盘上可能留下的连接信息。

Vessel 网站的代码与节点的主机设置，都完整公开在 [GitHub](https://github.com/anoni-net/vessel){target="_blank"}。欢迎大家一起检视、查核，发现问题或有更好的修正与功能，都可以开 issue 或提交 pull request。

## 蓝图样式的网站

[Vessel 的网站](https://vessel.anoni.net/zh-cn/){target="_blank"}是工程蓝图的样式，钴蓝色的线条、方格纸的底色，标题是一格格方块叠成的 Vessel。

Vessel 有船的意思，造船之前要先画图纸。每个零件的位置与尺寸都标在图纸上，检查时也看同一份。VPN 服务的网站上常见盾牌与锁头的图案，用户仍然无法得知内部如何运作。我们希望大家信任的是实际的做法，所以把网站画成一张摊开的图纸，连接经过哪些节点、名单如何比对、密钥在哪里生成，都画在首页。

Vessel 也有容器的意思，首页的方块标题会慢慢装满。像素小人扛着钴蓝色的数据包跳过字母，压进最后的 l，整个字由下往上填满。

## 使用前要知道的事

Vessel 不提供匿名，你连往的域名与 IP 会经过节点，需要匿名时请使用 Tor Browser。服务由志愿者维护，不保证服务不中断。伪装能降低被封锁的机会，但不保证每个网络都能连上（规则见[使用条款](https://vessel.anoni.net/zh-cn/terms/){target="_blank"}）。

有些地方限制或禁止未经批准的 VPN，在当地使用 Vessel 也可能受罚，当地的网络运营商仍然可以看到设备连到境外的 IP。处境敏感时，请先读常见问题的[所在地限制 VPN 时，使用 Vessel 安全吗？](https://vessel.anoni.net/zh-cn/faq/#q-risky){target="_blank"}与文档站的[出差与研讨会的数字准备](docs:scenarios/asia-travel/)，再决定是否使用。

## 分享给朋友的邀请码与反馈

如果你认识我们的社区，也认同社区维护、代码公开的做法，欢迎把 Vessel 分享给身边需要的人。账号创建满 14 天、而且有设备连接过之后，可以在[账号](https://vessel.anoni.net/zh-cn/account/){target="_blank"}页的“邀请朋友”生成一组邀请码。邀请码请给认识、信任的人使用，不要公开张贴。邀请码 7 天内有效，只能用来创建一个账号。

使用上遇到问题、连接质量不稳，或希望加开其他城市的节点，请写在[反馈](https://vessel.anoni.net/zh-cn/feedback/){target="_blank"}页，也可以通过以下渠道联系：

- **即时讨论**：Matrix 公开聊天室（主服务器 `im.anoni.net`，链接见[社区服务页](/zh-cn/services/)）
- **匿名线索**：whisper@anoni.net（[GPG 公钥](/zh-cn/contact/)）

## 相关阅读

- [Vessel 的常见问题](https://vessel.anoni.net/zh-cn/faq/){target="_blank"}
- [VPN 的风险与选择](docs:tools/vpn-guide/)
- [出差与研讨会的数字准备](docs:scenarios/asia-travel/)
