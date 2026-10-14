---
title: Development Environment Setup
description: The accounts and tools needed before contributing to the docs site, Tor Relay Watch (Pulse) and OONI Coverage (ASN Coverage), including installing Git, Python 3.12, uv and an editor, and the workflow from a fork to a pull request.
---

anoni.net's documentation site, [Tor Relay Watch](/projects/pulse/) (Pulse) and [OONI Coverage](/projects/asn-coverage/) (ASN Coverage) live in the [anoni-net organisation](https://github.com/anoni-net) on GitHub, one repository each (`docs`, `pulse`, `asn-coverage`). They use Git for version control and take contributions through pull requests.

## Accounts and Tools

- A [GitHub account](https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github)
- Git, Python, uv and an editor installed locally (installation is covered in the next section)

You can contribute without prior Git or GitHub experience. The one workflow to learn is: fork someone's repository, create a branch, commit, open a pull request. The references below all cover it.

!!! info "Git and GitHub basics"

    - [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics) from the official Pro Git book
    - [Fork a repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
    - [Editing files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files)
    - [Creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
    - [為你自己學 Git](https://gitbook.tw/), a full Git tutorial in Traditional Chinese

## Development Environment

### Python

Pulse and ASN Coverage are written in Python, as are the documentation site's build scripts, and all three repositories require Python 3.12 or newer. [為你自己學 Python](https://pythonbook.cc/), in Traditional Chinese, is a good introduction if the language is new to you.

!!! tip "Installation by platform"

    === "Windows"

        1. Download the installer from [python.org](https://www.python.org/).
        2. Run it, and make sure "Add Python to PATH" is checked on the first screen so Python is added to the system environment variables. Choose "Customize installation" to review or change the options, or "Install Now" for the defaults.
        3. Open Command Prompt and run `python --version` or `python`. A successful install prints the version number; check that it is 3.12 or newer.

    === "macOS"

        1. Homebrew is the recommended route: open Terminal and run `brew install python`. Install Homebrew first if you do not have it.
        2. Alternatively, download the macOS `.pkg` installer from [python.org](https://www.python.org/) and follow the prompts.
        3. Run `python3 --version` in Terminal and check that the version is 3.12 or newer.

    === "Linux"

        1. On Ubuntu, run `sudo apt update` to refresh the package list, then `sudo apt install python3`.
        2. Run `python3 --version` and check that the version is 3.12 or newer.

### uv

[uv](https://docs.astral.sh/uv/) manages Python packages and virtual environments, and every anoni.net project uses it for dependencies. Running `uv sync` in a repository's directory creates an isolated virtual environment and installs every package that project needs, so dependencies never collide between projects. See the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/) for installation.

### Editor

[Visual Studio Code](https://code.visualstudio.com/) (VS Code) is a cross-platform editor from Microsoft with built-in Git support, and its extensions cover Python and Markdown, the formats these projects use. If you already have an editor you like, keep using it; VS Code is only a suggestion for people without a preference.

## Fork and Pull Request Workflow

A fork copies someone else's repository into your own GitHub account, so you can change and experiment with it without affecting the original. It is the usual way to contribute to an open-source project you do not have write access to.

Log into GitHub, open the repository you want to work on, and click **Fork** in the upper right. GitHub copies the repository to your account.

Clone your fork locally, then create a branch so your work stays off the main branch. Using the documentation site's `docs` repository as the example:

```bash
git clone https://github.com/<your-username>/docs.git
cd docs
git checkout -b your-branch-name
```

When your changes on the branch are done, stage and commit them to your local repository:

```bash
git add .
git commit -m "A short description of your change"
```

Then push the branch to your fork on GitHub:

```bash
git push origin your-branch-name
```

Your repository page will then show a **Compare & pull request** button. Click it, describe what you changed and why, and click **Create pull request** to submit. A maintainer reviews the change and merges it into the main line.

## Related Reading

- [ASN Observation Data Retrieval and Analysis](/projects/asn-coverage/howto/): setup and usage of the OONI Coverage command-line tool
- [Contributor handbook](docs:community/contributor-handbook/): file naming, the PR process and translation guidelines for the docs site
- [How to Contribute](docs:community/how-to-contribute/): the practical mechanics of getting a change accepted
- [Self-skills evaluation form](docs:community/skill-level/): work out where to start based on how well you know Tor, Tails and OONI
- [Take part](/join/): how to join the community, and how to reach us if you get stuck
