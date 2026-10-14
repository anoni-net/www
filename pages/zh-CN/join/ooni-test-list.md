---
title: OONI 网站检测清单的维护
description: OONI Probe 检测网站时依据的 Citizen Lab 清单，包含收录分类、OONI 依分类安排检测频率的方式、台湾 tw.csv 的现况与参与维护的方式。
---

OONI Probe 执行网站连接测试时，按照一份事先列好的网址清单逐一检查。清单收录哪些网站、分类是否正确、多久更新一次，决定了后续的观测能看到什么，[ASN 多样性](/projects/asn-coverage/asn-diversity/)这类分析也受同样的限制。清单过时的国家看起来像没有审查，原因可能只是会被封锁的网站没有人测。台湾的清单需要重新整理，维护工作不必写代码。

清单由 [Citizen Lab](https://citizenlab.ca/) 的 [test-lists](https://github.com/citizenlab/test-lists) 项目管理，分成全球（global）与各国（local）两种。全球清单以英文网站为主。各国清单由当地社区协助搜集，收录当地语言的网站与当地关注的主题，有网络审查的国家也会收录已知被封锁的网站，方便持续观测。

收录标准粗分为四大主题（CSV 里实际用约 30 个细项分类标记）：

1. **政治**：与现任政府立场不同的网站，也包含人权、言论自由、少数族群权利、宗教运动等延伸主题。
2. **社会**：性别、赌博、非法药物、酒精，以及其他在当地被视为敏感的议题。
3. **冲突与安全**：武装冲突、边界争议、分裂运动、激进团体相关的内容。
4. **互联网工具**：电子邮件、云存储、搜索、翻译、网络电话（VoIP）、规避审查工具等服务。

## 分类与检测频率

四大分类除了整理用途，也决定每个网址被测到的频率。OONI Probe 取得的清单是 OONI API 排序过的结果，并非直接读取 CSV。排序逻辑写在 [`prio.py`](https://github.com/ooni/backend/blob/master/api/ooniapi/prio.py)，分两段计算。

第一段算出每个网址的优先级（priority）。OONI 维护一组规则，每条规则有四个比对字段：分类、域名、完整网址、国家代码，`*` 代表不限。命中的规则全部相加，不互相取代。全局默认规则 `*/*/*/*` 给 50，分类规则再叠加上去。归在新闻媒体（`NEWS`）的网址优先级因此是 `50 + 100 = 150`，归在电子商务（`COMM`）的是 `50 + 20 = 70`。

目前的分类加权（实际优先级是加上基底 50 之后的值）：

| 加权 | 分类 | 实际优先级 |
|---:|---|---:|
| +120 | `GRP` 社交网络 | 170 |
| +100 | `ANON` 匿名与规避工具、`HUMR` 人权、`LGBT`、`NEWS` 新闻媒体、`POLR` 政治批评 | 150 |
| +80 | `COMT` 通讯工具、`MMED` 媒体分享、`PUBH` 公共卫生、`SRCH` 搜索引擎 | 130 |
| +60 | `ENV` 环境、`HOST` 主机与博客、`REL` 宗教、`XED` 性教育 | 110 |
| +40 | `CULTR` 文化、`FILE` 文件分享、`GOVT` 政府、`IGO` 国际组织 | 90 |
| +30 | `ALDR` 酒精与药物、`DATE` 交友、`GMB` 赌博、`HATE` 仇恨言论、`MILX` 武装团体、`PORN`、`PROV` 暴露服饰 | 80 |
| +20 | `COMM` 电子商务、`CTRL` 内容管控、`ECON` 经济、`GAME` 游戏、`HACK` 黑客工具、`MISC` 未分类 | 70 |

社交平台与言论类的加权最高，商业与娱乐最低，两端相差 2.4 倍，有落差但不到一个数量级。

第二段把优先级除以近期的测量次数，得到实际的排序键：

```
weight = priority / max(msmt_cnt, 0.1)
```

`msmt_cnt` 是该网址在本周与上周被测量的次数，范围限定在同一个国家，probe 有回报 ASN 时则限定在同一个 ASN。测得越多，权重下降得越快，网址往后排，其他网址随之往前。

排序会随测量次数变动，优先级决定一个网址能分到多少检测，测量次数决定已经用掉多少。加权高的分类换来的是测过之后较快排回前面，并非永远占住前排。

## 突发事件的专属规则

规则表除了分类加权，还有两种用法。第一种是把单一目标推到清单最前面，截至 2026-09 的设置如下：

| 目标 | 范围 | 优先级 |
|---|---|---:|
| `www.aljazeera.net` | 以色列 | `9999999` |
| `orda.kz` | 哈萨克斯坦 | `99999` |
| `eltoque.com` | 古巴 | `6969` |
| Twitter、Facebook、Instagram、YouTube 四个网址 | 全球 | `69999` |

优先级远高于分类加权的量级，目标因此在清单里几乎固定排在第一位，通常对应正在发生或刚发生的封锁事件。

第二种是把优先级设成负值来排除网址，程序遇到优先级小于等于零的项目直接跳过，不发给 probe。目前唯一的一组负值规则在阿富汗，把酒精与药物、交友、赌博、仇恨言论、`LGBT`、武装团体、`PORN`、性教育八个分类设为 `-9999`，用意是保护执行测量的人，避免网络记录里出现在当地可能带来危险的内容。

同一份规则表里没有台湾的国家层级规则，`tw.csv` 每一条的优先级都只有「50 加上分类加权」，分类因此是唯一能影响检测频率的字段。归错分类不会出现任何错误信息，只会让网址被测得比应有的频率少或多。提交清单修正时，分类判断的价值跟找到一个值得收录的网站一样大。

完整规则表可以从 OONI API 的 [`url-priorities/list`](https://api.ooni.io/api/_/url-priorities/list) 端点查询，设计背景见 OONI 的 [Building a smart URL list system](https://ooni.org/post/ooni-smart-url-list-system/)。

## tw.csv 的现况

台湾的清单 [`tw.csv`](https://github.com/citizenlab/test-lists/blob/master/lists/tw.csv) 共有 466 条，其中 361 条在 2017 年加入，之后多年缺乏维护。不少网站已停止运营或换了网址，也有 245 条仍以 `http://` 开头（2026-10 查核）。

!!! note "http:// 与 https://"

    有些网站不会用 [`301 Moved Permanently`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/301) 或 [`308 Permanent Redirect`](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/308) 把 `http://` 重定向到 `https://`，造成 OONI 检测误判。TLS 证书现在容易取得，加密传输也是网站的基本配备，清单上的网址应该默认使用 `https://`。

## 既有条目的检查

第一步是逐一检查 [`tw.csv`](https://github.com/citizenlab/test-lists/blob/master/lists/tw.csv) 上的网站，标记「需更新」或「可弃用」，再提交 pull request 到 [citizenlab/test-lists](https://github.com/citizenlab/test-lists)。同样的检查方式也适用于其他国家的 `lists/<国家代码>.csv`。

!!! info "PR #1444 与之后的做法"

    社区在 2023-09-28 提交过一份[检测名单修正](https://github.com/citizenlab/test-lists/pull/1444)，一次改动约 100 个国家的清单文件，难以审查。PR #1444 在 2026-09 关闭，没有合并。之后的 PR 只改 `lists/tw.csv`，每次的范围缩小到可以单独审查，逐条确认失效网址与 `http://` 网址。网站换了域名的，优先修改网址，不直接删除。

## 新增网站

2017 年之后规模最大的一次新增在 2026-09，[PR #2267](https://github.com/citizenlab/test-lists/pull/2267) 补上 74 个台湾的网站并已合并，其中政治批评（`POLR`）的 20 条最多。新增的候选依前面的四大分类筛选，筛选标准社区还在持续讨论。

## 参与方式

清单维护适合新贡献者入门，不需要写代码，需要的是：

- **网络用户的观察力**：哪些网站在台湾被讨论、哪些近期关闭、哪些是新出现值得纳入的对象
- **判断分类的能力**：对照四大分类与细项分类归类
- **基本的 GitHub 操作**：fork、修改 CSV、提交 PR

依想参与的部分，从下列页面开始：

- 清单维护：到 Matrix 的 anoni-net 公开空间表达意愿，会有伙伴协助分配要检查的范围（加入方式见[参与](/join/)）
- 观测数据的分析：[ASN 多样性与台湾的观测缺口](/projects/asn-coverage/asn-diversity/)、[ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)
- 测量数据的判读：[OONI 测量数据的结构](/projects/asn-coverage/ooni-data-format/)、[OONI 的封锁判定方式](/projects/asn-coverage/ooni-blocking-determination/)
- 清单以外的测项：[OONI 测项速查表](/projects/asn-coverage/ooni-nettests-map/)

## 相关阅读

- [参与开发的环境准备](/join/dev-setup/)：运行社区的分析工具前需要的开发环境
- [Tor 中继节点观测](/projects/pulse/)：社区的另一个观测项目，每小时收集台湾与邻近地区的 Tor 中继节点数据
- [什么是 OONI](docs:tools/what-is-ooni/)：OONI 的运作方式，以及适合与不适合的用途
- [网络自由为什么重要](docs:basics/internet-freedom/)：网络审查与网络自由的背景
