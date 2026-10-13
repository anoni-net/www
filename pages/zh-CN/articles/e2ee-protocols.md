---
title: 端对端加密的协议机制
description: Diffie-Hellman、前向保密、Double Ratchet、Sender Keys 与 MLS 的运作方式，多设备同步的三种策略，以及 Signal、MLS、SimpleX、Session 四种协议的设计取舍。
date: 2026-05-01
---

三种加密的界线、备份、手机号注册与安全码这些使用层面的问题，写在文档站的[端对端加密的保护范围](docs:basics/e2ee/)。

端对端加密（End-to-End Encryption，E2EE）的设计差异集中在密钥由谁产生、由谁保管、何时更新。同样的算法放进不同的协议，对抗的攻击者完全不同。

## Diffie-Hellman 密钥交换

两个从没见过面、只能通过监听者转发消息的人，要协商出一把只有双方知道的密钥，1976 年提出的 Diffie-Hellman 密钥交换（DH）解决了这个问题。双方各自选一个秘密值 a、b，交换 G^a 与 G^b，再各自算出共同的 G^ab。监听者只看过 G^a 与 G^b，要反推 a 或 b 需要解离散对数问题，在合理时间内无法完成。

现代协议普遍使用 X25519，一套基于椭圆曲线的密钥交换算法，比早期的有限域版本更小、更快，设计上也降低侧信道攻击（side channel，从运算时间、功耗等物理迹象反推密钥）的风险。Signal、Tor、TLS 1.3 与多数现代 SSH 实现（例如 OpenSSH）默认或优先使用 X25519。

![Diffie-Hellman 密钥交换流程：Alice 与 Bob 各自挑秘密 a、b，交换 G^a、G^b，双方各自算出共同密钥 G^ab，Eve 即使看到中间消息也无法在合理时间内反推](https://assets.anoni.net/diagrams/dh-exchange.zh-TW.drawio.svg)

DH 只解决协商共同密钥的问题。密钥长期存在时，只要有一天被偷，过去与未来的消息都会被解开。

## 前向保密

前向保密（Forward Secrecy，FS）确保长期密钥将来落入攻击者手中时，过去录下的密文仍然无法解密。做法是每次连接（或每段时间）都用一把临时密钥（ephemeral key）交换出当下的工作密钥，用完即丢。长期密钥只用来验证身份，确认对方真的是 Alice，攻击者取得它也无法还原过去的工作密钥。

TLS 1.3 默认启用前向保密，不具前向保密的 RSA 密钥交换已经淘汰。端对端加密的通讯协议更进一步，不只每次连接换一把临时密钥，连每条消息都换，也就是 Double Ratchet。

## Double Ratchet

Double Ratchet 是 Signal Protocol 的核心，名称来自两种同时运作的密钥更新机制。棘轮（ratchet）只能单向推进，旧密钥无法倒回。

- **DH ratchet**：每收到对方一条消息，双方执行一次新的 DH 密钥交换，更新根密钥（root key）
- **对称 ratchet**（symmetric ratchet）：两次 DH 交换之间，每发出一条消息就用对称算法导出下一把密钥，旧的立即丢弃

由此得到三项安全性质：

1. **完整前向保密**：每条消息有独立的对称密钥，攻击者取得当下的密钥，过去的消息仍然安全，之后的消息由下一项性质保护
2. **事后安全**（Post-Compromise Security，PCS，也称后向保密）：前向保密保护遭入侵之前的消息，事后安全保护之后的消息。设备一度被入侵、密钥被窃，只要攻击者没有拦下下一次 DH 交换，安全状态就会自行恢复，攻击者手上的旧密钥随即失效
3. **离线消息**：对方不在线时消息可以累积，等对方上线再批量同步，每条仍有独立的密钥

![Double Ratchet 的两种密钥更新机制：对称 ratchet 每发一条消息推进一格、DH ratchet 收到对方消息时整段重置，每条消息有独立密钥](https://assets.anoni.net/diagrams/double-ratchet.zh-TW.drawio.svg)

Double Ratchet 在 2014 年由 Open Whisper Systems 整合进 Signal Protocol[^1]，之后 WhatsApp、Facebook Messenger 与 Skype 的 Private Conversations 相继采用。Messenger 原本只在需手动开启的 Secret Conversations 使用，2023 年 12 月起把个人对话改为默认端对端加密，协议同样是 Signal Protocol[^2]。Skype 在 2025 年 5 月 5 日停止服务[^3]。

## 群组通讯的 Sender Keys 与 MLS

一对一通讯的解法已经成熟，群组的问题不同。100 人的群组若每条消息都做 100 次 DH，成本不切实际，业界目前有两条主流路线。

### Sender Keys

Signal 的群组使用 Sender Keys。每个发送者持有一把 Sender Key，加入群组时通过一对一的加密通道分发给每位成员。发送时用自己的 Sender Key 加密一次，成员用各自收到的副本解密。

发送端只加密一次，100 人与 1000 人的群组性能相近。代价有三项：

- 新成员加入时要重新分发 Sender Keys
- 成员退出时要全部更换密钥，才能保证退出的人无法读取新消息（PCS）
- 群组越大，分发成本越高

### MLS 与 TreeKEM

MLS（Messaging Layer Security，IETF RFC 9420）用树状密钥结构 TreeKEM，在没有大量并发更新时，把加入、退出与密钥更新的成本压在 O(log n)，理论上可以支持上万人的群组并维持 PCS。设计目标是让端对端加密从两三百人就吃力的规模，推进到企业与机构级别的群组。

IETF 在 2023 年发布 RFC 9420[^4]。Cisco Webex 与 Discord（DAVE 协议）已采用或宣布采用 MLS 处理群组密钥交换[^5]。

Sender Keys 简单、实现成熟，适合 Signal 的规模。MLS 较复杂，成员变动的成本随群组规模增长得比较慢，适合需要管理大型工作群组的场景。

## 多设备同步的三种策略

手机、平板、笔记本电脑要同时看到同一段对话时，密钥的处理方式有三种：

- **关联设备**（device linking，Signal、WhatsApp）：每台设备有独立的密钥，新增设备时通过二维码从主设备同步。隐私强、同步成本高，新设备看不到加入之前的消息，除非主设备重新发送
- **加密云端备份**（WhatsApp、iMessage）：消息记录用用户设定的密码或密钥加密后存到云端。换手机方便，强度取决于密码，云服务商被攻击时，所有人的密文集中受影响
- **跨设备共用根密钥**（早期的 iMessage、部分企业通讯软件）：所有设备共用一把长期密钥，同步简单，任何一台设备被偷就全部曝光

Telegram 的 Secret Chats 只存在参与对话的两台设备上，没有云端备份。

Signal 在 2025 年 9 月于 Android 的 beta 版推出加密备份（Secure Backups），2026 年 9 月 iOS 版上线时各平台都已提供[^6]。备份由设备上产生的 64 个字符的恢复密钥保护，由用户自行保存，Signal 的服务器不会取得。

## 四种协议的对照

| 协议 | 一对一 | 群组 | 多设备 | metadata 暴露 | 开源 |
|---|---|---|---|---|---|
| Signal | Double Ratchet | Sender Keys | 关联设备与加密备份 | Sealed Sender 隐藏发件人 | 是 |
| MLS | TreeKEM | TreeKEM（核心优势） | 视实现而定 | 视实现而定 | 是（IETF 标准） |
| SimpleX | Double Ratchet 变体 | 双层 ratchet | 没有中央账号，以邀请链接建立联系 | 没有用户标识符 | 是 |
| Session | 洋葱路由与点对点加密 | 半中心化 | 13 个词的助记词跨设备 | 走类似 Tor 的网络降低 metadata | 是 |

各自的设计取舍：

- **Signal**：成熟、用户多，使用体验接近主流通讯软件。Sealed Sender 只隐藏单条消息的发件人，账号本身的 metadata 仍在服务器上。注册以手机号为主，2026 年 9 月起 Android 的 beta 版开放付费、免手机号的 Signal Login[^7]，付款日期仍跟着账号保存（见[Signal 免手机号注册与付款记录](docs:blog/2026/09/2026-signal-login-numberless/)）
- **MLS**：协议层已经标准化，业界正在采用，完整的 MLS 客户端还不多，较适合企业或机构的场景
- **SimpleX**：没有用户标识符是设计上最大的差异，对 metadata 监控的抵抗力强。代价是生态小、使用体验仍在演进
- **Session**：流量走类似 Tor 的网络降低 metadata，跨设备只靠一组助记词，门槛低。代价是消息延迟较高。Session 从 Signal Protocol 改用自己的 Session Protocol 时去掉了前向保密，目前的正式版仍然没有，具前向保密的新版协议还没有发布[^8]

## 相关阅读

- [端对端加密的保护范围](docs:basics/e2ee/)：传输加密、端对端加密与存储加密的界线，以及各地的工具脉络
- [匿名通讯工具比较](docs:tools/messaging-comparison/)：Signal、SimpleX、Session、Briar、Matrix 的身份绑定与 metadata
- [Metadata 是什么，为什么重要](docs:basics/metadata/)：加密范围外的通联关系
- [后量子密码概观](/articles/post-quantum/)：Signal 等协议迁移到后量子密钥交换的进度
- [零知识身份验证与支付](/articles/zk-identity-payments/)：零知识证明在身份验证与支付上的应用

[^1]: [Double Ratchet Algorithm](https://en.wikipedia.org/wiki/Double_Ratchet_Algorithm) - Wikipedia
[^2]: [Building end-to-end security for Messenger](https://engineering.fb.com/2023/12/06/security/building-end-to-end-security-for-messenger/) - Engineering at Meta
[^3]: [Skype is retiring in May 2025: What you need to know](https://support.microsoft.com/en-us/skype/skype-is-retiring-in-may-2025-what-you-need-to-know-2a7d2501-427f-485e-8be0-2068a9f90472) - Microsoft Support
[^4]: [RFC 9420: The Messaging Layer Security (MLS) Protocol](https://www.rfc-editor.org/info/rfc9420/) - IETF / RFC Editor
[^5]: [Bringing DAVE to all Discord platforms](https://discord.com/blog/bringing-dave-to-all-discord-platforms) - Discord
[^6]: [Introducing Signal Secure Backups](https://signal.org/blog/introducing-secure-backups/) - Signal
[^7]: [Phone Numberless Registration for Android](https://support.signal.org/hc/en-us/articles/11197884108826-Phone-Numberless-Registration-for-Android) - Signal Support
[^8]: [Session Protocol V2](https://getsession.org/session-protocol-v2) - Session
