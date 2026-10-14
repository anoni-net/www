---
title: 參與開發的環境準備
description: 參與文件站、Tor 中繼節點觀測（Pulse）與 OONI 觀測涵蓋率（ASN Coverage）開發前需要的帳號與工具，包含 git、Python 3.12、uv 與編輯器的安裝，以及從 fork 到發 Pull Request 的流程。
---

anoni.net 的文件站、[Tor 中繼節點觀測](/projects/pulse/)（Pulse）與 [OONI 觀測涵蓋率](/projects/asn-coverage/)（ASN Coverage）都放在 GitHub 的 [anoni-net 組織](https://github.com/anoni-net)，各自一個 repo（`docs`、`pulse`、`asn-coverage`），用 git 做版本控制，透過 Pull Request 接受貢獻。

## 需要的帳號與工具

- 一個 [GitHub 帳號](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)
- 本機安裝 git、Python、uv 與一個編輯器（安裝方式見下一節）

沒用過 git 或 GitHub 也能參與，需要先熟悉的只有一條流程，依序是 fork 別人的 repo、開分支、commit、發 PR。下面幾份入門資料都涵蓋這段流程。

!!! info "git 與 GitHub 入門"

    - [什麼是 Git？為什麼要學習它？ - 為你自己學 Git](https://gitbook.tw/chapters/introduction/what-is-git)
    - [Git 基礎要點 - Git 官方文件](https://git-scm.com/book/zh-tw/v2/%E9%96%8B%E5%A7%8B-Git-%E5%9F%BA%E7%A4%8E%E8%A6%81%E9%BB%9E)
    - [如何 Fork 一個專案](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
    - [如何在 GitHub 上編輯檔案](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
    - [如何建立 Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
    - [為你自己學 Git](https://gitbook.tw/)，完整的 git 正體中文教學

## 開發環境安裝

### Python

Pulse 與 ASN Coverage 都用 Python 開發，文件站的建置腳本也是，三個 repo 都要求 Python 3.12 以上。還不熟悉 Python 的話，可以參考[為你自己學 Python](https://pythonbook.cc/)。

!!! tip "各平台的安裝方式"

    === "Windows"

        1. 從 [Python 官方網站](https://www.python.org/)下載安裝程式。
        2. 執行安裝程式，第一個畫面務必勾選 "Add Python to PATH"，把 Python 加進系統的環境變數。要檢視或修改安裝選項時選 "Customize installation"，使用預設值則直接點選 "Install Now"。
        3. 開啟命令提示字元（Command Prompt），輸入 `python --version` 或 `python`。安裝成功會顯示版本號，確認版本在 3.12 以上。

    === "macOS"

        1. 建議用 Homebrew 安裝，在終端機（Terminal）輸入 `brew install python`。還沒有 Homebrew 的話需先安裝。
        2. 也可以從 [Python 官方網站](https://www.python.org/)下載 macOS 版的 `.pkg` 檔案，依照引導安裝。
        3. 在終端機輸入 `python3 --version`，確認版本在 3.12 以上。

    === "Linux"

        1. 以 Ubuntu 為例，在終端機先執行 `sudo apt update` 更新套件清單，再執行 `sudo apt install python3` 安裝。
        2. 在終端機輸入 `python3 --version`，確認版本在 3.12 以上。

### uv

[uv](https://docs.astral.sh/uv/) 是 Python 的套件與虛擬環境管理工具，anoni.net 各專案統一用它管理相依套件。在 repo 的目錄執行 `uv sync`，會建立隔離的虛擬環境並安裝所有套件，各專案的相依套件不會互相衝突。安裝方式見 [uv 的官方文件](https://docs.astral.sh/uv/getting-started/installation/)。

### 編輯器

[Visual Studio Code](https://code.visualstudio.com/)（VS Code）是微軟開發的跨平台編輯器，內建 Git 支援，擴充套件也涵蓋各專案會用到的 Python 與 Markdown。已經有慣用的編輯器就繼續使用，VS Code 只是給沒有偏好的人參考。

## Fork 與 Pull Request 的流程

Fork 會把別人的 repo 複製一份到自己的 GitHub 帳號，修改與實驗都不會影響原始專案。沒有原始 repo 寫入權限的人，一般都用這個方式參與開源專案。

登入 GitHub 後開啟要參與的 repo，點選右上角的 "Fork" 按鈕，GitHub 會把 repo 複製到你的帳號底下。

Fork 完成後把 repo clone 到本機，再開一個新分支，修改就不會動到主分支。以文件站的 `docs` 為例：

```bash
git clone https://github.com/<你的帳號>/docs.git
cd docs
git checkout -b 新分支名稱
```

在新分支上修改完成後，把變更暫存並 commit 到本機的 repo：

```bash
git add .
git commit -m "你的修改描述"
```

再把分支推送到 GitHub 上你 fork 的 repo：

```bash
git push origin 新分支名稱
```

推送之後，你的 repo 頁面會出現 "Compare & pull request" 按鈕。點選後填寫修改的內容與原因，再按 "Create pull request" 送出。專案維護者審閱之後，會把修改合併進主線。

## 相關閱讀

- [ASN 觀測資料的擷取與分析](/projects/asn-coverage/howto/)：OONI 觀測涵蓋率命令列工具的設定與用法
- [貢獻者百科](docs:community/contributor-handbook/)：文件站的檔案命名、PR 流程與翻譯規範
- [自我技能評估表](docs:community/skill-level/)：依自己對 Tor、Tails、OONI 的了解程度，決定從哪裡開始
- [參與](/join/)：加入匿名網路社群的方式，以及遇到問題時的聯絡管道
