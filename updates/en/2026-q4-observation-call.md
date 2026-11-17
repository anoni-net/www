---
title: Call for talks and organizers for the December observation meetup, Q4 2026
description: We are planning a December meetup and a mobile measurement week, and are looking for talks on anonymity and privacy and for people to help organize them.
date: 2026-11-17
kind: update
---

We are anoni.net, a community based in Taiwan that started from anonymity and network measurement tools such as Tor (the onion routing network) and OONI (the Open Observatory of Network Interference). Our work has since grown to include watching censorship and privacy issues in Taiwan and across Asia, and building tools and projects such as our monitoring pages, quarterly reports and the [Privacy Mysteries](https://anoni.net/mystery/) game. In December we want to hold an observation meetup, and we are looking for talks on anonymity and privacy and for people to help organize it. Backgrounds in the humanities and social sciences, law, journalism, design and technology are all welcome.

In the same month we also want to run a mobile measurement week. In Taiwan 45% of internet users are on mobile networks, yet only about 4% of OONI measurements come from them, so if something is blocked on a mobile network there are very few records of it. Anyone in Taiwan with a Chunghwa Telecom or Far EasTone mobile number can add a measurement in a few minutes by opening one link.

This post also covers other ways to take part, including development and data analysis and running a Tor relay (a volunteer server that carries traffic for Tor users). The results will go into the second [quarterly report](/projects/reports/) in January 2027. It is written for readers in Taiwan, Hong Kong, Macau and anywhere else.

!!! tip "Where to start"

    - You would like to give a talk on anonymity or privacy, or spend 10 minutes on something you have been following: submit by 30 November, see [talk topics](#talks)
    - You can help organize the measurement week or the meetup in December: reply by 30 November, see [organizing help](#organizers)
    - You are in Taiwan with a Chunghwa Telecom or Far EasTone mobile number: open our [OONI Run link `10328`](https://run.ooni.org/v2/10328) (a link that adds a list of tests to OONI Probe in one tap), and follow the three steps under [mobile network measurements](#mobile)
    - You write code or analyse data: see [development and data analysis](#development)
    - You are outside Taiwan: read the risks under [readers outside Taiwan](#outside-taiwan) first, then decide whether to take part

    If you already run a Tor relay or want to set one up, see [running and setting up relays](#relays).

## The December meetup and measurement week

We want to hold an observation meetup in Taipei with several talks on anonymity and privacy, a walk through the monitoring pages, and time to set up relays or bridges and install OONI Probe on the spot. In the same month we want to run a mobile measurement week, asking people to run OONI Probe on their phones during one week so the quarterly report can compare the figures before and after. The two can be combined. Dates and format depend on how many speakers and organizers join, and are not fixed yet. The machines, connections and running order for the meetup will be planned together with the people who sign up.

!!! note "Venue still needed"

    We are still looking for a venue in Taipei. If we cannot find one, the meetup will run fully online through Jitsi. If you can offer a venue, please mention it when you sign up.

### Talk topics for the meetup {#talks}

Talks come in three lengths, 10, 20 and 30 minutes, and the audience will be a mix of technical and non-technical people. You do not need to know anything about Tor relays or OONI to submit, and first-time speakers are welcome.

- **10 minutes**: one thing you have been following, something you have noticed, or research in progress. It does not need a conclusion, and anyone interested can gather afterwards to keep talking
- **20 minutes**: experience with one topic or an introduction to a project, such as outreach work or how you actually use a privacy tool
- **30 minutes**: a topic that needs fuller treatment, such as findings from a study, an analysis of censorship measurements, or experience running digital security training

Topics should relate to anonymity and privacy. Some directions are below, and related topics are welcome too:

- Work and events that bring anonymity and privacy to a general audience, such as games, illustrated guides and workshops. Our [Privacy Mysteries](https://anoni.net/mystery/) game is one example, where players act as investigators and find the privacy leaks hidden in photos, letters and websites
- Social science, legal or media research on surveillance, censorship and privacy, such as interviews or fieldwork on chilling effects
- How privacy tools are used in reporting, advocacy, software development or daily life
- Experience teaching digital security and running training
- Internet freedom and censorship in Taiwan, Hong Kong and elsewhere
- Analysis of measurement data, or how measurement tools and privacy projects were built
- Experience running Tor relays, bridges or Snowflake

The meetup will not be recorded. Speakers may use a pseudonym or stay anonymous. Speakers who cannot attend in person can present over Jitsi, which runs in a browser with no account needed, and they can keep their camera off.

### Organizing help {#organizers}

For the measurement week:

- Run the steps once on a Chunghwa Telecom or Far EasTone number to check them and the data use, if you have a number with either carrier
- Make step-by-step graphics and share them in your own circles, if you design or have channels to share in
- After the week, work through the public OONI data with us, comparing measurement counts before and after and charting them, if you are interested in data

For the meetup:

- Offer a venue in Taipei (we are still looking), or host a session in another city, if you have access to a space
- Invite speakers from different fields, or take notes on the discussion at the meetup, if you know research, advocacy or community events
- Help people set up relays or bridges and install OONI Probe on the day, if you have run a relay yourself
- Use Jitsi to let people join remotely (no recording), if you are comfortable with online meeting tools

No previous experience organizing events is needed.

### How to submit or sign up

Write to <whisper@anoni.net> by 30 November, or leave a message in our [Matrix Public Space](https://matrix.anoni.net/#/room/%23community:im.anoni.net). For a talk, include a title, a three-to-five sentence summary, whether you want 10, 20 or 30 minutes, and whether you would present in person or online. One or two sentences are enough for a 10-minute talk. To help organize, say which tasks you would like to take on. In both cases, tell us which times in December suit you. If you want to submit anonymously, use email: the Matrix Public Space is a public room, and every member can see the messages. You can write from an address not tied to your real identity, and encrypt the message with the [PGP key on our contact page](/contact/#pgp).

We will reply within a week, then open an organizing room on Matrix to divide up tasks and plan the programme, with a community member as the point of contact. The measurement week needs some time after it for comparison, so it has to happen in early to mid December. We will announce the dates and programme in community updates and the newsletter once they are set.

## Mobile network measurements {#mobile}

Every measurement goes into OONI's public database, recording whether the network of a given provider could reach each website and service at that moment. We use these records to watch for censorship and include them in the quarterly report. In the 44 days from 1 October to mid November, Chunghwa Telecom's mobile network had measurements on only 13 days, so each extra day someone runs a test adds a day to the record. If you are in Taiwan with a Chunghwa Telecom or Far EasTone number, follow these three steps, and run them again a few days later if you can:

1. Open our [OONI Run link `10328`](https://run.ooni.org/v2/10328) on your phone to add the list to OONI Probe. If the app is not installed, the page will send you to your app store, and you open the link again after installing. You can do this step on Wi-Fi to save mobile data
2. Turn off Wi-Fi and any VPN, and switch to mobile data
3. Run the list you just added in the app. The result page shows the name of your provider when it finishes, so check that it is your mobile carrier and not Wi-Fi or a VPN

The list covers 10 services we run ourselves and checks whether each provider's network can reach them. It takes a few minutes.

??? info "Details and privacy before you run it"

    - A hotspot shared from another phone runs over a mobile network, but OONI records the connection as Wi-Fi, so do not use one
    - Tools like Tailscale also run through the phone's VPN system, so while they are on OONI measures someone else's connection. The app warns you when it detects a VPN
    - The app's home screen has a button that runs every test. The performance tests in that set leave your IP address in M-Lab's public dataset and use as much bandwidth as they can (an estimated 5 to 200 MB). This time, running the list you added is enough. See the [privacy notes in the 13 August post](/updates/2026/08/ooni-mobile-throttle-drill/#Privacy-implications-of-the-performance-tests) for details
    - If you have time, you can also run the Websites test, which checks a list of addresses one by one and takes a few minutes on a normal connection
    - OONI measurement data is public and includes the ASN (autonomous system number, roughly one provider's slice of the network) and the time, but not your IP address
    - Afterwards you can find the records in [OONI Explorer](https://explorer.ooni.org/search?ooni_run_link_id=10328) under link ID `10328`
    - On Android, OONI Probe is also available from F-Droid. See [What is OONI](docs:tools/what-is-ooni/) for an introduction
    - In the third-quarter [report](/projects/reports/2026-q3/), Chunghwa Telecom's mobile network had 17% of users but 0.3% of measurements, and nearly 90% of the measurements from link `10328` came from Taiwan Mobile

## Home cable broadband with no measurements

Several cable broadband providers in Taiwan had no measurements at all last quarter. If your home connection is TFN Media's cable broadband (sold as 台灣大寬頻) in the north, VeeTIME in greater Taichung, or a cable provider in Kaohsiung, running OONI Probe once on your home Wi-Fi may fill in a whole network. The steps are the same as above, except that this time you stay on Wi-Fi.

??? info "The list and registration records"

    - The "networks without measurements" list on the [OONI Coverage](/projects/asn-coverage/#gaps) page shows networks with a sizeable number of users and no measurements at all. In mid November, 10 networks with at least 0.1% of users had no measurements, covering about 3.8% of users together
    - The three networks with no measurements all of the third quarter are registered as UNION BROADBAND NETWORK, VEE TIME and New Kaohsiung Broadband. Going by the IP address registration records, the first two belong to TFN Media (sold as 台灣大寬頻) and VeeTIME. The third is a cable provider in Kaohsiung. So far this quarter only one of their ASNs has measurements, on two days
    - A single brand may use several networks. The network name and ASN on the result page are what count, and you can compare them with the list on the monitoring page

## Readers outside Taiwan {#outside-taiwan}

OONI measurement data is public and records your network provider and the time, which can reveal roughly where you are, so weigh the risks where you live before taking part. Running OONI Probe may be illegal in some places, or attract attention from your provider (see the [OONI Run v2 guide](docs:tools/ooni-run-v2/) on the docs site). In Hong Kong, surveillance and the chilling effect have grown since the 2020 National Security Law, so read the Hong Kong section of [VPN risks and choices](docs:tools/vpn-guide/) first. This post cannot make that judgement for you, so decide based on your own situation. If you are in mainland China or anywhere else with strict censorship, please do not run measurements or relay Tor traffic, and look at the [ways to help that need no equipment](#no-equipment) instead.

Meetup talks can be given online over Jitsi, with no recording and under a pseudonym if you like, and speakers outside Taiwan are welcome to submit (see [talk topics](#talks)). If you have weighed the risks and decided you can take part, there are three more things you can do from outside Taiwan.

### Snowflake

[Snowflake](docs:tools/tor-snowflake/) lets your browser relay Tor connections for people in censored regions. You only need to install a browser extension, the default bandwidth use is small, and it is the easiest way to help, though it does not show up in the monitoring figures. Your address is not listed publicly, but the people connecting through you can see it. Running it on a company or school network means using that organization's connection to carry other people's traffic, so check the rules first. The Snowflake page on the docs site also covers what readers in Hong Kong should weigh before taking part, so read it before installing.

### OONI measurements where you are

Besides Taiwan, [OONI Coverage](/projects/asn-coverage/) has pages for Hong Kong, Macau, Japan, South Korea, Singapore, Vietnam, Thailand, Malaysia, Indonesia, the Philippines and India, and each one lists the networks in that region without measurements. Pick your region, check the list, and run OONI Probe's default tests on your own network. Our `10328` list checks whether Taiwan's providers can reach our services, so readers outside Taiwan do not need to run it.

### Relays in Asia

Relays in all the Asian regions covered by [Tor Relay Watch](/projects/pulse/) are measured low (see [running and setting up relays](#relays)). Setting up a relay in Japan, South Korea, Hong Kong or Southeast Asia also adds to the number of relays in Asia. The steps in the [Tor Relay Setup Guide](/join/setup-tor-relay/) work anywhere, but its legal and network notes only cover Taiwan, so check your own region separately.

## Development and data analysis {#development}

Our monitoring pages and quarterly reports are open-source code built on public data, so people who write code or analyse data can start here:

- Monitoring code: [Tor Relay Watch](/projects/pulse/) (Pulse) and [OONI Coverage](/projects/asn-coverage/) (ASN Coverage) live in the [anoni-net organization](https://github.com/anoni-net) on GitHub, are written in Python, and take contributions through pull requests. See [Development Environment Setup](/join/dev-setup/) for the accounts and tools you need
- Checking the figures: the analysis of low relay weights in Asia uses public Onionoo data, so anyone can recompute it. The plan and the mid-quarter review are in [anoni-net/www#32](https://github.com/anoni-net/www/issues/32). If you find a wrong figure, comment on the issue or write to us
- Measurement week data: compare measurement counts before and after the week using OONI's public API. Mention this task when you sign up to help organize

## Running and setting up relays {#relays}

This section is for people who already run, or want to set up, Tor relays and bridges. Skip it if you do not plan to. Two thirds of Taiwan's Tor relays are on a single provider, Chunghwa Telecom's HiNet, so if that provider has a problem, most of the relays are affected at once.

### Relays already running

If you already run a relay, open the checklist below, which covers upgrading to the latest version and a few settings.

??? info "Checklist"

    - Upgrade to 0.4.9.17. Tor has released four versions this quarter, 0.4.9.14 to 0.4.9.17, and on 15 November only 3 of Taiwan's 12 relays were on the latest two
    - 3 relays in Taiwan have a bandwidth cap, and their reported bandwidth equals the cap exactly. If your connection has room, consider raising `RelayBandwidthRate` or the monthly traffic limit
    - Check that IPv6 is configured. If you run several relays, set up family
    - If you run an exit relay, first go through the [security checks after the October exit relay compromise](/articles/tor-exit-ssh-interception/)

### New relays

For a new relay, please prefer a network other than HiNet, such as cable broadband, a university network or another provider, or a data centre or VPS. The steps are in the [Tor Relay Setup Guide](/join/setup-tor-relay/). A relay's network address and contact email are public and anyone can look them up, so before running one at home, check the rules of your workplace, building or provider.

Relays in Asia currently get less traffic than relays in Europe. The cause is still being studied, and we will write a separate article on the data. A relay with little traffic still carries connections for users, and since Asia has few relays, each new one makes the Tor network more spread out. A new relay takes about two months to settle, so plan to run it for the long term.

??? info "Low weights and how long new relays take to settle"

    - Tor clients choose relays by consensus weight, which the bandwidth authorities measure. In the 12 October snapshot, dividing each region's share of weight by its share of self-reported bandwidth gives 0.22 for Taiwan and 1.26 for Germany. The same bandwidth in Taiwan earns roughly a fifth of the weight it would in Germany
    - The Tor network health team has recorded the same thing: relay weights in South Korea, Hong Kong, Singapore and Japan dropped from 2023 and have not recovered ([tpo/network-health/analysis#61](https://gitlab.torproject.org/tpo/network-health/analysis/-/issues/61)). We have not found an official explanation of where the measurements are taken from or why
    - On Tor Relay Watch, Taiwan's weight rose from about 0.005% to 0.013% between 10 and 14 November, alongside several other Asian regions. The cause is not yet known, it may fall back, and it does not count as a result of our work
    - A 2013 Tor Project blog post describes four phases for a new relay, with a steady state after about 68 days ([The lifecycle of a new relay](https://blog.torproject.org/lifecycle-of-a-new-relay)). The post is old, so treat the figure as an order of magnitude. A relay that comes online in December will show up in the second quarterly report as new, but its weight will not settle until the first quarter of 2027
    - A relay's IP address and `ContactInfo` are published in the consensus and on Onionoo

If you know people in a university IT centre or department, see [Tor Relays on Campus Track](/join/relay-on-campus/) and the template kit built from the National Taiwan Normal University case, and put them in touch with us.

### WebTunnel bridges

A [WebTunnel](/join/setup-tor-webtunnel/) bridge disguises Tor connections as ordinary website traffic, which makes it harder to block in heavily censored regions. When Iran's internet reopened, a lot of traffic went through our community's WebTunnel bridge (see [After Iran's 80-day blackout](/updates/2026/05/iran-blackout-webtunnel/)). Setting one up needs a small cloud server and a domain.

??? info "Requirements"

    - A VPS with at least 512 MB of RAM (1 GB recommended), a domain or subdomain whose DNS you can edit, and port 443 open. TLS certificates renew automatically with Let's Encrypt, so the main costs are the VPS fee and traffic
    - Bridges are not listed in the public consensus. Users get them through Tor Browser's built-in request, the website or email, and they are not handed out by relay consensus weight
    - Bridges are outside the monitoring pages' figures. Operators can check their bridge's status in Tor Metrics Relay Search using the hashed fingerprint

## Ways to help that need no equipment {#no-equipment}

- Maintaining the test list: the websites OONI Probe tests come from a list, and Taiwan's `tw.csv` needs updating. No coding is needed (see [Maintaining the OONI Test List](/join/ooni-test-list/))
- Passing this on: to people on Chunghwa Telecom or Far EasTone, people with cable broadband at home, friends who research privacy or censorship, friends with server space or a VPS, and university IT staff

## Where to see the results

- Mobile measurements: [OONI Explorer](https://explorer.ooni.org/search?ooni_run_link_id=10328), link ID `10328`
- Taiwan's relay count, networks and weight: [Tor Relay Watch](/projects/pulse/), updated hourly
- Networks without measurements: [OONI Coverage](/projects/asn-coverage/)
- The quarter's results: the second quarterly report is planned for January 2027. Follow community updates by [RSS](/en/updates/feed.xml) or subscribe to the [newsletter](/contact/)

## Related reading

- [First quarterly report and new monitoring pages](/updates/2026/10/quarterly-report-2026-q3/)
- [Call for OONI Measurements During Northern Taiwan's Mobile Throttle Drill on 13 August](/updates/2026/08/ooni-mobile-throttle-drill/)
- [Tor Relay Setup Guide](/join/setup-tor-relay/)
- [Tor Relays on Campus Track](/join/relay-on-campus/)
