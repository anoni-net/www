---
title: 2026 Roadmap
description: The anoni.net community's three tracks for 2026, the quarterly documentation schedule, events, outside collaboration, technical projects, and ways to get involved.
---

In 2026 the anoni.net community, based in Taiwan, continues its local advocacy for Tor (the onion routing network), Tails (the amnesic live operating system), and OONI (the Open Observatory of Network Interference), and takes on three new tracks: a personal privacy guide, Tor relays on university campuses, and anonymous payments. We review delivery at the end of each quarter and adjust the next one accordingly.

The 2025 retrospective and the background to how 2026 was scoped are in [Continuing from 2025 into 2026](/updates/2026/01/2025to2026/).

## Three thematic tracks

### Personal privacy guide

While promoting Tor, Tails, and OONI in 2025, the question we heard most often was "what do I actually do next to be safer". Answering it takes a practical privacy guide graded by situation. The guide covers tools and steps at three levels of exposure (everyday use, sensitive work, and high-risk situations), written up across the [Concepts](docs:basics/), [Tools](docs:tools/), and [Scenarios](docs:scenarios/) sections of the docs site.

The article index and current status are on the [Personal Privacy Guide Track](/join/privacy-guide/) page.

### Tor relays on university campuses

This track follows from the [Tor University Challenge](https://toruniversity.eff.org/), an EFF campaign to get stable relays running at higher education institutions. The IT centre of the Computer Science and Information Engineering department at National Taiwan Normal University runs a Tor relay, set up after a community member took the proposal through faculty and staff. The full account is in [Setting Up a Tor Relay at National Taiwan Normal University](/updates/2025/12/ntnu-nz/).

In 2025 we completed the Traditional Chinese translation of the Tor University Challenge site, and in 2026 we are taking the process onto campuses. In May 2026 the NTNU experience was published as three templates, a proposal, a setup SOP, and an FAQ for the university, which other schools can adapt to their own circumstances.

The templates, cases, and ways to join are on the [Tor Relays on Campus Track](/join/relay-on-campus/) page. The technical steps are in the [Tor Relay Setup Guide](/join/setup-tor-relay/).

### Anonymous payments

Cash is the most mature anonymous payment method, and it runs into clear limits across borders, online, and when an organization needs to receive donations. Within the bounds of the law, the community is researching what on-chain tools can do here, covering cryptocurrencies, stablecoins, zero-knowledge identity verification, and multi-signature setups. We have not found a systematic body of Chinese-language material on the subject, so the work starts with research and builds towards implementation guidance.

The article index and current status are on the [Anonymous Payments Track](/join/payments-research/) page.

## Quarterly documentation schedule

The Guides section of the docs site is divided into five sub-groups: concepts, tools, scenarios, advanced topics, and reports. Through 2026 we fill them in quarter by quarter.

The schedule below covers the site as a whole, where Traditional Chinese is the source of truth. The English site is a curated track carrying a subset of it, so several items land in Chinese first and reach English in a later batch. Where a section named here has no English equivalent yet, that is why.

- **Q1 (complete)**: core [concepts](docs:basics/) first, local regulatory coverage ([Taiwan's 2025 Data Protection Overhaul](docs:regional/taiwan-pdpa-2025/) on the Personal Data Protection Act of Taiwan, and [Taiwan's 2026 Virtual Asset Service Act](docs:regional/taiwan-vasp-2026/) on the virtual asset service provider regime), the [Emergency Help](docs:help/) page, community governance, and this roadmap
- **Q2 (first drafts published)**: in the tools layer, Tor Browser advanced settings, a comparison of anonymity operating systems, a comparison of messaging tools, password managers, and the cryptocurrency privacy spectrum, plus end-to-end encryption in the advanced layer, all under ongoing revision
- **Q3 (first drafts published)**: the scenarios layer (journalists, activists, survivors of domestic violence, LGBTQ+ people, election observers, among others), post-quantum cryptography and decentralized website publishing in the advanced layer, and a technical look at Taiwan's whistleblower protection act
- **Q4 (in progress)**: the draft [Governance Charter](/about/governance/) and the [Contributor Handbook](docs:community/contributor-handbook/) are published, and the annual retrospective follows at the end of the year

Actual progress depends on volunteer writing capacity.

## Events

### COSCUP 2026

Building on our 2025 experience at COSCUP (the Conference for Open Source Coders, Users, and Promoters, Taiwan's largest annual open source conference), the community ran a track again on 8 and 9 August 2026 at National Taiwan University of Science and Technology. The anonymous payments session, organized jointly with [ETHTaipei](https://ethtaipei.org/), ran on the afternoon of 8 August in room `TR-511`. The full program is on the [COSCUP 2026 Anonymity Networks Community track](/events/coscup-2026/) page, and the call for proposals that preceded it is at [COSCUP 2026 Call for Proposals](/events/coscup-2026-cfp/).

### Workshops and meetups

Following the [Anonymous Network Workshop 2025/08](/events/workshop-2025/) at National Taiwan University of Science and Technology, we schedule in-person workshops and online meetups through 2026 as topics mature and partners ask for them. The audiences include news organizations, independent journalists, civil society groups, technical communities, and interested members of the public.

## Outside collaboration

### Research and report translation

In the second half of 2025 we translated and shared InterSecLab's report on the export of China's censorship technology, [The Internet Coup](https://anoni.net/docs/reports/interseclab-network-coup/) (the translation is on the Traditional Chinese docs site only). Through 2026 we continue to select international reports with local relevance for translation and annotation, collected under [Curated Reports](docs:reports/).

### Participation in other events

Community members regularly attend local open source, civil society, and privacy events, such as hackathons, annual conferences, topic meetups, and talks. Most of the time this is individuals or community representatives exchanging views and following the context of an issue, an informal kind of contact. Formal collaboration, such as joint calls for proposals, report translation partnerships, or co-organized events, is announced on the [Events](/events/) page once it is confirmed.

## Technical projects

The community also develops and maintains several technical projects related to Tor, OONI, and password security:

- **[Tor Relay Watch](/projects/pulse/) (Pulse)**: Tor relay data collection and an API, built on FastAPI and PostgreSQL
- **[OONI Coverage](/projects/asn-coverage/) (ASN Coverage)**: a batch analysis tool over OONI's public data, with background in [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/)
- **Asian Diceware**: an EFF-compatible 7776-word passphrase list that blends in dictionary-attested Asian loanwords. The community plans its own anonymous service platform along the lines of the Tor Project's anonymous support ticketing service [AnonTicket](https://anonticket.torproject.org/), and the list is meant to serve as the source of its account codes. See [Asian Diceware, an Asian-flavored passphrase wordlist](docs:tools/asian-diceware/).

The code and issue trackers for the three projects are on GitHub at [anoni-net/pulse](https://github.com/anoni-net/pulse), [anoni-net/asn-coverage](https://github.com/anoni-net/asn-coverage), and [anoni-net/asian-diceware](https://github.com/anoni-net/asian-diceware). How the two observation tools relate to the work of the Tor Project's network-health team is covered in [Contributing to the Tor Project](/join/tor-project/).

## Ways to get involved

You do not need a technical background. Pick whichever entry point fits:

- **Following the issues and the community**: subscribe to the newsletter (see [Stay informed](/contact/)) and join Matrix
- **Translation and writing**: see [Localization and Translation](docs:community/i18n/) and [Take part](/join/)
- **Working out how deep you want to go technically**: see the [Self-skills evaluation form](docs:community/skill-level/)
- **Understanding the collaboration tools**: see the community's [Services](/services/)

Discussion happens mainly on Matrix (homeserver `im.anoni.net`), collaborative writing on CryptPad, and calls on Jitsi. Account requests and the entry points for each service are also on the [Services](/services/) page.

## Roadmap updates

We review and adjust the roadmap at the end of each quarter. Significant changes go through the community proposal process, set out in the [Governance Charter](/about/governance/), and are announced on Matrix.

**Last updated**: October 2026, with Q4 in progress.
