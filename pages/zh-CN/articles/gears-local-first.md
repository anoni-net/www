---
title: Gears 文件工作台与本机处理的设计
description: 社区从文档站的小工具延伸出 Gears 文件工作台的原因，以及它如何用 CSP、依赖包审查与统计白名单，让文件不离开设备成为读者能检查的事。
date: 2026-10-24
---

手机拍的照片里，通常记着拍摄地点的经纬度、手机型号与精确到秒的时间。聊天截图上有对方的名字与头像，Word 文件记着作者、公司名称，有时还有电脑上的文件夹路径。这些信息平时无害，文件一旦交给记者、发到网上，或寄给不完全信任的人，就可能让提供文件的人被认出来。

清除这些信息的在线服务不少，几乎都要先上传文件。为了保护一张照片，先把它交给一台不认识的服务器，顺序是反的。[Gears 文件工作台](https://anoni.net/gears/zh-cn/)把清除元数据、遮蔽个人信息、加密这些处理放进读者的浏览器，文件默认不离开设备。

## 另外做一个产品的原因

Gears 的前身是文档站的[小工具区](docs:utils/)。扣掉机器流量之后，小工具区是文档站首页以外使用最多的一区，用得最多的是清除元数据、遮蔽、密语生成器、QR code 与网址清理。使用的人大多是一般的正体中文用户，需求跟 Tor 没有直接关系。

文档站的小工具守着三条规则：离线可用、页面不联网、没有构建流程。规则让文档站在断网的地方照样能用，也让工具长不大。找人脸只能用 240 KB 的轻量检测器，合照里的小脸常常漏掉，清除元数据也读不了 iPhone 默认的 HEIC 照片。从搜索引擎进来的读者又几乎不会逛到小工具区，工具做好了，需要的人却找不到。

2026-10-14 我们决定把小工具延伸成独立的产品，文档站的小工具维持原样。Gears 可以用 npm 包、打包工具与几百 MB 的模型，换来文档站做不到的功能：HEIC 照片的清除、PDF 的遮蔽、录音转逐字稿、查证收到的文件。桌面按读者的目的分成交出去之前、安全地发送、检查收到的三组，所有工具共用一个只存在内存里的暂存区，关掉标签页就清空。两天后第一版上线，逐字稿与查证已经在里面，远程传送接着在 10-20 加入。

![Gears 的桌面，左侧是暂存区与选择文件的按钮，右侧的工具分成交出去之前、安全地发送、检查收到的三组](https://assets.anoni.net/www/articles/gears-local-first-1.zh-CN-a7519403.webp)

## 拿掉「页面不联网」之后

文档站的小工具有「页面不联网」这条规则撑着，读者不必相信我们，也知道文件不会被送走。Gears 拿掉了这条规则。npm 包里有几万行不是我们写的代码，逐字稿的大模型要从 Hugging Face 下载，远程传送要经过社区的服务器。每多一项，文件会不会被送走就多一分只能听我们说。

Gears 把页面能连到哪里写死在读者可以自行检查的地方，需要联网的功能逐一说明发送了什么、谁看得到，还做不到的部分如实写出来，用这种方式守住同一个承诺。下面是做法，以及开发这两周出过的三个错。

## 页面的 CSP

CSP（Content Security Policy，内容安全策略）是网站交给浏览器的一份规则，列出页面可以从哪里加载代码、可以连接到哪里，规则以外的请求由浏览器直接拦下。Gears 的每个页面在 `<head>` 里放一个 meta 标签，clearnet 版的内容如下（两个提交网址换成说明）：

```
default-src 'none'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self';
img-src 'self' blob: data:; media-src blob:;
connect-src 'self' <使用统计的提交网址> <建议与反馈的提交网址>;
worker-src 'self' blob:; font-src 'self'; manifest-src 'self';
base-uri 'none'; form-action 'none'
```

重点在 `connect-src`。即使某个依赖包被植入恶意代码，`fetch`、`XMLHttpRequest` 与 WebSocket 也只能连到自己的域名与两个提交网址，读者的文件发不出去。规则就在页面源代码里，在浏览器选「查看网页源代码」就看得到，不必相信我们的说法。`wasm-unsafe-eval` 给 HEIC 解码器与识别模型用的 WebAssembly，它只允许编译 WebAssembly，JavaScript 的 `eval` 仍然不能用。

规则产生在 [`vite.config.ts`](https://github.com/anoni-net/gears/blob/main/vite.config.ts) 的 `policy()`。新增任何对外连接都要改那里，界面上也要标示，代码审查时一眼就看得出来。

## 逐字稿 Worker 的对外请求

第一个错出在逐字稿。识别在 Web Worker 里执行，避免转录时界面卡住。Worker 从网址加载时，套用的是 Worker 脚本自己响应头里的 CSP，页面 meta 标签的规则管不到它。

2026-10-15 加入逐字稿时，Transformers.js 带着自己的一份 onnxruntime-web，默认从 jsDelivr 的 CDN 下载 WebAssembly。当时只有 meta 标签的 CSP，Worker 不受限制，请求真的发出去了。改法是用 Vite 的 `?url` 导入那一份 WebAssembly，从自己的域名加载，nginx 也改成用响应头发送一份 CSP，Worker 从此受到同一组规则约束。页面同时有响应头与 meta 标签时，请求要两边都符合才放行，页面本身仍然只能连到 meta 标签列出的对象。

同样的错误现在由浏览器测试把关。[`tests/e2e/guard.ts`](https://github.com/anoni-net/gears/blob/main/tests/e2e/guard.ts) 在每个测试记下页面发出的请求与控制台错误，连到测试服务器以外的请求，以及被 CSP 拦下时留在控制台的错误，都会让测试失败。

逐字稿的 large-v3-turbo 约 760 MB，从社区的主机发出流量太重，改由读者选择之后从 Hugging Face 下载。按钮写成「从 Hugging Face 下载并开始」，按下之前界面先说明 Hugging Face 看得到 IP 地址、浏览器与下载了哪个模型。响应头的 CSP 只开那几个模型、锁定 commit 的下载路径，每个文件读完比对 SHA-256，对不上就不保存，请求也不带 cookie 与 Referer。

![逐字稿选择模型的界面，选了 large-v3-turbo 之后，下方说明模型从 Hugging Face 下载、Hugging Face 会看到 IP 地址、浏览器与下载的模型，录音不会发送出去](https://assets.anoni.net/www/articles/gears-local-first-2.zh-CN-0b5b6117.webp)

## 依赖包新增的对外连接

CSP 是最后一道防线，平时要靠升级依赖包时先在包里搜索对外的网址。2026-10-15 Gears 第一次加入找人脸时用的是 MediaPipe。选版本时在包里搜索，发现 `@mediapipe/tasks-vision` 从 1.0.0 起多了发往 `odml.pa.googleapis.com` 的网址，所以停在还没有这段代码的 0.10.35。CSP 拦得下这种请求，但拦下之后控制台会留下错误，也很难确定依赖包在请求失败之后走了哪一条路，依赖包新增的对外连接要在升级时就发现。同一天找人脸因为准确度换成 OpenCV 的 YuNet，MediaPipe 也就从 Gears 拿掉了。

也有只能靠 CSP 的情况。查证工具用 c2pa-web 验证内容凭证（相机与编辑软件附在文件上的来源记录），遇到其中的身份声明时，底下的 c2pa-rs 会联网取得签发者的密钥，没有设置可以关掉（[c2pa-rs issue #1645](https://github.com/contentauth/c2pa-rs/issues/1645)）。这个请求由 CSP 拦下，是 Gears 唯一预期会出现的 CSP 错误，测试只放过这一个路径。

## 网址检查不发送网址

收到可疑的短信链接时，读者可以贴进 Gears 的网址检查，比对台湾 165 反诈骗咨询专线公开的「遭停止解析涉诈网站」清单。最直接的做法是把网址发到服务器查询，但查询记录会累积成一份「谁收到了哪些诈骗链接」的数据。

2026-10-14 查证时，清单有 86,173 个不重复的域名，整理成纯文本约 1.5 MB。压缩后约 400 KB，整份放进浏览器比对也不算大。Gears 在部署时下载清单，跟网站一起送到读者的浏览器，网址完全不必发出。比对用完整的主机名，清单里有共享平台的子域名，不能把整个平台标成诈骗。清单只收已经停止解析的域名，界面上也写明不在清单里不代表安全。

短网址的展开评估过之后决定不做。由服务器代为访问的话，任何人都能用自己的短网址取得主机的真实 IP，也可能被当成探测内网的跳板。诈骗短信又常给每个收件人不同的短网址，代为展开，在对方那边就记成一次点击，等于替读者确认收到了消息。遇到短网址时，Gears 提醒读者请对方提供完整的网址。

## Cloudflare 的注入与压缩

第二个错跟 Cloudflare 有关。anoni.net 前面是 Cloudflare，它会在整个 zone 的 HTML 响应里注入 Web Analytics 与 JS Detections 的 script。Gears 的 CSP 会拦下这些 script，但读者取得的页面应该跟构建出来的一样，所以响应带上 `Cache-Control: no-transform`，要求 Cloudflare 不改动内容。

2026-10-17 第一次部署时，`no-transform` 加在所有文件上。带了它的响应，Cloudflare 完全不压缩，连 nginx 发出的 gzip 也会解开，上线后实测 1.5 MB 的 165 清单与 14 MB 的 onnxruntime WebAssembly 都以原始大小送到读者手上。注入只发生在 HTML，所以改成只有页面与图片带 `no-transform`（图片是为了避开 Polish 重新压缩）。其他文件交给 Cloudflare 压缩，WebAssembly 压缩后约小四分之三。

Cloudflare 在边缘解开 TLS，经过它的文件对它来说是明文，所以 Gears 的原则写明，上传文件的端点不经过 Cloudflare。远程传送是例外，clearnet 的入口经过 Cloudflare，因为内容在两端之间另外加密。分享链接的 `#` 后面带着一把密钥，浏览器不会把 `#` 之后的内容发到服务器。两端用它导出密钥之后，每条消息再用 AES-256-GCM 加密，中继服务与 Cloudflare 只经手密文。

Cloudflare 仍然看得到两端的 IP 与连接时间，生成链接之前界面上会写明，经过哪些服务器、记下什么另外写在[远程传送的服务器说明](https://anoni.net/gears/zh-cn/remote-server/)。打开分享链接之后也要按「加入」才会连接。通讯软件生成链接预览时，可能在它的服务器上先打开这个网址，自动加入的话，一次性的房间会被预览用掉。

![远程传送生成链接之前的说明，路线是你、Cloudflare、中继服务器、对方，表格列出中继服务器与 Cloudflare 可得知 IP 地址与连接时间，无法得知文件名、内容与文字消息](https://assets.anoni.net/www/articles/gears-local-first-3.zh-CN-35f245b3.webp)

## 使用统计

维护者需要知道读者打开哪些工具、有没有处理完、在哪里失败。Gears 不加载 Umami 的 script，由代码直接把事件发到社区自建的 Umami，CSP 只开那一个网址。

每个事件只能带白名单里的字段，值也要在清单里，对不上就整条不发。文件名、文件大小、文件内容、读者输入的文字、检查的网址、邮件的发件人、哈希值与查证的结果都不发，屏幕尺寸只取到百位数。浏览器开了 Do Not Track 或 Global Privacy Control 时一律不发，页脚也可以选择不要记录。onion 版在构建时把整段代码拿掉，构建产物里没有发送统计的代码。

## Tor Browser 读到的随机数

第三个错出现在 2026-10-17 做 onion 版的时候。Tor Browser 15.0 在标准安全级别下，读者允许之前，canvas 的 `getImageData` 与 `toBlob` 一律返回随机数，不会报错。HEIC 转 JPEG、PDF 转成图片这类要从 canvas 读回像素的工具，因此输出一张看起来正常、内容却是噪点的图。

现在 `src/ui/canvas-access.ts` 在读取之前先画四个点、读回来比对，对不上就停下来，请读者在地址栏的 canvas 图标允许之后再按一次，同一个标签页之后就正常。

onion 版放在 `gears.<onion>`，构建之后由 `scripts/check-site.mjs --onion` 确认构建产物里没有连到 clearnet 的 anoni.net。Tor Browser 没有 service worker，不能离线使用。没有 cross-origin isolation，逐字稿只能用 1 个 CPU 核心。WebRTC 也整个关掉，面对面传送不能用。这些限制都写在界面上，面对面传送的位置建议改用远程传送，或完全不经过服务器的 OnionShare。

## 目前的对外连接

整理成一张表，打开浏览器开发者工具的网络面板就能对照：

| 连到哪里 | 什么时候 | 发送什么、谁看得到 |
|---|---|---|
| anoni.net 自己的域名 | 打开页面、第一次用到某个工具时 | 页面、代码与模型文件的请求，不含读者的文件 |
| 社区自建的 Umami | 使用工具时，开了 Do Not Track、Global Privacy Control 或选择不记录时不发 | 工具代号、事件与失败原因的代码 |
| 社区自建的 Formbricks | 读者在「建议与反馈」按下提交 | 读者填写的内容、从哪个工具过来、界面语言与版本 |
| assets.anoni.net | 读者选了社区转换的逐字稿模型 | 模型文件的请求 |
| Hugging Face | 读者选择逐字稿的 large-v3-turbo，并按下下载 | 模型文件的请求，Hugging Face 看得到 IP、浏览器与下载的模型 |
| 远程传送的中继服务 | 读者生成或加入远程传送的链接 | 两端之间加密过的内容，经手的 Cloudflare 看得到 IP 与时间 |
| Cloudflare Realtime 的 TURN | 远程传送的视频通话 | 加密过的音视频，TURN 看得到两端的 IP |

onion 版没有使用统计，社区转换的模型也改由同一个 onion 网站提供。

## 还没做到的部分

在 clearnet 选择从 Hugging Face 下载大模型时，Hugging Face 看得到读者的 IP。远程传送的视频通话经过 Cloudflare Realtime 的 TURN，社区自建的 coturn 已经配置好、验证过，还在等一台 VPS。

CSP 防的是被植入的依赖包，防不了被入侵的服务器，服务器被入侵时，发出的页面连同 CSP 都可以被换掉。要确认网站上执行的就是 repo 里的源代码，需要两段比对。第一段是网站与 `build` 分支：网站在 GitHub Actions 公开构建，构建产物推到 repo 公开的 `build` 分支，读者现在就可以拿网站上的文件跟它比对。

第二段是 `build` 分支与源代码，也就是可复现构建，任何人从同一个 commit 构建，都要得到逐字节相同的文件。这一段还没做到，也还没验证过。已知的障碍是 165 清单在构建时下载，每周一自动重新构建一次，同一个 commit 在不同周构建出来的清单不同，service worker 的版本号也跟着不同。

Gears 还在 Beta，文中的版本、数字与文件位置都是发文时的状态。对实现的意见欢迎到 [anoni-net/gears](https://github.com/anoni-net/gears) 开 issue，也可以在 Gears 的「建议与反馈」留言。

## 相关阅读

- [文档站离线阅读与本机加密的技术设计](/articles/offline-first-docs/)：Gears 的离线使用与 age 加密沿用同一套思路
- [远程传送的服务器说明](https://anoni.net/gears/zh-cn/remote-server/)：中继服务经过哪些服务器、看得到与保存什么
- [Gears 的设计文档](https://github.com/anoni-net/gears/blob/main/AGENTS.md)：本文提到的每一项设计，在这里有完整的规格与测试方式
