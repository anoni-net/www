---
title: OONI Coverage
description: Which networks OONI measurements in Taiwan and nearby regions come from, how many users they cover, and which networks have no measurements at all.
lead: Censorship monitoring only covers the networks where someone runs OONI Probe.
---

OONI's censorship measurements come from volunteers running OONI Probe on their own connections. Within one region, each provider and network (ASN, autonomous system number) may block different sites, so when only one or two providers are measured, blocking on the others goes unrecorded. This page sets OONI's measurement counts against APNIC's estimates of how many users each network has, to show how many users the measurements cover, which networks they concentrate on, and which networks have none.

The page is regenerated every hour and OONI's measurements are read every six hours. Taiwan is shown by default, with other regions as reference points; switch between them with the region list below. Each quarter's changes are written up in the [quarterly reports](/projects/reports/).

<!-- asn-coverage -->

## How the numbers are calculated

- Measurement counts come from [OONI's aggregation API](https://api.ooni.io/), across all tests, grouped by the day each measurement started (UTC)
- Users per network are [APNIC's estimates](https://stats.labs.apnic.net/aspop/), derived from ad-based sampling and updated weekly
- Network names come from the APNIC and RIPE NCC ASN name lists
- A single measurement is enough for a network to count as measured; whether it is measured enough shows in its share of measurements and the number of days
- Days without measurements are left as gaps in the charts rather than filled in

## Help fill the gaps

- Install [OONI Probe](https://ooni.org/install/) and run tests on your own connection, on a phone or a computer. Mobile data and home broadband are usually different ASNs, so testing on both helps
- The community's OONI Run link `10328` sets everything up in one tap; see the [OONI Run v2 guide](docs:tools/ooni-run-v2/) for the risks to consider before installing and what the list contains
- [ASN observation data analysis](docs:taiwan/ooni-asn-coverage/): why network diversity matters and how to read a single measurement
- [ASN Coverage](https://github.com/anoni-net/asn-coverage): a command-line tool that downloads raw measurements and breaks them down by network type and blocking method
