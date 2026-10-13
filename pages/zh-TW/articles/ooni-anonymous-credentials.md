---
title: OONI Probe 匿名憑證系統的設計與實作
description: OONI 公告文章的翻譯，介紹 OONI Probe 匿名憑證系統的需求、以 Rust 實作的憑證框架、憑證屬性與提交量測的協定，以及與 Go 程式碼的整合方式，另補上 OONI 2025 年文獻回顧裡的設計脈絡。
date: 2026-02-05
---

OONI 仰賴全球志工上傳網路審查的觀測資料，參與的人越多，假資料或錯誤量測混入的機會也越大，資料庫的可信度會跟著受影響。IP 封鎖、帳號登入或裝置認證這類傳統做法會暴露志工身分，與 OONI 保護隱私的承諾衝突。OONI 因此改用匿名憑證，以密碼學驗證一筆量測來自符合條件的 OONI Probe，同時不揭露使用者是誰、身在何處，也不讓不同網路上的活動被串連起來。

!!! info ""

    本文翻譯自 OONI 團隊的 [Announcing OONI's New Anonymous Credential System](https://ooni.org/post/2025-announcing-ooni-new-anonymous-credential-system/)（2026-01-30），文中的「我們」指 OONI，註腳為譯者補充。文末的[設計的演進脈絡](#evolution)一節由 anoni.net 整理。

在先前的文章中，我們已說明[為什麼 OONI 需要匿名憑證系統](https://ooni.org/post/2025-probe-security-without-identification/)，並整理了這類系統必須滿足的[資安與隱私需求](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/)。核心挑戰是 OONI 必須在不建立任何可能暴露使用者身分、或造成跨網路追蹤的識別碼的前提下，仍能確認上傳量測的可信度[^1]。

匿名憑證（anonymous credentials）是一種密碼學機制，可以驗證 OONI Probe 的某些屬性（例如長期參與的程度或量測的數量），同時不暴露使用者是誰、身在何處，也不把使用者在不同網路上的活動串連起來。

## OONI 的需求

要符合 OONI 的威脅模型（threat model），憑證系統必須滿足以下限制：

- **防止跨網路可連結性（cross-network linkability）**：只支援網路在地（network-local）的識別方式。
- **驗證中繼資料（metadata）**：驗證 `probe_age`、`measurement_count` 與封鎖清單或信任狀態（blocklist/trust status），但不揭露原始數值，也不破壞匿名性。
- **抵抗偽造與女巫攻擊（Sybil attacks）**：讓惡意者難以大量建立或操弄身分。
- **支援頻繁、多次出示（multi-show presentations）**：OONI Probe 會持續上傳量測資料。
- **避免縮小匿名集合（anonymity sets）**[^2]：即使在量測資料裡加入更多中繼資料，也不讓使用者變得更容易被辨識。

既有的憑證生態系（例如以盲簽章為基礎、適合零知識證明的簽章，或基於 SNARK 的建構）各自能滿足其中一部分需求，但無法一次涵蓋全部。OONI 尤其需要簽發者在地驗證（issuer-local verification）、高效率的範圍證明（range proofs）、依網路而定的假名（network-dependent pseudonyms），以及憑證更新協定（credential update protocols）。在不做重大妥協的前提下，沒有現成的方案能完整符合這些限制[^3]。

## 模組化、具表達力的憑證框架

我們與滑鐵盧大學、Tor Project 與 Risc Zero 的研究者合作，建立了一套分層式系統，用來建構零知識憑證與相關協定。系統包含三個 Rust crate（`cmz`、`sigma-compiler`、`sigma-proofs`），實作經過充分研究的 sigma-protocols，並把高階的敘述（statements）編譯成高效率、以線性代數為核心的證明敘述。我們也在推動這些協定的 CFRG 草案（[draft-irtf-cfrg-sigma-protocols](https://datatracker.ietf.org/doc/draft-irtf-cfrg-sigma-protocols/)、[draft-irtf-cfrg-fiat-shamir](https://datatracker.ietf.org/doc/draft-irtf-cfrg-fiat-shamir/)）[^4]。

對 OONI 特別重要的功能有四項：

1. **可多次出示（multi-show）且簽發者在地驗證（issuer-local verification）**：OONI 的使用模式類似 KVAC 憑證（簽發者與驗證者是同一方），CMZ 與 μCMZ 方案可以直接支援。
2. **高效率的範圍證明（range proofs）**：`probe_age` 與 `measurement_count` 需要以粗略的區間[^5]呈現（例如超過 1 週、超過 1000 筆量測），避免形成近乎唯一的組合。sigma-rs 的堆疊可以用相對精簡的方式支援範圍證明。
3. **網路在地假名（network-local pseudonyms）**：OONI Probe 在每個網路只呈現一個身分，不同網路之間則要保持不可連結，可以直接對應到 sigma-rs 的屬性與約束系統（例如 `pseudonym = secret * DOMAIN`）。
4. **簽發與更新協定（issuance + update protocols）**：我們的模型需要出示舊憑證，在不揭露底層數值的情況下取得更新後的新憑證（例如 `measurement_count` 加一），與 UserAuth 範例描述的模式相同。

## OONI 的憑證結構

OONI 的匿名憑證包含以下屬性：

``` rust
CMZ! { UserAuthCredential:
    nym_id, // a stable per-installation secret
    age, // coarse bucket
    measurement_count // measurements submitted
}
```

三個屬性對應到需求文章描述的額外中繼資料，同時仍遵守匿名性的限制。

### 提交量測協定的概觀

使用 sigma-rs 的 μCMZ API，提交新量測的協定在概念上寫成：

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

協定可以確保：

- OONI Probe 維持相同的網路在地假名
- `measurement_count` 單調遞增（不會倒退，也無法跳號造假）
- 年齡分桶（age bucket）保持正確
- OONI 看不到原始數值，只能驗證被證明的敘述
- 惡意的用戶端無法偽造可信度中繼資料

伺服器只會看到證明（proof）[^6]，看不到底層的屬性值。

`measurement_count` 用來評估使用者在該網路中的參與程度，不作為速率限制（rate limit）的依據。

## 與 OONI 程式碼庫的整合

OONI Probe 引擎主要以 Go 撰寫，匿名憑證系統則以 Rust 實作。為了讓兩者的整合保持單純，我們在 Rust 端提供一個小型、相容 C 的 API，再透過 rust2go 產生 Go 的綁定（bindings）。兩邊的職責清楚切分，Rust 負責所有密碼學（憑證簽發、零知識證明、驗證、更新），用戶端負責協調流程、持久化（persistence）與狀態機（state machines）。

Rust 函式庫是一個獨立的加密引擎（crypto engine），接收不透明（opaque）的輸入（目前的憑證與協定參數），產生要送給伺服器的協定訊息，再處理伺服器的回應、回傳更新後的憑證。所有狀態管理刻意交給呼叫端的應用程式處理，讓 API 維持精簡、容易移植[^7]。呼叫端有兩個：

- 行動裝置上是 OONI 的跨平台用戶端 [OONI probe-multiplatform](https://github.com/ooni/probe-multiplatform)
- 命令列上是 OONI 的 Go 用戶端（miniooni、ooniprobe）[OONI probe-cli](https://github.com/ooni/probe-cli)

用戶端負責儲存與重新載入：

- 最新的憑證 blob
- 請求之間需要保留的本機狀態（例如 request 與 response 之間尚未完成的協定狀態）

邊界因此維持清楚，Go 端把憑證與協定訊息都當成不透明的 bytes，所有正確性與隱私性屬性由 Rust 端在內部強制執行。

### 資料交換模型

Rust 與 Go 的邊界之間只傳遞三種資料：

- **不透明的序列化協定訊息**：bytes，為了以 JSON 傳輸通常會再做 Base64 編碼。
- **公開參數（public parameters）**：例如簽發者公鑰、協定參數。
- **網路情境（network context）**：domain separator、cc 與 asn 等。

Go 端因此不必重新實作密碼學就能整合，網路通訊與應用程式邏輯也能與 OONI Probe 的其他部分保持一致。

長期金鑰（long term keys）交給作業系統的原生機制管理與儲存，Android 使用 [Android Keystore](https://developer.android.com/privacy-and-security/keystore)，iOS 使用 [Keychain services](https://developer.apple.com/documentation/security/keychain-services)。

## 後續規劃

OONI 的資料使用者很快就能依下列條件篩選或註記量測資料：

- 長期運作與新加入的 OONI Probe
- 量測量高的貢獻者
- 被列入封鎖清單（blocklisted）或故障的 OONI Probe
- 受信任的機構型 OONI Probe

完整抵抗女巫攻擊（建立大量虛假帳號）仍是應用層的問題，例如註冊階段的速率限制。經過驗證的 `measurement_count` 與 `probe_age` 分桶，仍能對潛在的攻擊者形成實質的阻力。

我們歡迎密碼學研究者、實作者與任何感興趣的人提供回饋，希望這項工作能以安全、透明的方式服務全球的 OONI 社群。之後我們會進一步分享協定的設計細節、效能基準測試，以及 sigma-rs 如何隨下一個 OONI Probe 主要版本一起發布。

（2026-10 補註：OONI 在 2026 年 7 月的工程文章裡評估了這套系統的成效，文中提到系統正逐步導入正式環境，每筆量測會標成 verified、unverified 或 failed，導讀見 [OONI 錯誤量測的辨識方法與匿名憑證](/articles/ooni-faulty-measurements/)。）

## 設計的演進脈絡 {#evolution}

OONI 在 2025 年 2 月發表 [Probe Security Without Identification](https://ooni.org/post/2025-probe-security-without-identification/)，是規劃這套系統時的文獻回顧，以下由 anoni.net 整理其中仍有參考價值的背景。

當時設想的威脅分成兩種。惡意者在同一個網路、針對少數網站、短時間內上傳假資料，集中的模式相對容易辨識。較高階的對手從多個網路、針對多個網址，長時間分散上傳少量假資料，就難以偵測。攻擊的目的可能是讓外界質疑 OONI 平台的可信度，或散布某個國家、地區審查狀況的誤導訊息，例如宣稱被封鎖的網站沒有被封鎖，或反過來。錯誤量測也可能來自 OONI Probe 安裝錯誤，不一定出於惡意。OONI 同時重視使用者在網路層與應用層的隱私，使用者也可以透過 Tor 這類工具上傳量測。系統要在 `checkIn` 與 `upload` 兩段流程裡建立信任，並能擴充到每秒數百次的驗證。

文獻回顧把匿名憑證分成兩個維度。依驗證方式分，鍵控驗證憑證（KVAC）由同一方簽發與驗證，使用較輕量的密碼學，Signal 是採用者之一，公開驗證憑證則讓簽發者與驗證者可以是不同的單位。依出示次數分，單次使用的憑證（例如盲簽章，或 IETF Privacy Pass 標準採用的 VOPRF）出示一次就失效，多次出示的憑證則有 Camenisch–Lysyanskaya、Chase–Meiklejohn–Zaverucha（CMZ）與 BBS 等方案，其中 CMZ 用在 Signal 的私人群組與 Tor 的橋接分發。OONI Probe 會反覆上傳量測，一次發放一批單次令牌雖然可行，應用層就得自行管理令牌的庫存與補發，效率不如專為多次出示設計的方案。文中也列出有效期限、網路相關身分、撤銷、範圍證明等可以獨立於基礎方案加上的擴充功能。

2026 年的實作選了鍵控驗證的 CMZ 與 μCMZ，由 OONI 同時擔任簽發者與驗證者，並採用文獻回顧列出的範圍證明與網路相關身分兩項擴充，與 2025 年的方向一致。

## 相關閱讀

- [OONI 錯誤量測的辨識方法與匿名憑證](/articles/ooni-faulty-measurements/)
- [零知識身分驗證與支付](/articles/zk-identity-payments/)
- [什麼是 OONI](docs:tools/what-is-ooni/)
- [Requirements for OONI's anonymous credentials](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/)

[^1]: 伺服器需要分辨量測是否來自符合某些條件的 OONI Probe，同時又不能讓量測帶有可長期追蹤的固定身分。跨網路追蹤的風險在於同一個使用者在不同網路（例如家用 Wi‑Fi、公司網路、行動網路）都被認出是同一人，就可能被用來推回真實身分或行為軌跡。
[^2]: 匿名集合可以理解為看起來都一樣的一群人。附帶的中繼資料太細（例如精確的年齡、精確的筆數），很容易形成近乎唯一的組合，反而削弱匿名性。OONI 想驗證的是使用者符合某個範圍或條件，不需要知道精確的數值。
[^3]: 在 OONI 的使用情境下，issuer-local verification 通常代表簽發者（issuer）同時也是驗證者（verifier），由 OONI 自己簽發與驗證，不把驗證交給第三方。範圍證明是用零知識的方式證明某個值落在某個區間內（例如大於 1 週、超過 1000 筆），但不透露精確數值。
[^4]: CFRG（Crypto Forum Research Group）是 IRTF 底下的密碼學研究論壇，草案通常會朝標準化方向前進。Fiat–Shamir 是把互動式證明（需要來回的挑戰與回應）轉成非互動式證明的常見技巧，用戶端可以一次送出證明給伺服器驗證。
[^5]: 刻意用粗略的區間取代精確數值，是為了避免使用者的特徵過於獨特（例如 17,382 筆量測加上 39 天），導致容易被追蹤。每個網路一個身分，通常是透過與網路相關的 domain separator，把同一個安裝的秘密值對應到不同的假名，達成跨網路不可連結。
[^6]: 這段協定同時涵蓋出示舊憑證與取得新憑證（更新），伺服器可以驗證計數確實加一，但不會知道原本的精確計數。`@DOMAIN` 與 `NYM` 用來做 domain separation（避免跨情境重用導致可連結），讓同一個安裝在不同網路產生不同的假名。
[^7]: 關鍵的設計是邊界清楚，Go 端不碰密碼學細節，只把它當成黑盒（opaque bytes）使用，密碼學的正確性與隱私性由 Rust 端封裝保證。透過 C ABI 再產生 Go binding 是常見的跨語言整合方式，也能降低在 Go 端重寫密碼學而出錯的風險。
