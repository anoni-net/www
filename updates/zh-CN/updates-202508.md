---
title: 2025/08 项目进度更新
description: 近期社区活动更新信息
date: 2025-09-09
kind: update
---

![近期社区活动更新信息](https://assets.anoni.net/updates/post-update-6ce5f133.png){ .shot }

在 8 月 9 日 - 8 月 10 日的[工作坊活动](/events/workshop-2025/)已顺利举办完成，我们目前正在准备工作坊后的讨论、回顾，思考后续可以努力的方向。无论您是否参与了这两天的活动，首先感谢您持续关注我们！

接下来与您分享 2025 年 8 月这段期间我们的更新内容。

## 摊位、手册

在工作坊活动结束后，我们还参与了 [HITCON](https://hitcon.org/2025/)、[PyConTW](https://tw.pycon.org/2025/) 的研讨会活动。虽然我们没有申请摊位，但我们制作了一本关于 “匿名网络” 的手册，内容包括社区介绍、Tor/Tails、OONI 的介绍、网络自由、匿名网络议题说明，以及社区目前使用哪些开源软件来自架服务，并在研讨会会场中放置供领取。

这本手册将来仅能在实体活动参与时获得，每次都会少量印制，随时增补新信息到手册中。在工作坊活动时，我们也为每位参与者提供了一本。通过这次活动的观察，有助于参与者了解社区想要传达的“匿名网络、网络自由”理念。未来如果有类似的研讨会或社区活动，我们也会主动申请摊位，以继续推广。


## 整理协作笔记内容

工作坊活动后，我们计划在 9 月 21 日召开工作坊工作人员的回顾会议，整理活动协作笔记内容。你可以通过这里的[活动议程表](/events/workshop-2025/#%E5%AE%8C%E6%95%B4%E6%B4%BB%E5%8A%A8%E6%97%B6%E9%97%B4%E8%A1%A8)上的链接回顾协作笔记内容，也可以回信告诉我们你的想法，包括对 2025 年底或 2026 全年时间段的建议。

## 翻译文章

在 2025 年 8 月，我们仍在持续更新 Tor/Tails 和 OONI 官方网站的信息，不少内容在这个月发布。我们会尽可能在一周内将文章翻译、校对后上线。除非您有研究上的需求，也可以直接关注官方网站的信息发布。

- [Tails 7.0 发布第二个最终测试版本（7.0~rc2）](docs:blog/2025/09/tails-7-released/) - 2025/08/29
- [OMG！第三届 Open Measurement Gathering（OMG）的有问必答（AMA）活动总结](https://ooni.org/post/2025-omg/) - 2025/08/29
- [贪腐与管控：土库曼如何将网络审查变成一门生意](docs:blog/2025/08/tor-corruption-control/) - 2025/08/30
- [Tails 6.18 支持 WebTunnel 网桥协议](docs:changelog/tails/) - 2025/07/31

此外，我们还看到 [The MIT Press Reader](https://thereader.mitpress.mit.edu/) 发布了一篇不错的文章，并在获得 The MIT Press 的同意后翻译成中文内容。这篇文章我们不仅仅翻译了内容，还通过注释的方式补充提及到的一些历史事件的背景。

- [Tor 的秘密历史：如何从军事项目到维系隐私的生命线](docs:blog/2025/09/tor-military-to-privacy/) - 2025/09/07

## 匿名搜索 SearXNG

<figure markdown="span">
    ![SearXNG](https://assets.anoni.net/updates/searxng-d79d0c2c.png){width="50%" title="SearXNG"}
</figure>

[SearXNG](https://searxng.org/) 是一个开源的隐私网络搜索引擎，主要用于保护用户的隐私。SearXNG 从多个搜索网站来源汇总搜索结果，但不追踪用户，也不收集个人数据。SearXNG 可以自建服务器，增加隐私保护，并支持自定义设置，让用户选择想要的搜索引擎及过滤规则。

鉴于目前[公开的](https://searx.space/)服务器列表中，位于亚洲地区的服务器服务不多，我们在一周前已经把 SearXNG [架设起来](https://search.anoni.net/)，并[申请](https://github.com/searxng/searx-instances/issues/738)成为公开服务器服务，基本的技术要求已经通过，进入到两周的观察期。也欢迎协助我们测试，在这两周的观察期间，确认主机能承受日常的使用。

## Tor WebTunnel

<figure markdown="span">
    <a target="_blank"
       href="https://assets.anoni.net/updates/tor_relays-79b40891.svg">
        <img src="https://assets.anoni.net/updates/tor_relays-79b40891.svg"
            alt="Tor Relay 类型"
            title="Tor Relay 类型"
        >
    </a>
    <figcaption>Tor Relay 类型</figcaption>
</figure>

WebTunnel 是 Tor 网桥类型中的一种，帮助 Tor 用户在无法直接连接到 Onion 洋葱路由网络时，通过代理转接连接的服务器。详细的介绍与说明可以参考[这篇文章](docs:tools/what-is-tor/#%E4%B8%AD%E7%BB%A7%E8%8A%82%E7%82%B9%E6%A1%A5%E6%8E%A5%E8%8A%82%E7%82%B9)。自 Tails 6.18 版本起，也加入了对 WebTunnel 网桥方式的连接支持。由于网桥有其功能的重要性，因此不会在 Tor 官网上公开连接参数，需要通过[主动索取](https://bridges.torproject.org/)的方式获取连接信息。

因此，我们无法统计目前有多少台 Tor WebTunnel 的网桥建立在台湾。如果您有兴趣，可以参考 “[WebTunnel Docker setup](https://community.torproject.org/relay/setup/webtunnel/docker/)” 来建立，或者如果您已经有一个配置了 nginx 的服务，可以提供一个路径给 WebTunnel 网桥连接来[贡献一个节点](https://community.torproject.org/relay/setup/webtunnel/)，我们对此非常感谢！

当然，还有更简单的方法来协助贡献一个网桥，就是通过浏览器的方式建立 [Tor Snowflake 网桥](docs:tools/tor-snowflake/)！

## 最后

以上是目前社区的工作进度，也欢迎给我们[提供](/contact/)任何建议或意见，感谢！
