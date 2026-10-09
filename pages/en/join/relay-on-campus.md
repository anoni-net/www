---
title: Tor Relays on Campus Track
description: One of the community's three 2026 tracks — getting Tor relays running at universities in Taiwan, the template kit built from the first case, and how to join.
---

Getting Tor relays onto university campuses is one of anoni.net's three tracks for 2026, alongside the [personal privacy guide](/join/privacy-guide/) and [anonymous payments](/join/payments-research/). This page is the track's public entry point, covering the goals, the article index, the cases accumulated so far, and how to join.

## Why campuses

Tor's anonymity rests on **a diverse set of relays**. When most of them concentrate in a few countries or a few hosting providers, Tor's resistance to traffic analysis weakens.

Taiwan's relay count is small. As of June 2026, Tor Metrics showed roughly 15 running relays, against thousands in Germany and the United States, so the room for growth in diversity is substantial. The figure moves, and live observation is on the [Tor relay watcher](docs:regional/tor-relay-watcher/).

Universities are a good place to close that gap:

- **Stable bandwidth**: academic networks generally have plenty of it
- **Technical people on site**: computer science departments and IT centres have the skills to deploy and operate
- **Clearer institutional process**: a university has a formal proposal and review process, which makes the purpose easier to explain and support easier to obtain than it would be for an individual or a small company
- **Educational value**: the deployment itself is a concrete teaching setting for anonymity networks, security, and open source governance
- **International connection**: through EFF's [Tor University Challenge](https://toruniversity.eff.org/), bringing campuses in Taiwan into a global network of deployments

What the community is building is a reproducible method: the full deployment process, response templates for talking to a university, and real operational experience, so the second and third campus cost significantly less effort than the first.

## Goals for 2026

- **A campus deployment standard operating procedure**: from proposal, through talking to the university, technical setup, going live, and ongoing operation
- **Response templates and a case library**: reference answers for the frequent questions about legal exposure, bandwidth use, and purpose
- **Approaching a second and third university**, extending from the first case
- **A channel to EFF and the Tor Project**, feeding cases from Taiwan back into the global programme
- **Live observation** of campus nodes through [Pulse](https://anoni.net/api/readme)
- **Pairing with campus security events**: integrating relay deployment into security weeks, orientation talks, and similar occasions

## Related articles

- **The case**: [setting up a Tor relay at National Taiwan Normal University](docs:blog/2025/12/ntnu-nz/), an account of working the proposal through the institution
- **International**: [our guest post on the Tor Project blog](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)
- **Technical how-to**: [how to run a Tor relay](docs:community/setup-tor-relay/), [how to run a Tor WebTunnel bridge](docs:community/setup-tor-webtunnel/)
- **Observation**: [Tor relay watcher](docs:regional/tor-relay-watcher/)
- **Concepts**: [what is Tor](docs:tools/what-is-tor/), [Tor Snowflake](docs:tools/tor-snowflake/)

## Done so far

- **The first campus case is running**: the Tor relay at the Computer Science and Information Engineering department's IT centre at National Taiwan Normal University, deployed by community member NZ after working the proposal through faculty and staff
- **A guest post on the Tor Project blog**: the case written up in English and [published upstream](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/), putting it in front of a global audience
- **Tor University Challenge translated**: the [EFF site](https://toruniversity.eff.org/) translated into Traditional Chinese, lowering the language barrier for other universities in Taiwan
- **Pulse observation live**: the [Tor relay watcher](docs:regional/tor-relay-watcher/) shows relay activity across Taiwan, Japan, South Korea, and Hong Kong in real time
- **An interview**: the full deployment story recorded as a [long-form interview](docs:blog/2025/12/ntnu-nz/) for whoever goes next
- **The template kit**: the experience turned into a proposal document, a technical SOP, and an FAQ for university administrators, all reusable as-is

## The template kit

Assembled from NZ's work at National Taiwan Normal University, the kit exists to make **the second and third campus cheap**. Students elsewhere can copy the templates, adapt them, and take them into their own institution's review process.

- [Campus Tor relay proposal template](docs:community/campus-tor-relay-proposal/): the proposal document, four communication emails, and the administrative timeline
- [Campus Tor relay deployment SOP](docs:community/campus-tor-relay-sop/): `torrc`, firewall rules, the status page, monitoring, and an incident runbook
- [Campus Tor relay FAQ for administrators and legal counsel](docs:community/campus-relay-faq/): the questions universities ask, with answers

Suggested reading order: start with the [interview](docs:blog/2025/12/ntnu-nz/) for the whole picture, then pick the file matching your role. Proposers read the proposal template, operators read the SOP, and anyone heading into a meeting with the university brings the FAQ.

## In progress

- **Approaching a second university**: initial contact and assessment
- **Pairing with security events**: models for working with security weeks, orientation talks, and hackathons
- **Policy material**: programme descriptions and cross-country comparisons at ministry level
- Translation candidates, listed below

## Reading and translation candidates

- [Tor Project relay operator guides](https://community.torproject.org/relay/): the official operational documentation
- [Tor University Challenge case studies](https://toruniversity.eff.org/case-studies/): campus cases internationally
- [EFF legal FAQ for Tor relay operators](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)
- Campus Tor relay policy cases from universities elsewhere

## How to join

Discussion happens on Matrix (homeserver `im.anoni.net`), in the relevant rooms of the community's public Space. Account requests and service entry points are on [Community services](/services/).

Backgrounds we would particularly welcome:

- **Students, alumni, and staff**: you understand your own institution and can assess whether this is feasible there
- **Network operations experience**: for technical setup and long-term operation
- **Policy communication**: helping with the university, the IT centre, and legal counsel
- **Legal expertise**: reading the questions relay operation raises, including personal data, criminal exposure, and institutional rules
- **Event organizing**: folding deployment work into security weeks and orientation events

Having run a relay before is not required. Wanting to learn is a sufficient reason, and [how to run a Tor relay](docs:community/setup-tor-relay/) is there to work through with you.

If you are at Global Gathering 2026 in Estoril and your institution is weighing a relay, come and compare notes at our booth on 6 September. Details are in [the booth announcement](docs:blog/2026/08/2026-anoni-net-global-gathering/).

## Ground rules

All discussion presumes lawful use. This track is presented for education, research, and infrastructure participation, and does not assist unlawful conduct. Campus deployment uses institutional resources, so it goes through the formal proposal and review process, with the node's purpose and the operational responsibilities fully disclosed to the university.
