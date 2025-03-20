import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設置你的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('A3oUVaheUYgSpV+93g917AU5KASih9MdlVuEfQkJe1ZSC7WoPKvyFixZKawt/VSYUbDZDUmUMOrjUWZKjxXcyzMhwVDorisEegf7qwgGZyZgWS2aSvSTcKVbO8nx9s3xYhr2+3dPr8YyNWXi6FJEEAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6915f096ed9dea708c9c95f60e12f011')

@app.route("/callback", methods=['POST'])
@app.route("/", methods=['GET'])
def home():
    return "Welcome to the home page!"

def callback():
    # 確認請求來自 LINE
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 取得用戶發送的訊息
    user_message = event.message.text
    # 回覆用戶
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你說了: {user_message}")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
