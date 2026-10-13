---
title: 文档站互动区与 Tor 中继地球仪的开放数据许可
description: 文档站互动区的三件 Tor 作品，以及制作中继地球仪时查过的二十几份公开数据，哪些许可允许再分发、哪些受阻在条款。
date: 2026-07-28
kind: new
og_image: https://assets.anoni.net/games/tor-network.png
---

![Tor 中继地球仪](https://assets.anoni.net/games/tor-network.png){ .shot }

文档站添加了[互动与呈现](docs:games/)区，目前收录三件以 Tor 为题的作品。数据量最大的是 [Tor 中继地球仪](docs:games/tor-network/)，把全球近万台运作中的中继标在球面上，其中超过六成集中在美国、德国、荷兰。

制作地球仪时，我们查了二十几份公开数据，最后可用的只有六份。多数 API 都能正常响应，数据格式也干净，受阻的原因几乎都在条款不允许再分发。


## 用画面呈现的理由

匿名网络的基础设施很难用文字说清楚，难处在顺序与规模。

Tor 的顺序最具代表性。数据包在三个中继之间依序前进，每经过一跳剥除一层加密，到出口才还原成原本的请求。哪一层在哪一跳剥掉、每一站看得到什么，都由这个顺序决定。文字写得再仔细，读者仍需在脑中自行补上数据包移动的过程，每个人补出来的版本未必相同。

规模更难传达。「近万台中继，高度集中在少数国家」是一句读过即忘的叙述，把每一台实际标到地球上，北美与西欧连成一片光带，其余地区只有零星几点。同一份数字换成画面，读者不必仰赖我们的形容词，可以自行判断。

## 地球仪用到的六份数据

| 数据 | 来源 | 许可 |
|------|------|------|
| 中继分布 | [Onionoo](https://metrics.torproject.org/onionoo.html) | CC0 1.0 |
| 用户与网桥人数 | [Tor Metrics](https://metrics.torproject.org/) | CC0 1.0 |
| 连接受阻的观测 | [OONI](https://ooni.org/) | CC BY-NC-SA 4.0 |
| 断网事件 | [Access Now KeepItOn](https://www.accessnow.org/keepiton-data-dashboard/) | CC BY 4.0 |
| 海底电缆 | [OpenStreetMap](https://www.openstreetmap.org/copyright) 贡献者 | ODbL 1.0 |
| 国界与海岸线 | [Natural Earth](https://www.naturalearthdata.com/) | public domain |

Onionoo 的中继快照经过蒸馏，只保留国家层级的聚合，不含 fingerprint、nickname、IP 或联系信息。ASN 的登记名称另外过滤过，因为个人申请的 AS 在 RIR 登记的是持有人本名。对在审查严格地区运营中继的人来说，公开这个名称，等于把中继的归属与身份证上的名字一起公开。

陆地亮度可以切换四种指标。中继台数最直观。共识权重（consensus weight）反映该国实际承担的流量比重，常与台数有明显落差。单一服务商集中度是最大一家托管商在该国的占比，数字越高，该国的匿名流量越依赖同一个机房持续运作与配合。用户估计是需求端的数字，跟前三个供给端指标并列时，两端的落差本身就是信息。

!!! info "2026-07-31 补上的三份数据"

    发表后地球仪又加入三份数据，许可检查的标准相同。

    | 数据 | 来源 | 许可 |
    |------|------|------|
    | 上网人口比例 | [World Bank](https://data.worldbank.org/indicator/IT.NET.USER.ZS) | CC BY 4.0 |
    | 台湾的上网人口比例 | [数位发展部 国家数位近用调查](https://moda.gov.tw/digital-affairs/digital-service/operations/208) | 政府资料开放授权条款-第1版 |
    | 海底地形 | [Natural Earth](https://www.naturalearthdata.com/) | public domain |

    上网人口比例当作分母使用。画面原本只呈现各国使用 Tor 的人数，这个数字很大一部分反映的是人口多寡。知道该国有多少比例的人上网，才能判断两国的落差是否只因为其中一国上网的人本来就少。

    World Bank 那份涵盖的 217 个经济体里没有台湾，对本站来说是个尴尬的缺口。台湾的数字改取自数位发展部的调查，两份的方法论不同，一份是 ITU 汇总各国通报，一份是对 12 岁以上人口的电话抽样，画面上注明不宜直接比较。缺口来自数据政治，跟前面的许可限制不同类，结果同样由下游的用户承担。

    海底地形跟国界同源，没有新的许可要处理。地球仪取 200、1000、3000、5000 米四层等深线，最浅那一层就是大陆架。加上海底地形之后，海缆那一层才有解释力。海缆几乎都沿着陆架铺设、避开深海盆，两层对照可以看出缆线走那些路径的原因。

    顺着海缆又查了登陆点，登陆点是整条缆线最脆弱的位置，台湾的几处尤其受到关注。OpenStreetMap 本身没有收录这份数据，用 taginfo 查全球数量，`man_made=cable_landing_point`、`seamark:type=landing_point` 等五个候选标签都是 `0` 笔。登陆点坐标跟缆线几何一样是 TeleGeography 商品的一部分，受阻在同一道条款（2026-10 补注：之后地球仪以数位发展部公开的海缆清单为骨干，逐点交叉查证坐标，自建了台湾 14 处登陆点的数据集，细节见 [Tor 中继地球仪](docs:games/tor-network/)的说明页）。

## 刻意克制的呈现

OONI 的数据最能说明我们的取舍。OONI 提供各国 Tor 测试的异常率（anomaly rate），数字看起来足以画一张全球审查地图，中段却是测量噪声。实测瑞士 `22.2%`、加拿大 `21.2%`、新西兰 `41.1%`，这些国家都没有审查疑虑。把中段画成色阶，等于用噪声指控特定国家。

画面最后只标示异常率达 `85%` 以上且样本足够的少数国家，中段数值一律不上色，措辞也停在「没有照预期完成」。`85%` 这个门槛没有推导公式，是看过分布之后订的。噪声最高落在四成上下，拉到 `85%` 才留出足够的距离，我们宁可漏掉几个真的受阻的国家，也不要把没问题的国家标红。

Access Now 的断网事件则相反，每一笔都经过人工查证、成因清楚，可以明确标示此处发生过人为断网。武装冲突与族群冲突造成的中断未必出自政府决策，可能是战事破坏了基础设施，画面上与信息管制类分开说明。

基于同样的理由，我们放弃了 V-Dem 的数字社会指标。V-Dem 的许可在技术上可用，但数据是每个国家每年由约五位专家评分，再经统计模型转成连续量表。把专家评分画成地图色块，等于用我们的画面替某个机构的政治判断背书。

## 无法使用的数据

### 海底电缆

一开始想用领域内最权威的 [TeleGeography](https://www.submarinecablemap.com/) Submarine Cable Map，查下去才发现坐标数据已经是 TeleGeography 销售的正式商品。[License TeleGeography's Map Data](https://www2.telegeography.com/license-geocoded-map-data) 采用年费许可，GeoJSON 经 Amazon S3 或 API 交付、每次更新自动推送，GeoJSON 就是商品本体。

台湾的[海缆动态地图](https://smc.peering.tw/)在许可不明朗时采取了务实的做法。代码以 MIT 许可开源，几何数据放在另一个对外返回 404 的 repo，主 repo 的 README 直接写「You can leave the folder empty」。

地球仪上的海缆最后取自 OpenStreetMap 贡献者标注的路径，共 `228` 段，以欧洲、地中海与大西洋较完整，太平洋中段几乎是空的。OSM 社区 [2011 年的讨论帖](https://lists.openstreetmap.org/pipermail/talk/2011-October/060415.html)里，有人提议把 TeleGeography 的数据并进 OSM。社区成员判断那份许可禁止商业使用与改作，跟 ODbL 不兼容，提议之后没有下文。十五年后，太平洋中段仍然是空的。

### 网络基础设施

网络基础设施这一类查了一轮，几乎全部受阻，理由也相近。

[RIPE Atlas](https://atlas.ripe.net/) 部署在各地的测量节点（probe）数据质量很好，`2026` 年 7 月查询时全球有近六万个节点，含经纬度与 ASN，API 可以直接取得。服务条款则写明商业使用需另外取得 RIPE NCC 许可，也没有开放许可声明。PeeringDB 的 API 同样可以访问，可接受使用政策则写明不可批量转分发给第三方。Packet Clearing House 的 IXP 目录是 CC BY-NC-SA 3.0，Cloudflare Radar 是 CC BY-NC 4.0，两者的非商业条款都会延伸到我们的内容上。

[IODA](https://ioda.inetintel.cc.gatech.edu/) 是其中最可惜的一份。IODA 以 BGP 路由撤除、主动探测与 darknet 流量异常检测各国的网络中断，属于实际测量，主题跟本站高度吻合。API 有返回数据，响应里却附上一行 `Copyright (c) 2021-2025 Georgia Tech Research Corporation. All Rights Reserved.`。

完全没有条款的数据是另一类。各 RIR 的 delegated stats 文件可以下载，开头只有免责声明，没有一个字提到许可。root-servers.org 的节点清单有 JSON 端点，整站找不到许可声明。没有声明不能解读成允许，又比明文禁止更难处理，因为连判断的依据都没有。

### 指数类数据

Freedom House 的 Freedom on the Net 与无国界记者（RSF）的新闻自由指数最常被引用，两份都无法使用。RSF 的许可是 CC BY-**ND**，禁止改作，转成 JSON 重新呈现就违反条款。Freedom House 的官方页面查不到许可声明，取得数据需要写信申请。

## 没有个别询问许可的原因

依开放数据圈的常规做法，读完条款之后会再去信询问一次，通常有机会取得非营利或研究用途的例外。上面这几个机构，我们刻意没有这么做。

制作地球仪想了解的，正是一个下游再利用者实际会遇到什么。如果每一份受阻的数据都靠个别协商解决，得到的会是几封友善的回信，无法回答开放数据圈对想接手的人有多友善。条款写成什么样子，就是绝大多数人实际遇到的样子。没有人脉、没有机构背景、只是想做点东西的人，看到的就是那一页条款，所以本文只记录条款本身。

## 开放 API 与开放数据的落差

我们原本以为困难会在技术面，结果多数端点都能访问、数据格式也干净，受阻的全在条款，开放 API 不等于开放数据。RIR、CAIDA、RIPE NCC、PeeringDB 这些机构的默认立场是可以看、可以研究，但不能批量搬走，跟 Tor Metrics、OONI、Natural Earth 的文化完全不同。完全没写许可的数据也算在内，实务上等同不可用。业界确实有很多工具在用这类文件，风险由用户各自承担，公开发布的文档站不能比照办理。

文档站的架构也不容许「应该没问题」的侥幸。文档站是静态网站，数据文件会直接发布出去，还会推上 IPFS。内容寻址的数据发出去就收不回来，镜像可能长期存在。

相对地，地球仪能够完成，很大程度是因为 Tor Project 把 Onionoo 与 Tor Metrics 都以 CC0 发布，Natural Earth 则属公有领域。当年可能只是一行设置，十几年后一个不相干的社区就能直接取用，不必写信谈许可，也不必担心哪天被要求下架。

OONI 的数据采用 CC BY-NC-SA 4.0，其中的相同方式分享（ShareAlike）跟网站的 CC BY 4.0 互不兼容。处理方式是让 `ooni.json` 保持独立的一份，内容不并进其他数据文件，画面上也只跟其他来源并列，让整体属于 CC 定义的「集合」，相同方式分享的范围停在那一份文件。`NOTICE` 已经写明这个前提，避免日后有人把 OONI 的字段并进中继快照，让整份衍生物落入相同方式分享的范围。

## 另外两件作品

[Tor 路由解谜](docs:games/onion-routing/)让读者自行挑选三个中继，组成 guard、middle、exit 路径，过程中要避开被监听的节点、把三跳分散到不同 ASN，遇到封锁则改走网桥。看着电路因为三跳挤在同一个 ASN 而失败，比读十次「要分散」更容易记住。

[Tor 连线流量](docs:games/onion-rendezvous/)用发光粒子呈现两种路径的差异。连接 .onion 服务时，双方各建一条三跳电路，在随机选出的会合点相遇。连接明网网站时，则是走三跳到出口后原路往返。

三件作品都以 three.js 在浏览器中运行，免安装，支持正体中文、简体中文与英文。源代码在 [anoni-net/docs](https://github.com/anoni-net/docs) 的 `docs/zh-TW/games/` 底下，没有构建流程，修改后保存、刷新即可看到结果。

有想法的话，欢迎到[社区](/join/)找我们一起参与制作。
