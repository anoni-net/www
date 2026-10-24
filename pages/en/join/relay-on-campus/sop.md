---
title: Campus Tor Relay Deployment SOP
description: Technical procedure for running a Tor relay on a university network in Taiwan, with a torrc example, UFW firewall rules, two status page options, monitoring, an incident runbook, acceptance testing, IPv6, and handover.
---

This page covers what the [Tor Relay Setup Guide](/join/setup-tor-relay/) leaves out for a university network. It draws on community member NZ's deployment at National Taiwan Normal University, and is meant to be used with the [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/) and the [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/).

It assumes the institution has already approved the relay. If you are still deciding whether to do this or how to make the case to your institution, start with the [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/).

## Campus and personal deployments compared

A campus network differs structurally from a home connection or a personal VPS, and the differences drive the technical choices:

- **Institution-assigned IP address**: usually one static IPv4 address, requested through the IT centre
- **Separate IPv6 request**: most campuses do not enable IPv6 by default, so dual stack has to be requested on its own
- **Exceptions for externally reachable services**: on TANet campus networks, services are not reachable from outside by default, and each one goes through an exception request
- **SSH limited to the campus VPN range**: management access is not exposed to the internet
- **Every setting explainable to the institution**: every open port and every traffic flow should map to something in the proposal
- **Handover after graduation**: `ContactInfo` does not use anyone's personal address

## Scope and non-scope

When talking to an IT centre, stating what you will not do matters more than stating what you will.

### In scope

- A non-exit relay only, acting as entry guard and middle relay
- One public artifact: a node status page containing no user data

### Out of scope

- No VPN, proxy, or Tor client services (no SocksPort, no DNSPort)
- No onion services
- No changes to the campus border firewall, DNS resolution, or content filtering policy
- No deep packet inspection (DPI)

### Reversibility

The relay can be taken offline within 10 minutes at any time by stopping the systemd service and closing the ORPort.

## Services and connections

### Inbound

| Service | Port and protocol | Source | Notes |
|---|---|---|---|
| Tor ORPort | 9001/tcp | Internet | TLS between relays, the only required inbound port |
| HTTP (ACME) | 80/tcp | Internet | Let's Encrypt issuance and a 301 redirect |
| HTTPS (status page) | 443/tcp | Internet | The public status page |
| SSH | 22/tcp | Campus VPN range | Management only, campus range |
| DirPort | Closed | – | Left disabled to reduce attack surface |

Of the Tor-related TCP ports, only the ORPort is exposed. If 443 is not taken by the status page or another service, moving the ORPort to 443 makes the relay easier to reach for users on heavily censored networks.

### Outbound

| Purpose | Port and protocol | Destination |
|---|---|---|
| Directory consensus and connections to other relays | TCP 443, 9001, and others (dynamic) | Directory authorities and relays |
| System updates | TCP 80 and 443 | Package mirrors |
| Time synchronization | UDP 123 | Designated NTP server |

### Explicitly blocked

- All UDP except the designated NTP server
- Mail ports: SMTP 25, 465, 587
- IRC 6667 and 6697, and common peer-to-peer ports
- SocksPort, DNSPort, and HTTPTunnelPort, all left disabled

## Operating system and security baseline

Use a minimal install of Ubuntu Server 24.04 LTS, then apply the following:

1. **Minimal packages**: `tor`, `nginx`, `certbot`, `fail2ban`, `unattended-upgrades`, `rsyslog`, `auditd`, `chrony`, plus `prometheus-node-exporter` if needed
2. **SSH configuration**
    - Keys only: `PasswordAuthentication no`
    - No direct root login: `PermitRootLogin no`
    - Restricted users: `AllowUsers <account>`
    - Timeout: `ClientAliveInterval 300`
3. **Automatic security updates** through `unattended-upgrades`
4. **Time synchronization** with `chrony`, with incident timelines recorded in UTC
5. **Hardening**: AppArmor enabled, `fs.protected_*` parameters set
6. **Persistent logs**: `journald` with `Storage=persistent`, optionally forwarded to an institutional SIEM through `rsyslog`
7. **File integrity (optional)**: AIDE with periodic baseline comparison
8. **Disk encryption (optional)**: LUKS on the whole disk where the hardware allows, or at least protecting `/var/lib/tor`
9. **Backups**: offline or off-site copies of `/etc/tor/torrc` and `/var/lib/tor/keys/`, with the **identity key kept strictly confidential**

## Tor installation

- **Package source**: prefer the [Tor Project's own repository](https://support.torproject.org/apt/tor-deb-repo/), since distribution packages usually lag by a version or two
- **Service account**: run as the packaged `debian-tor` account, **never as root**
- **Non-exit only**: declare it explicitly with `ExitRelay 0` and `ExitPolicy reject *:*`, so the relay never acts as an exit

## torrc reference configuration

At `/etc/tor/torrc`:

```bash
# Identity
Nickname    <YourSchoolRelayName>
ContactInfo <project-email@example.edu> - Non-exit relay at <Dept/School>; Abuse: <noc@example.edu>

# Guard and middle only, never exit
ExitRelay   0
ExitPolicy  reject *:*

# ORPort: the only required inbound service
ORPort      0.0.0.0:9001

# No directory mirror
DirPort     0

# No local SOCKS proxy
SocksPort   0
SocksPolicy reject *

# Control port, local only, for nyx and operations
ControlPort           127.0.0.1:9051
CookieAuthentication  1
CookieAuthFileGroupReadable 1
DataDirectoryGroupReadable  1

# Bandwidth, adjusted to institutional policy
# Example: 80 MB/s sustained, 120 MB/s burst
RelayBandwidthRate    80 MB
RelayBandwidthBurst   120 MB

# Logging at notice level, avoiding sensitive detail
Log notice file /var/log/tor/notices.log

# MetricsPort (optional): local or internal monitoring only, never exposed
# MetricsPort       127.0.0.1:9035
# MetricsPortPolicy accept 127.0.0.1
```

### ContactInfo

- Use a project address or a shared society mailbox rather than a personal one
- Include an abuse contact so the Tor network health team can reach the operators
- The field appears publicly in Relay Search, so **treat it as public information before you write it**

### MetricsPort security

`MetricsPort` lets Prometheus scrape the relay's metrics. According to the [Tor Project's guidance](https://support.torproject.org/relay-operators/relay-bridge-overloaded/), exposing it publicly is dangerous for Tor users. For remote scraping, restrict the source strictly through both the firewall and `MetricsPortPolicy`, and put it behind a TLS proxy.

## UFW firewall rules

Default policy:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw logging on
```

SSH limited to the campus VPN range (replace `<campus CIDR>` with your institution's range):

```bash
sudo ufw allow from <campus CIDR> to any port 22 proto tcp comment 'SSH from campus VPN'
sudo ufw limit 22/tcp comment 'Rate-limit SSH'
```

Web services for the status page:

```bash
sudo ufw allow 80/tcp  comment 'HTTP for ACME/redirect'
sudo ufw allow 443/tcp comment 'HTTPS status site'
```

Tor ORPort, the only port a guard or middle relay needs open:

```bash
sudo ufw allow 9001/tcp comment 'Tor ORPort'
```

MetricsPort, closed by default and opened only to an internal monitoring host `<monitoring host IP>`:

```bash
sudo ufw allow from <monitoring host IP> to any port 9035 proto tcp comment 'Prometheus -> Tor MetricsPort'
```

Enable and verify:

```bash
sudo ufw enable
sudo ufw status numbered
```

## Public status page

A public page where the institution and outsiders can confirm the relay is running helps build trust. Either of the two architectures below works.

### Option A, Nginx and Onionoo

- Nginx serves an HTTPS status page
- The page pulls public data for your own fingerprint from the [Tor Onionoo API](https://metrics.torproject.org/onionoo.html): traffic, flags, uptime
- Only public information is shown, and no internal endpoint is exposed

Option A is the recommended one. The architecture is simple, all data comes from a public API on the client side, and no internal service is involved. The trade-off is less flexible charting.

### Option B, MetricsPort, Prometheus, and Grafana

Option B is for when you need full observability:

- Enable `MetricsPort 127.0.0.1:9035` locally, **never externally**
- Scrape `/metrics` with Prometheus on the host or the internal network
- Build dashboards in Grafana
- Only Grafana may face outward, and **only with**:
    1. Read-only accounts with strong passwords or single sign-on
    2. HTTPS
    3. Dashboards containing nothing sensitive
    4. Prometheus **not** exposed
    5. MetricsPort **never** exposed

### Nginx and TLS configuration

- `certbot --nginx` for issuance and renewal
- TLS 1.2 and 1.3 only, weak ciphers disabled
- HSTS, `X-Content-Type-Options: nosniff`, and `Content-Security-Policy`
- `X-Robots-Tag: noindex, nofollow` to stay out of search indexes
- `/.well-known/acme-challenge/` over port 80, everything else on 80 redirected 301 to 443

## Monitoring, logging, and incident response

### Logs

- `journald` persistent, forwarded through `rsyslog` where required
- Separate log files for Nginx and Tor, rotated with `logrotate`
- Tor at `Log notice`, avoiding sensitive detail
- Raise the level temporarily during an incident and restore it afterwards

### Host observability

- `node_exporter` bound to `127.0.0.1:9100`
- Local Prometheus scraping, Grafana displaying, **read-only if exposed**

### Change auditing

- `auditd` recording changes to `/etc/tor/torrc` and `/var/lib/tor/keys/`
- AIDE comparing periodically, with results emailed to the operations address

### Backups and key protection

- Offline or off-site copies of `torrc` and `/var/lib/tor/keys/`
- Losing the identity key means the relay rejoins the network under a new identity, and its accumulated stability record does not carry over

### Incident runbook

On an alert, work through these steps in order:

1. **Triage**:
    ```bash
    sudo ss -tnlp | egrep ':22|:80|:443|:9001|:9035'
    sudo journalctl -u tor@default -n 200
    sudo ufw status numbered
    ```
2. **Stop the service**:
    ```bash
    sudo systemctl stop tor@default
    ```
    Preserve complete snapshots of `/var/log` and `/var/lib/tor/`
3. **Internal notification**: a preliminary incident report within 30 minutes, covering impact, cause, action taken, and expected recovery time
4. **Suspected compromise**: preserve evidence, isolate the host, and rebuild. Unless a compromise can be ruled out, treat the old identity keys as compromised: generate a new relay identity instead of restoring the backup, and report to `bad-relays@lists.torproject.org` (see [The October 2026 Tor Exit Relay Compromise and Operator Security Checks](/articles/tor-exit-ssh-interception/) for checks and response)

**Conditions for taking it offline**: impact on campus networks, a security anomaly, or a request from the institution or the supervising professor.

## Acceptance and connectivity testing

1. **Configuration check**:
    ```bash
    sudo -u debian-tor tor --verify-config
    ```
2. **ORPort reachability**:
    ```bash
    # From another host outside the campus
    nmap -p 9001 <public IP>
    # or
    telnet <public IP> 9001
    ```
    A reachability warning about the ORPort in the Tor log usually means the firewall rule or the external exception has not taken effect yet
3. **Relay confirmation**: about three hours after starting the relay, look up its fingerprint in [Tor Metrics Relay Search](https://metrics.torproject.org/rs.html)

## IPv6 configuration (optional)

To support IPv6, request an IPv6 address from the IT centre, then add to `torrc`:

```bash
ORPort [<your IPv6>]:9001
```

Allow the corresponding IPv6 traffic in UFW as well. IPv6 is optional, but it adds noticeably to the diversity of the Tor network and is worth asking the institution for.

## Handover and operation after graduation

Operators graduate, and that is the largest difference between a campus relay and a personal one. Prepare for handover from the day the relay goes live:

- **Shared `ContactInfo` mailbox**: a society, project, or team address rather than a personal one
- **At least two key backups**: one with the operator, one in the supervising professor's laboratory
- **Handover checklist**: `torrc`, UFW rules, SSH keys, CDN and monitoring accounts, and the password for the `ContactInfo` mailbox
- **Early search for a successor**: settle who takes over a semester before graduation
- **Handover document**: the machine's history, problems already encountered, and the agreed operational schedule

!!! tip "After the relay goes live"

    - **Report your case**: get in touch through the channels on the [Services](/services/) page, and we will add your case to "Done so far" on the [Tor Relays on Campus Track](/join/relay-on-campus/), so institutions that join later have more to work from
    - **Ongoing operation**: the [Tor Relay Setup Guide](/join/setup-tor-relay/) covers monitoring with nyx, and its common questions cover software updates and how guard relays are selected
    - **Other ways to contribute**: running a [Tor Snowflake](docs:tools/tor-snowflake/) proxy alongside it helps users in censored regions reach Tor

## Related reading

- [Tor Relay Setup Guide](/join/setup-tor-relay/): the basic installation for a personal or home setup
- [Campus Tor Relay Proposal Template](/join/relay-on-campus/proposal/): the proposal document for your institution
- [Campus Tor Relay FAQ for University Administrators and Legal Counsel](/join/relay-on-campus/faq/): common institutional concerns and answers
- [Tor Relays on Campus Track](/join/relay-on-campus/): the community's entry point for campus relays
- [Tor Project relay operator guides](https://community.torproject.org/relay/): the official documentation
- [Relay post-install and good practices](https://community.torproject.org/relay/setup/post-install/): what to check once the relay is running

## Sources and acknowledgements

The original design documentation and operational experience behind this page come from community member **NZ (En-Li Su)**, based on the deployment at National Taiwan Normal University. NZ agreed to release the original material under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

If a step here does not fit your institution, or you have details worth adding, let us know through the channels on the [Services](/services/) page. We will keep this page updated.
