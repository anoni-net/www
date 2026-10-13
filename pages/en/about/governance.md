---
title: Governance Charter
description: 'The anoni.net governance charter: member roles, consensus and voting, dispute resolution, the code of conduct, and the amendment process.'
---

!!! warning "Draft, under community review"

    This charter is still a draft. It has not yet been formally ratified by community partners, and clauses may change at any time. Until it is ratified, the community works from this draft and resolves disputes by it. Ideas are welcome in the Matrix public rooms or as GitHub issues (the process is under [Charter amendments](#Charter-amendments)).

Once a community grows past a certain size, its way of making decisions needs to be written down so the same basic principles are not re-argued every time. This charter sets out anoni.net's member roles, decision-making, dispute resolution, and code of conduct. It is a living document, and significant changes are discussed openly in Matrix before any revision is merged.

First-time participants can skim the [Roles](#Roles) and [Code of conduct](#Code-of-conduct) sections for the basic expectations of members. Long-time members, proposal authors, and core members who handle disputes should read it through once.

## Scope

This charter applies to collaboration and interaction within:

- The anoni.net documentation site (zh-TW, zh-CN, en)
- Our self-hosted infrastructure: the Matrix homeserver `im.anoni.net`, CryptPad, Etherpad, Send, SearXNG, and Formbricks
- Workshops, meetups, and conference sessions held under the anoni.net name
- Representing anoni.net when collaborating with international organizations such as EFF, the Tor Project, and OONI
- Pull requests, issues, and discussions in the community's GitHub repositories

What members say or do as individuals on outside platforms is outside its scope, but conduct inside anoni.net spaces must follow this charter.

## Roles

The community keeps its role system low in formality, so that hierarchy does not alienate newcomers. The practical differences between roles are at the account level (who can merge a PR, who reviews Matrix account requests), not in how much anyone's voice counts.

### Core members

Core members have worked on operations over the long term and earned enough technical and community trust. They are responsible for:

- Operating the self-hosted services and reviewing account requests
- Merge authority on the GitHub repositories
- Representing anoni.net in dealings with international organizations
- Final review of proposed charter amendments
- Handling disputes that involve breaches of the code of conduct

New core members are added by consensus of the existing core members. There is currently no public application process.

### Contributors

Contributors are members with concrete output, such as articles, translations, code, event organizing, design, or research, and they take part actively in the relevant rooms of the Matrix Public Space.

How to join: claim a topic on the [Take part](/join/) page, open a PR, or help organize an event. There is no formal barrier to entry.

### Observers

Observers subscribe to the newsletter and join the Public Space but do not yet have concrete output. The community works asynchronously and does not expect everyone to be active, so observers are equally welcome.

### Visitors

Visitors have not joined Matrix, and follow the community by reading the documentation and blog or by writing in. Messages to <whisper@anoni.net> are handled by core members on rotation.

### Moving between roles

The roles describe activity, not rank. A visitor who joins Matrix and starts participating becomes an observer or contributor without any formal step. A contributor moves toward core membership through sustained work and trust, and is added by consensus of the current core members. Nobody is required to move: an observer who only wants to follow along is welcome to stay one.

## Decision-making

### Consensus by default

The community makes decisions by consensus. Consensus here means that no relevant member objects; it does not require unanimous agreement. The process:

1. The proposer raises the proposal in the relevant Matrix room, with context and options.
2. Anyone with concerns has at least 3 days to respond.
3. If no objection is raised, the proposal passes.
4. If there is an objection, discussion continues until both sides reach a version they can accept.

Most content, process, and design decisions go through this process.

### Voting as the exception

Voting only happens when consensus is clearly stuck, or when time pressure calls for a fast conclusion. Conditions:

- Initiated by at least two core members
- Eligible voters: all contributors (members with concrete output in the last 6 months)
- Method: a public Matrix poll, or a semi-anonymous CryptPad form
- Passing threshold: a simple majority (more than half)
- Major decisions (charter amendments, adding or removing a core member) require a 2/3 majority of active contributors

So far the community has rarely needed to vote, and consensus resolves most situations.

### Proposal channels

| Scope of impact | Proposal channel | Decision method |
|---|---|---|
| Single-article content, translation word choice | GitHub PR or Matrix room | consensus in review |
| Structural change (navigation, moving files, renaming) | Discuss in a Matrix room first, then open a PR | consensus, 3-day window |
| Adding, removing, or changing policy on a self-hosted service | Core Matrix room and public room in parallel | core-member consensus |
| Charter and code-of-conduct amendments | GitHub issue and Matrix in parallel | consensus, at least 7-day window |
| Public positions (statements, protests, letters of support) | Matrix public room | core members plus a majority of contributors |

## Dispute resolution

Disputes fall into two kinds. Substantive disputes are about how to do something, and interpersonal disputes involve conflict between people or a breach of the code of conduct.

### Substantive disputes

Substantive disputes follow the ordinary proposal process: raise the disagreement in Matrix, lay out both sides' arguments, and look for consensus. If no consensus emerges, the question goes to a vote. Technical disputes can stay open while each side experiments, and are re-evaluated on the results after a while.

### Interpersonal disputes

Conflicts between members are triaged by severity:

1. **Minor misunderstanding**: the members involved can sort it out privately.
2. **Clear breach of the code of conduct**: the affected party can report it to core members, who help resolve it (a private conversation, a public warning, temporary isolation).
3. **Serious incident** (harassment, stalking, physical threats): core members immediately remove the offending member's access, give a brief account of the response in a public room afterward without revealing the affected party's identity, and help the affected party contact authorities or support resources as needed.

Disputes that involve a core member are handled by the other core members, who may invite outside arbitration where necessary.

## Code of conduct

### Principles of interaction

- **Mutual respect**: members of different backgrounds, technical levels, and political views are treated alike.
- **Ideas, not people**: critique proposals, not identities.
- **Good faith**: start from the assumption that the other person's proposal is well-intentioned, then discuss the details.
- **Transparency**: keep relevant decisions in public rooms where possible, and sync the outcome of private coordination back to a public room afterward.
- **Newcomer-friendliness**: stay patient with basic questions and break down complex context clearly.

### The lawful-use precondition

All collaboration and discussion presumes lawful use. The community does not assist with, or provide instruction for, any of the following:

- Money laundering, tax evasion, or sanctions evasion
- Harassment, stalking, physical threats, or unauthorized intrusion
- Distribution of child sexual abuse material (CSAM), human trafficking, or drug trafficking
- Intelligence gathering against, or interference in the internal affairs of, another state's citizens (foreign-state intelligence operations)

Anonymity and privacy tools are used by all kinds of people. The community promotes them to journalists, civil-society groups, researchers, and individuals who need to protect themselves. If a collaborator turns out to have any of the unlawful intents above, the community ends the collaboration immediately.

### Sensitive information

- Content involving personal data, unpublished research, or sensitive victim identities goes through [Sending Us Sensitive Material](/join/upload-sensitive/).
- Do not post victims' personal data or unpublished source material directly in public rooms.
- When citing sensitive reporting, keep the original author and source, and do not summarize sensitive details without authorization.

### Public representation

Representing anoni.net publicly (media interviews, event remarks, community accounts) requires:

- Not advancing political positions that the community has not discussed
- Getting a member's consent before quoting their private opinion
- Syncing in Matrix before negotiating with international organizations (EFF, the Tor Project, OONI)

Members speaking as individuals note that it is "a personal position, not the community's."

## Enforcement

Responses to a breach of the code of conduct are decided by core members case by case, from lightest to most severe:

1. **Private reminder**: a core member sends a private note, with no public record.
2. **Public warning**: the breach is recorded openly in the relevant Matrix room.
3. **Temporary isolation**: Matrix account, CryptPad access, and GitHub permissions are suspended for days to weeks.
4. **Permanent removal**: revocation of all self-hosted-service accounts, the collaboration relationship, and eligibility to take part in community activities.

In deciding a response, core members weigh the severity of the breach, whether it is a repeat offense, and the person's attitude. The decision in a serious incident is briefly described in a public room without revealing the affected party's identity.

## Charter amendments

This charter is a living document, and anyone can propose an amendment. The process:

1. Open a GitHub issue describing what should change and why.
2. Post a notice in the Matrix public room at the same time.
3. Allow a discussion period of at least 7 days.
4. Once consensus is reached, a core member merges the change into `main` and posts a short note on the blog explaining it.

In an emergency (for example, a new form of harassment that calls for an immediate update to the enforcement principles), core members may update the charter on a temporary basis, and return to the regular process for review within 7 days.

## Related documents

- [Writing Style](/join/writing-style/): sentence patterns, punctuation, terminology, and translation rules shared by the three sites
- [Contributor Handbook](docs:community/contributor-handbook/): file naming, the PR workflow, and issue labels on the docs site
- [Take part](/join/): the entry path for first-time participants
- [Sending Us Sensitive Material](/join/upload-sensitive/): how sensitive material is handled
- [Services](/services/): entry points and account requests for Matrix, CryptPad, and the other self-hosted services
