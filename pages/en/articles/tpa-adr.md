---
title: The Tor Sysadmin Team's Switch to Architecture Decision Records
description: A summary of why Tor's system administration team (TPA) replaced RFCs with ADRs, a comparison with how other open source projects record decisions, and notes on decision records in Taiwan's projects and communities.
date: 2026-03-19
---

Most projects have some way of making decisions, and far fewer have a way of finding out, a year later, why a decision was made. The Tor Project's system administration team (TPA) rebuilt its process around that second problem, and the result is small enough for a volunteer project to copy.

## The Changes at TPA

TPA described the switch from its RFC process to Architecture Decision Records (ADRs) in [Keeping track of decisions using the ADR model](https://blog.torproject.org/tpa-adr/), published on the Tor Project blog on 16 February 2026. What follows is our summary of that post; the Chinese versions of this page carry a full translation. The change applies only to TPA, and other teams at Tor keep their own processes. The new process has three parts.

### A Five-Heading Template

The template (ADR-100) is a variant of the [Nygard template](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/locales/en/templates/decision-record-template-by-michael-nygard/index.md) with five headings: Context, Decision, Consequences, More Information (optional), and Metadata. The metadata lists status, decision date, decision makers, who was consulted, who must be informed, and a link to the discussion. The old RFC template had 17 headings and produced long documents. Pricing, brainstorming and detailed comparisons of alternatives now go into the GitLab discussion issue, which keeps the record itself short.

### A Short Process with a Named Decision Maker

Major decisions are presented to stakeholders in a meeting and smaller ones by email, with a delay before adoption so people can send final comments. The key element is what Jacob Kaplan-Moss calls the [one weird trick](https://jacobian.org/2023/dec/5/how-to-decide/): decide who decides. Each record names its stakeholders in three roles aligned with the [RACI matrix](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix): informed (previously "affected users"), consulted (previously undefined), and decision maker (replacing a vague "approval"). Defining who is consulted is also meant to curb [bike-shedding](https://en.wikipedia.org/wiki/Bike_shedding), where too many people weigh in on trivial points.

### Communication Kept Apart from the Record

Under ADR-102, making and recording a decision is kept separate from communicating it, because TPA found that one document could not serve both. There is no fixed template for announcements; the team suggests the [Five Ws](https://en.wikipedia.org/wiki/Five_Ws).

### Reasons for the Switch

TPA first came across ADRs in the [Thunderbird for Android project](https://github.com/thunderbird/thunderbird-android/blob/be2af5c6a0bce08385fc3f654c1185ccf9db3859/docs/architecture/adr/README.md), while also reviewing Kaplan-Moss's [case against RFCs](https://jacobian.org/2023/dec/1/against-rfcs/): RFC processes have no decision-making framework, tend toward endless discussion, reward whoever can write to exhaustion, and ignore expertise and power dynamics. The author admits to many of these, including proposals adopted out of exhaustion. Even so, the team documented 95 RFCs over six years under the old process. The post itself came out a few months after the switch, which the team gives as an example of how easily the separate communication step slips.

## Decision Records in Other Open Source Projects

The comparison below is ours and is not part of the TPA post.

- **GOV.UK Design System** uses RFCs to discuss proposals and ADRs to record the final decision. Its first proposal, [001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions](https://github.com/alphagov/govuk-design-system-architecture/blob/main/proposals/001-use-rfcs-and-adrs-to-discuss-proposals-and-record-decisions.md), sets out that split.
- **Bitwarden** keeps an [ADR index](https://contributing.bitwarden.com/architecture/adr/) in its contributor documentation, and ADRs are its main record of architectural decisions.
- **GitLab**'s Delivery group keeps ADRs in its public handbook under [Delivery Decisions](https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/gitlab-delivery/decisions/) (checked October 2026).
- **[adr.github.io](https://adr.github.io/)** maintains MADR (Markdown Architectural Decision Records), a lightweight general-purpose template with supporting tools.
- **Rust** proposes and discusses language and standard library changes through numbered [RFCs](https://github.com/rust-lang/rfcs), and the outcome stays in the same repository.
- **Python** uses [PEPs](https://peps.python.org/) (Python Enhancement Proposals) as the formal, numbered proposal mechanism for the language and standard library.
- **Kubernetes** uses [KEPs](https://github.com/kubernetes/enhancements) (Kubernetes Enhancement Proposals) for features and architectural changes.

GOV.UK runs RFC-style discussion and ADR-style records side by side, Bitwarden and now TPA rely mainly on ADRs, and large ecosystems use numbered proposals with their own traditions. Two parts of TPA's approach stand out: naming the decision maker explicitly, and keeping the decision record separate from the announcement. Both carry over to projects that never adopt the ADR name.

## Decision Records in Taiwan's Projects and Communities

We are a community based in Taiwan, and most projects we know there already have a way to propose, discuss and reach consensus. Few of them publish their decisions in an `adr/` directory or a MADR template.

- **Civic tech communities such as g0v** work through proposal documents, shared [HackMD notes](https://g0v.hackmd.io/@jothon/intro), hackathons and online meetings, as described in the [g0v collaboration guide](https://g0v.hackmd.io/@jothon/g0v-cowork-guideline/). Architectural decisions end up spread across notes, issues, pull requests, slides and hackathon proposals, and after a while the reasoning is hard to reconstruct.
- **Government and public-sector projects** produce specifications, design documents and final reports written at milestones, which do not accumulate into a running log. Many are not fully public, so outside contributors cannot see the trade-offs.
- **Open source projects from local companies** sometimes keep decision records or design documents in internal knowledge bases. The public repository has the code but not the history behind it.

What these projects lack is a record of decisions that stays stable, can be traced, and makes sense to someone from outside. One short file per decision, stating why it was made, avoids the pressure to write a large specification and lasts longer than a discussion buried in an issue tracker. A newcomer can read the records and see why the system looks the way it does without reopening settled debates.

Our own [governance charter](/about/governance/), still a draft, has a table in its decision-making section that maps each scope of change to a proposal channel and a decision method. Structural changes, for example, are discussed in a Matrix room before a pull request and given a three-day window, while policy changes to self-hosted services are decided by core-member consensus. The table answers TPA's question of who decides. The charter does not yet say what record a decision should leave behind, and a one-file-per-decision template like TPA's could fill that gap.

TPA is still collecting feedback on the new process in its [discussion issue](https://gitlab.torproject.org/tpo/tpa/team/-/issues/41428).
