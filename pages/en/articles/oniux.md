---
title: oniux and Tor Isolation with Linux Namespaces
description: A guide to the Tor Project's oniux, which uses Linux namespaces to force any program's traffic through Tor, with installation details checked in October 2026, its relationship to onionmasq, and our view on where it fits.
date: 2025-05-16
---

Routing a program through Tor usually depends on the program honouring a proxy setting. One misconfigured proxy, or one system call that skips the SOCKS layer, and traffic leaves the machine in the clear. oniux removes that dependency on Linux by putting the program in a network namespace where Tor is the only way out.

[![oniux announcement image](https://blog.torproject.org/introducing-oniux-tor-isolation-using-linux-namespaces/lead.webp){ .shot }](https://blog.torproject.org/introducing-oniux-tor-isolation-using-linux-namespaces/)

## The Original Announcement

The Tor Project introduced oniux on its blog on 14 May 2025, in [Introducing oniux: Kernel-level Tor isolation for any Linux app](https://blog.torproject.org/introducing-oniux-tor-isolation-using-linux-namespaces/). oniux is a small command-line tool written in Rust and built on Arti (the Rust implementation of Tor) and onionmasq. This page summarises the post and adds our own notes; the Chinese versions of this page carry a full translation.

## How oniux Isolates a Program

Linux namespaces, added to the kernel around 2000, give a process its own view of resources that are otherwise shared system-wide, such as network interfaces, mounts, the process list and user IDs. Docker builds its isolation on the same feature. oniux places the target program in a network namespace that has no access to the host's interfaces (such as `eth0`) and contains a single custom interface, `onion0`, whose traffic goes into Tor. The guarantee rests on the kernel rather than on the program cooperating.

The sequence, as described in the post and the project README:

1. oniux calls `clone(2)` to spawn a child process in new network, mount, PID and user namespaces.
2. The child mounts its own `/proc` and maps UIDs and GIDs to those of the parent.
3. It bind-mounts a temporary file over `/etc/resolv.conf`, so name resolution inside the namespace goes through Tor.
4. It uses onionmasq to create the `onion0` TUN interface and configures it with `rtnetlink(7)`, for example assigning IP addresses.
5. It passes the TUN file descriptor to the waiting parent over a Unix domain socket.
6. It drops the capabilities it held as root inside the user namespace, then runs the user's command.

## Comparison with torsocks

torsocks, the long-standing alternative, overrides network-related libc functions and redirects them to Tor's SOCKS proxy. Anything that makes system calls without going through a dynamically linked libc escapes it, whether by accident or by design; statically linked binaries and programs from the Zig ecosystem are the examples the post gives. The post's comparison:

| oniux | torsocks |
| --- | --- |
| Standalone application | Requires a running Tor daemon |
| Linux namespaces | `ld.so` preload hack |
| Works with any application | Only applications making system calls through libc |
| A malicious application cannot leak | A malicious application can leak with a raw assembly system call |
| Linux only | Cross-platform |
| New and experimental | More than 15 years of use |
| Arti as its engine | C Tor as its engine |
| Written in Rust | Written in C |

## Installation, Checked October 2026

The post installed a pinned `v0.4.0` tag. oniux now ships roughly monthly, shortly after each Arti release. When we checked in October 2026, the latest tag on the [GitLab project](https://gitlab.torproject.org/tpo/core/oniux/-/tags) was `v0.13.0` (9 September 2026), and building it needs Rust 1.91 or later.

Alpine Linux, Nix and Void Linux package oniux, and [Repology](https://repology.org/project/oniux/versions) tracks other distributions. The `oniux` crate on crates.io is a `0.0.0` placeholder, so install from the Tor Project's GitLab instead. With a current Rust toolchain from rustup:

```bash
$ cargo install --locked --git https://gitlab.torproject.org/tpo/core/oniux --tag v0.13.0 oniux
```

Replace the tag with the newest one when a release comes out. The project's own page on the [Arti website](https://arti.torproject.org/related/oniux) still showed `v0.10.0` at the time of our check, so the GitLab tags are the more reliable reference. oniux needs the `tun` kernel module; if it fails with `File not found`, run `modprobe tun` and try again.

Usage is the original command prefixed with `oniux`, for example `oniux curl https://icanhazip.com`, `oniux bash` for a whole shell, or a graphical application such as `oniux hexchat`.

## Known Limitations

The post labels oniux experimental: Arti and onionmasq are young, and torsocks has a much longer record. The README adds a limit of network namespaces themselves. A program inside oniux can still talk to processes outside it over inter-process channels such as Unix domain sockets, and those outside processes are not isolated. The README's example is Emacs in server mode: if the server runs outside oniux, every client that connects to it leaks network connections, whether or not the clients run under oniux. Blocking IPC entirely would make oniux no different from a virtual machine or a full container.

## Relationship with onionmasq

The `onion0` interface comes from [onionmasq](https://gitlab.torproject.org/tpo/core/onionmasq), a user-space network stack from the Tor Project that tracks TCP and UDP state so traffic arriving on a TUN device can be forwarded into Tor. oniux handles the namespace isolation, while onionmasq and Arti carry the packets into the Tor network. The same Arti and onionmasq stack underpins the Tor Project's Android app, Tor VPN, as described in the [Tor VPN Beta](https://blog.torproject.org/tor-vpn-beta/) post.

## Our View

We see oniux as most useful for command-line tools and scripts: measurement scripts, package downloads or one-off `curl` calls that lack proxy support or are statically linked, where configuring SOCKS per tool is error-prone. It controls where packets go, not what the application reveals. Cookies, logged-in accounts and browser fingerprints identify a user just as well over Tor, so it is no substitute for Tor Browser when browsing. Since it is Linux only and still experimental, high-risk work is better served by systems built for whole-machine isolation, such as Tails or Whonix (our docs site compares them in [Tails vs Whonix vs Qubes](docs:tools/tails-vs-whonix-vs-qubes/)).
