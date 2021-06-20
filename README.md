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

> 讀取指令，並產生相對應的結果

```
    if (mtext == '@本期中獎號碼') :
        try:
            message = TextSendMessage(text = monoNum(0))
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!')) 
    elif (mtext == '@前期中獎號碼') :
        try:
            message =TextSendMessage(text = 前期)
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))        
    elif (mtext == '@輸入發票最後三碼') :      
        try:
            message=TextMessage(text='請輸入發票最後三碼進行對獎！')
        except:
             line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))  
```

> 擷取單期中獎號碼的函式財政部公開資料發票中獎號碼XML檔中，每一期中獎號碼位於<item>標籤。讀取<item>標籤解析其中資料，可以組合成一期中獎號碼文字資料。
    
```
    elif(len(mtext) == 3 and mtext.isdigit()):            
        try:
            content=requests.get('https://invoice.etax.nat.gov.tw/invoice.xml')           
            tree = ET.fromstring(content.text) 
            items = list(tree.iter(tag='item'))
            title = items[0][0].text
            ptext = items[0][2].text
            ptext = ptext.replace('<p>','').replace('</p>','')
            temlist = ptext.split('：')
            prizelist = []
            prizelist.append(temlist[1][5:8])
            prizelist.append(temlist[2][5:8])
            for i in range(3):
                prizelist.append(temlist[3][9*i+5:9*i+8])
            sixlist = temlist[4].split('、')
            for i in range (len(sixlist)):
                prizelist.append(sixlist[i])
            if mtext in prizelist:
                message = '符合某獎項後三碼，請自行核對發票前五碼!\n\n'
                message += monoNum(0)
            else:
                message = '很可惜，未中獎。請輸入下一張發票後三碼。'
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))
    else:
          line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請輸入發票最後三碼進行對獎！'))
```
    
>不同功能需要使用不同期別資料，因此將讀取一期中獎號碼資料並組合成顯是文字的功能寫成函式
```
    def monoNum(n):
    content=requests.get('https://invoice.etax.nat.gov.tw/invoice.xml')           
    tree = ET.fromstring(content.text) 
    items = list(tree.iter(tag='item'))
    title = items[n][0].text
    ptext = items[n][2].text
    ptext = ptext.replace('<p>','').replace('</p>','\n')
    return title + '月\n'+ptext[:-1]
```
    
### 參考    
- Requests: https://docs.python-requests.org/en/master/
- Python: https://www.python.org/
- Flask: https://flask.palletsprojects.com/en/2.0.x/
- LINE Developers: https://developers.line.biz/zh-hant/
- ngrok: https://ngrok.com/
- 財政部開放資料: https://www.einvoice.nat.gov.tw/
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

