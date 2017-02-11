import json
import urllib.request
import urllib.parse
from app.models import db, Term 
from html.parser import HTMLParser
from google import search, get_page
from bs4 import BeautifulSoup
from datetime import datetime
from app.secrets import PAGE_TOKEN
from app.bot.constants import *
from app.bot.reply_generator import ReplyGenerator
from app.bot.intention_bot import IntentionBot


import enchant
import mafan
class ChineseToEnglishIntentionBot(IntentionBot):
    def __init__(self):
        super().__init__()


    def zh_to_en(self, s):
        s = mafan.to_traditional(s.strip())
        q = Term.query.filter_by(chinese=s).order_by(Term.hit_counts.desc()).first()

        if q is None:
            return None
        print("search DB: %s <=> %s [%d]" % (q.english, q.chinese, q.hit_counts))
        return q.english

    def handle_message(self, msg, sender, state, msgbody):

        # 先標記處理的人是誰~
        state.set_last_handler_bot(self.__class__.__name__)

        if 'text' in msgbody:
            s = msgbody['text']
            tr = self.zh_to_en(s)
            if tr is None:
                self.bot_send_message(sender, { "text": "翻譯失敗" })
                return
            self.bot_send_message(sender, self.reply_gen.translated_string(tr))
            return


        state.set_status('new')
        self.bot_send_message(sender, { "text": "很抱歉，這個功能林北還做不出來 ^_<" })
        return

        
