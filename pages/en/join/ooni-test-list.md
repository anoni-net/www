---
title: Maintaining the OONI Test List
description: The Citizen Lab test list that OONI Probe measures against, covering its categories, how OONI turns categories into testing frequency, the state of Taiwan's tw.csv, and how to help maintain it.
---

When OONI Probe runs a web connectivity test, it checks each URL on a pre-defined list. What the list contains, whether its categories are right, and how often it is updated set a ceiling on what any later analysis can show, including work like [ASN diversity](/projects/asn-coverage/asn-diversity/). A stale list can make a country look uncensored simply because nobody is testing the sites that would fail. We are a community based in Taiwan, and Taiwan's list needs a thorough review; the work requires no programming.

The lists are maintained by [Citizen Lab](https://citizenlab.ca/) in the [test-lists](https://github.com/citizenlab/test-lists) project, split into a global list and country lists. The global list is mostly English-language sites. Country lists are gathered with help from local communities and cover sites in the local language and topics that matter locally. In countries with internet censorship, the country list also includes sites known to be blocked, so they stay under observation.

URLs on the list fall into four broad themes (the CSV itself uses about 30 finer-grained category codes):

1. **Political:** websites expressing viewpoints that differ from the current government, extending to human rights, freedom of expression, minority rights, and religious movements.
2. **Social:** gender, gambling, illegal drugs, alcohol, and other subjects considered sensitive locally.
3. **Conflict and security:** armed conflicts, border disputes, separatist movements, and radical groups.
4. **Internet tools:** email, cloud storage, search, translation, Voice over IP (VoIP), and censorship circumvention services.

## Categories and Testing Frequency

Besides organising the list, the categories determine how often each URL is tested. OONI Probe does not read the CSV directly: it receives an ordered list from the OONI API, and the ordering is computed in [`prio.py`](https://github.com/ooni/backend/blob/master/api/ooniapi/prio.py) in two stages.

The first stage produces a priority for each URL. OONI maintains a set of rules, each matching on four fields: category, domain, full URL, and country code, where `*` means any. Every matching rule is added to the total rather than overriding the others. The global default rule `*/*/*/*` contributes 50, and the category rule is added on top, so a URL filed under news media (`NEWS`) has a priority of `50 + 100 = 150`, while one filed under e-commerce (`COMM`) has `50 + 20 = 70`.

The current category weights, with the effective priority after adding the base of 50:

| Weight | Categories | Effective priority |
|---:|---|---:|
| +120 | `GRP` social networking | 170 |
| +100 | `ANON` anonymization and circumvention, `HUMR` human rights, `LGBT`, `NEWS` news media, `POLR` political criticism | 150 |
| +80 | `COMT` communication tools, `MMED` media sharing, `PUBH` public health, `SRCH` search engines | 130 |
| +60 | `ENV` environment, `HOST` hosting and blogging, `REL` religion, `XED` sex education | 110 |
| +40 | `CULTR` culture, `FILE` file sharing, `GOVT` government, `IGO` intergovernmental organisations | 90 |
| +30 | `ALDR` alcohol and drugs, `DATE` dating, `GMB` gambling, `HATE` hate speech, `MILX` militant groups, `PORN`, `PROV` provocative attire | 80 |
| +20 | `COMM` e-commerce, `CTRL` content control, `ECON` economics, `GAME` gaming, `HACK` hacking tools, `MISC` uncategorised | 70 |

Social platforms and speech-related categories sit at the top, commerce and entertainment at the bottom. The spread between them is 2.4x — a real gap, but well short of an order of magnitude.

The second stage divides the priority by the recent measurement count to get the actual sort key:

```
weight = priority / max(msmt_cnt, 0.1)
```

`msmt_cnt` is how many times that URL was measured during the current and previous week, scoped to the same country, or to the same ASN when the probe reports one. The more a URL is measured, the faster its weight decays, moving it down the list so that other URLs come forward.

The ordering therefore shifts with measurement counts: priority sets how much testing a URL gets, and the measurement count tracks how much of it has been used. A high-weight category buys a faster return to the front after being tested, not a permanent place there.

## Rules for Sudden Events

Beyond category weights, the rule table is used in two more ways. The first pushes a single target to the very front of the list. The settings as of 2026-09:

| Target | Scope | Priority |
|---|---|---:|
| `www.aljazeera.net` | Israel | `9999999` |
| `orda.kz` | Kazakhstan | `99999` |
| `eltoque.com` | Cuba | `6969` |
| Twitter, Facebook, Instagram and YouTube (four URLs) | Global | `69999` |

These priorities are far above the category weights, so the target stays at or near the top of the list, usually in response to blocking that is happening or has just happened.

The second sets a priority to a negative value to exclude a URL: entries whose priority is zero or below are skipped and never handed to a probe. The only negative rules currently in place are for Afghanistan, where alcohol and drugs, dating, gambling, hate speech, `LGBT`, militant groups, `PORN` and sex education are all set to `-9999`. The intent is to protect the people running measurements, so that content which could be dangerous locally never appears in their network logs.

The rule table has no country-level rules for Taiwan, so every entry in `tw.csv` is scored purely on "50 plus the category weight", and the category is the only field that affects how often an entry is tested. A miscategorised URL produces no error; it is simply tested less often, or more often, than it should be. When submitting list corrections, getting the category right is worth as much as finding a site worth adding.

The full rule table is available from the OONI API's [`url-priorities/list`](https://api.ooni.io/api/_/url-priorities/list) endpoint, and the design rationale is in OONI's [Building a smart URL list system](https://ooni.org/post/ooni-smart-url-list-system/).

## Current State of tw.csv

Taiwan's list, [`tw.csv`](https://github.com/citizenlab/test-lists/blob/master/lists/tw.csv), has 466 entries, 361 of them added in 2017 and left largely unmaintained since. Many point to sites that have shut down or moved to a new address, and 245 still use `http://` (checked 2026-10).

!!! note "http:// and https://"

    Some websites do not redirect `http://` to `https://` with [`301 Moved Permanently`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301) or [`308 Permanent Redirect`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/308), which produces misleading OONI results. TLS certificates are now easy to obtain and encrypted transport is a baseline expectation, so `https://` should be the default form for URLs on the list.

## Review of Existing Entries

The first step is to check each site in [`tw.csv`](https://github.com/citizenlab/test-lists/blob/master/lists/tw.csv), mark it as needing an update or ready to be dropped, and then open a pull request against [citizenlab/test-lists](https://github.com/citizenlab/test-lists). The same review applies to `lists/<country code>.csv` for any other country.

!!! info "PR #1444 and the approach since"

    We [submitted a list revision](https://github.com/citizenlab/test-lists/pull/1444) on 2023-09-28. It touched the list files of about 100 countries at once, which made it hard to review, and it was closed unmerged in 2026-09. Pull requests since then change only `lists/tw.csv`, each scoped small enough to be reviewed on its own, checking dead URLs and `http://` URLs entry by entry. Where a site has moved to a new domain, the URL is updated rather than deleted.

## Additions to the List

The largest addition since 2017 came in 2026-09: [PR #2267](https://github.com/citizenlab/test-lists/pull/2267) added 74 Taiwan sites and has been merged, with political criticism (`POLR`) the largest group at 20 entries. Candidates are screened against the four themes above, and the screening criteria are still under discussion in the community.

## Ways to Help

List maintenance is a good entry point for new contributors. It needs no programming, only:

- **An observant internet user's eye:** which sites are being discussed in Taiwan, which have recently shut down, which are new and worth adding
- **Judgement on categories:** sorting candidates into the four themes and the finer category codes
- **Basic GitHub skills:** fork, edit a CSV, open a pull request

Where to start, depending on what you want to work on:

- List maintenance: say so in the anoni-net public space on Matrix, and someone will help you pick a slice of the list to check (see [Take part](/join/) for how to join)
- Data analysis: [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/) and [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/)
- Reading the measurements: [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/) and [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/)
- Tests beyond this list: [OONI Nettest Quick Reference](/projects/asn-coverage/ooni-nettests-map/)

## Related Reading

- [Development Environment Setup](/join/dev-setup/): the environment needed to run the community's analysis tools
- [Tor Relay Watch](/projects/pulse/): the community's other observation project, collecting hourly data on Tor relays in Taiwan and nearby regions
- [What Is OONI?](docs:tools/what-is-ooni/): how OONI works, and what it is and is not suited for
- [Why networked freedom matters](docs:basics/internet-freedom/): background on internet censorship and internet freedom
