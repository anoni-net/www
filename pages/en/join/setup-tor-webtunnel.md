---
title: Tor WebTunnel Bridge Setup Guide
description: Setting up and operating a Tor WebTunnel bridge on a VPS, covering the domain, TLS certificate, nginx reverse proxy, Docker deployment, firewall, cover page, and incident handling.
---

WebTunnel wraps Tor traffic inside an ordinary HTTPS connection, so the traffic closely resembles web browsing and is hard for deep packet inspection (DPI) to single out. When a censorship system uses DPI to block protocols such as obfs4, whose signatures differ from HTTPS, WebTunnel usually still gets through, which makes it one of the most censorship-resistant kinds of Tor bridge available today.

This guide follows the Tor Project's Docker deployment, and adds two nginx hardening settings the official docs leave out, along with monitoring, the cover page, the firewall, and incident handling once the bridge is live.

!!! info "Bridges and Relays"

    There are three ways to contribute to the Tor network, each with a different barrier to entry and level of censorship resistance:

    - [Tor Snowflake](docs:tools/tor-snowflake/): a temporary bridge that runs in a browser tab, with the lowest barrier. Snowflake runs over WebRTC, whose handshake can be fingerprinted, and China has already blocked it.
    - WebTunnel (this guide): needs a VPS, a domain, and a TLS certificate, disguises itself as HTTPS, and is the hardest to block on heavily censored networks.
    - [Tor relays](/join/setup-tor-relay/): carry the Tor network's bandwidth and add to its diversity; a relay is not a bridge.

    A bridge, like a relay, never connects directly to the destination a user is heading for; the destination site receives the connection from a Tor exit node. The legal risk of operating a bridge is therefore on par with guard and middle nodes, and far lower than an exit node.

## The Case for More WebTunnel Bridges

Censors block the bridge IPs they already know about, so the more countries and network providers (ASNs) bridges are spread across, the more entry points censored users have. Taiwan, where we are based, has little outbound censorship and plenty of bandwidth, which makes it a good place to host bridges. WebTunnel also needs fewer resources than a relay: a VPS with 512MB to 1GB of RAM is enough, with lower cost and upkeep.

In 2026 Iran imposed several large-scale internet shutdowns during military operations, the second lasting nearly three months, from late February to late May. After the network reopened, traffic through our community's WebTunnel bridge rose sharply, as documented in [traffic through our WebTunnel bridge after Iran's blackout](/updates/2026/05/iran-blackout-webtunnel/). On networks with strict DPI filtering, a bridge disguised as HTTPS is often one of the few remaining ways to reach Tor.

## Prerequisites

- A VPS running Debian or Ubuntu with at least 512MB of RAM; 1GB is recommended to give the Tor process headroom.
- A domain or subdomain whose DNS you can edit.
- Port 443 open to the internet, since WebTunnel uses the standard HTTPS port to look like an ordinary site.
- A contact email, which will be public in the bridge's `ContactInfo`.

!!! tip "Domain and Operational Privacy"

    WebTunnel's disguise depends on the domain looking like an ordinary website:

    - Choose a domain or subdomain that doesn't obviously read as a Tor bridge.
    - Serve a harmless page at the root path (`/`), such as a personal homepage, a parked-domain page, or a simple blog, so anyone scanning finds an ordinary website.
    - In a low-risk setting like Taiwan, a subdomain of an existing domain is usually fine. For stronger operational privacy, consider a separate, anonymously registered domain.

Setup has two parts. First configure the domain, TLS certificate, and reverse proxy so the server looks like an ordinary HTTPS website, then run the bridge with Docker.

## Domain, TLS, and the nginx Reverse Proxy

### DNS Record

Add an A record to your domain's DNS pointing the domain or subdomain (for example `bridge.example.com`) at the VPS's public IP, and wait for DNS to propagate before moving on.

### TLS Certificate

WebTunnel needs a browser-trusted TLS certificate so the connection looks like it is reaching an ordinary HTTPS website. Let's Encrypt is the simplest option.

```bash
apt update
apt install certbot python3-certbot-nginx
certbot --nginx -d bridge.example.com
```

The certbot package installs a systemd timer for automatic renewal, which you can check with:

```bash
systemctl status certbot.timer
```

!!! info "Other Ways to Issue a Certificate"

    You can also issue the certificate with an ACME client such as `acme.sh`; see [Tor Project | WebTunnel Bridge](https://community.torproject.org/relay/setup/webtunnel/).

### nginx Reverse Proxy Configuration

The WebTunnel bridge listens locally on `127.0.0.1:15000`. nginx handles the public HTTPS and reverse-proxies a secret path through to the bridge. Use a random string as the secret path; the examples below use `$PATH` to stand in for it.

Add this `location` block to an existing or new vhost. The WebSocket headers are required:

```nginx
location = /$PATH {
    proxy_pass http://127.0.0.1:15000;
    proxy_http_version 1.1;
    ### WebSocket headers ###
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ### Proxy headers ###
    proxy_set_header Accept-Encoding "";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    add_header Front-End-Https on;
    proxy_redirect off;
    access_log off;
    error_log /dev/null;
}
```

!!! tip "Two Reverse-Proxy Hardening Settings"

    Neither of these adjustments is in the official docs. They make the secret path harder to probe and keep long-lived connections stable.

    **Probe protection for the secret path**

    By default, a plain request to the secret path without a WebSocket handshake is still forwarded to the bridge. The bridge's response may differ from the rest of the site and give the path away. One extra line makes nginx return a 404 for any request without an `Upgrade` header, so the secret path responds like any non-existent URL on the site:

    ```nginx
    location = /$PATH {
        # Only a real WebTunnel handshake gets through; plain probes get a 404
        if ($http_upgrade = "") { return 404; }
        proxy_pass http://127.0.0.1:15000;
        # ...rest of the config as above
    }
    ```

    A WebTunnel connection always carries an `Upgrade` header, so this line won't block legitimate bridge clients.

    **Timeouts for long-lived connections**

    nginx's `proxy_read_timeout` defaults to 60 seconds, so a connection with no data for 60 seconds is dropped, and long-lived Tor circuits disconnect for no apparent reason. Raise the timeouts in the `location` block and enable TCP keepalive:

    ```nginx
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        proxy_socket_keepalive on;
    ```

Keep the root `location /` serving an ordinary web page, so the server as a whole looks like a normal site and only a Tor client that knows the secret path reaches the bridge. After editing, test the config and reload:

```bash
nginx -t && systemctl reload nginx
```

## Docker Deployment of the WebTunnel Bridge

### Docker Installation

```bash
apt install curl sudo
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

### The `.env` File

Set `URL` to your domain plus the secret path (the same `$PATH` as in the nginx config) and `OPERATOR_EMAIL` to your contact address, then run:

```bash
truncate --size 0 .env
echo "URL=https://bridge.example.com/your-secret-path" >> .env
echo "OPERATOR_EMAIL=your@email.org" >> .env
echo "BRIDGE_NICKNAME=WTBr$(cat /dev/urandom | tr -cd 'qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAQWERTUIOP0987654321'|head -c 10)" >> .env
echo "GENEDORPORT=4$(cat /dev/urandom | tr -cd '0987654321'|head -c 4)" >> .env
```

### The docker-compose File

```bash
curl https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/webtunnel/-/raw/main/release/container/docker-compose.yml?inline=false > docker-compose.yml
```

This compose file enables automatic updates by default, so the bridge updates to new versions automatically. Then start the container:

```bash
docker compose up -d
```

### Bridge Line and Verification

```bash
docker compose exec webtunnel-bridge get-bridge-line.sh
```

Paste the bridge line it prints into Tor Browser's bridge settings to test the connection.

!!! warning "Alternative Command"

    On newer container versions the container may be named `webtunnelBridge`, and the command above will fail. Use this instead:

    ```bash
    docker exec webtunnelBridge get-bridge-line.sh
    ```

The IP in the bridge line (especially the IPv6 one) is a randomly generated placeholder that is never used; the pluggable transport spec simply requires an IP in that position. Clients connect through your domain and secret path. By default, the bridge is distributed automatically to users who need it through [bridges.torproject.org](https://bridges.torproject.org/).

## Advanced Operations

### Firewall

WebTunnel only needs 443 (HTTPS) open to the internet; keep SSH as your management needs require. The bridge's `15000` listener is bound to `127.0.0.1` and should not be exposed.

```bash
ufw allow 443/tcp
ufw allow OpenSSH
ufw enable
ufw status
```

### Cover Page Design

The page at the root path is part of the disguise. Serve a static page with real content that won't raise suspicion, such as a personal portfolio, technical notes, or a parked-domain page. A blank page or the default nginx welcome page stands out.

### Monitoring and Health Checks

- Container status and logs:

    ```bash
    docker compose ps
    docker compose logs -f
    ```

- TLS certificate validity and renewal status: `systemctl status certbot.timer`.
- A few hours after the bridge goes live, you can check through the [bridges.torproject.org](https://bridges.torproject.org/) flow or in Tor Browser whether it is being distributed and is reachable.

### Software Updates

The compose file keeps the bridge itself updated. System-level Docker, nginx, and certbot still need a periodic `apt update && apt upgrade`, and TLS renewal is left to the certbot timer.

### Incident Runbook

- **Bridge unreachable**: check `docker compose logs` first, then confirm that the nginx secret path matches the `URL` path in `.env`, that the TLS certificate hasn't expired, and that 443 is open.
- **Certificate expired**: run `certbot renew`, then `systemctl reload nginx`.
- **Abuse reports or legal inquiries**: a bridge plays a role close to guard and middle nodes and never connects to the destination. Explain the role of a Tor bridge in your reply and refer to the [EFF Tor relay operator legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/).
- **Taking the bridge offline**: `docker compose down` stops the bridge; then remove the nginx `location` block and reload.

## FAQ

??? question "WebTunnel Compared with Snowflake and obfs4"

    All three are bridges for getting around censorship to reach Tor. Snowflake runs over WebRTC (the real-time connection technology browsers use for video calls) and runs from a browser, but it is easier to detect. obfs4 turns traffic into random noise, but DPI can still recognize it as not-HTTPS and block it. WebTunnel wraps traffic inside a genuine HTTPS connection, so blocking it means blocking large numbers of legitimate sites along with it, which makes it most effective on networks with strict DPI filtering.

??? question "Legal Risk of Operating a Bridge"

    Like guard and middle nodes, a bridge never connects to the final destination; the destination site receives the connection from a Tor exit node. In Taiwan, where the internet is relatively free, operating these nodes is currently allowed, and the risk is far lower than for an exit node. If you receive an inquiry, refer to the [EFF Tor relay operator legal FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/).

??? question "Server Requirements"

    A small VPS with 512MB of RAM can run a bridge, but 1GB is recommended, since the Tor process itself can use close to 1GiB of memory. CPU and bandwidth needs are both modest.

??? question "Running a Bridge on a Home Network"

    A home network works if you have a static public IP, can forward port 443 on your router, and your ISP permits this kind of traffic. A dynamic IP makes the bridge address unstable, so a VPS is usually simpler and more reliable.

??? question "Alternatives to Docker"

    You can also build and run the Go binary from source; see [Tor Project | Compile and run WebTunnel from source](https://community.torproject.org/relay/setup/webtunnel/source/). In most cases Docker is the simplest option.

## Related Reading

- [Why networked freedom matters](docs:basics/internet-freedom/)
- [What Is Tor?](docs:tools/what-is-tor/)
- [Tor Snowflake](docs:tools/tor-snowflake/): a temporary bridge that runs in a browser tab

## Other Ways to Get Involved

- [Tor Relay Setup Guide](/join/setup-tor-relay/): legal, technical, and administrative considerations for running a relay in Taiwan
- [Tor Relays on Campus Track](/join/relay-on-campus/): the programme and case studies for running Tor relays at universities
- [Tor Relay Watch](/projects/pulse/): relay counts, bandwidth, and versions in Taiwan and nearby regions

## Official References

- [Tor Project | WebTunnel Bridge](https://community.torproject.org/relay/setup/webtunnel/): the main doc for domain, TLS, and nginx setup
- [Tor Project | WebTunnel Docker setup](https://community.torproject.org/relay/setup/webtunnel/docker/): Docker deployment
- [Tor Project | Compile and run WebTunnel from source](https://community.torproject.org/relay/setup/webtunnel/source/): building from source
- [Introducing WebTunnel](https://blog.torproject.org/introducing-webtunnel-evading-censorship-by-hiding-in-plain-sight/): the design rationale behind WebTunnel
