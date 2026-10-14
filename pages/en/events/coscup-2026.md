---
title: COSCUP 2026 Anonymity Networks Community track
description: The two-day anoni.net track at COSCUP 2026 (8 and 9 August 2026, NTUST, Taipei), with talks and workshops on Tor, Tails, OONI, browser tracking, campus Tor relays, data-privacy rights and anonymous payments.
---

![COSCUP 2026 Anonymity Networks Community track hero image](https://assets.anoni.net/event/anoni-net-eth-taipei.webp){ .shot }

Journalists need to protect sources, civil-society groups need to protect members and donors, and developers want to know whether their tools hold up against surveillance. Then there are people rattled by scam texts or ad tracking who want some control back over their own data. All of these needs run into the same risks: traffic can be intercepted, identities can be traced, and the timing and amount of a single transfer can reconstruct a whole web of relationships. An organization's member list and money flows can be exposed without anyone inside noticing.

At COSCUP 2026, we, a community based in Taiwan, ran a two-day community track built on a year of hands-on work with [Tor](docs:tools/what-is-tor/) (the onion routing network), [Tails](docs:tools/what-is-tails/) (an amnesic live operating system), [OONI](docs:tools/what-is-ooni/) (the Open Observatory of Network Interference), personal privacy and anonymous payments. The program ran from how the internet and censorship work, through open-source privacy tools in practice, campus Tor relays, browser tracking and data-privacy rights, to an anonymous-payments session co-organized with ETHTaipei. Community members gave the first three primers; the rest were invited, co-organized and accepted talks.

!!! info "Event details"

    - Dates: August 8 (Sat) and 9 (Sun), 2026
    - Venue: National Taiwan University of Science and Technology (NTUST), Taipei. The community track was in `TR-510`; the Aug 8 afternoon session co-organized with ETHTaipei was in `TR-511`.
    - Format: community talks, hands-on workshops, and an anonymous-payments session co-organized with ETHTaipei
    - Language: most sessions were in Mandarin. Raghu's "The Workings of the Internet" was in English.
    - Admission: COSCUP was free, and the community track needed no separate registration. The [official COSCUP schedule](https://pretalx.coscup.org/coscup-2026/) is the authoritative record of times.
    - Status: the event has ended. This page keeps the program, session notes and speakers' slides as a record.
    - Slides: slides and recordings shared by speakers are linked under each session in the [schedule overview](#schedule-overview). Copyright stays with each speaker, so ask the speaker before reposting or adapting them unless a license is noted.

[COSCUP 2026 schedule](#schedule-overview){ .btn .solid }

!!! tip "Free, registration-free and anonymous attendance"

    COSCUP was free and the community track needed no advance sign-up, so attendees could simply walk into the room. For a community that promotes anonymity, attending could itself be anonymous: sitting in on a talk required no personal details at all.

!!! tip "Suggested sessions by audience"

    - **Newsrooms and independent journalists**: "Real-world open-source privacy tools" (Aug 8 morning) covered the secure intake channels, metadata scrubbing and isolation tools journalists actually use, and paired with "Threat models and metadata 101". On the Aug 9 afternoon, "Browser tracking, anti-tracking strategies" dealt with how an everyday browser can leak who you have contacted, and "After the health-insurance database case" and "Privacy guide 2026" extended into data-privacy rights and responding to legal data requests. Further reading: [Journalists and source protection](docs:scenarios/journalist/).
    - **Civil-society groups and NGOs**: the four Aug 8 morning primers were closest to organizational realities. "Real-world open-source privacy tools" surveyed the encrypted messaging, collaboration and leak-intake tools civil-society groups and NGOs rely on, and the talk on anonymous eligibility verification looked at how a beneficiary or a whistleblower can prove they qualify without leaving identifying data behind. "Privacy guide 2026" on Aug 9 covered preparing for legal data requests. For weighing anonymous donation channels, "I don't launder money — so why understand anonymous payments?" in the Aug 8 afternoon ETHTaipei session was the plain-language entry point, with no crypto background needed.
    - **Open-source and tech community**: Aug 9 was the most technical day, with hands-on material on OpenWRT, the NTNU Tor relay and browser-fingerprint research. The Aug 8 afternoon talks on zero-knowledge proofs with the Citizen Digital Certificate, privacy-preserving KYC (know-your-customer identity checks) and stealth addresses were the most substantial protocol-level content. To contribute, see [Take part](/join/).

## <i data-icon="calendar-text"></i> Schedule overview { #schedule-overview }

The community track program is below; the [official COSCUP schedule](https://pretalx.coscup.org/coscup-2026/) is authoritative for times. Session titles are translated from the program, and each title links to its page on pretalx. Changeover breaks sat between sessions: 10 minutes on the Aug 8 morning, and 5 minutes on Aug 9 to fit a fuller day.

### Day 1, Saturday 8 August 2026

Aug 8 morning was four open-source anonymity primers, the first three led by anoni.net community members and the fourth an invited talk. All four were pitched at entry level, with open-source tools as the through-line, and suited civil-society groups, news media and independent journalists. From 13:00, the "Anonymous Payments" session co-organized with ETHTaipei took over with heavier protocol-level content.

**Morning 09:30–12:00 · community open-source anonymity primers (room `TR-510`)**

| Time | Session | Speaker |
|------|---------|---------|
| 09:30-10:00<br>30 min | <span class="tag">General</span> <i data-icon="account-group"></i> **[Meet Anonymity Networks Community: open-source anonymity tools, community practice, and the three 2026 themes](https://pretalx.coscup.org/coscup-2026/talk/8CZ7ER/)**<br><i data-icon="arrow-right-bottom"></i> Who we are, our work localizing Tor, Tails and OONI into Chinese, and why high-risk work needs tools whose source code can be checked | anoni.net community |
| 10:10-10:40<br>30 min | <span class="tag">General</span> <i data-icon="target-account"></i> **[Threat models and metadata 101: know your adversary, and why anonymity tools must be open source to be trustworthy](https://pretalx.coscup.org/coscup-2026/talk/GFKLC8/)**<br><i data-icon="arrow-right-bottom"></i> Even if your calls aren't tapped, who you contacted and when is often enough to expose a source. How to work out who you're defending against, and how far to go | anoni.net community |
| 10:50-11:20<br>30 min | <span class="tag">General</span> <i data-icon="toolbox-outline"></i> **[Real-world open-source privacy tools: how civil-society groups, independent journalists, and individuals actually use them](https://pretalx.coscup.org/coscup-2026/talk/QPDZEC/)**<br><i data-icon="arrow-right-bottom"></i> The open, auditable, free tools journalists, NGOs and privacy-minded individuals actually use, laid out so anyone can pick one or two to start with | anoni.net community |
| 11:30-12:00<br>30 min | <span class="tag">General</span> <i data-icon="scale-balance"></i> **[Drugs that aren't drugs, laundering that isn't laundering: on anonymous eligibility verification](https://pretalx.coscup.org/coscup-2026/talk/WYGFAZ/)**<br><i data-icon="arrow-right-bottom"></i> The same thing gets sorted into two categories under different rules, so who gets to define lawful and unlawful? A search for a third path between full real-name identification and no identification at all; no cryptography background needed | Denken Chen |

**Afternoon 13:00–16:30 · ETHTaipei "Anonymous Payments" session (room `TR-511`, program arranged by ETHTaipei)**

| Time | Session | Speaker |
|------|---------|---------|
| 13:00-13:30<br>30 min | <span class="tag">Payments</span> <i data-icon="card-account-details-outline"></i> **[Zero-knowledge proofs and Citizen Digital Certificate identity verification](https://pretalx.coscup.org/coscup-2026/talk/997SN8/)**<br><i data-icon="arrow-right-bottom"></i> Proving to a service that you are a Taiwanese citizen without handing over any personal data | Ya-wen Jeng |
| 13:40-14:10<br>30 min | <span class="tag">Payments</span> <i data-icon="account-check-outline"></i> **[The Privacy-preserving Identity Pipeline in KYC](https://pretalx.coscup.org/coscup-2026/talk/BBQDPR/)**<br><i data-icon="arrow-right-bottom"></i> A stack of cryptographic primitives that passes KYC without the server ever seeing your identity data | ryanycw (Ryan Wang) |
| 14:20-14:50<br>30 min | <span class="tag">Payments</span> <i data-icon="link-off"></i> **[Starting from unlinkability: how stealth addresses solve on-chain financial privacy (Fluidkey case study)](https://pretalx.coscup.org/coscup-2026/talk/WK8EEE/)**<br><i data-icon="arrow-right-bottom"></i> Stealth addresses scatter one person's payments across unrelated addresses that no outsider can link | Jennifer HSU |
| 15:00-15:30<br>30 min | <span class="tag">Payments</span> <i data-icon="bitcoin"></i> **["I don't launder money — so why understand anonymous payments?" A from-scratch intro to private crypto flows](https://pretalx.coscup.org/coscup-2026/talk/QGUGMK/)**<br><i data-icon="arrow-right-bottom"></i> Why advocacy groups and donors should understand the privacy risks of crypto payments, with several approaches explained in plain language<br><i data-icon="presentation"></i> [Slides (web)](https://mashbean.net/decks/coscup-2026-privacy-money/) | mashbean |
| 15:40-16:30<br>50 min | <span class="tag">Payments</span> <i data-icon="hammer-wrench"></i> **[Hands-on private payments workshop: from Tornado Cash to Privacy Pool](https://pretalx.coscup.org/coscup-2026/talk/3WHJYA/)**<br><i data-icon="arrow-right-bottom"></i> Props and live demos of how Tornado Cash and Privacy Pool work, with a simulated network on site for attendees who brought a laptop<br><i data-icon="presentation"></i> [Slides (web)](https://chihchengliang.github.io/notes/2026-07-27_privacy_pools/slides.html) | Liangcc |

### Day 2, Sunday 9 August 2026

Aug 9 was a full day of seven accepted talks, spanning network and censorship basics, home networking and campus Tor relays, on-chain identity, browser tracking, health-database privacy rights and personal privacy. Technical and everyday-facing sessions alternated through the day.

**Morning 10:00–12:00 (room `TR-510`)**

| Time | Session | Speaker |
|------|---------|---------|
| 10:00-10:50<br>50 min | <span class="tag">General</span> <i data-icon="web"></i> **[The Workings of the Internet: how the net works and how censors block you (in English)](https://pretalx.coscup.org/coscup-2026/talk/UY8UQN/)**<br><i data-icon="arrow-right-bottom"></i> A postcard analogy for who sits between you and a website, and what they can see or change<br><i data-icon="presentation"></i> [Slides (PDF)](https://saxrag.com/bucket/random/workings_of_the_internet.pdf) (CC BY 4.0) | Raghu |
| 10:55-11:25<br>30 min | <span class="tag">General</span> <i data-icon="router-network"></i> **[Building a home network with OpenWRT and other open-source software](https://pretalx.coscup.org/coscup-2026/talk/CNNASG/)**<br><i data-icon="arrow-right-bottom"></i> Advanced router setups that consumer gear lacks: VLAN isolation, multi-WAN, site-to-site VPN, and Tor as upstream<br><i data-icon="presentation"></i> [Slides (PDF)](https://assets.anoni.net/event/coscup-2026/pellaeon-openwrt-home-network.pdf) (all rights reserved, view only) | Pellaeon |
| 11:30-12:00<br>30 min | <span class="tag">Payments</span> <i data-icon="fingerprint"></i> **[Open-standard real-identity methods on blockchain networks](https://pretalx.coscup.org/coscup-2026/talk/ZV88PP/)**<br><i data-icon="arrow-right-bottom"></i> After Taiwan passed its virtual asset service provider law, which open standards could be used to locate Taiwanese users' identities on-chain | Yusef Schultz |

(12:00–13:00 lunch)

**Afternoon 13:00–16:00 (room `TR-510`)**

| Time | Session | Speaker |
|------|---------|---------|
| 13:00-13:30<br>30 min | <span class="tag">Tor Relay</span> <i data-icon="simple-torproject"></i> **[Growing onions on campus? Running an academic Tor node at NTNU and lessons from the EFF Tor University Challenge](https://pretalx.coscup.org/coscup-2026/talk/7AP8HY/)**<br><i data-icon="arrow-right-bottom"></i> The full story of standing up an academic Tor relay, from technical configuration to campus policy<br><i data-icon="presentation"></i> [Slides (PDF)](https://assets.anoni.net/event/coscup-2026/nz-tor-relay-on-campus.pdf) <i data-icon="video-outline"></i> [Recording (Google Drive)](https://drive.google.com/file/d/1bAzgU6rSNg9hXSrDhDIXYd4PM-P8Dxte/view?usp=sharing) | NZ |
| 13:35-14:25<br>50 min | <span class="tag">Privacy</span> <i data-icon="eye-off-outline"></i> **[Browser tracking, anti-tracking strategies, and user autonomy](https://pretalx.coscup.org/coscup-2026/talk/KSWEDB/)**<br><i data-icon="arrow-right-bottom"></i> How an everyday browser gets fingerprinted and may leak who you contact, and how to push back<br><i data-icon="presentation"></i> [Slides (PDF)](https://assets.anoni.net/event/coscup-2026/pellaeon-browser-tracking-and-user-autonomy.pdf) (all rights reserved, view only) | Pellaeon |
| 14:30-15:00<br>30 min | <span class="tag">Privacy</span> <i data-icon="database-lock"></i> **[After the health-insurance database case: exercising the right to stop secondary use, and other large databases](https://pretalx.coscup.org/coscup-2026/talk/GEKJRV/)**<br><i data-icon="arrow-right-bottom"></i> From the opt-out lawsuit to the amended law, and how to exercise the right over your own medical data<br><i data-icon="presentation"></i> [Slides (PDF)](https://assets.anoni.net/event/coscup-2026/kuan-nhi-database-right-to-opt-out.pdf) | Kuan-Ju Chou |
| 15:05-15:55<br>50 min | <span class="tag">Privacy</span> <i data-icon="shield-account-outline"></i> **[Privacy guide 2026](https://pretalx.coscup.org/coscup-2026/talk/K8BYBU/)**<br><i data-icon="arrow-right-bottom"></i> From a personal risk matrix, to NGO and newsroom preparation for legal data requests, to threshold signatures and MPC<br><i data-icon="presentation"></i> [Slides (PDF)](https://assets.anoni.net/event/coscup-2026/justyn-privacy-guides-2026.pdf) | Justyn |

## <i data-icon="handshake"></i> Cross-community collaboration with ETHTaipei { #cross-community }

In 2026 we partnered with [ETHTaipei](https://ethtaipei.org/) (the Taipei Ethereum Community) on programming. The Aug 8 afternoon "Anonymous Payments" session was aimed at both people working on digital rights and blockchain developers: NGOs and journalists could learn the privacy risks of donations and money flows, while developers heard about protocol-level zero-knowledge proofs and stealth-address implementations. During the call for proposals, application-oriented and introductory talks went to the Anonymity Networks Community track, and technical and protocol-level talks could move to the ETHTaipei blockchain track (see the joint review section of the [COSCUP 2026 Call for Proposals](/events/coscup-2026-cfp/#anoni-netxETHTaipei)). Attendees could move freely between the two tracks.

## <i data-icon="account-voice"></i> Speakers { #speakers }

The first three Aug 8 morning primers were led by anoni.net community members, people who run Tor relays and work on the Traditional Chinese localization and bug reports for Tails and OONI (more on the community in [About anoni.net](/about/)). The invited, co-organized and accepted speakers are listed below in program order; each name links to the full bio the speaker provided on COSCUP pretalx, except Raghu and Pellaeon, whose names link to their own website and blog at their request.

**Aug 8 morning · invited talk**

- **[Denken Chen](https://pretalx.coscup.org/coscup-2026/speaker/FW9HYA/)**: over ten years in software development and writing; works on the W3C Decentralized Identifiers and Verifiable Credentials standards, takes part in the Credentials Community Group and in Taiwan's digital identity wallet, and started the Ptt-iOS and Taiwan E-Book Search open-source projects. Spoke on "Drugs that aren't drugs, laundering that isn't laundering: on anonymous eligibility verification", and co-presented "Age verification, digital surveillance, and privacy: before we debate any of it, how about open source first?" with mashbean in the Aug 9 Open Source Policy track.

**Aug 8 afternoon · ETHTaipei "Anonymous Payments" session**

- **[Ya-wen Jeng (Vivian Jeng)](https://pretalx.coscup.org/coscup-2026/speaker/KBPWBX/)**: on the Privacy Stewards of Ethereum team at the Ethereum Foundation, focused on zero-knowledge proofs and privacy tech; led the Mopro and Unirep open-source tools. Spoke on "Zero-knowledge proofs and Citizen Digital Certificate identity verification".
- **[ryanycw (Ryan Wang)](https://pretalx.coscup.org/coscup-2026/speaker/8WM9UR/)**: DeFi developer and ETHTaipei co-organizer, interested in privacy, tech and Ethereum. Spoke on "The Privacy-preserving Identity Pipeline in KYC".
- **[Jennifer HSU](https://pretalx.coscup.org/coscup-2026/speaker/ZJ98MX/)**: works at the self-custodial privacy wallet Fluidkey and founded the XueDAO developer community in Taiwan. Spoke on "Starting from unlinkability: how stealth addresses solve on-chain financial privacy".
- **[mashbean](https://pretalx.coscup.org/coscup-2026/speaker/ZMHFCQ/)**: focused on decentralized tech and digital self-sovereignty; GM of Matters and former security-systems engineer at Taiwan's Ministry of Digital Affairs, and at the time of the event a Harvard policy visiting fellow and an Ethereum Foundation Silviculture member. Spoke on "I don't launder money — so why understand anonymous payments?".
- **[Liangcc (CC)](https://pretalx.coscup.org/coscup-2026/speaker/UYKEPE/)**: builds zero-knowledge applications in the Ethereum ecosystem; interested in the humanities, economics and cryptographic proofs. Ran the "Hands-on private payments workshop".

**Aug 9 · Day 2 sessions**

- **[Raghu](https://saxrag.com/)**: backend engineer working in networking (IP, TCP, packet analysis) and security research. Spoke on "The Workings of the Internet" (in English).
- **[Pellaeon](https://nyllep.wordpress.com/)**: digital security researcher and trainer focused on digital rights and FOSS. Spoke on "Building a home network with OpenWRT" and "Browser tracking, anti-tracking strategies, and user autonomy".
- **[Yusef Schultz](https://pretalx.coscup.org/coscup-2026/speaker/FAGUY7/)**: spoke on "Open-standard real-identity methods on blockchain networks"; full bio on pretalx.
- **[NZ (En-Li Su)](https://pretalx.coscup.org/coscup-2026/speaker/WCJNBL/)**: a CS student at NTNU maintaining the first Tor relay on the Taiwan Academic Network (TANet), interested in security and internet governance. Spoke on "Growing onions on campus? Running an academic Tor node at NTNU".
- **[Kuan-Ju Chou](https://pretalx.coscup.org/coscup-2026/speaker/UAREZS/)**: works on digital rights at the Taiwan Association for Human Rights. Spoke on "After the health-insurance database case".
- **[Justyn](https://pretalx.coscup.org/coscup-2026/speaker/WZGMJG/)**: spoke on "Privacy guide 2026"; the pretalx speaker page has no bio.

## <i data-icon="link-variant"></i> Related links

- [COSCUP 2026 Call for Proposals](/events/coscup-2026-cfp/): topics, cross-community collaboration, and how to submit
- [Anonymous Network Workshop 2025/08](/events/workshop-2025/): the two-day workshop and roundtables of 2025
- [Continuing from 2025 into 2026: Personal Privacy Guidelines, Tor Relay Campus Deployment Competition, and Exploration of Anonymous Payments](/updates/2026/01/2025to2026/)
- [About anoni.net](/about/)
- [Take part](/join/): the entry point for helping with Tor, OONI, translation or running a relay
- [Contributing to the Tor Project](/join/tor-project/): ways to take part in the upstream Tor Project

!!! info "Official schedule and event updates"

    The [official COSCUP schedule](https://pretalx.coscup.org/coscup-2026/) is the authoritative record of session times and titles. To hear about our future events, see [Stay informed](/contact/).
