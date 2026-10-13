---
title: Deployment Paths and Open Problems for Stateless Tor Relays
description: A guide to Osservatorio Nessuno's Tor Blog post A Server That Forgets, covering TPM-backed relay keys, three deployment paths and the unsolved engineering problems, with notes for relay operators in Taiwan.
date: 2026-04-10
---

The less a seized relay can hand over, the safer its users are. Osservatorio Nessuno, which runs exit relays in Italy, takes that idea down to the operating system: every boot starts from the same read-only image, and the relay's identity key is kept by the TPM. Their guest post on the Tor Blog compares three deployment paths already in use and lists the problems nobody has solved yet, including re-sealing, automatic updates and memory ceilings. It is a useful map for operators weighing hardware and deployment options.

This guide follows the structure of [A Server That Forgets: Exploring Stateless Relays](https://blog.torproject.org/exploring-stateless-relays/), published on 2026-04-08 as part of the Tor Blog's spotlight series on organizations defending the free internet. Where the summary says "the authors", it means Osservatorio Nessuno. The notes for relay operators in Taiwan at the end were added by the anoni.net community.

[![A Server That Forgets](https://forum.torproject.org/uploads/default/original/2X/e/ee9375b0ec3906d4a0338bc230d97d0a659d996a.jpeg){ .shot }](https://blog.torproject.org/exploring-stateless-relays/)

Relay operators work against adversaries, private and state-backed, who try to undermine Tor by attacking the nodes it is made of. Some operators also face seizures, raids and direct physical access to their hardware, with precedents in [Austria](https://www.zdnet.com/article/austrian-man-raided-for-operating-tor-exit-node/), [Germany](https://forum.torproject.org/t/tor-relays-artikel-5-e-v-another-police-raid-in-germany-general-assembly-on-sep-21st-2024/14533), [the United States](https://www.npr.org/sections/alltechconsidered/2016/04/04/472992023/when-a-dark-web-volunteer-gets-raided-by-the-police) and [Russia](https://torservers.net/blog/2017-04-14-freebogatov-relaymob/), and very likely elsewhere. In those cases the server itself becomes a liability.

Tor is designed so that no single operator or server can reconstruct who is talking to whom, and journalists, activists and whistleblowers rely on that property. A relay whose contents can be handed over after a seizure erodes the trust the whole system depends on. The authors explore how a stateless, diskless operating system can improve relay security from firmware to user space, with the emphasis on software integrity and resistance to physical attacks. They are explicit that relay management varies with context, technical capability, budget and jurisdiction, and that they want to start a discussion rather than prescribe one model.

## Stateless Systems

A stateless system keeps nothing between reboots. Each boot starts from a known, fixed image, the same approach [Tails](https://tails.net/) takes. Running a Tor relay entirely in RAM is an old idea: [Tor-ramdisk](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html), a uClibc-based micro Linux distribution built for exactly this purpose, dates back to at least 2015.

For relay operators, the design enforces better habits and raises the security bar:

- **Physical attack resistance**: a seized or cloned machine has nothing to analyze, and depending on the setup, extracting the relay keys may become infeasible.
- **Declarative configuration**: the system is version controlled, and since every boot applies the declared configuration from scratch, it cannot drift.
- **Immutable runtime**: the filesystem is read-only, so an attacker who gains code execution cannot persist anything across a reboot.
- **Reproducibility**: a system that does not change between reboots is easier to verify, and eventually to reproduce and audit.

## The Difficulty of Stateless Tor Relays

Relays build reputation over time. One that has run for months earns bandwidth flags that make it more useful to the network, and that reputation is tied to a long-term cryptographic identity key. Lose the key and the relay loses its identity and its standing, and has to start from scratch. The identity therefore has to survive reboots without being extractable. A key on disk can be seized and copied; a key held in a security chip such as a TPM is likely harder for an attacker to get at.

Identity is not the only state. A relay also accumulates a state file with bandwidth history and other temporary information, and discarding it on every reboot costs performance. Running entirely in RAM means the whole OS has to fit in memory with no swap to fall back on, and when processes exceed the available memory, the kernel's OOM killer terminates them outright. Swapping glibc's allocator for jemalloc or mimalloc [cuts Tor's memory footprint](https://1aeo.com/blog/tor-memory-optizations-what-actually-works.html) from around 5.7 GB to under 1.2 GB on a busy guard relay, mostly by avoiding fragmentation from high-churn directory cache objects.

## The Role of the TPM

A TPM (Trusted Platform Module) is a dedicated chip on the motherboard that stores cryptographic keys and performs operations with them without exposing the private key to the operating system. It can seal a secret, binding it to a specific measured state of the machine, so the key is usable only when the measured software stack matches the one present when the key was created.

For a stateless relay, this means the identity key lives in hardware, survives reboots, and cannot be extracted by conventional means even with physical access. TPMs also support remote attestation: the chip can prove to an external system which software the machine booted, backed by a hardware-rooted signature. That makes it possible to verify what a node is running without trusting its operator.

The TPM has limits. Tor's ed25519-based keys are not supported by TPM chips, so the key is encrypted by the TPM but still stored as a byte string in non-volatile memory, and exporting it remains technically possible. Sealing also requires deciding in advance which software state the TPM will trust. Updating the kernel or bootloader changes the measured state, and the operator has to re-seal by predicting what the next boot will look like.

## Existing Deployment Paths

Operators have settled at different points on the trade-off between simplicity and depth of security.

### Minimal Ramdisk

The simplest approach runs everything in RAM and manages keys by hand. [Tor-ramdisk](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html) has worked this way since 2015: identity keys are exported and imported over SCP, and a reboot without that step means starting over. There is no TPM, no attestation and no verified boot, only the guarantee that RAM does not survive a power cut. It is still a meaningful step up from a conventional disk-based setup.

### VM-Based Ramdisk

[Emerald Onion](https://blog.emeraldonion.org/evolving-our-tor-relay-security-architecture) runs a separate Alpine Linux image (66 MB each) for every relay on a Proxmox hypervisor. The VMs boot entirely into RAM with no persistent storage attached. Identity is handled with Tor's OfflineMasterKey feature, so the long-term master key is generated offline and never touches the relay. Updates are image rebuilds, rollback is trivial, and no special hardware is needed.

### Bare Metal with a TPM-Bound Identity

The authors' own tool, [Patela](https://github.com/osservatorionessuno/patela), takes the hardware route. The relay boots through [stboot](https://docs.system-transparency.org/st-1.3.0/docs/reference/stboot-system/), a bootloader that fetches a signed OS image and verifies it cryptographically before handing over control. Once running, the node pulls its configuration from a central server over mTLS. A compromised central server can deny service, but it cannot push credentials to the node or extract keys from it. The identity key sits in the TPM's non-volatile memory, bound to the measured boot state, so it survives reboots and resists extraction even with physical access. The price is operational complexity: bare metal is required, and every update means re-sealing.

## Open Problems

Some of these are specific to the authors' setup; others apply to any stateless relay.

### Re-Sealing after Updates

When the software stack changes, so does the TPM's measured state. Automating re-sealing means predicting the boot measurements an update will produce, and that remains one of the harder unsolved problems. Tools such as systemd-pcrlock are moving in this direction but are not turnkey yet.

### Stateless Reboots versus Upgrades

The authors update the Tor binary with standard unattended upgrades, but a reboot reverts to the OS image, which still carries the previous version, and the relay is silently downgraded. Reconciling automatic security updates with stateless images is not fully solved.

### Memory Constraints

Without swap, a process that exceeds available memory is killed without warning, and Tor's memory use is hard to predict at runtime. The allocator change helps enormously, but the underlying constraint remains.

### Network Stability

Persistent updates can only be applied by rebuilding the image and booting it again. A relay that restarts too often risks losing its Stable flag, which affects how much traffic the network sends it.

## Future Directions

### Remote Attestation

Sealing binds a key to a machine state; attestation lets the node prove that state to someone else. A verifier such as a configuration server, or eventually the Tor directory authorities, can issue a cryptographic challenge that only a node running the expected software stack can answer. Boot integrity then becomes something checkable from outside, which reduces how much anyone has to trust the operator.

### Transparency Logs

A measured boot chain can be published. If operators provide reproducible build recipes, anyone can recompute the expected hash and compare it with what the TPM reports. An append-only transparency log would make those attestations publicly auditable, and the Tor community could run an independent monitor across the relay fleet.

### Confidential Computing

The VM path can be extended with technologies such as AMD SEV-SNP, which isolate a guest VM's memory from the hypervisor itself. This also reduces operator trust and narrows the security gap between the VM and bare-metal approaches.

### Smaller Hardware

Walking onions, a proposed Tor protocol extension, would remove the need for each node to hold a full view of the network locally. If arti and related tools can run on smaller hardware, devices that cannot currently afford the resource cost could become relays.

## The Authors' Conclusion

For a system like Tor, statelessness helps prevent both attacks and operator mistakes, and with further research it could raise the trustworthiness of the network as a whole. It comes with real operational costs and genuinely hard open problems, even for well-resourced projects and organizations, but it can serve as a foundation for privacy infrastructure, and similar ideas could apply to other layers of the stack.

The work started at [Tor Community Gathering 2025](https://tcg2025.4711.se/sessions/stateless_tor_relay/) and is ongoing. The authors want to hear from relay operators, Tor tooling developers, and anyone who has thought about these open problems.

## References

- [Stateless Tor Relay – Tor Community Gathering 2025](https://tcg2025.4711.se/sessions/stateless_tor_relay/)
- [Patela v1: A Basement Full of Amnesic Servers](https://osservatorionessuno.org/blog/2025/05/patela-a-basement-full-of-amnesic-servers/)
- [Patela v2: From Certificates to Hardware](https://osservatorionessuno.org/blog/2025/12/patela-v2-from-certificates-to-hardware/)
- [stboot System Documentation – System Transparency](https://docs.system-transparency.org/st-1.3.0/docs/reference/stboot-system/)
- [Tor-ramdisk 20150714 Release Announcement](https://archive.torproject.org/websites/lists.torproject.org/pipermail/tor-talk/2015-July/038493.html)
- [Evolving Our Tor Relay Security Architecture – Emerald Onion](https://blog.emeraldonion.org/evolving-our-tor-relay-security-architecture)
- [Tor Memory Optimizations: What Actually Works – 1AEO](https://1aeo.com/blog/tor-memory-optizations-what-actually-works.html)

---

## Notes for Relay Operators in Taiwan

These notes come from the anoni.net community, based in Taiwan. Taiwan is highly connected and has a mature commercial hosting market, and it also sits under the pressure of regional information conflict, so any technical approach there has to be quick to deploy and hold up under real strain. Operators in Hong Kong, Macau, Singapore or Malaysia work under different legal regimes and hosting markets, and the same questions need answering against local conditions.

Taiwan's small-server suppliers, datacenter services and civic-tech community can help operators move quickly to standardized images, incident procedures and verifiable operating records. Most relays in Taiwan, though, are run by volunteers spread across different places. When an abuse complaint, an equipment-handling request or contact from law enforcement arrives without a prepared process, a better architecture does nothing to reduce the risk the operator personally carries. Three directions are worth starting on.

### Volunteer Operations and Legal Process

Relay and exit operators in Taiwan can write down standard procedures for datacenter notices, law-enforcement contact and equipment seizure. Reducing what can be extracted from a machine in advance also reduces the operator's personal exposure when an incident happens.

### Hardware Sourcing and Supply-Chain Cost

TPM-equipped machines, small servers and hosting are all available in Taiwan, but costs vary widely. If the community settles on a few reproducible hardware and image profiles, maintenance and audit costs stay manageable. If every team assembles its own stack, security claims become hard to compare and maintenance costs keep rising.

### Public Accountability for Verifiable Computing

Measured boot chains, remote attestation and transparency logs matter beyond the Tor community; they connect to wider civic-tech conversations about transparency in critical infrastructure. Attestations support public trust only if they become shared evidence that people outside the field can understand. If only a handful of specialists can read them, outside trust still rests on reputation.

## Related Reading

- [Tor Relay Setup Guide](/join/setup-tor-relay/): setup steps and operating configuration for a middle relay
- [Tor Relays on Campus Track](/join/relay-on-campus/): assessment and field experience from running relays at colleges and universities
