---
title: About anoni.net
description: A community of open-source technologists based in Taiwan, covering the Sinophone Asia-Pacific, with our 2026 tracks, monitoring projects, governance, partners and publications.
---

We are anoni.net, a community of open-source technologists based in Taiwan, working from a civic-tech angle to put privacy and anonymity technology into practical use. We promote open-source tools such as Tor, Tails and OONI, run Tor relays and the services the community itself relies on, and write our own monitoring tools to follow network conditions in Taiwan and nearby regions.

We cover the Sinophone (Chinese-speaking) Asia-Pacific: Mainland China, Hong Kong, Macau, Singapore, Malaysia and Taiwan, plus the diaspora moving between them. Taiwan is the only place we can speak about first-hand. We follow the others through public sources and contacts there, and we mark the pages that rest on second-hand material.

<!-- diagram-regions -->

Most English-language privacy resources assume a Western threat model, and few of them compare places within this region. We document how the same tool behaves in Mainland China and in Taiwan and how a local statute changes the threat model, and we take measurements from inside the region.

## Community profile

- **Volunteers**: There is no salaried staff. Contributors produce this site, Tor Relay Watch, OONI Coverage and the regional translations in their own time, some under pseudonyms.
- **Based in Taipei**: The active core is in Taipei. We hope to bring in contributors from elsewhere in the region, and for now our exchange with collaborators outside Taiwan is occasional and informal.
- **Self-hosted infrastructure**: We run our own Matrix homeserver (`im.anoni.net`) and instances of CryptPad, Etherpad, Send, SearXNG and Formbricks, and we coordinate internally on these instead of third-party platforms (see [Services](/services/)).
- **Chinese first**: The Traditional Chinese (zh-TW) edition is the source of truth, with a re-localized Simplified Chinese (zh-CN) edition alongside it. The English edition of the documentation site is written separately rather than translated line by line, as plain-language guides with the regional context of the Sinophone Asia-Pacific built in.

## Origins

The community formed around 2023 to answer one question: how completely OONI's database covers each of Taiwan's networks (ASNs, autonomous system numbers). That study is now [OONI Coverage](/projects/asn-coverage/). The scope has since widened to regional observation, regulatory tracking, selective translation of regional research, and promoting and building anonymity tools. In August 2025 we held the [Anonymous Network Workshop](/events/workshop-2025/) at National Taiwan University of Science and Technology, where the first community members joined and the work for 2026 took shape.

<!-- diagram-history -->

## 2026 tracks

Most of this year's work falls under three tracks. The full plan, the quarterly deliverables and current status are in the [2026 Roadmap](/join/roadmap-2026/).

<!-- diagram-community -->

- **[Personal Privacy Guide Track](/join/privacy-guide/)**: practical tools and steps graded by exposure (everyday use, sensitive work, high-risk situations), published across the concepts, tools and scenarios sections of the docs site.
- **[Tor Relays on Campus Track](/join/relay-on-campus/)**: part of EFF's Tor University Challenge. A relay runs at National Taiwan Normal University (NTNU), set up by a community member who worked the proposal through faculty and staff. We turned the NTNU case into three templates: the [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/), the [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/) and the [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/). Each keeps its Taiwan-specific material in a separate regional note, so organizers in another jurisdiction can replace those parts and reuse the proposal structure, the outreach emails and the technical steps.
- **[Anonymous Payments Track](/join/payments-research/)**: still at the research stage. We are collecting real situations, such as who needs to pay anonymously and in what circumstances, where current practice breaks down, and what limits regulation and compliance impose. Anonymous payments were also the theme of our booth at [Global Gathering 2026](/updates/2026/08/2026-anoni-net-global-gathering/) in Estoril, Portugal, on 6 September 2026.

To join one of the tracks, see [Take part](/join/).

## Monitoring projects

We build our own monitoring tools, and all of them are open source. The full list is on [Projects](/projects/).

- **[Tor Relay Watch](/projects/pulse/) (Pulse)**: hourly tracking of Tor relays in Taiwan and fourteen other regions, with running status, version, ASN, relay role and flag distributions. Pulse is a FastAPI and PostgreSQL service with a REST API and a Vega-Lite chart API at [anoni.net/api](https://anoni.net/api/readme).
- **[OONI Coverage](/projects/asn-coverage/) (ASN Coverage)**: a coverage page on this site that sets OONI measurement counts against each network's estimated users, backed by a Python CLI that batch-processes OONI's public S3 data to map per-ASN observation completeness across regions. We use it to find under-observed networks and to compare regions.
- **[Tor relay lookup for AI assistants](/projects/onionoo-mcp/) (onionoo MCP)**: a hosted query service for Tor relay data. `onionoo-fastapi` wraps the Tor Project's [Onionoo](https://metrics.torproject.org/onionoo.html) API in an HTTP interface described by OpenAPI and in an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server, so an AI assistant can answer "how many Tor relays is Taiwan running right now" from live public data instead of from memory. The service runs at [onionoo.anoni.net](https://onionoo.anoni.net/docs), with source at [github.com/anoni-net/onionoo-fastapi](https://github.com/anoni-net/onionoo-fastapi).
- **[Quarterly Reports](/projects/reports/)**: each quarter's Tor relay and OONI coverage figures fixed in place, compared with the start of the quarter and with the quarter before, together with our reading of the numbers.

We also publish measurement write-ups built from public data, so that others can recheck them. On 13 August 2026, during an announced national resilience exercise, mobile networks in seven northern counties of Taiwan were throttled for 30 minutes. The date, the window, the counties and the carriers were all public before it ran, a condition studies of throttling rarely get. OONI recorded 238 connection speed tests from 47 devices in Taiwan that day, and during the window one Chunghwa Telecom Mobile handset measured 788 to 1,709 kbit/s, a range never before seen in Taiwan's public data. Six records from a single device are not enough for a national conclusion. Every query in [our write-up of the drill](docs:blog/2026/08/ooni-mobile-throttle-drill-results/) runs without an API key, so anyone can recheck the whole chain.

## Publications

- **anoni.net Docs**: the documentation site in three editions (zh-TW, zh-CN, en), with practical guides for readers new to privacy tools. It is hosted at [anoni.net/docs](https://anoni.net/docs/), with a Tor onion mirror at [docs.anoninetru5tflukgfaehun7q6khowgmymcff3gtk5oyesqazhmfxtyd.onion](http://docs.anoninetru5tflukgfaehun7q6khowgmymcff3gtk5oyesqazhmfxtyd.onion/) and source at [github.com/anoni-net/docs](https://github.com/anoni-net/docs).
- **Translated regional reports**: full Traditional Chinese translations of two reports so far, the 2025 InterSecLab report on the Geedge Networks / MESA Lab leak and the MADLink report on the Taiwanese link in the Geedge supply chain, both in the zh-TW edition. We add translations case by case, when a regional report fills a gap in Chinese-language coverage. InterSecLab's originals and our translations are both linked from the English [Curated Reports](docs:reports/) index.
- **Community updates and blog posts**: [Updates](/updates/) on community work and conference participation (RightsCon, COSCUP, ETHTaipei), and translated upstream announcements from the Tor Project, OONI and Tails on the [docs site's blog](docs:blog/).

## Governance

The community works by consensus with little formal structure. The full rules are in the [Governance Charter](/about/governance/), which is still a draft under community review and serves as the working reference until it is ratified.

- **Roles**: *core members* (long-term maintainers who operate the self-hosted services and can merge PRs), *contributors* (anyone with active output), *observers* (newsletter and Public Space participants) and *visitors* (anyone reading and writing to `whisper@anoni.net`).
- **Decisions**: consensus by default, with a 3-day window for objections. A vote happens only when consensus is blocked or time is short. Major decisions, such as charter changes and adding core members, need the support of two-thirds of all eligible voters, that is, contributors active in the last six months.
- **Disputes**: substantive disputes go through the proposal process, and interpersonal disputes go to core members. Severe cases (harassment, threats) lead to immediate removal of access, with case-by-case support for the people affected.
- **Code of conduct**: mutual respect across backgrounds, technical levels and politics, discussion about ideas rather than identities, transparency in public rooms, and an explicit refusal to assist illegal activity (money laundering, harassment, CSAM, foreign-state intelligence operations).

Decision history and significant changes are visible in the commit log of the [docs repository](https://github.com/anoni-net/docs) and in [Updates](/updates/).

## Partnerships and collaborations

We list an organization here only when the work went both ways: joint work, beyond citing them or attending their events.

- **[Tor Project](https://torproject.org/)**: translation contributions, [Snowflake](https://snowflake.torproject.org/) bridge support, and ongoing campus relay deployment in Taiwan. The NTNU relay was the subject of our guest post on the Tor Project blog in March 2026, [Setting Up a Tor University Relay in Taiwan](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/).
- **[OONI](https://ooni.org/)**: running OONI Probe in Taiwan, contributing to the regional websites test list, and translating OONI's methodology and announcements into Chinese for the community.
- **[Electronic Frontier Foundation](https://www.eff.org/)**: collaboration on the Tor relays on campus track, and the Traditional Chinese translation of the [Tor University Challenge](https://toruniversity.eff.org/zh-tw/), a joint EFF and Tor Project initiative.
- **University hosts**: National Taiwan Normal University (Tor relay deployment) and National Taiwan University of Science and Technology (venue for the 2025 Anonymous Network Workshop).

We credit collaborators explicitly and do not claim work that is not ours. Organizations thinking about working with us can find what we can and cannot take on in [Working with Organizations](/about/partners/).

## Other engagement

The following do not meet the bar above, but they are part of the community's public record.

- **[InterSecLab](https://www.interseclab.org/), independent translation**: We translated the 2025 Geedge Networks / MESA Lab leak report into Traditional Chinese in full and published it with attribution. It was our own translation of a public report, with no formal collaboration with InterSecLab.
- **[g0v](https://g0v.tw/), community participation**: Members take part in g0v's recurring hackathons in Taipei, presenting and discussing anoni.net work. This is attendance and informal coordination rather than an organizational partnership.
- **Conferences and convenings**: Members took part in RightsCon, COSCUP and ETHTaipei in 2025 and 2026. Recaps, and recordings where they exist, are in [Updates](/updates/).

## Funding and resources

The community is volunteer-run and has no external funding. Core members cover the operating costs: domain registration, server hosting for Matrix and the docs site, and conference travel. We are not set up to receive grants or donations, and we would want to talk with potential funders before setting that up.

Funders interested in network-freedom work across the Sinophone Asia-Pacific are welcome to reach us through the channels on [Take part](/join/).

## Licenses

Each part of the project has its own license:

- **Documentation site content** ([github.com/anoni-net/docs](https://github.com/anoni-net/docs)): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), free to share and adapt with attribution
- **Tor Relay Watch code, Pulse** ([github.com/anoni-net/pulse](https://github.com/anoni-net/pulse)): [MIT License](https://github.com/anoni-net/pulse/blob/main/LICENSE)
- **OONI Coverage code, ASN Coverage** ([github.com/anoni-net/asn-coverage](https://github.com/anoni-net/asn-coverage)): [GPL-3.0](https://github.com/anoni-net/asn-coverage/blob/main/LICENSE)
- **Tor relay lookup code, onionoo-fastapi** ([github.com/anoni-net/onionoo-fastapi](https://github.com/anoni-net/onionoo-fastapi)): [MIT License](https://github.com/anoni-net/onionoo-fastapi/blob/main/LICENSE)

To credit reused documentation, write "anoni.net Docs Project, [URL of the specific page], CC BY 4.0."

The logo, wordmark and colour tokens, with the rules for using them, are on [Brand Assets](/brand/).

## Verifiable records

Readers can check the following without relying on anything this page claims:

- The source of the documentation site, Tor Relay Watch (Pulse), OONI Coverage (ASN Coverage) and Tor relay lookup for AI assistants (onionoo-fastapi) is public at [github.com/anoni-net/docs](https://github.com/anoni-net/docs), [github.com/anoni-net/pulse](https://github.com/anoni-net/pulse), [github.com/anoni-net/asn-coverage](https://github.com/anoni-net/asn-coverage) and [github.com/anoni-net/onionoo-fastapi](https://github.com/anoni-net/onionoo-fastapi), with commit history and contributor lists
- Tor Relay Watch data is publicly readable at [anoni.net/api](https://anoni.net/api/readme), and the hosted onionoo service at [onionoo.anoni.net](https://onionoo.anoni.net/docs) accepts unauthenticated requests, so any result from it can be re-run
- The numbers behind each quarterly report are on [GitHub](https://github.com/anoni-net/www/tree/main/data/reports)
- The Tor onion mirror at [the docs onion address](http://docs.anoninetru5tflukgfaehun7q6khowgmymcff3gtk5oyesqazhmfxtyd.onion/) carries the same content as the clearnet site
- An IPFS mirror of the same content is at [ipfs.anoni.net](https://ipfs.anoni.net/), for readers who cannot reach the clearnet site. The DNSLink record `_dnslink.anoni.net` points at the same IPNS name, so any DNSLink-capable gateway serves the same mirror
- Community work and external participation are documented in [Updates](/updates/), with photos and recordings where available

## Contact channels

- **Matrix** (preferred for ongoing collaboration): the Public Space is [`#community:im.anoni.net`](https://matrix.to/#/#community:im.anoni.net). We run our own homeserver and approve accounts one by one, so request an account at `whisper@anoni.net`.
- **Encrypted email**: `whisper@anoni.net`, with the PGP key on [Stay informed](/contact/)
- **Newsletter**: sign up on [Stay informed](/contact/)
- **GitHub**: issues and PRs at [github.com/anoni-net/docs](https://github.com/anoni-net/docs)

For introductions, partnerships or research collaboration, the right channel for each purpose is listed on [Take part](/join/).
