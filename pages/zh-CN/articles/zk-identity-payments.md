---
title: 零知识身份验证与支付
description: Monero 的环签名与 RingCT、Zcash 的 zk-SNARKs 屏蔽交易、链上分析的能力与限制，以及零知识身份验证在私密 KYC、合规披露与匿名捐款的应用。
date: 2026-05-01
---

各条链提供的隐私程度差距很大，比特币的账本完全公开，任何人都可以查到每笔交易与每个地址的余额，Zcash 的屏蔽交易则连金额都看不见。多数设计落在两者之间，地址被混淆、金额被隐藏，交易图谱仍可被推测。Monero 与 Zcash 隐匿的层次不同，链上分析能追到的范围也跟着不同。合规要求不会因为链上隐私而消失，零知识证明可以把「证明自己合规」与「披露自己是谁」分开，零知识身份验证（zk-identity）在支付情境的应用就建立在这一点上。

本页是[匿名支付研究专题](/join/payments-research/)的技术背景。入门的说明见文档站的[加密货币的隐私光谱](docs:tools/crypto-privacy-spectrum/)与[为什么匿名支付重要](docs:basics/payments-anonymity/)。

## 链上隐私的可见度光谱

监控者观察一条链，可以看到四个层次：

1. **账户**（Account）：谁拥有哪个地址。比特币公开，Monero 用 stealth address 隐匿。
2. **金额**（Amount）：一笔交易转了多少。比特币公开，Monero 用 RingCT 隐匿，Zcash 屏蔽交易完全隐藏。
3. **交易图谱**（Transaction Graph）：A 与 B 之间的转账路径。比特币可以重建完整图谱，Monero 用 ring signatures 制造诱饵混淆，Zcash 屏蔽交易看不到图谱。
4. **元数据**（Metadata）：交易由哪个 IP、哪个钱包客户端、在什么时间点发出。所有链都依赖 P2P 网络层的隐私，搭配 Tor，或 Dandelion++ 这类打散交易广播路径、隐藏来源 IP 的协议。

注重隐私的加密货币多半只隐匿其中几层，四层全部隐匿的设计很少，Monero 与 Zcash 各自选了不同的组合。

## Monero 的环签名、Stealth Address 与 RingCT

Monero 的设计来自 2013 年的 CryptoNote 白皮书，核心是三个机制：

- **Stealth Address**：每笔交易生成新的一次性收款地址，链上看不到「Alice 的地址收了 100 元」，只看得到「某个一次性地址收了 100 元」。Alice 用自己的私钥可以识别哪些一次性地址属于她。
- **Ring Signatures**：发送方签署交易时，把真实签名混进从过去交易输出挑出的诱饵（decoys）之中。观察者只能确定「16 个输出之中有一个是真的」，无法确定是哪一个。Monero 目前默认的环大小为 16。
- **RingCT**（Ring Confidential Transactions）：用 Pedersen 同态承诺（不披露数字、仍可验算加总的加密承诺）隐藏金额，再以 Bulletproofs+ 范围证明确保每笔金额非负，整体证明输入总和等于输出总和，没有凭空增发。


三者组合起来，链上看到的是「某个一次性地址收到一笔隐藏金额，由 16 个可能的发送方之一发送」，没有 Alice 与 Bob 的概念。对照前面的四层，stealth address 遮盖账户层、RingCT 遮盖金额层、ring signatures 打散图谱层，第四层的元数据仍要靠 Tor 另外处理。

代价是区块链的体积较大、交易验证的计算量大，隐匿交易也难以满足 KYC（实名验证）的合规要求。要求 KYC 的交易所自 2021 年起陆续下架 Monero，2023 至 2024 年的下架规模最大，包括 Kraken 欧洲区、Binance、OKX[^1]。

## Zcash 的 zk-SNARKs 与屏蔽池

Zcash 走的路线更激进，屏蔽交易（shielded transaction）用 zk-SNARKs（Zero-Knowledge Succinct Non-Interactive Argument of Knowledge，可以证明「我知道某个秘密」而不泄露秘密内容的密码学工具）证明三件事：

- 我有花费这个 note 的权限。
- 我创建的新 note 金额总和等于消耗的 note 金额。
- 没有重复花费。

| 项目 | 链上 |
|---|---|
| zk-SNARK 证明 | 可见，证明交易有效 |
| nullifier | 可见，用来防止重复花费 |
| 新的 commitment | 可见，代表新建立的 note |
| 手续费 | 可见 |
| 发送方与接收方地址 | 不可见 |
| 金额 | 不可见 |
| 跟其他交易的关联 | 不可见 |

整个证明在链上只占几百 bytes，验证者不需要知道金额、地址与来源，链上能看到的只有发生了一笔屏蔽交易。对照四层，一笔屏蔽交易同时遮盖账户、金额、图谱三层，第四层的元数据同样留给网络层处理。

Zcash 经历过几代 zk-SNARKs：

- **Sprout**（2016）：用 BCTV14（PGHR13 的改良变体），需要可信设置（trusted setup）[^2]。
- **Sapling**（2018）：升级到 Groth16，可信设置的范围更小，性能也改善许多。
- **Halo 2**（2022 年 5 月随 NU5 升级启用）：不再需要可信设置。

Zcash 长期的问题在使用率，屏蔽池（shielded pool）的使用人数一度远少于透明池（transparent pool），多数交易仍是透明的。2025 年起屏蔽池的占比明显上升，但完全屏蔽的交易仍不是全部。没有足够的屏蔽流量提供混淆，密码学保证再好，被分析的风险仍在。

## 链上分析的能力与限制

链上分析是替政府与金融机构追踪加密货币资金流向的产业，Chainalysis、Elliptic、TRM Labs 这类公司把链上数据转成可用于诉讼、冻结与追溯的情报。依业者披露的能力与公开的研究，可以做到与做不到的分析大致如下。

### 可以做到的分析

- 比特币的完整图谱重建，跨多笔交易、多个地址，把属于同一个实体的地址聚类（clustering）。
- 比对已知交易所、混币服务、暗网市场的地址标签。
- Zcash 透明池与屏蔽池的进出边界分析。屏蔽池内部不可见，进出屏蔽池的金额与时间则看得到。
- Monero 早期环大小较小时的部分还原。环大小提升到 11、再到 16 之后，已知概率分析方法的追踪难度大幅上升[^3]。

### 做不到的分析

- 在 Monero 目前的环大小（16）下确定真实发送方。概率推测的命中率高于随机猜测。Monero 研究实验室（Monero Research Lab）2025 年 4 月在官网公布的 OSPEAD 研究估计，攻击者掌握真实输入的时间分布之后，猜中的概率可以从随机的 6.25%（1/16）提高到约 23.5%，相当于有效环大小只剩 4.2[^4]。Monero 的保证因此被削弱，但还不到能指认发送方的程度。
- Zcash 完全屏蔽交易（shielded-to-shielded）的还原。
- 不在公开链上的活动，例如 P2P 直接交易、闪电网络通道内部的交易。

混淆的效果取决于使用人数，所有人都用屏蔽池时，匿名集（anonymity set）够大，分析难度极高。只有少数人用时，使用屏蔽池本身反而会被标记为可疑活动。

## 零知识身份验证的属性证明

zk-SNARKs 的应用不限于支付，套到身份验证上，可以证明自己具备某个属性，同时不泄露属性的具体值，例如：

- **proof-of-age**：证明「我超过 18 岁」，不泄露出生年月日。
- **proof-of-citizenship**：证明「我是某国公民」，不泄露身份证号。
- **proof-of-uniqueness**：证明「我是独一无二的人，不是 bot」，不泄露是谁。

正在发展的系统有三个：

- **World ID**（所属项目 Worldcoin 已在 2024 年更名为 World）：用虹膜扫描（iris scan）生成唯一性凭证，用户以 zk proof 证明「我是独一无二的人」，不泄露虹膜数据。
- **Privado ID**（原名 Polygon ID，2024 年从 Polygon Labs 独立并改名[^5]）：以 Iden3 协议为基础，把政府、银行、医疗等机构签发的可验证凭证（Verifiable Credential）转成 zk proof。
- **Anon Aadhaar**：印度国民身份系统的 zk 封装，用户可以证明「我有有效的 Aadhaar」，不泄露号码。

三者的成熟度差距很大，Privado ID 的生态最完整，但需要 DID（去中心化标识符）基础设施。Anon Aadhaar 只服务印度的身份系统。World ID 最通用，虹膜扫描的争议也最大。台湾目前没有对应的本地服务。

传统 KYC 流程是「我把护照复印件交给你，由你判断是否信任」，零知识身份验证则是「我给你一个证明，你可以验证，但取不到原始数据」。三个系统的共同设计目标，都是把「我证明 X」与「我把 X 披露给谁」分开。

## 支付情境的应用

零知识证明套到支付情境，可以处理下列问题：

- **私密 KYC**：证明「这笔交易来自通过 KYC 的个人」，不泄露个人身份。交易所满足合规要求，用户的身份也受到保护。
- **合规披露**：监管机构稽查时，用户可以选择性披露特定属性（例如「这笔超过 100 万的交易出自合规的个人」），其他信息保持私密。
- **匿名捐款**：捐款人证明「我捐了合法、可抵税的金额」，不泄露个人身份。倡议组织可以保护捐款人，主管机关仍可稽核总额。
- **薪资隐私**：员工证明「我有资格领取该 NGO 的薪资补助」，不泄露个人薪资水平。

理论上的设计很干净，实现上最大的瓶颈是验证者必须信任底层的 zk 系统。可信设置、软件实现的 bug、量子计算机对椭圆曲线的长期威胁（见[后量子密码概观](/articles/post-quantum/)），都是需要管理的风险。

## 台湾与香港的法规环境

台湾的《虚拟资产服务法》在 2026 年 6 月 30 日经立法院三读通过，把 KYC 与 Travel Rule 落实到交易所层级，施行日要等总统公布后由行政院另行指定。本地交易所提供 Monero、Zcash 屏蔽交易等隐私功能会面临明确的监管压力，收受加密货币捐款的组织也要在捐款人匿名与会计披露之间取舍（条文与影响见文档站的[台湾 VASP 法 2026](docs:taiwan/vasp-2026/)）。

香港自 2023 年 6 月起实施虚拟资产交易平台（VATP）发牌制度，隐私币实务上无法在持牌平台上架。倡议捐款在香港更大的风险是资金用途本身可能被定性为危害国家安全，「612 人道支援基金」案就是一例（案情见[倡议组织的匿名捐款管道](docs:scenarios/nonprofit-anonymous-donation/)）。零知识身份验证可以让捐款人的身份不留在日后可能被调阅的记录里，但对资金用途本身的定性无能为力，技术再干净也无法取代法律风险评估。

## 相关阅读

- [匿名支付研究专题](/join/payments-research/)：社区追踪匿名支付技术与法规的研究方向
- [加密货币的隐私光谱](docs:tools/crypto-privacy-spectrum/)：各种加密货币的隐私程度比较
- [倡议组织的匿名捐款管道](docs:scenarios/nonprofit-anonymous-donation/)：组织与捐款人两端的实务做法
- [后量子密码概观](/articles/post-quantum/)：椭圆曲线密码面对量子计算机的迁移时程

[^1]: [Monero, Zcash and other privacy coins face delisting wave](https://www.coinspeaker.com/monero-xmr-zcash-zec-privacy-coins-delisting/) - Coinspeaker
[^2]: [Zcash Counterfeiting Vulnerability Successfully Remediated](https://electriccoin.co/blog/zcash-counterfeiting-vulnerability-successfully-remediated/) - Electric Coin Company
[^3]: [The rise of Monero: traceability challenges and research review](https://www.trmlabs.com/resources/blog/the-rise-of-monero-traceability-challenges-and-research-review) - TRM Labs
[^4]: [OSPEAD - Optimal Ring Signature Research](https://web.getmonero.org/2025/04/05/ospead-optimal-ring-signature-research.html) - getmonero.org
[^5]: [Introduction to Privado ID (prev. Polygon ID)](https://docs.privado.id/docs/introduction/) - Privado ID、[Privado ID becomes the latest project to spin out from Polygon Labs](https://www.theblock.co/post/299898/polygon-id-spins-out-from-polygon-labs-as-privado-id) - The Block
