# feel2

## 專案說明
---
- 主程式: main_control.py
- unit_test資料夾: 個別模組的單元測試.py檔
- sounds開頭的資料夾: 音效檔
- csv檔: 儲存色票, 播放次數, 對應音效, Code的對應資料表
- uniility資料夾: 存放檔案命名小工具


開機後自動執行autostart.sh，此程式會呼叫main_control.py，整個專案都透過此檔案執行，會先讀取all.csv，儲存Code與音檔的對應關係、載入背景音樂，此過程大約需要兩分鐘
運行過程中採用多執行緒的方式控制，步徑馬達、伺服馬達、QRCode讀取、音效播放、背景音樂播放、LED控制...分別開執行緒控制。

## 模組
---
| 名稱 | 控制方式 | 備註 |
| --- | --- | --- |
| QR Code Scanner GM77| Serial Input | 若要變更掃描設定(間隔、音效...)請參見manuel |
| LED | GPIO(27) | |
| Switch | GPIO(17) | 控制播放的按鈕
| 電位器 | GPIO(2,3,4) | 控制步徑馬達 |
| 繼電器 | GPIO(22) | 控制步徑馬達 |
| Servo | GPIO(18) | 控制角度 |


*GPIO皆為BCM pin*

## 開發環境要求
---

- Python3.7
- Pydub作為聲音引擎
- Raspberry Pi Model 4B(Rasbian OS)

## 畫作說明
---
1: 秀拉-星期日午後的加特島
2: 秀拉-馬戲團
3: 秀拉-騒動舞
4: 希涅克-費利克斯-芬尼的肖像 

## 常用連結
---
[音檔和色票對應file](https://docs.google.com/spreadsheets/d/1vDnh0Sb9ZLYLoW9fTqGnQfbzMFge6I3uIEwoA7uLpns/edit#gid=0)
[音色列表](https://docs.google.com/document/d/1vvbD43TpmT22kZZp7BF6BkinNLo6mANS4iosYzWDRcw/edit?usp=sharing)
