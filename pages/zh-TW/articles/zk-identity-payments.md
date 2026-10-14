---
title: 零知識身分驗證與支付
description: Monero 的環簽名與 RingCT、Zcash 的 zk-SNARKs 遮蔽交易、鏈上分析的能力與限制，以及零知識身分驗證在私密 KYC、合規揭露與匿名捐款的應用。
date: 2026-05-01
---

各條鏈提供的隱私程度差距很大，比特幣的帳本完全公開，任何人都可以查到每筆交易與每個地址的餘額，Zcash 的遮蔽交易則連金額都看不見。多數設計落在兩者之間，地址被混淆、金額被遮蔽，交易圖譜仍可被推測。Monero 與 Zcash 隱匿的層次不同，鏈上分析能追到的範圍也跟著不同。合規要求不會因為鏈上隱私而消失，零知識證明可以把「證明自己合規」與「揭露自己是誰」分開，零知識身分驗證（zk-identity）在支付情境的應用就建立在這一點上。

本頁是[匿名支付研究專題](/join/payments-research/)的技術背景。入門的說明見文件站的[加密貨幣的隱私光譜](docs:tools/crypto-privacy-spectrum/)與[為什麼匿名支付重要](docs:basics/payments-anonymity/)。

## 鏈上隱私的可見度光譜

監控者觀察一條鏈，可以看到四個層次：

1. **帳戶**（Account）：誰擁有哪個地址。比特幣公開，Monero 用 stealth address 隱匿。
2. **金額**（Amount）：一筆交易轉了多少。比特幣公開，Monero 用 RingCT 隱匿，Zcash 遮蔽交易完全隱藏。
3. **交易圖譜**（Transaction Graph）：A 與 B 之間的轉帳路徑。比特幣可以重建完整圖譜，Monero 用 ring signatures 製造誘餌混淆，Zcash 遮蔽交易看不到圖譜。
4. **元資料**（Metadata）：交易由哪個 IP、哪個錢包客戶端、在什麼時間點送出。所有鏈都仰賴 P2P 網路層的隱私，搭配 Tor，或 Dandelion++ 這類打散交易廣播路徑、隱藏來源 IP 的協定。

注重隱私的加密貨幣多半只隱匿其中幾層，四層全部隱匿的設計很少，Monero 與 Zcash 各自選了不同的組合。

## Monero 的環簽名、Stealth Address 與 RingCT

Monero 的設計來自 2013 年的 CryptoNote 白皮書，核心是三個機制：

- **Stealth Address**：每筆交易產生新的一次性收款地址，鏈上看不到「Alice 的地址收了 100 元」，只看得到「某個一次性地址收了 100 元」。Alice 用自己的私鑰可以辨識哪些一次性地址屬於她。
- **Ring Signatures**：寄件人簽署交易時，把真實簽章混進從過去交易輸出挑出的誘餌（decoys）之中。觀察者只能確定「16 個輸出之中有一個是真的」，無法確定是哪一個。Monero 目前預設的環大小為 16。
- **RingCT**（Ring Confidential Transactions）：用 Pedersen 同態承諾（不揭露數字、仍可驗算加總的加密承諾）隱藏金額，再以 Bulletproofs+ 範圍證明確保每筆金額非負，整體證明輸入總和等於輸出總和，沒有憑空增發。


三者組合起來，鏈上看到的是「某個一次性地址收到一筆隱藏金額，由 16 個可能的寄件人之一發送」，沒有 Alice 與 Bob 的概念。對照前面的四層，stealth address 遮蓋帳戶層、RingCT 遮蓋金額層、ring signatures 打散圖譜層，第四層的元資料仍要靠 Tor 另外處理。

代價是區塊鏈的體積較大、交易驗證的運算量重，隱匿交易也難以符合 KYC（實名驗證）的合規要求。要求 KYC 的交易所自 2021 年起陸續下架 Monero，2023 至 2024 年的下架規模最大，包含 Kraken 歐洲區、Binance、OKX[^1]。

## Zcash 的 zk-SNARKs 與遮蔽池

Zcash 走的路線更激進，遮蔽交易（shielded transaction）用 zk-SNARKs（Zero-Knowledge Succinct Non-Interactive Argument of Knowledge，可以證明「我知道某個秘密」而不洩漏秘密內容的密碼學工具）證明三件事：

- 我有花費這個 note 的權限。
- 我建立的新 note 金額總和等於消耗的 note 金額。
- 沒有重複花費。

| 項目 | 鏈上 |
|---|---|
| zk-SNARK 證明 | 可見，證明交易有效 |
| nullifier | 可見，用來防止重複花費 |
| 新的 commitment | 可見，代表新建立的 note |
| 手續費 | 可見 |
| 寄件人與收件人地址 | 不可見 |
| 金額 | 不可見 |
| 跟其他交易的關聯 | 不可見 |

整個證明在鏈上只占幾百 bytes，驗證者不需要知道金額、地址與來源，鏈上能看到的只有發生了一筆遮蔽交易。對照四層，一筆遮蔽交易同時遮蓋帳戶、金額、圖譜三層，第四層的元資料同樣留給網路層處理。

Zcash 經歷過幾代 zk-SNARKs：

- **Sprout**（2016）：用 BCTV14（PGHR13 的改良變體），需要可信設定（trusted setup）[^2]。
- **Sapling**（2018）：升級到 Groth16，可信設定的範圍更小，效能也改善許多。
- **Halo 2**（2022 年 5 月隨 NU5 升級啟用）：不再需要可信設定。

Zcash 長期的問題在使用率，遮蔽池（shielded pool）的使用人數一度遠少於透明池（transparent pool），多數交易仍是透明的。2025 年起遮蔽池的占比明顯上升，但完整遮蔽的交易仍不是全部。沒有足夠的遮蔽流量提供混淆，密碼學保證再好，被分析的風險仍在。

## 鏈上分析的能力與限制

鏈上分析是替政府與金融機構追蹤加密貨幣金流的產業，Chainalysis、Elliptic、TRM Labs 這類公司把鏈上資料轉成可用於訴訟、凍結與追溯的情報。依業者揭露的能力與公開的研究，可以做到與做不到的分析大致如下。

### 可以做到的分析

- 比特幣的完整圖譜重建，跨多筆交易、多個地址，把屬於同一個實體的地址分群（clustering）。
- 比對已知交易所、混幣服務、暗網市場的地址標籤。
- Zcash 透明池與遮蔽池的進出邊界分析。遮蔽池內部不可見，進出遮蔽池的金額與時間則看得到。
- Monero 早期環大小較小時的部分還原。環大小提升到 11、再到 16 之後，已知機率分析方法的追蹤難度大幅上升[^3]。

### 做不到的分析

- 在 Monero 目前的環大小（16）下確定真實寄件人。機率推測的命中率高於隨機猜測。Monero 研究實驗室（Monero Research Lab）2025 年 4 月在官網公布的 OSPEAD 研究估計，攻擊者掌握真實輸入的時間分布之後，猜中的機率可以從隨機的 6.25%（1/16）提高到約 23.5%，相當於有效環大小只剩 4.2[^4]。Monero 的保證因此被削弱，但還不到能指認寄件人的程度。
- Zcash 完全遮蔽交易（shielded-to-shielded）的還原。
- 不在公開鏈上的活動，例如 P2P 直接交易、閃電網路通道內部的交易。

混淆的效果取決於使用人數，所有人都用遮蔽池時，匿名集（anonymity set）夠大，分析難度極高。只有少數人用時，使用遮蔽池本身反而會被標記為可疑活動。

## 零知識身分驗證的屬性證明

zk-SNARKs 的應用不限於支付，套到身分驗證上，可以證明自己具備某個屬性，同時不洩漏屬性的具體值，例如：

- **proof-of-age**：證明「我超過 18 歲」，不洩漏出生年月日。
- **proof-of-citizenship**：證明「我是台灣公民」，不洩漏身分證字號。
- **proof-of-uniqueness**：證明「我是獨一無二的人，不是 bot」，不洩漏是誰。

正在發展的系統有三個：

- **World ID**（所屬專案 Worldcoin 已在 2024 年更名為 World）：用虹膜掃描（iris scan）產生獨特性憑證，使用者以 zk proof 證明「我是獨一無二的人」，不洩漏虹膜資料。
- **Privado ID**（原名 Polygon ID，2024 年從 Polygon Labs 獨立並改名[^5]）：以 Iden3 協定為基礎，把政府、銀行、醫療等機構發出的可驗證憑證（Verifiable Credential）轉成 zk proof。
- **Anon Aadhaar**：印度國民身分系統的 zk 包裝，使用者可以證明「我有有效的 Aadhaar」，不洩漏號碼。

三者的成熟度差距很大，Privado ID 的生態最完整，但需要 DID（去中心化識別碼）基礎設施。Anon Aadhaar 只服務印度的身分系統。World ID 最通用，虹膜掃描的爭議也最大。台灣目前沒有對應的本地服務。

傳統 KYC 流程是「我把護照影本交給你，由你判斷是否信任」，零知識身分驗證則是「我給你一個證明，你可以驗證，但取不到原始資料」。三個系統的共同設計目標，都是把「我證明 X」與「我把 X 揭露給誰」分開。

## 支付情境的應用

零知識證明套到支付情境，可以處理下列問題：

- **私密 KYC**：證明「這筆交易來自通過 KYC 的個人」，不洩漏個人身分。交易所滿足合規要求，使用者的身分也受到保護。
- **合規揭露**：監理機關稽查時，使用者可以選擇性揭露特定屬性（例如「這筆超過 100 萬的交易出自合規的個人」），其他資訊維持隱密。
- **匿名捐款**：捐款人證明「我捐了合法、可抵稅的金額」，不洩漏個人身分。倡議組織可以保護捐款人，主管機關仍可稽核總額。
- **薪資隱私**：員工證明「我有資格領取該 NGO 的薪資補助」，不洩漏個人薪資水準。

理論上的設計很乾淨，實作上最大的瓶頸是驗證者必須信任底層的 zk 系統。可信設定、軟體實作的 bug、量子電腦對橢圓曲線的長期威脅（見[後量子密碼概觀](/articles/post-quantum/)），都是需要管理的風險。

## 台灣與香港的法規環境

台灣的《虛擬資產服務法》在 2026 年 6 月 30 日經立法院三讀通過，把 KYC 與 Travel Rule 落實到交易所層級，施行日要等總統公布後由行政院另行指定。本地交易所提供 Monero、Zcash 遮蔽交易等隱私功能會面臨明確的監理壓力，收受加密貨幣捐款的組織也要在捐款人匿名與會計揭露之間取捨（條文與影響見文件站的[台灣 VASP 法 2026](docs:taiwan/vasp-2026/)）。

香港自 2023 年 6 月起實施虛擬資產交易平台（VATP）發牌制度，隱私幣實務上無法在持牌平台上架。倡議捐款在香港更大的風險是資金用途本身可能被定性為危害國家安全，「612 人道支援基金」案就是一例（案情見[倡議組織的匿名捐款管道](docs:scenarios/nonprofit-anonymous-donation/)）。零知識身分驗證可以讓捐款人的身分不留在日後可能被調閱的紀錄裡，但對資金用途本身的定性無能為力，技術再乾淨也無法取代法律風險評估。

## 相關閱讀

- [匿名支付研究專題](/join/payments-research/)：社群追蹤匿名支付技術與法規的研究方向
- [加密貨幣的隱私光譜](docs:tools/crypto-privacy-spectrum/)：各種加密貨幣的隱私程度比較
- [倡議組織的匿名捐款管道](docs:scenarios/nonprofit-anonymous-donation/)：組織與捐款人兩端的實務做法
- [後量子密碼概觀](/articles/post-quantum/)：橢圓曲線密碼面對量子電腦的遷移時程

[^1]: [Monero, Zcash and other privacy coins face delisting wave](https://www.coinspeaker.com/monero-xmr-zcash-zec-privacy-coins-delisting/) - Coinspeaker
[^2]: [Zcash Counterfeiting Vulnerability Successfully Remediated](https://electriccoin.co/blog/zcash-counterfeiting-vulnerability-successfully-remediated/) - Electric Coin Company
[^3]: [The rise of Monero: traceability challenges and research review](https://www.trmlabs.com/resources/blog/the-rise-of-monero-traceability-challenges-and-research-review) - TRM Labs
[^4]: [OSPEAD - Optimal Ring Signature Research](https://web.getmonero.org/2025/04/05/ospead-optimal-ring-signature-research.html) - getmonero.org
[^5]: [Introduction to Privado ID (prev. Polygon ID)](https://docs.privado.id/docs/introduction/) - Privado ID、[Privado ID becomes the latest project to spin out from Polygon Labs](https://www.theblock.co/post/299898/polygon-id-spins-out-from-polygon-labs-as-privado-id) - The Block
