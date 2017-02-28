import random
import json
from app.bot.constants import *

class ButtonTemplate:
    def __init__(self, text=""):
        self.button_list = []
        self.text = text
    
    def add_postback_button(self, title, payload):
        self.button_list.append({
            "type": "postback",
            "title": title,
            "payload": payload,
        })

    def set_text(self, s):
        self.text = s

    def generate(self):
        return {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": self.text,
                    "buttons": self.button_list
                }
            }
        }



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

    def ask_more(self, reply, user, msg, **template_params):
        """ 「想知道更多」的選項 """

        reply.set_text("您想要知道什麼呢？")
        reply.add_postback_button(title="%s 的圖片" % (user.get_q()),
                                  payload=PAYLOAD_PICTURE + ":" + user.get_q())
        reply.add_postback_button(title="%s 的食譜" % (user.get_q()),
                                  payload=PAYLOAD_RECIPE + ":" + user.get_q())
        reply.add_postback_button(title="%s 哪裡買得到" % (user.get_q()),
                                  payload=PAYLOAD_WHERE_TO_BUY + ":" + user.get_q())
