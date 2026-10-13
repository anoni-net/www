---
title: Pinning the Docs Site's IPFS Mirror
description: Pinning the anoni.net docs site's IPFS mirror with an always-on IPFS node and a scheduled script, covering installation, scheduling, verification and peering on Windows, Linux, macOS and Docker.
---

Alongside the main site, the anoni.net docs site is published as an IPFS mirror, so the docs stay readable when the main site is blocked or taken down. Content on IPFS only stays available while some node pins it. A check of the network in August 2026 found exactly one provider, the community's own node, which makes the whole mirror a single point of failure. Every extra node that pins it adds one more complete copy to the network, and the docs survive if the community's machine is suspended or fails.

To help, run an always-on IPFS node with a scheduled script that pins the latest version. The setup works on Windows, Linux and macOS, with or without Docker.

!!! tip "Requirements"

    - A computer that stays on most of the day with a network connection (a desktop, a home server or a small always-on box)
    - IPFS installed (covered below)
    - A scheduled script that pins the latest version every few hours

    The first fetch is roughly 240 MB and the only source right now is the community node, so set up [a steady connection to the community node](#peering) from the start; the initial sync goes much more smoothly that way. If you can't keep a node running, the last section covers pinning through a service instead.

## CIDs, IPNS and pins

The schedule is needed because the CID changes with the content. The full design of IPFS is covered in [decentralized website publishing](/articles/dweb-ipfs-onion/); what follows is only what pinning depends on.

- IPFS hashes a file's content into a CID (Content Identifier), and the CID is the content's address on IPFS. Identical content always has the same CID.
- Change the content and the CID changes with it. Every update and republish of the docs site produces a new CID.
- IPNS (InterPlanetary Name System) is a fixed name that points to the current CID. The docs site's IPNS name is the `k51…` string below.
- A pin keeps the content of one specific CID available. Pins are bound to a CID and do not follow IPNS, so once the docs site publishes a new version, what you pinned last time is still the old CID.

The pin script resolves IPNS to the current CID, pins it, then drops the old version. Because the CID changes on every publish, the script has to run on a schedule.

### Three lookalike identifiers

IPFS has three identifiers that look alike and do different jobs. Paste one into the wrong field and the tool rejects it outright.

| Identifier | Starts with | Changes? | Used for |
|---|---|---|---|
| CID | `bafybei…` | New one every publish | Pointing at one specific version |
| IPNS name | `k51qzi…` | Fixed | Getting the latest version, which is what pinning uses |
| Peer ID | `12D3KooW…` | Fixed | Pointing at one specific node |

Pinning the docs site only needs the IPNS name. The Peer ID is only used when setting up [a steady connection to the community node](#peering).

## Scheduled pinning through IPNS

IPNS is the shared sync point between nodes. When the docs site publishes a new version it only updates IPNS, and nobody has to send a notice. Your node resolves IPNS every few hours and pins the new version when the CID has changed, with no manual coordination.

!!! info "The docs site's IPFS coordinates"

    These are public values you can use directly.

    - IPNS name: `k51qzi5uqu5dlfm2jj0f70ex3r3babmwy8qh071inwknttr7wqa3uhdwvlmrmw`
    - Node Peer ID: `12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9` (only needed for peering)
    - DNSLink: `_dnslink.anoni.net` points at the same IPNS name, so any DNSLink-capable gateway serves the same content
    - Browser: the community's own [IPFS gateway](https://ipfs.anoni.net/) (`ipfs.anoni.net`). The old address `anoni-net.ipns.dweb.link` stopped operating on 30 September 2026; see [IPFS maintenance changes after September 2026](#ipfs-maintenance-2026)

Each run resolves IPNS to the current CID, pins the new CID, unpins the previous one and reclaims space. The old version is dropped only after the new one has pinned successfully, and if resolving or fetching fails, the copy already on your node stays as it is.

## An always-on IPFS node

Pinning needs a continuously running IPFS daemon on your machine to fetch the full content. Pick one of the setups below.

=== "Linux / macOS"

    Install [kubo](https://docs.ipfs.tech/install/command-line/), the official IPFS command-line implementation. On macOS you can use Homebrew:

    ```bash
    brew install kubo
    ```

    The Homebrew formula was renamed from `ipfs` to `kubo`. The old name still installs it, but the service commands below need `kubo`. Both Intel and Apple Silicon are supported.

    On Linux, download the kubo build for your architecture following the [official guide](https://docs.ipfs.tech/install/command-line/). Then initialize and start the daemon:

    ```bash
    ipfs init          # first time only
    ipfs daemon
    ```

    To keep the daemon running long-term, use a systemd user service on Linux. On macOS the Homebrew formula ships a service definition, so this command keeps it running and starts it at login:

    ```bash
    brew services start kubo
    ```

    For a quick test, running `ipfs daemon` in the background is enough.

=== "Windows"

    The simplest option is [IPFS Desktop](https://docs.ipfs.tech/install/ipfs-desktop/). It bundles kubo and stays in the system tray after you log in, with the daemon running. IPFS Desktop has had no dedicated maintainer since 30 September 2026 (see [IPFS maintenance changes after September 2026](#ipfs-maintenance-2026)), so a standalone kubo install or Docker removes that uncertainty on Windows.

    After installing, make sure `ipfs` can be called from the command line. A standalone kubo install needs `ipfs.exe` added to your PATH. With IPFS Desktop, if PATH can't find `ipfs`, use the full path in the script instead.

=== "Docker"

    Run kubo with a `docker-compose.yml`, naming the container `ipfs_host`:

    ```yaml
    services:
      ipfs_host:
        image: ipfs/kubo:latest
        restart: always
        volumes:
          - ./ipfs-data:/data/ipfs
        ports:
          - "4001:4001"   # swarm; exposing it helps reach other nodes
    ```

    Start it:

    ```bash
    docker compose up -d
    ```

    From here on, IPFS commands run through the container. Set this environment variable and the pin script picks it up automatically:

    ```bash
    export IPFS_CMD="docker exec ipfs_host ipfs"
    ```

## The pin script

The pin script resolves IPNS, pins the new version and unpins the old one. The IPNS name is hard-coded in it, so there is nothing to edit. Docker users need `IPFS_CMD` set from the previous step. The script will run on your machine on a schedule, so read the source on GitHub before you run it.

### `anoni-pin.sh` (Linux, macOS, Docker)

[<i data-icon="download"></i> Download anoni-pin.sh](https://raw.githubusercontent.com/anoni-net/docs/main/docs/_scripts/anoni-pin.sh){ .btn } [<i data-icon="octicons-mark-github-24"></i> View source on GitHub](https://github.com/anoni-net/docs/blob/main/docs/_scripts/anoni-pin.sh){ .btn }

Save it, make it executable and run it once by hand to check it works:

```bash
chmod +x anoni-pin.sh
./anoni-pin.sh          # run once by hand to check it works
```

### `anoni-pin.ps1` (Windows)

[<i data-icon="download"></i> Download anoni-pin.ps1](https://raw.githubusercontent.com/anoni-net/docs/main/docs/_scripts/anoni-pin.ps1){ .btn } [<i data-icon="octicons-mark-github-24"></i> View source on GitHub](https://github.com/anoni-net/docs/blob/main/docs/_scripts/anoni-pin.ps1){ .btn }

Run it once by hand to check it works. PowerShell blocks scripts by default, and `-ExecutionPolicy Bypass` allows this one run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\anoni-pin.ps1
```

## Scheduling

The docs site doesn't update often, so every 6 hours is enough; shorten the interval if you want to pick up new versions sooner.

=== "Linux / macOS"

    Use cron. Edit your crontab:

    ```bash
    crontab -e
    ```

    Add this line to run every 6 hours and write output to a log:

    ```bash
    0 */6 * * * /path/to/anoni-pin.sh >> $HOME/.anoni-pin/log 2>&1
    ```

    To catch up on runs missed while the machine was off, use a systemd timer with `Persistent=true` instead.

=== "Windows"

    Use Task Scheduler. Creating the task from the command line is quickest; this one runs every 6 hours:

    ```powershell
    schtasks /Create /TN "anoni-ipfs-pin" `
      /TR "powershell -NoProfile -ExecutionPolicy Bypass -File C:\Tools\anoni-pin.ps1" `
      /SC HOURLY /MO 6 /RL LIMITED
    ```

    Replace `C:\Tools\anoni-pin.ps1` with wherever you saved it. You can also create it in the Task Scheduler GUI: set "Program/script" to `powershell` and "Add arguments" to `-NoProfile -ExecutionPolicy Bypass -File your-path`.

=== "Docker"

    Schedule it according to your host OS (cron on Linux and macOS, Task Scheduler on Windows; see the two tabs above). The only difference is that `IPFS_CMD` has to be set before the script runs, for example with a small wrapper:

    ```bash
    #!/usr/bin/env bash
    export IPFS_CMD="docker exec ipfs_host ipfs"
    exec /path/to/anoni-pin.sh
    ```

    Point cron at the wrapper instead of the script.

## Verifying the pin

Resolve the current CID, then check that it appears in the pin list:

```bash
CID=$(ipfs name resolve --nocache /ipns/k51qzi5uqu5dlfm2jj0f70ex3r3babmwy8qh071inwknttr7wqa3uhdwvlmrmw)
ipfs pin ls --type=recursive | grep "${CID#/ipfs/}"
```

You can also open `http://127.0.0.1:8080${CID}/` on your local gateway; if the content renders, the pin worked. Docker users replace `ipfs` above with `docker exec ipfs_host ipfs` and rely on the commands, since the compose example above does not publish port 8080.

## A steady connection to the community node { #peering }

Pinning only needs the IPNS name, and the content is located through the DHT. Fetching the full mirror for the first time can drag on when DHT lookups are slow or come back empty. Configuring kubo's peering keeps a fixed connection between your node and the source node.

Edit `~/.ipfs/config` and add a `Peering` block at the top level:

```json
"Peering": {
  "Peers": [
    { "ID": "12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9" }
  ]
}
```

`Addrs` can be omitted, and kubo looks the addresses up in the DHT. Restart the daemon to apply the change. Docker users edit `./ipfs-data/config` instead, then run `docker compose restart`.

Check whether it connected:

```bash
ipfs swarm peers | grep 12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9
```

Peering here is one-way: the community node has no matching entry, so keeping the connection alive is up to your node. The [kubo config docs](https://github.com/ipfs/kubo/blob/master/docs/config.md#peering) note that one-way peering consumes connection resources on the other node, and that the load concentrates on one machine as the number of mirrors grows. Right now there is exactly one provider and the whole 240 MB first fetch comes from it, so turn peering on from the start. Once more nodes pin the mirror and the source is no longer a single machine, you can remove the setting.

## IPFS maintenance changes after September 2026 { #ipfs-maintenance-2026 }

Interplanetary Shipyard maintained most of the major IPFS software for the past few years. After Protocol Labs stopped funding it, Shipyard [ended its IPFS work on 30 September 2026](https://ipshipyard.com/blog/2026-the-end-of-ipfs-at-shipyard/). Everything on this page still works, with three changes.

- **Software maintenance**: kubo, Helia, Boxo, IPFS Desktop and IPFS Companion no longer have a dedicated maintainer, and the IPFS Foundation has moved to grants for individual maintainers. The software keeps working, but security updates will arrive more slowly, so check the release date before you install.
- **Public gateways and bootstrap nodes**: ipfs.io, dweb.link and the IPFS bootstrap nodes stopped operating on the same day. Since kubo 0.38 the default for `Bootstrap` is `auto`, and the expanded list contains those nodes.
- **The browsing address for this mirror**: the old `anoni-net.ipns.dweb.link` belonged to dweb.link and has been replaced by the community's own [IPFS gateway](https://ipfs.anoni.net/) (`ipfs.anoni.net`). Both serve the same IPNS name through the DNSLink record. The pin script works from the IPNS name and is unaffected by the gateway.

These commands show which bootstrap nodes your node currently has and how many peers it is connected to:

```bash
ipfs config Bootstrap --expand-auto
ipfs swarm peers | wc -l
```

With the nodes behind `auto` shut down, a freshly installed node may fail to join the DHT. The most direct fix is to set the community node as a fixed peer (see [a steady connection to the community node](#peering)); `Peering` only needs the Peer ID.

## Maintenance notes

- **Version updates**: when the docs site changes its CID, the next scheduled run pins the new version and drops the old one, with nothing for you to do.
- **Incremental fetches**: while the new version is being pinned, the old version's blocks are still on your node, so IPFS only fetches the blocks that differ. The first sync pulls the whole mirror; ordinary content updates after that are usually a few MB. Changes to the navigation or the theme are the exception, since every page's HTML is rewritten and the difference comes close to half the mirror.
- **Disk use**: after unpinning the old version the script runs a garbage collection, so only the latest version takes space. A full mirror is about 240 MB (measured August 2026).
- **Stopping**: unpin the current version and remove the schedule. Other nodes are not affected.
- **Privacy and risk**: what you pin is public documentation, so there is no privacy concern. The risk of offering IPFS pinning differs by jurisdiction; the limits are covered under "Known limits and risks" in [decentralized website publishing](/articles/dweb-ipfs-onion/).

## Pinning services as an alternative

If you'd rather not maintain a daemon and a schedule, use a pinning service such as [Pinata](https://www.pinata.cloud/) or [Storacha](https://storacha.network/). To pin by hand, paste the current CID into the service's interface; to automate it, script the service's API on a schedule. The logic is the same as this page's script: resolve IPNS to a CID, then hand the CID to the service.

The trade-off is that the mirror's survival then depends on a third-party provider. That works as a backup, but running your own node remains the most direct way to decentralize.

## Related reading

- [Decentralized Website Publishing](/articles/dweb-ipfs-onion/): the design of IPFS and onion services, and how the docs site is actually deployed
- [Onion Service Setup Guide](/join/setup-onion-service/): another way to run a censorship-resistant mirror
- [Tor Relay Setup Guide](/join/setup-tor-relay/): adding relays to the Tor network with your own machine and bandwidth
