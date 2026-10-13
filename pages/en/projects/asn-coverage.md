---
title: OONI Coverage
description: Which networks OONI measurements in Taiwan and nearby regions come from, how many users they cover, and which networks have no measurements at all.
lead: Censorship monitoring only covers the networks where someone runs OONI Probe.
---

OONI's censorship measurements come from volunteers running OONI Probe on their own connections. Within one region, each provider and network (ASN, autonomous system number) may block different sites, so when only one or two providers are measured, blocking on the others goes unrecorded. This page sets OONI's measurement counts against APNIC's estimates of how many users each network has, to show how many users the measurements cover, which networks they concentrate on, and which networks have none.

The page is regenerated every hour and OONI's measurements are read every six hours. Taiwan is shown by default, with other regions as reference points; switch between them with the region list below. The [glossary](#glossary) at the end of the page explains the fields. Each quarter's changes are written up in the [quarterly reports](/projects/reports/).

<!-- asn-coverage -->

## Glossary {#glossary}

- **OONI Probe**: an open-source app from OONI that tests from a phone or computer whether websites and services can be reached, with the results published in OONI's database
- **Measurement**: one result of OONI Probe testing one website or service. A single run of the website test produces hundreds, so a high count does not mean many people ran tests
- **Autonomous system (ASN)**: a group of networks run by one organisation under one routing policy, such as a telecom, a university or a cloud provider, each with its own AS number. A telecom's fixed and mobile networks are often separate ASNs
- **Network names**: copied from APNIC and RIPE NCC registry records and often abbreviated. In Taiwan, for example, HINET is Chunghwa Telecom's fixed network and EMOME-NET its mobile network
- **APNIC**: the Asia Pacific Network Information Centre, which allocates IP addresses and ASNs in the region and estimates each network's users from sampled web ads
- **Users, Measured (%)**: Users is the network's share of the region's internet users, and Measured is its share of the region's measurements. The further apart the two are, the more the measurements are out of proportion to the users
- **Days**: how many of the last 30 days had any measurements
- **Users covered**: the share of the region's internet users on networks with measurements, where a single measurement is enough to count
- **Users steadily covered**: counts only networks measured on at least 15 of the last 30 days
- **Top two networks**: the share of measurements from the two most measured networks; lower means more spread out
- **pp (percentage points)**: the difference between two percentages. Coverage going from 94.6% to 93.9% is written as −0.7 pp
- **OK, anomaly, confirmed, failure**: OK means the result matched the control. An anomaly means it did not, which can be blocking or an unstable connection. Confirmed blocking is an anomaly matching a known blocking pattern. A failure is a test that did not complete
- **Anomaly rate (messaging apps)**: the share of the app's measurements that were anomalies. Close to 100% usually means the app is blocked there
- **Reference region**: a region without its own page, listed in a comparison table for contrast

## How the numbers are calculated

- Measurement counts come from [OONI's aggregation API](https://api.ooni.io/), across all tests, grouped by the day each measurement started (UTC)
- Users per network are [APNIC's estimates](https://stats.labs.apnic.net/aspop/), derived from ad-based sampling and updated weekly
- Network names come from the APNIC and RIPE NCC ASN name lists
- A single measurement is enough for a network to count as measured; whether it is measured enough shows in its share of measurements and the number of days
- Steady coverage counts only networks measured on at least 15 of the last 30 days
- Messaging app results also come from the OONI aggregation API, counted by region; the reference regions at the end of the table have no pages of their own
- Days without measurements are left as gaps in the charts rather than filled in

## Help fill the gaps

- Install [OONI Probe](https://ooni.org/install/) and run tests on your own connection, on a phone or a computer. Mobile data and home broadband are usually different ASNs, so testing on both helps
- The community's OONI Run link `10328` sets everything up in one tap; see the [OONI Run v2 guide](docs:tools/ooni-run-v2/) for the risks to consider before installing and what the list contains
- [ASN observation data analysis](docs:taiwan/ooni-asn-coverage/): why network diversity matters and how to read a single measurement
- [ASN Coverage](https://github.com/anoni-net/asn-coverage): a command-line tool that downloads raw measurements and breaks them down by network type and blocking method

## Reading the measurement data

<ul class="rows">
  <li><a class="row" href="/projects/asn-coverage/ooni-data-format/"><span class="ic">ICON:code-json</span><span class="b"><span class="t">The Structure of an OONI Measurement</span><span class="d">Which fields make up a measurement, and how to read where it was taken and what it found.</span></span><span class="go">ICON:arrow-right</span></a></li>
  <li><a class="row" href="/projects/asn-coverage/ooni-blocking-determination/"><span class="ic">ICON:shield-search</span><span class="b"><span class="t">OONI Blocking Verdicts</span><span class="d">The evidence behind each of the four Web Connectivity verdicts, and why a verdict is not a confirmed block.</span></span><span class="go">ICON:arrow-right</span></a></li>
  <li><a class="row" href="/projects/asn-coverage/ooni-nettests-map/"><span class="ic">ICON:table-search</span><span class="b"><span class="t">OONI Nettest Quick Reference</span><span class="d">What each of the 41 nettests measures, which still produce data, and which ones show up in Taiwan.</span></span><span class="go">ICON:arrow-right</span></a></li>
  <li><a class="row" href="/projects/asn-coverage/howto/"><span class="ic">ICON:database-search</span><span class="b"><span class="t">ASN Observation Data Retrieval and Analysis</span><span class="d">Setting up the ASN Coverage command-line tool, the layout of the public S3 dataset, and the CSV fields it outputs.</span></span><span class="go">ICON:arrow-right</span></a></li>
</ul>
