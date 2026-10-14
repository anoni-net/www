---
title: Taipei Coffee and Circumvention Meetup 2025/10
description: 'Quick Recap: What Actions Can We Take Against State-Level Surveillance?'
date: 2025-10-18
kind: event
---

After presenting InterSecLab's [report](https://interseclab.org/research/the-internet-coup/) on data leakage related to the Great Firewall of China at the "Taipei Coffee and Circumvention Meetup 2025/10," there were many discussions during the latter part of the event. The questions centered around what actions we can ultimately take in the face of state-level surveillance methods and capabilities.

The previously provided cybersecurity recommendations also need to be revisited and revised. Below, we will review some of the topics discussed that day through text. We also recommend taking some time to read this report, as it will provide a clearer outline of the risks and challenges we are facing.

## Abuse of Open Source Software

The report found that some software used in the Great Firewall is built upon or modified from existing open source software. This raises a concern: many engineers contribute to open source projects in their fields, only to see their work misused by certain organizations **that completely disregard open source licensing guidelines**. Although these guidelines may lack substantial enforcement power, when contributions are used for privacy surveillance, we currently lack measures to resist or respond. When the misuse of open-source software escalates to a national level, how can we balance and hold accountable such actions?

During the discussion that evening, we did not arrive at an answer. **In the pursuit of internet freedom and democratic liberties**, we may have to temporarily attribute this situation to the neutrality of tools, a scenario that resembles the use of Tor and onion networks.

## WebTunnel, Which the Great Firewall Struggles to Effectively Block

The report mentions that while common VPN protocols can be identified and blocked, the Great Firewall currently cannot effectively block WebTunnel, a type of Tor bridge. Since the data leak occurred around December 2024, it remains uncertain whether, after 10 months, the Great Firewall's technology still cannot block it. Similarly, Snowflake, which disguises Tor connections through streaming, can also evade packet detection.

During the event that evening, we quickly introduced [Snowflake](https://snowflake.torproject.org/) to everyone. By using a browser extension, you can create a Tor bridge by establishing a stream similar to a video conference. This helps users in regions where Tor is completely inaccessible connect to the onion network through your bridge relay. For participants with technical capabilities, we also suggested setting up a bridge relay using the Tor-official [WebTunnel (Docker image)](https://community.torproject.org/relay/setup/webtunnel/docker/). This setup mimics browsing a website, thereby providing a bridge relay point.

## Taking Action

During the evening discussion, we explored whether we should take "**proactive**" measures. Given the known surveillance and repressive actions by some authoritarian governments, should we actively seek to change the current situation? Of course, after the initial surge of emotions, we realized that the issues we face might **not be as simple as** correcting a code deployment error or rebooting a server. When factoring in the defense of human rights, we might be confronted **with real-world dangers and threats to our lives**. At that moment, a brief pause allowed participants to reflect on the risks and assess **how determined we are to take action**.

To slightly ease the heavy atmosphere of the topic, we shared InterSecLab's next steps. They aim to recruit partners interested in **code analysis and research**. The report mentioned that a significant portion of the leaked data remains unexplored and unanalyzed. Moreover, in the countries where the Great Firewall technology has been exported, an entity code-named A24 has yet to be identified. Perhaps efforts from various professional fields can become a powerful form of resistance against authoritarian regimes!

---

This is a quick recap of the "Taipei Coffee and Circumvention Meetup 2025/10" event. If you haven’t read our **translated report** yet, you can access it [here](https://anoni.net/docs/report/interseclab-the-internet-coup/)! We are also preparing to develop user-friendly defensive capabilities based on the report's findings, possibly starting with privacy protection. Interested individuals are welcome to join the discussion through [this channel](https://matrix.to/#/#interseclab-the-internet-coup:im.anoni.net).

Of course, you can also [email us](/contact/) directly!
