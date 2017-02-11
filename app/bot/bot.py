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
        state = UserStatus(sender)

        # 時間間隔太久，一律視為新詢問
        tdelta = datetime.now() - state.get_last_active()
        if tdelta.total_seconds() >= 300:
            state.set_status('new')
        state.set_last_active(datetime.now())

        # 取得意圖
        intention_bot = self.intention_detector.get_intention_bot(sender, state, msgbody)

        # 處理意圖
        intention_bot.handle_message(msg, sender, state, msgbody)




