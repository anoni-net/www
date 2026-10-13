---
title: Taiwan's Response to the MADLink Report, an Observation Record from May 2026
description: How Taiwan's media, legislature and regulators responded after the MADLink report named the listed Taiwanese company ADLINK, recorded as a snapshot on 2026-05-20, with our verification work and the public sources worth watching.
date: 2026-05-20
---

InterSecLab's MADLink report named a publicly listed Taiwanese company and found that network appliances it shipped became the hardware foundation of the censorship system Geedge Networks, a Chinese company, deployed in Kazakhstan. The question the report raises is whether Taiwan's export controls can stop a local company from supplying surveillance and censorship equipment to authoritarian governments, and answering it depends on local journalism, legislative questioning and a regulator response. Nearly a month after publication, Taiwan's Chinese-language public sphere had responded very little.

We wrote down our verification work and what we observed at the time, so that later readers of the report can see how it was received in Taiwan, and anyone who wants to keep watching has a starting point.

!!! note "Snapshot as of 2026-05-20"

    This is an editorial observation by the anoni.net editorial team as of 2026-05-20 (first version 2026-05-16, independent verification added 2026-05-20), and is not part of InterSecLab's original report. It has not been updated since publication, and every status described here is as of the snapshot date. The translation of the report is in the docs site's [MADLink translation](https://anoni.net/docs/reports/interseclab-madlink/) (Traditional Chinese only), and the English original is on [InterSecLab's site](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/).


## Independent Verification

The report names a publicly listed company and cites a chain of technical details. Before recording the local reception, we ran an independent verification pass on the key claims so readers can reproduce the checks themselves.

### The MAC Address Prefix in EtherFabric

The IEEE OUI `00:30:64` is registered to ADLINK Technology, Inc. This hardware fingerprint is how the report links EtherFabric to ADLINK, and it is the most easily verifiable claim in the report. Two independent lookup services, macvendors.com ([`api.macvendors.com/00:30:64`](https://api.macvendors.com/00:30:64)) and macvendorlookup.com ([`api.macvendorlookup.com/api/v2/003064`](https://www.macvendorlookup.com/api/v2/003064)), both return "ADLINK TECHNOLOGY, INC." with ADLINK's old address in Zhonghe District, New Taipei. The result confirms at the hardware level that the MAC address on the EtherFabric management interface comes from ADLINK equipment.

### How the CSA-7400 Is Marketed

ADLINK describes the CSA-7400 as a general-purpose platform, and the report's rebuttal rests on how the product itself is positioned. On ADLINK's [official product page](https://www.adlinktech.com/Products/Network_Security_Appliance/4UNetworkAppliance/CSA-7400?lang=en), in both English and Chinese, the CSA-7400 sits in the "Network Security Appliance" category and is marketed as carrier-grade equipment for DPI, IDS/IPS, DDoS and NGFW workloads. The publicly mirrored [Quick Start Manual](https://manualzz.com/doc/55701658/adlink-technology-csa-7400-quick-start-manual) confirms it ships with CentOS 7 preinstalled, consistent with the report's description of early TSG-OS being CentOS-based.

### Geedge's Founding

Geedge (Hainan) Information Technology Co., Ltd. was founded in Hainan in 2018. [Chinese Wikipedia](https://zh.wikipedia.org/wiki/%E7%A7%AF%E8%87%B3%E4%BF%A1%E6%81%AF), [Epoch Times' reporting of 2025-09-13](https://www.epochtimes.com/b5/25/9/13/n14593857.htm) and [NTD](https://www.ntdtv.com/b5/2025/09/13/a104019706.html) cross-confirm the company's basic details, its founder's background, and its shared roots with the MESA Lab at the Chinese Academy of Sciences' Institute of Information Engineering.

### The New Bloom Magazine Article

The New Bloom Magazine article we cite exists: "[Taiwanese Company Implicated in Great Firewall Supply Chain By Report](https://newbloommag.net/2026/04/29/tw-adlink-geedge/)", published 2026-04-29 07:41 UTC.

## Media Coverage

### International and English-Language Media

- InterSecLab's [original report](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/) (April 2026) follows its September 2025 [The Internet Coup](https://interseclab.org/research/the-internet-coup/) and is the primary research in the series.
- [New Bloom Magazine](https://newbloommag.net/2026/04/29/tw-adlink-geedge/) (a Taiwan-focused English-language outlet, 2026-04-29) was, as of the snapshot date, the only Taiwan-related independent media piece directly engaging with the ADLINK–Geedge link. The article itself notes the surprising silence, given that Taiwan's government typically responds to cases involving Chinese companies.
- International tech and infosec outlets, including cybernews, osnews and Daily Security Review, mostly stayed within the framing of the September 2025 Geedge leak, without singling out ADLINK as a Taiwanese node in the supply chain.

### Taiwan's Chinese-Language Media

Cross-outlet searches for "凌華 Geedge", "MADLink 凌華" and "凌華 哈薩克" found that major Taiwanese outlets, including UDN, Liberty Times, CNA, TVBS, TechNews and iThome, had no direct reporting on MADLink or the ADLINK, Geedge and Kazakhstan link as of 2026-05-20. [TechNews](https://infosecu.technews.tw/2025/09/14/china-geedge-mesa-leak-analyzing-the-great-firewall-largest-document-leak/) covered the September 2025 leak of 500GB of Great Firewall documents itself, but did not follow up on ADLINK's place in the supply chain. Over the same period, ADLINK's Chinese-language press coverage stayed on its usual business beat: edge AI orders, Taiwan Excellence awards and the CYBERSEC 2026 expo.

## Responses from the Regulator, the Legislature and ADLINK

In its reply to InterSecLab, the Bureau of Foreign Trade of the Ministry of Economic Affairs (MOEA) explained that Taiwan's export controls on Strategic High-Tech Commodities exist to prevent the proliferation of weapons of mass destruction. The controlled goods list follows the four international export-control regimes, and the entity list follows sanctions lists from the UN Security Council and partner countries. On the specific case, the Bureau cited legal restrictions and declined to disclose information about individual companies (the full text is in the [appendix](https://anoni.net/docs/reports/interseclab-madlink/index_5/) of the translation).

The original report quotes a legislator arguing that Taiwan should build its own entity list rather than rely only on US and EU lists, and should set clearer standards for when a component manufacturer is responsible for end use. As of the snapshot date, searches of the Legislative Yuan's records, social media and press interviews found no follow-up statement from that legislator on the issue.

ADLINK's statement to InterSecLab of 14 November 2025 said it would launch an internal audit, and the full text is in the same appendix. Querying [Taiwan's Market Observation Post System](https://mopsov.twse.com.tw/) under stock code 6166 returned no material announcement regarding Geedge, the CSA-7400 shipment or the internal audit as of 2026-05-20.

## Possible Reasons for the Quiet in Taiwan

These are factors the editorial team observed, offered as hypotheses rather than verdicts, and we welcome additions and challenges.

- **Technical barrier**: connecting the CSA-7400, deep packet inspection, Geedge's TSG and export controls into one story is hard for general business and politics reporters. Without a local technical brief or translation, a story that lands for Taiwanese readers is expensive to produce.
- **Where infosec media look**: outlets such as iThome and Information Security (資安人) cover enterprise security procurement and technology trends, and "Taiwanese components used in authoritarian surveillance" sits outside their usual beat.
- **The news cycle**: MADLink named ADLINK only in April 2026, while the underlying Geedge leak story had cooled by late 2025, and Taiwanese media did not treat it as a thread to keep following.
- **Where civil society looks**: Taiwanese civil society groups working on information and digital rights have mostly focused on Chinese influence operations against Taiwan, disinformation governance and platform accountability, and rarely treat human-rights review of surveillance technology exports as a main issue. That is part of the gap anoni.net's translation of MADLink aims to address.

## The Gap in the Regulatory Framework

The report concludes that Taiwan's export-control framework is oriented toward non-proliferation and does not cover surveillance-capable technology shipped to vendors supplying authoritarian governments. Without media coverage, legislative questioning or civil society campaigns, regulators face no pressure to update the framework, and ADLINK faces no pressure to disclose the progress of its internal audit.

## Public Sources Worth Watching

### Government and Regulators

**Bureau of Foreign Trade, MOEA**

- Sources: [Strategic High-Tech Commodities entity list](https://publicinfo.trade.gov.tw/icp/exportList.html), [Bureau press releases](https://www.trade.gov.tw/Pages/List.aspx?nodeID=40)
- What to watch: whether surveillance and censorship equipment vendors are added to the entity list, whether end-use review is introduced, and whether the interagency review meetings publish any conclusion on this case

**Legislative Yuan**

- Sources: [Legislative Yuan IVOD](https://ivod.ly.gov.tw/), [proceedings and gazette](https://lci.ly.gov.tw/), [integrated information system](https://ppg.ly.gov.tw/ppg/)
- What to watch: written or oral questioning, proposals or press releases on the issue from the legislator quoted in the report or from others (particularly on the Economics, Foreign and National Defense, and Judiciary and Organic Laws committees), and whether a committee invites the responsible agency to report

**Financial Supervisory Commission and the Taiwan Stock Exchange (ADLINK is publicly listed)**

- Sources: [Market Observation Post System](https://mopsov.twse.com.tw/), stock code 6166 (material announcements, annual reports, ESG reports)
- What to watch: material announcements regarding the Geedge shipment, disclosure of the case and the internal audit in the 2026 annual report or sustainability report, and analyst questions at investor conferences

**Control Yuan**

- Source: corrective measures published by the [Control Yuan](https://www.cy.gov.tw/)
- What to watch: any corrective measure or impeachment over the regulators' failure to identify end use during export compliance review

### Media and Civil Society

- Chinese-language media: whether tech and investigative outlets that have covered the Great Firewall, Chinese infosec or export controls follow up
- Civil society: whether groups working on digital rights, open government or trade policy launch petitions, panel discussions or policy advocacy on the issue

### Ways to Track, by Cost

| Approach | One-time setup | Ongoing | How |
|---|---|---|---|
| Google Alerts | 10 minutes | 0 | Keywords such as "凌華 Geedge", "ADLINK Geedge" and "戰略性高科技貨品 監控", with an email on each hit |
| Manual check | 0 | About 30 minutes a month | A community rotation goes through the sources above and reports to the Matrix channel |
| RSS or HTML diff bot | 1–2 hours | 0 | Feeds Bureau press releases and stock code 6166 announcements into the community's Matrix channel |
| Scheduled scraper | 4–6 hours | 0 | Periodically fetches the entity list and material announcements, and opens a GitHub issue when content changes |

The four approaches can be combined, and the cheapest starting point is Google Alerts plus a manual check. Automated monitoring is worth adding once concrete signals appear, such as the Bureau updating the framework, a legislator raising the issue publicly, or ADLINK filing a material announcement.

## Additional Material

This post was published as a snapshot of 2026-05-20 and is not updated. If you find reporting, government documents or public statements it does not cover, please share them in the [Matrix discussion channel](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net).

## Related Reading

- [MADLink translation](https://anoni.net/docs/reports/interseclab-madlink/) (Traditional Chinese)
- [The Traditional Chinese Translation of InterSecLab's MADLink Report](/updates/2026/05/report-madlink/)
- [The Internet Coup translation](https://anoni.net/docs/reports/interseclab-network-coup/) (Traditional Chinese)

*[ADLINK]: ADLINK Technology, Inc., a company listed on the Taiwan Stock Exchange (stock code 6166).
*[Geedge Networks]: A Chinese network company that develops, deploys and exports internet censorship and surveillance technology.
*[CSA-7400]: A high-density 4U network platform from ADLINK, marketed by the vendor for firewall and deep packet inspection use.
*[TSG]: Tiangou Secure Gateway, Geedge Networks' flagship censorship and surveillance product.
