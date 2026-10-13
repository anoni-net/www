---
title: Tor 系统管理团队的 ADR 决策记录
description: Tor 系统管理团队（TPA）从 RFC 改用 ADR 的全文翻译，附上其他开源项目的提案与决策流程对照，以及台湾项目与社区的决策记录现状。
date: 2026-03-19
---

!!! info ""

    本文翻译自 Tor Project 博客的 [Keeping track of decisions using the ADR model](https://blog.torproject.org/tpa-adr/)（2026-02-16），文中的「我们」是 Tor Project 的系统管理团队 TPA。文末的「社区补充」一节由 anoni.net 撰写，对照其他开源项目的做法与台湾的现状。

在 Tor Project 的系统管理团队（俗称 TPA）里，我们最近改变了做决策的方式。之后无论是即将进行的变更，还是针对某项提案的具体问题，你从我们这边收到的沟通都会更清楚。

新流程只影响 TPA 团队，Tor 内部每个团队都有自己协调与决策的方式。我们鼓励 Tor 内外的其他团队评估一下，看能否改善你们的流程与文档。

## 新流程

我们过去一直使用 RFC（Request For Comments，请求意见）流程，最近改为 ADR（Architecture Decision Record，架构决策记录）。

对我们来说，ADR 流程相当简单，包含三件事：

1. 更精简的模板
2. 更精简的流程
3. 与决策记录分开的沟通准则

### 模板

作为团队负责人，我做的第一件事是提出新模板（见 [ADR-100](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/0100-adr-template)），它是 [Nygard 模板](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md)的变体。[TPA 版本的模板](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/template)同样简洁，只有 5 个标题，值得完整引用：

- **Context（背景）**：我们看到什么问题，促使我们做这项决策或变更？
- **Decision（决策）**：我们提议或正在进行的变更是什么？
- **Consequences（后果）**：变更之后，哪些事变得更容易或更困难？
- **More Information（更多信息，选填）**：还有什么我们该知道的？较大的项目可以考虑纳入时间表、成本估算，以及对受影响用户的冲击（或许包含既有的 Personas）。一般会在这里简短评估考虑过的替代方案。
- **Metadata（元数据）**：状态、决策日期、决策者、被咨询者、需被告知的用户，以及讨论区的链接。

[先前的 RFC 模板](https://gitlab.torproject.org/tpo/tpa/wiki-replica/-/blob/d52de1828d3ee406996345704d12663dd30f5513/policy/template.md)有 **17** 个标题，容易写成很长的文档。现在的决策记录一眼就能读完。

改用新模板之后，我更常把比较与头脑风暴放进 GitLab 的 issue。定价、替代方案的深入比较这类细节，改记在讨论用的 issue 里，文档本身保持精简。

### 流程

整个流程简单到也值得完整引用：

> 重大决策在会议中向利益相关方说明，较小的决策则用电子邮件。采纳之前保留一段时间，让大家提出最后的意见。

细节都写在 [ADR-101](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/0101-adr-process)，重点是保持简单。

提案的关键之一，是 Jacob Kaplan-Moss 称为 [one weird trick](https://jacobian.org/2023/dec/5/how-to-decide/) 的「先决定谁做决定」。我们过去的流程对谁来做决策交代得很模糊，新的模板与流程在每项决策上都写明决策者。

相对地，被咨询的利益相关方太多时，有些决策会变成在琐碎议题上没完没了的讨论，也就是[琐碎法则](https://en.wikipedia.org/wiki/Bike_shedding)（Law of triviality），又称自行车棚效应（Bike Shed syndrome）。

新流程把利益相关方分得更清楚：

- **需被告知者**（informed）：以前叫「受影响用户」
- **被咨询者**（consulted）：以前没有定义
- **决策者**（decision maker）：取代含糊的「核准」

要挑出这些利益相关方仍然不容易，但定义更明确了，也与经典的 [RACI 矩阵](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix)（Responsible, Accountable, Consulted, Informed）一致。

### 沟通准则

流程中很重要的一环（[ADR-102](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/0102-adr-communications)），是把做决策、记录决策与对外沟通决策拆开。两者要解决的问题截然不同，我们发现一份文档无法同时兼顾。

ADR 可能影响的范围很广，所以我们没有为沟通定固定的模板，只建议用[五何法](https://en.wikipedia.org/wiki/Five_Ws)（Five Ws，谁、什么、何时、哪里、为什么），一样保持简单。

## 改变的缘由

[ADR 流程](https://adr.github.io/)不是我发明的，我最早是在 [Thunderbird Android 项目](https://github.com/thunderbird/thunderbird-android/blob/be2af5c6a0bce08385fc3f654c1185ccf9db3859/docs/architecture/adr/README.md)看到它。同一段时间，我正在检讨 RFC 流程（见[讨论 issue](https://gitlab.torproject.org/tpo/tpa/team/-/issues/41428)），也读了 Jacob Kaplan-Moss 对 [RFC 流程的批评](https://jacobian.org/2023/dec/1/against-rfcs/)。他的论点大致是：

1. RFC 流程「没有包含任何决策框架」
2. 「RFC 流程容易导致无止境的讨论」
3. 流程「奖励能写到让人精疲力竭的人」
4. 「这些流程对专业不敏感」，对「权力动态与权力结构」也不敏感

上述问题我很多都犯过。我写东西很啰唆，写过[极长的提案](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy/tpa-rfc-33-monitoring)，我怀疑从来没有人从头读完。有些提案是大家累到放弃才通过的，有些则因为没找对利益相关方而被忽略。

我们的 RFC 流程有哪些问题，[讨论 issue](https://gitlab.torproject.org/tpo/tpa/team/-/issues/41428) 里有更多细节。公平地说，旧流程在当时还是有用的，有总比没有好，6 年间也记录了数量可观的变更与决策（[95 份 RFC](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/policy)）。

## 后续的实验

如何沟通决策，我们仍在实验，本文或许就是一例。沟通是独立的一步，所以容易被遗忘或拖延，本文就晚了好几个月才发出。

以前我们直接把 RFC 副本寄给大家，又快又简单，但多数人读不懂。现在需要另外写一份沟通稿，工作量变多，希望换来的结果更容易消化。

欢迎在原文底下或[讨论 issue](https://gitlab.torproject.org/tpo/tpa/team/-/issues/41428) 告诉我们你对新流程的想法，以及它在你那边的效果。我们特别想听已经在用类似流程的人，或读完本文之后打算采用的人的经验。

!!! note "重点整理"

    TPA 过去用 RFC 记录决策，6 年累积了 95 份。RFC 流程缺乏决策框架，讨论容易拖长，也奖励写得多的人，对专业与权力结构不敏感，结果文档难读，谁有权拍板也不清楚。

    改用 ADR 之后有三项变化。模板从 17 个标题缩成 5 个，比较与估价移到 GitLab issue。每项决策写明决策者、被咨询者、需被告知者，对齐 RACI，避免没人拍板，也避免太多人卷入琐事。ADR 只负责记录决策，对外公告另写一份。

## 社区补充

以下两节由 anoni.net 撰写，不属于原文。

### 其他开源项目的提案与决策流程

各项目提出提案、记录决策的方式不尽相同，几个常见的做法如下：

- **GOV.UK Design System**：用 RFC 讨论提案、用 ADR 记录最终决策，两者并行。提案放在公开的仓库，第一份就是 [001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions](https://github.com/alphagov/govuk-design-system-architecture/blob/main/proposals/001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions.md)。
- **Bitwarden**：在贡献者文档里维护 [ADR 索引](https://contributing.bitwarden.com/architecture/adr/)，以 ADR 为主要的架构决策记录。
- **GitLab**：Delivery 团队在公开的 handbook 维护 ADR，收在 [Delivery Decisions](https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/gitlab-delivery/decisions/)（2026-10 核查）。
- **ADR 社区与 MADR**：[adr.github.io](https://adr.github.io/) 提供 MADR（Markdown Architectural Decision Records）模板与工具，通用且轻量，许多项目采用。
- **Rust**：语言与标准库的变更走 [rust-lang/rfcs](https://github.com/rust-lang/rfcs) 的 RFC 流程，提案编号、公开讨论，决策结果留在同一个仓库。
- **Python**：语言与标准库的变更以 [PEP](https://peps.python.org/)（Python Enhancement Proposal）作为正式的提案与编号制度。
- **Kubernetes**：功能与架构变更以 [KEP](https://github.com/kubernetes/enhancements)（Kubernetes Enhancement Proposal）提案与讨论。

GOV.UK 让 RFC 讨论与 ADR 记录并行，Bitwarden 与 TPA 以 ADR 为主，大型生态系统则多半用编号提案（RFC、PEP、KEP）。TPA 的做法有两点与众不同，一是明确「先决定谁做决定」，二是把决策记录与对外沟通分开处理。

### 台湾项目与社区的现状

台湾多数的项目与社区已经有提案、讨论、取得共识的流程，只是不一定用 ADR 这个名称，也较少把决策文档放在 `adr/` 目录或用 MADR 模板公开。

- **公民科技社区（例如 g0v）**：常见做法是提案文档、[HackMD 协作文档](https://g0v.hackmd.io/@jothon/intro)、黑客松或线上会议讨论（见 [g0v 开源协作手册](https://g0v.hackmd.io/@jothon/g0v-cowork-guideline/)）。架构层级的关键决策分散在协作文档、issue、PR、演示文稿与大松提案里，过一段时间就不容易追溯当初的理由。
- **政府与公共部门的合作项目**：多半有规格书、系统设计文档或项目报告，形式接近在里程碑一次写完的大文档，不会随时间累积成 ADR log，而且通常不完全公开，外部贡献者看不到背后的取舍。
- **企业的开源项目**：有些团队在公司内部用决策记录或设计文档管理架构变更，但只留在内部的运维知识库，公开的只有代码，看不到决策历史。

上述项目缺少的是稳定、容易追溯、外部的人也读得懂的决策记录。ADR 让每个重要决定各自写成一份小文件，记下当时的理由，不必硬写一大本规格书，也比只留在 issue 里容易长期维护。新加入的人读过 ADR，就知道系统为什么是现在的样子，不必重复同样的讨论。

anoni.net 的[治理章程](/about/governance/)（草案）在「决策方式」一节用一张表，依影响范围列出提案渠道与决策方式，例如结构性变动先在 Matrix 讨论再提交 PR，保留 3 天缓冲，自架服务的政策变更由核心成员以共识决定。章程的表格回答了「谁做决定」，但没有规定决定之后要留下什么样的记录，ADR 的单文件模板可以补上记录的部分。
