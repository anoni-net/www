---
title: Privacy Mysteries at anoni.net/mystery
description: A privacy mystery game from anoni.net. Each case is a request to find the leaks in photos, emails and files; why we made it and how we hope it is used.
date: 2026-10-21
kind: new
og_image: https://anoni.net/mystery/og-en.png
---

<figure markdown="span">
    <a href="https://anoni.net/mystery/en/" target="_blank">
        <img src="https://anoni.net/mystery/og-en.png"
            alt="Dark blue Privacy Mysteries banner reading “Mistport Privacy Aid · Case board” above the title “Privacy Mysteries”, with a standing night heron on the right" class="shot">
    </a>
</figure>

The anoni.net community has launched [Privacy Mysteries](https://anoni.net/mystery/en/){target="_blank"}. You play an investigator at the fictional Mistport Privacy Aid, and every case starts with a request. Someone brings you a photo, an email or a list; you look for what gives people away in photos, emails, files and websites, then use the evidence to rule suspects out one by one.

The first case, Night Heron, went live on 9 October, and the second, Blue Magpie, on 11 October. By 20 October both were available in English, Mandarin and Simplified Chinese, each language with an interactive edition, a static edition that needs no JavaScript, and a printable PDF.

## Why we made a mystery game

Our docs site is written for people new to privacy and anonymity networks. The page [Metadata, and why it matters](docs:basics/metadata/) lists the time, device and location a photo can carry. Readers nod along, but when the moment comes to send a photo, few think about the file name, the time zone or what ended up in the corner of the frame. An explanation you have read does not always stay with you; working out for yourself what a photo gave away tends to.

Privacy advice is usually a list of things not to do: turn off location before taking the picture, strip metadata before uploading, do not click links in emails. Lists are easy to read and poor at explaining why. A mystery turns the perspective around and puts you in the seat of the person looking for the leak. Once you have watched scattered details get joined up, and a crowd of possible people shrink to one, you understand what each item on the list protects against, and you are better placed to judge the cases the list does not cover.

That shrinking crowd has a name in privacy research: the anonymity set. Whether someone stays anonymous depends on how many people they cannot be told apart from, and every detail that leaks makes the group smaller. Both cases are solved this way. You name one person at the end, and what backs it up is the evidence that ruled everyone else out.

The situations come from things readers may actually face. Night Heron is an employee leaking from inside a company, which connects to the docs page [Journalists and source protection](docs:scenarios/journalist/). Blue Magpie is a billing notice with no link in it: people who searched for support as the email told them lost their accounts. It touches on email aliases, search ads and the linked devices of messaging apps.

## Mistport Privacy Aid

Mistport Privacy Aid is a group of volunteers who help people with privacy problems: someone who leaked a document and fears being identified, someone who was scammed, someone whose account was taken over. The name comes from a harbour in fog, a place to tie up when you cannot see clearly. Fog, the volunteer on duty, gives hints on the internal channel and teaches you the terminal.

The stories are set in Taiwan in 2026, in real cities and districts, while every company, person and event is fictional. The game's internet has its own search engine (MistSearch), anonymous forum (Nameless Square) and photo network (PicNote) in place of real services, so no real brand is impersonated.

### Night Heron

"I turned off location." A whistleblower leaks a photo of an internal memo on an anonymous forum. The company says it will find the leaker within 72 hours. Get there first and work out what that photo gave away.

Skills you practise: EXIF metadata, time zones, file names, photo backgrounds, writing style and anonymity sets. About 45–75 minutes.

### Blue Magpie

"No link, so I thought it was real." A "3,480 a month" billing notice has no link, only a line telling you to search for support. People who searched lost their accounts, and the leaked list even had their hours of sleep. Find out who sold the member data.

Skills you practise: email headers, lookalike domains, search ads, QR codes, linked devices and canary records. About 60–90 minutes.

### How a case runs

A case opens with an encrypted chat with the client. You choose a few replies and receive the material the client has gathered. As you investigate, clues are logged on the evidence board automatically, and you can pin pages, tables and logs there too. Every case hides a trap: a step that looks like the natural next move but would hurt the client. Fall into it and Fog explains why.

The case report asks a few multiple-choice questions and then asks you to name one person. Your rank, from Trainee Investigator through Senior Privacy Volunteer to Chief Onion Investigator, depends on how many hints you used, how many wrong accusations you made and whether you fell into the trap. The cases stand alone, so you can start with either.

## Interactive, static and PDF editions

The interactive edition simulates an investigator's computer with encrypted chat, a browser, files, an image viewer, a terminal and an evidence board. You type real commands such as `exiftool` and `grep` into the terminal. If you have never used one, switch on the beginner's helper; it does not affect your rank. On a phone the layout becomes one screen at a time, and the terminal defaults to command blocks you assemble by tapping commands and files. The interactive edition installs as an app, stores about 1 MB per language on the device, and works offline.

The static edition uses only HTML and CSS, for people running Tor Browser at the "Safest" level. The content is the same: each choice in the chat is its own page, terminal commands show their output when opened, and files can be downloaded in their original form.

The PDF is an A4 case file to play offline or on paper. The solution is on the last pages behind a black "stop" page, printed upside down, small and in light grey so nobody reads it by accident while flipping through.

The leaked photo in Night Heron is a real JPEG with deliberately written EXIF data, so you can download it and inspect it with your own tools. All three languages share one save; switch language halfway through and the chat and evidence board follow. The English edition still takes place in Taiwan, and its writing-style clue uses English habits instead.

## Design choices

A game about privacy should hold itself to the same standard. Pages load no web fonts and make no requests to other sites; Tor Browser blocks remote fonts at its higher security levels, and the pages still render in full. Opening anoni.net/mystery in Tor Browser offers the onion address automatically.

On anoni.net, the interactive edition counts how many people start and close a case using our self-hosted Umami. It sets no cookies and sends nothing when Do Not Track or Global Privacy Control is on. All it sends is that a case was started, that it was closed, and the rank; who you accused, what you answered and which hints you opened are never sent. The onion version, the static editions and the PDFs collect nothing.

All the data in the cases is made up. IP addresses come only from the ranges reserved for documentation, domains belong to the game's own brands or end in `.mist`, and QR codes contain commands for a fictional app, so scanning one opens no website. Where a case borrows from a real scam, it takes the technique and leaves out the original text, real names, real addresses and phone numbers. The cases teach recognition and protection, never steps that could be used to track down a real person.

The source is on [GitHub at anoni-net/privacy-mystery](https://github.com/anoni-net/privacy-mystery){target="_blank"}. The code is under MIT; the story, characters, dialogue, hints and images are under CC BY 4.0. The repository holds no plaintext solutions. Each case's solution is encrypted with the culprit's full name as the key, and the game can only decrypt it when you name the right person. Anyone who has solved a case has the key and can help edit the story; anyone browsing the repository before solving it will not have it spoiled. With only a handful of suspects, trying every name would open it, so this only guards against accidental spoilers.

## How we hope it gets used

Above all, we hope readers of the docs site will treat the game as a place to practise. Play Night Heron after reading [Metadata, and why it matters](docs:basics/metadata/), or Blue Magpie after the [guide to email aliases](docs:tools/email-alias/), and a concept becomes something you have done. It works the other way round too: where you get stuck is often exactly what one of the docs pages explains.

Both cases are designed for one player or two to four working together, and take 45–90 minutes, which fits a class or a workshop. The PDF can be printed for group discussion, so not everyone needs a laptop, and a venue without internet is no obstacle. A facilitator can have groups compare who ruled out which suspect first and on what evidence, then move on to the practical protections in the docs. For handing out materials on the day, see the docs page [Handing things out at a workshop](docs:utils/case-workshop/).

Reading groups and internal training at civil society organisations or newsrooms are a good fit as well. New members may not have time to read a full digital security guide, but after spending one case checking a photo's metadata and an email's headers with their own hands, they are more likely to pause and look twice when it happens for real.

The content is under CC BY 4.0, so you can adapt a case for teaching, move it into a local setting or translate it into another language, as long as you credit the source with a link. We are also writing down the setting, so that future cases, including ones written by community members, keep their characters, websites and timeline consistent.

## Ideas and feedback for the next case

There is a "coming soon" card on the case board, and we would love to hear your ideas for it. A privacy topic you would like to see, or a situation where someone gave themselves away, can go on the [feedback page](https://anoni.net/mystery/en/feedback/?kind=idea){target="_blank"}; a rough direction is plenty. Impressions, places where you got stuck and bugs go through the same page. Feedback is read inside the community only; what you write and how to reach you are not published. If you have used a case in a classroom or workshop, we would especially like to hear how you split into groups, how long it took and where most people got stuck.

- Source code and bug reports: [GitHub at anoni-net/privacy-mystery](https://github.com/anoni-net/privacy-mystery){target="_blank"}. Please keep the culprit's name out of issues, pull requests and commit messages
- Real-time discussion: Matrix public room (home server `im.anoni.net`, link on the [services page](/services/))
- Anonymous tips: whisper@anoni.net ([GPG key](/contact/))

## Further reading

- [Metadata, and why it matters](docs:basics/metadata/)
- [Journalists and source protection](docs:scenarios/journalist/)
- [Email aliases, and who you hand your trust to](docs:tools/email-alias/)
- [Gears](https://anoni.net/gears/en/){target="_blank"}, a file workbench that strips metadata from photos in the browser; files stay on your device by default
