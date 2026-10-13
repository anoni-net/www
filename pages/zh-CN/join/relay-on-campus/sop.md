---
title: 校园 Tor Relay 架设 SOP
description: 在台湾校园网络架设 Tor Relay 的技术步骤，包含 torrc 范例、UFW 防火墙规则、状态网页的两种方案、监控与事件处置 runbook、验收测试、IPv6 与交接。
---

本页补充[Tor Relay 架设指南](/join/setup-tor-relay/)没有涵盖的校园网络情境，内容整理自社群伙伴 NZ 在台湾师范大学的实践经验，搭配[校园 Tor Relay 提案范本](/join/relay-on-campus/proposal/)与[给校方与法务的校园 Tor Relay FAQ](/join/relay-on-campus/faq/)使用。

本页假设你已经取得学校的上线许可。还在评估是否要做、如何说服学校时，先从[校园 Tor Relay 提案范本](/join/relay-on-campus/proposal/)开始。

## 校园与个人架设的差异

校园网络与家庭网络、个人 VPS 有几个结构上的差异，会直接影响技术选择：

- **IP 由学校分配**：通常是一个固定的 IPv4 地址，需走信息中心的申请流程
- **IPv6 另外申请**：多数学校默认不开放 IPv6，双栈需要额外提出申请
- **对外服务需申请例外开放**：台湾学术网络（TANet）的校园网络默认不开放对外服务，每一项都要走例外开放的申请
- **SSH 限校内 VPN 网段**：管理连接只开放校内 VPN 网段接入，不直接暴露在互联网上
- **每项配置都要能向校方说明**：每个对外开放的端口、每一段流量都要能对应到计划书里的描述
- **长期运维需考虑毕业交接**：ContactInfo 不使用个人的主要邮箱

## 项目范围与范围外事项

与信息中心沟通时，先说明不做哪些事，比说明要做什么更重要。

### 范围内

- 只建设非出口节点（Non-Exit Relay），也就是入口节点（Entry Guard）与中间节点（Middle Relay）
- 对外公开的只有节点状态页，不含用户数据

### 范围外

- 不提供 VPN、代理上网与 Tor 客户端服务（SocksPort、DNSPort）
- 不提供 Onion Services（.onion 服务）
- 不变更校园边界防火墙、DNS 解析与内容过滤的策略
- 不执行深度包检测（DPI）

### 可逆性

任何时间都可以在 10 分钟内下线，做法是停止 systemd 服务并关闭 ORPort。

## 服务与连接一览

### 对外公开的端口（Inbound）

| 服务 | 端口与协议 | 来源 | 说明 |
|---|---|---|---|
| Tor ORPort | 9001/tcp | Internet | Relay 之间的 TLS 连接，唯一必要的对外端口 |
| HTTP（ACME） | 80/tcp | Internet | Let's Encrypt 证书签发与 301 重定向 |
| HTTPS（状态页） | 443/tcp | Internet | 对外的状态网页 |
| SSH | 22/tcp | 校内 VPN 网段 | 管理用，限校内网段 |
| DirPort | 不开放 | – | 不开 DirPort，减少攻击面 |

Tor 相关的 TCP 端口只对外开放 ORPort 一个。443 没有被状态网页或其他服务占用时，也可以把 ORPort 改成 443，审查严格地区的用户比较容易连上。

### 对外主动连接（Outbound）

| 用途 | 端口与协议 | 去向 |
|---|---|---|
| 获取目录共识、连接其他 Relay | TCP 443、9001 等（动态） | Tor 目录权威（directory authority）与各 Relay |
| 系统更新 | TCP 80、443 | 软件包镜像站 |
| 时间同步 | UDP 123 | 指定的 NTP 服务器 |

### 明确封锁的项目

- 所有 UDP（指定的 NTP 服务器除外）
- 邮件端口 SMTP 25、465、587
- IRC 6667、6697 与 P2P 常用的端口
- SocksPort、DNSPort、HTTPTunnelPort 一律不启用

## 操作系统与安全基准

操作系统建议使用 Ubuntu Server 24.04 LTS 的最小安装（minimal install），再完成以下配置：

1. **最小化安装**：只安装 `tor`、`nginx`、`certbot`、`fail2ban`、`unattended-upgrades`、`rsyslog`、`auditd`、`chrony`，视需要加上 `prometheus-node-exporter`
2. **SSH 配置**
    - 只允许密钥登录：`PasswordAuthentication no`
    - 禁止 root 直接登录：`PermitRootLogin no`
    - 限定用户：`AllowUsers <你的账号>`
    - 连接超时：`ClientAliveInterval 300`
3. **自动安全更新**：启用 `unattended-upgrades`
4. **时间同步**：使用 `chrony`，事件调查的时间一律以 UTC 记录
5. **系统加固**：启用 AppArmor，设置 `fs.protected_*` 参数
6. **日志持久化**：`journald` 设为 `Storage=persistent`，可以再通过 `rsyslog` 转发到校内的 SIEM
7. **文件完整性（可选）**：部署 AIDE，定期比对文件基准
8. **磁盘加密（可选）**：硬件允许时以 LUKS 加密整块磁盘，至少保护 `/var/lib/tor`
9. **备份**：离线或异地备份 `/etc/tor/torrc` 与 `/var/lib/tor/keys/`，**身份密钥需严格保密**

## Tor 的安装

- **软件包来源**：优先使用 [Tor Project 官方软件源](https://support.torproject.org/apt/tor-deb-repo/)，发行版自带的版本通常落后一两版
- **服务账号**：以软件包默认的 `debian-tor` 账号运行，**不要用 root**
- **只运营非出口节点**：以 `ExitRelay 0` 与 `ExitPolicy reject *:*` 明确声明，避免成为 Exit Relay

## torrc 参考配置

配置文件位置：`/etc/tor/torrc`

```bash
# 基本身份
Nickname    <YourSchoolRelayName>
ContactInfo <project-email@example.edu> - Non-exit relay at <Dept/School>; Abuse: <noc@example.edu>

# 只做 Guard 与 Middle（非出口）
ExitRelay   0
ExitPolicy  reject *:*

# ORPort：对外服务唯一必要的入口
ORPort      0.0.0.0:9001

# 不需要目录镜像时关闭 DirPort
DirPort     0

# 不提供本机 Socks 代理
SocksPort   0
SocksPolicy reject *

# 控制端口（仅限本机，供 nyx 与运维使用）
ControlPort           127.0.0.1:9051
CookieAuthentication  1
CookieAuthFileGroupReadable 1
DataDirectoryGroupReadable  1

# 带宽与突发流量（依学校政策调整）
# 例：持续 80 MB/s，突发 120 MB/s
RelayBandwidthRate    80 MB
RelayBandwidthBurst   120 MB

# 日志（notice 级别即可，避免记录敏感细节）
Log notice file /var/log/tor/notices.log

# MetricsPort（可选）：只给本机或内网监控，绝不对外
# MetricsPort       127.0.0.1:9035
# MetricsPortPolicy accept 127.0.0.1
```

### ContactInfo 的写法

- 不使用个人的主要邮箱，改用项目邮箱或社团的共用邮箱
- 留下 abuse 联系邮箱，Tor 的 Network Health 团队才能联系到运维者
- 字段内容会公开显示在 Relay Search，**写入前就当成公开信息处理**

### MetricsPort 的安全考量

`MetricsPort` 让 Prometheus 可以采集 relay 的统计指标。依 [Tor 官方的说明](https://support.torproject.org/relay-operators/relay-bridge-overloaded/)，公开 MetricsPort 会危及 Tor 网络的用户。需要远程采集时，以防火墙与 `MetricsPortPolicy` 严格限制来源，并经过 TLS Proxy。

## UFW 防火墙规则

默认策略：

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw logging on
```

SSH 只开放校内 VPN 网段（把 `<学校 IP 段>` 换成学校的 CIDR）：

```bash
sudo ufw allow from <学校 IP 段> to any port 22 proto tcp comment 'SSH from campus VPN'
sudo ufw limit 22/tcp comment 'Rate-limit SSH'
```

状态网页的 Web 服务：

```bash
sudo ufw allow 80/tcp  comment 'HTTP for ACME/redirect'
sudo ufw allow 443/tcp comment 'HTTPS status site'
```

Tor ORPort（Guard 与 Middle 唯一需要开放的端口）：

```bash
sudo ufw allow 9001/tcp comment 'Tor ORPort'
```

MetricsPort 默认不开放，有内网监控主机 `<监控主机 IP>` 时才加上：

```bash
sudo ufw allow from <监控主机 IP> to any port 9035 proto tcp comment 'Prometheus -> Tor MetricsPort'
```

启用并确认规则：

```bash
sudo ufw enable
sudo ufw status numbered
```

## 对外状态网页

校方与外部人士可以从公开网页确认 relay 正在运行，有助于建立信任。以下两种架构任选其一即可。

### 方案 A，Nginx 与 Onionoo

- 以 Nginx 提供 HTTPS 状态页
- 页面向 [Tor Onionoo API](https://metrics.torproject.org/onionoo.html) 获取自身 fingerprint 的公开数据（流量、标志、上线状态）
- 只显示公开信息，不暴露任何内部 endpoint

推荐采用方案 A，架构简单，数据全部由前端向公开 API 获取，不涉及内部服务。缺点是图表的灵活性较低。

### 方案 B，MetricsPort、Prometheus 与 Grafana

需要完整的可观测性时采用方案 B：

- 本机启用 `MetricsPort 127.0.0.1:9035`，**不对外开放**
- 在本机或内网架设 Prometheus 采集 `/metrics`
- 以 Grafana 制作图表
- 对外只能公开 Grafana，并且**必须**符合以下条件：
    1. 只读账号，搭配强密码或 SSO
    2. HTTPS
    3. 只放公开、不含敏感信息的图表
    4. Prometheus **不直接对外**
    5. MetricsPort **绝不对外**

### Nginx 与 TLS 配置

- 以 `certbot --nginx` 自动签发与续期证书
- 只启用 TLS 1.2 与 1.3，关闭弱加密套件（cipher）
- 启用 HSTS、`X-Content-Type-Options: nosniff`、`Content-Security-Policy`
- 加上 `X-Robots-Tag: noindex, nofollow`，避免被搜索引擎索引
- `/.well-known/acme-challenge/` 走 80/TCP，其余 80 端口的请求全部以 301 重定向到 443

## 监控、日志与事件处置

### 日志

- `journald` 持久化，视需要以 `rsyslog` 转发
- Nginx 与 Tor 的日志各自写入独立文件，以 `logrotate` 轮转
- Tor 建议使用 `Log notice` 级别，避免记录敏感细节
- 事件发生时可以临时调高级别，处理完再恢复

### 主机层的可观测性

- `node_exporter` 绑定 `127.0.0.1:9100`
- 由本机的 Prometheus 采集、Grafana 显示，**对外公开时限只读**

### 变更审计

- `auditd` 记录关键文件的变更：`/etc/tor/torrc`、`/var/lib/tor/keys/`
- AIDE 定期比对，结果发送到运维邮箱

### 备份与密钥保全

- 离线或异地备份 `torrc` 与 `/var/lib/tor/keys/`
- 身份密钥丢失时，relay 只能以新的身份重新加入网络，先前累积的稳定度记录无法延续

### 事件处置 Runbook

收到异常告警时依序处理：

1. **初步判断（Triage）**：
    ```bash
    sudo ss -tnlp | egrep ':22|:80|:443|:9001|:9035'
    sudo journalctl -u tor@default -n 200
    sudo ufw status numbered
    ```
2. **停止服务**：
    ```bash
    sudo systemctl stop tor@default
    ```
    并保留 `/var/log` 与 `/var/lib/tor/` 的完整快照
3. **内部通报**：30 分钟内提交初步事故报告，内容包含影响范围、起因、处置与预计恢复时间
4. **疑似遭入侵**：依序封存证据、隔离主机、重建系统，确定密钥没有泄露时，才使用备份的身份密钥恢复

**下线条件**：影响校务网络、发生网络安全异常，或主管、导师要求下线。

## 验收与连接测试

1. **本机配置检查**：
    ```bash
    sudo -u debian-tor tor --verify-config
    ```
2. **ORPort 可达性**：
    ```bash
    # 从校外的另一台主机执行
    nmap -p 9001 <你的公网 IP>
    # 或
    telnet <你的公网 IP> 9001
    ```
    Tor 日志出现 ORPort 无法确认可达（reachability）的警告时，通常是防火墙或例外开放的申请还没生效
3. **Relay 上线确认**：启动约 3 小时后，到 [Tor Metrics Relay Search](https://metrics.torproject.org/rs.html) 以 fingerprint 查询状态

## IPv6 配置（可选）

要支持 IPv6 时，先向信息中心申请 IPv6 地址，再在 `torrc` 加入：

```bash
ORPort [<你的 IPv6>]:9001
```

UFW 也要放行对应的 IPv6 流量。IPv6 虽然是可选项目，对 Tor 网络的多样性有明显帮助，建议向学校争取。

## 交接与毕业后的运维

运维者会毕业是校园 Relay 与个人 Relay 最大的差别，从上线第一天就要准备交接：

- **共用的 ContactInfo 邮箱**：使用社团邮箱、项目邮箱或共用邮箱，不使用个人的主要邮箱
- **两份以上的密钥备份**：一份在运维者手上，一份放在导师的实验室
- **交接清单**：torrc、UFW 规则、SSH 密钥、CDN 与监控账号、ContactInfo 邮箱的密码
- **提早寻找接手者**：毕业前一学期就要确定接手的人
- **交接手册**：记录主机的历史、遇到过的问题与约定的运维频率

!!! tip "上线之后"

    - **回报案例**：通过[服务](/services/)页面的渠道联系匿名网络社群 anoni.net，我们会把你的案例加进[Tor Relay 校园建立研究专题](/join/relay-on-campus/)的「已完成的工作」，让之后加入的学校有更多参考
    - **长期运维**：[Tor Relay 架设指南](/join/setup-tor-relay/)有 nyx 监控的配置，常见问题一节补充了软件更新与入口节点的选定方式
    - **其他贡献方式**：另外运行 [Tor Snowflake](docs:tools/tor-snowflake/) 的代理，协助受审查地区的用户连上 Tor

## 相关阅读

- [Tor Relay 架设指南](/join/setup-tor-relay/)：个人与家庭环境的基础安装
- [校园 Tor Relay 提案范本](/join/relay-on-campus/proposal/)：与学校沟通用的提案文档
- [给校方与法务的校园 Tor Relay FAQ](/join/relay-on-campus/faq/)：校方常见的疑虑与回答
- [Tor Relay 校园建立研究专题](/join/relay-on-campus/)：社群推动校园 Relay 的入口
- [Tor Project Relay Operator Guides](https://community.torproject.org/relay/)：官方的运营指南
- [Tor Relay Post-install and good practices](https://community.torproject.org/relay/setup/post-install/)：上线后的注意事项

## 资料来源与致谢

本页的原始设计文档与实践经验由社群伙伴 **苏恩立（NZ）** 提供，整理自他在台湾师范大学的部署过程。NZ 同意原始材料以 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans) 授权发布。

按照本页操作时，若发现步骤不适用于你的学校环境，或有可以补强的细节，欢迎通过[服务](/services/)页面列出的渠道反馈，我们会持续更新本页的内容。
