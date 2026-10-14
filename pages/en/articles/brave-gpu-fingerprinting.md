---
title: Two Opposite Approaches to Flattening GPU Fingerprints in Brave
description: The three GPU fingerprinting protections Brave 1.93 enables by default, how uniformity and randomization split the work across WebGL and WebGPU, and how the approach compares with Tor Browser and Firefox.
date: 2026-08-19
---

JavaScript on a web page can read the graphics card model, its driver details, and the hardware features it supports. Those values barely change on a given machine, so a tracking company can combine them with other device traits into an identifier that needs no cookie, asks for no consent, and follows the user between sites.

The graphics card is one source among many: font lists, screen dimensions, time zone, and audio processing all feed the same identifier. This piece stays with the graphics card; the docs site's [introduction to browser fingerprinting](docs:basics/browser-fingerprinting/) covers the whole mechanism and where each browser stands by default.

Brave has handled these signals since version 1.93, on by default on desktop and Android and rolling out in stages[^brave]. Three protections ship together: the WebGL vendor and renderer strings become one generic string shared by every Brave user, the WebGPU hardware description fields are cleared, and the list of supported WebGL extensions gets noise added to it.

The first two make every user look alike. The third makes one user look different on every site. The two opposite techniques arrived in the same release, each assigned to a different API, and where that line falls is also where Brave and Tor Browser part company on fingerprinting.

## Identifying Power of Graphics Card Data

WebGL and WebGPU give sites hardware-accelerated graphics, which maps, games, and data visualization all depend on. To let a site adapt its rendering to the hardware, both APIs also expose low-level hardware detail to JavaScript.

Three kinds of information are available to a site[^brave]:

- **Vendor and renderer strings**, through the `UNMASKED_VENDOR_WEBGL` and `UNMASKED_RENDERER_WEBGL` parameters that the `WEBGL_debug_renderer_info` extension provides[^mdn]. A site receives something like `ANGLE (Apple, ANGLE Metal Renderer: Apple M5 Max)`, precise down to the chip model. Chrome originally opened this debugging extension for Google Maps, and it ended up callable by any site.
- **The list of supported extensions**, which a WebGL context reports in full. Its contents vary with GPU and driver, and a tracker hashes the whole list into one compact identifier.
- **The WebGPU hardware description**, where the newer API returns the adapter's `vendor`, `architecture`, and `device` fields, for instance `{vendor: 'apple', architecture: 'metal-3'}`.

Graphics cards are rarely replaced, so these values stay stable for years and outlast a cookie. Switching accounts, opening a private window, or clearing the browsing history leaves the hardware traits the API reports unchanged.

Brave ran a small-scale web crawl, analyzing the call stack behind each invocation on highly ranked sites. The conclusion in Brave's announcement is that for most sites calling these APIs, browser fingerprinting is the only purpose[^brave]. The size of the crawl and the proportions behind that finding are not published.

## Division of Work Between Uniformity and Randomization

| Signal | What Brave does | Type of technique |
|--------|-----------------|-------------------|
| WebGL vendor and renderer strings | Replaced with one generic string, identical for every Brave user | Uniformity |
| WebGPU adapter description | `vendor`, `architecture`, and `device` cleared | Uniformity |
| WebGL extension list | Noise added, differing per session, per site (eTLD+1), and per storage partition | Randomization |

The third protection reuses farbling, which Brave already had. In the 2020 privacy update that introduced it, Brave defined the technique as "slightly randomizing the output of semi-identifying browser features, in a way that's difficult for websites to detect, but doesn't break benign, user-serving websites"[^farbling].

## The Farbling Seed

On startup the browser generates a random session token, then mixes it through HMAC256 with each first-party, top-frame domain it visits, producing a per-domain token that lives as long as the session[^farbling]. Measuring the same site twice within one session gives identical values; another site gives different ones; a new session changes all of them. Third-party frames and scripts inherit the top-level eTLD+1 seed[^farbling], so embedding third-party content offers no way around it.

A fingerprinter hashes many semi-identifying traits into a single identifier, and randomizing any one of them poisons the whole hash. The technique traces back to two research papers, PriVaricator (WWW 2015) and FPRandom (ESSoS 2017)[^farbling].

## Reasons for Randomizing the Extension List

Brave's announcement does not say why the extension list gets randomization instead of uniformity. Judging by what each API is for, changing the two kinds of data has very different consequences for a site.

Vendor and renderer strings mostly serve performance tuning and hardware blocklists. When the string a site receives is not in its existing list, the worst outcome is a fall back to the ordinary rendering path. Collapsing the value to a constant drops that field's contribution to a fingerprint to zero at a limited cost.

The extension list serves feature negotiation: a site checks whether a given extension is present before enabling a rendering path or choosing a fallback. Given a uniform list that does not match the hardware, the site may pick a path the hardware cannot support, or abandon acceleration that was actually available. What remains is adding noise while preserving usability, which keeps the resulting hash unstable.

Uniformity reduces entropy, stripping a trait of its power to distinguish, with every Brave user in the world ideally identical on that field. Added noise undermines linkability instead: the value still carries information, but it differs on every site and every time, so a tracker cannot connect the same user across two sites.

## Tor Browser and Firefox Approaches

The Tor Project blog's 2019 introduction to fingerprinting opens with the position that all Tor users should have exactly the same fingerprint. The measures it describes include reporting one operating system across every platform, normalizing the time zone and screen resolution, and letterboxing. Letterboxing pads content with gray margins so the viewport snaps to fixed dimensions and a maximized window stops revealing the screen size[^tor].

The same piece covers the risk in randomization, citing what Eckersley called the Paradox of Fingerprintable Privacy Enhancing Technologies. Its example is an extension that rewrites a batch of values but misses `navigator.platform`, producing a combination of traits that exists nowhere in reality and leaving the user easier to identify than before[^tor]. Randomization only works with thorough coverage, which is why Brave keeps extending the list of endpoints farbling touches.

Firefox-based browsers disable the `WEBGL_debug_renderer_info` extension outright when `privacy.resistFingerprinting` is on, so a site cannot call it[^mdn]. The preference is off unless a user turns it on in `about:config`. With the extension disabled, a site gets nothing and has to handle the empty case. With a generic value, the data a site receives is indistinguishable from real hardware and the site carries on as usual. Brave chose the generic value, consistent with its habit of keeping breakage as low as possible. Another position in the announcement is that protection should be on by default rather than hidden behind a special mode or a flag[^brave].

In the 2020 farbling update, Brave recommended that users facing targeted attacks switch to Tor Browser[^farbling]. Randomization holds up against broadly deployed commercial tracking, but it provides no anonymity set.

## Practical Limits

The practical value of this release is that it works by default. Most people will not edit `about:config`, switch to a special mode, or install an extension for privacy, and the announcement also notes that extensions carry their own security and privacy problems[^brave]. To check whether the update has landed, EFF's [Cover Your Tracks](https://coveryourtracks.eff.org/) lists the WebGL vendor and renderer strings a browser reports; once the update has fully rolled out, both fields show the generic value[^brave].

Anonymity still calls for Tor Browser, because Brave's randomization addresses cross-site correlation only. The IP address still goes straight to the site, and an observer on the network path still sees where the connection went. Tor is heavily blocked in mainland China, where connecting needs bridges or another entry method, and generally reachable directly in Taiwan, Hong Kong, Macau, Singapore, and Malaysia. The docs site's [guide to device minimization and border crossings in Asia](docs:scenarios/asia-travel/) has the jurisdiction-by-jurisdiction detail on reachability and law.

Tor Browser's uniformity route depends on every user staying uniform. Installing extensions, maximizing the window, or changing font settings all make a user stand out ([Tor Browser advanced settings](docs:tools/tor-browser-advanced/) on the docs site covers the specifics). The same action costs little in Brave and undermines the premise of the protection in Tor Browser. For a general-audience explanation, see the docs site's [introduction to browser fingerprinting](docs:basics/browser-fingerprinting/).

## Remaining Gaps

When the announcement was published in August 2026, the list of supported WebGPU extensions was not randomized yet, and the announcement says that change is planned[^brave]. Graphics APIs remain an active area of fingerprinting research, and new leak channels keep appearing.

Site breakage is still under observation, and Brave kept the ability to adjust protection per site. On a site that genuinely will not work, a user can disable graphics protection for that site, disable fingerprinting protection, or turn off Shields entirely[^brave]. Keeping those switches means the trade-off is still live, and neither uniformity nor added noise can guarantee that every site behaves as before.

Beyond the graphics card, font lists, canvas rendering output, and audio processing traits can all still identify a browser. Signals that can safely collapse to a constant collapse; signals tied to feature negotiation get noise. The same dividing line is a useful test for any other tool that claims fingerprinting resistance.

## Related Reading

- [A browser fingerprint cannot be cleared the way a cookie can](docs:basics/browser-fingerprinting/): what a fingerprint is made of, why it resists a clean fix, and where each browser stands by default
- [How platforms collect your data, and the microphone question](docs:basics/platform-tracking/): where device fingerprinting sits among other tracking methods
- [Tor Browser advanced settings](docs:tools/tor-browser-advanced/): fingerprinting resistance and window size in practice
- [Threat modeling](docs:basics/threat-model/): establish who you are defending against before picking tools

[^brave]: [Brave improves protections against GPU fingerprinting](https://brave.com/privacy-updates/38-webgl-webgpu-fingerprinting-protections/) — Brave privacy update 38. Source for the three protections, the crawl observation, the compatibility handling, and the plans described here. Verified 2026-08-14.
[^farbling]: [Fingerprinting defenses 2.0](https://brave.com/privacy-updates/4-fingerprinting-defenses-2.0/) — Brave privacy update 4, 2020. Source for the definition of farbling, the HMAC256 seed mechanism, and the research lineage. The note that third-party frames inherit the top-level seed also appears in Brave's [Fingerprinting Protections wiki](https://github.com/brave/brave-browser/wiki/Fingerprinting-Protections), a page subject to ongoing edits. Verified 2026-08-18.
[^tor]: [Browser Fingerprinting: An Introduction and the Challenges Ahead](https://blog.torproject.org/browser-fingerprinting-introduction-and-challenges-ahead/) — Pierre Laperdrix, The Tor Project blog, 4 September 2019. Source for the uniformity route, letterboxing, and the Paradox of Fingerprintable Privacy Enhancing Technologies. The specific measures described there match the Tor Browser version current at the time of writing. The paradox itself is credited there to Eckersley, PETS 2010. Verified 2026-08-18.
[^mdn]: [WEBGL_debug_renderer_info](https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_debug_renderer_info) — MDN Web Docs. Source for the definitions of both constants and for Firefox disabling the extension when `privacy.resistFingerprinting` is true. Verified 2026-08-18.
