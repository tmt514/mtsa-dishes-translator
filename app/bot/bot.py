import json
import urllib.request
import urllib.parse
from app.app import redis_store
from app.models import db, Term 
from datetime import datetime
from app.bot.constants import *
from app.bot.reply_generator import ReplyGenerator
from app.bot.intention_detector import IntentionDetector
from app.bot.intention_bot import IntentionBot
from app.bot.user_status import UserStatus
from app.bot.state_machine import StateMachine

import re
class Bot:
    """ 處理一切訊息的那隻 Bot
        理論上 app 取得 request 以後就會丟到這裡。
    """
    def __init__(self, app):
        self.app = app
        self.state = {}
        self.intention_detector = IntentionDetector(self)

        # 讓 Bot 方便使用 sendAPI 做事情用的
        self.intention_bot = IntentionBot()

        # 載入 state machine, 取得 state graph
        self.state_machine = StateMachine()

    def handle_message(self, msg, sender, msgbody):
        """ 處理訊息的函式。

            Keyword Arguments: 
            msg -- (dictionary) Facebook 的 Message 格式
            sender -- (string) sender_id
            msgbody -- (dictionary) 特別把 message 的部份挑出來，方便處理

            Return:
            不回傳任何東西
        """
        # 這段應該是測試的 code...
        counter = int(redis_store.get('state::counter') or '0')
        counter += 1
        print(counter)
        redis_store.set('state::counter', str(counter))

        # 檢查 sender 現在的狀態（回答問題、問問題或是提供反饋）
        # 方法是從暫存的 redis 裡頭取出關於目前這個 sender 的所有資訊
        user = UserStatus(sender)

        # 時間間隔太久，一律視為新詢問
        # tdelta = datetime.now() - user.get_last_active()
        # if tdelta.total_seconds() >= 300:
        #    user.set_status('new')
        # user.set_last_active(datetime.now())

        # 從送進來的 msg 分析, 作為 input
        parsed_msg, template_params = self.intention_detector.parse_msg(user, msgbody)

        # 執行到下一個 state
        self.state_machine.run(self.intention_bot, user, parsed_msg, **template_params)


    def handle_postback(self, msg, sender, payload):
        """ 處理 postback 的函式。 """
        p = re.match(r'([^:]*):(.*)', payload)
        if p is not None:
            payload = p.group(1)
            target = p.group(2)
        
            self.handle_message(msg, sender, {"postback": {"payload": payload, "target": target}})
        else:
            self.handle_message(msg, sender, {"postback": {"payload": payload}})




