---
title: Zero-Knowledge Identity and Payments
description: Ring signatures and RingCT in Monero, zk-SNARK shielded transactions in Zcash, the capabilities and limits of chain analysis, and zero-knowledge identity applied to private KYC, compliance disclosure, and anonymous donations.
date: 2026-05-01
---

Chains differ widely in how much they hide. Bitcoin's ledger is entirely public, with every transaction and every address balance open to anyone, while Zcash's shielded transactions hide even the amount. Most designs sit in between: addresses obscured, amounts hidden, and the transaction graph still inferable. Monero and Zcash hide different layers, so chain analysis reaches different distances into each. Compliance requirements do not disappear because a chain is private, and zero-knowledge proofs can separate proving that you comply from disclosing who you are. That separation is what zero-knowledge identity (zk-identity) builds on in payments.

This page is the technical background to the [Anonymous Payments Track](/join/payments-research/). For an introduction, see [The cryptocurrency privacy spectrum](docs:tools/crypto-privacy-spectrum/) and [Why anonymous payments matter](docs:basics/payments-anonymity/) on the docs site.

## The On-Chain Visibility Spectrum

An observer watching a chain sees four layers:

1. **Accounts**: who holds which address. Public on Bitcoin, hidden on Monero through stealth addresses
2. **Amounts**: how much a transaction moved. Public on Bitcoin, hidden on Monero through RingCT, entirely hidden in Zcash shielded transactions
3. **Transaction graph**: the path of transfers between A and B. Fully reconstructible on Bitcoin, obscured on Monero through ring signatures with decoys, invisible in Zcash shielded transactions
4. **Metadata**: which IP address, which wallet client, and what time a transaction was sent from. Every chain depends on privacy at the peer-to-peer network layer, whether through Tor or a protocol such as Dandelion++ that scatters the broadcast path to hide the originating IP

Privacy-focused cryptocurrencies generally hide only some of these layers, and designs that hide all four are rare. Monero and Zcash chose different combinations.

## Ring Signatures, Stealth Addresses, and RingCT in Monero

Monero's design comes from the 2013 CryptoNote whitepaper and rests on three mechanisms:

- **Stealth addresses**: each transaction generates a fresh one-time receiving address, so the chain never shows that Alice's address received 100, only that some one-time address did. Alice identifies which one-time addresses are hers using her own private key
- **Ring signatures**: when signing, the sender's real signature is mixed with decoys drawn from past transaction outputs. An observer can establish that one of the 16 outputs is real without establishing which. Monero's current default ring size is 16
- **RingCT (Ring Confidential Transactions)**: Pedersen commitments, homomorphic commitments that allow sums to be checked without revealing the numbers, hide the amounts. Bulletproofs+ range proofs ensure each amount is non-negative, and the whole proves that inputs equal outputs, so no coins are created from nothing

![A Monero ring signature: the sender's real signature mixed among 15 decoys for a ring size of 16, where an observer can verify that one of the 16 is genuine without determining which (diagram labels in Chinese)](https://assets.anoni.net/diagrams/monero-ring.zh-TW.drawio.svg)

Taken together, what appears on the chain is a one-time address receiving a hidden amount from one of 16 possible senders, with no notion of Alice or Bob. Against the four layers, stealth addresses cover accounts, RingCT covers amounts, ring signatures obscure the graph, and metadata still needs Tor.

The costs are a larger blockchain, heavier verification, and transactions that are difficult to reconcile with know-your-customer (KYC) requirements. Exchanges requiring KYC began delisting Monero in 2021, with the largest wave across 2023 and 2024, including Kraken in Europe, Binance, and OKX[^1].

## zk-SNARKs and the Shielded Pool in Zcash

Zcash takes a more radical route. A shielded transaction uses zk-SNARKs (zero-knowledge succinct non-interactive arguments of knowledge, a cryptographic construction that proves you know a secret without revealing it) to prove three things:

- I am authorized to spend this note
- The new notes I create sum to the notes I consumed
- Nothing is being double-spent

![A Zcash shielded transaction: sender and recipient connected through a zk-SNARK proof. Visible on chain are the proof, nullifier, commitment, and fee. Not visible are the sender address, recipient address, amount, and graph relationship (diagram labels in Chinese)](https://assets.anoni.net/diagrams/zcash-shielded.zh-TW.drawio.svg)

The whole proof takes only a few hundred bytes on chain, and the verifier needs neither the amount nor the addresses nor the source. All the chain shows is that a shielded transaction occurred. Against the four layers, one shielded transaction covers accounts, amounts, and graph, with metadata again left to the network layer.

Zcash has been through several generations of zk-SNARK:

- **Sprout** (2016): used BCTV14, an improved variant of PGHR13, and required a trusted setup[^2]
- **Sapling** (2018): moved to Groth16, with a smaller trusted setup and much better performance
- **Halo 2** (activated with the NU5 upgrade in May 2022): no trusted setup required

Zcash's long-running problem has been usage. The shielded pool saw far fewer users than the transparent pool for years, and most transactions remained transparent. The shielded share has risen noticeably since 2025, though fully shielded transactions are still not the whole of it. However good the cryptographic guarantee, without enough shielded traffic to blend into, analysis remains a risk.

## Capabilities and Limits of Chain Analysis

Chain analysis is an industry that traces cryptocurrency flows for governments and financial institutions, with firms such as Chainalysis, Elliptic, and TRM Labs turning on-chain data into intelligence that supports prosecution, freezing, and tracing. Based on what these firms disclose and on published research, the picture is roughly as follows.

### Achievable Analysis

- Full graph reconstruction on Bitcoin, clustering addresses that belong to the same entity across many transactions and addresses
- Matching against address labels for known exchanges, mixing services, and darknet markets
- Boundary analysis between Zcash's transparent and shielded pools. The interior of the shielded pool is invisible, while amounts and times entering and leaving it are not
- Partial recovery on Monero from the era of small ring sizes. After the ring size rose to 11 and then 16, the difficulty of known probabilistic methods increased substantially[^3]

### Analysis Out of Reach

- Identifying the true sender on Monero with certainty at the current ring size of 16. Probabilistic guessing does better than chance. The OSPEAD research published by the Monero Research Lab on the project's site in April 2025 estimates that an adversary who knows the age distribution of real spends can raise the chance of guessing the real input from 6.25% (1 in 16) to about 23.5%, an effective ring size of 4.2[^4]. That weakens Monero's guarantee without amounting to identification
- Recovering fully shielded (shielded-to-shielded) Zcash transactions
- Activity that never reaches a public chain, such as direct peer-to-peer trades or the interior of Lightning Network channels

The effectiveness of blending depends on how many people are doing it. When everyone uses the shielded pool, the anonymity set is large and analysis is extremely difficult. When only a few do, using the pool is itself flagged as suspicious.

## Attribute Proofs in Zero-Knowledge Identity

zk-SNARKs are not limited to payments. Applied to identity, they let you prove you hold an attribute without revealing its value, for example:

- **Proof of age**: proving "I am over 18" without revealing a date of birth
- **Proof of citizenship**: proving "I am a citizen of Taiwan" without revealing an ID number
- **Proof of uniqueness**: proving "I am a distinct human, not a bot" without revealing which human

Three systems are in development:

- **World ID** (its parent project Worldcoin renamed itself World in 2024): uses an iris scan to generate a uniqueness credential, with the user proving "I am a distinct human" through a zero-knowledge proof rather than revealing the iris data
- **Privado ID** (formerly Polygon ID, spun out of Polygon Labs and renamed in 2024[^5]): built on the Iden3 protocol, turning verifiable credentials issued by governments, banks, and healthcare institutions into zero-knowledge proofs
- **Anon Aadhaar**: a zero-knowledge wrapper around India's national identity system, letting a user prove "I hold a valid Aadhaar" without revealing the number

Their maturity varies widely. Privado ID has the most complete ecosystem and requires decentralized identifier (DID) infrastructure. Anon Aadhaar serves one national system. World ID is the most general, and its iris scanning is the most contested. Taiwan currently has no equivalent local service.

Traditional KYC is "I hand you a copy of my passport and you decide whether to trust it". Zero-knowledge identity is "I hand you a proof you can verify without obtaining the underlying data". All three systems share the design goal of separating "I prove X" from "I disclose X to you".

## Applications in Payments

Applied to payments, zero-knowledge proofs address the following:

- **Private KYC**: proving "this transaction comes from a KYC-verified individual" without revealing which individual. The exchange meets its compliance requirement and the user's identity stays protected
- **Compliance disclosure**: during a regulatory audit, a user can selectively disclose specific attributes (for example, "this transaction over 1 million comes from a compliant individual") while everything else stays private
- **Anonymous donations**: a donor proves "I donated a lawful, tax-deductible amount" without revealing who they are. The advocacy organization can protect its donors while the authorities can still audit the total
- **Salary privacy**: an employee proves "I am eligible for this NGO's salary subsidy" without revealing their pay

The design is clean in theory, and the practical bottleneck is that the verifier has to trust the underlying zero-knowledge system. Trusted setups, implementation bugs, and the long-term quantum threat to elliptic curves (see [Post-Quantum Cryptography](/articles/post-quantum/)) are all risks to manage.

## Regulation in Taiwan and Hong Kong

Taiwan's Virtual Asset Service Act passed its third reading in the Legislative Yuan on 30 June 2026. It pushes KYC and the Travel Rule down to the exchange level, and its commencement date will be set by the Executive Yuan after presidential promulgation. Local exchanges offering privacy features such as Monero or Zcash shielded transactions face clear regulatory pressure, and organizations accepting cryptocurrency donations have to weigh donor anonymity against accounting disclosure (the provisions and their effects are covered in [Taiwan's 2026 Virtual Asset Service Act](docs:regional/taiwan-vasp-2026/) on the docs site).

Hong Kong has licensed virtual asset trading platforms since June 2023, and privacy coins are in practice unlistable on licensed platforms. The larger risk for donation-funded advocacy there is that the purpose of the funds may itself be characterized as endangering national security, as the 612 Humanitarian Relief Fund case showed (see [Anonymous donation channels for advocacy organizations](docs:scenarios/nonprofit-anonymous-donation/)). Zero-knowledge identity can keep a donor's identity out of records that a national security investigation could later reach. It does nothing about how the purpose of the funds is characterized, and no amount of clean technology substitutes for a legal risk assessment.

## Related Reading

- [Anonymous Payments Track](/join/payments-research/): the community's research on anonymous payment technology and regulation
- [The cryptocurrency privacy spectrum](docs:tools/crypto-privacy-spectrum/): how much privacy different cryptocurrencies offer
- [Anonymous donation channels for advocacy organizations](docs:scenarios/nonprofit-anonymous-donation/): practical arrangements for organizations and donors
- [Post-Quantum Cryptography](/articles/post-quantum/): the migration timeline for elliptic-curve cryptography in the face of quantum computers

[^1]: [Monero, Zcash and other privacy coins face delisting wave](https://www.coinspeaker.com/monero-xmr-zcash-zec-privacy-coins-delisting/), Coinspeaker
[^2]: [Zcash Counterfeiting Vulnerability Successfully Remediated](https://electriccoin.co/blog/zcash-counterfeiting-vulnerability-successfully-remediated/), Electric Coin Company
[^3]: [The rise of Monero: traceability challenges and research review](https://www.trmlabs.com/resources/blog/the-rise-of-monero-traceability-challenges-and-research-review), TRM Labs
[^4]: [OSPEAD - Optimal Ring Signature Research](https://web.getmonero.org/2025/04/05/ospead-optimal-ring-signature-research.html), getmonero.org
[^5]: [Introduction to Privado ID (prev. Polygon ID)](https://docs.privado.id/docs/introduction/), Privado ID, and [Privado ID becomes the latest project to spin out from Polygon Labs](https://www.theblock.co/post/299898/polygon-id-spins-out-from-polygon-labs-as-privado-id), The Block
