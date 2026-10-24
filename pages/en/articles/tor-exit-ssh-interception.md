---
title: The October 2026 Tor Exit Relay Compromise and Operator Security Checks
description: In early October 2026 the exit policies of hundreds of Tor exit relays were altered to intercept SSH logins. This article covers what happened, how the various figures were counted, what is still unresolved, and how relay operators can check, respond to and prevent a compromise.
date: 2026-10-24
---

In early October 2026 the exit policies of hundreds of Tor exit relays were altered. Anyone who logged in to SSH with a password through those relays may have had the password captured. The clearest known way in comes from the relay family hit hardest: the attacker used a reused password to log in to a management server that accepted SSH password logins. For people running relays, in Taiwan or elsewhere, the first thing to do is turn off SSH password logins and use separate passwords for login, sudo and backups.

## Timeline of the Incident

All times are UTC unless noted, and the information was checked up to 24 October 2026. There are four first-hand sources: the notice from the Tor Network Health team (the Tor Project team that watches the relay network for anomalies) on the tor-relays mailing list, a post-mortem by the operator of the Quetzalcoatl relay family, a directory data analysis by another relay operator, and a write-up by the user who first made the problem public (the finder below). The directory analysis uses public data from CollecTor (Tor Metrics' archive of past directory documents) and was done with help from AI tools. Its scripts and CSV files are on GitHub and can be reproduced, but it is not an official Tor Project count.

- **28 August**: The attacker logged in to the Quetzalcoatl family's management server with the operator account's password, succeeding on the first try. Within five minutes they had root and installed Ebury (an OpenSSH backdoor), and just over an hour later they logged in to another server running exit relays and installed Ebury there too.
- **1 October, from 15:33**: 40 relays belonging to 21 operators other than Quetzalcoatl switched to the same exit policy within about five minutes, mostly through a configuration reload.
- **2 October, from 09:27**: All 277 Quetzalcoatl relays switched to a second exit policy. That morning (time zone not given) the finder saw a changed-host-key warning while using SSH over Tor, scanned every exit with exitmap (a tool that connects through each exit in turn and compares the responses) and reported it to the Network Health team in the evening.
- **4 October**: In the 01:00 consensus, exits using the attackers' policies held 7.46% of usable exit weight, the peak. Around 13:56 the Quetzalcoatl family was contacted by the Network Health team and stopped Tor on one host. From 18:00 the directory authorities (the handful of servers that vote on the relay list) began voting BadExit (clients no longer use the relay as an exit) and MiddleOnly (the relay may only be a middle hop) on the affected relays. The 21:00 consensus (the hourly list of usable relays and their flags published by the directory authorities) carried both flags.
- **5 October**: From 17:00 no relay using the attackers' policies was in the consensus. At 17:50 the Network Health team posted its notice on tor-relays.
- **7 to 22 October**: The Quetzalcoatl post-mortem (7 October), the directory data analysis (9 October) and the finder's write-up (20 October) were published, followed by reports from The Hacker News and SecureWorld on 21 and 22 October.

The flags took effect about two days after the finder's report, and it took nearly another day before the affected relays were gone from the consensus. Anyone who logged in to SSH with a password over Tor during that time, and accepted a new host key, may have had the password taken.

## Settings the Attackers Changed

The directory analysis sorts the attackers' exit policies into two. Policy A rejects ports 25, 110, 143, 445, 3389 and a few others, and accepts everything else. Policy B is Tor's default policy plus rejecting 465, 587, 993 and 995. Both accept 22 (SSH), and both close the encrypted mail ports 993 and 995. Policy B also leaves the plaintext ports 110 and 143 open, so mail fetched through a policy B exit could only travel in plaintext. The public data does not show why the attackers closed the encrypted ports.

Tor's `ExitRelay` defaults to `auto`, so a relay acts as an exit according to its exit policy as soon as torrc (Tor's configuration file) sets `ExitPolicy`, `ReducedExitPolicy` or `IPv6Exit`. According to the Network Health team's notice, the attacker, after gaining access to a Linux host, edits the torrc of non-exit relays to turn them into exits. In the directory analysis, 24 relays were not exits before the change and all of them got the Exit flag afterwards, although most affected relays were exits already.

Changing the exit policy is not enough on its own; the connections also have to be redirected to the interception servers. The Network Health team's notice asks operators to look for NAT (network address translation) rules that send port 22 somewhere else. According to the finder's write-up, an SSH connection through an affected exit was sent to one of 12 interception servers. Once the user ignored the warning and logged in, the attackers had the password. They relayed the session to the real server while recording every command typed, and opened a second connection to install Ebury on that server.

The finder's honeypot (a host set up for attackers to log in to, so their methods can be observed) showed the interceptor checking whether the account could use sudo after getting the credentials, then running a base64-encoded Perl installer. According to the 2024 report from the security company ESET, Ebury is an OpenSSH backdoor that has compromised about 400,000 servers since 2009. What the Quetzalcoatl family found on its hosts was version 1.8.3: a setuid `libkeyutils` library that belongs to no package, with the `libkeyutils.so.1` symlink pointed at it. The packaged files were left unmodified, so neither `dpkg -V` nor `debsums` flags anything. Ebury records every password sshd receives, failed attempts included, while its own backdoor logins leave no login records or shell history.

## Sources of the Figures

333, 377, 7.46% and the Exit flag count come from four different methods and cannot be converted into one another.

| Figure | Source | How it was counted |
|---|---|---|
| 333 | The finder's write-up | An exitmap scan of about 3,000 exits on 2 October: around a dozen exits presented a fake host key themselves, and over 300 forwarded connections to the 12 interception servers. The list and raw data are not public |
| 377 relays, 59 operators | Directory data analysis | Relays that published policy A or B between 1 and 4 October, 277 of them in the Quetzalcoatl family. The analyst notes this is a policy match, not proof of compromise |
| 7.46% | Directory data analysis | The share of consensus weight among all usable exits held by 351 affected usable exits in the 01:00 consensus on 4 October |
| 3,084 → 2,715 | Tor Metrics | Relays with the Exit flag, down 369 from 3 to 5 October and at 2,688 on 21 October. The count was already falling before the incident: 3,235 on 2 September and 3,068 on 1 October |

The Hacker News describes "342 relays that had blocked SSH" and "24 relays that had not been exits" as two separate groups, but by the directory analysis's own breakdown the 342 already include those 24.

## Known Ways In

The Quetzalcoatl family's operator acknowledges in the post-mortem that the fault was theirs ("The root cause was ours"). SSH login, sudo and the backup passphrase shared one password, which sat in plaintext in scripts on both servers, and the internet-facing management server accepted SSH password logins. The relay master identity keys the operator believed were kept offline (the long-term keys that stay off the relay host when `OfflineMasterKey` is set) had copies in the workstation backup on the management server, encrypted with the very password the attacker already had.

Where the attacker got that password before 28 August is still unknown. The author of ESET's Ebury report (the ESET researcher below) guessed on the mailing list that it was recorded when the operator logged in from a host already infected with Ebury. Why the other exit host accepted a key for which the operator could find no matching `authorized_keys` entry is also unanswered.

Why the other 58 operators' relays showed the same policies, and whether their hosts were compromised, has no answer yet. According to the directory analysis, the affected hosts were concentrated at the hosting provider FranTech (brand name BuyVM, `AS53667`). In the 1 October consensus, 71 of the 101 relays other operators ran at FranTech were affected, against 13 of 9,054 elsewhere. Of the 12 operators with relays both at FranTech and on other networks, none of their 50 relays on other networks was affected.

One explanation is that the hosting provider itself was compromised, which the ESET researcher listed on the mailing list as one possibility. ESET's 2024 report includes a case of attackers using a hosting provider's infrastructure to install Ebury on rented servers in bulk. ESET rented a virtual server from one such compromised provider and had Ebury on it within seven days. In the [provider memo](https://github.com/1aeo/TorExitPolicyManipulation/blob/main/collector-exit-policy-analysis/PROVIDER_MEMO.md) in the analyst's GitHub repository, credential or session theft clustering on FranTech customers is ranked as the best fit for the public data, because a FranTech-only mechanism cannot explain victims at other providers. The Quetzalcoatl family's compromised management server was also at a different provider. A BuyVM customer also wrote on the list that their own virtual servers showed nothing unusual and did not think the provider was compromised.

## Affected Relays in Asia

We matched the 377 relay IP addresses published by the directory analysis against the GeoIP database (IPFire Location) shipped with Tor. The United States had 171, Luxembourg 97, Germany 56 and Singapore 24, with the rest spread across Croatia, Moldova, the Netherlands, Switzerland, the Seychelles and India. None was in Taiwan, Japan, South Korea or Hong Kong. All 24 in Singapore belong to the Quetzalcoatl family and sit in one provider's Asian data centre; the one in India belongs to a different operator. This is our own matching (geolocation databases can be wrong), and the Tor Project has not published such figures.

The daily figures from [Tor Relay Watch](/projects/pulse/) (the last snapshot of each day, UTC) record the same change. Relays with the Exit flag in [Singapore](/projects/pulse/sg/) went from 34 on 3 October to 9 on 4 October, and stood at 8 on 23 October. We take the drop to be mostly the 24 Singapore relays above. Taiwan had between two and four exits throughout the same period.

## Relay Self-Checks

According to the Network Health team's notice, operators on Linux should check:

- In [Relay Search](https://metrics.torproject.org/rs.html), whether your relay shows an Exit flag or an exit policy you did not set
- Whether `ExitRelay`, `ExitPolicy`, `ContactInfo`, `MyFamily` or `Nickname` has changed in torrc or any file pulled in with `%include`
- NAT rules sending port 22 elsewhere, with `nft list ruleset` or `iptables -t nat -S`
- Unknown outbound connections with `ss -tnp`, and listening processes with `ss -tlnp`. A reply in the notice thread points out that other relays running their ORPort (the port relays use to connect to each other) on 22 is normal, so connections to them are not a sign of trouble
- The tor binary against your distribution's package, with `debsums tor` or `rpm -V tor`
- New users, `authorized_keys` entries, cron jobs and systemd units; one persistence method mentioned in the notice (a way to keep malware running after a reboot) is a root process disguised as an uppercase `CRON`
- Unauthorised kernel module loading, tunnelling interfaces and unexplained memory use

A clean result on all of these does not mean the host is clean. The Quetzalcoatl family's two servers showed none of the notice's NAT redirects, new users or keys, cron jobs or systemd units, and the tor binary had not been modified. The operator's advice is to check from a rescue system or a mounted offline disk image. If you have to log in to a suspect host, use a key and never type a password, because Ebury will record it.

The post-mortem lists several signs of Ebury (the full text also lists the attacker's source address and the fingerprints of three SSH keys):

- A setuid `libkeyutils` file, or a `libkeyutils.so.1` symlink pointing at a file that belongs to no package (`find / -xdev -name 'libkeyutils*' -perm -4000`, `dpkg -S "$(readlink -f /usr/lib/x86_64-linux-gnu/libkeyutils.so.1)"`, or `rpm -qf` on RPM systems)
- An abstract Unix socket (one with no path on the file system) starting with `@event-` in `/proc/net/unix`
- A process other than sshd in the `ssh.service` cgroup (`systemctl status ssh`; on Ubuntu 24.04 check `init.scope` too)
- In the logs, apt transactions without `Requested-By:` (unattended-upgrades never writes that line), su sessions opened by uid 0, and sudo running `base64 -d | perl`

On a running system, Ebury's userland rootkit hides these files. ESET's [detect_ebury.sh](https://github.com/eset/malware-research/tree/master/ebury) includes a step for this. It tries to connect to the abstract Unix sockets used by each Ebury version and, when one answers, reports the version and process. The socket address for 1.8.3 was only added to ESET's script on 9 October, so the script available when the post-mortem came out (7 October) could not detect that version. The script itself says that finding no socket does not mean the system is free of Ebury, and the full list of indicators still has to be checked.

The Quetzalcoatl family also recommends regular checks from outside: compare the exit policy, family and `ContactInfo` published by Onionoo (Tor Metrics' API for current relay data) or CollecTor with what you deployed. A compromised host's own files can be rewritten, while descriptors that have already been published cannot.

## Response after a Compromise

The Network Health team's notice sets out the response in this order:

1. Take the relay offline
2. Preserve the disk and logs before wiping
3. Reinstall rather than clean up in place
4. Generate a new relay identity; treat the old keys as stolen
5. Rotate every credential that was on the host

The Quetzalcoatl family adds that the credentials include every SSH key, every password and the WireGuard keys, and that memory should be dumped before rebooting or wiping; the hidden processes on its host disappeared after a reboot. The ESET researcher suggests dumping the network configuration first (`iptables-save`, `nft list ruleset`, `ip rule show`). Ebury spreads to other hosts, so each machine listed in the compromised host's `~/.ssh/known_hosts` needs checking too.

If you confirm or suspect a compromise, write to `bad-relays@lists.torproject.org`. Operators whose IP addresses were blocked by the directory authorities also need to write to the same address after cleaning up to be taken off the block list.

Operators who declare their family with `FamilyId` should rotate the family key following the [FamilyId page](https://community.torproject.org/relay/setup/post-install/family-ids/); otherwise an attacker's relay could falsely claim to be part of the operator's family. The page's procedure is to generate a new key, copy it to every relay, run with both the old and new `FamilyId` for a few days and then remove the old one. The Quetzalcoatl family further recommends that if any machine that ever held an offline master key is compromised, every relay identity using that key should be retired.

On Debian relays running several instances, each instance has its own systemd unit that can be enabled separately. On the Quetzalcoatl host the attacker had added a symlink to the boot target, so `systemctl disable tor` could not stop those instances starting. The family's approach is to disable the `tor@` units with `systemctl mask` and, because a live backdoor can undo the mask, to take the host offline as well.

## Compromise Prevention

The Tor Project's operator documentation has no guidance on SSH configuration. The practices below come from the Quetzalcoatl post-mortem, the ESET researcher and the tor-relays discussion, and they are recommendations from operators and researchers.

The first priority is turning off SSH password logins, with both `PasswordAuthentication` and `KbdInteractiveAuthentication` set to `no`. The latter defaults to `yes`, and with PAM (Linux's pluggable authentication modules) it can still produce a password prompt. Only accept connections to jump hosts (management entry points used only to reach other servers) and management servers through a VPN or an IP allow-list. After changing the configuration, confirm the effective values with `sshd -T`. sshd takes the first value it reads, so a `PermitRootLogin yes` that a VPS image placed earlier overrides a `no` added later.

Use separate credentials for login, sudo and backup encryption, and keep passwords out of scripts. Run automation through key-only accounts with narrowly scoped `NOPASSWD` sudo rules. Some in the discussion also suggested multi-factor authentication for SSH, and OpenSSH has supported FIDO/U2F hardware keys since version 8.2. A passphrase on a private key does not count as a second factor.

Do not run public web services or keep key backups on management servers. The Quetzalcoatl management server had a WireGuard management interface that had once been exposed to the internet, in a version with an unauthenticated file-read flaw (`CVE-2026-44343`). The operator later ruled it out as the way in but still lists it as something to avoid.

Offline master keys need to be genuinely offline and must not sit in a backup on any networked machine. Ship logs to another host for storage, and alert when sshd's `LogLevel` is set below INFO. Use a tool such as AIDE (a file integrity checker) to watch library directories for files that belong to no package or are setuid.

The community's [campus relay SOP](/join/relay-on-campus/sop/) (standard operating procedure) already requires key-only logins and limits SSH to the campus VPN range. It also recommends at least two key backups, one kept in the supervising professor's lab; in light of this incident, that copy belongs on offline media. The SOP's incident response section has been revised in line with the Network Health team's notice. Unless a compromise can be ruled out, the old identity keys are treated as compromised and a new relay identity is generated.

## SSH over Tor

When a host key changes, OpenSSH warns, disables password authentication and, with `StrictHostKeyChecking` at its default of `ask`, refuses to connect. Only after the user deletes the old entry in `known_hosts` does ssh have nothing to compare against and go on to ask for a password. A server contacted for the first time has no entry either, and the user only sees the usual confirmation prompt. The fingerprint should then be checked through another channel, for example by asking the administrator. Checking against SSHFP records (DNS records that publish host key fingerprints) requires setting `VerifyHostKeyDNS`, and only records validated by DNSSEC (a mechanism that signs DNS responses) are trusted automatically.

The finder published the ED25519 fingerprint of one interception server, `SHA256:6baCZCPsl+AfQuujUS81fMEE/C7UeJ+AwjrImqmDB3E`. Anyone who accepted an unfamiliar key can list their stored fingerprints with `ssh-keygen -lf ~/.ssh/known_hosts` and compare. Other interception servers may have used different keys, so no match does not mean you were unaffected.

The Hacker News infers from `RFC 4252` (the specification for SSH authentication) that only password logins had credentials taken. In public key authentication the signature covers an identifier unique to the session, so the interceptor cannot reuse it against the real server. A password, by contrast, is sent in plaintext inside the encrypted channel to whoever is at the other end, and that is the interceptor. The report also notes that the interceptor could still accept a key login and show a fake shell. Our inference is that a sudo password typed in that fake shell could leak as well.

The Hacker News lists the possible victims as people who logged in to SSH with a password over Tor between 1 and 5 October and accepted an unfamiliar or changed host key (the report gives no time zone); none of the four first-hand sources gives such a range. The start date is only a guide, since the Quetzalcoatl servers had unexplained hidden processes from 30 September. A post on the Tor forum on 31 August also reported a host key warning while using SSH over Tor, without naming an exit, and nothing we found links it to this incident.

Anyone who logged in to SSH over Tor with a password in early October, and accepted a new or changed host key, should treat the password as stolen. The server they logged in to may carry Ebury, so do not type any password on it until it has been checked, including a new one. Check it with a key login or from a rescue system first, then change the password everywhere it was used.

To manage a server over Tor, you can run SSH as an onion service (a service with a .onion address that is reachable only through Tor). The connection then reaches the server inside the Tor network without passing through an exit relay. The setup is covered in the [Onion Service Setup Guide](/join/setup-onion-service/), and the client then connects over Tor with `torsocks` or ssh's `ProxyCommand`.

## Open Questions

As of 24 October there was no public information on how the relays of the 58 operators other than Quetzalcoatl were changed. Whether the NAT redirects and fake `CRON` process in the Network Health team's notice come from the same people as the Ebury on the Quetzalcoatl hosts is also unclear. Where the stolen credentials go, and whether more relays were changed after 9 October, is not covered by any data so far. The ESET researcher wrote on the list that there are most likely other compromised Tor relays still unnoticed. The finder guessed from the attackers' broad collection of unencrypted data that a financially motivated crime group is behind it, and called that speculation.

If you find something wrong with your relay, write to `bad-relays@lists.torproject.org`, and you are welcome to discuss it with the community on [Matrix](/contact/).

## References

- [Security incident affecting some relay operators](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/WOHPLKCSHYXFTBRZXDENDKJZMBMPLMG5/): the Tor Network Health team's notice, 2026-10-05
- [Ebury 1.8.3 on two Quetzalcoatl relay servers: timeline, lessons, open questions](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/QHRD6YOX6RZRDR7NCHNDO7GLCEA6VFM6/): the Quetzalcoatl family's post-mortem, 2026-10-07
- [Reply from the ESET researcher](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/thread/RXWGWYYYKBDEBNXC2C3NYIQ2HHHWXL7O/): tor-relays, 2026-10-08
- [Directory data analysis](https://lists.torproject.org/mailman3/hyperkitty/list/tor-relays@lists.torproject.org/message/Z2B6XYKJZBBQADU77MSNL6FJP7MHZHIV/): tor-relays, 2026-10-09, with scripts and data in [1aeo/TorExitPolicyManipulation](https://github.com/1aeo/TorExitPolicyManipulation)
- [How I got over 300 Tor exit nodes removed](https://kaba.cx/posts/20261020_Tor/): the finder's write-up, 2026-10-20
- [Attackers Hijacked Over 300 Tor Exit Relays to Intercept SSH Connections](https://thehackernews.com/2026/10/attackers-hijacked-over-300-tor-exit.html): The Hacker News, 2026-10-21
- [Tor Exit Relay Hijack: 'The Root Cause Was Ours'](https://secureworld.io/industry-news/tor-exit-relay-hijack-root-cause): SecureWorld, 2026-10-22
- [Ebury is alive but unseen](https://www.welivesecurity.com/en/eset-research/ebury-alive-unseen-400k-linux-servers-compromised-cryptotheft-financial-gain/): ESET, 2024-05-14
- [Bad relays](https://community.torproject.org/relay/community-resources/bad-relays/): the Tor Project's guide to reporting bad relays

## Related Reading

- [Tor Relay Setup Guide](/join/setup-tor-relay/): installing a middle relay, torrc settings and running several instances
- [Campus Tor Relay Deployment SOP](/join/relay-on-campus/sop/): a template for SSH, firewall and handover settings
- [Deployment Paths and Open Problems for Stateless Tor Relays](/articles/stateless-relays/): keeping relay hosts stateless and handing identity keys to a TPM
- [Tor Relay Watch](/projects/pulse/): relay counts, bandwidth and flag changes in Taiwan and nearby regions
