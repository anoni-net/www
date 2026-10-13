---
title: Post-Quantum Cryptography
description: The NIST standards ML-KEM, ML-DSA, and SLH-DSA, the harvest-now-decrypt-later threat model, and how far browsers, cloud providers, messaging protocols, SSH, and financial regulators in the region have got with migration.
date: 2026-05-01
---

Post-quantum cryptography (PQC) turns on three questions: whether today's public-key cryptography will be broken by quantum computers within the next decade, when that happens, and which algorithms to migrate first. A quantum computer large enough to break RSA and elliptic curves in practice does not exist yet, but an attacker can store ciphertext now and decrypt it once one does, so migration cannot wait for that day. NIST has published the first post-quantum standards, and browsers, TLS libraries, and the Signal Protocol have been adopting them.

## Harvest now, decrypt later

Harvest now, decrypt later (HNDL) is the main motivation for the migration. An attacker records encrypted traffic today and stores it, then, once a large quantum computer is available, uses Shor's algorithm (which factors large numbers and computes discrete logarithms efficiently on a quantum computer) to break the key exchange and recover everything recorded.

The risk is highest in these cases:

- **Data with long-lived value**: government secrets, medical records, commercial intelligence, and long-term identifiers such as national identity and passport numbers
- **Attackers with storage capacity**: state intelligence agencies, with the NSA's Bluffdale data centre and Chinese intelligence services long assumed to be collecting this kind of material
- **Ciphertext that cannot be recalled**: once recorded, traffic sent today cannot be re-encrypted, and the risk of future decryption stays with it

Personal real-time chat and short-lived session tokens lose their value quickly, so their HNDL risk is low. Bank KYC documents, medical imaging, and a human rights worker's interview records carry high risk.

NIST's IR 8547, published as an initial public draft in November 2024 and still not finalized as of October 2026, proposes deprecating the old public-key algorithms from 2030 and disallowing them from 2035. ENISA's roadmap works to the same two years, and the NSA's CNSA 2.0 sets its own deadlines of 2030 and 2033[^1]. New deployments should be planning a PQC path now.

<figure markdown="span">
    <img class="brand-frame" src="https://assets.anoni.net/diagrams/pq-timeline.zh-TW.drawio.svg" alt="Post-quantum migration timeline: Signal PQXDH in 2023, NIST FIPS standards and browser rollout in 2024, major systems expected to complete migration between 2030 and 2035, hard deadline for legacy cryptography by 2040">
</figure>

## The three 2024 NIST standards

NIST opened its PQC standardization process in 2016, selected the first algorithms in 2022, and published three final standards, FIPS 203, 204, and 205, in August 2024.

### ML-KEM (FIPS 203), key encapsulation

- Module-Lattice-based Key Encapsulation Mechanism, resting on lattice problems, which quantum computers also find hard
- Derived from CRYSTALS-Kyber
- Replaces RSA-OAEP and ECDH for key exchange in TLS, SSH, and encrypted messaging
- Public keys run 800 bytes at ML-KEM-512, 1,184 bytes at ML-KEM-768, and 1,568 bytes at ML-KEM-1024, all larger than X25519's 32 bytes. Packets grow slightly with no noticeable effect on ordinary connection speed, and the operations are fast and amenable to hardware acceleration

### ML-DSA (FIPS 204), digital signatures

- Module-Lattice-based Digital Signature Algorithm, derived from CRYSTALS-Dilithium
- Replaces RSA-PSS and ECDSA in certificates, software signing, and blockchains
- Signatures run roughly 2.4 to 4.6 KB depending on security level, against ECDSA's 64 bytes

### SLH-DSA (FIPS 205), hash-based signatures

- Stateless Hash-based Digital Signature Algorithm, derived from SPHINCS+
- A fallback for ML-DSA, with security resting only on the collision resistance of hash functions, the most conservative assumption available
- Signatures are large, roughly 8 to 50 KB depending on parameter set, and signing is slow, which suits long-lived certificates rather than high-frequency signing

NIST's fourth round continued evaluating code-based algorithms, and in March 2025 selected HQC as a backup KEM to ML-KEM, with the final standard expected in 2027[^2][^3]. The only isogeny-based candidate, SIKE, was broken and withdrawn in 2022. In the near term, ML-KEM with ML-DSA is what the industry deploys.

## Deployment in major systems, 2022 to 2025

The status of each item below was checked against the projects' official documentation and announcements in October 2026.

### Browsers and TLS

- **Chrome**: Chrome 124 (April 2024) turned on the draft X25519Kyber768Draft00 hybrid by default, and Chrome 131 (November 2024) replaced it with the standardized X25519MLKEM768[^4]. The two use different TLS code points and are not wire-compatible, which is worth knowing when reading coverage from before 2025
- **Firefox**: Firefox 132 (October 2024) added X25519MLKEM768 (which Firefox calls mlkem768x25519), on by default on desktop, and on by default on Android from Firefox 145[^5]
- **Safari**: TLS 1.3 connections in iOS 26, iPadOS 26, macOS Tahoe 26, and visionOS 26 (September 2025) offer X25519MLKEM768 by default and negotiate the hybrid wherever the server supports it, and Safari and other built-in apps adopted it with that release[^6][^7]

Hybrid means performing both a classical ECDH exchange and an ML-KEM exchange and combining the results. If ML-KEM turns out to have a flaw, classical ECDH still protects the connection. This is the insurance policy the industry has broadly adopted.

### Cloud providers

- Since October 2022, Cloudflare has supported hybrid post-quantum key agreement by default for every website and API it serves, initially with draft Kyber[^8] and now with X25519MLKEM768[^5]
- AWS added ML-KEM support to the TLS endpoints of KMS, ACM, and Secrets Manager in April 2025, with clients opting in through their SDK[^9]
- Google Cloud offers PQC options to enterprise customers

### Signal Protocol

Signal published PQXDH (post-quantum extended Diffie-Hellman) in 2023, adding post-quantum key encapsulation to the key agreement that sets up a conversation, initially CRYSTALS-Kyber and later ML-KEM. It was a direct answer to HNDL. PQXDH protects only the key agreement at the start of a conversation, so in October 2025 Signal added SPQR (Sparse Post-Quantum Ratchet), combining it with the existing Double Ratchet into what it calls the Triple Ratchet. Forward secrecy and post-compromise security during an ongoing conversation are now quantum-resistant too[^10]. Existing conversations move to the new protocol gradually, with nothing for users to do. The Double Ratchet itself is covered in [End-to-End Encryption Protocols](/articles/e2ee-protocols/).

### iMessage PQ3

Apple introduced the PQ3 protocol for iMessage in iOS 17.4 (March 2024), adding post-quantum algorithms to the message key exchange[^7].

### SSH and PGP

- OpenSSH 9.0 (April 2022) made the `sntrup761x25519` hybrid the default, 9.9 (September 2024) added the ML-KEM-based `mlkem768x25519-sha256`, 10.0 (April 2025) made that the default, and 10.1 (October 2025) warns when a connection negotiates a non-post-quantum algorithm[^11]
- Newer tools such as age and Sequoia PGP have begun experimenting with PQC, while traditional GnuPG has moved more slowly

### Blockchains and cryptocurrencies

- Bitcoin's ECDSA and Schnorr signatures are not secure against a large quantum computer, with the practical threat depending on when one exists
- Ethereum has proposals discussing post-quantum signature options, at a low priority for now
- The zero-knowledge proof systems in privacy coins such as Zcash and Monero face their own post-quantum migration

## Migration planning for individuals and organizations

The migration in Signal and the major browsers arrives with ordinary software updates, and what general users need to know is on the docs site in [The Scope of End-to-End Encryption](docs:basics/e2ee/). Matrix's Olm and Megolm have no post-quantum mechanism as of October 2026, and the specification discussion remains open[^12].

Needing active planning:

- **Enterprise PKI and certificates**: certificates used for signing, authentication, and long-term attestation need an ML-DSA or SLH-DSA path. The CA/Browser Forum has begun discussing PQC certificate standards
- **VPN and IPsec**: commercial VPN support for PQC is inconsistent and belongs in the evaluation when planning a corporate network
- **Long-term document encryption**: for legal documents, medical records, and research data, ask whether the document still has to be confidential in ten years. If it does, encrypt it with PQC
- **Hardware security modules (HSMs)**: HSMs in finance and healthcare depend on vendors shipping PQC algorithms, and the refresh cycle is long

Individuals and ordinary organizations have no need to deploy PQC by hand yet. Three things are worth doing now:

- Use tools that migrate to PQC through updates, such as the major browsers, Signal, and Cloudflare
- Inventory data that must stay confidential long-term, and deal with whatever carries high HNDL exposure first
- Include a PQC roadmap in evaluations when buying hardware or SaaS

## Compliance timelines in Taiwan, Hong Kong, and Singapore

Regulatory timelines in the region largely follow NIST and ENISA. The status below was checked against regulators' announcements in October 2026.

In Taiwan, the picture differs by sector:

- **Government and industry**: the Administration for Digital Industries under the Ministry of Digital Affairs published version 1.0 of its Post-Quantum Cryptography Migration Guidelines in April 2025. The steps it sets out for industry are drawing up a quantum readiness plan, inventorying cryptographic assets, talking to technology vendors, and confirming supply chain readiness[^13]. We have found no public timeline for government agencies' own systems
- **Finance**: the Financial Supervisory Commission (FSC) published the Post-Quantum Cryptography Migration Reference Guidelines for the Financial Industry in June 2026, as a reference for institutions planning their migration. The guidelines run in three phases: governance, a cryptographic inventory, and the groundwork for crypto-agility in 2026 and 2027, pilots and shared testing from 2027 to 2029, and migration of high-risk and critical systems first, by 2035[^14]
- **Healthcare**: electronic medical records and imaging need long retention (the Medical Care Act requires records to be kept for at least seven years, and imaging and follow-up data are often kept longer), which puts healthcare at high HNDL risk and possibly first in line among Taiwan's sectors to need active PQC planning

The Hong Kong Monetary Authority (HKMA) published a white paper on quantum preparedness in the banking sector in July 2026, together with the first Quantum Preparedness Index. The first score is 2.3 out of 10, and the target is full sector readiness, a score of 10, by 2030[^15]. The Securities and Futures Commission (SFC) is the other relevant regulator, and retention rules for medical and other long-lived records differ from Taiwan's.

The Monetary Authority of Singapore (MAS) issued an advisory to financial institutions on the cybersecurity risks of quantum computing in February 2024. It centres on crypto-agility, is advisory in nature, and sets no migration deadline[^16].

Across jurisdictions, the transferable judgement stays the same: follow the NIST and ENISA timelines, and handle long-lived data with high HNDL exposure first.

## Related reading

- [End-to-End Encryption Protocols](/articles/e2ee-protocols/)
- [Zero-Knowledge Identity and Payments](/articles/zk-identity-payments/)
- [Decentralized Website Publishing](/articles/dweb-ipfs-onion/)
- [Threat modeling](docs:basics/threat-model/)
- [Journalists and source protection](docs:scenarios/journalist/)

[^1]: [NIST IR 8547: Transition to Post-Quantum Cryptography Standards](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf), NIST
[^2]: [NIST IR 8545: Status Report on the Fourth Round of the PQC Standardization Process](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8545.pdf), NIST
[^3]: [NIST Selects HQC as Fifth Algorithm for Post-Quantum Encryption](https://www.nist.gov/news-events/news/2025/03/nist-selects-hqc-fifth-algorithm-post-quantum-encryption), NIST
[^4]: [A new path for Kyber on the web](https://security.googleblog.com/2024/09/a-new-path-for-kyber-on-web.html), Google Security Blog
[^5]: [Post-quantum cryptography support](https://developers.cloudflare.com/ssl/post-quantum-cryptography/pqc-support/), Cloudflare
[^6]: [Prepare your network for quantum-secure encryption in TLS](https://support.apple.com/en-us/122756), Apple
[^7]: [Get ahead with quantum-secure cryptography](https://developer.apple.com/videos/play/wwdc2025/314/), Apple WWDC25
[^8]: [Post-quantum cryptography for all](https://blog.cloudflare.com/post-quantum-for-all/), Cloudflare
[^9]: [ML-KEM post-quantum TLS now supported in AWS KMS, ACM, and Secrets Manager](https://aws.amazon.com/blogs/security/ml-kem-post-quantum-tls-now-supported-in-aws-kms-acm-and-secrets-manager/), AWS
[^10]: [Signal Protocol and Post-Quantum Ratchets](https://signal.org/blog/spqr/), Signal
[^11]: [OpenSSH Release Notes](https://www.openssh.org/releasenotes.html), OpenSSH
[^12]: [Quantum-resistant crypto (matrix-org/matrix-spec#975)](https://github.com/matrix-org/matrix-spec/issues/975), Matrix
[^13]: [數產署攜手後量子資安產業聯盟發布「後量子密碼遷移指引」](https://moda.gov.tw/ADI/news/latest-news/16090) (in Chinese), Administration for Digital Industries, Ministry of Digital Affairs
[^14]: [金管會發布「金融業後量子密碼遷移參考指引」 引導金融機構強化量子風險整備](https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0%2C2&mcustomize=news_view.jsp&dataserno=202606180001&dtable=News) (in Chinese), Financial Supervisory Commission
[^15]: [HKMA launches quantum preparedness whitepaper and index to support banking sector's readiness for quantum era](https://www.hkma.gov.hk/eng/news-and-media/press-releases/2026/07/20260727-3/), Hong Kong Monetary Authority
[^16]: [Advisory on Addressing the Cybersecurity Risks Associated with Quantum](https://www.mas.gov.sg/regulation/circulars/advisory-on-addressing-the-cybersecurity-risks-associated-with-quantum), Monetary Authority of Singapore
