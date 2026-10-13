---
title: Campus Tor Relay FAQ for University Administrators and Legal Counsel
description: The ten concerns university IT centres, legal offices, and network administrators most often raise about a campus Tor relay, with suggested responses and two one-page summaries.
---

When a Tor relay is proposed on campus, the IT centre, legal counsel, and network operations tend to raise the same ten concerns. This page derives from the [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/), adds a regional note to each answer, and works as an appendix to a proposal or as reading sent ahead of a meeting.

The FAQ at the end of the [Tor Relay Setup Guide](/join/setup-tor-relay/) is written for individual operators. This page is written for university administration, legal counsel, and network operations, so it focuses on institutional risk and on how to answer when someone asks.

The regional notes come from the first campus relay in Taiwan and from Taiwanese law. The general answers apply anywhere. A proposer elsewhere should replace the regional notes with their own jurisdiction's equivalents.

## Ways to Use This FAQ

- **With a proposal**: attach it as the first appendix
- **Before a meeting**: send it to the IT centre, network operations, and legal counsel to read first
- **When asked**: open the relevant question and quote it
- **The two one-page summaries at the end**: 30-second versions, for the top of an email or as a handout in a meeting

## Common Concerns

??? question "Why is a university a good place for a Tor relay?"

    Academic networks have stable bandwidth, and computer science departments, security groups, and IT centres already have the people to deploy and operate a relay. A deployment can start from the lowest-risk configuration, a non-exit relay, which never handles exit traffic and draws no complaints about outbound connections. The node can be stopped at any time, so the decision is reversible. Deploying and operating it is itself a teaching case in anonymity networks, security, and open source governance. For an institution that values academic freedom and access to information, it puts that commitment into infrastructure.

    **Regional note**

    Taiwan's first case is at the Department of Computer Science and Information Engineering of National Taiwan Normal University, live since November 2025. The process is described in a [guest post on the Tor Project blog](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/) and in a [community interview](/updates/2025/12/ntnu-nz/). Taiwan's universities already teach computer science, information security, and network governance, and a campus Tor relay gives those courses a working example.

??? question "We do not want to run an exit relay. Is that acceptable?"

    Yes. The Tor network needs every type of relay to stay healthy. By default, a relay acts as a guard (entry) or middle relay and only forwards encrypted traffic between Tor nodes. Guard and middle relays are the lowest-maintenance form, and they draw no complaints about exit traffic.

    You can also run a bridge or a [Tor Snowflake](docs:tools/tor-snowflake/) proxy alongside it, to help users in censored regions reach Tor.

    **Regional note**

    The Taiwanese campus case is a non-exit relay. Every campus relay project in Taiwan should start as non-exit and should not attempt an exit relay, whose legal and administrative costs exceed what an individual or a student group can carry.

??? question "I am willing to run a relay but do not want to handle abuse. How does that work?"

    Exit policy exists for exactly that. Every Tor relay has one, specifying which outbound connections it permits or refuses. The policy is published through the directory service, and Tor clients automatically avoid exit relays that would refuse their connections. Each relay decides which services, hosts, and networks it allows, based on abuse risk and its own circumstances.

    The default exit policy permits many common services such as web browsing, while restricting services with a high abuse risk such as mail, and services the Tor network cannot absorb such as the default file-sharing ports.

    If you permit any outbound connections, make sure DNS resolution works correctly.

    **Regional note**

    For a campus deployment the simplest approach is `ExitPolicy reject *:*`, which refuses all outbound connections. No traffic exits through the relay, so abuse complaints essentially do not occur, though keeping EFF's abuse response templates on hand is still sensible. The configuration is in the [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/#torrc-reference-configuration).

??? question "Doesn't Tor help criminals?"

    Tor's mission is to advance human rights and to help people resist mass surveillance and censorship through free, open source technology. The Tor community has always condemned the use of its tools for unlawful ends.

    Criminal intent belongs to people, not to tools. Encryption, telephones, and cash are all used maliciously, and Tor is no different. Removing Tor would move malicious actors to other tools rather than stop them.

    At the same time, Tor and other privacy tools protect the people who need them, guarding against crimes such as identity theft and physical stalking, and they help law enforcement investigate cases and support victims.

    **Regional note**

    Chapter 36 of Taiwan's Criminal Code, offences against computer use (Articles 358 to 363), addresses specific conduct, such as entering another person's account credentials without authority to intrude into their computer (Article 358), and obtaining, deleting, or altering the electromagnetic records on another person's computer without authority (Article 359). A middle relay does not touch content, does not parse user data, and does not know who its users are, which makes it comparable to network transmission infrastructure and places it outside the elements of those offences.

    Article 2 of Taiwan's Personal Data Protection Act defines personal data as data that can identify an individual directly or indirectly. A middle relay handles encrypted Tor cells with no identifying data, so no personal data processing is involved. When a relay is chosen as an entry guard, it does see the IP address of the connecting client, though not where that client is going, and Tor's default logging (`SafeLogging 1`) scrubs addresses from its logs. Whether an IP address counts as personal data depends on whether it can be matched with other data to identify a specific person, a point worth raising with legal counsel as well.

    This is the community's reading, not formal legal advice. For legal concerns about a specific situation, consult a lawyer.

??? question "What about distributed denial of service attacks?"

    DDoS attacks generally rely on thousands of machines sending UDP packets at once to saturate a victim's bandwidth.

    Tor carries only well-formed TCP connections, not arbitrary IP packets, so it cannot send UDP packets or perform attacks such as SYN floods. The common DDoS techniques do not work through Tor.

    Tor also does not permit bandwidth amplification: what goes in is what comes out. An attacker with enough bandwidth to mount a DDoS has no need to route it through Tor.

    **Regional note**

    There is no record of a Taiwanese ISP issuing a DDoS complaint against a middle relay, and the relay at National Taiwan Normal University has received no DDoS reports since going live in November 2025.

??? question "What about spam?"

    Tor's default exit policy refuses all SMTP traffic on port 25, so spam cannot be sent through Tor directly.

    A few relays may enable SMTP, which carries the same risk as running an open mail server and is not a risk specific to Tor. Spammers can also connect through Tor to an open HTTP proxy, exploit insecure CGI scripts, or control a botnet, all of which they can do without Tor.

    Many spam techniques, such as forged UDP packets, do not work through Tor at all, because Tor carries only TCP.

    **Regional note**

    With `ExitPolicy reject *:*` in place, SMTP traffic does not leave the relay either, so spam is not a concern for a campus non-exit relay.

??? question "Is Tor frequently abused?"

    Tor uses exit policies to reduce abuse risk, with each relay deciding which services it permits or refuses and publishing that to clients. The Tor Project also has a dedicated network health team that investigates malicious relays and removes them from the network.

    Tor is deliberately designed so that neither the Tor Project nor relay operators can monitor user behaviour. That design is what lets Tor provide strong privacy and anonymity for human rights workers, journalists, domestic violence survivors, whistleblowers, and law enforcement.

    **Regional note**

    For a campus non-exit relay the concept of abuse essentially does not apply, because the node never touches the content a user is ultimately reaching. All traffic through it is encrypted forwarding between Tor nodes, with at least one further relay between it and any external site.

??? question "What happens if we do run an exit relay?"

    A relay that permits outbound connections will sooner or later receive abuse complaints, for example:

    - Someone uses Tor to reach Hotmail and send a ransom note, and law enforcement such as the FBI contacts you. An explanation is generally accepted
    - Someone uses Tor to spam Google Groups, and your ISP receives a complaint
    - Someone uses Tor to cause trouble on IRC, and your server may be hit with a DDoS
    - Someone uses Tor to download a pirated film, and your ISP may receive a DMCA infringement notice. Responding with EFF's recommended template generally leaves no legal liability

    ISPs differ in how they treat exit relays: some cooperate, others are stricter. Some websites also block exit relay IP addresses, which is common. If you run an exit relay, use a dedicated IP address that does not affect other services.

    **Regional note**

    Running an exit relay on a campus in Taiwan is strongly discouraged. Outbound connectivity on Taiwan's academic network (TANet) goes through Ministry of Education review, and an exit relay's unpredictable traffic does not fit that framework. There is also no precedent to cite, which raises the cost of every conversation, and a student or society lead generally cannot carry the possible legal or administrative consequences.

    Anyone interested in exit relays should try one on a personal VPS with a Tor-friendly hosting provider overseas, and keep institutional resources out of it.

??? question "How do we respond to an ISP complaint?"

    The Tor community maintains complete response templates that relay operators can use when replying to an ISP, in the [EFF Tor legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/) and the [Tor abuse templates](https://community.torproject.org/relay/community-resources/tor-abuse-templates/).

    **Regional note**

    A campus non-exit relay never communicates directly with external sites, so in principle it receives no ISP complaints. If one arrives anyway, for instance from someone who assumes the relay is an exit, respond as follows:

    1. Confirm the time of the reported incident and the destination IP address or URL
    2. Provide a screenshot of your `ContactInfo` and `ExitPolicy reject *:*` settings
    3. Cite the [Tor Project's description of relay types](https://community.torproject.org/relay/types-of-relays/): a non-exit relay forwards encrypted traffic within the Tor network and does not connect to final destinations
    4. Bring in your supervising faculty member or the university's legal office if needed

??? question "How does Tor handle misuse of the technology?"

    The Tor Project condemns any criminal misuse of its technology and acts against malicious behaviour where it can, for example by blocking malicious relays.

    By design, Tor cannot monitor or prohibit user behaviour. The design can be exploited, but more often it protects the people who need it: human rights workers, journalists, domestic violence survivors, whistleblowers, law enforcement officers, and others who need privacy.

    **Regional note**

    Public attention in Taiwan to whistleblower protection, the prevention of domestic violence and stalking, and press freedom has grown in recent years. Tor's value to users in Taiwan in these situations matches its value elsewhere, and a campus relay is a concrete contribution to making that infrastructure available in Taiwan.

    Further reading: [Taiwan's Whistleblower Protection Act, from a Technical Angle](docs:regional/taiwan-whistleblower-law/) and [Domestic violence and tech-enabled abuse — digital safety for survivors](docs:scenarios/domestic-violence/).

## One-Page Summary for Network Administrators { #summary-for-network-administrators }

!!! info "30-Second Summary for Network and IT Centre Staff"

    **Node type**

    - A Tor relay (middle node), not an exit node
    - Forwards encrypted traffic within the Tor network only, with no direct communication with external sites

    **Deployment requirements**

    - One static IPv4 address
    - One inbound TCP port (ORPort 9001, or 443)
    - Optionally port 80 or 443 for a status page
    - All other ports closed

    **What does not happen**

    - No parsing or logging of user traffic
    - No abuse complaints, on a non-exit relay
    - No additional load on the campus border firewall
    - No effect on campus DNS or content filtering policy

    **Reversibility**

    - Can be taken offline within 10 minutes by stopping the systemd service
    - Removable at any time with no effect on the campus network

    **Precedent**

    - Universities worldwide run relays, including MIT, Stanford, Cambridge, and Carnegie Mellon
    - The first case in Taiwan: [National Taiwan Normal University, live since November 2025](/updates/2025/12/ntnu-nz/)
    - The international programme: [EFF Tor University Challenge](https://toruniversity.eff.org/)

## One-Page Summary for Administration and Legal Counsel { #summary-for-administration-and-legal }

!!! info "30-Second Summary for University Administration and Legal Counsel"

    **Background**

    Running a Tor relay on campus means taking part in the Tor University Challenge, an international programme run by the Electronic Frontier Foundation (EFF). Universities worldwide participate, including MIT, Stanford, Cambridge, and Carnegie Mellon.

    **Legal position**

    - What is deployed is a non-exit relay, legally comparable to network transmission infrastructure
    - It does not touch user content and does not identify personal data
    - It falls outside the elements of the offences against computer use in Taiwan's Criminal Code and of the Personal Data Protection Act (the community's reading, not formal legal advice)
    - EFF provides legal and technical resources

    **Value to the institution**

    - A concrete commitment to information freedom and privacy, expressed in infrastructure
    - A place on the Tor University Challenge's international list of participating universities
    - Teaching: a case study for computer science, information security, and network governance
    - Research: material for network research and coursework

    **Operational impact**

    - Can be taken offline at any time, within 10 minutes
    - Operated jointly by students and supervising faculty, with a low administrative burden
    - No changes required to the existing campus firewall or content filtering policy

    **Reference cases**

    - In Taiwan: [National Taiwan Normal University, live since November 2025](/updates/2025/12/ntnu-nz/)
    - Internationally: [Setting Up a Tor University Relay in Taiwan](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/), on the Tor Project blog

!!! tip "Next Steps"

    Continue from where you are:

    - **No proposal written yet**: go back to the [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/), adapt it for your institution, and attach this page
    - **Proposal approved**: follow the [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/) for the technical work
    - **Just asked about Tor relays**: forward the [summary for network administrators](#summary-for-network-administrators) or the [summary for administration and legal counsel](#summary-for-administration-and-legal)

## Related Reading

- [Tor Relays on Campus Track](/join/relay-on-campus/): the entry point to the three templates and the track's progress
- [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/): a proposal document for other institutions to adapt
- [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/): the technical detail on torrc, UFW, monitoring, and incident response
- [Setting Up a Tor Relay at National Taiwan Normal University](/updates/2025/12/ntnu-nz/): the full account of the first case in Taiwan
- [EFF Tor legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/): a complete legal FAQ based on US law

## Sources and Acknowledgements

The ten questions at the core of this page come from community member 蘇恩立 (NZ), drawn from the original proposal document at National Taiwan Normal University. The regional notes were added by anoni.net. The original material is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) with NZ's agreement.
