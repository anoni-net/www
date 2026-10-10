---
title: OONI 观测覆盖率
description: 台湾与邻近地区的 OONI 测量来自哪些网络、覆盖多少用户，以及哪些网络还没有任何测量。
lead: 网络审查的观测只覆盖有人运行 OONI Probe 的网络。
---

OONI 的网络审查测量来自志愿者在自己的网络上运行 OONI Probe。同一个地区里，不同的电信商与网络（ASN，自治系统编号）可能各自封锁不同的网站，只有一两家电信商的测量时，其他网络上的封锁不会被记录下来。页面把 OONI 的测量数跟 APNIC 估计的各网络用户人数放在一起，看测量覆盖多少用户、集中在哪几个网络，以及有哪些网络还没有任何测量。

页面每小时重新生成，OONI 的测量每六小时读取一次。默认显示台湾，其他地区作为参照，从下方的地区列表切换。

<!-- asn-coverage -->

## 数据的计算方式

- 测量数来自 [OONI 的汇总 API](https://api.ooni.io/)，包含所有测试项目，依测量开始的日期（UTC）分天
- 各网络的用户人数是 [APNIC 的估计](https://stats.labs.apnic.net/aspop/)，从网页广告的抽样测量推算，每周更新
- 网络名称来自 APNIC 与 RIPE NCC 的 ASN 名称表
- 一个网络只要有一笔测量就算有测量，测得够不够多要另外看测量占比与天数
- 没有测量的日子在图上留下缺口，不补值

## 参与测量的方式

- 安装 [OONI Probe](https://ooni.org/install/)，在自己的网络上运行测试，手机与电脑都可以。移动网络与家用宽带通常是不同的 ASN，两边都测更好
- 社区维护的 OONI Run 链接 `10328` 点一次就完成设置，安装前的风险前提与列表内容见 [OONI Run v2 操作说明](docs:tools/ooni-run-v2/)
- [ASN 自治网络观测数据分析](docs:taiwan/ooni-asn-coverage/)：为什么要关注网络的多样性，以及如何解读单笔测量
- [ASN Coverage](https://github.com/anoni-net/asn-coverage)：下载原始测量、分析网络类型与封锁方式的命令行工具
