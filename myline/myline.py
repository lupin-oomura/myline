from flask import request

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
)


class myline:
    configuration = None
    handler = None
    line_bot_api = None

    def __init__(self, access_token, secret):
        self.configuration = Configuration(access_token=access_token)
        self.handler = WebhookHandler(secret)
        self.line_bot_api = MessagingApi(ApiClient(self.configuration))

    def handle(self) -> str :
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
 
        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError:
            return "error:Invalid signature. Please check your channel access token/channel secret."

        return 'OK'

    def get_username(self, event) :
        profile = self.line_bot_api.get_profile(event.source.user_id)
        return profile.display_name

    def get_handler(self) :
        return self.handler
    
    def send_message(self, event, text):
        if text.strip() == "" :
            print("no message")
            return
        
        message_dict = {
            'to': event.source.user_id,
            'messages': [
                {'type': 'text', 'text': text},
            ]
        }
        self.line_bot_api.push_message_with_http_info(
            PushMessageRequest.from_dict(message_dict)
        )

    def reply_message(self, event, text) :
        if text.strip() == "" :
            print("no message")
            return

        self.line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"{text}")]
            )
        )

    def send_image(self, event, original_url, preview_url):
        message_dict = {
            'to': event.source.user_id,
            'messages': [{
                'type': 'image',
                'originalContentUrl': original_url,
                'previewImageUrl': preview_url
            }]
        }
        self.line_bot_api.push_message_with_http_info(
            PushMessageRequest.from_dict(message_dict)
        )



    # def send_video(self, event, original_url, preview_url):
    #     message_dict = {
    #         'to': event.source.user_id,
    #         'messages': [
    #             {'type': 'video',
    #              'originalContentUrl': original_url,
    #              'previewImageUrl': preview_url}
    #         ]
    #     }
    #     self.line_bot_api.push_message_with_http_info(
    #         PushMessageRequest.from_dict(message_dict)
    #     )

    # You can add more methods for other message types




# #--- Sample Program ---
# import os
# from flask import Flask, request, abort
# from linebot.v3.webhooks import (
#     MessageEvent,
#     TextMessageContent
# )
# from myline import myline

# at = os.getenv('LINE_ACCESS_TOKEN')
# secret = os.getenv('LINE_SECRET_KEY')

# app = Flask(__name__)
# ml = myline(at, secret)
# line_handler = ml.get_handler()


# @app.route("/")
# def test() :
#     return "running"

# @app.route("/callback", methods=['POST'])
# def callback():
#     if ml.handle() != "OK" :
#         app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
#         abort(400)

# # ハンドラの登録
# @line_handler.add(MessageEvent, message=TextMessageContent)
# def handle_message_wrapper(event):
#     ml.send_message(event, "⌛")
#     ml.reply_message(event, f"you said {event.message.text}")

# if __name__ == "__main__":
#     app.run()
# #--- Sample Program ---

#----------------------------------------------------------------#
#--- ローカルで通信を試す場合、ngrokがすごく便利 -------------------#
#----------------------------------------------------------------#
# ./ngrok http http://localhost:5000
# 初めて使うときは、トークン認証を通す必要がある。
# ngrok config add-authtoken マイページにある認証トークン
