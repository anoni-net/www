---
title: OONI Nettest Quick Reference
description: What each of the 41 nettests in ooni/spec measures, which still produce data and which appear in Taiwan, with upstream spec links for picking a nettest.
---

OONI (Open Observatory of Network Interference) defines its network tests, or nettests, in the `nettests` directory of [ooni/spec](https://github.com/ooni/spec/tree/master/nettests). The directory holds 41 specifications, a fair share of which are no longer in use. When picking a nettest or making sense of data you already have, checking which ones still produce measurements is quicker than reading every specification.

At anoni.net, a community based in Taiwan, we have condensed all 41 into reference tables, noting each one's upstream status, whether public data still exists, and which ones show up in Taiwan. The fields their output shares are defined separately in [data-formats](https://github.com/ooni/spec/tree/master/data-formats).

!!! info "Status column definitions"

    **Spec status** comes from the `_status_` marker at the top of each specification. The marker is one of `current`, `experimental` or `obsolete`, and reflects how the upstream project positions that nettest.

    **Data in circulation** is an empirical check. As a snapshot on the day of writing (2026-08-04), we surveyed each nettest's most recent public measurements through the [OONI API](https://api.ooni.org/api/v1/measurements).

    **Taiwan** comes from the S3 public dataset. We spot-checked five time slots on 2026-08-03 and listed the nettest directories that appeared under Taiwan.

## Gaps between status markers and actual data

Status markers and actual data disagree in two directions:

- **Marked `current` with no data to be found**: `tlsmiddlebox`, `portfiltering` and `captiveportal`.
- **Marked `experimental` with data every day**: `dnscheck`, `echcheck`, `openvpn`, `stunreachability` and `vanilla_tor` among others, at volumes comparable to some `current` nettests.

An `experimental` marker concerns only the maturity of the specification itself, with no bearing on data volume. To judge whether a nettest suits your analysis, query the API for data rather than relying on the status marker.

## Nettests by purpose

Grouped by what they observe, with details in the tables that follow:

- **Website blocking detection**: `web_connectivity`
- **Middleboxes and interference techniques**: `http_header_field_manipulation`, `http_invalid_request_line`, `sni_blocking`, `echcheck`
- **Messaging app reachability**: `telegram`, `whatsapp`, `signal`, `facebook_messenger`
- **Circumvention tool availability**: `tor`, `vanilla_tor`, `torsf`, `psiphon`, `riseupvpn`, `openvpn`
- **DNS behaviour**: `dnscheck`, `dnsping`
- **Connection performance**: `ndt`, `dash`, `stunreachability`, `quicping`

## Nettests still producing data

Every nettest below had public measurements available on the day of writing. These are also the nettests you will meet most often in OONI data.

| Nettest | What it measures | Spec status | Taiwan |
|---|---|---|---|
| [`web_connectivity`](https://github.com/ooni/spec/blob/master/nettests/ts-017-web-connectivity.md) | Website reachability and block verdicts, by far the largest nettest by volume | current | yes |
| [`tor`](https://github.com/ooni/spec/blob/master/nettests/ts-023-tor.md) | Reachability of Tor directory authorities and bridges | current | yes |
| [`vanilla_tor`](https://github.com/ooni/spec/blob/master/nettests/ts-016-vanilla-tor.md) | Whether unobfuscated Tor can bootstrap a connection | experimental | yes |
| [`torsf`](https://github.com/ooni/spec/blob/master/nettests/ts-030-torsf.md) | Tor over the Snowflake pluggable transport | experimental | no |
| [`telegram`](https://github.com/ooni/spec/blob/master/nettests/ts-020-telegram.md) | Reachability of Telegram web and its data centre endpoints | current | yes |
| [`whatsapp`](https://github.com/ooni/spec/blob/master/nettests/ts-018-whatsapp.md) | Reachability of WhatsApp endpoints and its registration service | current | yes |
| [`signal`](https://github.com/ooni/spec/blob/master/nettests/ts-029-signal.md) | Reachability of Signal service endpoints | current | yes |
| [`facebook_messenger`](https://github.com/ooni/spec/blob/master/nettests/ts-019-facebook-messenger.md) | Reachability of Facebook Messenger endpoints | current | yes |
| [`dnscheck`](https://github.com/ooni/spec/blob/master/nettests/ts-028-dnscheck.md) | Behaviour of a given DNS resolver, covering encrypted queries (DoH, DoT) | experimental | yes |
| [`dnsping`](https://github.com/ooni/spec/blob/master/nettests/ts-035-dnsping.md) | Latency and response behaviour of DNS queries | experimental | no |
| [`echcheck`](https://github.com/ooni/spec/blob/master/nettests/ts-039-echcheck.md) | Support for and interference with Encrypted Client Hello (ECH) | experimental | yes |
| [`http_header_field_manipulation`](https://github.com/ooni/spec/blob/master/nettests/ts-006-header-field-manipulation.md) | Whether middleboxes tamper with HTTP headers | current | yes |
| [`http_invalid_request_line`](https://github.com/ooni/spec/blob/master/nettests/ts-007-http-invalid-request-line.md) | How middleboxes react to malformed request lines, used to detect transparent proxies | current | yes |
| [`openvpn`](https://github.com/ooni/spec/blob/master/nettests/ts-040-openvpn.md) | Whether an OpenVPN handshake completes | experimental | yes |
| [`psiphon`](https://github.com/ooni/spec/blob/master/nettests/ts-015-psiphon.md) | Whether the Psiphon circumvention tool can establish a connection | current | yes |
| [`riseupvpn`](https://github.com/ooni/spec/blob/master/nettests/ts-026-riseupvpn.md) | Reachability of the RiseupVPN service | current | yes |
| [`stunreachability`](https://github.com/ooni/spec/blob/master/nettests/ts-025-stun-reachability.md) | Reachability of STUN servers, which affects WebRTC calls | experimental | yes |
| [`ndt`](https://github.com/ooni/spec/blob/master/nettests/ts-022-ndt.md) | Connection speed and performance diagnostics | current | yes |
| [`dash`](https://github.com/ooni/spec/blob/master/nettests/ts-021-dash.md) | Video streaming playback quality | current | yes |
| [`browser_web`](https://github.com/ooni/spec/blob/master/nettests/ts-036-browser_web.md) | Loading pages with a real browser engine | experimental | no |

!!! note "Abbreviations in the table"

    - **DoH, DoT**: DNS queries wrapped in HTTPS or TLS, so query contents do not cross the network in plaintext. See [Encrypted DNS](docs:tools/encrypted-dns/).
    - **ECH (Encrypted Client Hello)**: the first message of a TLS handshake normally carries the destination domain in plaintext, and ECH encrypts that field.
    - **SNI (Server Name Indication)**: the destination domain sent in plaintext during a TLS handshake, frequently used as the basis for blocking decisions.
    - **STUN**: a protocol that helps a device discover its own public IP and port, used when WebRTC calls set up a connection.
    - **QUIC**: a UDP-based transport protocol that HTTP/3 is built on.

## Nettests with only occasional data

| Nettest | What it measures | Spec status | Most recent |
|---|---|---|---|
| [`quicping`](https://github.com/ooni/spec/blob/master/nettests/ts-031-quicping.md) | Reachability of the QUIC protocol | experimental | 2026-07-30 |
| [`sni_blocking`](https://github.com/ooni/spec/blob/master/nettests/ts-024-sni-blocking.md) | Blocking targeted at the TLS SNI field | experimental | 2026-07-20 |

## Nettests with no public data

The API returns no public measurements for the seven nettests below. Their specifications remain in the upstream repository, for reference when designing a new nettest or a research method.

| Nettest | What it measures | Spec status |
|---|---|---|
| [`tlsmiddlebox`](https://github.com/ooni/spec/blob/master/nettests/ts-037-tlsmiddlebox.md) | Middlebox behaviour along a TLS connection path | current |
| [`portfiltering`](https://github.com/ooni/spec/blob/master/nettests/ts-038-port-filtering.md) | Whether specific ports are filtered | current |
| [`captiveportal`](https://github.com/ooni/spec/blob/master/nettests/ts-010-captive-portal.md) | Whether the network requires a login to get out | current |
| [`urlgetter`](https://github.com/ooni/spec/blob/master/nettests/ts-027-urlgetter.md) | A general-purpose fetching component reused by other nettests | experimental |
| [`tcpping`](https://github.com/ooni/spec/blob/master/nettests/ts-032-tcpping.md) | Round-trip latency at the TCP layer | experimental |
| [`tlsping`](https://github.com/ooni/spec/blob/master/nettests/ts-033-tlsping.md) | Round-trip latency of a TLS handshake | experimental |
| [`simplequicping`](https://github.com/ooni/spec/blob/master/nettests/ts-034-simplequicping.md) | A simplified QUIC latency measurement | experimental |

## Historical nettests marked obsolete

Twelve specifications are marked `obsolete` upstream. Most of their functionality was absorbed into `web_connectivity` or retired as measurement methods evolved. Their records can still turn up in historical data, but there is no reason to adopt them for new observation work.

| Nettest | Specification |
|---|---|
| bridgeT | [ts-001](https://github.com/ooni/spec/blob/master/nettests/ts-001-bridget.md) |
| DNS Consistency | [ts-002](https://github.com/ooni/spec/blob/master/nettests/ts-002-dns-consistency.md) |
| HTTP Requests | [ts-003](https://github.com/ooni/spec/blob/master/nettests/ts-003-http-requests.md) |
| HTTP Host | [ts-004](https://github.com/ooni/spec/blob/master/nettests/ts-004-http-host.md) |
| DNS Spoof | [ts-005](https://github.com/ooni/spec/blob/master/nettests/ts-005-dns-spoof.md) |
| TCP Connect | [ts-008](https://github.com/ooni/spec/blob/master/nettests/ts-008-tcp-connect.md) |
| Multi Protocol Traceroute | [ts-009](https://github.com/ooni/spec/blob/master/nettests/ts-009-multi-protocol-traceroute.md) |
| Bridge Reachability | [ts-011](https://github.com/ooni/spec/blob/master/nettests/ts-011-bridge-reachability.md) |
| DNS Injection | [ts-012](https://github.com/ooni/spec/blob/master/nettests/ts-012-dns-injection.md) |
| Lantern | [ts-013](https://github.com/ooni/spec/blob/master/nettests/ts-013-lantern.md) |
| Meek Fronted Requests | [ts-014](https://github.com/ooni/spec/blob/master/nettests/ts-014-meek-fronted-requests.md) |
| OpenVPN Client Test (legacy) | [ts-016](https://github.com/ooni/spec/blob/master/nettests/ts-016-openvpn.md) |

!!! note "Duplicate ts-016 number and the legacy OpenVPN specification"

    Upstream has two specifications numbered `ts-016`: `ts-016-openvpn.md`, marked `obsolete` in the table above, and `ts-016-vanilla-tor.md`, marked `experimental`. The current OpenVPN specification is `ts-040-openvpn.md`, so take care not to cite the old one.

## Nettests observed in Taiwan

In a spot check of five time slots on 2026-08-03, 17 nettests appeared under Taiwan (written here in the API's underscore form): `web_connectivity`, `tor`, `vanilla_tor`, `telegram`, `whatsapp`, `signal`, `facebook_messenger`, `dnscheck`, `echcheck`, `http_header_field_manipulation`, `http_invalid_request_line`, `openvpn`, `psiphon`, `riseupvpn`, `stunreachability`, `ndt`, `dash`.

Directory names on S3 are written differently from the test name field (`test_name`). Directory names carry no underscores (`webconnectivity`, `vanillator`, `facebookmessenger`), while API queries need the underscore form (`web_connectivity`, `vanilla_tor`, `facebook_messenger`). For the retrieval path in detail, see [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/).

Taiwan's observations concentrate on `web_connectivity`, with small sample sizes for everything else. For widening local coverage, `tor` and `dnscheck` sit closest to our existing themes.

If OONI itself is new to you, start with [What is OONI?](docs:tools/what-is-ooni/). To run a specific nettest, choose which nettests to enable in the settings of [OONI Probe](https://ooni.org/install/) on desktop or mobile. To invite others to measure a fixed list of URLs, create a shareable link with [OONI Run v2](docs:tools/ooni-run-v2/). The link ID we currently maintain is `10328`.

## Related reading

- [The Structure of an OONI Measurement](/projects/asn-coverage/ooni-data-format/): the fields that make up an OONI measurement, and how to read them
- [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/): how OONI determines that a website is blocked
- [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/): the retrieval path for observation data, and how to analyse it
- [OONI Run v2 for regional measurement](docs:tools/ooni-run-v2/): creating and sharing a test link
- [OONI Website Testing List](docs:regional/ooni-checklist/): the list of websites that OONI Probe measures against
