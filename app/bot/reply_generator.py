import random
from app.bot.constants import *

class ReplyGenerator:
    def __init__(self):
        pass

    def sticker(self, tag):
        if tag == "thank you":
            return random.choice([
                #{ "attachment": {
                #    "type": "image",
                #    "payload": {
                #        "url": "http://i.giphy.com/3oz8xIsloV7zOmt81G.gif"
                #    }
                #}},
                { "text": "大感激呀~~~ ^__^" },
                { "text": "耶～謝謝你 :)" },
                { "text": "太感謝你了 :D" },
                { "text": "耶嘿～" },
                { "text": "謝謝你 (y)" },
                ])
        return {
            "text": "：）"
        }

    def translated_string(self, msg):
        return {
                "text": msg,
                "quick_replies":[
                    {
                        "content_type": "text",
                        "title": "正確",
                        "payload": TMT_CONFIRM_TRANSLATION,
                        "image_url": "http://plainicon.com/download-icons/54418/plainicon.com-54418-3652-128px.png"
                    },
                    {
                        "content_type": "text",
                        "title": "我要校正",
                        "payload": TMT_FIX_TRANSLATION
                    },
                    {
                        "content_type": "text",
                        "title": "取消",
                        "payload": TMT_CANCEL
                    }
                ]
            }
