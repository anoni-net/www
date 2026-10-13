---
title: Working with Organizations
description: How civil-society groups, advocacy organizations, newsrooms and researchers can work with anoni.net, what we cannot take on, and how a collaboration runs.
---

anoni.net is a volunteer community based in Taiwan. What we can offer organizations is mostly public documentation, one-off workshops, and self-hosted services, plus the regional layer: localization, local context, and measurement from inside Taiwan. This page is for civil-society groups, advocacy organizations, newsrooms, independent media, and researchers whose work touches the Sinophone Asia-Pacific.

Taiwan is the only jurisdiction where we have first-hand standing. Mainland China, Hong Kong, Macau, Singapore, and Malaysia we follow through public sources and local contacts, and wherever a piece of work rests on second-hand material we say so. Some of what follows uses Taiwan as the example, so organizations elsewhere should weigh it against their own situation.

Apart from the public projects listed under [Partnerships and collaborations](/about/#Partnerships-and-collaborations) on the About page, we don't publish which organizations have worked with us, and no page describes the tools a particular organization uses. For advocacy groups and newsrooms, having asked a community for security training is itself something that can end up in a file.

## Organizations that fit

- Advocacy groups, social-service organizations, and research NGOs. The organizational groundwork is in the [Civil society](docs:start/civil-society/) starting path
- Newsrooms with an editorial desk, legal, and IT. The newsroom-level practices are in the [Newsrooms](docs:start/media/) starting path
- Independent media and one-person teams. The individual practices are in the [Independent journalists](docs:start/independent-journalist/) starting path
- International organizations, researchers, and funders covering Internet freedom in the region. Our regional pages start at the [Regional Observatory](docs:regional/)
- Universities considering a Tor relay. The campus track is the [Tor Relays on Campus Track](/join/relay-on-campus/)

## Ways to work together

### Staff training and device reviews

We can walk your staff through a device review. The procedure is in [Walking a new colleague through a device review](docs:utils/case-onboarding/): two people and an hour, answering three questions with the [Threat model checklist](docs:utils/threat-model/), then recording what comes next in [My preparation checklist](docs:utils/checklist/).

It runs as a one-off workshop built entirely from public pages on the docs site, which keep working offline once saved to a device. Sessions depend on volunteer time and follow no fixed schedule.

### Self-hosted services for collaboration

The Matrix, CryptPad, Etherpad, and Send instances the community self-hosts are all open for collaboration, and [Services](/services/) describes each one and how to get access. Etherpad and Send need no account, while Matrix and CryptPad accounts are created by hand on request by email.

The services are run by volunteers with no service-level commitment, so they suit collaboration better than being your organization's system of record. For exchanging sensitive files with us, see [Sending Us Sensitive Material](/join/upload-sensitive/).

### Newsroom intake channels

The trade-offs between Signal, SecureDrop, onion inboxes, and email aliases are covered in the first contact section of [Journalists and source protection](docs:scenarios/journalist/#First-contact). For an onion inbox, you can self-host one with the [Onion Service Setup Guide](/join/setup-onion-service/) or run a lighter version with [OnionShare](docs:tools/onionshare/). If you get stuck following the documentation, ask on Matrix or by email.

### Security update alerts

The person who handles security in an organization can subscribe to the Now and Soon feed only, and pass a Now item to the people it affects the same day. The details are in the security contacts section of the [Software Changelog](docs:changelog/#Security-contacts-in-organisations). We put upstream announcements from many sources on one rating scale, so your organization does not need someone to track them separately.

### Anonymous accounts of practice

What your organization runs into in practice can be sent anonymously to [whisper@anoni.net](mailto:whisper@anoni.net). We fold it into scenario pages or new starting paths on the docs site without identifying the organization or the people involved.

### Localization and translation review

We can translate and adapt security guides, tool documentation, interface strings, and reports into Traditional Chinese written for Taiwan, or review a Chinese translation you already have. Terms follow a shared glossary (see the terminology section of [Localization and Translation](docs:community/i18n/#Terminology-and-glossary-consistency)), and we write 正體中文 rather than 繁體中文 for the reasons in [Why We Say "Orthodox Chinese" Rather Than "Complex Chinese"](docs:community/zh-hant-naming/).

Our past translation work is public: upstream translations for the Tor Project, OONI, and CryptPad, the Traditional Chinese edition of the Tor University Challenge site, and full Traditional Chinese translations of two long-form regional reports, indexed in [Translated Reports](docs:reports/). Bringing regional research in the other direction, from Chinese into English, is part of the same work.

### Local context review

Before you publish a report, a guide, or an advocacy piece that touches Taiwan, we can read it for how it lands in Taiwan's legal and platform environment: which statutes apply, which platforms people actually use, which terms read naturally. Our regulatory explainers include [Taiwan's 2025 Data Protection Overhaul](docs:regional/taiwan-pdpa-2025/), [Taiwan's 2026 Virtual Asset Service Act](docs:regional/taiwan-vasp-2026/), [Taiwan's Whistleblower Protection Act, from a Technical Angle](docs:regional/taiwan-whistleblower-law/), and [Identity Binding and Taiwan's Data Market](docs:regional/taiwan-realname-data-market/), all linked from the [Regional Observatory](docs:regional/).

For other jurisdictions, we can point out where a draft conflicts with the public sources we follow, and we label that clearly as second-hand.

### Joint research

The community's three 2026 tracks, the [Personal Privacy Guide Track](/join/privacy-guide/), the [Anonymous Payments Track](/join/payments-research/), and the [Tor Relays on Campus Track](/join/relay-on-campus/), each publish their research goals and work in progress. Organizations can join one of those research questions or co-publish on a related one, just as individuals can.

We credit other people's work explicitly and don't claim a formal arrangement where none exists.

### Network measurement and citable data

We run OONI Probe in Taiwan and help maintain the [OONI Website Testing List](docs:regional/ooni-checklist/). If your organization's site fits one of the list's categories, write to us and we will review it for the next batch of list updates. Once it is on the list, its reachability across Taiwan's networks is measured and published over time.

When reporting on shutdowns, blocking, or Tor, or when research needs numbers, you can cite [How many people use Tor in Taiwan](docs:regional/taiwan-tor-users/), the [ASN observation data analysis](docs:regional/ooni-asn-coverage/), and [Tor Relay Watch](/projects/pulse/). The Taiwan Tor user figures can be reproduced from two public CSV files, and Tor Relay Watch updates hourly across 15 regions including Taiwan. To look up public relay data yourself, use the [Tor relay lookup for AI assistants](/projects/onionoo-mcp/). We are glad to explain how to read the numbers.

### Co-hosted events

The community has run a track at COSCUP two years in a row and has co-hosted sessions with other communities. Past events are on the [Events](/events/) page, and proposals for a joint session or workshop are welcome.

## Work we cannot take on

- **Incident response and device forensics**: For a compromised account or suspected spyware, start with [Emergency Help](docs:help/) on the docs site. International helplines, including Access Now, RSF, and CPJ, are listed in the regional angle section of [Journalists and source protection](docs:scenarios/journalist/#The-regional-angle-that-changes-the-advice)
- **Legal advice**: The regulatory pages on the docs site summarize and explain; they are not legal advice
- **Holding your data**: The self-hosted services are for collaboration, and your organization's records belong in systems you control
- **Long-term consulting or custom development**: Volunteer time is limited, so the work centers on public documentation and one-off workshops
- **First-hand work outside Taiwan**: Local context and observation for other jurisdictions come from public sources, and we cannot run measurements there ourselves

## The collaboration process

1. Write to [whisper@anoni.net](mailto:whisper@anoni.net) with the kind of organization you are and what you have in mind. If you need encryption, use the PGP key on [Stay informed](/contact/#pgp)
2. We reply and set up a call on Jitsi, which the community uses for its own meetings
3. Before the call, each side fills in the [Threat model checklist](docs:utils/threat-model/) and brings the copied summary
4. After the call, we agree on which pieces to take on, on a timeline set by volunteer availability

What you send us is used only to arrange the work. It is not passed to third parties and does not appear on any page of this site.

## Further reading

- [Take part](/join/): how individuals join the community's work
- [Services](/services/): what each service is for and how to get access
- [2026 Roadmap](/join/roadmap-2026/): the community's three tracks and events this year
- [About anoni.net](/about/): the partnerships we have and how we are funded
