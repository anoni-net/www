---
title: Tor Relay Watch
description: Pulse, run by the anoni.net community, collects Tor relay data for Taiwan and nearby regions every hour. The charts show relay counts, bandwidth, the networks relays run on, Tor versions and relay roles.
lead: How many Tor relays Taiwan and nearby regions run, and on which networks.
---

Tor relays are volunteer servers that carry encrypted traffic for Tor users around the world. The more running relays and bandwidth a region has, the more it contributes to the network. Spread matters too: when every relay sits on one provider, trouble at that provider, or pressure on it, takes them all down together.

The data comes from [Pulse](https://github.com/anoni-net/pulse), which the community runs. It collects from Onionoo, part of Tor Metrics, every hour, and the page is regenerated every hour as well. Taiwan is shown by default, with other regions as reference points; switch between them with the region list below. The [glossary](#glossary) at the end of the page explains the fields and flags. Each quarter's changes are written up in the [quarterly reports](/projects/reports/).

<!-- pulse -->

## Glossary {#glossary}

- **Tor relay**: a server that carries encrypted traffic for Tor users. A Tor connection passes through three relays in turn, an entry (guard), a middle and an exit, and each relay only knows the one before and the one after it
- **Snapshot**: Pulse reads the state of every relay from Onionoo once an hour, and each reading is a snapshot. Times on the page are UTC
- **Running, stopped**: a running relay is listed in the latest Tor network consensus. A stopped relay appeared in the past week but is missing from that consensus
- **Observed bandwidth**: the most traffic a relay reports it could sustain over the past few days, an upper bound on what it can carry. Actual traffic is usually lower. MB/s is megabytes per second; multiply by 8 for roughly Mbps
- **Autonomous system (ASN)**: a group of networks run by one organisation under one routing policy, such as a telecom, a university or a cloud provider, each with its own AS number
- **Exit relay**: the last relay on a connection, which reaches ordinary websites on the user's behalf. Websites see the exit relay's IP address, so exit operators handle more abuse complaints
- **Roles and flags**: the roles chart follows Onionoo's probabilities, counting any relay with a probability above zero. Flags come from the directory authorities under stricter conditions, so a region's number of guards by role and by flag can differ
- **Directory authorities**: a handful of servers run by people the Tor Project trusts, which vote every hour on the network consensus listing every relay and its flags
- **Tor version**: for example `0.4.9.13`. Versions sharing the first three parts belong to one series, and the last part is an update within it, usually with security fixes
- **Concurrent users**: Tor Metrics' estimate of the average number of Tor clients connected at the same time during a day. One person may use several devices, or use Tor for only a few minutes a day, so this is not a count of people
- **Bridge**: an entry relay that is not publicly listed in the Tor directory. Where connecting to Tor directly is blocked, users connect through bridges
- **Share of world users**: the region's users, direct and through bridges, as a share of all Tor users
- **Share of network weight**: Tor gives each relay a weight from bandwidth measurements (consensus weight), and clients pick relays by weight. The total weight of a region's relays roughly matches the share of Tor traffic passing through it
- **Reference region**: a region without its own page, listed in a comparison table for contrast

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
- [Tor relay lookup for AI assistants](/projects/onionoo-mcp/)
- [How many people use Tor in Taiwan](docs:regional/taiwan-tor-users/)
