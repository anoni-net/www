---
title: Campus Tor Relay Proposal Template
description: A campus Tor relay proposal document, four outreach emails, and an administrative timeline drawn from the National Taiwan Normal University case, ready to adapt for your own institution's review process.
---

Most of the time it takes to run a Tor relay at a university goes into the administrative process, about two months from the first conversation with a supervisor to a live relay. The proposal document, the four outreach emails, and the timeline on this page come from community member NZ's work at National Taiwan Normal University (NTNU), where NZ took the proposal through every stage of approval inside TANet, Taiwan's academic network, and brought up the first Tor relay on that network. The full account is in [the interview about setting up a Tor relay at NTNU](/updates/2025/12/ntnu-nz/).

To do the same at your institution, copy the template, replace each `<placeholder>` with your own details, and attach the [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/) and the [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/). Together they make a complete proposal.

!!! note "Schools outside Taiwan"

    The administrative structure here is Taiwan's: a university IT centre, a departmental network administrator, and an academic network with ministry-level oversight of outbound connectivity. The shape recurs across the region and beyond, with different names for the offices. The proposal body, the emails, and the common mistakes transfer directly. What needs replacing is the specific jurisdiction's legal framing and the names of the approving bodies.

## Contents and audience

- **Contents**: a proposal document, four outreach emails, a two-month administrative timeline, and the common mistakes
- **For**: students, research assistants, and staff at a university who want to run a Tor relay
- **Not included**: the technical installation steps (see the [deployment SOP](/join/relay-on-campus/sop/)) and the institutional concerns (see the [FAQ](/join/relay-on-campus/faq/))
- **Licence**: CC BY 4.0, so copy, modify, and submit it freely. Suggested attribution: "adapted from the anoni.net campus Tor relay template"

## Steps for using the template

1. Copy the proposal body below into Google Docs or Word
2. Search for `<` to find every placeholder and replace each one
3. Attach the [FAQ](/join/relay-on-campus/faq/) as appendix one
4. Attach the technical detail from the [SOP](/join/relay-on-campus/sop/) as appendix two
5. Ask a faculty member willing to sponsor it to review it with you
6. Submit it into your institution's review process

## Proposal body, ready to copy

??? example "Full proposal template"

    # Tor University Challenge at `<institution>`

    ## Project proposal

    **"Tor University Challenge" at `<institution>`**

    **Establishing a Tor relay at `<institution>`**

    ---

    **Project lead**: `<department>` `<student number>` `<name>`

    **Faculty supervisor**: `<supervisor name>`

    **Team**: `<student society or laboratory>`

    ---

    ### 1. Background

    This project responds to the Electronic Frontier Foundation's [Tor University Challenge](https://toruniversity.eff.org/), which encourages universities worldwide to run Tor relays in support of privacy, information security education, and academic research.

    Tor (The Onion Router) originated at the US Naval Research Laboratory and is now maintained by the non-profit Tor Project. Its principal uses:

    - Protecting user privacy and anonymity
    - Helping journalists protect their sources
    - Helping people in censored environments reach information
    - Supporting lawyers, patients, and researchers in sensitive communication

    Universities including MIT, Stanford, and Cambridge already run Tor relays. Taiwan's first case is at the Department of Computer Science and Information Engineering of National Taiwan Normal University, documented in a [Tor Project blog guest post](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/). Taking part would support this institution's teaching in computer science and put its commitment to information freedom and privacy into practice.

    ### 2. Scope

    #### 2.1 Type of relay

    - This project deploys a **non-exit relay** only, functioning as a guard or middle relay
    - A non-exit relay forwards encrypted traffic within the Tor network and never connects to external sites directly, so it rarely generates abuse complaints and carries far less legal risk than an exit relay

    #### 2.2 Resources required

    - **Server**: provided by `<supervisor, department, or self-provided>`
    - **Bandwidth**: the most the deployment location can provide, adjustable at the IT centre's request
    - **IP address**: one IPv4 address from the campus network. IPv6 can be requested separately for dual-stack
    - **Running costs**: rack space, power, and bandwidth come out of existing departmental capacity, with no separate budget line requested. Where your institution meters and cross-charges these internally, fill in the figures here

    #### 2.3 Operation

    - The project lead configures and maintains the relay
    - A Tor relay needs little maintenance, only monitoring once deployed
    - Removing it is straightforward and has no effect on the campus network
    - Before graduation, operation transfers to `<successor, society, or laboratory>`

    ### 3. Security and risk

    - **Low abuse risk**: a non-exit relay does not interact with external services, so it rarely receives abuse notices and carries far less legal risk than an exit relay
    - **Traffic stays within Tor**: data is encrypted and encapsulated before entering or leaving the campus network
    - **Lawful**: universities and research institutions worldwide participate, and EFF provides legal and technical resources
    - **Reversible at any time**: at the institution's request, the service stops and the port closes within 10 minutes

    Detailed responses to institutional concerns are in appendix one.

    ### 4. Academic and institutional value

    - **Education**: students learn how information security and anonymity networks work in practice
    - **Visibility**: shows the institution's commitment to information freedom and privacy through an international programme
    - **Research**: usable as a case study and teaching material
    - **International exchange**: connects the institution with other participating universities through EFF's Tor University Challenge

    ### 5. Process

    1. Present the requirement to the IT centre (this document)
    2. Confirm with the departmental network administrator that the network configuration is feasible
    3. Build and test on a laboratory server under faculty supervision
    4. Apply to open the ORPort externally (443 or 9001) once live
    5. Report node status to the supervisor and the IT centre periodically

    ### 6. Contact

    - **Project lead**: `<name>`, `<department>` `<year>`, `<email>`
    - **Team**: `<society or laboratory>`, `<team email>`
    - **Faculty supervisor**: `<supervisor name>`, `<supervisor email>`

    We would welcome the IT centre's consideration and support, and will provide any further explanation or technical detail required.

    ### Appendices

    - Appendix one, frequently asked questions: the [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/)
    - Appendix two, technical detail: the [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/)

## Typical administrative timeline

The timeline follows the actual process at NTNU, about two months from the first conversation with a supervisor to the node appearing in Relay Search. Every institution moves at its own pace, so treat the timings as reference rather than a commitment, and plan around holidays and exam periods.

| Stage | Approximate timing | Action |
|---|---|---|
| T+0 | Week 1 | Explain the plan to your project or thesis supervisor and get verbal support |
| T+1 week | Week 2 | Email the proposal to the head of the IT centre's network group |
| T+1 to 2 weeks | Weeks 2 to 3 | Prepare the next stage and borrow a machine from your supervisor for initial setup |
| T+2 to 3 weeks | Weeks 3 to 4 | Request rack space and one IPv4 address from the departmental network administrator |
| T+8 weeks | Week 9 | Schedule machine room access with the network administrator |
| T+9 weeks | Week 10 | Rack the machine and bring it online |
| T+9 weeks | Week 10 | The network administrator forwards the request to open external ports (9001, 443) to the IT centre |
| T+9 weeks | Week 10 | The node first appears in Tor Relay Search within hours |
| T+13 weeks | Week 14 | The node is listed on the EFF Tor University Challenge site |

The longest wait is usually between requesting rack space and getting into the machine room, because it depends on departmental resource scheduling and the IT centre's outbound connectivity review. Allow an extra two to three weeks.

## Email templates

The four emails match the four most common points of contact in the process. Keep the structure and adapt it to your own voice. Before sending, **replace every placeholder**, particularly email domains, supervisor names, and IP ranges.

??? note "Template one, to your supervisor (T+0)"

    **Subject**: Proposal to run a Tor relay at `<institution>`

    Dear `<supervisor>`,

    I am `<name>`, a `<year>` student in `<department>`, currently researching anonymity networks. I would like to propose running a **non-exit relay** at `<institution>` in response to EFF's Tor University Challenge ([https://toruniversity.eff.org/](https://toruniversity.eff.org/)).

    A non-exit relay forwards encrypted traffic within the Tor network and **does not communicate with external sites directly**, so it rarely attracts abuse complaints and carries far less legal risk than an exit relay. Universities including MIT, Stanford, and Cambridge participate, and National Taiwan Normal University's Department of Computer Science and Information Engineering was the first in Taiwan.

    If it goes ahead, I would:

    - Find a spare or self-provided machine, and I would welcome your thoughts on whether the department has suitable resources
    - Follow the IT centre's process for an outbound connectivity exception
    - Write a proposal document for the IT centre's review
    - Handle monitoring and maintenance once it is live

    Three questions:

    1. Would you be willing to act as supervisor for this project, so I can reference that when speaking to the IT centre?
    2. Is there a suitable machine available?
    3. Are there concerns I should address first?

    I have drafts of the proposal document and an FAQ, and can bring them to a meeting.

    `<name>`
    `<email>`

??? note "Template two, to the IT centre's network group (T+1 week)"

    **Subject**: Tor relay proposal for review, `<institution>`

    Dear `<head of network group>`,

    I am `<name>`, a `<year>` student in `<department>`, supervised by `<supervisor name>`. We would like to run a Tor relay in `<department or laboratory>`, in response to EFF's Tor University Challenge.

    **Summary**:

    - Type: a **non-exit relay**, forwarding encrypted traffic within the Tor network only, with no direct communication with external sites
    - Legal exposure: as a non-exit relay, it **rarely receives abuse notices and carries far less legal risk than an exit relay**
    - International precedent: MIT, Stanford, and Cambridge among others, with National Taiwan Normal University the first case in Taiwan
    - Operation: shared between myself and my supervisor, with the ability to go offline within 10 minutes

    The proposal, the FAQ, and the technical detail are attached:

    - Proposal: `<attachment or link>`
    - FAQ for administrators: `<attachment or link>`
    - Technical detail (configuration, firewall, monitoring): `<attachment or link>`

    If the IT centre has questions about any of it, I am happy to explain in person or provide further documentation.

    `<name>`
    `<email>`
    `<supervisor name>`
    `<supervisor email>`

??? note "Template three, requesting rack space and an IP address (T+2 to 3 weeks)"

    **Subject**: Request for rack space and one IPv4 address (Tor relay project)

    Dear `<network administrator>`,

    The IT centre has given preliminary approval to the Tor relay project proposed by `<supervisor name>` and myself (earlier correspondence attached). Moving to the hardware stage, I would like to request:

    1. **Rack space**: one 1U chassis or tower, to be placed in `<departmental machine room or laboratory>`
    2. **One static IPv4 address**: for the ORPort service

    Machine specification:

    - OS: Ubuntu Server 24.04 LTS
    - Services: Tor relay (non-exit) only, SSH restricted to the campus VPN range, and an Nginx status page
    - External ports: 9001/tcp (ORPort), 443/tcp (HTTPS status page) and 80/tcp (certificate issuance and redirects), everything else closed

    Please let me know when machine room access can be arranged.

    `<name>`
    `<email>`

??? note "Template four, opening external ports (T+9 weeks, forwarded to the IT centre by the network administrator)"

    **Subject**: Request to open external ports (Tor relay project, `<hostname or IP>`)

    Dear `<IT centre network group>`,

    The machine is online and tested. We now request the following ports be opened externally:

    | Port | Protocol | Purpose | Source |
    |---|---|---|---|
    | 9001 | TCP | Tor ORPort, TLS connections between relays | Anywhere |
    | 443 | TCP | HTTPS status page showing relay operation | Anywhere |
    | 80 | TCP | HTTP, for ACME challenge and a 301 redirect only | Anywhere |

    All other ports remain closed. SSH is restricted to the campus VPN range `<range>`.

    As a non-exit relay, this machine does not establish connections to external sites and forwards encrypted traffic within the Tor network only, so it **presents no abuse risk from outbound services**.

    Please let me know if anything further is needed.

    `<name>`
    `<email>`

## Preparation checklist

Handling these before you start saves a lot of back and forth:

- [ ] **Faculty sponsor**: find a faculty member willing to put their name to it. University administration treats a proposal with a named academic behind it very differently
- [ ] **Outbound connectivity policy**: check your institution's rules. Most universities block outbound by default, with exceptions requiring formal application
- [ ] **Machine**: a supervisor's laboratory, a spare departmental machine, or your own VM all work, since resource requirements are low
- [ ] **Project email address**: do not tie `ContactInfo` to a personal account. A society or project address survives graduation and makes handover easier
- [ ] **Handover after graduation**: a successor, joint society operation, or transfer to the laboratory all work, and the proposal should say which
- [ ] **Institutional concerns**: read the [FAQ](/join/relay-on-campus/faq/), so nothing in a meeting catches you out
- [ ] **Technical picture**: read the [SOP](/join/relay-on-campus/sop/), so you know what deployment and operation involve
- [ ] **Precedent**: read the [NTNU interview](/updates/2025/12/ntnu-nz/), for the tone of the conversations and where things went wrong

## Common mistakes

The places the NTNU case most often stalled:

- **Assuming technical correctness is enough**: on an academic network, the institution decides the outcome more often than the technology does, so be patient with the paperwork
- **Underestimating ministry oversight of the academic network**: most institutions block outbound by default, and an exception has to fit the reporting process
- **Not planning maintenance and accounts**: account permissions after graduation determine whether the node keeps running. **Do not tie `ContactInfo` to a personal address**
- **Overselling it**: do not describe Tor as something edgy or radical. Use language the institution can work with, so whoever approves it can answer for it later
- **Not distinguishing a relay from an exit node**: this matters more than anything else in the conversation. State explicitly that it is a **non-exit relay**

!!! tip "The two documents after the proposal"

    1. [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/): go through the institutional concerns before any meeting, and attach it to the proposal as appendix one
    2. [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/): once the proposal is approved and you have the IP address and rack space, deploy from there

## Related reading

- [Tor Relays on Campus Track](/join/relay-on-campus/): the community's entry point for this work
- [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/): the institutional concerns
- [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/): `torrc`, UFW, monitoring, and incident handling
- [The NTNU interview](/updates/2025/12/ntnu-nz/): the full account of the first case
- [EFF Tor University Challenge](https://toruniversity.eff.org/): the international programme
- [The NTNU guest post on the Tor Project blog](https://blog.torproject.org/setting-up-tor-university-relay-taiwan/): the case in English

## Sources and acknowledgements

The original proposal and presentation slides behind this template come from community member **Su En-Li (NZ)**, drawn from his work at National Taiwan Normal University. NZ agreed to release the material under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) as a reference for other institutions.

!!! info "The original case files"

    NZ has published the original Google Drive folder, [Tor relay 架設分享@師大](https://drive.google.com/drive/folders/1B9ysi2ELC9w46bD3o7TMsnv55nupI1nz) (Tor relay deployment at NTNU), containing the original proposal document (a Google Doc), slides from an internal presentation on 21 December 2025, and photographs.

    To propose this at your own institution, adapt the placeholder version on this page rather than copying the original document. The original contains NZ's personal email address, supervisor details, and campus IP ranges, and missing one of those before submitting would hand it to your institution along with the proposal. The archive is there so you can see what a real version looks like and learn its structure and register.

If you get a relay running at your institution using this template, **tell us**. We will add your case to the [Tor Relays on Campus Track](/join/relay-on-campus/) so the schools that follow have more to work from. Contact routes are on [Services](/services/).
