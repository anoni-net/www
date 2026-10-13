---
title: 上传机敏信息流程
description: 把个人数据、爆料素材或敏感文件交给 anoni.net 社区的流程，使用社区自架的 Send，链接设成下载一次就失效，并加上另外约定的密码。给社区成员与外部协作者。
---

需要把个人数据、爆料素材或敏感的协作文件交给社区成员时，请用社区自架的 Send 上传，再把分享链接传给收件人。文件在你的浏览器加密后才上传，链接在下载一次或 7 天后失效，下载时还要输入另外约定的密码。服务器保存哪些数据、保存多久，见 [send.anoni.net 的数据处理](/services/send/)。

## 上传流程

1. 前往社区自架的 [Send](https://send.anoni.net/)。
2. 选择要上传的文件。
3. 失效条件设成「**一次下载**」与「**7 天**」，两者先到的为准。
4. 勾选「**使用密码保护**」，填入事先与收件人约定的密码。
5. 确认设置后点击「**上传**」。

上传完成后会产生分享链接，点击「复制链接」再传给收件人。

!!! danger "链接与密码分开传送"

    分享链接里含有解密的密钥，取得链接的人只要再有密码就能下载文件。密码要用跟链接不同的渠道约定，例如链接用 email 寄、密码当面或用 Signal 告知，其中一个渠道泄露时文件仍然安全。

!!! info ""

    [Send](https://github.com/timvisee/send) 是开源的自架文件分享软件，文件以端到端加密传送，分享链接会自动失效，文件不会永久留在网络上或邮件服务里。

## 流程示意图

前往 Send。

![Step 1](https://assets.anoni.net/docs/send-censorship-1.png){ .shot }

选择文件、设置失效条件，再送出。

![Step 2](https://assets.anoni.net/docs/send-censorship-2.png){ .shot }

复制链接传给收件人。

![Step 3](https://assets.anoni.net/docs/send-censorship-3.png){ .shot }
