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
    def __init__(self, target=None):
        super().__init__()
        self.target = target

    def wiki_zh_to_en(self, s):
        """ 利用維基百科的頁面跳轉功能找到英文 """
        #""" 利用 google translate 中翻英 """
        #url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-TW&tl=en&dt=t&q=%s" %\
        #    (urllib.parse.quote(s))
        #response = urllib.request.urlopen(url)
        #html = response.read()
        #print(html)
        url = "https://zh.wikipedia.org/wiki/%s" % (urllib.parse.quote(s))
        try:
            page = get_page(url)
                
            soup = BeautifulSoup(page, 'lxml')
            en_link = soup.findAll('li', class_='interwiki-en')
            if len(en_link) == 0:
                return None
            p = en_link[0].a
            if p is None:
                return None
            en = p.get('href', None)
            if en is None:
                return None
            tr = en.split('/')[-1].lower().replace("_", " ")
            print("找到翻譯了... [%s] => %s" % (s, tr))
            return tr
        except Exception as e:
            print("Error: %s" % str(e))
            return None

    def zh_to_en(self, s):
        s = mafan.to_traditional(s.strip())
        q = Term.query.filter_by(chinese=s).order_by(Term.hit_counts.desc()).first()

        if q is None:
            tr = self.wiki_zh_to_en(s)
            return tr
        print("search DB: %s <=> %s [%d]" % (q.english, q.chinese, q.hit_counts or 0))
        return q.english

    def handle_message(self, msg, sender, state, msgbody):

        # 先標記處理的人是誰~
        state.set_last_handler_bot(self.__class__.__name__)

        payload = None
        if 'quick_reply' in msgbody and 'payload' in msgbody['quick_reply']:
            payload = msgbody['quick_reply']['payload']

        # 首先判斷是否為取消
        if payload == TMT_CANCEL:
            state.set_status('new')
            return

        # 判斷是否為「我要校正」的選項
        if payload == TMT_FIX_TRANSLATION:
            state.set_status(STATE_WAIT_FOR_FIX_ENGLISH)
            # TODO: Get Similars as quick replies
            self.bot_send_message(sender, { "text": "請輸入「%s」對應的正確英文～" % state.get_q() })
            return
        
        # 確認翻譯
        if payload == TMT_CONFIRM_TRANSLATION:
            q = Term.query.filter_by(english=state.get_english(), chinese=state.get_chinese()).first()
            if q is None:
                q = Term(english=state.get_english(), chinese=state.get_chinese(), hit_counts=1)
                db.session.add(q)
            else:
                q.hit_counts = (q.hit_counts+1 if q.hit_counts else 1)
            print("update DB: %s <=> %s [%d]" % (q.english, q.chinese, q.hit_counts or 0))
            db.session.commit()
            self.bot_send_message(sender, self.reply_gen.sticker('thank you'))
            return

        # 判斷是否為「更多」選項
        if payload == TMT_MORE:
            self.bot_send_message(sender, self.reply_gen.ask_more(state))
            return
            
        if state.get_status() == STATE_WAIT_FOR_FIX_ENGLISH:
            if 'text' in msgbody:
                state.set_status(STATE_ZhTw2En_IS_CALLED)
                msgtext = msgbody['text'].strip()
                state.set_english(msgtext.lower())
                self.bot_send_message(sender, self.reply_gen.translated_string("\"" + msgtext + "\" 這樣對嗎？"))
            else:
                state.set_status('new')
                self.bot_send_message(sender, { "text": "已取消 ：）" })
            return

        if 'text' in msgbody:
            msgtext = msgbody['text']
            # 如果已有 self.target, 那麼就用 target
            if self.target:
                msgtext = self.target

            state.set_status(STATE_En2ZhTw_IS_CALLED)
            state.set_q(msgtext)

            tr = self.zh_to_en(msgtext)
            if tr is None:
                self.bot_send_message(sender, { "text": "翻譯失敗" })
                return

            state.set_english(tr)
            state.set_chinese(msgtext.strip())
            self.bot_send_message(sender, self.reply_gen.translated_string(tr))
            
            q = Term.query.filter_by(chinese=msgtext.strip(), english=tr).first()
            if q is not None and q.photos.first() is not None:
                self.bot_send_message(sender, self.reply_gen.image(q.photos.first().url))
            return


        state.set_status('new')
        self.bot_send_message(sender, { "text": "很抱歉，這個功能林北還做不出來 ^_<" })
        return

        
