---
title: 参与开发的环境准备
description: 参与文档站、Tor 中继节点观测（Pulse）与 OONI 观测覆盖率（ASN Coverage）开发前需要的账号与工具，包含 git、Python 3.12、uv 与编辑器的安装，以及从 fork 到提交 Pull Request 的流程。
---

anoni.net 的文档站、[Tor 中继节点观测](/projects/pulse/)（Pulse）与 [OONI 观测覆盖率](/projects/asn-coverage/)（ASN Coverage）都放在 GitHub 的 [anoni-net 组织](https://github.com/anoni-net)，各自一个 repo（`docs`、`pulse`、`asn-coverage`），用 git 做版本控制，通过 Pull Request 接受贡献。

## 需要的账号与工具

- 一个 [GitHub 账号](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)
- 本机安装 git、Python、uv 与一个编辑器（安装方式见下一节）

没用过 git 或 GitHub 也能参与，需要先熟悉的只有一条流程，依次是 fork 别人的 repo、开分支、commit、提交 PR。下面几份入门资料都涵盖这段流程。

!!! info "git 与 GitHub 入门"

    - [什么是 Git？为什么要学习它？- 为你自己学 Git](https://gitbook.tw/chapters/introduction/what-is-git)
    - [Git 基础要点 - Git 官方文档](https://git-scm.com/book/zh-cn/v2/%E5%BC%80%E5%A7%8B-Git-%E5%9F%BA%E7%A1%80%E8%A6%81%E7%82%B9)
    - [如何 Fork 一个项目](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
    - [如何在 GitHub 上编辑文件](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
    - [如何创建 Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
    - [为你自己学 Git](https://gitbook.tw/)，完整的 git 教程（正体中文）

## 开发环境安装

### Python

Pulse 与 ASN Coverage 都用 Python 开发，文档站的构建脚本也是，三个 repo 都要求 Python 3.12 以上。还不熟悉 Python 的话，可以参考[为你自己学 Python](https://pythonbook.cc/)（正体中文）。

!!! tip "各平台的安装方式"

    === "Windows"

        1. 从 [Python 官方网站](https://www.python.org/)下载安装程序。
        2. 运行安装程序，第一个界面务必勾选 "Add Python to PATH"，把 Python 加入系统的环境变量。要查看或修改安装选项时选 "Customize installation"，使用默认值则直接点击 "Install Now"。
        3. 打开命令提示符（Command Prompt），输入 `python --version` 或 `python`。安装成功会显示版本号，确认版本在 3.12 以上。

    === "macOS"

        1. 建议用 Homebrew 安装，在终端（Terminal）输入 `brew install python`。还没有 Homebrew 的话需先安装。
        2. 也可以从 [Python 官方网站](https://www.python.org/)下载 macOS 版的 `.pkg` 文件，按照引导安装。
        3. 在终端输入 `python3 --version`，确认版本在 3.12 以上。

    === "Linux"

        1. 以 Ubuntu 为例，在终端先执行 `sudo apt update` 更新包列表，再执行 `sudo apt install python3` 安装。
        2. 在终端输入 `python3 --version`，确认版本在 3.12 以上。

### uv

[uv](https://docs.astral.sh/uv/) 是 Python 的包与虚拟环境管理工具，anoni.net 各项目统一用它管理依赖。在 repo 的目录执行 `uv sync`，会创建隔离的虚拟环境并安装所有包，各项目的依赖不会互相冲突。安装方式见 [uv 的官方文档](https://docs.astral.sh/uv/getting-started/installation/)。

### 编辑器

[Visual Studio Code](https://code.visualstudio.com/)（VS Code）是微软开发的跨平台编辑器，内置 Git 支持，扩展也涵盖各项目会用到的 Python 与 Markdown。已经有惯用的编辑器就继续使用，VS Code 只是给没有偏好的人参考。

## Fork 与 Pull Request 的流程

Fork 会把别人的 repo 复制一份到自己的 GitHub 账号，修改与实验都不会影响原始项目。没有原始 repo 写入权限的人，一般都用这个方式参与开源项目。

登录 GitHub 后打开要参与的 repo，点击右上角的 "Fork" 按钮，GitHub 会把 repo 复制到你的账号下。

Fork 完成后把 repo clone 到本地，再开一个新分支，修改就不会动到主分支。以文档站的 `docs` 为例：

```bash
git clone https://github.com/<你的账号>/docs.git
cd docs
git checkout -b 新分支名称
```

在新分支上修改完成后，把变更暂存并 commit 到本地的 repo：

```bash
git add .
git commit -m "你的修改描述"
```

再把分支推送到 GitHub 上你 fork 的 repo：

```bash
git push origin 新分支名称
```

推送之后，你的 repo 页面会出现 "Compare & pull request" 按钮。点击后填写修改的内容与原因，再按 "Create pull request" 提交。项目维护者审阅之后，会把修改合并进主线。

## 相关阅读

- [ASN 观测数据的提取与分析](/projects/asn-coverage/howto/)：OONI 观测覆盖率命令行工具的配置与用法
- [贡献者百科](docs:community/contributor-handbook/)：文档站的文件命名、PR 流程与翻译规范
- [自我技能评估表](docs:community/skill-level/)：按自己对 Tor、Tails、OONI 的了解程度，决定从哪里开始
- [参与](/join/)：加入匿名网络社区的方式，以及遇到问题时的联系渠道
