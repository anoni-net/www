---
title: Tor WebTunnel 桥接架设指南
description: Tor WebTunnel 桥接在 VPS 上的架设步骤与运维做法，包含域名、TLS 证书、nginx 反向代理、Docker 部署、防火墙、伪装页与事件处置。
---

WebTunnel 把 Tor 流量包进普通的 HTTPS 连接，流量形态与浏览网页相近，深度包检测（DPI）很难单独把它挑出来。审查系统用 DPI 封锁 obfs4 这类特征与 HTTPS 不同的协议时，WebTunnel 通常仍能通过，是 Tor 目前抗审查能力最强的桥接方式之一。

本页以 Tor Project 的 Docker 部署方式为准，另外补上官方文档没有写的 nginx 加固配置，以及上线后的监控、伪装页、防火墙与事件处置。

!!! info "桥接与中继的区别"

    为 Tor 网络出力的方式有三种，门槛与抗审查强度各不相同：

    - [Tor Snowflake](docs:tools/tor-snowflake/)：开一个浏览器标签页就能运行的临时桥接，门槛最低。Snowflake 走 WebRTC，握手特征可能被指纹识别，中国已有封锁记录。
    - WebTunnel（本页）：需要 VPS、域名与 TLS 证书，伪装成 HTTPS，在重度审查的网络里最难被封锁。
    - [Tor 中继节点](/join/setup-tor-relay/)：为 Tor 网络提供带宽与节点多样性，不属于桥接。

    桥接（bridge）跟中继一样不直接连向用户要访问的目的地，目的地网站收到的连接来自 Tor 出口节点。运营桥接的法律风险因此与入口、中间节点同级，远低于出口节点。

## 增设 WebTunnel 桥接的理由

审查者会封锁已知的桥接 IP，桥接分散在越多国家与网络运营商（ASN），受审查的用户可用的入口就越多。台湾对外连接受审查的程度低、带宽充足，适合作为桥接的来源地。WebTunnel 也比中继节点省资源，一台 512MB 到 1GB RAM 的 VPS 即可运行，成本与运维负担都比较低。

2026 年伊朗在军事行动期间多次大规模断网，第二阶段从 2 月底持续到 5 月底，将近三个月。网络重新开放后，社群架设的 WebTunnel 流量明显增加（见[伊朗封网后的 WebTunnel 流量](/updates/2026/05/iran-blackout-webtunnel/)）。在以 DPI 严格过滤的网络里，伪装成 HTTPS 的桥接常是少数还能连上 Tor 的方式。

## 架设前的准备

- 一台 VPS，Debian 或 Ubuntu，512MB RAM 以上，建议 1GB，让 Tor 进程有余裕。
- 一个可以编辑 DNS 的域名或子域名。
- 对外开放的 443 端口，WebTunnel 走标准的 HTTPS 端口才像普通网站。
- 联系用的 email，会公开在桥接的 `ContactInfo`。

!!! tip "域名与运营隐私"

    WebTunnel 的伪装效果取决于域名看起来是否像普通网站：

    - 选用无法一眼看出是 Tor 桥接的域名或子域名。
    - 根路径（`/`）放一个无害的页面，例如个人主页、域名停放页或简单的博客，让扫描者看到的是普通网站。
    - 在台湾这类低风险的环境，用现有域名的子域名通常没有问题。需要更高的运营隐私时，再考虑匿名注册的独立域名。

架设分成两部分。先配置域名、TLS 证书与反向代理，让服务器对外像普通的 HTTPS 网站，再用 Docker 运行桥接。

## 域名、TLS 与 nginx 反向代理

### DNS 记录

在域名的 DNS 新增一条 A 记录，把域名或子域名（例如 `bridge.example.com`）指向 VPS 的公网 IP，等 DNS 生效后再进行下一步。

### TLS 证书

WebTunnel 需要浏览器信任的 TLS 证书，连接才会像连到普通的 HTTPS 网站，用 Let's Encrypt 最简便。

```bash
apt update
apt install certbot python3-certbot-nginx
certbot --nginx -d bridge.example.com
```

certbot 软件包会安装自动续期的 systemd timer，确认方式：

```bash
systemctl status certbot.timer
```

!!! info "其他签发证书的方式"

    也可以用 `acme.sh` 之类的 ACME 客户端签发证书，做法见 [Tor Project | WebTunnel Bridge](https://community.torproject.org/relay/setup/webtunnel/)。

### nginx 反向代理配置

WebTunnel 桥接在本机的 `127.0.0.1:15000` 监听，nginx 负责对外的 HTTPS，再把一条秘密路径反向代理到桥接。秘密路径用一串随机字符串，下方示例以 `$PATH` 代表。

在现有或新建的 vhost 加上下面的 `location` 区块，WebSocket 请求头不可省略：

```nginx
location = /$PATH {
    proxy_pass http://127.0.0.1:15000;
    proxy_http_version 1.1;
    ### WebSocket 请求头 ###
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    ### 代理请求头 ###
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

!!! tip "反向代理的两项加固配置"

    以下两项调整不在官方文档里，可以让秘密路径更难被探测，长时间的连接也更稳定。

    **秘密路径的探测防护**

    默认配置下，不带 WebSocket 握手的普通请求发到秘密路径时，nginx 也会转发给桥接。桥接的响应可能与站上其他路径不同，反而暴露出路径的存在。加上一行配置，让没有 Upgrade 请求头的请求一律返回 404，秘密路径的响应就与站上任何不存在的网址相同：

    ```nginx
    location = /$PATH {
        # 只有真正的 WebTunnel 握手能通过，普通的探测一律返回 404
        if ($http_upgrade = "") { return 404; }
        proxy_pass http://127.0.0.1:15000;
        # ……其余配置同上
    }
    ```

    WebTunnel 的连接一定带有 Upgrade 请求头，这行配置不会挡下正常的桥接客户端。

    **长连接的超时配置**

    nginx 的 `proxy_read_timeout` 默认是 60 秒，连接超过 60 秒没有数据传输就会被切断，长时间维持的 Tor 线路会因此无故断线。在 `location` 区块里调高超时，并开启 TCP keepalive：

    ```nginx
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
        proxy_socket_keepalive on;
    ```

根路径的 `location /` 维持返回普通网页，服务器整体看起来就是普通网站，只有知道秘密路径的 Tor 客户端会连到桥接。改完后测试配置并重新加载：

```bash
nginx -t && systemctl reload nginx
```

## WebTunnel 桥接的 Docker 部署

### Docker 安装

```bash
apt install curl sudo
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

### `.env` 配置文件

`URL` 换成域名加上秘密路径（与 nginx 配置里的 `$PATH` 相同），`OPERATOR_EMAIL` 换成联系用的邮箱，再执行：

```bash
truncate --size 0 .env
echo "URL=https://bridge.example.com/your-secret-path" >> .env
echo "OPERATOR_EMAIL=your@email.org" >> .env
echo "BRIDGE_NICKNAME=WTBr$(cat /dev/urandom | tr -cd 'qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAQWERTUIOP0987654321'|head -c 10)" >> .env
echo "GENEDORPORT=4$(cat /dev/urandom | tr -cd '0987654321'|head -c 4)" >> .env
```

### docker-compose 配置文件

```bash
curl https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/webtunnel/-/raw/main/release/container/docker-compose.yml?inline=false > docker-compose.yml
```

compose 配置文件默认开启自动更新，桥接会自动更新到新版。接着启动容器：

```bash
docker compose up -d
```

### 桥接行与连接验证

```bash
docker compose exec webtunnel-bridge get-bridge-line.sh
```

把输出的桥接行（bridge line）粘贴到 Tor Browser 的桥接设置，即可测试能否连接。

!!! warning "命令失效时的替代写法"

    较新版本的容器名称可能是 `webtunnelBridge`，上面的命令会执行失败，改用：

    ```bash
    docker exec webtunnelBridge get-bridge-line.sh
    ```

桥接行里的 IP（特别是 IPv6）是随机生成的占位值，因为 pluggable transport 规范要求那个位置要有 IP，实际上不会使用。客户端连接时用的是域名与秘密路径。桥接默认会通过 [bridges.torproject.org](https://bridges.torproject.org/) 自动分发给需要的用户。

## 进阶运维

### 防火墙

WebTunnel 对外只需要开放 443（HTTPS），SSH 依管理需求保留。桥接监听的 `15000` 绑定在 `127.0.0.1`，不要对外开放。

```bash
ufw allow 443/tcp
ufw allow OpenSSH
ufw enable
ufw status
```

### 伪装页设计

根路径的页面也是伪装的一部分，建议放有实际内容、不会引人怀疑的静态页，例如个人作品集、技术笔记或域名停放页。空白页与 nginx 默认的欢迎页反而显眼。

### 监控与健康检查

- 容器状态与日志：

    ```bash
    docker compose ps
    docker compose logs -f
    ```

- TLS 证书的有效期与续期状态：`systemctl status certbot.timer`。
- 桥接上线数小时后，可以通过 [bridges.torproject.org](https://bridges.torproject.org/) 的流程或 Tor Browser 实测桥接是否已被分发、能否连接。

### 软件更新

桥接本体由 compose 配置自动更新。系统层的 Docker、nginx、certbot 仍需定期执行 `apt update && apt upgrade`，TLS 证书的续期交给 certbot timer。

### 事件处置 runbook

- **桥接无法连接**：先看 `docker compose logs`，再确认 nginx 的秘密路径与 `.env` 的 `URL` 路径一致、TLS 证书未过期、443 已开放。
- **证书过期**：执行 `certbot renew` 之后 `systemctl reload nginx`。
- **滥用投诉或法律询问**：桥接的角色接近入口与中间节点，不直接连向目的地。回复时说明 Tor 桥接的角色，并附上 [EFF 的 Tor 中继运营者法律 FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)。
- **桥接下线**：`docker compose down` 停止桥接，再移除 nginx 的 `location` 区块并重新加载。

## 常见问题

??? question "WebTunnel 与 Snowflake、obfs4 的区别"

    三者都是绕过审查、连上 Tor 的桥接。Snowflake 通过 WebRTC（浏览器用于视频通话的实时连接技术）运作，打开浏览器就能运行，但容易被检测。obfs4 把流量变成随机噪声，DPI 仍可能识别出它不像 HTTPS 而封锁。WebTunnel 把流量包进真正的 HTTPS 连接，审查者要封锁它就得连带封掉大量正常网站，所以在 DPI 过滤严格的网络里最有效。

??? question "运营桥接的法律风险"

    桥接与入口、中间节点一样不连向最终目的地，目的地网站收到的连接来自 Tor 出口节点。台湾的网络相对自由，目前允许运营这类节点，风险远低于出口节点。收到询问时可以参考 [EFF 的 Tor 中继运营者法律 FAQ](https://community.torproject.org/relay/community-resources/eff-tor-legal-faq/)。

??? question "服务器规格"

    512MB RAM 的小型 VPS 可以运行，但建议配置 1GB，Tor 进程本身可能用到接近 1GiB 的内存。CPU 与带宽的需求都不高。

??? question "家庭网络的架设条件"

    家庭网络也能架设，条件是有固定的公网 IP、能在路由器配置 443 的端口转发，而且 ISP 允许这类流量。动态 IP 会让桥接地址不稳定，用 VPS 通常更简便、稳定。

??? question "Docker 以外的安装方式"

    也可以从源代码编译 Go 可执行文件，做法见 [Tor Project | Compile and run WebTunnel from source](https://community.torproject.org/relay/setup/webtunnel/source/)。多数情况下 Docker 最简便。

## 相关阅读

- [网络自由为什么重要](docs:basics/internet-freedom/)
- [什么是 Tor](docs:tools/what-is-tor/)
- [Tor Snowflake](docs:tools/tor-snowflake/)：打开浏览器标签页就能运行的临时桥接

## 其他参与方式

- [Tor Relay 架设指南](/join/setup-tor-relay/)：在台湾架设中继节点的法律、技术与行政考量
- [Tor Relay 校园建立研究专题](/join/relay-on-campus/)：在大学校园架设 Tor 中继节点的计划与案例
- [Tor 中继节点观测](/projects/pulse/)：台湾与邻近地区中继节点的数量、带宽与版本变化

## 官方参考文档

- [Tor Project | WebTunnel Bridge](https://community.torproject.org/relay/setup/webtunnel/)：域名、TLS、nginx 配置的主要文档
- [Tor Project | WebTunnel Docker setup](https://community.torproject.org/relay/setup/webtunnel/docker/)：Docker 部署
- [Tor Project | Compile and run WebTunnel from source](https://community.torproject.org/relay/setup/webtunnel/source/)：从源代码编译
- [Introducing WebTunnel](https://blog.torproject.org/introducing-webtunnel-evading-censorship-by-hiding-in-plain-sight/)：WebTunnel 的设计理念
