# CS381

開放平台軟體final-project:Line Bot 自動對發票機器人

### 簡介
此機器人透過Python網路爬蟲財政部公開資料，結合Line messaging API 實做一個簡易的發票兌獎機器人

平常對發票實需要額外下載APP來對獎，透過自行實作line bot 來省去額外的工作

### 使用說明
1.掃描QRcode將Line bot 機器人加入好友

2.相關指令

├── @輸入發票最後三碼           
├── @前期中獎號碼              
├── @本期中獎號碼

在輸入@前期中獎號碼/@本期中獎號碼後，過一段時間會顯示出相對應的資訊，@輸入發票最後三碼則會顯示出輸入末三碼的訊息，依指令輸入後即可判斷是否有中獎

### 實作細節

發票中獎號碼網頁為XML，因此使用Python內建的xml.etree.ElementTree模組來解析。

```
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET 
```
> 建立callback 路由，檢查LINE Bot 的資料是否正確

```
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
```








