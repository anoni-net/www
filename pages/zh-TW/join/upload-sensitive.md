---
title: 上傳機敏資訊流程
description: 把個資、爆料素材或敏感檔案交給 anoni.net 社群的流程，使用社群自架的 Send，連結設成下載一次就失效，並加上另外約定的密碼。給社群成員與外部協作者。
---

需要把個人資料、爆料素材或敏感的協作檔案交給社群成員時，請用社群自架的 Send 上傳，再把分享連結傳給收件人。檔案在你的瀏覽器加密後才上傳，連結在下載一次或 7 天後失效，下載時還要輸入另外約定的密碼。伺服器保存哪些資料、保存多久，見 [send.anoni.net 的資料處理](/services/send/)。

## 上傳流程

1. 前往社群自架的 [Send](https://send.anoni.net/)。
2. 選擇要上傳的檔案。
3. 失效條件設成「**一次下載**」與「**7 天**」，兩者先到的為準。
4. 勾選「**使用密碼保護**」，填入事先與收件人約定的密碼。
5. 確認設定後按「**上傳**」。

上傳完成後會產生分享連結，按「複製連結」再傳給收件人。

!!! danger "連結與密碼分開傳送"

    分享連結裡含有解密的金鑰，取得連結的人只要再有密碼就能下載檔案。密碼要用跟連結不同的管道約定，例如連結用 email 寄、密碼當面或用 Signal 告知，其中一個管道外洩時檔案仍然安全。

!!! info ""

    [Send](https://github.com/timvisee/send) 是開源的自架檔案分享軟體，檔案以端對端加密傳送，分享連結會自動失效，檔案不會永久留在網路上或郵件服務裡。

## 流程示意圖

前往 Send。

![Step 1](https://assets.anoni.net/docs/send-censorship-1.png){ .shot }

選擇檔案、設定失效條件，再送出。

![Step 2](https://assets.anoni.net/docs/send-censorship-2.png){ .shot }

複製連結傳給收件人。

![Step 3](https://assets.anoni.net/docs/send-censorship-3.png){ .shot }
