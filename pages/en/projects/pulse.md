---
title: Tor Relay Watch
description: Pulse, run by the anoni.net community, collects Tor relay data for Taiwan and nearby regions every hour. The charts show relay counts, bandwidth, the networks relays run on, Tor versions and relay roles.
lead: How many Tor relays Taiwan and nearby regions run, and on which networks.
---

Tor relays are volunteer servers that carry encrypted traffic for Tor users around the world. The more running relays and bandwidth a region has, the more it contributes to the network. Spread matters too: when every relay sits on one provider, trouble at that provider, or pressure on it, takes them all down together.

The data comes from [Pulse](https://github.com/anoni-net/pulse), which the community runs. It collects from Onionoo, part of Tor Metrics, every hour, and the page is regenerated every hour as well. Taiwan is shown by default, with other regions as reference points; switch between them with the region list below. Each quarter's changes are written up in the [quarterly reports](/projects/reports/).

<!-- pulse -->

## How the numbers are calculated

- Each day uses its last snapshot, not every relay seen during the day
- Bandwidth is the sum of the observed bandwidth of running relays
- Share of network weight is the sum of the running relays' consensus weight fractions, collected since October 2026
- User estimates come from [Tor Metrics](https://metrics.torproject.org/userstats-relay-country.html), updated daily with a lag of two to three days; [How many people use Tor in Taiwan](docs:regional/taiwan-tor-users/) explains the method and its limits
- Relay roles follow Onionoo's probabilities: a relay counts as a guard, middle or exit when that probability is above zero
- Days when collection was interrupted show as gaps in the charts, with nothing filled in
- The raw data is available from the [Pulse API](https://anoni.net/api/readme); this page uses `/api/summary`

## Running your own

- [Setting up a Tor relay](docs:community/setup-tor-relay/)
- [Tor relays on campus](/join/relay-on-campus/), one of the community's three focus areas for 2026
- [Ask about Tor relays in plain language](docs:community/onionoo-mcp/)
- [How many people use Tor in Taiwan](docs:regional/taiwan-tor-users/)
