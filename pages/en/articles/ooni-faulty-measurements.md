---
title: Faulty Measurement Detection and Anonymous Credentials at OONI
description: A guide to an OONI engineering post, covering the findings of four heuristic checks, proposed new detection methods, the principles for handling faulty measurements, and how the anonymous credential system scores trust without storing personal data.
date: 2026-07-17
---

Many people rely on OONI's public dataset to judge whether a website is reachable in a given country, and our [OONI Coverage](/projects/asn-coverage/) work for Taiwan and neighbouring regions is built on the same data. Anyone can submit to the dataset, so fabricated submissions or misconfigured devices producing misleading records dilute the reliability of the whole thing. In a recent engineering post,[^1] OONI explains how it finds faulty measurements and how the anonymous credential system it is rolling into production blocks abuse without storing personal data. Scoring the trustworthiness of measurements without keeping personal data is a privacy-engineering pattern worth studying in its own right, and we come back to it in the [section on the credential system](#credentials).

!!! info ""

    This is our guide to and summary of OONI's engineering post [From Heuristics to Anonymous Credentials: Assessing OONI's Approach to Bad Measurements](https://ooni.org/post/2026-faulty-measurements/) (2026-07-06). It follows the post's sections rather than translating it. The original has around 20 charts and several full data tables; read it for the detailed numbers.

OONI (Open Observatory of Network Interference) is a global project that observes internet censorship. OONI Probe connects to the sites on a test list one by one and reports whether each is reachable locally, and every result goes into a public dataset. Anyone can download the data for analysis, and anyone can also send data in. The question the post sets out to answer is how to recognise and filter out poor-quality measurements while keeping submissions open.

## Structure of the Original Post

OONI first builds a baseline for spotting faulty measurements from the data it already has, then assesses how far the new anonymous credential system can raise that baseline. A heuristic here is a simple, cheap rule of thumb: it does not aim for perfect accuracy, only for a first pass that flags suspicious measurements. The post has three parts. It checks how many problems simple rules can find in existing data (existing heuristics and four groups of findings), proposes more advanced rules (new heuristics), and then sets out what to do once faulty data has been found (mitigation strategies and anonymous credentials).

## Existing Metrics and Four Checks

The Existing metrics and heuristics section uses no new technology. It only asks whether the data OONI already collects is enough to recognise faulty measurements. OONI picked four checks that cost users no privacy: IP geolocation mismatches, measurement volume spikes, timestamp inconsistencies, and contradictions between OS and version metadata. Each comes with a caveat describing when the signal misfires. The GeoIP database bundled with the probe can be out of date, for example, so `probe_cc` (the country code the probe reports) will sometimes disagree with the real IP for ordinary reasons, and that baseline error has to be filtered out first. The four checks and their caveats are the methodological basis for everything that follows.

## Findings Across Four Anomaly Types

### IP Geolocation Mismatches

From 19 to 21 March 2025, OONI logged calls to the `/api/v1/check-in` endpoint and compared the country code and ASN (autonomous system number) each probe reported with the real egress IP seen by the collector. Of 16,139 samples, 1,196 did not match, about 7.41%. The ten most common country-code mismatches:

| Reported country | Country of real IP | Count |
|---|---|---|
| US United States | CA Canada | 89 |
| CA Canada | RU Russia | 49 |
| CZ Czechia | US United States | 43 |
| BS Bahamas | US United States | 36 |
| CA Canada | US United States | 30 |
| CA Canada | SG Singapore | 30 |
| CZ Czechia | GB United Kingdom | 25 |
| CA Canada | KH Cambodia | 18 |
| AU Australia | KH Cambodia | 18 |
| US United States | DE Germany | 16 |

Almost all of the mismatches came from VPNs. The networks that appeared most were known VPN hosting providers such as Datacamp, Cloudflare and M247. All 49 records reporting Canada with a real IP in Russia came from Cloudflare, which corresponds to users of a VPN such as WARP. Most rows in the table follow the same pattern: the probe reports country A while its traffic leaves through a VPN exit in country B. The post found no mismatches clearly attributable to deliberate tampering or probe misconfiguration.

### Measurement Volume Spikes

OONI counted how many measurements each probe produced per minute. The mean was 8 and the 99th percentile was 54. Filtering for extreme cases above 200 per minute turned up a client calling itself `ooniprobe-react-os`, which is not an official OONI release. It submitted data only for `probe_cc = CN` (China), sending `web_connectivity` measurements at 200 per minute, roughly three per second, far outside the normal range. More oddly, `ooniprobe-react-os` submitted faster than other probes in the same region, with no network bottleneck to match its volume. Another case was a burst of submissions from Myanmar on 6 January 2025.

### Timestamp Inconsistencies

OONI compared each measurement's `measurement_start_time` with the timestamp embedded in its `measurement_uid`, looking for records uploaded too late or dated in the future. Between 2 March and 1 April 2025, only 0.82% of more than 34.4 million measurements had timestamp anomalies. Most were in the past, and they were concentrated on Linux, whose 2.16% anomaly rate is clearly higher than the other platforms:

| Platform | Past anomalies (>1h) | Future anomalies (>1h) | Total anomalies | Platform total | Anomaly rate |
|---|---|---|---|---|---|
| ios | 2,375 | 0 | 2,375 | 240,843 | 0.99% |
| windows | 34,192 | 24,938 | 59,130 | 10,503,040 | 0.56% |
| android | 21,132 | 5,509 | 26,641 | 10,389,320 | 0.26% |
| macos | 906 | 0 | 906 | 3,103,961 | 0.03% |
| linux | 185,322 | 7,908 | 193,230 | 8,947,716 | 2.16% |

A large share of the anomalies came from a single ASN in Venezuela. After contacting a local partner, OONI found that those devices had the wrong time zone configured. With Venezuela excluded, the Linux figures drop sharply while the other platforms barely change. Misconfiguration alone is enough to produce misleading records, with no malice involved.

### Contradictory OS and Version Metadata

OONI checked whether the software name matched the platform, for example `software_name = ooniprobe-android` labelled as iOS. There were 718 measurements from Android software on non-Android platforms. Some were traced to OONI team members' own development machines; others came from the same China-only `ooniprobe-react-os` client. The post also lists several unfamiliar software names (Vladhog, murakami-ooniprobe, MySorgenia, Dismantle and others) and works out where each came from. Much of the data that looks suspicious comes from development work or third-party forks and has nothing to do with attacks.

### Implications for Data Users

OONI found no large-scale malicious pollution in its data. The vast majority of anomalies come from VPNs, misconfiguration, development machines or unofficial forks. Defences are still needed, but the threat today is not an imminent large-scale attack.

Our OONI Coverage analysis rests on the same public data, so a source without heavy pollution gives that analysis firmer footing. The four findings are also a reminder that `probe_cc` is not ground truth for local network conditions. Geolocation mismatches caused by VPNs and wrong time zones are part of the data, and they need filtering before analysis. In networks where genuine coverage is already thin, as in much of the Asia-Pacific, a small amount of such noise moves the picture more than it would elsewhere.

## Proposed New Heuristics

Beyond the existing rules, OONI wants to add more advanced detection. Location has always been the hardest part, because the probe looks up the GeoIP database itself and the database goes stale. The options under consideration include asking the phone's operating system for the mobile country and network codes (MCC/MNC), querying the OS location service, or matching IPs to locations on the server instead. The post notes a limitation for each: server-side matching cannot see the real IP when a circumvention tool sits in between, and asking for location permission may worry users. OONI also wants anomaly detection at the network and protocol layers, such as recognising man-in-the-middle devices (antivirus software that rewrites traffic, for instance) from their TLS handshake fingerprints.

## Principles for Handling Faulty Measurements

Detection is followed by handling, and OONI sets two principles. First, the final decision on whether a measurement is faulty goes through human review, so that automated rules do not discard good data. Second, data that has already been submitted is never modified unless leaving it unchanged would affect user privacy. Because a human has to be involved, handling can only happen after the faulty data has entered the data pipeline.

The available tools include blocking pseudonyms that behave abnormally, rate-limiting submissions, dynamically adjusting how many submissions are accepted for a given region and time window, and rotating issuer keys. A pseudonym is the identifier the anonymous credential system gives a probe. It stays fixed within one network, cannot be linked across networks, and does not map to anyone's real identity; the next section explains how. The post is open about the trade-offs. A rule accepting only probes older than six months would block Sybil attacks (flooding the dataset with fake identities), and it would also block legitimate new probes.

## The Anonymous Credential System {#credentials}

### Problems with Fixed Probe IDs

The obvious approach is to give every probe an ID and keep an allowlist on the server. Even a random ID, if it never changes, is enough to single out one probe, which is a privacy disaster, and a probe can get around a block by switching to a new ID. The core tension the credential system resolves is how to do access control and trust scoring together without keeping personal data long-term.

### Range-Based Credentials

The idea is close to an age check at a bar door: the staff look at a document proving the holder is an adult and let them in, without learning their name, address or date of birth. OONI's credential proves something different, namely that a probe has been around long enough and has submitted enough measurements.

The server issues the credential, but it is stored only on the probe; the server keeps no copy and the credential is not sent anywhere else. It cryptographically encodes the probe's age and submission count (`msm_count`), and proves only that each value falls within a range, such as "more than 1,000 measurements" or "older than a week", without revealing the exact figures. Ranges are a deliberate choice: an exact submission count is close to a unique fingerprint and would make the probe identifiable, while a coarse range does not leak identity.

### Zero-Knowledge Proofs at Submission

When it submits, the probe uses its credential to produce a zero-knowledge proof, a cryptographic method for proving a statement true without revealing the details. The server sees only the proof, never the underlying values, and can still decide whether the measurement satisfies an access rule, such as "probes in this country and ASN need 1,000 prior submissions". Trust is also bound to a specific country-code and ASN pair. Reputation a probe builds in one network cannot be carried to another, which stops someone from building up credentials in a low-threshold network and using them to attack a different one.

A brand-new probe starts with little age and few submissions, so it does not meet the stricter rules and simply keeps running measurements. Each time it submits, the server verifies the proof and returns an updated credential with the count incremented by one. Once enough time and volume have accumulated, the probe crosses thresholds like "one week" and "1,000 measurements", and its measurements from then on can be marked verified. At no point does OONI obtain a fixed ID for the probe or store any personal data.

### Copied Credentials and Sybil Attacks

Since the credential lives on the probe, could someone copy it a hundred times and pose as a hundred probes, each with its own reputation? The network-local property described above prevents this. Within one network, the same credential always derives the same pseudonym, so any number of copies is still treated as one probe rather than a hundred independent trusted identities. OONI is candid that credentials alone cannot fully solve Sybil attacks; complete defence needs application-layer measures such as rate-limiting new registrations and capping submissions per region. What the credential does is raise the cost of an attack, because an adversary first has to cultivate a set of probes that are old enough and have submitted enough.

### Verification States and Long-Term Metrics

Each measurement ends up marked verified, unverified or failed, and data users can decide for themselves how much weight to give each. Some effects only show over time. OONI will keep tracking the ratio between the three states to diagnose whether a client update has broken the protocol implementation, or whether old probes have not been updated. It will also count probes by protocol version and measure how long server-side verification of one measurement takes, so that performance regressions are caught early.

### Value as a Privacy Design Reference

Access control and trust scoring without storing personal data is a problem many systems run into. OONI trades away precise blocking of individual probes, and in return gets anonymity through range proofs and credentials stored only on the client. That trade-off is useful study material for anyone who cares about privacy design, and it connects to our [Personal Privacy Guide Track](/join/privacy-guide/).

## Reliability of the Dataset

OONI's public data is not heavily polluted by malicious submissions. The anomalies it found mostly come from honest mistakes such as VPNs, wrong time zones and development machines, so the data remains a sound basis for understanding blocking in Taiwan and elsewhere. For the cryptography behind the credentials, OONI has two related posts: one sets out the system's [requirements](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/),[^2] and the other [announces its design and implementation](https://ooni.org/post/2025-announcing-ooni-new-anonymous-credential-system/).[^3] Our guide to the second is [OONI Probe's Anonymous Credential System](/articles/ooni-anonymous-credentials/).

## Section-by-Section Summary

| Section in the original | Focus | Key figure or conclusion |
|---|---|---|
| Existing metrics and heuristics, Approach | A detection baseline from existing data | Four checks that cost no privacy |
| IP geolocation mismatches | Reported location against real IP | 7.41% mismatched, mostly VPNs |
| Measurement volume anomalies | Submission rate spikes from single probes | China-only `ooniprobe-react-os` at three per second |
| Timestamp inconsistencies | Measurement timestamps that do not line up | 0.82% anomalous, wrong time zones in Venezuela |
| Probe OS, version metadata | Software names that contradict the platform | 718 records, including team development machines |
| New heuristics | More advanced detection ideas | MCC/MNC, server-side GeoIP, TLS fingerprints |
| Mitigation strategies | Handling faulty data once found | Human review, no retroactive edits, rate limits, Sybil resistance |
| Naive solution | Problems with fixed IDs | A fixed ID de-anonymizes; a new ID evades blocks |
| Anonymous credentials solution | Credential-based trust scoring | Range proofs, client-side storage, no fixed ID |
| Future validation | Long-term validation metrics | Ratio of verified, unverified and failed |

## Glossary

| Term | Meaning |
|---|---|
| Heuristic | A simple, cheap rule of thumb that flags suspicious measurements without aiming for perfection |
| OONI Probe | OONI's mobile and desktop app, which connects to each site on a test list and reports whether it is reachable locally |
| Probe | The device or program running measurements |
| `probe_cc` | The country code the probe reports |
| `probe_asn` | The ASN the probe reports |
| ASN | Autonomous system number, identifying a block of IP addresses under one administration, usually an ISP or institution |
| `msm_count` | The number of measurements a probe has submitted |
| Check-in endpoint | The API a probe calls before measuring, reporting its country code and ASN |
| `web_connectivity` | Web Connectivity, OONI's most common test, which checks whether a website is reachable locally |
| Ground truth | The actual local network conditions, used as the reference for what probes report |
| Sybil attack | An attack that floods the dataset with fake identities to skew results |
| Pseudonym | A probe's identifier under the credential system, fixed within one region and IP, unlinkable across networks, and not a personal identity |
| verified, unverified, failed | The three trust labels the credential system gives each measurement |

## Related Reading

- [OONI Probe's Anonymous Credential System](/articles/ooni-anonymous-credentials/)
- [OONI Run v2 Usage Patterns, a Census of 336 Links](/articles/ooni-run-v2-usage-patterns/)
- [OONI Coverage](/projects/asn-coverage/)
- [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/)
- [What is OONI](docs:tools/what-is-ooni/)
- [ASN Diversity and Gaps in Taiwan's OONI Coverage](/projects/asn-coverage/asn-diversity/)

[^1]: [From Heuristics to Anonymous Credentials: Assessing OONI's Approach to Bad Measurements, OONI 2026-07-06](https://ooni.org/post/2026-faulty-measurements/)
[^2]: [Requirements for OONI's anonymous credentials, OONI](https://ooni.org/post/2025-requirements-for-oonis-anonymous-credentials/)
[^3]: [Announcing OONI's new anonymous credential system, OONI 2026-01-30](https://ooni.org/post/2025-announcing-ooni-new-anonymous-credential-system/)
