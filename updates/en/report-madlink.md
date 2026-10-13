---
title: The Traditional Chinese Translation of InterSecLab's MADLink Report
description: InterSecLab's MADLink report found that 1,708 CSA-7400 appliances shipped by ADLINK in 2019 and 2020 formed the hardware base of Geedge's first-generation firewall platform. The community's Traditional Chinese translation is on the docs site, with a separate record of how Taiwan responded.
date: 2026-05-23
kind: new
---

![MADLink report cover](https://interseclab.org/wp-content/uploads/2026/04/MADLink-A-Taiwanese-Vestige-in-the-Geedge-Suply-Chain.jpg){ .shot }

Network appliances shipped by a publicly listed Taiwanese company ended up at the core of a national internet censorship and surveillance system in Kazakhstan. InterSecLab's MADLink report traces that supply chain, and we, a community based in Taiwan, have translated it into Traditional Chinese for the docs site's [research report translations](https://anoni.net/docs/reports/).

The supplier was ADLINK Technologies (TWSE: 6166) and the customer was the Chinese company Geedge Networks, whose flagship Tiangou Secure Gateway (TSG) has capabilities comparable to China's Great Firewall. [MADLink: A Taiwanese Vestige in the Geedge Supply Chain](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/) was published in April 2026 as InterSecLab's first follow-up on the Geedge supply chain after [The Internet Coup](https://interseclab.org/research/the-internet-coup/) in September 2025.


## Main Findings of the Report

Between 2019 and 2020, ADLINK shipped 1,708 CSA-7400 appliances to Geedge. They formed the hardware foundation of Geedge's first-generation firewall platform, deployed in Kazakhstan for national-scale internet censorship and surveillance. The CSA-7400 is a 4U high-density appliance that ADLINK itself markets for deep packet inspection (DPI) and firewall workloads.

ADLINK hardware also turned up inside EtherFabric, a custom network packet broker (NPB) that Geedge deploys in Myanmar to distribute traffic across multiple TSG nodes. A MAC address recovered from leaked documents traces back to ADLINK, so ADLINK's place in Geedge's product line goes beyond the single CSA-7400 transaction.

Geedge's current-generation TSG, deployed in Ethiopia, Pakistan and Myanmar, runs on servers from Nettrix, a subsidiary of the US-sanctioned Sugon, with Inspur storage. These are standard x86 components that can be bought on the secondary market even where direct procurement is restricted. The report concludes that purpose-built surveillance hardware, such as the CSA-7400 and the ADLINK components inside EtherFabric, is where export controls have the most leverage.

## Chapters of the Translation

The full translation is the [MADLink translation](https://anoni.net/docs/reports/interseclab-madlink/) on the docs site, in Traditional Chinese only. The original report is a single long page, and the translation team split it into five chapters so that discussion on Matrix can refer to specific sections:

- [Chapter 1: Executive summary and main findings](https://anoni.net/docs/reports/interseclab-madlink/index_1/)
- [Chapter 2: The Geedge supply chain in depth, three generations of TSG hardware](https://anoni.net/docs/reports/interseclab-madlink/index_2/)
- [Chapter 3: EtherFabric, and ADLINK's role and response](https://anoni.net/docs/reports/interseclab-madlink/index_3/)
- [Chapter 4: Conclusion](https://anoni.net/docs/reports/interseclab-madlink/index_4/)
- [Chapter 5: Appendix, the full statements from ADLINK and the Ministry of Economic Affairs](https://anoni.net/docs/reports/interseclab-madlink/index_5/)

The full replies from ADLINK and the Bureau of Foreign Trade are kept in the appendix, so readers can compare both sides directly.

## A Record of Taiwan's Response

A report naming a listed Taiwanese company would normally draw follow-up from local press, questions from legislators and a regulator response, yet as of 2026-05-20 Taiwan's Chinese-language public sphere had responded very little. We collected our verification work, the media coverage and the official responses in a separate [observation record](/updates/2026/05/madlink-editorial-2026-05/), published as a snapshot of that day.

## Thanks and Discussion

Thanks to InterSecLab for continuing this series of investigations, and to the community members who worked on the translation and the observation record.

Discussion of both reports, The Internet Coup and MADLink, happens in one [Matrix discussion channel](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net). If you come across new reporting, government documents or public statements on the case, please share them there.

## Related Reading

- [MADLink translation](https://anoni.net/docs/reports/interseclab-madlink/) (Traditional Chinese)
- [Taiwan's Response to the MADLink Report, an Observation Record from May 2026](/updates/2026/05/madlink-editorial-2026-05/)
- [The Internet Coup translation](https://anoni.net/docs/reports/interseclab-network-coup/) (Traditional Chinese)
- [The Traditional Chinese Translation of InterSecLab's The Internet Coup](/updates/2025/10/report-the-internet-coup/)
