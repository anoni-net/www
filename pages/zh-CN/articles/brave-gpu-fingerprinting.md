---
title: Brave 抹平 GPU 指纹的两种相反手法
description: Brave 1.93 默认启用的三项 GPU 指纹防护、一致化与随机化在 WebGL 与 WebGPU 之间的分工，以及与 Tor Browser、Firefox 做法的对照。
date: 2026-08-19
---

网页上的 JavaScript 可以取得显卡型号、驱动信息，以及硬件支持哪些功能。返回的值在同一台电脑上几乎不变，跟踪公司把它们与其他设备特征组合起来，就成了一组不需要 cookie、不需要用户同意、跨网站跟着用户的标识符。

显卡是浏览器指纹的来源之一，字体清单、屏幕尺寸、时区、音频运算结果同样算在里面，本文只处理显卡（整套机制与各家浏览器的默认状态见文档站的[浏览器指纹说明](docs:basics/browser-fingerprinting/)）。

Brave 从 1.93 版起处理这组信号，桌面版与 Android 版默认开启、分批推送[^brave]。三项防护分别是把 WebGL 的厂商与渲染器字符串换成所有 Brave 用户一致的通用字符串、清空 WebGPU 的硬件描述字段，以及在 WebGL 支持的扩展清单注入噪声。

前两项让所有用户看起来一样，第三项让同一个用户在每个网站看起来都不一样。两种方向相反的手法在同一次更新里各自负责不同的 API，分工的界线也是 Brave 与 Tor Browser 在指纹抗性上分歧的起点。

## 显卡信息的识别力

WebGL 与 WebGPU 让网站使用硬件加速绘图，地图、游戏、数据可视化都仰赖它们。为了让网站能针对硬件调整绘图方式，两组 API 也把底层的硬件细节开放给 JavaScript 查询。

网站能取得的信息有三类[^brave]：

- **厂商与渲染器字符串**：通过 `WEBGL_debug_renderer_info` 扩展提供的 `UNMASKED_VENDOR_WEBGL` 与 `UNMASKED_RENDERER_WEBGL` 两个参数[^mdn]，网站会取得类似 `ANGLE (Apple, ANGLE Metal Renderer: Apple M5 Max)` 的字符串，精确到芯片型号。调试用的扩展最早是 Chrome 为了 Google Maps 开放，后来所有网站都能调用。
- **支持的扩展清单**：同一个 WebGL context 会回报它支持的完整扩展清单，内容随 GPU 与驱动而异，跟踪者把整份清单哈希成一组精简的标识符。
- **WebGPU 的硬件描述**：较新的 WebGPU API 会返回 adapter 的 `vendor`、`architecture` 与 `device` 字段，例如 `{vendor: 'apple', architecture: 'metal-3'}`。

显卡不会天天更换，所以这些值长期稳定，比 cookie 更难清除。用户换账号、开无痕窗口、清空浏览记录，API 回报的硬件特征仍是同一组。

Brave 做了一次小规模的网络爬取，分析排行前段的网站调用这些 API 之前的调用堆栈（stack trace）。公告里的结论是多数网站调用它们的唯一用途是浏览器指纹识别[^brave]，爬取规模与比例没有公开。

## 一致化与随机化的分工

| 信号 | Brave 的处理 | 手法性质 |
|------|--------------|----------|
| WebGL 厂商与渲染器字符串 | 换成单一通用字符串，所有 Brave 用户取得相同的值 | 一致化 |
| WebGPU 的 adapter 描述 | 清空 `vendor`、`architecture`、`device` | 一致化 |
| WebGL 扩展清单 | 注入噪声，每个 session、每个网站（eTLD+1）、每个存储区取得的值都不同 | 随机化 |

第三项沿用 Brave 既有的 farbling 机制，Brave 在 2020 年的隐私更新里把它定义为「对半识别性的浏览器功能输出做轻微随机化，让网站难以检测，又不破坏良性、以用户为本的网站」[^farbling]。

## farbling 的种子机制

浏览器启动时产生一组随机的 session token，再与每个访问的第一方顶层框架域名经 HMAC256 混合，得出每个域名一组、寿命与 session 相同的 token[^farbling]。同一个网站在同一个 session 内重复测量会取得完全相同的值，换一个网站取得不同的值，下一个 session 再全部换过。第三方 frame 与 script 沿用顶层 eTLD+1 的种子[^farbling]，所以无法靠嵌入第三方内容绕过。

指纹器会把大量半识别特征哈希成单一标识符，只要其中一项被随机化，整组哈希值就被污染。技术源头是 PriVaricator（WWW 2015）与 FPRandom（ESSoS 2017）两项研究[^farbling]。

## 扩展清单改走随机化的原因

公告里没有写扩展清单改走随机化的原因，从 API 的用途推测，改动两种数据对网站功能的冲击差距很大。

厂商与渲染器字符串主要用于性能调校与硬件黑名单。网站取得的字符串不在既有清单里时，最坏的结果是改走一般绘图路径。把值收敛成一个常数，该字段对指纹的贡献直接归零，代价有限。

扩展清单用于功能协商，网站依清单里是否有某个扩展，决定启用哪条绘图路径或改走哪一种后备方案。给一份与硬件实况不符的统一清单，网站可能选到硬件无法支持的路径，也可能放弃本来可用的加速。剩下的做法是在保留可用性的前提下加入噪声，让哈希值不稳定。

一致化降低熵（entropy），让某一项特征失去区辨力，理想状态是全世界的 Brave 用户在该字段完全相同。注入噪声则破坏可链接性（linkability），值仍然带有信息，但每个网站、每次取得的都不一样，跟踪者无法把两个网站上的同一位用户串在一起。

## Tor Browser 与 Firefox 的做法

Tor Project 博客 2019 年的指纹介绍文章，开头就写着「所有 Tor 用户应该有完全相同的指纹」。当时的具体做法包含在所有平台回报同一组操作系统信息、统一时区与屏幕分辨率，以及 letterboxing。letterboxing 在内容周围加上灰边，把可视区域对齐到固定尺寸，避免最大化的窗口泄漏屏幕大小[^tor]。

随机化的风险也写在同一篇文章里，文中引用 Eckersley 提出的「可指纹化的隐私增强技术悖论」（Paradox of Fingerprintable Privacy Enhancing Technologies）。文中的例子是某个扩展程序改掉一批数值，却漏改 `navigator.platform`，造出一组现实中不存在的特征组合，用户反而更容易被辨认[^tor]。要让随机化有效，覆盖范围必须够完整，Brave 持续扩充 farbling 的端点清单也是同一个原因。

Firefox 系的浏览器在 `privacy.resistFingerprinting` 开启时直接停用 `WEBGL_debug_renderer_info`，网站调用不到这个扩展[^mdn]。该开关默认关闭，需要用户自行到 `about:config` 开启。停用之后网站取不到值、需要自行处理空值。返回通用值时，网站收到的数据与真实硬件无异，可以照常运作。Brave 选择返回通用值，与它一贯压低功能损坏风险的取向一致。公告里的另一项主张是防护要默认开启，不藏在特殊模式或旗标后面[^brave]。

Brave 在 2020 年说明 farbling 的更新里建议，需要对抗定向攻击的用户改用 Tor Browser[^farbling]。随机化挡得住大规模部署的商业跟踪，但不提供匿名集（anonymity set）。

## 实务上的界线

Brave 这次更新最实际的价值是默认生效，多数人不会为了隐私去改 `about:config`、切换特殊模式或安装扩展程序，公告里也写了扩展程序本身带有安全与隐私问题[^brave]。要确认更新是否生效，可以用 EFF 的 [Cover Your Tracks](https://coveryourtracks.eff.org/) 检查浏览器回报的 WebGL 厂商与渲染器字符串，更新完整推送之后两个字段会变成通用值[^brave]。

需要匿名时仍要用 Tor Browser，因为 Brave 的随机化只处理跨站串接。IP 地址照样直接送到网站，网络路径上的观察者也看得到连接的目的地。Tor 在中国大陆受到重度封锁，需要网桥或其他接入方式，在台湾、香港、澳门、新加坡、马来西亚一般可以直连（逐地的可达性与法规见文档站的[东亚与东南亚出差准备](docs:scenarios/asia-travel/)）。

Tor Browser 的一致化路线靠所有用户维持相同的样貌，安装扩展程序、最大化窗口、改动字体设置，都会让用户从人群里凸显出来（细节见文档站的 [Tor Browser 进阶设定](docs:tools/tor-browser-advanced/)）。同一个动作在 Brave 上影响有限，在 Tor Browser 上会直接破坏防护的前提。写给一般读者的完整说明见文档站的[浏览器指纹说明](docs:basics/browser-fingerprinting/)。

## 尚未涵盖的范围

公告发布时（2026-08），WebGPU 支持的扩展清单还没纳入随机化，公告里写了之后会补上[^brave]。图形 API 仍是指纹研究的活跃领域，新的泄漏管道会持续出现。

网站功能受损的情况仍在观察中，Brave 保留了逐站调整防护的能力。遇到确实无法正常运作的网站，用户可以单站关闭图形防护、关闭指纹防护，或整个关掉 Shields[^brave]。保留这些开关代表取舍仍在，一致化与注入噪声都无法保证所有网站维持原本的行为。

显卡之外，字体清单、canvas 绘图结果、音频运算特征仍然可以用来识别浏览器。能安全收敛成常数的信号就收敛，牵涉功能协商的信号就注入噪声，检视其他标榜指纹抗性的工具时也可以用同一条分工线对照。

## 相关阅读

- [浏览器指纹是什么，为什么很难摆脱](docs:basics/browser-fingerprinting/)：指纹由哪些特征组成、结构上难以规避的原因，以及各家浏览器的默认状态
- [社交平台怎么收集你的数据](docs:basics/platform-tracking/)：设备指纹在整套跟踪机制里的位置
- [Tor Browser 进阶设定](docs:tools/tor-browser-advanced/)：指纹抗性与窗口大小的实际操作
- [威胁模型如何建立](docs:basics/threat-model/)：先确认要防范谁，再选工具

[^brave]: [Brave improves protections against GPU fingerprinting](https://brave.com/privacy-updates/38-webgl-webgpu-fingerprinting-protections/) - Brave 隐私更新第 38 篇。本文引用的三项防护、爬取观察、兼容处理与后续规划皆出自此文。查证日 2026-08-14。
[^farbling]: [Fingerprinting defenses 2.0](https://brave.com/privacy-updates/4-fingerprinting-defenses-2.0/) - Brave 隐私更新第 4 篇，2020 年。farbling 的定义、HMAC256 种子机制与研究出处出自此文，第三方 frame 沿用顶层种子的说明另见 Brave 的 [Fingerprinting Protections wiki](https://github.com/brave/brave-browser/wiki/Fingerprinting-Protections)。wiki 页面会被持续编辑，查证日 2026-08-18。
[^tor]: [Browser Fingerprinting: An Introduction and the Challenges Ahead](https://blog.torproject.org/browser-fingerprinting-introduction-and-challenges-ahead/) - Pierre Laperdrix，The Tor Project 博客，2019 年 9 月 4 日。一致化路线、letterboxing 与可指纹化隐私增强技术悖论的说明出自此文，文中的具体做法对应撰文当时的 Tor Browser 版本，该悖论一词出自 Eckersley 的 PETS 2010 论文，由本文引用。查证日 2026-08-18。
[^mdn]: [WEBGL_debug_renderer_info](https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_debug_renderer_info) - MDN Web Docs。两个常数的定义，以及 Firefox 在 `privacy.resistFingerprinting` 为 true 时停用此扩展的说明。查证日 2026-08-18。
