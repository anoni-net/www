---
title: Tor Relay 架设指南
description: 在 Debian 或 Ubuntu 架设 Tor 中间节点的步骤，包含 torrc 配置、nyx 监控、同一台主机运行多个 instance，以及法律风险、家庭网络与带宽需求的常见问题。
---

Tor 网络的带宽与稳定性来自各地志愿者运营的中继节点（relay），每多一个中继，就有更多人能安全、匿名地上网。中间节点（Middle Relay）只在 Tor 网络内转发流量，不直接连到最终目的地，运营者承担的法律风险比出口节点低得多（各类节点的角色见[什么是 Tor](docs:tools/what-is-tor/)）。本页的步骤以中间节点为例。

## 架设前的评估

![Tor 中继节点的运作流程](https://assets.anoni.net/www/tor-diagram-fac3c33d.webp)

架设前需先决定下列事项，打算架设出口节点的话，还要另外评估自己能承受的风险：

- 节点类型：出口节点，或网桥、中间节点这类非出口节点。
- 出口策略：架设出口节点时要开放哪些端口。开放的端口越多，通常会收到越多滥用或违法投诉。
- `ORPort`：接受 Tor 连接的对外 TCP 端口。服务器上没有其他服务占用 443 时，建议设成 `ORPort 443`。公共 Wi-Fi 通常只开放少数几个端口，443 多半在其中。9001 也是常用的 `ORPort`。
- `ContactInfo`：节点的联系邮箱，会公开显示。
- 带宽与流量：愿意分给 Tor 的带宽与每月流量。
- IPv6：服务器是否有 IPv6 地址。

## 中间节点的架设

建议使用 Debian 或 Ubuntu，以下示例以这两个发行版操作。其他操作系统与更详细的安装说明见官方文档 [Tor Project | Middle/Guard relay](https://community.torproject.org/relay/setup/guard/)。

### 软件包安装

```bash
apt update
apt install tor
```

!!! info "最新版与测试版"

    各 Linux 发行版收录的 tor 不一定是最新版本，需要最新版或测试版时，按官方说明改用 Tor Project 的软件源：[Why and how I can enable Tor Package Repository in Debian?](https://support.torproject.org/apt/tor-deb-repo/)

### torrc 配置

编辑配置文件 `/etc/tor/torrc`：

```bash
Nickname    myNiceRelay # 把 "myNiceRelay" 改成要公开显示的名称
ContactInfo your@e-mail # 联系方式，会公开显示
                        # 不想公开可设成 none
ORPort      9001        # 默认的端口为 9001
                        # 改用 443 这类常见的 HTTPS 端口
                        # 审查严格地区的用户更容易连上
                        # 记得在防火墙与路由器开放对应的端口
ExitRelay   0           # 不成为出口节点
SocksPort   0
Log notice file /var/log/tor/notices.log # 开启日志记录
```

重新启动 tor，默认的 instance 是 `tor@default`：

```bash
systemctl restart tor@default
```

接着检查 `/var/log/tor/notices.log` 或系统日志 `/var/log/syslog`，出现 `Self-testing indicates your ORPort` 与 `reachable` 字样，代表外部可以连到 ORPort。约三个小时后，可以在 [Relay Search](https://metrics.torproject.org/rs.html) 搜索到节点的信息。

!!! info "安装后的运维事项"

    安装完成后的注意事项见官方文档 [Tor Project | Relay Post-install and good practices](https://community.torproject.org/relay/setup/post-install/)。

## nyx 监控

nyx 是 Tor 的终端监控工具，可以实时查看节点的状态与性能，安装后运行 `nyx` 即可打开。

```bash
apt install nyx
```

## 同一台主机的多个 instance

Debian 与 Ubuntu 的 tor 软件包附带 `tor-instance-create` 脚本，可以在同一台服务器建立多个独立的 Tor instance，各自的配置与日志分开管理。

### instance 的建立

`tor-instance-create` 的参数是 instance 名称，只能使用英文字母与数字，对应的 systemd 服务是 `tor@<instance 名称>`。

```bash
tor-instance-create {instance-name}
tor-instance-create mytor2
```

上例建立名为 `mytor2` 的 instance，配置文件在 `/etc/tor/instances/mytor2/torrc`，数据目录是 `/var/lib/tor-instances/mytor2`。

### instance 的配置

在 `/etc/tor/instances/mytor2/torrc` 设置这个 instance 的参数，例如：

```bash
ORPort 9002  # 设置新的 ORPort，每个 instance 使用不同的端口
DataDirectory /var/lib/tor-instances/mytor2/data
Log notice file /var/lib/tor-instances/mytor2/notice.log
```

### instance 的启动

启动或重新启动新建立的 instance：

```bash
# systemctl start tor@{instance-name}
systemctl start tor@mytor2
```

### 单个 instance 的 nyx 监控

nyx 用 `-s` 指定该 instance 的 control socket：

```bash
nyx -s /run/tor-instances/{instance-name}/control
```

## 常见问题

### 法律风险

入口节点（Guard Relay）与中间节点只在 Tor 网络内转发流量，不直接连到最终目的地，执法单位因此找上运营者的机会很低。出口节点（Exit Relay）的法律风险较高，架设前需审慎评估。

在台湾架设 Tor 中继目前是合法的，法律状况仍可能变动，建议持续关注网络自由相关的议题与法规。台湾以外的地区可以先读 EFF 的 [Legal FAQ for Tor Relay Operators](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)。

### 家庭网络

用家庭网络（例如台湾的中华电信光世代、有线电视宽带）架设时，可能需要调整电信运营商提供的路由器，有一定的技术门槛。家用路由器默认会拦截所有入站连接，需要在防火墙放行 ORPort 的入站流量，并在路由器设置端口转发。

### 带宽与网络条件

Tor Project 建议中继的上传与下载带宽各至少 10 Mbit/s（约 1.25 MB/s，见 [Relay requirements](https://community.torproject.org/relay/relays-requirements/)）。带宽不足 10 Mbit/s 但仍有 1 Mbit/s 以上时，官方建议改为架设 obfs4 网桥。中继另外需要固定的 IP 地址，也要确认 ISP 允许这类流量，防火墙与路由器能设置所需的端口转发。

中继只会用到设置的带宽上限，不会占满所有网络资源。高负载时仍可能感觉到网速稍慢，可以视需要调整配置里的带宽限制。

### 运营者的隐私

中继本身不会访问或追踪用户的流量。设置时留意会公开的身份信息，`ContactInfo` 不要用能识别个人身份的邮箱。

### 软件更新

Tor 软件需保持更新，才能取得安全补丁与新功能。多数 Linux 系统通过包管理器更新，Windows 与 macOS 需定期到 Tor 官网确认新版本。

### 入口节点的选定

入口节点的身份是自动指派的，运营者无法手动设置。节点稳定运行且带宽足够时，就有机会被选为入口节点。

## 相关阅读

- [Tor WebTunnel 网桥架设指南](/join/setup-tor-webtunnel/)：把网桥流量伪装成一般 HTTPS，适合一般中继无法连上的受审查网络
- [Tor 中继节点观测](/projects/pulse/)：台湾与邻近地区中继节点的数量、带宽与角色变化
- [Tor Relay 校园建立研究专题](/join/relay-on-campus/)：在校园网络架设中继的计划与案例
- [参与 Tor Project](/join/tor-project/)：参与 Tor 上游的方式与官方沟通渠道
