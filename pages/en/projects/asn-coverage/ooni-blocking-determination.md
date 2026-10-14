---
title: OONI Blocking Verdicts
description: How the blocking field in OONI's Web Connectivity test is computed, the evidence behind each verdict, and why a value there is not a confirmed block.
---

In OONI (Open Observatory of Network Interference) data, `blocking` only records that one measurement disagreed with its control, which is several steps short of a confirmed block. Seeing `blocking: "dns"` is therefore usually not enough to conclude that a site is blocked in a given country.

Where each field sits in a measurement is described in [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/).

## The two-sided comparison

Measurements from the Probe alone cannot separate "the site is being interfered with" from "the site is down". The Web Connectivity test (`web_connectivity`) therefore measures the same URL twice, once from the Probe's network and once via an OONI test helper on an unrestricted network, and the two results are then compared.

A test helper is a measurement server OONI runs on an unrestricted network. Its observations are collected under `test_keys.control` and cover DNS resolution, TCP connection state and the HTTP response. Every verdict field is built on the difference between the two sides. The comparison runs stage by stage in the order below and stops at the first stage where the two sides differ:

<ol class="flow" aria-label="The four verdict stages of the Web Connectivity test">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>DNS resolution</b><span class="d">Compares both sides' A and AAAA answers for the same domain</span><span class="out"><span class="if">Answers differ</span><code>blocking: "dns"</code></span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>TCP connection</b><span class="d">Whether each side can connect to the target IP and port</span><span class="out"><span class="if">Only the Probe fails to connect</span><code>blocking: "tcp_ip"</code></span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>HTTP request</b><span class="d">Whether an HTTP response comes back once connected</span><span class="out"><span class="if">The HTTP stage fails</span><code>blocking: "http-failure"</code></span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>Response content</b><span class="d">Compares status code, title, headers and body length</span><span class="out"><span class="if">Content differs</span><code>blocking: "http-diff"</code></span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>All four stages agree</b><span class="out"><code>blocking: false</code><code>accessible: true</code></span></span></li>
</ol>

Because the comparison has already stopped at an earlier stage, all four `*_match` fields are `null` in the first three cases. Each of the four real measurements in the next section stops at one of these stages.

!!! tip "Reading order for `control` and `blocking`"

    `blocking` is the result of a two-sided comparison, not an observation from the Probe alone. When reading any anomalous measurement, first check what the test helper recorded in `test_keys.control`, then go back to `blocking`. In the `tcp_ip` example in the next section, skipping `control` would turn a site's own problem into an apparent block.

The full verdict algorithm is defined upstream in [ts-017-web-connectivity](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md), and the unified naming for failure strings is in [df-007-errors](https://github.com/ooni/spec/blob/master/data-formats/df-007-errors.md).

## The evidence behind each verdict

The five measurements cited below are all public data from 2026-08-04, and the raw content can be looked up on [OONI Explorer](https://explorer.ooni.org/).

### `dns`, mismatched DNS answers

In a measurement of `https://ntc.party/` from Taiwan, the Probe's A and AAAA queries both returned `dns_nxdomain_error` (domain does not exist) while the test helper resolved the name, so `dns_consistency` was marked `inconsistent`.

```json title="test_keys.queries"
{"query_type": "A", "failure": "dns_nxdomain_error", "answers": []}
{"query_type": "AAAA", "failure": "dns_nxdomain_error", "answers": []}
```

When reading a DNS verdict, check which network the resolver belongs to. In that measurement, the resolver's autonomous system number (ASN, `resolver_asn`) is `AS13335` (Cloudflare), while the Probe's ASN (`probe_asn`) is `AS3462` (Chunghwa Telecom). When the measurer points DNS at an overseas service, an anomaly at the DNS stage does not necessarily reflect what the local carrier is doing.

### `tcp_ip`, failed connections to the target address

A measurement of `http://www.tkec.com.tw/` from Taiwan came back as `tcp_ip`. DNS resolved normally to `210.64.193.1`, and the Probe timed out connecting to port `80`.

Reading only the Probe side invites the conclusion that the site was blocked, but comparing it with `control` gives a different result:

```json title="test_keys.control.tcp_connect"
{"210.64.193.1:443": {"status": true,  "failure": null},
 "210.64.193.1:80":  {"status": false, "failure": "generic_timeout_error"}}
```

The test helper timed out on port `80` from the outside as well, so the site's port `80` was unreachable from anywhere, and the network in Taiwan had nothing to do with it. Port `443` on the same IP connected from both sides, which places the problem at that one port rather than along the path.

### `http-failure`, failed content retrieval after connecting

A measurement of `https://bit.ly/` from Taiwan came back as `http-failure`. DNS was fine, port `443` on both target IPs connected, and `control` recorded the same from the test helper's side. The difference showed up during the HTTP stage as `generic_timeout_error`.

A working connection layer with a failing application layer is common with server-side rate limiting, refusal of service to particular sources, and breaks at the TLS layer. Telling those apart means reading the timing in `tls_handshakes` and `network_events`.

### `http-diff`, mismatched content

Taiwan's data does contain `http-diff`, though not in this shape (see "Taiwan's current data" below), so the example here comes from Indonesia to show a typical block page.

Of the four types only `http-diff` puts the four `*_match` fields to work, and a measurement of `http://www.sportsinteraction.com/` in Indonesia is a textbook case:

| Observer | Status code | Title | Body length |
|---|---|---|---|
| Probe | `200` | `Trustpositif` | 7,044 |
| test helper | `403` | `Maintenance` | 7,067 |

The Probe's request was redirected to `http://lamanlabuh.aduankonten.id/`, an Indonesian government content-complaint domain, and the page title `Trustpositif` is the name of the country's content filtering system. An ISP steering users to a notice page mid-connection is the most typical cause of `http-diff`.

In the same measurement, no single field would have been enough on its own:

```text title="The four *_match fields and body_proportion"
title_match: false        status_code_match: false
headers_match: true       body_length_match: true
body_proportion: 0.9967
```

`body_length_match` is `true` and `body_proportion` is close to `1` purely because the block page happens to be about as long as the control page. Reading length alone gives the wrong answer. Read all four together, and note that `title_match` and `status_code_match` usually discriminate best.

## Sources of misreading

A value in `blocking` with no actual network interference behind it is normal in this dataset, and the unreachable port `80` on `tkec.com.tw` above is one case.

A measurement of `http://www.newipnow.com/` from Egypt is a subtler one. It came back as `http-diff`, with three of the four `*_match` fields not matching and `body_proportion` at just `0.02`, which looks like an injected block page. The actual content:

| Observer | Status code | Title |
|---|---|---|
| Probe | `520` | `newipnow.com \| 520: Web server is returning an unknown error` |
| test helper | `200` | `Buy Private Proxies: $0.88 per Dedicated Premium IP - NewIPNow` |

`520` is the error page returned by Cloudflare, sitting in front of the target site, when the origin server misbehaves. It means the site itself was failing at the time, and Egyptian network controls had nothing to do with it. That measurement's `probe_asn` is `AS13335` (Cloudflare), so the measuring end was also running on Cloudflare's network, which falls under the second category below.

Common sources of misreading group into a few kinds:

- **The origin site's own state**: server errors, maintenance pages, CDN error pages, geographic restrictions.
- **The measurement environment**: with a VPN or Tor (onion routing network) running, the Probe measures the network at the exit instead.
- **Dynamic site content**: rotating ads, personalisation and A/B tests make the two sides differ by design.
- **A failing control**: when `control_failure` has a value, the comparison has no basis.

OONI handles the same class of problem at the dataset level, and the heuristics it uses to filter anomalous submissions are described in [Faulty Measurement Detection and Anonymous Credentials at OONI](/articles/ooni-faulty-measurements/).

## Corroboration beyond a single measurement

Getting from an observation to "this site is blocked in this place" takes more than one measurement, and in practice a few more dimensions have to be added:

1. **Across time**: the same URL producing the same verdict repeatedly over days or weeks rules out a one-off outage.
2. **Across ASNs**: several carriers measuring the same result points at behaviour common to the network layer. A result confined to one ASN is more likely that operator's own configuration.
3. **Across resolvers**: a result that stays anomalous after switching DNS resolvers rules out the resolver itself.
4. **The `confirmed` field**: OONI's backend matches measurements against known block-page fingerprints and marks `confirmed` as `true` on a hit. The field appears in [measurements API](https://api.ooni.org/api/v1/measurements) responses as backend analysis, and is not part of the raw data the Probe produces.

Bulk retrieval for comparisons across time or across ASNs is described in [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/).

!!! warning "`confirmed` versus `http-diff`"

    `confirmed` is based on block fingerprint matching and is easily conflated with `http-diff`. DNS steered to a known blocking IP is also marked `confirmed`, while the verdict type stays `dns`. At the time of writing, we spot-checked 5 `confirmed` measurements each from Iran, Russia, Turkey and China, and every sample had `blocking: "dns"`. The sample is small, enough to tell the two apart but not to support a general rule.

## Taiwan's current data

The figures below come from the full 24 hours of Taiwanese `web_connectivity` data ending 2026-08-05, 22,105 measurements in total. Every measurement in that window was parsed line by line from S3 and its `test_keys.blocking` tallied per ASN:

| Verdict | Measurements | Share |
|---|---|---|
| `false` (no interference observed) | 21,029 | 95.13% |
| `none` (no verdict recorded) | 512 | 2.32% |
| `tcp_ip` | 312 | 1.41% |
| `dns` | 150 | 0.68% |
| `http-failure` | 67 | 0.30% |
| `http-diff` | 35 | 0.16% |

The four interference types add up to 564 measurements, 2.55% of the total. `none` covers measurements with missing `test_keys` or a `null` blocking, so before calculating an anomaly rate, decide whether they belong in the denominator.

Separately, of 100 anomalous measurements checked, 0 had `confirmed` set to `true`, consistent with the long-standing findings in [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/).

!!! warning "Distribution bias from small samples"

    In an earlier draft of this page, we estimated the verdict distribution from 40 measurements sampled off the measurements API's anomaly listing and concluded that `dns` dominated and `http-diff` was absent. Full-population counts contradict both: `tcp_ip` runs more than double `dns`, and `http-diff` does occur. The API's anomaly listing has its own ordering and does not behave as a random sample. For distributions, run the full-population count, as described in [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/).

Taiwan's `http-diff` is a different phenomenon from the Indonesian example above. Across 15 of them sampled from a four-hour window, `body_proportion` ran between `0.004` and `0.21`, meaning the Probe retrieved far less content than the control, the opposite of the block page pattern that sits close to `1`. Very short content usually points at an error page or an empty response. Establishing the cause needs the evidence layer checked measurement by measurement, and we do not attempt that here.

To rerun the statistics above yourself:

```bash title="Get the verdict distribution"
uv run python ooni.py lookback --units=24 --loc=TW --frame=hours
```

Running it prints the `blocking` totals and writes the per-ASN distribution into the CSV. Individual measurements still come from the API:

```bash title="List anomalous measurements from Taiwan"
curl -s "https://api.ooni.org/api/v1/measurements?probe_cc=TW&test_name=web_connectivity&anomaly=true&limit=100" \
  | python3 -m json.tool | head -40
```

These figures are a snapshot of a single 24-hour window, reflecting that day's shape and not enough to conclude anything about longer trends. Trends need a longer span, and Taiwan's observations carry their own limitation in how concentrated they are across ASNs (see [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/)).

## Related reading

- [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/): the starting point for comparisons across time and ASNs, covering bulk retrieval from the public dataset and how coverage is calculated
- [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/): the fields that make up a single measurement and how to read them
- [OONI Nettest Quick Reference](/projects/asn-coverage/ooni-nettests-map/): what each nettest in ooni/spec measures and which appear in Taiwan's dataset
- [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/): OONI coverage across Taiwan's ASNs and how concentrated it is
- [Maintaining the OONI Test List](/join/ooni-test-list/): how the test list that OONI Probe measures against is maintained
