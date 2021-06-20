from flask import Flask #建立網站伺服器 使用 Flask 模組
import requests
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET 
app = Flask(__name__)

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage,LocationSendMessage, QuickReply, QuickReplyButton, MessageAction

line_bot_api=LineBotApi('7yMZm3UwGAaSNmWMbyiMDaW3jbwNSrptj1yvlXVyY6iitRtcqoW9R2L0KWLWDkpXvxAv897OxbLEqpK7l2afuQBH23kKuSLAJUk3MvxmK/cBLBrOeVkdQFLs4+6OPpkZlrEE2YWDiKI5QRHLk/62IAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e8a77aff27140aa956a696e74fd8461b')

@app.route("/callback", methods=['POST'])#建立callback路由，檢查LINE Bot的資料是否正確
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)#如果接到使用者傳送的訊息，就將相對應的文字訊息傳回
def handle_message(event):
    mtext = event.message.text #取得使用者傳送的文字於mtext變數中
    前期=monoNum(1)+'\n\n'+monoNum(2)
    if (mtext == '@本期中獎號碼') : #顯示本期中獎號碼(@是特殊指令與一般使用者輸入文字做區別)
        try:
            message = TextSendMessage(text = monoNum(0))
            line_bot_api.reply_message(event.reply_token,message) #LINE Bot回傳文字訊息
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!')) #LINE Bot發生錯誤時，回傳「發生錯誤」訊息
    elif (mtext == '@前期中獎號碼') :#顯示前期中獎號碼(@是特殊指令與一般使用者輸入文字做區別)
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
    elif(len(mtext) == 3 and mtext.isdigit()):     #判斷是否中獎        
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

def monoNum(n):
    content=requests.get('https://invoice.etax.nat.gov.tw/invoice.xml')           
    tree = ET.fromstring(content.text) 
    items = list(tree.iter(tag='item'))
    title = items[n][0].text
    ptext = items[n][2].text
    ptext = ptext.replace('<p>','').replace('</p>','\n')
    return title + '月\n'+ptext[:-1]

if __name__ == '__main__':
    app.run()




