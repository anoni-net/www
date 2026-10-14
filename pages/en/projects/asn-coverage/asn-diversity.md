---
title: ASN Diversity and Gaps in Taiwan's OONI Coverage
description: How concentrated Taiwan's OONI measurements are across a few ASNs, with figures from December 2023 and October 2026, how to help fill the gaps, and how to read a single measurement.
---

OONI Probe produces plenty of measurements in Taiwan, but if nearly all of them come from one or two carriers, the data reflects those carriers' networks and not the country's connectivity as a whole. If a website is blocked on only one carrier and nobody happens to be measuring from that carrier, the block leaves no record. Low diversity in the ASNs (autonomous system numbers) that measurements come from is currently the clearest weakness in Taiwan's OONI data. Which websites get tested is set by the test list (see [Maintaining the OONI Test List](/join/ooni-test-list/)); this page looks at which networks the measurements come from.

## Measurement by ASN

The internet is a mesh of interconnected Autonomous Systems (AS). Each AS is a group of networks under one administration, such as a telecom operator, a university, a company or a CDN provider, with its own routing policy, exchanging routes with other ASes over BGP. Every AS has a unique number, its ASN. Cloudflare Learning covers the basics in [What is an autonomous system?](https://www.cloudflare.com/learning/network-layer/what-is-an-autonomous-system/) and [What is BGP?](https://www.cloudflare.com/learning/security/glossary/what-is-bgp/).

For OONI measurement, the ASN is the smallest useful unit of "which network did we see this censorship on". The same website may be unreachable on Chunghwa Telecom and fine on Taiwan Mobile, and you cannot tell those apart without breaking the data down by ASN. That is why OONI analysis keeps asking how many distinct ASNs a region's measurements come from. The higher that share, the better the data reflects the region's actual connectivity.

To find the ASN you are currently on, use [ip.me](https://ip.me/). The AS pages on [Cloudflare Radar](https://radar.cloudflare.com/en-us/as3462) show traffic trends and history for a single ASN (AS3462, for example), and [Is BGP safe yet?](https://isbgpsafeyet.com/) checks whether your ISP has deployed RPKI route validation.

## Concentration of Taiwan's Measurements

[OONI](https://ooni.org/) (Open Observatory of Network Interference) relies on volunteers around the world who run [OONI Probe](https://ooni.org/install/) to test for censorship, and every result is uploaded to the project's [open data repository](https://registry.opendata.aws/ooni/). From November 2023 to March 2024, we analysed OONI's open data with [ASN Coverage](https://github.com/anoni-net/asn-coverage). The December 2023 results:

- Taiwan ranked among the top ten in OONI Explorer by number of measurements
- 78.94% of measurements came from [AS3462 (Chunghwa Telecom)](https://radar.cloudflare.com/en-us/as3462) and [AS18041 (Taiwan Digital Streaming)](https://radar.cloudflare.com/en-us/as18041)
- Taiwan has roughly 437 ASNs, and distinct ASNs in the measurement data covered only 7.32% of them

High volume concentrated in two ASNs cannot reflect the full range of Taiwan's networks. The three major carriers, cable broadband, fixed-line networks and Type II telecom operators (companies that lease telecom infrastructure to offer services, such as MVNOs and VoIP resellers) are all under-covered.

For what has changed since 2023, see the project home page, [OONI Coverage](/projects/asn-coverage/). It is regenerated every hour from the last 60 days of OONI measurements, set against APNIC's estimates of each network's user population, and lists networks with many users and few measurements. In the 2026-10 data, Chunghwa Telecom HiNet (AS3462) still has the most measurements, while Chunghwa Telecom's mobile network (AS17421) has about 16% of users and less than 0.1% of measurements.

### Ways to Help Fill the Gaps

The most direct way to improve coverage is to keep one device measuring from an ASN nobody has covered yet. The community's OONI Run link `10328` is a ready-made entry point: install [OONI Probe](https://ooni.org/install/mobile) on a mobile device, tap the link once to set it up, and leave OONI Probe running in the background. The risks to weigh beforehand and the contents of the list are covered in the [OONI Run v2 guide](docs:tools/ooni-run-v2/).

Existing measurements cluster on a handful of fixed-line ASNs, and data from mobile carriers and Type II telecom operators is the scarcest, so helpers on mobile networks are especially valuable. Networks with no measurements yet are listed under "Networks without measurements" on the OONI Coverage page.

## Reading a Single Measurement

The quickest way in is to produce a measurement of your own with OONI Probe:

1. Download [OONI Probe](https://ooni.org/install/) (mobile or desktop)
2. Open OONI Probe, select "Websites" and run the test
3. When it finishes, go to "Test Results", find the websites test you just ran, and look for items marked "!" or "?"
4. Tap any "!" or "?" item to see the possible issue, along with "Data" and "Show in OONI Explorer" links
5. Follow either link to view the raw measurement data

Take this measurement as an example: [`20241024185921.623617_TW_webconnectivity_578b6d3845fed2e2`](https://explorer.ooni.org/m/20241024185921.623617_TW_webconnectivity_578b6d3845fed2e2)

The result reads `Test failure on AS3462`, with the failure message `unknown_failure: dial tcp [scrubbed]: connect: host is down`, meaning the host did not respond at the time of the test. The "DNS queries" section records that `www.asap.com.tw` has a DNS `A` record pointing to `60.250.151.72` (AS3462, Chunghwa Telecom Co., Ltd.), resolved through Cloudflare DNS at `162.158.242.36`.

Details the results page does not show in full are in the "Raw Measurement Data" section, which holds the raw output of every test item and is the material for further analysis.

![The raw measurement data view in OONI Explorer](https://assets.anoni.net/www/ooni-raw-data-b3b80fe2.webp)

!!! note "Probe ASN and Resolver ASN"

    OONI Probe records the whole test path. In the example above, the connection went through Chunghwa Telecom's network while the DNS query was answered by Cloudflare, so `probe_asn` and `resolver_asn` in the raw data belong to two different ASNs. When a website is blocked and cannot be reached, whether the problem lies with the network the probe is on or with DNS resolution has to be worked out from these two fields separately.

What each field means is covered in [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/), how verdicts are computed in [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/), and what each nettest measures in [OONI Nettest Quick Reference](/projects/asn-coverage/ooni-nettests-map/).

## Computing Coverage Yourself

To retrieve OONI's public data and calculate ASN coverage for a region yourself, the tool setup and commands are in [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/), and the environment you need first is in [Development Environment Setup](/join/dev-setup/).

[<i data-icon="database-search"></i> ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/){ .btn .solid }

## Next Steps

We plan to break coverage down by network type (mobile, home broadband). The fields this needs exist only in raw measurements and are not in OONI's aggregation API, so for now the work is done by hand with the tool in [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/). The other direction is pairing this with [Maintaining the OONI Test List](/join/ooni-test-list/), improving both which websites are tested and how varied the measurement sources are.

## Related Reading

- [Maintaining the OONI Test List](/join/ooni-test-list/): the website list OONI Probe uses in Taiwan, and how to help maintain it
- [OONI Coverage](/projects/asn-coverage/): users and measurements per network, updated hourly
- [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/): the command-line tool for retrieving OONI's public data and computing coverage
- [Call for OONI Measurements During Northern Taiwan's Mobile Throttle Drill on 13 August](/updates/2026/08/ooni-mobile-throttle-drill/): how measurements were spread across networks in July and August 2026, with HiNet alone at 39.3%
- [Tor Relay Watch](/projects/pulse/): the community's other observation project
- [Why networked freedom matters](docs:basics/internet-freedom/): the introduction on the docs site
