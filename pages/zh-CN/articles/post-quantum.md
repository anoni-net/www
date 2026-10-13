---
title: 后量子密码概观
description: NIST 后量子标准 ML-KEM、ML-DSA、SLH-DSA 的选型，「现在收集、未来解密」的威胁模型，以及浏览器、云服务、通信协议、SSH 与各地金融监管的迁移进度。
date: 2026-05-01
---

后量子密码（Post-Quantum Cryptography，PQC）要回答三个问题：现有的公钥密码学是否会在未来十年内被量子计算机攻破、何时发生、哪些算法要先迁移。能实际攻破 RSA 与椭圆曲线的大型量子计算机还没有出现，但攻击者可以先把密文存起来，等量子计算机成熟再解密，迁移因此不能等到那一天。NIST 已经发布第一批后量子标准，浏览器、TLS 库与 Signal Protocol 都已陆续导入。

## Harvest Now, Decrypt Later 威胁模型

「现在收集、未来解密」（Harvest Now, Decrypt Later，HNDL）是后量子迁移的主要动机。攻击者今天录下加密通信并存档，等日后取得大型量子计算机，再用 Shor 算法（在量子计算机上能高效地分解大数与计算离散对数）破解当时的密钥交换，还原所有录下的密文。

以下几种情况的风险最高：

- **数据的长期价值高**：政府机密、医疗记录、商业情报、长期有效的身份数据（身份证号、护照号码）。
- **攻击者有存储能力**：国家级情报机构（NSA 的 Bluffdale 数据中心、中国的情报单位）长期被外界推测在收集这类数据。
- **密文无法收回**：今天传出去的密文一旦被录下，就无法重新加密，未来被解密的风险会一直存在。

个人的即时聊天与短期的 session token 很快就失去价值，HNDL 风险低。银行的 KYC 文件、医疗影像、人权工作者的访谈记录，风险高。

NIST IR 8547 的初稿（2024-11 公开征求意见，截至 2026-10 尚未定稿）提出 2030 年起弃用旧的公钥算法、2035 年起全面禁用的时间表，ENISA 的路线图也以这两个年份为准，NSA 的 CNSA 2.0 另订 2030 与 2033 年的期限[^1]。新部署从现在起就应该规划 PQC 的迁移路径。

<figure markdown="span">
    <img class="brand-frame" src="https://assets.anoni.net/diagrams/pq-timeline.zh-TW.drawio.svg" alt="后量子密码迁移时程：从 2023 Signal PQXDH、2024 NIST FIPS 与主流浏览器启用、到 2030–2035 主要系统应完成迁移、2040 旧密码学硬时间表">
</figure>

## NIST 2024 年的三项标准

NIST 在 2016 年启动 PQC 标准化征集，2022 年选出第一批算法，2024 年 8 月发布 FIPS 203、204、205 三份正式标准。

### ML-KEM（FIPS 203），密钥封装

- 全称 Module-Lattice-based Key Encapsulation Mechanism，以格密码（lattice）为基础，量子计算机同样难以求解这类数学问题。
- 源自 CRYSTALS-Kyber。
- 用途：取代 RSA-OAEP 与 ECDH，在 TLS、SSH 与加密通信中负责密钥交换。
- 公钥大小依安全等级而定，ML-KEM-512 为 800 bytes、ML-KEM-768 为 1,184 bytes、ML-KEM-1024 为 1,568 bytes，都比 X25519 的 32 bytes 大。数据包略为变大，对一般连接速度没有明显影响，运算速度快，也容易用硬件加速。

### ML-DSA（FIPS 204），数字签名

- 全称 Module-Lattice-based Digital Signature Algorithm，源自 CRYSTALS-Dilithium。
- 用途：取代 RSA-PSS 与 ECDSA，用在证书、软件签名与区块链。
- 签名大小约 2.4–4.6 KB（依安全等级而定），ECDSA 只有 64 bytes。

### SLH-DSA（FIPS 205），哈希签名

- 全称 Stateless Hash-based Digital Signature Algorithm，源自 SPHINCS+。
- 用途：作为 ML-DSA 的备用方案，安全性只依赖哈希函数的抗碰撞性，数学假设最保守。
- 缺点是签名大（约 8–50 KB，依参数集而定）、签名速度慢，适合长期证书，不适合高频率签名。

NIST 第四轮继续评估以编码理论（code-based）为基础的算法，2025 年 3 月选定 HQC 作为 ML-KEM 的备用 KEM，正式标准预计 2027 年发布[^2][^3]。唯一以同源映射（isogeny）为基础的候选 SIKE 已在 2022 年被破解而退出。短期内业界部署的主流仍是 ML-KEM 搭配 ML-DSA。

## 2022–2025 年主要系统的部署进度

本节各项的状态在 2026-10 依各项目的官方文档与公告核查。

### 浏览器与 TLS

- **Chrome**：Chrome 124（2024-04）默认启用 Kyber 草案版本的混合密钥交换 X25519Kyber768Draft00，Chrome 131（2024-11）改用正式标准的 X25519MLKEM768[^4]。两者在 TLS 的码点不同、彼此不兼容，读 2024 年以前的报道时要留意。
- **Firefox**：Firefox 132（2024-10）加入 X25519MLKEM768（Firefox 称为 mlkem768x25519），桌面版默认启用，Android 版从 Firefox 145 起默认启用[^5]。
- **Safari**：iOS 26、iPadOS 26、macOS Tahoe 26 与 visionOS 26（2025-09）的 TLS 1.3 连接默认提出 X25519MLKEM768，服务器支持时就协商出混合密钥交换，Safari 等内置 App 也随这一版导入[^6][^7]。

混合（hybrid）指同时做传统 ECDH 与 ML-KEM 两次密钥交换，再把两个结果合并。万一 ML-KEM 日后被发现有漏洞，传统 ECDH 仍能提供保护，业界普遍采取这种保险做法。

### 云服务

- Cloudflare 从 2022-10 起让所有经由它提供的网站与 API 默认支持混合后量子密钥协商，当时用的是 Kyber 草案版本[^8]，现在改用 X25519MLKEM768[^5]。
- AWS 在 2025-04 让 KMS、ACM、Secrets Manager 的 TLS 端点支持 ML-KEM，客户端需要在 SDK 另外开启[^9]。
- Google Cloud 为企业客户提供 PQC 选项。

### Signal Protocol

Signal 在 2023 年发布 PQXDH（Post-Quantum Extended Diffie-Hellman），在建立会话的密钥协商中加入后量子密钥封装（初期用 CRYSTALS-Kyber，后升级至 ML-KEM），直接回应 HNDL 威胁。PQXDH 只保护会话建立时的密钥协商，Signal 在 2025-10 再加入 SPQR（Sparse Post-Quantum Ratchet），与既有的 Double Ratchet 合成 Triple Ratchet。会话进行中的前向保密（forward secrecy）与入侵后安全性（post-compromise security）因此也具备抗量子能力[^10]。既有会话会逐步改用新协议，用户不需要操作。Double Ratchet 的运作方式见[端对端加密的协议机制](/articles/e2ee-protocols/)。

### iMessage PQ3

Apple 在 iOS 17.4（2024-03）为 iMessage 导入 PQ3 协议，在消息的密钥交换中加入后量子算法[^7]。

### SSH 与 PGP

- OpenSSH 9.0（2022-04）把 sntrup761x25519 混合密钥交换设为默认，9.9（2024-09）加入以 ML-KEM 为基础的 mlkem768x25519-sha256，10.0（2025-04）改以它为默认，10.1（2025-10）在协商到非后量子算法时显示警告[^11]。
- age、Sequoia PGP 等较新的工具开始试验 PQC，传统的 GnuPG 进度较慢。

### 区块链与加密货币

- 比特币的 ECDSA 与 Schnorr 签名在大型量子计算机面前不安全，实际威胁取决于量子计算机出现的时间。
- 以太坊已有提案讨论后量子签名选项，短期内的优先级不高。
- Zcash、Monero 等隐私币的零知识证明系统同样面临后量子迁移的挑战。

## 个人与组织的迁移规划

Signal 与主流浏览器的迁移随软件更新自动完成，一般用户需要知道的部分整理在文档站的[端对端加密的保护范围](docs:basics/e2ee/)。Matrix 的 Olm 与 Megolm 截至 2026-10 还没有后量子机制，规范的讨论仍未结案[^12]。

需要主动规划的项目：

- **企业 PKI 与证书**：用于签名、认证与长期存证的证书，需要规划 ML-DSA 或 SLH-DSA 的迁移路径。CA/Browser Forum 已开始讨论 PQC 证书标准。
- **VPN 与 IPsec**：商用 VPN 对 PQC 的支持程度不一，企业网络规划时要纳入评估。
- **长期文件加密**：法务文件、医疗记录与研究数据要先确认十年后是否仍须保密，需要的话就改用 PQC 加密。
- **硬件安全模块（HSM）**：金融与医疗领域的 HSM 需要供应商提供 PQC 算法，更新周期长。

个人与一般组织现在不需要急着手动部署 PQC，可以先做的有三件：

- 采用会自动更新到 PQC 的工具，例如主流浏览器、Signal 与 Cloudflare。
- 盘点需要长期保密的数据，HNDL 风险高的先处理。
- 采购硬件与 SaaS 服务时，把 PQC 路线图纳入评估。

## 台湾、香港与新加坡的合规时间表

各地的监管时间表大致跟随 NIST 与 ENISA。以下状态在 2026-10 依主管机关的公告核查。

台湾的情况分三个领域：

- **政府与产业**：台湾数位发展部数位产业署在 2025-04 发布《后量子密码迁移指引》1.0 版，给产业参考的迁移步骤是拟定量子准备计划、盘点密码资产、与技术供应商讨论、确认供应链的准备程度[^13]。政府机关内部系统的迁移时间表目前没有查到公开资料。
- **金融**：台湾金融监督管理委员会在 2026-06 发布《金融业后量子密码迁移参考指引》，作为金融机构办理迁移的参考。指引分三个阶段，2026–2027 年建立治理架构、密码技术清册与加密敏捷性的基础，2027–2029 年推动试点验证与共同测试，至 2035 年优先完成高风险与高关键系统的迁移[^14]。
- **医疗**：电子病历与医疗影像需要长期保存（台湾《医疗法》规定病历至少保存 7 年，部分影像与追踪数据保存更久），HNDL 风险高，可能是台湾最早需要主动规划 PQC 的领域。

香港金融管理局（HKMA）在 2026-07 发布银行业量子准备白皮书与第一期量子准备指数（Quantum Preparedness Index），第一期分数是 2.3 分（满分 10 分），目标是 2030 年全行业达到 10 分[^15]。证券及期货事务监察委员会（SFC）是另一个相关的监管机关，病历等长期数据的保存规范也与台湾不同。

新加坡金融管理局（MAS）在 2024-02 向金融机构发布量子相关网络安全风险的建议（advisory），重点是提升加密敏捷性，属建议性质，没有订出迁移期限[^16]。

跨地区通用的判断仍是依循 NIST 与 ENISA 的时间表，先处理 HNDL 风险高的长期数据。

## 相关阅读

- [端对端加密的协议机制](/articles/e2ee-protocols/)
- [零知识身份验证与支付](/articles/zk-identity-payments/)
- [去中心化网站发布](/articles/dweb-ipfs-onion/)
- [威胁模型如何建立](docs:basics/threat-model/)
- [记者保护消息来源](docs:scenarios/journalist/)

[^1]: [NIST IR 8547: Transition to Post-Quantum Cryptography Standards](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf) - NIST
[^2]: [NIST IR 8545: Status Report on the Fourth Round of the PQC Standardization Process](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf) - NIST
[^3]: [NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption) - NIST
[^4]: [A new path for Kyber on the web](https://security.googleblog.com/2024/09/a-new-path-for-kyber-on-web.html) - Google Security Blog
[^5]: [Post-quantum cryptography support](https://developers.cloudflare.com/ssl/post-quantum-cryptography/pqc-support/) - Cloudflare
[^6]: [Prepare your network for quantum-secure encryption in TLS](https://support.apple.com/en-us/122756) - Apple
[^7]: [Get ahead with quantum-secure cryptography](https://developer.apple.com/videos/play/wwdc2025/314/) - Apple WWDC25
[^8]: [Post-quantum cryptography for all](https://blog.cloudflare.com/post-quantum-for-all/) - Cloudflare
[^9]: [ML-KEM post-quantum TLS now supported in AWS KMS, ACM, and Secrets Manager](https://aws.amazon.com/blogs/security/ml-kem-post-quantum-tls-now-supported-in-aws-kms-acm-and-secrets-manager/) - AWS
[^10]: [Signal Protocol and Post-Quantum Ratchets](https://signal.org/blog/spqr/) - Signal
[^11]: [OpenSSH Release Notes](https://www.openssh.org/releasenotes.html) - OpenSSH
[^12]: [Quantum-resistant crypto（matrix-org/matrix-spec#975）](https://github.com/matrix-org/matrix-spec/issues/975) - Matrix
[^13]: [數產署攜手後量子資安產業聯盟發布「後量子密碼遷移指引」](https://moda.gov.tw/ADI/news/latest-news/16090) - 台湾数位发展部数位产业署
[^14]: [金管會發布「金融業後量子密碼遷移參考指引」 引導金融機構強化量子風險整備](https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0%2C2&mcustomize=news_view.jsp&dataserno=202606180001&dtable=News) - 台湾金融监督管理委员会
[^15]: [HKMA launches quantum preparedness whitepaper and index to support banking sector's readiness for quantum era](https://www.hkma.gov.hk/eng/news-and-media/press-releases/2026/07/20260727-3/) - 香港金融管理局
[^16]: [Advisory on Addressing the Cybersecurity Risks Associated with Quantum](https://www.mas.gov.sg/regulation/circulars/advisory-on-addressing-the-cybersecurity-risks-associated-with-quantum) - 新加坡金融管理局
