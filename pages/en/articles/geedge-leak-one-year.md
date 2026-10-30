---
title: One Year of Research on the Geedge Leak
description: After internal files from Geedge Networks and the MESA Lab leaked, researchers could for the first time compare the Great Firewall against the source code of commercial censorship equipment. This article reviews what two papers and civil society investigations confirmed over the year, what remains uncertain, and where news reporting and the papers' wording diverge.
date: 2026-10-30
---

For nearly three decades, researchers have had almost no option but to infer how the Great Firewall works from outside it. They sent crafted packets, recording which were blocked and how, and working back to the equipment behind them. When internal files from Geedge Networks leaked, researchers for the first time had the source code, build packages and tickets of a commercial censorship vendor closely tied to the Great Firewall. The authors of the USENIX Security 2026 paper state that this is the first time the source code of commercial DPI (deep packet inspection, which analyses the content of each connection to decide whether to let it through) has leaked.[^blackbox] Researchers can now read the code first to find distinguishing traits, then go back to real networks to compare, instead of relying on black-box inference alone.

A year on, the matches found are narrower than some reporting has claimed. The measurements suggest that the leaked code, or a close derivative of it, is deployed on part of the Great Firewall's equipment. Other Great Firewall devices measured in the same way do not match it, no device matches the latest leaked version exactly in the TLS comparison, and for the other customer countries the results mostly stop at "potential" or "cannot confirm".[^summary][^nomatch][^mm-kz-pk] At the same time, these conclusions rest on evidence from both the source code and measurement, which makes them more solid than earlier work based on remote inference alone. It is written for readers who build circumvention tools, do measurement research or follow supply chains. Technical detail stops at the level of mechanisms, and the original papers cover the rest.

<details markdown="1">
<summary>For readers without a technical background</summary>

In September 2025, internal files and source code leaked from Geedge Networks, a company that builds internet censorship systems for China and other countries. For the first time, researchers could read the code of censorship equipment directly instead of only inferring how it works from outside.

A research team built the software and compared it with real networks. Judging by the results, part of China's Great Firewall likely runs this code or a close version of it. The other devices do not match, and there is no public evidence of who built them. According to the leaked documents, Geedge also sold the system to Kazakhstan, Ethiopia, Pakistan and Myanmar, but in those countries measurements mostly stop at "possible" or "cannot confirm".

Circumvention tools and VPNs are a constant target: customers report which tools can still connect, and Geedge adjusts its blocking rules. The paper did not test Tor. InterSecLab's report states that at the time of the leak Geedge appeared to have no effective way to block WebTunnel (a way of connecting to Tor that disguises traffic as ordinary web browsing), and InterSecLab found no evidence of Geedge discovering or exploiting unknown vulnerabilities in Tor.

More than 90% of the sites in the leak that were measured as blocked do not appear on the two website lists researchers commonly measure with, so when a list-based measurement finds no blocking, that does not mean there is none.

Geedge's system relies heavily on open source software such as Linux and Kafka, and some of that code may have been used in breach of its licence terms. Open source licences do not restrict use, so the censorship system and circumvention tools such as Tor are both built on open source software.

ADLINK, a Taiwanese company, shipped a batch of hardware to Geedge between 2019 and early 2020. Geedge is still not on the US or EU sanctions lists we checked.

For background, see the anoni.net Docs site's [Why networked freedom matters](https://anoni.net/docs/en/basics/internet-freedom/), [What surveillance can actually do](https://anoni.net/docs/en/basics/surveillance-capability/), [What Is Tor?](https://anoni.net/docs/en/tools/what-is-tor/) and [VPN: risks and how to choose](https://anoni.net/docs/en/tools/vpn-guide/).

</details>

## A Year of Research

In the year since the leak, joint investigations have read the documents to map Geedge's clients and deployments, while academics have read the source code and measured remotely, and the two produce different kinds of evidence.
{: .sec-lead }

The leaked files come from both Geedge and the MESA Lab. The MESA Lab (Massive and Effective Stream Analysis) belongs to the Institute of Information Engineering of the Chinese Academy of Sciences, and in GFW Report's description the two together are an important branch of the Great Firewall's R&D capacity. According to GFW Report, Geedge was founded in Hainan in 2018, with Fang Binxing, known as the "father of the Great Firewall", as its chief scientist. By the FOCI paper's count, the leak totals 572 GiB, comprising source code repositories, project management records, client deployment configurations and operational data, and more than 80% of it is an archive of an RPM package repository (RPM being a Linux software package format).[^gfwr-geedge]

![Map of Geedge deployment locations recorded in the leaked documents, marking Kazakhstan, Ethiopia, Pakistan and Myanmar, and Xinjiang, Fujian and Jiangsu in China](https://assets.anoni.net/www/articles/geedge-leak-one-year-map-e2b327c5.svg){: .map-img width="720" height="426" loading="lazy" }

Geedge deployment locations recorded in the leaked documents. Client countries are shown in the main colour: ① Kazakhstan (`K18`, `K24`), ② Ethiopia (`E21`), ③ Pakistan (`P19`), ④ Myanmar (`M22`). China is shown in a second shade, with dots for the provincial firewall projects: ⑤ Xinjiang (`J24`), ⑥ Fujian, ⑦ Jiangsu. The unidentified client `A24` is not on the map.[^map]
{: .fig-note }

<ol class="tl" aria-label="Reporting, investigations and papers in the year after the leak">
  <li><span class="tl-when">2025-09-08</span><span class="tl-b"><span class="tl-t">The Globe and Mail</span><span class="tl-d">Reporting from the joint investigation begins, three days before the files are made public</span></span></li>
  <li><span class="tl-when">2025-09-09</span><span class="tl-b"><span class="tl-t">InterSecLab, "The Internet Coup"</span><span class="tl-d">Amnesty International's <em>Shadows of Control</em> and Justice For Myanmar's <em>Silk Road of Surveillance</em> come out the same month. The community has a <a href="https://anoni.net/docs/reports/interseclab-network-coup/">Traditional Chinese translation</a></span></span></li>
  <li class="tl-origin"><span class="tl-when">2025-09-11</span><span class="tl-b"><span class="tl-t">Files made public</span><span class="tl-d">Enlace Hacktivista releases all the files, and DDoSecrets also makes them available for download</span></span></li>
  <li><span class="tl-when">2025-09-12</span><span class="tl-b"><span class="tl-t">GFW Report analysis</span><span class="tl-d">Last updated on 29 December, noting that the source code part of the leak has not yet been carefully analysed</span></span></li>
  <li class="tl-year"><span>2026</span></li>
  <li><span class="tl-when">2026-02-19</span><span class="tl-b"><span class="tl-t">FOCI 2026, "Geedge Cases"</span><span class="tl-d">Researchers from the University of Massachusetts Amherst and GFW Report compare the domains in the leak with two widely used domain lists</span></span></li>
  <li><span class="tl-when">2026-04-24</span><span class="tl-b"><span class="tl-t">InterSecLab, "MADLink"</span><span class="tl-d">The first instalment of a supply chain series, on the server and networking hardware Geedge uses, including hardware from ADLINK in Taiwan. The community has a <a href="https://anoni.net/docs/reports/interseclab-madlink/">Traditional Chinese translation</a></span></span></li>
  <li><span class="tl-when">2026-08-05</span><span class="tl-b"><span class="tl-t">geedge.report post</span><span class="tl-d">The USENIX paper's authors publish an explanatory post on their project site</span></span></li>
  <li><span class="tl-when">2026-08-12</span><span class="tl-b"><span class="tl-t">USENIX Security 2026 paper</span><span class="tl-d">"Technical Analysis of the Geedge Networks Firewall Source Code Leak" is presented at the symposium (12 to 14 August), by authors from the University of Michigan, Paderborn University, the University of Massachusetts Amherst, the University of Colorado Boulder and GFW Report</span></span></li>
  <li><span class="tl-when">2026-08-21</span><span class="tl-b"><span class="tl-t">Risky Bulletin</span><span class="tl-d">Reports the paper's results in more assertive terms than the paper (see the section on the gap between reporting and the paper's wording below)</span></span></li>
</ol>

The news reports came out three days before the files were made public. In the introduction to the USENIX paper, the authors write that several news organisations and journalists "who were granted early access have worked together for the past year to analyze the documents from a non-technical perspective".[^early] According to the acknowledgements in ["The Internet Coup"](https://interseclab.org/research/the-internet-coup/), the Tor Project was also a partner in this joint investigation.[^coup-ack] The joint investigation worked from documents and tickets, establishing Geedge's customers, the countries where it deployed and the features of its products. Before the USENIX paper, the source code itself had been left largely unexplored.[^early][^gfwr-src] Academic research has followed a separate track: reading the source code, building the system and then running remote measurements.

From documents we can learn whom Geedge sold to and what its customers asked for, while measurement is used to judge whether a particular device behaves consistently with the code. Some reporting has applied conclusions of the first kind to the second (see the section on the gap between reporting and the paper's wording below for examples).

This review draws mainly on five papers and reports, which differ widely in scope and method. The table below can help in choosing which to read first (sources and links are in the references at the end).

| Paper or report | Scope | Method | Suited to |
|---|---|---|---|
| "Technical Analysis of the Geedge Networks Firewall Source Code Leak", USENIX Security 2026 | TSG's architecture and third-party code; how TSG compares with censors in the Great Firewall, Henan, Kazakhstan, Myanmar, Pakistan and Iran; ticket records of circumvention tool signatures being tuned | Reading the source code, building the latest tagged release and testing it in isolation, then comparing DNS, IP fragment, TCP, TLS and QUIC fingerprints from remote vantage points[^build][^method] | Researchers working on DPI fingerprinting, censorship measurement or circumvention tools |
| "Geedge Cases", FOCI 2026 | Domains that appear in the leak, and how their coverage differs from Tranco and the Citizen Lab test lists | Extracting candidate domains from the leak, filtering by resolution, and testing DNS injection and TLS SNI blocking from vantage points in China, Pakistan, Myanmar and Algeria, 25 times per domain[^foci-meas] | Researchers who maintain test lists or choose measurement targets |
| "The Internet Coup", InterSecLab, September 2025 | Geedge's products, client countries and deployment modes, its ties to the MESA Lab, and its handling of circumvention tools | Reading the leaked documents and tickets, as part of a joint investigation with media and civil society organisations[^coup-ack] | Readers interested in clients, deployments and human rights impact; a community Chinese translation is available |
| "MADLink", InterSecLab, April 2026 | The sources and suppliers of three generations of TSG hardware, and ADLINK's shipments | Matching hardware records and MAC address vendor prefixes in the leaked documents, and putting questions to the vendor and Taiwan's Ministry of Economic Affairs[^madlink-hw] | Readers studying export controls and supply chains; a community Chinese translation is available |
| "Geedge & MESA Leak", GFW Report, September 2025 | The composition of the leak, the background of Geedge and the MESA Lab, and a round-up of published investigations | Mapping the file structure and existing reporting, with advice on handling the files safely[^gfwr-geedge] | Researchers coming to the leaked material for the first time |

## TSG in the Source Code

The researchers built a working copy of TSG from the leaked source code and found it is made of separately developed components, with two of its three application detection systems built on third-party code.
{: .sec-lead }

### Build and Testing

The USENIX paper analyses Geedge's flagship product, the Tiangou Secure Gateway (TSG), which the authors describe as "a full-stack censorship platform designed to fully integrate into national telecommunications controls". The leak contains more than 100,000 internal documents and over 500 Git repositories alone, covering more than five years of commit history, with the newest files dating from November 2024. Analysis is hard because TSG's logic is spread across many repositories and the same component exists in several branches and versions, and the authors found at least two fully separate IP, UDP and TCP protocol stacks (the part of the code that implements basic protocols such as IP and TCP).

The research team read the code following the four stages of DPI: receiving traffic, reassembly and parsing, rule matching, and interfering with connections. For the build, the team started from the latest tagged release, mapped it across several repositories and package archives, and bypassed the licence check.

Once the build was complete, the team tested its handling of DNS, HTTP, TLS and QUIC (a protocol carried over UDP and used by HTTP/3) in an isolated test environment, successfully triggering injected forged responses, packet drops and deferred blocking, and used the rule engine to define a custom blocking target.[^build] The authors do not say whether all three application detection systems (see Third-Party Code below) were running in this build, so this article only goes as far as saying that the team built and ran TSG's latest tagged release and tested its blocking of several protocols locally. The authors deliberately withhold the full build procedure, for reasons covered in the research ethics section below.

### Core Components

TSG consists of several components that are developed and versioned separately. SAPP is the lowest-level packet processing platform, developed by the MESA Lab since 2005 through four major iterations, and written in C. SAPP assembles packets into TCP and UDP streams and hands them to plugins. It makes no blocking decisions itself and only provides the functions that blocking needs. Plugins come in three types: platform plugins provide shared functions, protocol plugins extract fields such as domain names from DNS queries and from TLS and QUIC handshakes, and business plugins use those fields to implement application logic such as blocking.

Stellar is a separate platform developed by Geedge in C++, with more complete connection state tracking than SAPP and richer ways for plugins to communicate. Stellar-on-SAPP is a SAPP platform plugin that converts SAPP streams into Stellar sessions for Stellar plugins to process, and it is explicitly identified in its README as a transition solution between the two platforms. In the leaked version, Stellar plugins run on SAPP through Stellar-on-SAPP. The standalone stellar repository appeared to be under active development at the time, was not referenced in any build repository, and had not been integrated into TSG.

Maat is the rule engine. Blocking rules are stored in Maat, and plugins match the fields they extract against those rules to get the action to take. Rules can match a wide range of fields, including transport and application protocols, the inner and outer addresses of tunnel encapsulation, source and destination IPs, ports, domain names and SNI (the site name sent in plaintext at the start of a TLS connection), ASN (autonomous system number) and country. The Firewall plugin is attached to both SAPP and Stellar, aggregates the fields extracted along each path, queries Maat and then enforces the block. Besides packet drops and RST (the TCP reset packet, which terminates the connection), blocking actions include throttling, HTTP and DNS redirects, mail and SIP blocking, tampering and deferred blocking.

From hardware to enforcement, TSG's components can be arranged in seven layers:[^madlink-gen][^thirdparty][^oss-stack]

<figure class="st-fig">
<svg class="st" viewBox="0 0 360 596" role="img" aria-labelledby="st-t">
<title id="st-t">The TSG stack, as of the leaked version</title>
<defs><marker id="st-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path class="st-ah" d="M0 0L10 5L0 10z"/></marker></defs>
<rect class="st-band" x="0" y="0" width="360" height="64" rx="6"/>
<text class="st-l" x="10" y="16">Action</text>
<rect class="st-box" x="8.0" y="24" width="344.0" height="30" rx="5"/>
<text class="st-t" x="180.0" y="40.0">Allow, drop, RST, throttle, redirect, tamper, delay</text>
<rect class="st-band" x="0" y="70" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="86">Rule matching</text>
<rect class="st-box" x="8.0" y="94" width="163.0" height="40" rx="5"/>
<text class="st-t" x="89.5" y="108">Firewall plugin</text>
<text class="st-s" x="89.5" y="124">Combines fields</text>
<line class="st-ar" x1="173.0" y1="114.0" x2="185.0" y2="114.0" marker-end="url(#st-a)"/>
<rect class="st-box" x="189.0" y="94" width="163.0" height="40" rx="5"/>
<text class="st-t" x="270.5" y="108">Maat</text>
<text class="st-s" x="270.5" y="124">Rule engine</text>
<rect class="st-band" x="0" y="150" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="166">Application detection</text>
<rect class="st-box" x="8.0" y="174" width="110.7" height="40" rx="5"/>
<text class="st-t" x="63.3" y="188">CBD</text>
<text class="st-s" x="63.3" y="204">Geedge&#x27;s own</text>
<rect class="st-box st-oss" x="124.7" y="174" width="110.7" height="40" rx="5"/>
<text class="st-t" x="180.0" y="188">Glimpse</text>
<text class="st-s" x="180.0" y="204">libprotoident, nDPI</text>
<rect class="st-box st-prop" x="241.3" y="174" width="110.7" height="40" rx="5"/>
<text class="st-t" x="296.7" y="188">QDPI</text>
<text class="st-s" x="296.7" y="204">Qosmos ixEngine</text>
<rect class="st-band" x="0" y="230" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="246">Plugins</text>
<rect class="st-box" x="8.0" y="254" width="110.7" height="40" rx="5"/>
<text class="st-t" x="63.3" y="268">Platform</text>
<text class="st-s" x="63.3" y="284">Shared functions</text>
<rect class="st-box" x="124.7" y="254" width="110.7" height="40" rx="5"/>
<text class="st-t" x="180.0" y="268">Protocol</text>
<text class="st-s" x="180.0" y="284">DNS, SSL, QUIC</text>
<rect class="st-box" x="241.3" y="254" width="110.7" height="40" rx="5"/>
<text class="st-t" x="296.7" y="268">Business</text>
<text class="st-s" x="296.7" y="284">Firewall, etc.</text>
<rect class="st-band" x="0" y="310" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="326">Packet processing platforms</text>
<rect class="st-box" x="8.0" y="334" width="169.0" height="40" rx="5"/>
<text class="st-t" x="92.5" y="348">SAPP</text>
<text class="st-s" x="92.5" y="364">C, MESA Lab</text>
<rect class="st-box" x="183.0" y="334" width="169.0" height="40" rx="5"/>
<text class="st-t" x="267.5" y="348">Stellar</text>
<text class="st-s" x="267.5" y="364">C++, via Stellar-on-SAPP</text>
<rect class="st-band" x="0" y="390" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="406">Operating system and packet I/O</text>
<rect class="st-box st-oss" x="8.0" y="414" width="169.0" height="40" rx="5"/>
<text class="st-t" x="92.5" y="428">Rocky Linux</text>
<text class="st-s" x="92.5" y="444">Basis of TSG-OS</text>
<rect class="st-box st-oss" x="183.0" y="414" width="169.0" height="40" rx="5"/>
<text class="st-t" x="267.5" y="428">DPDK</text>
<text class="st-s" x="267.5" y="444">Packet processing</text>
<rect class="st-band" x="0" y="470" width="360" height="74" rx="6"/>
<text class="st-l" x="10" y="486">Hardware</text>
<rect class="st-box st-tw" x="8.0" y="494" width="81.5" height="40" rx="5"/>
<text class="st-t" x="48.8" y="508">TSG-ADC</text>
<text class="st-s" x="48.8" y="524">CSA-7400</text>
<rect class="st-box" x="95.5" y="494" width="81.5" height="40" rx="5"/>
<text class="st-t" x="136.2" y="508">TSG-9140</text>
<text class="st-s" x="136.2" y="524">ATCA gear</text>
<rect class="st-box" x="183.0" y="494" width="81.5" height="40" rx="5"/>
<text class="st-t" x="223.8" y="508">TSG-X</text>
<text class="st-s" x="223.8" y="524">x86 servers</text>
<rect class="st-box st-tw" x="270.5" y="494" width="81.5" height="40" rx="5"/>
<text class="st-t" x="311.2" y="508">EtherFabric</text>
<text class="st-s" x="311.2" y="524">Load balancing</text>
<rect class="st-box st-oss" x="8" y="556" width="16" height="12" rx="3"/>
<text class="st-s st-lg" x="30" y="562">Open source</text>
<rect class="st-box st-prop" x="113.76" y="556" width="16" height="12" rx="3"/>
<text class="st-s st-lg" x="135.76" y="562">Proprietary</text>
<rect class="st-box st-tw" x="8" y="578" width="16" height="12" rx="3"/>
<text class="st-s st-lg" x="30" y="584">Taiwanese hardware or components</text>
</svg>
<figcaption>A simplified layering based on Section 3 of the USENIX paper and on MADLink. CBD is a library integrated into the Firewall plugin, Glimpse and QDPI are Stellar plugins, and the Firewall plugin runs on both SAPP and Stellar, so the actual call relationships are more tangled than the layers suggest. The Taiwanese hardware markings follow MADLink: TSG-ADC uses ADLINK's CSA-7400, and EtherFabric appears to contain ADLINK components.</figcaption>
</figure>

How TSG handles one connection can be simplified into the path below. In practice several processing paths run in parallel, and their results are combined in the Firewall plugin.[^modular]

<ol class="flow" aria-label="A simplified view of how TSG handles one connection">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>Ingest and reassembly (SAPP)</b><span class="d">Receives traffic and assembles packets into TCP and UDP streams for the plugins</span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>Field extraction (protocol plugins)</b><span class="d">Pulls domain names, the SNI and other fields from DNS queries and the TLS and QUIC handshakes</span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>Application detection</b><span class="d">Decides, with three systems, which app a flow belongs to</span><span class="out"><span>CBD: Geedge's own</span><span>Glimpse: libprotoident, nDPI</span><span>QDPI: Qosmos ixEngine</span></span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>Rule matching (Firewall plugin and Maat)</b><span class="d">Combines the extracted fields and detection results and matches them against the blocking rules in Maat</span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>Action</b><span class="d">Allows the connection, or drops it, sends RSTs, throttles, redirects, tampers with content or delays blocking</span></span></li>
</ol>

The authors draw two points from the architecture, and both bear on every comparison that follows. Because components are developed and versioned separately, fingerprinting one plugin remotely (a fingerprint being a trait that identifies a system or version) does not mean another plugin is present in the same deployment, and reveals nothing about that plugin's version. Blocking decisions are made only after the results of several processing paths are aggregated, so a connection can be blocked on the result of any one of them.[^modular]

### Third-Party Code

TSG has three application detection systems, which determine which app or protocol a flow belongs to, and two of them are built on third-party code. CBD (Context-Based Detector, formerly AppSketch) is TSG's own system and works from signatures loaded through Maat. Glimpse's protocol classification core is libprotoident, free software from the Libtrace team at the University of Waikato, and all the code required for its classification function carries libprotoident's copyright notice. Glimpse's OpenVPN detection code, as the paper describes it, appears to be a modified copy of code from a 2022 version of nDPI (an LGPL-licensed DPI library, described in the paper as GPL)[^ndpi-license], with the main function renamed and the logic nearly identical. The third system, QDPI, is built on Qosmos ixEngine, a proprietary commercial DPI library; the authors base this on the code calling ixEngine functions and including its header file.[^thirdparty]

For libprotoident and nDPI, the paper's wording is that the code was copied and adapted. For Qosmos it says only that QDPI is built on it, and the authors make no judgement on whether Geedge had a licence. The team disclosed Geedge's use of this code to the libprotoident team and to Enea, the parent company of Qosmos. Both had responded by the time the paper was published and meetings had been scheduled, but what they said has not been made public. nDPI is not among the parties the paper lists as notified. In the authors' words, TSG's reliance on third-party libraries for two of its three detection systems "suggests that comprehensive protocol classification is costly to build from scratch, even for a well-resourced, state-linked vendor".[^disclose] Findings like these depend on reading the source code, since remote measurement can hardly tell whose code a detection system uses.[^beyond]

## Comparison with the Great Firewall

The paper reports "high levels of correspondence" only for three Great Firewall devices (Injector 2, GFW II and GFW III). Other devices and Geedge's client countries mostly come out as no match or inconclusive.
{: .sec-lead }

### Comparison Method

According to the USENIX paper, the Great Firewall was long thought to be highly centralised, but a growing body of evidence in recent years points to multiple DPI devices operating independently with different roles, and earlier measurement studies have named several of them.[^gfw-multi] Devices doing DNS injection (a censor sending a forged DNS response before the real server can answer) are known as Injector 1, 2 and 3, names taken from "Triplet Censors" at FOCI 2020. Devices that send RSTs to terminate TCP connections are known as GFW I, II and III, alongside a separate regional censorship system in Henan province, names taken from "A Wall Behind A Wall" at IEEE S&P 2025.

From the source code, the team identified traits that can be measured remotely, such as idiosyncrasies in how protocols are parsed and a custom random number generator used to set packet fields. They then sent test packets between two hosts they own and compared whether censors in each location responded as TSG would. Measurements covered China's Great Firewall, Henan, Kazakhstan, Myanmar and Pakistan, with only DNS tested in Iran, across DNS, IP fragment reassembly, TCP, TLS and QUIC.

The comparison has four steps and a verdict, and every comparison rests on both the source code and measurements:[^method]

<ol class="flow" aria-label="Comparison steps">
  <li><span class="n" aria-hidden="true">1</span><span class="b"><b>Source code analysis</b><span class="d">Picks out behaviour observable from a distance, such as fields in forged packets or idiosyncrasies in protocol parsing</span></span></li>
  <li><span class="n" aria-hidden="true">2</span><span class="b"><b>Local verification</b><span class="d">Runs TSG in an isolated testbed to confirm the behaviour actually occurs</span></span></li>
  <li><span class="n" aria-hidden="true">3</span><span class="b"><b>Remote measurement</b><span class="d">Sends test packets from vantage points in each location to hosts the team owns and records how censors respond</span></span></li>
  <li><span class="n" aria-hidden="true">4</span><span class="b"><b>Behaviour comparison</b><span class="d">Checks the measured responses against TSG's behaviour item by item</span></span></li>
  <li class="ok"><span class="n" aria-hidden="true">✓</span><span class="b"><b>Verdict</b><span class="d">Each comparison falls into one of the results in the matrix legend</span><span class="out"><span>Match, same as an older version, partial match</span><span>No match, inconclusive</span></span></span></li>
</ol>

Censors can be connected to a network in two ways, and how much measurement can reveal depends on which one a device uses:[^modes]

<figure class="pd-fig">
<svg class="pd" viewBox="0 0 360 352" role="img" aria-labelledby="pd-t">
<title id="pd-t">Censors deployed in mirrored and in-line mode</title>
<defs><marker id="pd-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="pd-ah" d="M0 0L10 5L0 10z"/></marker>
<marker id="pd-ai" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="pd-ahi" d="M0 0L10 5L0 10z"/></marker></defs>
<text class="pd-h" x="0" y="16">Mirrored mode: traffic copied beside the line</text>
<text class="pd-s" x="180" y="48" text-anchor="middle">Original packets still reach the website</text>
<line class="pd-wire" x1="74" y1="76" x2="284" y2="76" marker-end="url(#pd-a)"/>
<rect class="pd-box" x="2" y="59" width="72" height="34" rx="6"/><text class="pd-t" x="38" y="76">User</text>
<rect class="pd-box" x="286" y="59" width="72" height="34" rx="6"/><text class="pd-t" x="322" y="76">Website</text>
<line class="pd-tap" x1="200" y1="76" x2="200" y2="118"/><text class="pd-s" x="208" y="102">Copy</text>
<rect class="pd-cen" x="145" y="118" width="110" height="34" rx="6"/><text class="pd-ct" x="200" y="135">Censor</text>
<path class="pd-inj" d="M145 135 Q60 135 40 96" marker-end="url(#pd-ai)"/>
<text class="pd-s" x="2" y="174">Forged DNS response or RST, sent ahead of the real reply</text>
<text class="pd-h" x="0" y="214">In-line mode: traffic must pass through the censor</text>
<rect class="pd-box" x="2" y="243" width="72" height="34" rx="6"/><text class="pd-t" x="38" y="260">User</text>
<line class="pd-wire" x1="74" y1="260" x2="143" y2="260" marker-end="url(#pd-a)"/>
<rect class="pd-cen" x="145" y="243" width="90" height="34" rx="6"/><text class="pd-ct" x="190" y="260">Censor</text>
<line class="pd-wire pd-cut" x1="235" y1="260" x2="284" y2="260"/>
<path class="pd-x" d="M252 251L268 269M268 251L252 269"/>
<rect class="pd-box" x="286" y="243" width="72" height="34" rx="6"/><text class="pd-t" x="322" y="260">Website</text>
<text class="pd-s" x="2" y="304">Can drop packets outright, or send an RST</text>
<text class="pd-s" x="2" y="324">From outside, drops cannot be traced to a device</text>
</svg>
<figcaption>A device in mirrored mode only receives a copy of the traffic, so it cannot stop the original packets and can only race to send forged ones. An in-line device sits on the line and can drop packets directly, but from outside there is no way to tell which device dropped them. That is why the TLS results for the packet-dropping devices in Kazakhstan and Pakistan are inconclusive.</figcaption>
</figure>

As the authors explain in the TLS section, a path may have more than one censorship device on it. A test packet that TSG lets through may still be blocked by another device, whereas a packet that TSG blocks is guaranteed to be blocked whenever it passes through TSG. Our inference is that when the blocking behaviour does not reveal its source, a measured "blocked" result could come from any device on the path and cannot on its own prove that TSG is there. Conversely, a result where TSG should block but the measured packet gets through rules out a TSG component with the same behaviour on that path.[^asym] Because the components are modular, one deployment might run the same version of SAPP with a different version of the SSL plugin, so each comparison speaks to only one component.

Geedge's clients appear in the leaked documents under code names: Kazakhstan is `K18` and `K24`, Ethiopia `E21`, Pakistan `P19`, Myanmar `M22` and Xinjiang `J24`, with one unidentified client, `A24`.[^codes] The table summarises the results for the five protocols, with the client code names from the leaked documents. The codes identify the clients on record, not that the devices measured belong to those projects. Great Firewall devices are listed under the names used in earlier research. The QUIC comparison does not separate Great Firewall devices, so it has its own row.[^matrix]

<div class="match-wrap">
<table class="match" aria-label="Comparison of TSG with censorship devices by location">
<thead><tr><th scope="col">Device or location</th><th scope="col">DNS</th><th scope="col">IP fragments</th><th scope="col">TCP RST</th><th scope="col">TLS</th><th scope="col">QUIC</th></tr></thead>
<tbody>
<tr class="grp"><th colspan="6" scope="rowgroup"><span>China's Great Firewall</span></th></tr>
<tr><th scope="row">Injector 1<small>DNS injector</small></th><td class="m-no">No match</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">Injector 2<small>DNS injector</small></th><td class="m-yes">Match</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">Injector 3<small>DNS injector</small></th><td class="m-no">No match</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
<tr><th scope="row">GFW I</th><td class="m-na"></td><td class="m-no">No match</td><td class="m-no">No match</td><td class="m-no">No match</td><td class="m-na"></td></tr>
<tr><th scope="row">GFW II</th><td class="m-na"></td><td class="m-part">Partial</td><td class="m-yes">Match</td><td class="m-old">Older</td><td class="m-na"></td></tr>
<tr><th scope="row">GFW III</th><td class="m-na"></td><td class="m-unk">Inconclusive</td><td class="m-yes">Match</td><td class="m-no">No match</td><td class="m-na"></td></tr>
<tr><th scope="row">Great Firewall<small>devices not separated</small></th><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-part">Partial</td></tr>
<tr class="grp"><th colspan="6" scope="rowgroup"><span>Other locations</span></th></tr>
<tr><th scope="row">Henan</th><td class="m-na"></td><td class="m-unk">Inconclusive</td><td class="m-no">No match</td><td class="m-no">No match</td><td class="m-na"></td></tr>
<tr><th scope="row">Kazakhstan<small>K18, K24</small></th><td class="m-na"></td><td class="m-unk">Inconclusive</td><td class="m-na"></td><td class="m-unk">Inconclusive</td><td class="m-old">Older</td></tr>
<tr><th scope="row">Myanmar<small>M22</small></th><td class="m-na"></td><td class="m-no">No match</td><td class="m-unk">Inconclusive</td><td class="m-no">No match</td><td class="m-no">No match</td></tr>
<tr><th scope="row">Pakistan<small>P19, RST device</small></th><td class="m-na"></td><td class="m-unk">Inconclusive</td><td class="m-no">No match</td><td class="m-no">No match</td><td class="m-na" rowspan="2">No conclusion</td></tr>
<tr><th scope="row">Pakistan<small>P19, packet-dropping device</small></th><td class="m-na"></td><td class="m-no">No match</td><td class="m-na"></td><td class="m-unk">Inconclusive</td></tr>
<tr><th scope="row">Iran</th><td class="m-no">No match</td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td><td class="m-na"></td></tr>
</tbody>
</table>
</div>

<ul class="match-key" aria-label="Legend">
  <li><span class="sw m-yes"></span>Match</li>
  <li><span class="sw m-old"></span>Same as an older version of TSG</li>
  <li><span class="sw m-part"></span>Partial match</li>
  <li><span class="sw m-unk"></span>Inconclusive</li>
  <li><span class="sw m-no"></span>No match</li>
  <li><span class="sw m-na"></span>Not measured, or no conclusion in the paper</li>
</ul>

<dl class="match-terms" aria-label="What each column compares">
  <dt>DNS</dt><dd>the forged DNS responses a censor races back, compared on their flags, whether they use compression pointers, and the limit on following compression pointers when parsing a query</dd>
  <dt>IP fragments</dt><dd>whether a censor reassembles an IP packet sent in several fragments before inspecting it, and how many fragments it will reassemble</dd>
  <dt>TCP RST</dt><dd>the RST packets a censor forges to tear down a connection, compared on their header settings, how many are sent at once, and whether a constant seed can be worked back from the header fields</dd>
  <dt>TLS</dt><dd>whether a censor still extracts the domain and blocks the connection when the length fields in the first TLS packet (the ClientHello) are tampered with</dd>
  <dt>QUIC</dt><dd>which QUIC versions a censor supports, and how it handles fragment reassembly, the minimum packet size and length fields</dd>
</dl>

### Matches

China's Injector 2 is the only injector that matches all three DNS traits: the flag value in forged responses, the use of compression pointers in those responses (the way a DNS packet refers back to a domain name already written), and the limit on compression pointers when parsing queries. The authors write that these results "strongly suggest that TSG provides the GFW Injector 2's DNS injection implementation".[^dns-inj2]

When TSG forges RST packets, it fills several header fields using a custom random number generator. From the packets sent by GFW II and GFW III, a fixed seed value (the generator's starting value) can be worked back, and it is TSG's default. The authors estimate the probability of a constant seed occurring by chance at about 10⁻⁴⁴, before even considering that the value equals TSG's default, and describe the result as "strongly indicating usage of TSG code".[^seed]

The same section lists where both deviate from TSG. The RSTs sent by GFW II and GFW III both use a fixed TTL (the count of how many more routers a packet may pass through), whereas TSG's TTL varies with internal state. In measurements from December 2023, GFW II's TTL was still consistent with TSG, which the authors take as suggesting that GFW II has slightly changed its implementation since then. Earlier research recorded GFW II sending several identical RSTs in a row; when the team configured TSG to send the same number of RSTs in a row, the IPID (the identification field of an IP packet) changed between packets.[^rst-dev]

IP fragment reassembly produced a partial match: the maximum number of fragments GFW II reassembles at once is very close to TSG's. The authors are more cautious on this point, writing only that the result suggests "the two potentially share similar code".[^frag]

The TLS tests altered each of the length fields in the ClientHello to see whether a device still parsed out the domain and blocked it. No device behaved exactly like the latest leaked version. GFW II's behaviour is equivalent to an older version of TSG's SSL module, which, the authors write, "suggests usage of this older version in GFW II's SSL parsing". For QUIC, the Great Firewall and Kazakhstan blocked the same test packets as TSG, but both support different QUIC versions from TSG, so they cannot be matched fully. Kazakhstan's parsing fingerprint does fully match an older version of TSG's QUIC parsing code.[^tls-quic]

Section 6 of the paper sums up these results in one sentence, reporting high levels of correspondence with Injector 2, GFW II and GFW III, "suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall". The authors hedge the claim with "suggesting" and add emphasis with "indeed". The TLS match for GFW II and the QUIC match for Kazakhstan are with older TSG versions, the RSTs from GFW II and GFW III also deviate from TSG, and the geedge.report post likewise explains that the match changes over time and that the deployed code has drifted from the leaked version.[^summary]

### Mismatches and Inconclusive Results

Injector 1 and Injector 3 do not match; in these measurements Injector 3 used different flags and no longer used compression pointers, unlike when it was first observed in 2020. For GFW I, Henan, Myanmar, and the device in Pakistan that sends RSTs, no fixed seed could be worked back. In the IP fragment comparison, several devices handle reassembly differently from TSG's default, and since the paper notes that reassembly is an option in TSG's configuration file, we class these as inconclusive.[^nomatch]

Myanmar's RST behaviour can be reproduced with TSG's settings, and its supported QUIC versions are exactly the same as TSG's. Its parsing fingerprint does not match, however, and the authors conclude that "we cannot confirm its use". Some devices in Kazakhstan and Pakistan block by dropping packets, which makes it impossible to tell whether a test packet got through, and the authors write that both countries "support potential TSG deployments". Kazakhstan's censors do not send RSTs, so no RST comparison was done there. Even with a QUIC parsing result that fully matches an older version, the authors still do not describe Kazakhstan as a confirmed deployment.[^mm-kz-pk] Iran's DNS flags differ from TSG's, and Ethiopia appears only in the leaked documents, with no measurements.

The evidence that Geedge has customers in these countries comes from documents. The paper's background section cites civil society investigations listing deployments in Kazakhstan, Ethiopia, Pakistan and Myanmar, and the records the team found by searching Jira for "vpn" also mostly concern sites in Myanmar and Ethiopia.[^civil] As far as the USENIX paper's measurements go, the only devices the paper describes as showing "high levels of correspondence" are some of China's.[^summary]

### The Gap between Reporting and the Paper's Wording

In Risky Bulletin's report, TSG is "one of the Great Firewall's three known traffic filtering capabilities",[^risky] a phrase that appears nowhere in the paper.[^no-three] The "three" may come from earlier research's classification of Great Firewall devices. DNS injectors are divided into three, and the paper finds a match for one. RST injectors are also divided into GFW I, II and III, and the paper matches two. The researcher's post quoted in the same report also states that Geedge is only one of the vendors involved in the Great Firewall.[^risky] The bold headline on the geedge.report home page reads "China's Great Firewall is running parts of TSG", which is more assertive than the paper, while the text under the same item uses "appears to be".[^geedge-home]

The paper's results support a narrower claim: part of the Great Firewall's equipment uses TSG or a close version of it, the other devices measured do not match TSG, and there is currently no public evidence of who supplied them. Nor do the authors say that Geedge developed the Great Firewall; the words they use are "ties", "affiliated", and a "close collaborative relationship" with the MESA Lab.[^ties] That is far narrower than claims equating Geedge with the Great Firewall, but it rests on evidence from both default values in the source code and remote measurement, which earlier research relying only on remote inference could not achieve.

## Circumvention Tool Signatures and Blocking

TSG's signatures for circumvention tools are revised again and again in response to client reports, and tools without obvious traffic features, such as Psiphon, are blocked by server IP instead.
{: .sec-lead }

According to the USENIX paper, the leaked files show client-driven, iterative efforts to block specific circumvention tools, including Psiphon, Tor and popular VPNs such as ExpressVPN and NordVPN, with methods ranging from IP-based blocking to matching byte patterns. Signatures (rules describing the traffic traits of a given app) combine server IPs, domain names, TLS fingerprints, certificate fields, packet lengths and byte patterns. A Confluence document analysed in the paper records several updates to a signature bundle between March and November 2024, with signature risk levels between 3 and 5, most of them 5, while another test log aimed mainly at Chinese apps gives every signature a risk level of 1.[^circ] The specific signature conditions are in the paper's tables, and this article does not repeat them.

| Tool | What the leak and the research show |
|---|---|
| Commercial VPNs (ExpressVPN, NordVPN and others) | Signatures combine server IPs, domain names, TLS fingerprints, certificate fields and byte patterns, revised in response to client reports.[^circ] The leak also contains complete NordVPN server lists.[^foci-vpn] |
| Psiphon | According to internal documents, no obvious traffic features, so blocking moved to server IPs, with a whitelist to limit collateral blocking.[^psiphon] The leak contains Psiphon's CDN domains.[^foci-vpn] |
| OpenVPN | The detection code appears to be taken from the open-source nDPI.[^thirdparty] |
| Tor | Listed in the signature risk table. The USENIX paper neither describes the signature nor tests Tor connections.[^tor] |
| WebTunnel | A Tor pluggable transport that disguises traffic as ordinary HTTPS web browsing. At the time of the leak Geedge appeared to have no effective countermeasure, and MESA Lab students had done preliminary research on blocking it.[^webtunnel] |
| Signal | One ticket records blocking failing once Signal's censorship circumvention option was enabled.[^circ] |

Searching Jira for "vpn", the team found 700 tickets across 182 issues, covering reports of extracted server IPs, setting blocking priorities, repeated revisions after signatures stopped working, and over-blocking of other services. The authors' summary is that circumvention tool signatures are tuned with customer involvement: customers can report failures, set priorities and flag over-blocking.[^circ]

In the Psiphon records, obfuscation (techniques that make traffic look unlike any known protocol) raised the cost of detection. According to an internal document analysing the collateral damage of blocking Psiphon, Psiphon traffic lacks obvious signatures, so identification switched to server IPs, combined with a "whitelist protection mechanism" to avoid misidentification. The risk of over-blocking when blocking by IP and SNI also comes up in another ticket. In their conclusion, the authors balance this against the opposite finding, that TSG "is capable of identifying circumvention tools at a relatively low cost", often matching very early in the connection.[^psiphon]

The only material in the paper relating to TSG blocking Tor is the target list in the introduction and the signature risk level table, which includes an entry for Tor Browser.[^tor] The paper does not describe the content of the Tor Browser signature and did not test Tor connections, so it reveals nothing about how TSG identifies Tor, still less that it can block Tor. InterSecLab's "The Internet Coup", which works from documents, reports that "Geedge Networks appears to lack any effective countermeasures against WebTunnel at the time of the leak", and that students at the MESA Lab had done preliminary research on ways to block it. InterSecLab also states that it found no evidence of Geedge discovering or exploiting previously unknown vulnerabilities in Tor, and coordinated disclosure with the Tor Project.[^webtunnel]

The FOCI paper adds evidence from the domain side. Several files in the leak specifically target VPNs and circumvention tools, including complete NordVPN server lists and Psiphon's CDN domains.[^foci-vpn] For developers of circumvention tools, server IPs and domains are themselves targets of collection and blocking, and traffic traits are only one of the methods.

The authors conclude that TSG's complexity and flexibility are "a double-edged sword": they make circumvention harder, but they also undermine code maintainability and correctness. The core components SAPP and its protocol plugins are written in memory-unsafe C, the system still relies on transitional solutions such as Stellar-on-SAPP, and code is copied from several third parties. The tickets include a case of an AppSketch database upgrade causing SAPP to restart, which the authors describe as part of a "patchwork" development process, and they see room for further study with fuzzing (feeding in large amounts of malformed input to find bugs) and symbolic execution (analysing a program's execution paths with symbolic rather than actual inputs). The paper reports no CVE numbers or specific exploitable vulnerabilities.[^no-cve]

## Domain List Coverage

More than nine in ten of the leaked domains that were measured as blocked appear in neither of the two lists researchers usually rely on, so measuring with those lists alone shows only part of what is censored.
{: .sec-lead }

Censorship measurement starts by deciding which domains to test, and two lists are commonly used. Tranco is a ranking of popular sites by traffic, while the Citizen Lab test lists are maintained manually by researchers and the community and organise sites likely to be blocked by content category. The FOCI paper extracted 14,365,453 candidate domains from the leak, leaving 6,915,266 after resolution filtering. Vantage points in Guangzhou and Nanjing tested DNS injection, which is more reliable. Vantage points in Pakistan, Myanmar and Algeria tested whether TLS handshakes were cut off because of the SNI, which is less reliable. Each domain was tested 25 times so that intermittent blocking was also counted. Kazakhstan and Ethiopia are known customers, but the team could not obtain suitable vantage points there.[^foci-meas]

Of the leaked domains measured as blocked, 298,955 (93.7%) appear in neither Tranco nor the Citizen Lab lists. Conversely, the leak covers only 37.1% to 61.6% of the blocked Tranco domains. Each of the three lists has its own role. In the FOCI authors' words, "Tranco informs which globally popular sites are censored, CitizenLab monitors types of sensitive content over time, and the GNL [Geedge Networks leak] reveals which domains commercial vendors consider of interest".[^foci-937]

The FOCI authors do not treat a domain's appearance in the leak as meaning it is blocked. Explicit blocklists are sensitive customer data and rare in the leak; the domains mostly come from internal documents discussing customer environments and represent content "of interest" to Geedge or its customers. The largest source is the MESA Lab's SNI datasets, which the authors judge "appear to be gathered from network taps" (a network tap is a device that copies traffic on a line). The leak also contains copies of ranking lists such as Alexa and SecRank, used for MESA research.[^of-interest] So the 93.7% reflects a gap in the common lists, and which domains are actually blocked still has to be confirmed by measurement, the same approach the USENIX paper takes in reading the code first and then going back to the network to compare.

The community-maintained Taiwan section of the Citizen Lab test lists (`tw.csv` in `anoni-net/citizenlab-test-lists`) is likewise a hand-curated list, reflecting what its maintainers consider important. In light of FOCI's results, when measurement with a list finds no blocking, the conclusion covers only the sites on the list; domains outside it were never within the scope of observation. How to read a single measurement is covered in [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/), and how many measurements each network has in [OONI Coverage](/projects/asn-coverage/).

## Supply Chain and Policy

From the leaked documents, InterSecLab traced part of Geedge's hardware to ADLINK in Taiwan, yet Geedge does not appear on the US and EU sanctions lists we checked.
{: .sec-lead }

In "MADLink", InterSecLab followed the leaked documents to the hardware supply chain. ADLINK of Taiwan, through its Beijing branch, shipped 1,708 CSA-7400 units (a high-density network platform the vendor markets for firewall and DPI use) to Geedge between 2019 and early 2020. According to the report, they were the hardware basis of the first-generation TSG platform, and in the leaked documents this configuration was deployed only in Kazakhstan. Geedge's own EtherFabric (a network packet broker that distributes traffic among multiple TSG nodes) is deployed in Myanmar, and in the leaked documents the vendor prefix of its management interface's MAC address is registered to ADLINK. On that basis InterSecLab judges that it contains ADLINK components, most likely a management compute board.[^madlink-hw]

The leaked documents show three generations of TSG hardware, plus Geedge's own EtherFabric:[^madlink-gen]

| Product | Hardware | Supplier | Deployed in |
|---|---|---|---|
| First generation, TSG-ADC | CSA-7400 high-density network platform | ADLINK (Taiwan) | Kazakhstan |
| Second generation, TSG-9140 | ATCA-format telecom equipment, apparently based on the VELA ATCA platform | Beijing Hengguang Information Technology | Ethiopia (`E21`) |
| Current generation, TSG-X | Commodity x86 compute and storage servers | Nettrix (a Sugon subsidiary), Inspur | Ethiopia (`E21`), Pakistan (`P19`), Myanmar (`M22`) |
| EtherFabric | Apparently reuses the TSG-9140's VELA ATCA hardware, with some networking components possibly from ADLINK | Beijing Hengguang Information Technology, ADLINK | Myanmar (`M22`), a proof of concept for `A24` |

In its reply to InterSecLab, ADLINK confirmed the number of units shipped, and said that it had screened against export control lists before shipping, that Geedge was not on any restricted list, and that it would begin an internal audit. According to ADLINK, it supplies only general-purpose hardware platforms and was not involved in software integration or system design related to end use. InterSecLab's rebuttal is that the leaked documents contain records of TSG-ADC load balancing depending on ADLINK's PacketManager software, and that the CSA-7400 itself is marketed as DPI and firewall equipment.[^adlink] According to the Ministry of Economic Affairs, Taiwan's export control framework draws on international non-proliferation regimes and sanctions lists, and the ministry declined to comment on individual cases, citing legal restrictions.

The report argues that Geedge's current servers are mostly general-purpose x86 hardware that could still be obtained on the secondary market when regular procurement is blocked, and that purpose-built DPI and firewall equipment such as the CSA-7400 is where export controls can actually have an effect.[^adlink] We have made a [Traditional Chinese translation of the full report](https://anoni.net/docs/reports/interseclab-madlink/), and recorded [Taiwan's public response to the MADLink report](/updates/2026/05/madlink-editorial-2026-05/).

MADLink rests on documents and the vendor's replies, which can be set against the USENIX paper's three measurements in Kazakhstan: QUIC parsing matching an older version, TLS inconclusive because of packet drops, and no RST comparison possible. There is a time gap between the two. The CSA-7400 is first-generation hardware shipped between 2019 and early 2020, years before the paper's measurements, and whether the devices measured are still that batch of hardware cannot currently be determined.[^gap]

According to MADLink, the servers in Geedge's current hardware come from Nettrix, whose parent company Sugon is already under US sanctions.[^adlink] In a press release on 19 June 2024, Justice For Myanmar called on governments to sanction companies including Geedge Networks.[^jfm] As of 30 October 2026, we had checked the sanctions lists of the US Treasury's OFAC and of the EU, and the Entity List notices in the US Federal Register, and found no listing of Geedge.[^sanction]

## Open Source Software in the Censorship System

Open source software publishes its source code for anyone to use, and Geedge's censorship system relies on it heavily. The researchers, journalists and communities who exposed the system have worked in the open too.
{: .sec-lead }

### Open Source Software in Geedge's System

Open source software makes its source code public and lets anyone use, modify and redistribute it; Linux and many networking tools are examples. According to MADLink, Geedge's entire software stack is built on open source foundations. The leaked documents also record that Geedge considered switching to Huawei's EulerOS but dropped the idea because the licensing fees were too high.[^oss-stack] The two reports and the USENIX paper mention seven open source projects:[^oss-coup][^thirdparty]

| Open source project | What it was made for | Use in Geedge's system |
|---|---|---|
| Rocky Linux | A Linux operating system | The TSG-OS operating system on the censorship equipment |
| DPDK | Letting ordinary servers process large volumes of network packets quickly | Processing the packets passing through the equipment without tying it to one vendor's network hardware |
| Apache Kafka | Handling large volumes of real-time data, often for retail and advertising analytics | The TSG Galaxy surveillance data warehouse |
| tcpdump | Capturing and recording network packets | Modified into tcpdump_mesa to extract application traffic fingerprints |
| Grafana | Dashboards for monitoring system status | Apparently the model for the Network Zodiac monitoring product |
| libprotoident | Identifying which protocol a flow belongs to, developed by a university team | The core of the Glimpse protocol detection system |
| nDPI | Identifying which application a flow belongs to | Glimpse's OpenVPN detection code, apparently a modified copy |

As MADLink sees it, the software is open source and the servers are widely available general-purpose hardware, so both can still be obtained on secondary markets if regular procurement is blocked. The only place export controls can realistically bite is specialised hardware such as the CSA-7400.[^oss-export]

### Licences That Do Not Restrict Use

Open source software comes with licence terms that set conditions for use, modification and distribution. "The Internet Coup" reports that Geedge incorporates open source code in ways that may violate licensing terms, which it suggests helps Geedge match leading competitors faster while building resilience to sanctions.[^oss-license] libprotoident and nDPI are both licensed under LGPL-3.0.[^ndpi-license] Commercial products may use them, but distribution comes with conditions, such as publishing the source of a modified library. Neither the reports nor the papers reach a conclusion on whether Geedge met them.

Licence terms govern how software is distributed and modified, not what it is used for. Section 6 of the Open Source Initiative's Open Source Definition requires that a licence not restrict anyone from using the program in a specific field, and freedom 0 in the Free Software Foundation's definition is the freedom to run the program for any purpose.[^oss-principle] Vendors building censorship and surveillance systems can draw on the same code as anyone else. When "The Internet Coup" describes Tor and Psiphon, two of the tools being blocked, it calls both free and open source.[^oss-tools] **In our view, the same open source ecosystem supplies both the censors and those circumventing them, and that is one of the costs of openness.**

### Open Source Values in Practice

Over the year since the leak, the researchers, journalists and communities exposing Geedge have worked in the open:

| Practice | Who | What they did |
|---|---|---|
| Circumvention tools are open source | Tor, Psiphon | Free, open source tools whose code users and researchers can inspect for themselves[^oss-tools] |
| Learning about DPI from open source systems | The research community | Before this source code leaked, outside knowledge of how DPI works internally came, apart from measurement, mainly from open source systems such as Snort, Suricata, Zeek and nDPI[^oss-research] |
| Publishing research tools and results | The USENIX paper's team | Published its measurement results, anonymised packet captures and scripts on Zenodo,[^open-science] and built its test vectors by extending the open source tool Censor-Scanner[^oss-research] |
| Open licensing of papers | The FOCI paper's team | The paper is licensed under CC BY 4.0[^foci-license] |
| Notifying open source maintainers | The USENIX paper's team | Notified the Libtrace team about Geedge's use of libprotoident code; the team responded and meetings have been scheduled[^disclose] |
| Investigating with open source tools | InterSecLab | Used the open source tools Datashare and Apache Tika to process more than 100,000 leaked documents for partners in several countries to search[^oss-research] |
| Open licensing and translation | InterSecLab, the anoni.net community | InterSecLab's website is licensed under CC BY-NC-SA 4.0; the community translated "The Internet Coup" and "MADLink" into Chinese, and InterSecLab links to the translations from its report pages[^interseclab-license] |
| Open analysis and discussion | GFW Report | Published its analysis in Chinese and English, with later findings posted to the public net4people thread[^gfwr-open] |
| Publicly maintained test lists | Citizen Lab, the anoni.net community | The test lists are public on GitHub, and the community maintains the Taiwan list (see the section on domain list coverage above) |

The USENIX paper's openness has limits: its measurement results and scripts are public, but the leaked source code and the team's build are not, on the grounds that the risk of censors benefiting outweighs the benefit to the community (see the next section).[^open-science] We think what the community can do is keep exposing the use of open source software in censorship and surveillance, and keep circumvention and measurement tools open and easy to obtain.

## Research Ethics and Data Handling

Neither research team publishes the raw leak, and the USENIX authors withhold the full method for building TSG, so what outsiders can reproduce is mainly the remote measurement.
{: .sec-lead }

The ethical considerations section of the USENIX paper identifies five groups of stakeholders: Geedge employees and shareholders, third-party companies whose code is integrated in TSG, the countries deploying TSG, users under censorship in those countries, and the anti-censorship community. The leaked Git repositories contain developers' names and email addresses. The authors handle this by focusing on the systems and architecture, not reporting on individuals, and not including source material from the leak in their public repository.[^local]

Running a local copy of TSG carries its own risk, since it could help deploying countries refine their systems or make deployment easier for other censors. The authors therefore chose not to publish how to set up the firewall, and the published material is limited to what is useful for identifying deployments. The team also considered not running it locally at all. They concluded that with a working copy, the anti-censorship community can fingerprint deployments in different places, develop and test circumvention strategies against a real system, and generalise those strategies to other countries' firewalls.[^local]

Measurements were run only between two hosts the team owns, with no third-party server as a target, and when renting vantage points the team checked that the providers were not on the EU sanctions list. Neither the leaked source code nor the team's build is published, and the authors have committed to sharing the build with trusted network security researchers on request. What is public on Zenodo is the measurement results, anonymised packet captures and the measurement scripts. As a result, other researchers can reproduce the remote measurements with the published scripts, while the source code side of the comparison can only be reproduced by researchers who are given access.[^share]

The FOCI authors take the position that the broad public interest of the information overrides potential intellectual property concerns, since the leaked data has already been made public by Enlace Hacktivista and DDoSecrets. The GFW Report analysis recommends analysing these files only in an isolated (virtual) machine without internet access.[^foci-ethics]

Lantern's geedge.lantern.io, an index of findings extracted from the leak, takes a different approach. Its page describes it as a sibling to corpus.lantern.io, meant to tell circumvention tool builders exactly what they are up against, but does not say who is behind it, and its relationship to the Lantern circumvention tool cannot be confirmed from the page.[^lantern-site] The index does not rehost raw leak content, and each finding comes with source information.

The findings in the index are extracted automatically by an LLM. According to the page, extraction is done by Sonnet-tier agents reading batches of extracted text, and the home page listed 880 findings when we read it. We sampled five, all marked at the highest confidence level. Three of them inferred that the system logs every connection from the field names of data tables alone, mostly citing test configuration files and giving no commit hash.[^lantern] Lantern's index can serve as a starting point for finding leads, but anything taken from it should first be checked against the original material, and it cannot be treated as evidence on its own.

In the net4people discussion thread, the only sourced follow-up research after October 2025 is the FOCI paper. The rest is mostly commenters' own comparisons and speculation,[^n4p] and some comments link to mirrors of the leaked internal systems, which this article does not cite.

This article holds to the same lines. It does not reproduce content from the leaked files, domain lists or file paths, does not give parameters, trait values or signature conditions that could be used to evade detection or improve blocking (the papers themselves publish some of these, and readers who want more can go to the originals), and does not mention the people who appear in the leaked data.

## Open Questions

Who A24 is, who supplies the rest of the Great Firewall, and whether measurement can confirm the deployments in client countries all remain without public answers.
{: .sec-lead }

Injector 1, Injector 3 and GFW I all fail to match TSG. The paper's results point only to part of the Great Firewall's equipment using TSG or similar code, and there is no public evidence yet on who developed the rest.

In September 2025 InterSecLab wrote that the data on `A24` contains no locations or ISPs that could identify it, and that the only clues are the first letter A and the year 2024, although the digits in a code name do not always mark a year. The relationship was at an early stage when the files leaked, with two proof-of-concept deployments of Geedge equipment, one in mirrored mode and one in-line. In April 2026, InterSecLab's "MADLink" still described `A24` as an unknown customer known only by its code name, and added that Geedge's EtherFabric had also been installed there as a proof of concept. Neither paper, nor GFW Report, nor the net4people thread offers any further clue.[^a24]

Kazakhstan, Pakistan, Myanmar and Ethiopia all have documentary evidence of a customer relationship, yet measurement stops at "potential" or "cannot confirm". The FOCI team could not obtain vantage points in Kazakhstan and Ethiopia, the USENIX paper had a vantage point in Kazakhstan but some results were inconclusive, and neither paper has measurements from Ethiopia. Deployments also keep changing. The leaked files stop at November 2024, and GFW II's TTL had changed between December 2023 and the paper's measurements,[^rst-dev] so future measurements will need to account for version differences.

The team's build loaded only three SAPP protocol plugins, DNS, SSL and QUIC, and the AppSketch database archives are all encrypted. The authors found no code converting the signature formats into Maat rules and only inferred such a conversion from similarities between the formats, and the paper does not cover the rest of the source code. The authors hope the paper will "serve as a guide for future research on the leak". The FOCI authors list as future work searching the leak for IP addresses, analysing PDFs and other documents, improving OCR (optical character recognition), and comparing against domain data from Common Crawl and ICANN.[^future]

On the circumvention side, in the net4people thread tracking the leak (comments from October 2025 onwards), we saw no public statement from Tor, Psiphon or VPN providers on adjustments made in response to the leak.[^n4p] The Tor Project had reviewed the Tor section of "The Internet Coup", and the Psiphon team the Psiphon section.[^coup-ack] With the leaked source code, researchers can now compare real censorship equipment against it; what comes next depends on whether vantage points can be extended to more customer countries, and on how tool developers use the results. You are welcome to join the discussion with us on [Matrix](/contact/).

## References

- [Technical Analysis of the Geedge Networks Firewall Source Code Leak](https://www.usenix.org/conference/usenixsecurity26/presentation/ablove): USENIX Security 2026, by the University of Michigan, Paderborn University, the University of Massachusetts Amherst, the University of Colorado Boulder and GFW Report
- [Geedge Cases: Censorship Measurement Insights from the Geedge Networks Leak](https://gfw.report/publications/foci26b/en/): FOCI 2026, by the University of Massachusetts Amherst and GFW Report, 2026-02-19
- [geedge.report](https://geedge.report/): the project site of the USENIX paper's authors, with the summary post [Geedge firewall source code analysis](https://geedge.report/posts/2026/08/geedge-firewall-source-code-analysis/) published on 2026-08-05
- [Geedge & MESA Leak: Analyzing the Great Firewall's Largest Document Leak](https://gfw.report/blog/geedge_and_mesa_leak/en/): GFW Report, 2025-09-12, updated 2025-12-29
- [The Internet Coup](https://interseclab.org/research/the-internet-coup/): InterSecLab, 2025-09-09
- [MADLink: A Taiwanese Vestige in the Geedge Supply Chain](https://interseclab.org/research/madlink-a-taiwanese-vestige-in-the-geedge-supply-chain/): InterSecLab, 2026-04-24
- [Pakistan: Shadows of Control](https://www.amnesty.org/en/documents/asa33/0206/2025/en/): Amnesty International, 2025-09
- [Silk Road of Surveillance](https://www.justiceformyanmar.org/stories/silk-road-of-surveillance): Justice For Myanmar, 2025-09
- [JFM calls for action against Chinese and Myanmar companies involved in junta digital surveillance and censorship](https://www.justiceformyanmar.org/press-releases/jfm-calls-for-action-against-chinese-and-myanmar-companies-involved-in-junta-digital-surveillance-and-censorship): Justice For Myanmar press release, 2024-06-19
- [Leaked files show a Chinese company is exporting the Great Firewall's censorship technology](https://www.theglobeandmail.com/world/article-leaked-files-show-a-chinese-company-is-exporting-the-great-firewalls/): The Globe and Mail, 2025-09-08
- [Academics find source code overlaps between Geedge and China's Great Firewall](https://news.risky.biz/risky-bulletin-academics-find-source-code-overlaps-between-geedge-and-chinas-great-firewall/): Risky Bulletin, 2026-08-21
- [geedge.lantern.io](https://geedge.lantern.io/): Lantern's index of the leak, with findings extracted automatically by an LLM, usable only as leads

## Related Reading

- [The Internet Coup, Traditional Chinese translation](https://anoni.net/docs/reports/interseclab-network-coup/): the community's translation of InterSecLab's "The Internet Coup"
- [MADLink, Traditional Chinese translation](https://anoni.net/docs/reports/interseclab-madlink/): the community's translation of InterSecLab's "MADLink"
- [OONI Blocking Verdicts](/projects/asn-coverage/ooni-blocking-determination/): the gap between the verdict on a single measurement and a confirmed block
- [OONI Coverage](/projects/asn-coverage/): which networks the measurements in Taiwan and nearby regions come from

[^blackbox]: USENIX paper, §1: "Traditionally, the study of DPI-based censorship systems has relied almost exclusively on black-box analysis" and "This is the first time that the source code of a commercial DPI has been leaked".
[^summary]: USENIX paper, §6: "Notably, we find high levels of correspondence with GFW DNS Injector 2 [9] and TCP GFW II and GFW III [47], suggesting that the leaked TSG code (or a close derivative) is indeed deployed on part of China's national firewall". §6.4: "While no middlebox exhibited exactly the same behavior as the latest leaked TSG". geedge.report, "Geedge firewall source code analysis": "The match is not frozen in time" and "the deployed code has drifted from the leaked version".
[^nomatch]: USENIX paper, caption of Table 5: "Injector 3 has different flags and no longer uses compression pointers, different from the initial observation". The mismatch for Injector 1 rests on the same sentence in §6.1, by which only Injector 2 has all three traits. §6.3: "In contrast, the other injectors exhibit markedly different behaviors and header values" and "While we did not observe the seed key correspondence in other regions"; the first covers GFW I and the second the other regions. Caption of Table 7: "'no' also includes cases where TCP window values remain identical all the time rendering k undefined". §6.2: "This is configurable", which refers to the reassembly option in TSG's configuration file. Which devices handle reassembly differently is in the paper's Table 6, and we do not repeat it here.
[^mm-kz-pk]: USENIX paper, §6.3: "TSG can be configured to match the behavior in Myanmar" and "We did not test in Kazakhstan because its censors do not generate TCP RST packets". §6.5: "We also find the supported QUIC versions in Myanmar align exactly with those supported by TSG's QUIC, though the parsing fingerprint mismatch means we cannot confirm its use". §6.4: "both Kazakhstan and Pakistan (DROP) support potential TSG deployments, as their generic censorship mechanism of packet drops makes bypass failures inconclusive". That the paper does not describe Kazakhstan as a confirmed deployment is our check: a case-insensitive search of the full paper for `confirm` returns 4 hits, in §2.1, the ticket in Figure 2, §6.3 and §6.5, and none of them confirms a deployment in Kazakhstan; nor does any sentence in §6 that mentions Kazakhstan. For Iran, see Table 5, where the Iran row differs from TSG in all three of flags, compression pointers and limit. Ethiopia is not among the vantage points listed in Table 10, which has only Henan, Beijing, Almaty, Yangon, Karachi and Islamabad.
[^gfwr-geedge]: GFW Report, "Geedge & MESA Leak": "This leak originates from an important branch of the GFW's R&D capacity" and "Geedge (Hainan) Information Technology Co., Ltd. (Geedge Networks Ltd.) was founded in the same year. Fang served as chief scientist". The "same year" in that passage is 2018. FOCI paper, §2.1: "572 GiB of internal documents from Geedge Networks and the related MESA lab including source code repositories, project management records, client deployment configurations, and operational data". The figure of more than 80% is our calculation from Table 1 of the USENIX paper, where the archive of the RPM repository accounts for 463.0 GiB, about 81% of the total.
[^map]: "The Internet Coup", "Identifying Client Governments in the Leaked Documents": "Identified code names for clients include Kazakhstan (K18 and K24), Pakistan (P19), Ethiopia (E21), Myanmar (M22), and Xinjiang (J24)". "Key Findings": "InterSecLab has identified regional Chinese provincial firewall projects in Xinjiang, Fujian, and Jiangsu". The report also has its own map (Figure 14), "This map shows the jurisdictions where Geedge Networks operates". Our map is redrawn from these statements, with the dots placed near each provincial capital to mark the province, not an actual deployment site. Boundaries from Natural Earth 1:50m (public domain).
[^early]: USENIX paper, §1: "Several news organizations and journalists who were granted early access have worked together for the past year to analyze the documents from a non-technical perspective", "The current reporting is mostly geared to non-technical audiences" and "leaving the source code itself largely unexplored".
[^coup-ack]: "The Internet Coup", Acknowledgments: "This research by InterSecLab is part of the Great Firewall Export investigation, a joint collaboration with the partners Amnesty International, Justice For Myanmar, Paper Trail Media, The Globe and Mail, the Tor Project, the Austrian newspaper DER STANDARD and Follow The Money". The same passage continues: "We also appreciate the contributions from the Tor Project team, who reviewed the Tor section, and the Psiphon team, who provided valuable information and reviewed the Psiphon section".
[^gfwr-src]: GFW Report, "Geedge & MESA Leak": "The source-code portion of the leaked files has not yet been carefully analyzed".
[^build]: USENIX paper, §1: "we successfully build and run TSG's latest tagged release version". §5.2: "We were able to successfully test the DNS, HTTP, TLS, and QUIC protocols and trigger injection responses, packet drops, and deferred blocking actions".
[^method]: USENIX paper, §5.2: "We developed a testbed to evaluate TSG's blocking behaviors in a controlled environment". Ethical Considerations: "We performed all of our scans between two vantage points that we own, not including any other third-party server as the target of our scan". On extracting fingerprints from the source code before measuring, §1: "we extract several fingerprints from TSG, including custom random number generators and parsing idiosyncrasies".
[^foci-meas]: FOCI paper, §3.2: "we produce a list of 14,365,453 potential domains" and "we produce a final list of 6,915,266 domains". §3.4: "we perform measurements across vantage points in China (Guangzhou and Nanjing), Myanmar, Pakistan, and Algeria", "While Kazakhstan and Ethiopia are known customers of Geedge Networks [12], we were unable to obtain access to appropriate vantage points in these countries", "DNS censorship is highly reliable", "which are inherently less reliable indicators" and "we perform 25 tests per domain to ensure intermittently blocked domains are included".
[^madlink-hw]: "MADLink", Executive Summary: "These units formed the basis of Geedge's first-generation firewall platform". Section "First generation: TSG-ADC (Kazakhstan)": "Leaked documents indicate this configuration was deployed exclusively at the Kazakhstan" and "ADLINK confirmed to InterSecLab that it shipped 1,708 CSA-7400 units to Geedge between 2019 and early 2020". Section "EtherFabric: Geedge's custom network packet broker": "EtherFabric was deployed at the Myanmar", "is registered to ADLINK Technology, Inc." and "contains at least one ADLINK component, most likely the compute board that runs the management software". ADLINK's reply: "ADLINK confirmed that ADLINK Technology (China) Co., Ltd., Beijing Branch supplied standard CSA-7400 network security platform equipment to Geedge Networks". We leave out the site codes and the value of the MAC address prefix.
[^madlink-gen]: "MADLink", "Geedge Networks' Supply Chain: A Closer Look" and the following sections: "three successive generations of server hardware", "The first-generation TSG platform, TSG-ADC, was built on the CSA-7400", "The second-generation platform, TSG-9140, used the AdvancedTCA (ATCA) form factor", "It appears to be based on the VELA ATCA platform from Chinese company Beijing Hengguang Information Technology", "Leaked documents show the TSG-9140 was deployed exclusively at the Ethiopia (E21) customer site", "The current generation, TSG-X, uses Nettrix servers for the primary TSG compute nodes and Inspur servers for storage", "TSG-X is deployed at the Ethiopia (E21), Pakistan (P19) and Myanmar (M22) customer sites", "EtherFabric appears to reuse the same VELA ATCA hardware from Beijing Hengguang Information Technology as the TSG-9140", "some networking components may be supplied by ADLINK Technologies", "was also installed as a proof of concept for an unknown customer identified only by the code name A24".
[^thirdparty]: USENIX paper, §1: "including two of the three core application detection systems". §4.2.1: "a free software project from the Libtrace team at the University of Waikato", "All code required for this function contains the libprotoident copyright", "appears to be a modified copy of openvpn.c from a 2022 version of nDPI" and "the logic remains nearly identical". §4.2.2: "QDPI is built off of Qosmos ixEngine, a proprietary, enterprise DPI library" and "This is most clearly indicated by the Stellar session callback subscriber function eventually calling", followed by the name of an ixEngine function.
[^oss-stack]: "MADLink", section "Geedge Networks' Supply Chain: A Closer Look": "Geedge's entire software stack is built on open-source foundations", "is based on Rocky Linux (previously CentOS), and its network packet processing relies on Intel's open-source DPDK toolkit" and "Geedge considered switching to Huawei's EulerOS but rejected it because of high licensing fees".
[^modular]: USENIX paper, takeaways of §3.2 and §3.5: "fingerprinting one plugin does not necessarily imply the presence or version of another in the same deployment" and "The firewall aggregates attributes from multiple parallel processing paths".
[^ndpi-license]: The GitHub repositories of nDPI and libprotoident, read on 30 October 2026: the COPYING file of both is the GNU Lesser General Public License v3.0 (LGPL-3.0). The USENIX paper, §4.2.1, describes nDPI as "a GPL-licensed DPI library".
[^disclose]: USENIX paper, §4.2: "we find instances of third-party libraries intentionally copied and adapted into the Geedge Networks code base". Ethical Considerations: "We disclosed the usage of code by Geedge Networks to both the Libprotoident team and Enea, the parent company of Qosmos. Both have responded to our initial disclosures, and we have scheduled meetings to engage in further discussion". Takeaway of §4.2: "suggests that comprehensive protocol classification is costly to build from scratch, even for a well-resourced, state-linked vendor".
[^beyond]: Our view, based on the USENIX paper, §1: "For the first time, we can move beyond remote inference".
[^gfw-multi]: USENIX paper, §2.1: "there has been increasing evidence pointing to the deployment of multiple, independently operating deep packet inspection (DPI) devices with distinct enforcement roles".
[^modes]: "The Internet Coup", "System Modes for Censorship and Surveillance": "In mirrored mode, clients are unable to stop specific traffic from passing through and have to rely on packet injection to block connections", "In in-line mode, also referred to as “active” mode in the documents, the traffic must pass through the Geedge appliance before continuing to its destination" and "The advantage of this mode is that one can fully stop specific traffic flows from ever making it through the network". USENIX paper, §5.2: "It also supports both in- and on-path deployment". §3.1: "Both require TSG to be deployed in-path to stop packets". §6.4: "their generic censorship mechanism of packet drops makes bypass failures inconclusive".
[^asym]: Our inference, based on the USENIX paper, §6.4: "Note, we can highlight comparisons with test vectors that are successfully blocked by TSG in cases of non-fingerprintable censorship decisions" and "if a test vector evades TSG, it could still get blocked by another middlebox, but if it is blocked by TSG, it is guaranteed to be blocked". The authors use this logic to choose which TLS results to compare; we extend it to the other protocols and conclude from it that a result where the packet gets through can rule out TSG.
[^codes]: "The Internet Coup", "Identifying Client Governments in the Leaked Documents": "Identified code names for clients include Kazakhstan (K18 and K24), Pakistan (P19), Ethiopia (E21), Myanmar (M22), and Xinjiang (J24)", "An unidentified client, referred to by the code name A24 is also mentioned in the data", "It is possible that the last two digits of the code names indicate Geedge Networkʼs start year for projects in the region, though this does not always hold true".
[^matrix]: Our classification, based on Tables 5 to 9 and the text of §6.1 to §6.5 of the USENIX paper. Match: Injector 2 in §6.1; GFW II and GFW III in §6.3, where the constant seed equals TSG's default. Older: §6.4, "GFW II shows behavior equivalent to an older version of TSG's SSL module"; §6.5, "the parsing fingerprint exhibited in Kazakhstan fully matches an older version of TSG's QUIC parsing code". Partial: GFW II in §6.2 ("The observed boundary of […] fragments for GFW II is very close to TSG's"), which we class as partial because the limit is only close; §6.5, "both Kazakhstan and the GFW block the same test vectors as TSG's QUIC plugin, though we cannot match them fully due to a difference in supported QUIC versions". Inconclusive: devices in §6.2 whose reassembly differs from TSG's default (the paper notes this is a configurable TSG setting); §6.4, "both Kazakhstan and Pakistan (DROP) support potential TSG deployments"; §6.3, "TSG can be configured to match the behavior in Myanmar". No match: the other injectors and Iran in Table 5 (§6.1); devices in §6.2 that still reassembled at the test limit; §6.3, "the other injectors exhibit markedly different behaviors and header values"; devices other than GFW II and the two packet-dropping devices under §6.4, "no middlebox exhibited exactly the same behavior as the latest leaked TSG"; §6.5, "the parsing fingerprint mismatch means we cannot confirm its use" (Myanmar). Pakistan appears in Table 9, but the text does not discuss its QUIC results. The device in Kazakhstan does not send RSTs, so the paper made no TCP comparison there. For Henan and the device in Pakistan that sends RSTs, every TLS difference in Table 12 is a vector TSG lets through but the device blocks. Because these devices block with RSTs, the source of the blocking can be identified from the RSTs, so we class them as no match; the paper's text draws no conclusion on these two cells.
[^dns-inj2]: USENIX paper, §6.1: "Our results in Table 5 strongly suggest that TSG provides the GFW Injector 2's DNS injection implementation" and "only China's Injector 2 exhibits the combination of the flag value". We leave out the flag value itself.
[^seed]: USENIX paper, §6.3: "corresponding to TSG's default seed_key, strongly indicating usage of TSG code" and "of exhibiting a constant seed key by random chance is approximately", the sentence that gives the probability estimate of 10⁻⁴⁴. We leave out the seed value itself.
[^rst-dev]: USENIX paper, §6.3: "both GFW II and GFW III exhibit deviations from TSG", "Both fix TTL values at […], but TSG generates TTL values dependent on an internal state variable", "GFW II did exhibit TTL values consistent with TSG, suggesting that it slightly changed its implementation since then" and "GFW II is known to send […] identical RST+ACK packets [47], while our build of TSG, when configured to also send […] RST+ACK packets per injection, decreases the IPID". […] marks values we leave out.
[^frag]: USENIX paper, §6.2: "The observed boundary of […] fragments for GFW II is very close to TSG's, suggesting the two potentially share similar code". […] marks the fragment limit, which we leave out.
[^tls-quic]: USENIX paper, §6.4: "While no middlebox exhibited exactly the same behavior as the latest leaked TSG, GFW II shows behavior equivalent to an older version of TSG's SSL module, which suggests usage of this older version in GFW II's SSL parsing". §6.5: "both Kazakhstan and the GFW block the same test vectors as TSG's QUIC plugin, though we cannot match them fully due to a difference in supported QUIC versions" and "the parsing fingerprint exhibited in Kazakhstan fully matches an older version of TSG's QUIC parsing code".
[^civil]: USENIX paper, §2.2: "Civil society investigations have highlighted evidence of deployments of Geedge Networks' products across multiple countries, including Kazakhstan", "Ethiopia", "Pakistan" and "and Myanmar"; we leave out the site code given after each country. §4.1.2: "we conducted a case-insensitive search for 'vpn'" and "We found major threads of site correspondence with Myanmar (440 tickets) and Ethiopia (53 tickets)".
[^risky]: Risky Bulletin, 2026-08-21: "as one of the Great Firewall's three known traffic filtering capabilities". From the researcher's post quoted in the same report: "Geedge is only one of the vendors involved in the GFW" and "the authors found only 1 out of the 3 of the characterized DNS injectors that comprise the GFW matched".
[^no-three]: Our check. A search of the full USENIX paper, including the appendices and references, for `three known` and `filtering capabilit` returns 0 hits each. `filtering` appears only once, in the title of a cited paper. That the "three" may come from earlier research's classification is our inference, based on §2.1: "DNS manipulation is managed by three independent on-path injectors", §6.3: "We evaluated three TCP RST injectors", and the researcher's post quoted by Risky Bulletin: "1 out of the 3 of the characterized DNS injectors".
[^geedge-home]: geedge.report home page: "China's Great Firewall is running parts of TSG". The explanation under the same item: "The same code, or a close relative, appears to be part of China's national censorship system".
[^ties]: USENIX paper, Abstract: "a Chinese DPI company with ties to the Great Firewall of China". §1: "affiliated with the Great Firewall of China". §2.2: "maintains a close collaborative relationship with the Massive and Effective Stream Analysis (MESA) Lab".
[^circ]: USENIX paper, §1: "we identify client-driven, iterative efforts to block specific circumvention tools, including Psiphon, Tor, and many popular VPN providers" and "ranging from IP-based blocking to matching byte patterns". §4.1.1: "including server IP addresses, domain names, JA3/JA4 hashes, SSL certificate fields (e.g., issuer name), payload length, and byte patterns", "records a log of updates to a signature ZIP from March through November 2024", "carry risk levels between three and five", "the majority (21/29) are ranked five" and "which target predominantly Chinese applications and all have a risk score of one". §4.1.2: "finding 700 tickets across 182 issues", "ineffective blocking of Signal when the 'censorship circumvention' option is enabled" and "customers can report failures, set priorities, and flag collateral damage".
[^foci-vpn]: FOCI paper, §4.2: "Multiple files specifically target VPN and circumvention tools, including comprehensive NordVPN server lists and Psiphon CDN domains".
[^psiphon]: USENIX paper, §4.1.2: "based on server IP addresses due to the lack of obvious signatures and integration of a 'whitelist protection mechanism' to avoid misidentification". Caption of Figure 3: "concerns of collateral damage from blocking Psiphon by IP addresses and SNI". §7: "we also find evidence of obfuscation raising the cost of detection", "TSG is capable of identifying circumvention tools at a relatively low cost" and "often very early in the connection".
[^tor]: Our check. A case-sensitive search of the full USENIX paper for the whole word `Tor` finds 5 occurrences: the list of blocking targets in the §1 introduction, the review of earlier research on the Great Firewall blocking Tor in §2.1, the Tor Browser entry in the Table 3 risk level table, and the titles of two cited papers. Tor does not appear in the measurements in §6.
[^webtunnel]: "The Internet Coup", section "Blocking Tor" in the chapter "Blocking Online Privacy & Circumvention Tools": "Geedge Networks appears to lack any effective countermeasures against WebTunnel at the time of the leak", "our investigation uncovered preliminary research conducted by students at Mesalab on" and "potential methods to block WebTunnel" (the sentence breaks across a page in the PDF), "We have coordinated the responsible disclosure of these findings with the Tor Project" and "we have not found any evidence indicating that Geedge Networks has discovered or is exploiting any previously unknown vulnerabilities in the Tor software or its design".
[^no-cve]: Our check. A case-insensitive search of the full USENIX paper for `CVE`, `vulnerab` and `exploit` returns 0 hits each. `memory-unsafe` and `fuzzing` appear once each, both in the §7 conclusion. §7: "while they pose a significant obstacle to circumvention, they also undermine code maintainability and correctness", "core components such as SAPP and its protocol plugins are written in memory-unsafe C", "The Jira tickets corroborate this patchwork development process; we detail an example of an upgrade to the AppSketch database causing SAPP to restart" and "these reinforce the potential for future work in fuzzing or symbolic execution".
[^foci-937]: FOCI paper, Abstract: "298,955 censored GNL domains (93.7% of all censored GNL domains) are not included in either Tranco or the CitizenLab lists". §5: "the GNL captures between 37.1% and 61.6% of censored Tranco domains" and "Tranco informs which globally popular sites are censored, CitizenLab monitors types of sensitive content over time, and the GNL reveals which domains commercial vendors consider of interest". GNL is the FOCI paper's abbreviation for the leaked data.
[^of-interest]: FOCI paper, §4.1: "we do not assume domains are censored simply because they appear in the GNL", "explicit blocklists are rare in the leak, as they constitute sensitive customer data" and "domains in the GNL represent content 'of interest'". §4.2: "The largest number of domains comes from MESA lab's specialized SNI datasets" and "appear to be gathered from network taps"; we leave out the dataset file names. §5: "The GNL contains copies of popularity lists (Alexa, SecRank) that appear to be used for MESA lab research projects rather than deployed Geedge products".
[^adlink]: "MADLink", section "ADLINK's role and response": "The company stated that it completed export control list screening, confirmed that Geedge was not on any restricted list", "The company also stated that it would begin an internal audit", "ADLINK stated that it only provided the general-purpose hardware platform and did not participate in any software integration, system design, or operational activities related to the product's end use" and "However, this characterization is contradicted by leaked documents showing that Geedge's TSG-ADC configuration relied on ADLINK's PacketManager software for load-balancing functions". On ADLINK's description of the CSA-7400 as a general-purpose platform, the report's response is that it is "difficult to reconcile with the product's own marketing, which positions it as a high-density network security appliance designed for deep packet inspection and firewall applications". Executive Summary: "The Taiwan Ministry of Economic Affairs, responding to InterSecLab's inquiry, described this framework but declined to address the specific case, citing legal constraints" and "their components could likely be sourced from secondary markets even if direct procurement was restricted". Conclusions: "its current-generation servers are commodity x86 hardware that could be sourced from secondary markets". Section "Current generation: TSG-X (Ethiopia, Pakistan, Myanmar)": "Nettrix is a subsidiary of Sugon, a Chinese supercomputer maker that is already sanctioned by the U.S.".
[^gap]: Our inference, based on "MADLink", section "ADLINK's role and response": "ADLINK confirmed that shipments continued into early 2020", and the USENIX paper, §6.3: "looking at previous measurements collected in December 2023". The paper compares against those older measurements from December 2023, and its own measurements came later, though no date is given. With shipments ending in early 2020 and the measurements coming after December 2023, the two are more than three years apart.
[^jfm]: Justice For Myanmar press release, 2024-06-19: "Justice For Myanmar calls on governments to urgently impose sanctions against Geedge Networks, CEIEC and Mascots Group, its directors and related companies".
[^sanction]: Our check, not a claim from any source. On 30 October 2026 we downloaded the SDN list and the Consolidated list of the US Treasury's OFAC and the EU's consolidated financial sanctions list, and searches for `Geedge` and for `Jizhi` (the romanised Chinese name) returned no matching entries. For comparison, Sugon (Dawning Information Industry) appears on OFAC's Consolidated list. Additions to the Entity List are all published in the Federal Register. A search of the US Federal Register for `Geedge` returns 0 results, and the only result for `Jizhi` is a different company, Changguang Jizhi Optical Technology, being added to the Entity List. The UK sanctions list and the US Commerce Department's Consolidated Screening List could not be downloaded this time and are outside the scope of the check.
[^oss-coup]: "The Internet Coup", "Products & Offerings": "It is built on the open-source Apache Kafka stream-processing platform" (TSG Galaxy), "Using the open source DPDK allows them to make the network stack hardware vendor agnostic" and "Network Zodiac seems to be modeled on Grafana". Footnote 10 of the same chapter: "Geedge and the Mesalab students use a modified version of the open-source tool tcpdump, which they call tcpdump_mesa".
[^oss-export]: "MADLink", "Conclusions": "Geedge's software is open-source, and its current-generation servers are commodity x86 hardware that could be sourced from secondary markets" and "This makes them a realistic target for export control measures in a way that commodity server components are not".
[^oss-license]: "The Internet Coup", "Copying and Building on Existing Commercial Products and Open Source Code": "They also incorporate open-source code in ways that may violate licensing terms" and "Geedge seems to be using these tactics for competitive advantage".
[^oss-principle]: Open Source Initiative, "The Open Source Definition", section 6, "No Discrimination Against Fields of Endeavor": "The license must not restrict anyone from making use of the program in a specific field of endeavor". Free Software Foundation, "What is Free Software?": "The freedom to run the program as you wish, for any purpose (freedom 0)". Both read on 30 October 2026.
[^oss-tools]: "The Internet Coup", "Blocking Tor": "The Tor network is a free, open-source system". "Circumventing Psiphon Protective Measures": "Psiphon is a free and open-source internet circumvention tool".
[^oss-research]: USENIX paper, §2.2: "has been inferred from measurements" and "or learned from open-source systems such as Snort", with Suricata, Zeek and nDPI listed in the same sentence. §6.4: "We created our test vectors by extending the open-source tool Censor-Scanner". "The Internet Coup", "Methodology": "The more than 100,000 leaked documents reviewed for this research", "indexing the documents into the open-source document discovery platform Datashare" and "We then used the open-source text extraction library Apache Tika".
[^open-science]: USENIX paper, Open Science: "In the context of the open science policy, we made all of our artifacts available in the following Zenodo link", "We consider the risk of censors benefiting from such a publication greater than the potential benefit to the community" and "we do not provide the artifact openly".
[^foci-license]: FOCI paper, first page: "This work is licensed under the Creative Commons Attribution 4.0 International License".
[^interseclab-license]: InterSecLab, "The Internet Coup" page, read on 30 October 2026: "Translated into Traditional Chinese by Anonymity Networks Community". Site footer: "The content of this website is licensed under a CC BY-NC-SA 4.0".
[^gfwr-open]: GFW Report, "Geedge & MESA Leak": "GFW Report will continue to update our analysis and findings on the current page as well as on Net4People".
[^local]: USENIX paper, Ethical Considerations: "the git repositories contain commits and directories that list emails and names of individual developers", "we emphasize that our focus is on the systems and architecture, and not on individual persons", "do not include source material in our repository", "our efforts to run a local operational copy of TSG could harm users experiencing censorship by enabling deploying countries to refine their systems", "we choose not to publicly document or provide additional details on how to set up this firewall", "We also considered whether it would be better to not deploy the firewall ourselves at all" and "develop and test circumvention strategies against a working instance".
[^share]: USENIX paper, Ethical Considerations: "We performed all of our scans between two vantage points that we own" and "we made sure that no entity is present on the current EU sanctions list". Open Science: "We decided against the publication of the leaked source code and our deployment of the Firewall due to ethical concerns". §1: "We will make our build available to trusted network security researchers upon request". geedge.report, Resources page: "All of our result files, anonymized PCAPs, and the scripts and tools used to conduct our scans are archived on Zenodo". The last sentence of the paragraph is our inference.
[^foci-ethics]: FOCI paper, Ethical Considerations: "we believe the broad public interest of this information overrides potential intellectual property concerns". GFW Report, "Geedge & MESA Leak": "analyzing these files only in an isolated (virtual) machine without internet access".
[^lantern-site]: geedge.lantern.io home page, read on 30 October 2026: "Lantern research · sibling to", followed by a link to corpus.lantern.io, and "Sibling project" in the footer. The purpose is stated on the home page: "extracted for one purpose: telling a circumvention-tool builder exactly what they're up against". About page: "Raw leak content is never rehosted".
[^lantern]: geedge.lantern.io, about page: "Finding extraction runs as Sonnet-tier agents reading batches of extracted text" and "`high` requires an unambiguous, explicit source". Home page footer, read on 30 October 2026: "880 findings indexed from the September 2025 Geedge/MESA leak". The sampling is our check. On the same day we picked five findings from the Recent findings list on the home page, all five marked high. The first three infer per-connection logging from the fields of data tables, in the words "This confirms, at the OLAP schema level", "not just connection metadata" and "tags every session". The other two rest on code and on a changelog respectively. We counted a source as a test setup when its path showed a configuration set for a test environment, which was the case for four of the five. The source field of all five gives only an archive and a path, with no commit hash.
[^n4p]: Our check: on 30 October 2026 we read thread #519 in net4people/bbs, covering comments from October 2025 onwards. Sourced means that the comment links to a paper or a formal report.
[^a24]: "The Internet Coup", "A24: The Unknown Client in the Early Stages": "data related to A24 does not include any of these indicators that could identify the client", "The only clues about the identity of the A24 client is the first letter A and the year 2024", "at the time of the leak, A24 and Geedgeʼs relationship appeared to be in its early stages". "MADLink", "EtherFabric: Geedge's custom network packet broker": "was also installed as a proof of concept for an unknown customer identified only by the code name A24". The absence of any public identification is our check, as of 30 October 2026: A24 appears 0 times in the full text of the USENIX paper and the FOCI paper. The Chinese version of GFW Report's analysis states that every code name except A24 has been matched to a country, and otherwise restates InterSecLab's findings. Of the 98 comments in the net4people thread, 2 mention `A24` (10 and 11 September 2025), and both quote InterSecLab's report.
[^future]: USENIX paper, §5.1: "which we use to load SAPP's DNS, SSL, and QUIC plugins". §4.2.2: "While all available archives" and "of the database in the leak are encrypted", one sentence that breaks across columns in the PDF layout. §4.1.1: "Although we found no code explicitly converting ASW or TSG2402 formats into Maat signature definitions". §7: "We hope this work will serve as a guide for future research on the leak". FOCI paper, Future Work: "areas for future work include searching for IP addresses in the GNL, deeper analysis of documents such as PDFs, and improved OCR" and "the Tranco and Citizen Lab lists are limited compared to larger censorship measurement lists such as Common Crawl or ICANN CZDS".
