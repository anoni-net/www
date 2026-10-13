---
title: Unredacted's Circumvention Infrastructure, Seen from Taiwan
description: A guide to Unredacted's Tor Blog guest post on FreeSocks, Tor bridges and Snowflake across 300-plus servers, and GreenWare's 123 exit relays on roughly 400W, with notes on Taiwan's relay count, running GreenWare-style hardware in Taiwan, and ways to take part.
date: 2026-06-01
---

The harder the censorship, the more alternative routes people need, and every route runs on servers, bandwidth and electricity. Unredacted operates more than 300 servers worldwide to give people under censorship a way around the blocks, and is experimenting with single-board computers to cut the power draw of Tor exit relays. This guide walks through their guest post on the Tor Blog. Three sections from the anoni.net community follow, comparing Taiwan's relay count, the cost of running GreenWare-style hardware in Taiwan, and ways readers can take part.

The original is [Keeping the doors open](https://blog.torproject.org/keeping-the-doors-open-unredacted/), published on 2026-05-15 as part of the Tor Blog's spotlight series on organizations defending the free internet. Where this guide says "they", it means Unredacted.

The post opens with a message from a user in China:

> "You have helped many many people to overcome the great firewall. Without your help, I would be in the totally darkness trap and being brain-washed."

Unredacted rarely hears from the people who use its services. Most of them cannot, or do not feel they can, safely send a message, and each one that gets through is a reminder of what is at stake.

Unredacted is a US-based 501(c)(3) non-profit that builds and operates internet infrastructure to help people reach the open internet and protect their right to privacy, running a network of more than 300 servers around the world. In their words, they are "a way through when the front door is locked, and a place to communicate when the public square isn't safe." Most of the work is invisible: datacenter work, hardware, automation, open source software, bandwidth, abuse queues, monitoring alerts, and late nights keeping it all online.

Their work falls into three areas. Censorship Evasion is home to Unredacted Door, the umbrella for every service built to route around blocking. Secure Infrastructure covers [XMPP.is](https://xmpp.is/), their Matrix homeserver and other free services built with security and privacy in mind. Unredacted Education is the writing side, guides and explainers for people who want to understand the work and replicate it. Alongside these, Unredacted Labs is where they try infrastructure ideas that are not yet production-ready. GreenWare is one of them, an effort to carry real network capacity on hardware that does not draw much power.

## Unredacted Door

The name is literal: when the entrance to the open internet is walled off, people need another way in.

Unredacted Door brings together FreeSocks, messaging proxies for Signal and Telegram, Tor bridges and Snowflake proxies. In a recent 30-day window these services carried nearly 300 TiB for tens of thousands of people routing around censorship in their own countries, roughly the bandwidth needed to stream tens of thousands of hours of 4K video. Demand is not slowing, and they need to keep building. Every new filter, every new law and every "for your safety" rollout sends more people looking for a route the censors have not found yet.

The largest piece is FreeSocks, free proxies for people in places where censorship is severe. A proxy is a relay point: the app connects to the proxy server instead of the blocked service, and the server carries the connection past whatever filters sit between the user and the wider internet.

FreeSocks is designed to make that relay point unremarkable, which is the trait a standard VPN lacks. A VPN has a known endpoint, a known handshake and an obvious shape on the wire, and censors are very good at blocking what they can recognize.

Tor Browser gives strong privacy and anonymity for browsing. Snowflake helps people reach Tor when the network itself is blocked. FreeSocks proxies push specific traffic along a route that is harder to spot. No single tool covers every situation, so people living under censorship usually keep several on hand, because no door stays open forever.

That is why Unredacted is putting serious work into FreeSocks v2. It uses Xray, a versatile traffic-routing engine that can make proxy traffic look more like ordinary web traffic, bundled with Unredacted's own open-source control plane, which rotates endpoints automatically when censors find and block a server. Users are already under pressure, and the less they have to adjust their setup, the better.

!!! note "Xray"

    Xray is a traffic-routing and obfuscation tool descended from the V2Ray project. Protocols such as VLESS, Trojan and Reality disguise proxy traffic as ordinary HTTPS and TLS, so the handshake and packet shapes that make a conventional VPN easy to identify are much harder to find in Xray traffic. That has made it a common proxy tool on heavily censored networks in recent years. See the [Xray-core project](https://github.com/XTLS/Xray-core).

## GreenWare and Low-Power Hardware

Tor relays, bridges and proxies all run on datacenter hardware, and that hardware has a financial, operational and environmental footprint. If privacy infrastructure is meant to last, the question is what is actually sustainable to operate.

GreenWare is Unredacted's attempt to shrink that footprint without shrinking capacity. Most Tor relay traffic does not need a server that draws power like a space heater. A relay needs a steady network, predictable CPU and enough memory to hold its state, a workload a single-board computer can handle if the chassis around it is built for the job.

They started with Raspberry Pi 5 boards powered over PoE (Power over Ethernet), with power and data fed through a single network cable. The idea worked: a typical datacenter server draws about as much as a small space heater, and a Pi draws less than a lightbulb. The first generation had limits, though. Density was lower than they wanted, and some supporting components were not built for the hours they were putting on them.

They now run two deployments in parallel. The first is a 1U chassis holding 20 ComputeBlade modules, all 20 deployed in their datacenter with part of their Tor exit relays moved onto them. The chassis pulls a little over 100W under load, about what an old incandescent bulb burns. The second is a custom Raspberry Pi chassis they designed after the ComputeBlade work showed them what they needed in the field. Both are live, and as of writing all 123 of their Tor exit relays run on this combined infrastructure, drawing roughly 400W in total. They plan to share more about the chassis design as the project matures.

The Tor network depends on people and organizations willing to operate infrastructure for it, and exits are the hardest part of that job, needing bandwidth, maintenance, abuse handling, legal nerve and money. Lowering the cost and power needed for real exit capacity means more people can take on a piece of the work, diversifying and growing the network.

Longer term, Unredacted wants to keep pushing on efficient hardware and carbon tracking, and eventually on renewable-powered micro points of presence, and welcomes partnerships with organizations and companies that want to see this grow.

The post closes on the people who keep the open internet open: researchers measuring censorship, relay operators providing bandwidth, and communities that refuse to leave one another behind. Unredacted's part is building and maintaining the routes people may need when the obvious ones disappear.

---

The following three sections were added by the anoni.net community.

## A Taiwan Comparison

Messages like the one Unredacted quotes are rare, because people living under censorship seldom have a safe channel to send them. We are a community based in Taiwan, where the network environment is relatively free: there is no Great Firewall, no mandatory VPN registration, and no state censorship orders to ISPs. That leaves Taiwan well placed to host Tor relays and bridges for blocked regions and carry a share of the circumvention work. Other places with similarly free connectivity, such as Singapore and Malaysia, are just as suitable as hosting locations.

The anoni.net community tracks the number and distribution of Tor relays in Taiwan through [Tor Relay Watch](/projects/pulse/). As of 2026-05-31, Onionoo (the Tor Project's relay data service) listed 12 running relays in Taiwan, only 3 of them with the Exit flag. A single organization, Unredacted, runs 123 exit relays and carried nearly 300 TiB in 30 days; Taiwan's nationwide exit count is under 3% of theirs. For the latest numbers, see [Tor Relay Watch](/projects/pulse/), which is updated continuously. How well OONI measurements cover Taiwan's networks is tracked on the [OONI Coverage](/projects/asn-coverage/) page.

Circumvention resources written in Chinese are comparatively scarce. Part of anoni.net's work is filling that gap with Chinese-language documentation such as [What Is Tor?](docs:tools/what-is-tor/), [Tor Snowflake](docs:tools/tor-snowflake/) and [What Is OONI?](docs:tools/what-is-ooni/), the same direction Unredacted Education takes.

## GreenWare's Feasibility in Taiwan

Unredacted runs 123 exit relays on 400W. At a typical Taiwan commercial electricity rate of roughly NT$3.5–6 per kWh (about US$0.11–0.19),[^1] 400W running year-round comes to about 3,500 kWh, or roughly NT$12,000–21,000 a year (about US$400–700). That is within reach for a campus IT center or a community workspace. Readers elsewhere can convert using their local rate.

Scaling up depends on hardware design. Maker communities in Taiwan know the Raspberry Pi 5 well, and PoE+ HATs and PoE switches are available through ordinary electronics retailers and online stores. ComputeBlade (the 20-module 1U chassis) has fewer retail channels in Taiwan and is usually obtained through official overseas orders or a community group buy. A campus server room suits this better than a home network: it has a static IP, academic network bandwidth, and someone to check on the machines regularly.

Campus Tor relays are one of anoni.net's three focus areas for 2026, and the community is turning campus deployment experience into a standard operating procedure (see the [Tor Relays on Campus Track](/join/relay-on-campus/) and the [account of setting up a Tor relay at NTNU](/updates/2025/12/ntnu-nz/)). Schools assessing a deployment can use Unredacted's GreenWare engineering as a reference point: start with a single PoE-powered Raspberry Pi 5 as a middle relay, and consider exits and chassis density once it runs stably.

Individuals and small groups can start with a Snowflake proxy (a browser extension or Docker), which costs almost nothing in electricity and is the lowest-barrier way into circumvention infrastructure (see [Tor Snowflake](docs:tools/tor-snowflake/)).

## Ways to Take Part

To help keep another route open for people in censored regions, start with any of these:

- **Learn about Unredacted**: visit [unredacted.org](https://unredacted.org/) for their services and transparency information, then decide whether to support their servers, bandwidth and staffing through their official channels.
- **Run Snowflake**: the lowest-barrier contribution, run from a browser extension or Docker (see [Tor Snowflake](docs:tools/tor-snowflake/)).
- **Run a Tor relay or bridge**: this needs a steady network and some operating time. The steps are in the [Tor Relay Setup Guide](/join/setup-tor-relay/) and the [Tor WebTunnel Bridge Setup Guide](/join/setup-tor-webtunnel/).
- **Campus Tor relays**: if you work or study at a college or university, start your assessment from the [Tor Relays on Campus Track](/join/relay-on-campus/).
- **Join the community discussion**: trade notes with other members over Matrix. The entry point is on [Take part](/join/), and other channels are on [Stay informed](/contact/).

## Related Reading

- [What Is Tor?](docs:tools/what-is-tor/)
- [What Is OONI?](docs:tools/what-is-ooni/)
- [Traffic through our community's Tor WebTunnel bridge after Iran's 80-day blackout](/updates/2026/05/iran-blackout-webtunnel/)
- [Setting up a Tor relay at NTNU](/updates/2025/12/ntnu-nz/)
- [Tor Relay Watch](/projects/pulse/)
- Same series: [Defending the public's right to know (OONI)](https://blog.torproject.org/Defending-the-right-to-know/), [Preserving evidence: How OpenArchive fosters accountability and media sovereignty](https://blog.torproject.org/preserving-evidence-openarchive-fosters-accountability-media-sovereignty/)

[^1]: Taiwan's 2026 average electricity rate is NT$3.7823 per kWh, held for April to September by the rate review of 2026-03-27; the actual per-kWh price varies by customer class and time-of-use tier. Source: [Taipower electricity rate schedule](https://www.taipower.com.tw/2289/2290/46940/). (Note added 2026-10: the rate review of 2026-09-18 deferred any adjustment, so the national average stays at NT$3.7823 per kWh from October, as [reported by Business Today](https://www.businesstoday.com.tw/article/category/183027/post/202609180046/), in Chinese.)
