import os
from flask import Flask, request, abort
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
# from myline import myline #ローカルのmyline.pyを使う場合
import myline #ライブラリのmyline.pyを使う場合

at = os.getenv('LINE_ACCESS_TOKEN')
secret = os.getenv('LINE_SECRET_KEY')

app = Flask(__name__)
# ml = myline(at, secret) #ローカルのmyline.pyを使う場合
ml = myline.myline(at, secret) #ライブラリのmyline.pyを使う場合
line_handler = ml.get_handler()


@app.route("/")
def test() :
    return "running"

@app.route("/callback", methods=['POST'])
def callback():
    if ml.handle() != "OK" :
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

# ハンドラの登録
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message_wrapper(event):
    ml.send_message(event, "⌛")
    ml.reply_message(event, f"you said {event.message.text}")



if __name__ == "__main__":
    app.run()