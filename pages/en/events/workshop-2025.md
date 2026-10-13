---
title: Anonymous Network Workshop 2025/08
description: Two days at National Taiwan University of Science and Technology, 9 and 10 August 2025, with hands-on Tor, Tails and OONI sessions led by the anoni.net community and five roundtables on open-source trust, community relays and a localized toolkit.
---

![Recruiting staff to help organize the event](docs:assets/images/event-workshop-2025.png){ .shot }

Journalists, civil society groups and human rights advocates work under the risk of intercepted communications and tracked identities, and the people they interview can be put in danger as a result. The workshop gave them two days of hands-on sessions and discussion built on open-source anonymity tools, so that control over their communications stays with them instead of with a single platform.

- Date: Saturday 9 and Sunday 10 August 2025
- Location: Room TR-510, Yan-Yang Teaching Building, National Taiwan University of Science and Technology（國立臺灣科技大學 研揚教學大樓 TR-510 教室）
- Format: workshops and roundtable discussions

!!! info "Event record"

    The workshop has ended, and this page keeps the agenda as it was published. Notes from each session are linked from the "note" tag in the agenda tables, and our follow-up after the event is in the [2025/08 Project Update](/updates/2025/09/updates-202508/).

We, a community based in Taiwan, provided the technical support and hands-on guidance. The sessions introduced [Tor](docs:tools/what-is-tor/) (the onion routing network), [Tails](docs:tools/what-is-tails/) (an amnesic live operating system) and [OONI](docs:tools/what-is-ooni/) (the Open Observatory of Network Interference), and walked participants through preparing a second, secure device, connecting anonymously and measuring censorship themselves.

## Workshop topics

### Digital security and anonymity

- Anonymous browsing over the Tor network
- A **second work environment** built with Tails on a USB drive, leaving no record on the computer it runs on
- Basic threat modelling: your adversaries, the risks and the matching responses
- Reaching Tor from censored countries or networks with bridges and [Snowflake](docs:tools/tor-snowflake/)

### Hands-on skills and tools

- A **portable anonymous operating system** made with Tails, for working safely on public or untrusted devices
- How [OONI Probe](https://ooni.org/install/) measures internet censorship and service blocking, and how its results reach OONI's global open dataset
- Sharing files and collaborating securely with [Tor Browser](https://www.torproject.org/download/) and [OnionShare](docs:tools/onionshare/)

### Community support and continued learning

- The anoni.net community in Taiwan (see [About anoni.net](/about/))
- Ways to contribute to international open-source projects such as Tor, Tails and OONI
- Technical advice and further learning resources after the event

### Use cases

- Reporting on sensitive topics, contacting **whistleblowers** (see Taiwan's [Whistleblower Protection Act](https://www.president.gov.tw/Page/294/49717), in Chinese), and verifying material with partners across borders
- Anonymous communication and coordination channels for cross-border NGO work, or for advocacy in countries and regions where the internet is restricted
- A baseline for in-house digital security training and SOPs

## Roundtable topics

### Local participation and infrastructure

- **Open source and anonymity networks**: the open-source principles behind Tor, Tails and OONI, and why privacy protection and censorship resistance depend on free software.
- **Local participation**: how users in Taiwan can become local contributors to Tor and OONI, bringing the tools closer to local languages and culture.
- **Building and running community nodes**: helping set up Tor relays, OONI Probe installations and similar infrastructure, along with the risks involved and the ways to contribute.

### Decentralized outreach and collaboration

- **A local open-source anonymity toolkit for Taiwan**: packaging these tools into a toolkit that NGOs, news organizations and independent journalists can pick up easily.
- **Strategy and challenges of decentralized outreach**: how a decentralized, open-source outreach effort could work in Taiwan, and how to divide people's time across education, technology and community work.
- **Links with anonymity network communities in the Indo-Pacific**: the potential and current state of regional cooperation, and ways to exchange and collaborate with other advocates in the region.

---

## Sessions

### Venue

The event combined workshops and roundtable discussions over two days, in a room that holds about 30 to 45 people.

- Date: Saturday 9 and Sunday 10 August 2025
- Location: Room TR-510, Yan-Yang Teaching Building, National Taiwan University of Science and Technology
    - In Chinese: 國立臺灣科技大學 研揚教學大樓 TR-510 教室
    - The teaching building is on the Lane 155, Section 3, Keelung Road side of campus, next to the NTU Cancer Center. The main gate of NTUST is a long walk away.
    - Building `15` on the [campus map](https://oia-r.ntust.edu.tw/var/file/60/1060/img/layout_ntust_20240328_new-try.jpg)

### OONI Network Interference Observation

- Time: `2025/08/09 12:30 - 13:30 UTC+8`{style="color: green; font-weight: bold;"}
- Content:
    - Introduction to the OONI project
    - How OONI Probe works
        - Installing and using the mobile app, and the outdated test list for Taiwan
    - Reading measurement data in OONI Explorer
        - Data over a time range, comparisons by country and category, how results are classified
    - Building a list of websites to measure with OONI Run v2
        - Creating your own list and finding your own results in OONI Explorer
    - Other measurement projects similar to OONI
        - Cloudflare Radar, IODA, Sinar Project

### Tor, Tails Anonymous Network

- Time: `2025/08/09 13:30 - 15:30 UTC+8`{style="color: green; font-weight: bold;"}
- Content:
    - The idea of a second device, and when to use one
        - Separating work from personal activity to protect your online identity and data
    - The Tails anonymous operating system
        - How Tails integrates with Tor for anonymous browsing and communication
    - How Tor works
        - Reaching .onion sites
    - Installing Tails, hands-on
        - Installing and configuring Tails on a USB flash drive for secure work online and offline

Both workshop sessions required a laptop. Participants brought their own, and a temporary network was set up on site for the sessions.

### Lecture

The only lecture of the two days revisited Roger's talk at RightsCon 2025 in Taipei: the state of Tor around the world, the common misconception that equates the Tor onion routing network with the dark web, and how to protect personal privacy while pushing for sound internet freedom policy.

| Type/Date/Time | Topic |
| --- | --- |
| <span class="tag tag--solid">Lecture</span><br>2025/08/09<br>10:30-11:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1030)</span> | <span class="tag-text"><i data-icon="simple-torproject"></i>Tor: Defending your online privacy in a surveillance world</span><br><i data-icon="arrow-right-bottom"></i>A review of the Tor Project founder's account of the state of internet freedom and of Tor's work protecting user privacy.<br><i data-icon="arrow-right-bottom"></i>Misuse and misunderstanding of the technology, the stereotypes about the dark web that follow, and how to address them.<br><i data-icon="arrow-right-bottom"></i>Educating users on protecting their privacy, and supporting or joining policy advocacy for reasonable internet freedom policy. |

### Roundtables

In five roundtables alongside the workshops, participants discussed how news media, independent journalists, civil society groups and the open-source technology community could work together. They were also invited to describe what they wanted the community to become, and what technical help or resources it could offer.

| Type/Date/Time | Topic |
| --- | --- |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/09<br>11:30-12:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1130)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> Free Software and Digital Rights: Why Is Open Source Key to Anonymous Tools?</span><br><i data-icon="arrow-right-bottom"></i>Why does open source matter to journalists and civic groups? How can they come to trust these tools?<br><i data-icon="arrow-right-bottom"></i>Core values such as verifiability, censorship resistance and community governance.<br><i data-icon="arrow-right-bottom"></i>Open-source or closed commercial security tools: how to choose? |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/09<br>15:30-16:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1530)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> Promoting a Decentralized, Open-Source Collaborative Anonymous Network Initiative</span><br><i data-icon="arrow-right-bottom"></i>How could the work be divided under a civic tech and open-source collaboration model?<br><i data-icon="arrow-right-bottom"></i>Could an open-source maintenance team (working group model) run Tor and OONI servers and test ISP blocking on a regular schedule?<br><i data-icon="arrow-right-bottom"></i>Which non-technical roles (design, translation, teaching, writing) could take part? |

| Type/Date/Time | Topic |
| --- | --- |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/10<br>11:00-12:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d2-1100)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> From User to Contributor: How Taiwan Can Establish Community Nodes and Feedback Models for Tor/OONI</span><br><i data-icon="arrow-right-bottom"></i>Does Taiwan already have infrastructure such as Tor relays and OONI Probe installations? How is it doing?<br><i data-icon="arrow-right-bottom"></i>What technical, administrative and legal challenges come up in practice? (For example hosting costs, blocking, legal concerns.)<br><i data-icon="arrow-right-bottom"></i>Could a community approach help run them and train newcomers? |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/10<br>13:00-14:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d2-1300)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> The Open-Source foundation and Local Participation Possibilities of Tor/Tails/OONI</span><br><i data-icon="arrow-right-bottom"></i>How do these tools work, and which free software and open-source licenses do they use?<br><i data-icon="arrow-right-bottom"></i>Where can developers and security researchers in Taiwan contribute? (For example translation, bug reports, tutorials.)<br><i data-icon="arrow-right-bottom"></i>How can the technical barrier be lowered so that more people want to contribute? |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/10<br>14:00-15:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d2-1400)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> How to Localize an Open-Source Anonymous Toolkit?</span><br><i data-icon="arrow-right-bottom"></i>From everyday browsing (Tor) to an operating system (Tails) and network measurement (OONI), what other open-source tools belong in the kit?<br><i data-icon="arrow-right-bottom"></i>What should the toolkit contain? (For example a Live USB image, local language packs, manuals.)<br><i data-icon="arrow-right-bottom"></i>A simplified "Taiwan edition" for NGOs, journalists and beginners. |

## Full schedule

- Date: Saturday 9 and Sunday 10 August 2025
- Location: Room TR-510, Yan-Yang Teaching Building, National Taiwan University of Science and Technology

<figure markdown="span">
  ![Event schedule](docs:assets/images/event_workshop_2025_schedule.svg)
  <figcaption>The planned schedule for the two days.</figcaption>
</figure>

### Saturday 9 August

| Type/Date/Time | Topic |
| --- | --- |
| <span class="tag tag--solid">Lecture</span><br>2025/08/09<br>10:30-11:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1030)</span> | <span class="tag-text"><i data-icon="simple-torproject"></i>Tor: Defending your online privacy in a surveillance world</span><br><i data-icon="arrow-right-bottom"></i>A review of the Tor Project founder's account of the state of internet freedom and of Tor's work protecting user privacy.<br><i data-icon="arrow-right-bottom"></i>Misuse and misunderstanding of the technology, the stereotypes about the dark web that follow, and how to address them.<br><i data-icon="arrow-right-bottom"></i>Educating users on protecting their privacy, and supporting or joining policy advocacy for reasonable internet freedom policy. |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/09<br>11:30-12:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1130)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> Free Software and Digital Rights: Why Is Open Source Key to Anonymous Tools?</span><br><i data-icon="arrow-right-bottom"></i>Why does open source matter to journalists and civic groups? How can they come to trust these tools?<br><i data-icon="arrow-right-bottom"></i>Core values such as verifiability, censorship resistance and community governance.<br><i data-icon="arrow-right-bottom"></i>Open-source or closed commercial security tools: how to choose? |
| <span class="tag tag--solid">Workshop</span><br>2025/08/09<br>12:30-13:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1230)</span> | <span class="tag-text"><i data-icon="tools"></i> OONI Network Interference Observation</span><br><i data-icon="arrow-right-bottom"></i>Introduction to the OONI project<br><i data-icon="arrow-right-bottom"></i>How OONI Probe works<br><i data-icon="arrow-right-bottom"></i>Reading measurement data in OONI Explorer<br><i data-icon="arrow-right-bottom"></i>Building a list of websites to measure with OONI Run v2<br><i data-icon="arrow-right-bottom"></i>Other measurement projects similar to OONI |
| <span class="tag tag--solid">Workshop</span><br>2025/08/09<br>13:30-15:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1330)</span> | <span class="tag-text"><i data-icon="tools"></i> Tor, Tails Anonymous Network</span><br><i data-icon="arrow-right-bottom"></i>The idea of a second device, and when to use one<br><i data-icon="arrow-right-bottom"></i>The Tails anonymous operating system<br><i data-icon="arrow-right-bottom"></i>How Tor works<br><i data-icon="arrow-right-bottom"></i>Installing Tails, hands-on |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/09<br>15:30-16:30<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d1-1530)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> Promoting a Decentralized, Open-Source Collaborative Anonymous Network Initiative</span><br><i data-icon="arrow-right-bottom"></i>How could the work be divided under a civic tech and open-source collaboration model?<br><i data-icon="arrow-right-bottom"></i>Could an open-source maintenance team (working group model) run Tor and OONI servers and test ISP blocking on a regular schedule?<br><i data-icon="arrow-right-bottom"></i>Which non-technical roles (design, translation, teaching, writing) could take part? |

### Sunday 10 August

| Type/Date/Time | Topic |
| --- | --- |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/10<br>11:00-12:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d2-1100)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> From User to Contributor: How Taiwan Can Establish Community Nodes and Feedback Models for Tor/OONI</span><br><i data-icon="arrow-right-bottom"></i>Does Taiwan already have infrastructure such as Tor relays and OONI Probe installations? How is it doing?<br><i data-icon="arrow-right-bottom"></i>What technical, administrative and legal challenges come up in practice? (For example hosting costs, blocking, legal concerns.)<br><i data-icon="arrow-right-bottom"></i>Could a community approach help run them and train newcomers? |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/10<br>13:00-14:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d2-1300)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> The Open-Source foundation and Local Participation Possibilities of Tor/Tails/OONI</span><br><i data-icon="arrow-right-bottom"></i>How do these tools work, and which free software and open-source licenses do they use?<br><i data-icon="arrow-right-bottom"></i>Where can developers and security researchers in Taiwan contribute? (For example translation, bug reports, tutorials.)<br><i data-icon="arrow-right-bottom"></i>How can the technical barrier be lowered so that more people want to contribute? |
| <span class="tag tag--solid">Roundtable</span><br>2025/08/10<br>14:00-15:00<br><span class="tag">[<i data-icon="file-edit-outline"></i> note](https://pad.anoni.net/p/ws-note-d2-1400)</span> | <span class="tag-text"><i data-icon="chat-processing-outline"></i> How to Localize an Open-Source Anonymous Toolkit?</span><br><i data-icon="arrow-right-bottom"></i>From everyday browsing (Tor) to an operating system (Tails) and network measurement (OONI), what other open-source tools belong in the kit?<br><i data-icon="arrow-right-bottom"></i>What should the toolkit contain? (For example a Live USB image, local language packs, manuals.)<br><i data-icon="arrow-right-bottom"></i>A simplified "Taiwan edition" for NGOs, journalists and beginners. |

## Related pages

- [Anonymous Network Workshop 2025/08 staff](/events/workshop-2025-prepare/): recruiting staff and teaching assistants before the event
- [2025/08 Project Update](/updates/2025/09/updates-202508/): our follow-up after the event, and the brochure we left at conference venues
- [Continuing from 2025 into 2026: Personal Privacy Guidelines, Tor Relay Campus Deployment Competition, and Exploration of Anonymous Payments](/updates/2026/01/2025to2026/): a look back at 2025 and the three tracks for 2026
- [COSCUP 2026 Anonymity Networks Community track](/events/coscup-2026/): our two-day track in the same room in August 2026
