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
        if tag == "you are welcome":
            return random.choice([
                { "text": "哪裡哪裡，您太客氣咯^^" },
                { "text": "不客氣 :)" },
                { "text": "謝謝您的支持!" },
                { "text": "不客氣，希望對您有幫助！" },
                { "text": "我才要謝謝您呢！" },
                ])
        return {
            "text": "：）"
        }

    def add_quick_replies(self, value_payloads=None, flags=None):
        # TODO: flags
        return [
                    {
                        "content_type": "text",
                        "title": "正確",
                        "payload": PAYLOAD_CONFIRM,
                        "image_url": "http://plainicon.com/download-icons/54418/plainicon.com-54418-3652-128px.png"
                    },
                    {
                        "content_type": "text",
                        "title": "校正",
                        "payload": PAYLOAD_FIX,
                        "image_url": "http://icons.iconarchive.com/icons/handdrawngoods/busy/128/pencil-icon.png"
                    },
                    {
                        "content_type": "text",
                        "title": "取消",
                        "payload": PAYLOAD_CANCEL
                    },
                    {
                        "content_type": "text",
                        "title": "更多",
                        "payload": PAYLOAD_MORE,
                        "image_url": "https://image.flaticon.com/icons/png/128/60/60969.png"
                    }
                ]


    def translated_string(self, msg):
        ret = {
                "text": msg,
            }
        ret['quick_replies'] = self.add_quick_replies()
        return ret

    def image(self, url):
        ret = {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": url
                }
            }
        }
        ret['quick_replies'] = self.add_quick_replies()
        return ret

    def ask_more(self, state):
        """ 「想知道更多」的選項 """

        # TODO: 圖片、食譜、哪裡買得到
        return {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "您想要知道什麼呢？",
                        "buttons": [
                            {
                                "type": "postback",
                                "title": "%s 的圖片" % (state.get_q()),
                                "payload": PAYLOAD_PICTURE + ":" + state.get_q(),
                            },
                            {
                                "type": "postback",
                                "title": "%s 的食譜" % (state.get_q()),
                                "payload": PAYLOAD_RECIPE + ":" + state.get_q(),
                            },
                            {
                                "type": "postback",
                                "title": "%s 在哪裡買得到" % (state.get_q()),
                                "payload": PAYLOAD_WHERE_TO_BUY + ":" + state.get_q(),
                            }
                        ]
                    }
                }
            }
