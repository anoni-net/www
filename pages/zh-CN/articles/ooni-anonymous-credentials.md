---
title: OONI Probe 匿名凭证系统的设计与实现
description: OONI 公告文章的翻译，介绍 OONI Probe 匿名凭证系统的需求、以 Rust 实现的凭证框架、凭证属性与提交测量的协议，以及与 Go 代码的整合方式，另补上 OONI 2025 年文献回顾里的设计脉络。
date: 2026-02-05
---

OONI 依靠全球志愿者上传网络审查的观测数据，参与的人越多，虚假数据或错误测量混入的机会也越大，数据库的可信度会跟着受影响。IP 封锁、账户登录或设备认证这类传统做法会暴露志愿者身份，与 OONI 保护隐私的承诺冲突。OONI 因此改用匿名凭证，以密码学验证一条测量来自符合条件的 OONI Probe，同时不揭露用户是谁、身在何处，也不让不同网络上的活动被关联起来。

!!! info ""

    本文翻译自 OONI 团队的 [Announcing OONI's New Anonymous Credential System](https://ooni.org/post/2025-announcing-ooni-new-anonymous-credential-system/)（2026-01-30），文中的「我们」指 OONI，脚注为译者补充。文末的[设计的演进脉络](#evolution)一节由 anoni.net 整理。

在先前的文章中，我们已说明[为什么 OONI 需要匿名凭证系统](https://ooni.org/post/2025-probe-security-without-identification/)，并整理了这类系统必须满足的[信息安全与隐私需求](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/)。核心挑战是 OONI 必须在不建立任何可能暴露用户身份、或造成跨网络追踪的标识符的前提下，仍能确认上传测量的可信度[^1]。

匿名凭证（anonymous credentials）是一种密码学机制，可以验证 OONI Probe 的某些属性（例如长期参与的程度或测量的数量），同时不暴露用户是谁、身在何处，也不把用户在不同网络上的活动关联起来。

## OONI 的需求

要符合 OONI 的威胁模型（threat model），凭证系统必须满足以下限制：

- **防止跨网络可关联性（cross-network linkability）**：只支持网络本地（network-local）的识别方式。
- **验证元数据（metadata）**：验证 `probe_age`、`measurement_count` 与封锁清单或信任状态（blocklist/trust status），但不揭露原始数值，也不破坏匿名性。
- **抵抗伪造与女巫攻击（Sybil attacks）**：让恶意者难以大量创建或操纵身份。
- **支持频繁、多次出示（multi-show presentations）**：OONI Probe 会持续上传测量数据。
- **避免缩小匿名集合（anonymity sets）**[^2]：即使在测量数据里加入更多元数据，也不让用户变得更容易被识别。

既有的凭证生态系统（例如以盲签名为基础、适合零知识证明的签名，或基于 SNARK 的构造）各自能满足其中一部分需求，但无法一次涵盖全部。OONI 尤其需要签发者本地验证（issuer-local verification）、高效率的范围证明（range proofs）、依网络而定的假名（network-dependent pseudonyms），以及凭证更新协议（credential update protocols）。在不做重大妥协的前提下，没有现成的方案能完整符合这些限制[^3]。

## 模块化、具表达力的凭证框架

我们与滑铁卢大学、Tor Project 与 Risc Zero 的研究者合作，建立了一套分层式系统，用来构造零知识凭证与相关协议。系统包含三个 Rust crate（`cmz`、`sigma-compiler`、`sigma-proofs`），实现经过充分研究的 sigma-protocols，并把高阶的陈述（statements）编译成高效率、以线性代数为核心的证明陈述。我们也在推动这些协议的 CFRG 草案（[draft-irtf-cfrg-sigma-protocols](https://datatracker.ietf.org/doc/draft-irtf-cfrg-sigma-protocols/)、[draft-irtf-cfrg-fiat-shamir](https://datatracker.ietf.org/doc/draft-irtf-cfrg-fiat-shamir/)）[^4]。

对 OONI 特别重要的功能有四项：

1. **可多次出示（multi-show）且签发者本地验证（issuer-local verification）**：OONI 的使用模式类似 KVAC 凭证（签发者与验证者是同一方），CMZ 与 μCMZ 方案可以直接支持。
2. **高效率的范围证明（range proofs）**：`probe_age` 与 `measurement_count` 需要以粗略的区间[^5]呈现（例如超过 1 周、超过 1000 条测量），避免形成近乎唯一的组合。sigma-rs 的技术栈可以用相对精简的方式支持范围证明。
3. **网络本地假名（network-local pseudonyms）**：OONI Probe 在每个网络只呈现一个身份，不同网络之间则要保持不可关联，可以直接对应到 sigma-rs 的属性与约束系统（例如 `pseudonym = secret * DOMAIN`）。
4. **签发与更新协议（issuance + update protocols）**：我们的模型需要出示旧凭证，在不揭露底层数值的情况下取得更新后的新凭证（例如 `measurement_count` 加一），与 UserAuth 示例描述的模式相同。

## OONI 的凭证结构

OONI 的匿名凭证包含以下属性：

``` rust
CMZ! { UserAuthCredential:
    nym_id, // a stable per-installation secret
    age, // coarse bucket
    measurement_count // measurements submitted
}
```

三个属性对应到需求文章描述的额外元数据，同时仍遵守匿名性的限制。

### 提交测量协议的概观

使用 sigma-rs 的 μCMZ API，提交新测量的协议在概念上写成：

``` rust
muCMZProtocol!(submit<min_age_today, max_age, min_measurement_count, max_measurement_count, @DOMAIN, @NYM>,
    Old: UserAuthCredential { nym_id: H, age: H, measurement_count: H},
    New: UserAuthCredential { nym_id: H, age: H, measurement_count: H},
    // the per-installation secret is the same
    Old.nym_id = New.nym_id,
    // the age is the same
    Old.age = New.age,
    // the new measurement count is increased
    New.measurement_count = Old.measurement_count + 1,
    // the submitted NYM is correct
    NYM = Old.nym_id * DOMAIN,
    // the age and measurement counts are within the desired range
    (min_age_today..=max_age).contains(Old.age),
    (min_measurement_count..=max_measurement_count).contains(Old.measurement_count) );
```

协议可以确保：

- OONI Probe 维持相同的网络本地假名
- `measurement_count` 单调递增（不会倒退，也无法跳号造假）
- 年龄分桶（age bucket）保持正确
- OONI 看不到原始数值，只能验证被证明的陈述
- 恶意的客户端无法伪造可信度元数据

服务器只会看到证明（proof）[^6]，看不到底层的属性值。

`measurement_count` 用来评估用户在该网络中的参与程度，不作为速率限制（rate limit）的依据。

## 与 OONI 代码库的整合

OONI Probe 引擎主要以 Go 编写，匿名凭证系统则以 Rust 实现。为了让两者的整合保持简单，我们在 Rust 端提供一个小型、兼容 C 的 API，再通过 rust2go 生成 Go 的绑定（bindings）。两边的职责清楚切分，Rust 负责所有密码学（凭证签发、零知识证明、验证、更新），客户端负责协调流程、持久化（persistence）与状态机（state machines）。

Rust 库是一个独立的加密引擎（crypto engine），接收不透明（opaque）的输入（当前的凭证与协议参数），生成要送给服务器的协议消息，再处理服务器的响应、返回更新后的凭证。所有状态管理刻意交给调用端的应用程序处理，让 API 维持精简、容易移植[^7]。调用端有两个：

- 移动设备上是 OONI 的跨平台客户端 [OONI probe-multiplatform](https://github.com/ooni/probe-multiplatform)
- 命令行上是 OONI 的 Go 客户端（miniooni、ooniprobe）[OONI probe-cli](https://github.com/ooni/probe-cli)

客户端负责存储与重新加载：

- 最新的凭证 blob
- 请求之间需要保留的本机状态（例如 request 与 response 之间尚未完成的协议状态）

边界因此维持清楚，Go 端把凭证与协议消息都当成不透明的 bytes，所有正确性与隐私性属性由 Rust 端在内部强制执行。

### 数据交换模型

Rust 与 Go 的边界之间只传递三种数据：

- **不透明的序列化协议消息**：bytes，为了以 JSON 传输通常会再做 Base64 编码。
- **公开参数（public parameters）**：例如签发者公钥、协议参数。
- **网络上下文（network context）**：domain separator、cc 与 asn 等。

Go 端因此不必重新实现密码学就能整合，网络通信与应用程序逻辑也能与 OONI Probe 的其他部分保持一致。

长期密钥（long term keys）交给操作系统的原生机制管理与存储，Android 使用 [Android Keystore](https://developer.android.com/privacy-and-security/keystore)，iOS 使用 [Keychain services](https://developer.apple.com/documentation/security/keychain-services)。

## 后续规划

OONI 的数据使用者很快就能依下列条件筛选或标注测量数据：

- 长期运行与新加入的 OONI Probe
- 测量量高的贡献者
- 被列入封锁清单（blocklisted）或故障的 OONI Probe
- 受信任的机构型 OONI Probe

完整抵抗女巫攻击（创建大量虚假账户）仍是应用层的问题，例如注册阶段的速率限制。经过验证的 `measurement_count` 与 `probe_age` 分桶，仍能对潜在的攻击者形成实质的阻力。

我们欢迎密码学研究者、实现者与任何感兴趣的人提供反馈，希望这项工作能以安全、透明的方式服务全球的 OONI 社区。之后我们会进一步分享协议的设计细节、性能基准测试，以及 sigma-rs 如何随下一个 OONI Probe 主要版本一起发布。

（2026-10 补注：OONI 在 2026 年 7 月的工程文章里评估了这套系统的成效，文中提到系统正逐步导入生产环境，每条测量会标成 verified、unverified 或 failed，导读见 [OONI 错误测量的识别方法与匿名凭证](/articles/ooni-faulty-measurements/)。）

## 设计的演进脉络 {#evolution}

OONI 在 2025 年 2 月发表 [Probe Security Without Identification](https://ooni.org/post/2025-probe-security-without-identification/)，是规划这套系统时的文献回顾，以下由 anoni.net 整理其中仍有参考价值的背景。

当时设想的威胁分成两种。恶意者在同一个网络、针对少数网站、短时间内上传假数据，集中的模式相对容易识别。较高阶的对手从多个网络、针对多个网址，长时间分散上传少量假数据，就难以检测。攻击的目的可能是让外界质疑 OONI 平台的可信度，或散布某个国家、地区审查状况的误导信息，例如宣称被封锁的网站没有被封锁，或反过来。错误测量也可能来自 OONI Probe 安装错误，不一定出于恶意。OONI 同时重视用户在网络层与应用层的隐私，用户也可以通过 Tor 这类工具上传测量。系统要在 `checkIn` 与 `upload` 两段流程里建立信任，并能扩展到每秒数百次的验证。

文献回顾把匿名凭证分成两个维度。依验证方式分，密钥验证凭证（KVAC）由同一方签发与验证，使用较轻量的密码学，Signal 是采用者之一，公开验证凭证则让签发者与验证者可以是不同的单位。依出示次数分，单次使用的凭证（例如盲签名，或 IETF Privacy Pass 标准采用的 VOPRF）出示一次就失效，多次出示的凭证则有 Camenisch–Lysyanskaya、Chase–Meiklejohn–Zaverucha（CMZ）与 BBS 等方案，其中 CMZ 用在 Signal 的私密群组与 Tor 的网桥分发。OONI Probe 会反复上传测量，一次发放一批单次令牌虽然可行，应用层就得自行管理令牌的库存与补发，效率不如专为多次出示设计的方案。文中也列出有效期限、网络相关身份、撤销、范围证明等可以独立于基础方案加上的扩展功能。

2026 年的实现选了密钥验证的 CMZ 与 μCMZ，由 OONI 同时担任签发者与验证者，并采用文献回顾列出的范围证明与网络相关身份两项扩展，与 2025 年的方向一致。

## 相关阅读

- [OONI 错误测量的识别方法与匿名凭证](/articles/ooni-faulty-measurements/)
- [零知识身份验证与支付](/articles/zk-identity-payments/)
- [什么是 OONI](docs:tools/what-is-ooni/)
- [Requirements for OONI's anonymous credentials](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/)

[^1]: 服务器需要分辨测量是否来自符合某些条件的 OONI Probe，同时又不能让测量带有可长期追踪的固定身份。跨网络追踪的风险在于同一个用户在不同网络（例如家用 Wi‑Fi、公司网络、移动网络）都被认出是同一人，就可能被用来推回真实身份或行为轨迹。
[^2]: 匿名集合可以理解为看起来都一样的一群人。附带的元数据太细（例如精确的年龄、精确的条数），很容易形成近乎唯一的组合，反而削弱匿名性。OONI 想验证的是用户符合某个范围或条件，不需要知道精确的数值。
[^3]: 在 OONI 的使用情境下，issuer-local verification 通常代表签发者（issuer）同时也是验证者（verifier），由 OONI 自己签发与验证，不把验证交给第三方。范围证明是用零知识的方式证明某个值落在某个区间内（例如大于 1 周、超过 1000 条），但不透露精确数值。
[^4]: CFRG（Crypto Forum Research Group）是 IRTF 下属的密码学研究论坛，草案通常会朝标准化方向前进。Fiat–Shamir 是把交互式证明（需要来回的挑战与响应）转成非交互式证明的常见技巧，客户端可以一次送出证明给服务器验证。
[^5]: 刻意用粗略的区间取代精确数值，是为了避免用户的特征过于独特（例如 17,382 条测量加上 39 天），导致容易被追踪。每个网络一个身份，通常是通过与网络相关的 domain separator，把同一个安装的秘密值映射到不同的假名，达成跨网络不可关联。
[^6]: 这段协议同时涵盖出示旧凭证与取得新凭证（更新），服务器可以验证计数确实加一，但不会知道原本的精确计数。`@DOMAIN` 与 `NYM` 用来做 domain separation（避免跨情境重用导致可关联），让同一个安装在不同网络产生不同的假名。
[^7]: 关键的设计是边界清楚，Go 端不碰密码学细节，只把它当成黑盒（opaque bytes）使用，密码学的正确性与隐私性由 Rust 端封装保证。通过 C ABI 再生成 Go binding 是常见的跨语言整合方式，也能降低在 Go 端重写密码学而出错的风险。
