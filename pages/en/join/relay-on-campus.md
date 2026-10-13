---
title: Tor Relays on Campus Track
description: One of anoni.net's three tracks for 2026, on running Tor relays at universities in Taiwan, with the goals, the National Taiwan Normal University case, the proposal and deployment templates, and how to take part.
---

Getting Tor relays onto university campuses is one of anoni.net's three tracks for 2026, alongside the [personal privacy guide](/join/privacy-guide/) and [anonymous payments](/join/payments-research/). We are deploying relays at universities in Taiwan and turning the proposal, the conversations with the institution, the technical setup, and ongoing operation into templates, so each campus that follows spends less effort getting there. Students, alumni, staff, and anyone with network operations experience are welcome to join (see [ways to take part](#Ways-to-take-part)).

## Campuses as a starting point

Tor's anonymity rests on a diverse set of relays. When most of them concentrate in a few countries or a few hosting providers, Tor's resistance to traffic analysis weakens. Taiwan's relay count is small: as of June 2026, Tor Metrics showed roughly 15 running relays, against more than a thousand in Germany and several thousand in the United States. The figure moves, and live numbers are on [Tor Relay Watch](/projects/pulse/).

Universities are a good place to close that gap:

- **Stable bandwidth**: academic networks generally have plenty of it
- **Technical people on site**: computer science and information management departments and campus IT centres have the skills to deploy and operate a relay
- **A clear institutional process**: a university has formal proposal and review procedures, which make the purpose easier to explain and support easier to obtain than it would be for an individual or a small company
- **Educational value**: the deployment itself is a teaching setting for anonymity networks, security, and open source governance
- **An international programme**: through EFF's [Tor University Challenge](https://toruniversity.eff.org/), campuses in Taiwan join a global network of university relays

## Goals for 2026

- **A campus deployment SOP**: the full process from proposal, through talking to the university, technical setup, and going live, to ongoing operation (published with the template kit in May 2026)
- **Response templates and a case library**: reference answers for the frequent questions about legal exposure, bandwidth use, and purpose
- **Approaching other universities**, building on the first case at National Taiwan Normal University
- **A channel to EFF and the Tor Project**, feeding cases from Taiwan back into the global programme
- **Live observation** of campus nodes through [Tor Relay Watch](/projects/pulse/)
- **Pairing with campus security events**: building relay deployment into security awareness campaigns, orientation talks, and similar occasions

## Related articles

- **The case**: [setting up a Tor relay at National Taiwan Normal University](/updates/2025/12/ntnu-nz/), an account of working the proposal through the institution
- **International**: our guest post on the Tor Project blog, [Setting Up a Tor University Relay in Taiwan](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/)
- **Setup guides**: [Tor Relay Setup Guide](/join/setup-tor-relay/), [Tor WebTunnel Bridge Setup Guide](/join/setup-tor-webtunnel/)
- **Observation**: [Tor Relay Watch](/projects/pulse/)
- **Concepts**: [What Is Tor?](docs:tools/what-is-tor/), [Tor Snowflake](docs:tools/tor-snowflake/)
- **Further reading**: [A Server That Forgets](docs:blog/2026/04/a-server-that-forgets-exploring-stateless-relays/), on stateless relays

## Done so far

- **The first campus relay**: running at the IT centre of the Department of Computer Science and Information Engineering, National Taiwan Normal University, deployed by community member NZ after working the proposal through faculty and staff
- **A guest post on the Tor Project blog**: the case written up in English and [published on the Tor Project blog](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/), where organizers in other countries can read it
- **Tor University Challenge in Traditional Chinese**: the [EFF Tor University Challenge site](https://toruniversity.eff.org/) translated into Traditional Chinese, lowering the language barrier for other universities in Taiwan
- **Tor Relay Watch live**: [the watch page](/projects/pulse/) shows relays in Taiwan and fourteen other nearby regions, updated hourly
- **The case interview**: the deployment recorded as a [long-form interview](/updates/2025/12/ntnu-nz/) for whoever goes next
- **The template kit**: the experience turned into a proposal document, a technical SOP, and an FAQ for university administrators, which other universities can adopt directly (see [the announcement](/updates/2026/05/2026-campus-tor-relay-template-kit/) and the next section)

## The template kit

The kit is assembled from NZ's work at National Taiwan Normal University. Students elsewhere do not have to start from nothing: they can copy the templates, adapt them to their institution, and take them into its review process.

- [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/): the proposal document, four communication emails, and the administrative timeline
- [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/): `torrc`, UFW firewall rules, the status page, monitoring, and an incident runbook
- [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/): the concerns universities raise, with answers and notes on the Taiwan context

Start with the [interview](/updates/2025/12/ntnu-nz/) for the whole picture, then read the template that matches your role. Proposers read the proposal template, operators read the SOP, and anyone heading into a meeting with the university brings the FAQ.

## Work in progress

- **Approaching other universities**: initial contact and assessment
- **Pairing with security events**: models for working with security weeks, orientation talks, and hackathons
- **Policy material**: programme descriptions and cross-country comparisons for the Ministry of Education level
- **Translating outside resources**: candidates are listed in the next section

## Translation candidates and further reading

We have marked a few outside resources as translation candidates, and volunteers are welcome to translate them or summarize the key points:

- [Tor Project relay operator guides](https://community.torproject.org/relay/): the Tor Project's official operational documentation
- [Tor University Challenge case studies](https://toruniversity.eff.org/case-studies/): campus cases from other countries
- [EFF legal FAQ for Tor relay operators](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/): legal questions around running a relay
- Campus Tor relay policies from universities in other countries (MIT, Stanford, CMU, and others)

## Ways to take part

Discussion happens on Matrix (homeserver `im.anoni.net`), with the campus relay conversations in the relevant rooms of the community's public Space. Account requests and service entry points are on [Services](/services/).

Backgrounds we would particularly welcome:

- **Students, alumni, and staff**: you understand your own institution and can assess whether a relay is feasible there
- **Network operations experience**: technical setup and long-term operation
- **Policy communication**: working with the university administration, the IT centre, and legal counsel
- **Legal expertise**: interpreting the legal questions relay operation raises, including personal data, criminal liability, and institutional rules
- **Event organizing**: folding deployment work into security weeks, orientation, and other campus events

Having run a relay before is not required. Wanting to learn is reason enough, and we will work through the [Tor Relay Setup Guide](/join/setup-tor-relay/) with you.

## Ground rules

All discussion presumes lawful use. This track is about education, research, and taking part in network infrastructure, and does not assist unlawful conduct. Campus deployment uses institutional resources, so it goes through the formal proposal and review process, with the node's purpose and the operational responsibilities fully explained to the university.
