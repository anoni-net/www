---
title: .onion 服务架设指南
description: 用 Tor 官方的方式架设 v3 onion 服务，含 nginx 导流、子域名、权限、日志、排错与上线后的运维，以及 vanity 地址的生成方式与限制。
---

Onion 服务让别人通过 Tor 直接连到你的服务器，过程中不需要公开服务器的 IP，也不需要向任何证书机构注册域名。连接两端都在 Tor 网络内完成，加密由 Tor 本身处理。

!!! info "与中继、桥接的区别"

    运营 [Tor 中继节点](/join/setup-tor-relay/)、[WebTunnel 桥接](/join/setup-tor-webtunnel/)与 [Snowflake](docs:tools/tor-snowflake/)，是**把带宽贡献给 Tor 网络**、替别人转发流量。

    Onion 服务则是**用 Tor 架设自己的网站**，只提供自己的内容、不转发他人的流量，也不增加 Tor 网络的容量。两者的风险、法律处境与运维负担都不同。

onion 服务的设计原理、与 IPFS 的取舍，以及 anoni.net 文档站三轨部署的架构，见[去中心化网站发布](docs:advanced/dweb-ipfs-onion/)。只想临时分享文件或架设用完即弃的网站时，[OnionShare](docs:tools/onionshare/) 的成本比自行架设服务低。

## 事前准备

- 可以自行管理的服务器，以 Linux 为主
- 已安装的 `tor`，用 `tor --version` 确认，发行版软件源的版本通常都支持 v3
- 可以从 `127.0.0.1` 连接的网页服务

### 网页服务的监听地址

```bash
sudo ss -ltnp | grep -E 'nginx|apache|caddy'
```

输出的 `Local Address` 列是 `127.0.0.1:80` 时，只有本机可以连接。`0.0.0.0:80` 或 `*:80` 则代表对整个互联网开放。

两种情况都可以接上 onion 服务，要同时保留 clearnet 版本就维持对外监听，Tor 一样可以连到 `127.0.0.1`。目的是让服务器完全不在 clearnet 上露出时，才需要把服务改成只绑定 `127.0.0.1`，并关闭对外的端口。

### 出站连接

Tor 需要主动向外连接才能加入 Tor 网络。防火墙**不需要**为 onion 服务开放任何入站端口。机器位于限制出站连接的企业内网时，Tor 无法连上 Tor 网络，后续每一步都不会成功。出站受限通常是内网环境最先遇到的问题。

## 一、Tor 官方的配置方式

配置文件是 `/etc/tor/torrc`，加上两行即可，以下是 [Tor 官方文档](https://community.torproject.org/onion-services/setup/)的示例：

```
HiddenServiceDir /var/lib/tor/my_website/
HiddenServicePort 80 127.0.0.1:80
```

`HiddenServiceDir` 是 Tor 存放服务身份的目录。`HiddenServicePort` 的第一个数字是 onion 地址对外的端口，后面接后端服务实际监听的地址与端口。

同一个 `torrc` 可以配置多组，每组各有独立的 onion 地址：

```
HiddenServiceDir /var/lib/tor/site-a/
HiddenServicePort 80 127.0.0.1:8080

HiddenServiceDir /var/lib/tor/site-b/
HiddenServicePort 80 127.0.0.1:8081
```

每一行 `HiddenServicePort` 都归属于它上方最近的 `HiddenServiceDir`。

### 目录权限

官方文档对权限只写了目录要「readable/writeable by the user that will be running Tor」，没有具体的权限数值。实际上目录权限必须是 `0700`，权限较宽时 Tor 会拒绝使用这个目录。

软件包安装的 `tor` 通常以 `debian-tor` 或 `tor` 用户执行，确认执行身份：

```bash
systemctl cat tor@default.service | grep -E 'User=|debian-tor'
ps -o user= -C tor
```

权限设置与确认：

```bash
sudo chown -R debian-tor:debian-tor /var/lib/tor/my_website
sudo chmod 0700 /var/lib/tor/my_website
sudo ls -ld /var/lib/tor/my_website
```

目录由 Tor 自行创建时（`torrc` 写好后重启即可），权限本来就正确，`chown` 与 `chmod` 只在手动创建目录时需要。

其他程序需要读取 `hostname` 时，可以在 `torrc` 设置 `HiddenServiceDirGroupReadable 1`，开放同组读取目录与 `hostname` 文件（默认是 `0`）。密钥文件不会因此变成组可读。

### 应用配置

```bash
sudo tor --verify-config          # 先检查语法，不影响运行中的服务
sudo systemctl restart tor@default
sudo systemctl status tor@default
```

!!! warning "Debian 与 Ubuntu 的两个 tor unit"

    软件包同时提供 `tor.service` 与 `tor@default.service`。实际运行的是 `tor@default.service`，`tor.service` 只是不做任何事的外壳。只重启 `tor.service` 不会应用新配置，界面上也看不出差别。

    不确定时用 `systemctl list-units 'tor*'` 查看哪一个处于 `running`。

### 日志的位置

Tor 出问题时，原因几乎都能从日志找到。通过 systemd 运行时：

```bash
sudo journalctl -u tor@default -n 50 --no-pager
sudo journalctl -u tor@default -f          # 持续输出新的日志
```

也可以在 `torrc` 另外指定日志文件，这一行默认是注释掉的：

```
Log notice file /var/log/tor/notices.log
```

首先确认 Tor 是否已连上 Tor 网络，日志里要有这一行：

```
Bootstrapped 100% (done): Done
```

没有这一行代表 Tor 还没连上网络，原因多半是出站连接被拦截。此时无论 `HiddenServiceDir` 是否配置正确，都不会生成 onion 地址。

### onion 地址与密钥

Tor 正常启动后，`HiddenServiceDir` 下面会有下列文件：

| 文件 | 内容 |
|---|---|
| `hostname` | 56 字符的 v3 地址加上 `.onion` |
| `hs_ed25519_public_key` | 公钥 |
| `hs_ed25519_secret_key` | **私钥，泄露即无法挽回** |
| `authorized_clients/` | 访问控制用的目录，默认是空的 |

目录是 `0700`、文件是 `0600`，都由 Tor 自行创建。只有 Tor 的执行身份可以读取，查看地址要用 `sudo`：

```bash
sudo cat /var/lib/tor/my_website/hostname
```

其余文件是服务的密钥，官方文档的警告如下：

> The other files are your Onion Service keys, so it is imperative that these are kept private. If your keys leak, other people can impersonate your Onion Service, deeming it compromised, useless, and dangerous to visit.

onion 地址就是公钥的编码，既没有吊销机制、也没有机构可以代为注销，密钥泄露后无从补救。唯一的处理是生成新地址并通知所有读者，而在抗审查的情境下，通知本身往往无法做到。

!!! tip "权限与备份的检查"

    `sudo ls -la /var/lib/tor/my_website` 的输出中，目录是 `drwx------`、文件是 `-rw-------`、所有者是 Tor 的执行身份，就是正常状态。Tor 自行创建的目录本来就是如此，不需要额外处理。

    备份整个 `HiddenServiceDir` 目录，存放位置要以等同或高于服务器的标准保护。具体做法是加密（例如放进已加密的密码管理器，或用 `gpg -c` 加密后再存），不要放进一般的云盘或代码仓库。

## 二、nginx 导流

Onion 服务只负责把连接转到指定的地址与端口，之后的导流由 nginx 的配置决定。

Debian 与 Ubuntu 的惯例是把配置放进 `/etc/nginx/sites-available/`，再链接到 `sites-enabled/`：

```bash
sudo nano /etc/nginx/sites-available/onion
sudo ln -s /etc/nginx/sites-available/onion /etc/nginx/sites-enabled/
sudo nginx -t                     # 语法检查，一定要先执行
sudo systemctl reload nginx
```

配置内容：

```nginx
server {
    listen 127.0.0.1:80;
    server_name <你的地址>.onion;

    root /var/www/site;
    index index.html;
}
```

`server_name` 填入实际的 onion 地址。同一个 `listen` 上只有一个 server block 时，填错也不影响。多个 server block 共用同一个 `listen` 时（例如第三节的子域名），没有匹配的请求会落到 nginx 的 default server，返回错误的内容或默认页。

### Unix socket 连接

`torrc` 的 `HiddenServicePort` 指向 `unix:` 路径时，nginx 要改成监听同一个 socket，后端就完全不经过 TCP。

!!! danger "`/run/tor/` 的权限限制"

    `/run/tor/` 是 Tor 的 runtime 目录，由 systemd 在启动时以 `debian-tor` 身份创建（unit 的 `ExecStartPre` 写着 `-o debian-tor -g debian-tor -d /run/tor`）。nginx 以 `www-data` 运行，无法在该目录创建 socket。

另外创建一个两边都能访问的目录：

```bash
sudo mkdir -p /run/onion
sudo chown www-data:debian-tor /run/onion
sudo chmod 0770 /run/onion
```

`/run` 是 tmpfs，重启会清空，要让目录在重启后重建，需加一条 tmpfiles 规则：

```bash
echo 'd /run/onion 0770 www-data debian-tor -' | sudo tee /etc/tmpfiles.d/onion.conf
sudo systemd-tmpfiles --create
```

`torrc` 与 nginx 指向同一个路径：

```
HiddenServicePort 80 unix:/run/onion/site.sock
```

```nginx
server {
    listen unix:/run/onion/site.sock;
    server_name <你的地址>.onion;

    root /var/www/site;
    index index.html;
}
```

socket 由 nginx 创建，Tor 是连接的一方，所以 Tor 的执行身份需要有写入权限。nginx 的 `listen` 指令没有设置 socket 所有者、组或权限的参数，权限只能在目录这一层控制。

reload 之后实际检查一次，不要假设默认值可用：

```bash
ls -l /run/onion/site.sock
```

权限太严时 Tor 无法连接，太宽则本机任何用户都可以连到后端，两个方向都要检查。

`torrc` 的 `GroupWritable` 与 `WorldWritable` 标志只作用在 Tor 自行创建的 socket（例如 `ControlSocket` 与 `SocksPort`），对 nginx 创建的 socket 没有作用。

### HTTPS 的取舍

连到 onion 服务的连接本身已经端到端加密并经过验证，地址就是公钥。再包一层 TLS 在密码学上不会增加保护，默认建议维持 HTTP，由 Tor 处理加密。

审计规定要求「一律要有 TLS」时，可以改用公开 CA 签发的 onion 证书。CA/Browser Forum 在 2021 年通过修正案，允许为 v3 `.onion` 签发 DV 证书，目前有商业 CA 提供付费服务。Tor Browser 曾把纯 HTTP 的 `.onion` 标示为不安全，这个问题在 2017 年已经修正（[`#21321`](https://gitlab.torproject.org/tpo/applications/tor-browser/-/issues/21321)），不必为了地址栏的提示加上 TLS。

### 常见的配置错误

- **响应里写死的 clearnet 网址**：页面上的链接、表单 action、重定向指向原本的域名时，访客点一下就离开 Tor，匿名性随即失效
- **外部资源**：图片、字体、分析脚本从 clearnet 加载时，访客的浏览器同样会对外连接
- **Referrer 泄露**：页面上连到 clearnet 网站的链接，浏览器默认会带上 `Referer`，你的 `.onion` 地址就会出现在对方的日志里。可以加上 `add_header Referrer-Policy no-referrer;`，或在链接加上 `rel="noreferrer"`
- **`Host` 头部检查**：有些应用框架会拒绝不在允许列表内的 `Host`，onion 地址要另外加进去
- **access log 里的 `127.0.0.1`**：所有连接都经过本机的 Tor 转发，日志记录的一律是本机地址，属于正常现象，日志配置没有问题

## 三、子域名的运作方式

Onion 地址可以带子域名，不需要另外申请或配置 DNS。Tor 把完整的 `Host` 原样传给后端，由 nginx 决定如何分流。

anoni.net 文档站的 onion 地址就是这种结构：

```
docs.anoninetru5tflukgfaehun7q6khowgmymcff3gtk5oyesqazhmfxtyd.onion
└┬─┘ └──────────────────── 56 个字符的 v3 地址 ────────────────────┘
 └── 子域名，由 nginx 的 server_name 分流
```

同一个 onion 地址可以承载多个子域名，nginx 的配置如下：

```nginx
server {
    listen 127.0.0.1:80;
    server_name docs.<你的地址>.onion;
    root /var/www/docs;
}

server {
    listen 127.0.0.1:80;
    server_name <你的地址>.onion;
    root /var/www/main;
}
```

`torrc` 不需要为子域名另外配置，一组 `HiddenServiceDir` 与 `HiddenServicePort` 即可。

## 四、访问控制

服务不打算对所有人开放时，可以用 v3 onion 内建的访问控制（client authorization）。未经授权的连接在会合阶段就被拒绝，无法取得任何内容，比只靠地址保密可靠得多。

服务器端把授权用的公钥放进 `HiddenServiceDir/authorized_clients/`，客户端在自己的 `torrc` 用 `ClientOnionAuthDir` 指向存放私钥的目录。内部工具与只提供给特定伙伴的镜像，都适合用这种方式。

密钥的生成方式与文件格式见 [Tor 官方的 client authorization 说明](https://community.torproject.org/onion-services/advanced/client-auth/)。

## 五、vanity 地址（可选）

!!! info "可略过的步骤"

    Vanity 地址只让开头的字符串比较好记，不影响服务是否可用，也不影响安全性。第一次架设建议先跳过，等服务运作正常再回来配置。

默认生成的地址是完全随机的 56 个字符。想让开头是可辨识的字符串（例如 anoni.net 的 `anoninet`），需要反复生成密钥，直到开头符合为止。

[mkp224o](https://github.com/cathugger/mkp224o) 是常用的工具，[Tor 官方的 vanity 地址说明](https://community.torproject.org/onion-services/advanced/vanity-addresses/)也以它为主。

依 mkp224o 说明文档所列，先安装编译需要的软件包：

```bash
sudo apt install gcc libc6-dev libsodium-dev make autoconf
```

编译与执行：

```bash
./autogen.sh
./configure
make
./mkp224o -d nekokeys neko
```

AMD64 平台可以在 `configure` 加上 `--enable-amd64-51-30k` 提升性能，BSD 系统把 `make` 换成 `gmake`。生成的密钥目录结构与 `HiddenServiceDir` 相同，搬过去之后照「目录权限」一节设置所有者与权限。

### 运算成本

依 mkp224o 说明文档的估计，6 个字符的前缀「shouldn't take more than few tens of minutes」，前提是 `if using batch mode`（细节在 `OPTIMISATION.txt`）。7 个字符则是「can take hours to days」。同一份文档也写明结果「depends on pure luck」，所需时间无法保证。

每多一个字符，搜索空间乘以 32。anoni.net 使用的 `anoninet` 有 8 个字符，难度是「hours to days」那一级 7 个字符的 32 倍。

### 字符集的限制

onion 地址用 base32 编码，字符集是 `a` 到 `z` 与 `2` 到 `7`，不含数字 `0`、`1`、`8`、`9`，带这些数字的前缀不可能生成。mkp224o 会在开始前检查并提前报错。

### vanity 地址与身份验证

Vanity 地址最容易被误解的地方在身份，Tor 官方文档的说明如下：

> An attacker wishing to impersonate an existing onionsite by creating a fake version of it might use vanity addresses as an additional way to convince users that their address is the right one.

任何人都可以用一般的运算资源，生成另一组以 `anoninet` 开头的地址。前缀相同不代表是同一个服务，前缀只提升可读性，没有验证作用。

对外公布地址时要给完整的 56 个字符，读者验证时也要比对完整地址，不能只看开头。

前缀以外的部分仍然随机生成，所以安全性不受影响，vanity 地址不会比一般地址容易被破解。

## 六、上线前的检查

以下六项依序确认。

### 1. Tor 网络的连接状态

```bash
sudo journalctl -u tor@default | grep -i bootstrapped | tail -1
```

输出要有 `Bootstrapped 100% (done)`。

### 2. onion 地址

```bash
sudo cat /var/lib/tor/my_website/hostname
```

输出应为 56 个字符加上 `.onion`。

### 3. 后端的本机响应

```bash
curl -sI http://127.0.0.1:80/ -H 'Host: <你的地址>.onion' | head -1
```

输出应为 `HTTP/1.1 200 OK`。带上 `Host` 头部可以模拟 Tor 实际转来的请求，同时验证 `server_name` 是否匹配。

### 4. 经由 Tor 的连接

用 Tor Browser 打开该 `.onion` 地址，没有图形界面时改用 `torsocks`：

```bash
sudo apt install torsocks
torsocks curl -sI http://<你的地址>.onion/ | head -1
```

!!! warning "描述符发布前的空窗"

    服务的描述符（descriptor）要先发布到 Tor 网络，刚配置完的前几分钟无法连接属于正常现象。等几分钟再试一次，先不要回头改配置。

    重启 Tor 之后也有同样的空窗。

### 5. 对外连接

查看页面源代码，确认图片、字体、脚本都没有从 clearnet 加载，再点过站上主要的链接，确认不会离开 Tor。

### 6. 密钥备份

做法见第一节的「权限与备份的检查」。

### Onion-Location 头部

clearnet 网站加上 `Onion-Location` 头部后，用 Tor Browser 访问的访客会看到切换到 onion 版本的提示：

```nginx
add_header Onion-Location http://<你的地址>.onion$request_uri;
```

依官方说明，这个头部要加在**走 HTTPS 的 clearnet 网站**上，加在 onion 网站本身没有作用。

## 七、常见的连接问题

??? question "Tor 启动失败"

    先查看日志：`sudo journalctl -u tor@default -n 50`。

    出现 `Permissions on directory ... are too permissive` 是目录权限过宽，对该目录执行 `sudo chmod 0700` 即可。

    出现 `Failed to parse/validate config` 表示 `torrc` 语法有误，用 `sudo tor --verify-config` 可以找出是哪一行。

??? question "修改 torrc 后未生效"

    多半是重启了 `tor.service`，实际运行的 `tor@default.service` 没有重启。用 `systemctl list-units 'tor*'` 确认哪一个在运行。

??? question "日志正常但无法连接"

    依序排除：

    1. 日志是否有 `Bootstrapped 100%`，没有的话是 Tor 无法连上 Tor 网络，检查出站防火墙
    2. `hostname` 文件是否存在，不存在表示 `HiddenServiceDir` 那段配置没有生效
    3. 刚配置完或刚重启时，描述符发布需要时间，等几分钟再试
    4. 本机直接连后端是否正常（见第六节第 3 项），不正常的话问题在 nginx，与 Tor 无关

??? question "权限正确但 Tor 无法访问"

    使用非默认的路径时，可能是 AppArmor 或 SELinux 拦下了访问。这类失败不会显示成权限错误，`ls -l` 的结果也一切正常。

    ```bash
    sudo journalctl -k | grep -i 'apparmor.*DENIED'
    sudo dmesg | grep -i denied
    ```

    有匹配的记录时，把路径改回 `/var/lib/tor/` 下面是最快的解法。systemd unit 本身的沙箱配置（`ProtectSystem`、`ReadWritePaths`）也可能拦下非默认路径，要一并确认。

??? question "nginx 端的排查"

    ```bash
    sudo nginx -t
    sudo tail -50 /var/log/nginx/error.log
    ```

    使用 Unix socket 时，用 `ls -l /run/onion/site.sock` 确认 socket 文件存在，且 Tor 的执行身份有写入权限。

??? question "重启后的连接失败"

    socket 所在的目录放在 `/run` 下面时，重启会被清空（`/run` 是 tmpfs），需要 `/etc/tmpfiles.d/` 的规则才会重建（见第二节）。

    另外确认 nginx 与 tor 的启动顺序，nginx 先创建 socket，Tor 才能连上。

## 八、上线后的运维

### 故障检测

Tor 的进程仍在运行，不代表描述符还正常发布在网络上。最直接的检查是定期从外部实际连接，例如用 `torsocks curl` 排一个定时任务。

### 重启后的空窗

每次重启 Tor 都要重新发布描述符，服务会有几分钟无法连接，不属于故障。

### 连接延迟

连接要经过数个中继，往返延迟通常是几百毫秒到超过一秒。交互式的应用（后台管理界面、实时协作）在 onion 上的体感明显比 clearnet 差，静态内容影响较小，决定是否把某个服务放上 onion 前要先纳入考量。

### 主机迁移

地址绑在密钥上，把整个 `HiddenServiceDir` 搬到新主机并设置正确权限，地址就不会改变。也因此，这个目录的备份要当成机密数据保管。

### 服务下线

移除 `torrc` 里对应的两行并重启即可。地址停用后，onion 这一侧无法告知访客发生了什么事，有读者依赖这个地址时，先在 clearnet 那一侧公告。

### 多台主机的负载分摊

需要多台机器分摊同一个 onion 地址的流量时，可以考虑 Tor Project 下面的 [OnionBalance](https://gitlab.torproject.org/tpo/onion-services/onionbalance)。项目在 2021 到 2025 年之间停滞过一段时间，2025 年 4 月恢复发布，最新版本是 `0.2.4`（2026-10 查核）。评估前先确认项目的近况。

## 九、Caddy 的配置方式

环境里已经使用 Caddy 的话，可以照着 [Onion mirror with Caddy](https://flower.codes/2025/10/23/onion-mirror.html) 的说明配置。

Caddy 默认会自动申请 TLS 证书，用在 onion 服务上要关闭（理由见第二节的「HTTPS 的取舍」）。整体流程与本文相同，差别只在导流的配置语法。

## 相关阅读

- [去中心化网站发布](docs:advanced/dweb-ipfs-onion/)：onion 服务的设计原理、与 IPFS 的取舍，以及 anoni.net 三轨部署的架构
- [文档站 IPFS 镜像的 pin 节点](/join/pin-ipfs-mirror/)：另一种抗封锁镜像，欢迎协助 pin
- [Tor Relay 架设指南](/join/setup-tor-relay/)：把带宽贡献给 Tor 网络，与本文是不同性质的工作
- [OnionShare](docs:tools/onionshare/)：临时分享文件与建站，不需要自行运维服务
