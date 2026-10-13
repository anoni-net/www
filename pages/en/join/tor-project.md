---
title: Contributing to the Tor Project
description: The Tor Project's plans and active projects, its official channels, practical ways for a regional community to contribute, and how anoni.net's work relates to Tor.
---

The Tor Project, which maintains the Tor onion routing network, is a non-profit with public governance. Most of its communication channels, source code, and planning documents are open, and an individual can start contributing through translation, running a relay, or hosting a meetup without representing any organization. Over the past year of promoting Tor, Tails (the amnesic live operating system), and OONI (the Open Observatory of Network Interference), the question we at anoni.net, a community based in Taiwan, hear most is how to take part in Tor upstream.

Regional measurement data can go to the Tor team that maintains network health, and every new relay in the Asia-Pacific spreads the network across more addresses. The Traditional Chinese translation of Tor's documentation also needs people to keep it current with every release. Where a step has a guide on the docs site, it links there.

!!! tip "The two lowest-barrier ways to contribute"

    The first is proofreading the Traditional Chinese translation of Tor's support documentation on Weblate. `zh_Hant` is largely complete, so the work is keeping up with changes to the source ([Tor new-support-portal](https://hosted.weblate.org/projects/tor/new-support-portal/), process in [localization and translation](docs:community/i18n/)). The second is introducing yourself on the Tor forum and in `#tor-project:matrix.org`. Neither needs anyone's approval and both can be done as an individual. Any formal collaboration later builds on that record of contributions.

## Tor's public planning documents

The Tor Project publishes its plans at two levels: strategy for a general audience on its blog, and detailed planning for contributors in a self-hosted GitLab wiki.

Each year the Tor Project publishes an annual direction post on [its blog](https://blog.torproject.org/), setting out that year's priorities. For 2026 the focus is integrating censorship circumvention into more Tor software, such as Tails and Tor VPN, while continuing to track states such as Russia and China that wall off their own networks[^1]. Its year in review lists four long-term areas: performance and security, network health, censorship resistance, and compatibility with third-party integrations[^2]. In the financial reports, the US government's share of funding falls from 53.5% in FY2021-22 to 35.08% in FY2023-24, in line with a goal of depending less on any single funder[^3]. State of the Onion, the online assembly, usually takes place at the end of the year; in 2025 it ran as two sessions, a team update in November and a community update in December, and it is the single best place to follow the year's direction[^4].

Detailed planning is on [Tor's GitLab](https://gitlab.torproject.org/tpo), where public projects can be read without an account. Each team's `team` meta project keeps roadmaps and meeting notes in its wiki, and the sponsored projects across the organization are collected on the Sponsors overview page in `tpo/team`[^5]. The system administration team's (TPA) annual roadmap is the most concrete of them[^6], and Arti's milestones are on issues in the group carrying the Roadmap label[^7]. The milestones endpoint requires a login and scheduled dates are not available through the public API, so they have to be traced through the links embedded in each wiki.

## Current directions and active projects

This section was checked in June 2026. Tor's projects and funding change quickly, and the official announcements take precedence. None of this technical detail is needed to contribute; to go straight to what you can do, see [ways to contribute](#ways-to-contribute).

### Project activity

Tor's GitLab holds more than two hundred projects, with widely varying activity. A scan of the public API in June 2026 found about 252 non-archived projects, of which about 103 had activity in the previous 30 days. network-health was the most active, and web, core, tpa, and applications also had many projects under active development[^8]. The numbers change over time; sorting GitLab by `last_activity_at` shows the current state.

### Technical threads

- **Censorship-resistant transports**: WebTunnel disguises bridge traffic as ordinary HTTPS and was an important circumvention tool in Russia during 2025. Snowflake uses volunteers' browsers as temporary proxies over WebRTC (the technology browsers use for real-time connections with each other) and runs stably; see [Tor Snowflake](docs:tools/tor-snowflake/). Conjure uses address space that ISPs leave unused, countering censors who list known proxy addresses and block them one by one, with a phased rollout planned from 2026[^9].
- **Arti**, Tor rewritten in Rust. The client core, circuits, and onion services are stable, while relay and directory authority (the core servers that maintain the list of relays) support are still in development. The project has not committed to a timeline for feature parity with the older C implementation.
- **Counter Galois Onion (CGO)**, a new symmetric encryption scheme that fixes weaknesses in the old one, under which traffic could be tampered with and used to trace connections. It is marked experimental in Arti and will be enabled by default once testing is complete.
- **Tor VPN for Android**, built on Arti and in beta since September 2025. The project marks it as experimental and unsuitable for high-risk situations. On iOS, Orbot remains the option.
- **Onion services**, including usability and abuse resistance, and the integration of Tails since it joined the Tor Project; see [what is Tails](docs:tools/what-is-tails/).

### Sponsored projects and lasting directions

Funding is the clearest indication of which directions will continue. The table lists some of the sponsored projects on the Sponsors overview page[^5], numbered with an `S` prefix.

| Sponsor | Direction | Relevance to anoni.net |
|---|---|---|
| `S96` | Censorship circumvention for China, Hong Kong, and Tibet, including new pluggable transports, harder-to-block bridges, and better bridge distribution | The circumvention questions we follow |
| `S112` | Countering malicious relays and improving network health, including monitoring tools, a code of conduct for relay operators, and resistance to relay attacks | Our measurement work |
| `S119` | Arti, Tor rewritten in Rust | The next technical foundation |
| `S150` | Retiring BridgeDB in favour of the RDSys distribution system | How bridges are distributed |
| `S101` | Tor VPN for Android | A product for general users |
| `S131` | Refactoring Mullvad Browser and Tor Browser | Browsers |

`S96` and `S112` are closest to our work: the first covers the censorship that Chinese-speaking users face across the region, and the second matches the reachability measurement we run.

## Official channels

Tor bridges IRC on the OFTC network with Matrix in both directions, so joining through Element or through IRC leads to the same channel[^10]. These official channels are on `matrix.org` and are separate from `im.anoni.net`, the Matrix server we host for our own community.

| Channel | Purpose |
|---|---|
| `#tor` | User support and questions about using Tor |
| `#tor-dev` | Development, protocol, and code discussion |
| `#tor-project` | Organizational and community matters, meetups, outreach |
| `#tor-relays` | The relay operator community |
| `#tor-l10n` | Translation and localization |
| `#tor-meeting` | Observing or joining team meetings with public minutes |

Written discussion and announcements are on the [Tor Forum](https://forum.torproject.org/), a Discourse forum with categories for user support, localization, events, and more. Mailing lists can be subscribed to at [lists.torproject.org](https://lists.torproject.org/). Organizational matters go by email: non-profit business, trademarks, and partnership coordination to <frontdesk@torproject.org>, speaker invitations to <speaking@torproject.org>, and security issues to <security@torproject.org>.

Before joining any of these, read Tor's [community policies and code of conduct](https://community.torproject.org/policies/).

## Ways to contribute

These are ordered by how feasible each is for a regional community, with a link wherever the docs site has a guide.

1. **Localization**: The lowest barrier, needing no account review and no technical background. An individual can start on Weblate right away and improve the Traditional Chinese at the same time, and it is the fastest way to build a record of contributions. The process and the Weblate links are in the Tor translation section of [localization and translation](docs:community/i18n/); first-time contributors should read [becoming a Tor translator](https://community.torproject.org/localization/becoming-tor-translator/).
2. **An introduction in `#tor-project` and on the forum**: Meetups, outreach, and community matters are discussed there, and any formal collaboration starts there too.
3. **A local meetup**: Tor's [outreach programme](https://community.torproject.org/outreach/) provides a Street Team Kit, slides, and material for hosting a Tor meetup. The project encourages independent meetups and they need no approval. To request a speaker, write to <speaking@torproject.org>.
4. **A relay or a bridge**: Members with a machine and bandwidth can run a relay and add to Asia-Pacific coverage; the steps are in [how to run a Tor relay](docs:community/setup-tor-relay/). For a bridge disguised as HTTPS, see [setting up Tor WebTunnel](docs:community/setup-tor-webtunnel/). Help is available in `#tor-relays` and on the tor-relays mailing list.
5. **Development and bug reports**: [anonticket.torproject.org](https://anonticket.torproject.org/) lets you request a GitLab account or file a report anonymously; with an account, issues go on the relevant repository. Newcomers can start with issues labelled first-contributors, and technical discussion happens in `#tor-dev`.
6. **Training partnership**: Tor's [training partners](https://community.torproject.org/training/partners/) programme is the most formal arrangement between an organization and the project. It usually follows a record of contributions in the areas above, and suits a medium-term goal.

## anoni.net's work and its links to Tor

- **Traditional Chinese translation and terminology**: We already maintain `zh_Hant` translation and terminology standards, which carry over directly to Tor's translations on Weblate.
- **Reachability measurement**: [Tor Relay Watch](/projects/pulse/) (Pulse) and [OONI Coverage](/projects/asn-coverage/) (ASN Coverage), both run by the community, correspond to the network-health team's work and to `S112`, and their results can be shared at that team's community sessions.
- **Campus relays**: The [Tor Relays on Campus Track](/join/relay-on-campus/) grew out of the Tor University Challenge, a campaign by EFF with the Tor Project. National Taiwan Normal University already runs a relay; see [the interview](/updates/2025/12/ntnu-nz/).

How this work fits the community's annual plan is in the [2026 roadmap](/join/roadmap-2026/). The community session of State of the Onion has an open call for updates from local communities, and that is where we can report this work internationally.

## Related reading

- [Localization and translation](docs:community/i18n/): how Tor's documentation is translated, and how to use Weblate
- [How to run a Tor relay](docs:community/setup-tor-relay/): the steps for running a relay
- [Setting up Tor WebTunnel](docs:community/setup-tor-webtunnel/): running a bridge disguised as ordinary HTTPS
- [Take part](/join/): ways to join anoni.net and take on a yearly theme

[^1]: [Advancing digital rights in 2026](https://blog.torproject.org/advancing-digital-rights-in-2026/), The Tor Project Blog
[^2]: [The Tor Project's 2024 year in review](https://blog.torproject.org/2024-year-in-review/), The Tor Project Blog
[^3]: [The Tor Project financial reports for July 2023 to June 2024](https://blog.torproject.org/financials-blog-post-2023-2024/), The Tor Project Blog
[^4]: [State of the Onion 2025](https://blog.torproject.org/state-of-the-onion-2025/), The Tor Project Blog
[^5]: [tpo/team wiki: sponsors overview](https://gitlab.torproject.org/tpo/team/-/wikis/Projects/Sponsors-2023), Tor Project GitLab
[^6]: [tpo/tpa/team wiki: roadmap/2025](https://gitlab.torproject.org/tpo/tpa/team/-/wikis/roadmap/2025), Tor Project GitLab
[^7]: [Roadmap-tagged issues in the tpo group](https://gitlab.torproject.org/groups/tpo/-/issues/?label_name[]=Roadmap&state=opened), Tor Project GitLab
[^8]: [Tor Project GitLab public API](https://gitlab.torproject.org/api/v4/groups/tpo/projects?include_subgroups=true), activity snapshot of non-archived projects scanned in June 2026
[^9]: [Staying ahead of the censors in 2025](https://blog.torproject.org/staying-ahead-of-censors-2025/), The Tor Project Blog
[^10]: [Chat with the Tor community](https://support.torproject.org/get-in-touch/chat-with-us/), Tor Project Support
