---
title: Decentralized Website Publishing
description: The design trade-offs between self-hosting, CDNs, IPFS, and onion services, how content addressing differs from connection anonymity, and how the anoni.net docs site publishes three copies at once.
date: 2026-05-01
---

Beyond a self-hosted server with DNS, a website can now be published through a CDN that caches content on edge nodes worldwide, through IPFS, which uses content addressing to move files between nodes, or as a Tor onion service running directly on the Tor network under a `.onion` address. The last two are often discussed together, yet IPFS addresses deletion and takedown while onion services address connection anonymity and IP blocking. Treating IPFS as an anonymity tool, or expecting an onion service to survive a takedown, ends in disappointment. The anoni.net docs site publishes a standard site, an onion copy, and an IPFS copy, and its deployment serves as a worked example.

## Publishing Options

From centralized and fast to decentralized and censorship-resistant, there are five common options:

- **Self-hosted server**: you manage your own IP address and DNS. Entirely under your control and entirely concentrated. A blocked IP address or a seized server takes the site offline.
- **CDN** (Cloudflare, Fastly, CloudFront): edge nodes proxy the traffic. Strong performance and DDoS resistance, with heavy dependence on the CDN provider and on DNS.
- **Static hosting** (GitHub Pages, Cloudflare Pages, Netlify): simple deployment, and the provider can remove the site unilaterally.
- **IPFS**: content is addressed by hash, so any node can serve the same content. There is no single point to take down, and whether the content survives depends on someone pinning it.
- **Onion service**: the site runs on the Tor network with no public IP address and no DNS. Connection anonymity and immunity to IP blocking, at the cost of performance and a limited set of clients that can reach it.

Real deployments usually mix them: a CDN for the main site's performance, an IPFS mirror against deletion, and an onion mirror against blocking.

## IPFS Design

IPFS (InterPlanetary File System) is built around content addressing:

- **CID (content identifier)**: a hash computed from a file's content, which also serves as its address. Identical content has an identical CID on every node.
- **DHT (distributed hash table)**: nodes ask each other who holds a given CID and locate it with the Kademlia algorithm, with no central registry.
- **IPNS (InterPlanetary Name System)**: maps a fixed name to the current CID. Updating content changes the CID, and the IPNS record follows.

Content addressing gives publishing three properties:

1. **No single place to take down**: as long as some node pins the CID, the content stays retrievable.
2. **Detectable tampering**: the CID is a hash of the content, so any modification changes it, and readers can verify it themselves.
3. **Sharing across nodes**: one file referenced by any number of sites has a single CID and a shared cache.

The limits:

- **Survival depends on pinning**: content no node pins disappears in garbage collection. Putting something on IPFS is not the same as preserving it.
- **DHT lookup latency**: first retrieval is slower than HTTP.
- **Gateway dependence**: most readers go through a public gateway, and a blocked gateway means no access. The pool of public gateways is also shrinking. Cloudflare retired cloudflare-ipfs.com and cf-ipfs.com in August 2024 and redirected their traffic to ipfs.io and dweb.link, and those two shut down on 30 September 2026 when Interplanetary Shipyard ended its IPFS work (the effect on pinning nodes is covered in [Pinning the Docs Site's IPFS Mirror](/join/pin-ipfs-mirror/#ipfs-maintenance-2026)).
- **Limited dynamic content**: IPFS suits static content, and anything dynamic needs another layer.

## Onion Service Design

Version 3 Tor onion services put a site directly on the Tor network (setup steps are in the [Onion Service Setup Guide](/join/setup-onion-service/)):

- **Self-authenticating addresses**: a v3 `.onion` address is 56 characters long and encodes the service's ed25519 public key, so it needs no DNS and no certificate authority, and there is one less place where name resolution can be intercepted or altered[^1].
- **Descriptor publishing**: the service publishes a descriptor listing its introduction points to the hidden service directories (HSDirs).
- **Rendezvous protocol**: the user and the service build an encrypted connection through a rendezvous point inside the Tor network, and neither learns the other's IP address.

What that means for publishing:

1. **Two-way connection anonymity**: the site cannot see the visitor's IP address, and the visitor cannot see the site's.
2. **No DNS dependence**: the `.onion` address authenticates itself, with no certificate authority trust chain involved.
3. **Immunity to IP blocking**: traffic stays inside Tor, so blocking the site's IP address achieves nothing.
4. **No public IPv4 address needed**: the service can start from behind NAT or on a dynamic address.

The limits:

- **Performance**: the circuit has three hops on the client side and three on the service side, six relays in total, plus the rendezvous step, so latency is higher than a direct connection.
- **Tor dependence**: heavy blocking of Tor relays affects the whole `.onion` ecosystem.
- **Poor fit for heavy static assets**: sending images and video over Tor is expensive.
- **Visitor barrier**: visitors need Tor Browser or another onion-capable client.

## IPFS and Onion Services Compared


| Aspect | IPFS | Onion |
|---|---|---|
| Problem addressed | Deletion resistance, no central point of failure | Connection anonymity, resistance to IP blocking |
| Visitor anonymity | ❌ none built in | ✅ by default |
| Service anonymity | ❌ node IP visible | ✅ by default |
| Tamper detection | ✅ the CID is a hash | Requires TLS or signatures on top |
| Takedown resistance | ✅ multiple nodes pinning | Partial, since the operator can shut a single service down |
| Large file performance | Moderate | Poor |
| Dynamic content | Difficult | Comparable to an ordinary site |
| Visitor barrier | Low, a browser through a gateway | High, requires Tor Browser |

For deletion resistance, use IPFS. For connection anonymity, use an onion service. When both matter, publish the same site as two mirrors.

## Known Limits and Risks

Before choosing a combination, weigh what each technology cannot deliver:

- **IPFS provides no connection anonymity**: the PeerID is long-lived, DHT lookups happen on the public network, and third parties can see which IP address is looking for which CID (the full picture of what is exposed is in [Networks Mistaken for Anonymity](docs:basics/mistaken-for-anonymity/)).
- **IPFS content survives only while someone actively pins it**: centralized pinning services such as Pinata, or decentralized storage protocols built on token incentives such as Filecoin, put permanent storage back in the hands of a third party.
- **Onion services depend on the Tor network**: heavy blocking of relays, or the Tor Project ceasing operation, would affect the whole `.onion` ecosystem.
- **The entry points are mostly still centralized services**: readers arrive through a public gateway or Tor Browser, and those entry points are themselves attack surface. Public gateways also shut down in batches, and a site that hardcodes one gateway into its URLs loses those links when that gateway closes.
- **Legal grey areas**: running a Tor exit node or offering IPFS pinning carries different risks in different jurisdictions.

## Common Combinations

### Onion and IPFS Mirrors

The main site is published to the ordinary web as usual, with two mirrors alongside it:

- An IPFS mirror, with one CID for each release, which community volunteers can help pin (see [Pinning the Docs Site's IPFS Mirror](/join/pin-ipfs-mirror/)).
- An onion mirror, carrying the same content as the main site with anonymous access.

EFF[^2], Proton, the BBC, and the US Central Intelligence Agency (CIA) have all set up official onion mirrors, and the onion site The New York Times ran from 2017 closed in March 2025[^3]. Cloudflare also offers Onion Routing: once a site enables it, responses carry an `alt-svc` header, and Tor Browser visitors connect through a Cloudflare `.onion` endpoint instead of through an exit relay[^4].

### IPFS and ENS

ENS (Ethereum Name Service) can give IPFS content a memorable name (for example `example.eth`), with an ENS record pointing at the current CID and updated on each release. ENS itself depends on the Ethereum blockchain and names cost money, so the decentralization comes with conditions.

## The anoni.net Docs Site Deployment

The anoni.net docs site publishes a standard site, an onion copy, and an IPFS copy with the same content, and three build pipelines handle the differences in URLs and paths.


1. **Source**: Markdown for MkDocs Material, kept in `anoni-net/docs` on GitHub.
2. **Standard site and onion**: a push to the `docs` branch triggers `build_docs.yml` in GitHub Actions, which builds both copies of the three-language static site and uploads them with `aws s3 sync --delete` to two prefixes in the same S3 bucket (`docs/` and `docs-onion/`). The standard site is served through Cloudflare. Before the onion build, `replace_sitename_anoni_onion.sh` rewrites the site's URLs to `docs.<onion address>`, and the analytics scripts and service worker are removed. `build_docs_anoni.sh` and `build_docs_anoni_onion.sh` are local versions of the same steps.
3. **IPFS**: `build_docs_anoni_ipfs.sh` is not part of the workflow and runs separately. The script rewrites URLs to the IPFS gateway address, builds the three languages, confirms that no main-site URLs remain in the output, and then `upload_to_ipfs.sh` uploads the result and updates the IPNS name. The community's own gateway is `ipfs.anoni.net`, and `_dnslink.anoni.net` points at the same IPNS name.

How readers use the onion or IPFS copy, and who can see what along the way, is covered in [How you are reading this](docs:about/how-you-are-reading/).

### Operational Trade-Offs

- **Pinning and survival**: community members can pin the mirror to improve its odds of survival ([instructions](/join/pin-ipfs-mirror/)), with no formal guarantee.
- **Onion latency**: over Tor, single-page applications and heavy JavaScript bundles are unpleasant to use, so the docs site stays a static site with one HTML file per page.
- **Roles of the three addresses**: the standard site is the main entry point, and the IPFS and onion copies are the redundancy and anti-blocking channels.

### Problems in Practice

- Public IPFS gateways are sometimes unstable, which affects first loads. Gateways can also shut down, so the mirror uses site-root-relative internal links, and switching gateways does not require rebuilding the whole mirror.
- The IPFS mirror is built and uploaded separately, so it may update later than the standard site and the onion copy.
- Three languages increase the number of CIDs on IPFS, and the pin list grows accordingly.

## Related Reading

- [How you are reading this](docs:about/how-you-are-reading/): how the standard site, the onion copy, and the IPFS mirror differ for readers
- [Networks Mistaken for Anonymity](docs:basics/mistaken-for-anonymity/): what IPFS and similar networks expose
- [What Is Tor?](docs:tools/what-is-tor/): the design of the Tor network and the threats it faces
- [The Internet Coup](https://anoni.net/docs/reports/interseclab-network-coup/) (in Chinese): InterSecLab's analysis of leaked documents on the export of China's Great Firewall technology to other countries, showing how centralized censorship infrastructure operates
- [Post-Quantum Cryptography](/articles/post-quantum/): the threat quantum computers pose to current public-key cryptography, and the migration timeline

## Ways to Get Involved

- [Pinning the Docs Site's IPFS Mirror](/join/pin-ipfs-mirror/): keep an extra copy of the docs site's IPFS mirror on an always-on IPFS node
- [Onion Service Setup Guide](/join/setup-onion-service/): set up a v3 onion service, connect it to nginx, and keep it running
- [Tor Relay Setup Guide](/join/setup-tor-relay/): setting up and maintaining middle relays, bridges, and exit relays
- [Tor Relays on Campus Track](/join/relay-on-campus/): proposing and negotiating a relay at a school
- [Localization and Translation](docs:community/i18n/): the translation workflow for the docs site and Tor documentation

[^1]: [V3 onion services usage](https://blog.torproject.org/v3-onion-services-usage/), The Tor Project
[^2]: [EFF Now Has Tor Onions](https://www.eff.org/deeplinks/2023/04/eff-now-has-tor-onions), Electronic Frontier Foundation
[^3]: [\[Onion services\] Remove NYTimes logo](https://gitlab.torproject.org/tpo/web/community/-/issues/374), Tor Project GitLab
[^4]: [Onion Routing](https://developers.cloudflare.com/network/onion-routing/), Cloudflare
