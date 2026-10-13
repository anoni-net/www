---
title: oniux，以 Linux 命名空间隔离应用程序的 Tor 工具
description: Tor Project 介绍 oniux 的翻译，说明它如何用 Linux 命名空间让任意程序只能经由 Tor 连接，附上 2026-10 核查的安装方式，以及 oniux 与 onionmasq 的关系。
date: 2025-05-16
---

!!! info ""

    本文翻译自 Tor Project 博客的 [Introducing oniux: Kernel-level Tor isolation for any Linux app](https://blog.torproject.org/introducing-oniux-tor-isolation-using-linux-namespaces/)（2025-05-14），文中的「我们」是 Tor Project。安装方式依 2026-10 的官方文档更新，补注、「oniux 与 onionmasq」与「社区的看法」两节由 anoni.net 撰写。

![oniux 的介绍图](https://blog.torproject.org/introducing-oniux-tor-isolation-using-linux-namespaces/lead.webp){ .shot }

开发者在推出重视隐私的应用程序与服务时，希望每一个数据包都确实经由 Tor 传送。只要代理配置错一处，或有一次系统调用不小心绕过了 SOCKS，数据就可能泄露。

我们因此推出 oniux，一个小型的命令行工具，利用 Linux 命名空间为第三方应用程序提供 Tor 网络隔离。oniux 构建在 Arti 与 onionmasq 之上，把任何 Linux 程序放进专属的网络命名空间，流量全部经由 Tor 路由，排除数据泄露的可能。工作、行动或研究需要严格的流量隔离时，可以考虑 oniux。

## Linux 命名空间

命名空间（namespace）是 Linux 内核大约在 2000 年引入的隔离功能，可以安全地把应用程序的特定部分与系统的其余部分隔开。命名空间有网络、挂载、进程等多种，每一种隔离一部分系统资源。

系统资源是系统上所有应用程序共享的东西，最明显的例子是操作系统的时钟，其他还有进程列表、文件系统与用户列表。

命名空间把应用程序的某一部分与操作系统的其余部分容器化，Docker 的隔离机制就是用它实现的。

## Tor 与命名空间的结合

命名空间可以用来隔离任意应用程序的 Tor 网络访问。我们把每个应用程序放进一个网络命名空间，里面看不到系统级别的网络接口（例如 `eth0`），只有一个自定义的网络接口 `onion0`。

以命名空间隔离仰赖操作系统内核提供的安全机制，是软件层面隔离任意应用程序最安全的方式。SOCKS 代理则不同，开发者一时疏忽，让某条连接没有经过配置好的 SOCKS，数据就会意外泄露。

## oniux 与 torsocks 的比较

另一个目标相近的工具是 `torsocks`，它覆盖所有与网络相关的 libc 函数，把流量导向 Tor 提供的 SOCKS 代理。torsocks 的跨平台能力稍好，缺点是应用程序只要不经由动态链接的 libc 发出系统调用，无论有意或无意，数据都会泄露。纯静态的二进制文件与 Zig 生态系统的应用程序因此都不适用。

| oniux                | torsocks                                           |
| -------------------- | -------------------------------------------------- |
| 独立的应用程序       | 需要运行 Tor 守护进程                              |
| 使用 Linux 命名空间  | 使用 ld.so 预加载（preload）的手法                 |
| 适用于所有应用程序   | 只适用于经由 libc 发出系统调用的应用程序           |
| 恶意应用程序无法泄露 | 恶意应用程序可以直接用汇编语言发出系统调用泄露数据 |
| 只支持 Linux         | 跨平台                                             |
| 新项目，仍属实验性质 | 超过 15 年的实际使用记录                           |
| 以 Arti 为引擎       | 以 C Tor 为引擎                                    |
| 以 Rust 编写         | 以 C 编写                                          |

## 安装与使用

原文发表时的安装命令指定 `v0.4.0` 标签，以下依 2026-10 核查的官方资料更新。oniux 大约每月随 Arti 的发布推出新版，2026-10 核查时最新的标签是 `v0.13.0`（2026-09-09），编译需要 Rust 1.91 以上。

官方说明页列出 Alpine Linux、Nix、Void Linux 已收录 oniux 软件包，其他发行版的收录情况见 [Repology](https://repology.org/project/oniux/versions)。crates.io 上名为 oniux 的包只是 0.0.0 版的占位包，要从 Tor Project 的 GitLab 获取源代码安装。

发行版没有软件包时，先用 rustup 安装新版的 Rust 工具链，再用 cargo 安装：

```bash
$ cargo install --locked --git https://gitlab.torproject.org/tpo/core/oniux --tag v0.13.0 oniux
```

新版发布之后，把 `--tag` 换成 [oniux 的 GitLab 项目](https://gitlab.torproject.org/tpo/core/oniux/-/tags)上最新的标签即可。oniux 需要 `tun` 内核模块，多数发行版默认就会加载，运行时出现 `File not found` 错误的话，先执行 `modprobe tun` 再试一次。

使用方式是在原本的命令前面加上 `oniux`：

```bash
# 用 oniux 做一次简单的 HTTPS 查询
$ oniux curl https://icanhazip.com
<A TOR EXIT NODE IP ADDRESS>

# 也支持 IPv6
$ oniux curl -6 https://ipv6.icanhazip.com
<A TOR EXIT NODE IPv6 ADDRESS>

# 连接到洋葱服务
$ oniux curl http://2gzyxa5ihm7nsggfxnu52rck2vv4rvmdlkiu3zzui5du4xyclen53wid.onion/index.html

# 需要调试时可以开启日志
$ RUST_LOG=debug oniux curl https://icanhazip.com

# 把整个 shell 放进 oniux，里面的所有进程都经由 Tor 连接
$ oniux bash

# 在桌面环境里也可以隔离图形界面的应用程序
$ oniux hexchat
```

## 内部运作

oniux 一启动就用 `clone(2)` 系统调用产生一个子进程，放在独立的网络、挂载、PID 与用户命名空间里。子进程挂载自己的 `/proc`，再依父进程的 UID 与 GID 设置对应的 UID、GID 映射。

接着，子进程建立一个写有 nameserver 项目的临时文件，绑定挂载（bind mount）到 `/etc/resolv.conf`，命名空间里的应用程序因此改用可以经由 Tor 解析域名的解析器。

然后，子进程用 onionmasq 建立名为 `onion0` 的 TUN 接口，再通过 `rtnetlink(7)` 完成必要的设置，例如分配 IP 地址。

子进程接着用 Unix domain socket 把 TUN 接口的文件描述符（file descriptor）传给父进程。父进程从执行 `clone(2)` 之后就一直在等这条消息。

完成上述步骤后，子进程放弃它作为用户命名空间里的 root 进程所取得的全部权限（capabilities）。

最后，oniux 用 Rust 标准库提供的功能执行用户指定的命令。

## 实验阶段的限制

oniux 还很新，使用的 Arti 与 onionmasq 也都是新的 Tor 软件。目前功能都按预期运作，但 torsocks 这类工具已经存在超过 15 年，实际使用的经验多得多。我们希望 oniux 也能达到同样稳定的程度，欢迎试用。

!!! note "2026-10 补注"

    oniux 的 README 写明，应用程序在 oniux 里比在 torsocks 下更难泄露流量，但无法完全避免。应用程序通过 Unix domain socket 等进程间通信连到 oniux 外面的进程时，连接会绕过隔离。以服务器模式运行的 Emacs 是一个例子。服务器进程在 oniux 外面时，连上它的客户端无论是否经由 oniux 运行，网络连接都会泄露。网络命名空间在技术上就有这项限制，挡下进程间通信又会牺牲可用性（见 [oniux 的 GitLab 项目](https://gitlab.torproject.org/tpo/core/oniux)）。

## oniux 与 onionmasq

oniux 里的 `onion0` 接口由 onionmasq 提供。onionmasq 是 Tor Project 用 Rust 开发的用户空间网络栈，负责处理 TCP 与 UDP 的连接状态，让 TUN 接口收到的流量可以转进 Tor 网络（见 [onionmasq 的 GitLab 项目](https://gitlab.torproject.org/tpo/core/onionmasq)）。oniux 处理命名空间的隔离，数据包进入 Tor 网络的部分交给 onionmasq 与 Arti。Tor Project 的 Android 版 Tor VPN 也构建在以 Arti 与 onionmasq 为核心的模块化 Tor 栈上（见 Tor Project 博客的 [Tor VPN Beta](https://blog.torproject.org/tor-vpn-beta/)）。

## 社区的看法

oniux 最适合命令行工具与脚本，例如测量脚本、软件包下载或临时的 `curl` 查询。这类程序常常不支持代理配置，或是静态链接，逐一配置 SOCKS 容易漏掉。oniux 决定数据包的去向，但不会改变应用程序自己透露的信息。cookie、登录的账号与浏览器指纹经由 Tor 一样能识别出用户，浏览网页仍然要用 Tor Browser。oniux 只支持 Linux，也还在实验阶段。高风险的工作比较适合整台机器隔离的系统，例如 Tails 或 Whonix（文档站的 [Tails、Whonix、Qubes 的差别](docs:tools/tails-vs-whonix-vs-qubes/)有比较）。

## 致谢与来源

Tor Project 在原文最后感谢 `smoltcp` 的开发者，oniux 大量使用这个以 Rust 实现完整 IP 协议栈的 crate。另一位受感谢的贡献者，教开发团队不靠 `capabilities(7)`、改用正确的 `user_namespaces(7)` 实现隔离。oniux 的开发经费来自支持 Tor Project 的个人与组织，想支持这项工作可以[捐款给 Tor Project](https://donate.torproject.org/)。

oniux 现在有自己的说明页，放在 [Arti 的网站](https://arti.torproject.org/related/oniux)。2026-10 核查时说明页的安装命令仍写 `v0.10.0`，最新版本以 GitLab 项目的标签为准。
