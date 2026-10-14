---
title: Tor Users in Taiwan
description: Tor Metrics estimates of Tor usage in Taiwan, the four-year trend and regional comparisons, and the counting bug behind the tenfold spike of 2025.
---

[Tor Relay Watch](/projects/pulse/) covers the relay side: how many relays Taiwan runs, which autonomous systems (ASNs) they sit in, and how much bandwidth they contribute. This page covers the user side of the same network: how many clients connect to [Tor](docs:tools/what-is-tor/) (onion routing network) from Taiwan, how that has changed over four years, and how the pattern of use compares with other regions.

The data comes from public Tor Metrics CSV files under CC0. Retrieval commands are at the end of the page, so anyone can reproduce the figures.

Taiwan averages about 9,500 Tor clients online at any given moment, up gradually from roughly 7,400 four years ago with no jump in any single year. Between September 2025 and mid-2026 the same figure briefly reached ninety thousand. That stretch came from a bug in Tor's own counting code and cannot be read as user growth.

## Estimation Method

Tor has no accounts and does not count devices, so the number of users can only be inferred. Relays record how many directory requests they serve, and Tor Metrics works backwards from the request count. The formula is in the project's Reproducible Metrics documentation[^1]:

```
r(N) = floor(r(R) / frac / 10)
```

`r(R)` is the number of successful directory requests reported from a country on a given day, and `frac` is the share of relays reporting statistics that day. The division by `10` comes from an assumption stated in the documentation: "A client that is connected 24/7 makes about 15 requests per day, but not all clients are connected 24/7, so we picked the number 10 for the average client."

The limit of the estimate is stated in the same document:

> The result is an average number of concurrent users, estimated from data collected over a day. We can't say how many distinct users there are.

The accurate phrasing of "Taiwan has 9,500 Tor users" is therefore **an average of about 9,500 Tor clients concurrently online**. The number of people in Taiwan who opened Tor Browser at some point during a year is considerably higher, and the official method cannot produce that figure.

Tor Metrics also publishes a confidence interval[^2]:

| Measure | Average since August 2026 |
|---|---|
| Estimate | 9,541 |
| Lower bound | 6,641 |
| Upper bound | 13,823 |

Single days have wider intervals: the estimate for 2026-09-15 is 8,312, with an interval from 3,119 to 16,881. The figures on this page carry direction and relative change; treated as a precise headcount they go beyond what the data supports.

## Four Years of Slow Growth

Excluding the period affected by the counting bug from September 2025, and taking the same months each year[^3]:

| Period | Average concurrent clients | Per 100,000 residents |
|---|---|---|
| June to August 2023 | 7,420 | 31.9 |
| June to August 2024 | 8,638 | 37.2 |
| June to August 2025 | 8,794 | 37.8 |
| August to mid-September 2026 | 9,541 | 41.1 |

That is roughly 29% over four years, or about 8.7% a year compounded across the three annual intervals, with every interval rising.

The size of the growth splits into two questions with different answers: how precise the absolute count is, and whether the level moved.

On the absolute count, the official confidence interval runs from 4,782 to 10,233 in summer 2023 and from 6,641 to 13,823 in summer 2026. The two overlap, so the data cannot answer "how many thousand people in Taiwan use Tor" with a usefully narrow range.

On the level, daily means computed the same way fall between 7,173 and 7,667 in 2023 and between 8,286 and 10,795 in 2026. Those do not overlap[^10], and the level did rise.

The two answers do not conflict, because a large part of the official interval comes from the estimation method itself. The `frac` extrapolation and the ten-requests-per-client assumption belong to that part, and their error leans the same way every year. It largely cancels when comparing how much this year exceeds earlier years, and does not cancel when asking how many people there are this year. The data supports "the level in Taiwan rose about 29% over four years". It does not support "Taiwan has 9,541 Tor users".

The same windows applied to nearby jurisdictions and a few reference countries put Taiwan's 28.6% in the middle of the range[^12]:

| Region | Four-year change | Region | Four-year change |
|---|---|---|---|
| United Kingdom | +92.9% | Taiwan | +28.6% |
| Australia | +56.2% | Hong Kong | +7.6% |
| Singapore | +55.3% | United States | +4.2% |
| South Korea | +44.9% | Japan | −6.9% |

The median across those eight is 26.3%, which puts Taiwan almost exactly in the middle. Tor use has grown gradually across most open network environments in these years, and Taiwan is neither leading nor lagging.

## The 2025 Tenfold Spike and the Counting Bug

Taiwan's curve on Tor Metrics rises sharply from September 2025. The daily figures:

| Date | Taiwan | Worldwide |
|---|---|---|
| 2025-08-30 | 8,429 | 1,932,889 |
| 2025-08-31 | 14,531 | 2,951,998 |
| 2025-09-01 | 82,626 | 14,824,760 |
| 2025-09-02 | 109,607 | 19,374,696 |

Worldwide the count went from 1.95 million to 14.8 million in a single day, and Taiwan's from 8,429 to 82,626. Real adoption curves do not have that shape, and a simultaneous jump worldwide places the problem in the Tor network as a whole rather than in anything local to Taiwan.

The cause is documented in the release notes for Tor `0.4.8.22`: two problems compounded, and each received a fix[^4]. The first fix concerns old clients that could no longer reach a directory server:

> Allow old clients to fetch the consensus even if they use version 0 of the SENDME protocol. In mid 2025 we changed the required minimum version of the "FlowCtrl" protocol to 1, meaning directory caches hang up on clients that send a version 0 SENDME cell. Since old clients were no longer able to retrieve the consensus, they couldn't learn about this required minimum version -- meaning we've had many many old clients loading down directory servers for the past months.

The second concerns incomplete transfers being counted as successes:

> Don't count networkstatus serves until they finish. When we started serving a consensus document but the client didn't receive all of it, we were still counting that as a success in our stats. This mistake, which can be triggered for example by obsolete clients or by DPI-based censorship, led to wildly inflated user counts because we estimate total users in the world based on successful consensus fetches.

Once the minimum protocol version was raised, directory servers hung up on old clients mid-transfer. The upgrade requirement was inside the consensus those clients could no longer fetch, so they kept retrying. Every incomplete request was recorded as a success, and the user estimate inflated in proportion.

The fix was released on 2026-01-28 and took effect gradually as relays upgraded. Network-wide upgrade share against Taiwan's monthly average:

| Date | Relays running the fixed version | Taiwan monthly average |
|---|---|---|
| 2026-01-15 | 2.6% | 91,258 |
| 2026-03-15 | 65.8% | 25,906 |
| 2026-05-15 | 80.7% | 23,647 |
| 2026-07-15 | 89.0% | 11,075 |
| 2026-09-15 | 99.5% | 8,803 |

The two curves track each other segment by segment, and the endpoint of the decline (about 8,800) sits almost exactly at the pre-event level (8,794 averaged across June to August 2025).

Inflation varied by region. Taking August 2025 as the baseline against January 2026: Indonesia 12.4x, Thailand 10.8x, Taiwan 10.2x, and Vietnam 9.1x, against the United States at 1.6x, the United Kingdom at 1.5x, and Germany at 1.4x. Regions with more old clients were hit hardest.

When a similar jump appears, first compare it against the worldwide figure and neighbouring regions for the same period; if everything moves together, it is not a local event. Then read Tor's release notes for changes to how counting works. Any comparison spanning September 2025 to June 2026 needs a note that the two sides are not comparable.

## Four Characteristics of Tor Use in Taiwan

### Low Bridge Share

People who cannot reach public relays switch to bridges, the entry points not listed in the public directory. A high bridge share usually indicates that Tor is being blocked locally[^5]:

| Region | Direct | Bridge | Bridge share |
|---|---|---|---|
| Russia | 22,224 | 90,192 | 80.2% |
| Mainland China | 2,301 | 2,513 | 52.2% |
| Iran | 64,619 | 21,943 | 25.4% |
| Hong Kong | 6,332 | 521 | 7.6% |
| Taiwan | 9,541 | 503 | 5.0% |
| Germany | 307,354 | 6,063 | 1.9% |
| Vietnam | 23,298 | 278 | 1.2% |

Taiwan's 5.0% falls in the range of unobstructed environments, an order of magnitude below the blocked ones.

The bridge share alone cannot establish how heavy the blocking is. Vietnam's 1.18% sits below Germany's 1.93%, while Vietnam's network controls are generally considered the stricter of the two. Bridge use also has motives beyond national blocking: a corporate or campus network blocking Tor exit addresses, or someone not wanting the local network administrator to see Tor traffic, both push the share up. A high share almost always means something is in the way. A low share does not guarantee that nothing is.

Measurements from [OONI](docs:tools/what-is-ooni/) (Open Observatory of Network Interference) agree: across 168,197 `tor` tests from Taiwan since 2023, confirmed blocking stands at 0[^6]:

| Year | Measurements | Anomaly rate | Confirmed blocking |
|---|---|---|---|
| 2023 | 28,124 | 12.3% | 0 |
| 2024 | 60,930 | 13.3% | 0 |
| 2025 | 40,546 | 16.7% | 0 |
| 2026 | 38,597 | 8.2% | 0 |

The anomaly rate in each year is within the test's ordinary variation and shows no sign of systematic blocking.

### Weekday-Shaped Usage Curve

Dividing the weekend average by the weekday average, a value below 1 means lighter weekend use[^7]:

| Region | Ratio | Region | Ratio |
|---|---|---|---|
| Indonesia | 0.705 | Russia | 0.995 |
| Thailand | 0.735 | United States | 0.996 |
| Philippines | 0.822 | United Kingdom | 1.000 |
| India | 0.838 | Australia | 1.005 |
| Vietnam | 0.845 | Germany | 1.016 |
| South Korea | 0.854 | Singapore | 1.016 |
| Malaysia | 0.905 | Iran | 1.019 |
| Taiwan | 0.947 | Japan | 1.028 |

Europe, North America, and Japan sit at or above 1.0, where Tor is closer to part of ordinary personal browsing. Taiwan's 0.947 leans toward weekdays, which may mean that work and research settings carry more of the weight.

### Mid-Range Position in the Asia-Pacific

Converted to users per 100,000 residents[^8]:

| Region | Per 100,000 | Region | Per 100,000 |
|---|---|---|---|
| Singapore | 437 | Taiwan | 43 |
| Germany | 371 | Malaysia | 37 |
| United Kingdom | 177 | Thailand | 31 |
| United States | 164 | Japan | 26 |
| Australia | 139 | Vietnam | 23 |
| Iran | 94 | Indonesia | 22 |
| Hong Kong | 91 | Philippines | 21 |
| Russia | 78 | India | 9 |
| South Korea | 55 | Mainland China | 0.3 |

Taiwan sits above Japan, Southeast Asia, and India, and below South Korea, Hong Kong, Europe, and North America. Singapore's and Germany's high values need the hosting factor taken into account. Both host large volumes of cloud servers, and clients running on VPS instances count toward the country where the server is located.

### Bridge Use Growth in 2026

Taiwan's bridge users rose from a quarterly average of 137 in Q2 2025 to 501 in Q3 2026. The growth came after the counting bug was fixed, and bridge statistics follow a different path from direct-connection statistics, so it is more likely a real change, though the cause is still unclear.

Broken out by transport[^9]:

| Quarter | obfs4 | snowflake | webtunnel | unobfuscated | Total |
|---|---|---|---|---|---|
| 2025Q2 | 94 | 8 | 3 | 30 | 137 |
| 2026Q1 | 100 | 25 | 12 | 43 | 184 |
| 2026Q2 | 151 | 47 | 13 | 62 | 276 |
| 2026Q3 | 321 | 27 | 17 | 135 | 502 |

The growth concentrates in obfs4 and in unobfuscated bridges, with WebTunnel rising from 3 to 17 (see [Tor Browser advanced settings](docs:tools/tor-browser-advanced/) for the differences between transports). Q3 2026 covers less than three months, and the Tor Metrics news page records several fixes to Snowflake statistics in February and March 2026, so short-term movement in the snowflake column calls for caution.

In an environment with no national-level blocking, bridge demand still exists and still moves. Institutional blocking is a plausible explanation, but national-level measurement cannot separate it out. OONI Probe runs mostly on residential networks, and corporate and campus networks fall outside its coverage.

## Gap Between Usage and Relay Contribution

Taiwan accounts for about 0.33% of Tor users worldwide while hosting only 0.12% of the network's relays, a gap of roughly three to one between consumption and contribution[^11]. Per local relay that works out to 795 local users in Taiwan, against 168 in the United States and 188 in Germany. The ratio reflects how responsibility is shared and has no bearing on actual traffic load, because Tor path selection does not prefer relays in the user's own country. Relay counts in the United States and Germany are high partly because those are cheap, legally settled hosting markets where volunteers worldwide place their nodes, so those two figures reflect hosting economics as much as local participation. Live relay-side figures and the ASN breakdown are on [Tor Relay Watch](/projects/pulse/), and the [Tor Relay Setup Guide](/join/setup-tor-relay/) covers adding a relay.

!!! example "Reproducing the Figures"

    Taiwan's direct and bridge user counts come from two public CSV files, with no key required:

    ```bash
    curl -o tw-relay.csv "https://metrics.torproject.org/userstats-relay-country.csv?start=2023-01-01&end=2026-09-19&country=tw&events=off"
    curl -o tw-bridge.csv "https://metrics.torproject.org/userstats-bridge-combined.csv?start=2023-01-01&end=2026-09-19&country=tw"
    ```

    Omitting `start` and `end` returns the full history from 2011 onwards, about 37 MB each. The files open with several lines of `#` comments that need filtering before reading them with a CSV module. Substituting another two-letter country code reproduces any of the regional comparisons above.

## Related Reading

- [Tor Relay Watch](/projects/pulse/): relay counts, bandwidth, and ASN distribution for Taiwan and nearby regions, updated hourly
- [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/): how Taiwan's OONI measurements concentrate in a few ASNs
- [Tor Relay Setup Guide](/join/setup-tor-relay/): installing, configuring, and monitoring relays, bridges, and exit nodes
- [Tor Relays on Campus Track](/join/relay-on-campus/): the process and experience of running relays on campus networks

[^1]: Formula and assumption from the Tor Project's [Reproducible Metrics](https://metrics.torproject.org/reproducible-metrics.html). `frac` measures the share of relays network-wide reporting statistics on a given day. Its value is identical across all countries on the same date, so it is not a per-country reliability score: on 2023-06-15 every country reads `64`, and on 2026-09-15 every country reads `56`.
[^2]: Confidence bounds are the `lower` and `upper` columns of `userstats-relay-country.csv`, present on 97% of days across the period. The table averages 2026-08-01 to 2026-09-17.
[^3]: Matching months each year avoids seasonal effects. The 2026 window moves to August and September because only 80% to 89% of the network had upgraded to a fixed version during that June to August, leaving residual counting-bug inflation in those months; the figures are clean only after the upgrade share reached 99.5% in mid-September. The cost is that the 2026 window covers two months rather than three and falls in different months, so the seasonal effect is not fully avoided. Population figures for Taiwan use the Ministry of the Interior count of 23,235,002 (July 2026).
[^4]: Both quotations come from the release notes for Tor `0.4.8.22`, published 2026-01-28, corresponding to issues [`41191`](https://gitlab.torproject.org/tpo/core/tor/-/issues/41191) and [`41192`](https://gitlab.torproject.org/tpo/core/tor/-/issues/41192). Upgrade shares are computed from `versions.csv`, treating the `0.4.9` series and `0.4.8.22` as carrying the fix. The Tor Metrics news page carries no annotation for this period.
[^5]: Direct and bridge figures both average 2026-08-01 to 2026-09-17, from `userstats-relay-country.csv` and `userstats-bridge-country.csv`.
[^6]: From the OONI API `aggregation` endpoint with `probe_cc=TW` and `test_name=tor`. The 2026 row runs to September 20. "Confirmed blocking" is OONI's `confirmed` category, which requires a recognisable block page.
[^7]: Daily data from 2023-01-01 to 2025-08-30, avoiding the period affected by the counting bug. Block bootstrap resampling by week puts Taiwan's ratio at 0.947 with a 95% interval of 0.935 to 0.959, separable from Japan, South Korea, Malaysia, Thailand, Indonesia, and Germany, but overlapping with the United States.
[^8]: User counts combine direct and bridge connections, averaged 2026-08-01 to 2026-09-17. Population figures outside Taiwan are approximate 2025 estimates, so this column carries orders of magnitude rather than a precise ranking. Total population rather than online population is the denominator, which systematically understates density in Indonesia, Vietnam, and India.
[^9]: From `userstats-bridge-combined.csv`, which supplies `low` and `high` bounds; the table takes the midpoint. "Unobfuscated" is the file's `<OR>` category, meaning a plain bridge with no pluggable transport. Bridges do not report directory requests by transport, so the Tor Project approximates the split using each transport's share of unique IP addresses and then applies the same formula used for direct connections, layering two approximations.
[^10]: Daily figures are strongly autocorrelated, so dividing the standard deviation by the square root of the day count understates the standard error. These intervals correct the effective sample size using the first-order autocorrelation coefficient: `ρ` is 0.604 in summer 2023, reducing 92 days to an effective 22.7, and 0.782 in 2026, reducing 48 days to 5.9. The two intervals remain separate after the correction.
[^11]: The two shares use different windows. The user share is a Q3 2026 quarterly average from `userstats-relay-country.csv`; the relay share is a point-in-time snapshot from Onionoo on 2026-09-19. Comparing across windows carries the order of magnitude, not the decimal.
[^12]: Every region uses the same windows as Taiwan: June to August 2023 against August 1 to September 17, 2026. Germany and the worldwide total are excluded because both were affected by Germany's anomalously high user count in summer 2023, which makes that span non-comparable.
