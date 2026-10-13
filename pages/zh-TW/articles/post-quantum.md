---
title: 後量子密碼概觀
description: NIST 後量子標準 ML-KEM、ML-DSA、SLH-DSA 的選型，「現在收集、未來解密」的威脅模型，以及瀏覽器、雲端服務、通訊協定、SSH 與各地金融監理的轉換進度。
date: 2026-05-01
---

後量子密碼（Post-Quantum Cryptography，PQC）要回答三個問題：現有的公鑰密碼學是否會在未來十年內被量子電腦攻破、何時發生、哪些演算法要先轉換。能實際攻破 RSA 與橢圓曲線的大型量子電腦還沒有出現，但攻擊者可以先把密文存起來，等量子電腦成熟再解密，轉換因此不能等到那一天。NIST 已經發布第一批後量子標準，瀏覽器、TLS 函式庫與 Signal Protocol 都已陸續導入。

## Harvest Now, Decrypt Later 威脅模型

「現在收集、未來解密」（Harvest Now, Decrypt Later，HNDL）是後量子轉換的主要動機。攻擊者今天錄下加密通訊並存檔，等日後取得大型量子電腦，再用 Shor 演算法（在量子電腦上能有效率地分解大數與計算離散對數）破解當時的金鑰交換，還原所有錄下的密文。

以下幾種情況的風險最高：

- **資料的長期價值高**：政府機密、醫療紀錄、商業情報、長期有效的身分資料（身分證號、護照號碼）。
- **攻擊者有儲存能力**：國家級情報機構（NSA 的 Bluffdale 資料中心、中國的情報單位）長期被外界推測在收集這類資料。
- **密文無法回收**：今天傳出去的密文一旦被錄下，就無法重新加密，未來被解密的風險會一直存在。

個人的即時聊天與短效的 session token 很快就失去價值，HNDL 風險低。銀行的 KYC 文件、醫療影像、人權工作者的訪談紀錄，風險高。

NIST IR 8547 的初稿（2024-11 公開徵求意見，截至 2026-10 尚未定稿）提出 2030 年起棄用舊的公鑰演算法、2035 年起全面禁用的時程，ENISA 的路線圖也以這兩個年份為準，NSA 的 CNSA 2.0 另訂 2030 與 2033 年的期限[^1]。新部署從現在起就應該規劃 PQC 的轉換路徑。

<figure markdown="span">
    <img class="brand-frame" src="https://assets.anoni.net/diagrams/pq-timeline.zh-TW.drawio.svg" alt="後量子密碼遷移時程：從 2023 Signal PQXDH、2024 NIST FIPS 與主流瀏覽器啟用、到 2030–2035 主要系統應完成轉換、2040 舊密碼學硬時間表">
</figure>

## NIST 2024 年的三項標準

NIST 在 2016 年啟動 PQC 標準化徵選，2022 年選出第一批演算法，2024 年 8 月發布 FIPS 203、204、205 三份正式標準。

### ML-KEM（FIPS 203），金鑰封裝

- 全名 Module-Lattice-based Key Encapsulation Mechanism，以格密碼（lattice）為基礎，量子電腦同樣難以求解這類數學問題。
- 源自 CRYSTALS-Kyber。
- 用途：取代 RSA-OAEP 與 ECDH，在 TLS、SSH 與加密通訊中負責金鑰交換。
- 公鑰大小依安全等級而定，ML-KEM-512 為 800 bytes、ML-KEM-768 為 1,184 bytes、ML-KEM-1024 為 1,568 bytes，都比 X25519 的 32 bytes 大。封包略為變大，對一般連線速度沒有明顯影響，運算速度快，也容易用硬體加速。

### ML-DSA（FIPS 204），數位簽章

- 全名 Module-Lattice-based Digital Signature Algorithm，源自 CRYSTALS-Dilithium。
- 用途：取代 RSA-PSS 與 ECDSA，用在憑證、軟體簽章與區塊鏈。
- 簽章大小約 2.4–4.6 KB（依安全等級而定），ECDSA 只有 64 bytes。

### SLH-DSA（FIPS 205），雜湊簽章

- 全名 Stateless Hash-based Digital Signature Algorithm，源自 SPHINCS+。
- 用途：作為 ML-DSA 的備援，安全性只仰賴雜湊函數的抗碰撞性，數學假設最保守。
- 缺點是簽章大（約 8–50 KB，依參數集而定）、簽署速度慢，適合長效憑證，不適合高頻率簽章。

NIST 第四輪持續評估以編碼理論（code-based）為基礎的演算法，2025 年 3 月選定 HQC 作為 ML-KEM 的備援 KEM，正式標準預計 2027 年發布[^2][^3]。唯一以同源映射（isogeny）為基礎的候選 SIKE 已在 2022 年被破解而退出。短期內業界部署的主流仍是 ML-KEM 搭配 ML-DSA。

## 2022–2025 年主要系統的部署進度

本節各項的狀態在 2026-10 依各專案的官方文件與公告查核。

### 瀏覽器與 TLS

- **Chrome**：Chrome 124（2024-04）預設啟用 Kyber 草案版本的混合金鑰交換 X25519Kyber768Draft00，Chrome 131（2024-11）改用正式標準的 X25519MLKEM768[^4]。兩者在 TLS 的代碼點不同、彼此不相容，讀 2024 年以前的報導時要留意。
- **Firefox**：Firefox 132（2024-10）加入 X25519MLKEM768（Firefox 稱為 mlkem768x25519），桌面版預設啟用，Android 版從 Firefox 145 起預設啟用[^5]。
- **Safari**：iOS 26、iPadOS 26、macOS Tahoe 26 與 visionOS 26（2025-09）的 TLS 1.3 連線預設提出 X25519MLKEM768，伺服器支援時就協商出混合金鑰交換，Safari 等內建 App 也隨這一版導入[^6][^7]。

混合（hybrid）指同時做傳統 ECDH 與 ML-KEM 兩次金鑰交換，再把兩個結果合併。萬一 ML-KEM 日後被發現有漏洞，傳統 ECDH 仍能提供保護，業界普遍採取這種保險做法。

### 雲端服務

- Cloudflare 從 2022-10 起讓所有經由它提供的網站與 API 預設支援混合後量子金鑰協議，當時用的是 Kyber 草案版本[^8]，現在改用 X25519MLKEM768[^5]。
- AWS 在 2025-04 讓 KMS、ACM、Secrets Manager 的 TLS 端點支援 ML-KEM，用戶端需要在 SDK 另外開啟[^9]。
- Google Cloud 對企業客戶提供 PQC 選項。

### Signal Protocol

Signal 在 2023 年發布 PQXDH（Post-Quantum Extended Diffie-Hellman），在建立對話的金鑰協商中加入後量子金鑰封裝（初期用 CRYSTALS-Kyber，後升級至 ML-KEM），直接回應 HNDL 威脅。PQXDH 只保護對話建立時的金鑰協商，Signal 在 2025-10 再加入 SPQR（Sparse Post-Quantum Ratchet），與既有的 Double Ratchet 合成 Triple Ratchet。對話進行中的前向保密（forward secrecy）與入侵後安全性（post-compromise security）因此也具備抗量子能力[^10]。既有對話會逐步改用新協定，使用者不需要操作。Double Ratchet 的運作方式見[端對端加密的協定機制](/articles/e2ee-protocols/)。

### iMessage PQ3

Apple 在 iOS 17.4（2024-03）為 iMessage 導入 PQ3 協定，在訊息的金鑰交換中加入後量子演算法[^7]。

### SSH 與 PGP

- OpenSSH 9.0（2022-04）把 sntrup761x25519 混合金鑰交換設為預設，9.9（2024-09）加入以 ML-KEM 為基礎的 mlkem768x25519-sha256，10.0（2025-04）改以它為預設，10.1（2025-10）在協商到非後量子演算法時顯示警告[^11]。
- age、Sequoia PGP 等較新的工具開始實驗 PQC，傳統的 GnuPG 進度較慢。

### 區塊鏈與加密貨幣

- 比特幣的 ECDSA 與 Schnorr 簽章在大型量子電腦面前不安全，實際威脅取決於量子電腦出現的時間。
- 以太坊已有提案討論後量子簽章選項，短期內的優先順序不高。
- Zcash、Monero 等隱私幣的零知識證明系統同樣面臨後量子轉換的挑戰。

## 個人與組織的轉換規劃

Signal 與主流瀏覽器的轉換隨軟體更新自動完成，一般使用者需要知道的部分整理在文件站的[端對端加密的保護範圍](docs:basics/e2ee/)。Matrix 的 Olm 與 Megolm 截至 2026-10 還沒有後量子機制，規格的討論仍未結案[^12]。

需要主動規劃的項目：

- **企業 PKI 與憑證**：用於簽章、認證與長期存證的憑證，需要規劃 ML-DSA 或 SLH-DSA 的轉換路徑。CA/Browser Forum 已開始討論 PQC 憑證標準。
- **VPN 與 IPsec**：商用 VPN 對 PQC 的支援程度不一，企業網路規劃時要納入評估。
- **長期文件加密**：法務文件、醫療紀錄與研究資料要先確認十年後是否仍須保密，需要的話就改用 PQC 加密。
- **硬體安全模組（HSM）**：金融與醫療領域的 HSM 需要供應商提供 PQC 演算法，更新週期長。

個人與一般組織現在不需要急著手動部署 PQC，可以先做的有三件：

- 採用會自動更新到 PQC 的工具，例如主流瀏覽器、Signal 與 Cloudflare。
- 盤點需要長期保密的資料，HNDL 風險高的先處理。
- 採購硬體與 SaaS 服務時，把 PQC 路線圖納入評估。

## 台灣、香港與新加坡的合規時程

各地的監理時程大致跟隨 NIST 與 ENISA。以下狀態在 2026-10 依主管機關的公告查核。

台灣的情況分三個領域：

- **政府與產業**：數位發展部數位產業署在 2025-04 發布《後量子密碼遷移指引》1.0 版，給產業參考的遷移步驟是擬定量子準備計畫、盤點密碼資產、與技術供應商討論、確認供應鏈的準備程度[^13]。政府機關內部系統的轉換時程目前沒有查到公開資料。
- **金融**：金融監督管理委員會在 2026-06 發布《金融業後量子密碼遷移參考指引》，作為金融機構辦理遷移的參考。指引分三個階段，2026–2027 年建立治理架構、密碼技術清冊與加密敏捷性的基礎，2027–2029 年推動試辦驗證與共同測試，至 2035 年優先完成高風險與高關鍵系統的遷移[^14]。
- **醫療**：電子病歷與醫療影像需要長期保存（《醫療法》規定病歷至少保存 7 年，部分影像與追蹤資料保存更久），HNDL 風險高，可能是台灣最早需要主動規劃 PQC 的領域。

香港金融管理局（HKMA）在 2026-07 發布銀行業量子準備白皮書與第一期量子準備指數（Quantum Preparedness Index），第一期分數是 2.3 分（滿分 10 分），目標是 2030 年全行業達到 10 分[^15]。證券及期貨事務監察委員會（SFC）是另一個相關的監管機關，病歷等長期資料的保存規範也與台灣不同。

新加坡金融管理局（MAS）在 2024-02 向金融機構發布量子相關資安風險的建議（advisory），重點是提升加密敏捷性，屬建議性質，沒有訂出遷移期限[^16]。

跨地區通用的判斷仍是依循 NIST 與 ENISA 的時程，先處理 HNDL 風險高的長期資料。

## 相關閱讀

- [端對端加密的協定機制](/articles/e2ee-protocols/)
- [零知識身分驗證與支付](/articles/zk-identity-payments/)
- [去中心化網站發布](/articles/dweb-ipfs-onion/)
- [威脅模型如何建立](docs:basics/threat-model/)
- [記者保護消息來源](docs:scenarios/journalist/)

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
[^13]: [數產署攜手後量子資安產業聯盟發布「後量子密碼遷移指引」](https://moda.gov.tw/ADI/news/latest-news/16090) - 數位發展部數位產業署
[^14]: [金管會發布「金融業後量子密碼遷移參考指引」 引導金融機構強化量子風險整備](https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0%2C2&mcustomize=news_view.jsp&dataserno=202606180001&dtable=News) - 金融監督管理委員會
[^15]: [HKMA launches quantum preparedness whitepaper and index to support banking sector's readiness for quantum era](https://www.hkma.gov.hk/eng/news-and-media/press-releases/2026/07/20260727-3/) - 香港金融管理局
[^16]: [Advisory on Addressing the Cybersecurity Risks Associated with Quantum](https://www.mas.gov.sg/regulation/circulars/advisory-on-addressing-the-cybersecurity-risks-associated-with-quantum) - 新加坡金融管理局
