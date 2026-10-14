---
title: 端對端加密的協定機制
description: Diffie-Hellman、前向保密、Double Ratchet、Sender Keys 與 MLS 的運作方式，多裝置同步的三種策略，以及 Signal、MLS、SimpleX、Session 四種協定的設計取捨。
date: 2026-05-01
---

三種加密的界線、備份、門號註冊與安全碼這些使用面的問題，寫在文件站的[端對端加密的保護範圍](docs:basics/e2ee/)。

端對端加密（End-to-End Encryption，E2EE）的設計差異集中在金鑰由誰產生、由誰保管、何時更新。同樣的演算法放進不同的協定，對抗的攻擊者完全不同。

## Diffie-Hellman 金鑰交換

兩個從沒見過面、只能透過監聽者轉送訊息的人，要協商出一把只有雙方知道的金鑰，1976 年提出的 Diffie-Hellman 金鑰交換（DH）解決了這個問題。雙方各自選一個秘密值 a、b，交換 G^a 與 G^b，再各自算出共同的 G^ab。監聽者只看過 G^a 與 G^b，要反推 a 或 b 需要解離散對數問題，在合理時間內無法完成。

現代協定普遍使用 X25519，一套以橢圓曲線為基礎的金鑰交換演算法，比早期的有限體版本更小、更快，設計上也降低側通道攻擊（side channel，從運算時間、功耗等物理跡象反推金鑰）的風險。Signal、Tor、TLS 1.3 與多數現代 SSH 實作（例如 OpenSSH）預設或優先使用 X25519。


DH 只解決協商共同金鑰的問題。金鑰長期存在時，只要有一天被偷，過去與未來的訊息都會被解開。

## 前向保密

前向保密（Forward Secrecy，FS）確保長期金鑰將來落入攻擊者手中時，過去錄下的密文仍然無法解密。做法是每次連線（或每段時間）都用一把臨時金鑰（ephemeral key）交換出當下的工作金鑰，用完即丟。長期金鑰只用來驗證身分，確認對方真的是 Alice，攻擊者取得它也無法還原過去的工作金鑰。

TLS 1.3 預設啟用前向保密，不具前向保密的 RSA 金鑰交換已經淘汰。端對端加密的通訊協定更進一步，不只每次連線換一把臨時金鑰，連每則訊息都換，也就是 Double Ratchet。

## Double Ratchet

Double Ratchet 是 Signal Protocol 的核心，名稱來自兩種同時運作的金鑰更新機制。棘輪（ratchet）只能單向推進，舊金鑰無法倒回。

- **DH ratchet**：每收到對方一則訊息，雙方執行一次新的 DH 金鑰交換，更新根金鑰（root key）
- **對稱 ratchet**（symmetric ratchet）：兩次 DH 交換之間，每送出一則訊息就用對稱演算法導出下一把金鑰，舊的立即丟棄

由此得到三項安全性質：

1. **完整前向保密**：每則訊息有獨立的對稱金鑰，攻擊者取得當下的金鑰，過去的訊息仍然安全，之後的訊息由下一項性質保護
2. **事後安全**（Post-Compromise Security，PCS，也稱後向保密）：前向保密保護遭入侵之前的訊息，事後安全保護之後的訊息。裝置一度被入侵、金鑰被竊，只要攻擊者沒有攔下下一次 DH 交換，安全狀態就會自行恢復，攻擊者手上的舊金鑰隨即失效
3. **離線訊息**：對方不在線時訊息可以累積，等對方上線再批次同步，每則仍有獨立的金鑰


Double Ratchet 在 2014 年由 Open Whisper Systems 整合進 Signal Protocol[^1]，之後 WhatsApp、Facebook Messenger 與 Skype 的 Private Conversations 相繼採用。Messenger 原本只在選擇性開啟的 Secret Conversations 使用，2023 年 12 月起把個人對話改為預設端對端加密，協定同樣是 Signal Protocol[^2]。Skype 在 2025 年 5 月 5 日停止服務[^3]。

## 群組通訊的 Sender Keys 與 MLS

一對一通訊的解法已經成熟，群組的問題不同。100 人的群組若每則訊息都做 100 次 DH，成本不切實際，業界目前有兩條主流路線。

### Sender Keys

Signal 的群組使用 Sender Keys。每個發送者持有一把 Sender Key，加入群組時透過一對一的加密通道分送給每位成員。發送時用自己的 Sender Key 加密一次，成員用各自收到的副本解密。

發送端只加密一次，100 人與 1000 人的群組效能相近。代價有三項：

- 新成員加入時要重新分發 Sender Keys
- 成員退出時要全部換鑰，才能保證退出的人無法讀取新訊息（PCS）
- 群組越大，分發成本越高

### MLS 與 TreeKEM

MLS（Messaging Layer Security，IETF RFC 9420）用樹狀金鑰結構 TreeKEM，在沒有大量並行更新時，把加入、退出與金鑰更新的成本壓在 O(log n)，理論上可以支援上萬人的群組並維持 PCS。設計目標是讓端對端加密從兩三百人就吃力的規模，推進到企業與機構等級的群組。

IETF 在 2023 年發布 RFC 9420[^4]。Cisco Webex 與 Discord（DAVE 協定）已採用或宣布採用 MLS 處理群組金鑰交換[^5]。

Sender Keys 簡單、實作成熟，適合 Signal 的規模。MLS 較複雜，成員異動的成本隨群組規模增長得比較慢，適合需要管理大型工作群組的場景。

## 多裝置同步的三種策略

手機、平板、筆電要同時看到同一段對話時，金鑰的處理方式有三種：

- **連結裝置**（device linking，Signal、WhatsApp）：每台裝置有獨立的金鑰，新增裝置時透過 QR code 從主裝置同步。隱私強、同步成本高，新裝置看不到加入之前的訊息，除非主裝置重新傳送
- **加密雲端備份**（WhatsApp、iMessage）：訊息紀錄用使用者設定的密碼或金鑰加密後存到雲端。換手機方便，強度取決於密碼，雲端業者被攻擊時，所有人的密文集中受影響
- **跨裝置共用根金鑰**（早期的 iMessage、部分企業通訊軟體）：所有裝置共用一把長期金鑰，同步簡單，任何一台裝置被偷就全部曝光

Telegram 的 Secret Chats 只存在參與對話的兩台裝置上，沒有雲端備份。

Signal 在 2025 年 9 月於 Android 的 beta 版推出加密備份（Secure Backups），2026 年 9 月 iOS 版上線時各平台都已提供[^6]。備份由裝置上產生的 64 字元復原金鑰保護，由使用者自行保存，Signal 的伺服器不會取得。

## 四種協定的對照

| 協定 | 一對一 | 群組 | 多裝置 | metadata 揭露 | 開源 |
|---|---|---|---|---|---|
| Signal | Double Ratchet | Sender Keys | 連結裝置與加密備份 | Sealed Sender 隱藏寄件人 | 是 |
| MLS | TreeKEM | TreeKEM（核心優勢） | 視實作而定 | 視實作而定 | 是（IETF 標準） |
| SimpleX | Double Ratchet 變體 | 雙層 ratchet | 沒有中央帳號，以邀請連結建立聯繫 | 沒有使用者識別碼 | 是 |
| Session | 洋蔥路由與點對點加密 | 半中心化 | 13 個字的助記詞跨裝置 | 走類似 Tor 的網路降低 metadata | 是 |

各自的設計取捨：

- **Signal**：成熟、使用者多，使用體驗接近主流通訊軟體。Sealed Sender 只隱藏單則訊息的寄件人，帳號本身的 metadata 仍在伺服器上。註冊以手機號碼為主，2026 年 9 月起 Android 的 beta 版開放付費、免門號的 Signal Login[^7]，付款日期仍跟著帳號保存（見[Signal 免門號註冊與付款紀錄](docs:blog/2026/09/2026-signal-login-numberless/)）
- **MLS**：協定層已經標準化，業界正在採用，完整的 MLS 用戶端還不多，較適合企業或機構的場景
- **SimpleX**：沒有使用者識別碼是設計上最大的差異，對 metadata 監控的抵抗力強。代價是生態小、使用體驗仍在演進
- **Session**：流量走類似 Tor 的網路降低 metadata，跨裝置只靠一組助記詞，門檻低。代價是訊息延遲較高。Session 從 Signal Protocol 改用自己的 Session Protocol 時拿掉了前向保密，目前的正式版仍然沒有，具前向保密的新版協定還沒有發布，2026-08 的開發進度把它排在 Session Pro 之後[^8][^9]

## 相關閱讀

- [端對端加密的保護範圍](docs:basics/e2ee/)：傳輸加密、端對端加密與儲存加密的界線，以及在地的工具脈絡
- [匿名通訊工具比較](docs:tools/messaging-comparison/)：Signal、SimpleX、Session、Briar、Matrix 的身分綁定與 metadata
- [Metadata 是什麼，為什麼重要](docs:basics/metadata/)：加密範圍外的通聯關係
- [後量子密碼概觀](/articles/post-quantum/)：Signal 等協定轉換到後量子金鑰交換的進度
- [零知識身分驗證與支付](/articles/zk-identity-payments/)：零知識證明在身分驗證與支付上的應用

[^1]: [Double Ratchet Algorithm](https://en.wikipedia.org/wiki/Double_Ratchet_Algorithm) - Wikipedia
[^2]: [Building end-to-end security for Messenger](https://engineering.fb.com/2023/12/06/security/building-end-to-end-security-for-messenger/) - Engineering at Meta
[^3]: [Skype is retiring in May 2025: What you need to know](https://support.microsoft.com/en-us/skype/skype-is-retiring-in-may-2025-what-you-need-to-know-2a7d2501-427f-485e-8be0-2068a9f90472) - Microsoft Support
[^4]: [RFC 9420: The Messaging Layer Security (MLS) Protocol](https://www.rfc-editor.org/info/rfc9420/) - IETF / RFC Editor
[^5]: [Bringing DAVE to all Discord platforms](https://discord.com/blog/bringing-dave-to-all-discord-platforms) - Discord
[^6]: [Introducing Signal Secure Backups](https://signal.org/blog/introducing-secure-backups/) - Signal
[^7]: [Phone Numberless Registration for Android](https://support.signal.org/hc/en-us/articles/11197884108826-Phone-Numberless-Registration-for-Android) - Signal Support
[^8]: [Session Protocol V2](https://getsession.org/session-protocol-v2) - Session
[^9]: [Session Development Update - Pro Beta and Protocol v2](https://getsession.org/session-development-update-pro-beta-protocol-v2) - Session
