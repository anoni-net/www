---
title: The first quarterly observation report, and new homes for the monitoring pages
description: In the third quarter of 2026 Taiwan's running Tor relays fell from 13 to 11, with 8 on Chunghwa Telecom's HiNet, and mobile networks served 45% of users but produced 4% of OONI measurements. In October the monitoring pages moved to the projects section of anoni.net and now cover more of Asia.
date: 2026-10-11
og_image: https://assets.anoni.net/reports/2026-q3-og-en-3138faf3.png
---

The community collects two kinds of observation data every day: how many volunteer-run Tor relays Taiwan and nearby regions have, and which networks the censorship measurements come from. Until now the numbers lived only on the monitoring pages of the documentation site, which show the last two months but not how a whole quarter changed, and made it hard to compare Taiwan with the regions around it. From October the community writes a [quarterly observation report](/projects/reports/) every three months, and the monitoring pages have moved to the [projects](/projects/) section of anoni.net with more Asian regions covered.

## What the third quarter showed

The [report for the third quarter of 2026](/projects/reports/2026-q3/) covers 1 July to 30 September and has two main findings.

Running Tor relays in Taiwan fell from 13 at the start of the quarter to 11, and 8 of them sit on Chunghwa Telecom's HiNet. The top two networks carry 82% of Taiwan's relays, the most concentrated of the ten regions tracked at the time. Per million internet users Taiwan runs about 0.4 relays, close to South Korea, against 3.2 in Hong Kong and 15 in Singapore. If HiNet has an outage or comes under pressure, most of Taiwan's relays go down together.

OONI collected about 2.76 million censorship measurements from Taiwan this quarter. Networks with at least one measurement cover 95% of internet users, but the measurements are concentrated on fixed lines. Mobile networks serve 45% of users and produced 4% of the measurements; Chunghwa Telecom's mobile network alone serves 17% of users and produced 0.3%. If blocking happened on a mobile network, very few devices would be there to record it. The community's OONI Run link `10328` sent 39,116 measurements this quarter, 2.2 times the quarter before, nine tenths of them from Taiwan Mobile, which closes part of the gap.

The report also covers relays that joined and left, how quickly relays upgraded to new Tor releases, networks with no measurements all quarter, and comparisons with nearby regions. Relay data collection stopped between 8 July and 23 August, so the quarter has 45 days of relay data, as the report notes.

## New homes for the monitoring pages

The Tor relay watcher and the ASN observation analysis that used to sit on the documentation site are now two monitoring pages in the projects section of anoni.net, with one page per region. The charts are drawn when the site is built, so the pages need no JavaScript and work in full over the onion service. Old addresses on the documentation site redirect to the new pages.

<!-- region-map -->

[Tor Relay Watch](/projects/pulse/) updates hourly and covers fifteen regions: Taiwan, Japan, South Korea, Hong Kong and Macau in East Asia; Singapore, Vietnam, Thailand, Malaysia, Indonesia and the Philippines in Southeast Asia; India in South Asia; and Germany, the Netherlands and the United States, which run the most relays, as reference points. Besides relay counts, bandwidth, networks and Tor versions, each region now has a "Use and contribution" section that sets Tor Metrics' estimate of users beside the region's share of the whole Tor network's relay weight. On 10 October Taiwan accounted for about 0.25% of the world's Tor users and 0.008% of the network's weight. About 6% of Taiwan's users connected through bridges, about 16% in Thailand, and close to half in China, listed as a reference at the end of the comparison table.

[OONI Coverage](/projects/asn-coverage/) covers Taiwan, Hong Kong, Macau, Japan, South Korea, Singapore, Vietnam, Thailand, Malaysia, Indonesia, the Philippines and India. Alongside the existing coverage figure there is now steady coverage, which counts only networks measured on at least 15 of the last 30 days. Taiwan's coverage is 93.9% and its steady coverage 68%; Hong Kong's are 69% and 31%. The gap shows how many users sit on networks with only scattered measurements. The page also lists the results of OONI's Signal, WhatsApp and Telegram tests in each region. Anomaly rates in the regions we track are all below 4%, while China, Myanmar and Pakistan, listed as references, each have apps above 90%.

The guide to asking an AI assistant about Tor relays has also moved from the documentation site to the projects section, as [Tor relay lookup for AI assistants](/projects/onionoo-mcp/). These are now the names for the three monitoring tools; the code names of the programs and repositories (Pulse, ASN Coverage, onionoo MCP) appear only when the programs themselves are meant. Both monitoring pages end with a glossary for readers meeting terms like ASN, bridge or pp for the first time.

## How to help next quarter

- Mobile measurements: install [OONI Probe](https://ooni.org/install/mobile) on a phone that uses mobile data and open the community's [OONI Run link](https://run.ooni.org/v2/10328). The [OONI Run v2 guide](docs:tools/ooni-run-v2/) covers the risks to weigh first
- Cable broadband: the report lists the [networks with no measurements all quarter](/projects/reports/2026-q3/#Networks-with-no-measurements-this-quarter), mostly cable TV broadband. If your home connection is on the list, you can add a network
- Tor relays outside HiNet: university networks and other providers both help; see [how to set up a Tor relay](docs:community/setup-tor-relay/) and [Tor relays on campus](/join/relay-on-campus/)
- Upgrades: if you run a relay, move to 0.4.9.13 or later

The report comes out every three months. The next one covers the fourth quarter and is planned for January 2027, and you can follow community updates by [RSS](/en/updates/feed.xml). Thoughts on the report, or a figure you think is wrong, are welcome at <whisper@anoni.net> or as an issue on [GitHub](https://github.com/anoni-net/www/issues).
