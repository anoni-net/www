---
title: Gears 文件工作台与本机处理的设计
description: 社区从文档站的小工具延伸出 Gears 文件工作台的原因，以及它如何用 CSP、依赖包审查与统计白名单，让读者自行检查文件是否离开设备。
date: 2026-10-24
---

手机拍的照片里，通常记着拍摄地点的经纬度、手机型号与精确到秒的时间。聊天截屏上有对方的名字与头像，Word 文件记着作者、公司名称，有时还有电脑上的文件夹路径。这类信息统称元数据（metadata），平常无害。文件一旦交给记者、贴到网络上或寄给不完全信任的人，就可能让提供文件的人被认出来。

清除这些信息的在线服务不少，几乎都要先上传文件。为了保护一张照片，反而需先把它交给一台不认识的服务器。[Gears 文件工作台](https://anoni.net/gears/zh-cn/)把清除元数据、遮蔽个人信息、加密这些处理放进读者的浏览器，文件默认不离开设备。Gears 也用了文档站不能用的依赖包与模型，所以页面可以连到哪里，都写在读者能自行检查的地方。

## 另外做一个产品的原因

Gears 的前身是文档站的[小工具区](docs:utils/)。扣除机器流量之后，小工具区是文档站首页以外最多人使用的一区，用得最多的是清除元数据、遮蔽、密码短语生成器、QR code 与网址清理。使用的人多半是一般的正体中文用户，需求跟 Tor 没有直接关系。

文档站的小工具有三条规则：离线可用、页面不联网、没有构建流程。这些规则让文档站在断网的地方仍然可用，也限制了工具的规模。检测人脸只能用 240 KB 的轻量检测器，常常漏掉合照里的小脸，清除元数据的工具也无法读取 iPhone 默认的 HEIC 照片。从搜索引擎进来的读者又几乎不会进到小工具区，需要这些工具的人不容易发现它们。

2026-10-14 我们决定把小工具延伸成独立的产品，文档站的小工具维持原样。Gears 可以用 npm 包、打包工具与几百 MB 的模型，换来文档站无法提供的功能，包括 HEIC 照片的清除、PDF 的遮蔽、录音转逐字稿与查证收到的文件。Gears 的首页（桌面）依读者的目的分成「交出去之前」、「安全地发送」、「检查收到的」三组，所有工具共用一个只存在内存里的暂存区，关掉标签页就清空。两天后第一版上线，逐字稿与查证已经在里面，远程传送接着在 10-20 加入。

![Gears 的桌面，左侧是暂存区与选择文件的按钮，右侧的工具分成交出去之前、安全地发送、检查收到的三组](https://assets.anoni.net/www/articles/gears-local-first-1.zh-CN-a7519403.webp)

## 取代「页面不联网」的检查方式

文档站的小工具因为有「页面不联网」的规则，读者不必相信我们，也能确定文件不会被送走。Gears 拿掉了这条规则。npm 包里有几万行不是我们写的程序，逐字稿的大模型要从 Hugging Face（公开的机器学习模型托管平台）下载，远程传送要经过社区的服务器。每多一项，读者就多一处无法自行确认、只能相信我们说法的地方。

Gears 把页面可以连接的对象写在读者能自行检查的地方，需要联网的功能逐一说明发送了什么、谁可以得知。还没做到的部分也不回避，一并写出来。

## 页面的 CSP

CSP（Content Security Policy，内容安全政策）是网站交给浏览器的一份规则，列出页面可以从哪里加载程序、可以连接到哪里，规则以外的请求由浏览器直接挡下。Gears 在每个页面的 `<head>` 放一个 meta 标签，clearnet 版（一般网络上的 anoni.net）的内容如下（两个发送网址换成说明）：

```
default-src 'none'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self';
img-src 'self' blob: data:; media-src blob:;
connect-src 'self' <使用统计的发送网址> <建议与反馈的发送网址>;
worker-src 'self' blob:; font-src 'self'; manifest-src 'self';
base-uri 'none'; form-action 'none'
```

`connect-src` 限制程序可以连接的对象。即使某个依赖包被植入恶意程序，`fetch`、`XMLHttpRequest` 与 WebSocket 也只能连到 Gears 自己的域名与两个发送网址，读者的文件无法发送。规则就在页面源代码里，在浏览器选「查看源代码」就可以看到，不必相信我们的说法。`wasm-unsafe-eval` 让 HEIC 解码器与辨识模型可以运行 WebAssembly（浏览器里以接近原生速度运行的程序格式），它只允许编译 WebAssembly，JavaScript 的 `eval` 仍然无法使用。

规则由 [`vite.config.ts`](https://github.com/anoni-net/gears/blob/main/vite.config.ts) 的 `policy()` 生成，添加任何对外连接都要改那里，界面上也要标示。代码审查时可以直接看出添加了哪些连接。

## 逐字稿 Worker 的对外请求

逐字稿的语音辨识在 Web Worker（浏览器在后台另开的线程）里运行，避免转录时界面停住。Worker 从网址加载时，套用的是 Worker 脚本本身响应头里的 CSP，页面 meta 标签的规则不适用于 Worker。

2026-10-15 加入逐字稿时，Transformers.js（在浏览器运行机器学习模型的库）内含一份 onnxruntime-web（模型的运行引擎），默认从 jsDelivr（公开的 CDN）下载 WebAssembly。当时只有 meta 标签的 CSP，Worker 不受限制，请求因此发了出去。改法是用 Vite 的 `?url` 导入那一份 WebAssembly，从自己的域名加载。nginx 也改成用响应头送一份 CSP，Worker 从此受到同一组规则约束。页面同时有响应头与 meta 标签时，请求要两边都符合才放行，页面本身仍然只能连到 meta 标签列出的对象。

同样的错误现在由浏览器测试把关。[`tests/e2e/guard.ts`](https://github.com/anoni-net/gears/blob/main/tests/e2e/guard.ts) 在每个测试记下页面发出的请求与控制台错误。只要有连到测试服务器以外的请求，或控制台出现被 CSP 挡下的错误，测试就失败。

逐字稿的 large-v3-turbo 约 760 MB，从社区的主机发送流量太重，改由读者选择之后从 Hugging Face 下载。按钮写成「从 Hugging Face 下载并开始」，按下之前界面先说明 Hugging Face 可以得知 IP 地址、浏览器与下载了哪个模型。响应头的 CSP 只允许那几个模型在固定 commit 下的下载路径。每个文件读完会比对 SHA-256 哈希值，不符就不保存，请求也不带 cookie 与 Referer。

![逐字稿选择模型的界面，选了 large-v3-turbo 之后，下方说明模型从 Hugging Face 下载、Hugging Face 会看到 IP 地址、浏览器与下载的模型，录音不会发送出去](https://assets.anoni.net/www/articles/gears-local-first-2.zh-CN-0b5b6117.webp)

## 依赖包添加的对外连接

CSP 是最后一道防线，平常的检查在升级依赖包时进行，先在依赖包里搜索对外的网址。2026-10-15 Gears 加入人脸检测时，第一版用的是 MediaPipe（Google 的机器学习库）。选版本时在依赖包里搜索，发现 `@mediapipe/tasks-vision` 从 1.0.0 起多了送往 `odml.pa.googleapis.com` 的网址，所以停在还没有这段程序的 0.10.35。CSP 可以挡下这种请求，但挡下之后控制台会留下错误，也很难确定依赖包在请求失败之后运行了哪一段程序。所以要在升级时就发现依赖包添加的对外连接。同一天人脸检测因为准确度改用 OpenCV 的 YuNet，MediaPipe 也从 Gears 移除。

有些请求只能靠 CSP 挡下。查证工具用 c2pa-web（C2PA 标准的开源库）验证内容凭证（相机与编辑软件附在文件上的来源记录）。遇到其中的身份声明时，底下的 c2pa-rs 会连接取得签发者的密钥，而且没有设置可以关闭（[c2pa-rs issue #1645](https://github.com/contentauth/c2pa-rs/issues/1645)）。这个请求由 CSP 挡下，是 Gears 唯一预期会出现的 CSP 错误，测试只允许这一个路径的错误。

## 网址检查的本机比对

收到可疑的短信链接时，读者可以贴进 Gears 的网址检查，比对 165 反诈骗咨询专线公开的「遭停止解析涉诈网站」清单。最直接的做法是把网址送到服务器查询，但服务器上的查询记录会累积成一份名单，记下谁收到了哪些诈骗链接。

2026-10-14 查证时，清单有 86,173 个不重复的域名，整理成纯文本约 1.5 MB。压缩后约 400 KB，整份放进浏览器比对也不算大。Gears 在部署时下载清单，跟网站一起送到读者的浏览器，网址完全不必发送。清单里有共用平台的子域名，为了不把整个平台标成诈骗，比对时用完整的主机名称。清单只收已经停止解析的域名，界面上也写明不在清单里不代表安全。

我们评估之后决定不展开短网址。由服务器代为连接的话，任何人都能用自己的短网址取得主机的真实 IP，主机也可能被当成探测内部网络的跳板。诈骗短信常给每个收件人不同的短网址。代为展开时，诈骗方的记录会多一次点击，等于替读者向对方确认收到了消息。遇到短网址时，Gears 提醒读者请对方提供完整的网址。

## Cloudflare 的注入与压缩

读者取得的页面要跟构建产物相同，才能拿来跟公开的源代码比对。anoni.net 前面是 Cloudflare，它会在整个 zone（同一个域名的设置范围）的 HTML 响应里注入 Web Analytics 与 JS Detections（Cloudflare 的流量统计与机器人检测）的 script。Gears 的 CSP 会挡下这些 script，响应另外带上 `Cache-Control: no-transform`，要求 Cloudflare 不改动内容。

2026-10-17 第一次部署时，`no-transform` 加在所有文件上。带了它的响应，Cloudflare 完全不压缩，连 nginx 发送的 gzip 也会解开。上线后实测，1.5 MB 的 165 清单与 14 MB 的 onnxruntime WebAssembly 都以原始大小送到读者手上。注入只发生在 HTML，所以改成只有页面与图片带 `no-transform`（图片是为了避开 Polish 重新压缩）。其他文件交给 Cloudflare 压缩，WebAssembly 压缩后约小四分之三。

Cloudflare 在边缘节点（离读者最近的机房）解开 TLS，经过的文件在 Cloudflare 上是明文。所以 Gears 的原则写明，上传文件的端点不经过 Cloudflare。远程传送是例外，clearnet 的入口经过 Cloudflare，因为内容在两端之间另外加密。分享链接的 `#` 后面带着一把密钥，浏览器不会把 `#` 之后的内容送到服务器。两端用它导出密钥之后，每则消息再用 AES-256-GCM 加密，中继服务与 Cloudflare 只经手密文。

Cloudflare 仍然可以得知两端的 IP 与连接时间，生成链接之前界面上会写明。经过哪些服务器、记下什么，另外写在[远程传送的服务器说明](https://anoni.net/gears/zh-cn/remote-server/)。通信软件生成链接预览时，可能先在它的服务器上打开网址。为了不让预览占用一次性的房间，打开分享链接之后要按「加入」才会连接。

![远程传送生成链接之前的说明，路线是你、Cloudflare、中继服务器、对方，表格列出中继服务器与 Cloudflare 可得知 IP 地址与连接时间，无法得知文件名、内容与文字消息](https://assets.anoni.net/www/articles/gears-local-first-3.zh-CN-35f245b3.webp)

## 使用统计

维护者需要知道读者打开哪些工具、是否处理完、在哪里失败。Gears 不加载 Umami（开源的网站流量统计服务）的 script，由程序直接把事件送到社区自建的 Umami，CSP 只允许那一个网址。

每个事件只能带白名单里的字段，值也要在清单里，不符就整条不送。文件名、文件大小、文件内容、读者输入的文本、检查的网址、信件的寄件人、哈希值与查证的结果都不送，屏幕尺寸只取到百位数。浏览器开了 Do Not Track 或 Global Privacy Control（浏览器通知网站不要追踪的设置）时一律不送，读者也可以在页脚选择不记录。构建 onion 版（通过 Tor 连接的 .onion 网站）时会移除整段统计程序，产物里没有发送统计的代码。

## Tor Browser 的 canvas 随机数

onion 版放在 `gears.<onion>`，构建之后由 `scripts/check-site.mjs --onion` 确认产物里没有连到 clearnet 的 anoni.net。2026-10-17 制作 onion 版时，我们发现在 Tor Browser 15.0 的标准安全级别下，canvas（网页上用程序绘图的组件）的 `getImageData` 与 `toBlob` 在读者允许之前一律返回随机数而不报错。HEIC 转 JPEG、PDF 转成图片这类要从 canvas 读回像素的工具，因此输出一张看起来正常、内容却是噪点的图。

现在 `src/ui/canvas-access.ts` 在读取之前先画四个点再读回比对，不符就停止。界面会请读者在地址栏的 canvas 图标允许之后再按一次，同一个标签页之后就正常。

Tor Browser 不支持 service worker（让网页离线也能打开的后台程序），onion 版不能离线使用。Tor Browser 也没有 cross-origin isolation（多线程运算需要的隔离设置），逐字稿只能用 1 个 CPU 内核。WebRTC 完全停用，面对面传送无法使用。这些限制都写在界面上，原本面对面传送的位置改为建议使用远程传送，或完全不经过服务器的 OnionShare（通过 Tor 分享文件的开源工具）。

## 目前的对外连接

Gears 目前的对外连接如下表，打开浏览器开发者工具的网络面板就能逐项对照。

| 连到哪里 | 什么时候 | 发送什么、谁可得知 |
|---|---|---|
| anoni.net 自己的域名 | 打开页面、第一次用到某个工具时 | 页面、程序与模型文件的请求，不含读者的文件 |
| 社区自建的 Umami | 使用工具时，开了 Do Not Track、Global Privacy Control 或选择不记录时不送 | 工具代号、事件与失败原因的代码 |
| 社区自建的 Formbricks（开源的表单服务） | 读者在「建议与反馈」按下提交 | 读者填写的内容、从哪个工具过来、界面语言与版本 |
| assets.anoni.net | 读者选了社区转换的逐字稿模型 | 模型文件的请求 |
| Hugging Face | 读者选择逐字稿的 large-v3-turbo，并按下下载 | 模型文件的请求，Hugging Face 可得知 IP、浏览器与下载的模型 |
| 远程传送的中继服务 | 读者生成或加入远程传送的链接 | 两端之间加密过的内容，经手的 Cloudflare 可得知 IP 与时间 |
| Cloudflare Realtime 的 TURN（无法直接连接时转送音视频的服务器） | 远程传送的视频通话 | 加密过的音视频，TURN 服务器可得知两端的 IP |

onion 版没有使用统计，社区转换的模型也改由同一个 onion 网站提供。

## 还没做到的部分

在 clearnet 选择从 Hugging Face 下载大模型时，Hugging Face 可以得知读者的 IP。远程传送的视频通话经过 Cloudflare Realtime 的 TURN，社区自建的 coturn（开源的 TURN 服务器）已经设置好、验证过，还在等一台 VPS。

CSP 能防范被植入恶意程序的依赖包，无法防范被入侵的服务器。服务器被入侵时，发送的页面连同 CSP 都可能被替换。要确认网站上运行的就是 repo 里的源代码，需要两段比对。第一段是网站与 `build` 分支：网站在 GitHub Actions 公开构建，产物推到 repo 公开的 `build` 分支，读者现在就可以拿网站上的文件跟它比对。

第二段是 `build` 分支与源代码，也就是可重现构建（reproducible build）：任何人从同一个 commit 构建，都要得到逐字节相同的文件。这部分还没做到，也还没验证过。已知的障碍是 165 清单在构建时下载，网站每周一自动重建一次。同一个 commit 在不同周构建出来的清单不同，service worker 的版本号也跟着不同。

Gears 还在 Beta，文中的版本、数字与文件位置都是发文时的状态。对实现的意见欢迎到 [anoni-net/gears](https://github.com/anoni-net/gears) 开 issue，也可以在 Gears 的「建议与反馈」留言。

## 相关阅读

- [文档站离线阅读与本机加密的技术设计](/articles/offline-first-docs/)：Gears 的离线使用与 age 加密沿用同一套思路
- [远程传送的服务器说明](https://anoni.net/gears/zh-cn/remote-server/)：中继服务经过哪些服务器、可以得知与保存什么
- [Gears 的设计文档](https://github.com/anoni-net/gears/blob/main/AGENTS.md)：本文提到的每一项设计，在这里有完整的规格与测试方式
