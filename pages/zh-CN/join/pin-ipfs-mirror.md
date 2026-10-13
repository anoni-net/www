---
title: 文档站 IPFS 镜像的 pin 节点
description: 用常驻的 IPFS 节点与定时脚本 pin anoni.net 文档站的 IPFS 镜像，包含 Windows、Linux、macOS 与 Docker 的安装、定时任务、验证与 peering 配置。
---

anoni.net 文档站在主站之外另有一份 IPFS 镜像，主站被封锁或下架时仍可以读取文档。IPFS 上的内容需要有节点 pin 住才会留存。2026 年 8 月查询网络上的提供者，只有社群自己的一台节点，整份镜像目前是单点。每多一个节点协助 pin，网络上就多一份完整副本，社群那台机器被停用或故障时文档仍然留存。

协助的方式是架设一个常驻的 IPFS 节点，再用定时脚本定期 pin 最新版本。Windows、Linux、macOS 都适用，用不用 Docker 皆可。

!!! tip "所需条件"

    - 一台几乎整天开机、能连上网络的电脑（台式机、家用服务器或小主机）
    - 安装好的 IPFS（安装方式见下方）
    - 一支每隔几小时自动 pin 最新版本的定时脚本

    第一次要下载的整份镜像约 240 MB，来源目前只有社群那一台，建议一开始就配置[与社群节点的固定连接](#peering)，下载会顺利许多。无法常驻节点的话，文末有改用 pinning service 代 pin 的做法。

## CID、IPNS 与 pin 的关系

需要定时任务的原因在于 CID 会随内容改变。IPFS 的完整设计见[去中心化网站发布](docs:advanced/dweb-ipfs-onion/)，以下只整理 pin 会用到的概念。

- IPFS 依文件内容算出一段 hash，称为 CID（Content Identifier），也就是内容在 IPFS 上的地址。内容相同则 CID 相同。
- 内容一改，CID 就跟着改变。文档站每次更新、重新发布，都会产生新的 CID。
- IPNS（InterPlanetary Name System）是固定的名称，指向目前最新的 CID，文档站的 IPNS 名称是下方那串 `k51…`。
- pin 代表保留某个 CID 的内容。pin 绑在 CID 上，不会跟着 IPNS 更新。文档站发布新版之后，上次 pin 的仍是旧 CID。

pin 脚本先把 IPNS 解析成当前的 CID 并 pin 住，再放掉旧版。CID 每次发布都会变，所以要用定时任务定期重新执行。

### 三种相似的标识符

IPFS 有三种外观相近、用途不同的标识符，贴错字段时工具会直接报错。

| 标识符 | 开头 | 是否改变 | 用途 |
|---|---|---|---|
| CID | `bafybei…` | 每次发布都变 | 指定某一版内容 |
| IPNS 名称 | `k51qzi…` | 固定 | 取得最新版，本页的 pin 用这个 |
| Peer ID | `12D3KooW…` | 固定 | 指定要连到哪一个节点 |

pin 文档站只需要 IPNS 名称，Peer ID 在配置[与社群节点的固定连接](#peering)时才会用到。

## 定时 pin 的运作方式

IPNS 是各节点共用的同步点，文档站发布新版时只更新 IPNS，社群不需要另外通知。节点这端每隔几小时解析一次 IPNS，发现 CID 改变就 pin 新版，全程不需要人工协调。

!!! info "文档站的 IPFS 坐标"

    以下都是公开值，可以直接使用。

    - IPNS 名称：`k51qzi5uqu5dlfm2jj0f70ex3r3babmwy8qh071inwknttr7wqa3uhdwvlmrmw`
    - 节点 Peer ID：`12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9`（配置 peering 时才会用到）
    - DNSLink：`_dnslink.anoni.net` 指向同一个 IPNS 名称，通过任何支持 DNSLink 的网关都能读取同一份内容
    - 浏览器：社群自建的 [IPFS 网关](https://ipfs.anoni.net/)（`ipfs.anoni.net`）。旧网址 `anoni-net.ipns.dweb.link` 在 2026 年 9 月 30 日停止运营，见[2026 年 9 月之后的 IPFS 维护变化](#ipfs-maintenance-2026)

脚本每次执行时依次解析 IPNS 取得当前 CID、pin 新 CID、unpin 上一版，最后回收空间。新版 pin 成功之后才会放掉旧版，解析失败或下载不到内容时，节点上现有的副本维持原状。

## 常驻的 IPFS 节点

pin 需要本机有持续运作的 IPFS daemon 才能取得完整内容，依环境择一安装。

=== "Linux / macOS"

    安装 IPFS 官方的命令行实现 [kubo](https://docs.ipfs.tech/install/command-line/)，macOS 可以用 Homebrew：

    ```bash
    brew install kubo
    ```

    Homebrew 的包名称已从 `ipfs` 改为 `kubo`，旧名称仍可安装，但后面设置服务时需使用 `kubo`。Intel 与 Apple Silicon 都支持。

    Linux 依[官方说明](https://docs.ipfs.tech/install/command-line/)下载对应架构的 kubo，安装后初始化并启动 daemon：

    ```bash
    ipfs init          # 只有第一次需要
    ipfs daemon
    ```

    要让 daemon 长时间常驻，Linux 建议设成 systemd user service。macOS 用 Homebrew 安装时，包附有服务定义，执行下列命令即可常驻，并在登录时自动启动：

    ```bash
    brew services start kubo
    ```

    临时测试时，直接在后台执行 `ipfs daemon` 即可。

=== "Windows"

    最简便的做法是安装内含 kubo 的 [IPFS Desktop](https://docs.ipfs.tech/install/ipfs-desktop/)，登录后常驻在系统托盘，daemon 持续运作。IPFS Desktop 从 2026 年 9 月 30 日起没有专职维护者（见[2026 年 9 月之后的 IPFS 维护变化](#ipfs-maintenance-2026)），想减少这项不确定性，Windows 也可以安装独立版 kubo 或使用 Docker。

    安装后确认命令行可以调用 `ipfs`。独立版 kubo 需自行把 `ipfs.exe` 加进系统 PATH。使用 IPFS Desktop 而 PATH 找不到 `ipfs` 时，在脚本里改用完整路径即可。

=== "Docker"

    用 `docker-compose.yml` 执行 kubo，容器名称设为 `ipfs_host`：

    ```yaml
    services:
      ipfs_host:
        image: ipfs/kubo:latest
        restart: always
        volumes:
          - ./ipfs-data:/data/ipfs
        ports:
          - "4001:4001"   # swarm，对外开放有助于连上其他节点
    ```

    启动：

    ```bash
    docker compose up -d
    ```

    之后的 IPFS 命令都通过容器执行。设置下列环境变量，pin 脚本会自动套用：

    ```bash
    export IPFS_CMD="docker exec ipfs_host ipfs"
    ```

## pin 脚本

pin 脚本负责解析 IPNS、pin 新版与 unpin 旧版，IPNS 名称已写在脚本里，不需要修改。Docker 用户需先设置上一步的 `IPFS_CMD`。脚本会在你的机器上定期执行，建议先在 GitHub 读过源代码再执行。

### `anoni-pin.sh`（Linux、macOS、Docker）

[<i data-icon="download"></i> 下载 anoni-pin.sh](https://raw.githubusercontent.com/anoni-net/docs/main/docs/_scripts/anoni-pin.sh){ .btn } [<i data-icon="octicons-mark-github-24"></i> 在 GitHub 查看源代码](https://github.com/anoni-net/docs/blob/main/docs/_scripts/anoni-pin.sh){ .btn }

保存后加上执行权限，先手动执行一次确认运作正常：

```bash
chmod +x anoni-pin.sh
./anoni-pin.sh          # 先手动执行一次确认正常
```

### `anoni-pin.ps1`（Windows）

[<i data-icon="download"></i> 下载 anoni-pin.ps1](https://raw.githubusercontent.com/anoni-net/docs/main/docs/_scripts/anoni-pin.ps1){ .btn } [<i data-icon="octicons-mark-github-24"></i> 在 GitHub 查看源代码](https://github.com/anoni-net/docs/blob/main/docs/_scripts/anoni-pin.ps1){ .btn }

先手动执行一次确认运作正常。PowerShell 默认会阻止脚本，`-ExecutionPolicy Bypass` 只对这一次执行放行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\anoni-pin.ps1
```

## 定时任务设置

文档站更新不频繁，每 6 小时执行一次已足够，想更快跟上新版可以缩短间隔。

=== "Linux / macOS"

    使用 cron，编辑定时表：

    ```bash
    crontab -e
    ```

    加入下列一行，每 6 小时执行一次并把输出写进 log：

    ```bash
    0 */6 * * * /path/to/anoni-pin.sh >> $HOME/.anoni-pin/log 2>&1
    ```

    需要在开机后补执行错过的任务时，可以改用 systemd timer 并设置 `Persistent=true`。

=== "Windows"

    使用「任务计划程序」，从命令行创建最快。以下设置每 6 小时执行一次：

    ```powershell
    schtasks /Create /TN "anoni-ipfs-pin" `
      /TR "powershell -NoProfile -ExecutionPolicy Bypass -File C:\Tools\anoni-pin.ps1" `
      /SC HOURLY /MO 6 /RL LIMITED
    ```

    把 `C:\Tools\anoni-pin.ps1` 换成实际存放的路径。也可以用任务计划程序的图形界面创建，「程序或脚本」填 `powershell`，「添加参数」填 `-NoProfile -ExecutionPolicy Bypass -File 你的路径`。

=== "Docker"

    定时任务依主机的操作系统设置（Linux、macOS 用 cron，Windows 用任务计划程序，见前两个分页），差别在执行脚本前需先设置 `IPFS_CMD`，例如包一层 wrapper：

    ```bash
    #!/usr/bin/env bash
    export IPFS_CMD="docker exec ipfs_host ipfs"
    exec /path/to/anoni-pin.sh
    ```

    cron 改为执行这支 wrapper 即可。

## pin 结果的验证

先解析出当前的 CID，再确认它在 pin 列表里：

```bash
CID=$(ipfs name resolve --nocache /ipns/k51qzi5uqu5dlfm2jj0f70ex3r3babmwy8qh071inwknttr7wqa3uhdwvlmrmw)
ipfs pin ls --type=recursive | grep "${CID#/ipfs/}"
```

也可以从本机网关打开 `http://127.0.0.1:8080${CID}/`，内容正常显示即代表 pin 成功。Docker 用户把上面的 `ipfs` 换成 `docker exec ipfs_host ipfs`，上方的 compose 示例没有对外开放 8080，用命令确认即可。

## 与社群节点的固定连接 { #peering }

pin 只需要 IPNS 名称，内容通过 DHT 查找。第一次下载整份镜像时，DHT 查询缓慢或查不到来源都会拖长时间。配置 kubo 的 peering，可以让节点与来源节点维持固定连接。

编辑 `~/.ipfs/config`，在最外层加入 `Peering` 区块：

```json
"Peering": {
  "Peers": [
    { "ID": "12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9" }
  ]
}
```

`Addrs` 可以省略，kubo 会自动向 DHT 查询地址。修改后重启 daemon 即生效。Docker 用户改的是 `./ipfs-data/config`，改完执行 `docker compose restart`。

确认是否已连上：

```bash
ipfs swarm peers | grep 12D3KooWEzvBhnLa6NZnjnw22Yoqs56xq4pNCZdkkxw5yxvi1eV9
```

peering 是单向配置，社群节点没有对应的条目，维持连接由你的节点负责。[kubo 的配置文档](https://github.com/ipfs/kubo/blob/master/docs/config.md#peering)里写到，单向 peering 会占用对方节点的连接资源，镜像数量增加之后负担会集中在同一台机器。目前提供者只有一台，第一次的 240 MB 都要从它下载，所以建议一开始就配置 peering。协助 pin 的节点变多、来源不再集中在同一台之后，再移除配置即可。

## 2026 年 9 月之后的 IPFS 维护变化 { #ipfs-maintenance-2026 }

Interplanetary Shipyard 是过去几年维护 IPFS 主要软件的团队，Protocol Labs 停止资助之后，Shipyard 在 [2026 年 9 月 30 日结束 IPFS 的工作](https://ipshipyard.com/blog/2026-the-end-of-ipfs-at-shipyard/)。本页的做法仍然可行，以下三项有所改变。

- **软件维护**：kubo、Helia、Boxo、IPFS Desktop、IPFS Companion 都已没有专职维护者，IPFS Foundation 改成对个别维护者发放 grant。程序继续运作，安全更新的节奏会变慢，安装前先确认版本的发布日期。
- **公共网关与 bootstrap 节点**：ipfs.io、dweb.link 与 IPFS 的 bootstrap 节点在同一天停止运营。kubo 0.38 之后 `Bootstrap` 的默认值是 `auto`，展开后的列表就包含这些节点。
- **本页的浏览网址**：旧的 `anoni-net.ipns.dweb.link` 属于 dweb.link，已换成社群自建的 [IPFS 网关](https://ipfs.anoni.net/)（`ipfs.anoni.net`）。两者读取同一个 IPNS 名称，通过 DNSLink 记录对应。pin 脚本使用 IPNS 名称，不受网关影响。

下列命令可以查看节点目前取得的 bootstrap 节点，以及已连上的 peer 数量：

```bash
ipfs config Bootstrap --expand-auto
ipfs swarm peers | wc -l
```

`auto` 展开的节点停止运营之后，新安装的节点可能无法加入 DHT。最直接的做法是把社群节点设为固定连接对象（见[与社群节点的固定连接](#peering)），`Peering` 只需要填 Peer ID。

## 维护与注意事项

- **版本更新**：文档站换了 CID 之后，下一次定时任务就会 pin 新版、放掉旧版，不需要人工处理。
- **差异下载**：pin 新版时旧版的区块仍在节点上，IPFS 只下载实际不同的区块。第一次要下载整份，之后一般的内容更新通常只有几 MB。改动导航栏或版式时例外，全站 HTML 会一起重写，差异接近镜像大小的一半。
- **硬盘用量**：脚本 unpin 旧版后会执行一次垃圾回收，只保留最新版本。一份完整镜像约 240 MB（2026 年 8 月实测）。
- **停止协助**：unpin 目前的版本并移除定时任务即可，不影响其他节点。
- **隐私与风险**：pin 的是公开文档，没有隐私上的顾虑。提供 IPFS pin 的风险依司法管辖而不同，相关限制见[去中心化网站发布](docs:advanced/dweb-ipfs-onion/)的「已知限制与风险」。

## pinning service 的替代做法

不想维护 daemon 与定时任务时，可以改用 [Pinata](https://www.pinata.cloud/)、[Storacha](https://storacha.network/) 这类 pinning service。手动 pin 时在服务的界面贴上当前的 CID，自动化则用服务的 API 写成定时任务，流程与本页的脚本相同（解析 IPNS 取得 CID，再交给服务 pin）。

代价是镜像的存续改为依赖第三方服务商，可以当作备用方案。要真正去中心化，自建节点仍是最直接的做法。

## 相关阅读

- [去中心化网站发布](docs:advanced/dweb-ipfs-onion/)：IPFS 与 Onion 服务的设计核心，以及文档站的实际部署
- [.onion 服务架设指南](/join/setup-onion-service/)：另一种抗封锁镜像的做法
- [Tor Relay 架设指南](/join/setup-tor-relay/)：用自己的机器与带宽增加 Tor 网络的中继节点
