---
title: Onion Service Setup Guide
description: A v3 onion service set up the way the Tor Project documents it, with nginx routing, subdomains, permissions, logs, troubleshooting and post-launch operations, plus how vanity addresses are generated and what they cannot prove.
---

An onion service lets people reach your server over Tor without the server's IP being public and without registering a domain with any certificate authority. Both ends of the connection stay inside the Tor network, and Tor handles the encryption.

!!! info "Differences from Relays and Bridges"

    Running a [Tor relay](/join/setup-tor-relay/), a [WebTunnel bridge](/join/setup-tor-webtunnel/), or [Snowflake](docs:tools/tor-snowflake/) **contributes bandwidth to the Tor network** by carrying other people's traffic.

    An onion service **uses Tor to host your own site**. It serves only your content, carries nobody else's traffic, and adds nothing to the network's capacity. The risks, the legal position, and the operational burden all differ between the two.

For how onion services are designed, how they compare with IPFS, and how anoni.net's docs site runs its three-track deployment, see [Decentralized Website Publishing](/articles/dweb-ipfs-onion/). If you only want to share files or put up a throwaway site, [OnionShare](docs:tools/onionshare/) costs less than running your own service.

## Prerequisites

- A server you manage yourself, Linux assumed
- `tor` installed. Check with `tor --version`; distribution packages generally support v3
- A web service reachable from `127.0.0.1`

### Web Service Listening Address

```bash
sudo ss -ltnp | grep -E 'nginx|apache|caddy'
```

When the `Local Address` column shows `127.0.0.1:80`, only the local machine can connect. `0.0.0.0:80` or `*:80` means the service is open to the whole internet.

Either works with an onion service. To keep a clearnet version of the site, leave it listening publicly, since Tor can still reach `127.0.0.1`. Only if the server should be invisible from clearnet do you need to rebind the service to `127.0.0.1` and close the public port.

### Outbound Connections

Tor joins the network by connecting outward. Your firewall needs **no inbound rule** for an onion service. On a corporate network that restricts egress, though, Tor cannot reach the Tor network and none of the later steps will work; on internal networks this is usually the first problem to surface.

## 1. The Tor Project's Standard Setup

The configuration file is `/etc/tor/torrc`, and two lines are enough. The example from the [Tor Project's setup guide](https://community.torproject.org/onion-services/setup/):

```
HiddenServiceDir /var/lib/tor/my_website/
HiddenServicePort 80 127.0.0.1:80
```

`HiddenServiceDir` is where Tor keeps the service's identity. In `HiddenServicePort`, the first number is the port exposed on the onion address, and what follows is the address and port your backend actually listens on.

One `torrc` can hold several services, each with its own onion address:

```
HiddenServiceDir /var/lib/tor/site-a/
HiddenServicePort 80 127.0.0.1:8080

HiddenServiceDir /var/lib/tor/site-b/
HiddenServicePort 80 127.0.0.1:8081
```

Each `HiddenServicePort` line belongs to the nearest `HiddenServiceDir` above it.

### Directory Permissions

The official guide says only that the directory must be "readable/writeable by the user that will be running Tor", with no specific permission values. In practice the directory has to be `0700`, and Tor refuses to use it if the permissions are looser.

Packaged installs typically run as the `debian-tor` or `tor` user. To check which:

```bash
systemctl cat tor@default.service | grep -E 'User=|debian-tor'
ps -o user= -C tor
```

Setting and verifying the permissions:

```bash
sudo chown -R debian-tor:debian-tor /var/lib/tor/my_website
sudo chmod 0700 /var/lib/tor/my_website
sudo ls -ld /var/lib/tor/my_website
```

When Tor creates the directory itself (write `torrc` and restart), the permissions are already correct, and `chown` and `chmod` are only needed for a directory you created by hand.

If another program needs to read `hostname`, set `HiddenServiceDirGroupReadable 1` in `torrc` to let the group read the directory and the `hostname` file (the default is `0`). The key files do not become group-readable through it.

### Applying the Configuration

```bash
sudo tor --verify-config          # syntax check, leaves the running service alone
sudo systemctl restart tor@default
sudo systemctl status tor@default
```

!!! warning "The Two Tor Units on Debian and Ubuntu"

    The package provides both `tor.service` and `tor@default.service`. The one that actually runs is `tor@default.service`; `tor.service` is a shell that does nothing. Restarting only `tor.service` leaves the new configuration unapplied, and nothing on screen shows the difference.

    When in doubt, `systemctl list-units 'tor*'` shows which one is `running`.

### Log Locations

When Tor misbehaves, the cause is almost always in the log. Under systemd:

```bash
sudo journalctl -u tor@default -n 50 --no-pager
sudo journalctl -u tor@default -f          # follow new log lines
```

`torrc` can also write to a separate log file. The line is commented out by default:

```
Log notice file /var/log/tor/notices.log
```

First confirm that Tor has reached the Tor network. The log should contain this line:

```
Bootstrapped 100% (done): Done
```

Without it, Tor has not joined the network yet, usually because outbound traffic is blocked. No onion address will appear until it does, however correct `HiddenServiceDir` is.

### Onion Address and Keys

Once Tor starts cleanly, `HiddenServiceDir` holds these files:

| File | Contents |
|---|---|
| `hostname` | the 56-character v3 address plus `.onion` |
| `hs_ed25519_public_key` | public key |
| `hs_ed25519_secret_key` | **private key, unrecoverable if it leaks** |
| `authorized_clients/` | directory for access control, empty by default |

The directory is `0700` and the files are `0600`, all created by Tor. Only Tor's user can read them, so use `sudo` to see the address:

```bash
sudo cat /var/lib/tor/my_website/hostname
```

The remaining files are the service's keys. The official warning:

> The other files are your Onion Service keys, so it is imperative that these are kept private. If your keys leak, other people can impersonate your Onion Service, deeming it compromised, useless, and dangerous to visit.

The onion address is an encoding of the public key, with no revocation mechanism and no authority that can retire it for you, so a key leak has no remedy. The only response is to generate a new address and tell every reader, and in a censored environment telling them is often impossible.

!!! tip "Permission and Backup Checks"

    In the output of `sudo ls -la /var/lib/tor/my_website`, a directory shown as `drwx------`, files as `-rw-------`, and Tor's user as the owner is the normal state. Tor creates them that way, so nothing extra is needed.

    Back up the whole `HiddenServiceDir` directory, and protect the backup to the same standard as the server or better. In practice that means encrypting it, for instance in an encrypted password manager or with `gpg -c`. Ordinary cloud storage and code repositories are the wrong place for it.

## 2. nginx Routing

The onion service only forwards connections to the address and port you name. Routing from there is up to the nginx configuration.

On Debian and Ubuntu the convention is a file in `/etc/nginx/sites-available/` symlinked into `sites-enabled/`:

```bash
sudo nano /etc/nginx/sites-available/onion
sudo ln -s /etc/nginx/sites-available/onion /etc/nginx/sites-enabled/
sudo nginx -t                     # syntax check, always run this first
sudo systemctl reload nginx
```

The configuration itself:

```nginx
server {
    listen 127.0.0.1:80;
    server_name <your-address>.onion;

    root /var/www/site;
    index index.html;
}
```

Put the actual onion address in `server_name`. With only one server block on that `listen`, a wrong value is harmless. Once several server blocks share the same `listen` (for example the subdomains in section 3), any request that fails to match lands on nginx's default server and gets the wrong content or a placeholder page.

### Unix Socket Connections

When `HiddenServicePort` in `torrc` points at a `unix:` path, nginx has to listen on that same socket, and the backend stays off TCP entirely.

!!! danger "Permission Limits of `/run/tor/`"

    `/run/tor/` is Tor's runtime directory, created at startup by systemd as `debian-tor` (the unit's `ExecStartPre` reads `-o debian-tor -g debian-tor -d /run/tor`). nginx runs as `www-data` and cannot create a socket there.

Create a separate directory both can use:

```bash
sudo mkdir -p /run/onion
sudo chown www-data:debian-tor /run/onion
sudo chmod 0770 /run/onion
```

`/run` is a tmpfs and is wiped on reboot. To have the directory recreated after a reboot, add a tmpfiles rule:

```bash
echo 'd /run/onion 0770 www-data debian-tor -' | sudo tee /etc/tmpfiles.d/onion.conf
sudo systemd-tmpfiles --create
```

Point `torrc` and nginx at the same path:

```
HiddenServicePort 80 unix:/run/onion/site.sock
```

```nginx
server {
    listen unix:/run/onion/site.sock;
    server_name <your-address>.onion;

    root /var/www/site;
    index index.html;
}
```

nginx creates the socket and Tor is the side that connects, so Tor's user needs write access to it. The nginx `listen` directive has no parameter for the socket's owner, group, or mode, which leaves the containing directory as the only place to control access.

After reloading, check the result instead of assuming the defaults work:

```bash
ls -l /run/onion/site.sock
```

Too strict and Tor cannot connect. Too loose and any local user can reach your backend. Check both directions.

The `GroupWritable` and `WorldWritable` flags in `torrc` apply only to sockets Tor creates itself (such as `ControlSocket` and `SocksPort`) and have no effect on a socket nginx creates.

### The HTTPS Trade-off

A connection to an onion service is already end-to-end encrypted and authenticated, because the address is the public key. Wrapping it in TLS adds no cryptographic protection, so the default advice is to serve plain HTTP and let Tor handle encryption.

If an audit policy requires TLS everywhere, use an onion certificate from a public CA. The CA/Browser Forum passed an amendment in 2021 allowing DV certificates for v3 `.onion` addresses, and commercial CAs now sell them. Tor Browser once marked plain-HTTP `.onion` sites as not secure, but that was fixed in 2017 ([`#21321`](https://gitlab.torproject.org/tpo/applications/tor-browser/-/issues/21321)), so the address bar is no reason to add TLS.

### Common Configuration Mistakes

- **Hard-coded clearnet URLs in responses**: links, form actions, and redirects that point at your original domain take the visitor out of Tor on the first click, and the anonymity is gone at that moment
- **External resources**: images, fonts, and analytics loaded from clearnet make the visitor's browser connect out the same way
- **Referrer leakage**: links to clearnet sites send a `Referer` by default, which puts your `.onion` address in that site's logs. Add `add_header Referrer-Policy no-referrer;`, or `rel="noreferrer"` on the links
- **`Host` header checks**: some application frameworks reject any `Host` not on an allowlist, so the onion address has to be added there
- **`127.0.0.1` in the access log**: every connection arrives through the local Tor daemon, so the log always records the local address. That is normal and does not mean the log configuration is broken

## 3. Subdomain Handling

An onion address can carry subdomains with no DNS registration or configuration. Tor passes the full `Host` through to the backend, and nginx decides how to route it.

The onion address of the anoni.net docs site has exactly this shape:

```
docs.anoninetru5tflukgfaehun7q6khowgmymcff3gtk5oyesqazhmfxtyd.onion
└┬─┘ └─────────────────── the 56-character v3 address ───────────────┘
 └── subdomain, routed by nginx's server_name
```

One onion address can host several subdomains. The nginx configuration:

```nginx
server {
    listen 127.0.0.1:80;
    server_name docs.<your-address>.onion;
    root /var/www/docs;
}

server {
    listen 127.0.0.1:80;
    server_name <your-address>.onion;
    root /var/www/main;
}
```

`torrc` needs no extra configuration for subdomains. One `HiddenServiceDir` and one `HiddenServicePort` cover all of them.

## 4. Access Control

If the service is not meant to be open to everyone, use the access control built into v3 onion services, known as client authorization. Unauthorized connections are refused at the rendezvous stage and receive nothing at all, which is far more reliable than keeping the address quiet.

On the server side, authorized public keys go in `HiddenServiceDir/authorized_clients/`. On the client side, `ClientOnionAuthDir` in the client's own `torrc` points to a directory holding the private keys. Internal tools and mirrors meant only for specific partners both suit this approach.

Key generation and file formats are covered in the [Tor Project's client authorization guide](https://community.torproject.org/onion-services/advanced/client-auth/).

## 5. Vanity Addresses (Optional)

!!! info "An Optional Step"

    A vanity address only makes the opening characters easier to remember. It affects neither whether the service works nor how secure it is. On a first deployment, skip it and come back once the service runs properly.

By default the address is 56 random characters. To get a recognisable string at the front (such as `anoninet` for anoni.net), you generate keys repeatedly until one starts the way you want.

[mkp224o](https://github.com/cathugger/mkp224o) is the usual tool, and the [Tor Project's page on vanity addresses](https://community.torproject.org/onion-services/advanced/vanity-addresses/) is built around it.

Install the build dependencies listed in the mkp224o documentation:

```bash
sudo apt install gcc libc6-dev libsodium-dev make autoconf
```

Building and running it:

```bash
./autogen.sh
./configure
make
./mkp224o -d nekokeys neko
```

On AMD64, adding `--enable-amd64-51-30k` to `configure` improves throughput. On BSD, use `gmake` instead of `make`. The key directory it produces has the same layout as `HiddenServiceDir`; after moving it into place, set the owner and permissions as described in "Directory Permissions".

### Computational Cost

The mkp224o documentation estimates that a 6-character prefix "shouldn't take more than few tens of minutes", on the condition `if using batch mode` (details in its `OPTIMISATION.txt`). Seven characters "can take hours to days". The same documentation adds that the result "depends on pure luck", so no time is guaranteed.

Each additional character multiplies the search space by 32. The `anoninet` prefix anoni.net uses is 8 characters, 32 times harder than the 7 characters put at "hours to days".

### Character Set Limits

Onion addresses use base32, whose alphabet is `a` through `z` and `2` through `7`. The digits `0`, `1`, `8`, and `9` are not in it, so no prefix containing them can be generated. mkp224o checks for this and fails early.

### Vanity Addresses and Identity

Identity is where vanity addresses are most often misunderstood. The Tor Project's documentation:

> An attacker wishing to impersonate an existing onionsite by creating a fake version of it might use vanity addresses as an additional way to convince users that their address is the right one.

Anyone with ordinary computing resources can generate another address starting with `anoninet`. A matching prefix does not mean the same service; the prefix only improves readability and carries no verification weight.

Publish the full 56 characters, and when readers verify an address, they should compare all of it rather than the opening.

Everything past the prefix is still randomly generated, so security is unaffected, and a vanity address is no easier to attack than any other.

## 6. Pre-Launch Checks

Work through these six checks in order.

### 1. Tor Network Connection

```bash
sudo journalctl -u tor@default | grep -i bootstrapped | tail -1
```

The output should include `Bootstrapped 100% (done)`.

### 2. Onion Address

```bash
sudo cat /var/lib/tor/my_website/hostname
```

The output should be 56 characters plus `.onion`.

### 3. Local Backend Response

```bash
curl -sI http://127.0.0.1:80/ -H 'Host: <your-address>.onion' | head -1
```

The output should be `HTTP/1.1 200 OK`. Sending the `Host` header mimics the request Tor will actually forward and confirms that `server_name` matches.

### 4. Connection over Tor

Open the `.onion` address in Tor Browser. Without a graphical interface, use `torsocks`:

```bash
sudo apt install torsocks
torsocks curl -sI http://<your-address>.onion/ | head -1
```

!!! warning "The Gap Before Descriptor Publication"

    The service descriptor has to be published to the Tor network first, so failing to connect in the first few minutes after setup is normal. Wait a few minutes and try again before changing any configuration.

    Restarting Tor opens the same gap.

### 5. Outbound Requests

Read the page source and confirm that images, fonts, and scripts do not load from clearnet, then click through the main links and confirm none of them leave Tor.

### 6. Key Backup

See "Permission and Backup Checks" in section 1.

### The Onion-Location Header

With an `Onion-Location` header on the clearnet site, visitors using Tor Browser see a prompt to switch to the onion version:

```nginx
add_header Onion-Location http://<your-address>.onion$request_uri;
```

Per the official guidance, the header belongs on a **clearnet site served over HTTPS**. Setting it on the onion site itself has no effect.

## 7. Common Connection Problems

??? question "Tor Startup Failure"

    Check the log first: `sudo journalctl -u tor@default -n 50`.

    `Permissions on directory ... are too permissive` means the directory permissions are too loose. Run `sudo chmod 0700` on that directory.

    `Failed to parse/validate config` means a `torrc` syntax error, and `sudo tor --verify-config` identifies the line.

??? question "torrc Changes Not Taking Effect"

    Usually `tor.service` was restarted while `tor@default.service`, the unit that actually runs, was not. Confirm which one is running with `systemctl list-units 'tor*'`.

??? question "Normal Logs but No Connection"

    Rule things out in this order:

    1. Whether the log shows `Bootstrapped 100%`. If not, Tor cannot reach the Tor network; check the outbound firewall
    2. Whether `hostname` exists. If not, the `HiddenServiceDir` block has not taken effect
    3. Whether you just set this up or restarted. Descriptor publication takes time, so wait a few minutes
    4. Whether the backend answers locally (item 3 in section 6). If not, the problem lies with nginx, not Tor

??? question "Access Failures Despite Correct Permissions"

    On a non-default path, AppArmor or SELinux may be blocking access. The failure does not show up as a permission error, and `ls -l` looks normal.

    ```bash
    sudo journalctl -k | grep -i 'apparmor.*DENIED'
    sudo dmesg | grep -i denied
    ```

    If there is a match, moving the path back under `/var/lib/tor/` is the quickest fix. The systemd unit's own sandboxing (`ProtectSystem`, `ReadWritePaths`) can also block non-default paths, so check that as well.

??? question "nginx-Side Troubleshooting"

    ```bash
    sudo nginx -t
    sudo tail -50 /var/log/nginx/error.log
    ```

    With a Unix socket, use `ls -l /run/onion/site.sock` to confirm the socket file exists and Tor's user has write access.

??? question "Connection Failures After a Reboot"

    A socket directory under `/run` is wiped on reboot (`/run` is a tmpfs) and comes back only with a rule in `/etc/tmpfiles.d/` (see section 2).

    Also check the startup order of nginx and tor: nginx has to create the socket before Tor can connect.

## 8. Post-Launch Operations

### Failure Detection

A running Tor process does not mean the descriptor is still published on the network. The most direct check is connecting from outside on a schedule, for instance a cron job running `torsocks curl`.

### The Gap After Restarts

Every Tor restart republishes the descriptor, and the service is unreachable for a few minutes. That is not a fault.

### Latency

Connections pass through several relays, and round trips typically run from a few hundred milliseconds to over a second. Interactive applications (admin panels, live collaboration) feel noticeably slower over onion than over clearnet, while static content is less affected. Factor this in before deciding to put a given service on an onion address.

### Server Migration

The address is bound to the key, so moving the whole `HiddenServiceDir` to the new server with the right permissions keeps the address unchanged. For the same reason, backups of that directory need to be kept as secret material.

### Service Shutdown

Remove the two lines from `torrc` and restart. Once the address is gone, there is no way to tell visitors on the onion side what happened, so if readers depend on it, announce the change on the clearnet side first.

### Load Distribution Across Servers

When one onion address needs to be served by several machines, the Tor Project hosts [OnionBalance](https://gitlab.torproject.org/tpo/onion-services/onionbalance). The project was dormant between 2021 and 2025 and resumed releases in April 2025; the latest version is `0.2.4` (checked 2026-10). Check its recent activity before committing to it.

## 9. Caddy Setup

If your environment already runs Caddy, [Onion mirror with Caddy](https://flower.codes/2025/10/23/onion-mirror.html) is a walkthrough you can follow.

Caddy requests TLS certificates automatically by default, and that should be switched off for an onion service (the reason is in "The HTTPS Trade-off" in section 2). The rest of the flow matches this page, and only the routing syntax differs.

## Related Reading

- [Decentralized Website Publishing](/articles/dweb-ipfs-onion/): how onion services are designed, the trade-offs with IPFS, and how anoni.net's three-track deployment fits together
- [Pinning the Docs Site's IPFS Mirror](/join/pin-ipfs-mirror/): a different kind of censorship-resistant mirror, where help with pinning is welcome
- [Tor Relay Setup Guide](/join/setup-tor-relay/): contributing bandwidth to the Tor network, a different kind of task from this one
- [OnionShare](docs:tools/onionshare/): sharing files and hosting a site without operating a service yourself
