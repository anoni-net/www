---
title: End-to-End Encryption Protocols
description: How Diffie-Hellman, forward secrecy, the Double Ratchet, Sender Keys, and MLS work, the three strategies for multi-device sync, and the design trade-offs across Signal, MLS, SimpleX, and Session.
date: 2026-05-01
---

The practical questions, where transport encryption, end-to-end encryption, and encryption at rest each stop, backups, phone-number registration, and safety numbers, are on the docs site in [the scope of end-to-end encryption](docs:basics/e2ee/).

The design differences in end-to-end encryption (E2EE) come down to who generates the keys, who holds them, and when they change. The same algorithms, placed in different protocols, defend against entirely different adversaries.

## Diffie-Hellman key exchange

Two people who have never met, and who can only pass messages through someone listening, need to agree on a key only they know. Diffie-Hellman key exchange, proposed in 1976, does this. Each side picks a secret, a and b, they exchange G^a and G^b, and each computes the shared G^ab. An observer has seen only G^a and G^b, and recovering a or b from them means solving the discrete logarithm problem, which cannot be done in any reasonable time.

Modern protocols use X25519, an elliptic-curve key exchange that is smaller and faster than the earlier finite-field versions and designed to reduce side-channel risk, meaning inference of a key from physical traces such as timing or power draw. Signal, Tor, TLS 1.3, and most modern SSH implementations such as OpenSSH use or prefer X25519.

![Diffie-Hellman key exchange: Alice and Bob pick secrets a and b, exchange G^a and G^b, each computes the shared key G^ab, and Eve seeing the intermediate messages cannot work backwards in reasonable time](https://assets.anoni.net/diagrams/dh-exchange.zh-TW.drawio.svg)

Diffie-Hellman settles how to agree on a shared key and nothing more. Once a key is long-lived, stealing it one day decrypts every message before and after.

## Forward secrecy

Forward secrecy (FS) ensures that recorded ciphertext stays unreadable even if an attacker later obtains the long-term key. Each connection, or each period, uses an ephemeral key to derive the working key for that moment, which is discarded after use. The long-term key only verifies identity, confirming that this really is Alice, and obtaining it does not reconstruct past working keys.

TLS 1.3 enables forward secrecy by default, and the old RSA key exchange without it has been retired. E2EE messaging protocols go further, changing keys not just per connection but per message, which is the Double Ratchet.

## The Double Ratchet

The Double Ratchet is the core of the Signal Protocol, named for two key-update mechanisms running at once. A ratchet advances in one direction only, and old keys do not come back.

- **DH ratchet**: each time a message arrives from the other party, both sides perform a fresh Diffie-Hellman exchange and update the root key
- **Symmetric ratchet**: between two DH exchanges, each message sent derives the next key symmetrically and discards the previous one immediately

Three security properties follow:

1. **Full forward secrecy**: every message has its own symmetric key, so an attacker who obtains the current key still cannot read past messages, and the next property covers future ones
2. **Post-compromise security** (PCS): forward secrecy protects messages before a compromise, and post-compromise security protects those after. Even if a device is breached and keys are stolen, the security state repairs itself at the next DH exchange provided the attacker did not intercept it, since the stolen keys stop working
3. **Offline messages**: messages accumulate while the other party is offline and sync in a batch when they return, each still with its own key

![The Double Ratchet's two key-update mechanisms: the symmetric ratchet advances one step per message sent, the DH ratchet resets the chain when a message arrives, and each message has its own key](https://assets.anoni.net/diagrams/double-ratchet.zh-TW.drawio.svg)

Open Whisper Systems integrated the Double Ratchet into the Signal Protocol in 2014[^1], and WhatsApp, Facebook Messenger, and Skype's Private Conversations adopted it afterwards. Messenger first used it only in opt-in Secret Conversations, and from December 2023 began making personal chats end-to-end encrypted by default, again on the Signal Protocol[^2]. Skype was retired on 5 May 2025[^3].

## Sender Keys and MLS for group messaging

One-to-one messaging is a solved problem, and groups are a different one. A group of 100 performing 100 Diffie-Hellman operations per message is impractical, and the industry has two main approaches.

### Sender Keys

Signal groups use Sender Keys. Each sender holds a Sender Key, distributed to every member through the one-to-one encrypted channels when joining. Sending encrypts once with your own Sender Key, and every member decrypts with the copy they received.

The advantage is one encryption per message, whether the group has 100 members or 1,000. The costs:

- A new member joining requires redistributing Sender Keys
- A member leaving requires rekeying everyone to guarantee they cannot read new messages (PCS)
- Distribution cost grows with group size

### MLS and TreeKEM

MLS (Messaging Layer Security, IETF RFC 9420) uses a tree-based key structure, TreeKEM, that keeps the cost of joining, leaving, and rekeying at O(log n) absent heavy concurrent updates, which in principle supports groups of tens of thousands while preserving post-compromise security. The design goal is moving E2EE from struggling at a few hundred members to working at organizational scale.

The IETF published RFC 9420 in 2023[^4]. Cisco Webex and Discord's DAVE protocol have adopted or announced adoption of MLS for group key exchange[^5].

Sender Keys are simple, mature, and suited to Signal's scale. MLS is more complex, with membership-change costs that grow more slowly as groups get larger, and suits large working groups.

## Three strategies for multi-device sync

When a phone, tablet, and laptop all need the same conversation, keys are handled in one of three ways:

- **Device linking** (Signal, WhatsApp): each device has its own keys, and a new device syncs history from the primary through a QR code. Strong on privacy, higher sync cost, and a new device cannot see old messages unless the primary re-sends them
- **Encrypted cloud backup** (WhatsApp, iMessage): message history encrypted under a user-set password or key and stored in the cloud. Convenient when changing phones, with strength bounded by the password, and a breach at the provider concentrates the exposure
- **A shared root key across devices** (early iMessage, some enterprise platforms): all devices share one long-term key, which makes sync simple and means one stolen device loses everything

Telegram's secret chats stay on the two devices involved, with no cloud backup at all.

Signal added encrypted backups in beta on Android in September 2025; by the time the iOS version shipped in September 2026 they were available on every platform[^6]. The backup is protected by a 64-character recovery key generated on the device, which the user records and Signal's servers never receive.

## Four protocols compared

| Protocol | One-to-one | Groups | Multi-device | Metadata exposure | Open source |
|---|---|---|---|---|---|
| Signal | Double Ratchet | Sender Keys | Device linking plus encrypted backup | Sealed Sender hides the sender | Yes |
| MLS | TreeKEM | TreeKEM, its core strength | Implementation-dependent | Implementation-dependent | Yes (IETF standard) |
| SimpleX | Double Ratchet variant | Two-layer ratchet | No central account, contact by invitation link | No user identifier | Yes |
| Session | Onion routing plus peer encryption | Semi-centralized | A 13-word mnemonic across devices | Tor-like network reduces metadata | Yes |

Their trade-offs:

- **Signal**: mature, widely adopted, with an experience close to mainstream messaging. Sealed Sender hides the sender of an individual message rather than the account's metadata. Registration is mainly by phone number, and since September 2026 the Android beta has offered Signal Login, a paid registration without a number[^7], whose payment date stays attached to the account (see [Signal Login and the payment trail it leaves](docs:blog/2026/09/2026-signal-login-numberless/))
- **MLS**: standardized at the protocol layer and being adopted, with few complete client implementations so far. It suits organizational settings
- **SimpleX**: having no user identifier is its largest design difference, and it holds up well against metadata surveillance. The costs are a small ecosystem and an evolving user experience
- **Session**: routing over a Tor-like network reduces metadata, and a mnemonic makes multi-device access easy. The costs are higher message latency and the missing forward secrecy: the move from the Signal Protocol to its own Session Protocol removed it, the released versions still lack it, and the revised protocol that restores it has not shipped[^8]

## Related reading

- [The scope of end-to-end encryption](docs:basics/e2ee/): where each kind of encryption stops, and the regional context for messaging tools
- [Secure messaging compared](docs:tools/messaging-comparison/): identity and metadata across Signal, SimpleX, Session, Briar, and Matrix
- [Metadata, and why it matters](docs:basics/metadata/): the contact patterns outside the encryption
- [Post-Quantum Cryptography](/articles/post-quantum/): where Signal and other protocols stand in moving to post-quantum key exchange
- [Zero-Knowledge Identity and Payments](/articles/zk-identity-payments/): zero-knowledge proofs applied to identity and payments

[^1]: [Double Ratchet Algorithm](https://en.wikipedia.org/wiki/Double_Ratchet_Algorithm), Wikipedia
[^2]: [Building end-to-end security for Messenger](https://engineering.fb.com/2023/12/06/security/building-end-to-end-security-for-messenger/), Engineering at Meta
[^3]: [Skype is retiring in May 2025: What you need to know](https://support.microsoft.com/en-us/skype/skype-is-retiring-in-may-2025-what-you-need-to-know-2a7d2501-427f-485e-8be0-2068a9f90472), Microsoft Support
[^4]: [RFC 9420: The Messaging Layer Security (MLS) Protocol](https://www.rfc-editor.org/info/rfc9420/), IETF
[^5]: [Bringing DAVE to all Discord platforms](https://discord.com/blog/bringing-dave-to-all-discord-platforms), Discord
[^6]: [Introducing Signal Secure Backups](https://signal.org/blog/introducing-secure-backups/), Signal
[^7]: [Phone Numberless Registration for Android](https://support.signal.org/hc/en-us/articles/11197884108826-Phone-Numberless-Registration-for-Android), Signal Support
[^8]: [Session Protocol V2](https://getsession.org/session-protocol-v2), Session
